# coding: utf-8




#ENV = 'prod' 
ENV = 'preprod' 
#ENV = 'local' 
print('=================== LODING SETTINGS FOR ENVIOIRMENT: {} ==================='.format(ENV))

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
            # 'APIKEY': '2168e86f66c35859c353fc056a3793fb1449fd97',
            # 'USERNAME' : 'josepato@linkaform.com',
            # 'APIKEY': '7e781c135a573e19a05c559bb47b366183d9c82d',
            #'USERNAME' : 'addons@lkf.com',
            # 'APIKEY': '8ff5828b33937cec61e791d1fd032bc7786b6df4',
            # 'USERNAME' : 'infosync@info-sync.com',
            # 'APIKEY': '4810288a0b0063653d6cfc331fdf1d107c7b3b3b',
            # 'USERNAME' : 'josepato@hotmail.com',
            # 'APIKEY': '07c7413b41c8b8a49dd518d3caf4f3cc59740090',
            # 'USERNAME' : 'ydelgado@bacao.com.co',
            'APIKEY': '133b3147e088a60fe159a67ad18ed47d9955b166',
            'USERNAME' : 'info@tecavan.com',
            # 'APIKEY': 'a405e197f567cb8b2040dfc2f3fcdde00c199cae',
            # 'USERNAME' : 'mantenimiento@linkaform.com',
})


from enviorment import *



