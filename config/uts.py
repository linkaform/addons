# coding: utf-8

#Utils for using LinkaFrom modules...
from linkaform_api import utils, lkf_models
# from lkf_addons.config import settings

_SEP = "=" * 60
_SETTINGS_HINT = (
    "Abre el archivo:  /srv/scripts/addons/config/local_settings.py\n"
    "Descomenta (o agrega) tu usuario y APIKEY:\n\n"
    "    config.update({\n"
    "        'USERNAME': 'tu_usuario@ejemplo.com',\n"
    "        'APIKEY':   'tu_apikey_aqui',\n"
    "    })\n"
)


def _check_credentials(username, apikey):
    if not username or username == 'your_likaform_username@here.com':
        raise ValueError(
            f"\n{_SEP}\n"
            f"ERROR: USERNAME no configurado en local_settings.py\n"
            f"{_SEP}\n"
            f"{_SETTINGS_HINT}"
            f"{_SEP}"
        )
    if not apikey or apikey == 'your_APIKEY_HERE':
        raise ValueError(
            f"\n{_SEP}\n"
            f"ERROR: APIKEY no configurado en local_settings.py\n"
            f"{_SEP}\n"
            f"{_SETTINGS_HINT}"
            f"{_SEP}"
        )


def update_settings(settings):
    username = settings.config.get('USERNAME', '')
    apikey = settings.config.get('APIKEY', '')
    _check_credentials(username, apikey)
    lkf_api = utils.Cache(settings)
    user = lkf_api.get_jwt(api_key=apikey, get_user=True)
    if not user or not user.get('user'):
        raise ValueError(
            f"\n{_SEP}\n"
            f"ERROR: No se pudo autenticar el usuario\n"
            f"{_SEP}\n"
            f"USERNAME: {username}\n"
            f"Verifica que el APIKEY sea correcto en local_settings.py\n"
            f"{_SEP}"
        )
    settings.config["JWT_KEY"] = user.get('jwt')
    settings.config["APIKEY_JWT_KEY"] = user.get('jwt')
    account_id = user['user']['parent_info']['id']
    settings.config["USER_ID"] = user['user']['id']
    settings.config["ACCOUNT_ID"] = account_id
    settings.config["USER"] = user['user']
    settings.config["MONGODB_USER"] = 'account_{}'.format(account_id)
    return settings

def get_lkf_api(settings):
    username = settings.config.get('USERNAME', '')
    apikey = settings.config.get('APIKEY', '')
    _check_credentials(username, apikey)
    lkf_api = utils.Cache(settings)
    user = lkf_api.get_jwt(api_key=apikey, get_user=True)
    if not user or not user.get('user'):
        raise ValueError(
            f"\n{_SEP}\n"
            f"ERROR: No se pudo autenticar el usuario\n"
            f"{_SEP}\n"
            f"USERNAME: {username}\n"
            f"Verifica que el APIKEY sea correcto en local_settings.py\n"
            f"{_SEP}"
        )
    settings.config["JWT_KEY"] = user.get('jwt')
    settings.config["ACCOUNT_ID"] = user['user']['parent_info']['id']
    settings.config["USER"] = user['user']
    lkf_api = utils.Cache(settings)
    return lkf_api

def get_lkf_module(settings):
    lkf_api = get_lkf_api(settings=settings)
    settings = lkf_api.settings
    lkf_modules = lkf_models.LKFModules(settings)
    user = lkf_api.get_jwt(api_key=settings.config['APIKEY'], get_user=True)
    settings.config["JWT_KEY"] = user.get('jwt')
    settings.config["ACCOUNT_ID"] = user['user']['parent_info']['id']
    settings.config["USER"] = user['user']
    lkf_modules = lkf_models.LKFModules(settings)
    return lkf_modules
