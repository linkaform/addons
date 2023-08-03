# coding: utf-8
import sys
import subprocess
import importlib

import settings

from linkaform_api import utils

from uts import get_lkf_api

commands = sys.argv
print('Running modules with command: ',commands)
base_modules = ['stock_move',]
#base_modules = ['test',]
base_modules = ['expenses',]
load_modules = []

try:
    f = open(".gitmodules", "r")
    gfile = f.readlines()
    f.close()
except:
    gfile = []

for line in gfile:
    line =  line.replace("\n","")
    if 'submodule' in line:
        try:
            name = line.replace('[','').replace(']','').split(' ')[1].replace('"','')
        except: 
            name = None
        if name: load_modules.append(name) 

submodules = {
    'stock_move':'https://github.com/linkaform/lkf-stock.git',  
    }

# print('load_modules', load_modules)

not_installed = []

cmd = ['pwd']
process = subprocess.Popen(args=cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
output, error = process.communicate()

load_modules += base_modules

for module, git_url in submodules.items():
    print('module>>>', module)
    print('v', git_url)
    if module not in load_modules: not_installed.append(module)

def do_clone_modules(module):
    cmd = ['git', 'clone', submodules[module]]
    print('cmd', cmd)
    process = subprocess.Popen(args=cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    output, error = process.communicate()
    print('output>>>>', output)
    print('error', error)

def do_add_modules(module):
    cmd = ['git', 'submodule', 'add', './{}'.format(module)]
    print('cmd', cmd)
    process = subprocess.Popen(args=cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    output, error = process.communicate()
    print('output>>>>', output)
    print('error', error)

#Este dato debe de venir del front
# install = {'all':False, 'stock_move':False, 'test':True}
install = {'all':False, 'stock_move':False, 'test':False, 'expenses':True}

# load_data = True
load_data = False
load_demo = True

def do_load_modules(load_modules):
    response = []
    for module in load_modules:
        # global forms
        print('-'*35 + f' Loding Module: {module} ' + '-'*35)
        ### Scripts
        scripts = importlib.import_module('{}.items.scripts'.format(module))
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
    from base import items 
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

print('Running on ', '{}:-:'.format(settings.ENV)*300)
environment =  set_value(input(f"We are running on {settings.ENV} Enviroment, are you sure [y/n] (default n):"))


if not environment:
    print('Ending session no enviornment confirmation found')
else:
    if 'uninstall' in commands:
        uninstall_modules(install)
    else:
        do_load_modules(load_modules)

