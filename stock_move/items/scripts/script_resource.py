# coding: utf-8
import simplejson

from linkaform_api import utils, lkf_models

from stock_move.items import Items 
#import load_items_file, load_module_template_file



class ScriptResource(Items):

    # def __init__(self, path, settings):
    #     self.path = path
    #     self.lkf_api = utils.Cache(settings)
    #     self.settings = settings
    #     self.lkf = lkf_models.LKFModules(self.settings)


    def install_scripts(self, module, instalable_scripts):
        install_order = []
        if instalable_scripts.get('install_order'):
            install_order = instalable_scripts.pop('install_order')
        else:
            install_order = []
        for script_name in install_order:
            if instalable_scripts:
                detail = instalable_scripts[script_name]
                if detail.get('properties') and detail['properties']:
                    properites = self.load_module_template_file(self.path,  detail['properties'])
                image = detail.get('image')
                script_location = '{}/{}.{}'.format(self.path, script_name, detail.get('file_ext'))
                res = self.lkf.install_script(module, script_location, image=image, script_properties=properites)


