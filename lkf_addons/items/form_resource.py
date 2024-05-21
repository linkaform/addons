# coding: utf-8
import simplejson

from linkaform_api import utils, lkf_models

from lkf_addons import items 


class FormResource(items.Items):

    def setup_workflows(self, conf_files, action, path=None, **kwargs):
        if not path:
            path = self.path
        for file_name in conf_files:
            file_name = file_name.split('.')[0]
            print('Installing Workflows: ', file_name)
            workflow_model = self.load_module_template_file(path, file_name)
            # res = self.lkf.install_workflows(module, workflow_model, 'update')
            if action == 'create':
            # if True:
                res = self.lkf_api.upload_workflows(workflow_model, 'POST')
            elif action =='update':
                res = self.lkf_api.upload_workflows(workflow_model, 'PATCH')
                if res.get('status_code') == 404:
                    res = self.lkf_api.upload_workflows(workflow_model, 'POST')
            #res = self.lkf_api.upload_workflows(workflow_model, 'PATCH')

    def setup_rules(self, conf_files, action, path=None):
        if not path:
            path = self.path
        for file_name in conf_files:
            file_name = file_name.split('.')[0]
            rules_model = self.load_module_template_file(path, file_name)
            print('Installing Rules: ',file_name )
            # res = self.lkf.install_workflows(module, workflow_model, 'update')
            if action == 'create':
                res = self.lkf_api.upload_rules(rules_model, 'POST')
            elif action =='update':
                res = self.lkf_api.upload_rules(rules_model, 'PATCH')
                if res.get('status_code') == 404:
                    res = self.lkf_api.upload_rules(rules_model, 'POST')
            #res = self.lkf_api.upload_rules(rules_model, 'PATCH')

    def install_forms(self, instalable_forms):
        if instalable_forms.get('install_order') or instalable_forms.get('install_order') == []:
            install_order = instalable_forms.pop('install_order', [])
        else:
            install_order = []
        install_order += [x  for x in instalable_forms.keys() if x not in install_order]
        response = []
        print('install_order', install_order)

        # install_order = ['green_house_inventory_move']

        for form_name in install_order:
            detail = instalable_forms[form_name]
            if detail.get('path'):
                this_path = '{}/{}'.format(self.path, detail['path'])
            else:
                this_path = self.path
            form_model = self.load_module_template_file(this_path, form_name)
            item_info = {
                # 'created_by' : user,
                'module': self.module,
                # 'name': 'como lo ponomes',
                'item_type': 'form',
                'item_name':form_name,
            }
            item = self.lkf.serach_module_item(item_info)
            res = self.lkf.install_forms(self.module, form_name, form_model, local_path=detail.get('path'))
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
                        self.setup_workflows(conf_files, res['status'], this_path)
                    if config == 'rules':
                        self.setup_rules(conf_files, res['status'], this_path)
            elif res.get('status_code') == 400:
                error = res.get('json',{}).get('error','Please try again!!!')
                raise self.LKFException(f'Error installing form: {form_name}. Error msg {error}')
        return response
 
    def get_form_modules(self, all_items, parent_path=None):
        data_file = []
        form_file = {}
        for file in all_items:
            if type(file) == dict:
                path = list(file.keys())[0]
                if parent_path:
                    path = '{}/{}'.format(parent_path, path)
                form_file.update(self.get_form_modules(list(file.values())[0], parent_path=path))
                continue
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
                if parent_path:
                    form_file[file_name].update({'path':parent_path})
        for item in list(form_file.keys()):
            for file_name in data_file:
                file_type = file_name.split('_')[-1]
                if file_name[:file_name.rfind('_')] == item:
                    #TODO hacer muylti extesion
                    form_file[item][file_type].append('{}.{}'.format(file_name, file_ext[1]))
        return form_file

    def instalable_forms(self, install_order=None):
        items_json = self.get_anddons_and_modules_items('forms')
        forms_data = self.get_form_modules(items_json)
        if install_order:
            forms_data['install_order'] = install_order
        else:
            forms_data['install_order'] = list(forms_data.keys())
        return forms_data