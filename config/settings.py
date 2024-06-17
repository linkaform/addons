# coding: utf-8
# print('=================== LODING SETTINGS FOR ENVIOIRMENT: {} ==================='.format(ENV))
from linkaform_api import settings

MODULES_PATH = '/srv/scripts/addons/modules'
ADDONS_PATH = '/usr/local/lib/python3.10/site-packages/lkf_addons/addons'

config = {
    'COLLECTION' : 'form_answer',
    # 'MONGODB_REPLICASET': 'linkaform_replica',
    # 'MONGO_READPREFERENCE': 'secondaryPreferred',
    'MONGODB_MAX_IDLE_TIME': 12000,
    'MONGODB_MAX_POOL_SIZE': 1000,
    'USER_ID' : '',
    'JWT_KEY': False,
    'USE_JWT': True,
    'COUCH_ENV':'prod',
    'COUCH_PROTOCOL':'http',
    'COUCH_USER':'',
    'COUCH_PASSWORD':'',
    'COUCH_HOST':'',
    'COUCH_PORT':'',
    'COUCH_DEV_PROTOCOL':'http',
    'COUCH_DEV_USER':'',
    'COUCH_DEV_PASSWORD':'',
    'COUCH_DEV_HOST':'',
    'COUCH_DEV_PORT':'',
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
    # print('loaidng local_settings')
except Exception as e:
    print('local_settings... NOT FOUND!!!', e)
    print('create a file with you own local_settings, just import this file with from  settings import * ')
    print('Then update your config with your own keys')


