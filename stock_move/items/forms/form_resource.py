# coding: utf-8
import simplejson

from linkaform_api import utils, lkf_models
from stock_move.items import Items 



class FormResource(Items):

    # def __init__(self, path, settings):
    #     self.path = path
    #     self.lkf_api = utils.Cache(settings)
    #     self.lkf = lkf_models
    #     self.settings = settings


    def install_forms(self, module, instalable_forms):
        if instalable_forms.get('install_order'):
            install_order = instalable_forms.pop('install_order', [])
        else:
            install_order = []
        install_order += [x  for x in instalable_forms.keys() if x not in install_order]
        response = []
        for form_name in install_order:
            detail = instalable_forms[form_name]
            print('detail', detail)
            print('form_name', form_name)
            form_model = self.load_module_template_file(self.path, form_name)
            res = self.lkf.install_forms(module, form_name, form_model)
            response.append(
                    {
                        'module':module,
                        'item_name': form_name,
                        'install_status':'installed',
                        'status_code': res.get('status_code'),
                        'error': res.get('json',{}).get('error'),
                        'lkf_response':res
                    }
                )
            print('res', res)
            print('dir', dir(self.lkf))
            print('dir data', self.lkf.module_data)
            for config, file_name in detail.items():
                print('config=', config)
                print('file_name=', file_name)
        return response
 
