# coding: utf-8
import os

from settings import config, SECRETS_PATH

def _env_activo():
    env = os.environ.get('LKF_ENV', '').strip()
    if not env:
        current_env_file = os.path.join(SECRETS_PATH, 'current_env')
        if os.path.exists(current_env_file):
            env = open(current_env_file, encoding='utf-8').read().strip()
    return env if env in ('local', 'preprod', 'prod', 'sbx-dev0', 'sbx-preprod', 'sbx-josepato0') else 'prod'

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

elif ENV == 'sbx-dev0':
    mongo_hosts = 'sbx-dev0.linkaform.com:27017'
    HOST = 'sbx-dev0.linkaform.com'
    PROTOCOL = 'https'
    COUCH_ENV = 'dev'
    COUCH_DEV_HOST = 'sbx-dev0-couchdb.linkaform.com'
    COUCH_DEV_PROTOCOL = 'https'
    COUCH_DEV_PORT = 443

elif ENV == 'sbx-preprod':
    mongo_hosts = 'sbx-preprod.linkaform.com:27017'
    HOST = 'sbx-preprod.linkaform.com'
    PROTOCOL = 'https'
    COUCH_ENV = 'dev'
    COUCH_DEV_HOST = 'sbx-preprod-couchdb.linkaform.com'
    COUCH_DEV_PROTOCOL = 'https'
    COUCH_DEV_PORT = 443

elif ENV == 'sbx-josepato0':
    mongo_hosts = 'sbx-josepato0.linkaform.com:27017'
    HOST = 'sbx-josepato0.linkaform.com'
    PROTOCOL = 'https'
    COUCH_ENV = 'dev'
    COUCH_DEV_HOST = 'sbx-josepato0-couchdb.linkaform.com'
    COUCH_DEV_PROTOCOL = 'https'
    COUCH_DEV_PORT = 443

# Couch dev: los sandboxes lo exponen por dominio (sbx-<entorno>-couchdb), detras del
# mismo proxy, en https/443. El resto de environments usa el default de linkaform_api.
COUCH_DEV_CFG = {}
if ENV.startswith('sbx-'):
    COUCH_DEV_CFG = {
        'COUCH_DEV_PROTOCOL': COUCH_DEV_PROTOCOL,
        'COUCH_DEV_HOST': COUCH_DEV_HOST,
        'COUCH_DEV_PORT': COUCH_DEV_PORT,
    }

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

config.update(COUCH_DEV_CFG)

def update_settings(settings):
    global config
    settings.config.update(config)
    return settings
