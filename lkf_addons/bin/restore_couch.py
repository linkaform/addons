#!/usr/bin/env python3
# coding: utf-8
"""restore_couch: replica las bases CouchDB de una cuenta de PRODUCCION a tu sandbox (sbx-*).

Corre DENTRO del contenedor lkf-addons; desde el host se invoca con `./lkf restore-couch`,
que solo hace el `docker exec`. Reemplaza al viejo replicate_db_to_cdb.py (sin secretos en
codigo: todo sale de secrets/accounts.ini).

De donde sale cada dato:
  - Destino:  el environment activo de `./lkf workon` (secrets/current_env o LKF_ENV).
              Solo sandboxes: nunca prod, preprod ni local. Host: <env>-couchdb.linkaform.com
  - Cuenta:   el argumento, o el account_id de la cuenta activa de `./lkf workwith`.
  - Origen:   couch_user / couch_password   (cuenta primero, luego [global]) -> produccion
  - Destino:  couch_dev_admin_user / couch_dev_admin_password (idem)         -> sandbox
              Debe ser SERVER ADMIN del couch del sandbox: borrar bases y create_target lo exigen.
              Los usuarios vienen URL-encoded en el ini (user%40dominio.com); se decodifican.

    ./lkf restore-couch --check      # solo prueba credenciales en ambos couch
    ./lkf restore-couch --dry-run    # muestra el plan (lee prod, no escribe nada)
    ./lkf restore-couch [account_id] [--with-imagenes]

Bases de la cuenta: account_properties_<id>, client_<id>_catalog_model, catalog_records_<cid>
por cada catalogo con individual_share y user_inbox_<uid> y clave_<uid> por cada
doc user_properties_<uid> de account_properties. `imagenes` solo con --with-imagenes (es grande).

Cada base: se BORRA en el sandbox y se replica con POST /_replicate al couch del sandbox.
"""
import argparse
import base64
import configparser
import os
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote, unquote

import requests

SECRETS_CANDIDATES = (
    os.environ.get('LKF_SECRETS', ''),
    '/srv/scripts/addons/secrets',  # dentro del contenedor lkf-addons
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'secrets'),
)
PROD_COUCH = 'https://couchdb.linkaform.com'
WORKERS = 30  # bases replicando a la vez en el sandbox
_print_lock = threading.Lock()


def say(msg):
    with _print_lock:
        print(msg, flush=True)


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


def basic(user, pwd):
    return 'Basic ' + base64.b64encode(('%s:%s' % (user, pwd)).encode()).decode()


def resolver(args):
    secrets = secrets_dir()
    env = os.environ.get('LKF_ENV', '').strip() or leer(os.path.join(secrets, 'current_env'))
    if not env.startswith('sbx-'):
        raise Error(
            'El environment activo es "%s" y restore-couch solo restaura en sandboxes '
            '(sbx-*).\nEsto BORRA las bases de destino; por eso nunca apunta a prod, preprod '
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
                    'Pasa el id:  ./lkf restore-couch <account_id>\n'
                    'o agrega account_id a [%s] en accounts.ini.' % (account_id, domain))

    creds = {}
    for etiqueta, ku, kp in (('origen', 'couch_user', 'couch_password'),
                             ('destino', 'couch_dev_admin_user', 'couch_dev_admin_password')):
        u, p = valor(cat, domain, ku), valor(cat, domain, kp)
        if not u or not p:
            raise Error('Faltan %s / %s en accounts.ini ([%s] o [global]) para el %s.\n(el destino necesita un server admin del couch del sandbox)'
                        % (ku, kp, domain, etiqueta))
        creds[etiqueta] = (unquote(u), p)

    return {
        'env': env, 'domain': domain, 'account_id': account_id,
        'src': args.source.rstrip('/'), 'src_auth': creds['origen'],
        'dst': 'https://%s-couchdb.linkaform.com' % env, 'dst_auth': creds['destino'],
    }


def http(method, base, auth, path, etiqueta, ok=(200, 201, 202), **kw):
    url = base + path
    try:
        r = requests.request(method, url, auth=auth, timeout=kw.pop('timeout', 30), **kw)
    except requests.RequestException as e:
        raise Error('%s: no pude contactar %s\n%s' % (etiqueta, base, e))
    if r.status_code not in ok:
        raise Error('%s: %s %s respondio %s: %s\nSi es 401/403 revisa las credenciales couch_* '
                    'de accounts.ini.' % (etiqueta, method, path, r.status_code, r.text[:300]))
    return r


def verificar(base, auth, etiqueta, admin=False):
    r = http('GET', base, auth, '/_session', etiqueta)
    name = (r.json().get('userCtx') or {}).get('name')
    if not name:
        raise Error('%s: %s no autentico (userCtx.name vacio).' % (etiqueta, base))
    if admin and '_admin' not in (r.json().get('userCtx') or {}).get('roles', []):
        raise Error('%s: %s autentica pero NO es server admin en %s; no podra borrar ni crear '
                    'bases.\nPon un admin del couch en couch_dev_admin_user / '
                    'couch_dev_admin_password de accounts.ini.' % (etiqueta, name, base))
    return name


def descubrir(p):
    """Lista de bases de la cuenta, leyendo account_properties_<id> en produccion."""
    base = 'account_properties_%s' % p['account_id']
    r = http('GET', p['src'], p['src_auth'], '/%s/_all_docs?include_docs=true' % quote(base, safe=''),
             'origen', timeout=120)
    catalogs, users = [], []
    for row in r.json().get('rows', []):
        m = re.match(r'^user_properties_(\d+)$', row['id'])
        if m:
            users.append(m.group(1))
        # `catalogs` llega como lista de dicts, como dict o vacio; en la lista hay basura (str).
        cats = (row.get('doc') or {}).get('catalogs')
        if isinstance(cats, dict):
            cats = [cats]
        for cat in cats if isinstance(cats, list) else []:
            if not isinstance(cat, dict):
                continue
            for name, data in cat.items():
                if isinstance(data, dict) and 'individual_share' in data and name not in catalogs:
                    catalogs.append(name)
    dbs = [base, 'client_%s_catalog_model' % p['account_id']]
    dbs += [c if c.startswith('catalog_records_') else 'catalog_records_%s' % c for c in catalogs]
    dbs += ['user_inbox_%s' % u for u in users]
    dbs += ['clave_%s' % u for u in users]  # si no existe en origen, replicar() la omite
    return dbs


def replicar(p, db):
    """Devuelve 'ok', 'omitida' (sin permiso o sin base en origen) o 'fallo'."""
    q = quote(db, safe='')
    try:
        st = http('GET', p['src'], p['src_auth'], '/' + q, 'origen', ok=(200, 403, 404)).status_code
        if st in (403, 404):
            say('  - %s: %s en origen, se omite (el sandbox no se toca)'
                % (db, 'sin permiso (403)' if st == 403 else 'no existe'))
            return 'omitida'
        http('DELETE', p['dst'], p['dst_auth'], '/' + q, 'destino', ok=(200, 202, 404))
        body = {
            'source': {'url': '%s/%s' % (p['src'], q),
                       'headers': {'Authorization': basic(*p['src_auth'])}},
            'target': {'url': '%s/%s' % (p['dst'], q),
                       'headers': {'Authorization': basic(*p['dst_auth'])}},
            'create_target': True, 'continuous': False,
        }
        res = http('POST', p['dst'], p['dst_auth'], '/_replicate', 'replicacion', json=body,
                   timeout=3600).json()
    except Error as e:
        say('  ! %s: %s' % (db, str(e).splitlines()[0]))
        return 'fallo'
    h = (res.get('history') or [{}])[0]
    fallos = h.get('doc_write_failures', 0)
    say('  %s %s: %s docs escritos, %s fallos' % ('!' if fallos else '+', db,
                                                  h.get('docs_written', '?'), fallos))
    return 'fallo' if fallos else 'ok'


def main(argv):
    ap = argparse.ArgumentParser(prog='lkf restore-couch')
    ap.add_argument('account_id', nargs='?', help='cuenta a copiar (default: la de workwith)')
    ap.add_argument('--source', default=PROD_COUCH,
                    help='couch de produccion de origen (default: %s)' % PROD_COUCH)
    ap.add_argument('--with-imagenes', action='store_true', help='replica tambien la base imagenes')
    ap.add_argument('--check', action='store_true', help='solo prueba credenciales en ambos couch')
    ap.add_argument('--dry-run', action='store_true', help='muestra el plan; no escribe nada')
    ap.add_argument('--workers', type=int, default=WORKERS,
                    help='bases replicando a la vez (default: %d)' % WORKERS)
    ap.add_argument('-y', '--yes', action='store_true', help='no pedir confirmacion')
    args = ap.parse_args(argv[1:])

    p = resolver(args)
    print('restore-couch')
    print('  origen  : %s  (produccion)' % p['src'])
    print('  destino : %s  (environment %s)' % (p['dst'], p['env']))
    print('  cuenta  : %s  (%s)' % (p['account_id'], p['domain']))

    print('\n1/3 verificando credenciales')
    print('  origen  OK  (usuario %s)' % verificar(p['src'], p['src_auth'], 'origen'))
    print('  destino OK  (usuario %s)' % verificar(p['dst'], p['dst_auth'], 'destino', admin=True))
    if args.check:
        print('\n(check: todo responde; no se toco nada)')
        return 0

    print('\n2/3 descubriendo bases de la cuenta en produccion')
    dbs = descubrir(p)
    if args.with_imagenes:
        dbs.append('imagenes')
    for db in dbs:
        print('  -', db)
    if args.dry_run:
        print('\n(dry-run: %d bases; no se escribio nada)' % len(dbs))
        return 0

    if not args.yes:
        resp = input('\nSe BORRAN y replican %d bases en %s.\n'
                     'Escribe el nombre del environment (%s) para continuar: '
                     % (len(dbs), p['dst'], p['env']))
        if resp.strip() != p['env']:
            print('Cancelado.')
            return 1

    print('\n3/3 replicando (%d a la vez)' % max(1, args.workers))
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as ex:
        res = list(zip(dbs, ex.map(lambda db: replicar(p, db), dbs)))
    omitidas = [db for db, r in res if r == 'omitida']
    fallidas = [db for db, r in res if r == 'fallo']
    if omitidas:
        print('\nOmitidas (%d, sin permiso o inexistentes en origen): %s'
              % (len(omitidas), ', '.join(omitidas)))
    if fallidas:
        raise Error('Replicacion con fallos en: %s' % ', '.join(fallidas))
    print('\nListo: %d bases replicadas, %d omitidas, en %s'
          % (len(dbs) - len(omitidas), len(omitidas), p['dst']))
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
