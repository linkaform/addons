# coding: utf-8
# local_settings.py de addons para GitHub Actions (lo copia bin/lkf_ci_setup.sh a
# config/local_settings.py). Es la parte generica del local_settings.py de dev:
# lee la seccion activa de secrets/accounts.ini, que en CI escribe el setup con
# la cuenta de preprod de los secrets PREPROD_*. Sin credenciales aqui.
from settings import *
from uts import update_settings

import configparser, os

_cat = configparser.ConfigParser(interpolation=None)
_cat.read(os.path.join(SECRETS_PATH, 'accounts.ini'), encoding='utf-8')
_domain = open(os.path.join(SECRETS_PATH, 'current_domain'), encoding='utf-8').read().strip()

for _sec in ('global', _domain):
    if _cat.has_section(_sec):
        for k, v in _cat.items(_sec):
            config[k.upper()] = v

print('Cuenta activa (CI):', _domain, '/ Enviorment:', ENV)

MAX_POOL_SIZE = 1000
WAIT_QUEUE_TIMEOUT = 1000
MONGODB_URI = 'mongodb://%s/' % (mongo_hosts)

settings.config.update(config)
settings = update_settings(settings)
