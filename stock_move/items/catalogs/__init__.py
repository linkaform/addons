# coding: utf-8
from base import items
from .catalog_resource import CatalogResource

module = __name__.replace('.','/')

install_order = [
    'employees_teams',
    'employees',
    'product',
    'warehouse',
    'product_presentation',
    'product_inventory',
    ]
donot_install = [
    'nouuse_unit_of_measure',
    'unit_of_measure',
    'product_product',
    ]

def get_catalog_modules(all_items):
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
            data_file.append(file)
        else:
            form_file[file_name] = {'data':[],'workflow':[], 'rules':[], 'demo':[] }
    for item in list(form_file.keys()):
        for file in data_file:
            file_ext = file.split('.')
            file_name = file_ext[0]
            file_type = file_name.split('_')[-1]
            if file_name[:file_name.rfind('_')] == item:
                #TODO hacer muylti extesion
                form_file[item][file_type].append(file)
    return form_file

def get_catalogs_to_install():
    catalogs_data = get_catalog_modules(items_json)
    catalogs_data['install_order'] = install_order
    for n in donot_install:
        if n in list(catalogs_data.keys()):
            catalogs_data.pop(n)
    return catalogs_data

items_json = items.get_all_items_json(module, 'catalogs')
instalable_catalogs = get_catalogs_to_install()

