# coding: utf-8

#Utils for using LinkaFrom modules...
from linkaform_api import utils, lkf_models
# from lkf_addons.config import settings 


def update_settings(settings):
    lkf_api = utils.Cache(settings)
    user = lkf_api.get_jwt(api_key=settings.config['APIKEY'], get_user=True)
    settings.config["JWT_KEY"] = user.get('jwt')
    settings.config["APIKEY_JWT_KEY"] = user.get('jwt')
    account_id = user['user']['parent_info']['id']
    settings.config["USER_ID"] = user['user']['id']
    settings.config["ACCOUNT_ID"] = account_id
    settings.config["USER"] = user['user']
    settings.config["MONGODB_USER"] = 'account_{}'.format(account_id)
    return settings

def get_lkf_api(settings):
    lkf_api = utils.Cache(settings)
    user = lkf_api.get_jwt(api_key=settings.config['APIKEY'], get_user=True)
    if not user:
        raise ('User not found or incorrecto APIKEY ')
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