# coding: utf-8
import os

from settings import config, SECRETS_PATH

def _env_activo():
    env = os.environ.get('LKF_ENV', '').strip()
    if not env:
        current_env_file = os.path.join(SECRETS_PATH, 'current_env')
        if os.path.exists(current_env_file):
            env = open(current_env_file, encoding='utf-8').read().strip()
    return env if env in ('local', 'preprod', 'prod') else 'prod'

ENV = _env_activo()

# print('=================== LODING SETTINGS FOR ENVIOIRMENT: {} ==================='.format(ENV))
mongo_hosts = config.get('mongo_hosts')
PROTOCOL = config.get('PROTOCOL')
HOST = config.get('HOST')
COUCH_ENV = config.get('COUCH_ENV')

if ENV == 'prod':
    mongo_hosts = 'db2.linkaform.com:27017,db3.linkaform.com:27017,db4.linkaform.com:27017'
    HOST = 'app.linkaform.com'
    PROTOCOL = 'https'
    COUCH_ENV = 'prod'

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
        # 'COUCH_ENV':COUCH_ENV,
        #'MONGODB_URI': MONGODB_URI,
        'COUCH_ENV':COUCH_ENV,
        'AIRFLOW_PROTOCOL' : 'https', #http or https
        'AIRFLOW_HOST' : 'bob.linkaform.com',
        #'AIRFLOW_PROTOCOL' : 'http', #http or https
        #'AIRFLOW_HOST' : '192.168.0.25',
        'AIRFLOW_PROTOCOL' : 'http', #http or https
        'AIRFLOW_PORT' : 5000, #http or https
        'AIRFLOW_HOST' : 'airflow.linkaform.com',

    })

def update_settings(settings):
    global config
    settings.config.update(config)
    return settings
