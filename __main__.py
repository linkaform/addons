# coding: utf-8
import sys
import subprocess
import importlib

print('Running modules with: ', sys.argv)

installed_modules = []
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
        if name: installed_modules.append(name) 



submodules = {
    'lkf_stock':'https://github.com/linkaform/lkf-stock.git',  
    }

print('installed_modules', installed_modules)

not_installed = []

cmd = ['pwd']
process = subprocess.Popen(args=cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
output, error = process.communicate()
print('output', output)
print('error', error)


for module, git_url in submodules.items():
    print('module', module)
    print('v', git_url)
    if module not in installed_modules: not_installed.append(module)

print('modules listed for install', not_installed)

def do_installed_modules(not_installed):
    for module in not_installed:
        print('/>>>>>>>>>>>>>>>')
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

install = {'all':False, 'lkf_stock':True}
load_data = False
load_demo = False

def do_load_modules(installed_modules):
    print('loading modules in order..')
    for module in installed_modules:
        print('installing module', module)
        global forms
        forms = importlib.import_module('{}.items.forms'.format(module))
        all_items = forms.items_json
        form_dict = forms.instalable_forms 
        print('form form_dict***************', form_dict)
        if install.get('all') or install.get(module):
            forms.install_forms(form_dict)

do_load_modules(installed_modules)
