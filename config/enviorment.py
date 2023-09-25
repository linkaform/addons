# coding: utf-8
from settings import ENV, config

mongo_hosts = config.get('mongo_hosts')
PROTOCOL = config.get('PROTOCOL')
HOST = config.get('HOST')

if ENV == 'prod':
    mongo_hosts = 'db2.linkaform.com:27017,db3.linkaform.com:27017,db4.linkaform.com:27017'
    HOST = 'preprod.linkaform.com'
    PROTOCOL = 'https'

elif ENV == 'preprod':
    mongo_hosts = 'dbs2.lkf.cloud:27918'
    HOST = 'app.linkaform.com'
    PROTOCOL = 'https'


MAX_POOL_SIZE = 1000
WAIT_QUEUE_TIMEOUT = 1000
MONGODB_URI = 'mongodb://%s/'%(mongo_hosts)

config.update({
        'PROTOCOL' : PROTOCOL,
        'HOST' : HOST,
        'MONGODB_PORT':27017,
        'MONGODB_HOST': mongo_hosts,
        #'MONGODB_URI': MONGODB_URI,
        'AIRFLOW_PROTOCOL' : 'https', #http or https
        'AIRFLOW_PORT' : 5000, #http or https
        'AIRFLOW_HOST' : 'airflow.linkaform.com',
        #'AIRFLOW_HOST' : 'airflow.linkaform.com',
    })

def update_settings(settings):
    global config
    settings.config.update(config)
    return settings
