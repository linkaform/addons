# coding: utf-8
from settings import config

#ENV = 'prod' 
ENV = 'preprod' 
#ENV = 'local' 
# print('=================== LODING SETTINGS FOR ENVIOIRMENT: {} ==================='.format(ENV))
mongo_hosts = config.get('mongo_hosts')
PROTOCOL = config.get('PROTOCOL')
HOST = config.get('HOST')
COUCH_ENV = config.get('COUCH_ENV')

if ENV == 'prod':
    mongo_hosts = 'db2.linkaform.com:27017,db3.linkaform.com:27017,db4.linkaform.com:27017'
    HOST = 'app.linkaform.com'
    PROTOCOL = 'https'

elif ENV == 'preprod':
    mongo_hosts = 'dbs2.lkf.cloud:27918'
    HOST = 'preprod.linkaform.com'
    PROTOCOL = 'https'
    COUCH_ENV = 'dev'

MAX_POOL_SIZE = 1000
WAIT_QUEUE_TIMEOUT = 1000
MONGODB_URI = 'mongodb://%s/'%(mongo_hosts)

config.update({
        'PROTOCOL' : PROTOCOL,
        'HOST' : HOST,
        'MONGODB_PORT':27017,
        'MONGODB_HOST': mongo_hosts,
        'COUCH_ENV':COUCH_ENV,
        #'MONGODB_URI': MONGODB_URI,
        'AIRFLOW_PROTOCOL' : 'https', #http or https
        #'AIRFLOW_PORT' : 5000, #http or https
        'AIRFLOW_HOST' : 'bob.linkaform.com',
        #'AIRFLOW_PROTOCOL' : 'http', #http or https
        #'AIRFLOW_HOST' : '192.168.0.25',
        #'AIRFLOW_HOST' : 'airflow.linkaform.com',

    })

def update_settings(settings):
    global config
    settings.config.update(config)
    return settings
