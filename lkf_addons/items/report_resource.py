# coding: utf-8
import simplejson
print('=============================================== ENTRA A ReportResource==============================')

from linkaform_api import utils, lkf_models

from lkf_addons import items 


class ReportResource(items.Items):


    def install_reports(self, instalable_reports, **kwargs):
        install_order = []
        inst = list(instalable_reports.keys())
        inst.sort()
        print('########## Reading Reports ############' )
        for x in inst:
            print(f"# {x} ".ljust(38) +'#')
        print('#'*39 )
        if instalable_reports.get('install_order'):
            install_order = instalable_reports.pop('install_order')
        else:
            install_order = []
        xml_reports=[]
        for report_name_ext in install_order:
            report_name = report_name_ext.split('__')[0]
            properites=None
            if instalable_reports:
                detail = instalable_reports[report_name_ext]
                if detail.get('properties') and detail['properties']:
                    properites = self.load_module_template_file(self.path,  detail['properties'])
                if detail.get('path'):
                    this_path = '{}/{}'.format(self.path, detail['path'])
                else:
                    this_path = self.path
                report_location = '{}/{}.{}'.format(this_path, report_name, detail.get('file_ext'))
                if detail.get('file_ext') == 'xml':
                    xml_reports.append(report_name_ext)
                elif detail.get('file_ext') == 'py':
                    image = detail.get('image')
                    res = self.lkf.install_script(
                        self.module, 
                        report_location, 
                        image=image, 
                        script_properties=properites, 
                        local_path=detail.get('path'),
                        **{'item_type':'report_script', 'folder_type':'script'})

        for report_name_ext in xml_reports:
            report_name = report_name_ext.split('__')[0]
            properites=None
            if instalable_reports:
                detail = instalable_reports[report_name_ext]
                if detail.get('properties') and detail['properties']:
                    properites = self.load_module_template_file(self.path,  detail['properties'])
                if detail.get('path'):
                    this_path = '{}/{}'.format(self.path, detail['path'])
                else:
                    this_path = self.path
                report_location = '{}/{}.{}'.format(this_path, report_name, detail.get('file_ext'))
            report_model = self.load_module_template_file(this_path,  report_name)
            res = self.lkf.install_report(self.module, report_name, report_location, report_model, local_path=detail.get('path'))

    def get_report_modules(self, all_items, parent_path=None):
        data_file = []
        form_file = {}
        default_image='linkaform/addons:latest'
        for file in all_items:
            if type(file) == dict:
                path = list(file.keys())[0]
                if parent_path:
                    path = '{}/{}'.format(parent_path, path)
                form_file.update(self.get_report_modules(list(file.values())[0], parent_path=path))
                continue
            file_ext = file.split('.')
            if len(file_ext) != 2:
                print('Not a supported file', file)
                continue
            file_name = file_ext[0]
            file_name_ext = f'{file_name}__{file_ext[-1]}'
            file_type = file_name.split('_')[-1]
            if file_type in ('properties'):
                data_file.append(file)
            else:
                form_file[file_name_ext] = {'properties':'', 'image':default_image}
                form_file[file_name_ext]['file_ext'] = file_ext[-1]
                if parent_path:
                    form_file[file_name_ext].update({'path':parent_path})
        for item in list(form_file.keys()):
            for file in data_file:
                file_ext = file.split('.')
                file_name = file_ext[0]
                file_type = file_name.split('_')[-1]
                if file_name[:file_name.rfind('_')] == item:
                    #TODO hacer muylti extesion
                    form_file[item][file_type] = file_name
        return form_file

    def instalable_reports(self, install_order=None):
        items_files = self.get_all_items_json('reports')
        reports_data = self.get_report_modules(items_files)
        if install_order:
            reports_data['install_order'] = install_order
        else:
            reports_data['install_order'] = list(reports_data.keys())
        return reports_data
