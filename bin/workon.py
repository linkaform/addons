#!/usr/bin/env python3
# coding: utf-8
"""workon: elige el environment activo (local | preprod | prod).

El puntero vive en secrets/current_env, igual que la cuenta activa vive en
secrets/current_domain. config/enviorment.py lo lee al arrancar, asi que cambiar de
environment ya no requiere editar codigo ni reconstruir nada: basta correr esto y
volver a lanzar el script.

    ./lkf workon <local|preprod|prod>
    ./lkf workon            # muestra el environment actual y los disponibles

La variable de entorno LKF_ENV, si esta puesta, gana sobre el archivo. Sirve para un
comando suelto contra otro environment sin mover el estado guardado:

    LKF_ENV=preprod lkfaddons.py install -m accesos -i scripts
"""
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRETS = os.path.join(REPO, 'secrets')
CURRENT_ENV = os.path.join(SECRETS, 'current_env')

ENVS = ('local', 'preprod', 'prod')
# Si el puntero falta o trae basura se cae aqui, nunca en prod.
DEFAULT_ENV = 'local'

# Solo para mostrar a donde apunta cada environment. La configuracion de verdad la
# arma config/enviorment.py; si cambias un HOST alla, actualizalo aqui tambien.
DESTINOS = {
    'local': '192.168.1.25:8000',
    'preprod': 'preprod.linkaform.com',
    'prod': 'app.linkaform.com',
}


class Error(Exception):
    pass


def env_actual():
    """El environment activo. LKF_ENV gana sobre el archivo; el default es local."""
    env = os.environ.get('LKF_ENV', '').strip()
    if not env and os.path.exists(CURRENT_ENV):
        env = open(CURRENT_ENV, encoding='utf-8').read().strip()
    return env if env in ENVS else DEFAULT_ENV


def env_es_override():
    """True si el environment viene de LKF_ENV y no del archivo."""
    return os.environ.get('LKF_ENV', '').strip() in ENVS


def descripcion(env):
    return '%-8s -> %s' % (env, DESTINOS.get(env, '?'))


def mostrar_estado():
    actual = env_actual()
    print('environment   : %s' % descripcion(actual))
    if env_es_override():
        print('                (viene de LKF_ENV, el archivo dice "%s")'
              % (open(CURRENT_ENV, encoding='utf-8').read().strip()
                 if os.path.exists(CURRENT_ENV) else '(nada)'))
    print('\nenvironments disponibles:')
    for env in ENVS:
        marca = '*' if env == actual else ' '
        print('  %s %s' % (marca, descripcion(env)))


def main(argv):
    if len(argv) < 2:
        mostrar_estado()
        return 0
    if argv[1] in ('-h', '--help'):
        print(__doc__)
        return 0

    env = argv[1].strip().lower()
    if env not in ENVS:
        raise Error('Environment "%s" invalido.\n\nValidos: %s'
                    % (env, ', '.join(ENVS)))

    anterior = env_actual()
    if not os.path.isdir(SECRETS):
        raise Error('No existe %s' % SECRETS)
    with open(CURRENT_ENV, 'w', encoding='utf-8') as fh:
        fh.write(env + '\n')
    os.chmod(CURRENT_ENV, 0o600)

    print('workon %s' % env)
    print('  environment   : %s' % descripcion(env))
    if anterior != env:
        print('  (antes %s)' % anterior)

    if env == 'prod':
        print('\n%s' % ('=' * 60))
        print('OJO: prod es la base de datos real de %s.' % DESTINOS['prod'])
        print('Lo que escribas aqui lo ven los clientes. Vuelve con:')
        print('\n    ./lkf workon local\n')
        print('=' * 60)

    if env_es_override():
        print('\n  LKF_ENV=%s esta puesta en tu shell y gana sobre este archivo.'
              % os.environ['LKF_ENV'].strip())
        print('  Quitala con:  unset LKF_ENV')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv))
    except Error as e:
        print('\n%s\n%s\n%s' % ('=' * 60, e, '=' * 60), file=sys.stderr)
        sys.exit(1)
