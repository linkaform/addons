# -*- coding: utf-8 -*-
import simplejson

from linkaform_api import settings, network, utils, lkf_models


class LKF_Base():

    def __init__(self, settings):
        self.lkf_base = {}
        self.lkf_api = utils.Cache(settings)
        #print('settings', dir(settings))
        #print('config', settings.config)
        config = settings.config
        self.net = network.Network(settings)
        self.cr = self.net.get_collections()
        self.lkm = lkf_models.LKFModules(settings)
        config['PROTOCOL'] = 'https'
        config['HOST'] ='app.linkaform.com'
        settings.config.update(config)
        self.lkf_api_prod = utils.Cache(settings)


    def get_related_records(self, query):
        records = self.cr.aggregate(query)
        return [r for r in records ]
