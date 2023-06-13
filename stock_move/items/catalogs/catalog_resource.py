# coding: utf-8
import simplejson

from linkaform_api import utils, lkf_models

from stock_move.items import Items 
#import load_items_file, load_module_template_file



class CatalogResource(Items):

    # def __init__(self, path, settings):
    #     self.path = path
    #     self.lkf_api = utils.Cache(settings)
    #     self.settings = settings
    #     self.lkf = lkf_models.LKFModules(self.settings)


    def install_catalogs(self, module, instalable_catalogs):
        install_order = []
        if instalable_catalogs.get('install_order'):
            install_order = instalable_catalogs.pop('install_order')
        else:
            install_order = []  
        install_order += [x  for x in instalable_catalogs.keys() if x not in install_order]
        for catalog_name in install_order:
            detail = instalable_catalogs[catalog_name]
            catalog_model = self.load_module_template_file(self.path, catalog_name)
            res = self.lkf.install_catalog(module, catalog_name, catalog_model)
            for file_type, files in detail.items():
                for file_name in files:
                    file = open('./{}/{}'.format(self.path, file_name))
                    # catalog_json = self.load_items_file(file_type, file, 'json')


