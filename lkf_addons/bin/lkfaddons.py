#!/usr/local/bin/python
# coding: utf-8
import sys, os
import subprocess
import importlib

from linkaform_api import utils
from download_module import download_modules

sys.path.append('/srv/scripts/addons/config/')
sys.path.append('/srv/scripts/addons/modules')

import settings
from uts import get_lkf_api

commands = sys.argv
commands.pop(0)
print('Running modules with command: ',commands)
base_modules = ['stock_move',]
#base_modules = ['test',]
base_modules = ['expenses',]
load_modules = []

not_installed = []

cmd = ['pwd']
process = subprocess.Popen(args=cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
output, error = process.communicate()

load_modules += base_modules

def search_modules():
    cmd = ['ls', '-d', '/srv/scripts/addons/modules/*/']
    cmd = ['find', '/srv/scripts/addons/modules' , '-maxdepth', '1', '-type', 'd']
    process = subprocess.Popen(args=cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    output, error = process.communicate()
    res = []
    output = output.split(b'\n')
    for x in output:
        x = x.decode('utf-8')
        x = x.replace('/srv/scripts/addons/modules','').strip('/')
        if x.find('.') == 0:
            continue
        if x:
            res.append(x)
    return res

#Este dato debe de venir del front
# install = {'all':False, 'stock_move':False, 'test':True}

# load_data = True
load_data = False
load_demo = True

def do_load_modules(load_modules):
    response = []
    print('load_modules====', load_modules)
    for module in load_modules:
        # global forms
        print('-'*35 + f' Loding Module: {module} ' + '-'*35)
        ### Scripts
        print('install', install)
        scripts = importlib.import_module('{}.items.scripts'.format(module))
        #TODO revisar porque no corren las reglas
        if install.get('all') or install.get(module):
            script_resource = scripts.ScriptResource(
                path=scripts.__path__[0], 
                module=module, 
                settings=settings,
                load_demo=load_demo, 
                load_data=load_data
                )
            try:
                install_order = scripts.install_order
            except:
                install_order = []
            script_dict = script_resource.instalable_scripts(install_order)
            ###scripts
            if load_script:
                script_resource.install_scripts(script_dict)

            ### Catalogs
            print('modules' , module)
            catalogs = importlib.import_module('{}.items.catalogs'.format(module))
            catalog_resource = catalogs.CatalogResource(
                path=catalogs.__path__[0], 
                module=module, 
                settings=settings, 
                load_demo=load_demo, 
                load_data=load_data
                )
            try:
                install_order = catalogs.install_order
            except:
                install_order = []
            catalog_dict = catalog_resource.instalable_catalogs(install_order)
            ### catalog
            if load_catalog:
                catalog_resource.install_catalogs(catalog_dict)
            
            ### Forms
            forms = importlib.import_module('{}.items.forms'.format(module))
            form_resource = forms.FormResource(
                path=forms.__path__[0], 
                module=module, 
                settings=settings, 
                load_demo=load_demo, 
                load_data=load_data
                )
            try:
                install_order = forms.install_order
            except:
                install_order = []
            form_dict = form_resource.instalable_forms(install_order)
            ###forms
            if load_form:
                response += form_resource.install_forms(form_dict)

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
                print('modules to uninstall', val)
                item_id = val.get('item_id')
                if item_id:
                    print('item_id = ',item_id)
                    res = item.delete_item(item_id)
                    print('res = ',res)
                    if res.get('status_code') == 204:
                        remove_items.append(item_id)
                    remove_items.append(item_id)
            res = item.remove_module_items(remove_items)
            print('res...=',res)
            

lkf_api = get_lkf_api()

print('commands', commands)


load_data = False
load_demo = False
load_script  = False
load_catalog = False
load_form    = False

ask_data =    True
ask_demo =    True
ask_script  = True
ask_catalog = True
ask_form    = True



if 'script' in commands:
    load_script = True
    ask_script = False
if 'catalog' in commands:
    load_catalog = True
    ask_catalog = False
if 'form' in commands:
    load_form = True
    ask_form = False
if 'demo' in commands:
    load_demo = True
    ask_demo = False
if 'data' in commands:
    load_data = True
    ask_data = False



def set_value(value):
    if value == 'y' or value == 'Y':
        return True
    return False

def set_value_id(value):
    return value


def get_modules_2_install(commands):
    modules = search_modules()
    for idx, c in enumerate(commands):
        if c == '--module' or c == '-m':
            module = commands[idx+1]
            if module in modules:
                return module
            else:
                raise ValueError(f'No module found with name: {module}, available options are: {modules}')
    return modules


install = {'all':False, 'stock_move':False, 'test':False, 'expenses':True}
install = {}


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

print('load_modules', load_modules)

if __name__ == '__main__':
    print('Running on ', '{}:-:'.format(settings.ENV)*300)
    environment =  set_value(input(f"We are running on {settings.ENV} Enviroment, are you sure [y/n] (default n):"))

    if not environment:
        print('Ending session no enviornment confirmation found')
    else:
        if commands[0] == 'uninstall':
            uninstall_modules(install)
        elif commands[0] == 'install':
            if ask_data:
                load_demo = set_value(input("Load DEMO data [y/n] (default n):"))
            if ask_demo:    
                load_data = set_value(input("Load DATA [y/n] (default n):"))
            if ask_form:    
                load_form = set_value(input("Load Forms [y/n] (default n):"))
            if ask_catalog:    
                load_catalog = set_value(input("Load Catalogs [y/n] (default n):"))
            if ask_script:    
                load_script = set_value(input("Load Scripts [y/n] (default n):"))
            install = {'all':True}
            do_load_modules(load_modules)
        elif commands[0] == 'download':
            options = []
            if ask_form:    
                load_form = set_value(input("Download Forms [y/n] (default n):"))
                if load_form:
                    options.append('forms')
            else:
                options.append('forms')
            if ask_catalog:    
                load_catalog = set_value(input("Download Catalogs2 [y/n] (default n):"))
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
            download_items = {}
            if not load_modules:
                if load_form:
                    form_id = set_value(input("Form id to download:"))
                    download_items.update({'forms':{form_id:None}})
                if load_catalog:
                    catalog_id = set_value_id(input("Catalog id to download:"))
                    print('inpuuutttt....', catalog_id)
                    download_items.update({'catalogs':{catalog_id:None}})
                if load_script:
                    script_id = set_value(input("Script id to download:"))
                    download_items.update({'scripts':{script_id:None}})
            print('download_items========================',download_items)
            download_modules(load_modules, options, items_ids=download_items)


