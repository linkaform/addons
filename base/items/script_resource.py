# coding: utf-8
import simplejson

from linkaform_api import utils, lkf_models

from base import items 


class ScriptResource(items.Items):

    def install_scripts(self, instalable_scripts):
        install_order = []
        print('instalable_scripts-=',instalable_scripts)
        if instalable_scripts.get('install_order'):
            install_order = instalable_scripts.pop('install_order')
        else:
            install_order = []
        for script_name in install_order:
            properites=None
            if instalable_scripts:
                detail = instalable_scripts[script_name]
                if detail.get('properties') and detail['properties']:
                    properites = self.load_module_template_file(self.path,  detail['properties'])
                image = detail.get('image')
                script_location = '{}/{}.{}'.format(self.path, script_name, detail.get('file_ext'))
                res = self.lkf.install_script(self.module, script_location, image=image, script_properties=properites)

    def get_script_modules(self, all_items):
        data_file = []
        form_file = {}
        default_image='linkaform/python3_lkf:latest'
        for file in all_items:
            file_ext = file.split('.')
            if len(file_ext) != 2:
                print('Not a supported file', file)
                continue
            file_name = file_ext[0]
            file_type = file_name.split('_')[-1]
            if file_type in ('properties'):
                data_file.append(file)
            else:
                form_file[file_name] = {'properties':'', 'image':default_image}
                form_file[file_name]['file_ext'] = file_ext[-1]
        for item in list(form_file.keys()):
            for file in data_file:
                file_ext = file.split('.')
                file_name = file_ext[0]
                file_type = file_name.split('_')[-1]
                if file_name[:file_name.rfind('_')] == item:
                    #TODO hacer muylti extesion
                    form_file[item][file_type] = file_name
        return form_file

    def instalable_scripts(self, install_order=None):
        items_files = self.get_all_items_json('scripts')
        scripts_data = self.get_script_modules(items_files)
        if install_order:
            scripts_data['install_order'] = install_order
        else:
            scripts_data['install_order'] = list(scripts_data.keys())
        return scripts_data
