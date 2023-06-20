# coding: utf-8
from base import items
from .script_resource import ScriptResource

module = __name__.replace('.','/')

install_order = [
    'inventory_move_warehouse_location',
    'calculates_production_warehouse',
    'inventory_move_warehouse_scrap'
    ]

donot_install = ['the_script']

default_image = 'linkaform/python3_lkf:latest'

def get_script_modules(all_items):
    data_file = []
    form_file = {}
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

def get_scritps_to_install():
    scripts_data = get_script_modules(items_files)
    scripts_data['install_order'] = install_order
    for n in donot_install:
        if n in list(scripts_data.keys()):
            scripts_data.pop(n)
    return scripts_data

items_files = items.get_all_items_json(module, 'scripts')
instalable_scripts = get_scritps_to_install()

