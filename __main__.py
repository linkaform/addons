# coding: utf-8
import sys
import subprocess
import importlib

import settings

from linkaform_api import utils

print('Running modules with command: ', sys.argv)
base_modules = ['stock_move',]
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

print('load_modules', load_modules)

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


def do_load_modules(not_installed):
    for module in not_installed:
        print('....')
        # do_clone_modules(module)
        # do_add_modules(module)
        # cmd = ['git', 'submodule', 'init', module]
        # print('cmd', cmd)
        # process = subprocess.Popen(args=cmd,
        #     stdout=subprocess.PIPE,
        #     stderr=subprocess.PIPE)
        # output, error = process.communicate()
        # print('output>>>>', output)
        # print('error', error)

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
install = {'all':False, 'stock_move':True}
load_data = False
load_demo = False

def do_load_modules(load_modules):
    response = []
    for module in load_modules:
        # global forms
        print('loaidng module', module)
        print('--------------------------------------------------------------')
        #scripts
        scripts = importlib.import_module('{}.items.scripts'.format(module))
        all_items_script = scripts.items_files
        script_dict = scripts.instalable_scripts
        #catalogs
        catalogs = importlib.import_module('{}.items.catalogs'.format(module))
        all_items_catalog = catalogs.items_json
        catalog_dict = catalogs.instalable_catalogs
        #forms
        forms = importlib.import_module('{}.items.forms'.format(module))
        all_items = forms.items_json
        form_dict = forms.instalable_forms 
        if install.get('all') or install.get(module):
            # #scripts
            script_resource = scripts.ScriptResource(path=scripts.__path__[0], settings=settings)
            script_resource.install_scripts(module, script_dict)
            # # #catalog
            catalog_resource = catalogs.CatalogResource(path=catalogs.__path__[0], settings=settings)
            catalog_resource.install_catalogs(module, catalog_dict)
            # #forms
            form_resource = forms.FormResource(path=forms.__path__[0], settings=settings)
            response += form_resource.install_forms(module, form_dict)


lkf_api = utils.Cache(settings)
user = lkf_api.get_jwt(api_key=settings.config['APIKEY'], get_user=True)
settings.config["JWT_KEY"] = user.get('jwt')
settings.config["ACCOUNT_ID"] = user['user']['parent_info']['id']
settings.config["USER"] = user
print('settings.config["ACCOUNT_ID"]', settings.config["ACCOUNT_ID"])
print('load_modules', load_modules)
do_load_modules(load_modules)
