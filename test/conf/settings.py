# coding: utf-8

from hashlib import md5, sha1
import sys


#class pwd(self):

def get_pwd(user_id):
    alias = 'client_{0}'.format(user_id)
    MONGO_SECRET = '_lkf'
    pswd =  sha1('{}{}'.format(md5(alias.encode('utf-8')).hexdigest(), MONGO_SECRET).encode('utf-8')).hexdigest()
    return pswd




#ENV = 'prod' 
ENV = 'test' 
print('=================== LODING SETTINGS FOR ENVIOIRMENT: {} ==================='.format(ENV))
#mongo_hosts = 'dev1.linkaform.com:27017,dev2.linkaform.com:27027,dev3.linkaform.com:27037'


if ENV == 'prod':
    mongo_hosts = 'db2.linkaform.com:27017,db3.linkaform.com:27017,db4.linkaform.com:27017'
else:
    mongo_hosts = '192.168.0.25:27017'

MAX_POOL_SIZE = 1000
WAIT_QUEUE_TIMEOUT = 1000
MONGODB_URI = 'mongodb://%s/'%(mongo_hosts)

account_id = 12068

config = {
    'COLLECTION' : 'form_answer',
    'MONGODB_PORT':27017,
    'MONGODB_HOST': mongo_hosts,
    'MONGODB_URI': MONGODB_URI,
    # 'MONGODB_REPLICASET': 'linkaform_replica',
    # 'MONGO_READPREFERENCE': 'secondaryPreferred',
    'MONGODB_USER': 'account_{}'.format(account_id),
    'MONGODB_PASSWORD':  get_pwd(account_id),
    'MONGODB_MAX_IDLE_TIME': 12000,
    'MONGODB_MAX_POOL_SIZE': 1000,
    'USER_ID' : account_id,
    'ACCOUNT_ID' : account_id,
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
            'APIKEY': '07c7413b41c8b8a49dd518d3caf4f3cc59740090',
            'USERNAME' : 'ydelgado@bacao.com.co',
            # 'APIKEY': '133b3147e088a60fe159a67ad18ed47d9955b166',
            # 'USERNAME' : 'info@tecavan.com',
})


if ENV == 'prod':
    config.update({
            'PROTOCOL' : 'https', #http or https
            'HOST' : 'app.linkaform.com',
            'AIRFLOW_PROTOCOL' : 'https', #http or https
            'AIRFLOW_PORT' : 5000, #http or https
            'AIRFLOW_HOST' : 'af.linkaform.com',
            #'AIRFLOW_HOST' : 'airflow.linkaform.com',
        })

elif ENV == 'preprod':
    config.update({
                'PROTOCOL' : 'http', #http or https
                'HOST' : '192.168.0.25:8000',
                'AIRFLOW_PROTOCOL' : 'https', #http or https
                'AIRFLOW_PORT' : 5000, #http or https
                'AIRFLOW_HOST' : 'af.linkaform.com',
                #'AIRFLOW_HOST' : 'airflow.linkaform.com',
            })
        
else:
    config.update({
            'PROTOCOL' : 'http', #http or https
            'HOST' : '192.168.0.25:8000',
            'AIRFLOW_PROTOCOL' : 'https', #http or https
            'AIRFLOW_PORT' : 5000, #http or https
            'AIRFLOW_HOST' : 'af.linkaform.com',
            #'AIRFLOW_HOST' : 'airflow.linkaform.com',
        })
    



