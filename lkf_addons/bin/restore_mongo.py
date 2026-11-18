#!/usr/bin/env python3
# coding: utf-8
"""restore_mongo: copia la base de una cuenta de PRODUCCION a tu sandbox (sbx-*).

Corre DENTRO del contenedor lkf-addons (ya trae mongodump/mongorestore y pymongo); desde
el host se invoca con `./lkf restore-mongo`, que solo hace el `docker exec`.

De donde sale cada dato:
  - Destino:   el environment activo de `./lkf workon` (secrets/current_env o LKF_ENV).
               Solo sandboxes: nunca prod, preprod ni local.
  - Cuenta:    el argumento, o el account_id de la cuenta activa de `./lkf workwith`.
  - Clave:     el back la entrega por apikey (GET /api/infosync/user_admin/mongodb_pwd/),
               igual que linkaform_api.network.get_mongo_password. Se pide a produccion
               para el origen y al propio sandbox para el destino. El usuario de mongo es
               account_<id>: una credencial POR CUENTA, que alcanza
               infosync_answers_client_<id> pero no la base `admin`.
  - apikey:    [<cuenta>] de secrets/accounts.ini (username + apikey).

    ./lkf restore-mongo --check      # solo pide claves y hace ping; no borra nada
    ./lkf restore-mongo --dry-run    # muestra el plan sin llamar a nadie
    ./lkf restore-mongo [account_id]

Pasos: verifica origen y destino -> eliges collections -> BORRA la base en el sandbox ->
mongodump | mongorestore.

Collections: por defecto se omiten las pesadas (answer_version, form_answer_archived, Tableau,
download_history, pacos, report_answer). Con terminal interactiva se abre un menu para
marcar/desmarcar cada una (se muestran con su tamano); tu ultima seleccion se recuerda por
cuenta en secrets/restore_mongo.json (local, no se versiona). Sin menu:

    --exclude a,b     omite esas collections          --include c   restaura c aunque este
    --no-menu / -y    no preguntar: usa flags > ultima seleccion > defaults

--with-admin copia ademas la base `admin` de produccion (usuarios y permisos). Eso exige
una credencial administrativa que el endpoint no entrega: ponla en accounts.ini como
mongo_user / mongo_password (en [global] o en la cuenta). Solo hace falta para el primer
setup de un sandbox, cuando aun no existen los usuarios account_<id>.
"""
import argparse
import configparser
import json
import os
import subprocess
import sys
import tempfile
from urllib.parse import quote

import requests

SECRETS_CANDIDATES = (
    os.environ.get('LKF_SECRETS', ''),
    '/srv/scripts/addons/secrets',  # dentro del contenedor lkf-addons
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'secrets'),
)
PROD_URL = 'https://app.linkaform.com'
PROD_MONGO = 'db3.linkaform.com:27017'
PWD_PATH = '/api/infosync/user_admin/mongodb_pwd/'
EXCLUDED = ('answer_version', 'form_answer_archived', 'Tableau',
            'download_history', 'pacos', 'report_answer')


class Error(Exception):
    pass


def secrets_dir():
    for d in SECRETS_CANDIDATES:
        if d and os.path.exists(os.path.join(d, 'accounts.ini')):
            return os.path.abspath(d)
    raise Error('No encuentro secrets/accounts.ini (busque en: %s).'
                % ', '.join(d for d in SECRETS_CANDIDATES if d))


def leer(path):
    return open(path, encoding='utf-8').read().strip() if os.path.exists(path) else ''


def valor(cat, domain, key):
    if domain and cat.has_option(domain, key):
        return cat.get(domain, key).strip()
    if cat.has_option('global', key):
        return cat.get('global', key).strip()
    return ''


def pedir_clave(base_url, username, apikey, etiqueta):
    """La clave de mongo de la cuenta, segun el back de `base_url`."""
    url = base_url + PWD_PATH
    try:
        r = requests.get(url, timeout=20, headers={
            'Content-type': 'application/json',
            'Authorization': 'ApiKey {}:{}'.format(username, apikey)})
    except requests.RequestException as e:
        raise Error('%s: no pude contactar %s\n%s' % (etiqueta, url, e))
    # linkaform_api espera 201; se acepta 200 por si el back lo normaliza.
    if r.status_code not in (200, 201):
        raise Error('%s: %s respondio %s (se esperaba 201).\n'
                    'Si es 401/403 revisa username/apikey en accounts.ini; si es 404, ese '
                    'ambiente no expone el endpoint.' % (etiqueta, url, r.status_code))
    try:
        pwd = r.json()['mongo_password']
    except (ValueError, KeyError):
        raise Error('%s: la respuesta de %s no trae mongo_password.' % (etiqueta, url))
    return pwd


def resolver(args):
    secrets = secrets_dir()
    env = os.environ.get('LKF_ENV', '').strip() or leer(os.path.join(secrets, 'current_env'))
    if not env.startswith('sbx-'):
        raise Error(
            'El environment activo es "%s" y restore-mongo solo restaura en sandboxes '
            '(sbx-*).\nEsto BORRA la base de destino; por eso nunca apunta a prod, preprod '
            'ni local.\n\nElige tu sandbox con:  ./lkf workon sbx-<nombre>' % (env or '(ninguno)'))

    cat = configparser.ConfigParser(interpolation=None)
    cat.read(os.path.join(secrets, 'accounts.ini'), encoding='utf-8')
    domain = leer(os.path.join(secrets, 'current_domain'))
    if not domain or not cat.has_section(domain):
        raise Error('No hay cuenta activa valida (current_domain="%s").\n'
                    'Elige una con:  ./lkf workwith <dominio>' % domain)

    account_id = (args.account_id or '').strip() or valor(cat, domain, 'account_id')
    if not account_id.isdigit():
        raise Error('No se de que cuenta copiar (account_id="%s").\n'
                    'Pasa el id:  ./lkf restore-mongo <account_id>\n'
                    'o agrega account_id a [%s] en accounts.ini.' % (account_id, domain))

    username = valor(cat, domain, 'username')
    apikey = valor(cat, domain, 'apikey')
    if not username or not apikey:
        raise Error('Faltan username / apikey en [%s] de accounts.ini.' % domain)

    admin = None
    if args.with_admin:
        au, ap = valor(cat, domain, 'mongo_user'), valor(cat, domain, 'mongo_password')
        if not au or not ap:
            raise Error('--with-admin necesita mongo_user / mongo_password en accounts.ini '
                        '(credencial administrativa; el endpoint no la entrega).')
        admin = (au, ap)

    return {
        'env': env, 'domain': domain, 'account_id': account_id,
        'username': username, 'apikey': apikey,
        'db': 'infosync_answers_client_%s' % account_id,
        'user': 'account_%s' % account_id,
        'src_url': PROD_URL, 'src_mongo': args.source,
        'dst_url': 'https://%s.linkaform.com' % env,
        'dst_mongo': '%s.linkaform.com:27017' % env,
        'admin': admin,
        'secrets': secrets,
        'prefs': cargar_prefs(secrets, account_id),
        'include': lista(args.include),
        'exclude': lista(args.exclude),
    }


def uri(user, pwd, host, db):
    return 'mongodb://%s:%s@%s/%s?authSource=%s' % (quote(user, safe=''), quote(pwd, safe=''),
                                                    host, db, db)


def verificar(host, user, pwd, db, etiqueta):
    """Autentica de verdad: listar colecciones exige credenciales validas."""
    from pymongo import MongoClient
    from pymongo.errors import PyMongoError
    try:
        c = MongoClient(uri(user, pwd, host, db), serverSelectionTimeoutMS=10000)
        n = len(c[db].list_collection_names())
        c.close()
    except PyMongoError as e:
        raise Error('%s: no pude autenticar %s en %s\n%s' % (etiqueta, user, host, e))
    return n


def archivo_config(pwd):
    """Config de las database-tools con la clave fuera del argv (se veria en `ps`)."""
    fd, path = tempfile.mkstemp(prefix='lkf-mongo-', suffix='.yml')
    with os.fdopen(fd, 'w', encoding='utf-8') as fh:
        fh.write('password: %s\n' % json.dumps(pwd))  # escalar YAML valido
    os.chmod(path, 0o600)
    return path


def copiar(src, dst, db, extra, etiqueta, authdb):
    """mongodump (origen) | mongorestore (destino); revisa el codigo de ambos."""
    (s_host, s_user, s_cfg), (d_host, d_user, d_cfg) = src, dst
    dump = ['mongodump', '--host', s_host, '-u', s_user, '--config', s_cfg,
            '--authenticationDatabase', authdb, '--db', db, '--archive'] + extra
    rest = ['mongorestore', '--host', d_host, '-u', d_user, '--config', d_cfg,
            '--authenticationDatabase', authdb, '--archive']
    print('  %s ...' % etiqueta, flush=True)
    p_dump = subprocess.Popen(dump, stdout=subprocess.PIPE)
    p_rest = subprocess.Popen(rest, stdin=p_dump.stdout)
    p_dump.stdout.close()
    rc_rest, rc_dump = p_rest.wait(), p_dump.wait()
    if rc_dump or rc_rest:
        raise Error('%s fallo (mongodump=%s, mongorestore=%s).' % (etiqueta, rc_dump, rc_rest))


PREFS_FILE = 'restore_mongo.json'


def lista(valores):
    """['a,b', 'c'] -> ['a', 'b', 'c']"""
    return [x.strip() for v in (valores or []) for x in v.split(',') if x.strip()]


def cargar_prefs(secrets, account_id):
    try:
        with open(os.path.join(secrets, PREFS_FILE), encoding='utf-8') as fh:
            return json.load(fh).get(str(account_id), {})
    except (OSError, ValueError):
        return {}


def guardar_prefs(secrets, account_id, excluded, known):
    path = os.path.join(secrets, PREFS_FILE)
    try:
        with open(path, encoding='utf-8') as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        data = {}
    data[str(account_id)] = {'excluded': sorted(excluded), 'known': sorted(known)}
    try:
        with open(path, 'w', encoding='utf-8') as fh:
            json.dump(data, fh, indent=2, sort_keys=True)
            fh.write('\n')
    except OSError as e:
        print('  (no pude guardar tu seleccion en %s: %s)' % (path, e))


def exclusion_base(p):
    """Exclusion de partida, sin red: ultima seleccion guardada o defaults; luego flags."""
    prefs = p['prefs']
    excluded = set(prefs['excluded']) if 'excluded' in prefs else set(EXCLUDED)
    excluded |= set(p['exclude'])
    excluded -= set(p['include'])
    return excluded


def fmt_size(n):
    if n is None:
        return '?'
    for unit in ('B', 'KB', 'MB', 'GB'):
        if n < 1024 or unit == 'GB':
            return '%.1f%s' % (n, unit) if unit != 'B' else '%d%s' % (n, unit)
        n /= 1024.0


def listar_collections(host, user, pwd, db):
    """[(nombre, bytes|None)] ordenado por nombre. Si no hay permiso de stats, bytes=None."""
    from pymongo import MongoClient
    from pymongo.errors import PyMongoError
    try:
        c = MongoClient(uri(user, pwd, host, db), serverSelectionTimeoutMS=10000)
        out = []
        for name in sorted(c[db].list_collection_names()):
            try:
                size = c[db].command('collStats', name).get('size')
            except PyMongoError:
                size = None
            out.append((name, size))
        c.close()
    except PyMongoError as e:
        raise Error('No pude listar las collections de %s: %s' % (db, e))
    return out


def parse_seleccion(texto, total):
    """'1 3-5' -> {1,3,4,5}; None si algo no se entiende."""
    idx = set()
    for tok in texto.replace(',', ' ').split():
        try:
            if '-' in tok:
                a, b = tok.split('-', 1)
                a, b = int(a), int(b)
                rango = range(min(a, b), max(a, b) + 1)
            else:
                rango = [int(tok)]
        except ValueError:
            return None
        if any(i < 1 or i > total for i in rango):
            return None
        idx.update(rango)
    return idx


def menu_collections(db, colls, excluded):
    """Menu de texto. Marcadas = se restauran. Devuelve el set excluido, o None si cancela."""
    nombres = [n for n, _ in colls]
    marcadas = {n for n in nombres if n not in excluded}
    defaults = {n for n in nombres if n not in EXCLUDED}
    ancho = max([len(n) for n in nombres] + [10])
    while True:
        print('\nCollections de %s   [x] se restaura   [ ] se omite\n' % db)
        for i, (n, size) in enumerate(colls, 1):
            print('  %3d  [%s] %-*s  %s' % (i, 'x' if n in marcadas else ' ', ancho, n,
                                           fmt_size(size)))
        total = sum(s or 0 for n, s in colls if n in marcadas)
        print('\n  %d de %d marcadas, ~%s a copiar' % (len(marcadas), len(nombres),
                                                      fmt_size(total)))
        print('  numero o rango (3 5-7) alterna | a todas | n ninguna | d defaults | '
              'Enter confirma | q cancela')
        resp = input('> ').strip().lower()
        if resp == '':
            if not marcadas:
                print('  Desmarcaste todo: no habria nada que restaurar.')
                continue
            return set(nombres) - marcadas
        if resp == 'q':
            return None
        if resp == 'a':
            marcadas = set(nombres)
        elif resp == 'n':
            marcadas = set()
        elif resp == 'd':
            marcadas = set(defaults)
        else:
            sel = parse_seleccion(resp, len(nombres))
            if sel is None:
                print('  No entendi "%s".' % resp)
                continue
            for i in sel:
                marcadas ^= {nombres[i - 1]}


def main(argv):
    ap = argparse.ArgumentParser(prog='lkf restore-mongo')
    ap.add_argument('account_id', nargs='?', help='cuenta a copiar (default: la de workwith)')
    ap.add_argument('--source', default=PROD_MONGO,
                    help='mongo de produccion de origen (default: %s)' % PROD_MONGO)
    ap.add_argument('--with-admin', action='store_true',
                    help='copia tambien la base admin (requiere mongo_user/mongo_password)')
    ap.add_argument('--exclude', action='append', metavar='COL[,COL]',
                    help='omite estas collections (repetible)')
    ap.add_argument('--include', action='append', metavar='COL[,COL]',
                    help='restaura estas collections aunque esten excluidas (repetible)')
    ap.add_argument('--no-menu', action='store_true',
                    help='no abrir el menu de collections (usa flags > ultima seleccion > defaults)')
    ap.add_argument('--check', action='store_true',
                    help='pide las claves y hace ping a origen y destino; no borra nada')
    ap.add_argument('--dry-run', action='store_true', help='solo muestra el plan, sin red')
    ap.add_argument('-y', '--yes', action='store_true', help='no pedir confirmacion')
    args = ap.parse_args(argv[1:])

    p = resolver(args)
    print('restore-mongo')
    print('  origen   : %s  (produccion, %s)' % (p['src_mongo'], p['src_url']))
    print('  destino  : %s  (environment %s)' % (p['dst_mongo'], p['env']))
    print('  usuario  : %s  (clave por apikey de [%s])' % (p['user'], p['domain']))
    print('  base     : %s  (se BORRA en el destino y se restaura)' % p['db'])
    print('  admin    : %s' % ('se copia (credencial de accounts.ini)' if p['admin']
                              else 'no se copia'))
    print('  omite    : %s' % (', '.join(sorted(exclusion_base(p))) or '(nada)'))
    if args.dry_run:
        print('  (el menu de collections se abre al correr de verdad, no en dry-run)')
        print('\n(dry-run: no se llamo a nadie ni se toco nada)')
        return 0

    print('\n1/4 pidiendo claves al back y verificando conexion')
    src_pwd = pedir_clave(p['src_url'], p['username'], p['apikey'], 'origen')
    n = verificar(p['src_mongo'], p['user'], src_pwd, p['db'], 'origen')
    print('  origen  OK  (%d colecciones en %s)' % (n, p['db']))
    dst_pwd = pedir_clave(p['dst_url'], p['username'], p['apikey'], 'destino')
    n = verificar(p['dst_mongo'], p['user'], dst_pwd, p['db'], 'destino')
    print('  destino OK  (%d colecciones en %s)' % (n, p['db']))

    print('\n  listando collections de %s ...' % p['db'])
    colls = listar_collections(p['src_mongo'], p['user'], src_pwd, p['db'])
    nombres = {n for n, _ in colls}
    desconocidas = (set(p['include']) | set(p['exclude'])) - nombres
    if desconocidas:
        print('  (no existen en el origen y se ignoran: %s)' % ', '.join(sorted(desconocidas)))
    excluded = exclusion_base(p) & nombres
    nuevas = nombres - set(p['prefs'].get('known', nombres))
    if nuevas:
        print('  (collections nuevas desde tu ultima seleccion, quedan marcadas: %s)'
              % ', '.join(sorted(nuevas)))
    interactivo = sys.stdin.isatty() and not args.yes and not args.no_menu
    if interactivo:
        elegido = menu_collections(p['db'], colls, excluded)
        if elegido is None:
            print('Cancelado.')
            return 1
        excluded = elegido
        if not args.check:
            guardar_prefs(p['secrets'], p['account_id'], excluded, nombres)
    if len(excluded) >= len(nombres):
        raise Error('No queda ninguna collection por restaurar.')
    incluidas = [(n, sz) for n, sz in colls if n not in excluded]
    print('\n  se restauran %d collections (~%s); se omiten: %s'
          % (len(incluidas), fmt_size(sum(sz or 0 for _, sz in incluidas)),
             ', '.join(sorted(excluded)) or '(ninguna)'))
    if args.check:
        print('\n(check: todo responde; no se toco nada ni se guardo la seleccion)')
        return 0

    if not args.yes:
        resp = input('\nEscribe el nombre del environment (%s) para continuar: ' % p['env'])
        if resp.strip() != p['env']:
            print('Cancelado.')
            return 1

    cfgs = []
    try:
        s_cfg, d_cfg = archivo_config(src_pwd), archivo_config(dst_pwd)
        cfgs += [s_cfg, d_cfg]

        print('2/4 borrando %s en %s' % (p['db'], p['dst_mongo']))
        from pymongo import MongoClient
        from pymongo.errors import PyMongoError
        try:
            c = MongoClient(uri(p['user'], dst_pwd, p['dst_mongo'], p['db']),
                            serverSelectionTimeoutMS=10000)
            c.drop_database(p['db'])
            c.close()
        except PyMongoError as e:
            raise Error('No pude borrar %s: %s\n(Si es "not authorized", %s no tiene '
                        'permiso dropDatabase en el sandbox.)' % (p['db'], e, p['user']))

        print('3/4 restaurando %s' % p['db'])
        copiar((p['src_mongo'], p['user'], s_cfg), (p['dst_mongo'], p['user'], d_cfg), p['db'],
               ['--excludeCollection=%s' % c for c in sorted(excluded)], p['db'], p['db'])

        if p['admin']:
            print('4/4 copiando la base admin')
            au, apw = p['admin']
            a_cfg = archivo_config(apw)
            cfgs.append(a_cfg)
            copiar((p['src_mongo'], au, a_cfg), (p['dst_mongo'], au, a_cfg), 'admin', [],
                   'admin', 'admin')
        else:
            print('4/4 base admin: omitida (usa --with-admin para copiarla)')
    finally:
        for path in cfgs:
            try:
                os.remove(path)
            except OSError:
                pass

    print('\nListo: %s restaurada en %s' % (p['db'], p['dst_mongo']))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv))
    except Error as e:
        print('\n%s\n%s\n%s' % ('=' * 60, e, '=' * 60), file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print('\nInterrumpido.', file=sys.stderr)
        sys.exit(130)
