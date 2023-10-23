# coding: utf-8


from linkaform_api import settings

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
except:
    print('local_settings... NOT FOUND!!!')
    print('create a file with you own local_settings, just import this file with from  settings import * ')
    print('Then update your config with your own keys')


