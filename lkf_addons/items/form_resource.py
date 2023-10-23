# coding: utf-8
import simplejson

from linkaform_api import utils, lkf_models

from lkf_addons import items 


class FormResource(items.Items):

    def setup_workflows(self, conf_files, action):
        for file_name in conf_files:
            file_name = file_name.split('.')[0]
            print('Installing Workflows: ', file_name)
            workflow_model = self.load_module_template_file(self.path, file_name)
            # res = self.lkf.install_workflows(module, workflow_model, 'update')
            if action == 'create':
                res = self.lkf_api.upload_workflows(workflow_model, 'POST')
            elif action =='update':
                res = self.lkf_api.upload_workflows(workflow_model, 'PATCH')
            #res = self.lkf_api.upload_workflows(workflow_model, 'PATCH')

    def setup_rules(self, conf_files, action):
        for file_name in conf_files:
            file_name = file_name.split('.')[0]
            rules_model = self.load_module_template_file(self.path, file_name)
            print('Installing Rules: ',file_name )
            # res = self.lkf.install_workflows(module, workflow_model, 'update')
            if action == 'create':
                res = self.lkf_api.upload_rules(rules_model, 'POST')
            elif action =='update':
                res = self.lkf_api.upload_rules(rules_model, 'PATCH')
            #res = self.lkf_api.upload_rules(rules_model, 'PATCH')

    def install_forms(self, instalable_forms):
        if instalable_forms.get('install_order'):
            install_order = instalable_forms.pop('install_order', [])
        else:
            install_order = []
        install_order += [x  for x in instalable_forms.keys() if x not in install_order]
        response = []
        for form_name in install_order:
            print('Installing Form: ', form_name)
            detail = instalable_forms[form_name]
            form_model = self.load_module_template_file(self.path, form_name)
            item_info = {
                # 'created_by' : user,
                'module': self.module,
                # 'name': 'como lo ponomes',
                'item_type': 'form',
                'item_name':form_name,
            }
            item = self.lkf.serach_module_item(item_info)
            res = self.lkf.install_forms(self.module, form_name, form_model)
            response.append(
                    {
                        'module':self.module,
                        'item_name': form_name,
                        'install_status':'installed',
                        'status_code': res.get('status_code'),
                        'error': res.get('json',{}).get('error'),
                        'lkf_response':res
                    }
                )
            if res.get('status') in ('update','create','unchanged'):
                for config, conf_files in detail.items():
                    if config == 'workflow':
                        # res['status'] = 'create'
                        self.setup_workflows(conf_files, res['status'])
                    if config == 'rules':
                        self.setup_rules(conf_files, res['status'])
            elif res.get('status_code') == 400:
                print('res=',res)
                raise self.LKFException('Error installing form: {}. Error msg'.format(form_name, res['json']['error']))
        return response
 
    def get_form_modules(self, all_items):
        data_file = []
        form_file = {}
        for file in all_items:
            file_ext = file.split('.')
            if len(file_ext) != 2:
                print('Not a supported file', file)
                continue
            file_name = file_ext[0]
            file_type = file_name.split('_')[-1]
            if file_type in ('data', 'demo', 'workflow', 'rules'):
                if file_name not in data_file:
                    data_file.append(file_name)
            else:
                form_file[file_name] = {'data':[],'workflow':[], 'rules':[], 'demo':[] }
        for item in list(form_file.keys()):
            for file_name in data_file:
                file_type = file_name.split('_')[-1]
                if file_name[:file_name.rfind('_')] == item:
                    #TODO hacer muylti extesion
                    form_file[item][file_type].append('{}.{}'.format(file_name, file_ext[1]))
        return form_file

    def instalable_forms(self, install_order=None):
        items_json = self.get_all_items_json('forms')
        forms_data = self.get_form_modules(items_json)
        if install_order:
            forms_data['install_order'] = install_order
        else:
            forms_data['install_order'] = list(forms_data.keys())
        return forms_data