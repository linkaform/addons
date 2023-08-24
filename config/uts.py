# coding: utf-8

#Utils for using LinkaFrom modules...
from linkaform_api import utils, lkf_models
import settings 


def get_lkf_api():
    lkf_api = utils.Cache(settings)
    user = lkf_api.get_jwt(api_key=settings.config['APIKEY'], get_user=True)
    settings.config["JWT_KEY"] = user.get('jwt')
    settings.config["ACCOUNT_ID"] = user['user']['parent_info']['id']
    settings.config["USER"] = user['user']
    lkf_api = utils.Cache(settings)
    return lkf_api


def get_lkf_module():
    lkf_api = get_lkf_api()
    settings = lkf_api.settings
    lkf_modules = lkf_models.LKFModules(settings)
    user = lkf_api.get_jwt(api_key=settings.config['APIKEY'], get_user=True)
    settings.config["JWT_KEY"] = user.get('jwt')
    settings.config["ACCOUNT_ID"] = user['user']['parent_info']['id']
    settings.config["USER"] = user['user']
    lkf_modules = lkf_models.LKFModules(settings)
    return lkf_modules