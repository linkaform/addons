#!/usr/bin/env python3
# coding: utf-8
"""workwith: elige la cuenta activa y deja modules/ en su rama.

Corre en el HOST, no dentro del contenedor: modules/ es un submodulo cuyo .git real vive
en ../.git/modules/modules, que no esta montado, asi que git no funciona ahi adentro.

No hace login ni toca la red, a proposito: tiene que servir justamente cuando las
credenciales activas estan rotas.

    ./lkf workwith <domain_name>
    ./lkf workwith            # muestra la cuenta actual y los dominios disponibles
"""
import configparser
import os
import subprocess
import sys

# El environment activo lo maneja workon.py (mismo directorio); aqui solo se muestra.
from workon import descripcion as descripcion_env, env_actual

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRETS = os.path.join(REPO, 'secrets')
ACCOUNTS = os.path.join(SECRETS, 'accounts.ini')
CURRENT = os.path.join(SECRETS, 'current_domain')
MODULES = os.path.join(REPO, 'modules')

SEC_GLOBAL = 'global'


class Error(Exception):
    pass


def git(*args, check=True):
    """git dentro de modules/. Devuelve stdout; lanza Error si falla y check."""
    res = subprocess.run(['git', '-C', MODULES] + list(args),
                         capture_output=True, text=True)
    if check and res.returncode != 0:
        raise Error('git %s fallo:\n%s' % (' '.join(args), (res.stderr or res.stdout).strip()))
    return res.stdout.strip()


def cargar_catalogo():
    if not os.path.exists(ACCOUNTS):
        raise Error('No existe el catalogo de cuentas: %s' % ACCOUNTS)
    # interpolation=None: los couch_user vienen url-encoded y el % rompe el interpolador
    cat = configparser.ConfigParser(interpolation=None)
    cat.read(ACCOUNTS, encoding='utf-8')
    return cat


def dominios(cat):
    return [s for s in cat.sections() if s != SEC_GLOBAL]


def dominio_actual():
    if os.path.exists(CURRENT):
        return open(CURRENT, encoding='utf-8').read().strip()
    return None


def rama_de(cat, domain):
    """La rama del dominio: branch_name si esta definido, si no el propio dominio."""
    return cat[domain].get('branch_name', '').strip() or domain


def exigir_rama_limpia():
    sucio = git('status', '--porcelain')
    if sucio:
        archivos = [l.strip() for l in sucio.splitlines() if l.strip()]
        msg = ['modules/ tiene %d cambio(s) sin commitear:' % len(archivos), '']
        msg += ['    ' + a for a in archivos[:15]]
        if len(archivos) > 15:
            msg.append('    ... y %d mas' % (len(archivos) - 15))
        msg += ['',
                'Cambiar de rama ahora arrastraria esos cambios a la rama de otra cuenta.',
                'Haz commit o guardalos antes:',
                '',
                '    cd modules && git stash        # los recuperas con: git stash pop',
                '    cd modules && git commit -am "..."']
        raise Error('\n'.join(msg))


def ir_a_rama(rama):
    """Cambia a la rama, creandola desde origin/<rama> si solo existe en el remoto."""
    actual = git('rev-parse', '--abbrev-ref', 'HEAD')
    if actual == rama:
        print('  rama          : %s (ya estabas ahi)' % rama)
        return
    locales = set(git('branch', '--format=%(refname:short)').split())
    remotas = {b.split('origin/', 1)[1] for b in git('branch', '-r', '--format=%(refname:short)').split()
               if b.startswith('origin/')}
    if rama in locales:
        git('checkout', rama)
    elif rama in remotas:
        git('checkout', '-b', rama, 'origin/' + rama)
        print('  (creada desde origin/%s)' % rama)
    else:
        raise Error('La rama "%s" no existe ni local ni en origin.\n\n'
                    'Si la cuenta todavia usa el nombre viejo, ponlo en su seccion del catalogo:\n'
                    '    branch_name = account_<id>\n\n'
                    'Ramas disponibles: %s' % (rama, ', '.join(sorted(locales | remotas))))
    print('  rama          : %s (antes %s)' % (rama, actual))


def merge_master():
    """Trae master conservando lo de la rama, y reporta que se resolvio a favor nuestro.

    Se hace un merge de prueba primero solo para saber que archivos habrian chocado: con
    -X ours esa informacion se pierde, y es justo lo que hay que revisar despues.
    """
    if not git('rev-parse', '--verify', '--quiet', 'origin/master', check=False):
        print('  master        : no existe origin/master, se omite')
        return []

    if not git('rev-list', '--count', 'HEAD..origin/master'):
        return []
    pendientes = int(git('rev-list', '--count', 'HEAD..origin/master') or 0)
    if pendientes == 0:
        print('  master        : ya estabas al dia')
        return []

    # Merge de prueba solo para saber que habria chocado: con -X ours esa lista se pierde.
    choques = []
    prueba = subprocess.run(['git', '-C', MODULES, 'merge', '--no-commit', '--no-ff', 'origin/master'],
                            capture_output=True, text=True)
    if prueba.returncode != 0:
        choques = [f for f in git('diff', '--name-only', '--diff-filter=U').splitlines() if f]
    git('merge', '--abort', check=False)

    subprocess.run(['git', '-C', MODULES, 'merge', '-X', 'ours', '--no-commit', '--no-ff',
                    'origin/master'], capture_output=True, text=True)
    # -X ours resuelve choques de contenido, pero NO los de arbol (modify/delete y
    # similares). Esos hay que cerrarlos a mano, tambien a favor de la rama.
    for f in [f for f in git('diff', '--name-only', '--diff-filter=U').splitlines() if f]:
        etapas = git('ls-files', '-u', '--', f)
        nuestra = any(l.split()[2] == '2' for l in etapas.splitlines() if len(l.split()) > 2)
        if nuestra:
            git('checkout', '--ours', '--', f)
            git('add', '--', f)
        else:
            git('rm', '--force', '--quiet', '--', f)   # la rama lo borro: sigue borrado

    if git('diff', '--name-only', '--diff-filter=U'):
        raise Error('Quedaron conflictos sin resolver en modules/. Resuelvelos a mano:\n'
                    '    cd modules && git status')
    git('commit', '--no-edit', '--quiet')
    print('  master        : %d commit(s) integrados' % pendientes)
    return choques


def mostrar_estado(cat):
    actual = dominio_actual()
    print('cuenta activa : %s' % (actual or '(ninguna)'))
    if actual and cat.has_section(actual):
        print('usuario       : %s' % cat[actual].get('username', '?'))
        print('rama esperada : %s' % rama_de(cat, actual))
    print('environment   : %s        (cambialo con: ./lkf workon <env>)'
          % descripcion_env(env_actual()))
    try:
        print('rama de modules: %s' % git('rev-parse', '--abbrev-ref', 'HEAD'))
    except Error:
        pass
    print('\ndominios disponibles (%d):' % len(dominios(cat)))
    disp = sorted(dominios(cat))
    for i in range(0, len(disp), 4):
        print('  ' + '  '.join('%-22s' % d for d in disp[i:i + 4]).rstrip())


def main(argv):
    cat = cargar_catalogo()

    if len(argv) < 2 or argv[1] in ('-h', '--help'):
        if len(argv) < 2:
            mostrar_estado(cat)
            return 0
        print(__doc__)
        return 0

    domain = argv[1].strip()
    if not cat.has_section(domain):
        sug = [d for d in dominios(cat) if domain.lower() in d.lower()]
        msg = 'El dominio "%s" no esta en %s.' % (domain, ACCOUNTS)
        if sug:
            msg += '\n\n¿Quisiste decir?  %s' % ', '.join(sug)
        msg += '\n\nCorre  ./lkf workwith  para ver todos.'
        raise Error(msg)
    if domain == SEC_GLOBAL:
        raise Error('"%s" es la seccion de secretos compartidos, no una cuenta.' % SEC_GLOBAL)

    rama = rama_de(cat, domain)
    print('workwith %s' % domain)
    print('  usuario       : %s' % cat[domain].get('username', '?'))
    print('  environment   : %s' % descripcion_env(env_actual()))

    exigir_rama_limpia()
    git('fetch', 'origin', '--quiet')
    ir_a_rama(rama)
    choques = merge_master()

    # El puntero se escribe al final: si git falla, la cuenta activa no cambia y no
    # quedas con las credenciales de una cuenta y la rama de otra.
    with open(CURRENT, 'w', encoding='utf-8') as fh:
        fh.write(domain + '\n')
    os.chmod(CURRENT, 0o600)
    print('  cuenta activa : %s' % domain)

    if choques:
        print('\n  %d archivo(s) resueltos a favor de tu rama (se descarto lo de master):'
              % len(choques))
        for f in choques:
            print('     %s' % f)
        print('  revisalos si master traia algo que te sirva.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv))
    except Error as e:
        print('\n%s\n%s\n%s' % ('=' * 60, e, '=' * 60), file=sys.stderr)
        sys.exit(1)
