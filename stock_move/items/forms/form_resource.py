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

    def setup_workflows(self, module, conf_files, action):
        for file_name in conf_files:
            file_name = file_name.split('.')[0]
            workflow_model = self.load_module_template_file(self.path, file_name)
            # res = self.lkf.install_workflows(module, workflow_model, 'update')
            if action == 'create':
                res = self.lkf_api.upload_workflows(workflow_model, 'POST')
            elif action =='update':
                res = self.lkf_api.upload_workflows(workflow_model, 'PATCH')
            res = self.lkf_api.upload_workflows(workflow_model, 'PATCH')

    def setup_rules(self, module, conf_files, action):
        for file_name in conf_files:
            file_name = file_name.split('.')[0]
            rules_model = self.load_module_template_file(self.path, file_name)
            # res = self.lkf.install_workflows(module, workflow_model, 'update')
            if action == 'create':
                res = self.lkf_api.upload_rules(rules_model, 'POST')
            elif action =='update':
                res = self.lkf_api.upload_rules(rules_model, 'PATCH')
            res = self.lkf_api.upload_rules(rules_model, 'PATCH')


    def install_forms(self, module, instalable_forms):
        if instalable_forms.get('install_order'):
            install_order = instalable_forms.pop('install_order', [])
        else:
            install_order = []
        install_order += [x  for x in instalable_forms.keys() if x not in install_order]
        response = []
        for form_name in install_order:
            detail = instalable_forms[form_name]
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
            if res['status'] in ('update','create','unchanged'):
                for config, conf_files in detail.items():
                    if config == 'workflow':
                        self.setup_workflows(module, conf_files, res['status'])
                    if config == 'rules':
                        self.setup_rules(module, conf_files, res['status'])
        return response
 
