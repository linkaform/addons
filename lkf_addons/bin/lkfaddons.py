#!/usr/local/bin/python
# coding: utf-8
import sys, os
import subprocess
import importlib

from linkaform_api import utils, lkf_object
from linkaform_api.lkf_object import LKFBase 

from download_module import download_modules
from download_module import ADDONS_PATH, MODULES_PATH

# sys.path.append(ADDONS_PATH)
# sys.path.append('/srv/scripts/addons/config/')
# sys.path.append('/srv/scripts/addons/modules')

import settings
from uts import get_lkf_api

commands = sys.argv
commands.pop(0)
print('==== Running LinkaForm Module Manager ====')
base_modules = []
#base_modules = ['stock_move',]
#base_modules = ['test',]
#base_modules = ['expenses',]
load_modules = []

not_installed = []

cmd = ['pwd']
process = subprocess.Popen(args=cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
output, error = process.communicate()

load_modules += base_modules


#Este dato debe de venir del front
# install = {'all':False, 'stock_move':False, 'test':True}

# load_data = True
lkf_api = get_lkf_api()

ask_4_items = True
load_data = False
load_demo = False
load_script  = False
load_reports  = False
load_catalog = False
load_form    = False

ask_data =    True
ask_demo =    True
ask_script  = True
ask_catalog = True
ask_form    = True
ask_reports = True

kwargs = {}
download_related = False


def get_module_dependencies(module, depend_modules):
    print('Dependecies: ', module)
    res = []
    try:
        this_m = importlib.import_module(f'{module}')
        this_obj = this_m
        if hasattr(this_obj, 'depends'):
            if this_obj.depends not in depend_modules:
                res = this_obj.depends
        else:
            res = []
    except:
        res = []
    return res

def do_load_modules(load_modules, **kwargs):
    response = []
    depend_modules = []
    depends_on = []
    for module in load_modules:
        depends_on += get_module_dependencies(module, depends_on)
    for module in load_modules:
        if module not in depends_on:
            depends_on.append(module)
    kwargs.update({'depends_on': get_module_dependencies(module, depends_on)})
    if kwargs.get('dependencies'):
        depend_modules = kwargs['depends_on']
        print('Installing Denpendencies: ', depend_modules)
        depend_modules += load_modules
    else:
        depend_modules = load_modules
    for module in depend_modules:
        # global forms
        print('-'*35 + f' Loding Module: {module} ' + '-'*35)
        #TODO revisar porque no corren las reglas
        if install.get('all') or install.get(module):
            #####################################################################
            ### Scripts
            if load_script:
                scripts = importlib.import_module('{}.items.scripts'.format(module))
                script_resource = scripts.ScriptResource(
                    path=scripts.__path__[0], 
                    module=module, 
                    settings=settings,
                    load_demo=load_demo, 
                    load_data=load_data, 
                    **kwargs
                    )
                try:
                    install_order = scripts.install_order
                except:
                    install_order = []
                script_dict = script_resource.instalable_scripts(install_order)
                ###scripts
                script_resource.install_scripts(script_dict, **kwargs)

            ### Catalogs
            if load_catalog:
                catalogs = importlib.import_module('{}.items.catalogs'.format(module))
                catalog_resource = catalogs.CatalogResource(
                    path=catalogs.__path__[0], 
                    module=module, 
                    settings=settings, 
                    load_demo=load_demo, 
                    load_data=load_data, 
                    **kwargs
                    )
                try:
                    install_order = catalogs.install_order
                except:
                    install_order = []
                catalog_dict = catalog_resource.instalable_catalogs(install_order)
                ### catalog
                catalog_resource.install_catalogs(catalog_dict, **kwargs)
            
            ### Forms
            if load_form:
                forms = importlib.import_module('{}.items.forms'.format(module))
                form_resource = forms.FormResource(
                    path=forms.__path__[0], 
                    module=module, 
                    settings=settings, 
                    load_demo=load_demo, 
                    load_data=load_data, 
                    **kwargs
                    )
                try:
                    install_order = forms.install_order
                except:
                    install_order = []
                form_dict = form_resource.instalable_forms(install_order)
                ###forms
                response += form_resource.install_forms(form_dict, **kwargs)

            ### Reports
            if load_reports:
                print('Module: ', module)
                print('Load Demo info: ', load_demo)
                print('Load Module Data: ', load_data)
                #try:
                if True:
                    reports = importlib.import_module('{}.items.reports'.format(module))
                    report_resource = reports.ReportResource(
                        path=reports.__path__[0], 
                        module=module, 
                        settings=settings,
                        load_demo=load_demo, 
                        load_data=load_data,
                        **kwargs
                        )
                    install_order = reports.install_order
                # except Exception as e:
                #     print('excetp???', e)
                #     install_order = []
                report_dict = report_resource.instalable_reports(install_order)
                ###reports
                report_resource.install_reports(report_dict, **kwargs)

def uninstall_modules(uninstall_dict):
    # from base import items 
    from lkf_addons import items
    print('uninstlling...')
    for module, install in uninstall_dict.items():
        if install:
            item = items.Items(path=items.__path__[0], module=module, settings=settings)
            items_dict = item.get_module_items()
            remove_items = []
            for val in items_dict:
                print('Module to unistall: ', val)
                item_id = val.get('item_id')
                if item_id:
                    res = item.delete_item(item_id)
                    if res.get('status_code') == 204:
                        remove_items.append(item_id)
                    remove_items.append(item_id)
            res = item.remove_module_items(remove_items)

def set_value(value):
    if value == 'y' or value == 'Y':
        return True
    return False

def set_value_id(value):
    return value

def get_modules_2_install(commands):
    lkf_base = LKFBase()
    addons = lkf_base.search_modules(path=ADDONS_PATH)
    modules = lkf_base.search_modules(path=MODULES_PATH)
    modules.sort()
    all_modules = list(set(addons)|set(modules))
    all_modules.sort()
    for idx, c in enumerate(commands):
        if c == '--module' or c == '-m':
            module = commands[idx+1]
            if module in all_modules:
                return module
            else:
                raise ValueError(f'No module found with name: {module}, available options are: {modules}')
    return modules

def get_items_2_load(commands):
    global ask_4_items, download_related
    for idx, c in enumerate(commands):
        if c.strip() == '-r':
            download_related = True
    for idx, c in enumerate(commands):
        if c.strip() == '--item' or c.strip() == '-i':
            ask_4_items = False
            return commands[idx+1]
    return False

def get_enviorment_2_load(commands):
    for idx, c in enumerate(commands):
        if c.strip() == '--env' or c.strip() == '-e':
            return commands[idx+1]
    return False

def print_help():
    print('Usage: lkfaddons action [option | value] [option | value] \n')
    print('actions:')
    print('download:')
    print('        Downloads a scpecific module (-m) and a specific item kind if given')
    print('install:')
    print('        Installs the given modules and items is speficy')
    print('uninstall:')
    print('        UNistalls the given modules and items is speficy')
    print('')
    print('option:')
    print('-m, --module:')
    print('        stands for module, you con type -m module_name -m module_name')
    print('        or can type the module names separated by a " " module_name module_name')
    print('-d, --depends:')
    print('        install module dependencies')
    print('-i, --item:')
    print('        stands for items, you can speficy to load or download only speficif items')
    print('        Available values are, forms, catalogs, scripts, reports')
    print('        you can select multilple values separatede by a " "')
    print('-id:')
    print('        use for downloding a specific item_id. It will download it to the moduel (-m) and item kind (-i) specified')
    print('        MUST be used with the options -m and -i')
    print('        works only on download action')
    print('-e, --env:')
    print('        stands for environment, values are prod, local, preprod')
    print('-r:')
    print('        download related items.')    
    print('-y')
    print('        yes to all item types instalations.') 
    print('-h, --help:')
    print('        Heeelp!!!')
    print('\n')

# install = {'all':False, 'stock_move':False, 'test':False, 'expenses':True}
install = {}



if __name__ == '__main__':

    print('commands', commands)
    item_ids = []
    if not commands or '-h' in commands or '--help' in commands:
        print_help()
    else:
        load_modules_options  = get_modules_2_install(commands)
        load_modules = []
        if type(load_modules_options) == str:
            load_modules.append(load_modules_options)
            install[load_modules_options] = True
        else:
            for module in load_modules_options:
                print('loadmodule', module)
                load = set_value(input(f"*** {commands[0].title()} the module {module}:[y/n] (default n):"))
                if load:
                    load_modules.append(module)
                    install[module] = True
                else:
                    install[module] = False

        preload_item = get_items_2_load(commands)

        if 'script' in commands or 'scripts' in commands:
            load_script = True
            ask_script = False
        if 'report' in commands or 'reports' in commands:
            load_reports = True
            ask_reports = False
        if 'catalog' in commands or 'catalogs' in commands:
            load_catalog = True
            ask_catalog = False
        if 'form' in commands or 'forms' in commands:
            load_form = True
            ask_form = False
        if 'demo' in commands:
            load_demo = True
            ask_demo = False
        if 'data' in commands:
            load_data = True
            ask_data = False
        if 'report' in commands:
            load_reports = True
            ask_reports = False

        if '-f' in commands:
            kwargs.update({'force':True})
        if '-id' in commands:
            item_ids = commands[(commands.index('-id') + 1 )].split(',')
            kwargs.update({'item_ids':item_ids})
        if '-y' in commands:
            ask_form = False
            load_form = True
            ask_script = False
            load_script = True
            ask_catalog = False
            load_catalog = True
            ask_demo = False
            load_demo = True
            ask_data = False
            load_data = True
            ask_reports = False
            load_reports = True
            kwargs.update({'yes':True})
        if '-d' in commands:
            kwargs.update({'dependencies':True})
        else:
            kwargs.update({'dependencies':False})

        print('Running on:', '== {} =='.format(settings.ENV) * 10)
        print('With User:', '== {} =='.format(settings.config['USERNAME']))
        environment = get_items_2_load(commands)
        if not environment or environment == 'prod' or settings.ENV == 'prod':
            environment =  set_value(input(f"We are running on {settings.ENV} Enviroment, are you sure [y/n] (default n):"))
        if settings.ENV  == 'prod':
            sure = set_value(input(f"REALLY SURE to set enviornment to  {settings.ENV} [y/n] (default n):"))
            if sure:
                print('ok doing installation')
            else:
                raise('Stoping installation')
        if not environment:
            print('Ending session no enviornment confirmation found')
        else:
            if commands[0] == 'uninstall':
                uninstall_modules(install)
            elif commands[0] == 'install':
                if ask_4_items:
                    if ask_form:    
                        load_form = set_value(input("Load Forms [y/n] (default n):"))
                    if ask_catalog:    
                        load_catalog = set_value(input("Load Catalogs [y/n] (default n):"))
                        if ask_data:
                            load_demo = set_value(input("Load DEMO data [y/n] (default n):"))
                        if ask_demo:    
                            load_data = set_value(input("Load DATA [y/n] (default n):"))
                    if ask_script:    
                        load_script = set_value(input("Load Scripts [y/n] (default n):"))
                    if ask_reports:    
                        load_reports = set_value(input("Load Reports [y/n] (default n):"))
                else:
                    if load_catalog:
                        load_demo = set_value(input("Load DEMO data [y/n] (default n):"))
                        load_data = set_value(input("Load DATA [y/n] (default n):"))

                install = {'all':True}
                do_load_modules(load_modules, **kwargs)
            elif commands[0] == 'download':
                options = []
                if preload_item:
                    options.append(preload_item)
                else:
                    if ask_form:
                        load_form = set_value(input("Download Forms [y/n] (default n):"))
                        if load_form:
                            options.append('forms')
                    else:
                        options.append('forms')
                    if ask_catalog:    
                        load_catalog = set_value(input("Download Catalogs [y/n] (default n):"))
                        if load_catalog:
                            options.append('catalogs')
                    else:
                            options.append('catalogs')
                    if ask_script:    
                        load_script = set_value(input("Download Scripts [y/n] (default n):"))
                        if load_script:
                            options.append('scripts')
                    else:
                            options.append('scripts')
                    if ask_reports:    
                        load_reports = set_value(input("Download Reports [y/n] (default n):"))
                        if load_reports:
                            options.append('reports')
                    else:
                            options.append('reports')
                download_items = {}
                if not load_modules:

                    if load_form:
                        form_id = set_value(input("Form id to download:"))
                        if item_ids and preload_item == 'form':
                            download_items.update({'forms':{item_ids:None}})
                        else:
                            download_items.update({'forms':{form_id:None}})

                    if load_catalog:
                        catalog_id = set_value_id(input("Catalog id to download:"))
                        if item_ids and preload_item == 'form':
                            download_items.update({'catalogs':{catalog_id:None}})
                        else:
                            download_items.update({'catalogs':{catalog_id:None}})
                    if load_script:
                        script_id = set_value(input("Script id to download:"))
                        download_items.update({'scripts':{script_id:None}})
                    if load_reports:
                        script_id = set_value(input("Reports id to download:"))
                        download_items.update({'reports':{script_id:None}})
                download_modules(load_modules, options, items_ids=download_items, download_related=download_related, **kwargs)


