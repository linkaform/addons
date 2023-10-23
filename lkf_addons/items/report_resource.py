# coding: utf-8
import simplejson
print('=============================================== ENTRA A ReportResource==============================')

from linkaform_api import utils, lkf_models

from lkf_addons import items 

from .script_resource import ScriptResource

class ReportResource(ScriptResource):

    # def get_script_modules(self, all_items):
    #     data_file = []
    #     form_file = {}
    #     default_image='linkaform/addons:latest'
    #     for file in all_items:
    #         file_ext = file.split('.')
    #         if len(file_ext) != 2:
    #             print('Not a supported file', file)
    #             continue
    #         file_name = file_ext[0]
    #         file_type = file_name.split('_')[-1]
    #         if file_type in ('properties'):
    #             data_file.append(file)
    #         else:
    #             form_file[file_name] = {'properties':'', 'image':default_image}
    #             form_file[file_name]['file_ext'] = file_ext[-1]
    #     for item in list(form_file.keys()):
    #         for file in data_file:
    #             file_ext = file.split('.')
    #             file_name = file_ext[0]
    #             file_type = file_name.split('_')[-1]
    #             if file_name[:file_name.rfind('_')] == item:
    #                 #TODO hacer muylti extesion
    #                 form_file[item][file_type] = file_name
    #     return form_file

    def instalable_reports(self, install_order=None):
        items_files = self.get_all_items_json('reports')
        print('items_files=',items_files)
        scripts_data = self.get_script_modules(items_files)
        if install_order:
            scripts_data['install_order'] = install_order
        else:
            scripts_data['install_order'] = list(scripts_data.keys())
        return scripts_data
