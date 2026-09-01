# coding: utf-8
# print('=================== LODING SETTINGS FOR ENVIOIRMENT: {} ==================='.format(ENV))
import os

from linkaform_api import settings

MODULES_PATH = '/srv/scripts/addons/modules'
ADDONS_PATH = '/usr/local/lib/python3.10/site-packages/lkf_addons/addons'

# Raiz de secrets/ (accounts.ini, current_domain, current_env). Se resuelve relativo
# a este archivo en vez de hardcodearse, para que de lo mismo correr en el host que
# dentro del contenedor, donde el repo vive en /srv/scripts/addons. local_settings.py
# lo consume por el `from settings import *`.
SECRETS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'secrets')

config = {
    'COLLECTION' : 'form_answer',
    # 'MONGODB_REPLICASET': 'linkaform_replica',
    # 'MONGO_READPREFERENCE': 'secondaryPreferred',
    'MONGODB_MAX_IDLE_TIME': 12000,
    'MONGODB_MAX_POOL_SIZE': 1000,
    'USER_ID' : '',
    'JWT_KEY': False,
    'USE_JWT': True,
}


config.update({
            'USERNAME' : 'your_likaform_username@here.com',
            'APIKEY': 'your_APIKEY_HERE',
})


settings.config.update(config)

from enviorment import *


settings = update_settings(settings)

try:
    from local_settings import *
except Exception as e:
    print('===='*40)
    print('local_settings... NOT FOUND!!!')
    print('create a file with you own local_settings, just import this file with from  settings import * ')
    print('Then update your config with your own keys')
    print('Error: ', e)
    print('Envioroment: ', ENV)
    print('===='*40)

settings.ENV = ENV

def get_settings():
    return settings