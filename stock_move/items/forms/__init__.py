# coding: utf-8
from stock_move import items
from stock_move.items.forms.form_resource import FormResource

install_order = ['stock_move']
donot_install = ['stock_inventory', 'stock_move_warehouse']


def get_form_modules(all_items):
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
                form_file[item][file_type].append('{}.json'.format(file_name))
    return form_file

def get_forms_to_install():
    catalogs_data = get_form_modules(items_json)
    catalogs_data['install_order'] = install_order
    for n in donot_install:
        if n in list(catalogs_data.keys()):
            catalogs_data.pop(n)
    return catalogs_data


items_json = items.get_all_items_json('forms')
instalable_forms = get_forms_to_install()




