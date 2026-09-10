# coding: utf-8
"""Configuracion del mini-back. Todo sale de variables de entorno.

La tabla completa de variables esta en miniback/README.md.
"""

import configparser
import os

# --- destinos -----------------------------------------------------------
# Un script se corre en el contenedor que le toca segun su nombre. Los dos
# destinos difieren en el contenedor, en donde viven los modulos y en el
# entorno que necesita el interprete.

# Sufijo que manda un script al contenedor de la app Sanic.
SDK_SUFFIX = '_sdk.py'

ADDONS = {
    'name': 'addons',
    'container': os.environ.get('LKF_ADDONS_CONTAINER', 'lkf-addons'),
    'modules_path': os.environ.get('LKF_MODULES_PATH', '/srv/scripts/addons/modules'),
    'env': {},
}

# Los *_sdk.py son wrappers CLI que le pegan por HTTP a la app Sanic de su
# propio contenedor (app/middleware/auth.py, dispatch -> 0.0.0.0:8000), asi
# que ahi no basta con que el contenedor exista: la app tiene que estar
# sirviendo. El PYTHONPATH es necesario porque `from account_settings import *`
# pide config/ en el path y `from middleware.auth import ...` pide su padre.
SANIC = {
    'name': 'sdk',
    'container': os.environ.get('LKF_SANIC_CONTAINER', 'lkf-sanic-app'),
    'modules_path': os.environ.get('LKF_SANIC_MODULES_PATH', '/srv/lkf-sanic-app/modules'),
    'env': {
        'PYTHONPATH': os.environ.get(
            'LKF_SANIC_PYTHONPATH',
            '/srv/lkf-sanic-app/config:/srv/lkf-sanic-app'),
    },
}

TARGETS = (ADDONS, SANIC)


def target_for(script_name):
    """A que contenedor le toca este script. El nombre manda, sin fallback."""
    return SANIC if script_name.endswith(SDK_SUFFIX) else ADDONS


# --- resto de la configuracion ------------------------------------------

# secrets/ del repo addons, montado en este contenedor. Solo se usa para
# resolver el account_id por default.
SECRETS_PATH = os.environ.get('LKF_SECRETS_PATH', '/srv/scripts/addons/secrets')

# Destino del proxy de login.
UPSTREAM = os.environ.get('LKF_UPSTREAM', 'https://app.linkaform.com').rstrip('/')

# Segundos maximos por `docker exec`.
TIMEOUT = int(os.environ.get('MINIBACK_TIMEOUT', 120))

# Segundos de vida del indice de scripts antes de recalcularlo.
INDEX_TTL = int(os.environ.get('MINIBACK_INDEX_TTL', 30))

# Tope de scripts corriendo a la vez. 0 = sin tope (default): las peticiones
# del front corren en paralelo. Subirlo de 0 solo si la maquina se queda sin
# memoria, porque cada corrida es un proceso de python cargando linkaform_api.
MAX_CONCURRENT = int(os.environ.get('MINIBACK_MAX_CONCURRENT', 0))

# Puerto dentro del contenedor. El puerto publicado en el host lo decide
# MINIBACK_PORT en docker-compose.miniback.yml, no esta variable.
LISTEN_PORT = int(os.environ.get('MINIBACK_LISTEN_PORT', 8000))


def _account_id_de_secrets():
    """Lee la cuenta activa igual que config/local_settings.py:32-46.

    secrets/current_domain dice que seccion de secrets/accounts.ini esta
    activa; de ahi sale account_id. Devuelve None si no se puede resolver.
    """
    current = os.path.join(SECRETS_PATH, 'current_domain')
    accounts = os.path.join(SECRETS_PATH, 'accounts.ini')
    if not os.path.exists(current) or not os.path.exists(accounts):
        return None
    try:
        domain = open(current, encoding='utf-8').read().strip()
        if not domain:
            return None
        # interpolation=None: los COUCH_USER vienen url-encoded ('user%40dominio')
        # y el interpolador por defecto trata el % como sintaxis y revienta.
        cat = configparser.ConfigParser(interpolation=None)
        cat.read(accounts, encoding='utf-8')
        if not cat.has_section(domain):
            return None
        value = cat.get(domain, 'account_id', fallback=None)
        if value is None and cat.has_section('global'):
            value = cat.get('global', 'account_id', fallback=None)
        if not value:
            return None
        value = value.strip()
        return int(value) if value.isdigit() else value
    except Exception as e:
        print('miniback: no se pudo leer el account_id de {}: {}'.format(accounts, e))
        return None


def resolve_account_id():
    """account_id por default: LKF_ACCOUNT_ID y si no, secrets/."""
    env = os.environ.get('LKF_ACCOUNT_ID', '').strip()
    if env:
        return int(env) if env.isdigit() else env
    return _account_id_de_secrets()


ACCOUNT_ID = resolve_account_id()
