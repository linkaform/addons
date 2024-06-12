# coding: utf-8
import simplejson

from linkaform_api import utils, lkf_models

from lkf_addons import items 


class CatalogResource(items.Items):

    def load_info(self, files, file_type, module_info):
        catalog_id = module_info.get('item_id')
        for full_file_name in files:
            file_name = full_file_name.split('.')[0]
            if module_info.get(f'load_{file_type}',{}) and  module_info.get(f'load_{file_type}',{}).get(file_name):
                continue
            try:
                #file = open('{}/{}'.format(self.this_path, full_file_name))
                print('file=', '{}/{}'.format(self.this_path, full_file_name))
                # file_read = file.read()
                with open('{}/{}'.format(self.this_path, full_file_name), "r") as file:
                    file_data = simplejson.loads(file.read())
            except FileNotFoundError:
                print(f'File not found {self.this_path + full_file_name}, continue')
                return False

            catalog_map = file_data['mapping']
            spreadsheet_url = file_data['spreadsheet_url']
            res = self.lkf_api.catalog_load_rows(catalog_id, catalog_map, spreadsheet_url)
            if res.get('status_code') == 202:
                update_query = {'_id': module_info['_id']}
                item_info = {
                    f'load_{file_type}': {file_name:True}
                }
                self.lkf.update(update_query, item_info)

    def install_catalogs(self, instalable_catalogs, **kwargs):
        print('********************* Installing Catalogs **************************')
        install_order = []
        if instalable_catalogs.get('install_order'):
            install_order = instalable_catalogs.pop('install_order')
        else:
            install_order = []  
        install_order += [x  for x in instalable_catalogs.keys() if x not in install_order]
        for catalog_name in install_order:
            print('Installing Catalog: ', catalog_name)
            detail = instalable_catalogs[catalog_name]
            if detail.get('path'):
                this_path = '{}/{}'.format(self.path, detail['path'])
            else:
                this_path = self.path
            catalog_model = self.load_module_template_file(this_path, catalog_name)
            self.this_path = this_path
            res = self.lkf.install_catalog(self.module, catalog_name, catalog_model, local_path=detail.get('path'))
            for file_type, files in detail.items():
                if file_type == 'data' and self.load_data:
                    self.load_info(files, file_type, res )
                if file_type == 'demo' and self.load_demo:
                    self.load_info(files, file_type, res )
                    
                        # catalog_json = self.load_items_file(file_type, file, 'json')

    def get_catalog_modules(self, all_items, parent_path=None):
        data_file = []
        form_file = {}
        for file in all_items:
            if type(file) == dict:
                path = list(file.keys())[0]
                if parent_path:
                    path = '{}/{}'.format(parent_path, path)
                form_file.update(self.get_catalog_modules(list(file.values())[0], parent_path=path))
                continue
            file_ext = file.split('.')
            if len(file_ext) != 2:
                print('Not a supported file', file)
                continue
            file_name = file_ext[0]
            file_type = file_name.split('_')[-1]
            if file_type in ('data', 'demo', 'workflow', 'rules'):
                data_file.append(file)
            else:
                form_file[file_name] = {'data':[],'workflow':[], 'rules':[], 'demo':[] }
                if parent_path:
                    form_file[file_name].update({'path':parent_path})
        for item in list(form_file.keys()):
            for file in data_file:
                file_ext = file.split('.')
                file_name = file_ext[0]
                file_type = file_name.split('_')[-1]
                if file_name[:file_name.rfind('_')] == item:
                    #TODO hacer muylti extesion
                    form_file[item][file_type].append(file)
        return form_file

    def instalable_catalogs(self, install_order=None, path='/srv/scripts/addons/modules'):
        items_json = self.get_anddons_and_modules_items('catalogs')
        
        catalogs_data = self.get_catalog_modules(items_json)
        if install_order:
            catalogs_data['install_order'] = install_order
        else:
            catalogs_data['install_order'] = list(catalogs_data.keys())
        return catalogs_data