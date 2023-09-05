# coding: utf-8



from settings import ENV, config

if ENV == 'prod':
    mongo_hosts = 'db2.linkaform.com:27017,db3.linkaform.com:27017,db4.linkaform.com:27017'
elif ENV == 'preprod':
    mongo_hosts = 'dbs2.lkf.cloud:27918'
elif ENV == 'local':
    mongo_hosts = '192.168.0.25:27017'

MAX_POOL_SIZE = 1000
WAIT_QUEUE_TIMEOUT = 1000
MONGODB_URI = 'mongodb://%s/'%(mongo_hosts)

if ENV == 'prod':
    config.update({
            'PROTOCOL' : 'https', #http or https
            'MONGODB_PORT':27017,
            'MONGODB_HOST': mongo_hosts,
            'MONGODB_URI': MONGODB_URI,
            'HOST' : 'app.linkaform.com',
            'AIRFLOW_PROTOCOL' : 'https', #http or https
            'AIRFLOW_PORT' : 5000, #http or https
            'AIRFLOW_HOST' : 'airflow.linkaform.com',
            #'AIRFLOW_HOST' : 'airflow.linkaform.com',
        })

elif ENV == 'preprod':
    config.update({
                'PROTOCOL' : 'https', #http or https
                'MONGODB_URI': MONGODB_URI,
                'MONGODB_PORT':27017,
                'MONGODB_HOST': mongo_hosts,
                'HOST' : 'preprod.linkaform.com',
                'AIRFLOW_PROTOCOL' : 'https', #http or https
                'AIRFLOW_PORT' : 5000, #http or https
                'AIRFLOW_HOST' : 'af.linkaform.com',
                #'AIRFLOW_HOST' : 'airflow.linkaform.com',
            })
        
elif ENV == 'local':
    config.update({
            'PROTOCOL' : 'http', #http or https
            'MONGODB_PORT':27017,
            'MONGODB_HOST': mongo_hosts,
            'MONGODB_URI': MONGODB_URI,
            'HOST' : '192.168.0.25:8000',
            'AIRFLOW_PROTOCOL' : 'https', #http or https
            'AIRFLOW_PORT' : 5000, #http or https
            'AIRFLOW_HOST' : 'af.linkaform.com',
            #'AIRFLOW_HOST' : 'airflow.linkaform.com',
        })
