# coding: utf-8

import os
import xml.etree.ElementTree as ET
import xml.dom.minidom
from copy import deepcopy
import urllib.request, re, sys

from linkaform_api import utils


sys.path.append('/srv/scripts/addons/config/')
sys.path.append('/srv/scripts/addons/modules')
MODULES_PATH = '/srv/scripts/addons/modules'
ADDONS_PATH = '/usr/local/lib/python3.7/site-packages/lkf_addons/addons'


import settings
from uts import get_lkf_api, get_lkf_module



from json_xml import json_to_xml

import simplejson

from settings import *

force_items = {
    "forms":{
        #119180:None,
        # 118588:None,

        },
    "catalogs":{
        #119180:None,
        # 118583:None,
        # 118585:None,
        # 118586:None

 },
    "scripts":{
    # 116098:None

    }
}
items_obj_id = {
    "forms":{
        },
    "catalogs":{
    },
    "scripts":{
    }
}

modules = {'expenses':
                { 'items':{"forms":{},"catalogs":{}, "scripts":{}} }
}

modules = {}


installed_items = {'catalogs': {},'scripts':{}, 'forms':{}}

lkf_modules = None
lkf_api = None

def download_file(url, destination):
    print('destination', destination)
    file_path = destination.split('/')
    file_path.pop(-1)
    file_path = '/'.join(file_path)
    os.makedirs(file_path, exist_ok=True)
    urllib.request.urlretrieve(url, destination)

def download_modules(modules, options, items_ids={}, download_related=False):
    global lkf_api, lkf_modules, module_name, items
    if items_ids:
        items = items_ids
        modules = list(items.keys())
    else:
        lkf_modules = get_lkf_module()
        set_module_items(modules)
    lkf_api = get_lkf_api()
    for module_name in modules:
        if 'forms' in options or 'form' in options:
            print('Download Related Forms : ', download_related)
            get_forms(force_items['forms'], download_related=download_related)
        if 'catalogs' in options or 'catalog' in options:
            print('------------------')
            get_catalogs(force_items['catalogs'], download_related=download_related)
        if 'scripts' in options or 'script' in options:
            get_scripts(force_items['scripts'])

def drop_hashKey(catalog_json):
    res = {}
    if isinstance(catalog_json, dict):
        for key, value in catalog_json.items():
            if isinstance(value, list):
                if len(value) > 0:
                    rlist = []
                    for y in value:
                        rlist.append(drop_hashKey(y))
                    key = update_key(key)
                    res.update({key:rlist})
                else:
                    if not key =='$$hashKey':
                        key = update_key(key)
                        res.update({key:value})
            elif type(value) ==dict:
                if len(value) > 0:
                    key = update_key(key)
                    res.update({key:drop_hashKey(value)})
                else:
                    if not key =='$$hashKey':
                        key = update_key(key)
                        res.update({key:value})
            else:
                if not key =='$$hashKey':
                    key = update_key(key)
                    res.update({key:value})
    elif type(catalog_json) == list:
        if len(catalog_json) > 0:
            zlist = []
            for x in catalog_json:
                zlist.append(drop_hashKey(x))
            return zlist
    else:
        if not catalog_json =='$$hashKey':
            return catalog_json
    return res

def get_catalogs(download_catalogs={}, download_related=False):
    print('Fetching catalogs...')
    global items, installed_items
    if not download_catalogs:
        download_catalogs = deepcopy(items['catalogs'])
    print('Downloading Catalogs : ',download_catalogs)
    for catalog_id, catalog_name in download_catalogs.items():
        print('\n')
        catalog_name = get_item_name('catalogs', catalog_id)
        print(f'Downloading Catalog Name: {catalog_name} with id: {catalog_id}')
        catalog_json = lkf_api.get_catalog_id_fields(catalog_id, jwt_settings_key='JWT_KEY')
        if not catalog_json.get('catalog'):
            print(f'Catalog : {catalog_name} NOT found')
            print('Skipping its download')
            continue
        catalog_json = catalog_json.get('catalog')
        if catalog_json.get('fields'):
            catalog_json.pop('fields')
        res = drop_hashKey(catalog_json)
        # print('res=',simplejson.dumps(res, indent=4))  
        catalog_data_xml = json_to_xml(res)
        # print('catalog_data_xml',catalog_data_xml)  
        save_catalog_xml(catalog_data_xml, catalog_name)
    installed_items['catalogs'].update(download_catalogs)
    if download_related:
        get_new_items('catalogs')

def get_forms(download_forms={}, download_related=False):
    global items
    if not download_forms:
        download_forms = deepcopy(items['forms'])
    for form_id in list(download_forms.keys()):
        form_name = get_item_name('forms', form_id)
        print('\n')
        print(f'Downloading form: {form_name} with id: {form_id}')
        form_data_json = lkf_api.get_form_to_duplicate(form_id, jwt_settings_key='JWT_KEY')
        if not form_data_json:
            print('************* WARNING ************* : Form_id not found', form_id)
            continue
        if form_data_json.get('fields'):
            form_data_json.pop('fields')
        try:
            form_data_json = drop_hashKey(form_data_json)
            form_data_xml = json_to_xml(form_data_json)
        except:
            self.LKFException(form_data_json)

        save_form_xml(form_data_xml, form_name)
        rules_json = lkf_api.get_form_rules(form_id, jwt_settings_key='JWT_KEY')
        if isinstance(rules_json, list):
            if rules_json and len(rules_json) > 0:
               rules_xml = json_to_xml(rules_json[0])
               save_rule_xml(rules_xml, form_name)
        workflow_json = lkf_api.get_form_workflows(form_id, jwt_settings_key='JWT_KEY')
        if isinstance(workflow_json, list):
            if workflow_json and len(workflow_json) > 0:
                workflow_xml = json_to_xml(workflow_json[0])
                save_workflow_xml(workflow_xml, form_name)
        # print('workflow_json=workflow_json',workflow_json)
    installed_items['forms'].update(download_forms)
    if download_related:
        print('\n')
        print('>>>>>>>>>>>>>>>>>> Downloading Related Files <<<<<<<<<<<<<<<<<<<<<<<')
        get_new_items('forms')
        get_new_items('catalogs')
        get_new_items('scripts')

def get_new_items(item_type):
    global items, installed_items
    new_items = deepcopy(items[item_type])
    for item_id in list(installed_items[item_type].keys()):
        new_items.pop(item_id)
    if new_items:
        if item_type == 'catalogs':
            get_catalogs(new_items)
        elif item_type == 'forms':
            get_forms(new_items)

def get_item_name(item_type, item_id=None, element=None, attribute='name', item_obj_id=None):
    global items, items_obj_id
    if item_obj_id:
        item = items_obj_id.get(item_type,{})
        if item.get(item_obj_id) and item[item_obj_id]:
            return item[item_obj_id]
        else:
            catalog_name = lkf_modules.get_item_name_obj_id(item_obj_id, 'catalog')
            cname = None
            for name in catalog_name:
                cname = name.get('item_name')
            if cname:
                return cname
            return None
    item_id = int(float(item_id))
    item = items.get(item_type,{})
    item_name = None
    if item.get(item_id) and item[item_id]:
        return item[item_id]
    elif element:
        label = element.find(attribute)
        if label:
            item_name = label.text
    if not item_name:
        item_type_dict = {'catalogs':'catalog','scripts':'script', 'forms':'form', 'reports':'report'}
        item_obj = lkf_api.get_item(item_id, item_type_dict[item_type])
        item_obj = item_obj.get('data',[])
        item_json={}
        if item_obj and len(item_obj) > 0:
            try:
                item_json = item_obj[0]
            except:
                msg = f"Something went wrong, plese check that the item_id: {item_id} "
                msg += "The most common thing here is that the id does not exists and someone is seraching for it"
                msg += "See who is tring to search form it!!!"
                print('msg',  msg)
                raise BaseException(msg)
        item_name = item_json.get('name', 'no_name')
    item_name = strip_chaaracters(item_name)
    items[item_type][item_id] = item_name
    return item_name

def get_scripts(download_scritps={}):
    global items
    account_id = settings.config["ACCOUNT_ID"]
    global module_name
    if not download_scritps:
        download_scritps = deepcopy(items['scripts'])
    for script_id, script_name in download_scritps.items():
        print('Download Script: ',script_name)
        script_data_json = lkf_api.get_item(script_id, 'script', jwt_settings_key='JWT_KEY')
        script_obj = script_data_json.get('data',[])
        if script_obj and len(script_obj) > 0:
            complete_name = script_obj[0].get('name')
            destination = f'{MODULES_PATH}/{module_name}/items/scripts/_downloads/{complete_name}'
            url = "https://f001.backblazeb2.com/file/app-linkaform/public-client-{}/scripts/{}".format(account_id, complete_name)
            download_file(url, destination)
    return True

def save_form_xml(xml_data, form_name):
    global items, module_name
    tree = ET.ElementTree(ET.fromstring(xml_data))
    root = tree.getroot()
    # print('dir' ,dir(element))
    if root.findall("form_pages"):
        for page in root.find('form_pages'):
            fields = page.find('page_fields')
            for field in list(fields):
                is_catalog = False
                catalog_element = field.find('catalog')
                for cprop in list(catalog_element):
                    is_catalog = True
                    if cprop.tag == 'catalog_id':
                        catalog_name = get_item_name('catalogs', cprop.text, field, attribute='label')
                        cprop.text = "{{ catalog." + catalog_name + ".id }}"
                        field_type = field.find('field_type')
                        if field_type.text == 'catalog':
                            field_id = field.find('field_id')
                            field_id.text = "{{ catalog." + catalog_name + ".obj_id }}"
                        else:
                            catalog_field_id = catalog_element.find('catalog_field_id')
                            if catalog_field_id != None and catalog_field_id.text != None:
                                catalog_field_id.text = "{{ catalog." + catalog_name + ".obj_id }}"

    #a = tree.write(f'{MODULES_PATH}/{module_name}/items/forms/downloads/{form_name}.xml', encoding="utf-8", xml_declaration=True)
    file_name = f'{form_name}.xml'
    save_file(tree, module_name, 'forms', file_name)
    return True

def save_catalog_xml(xml_data, form_name):
    global items, module_name
    tree = ET.ElementTree(ET.fromstring(xml_data))
    root = tree.getroot()
    # print('dir' ,dir(element))
    if root.findall("catalog_pages"):
        for page in root.find('catalog_pages'):
            page_items = page.find('page_fields')
            for fitems in list(page_items):
                is_catalog = False
                field_type = fitems.find('field_type')
                if field_type.tag == 'field_type' and field_type.text =='catalog':
                    is_catalog = True
                catalog_element = fitems.findall('catalog')
                if catalog_element != None:
                    for catalog in list(catalog_element):
                        catalog_id = catalog.find('catalog_id')
                        if catalog_id != None:
                            catalog_name = get_item_name('catalogs', catalog_id.text, catalog, attribute='name')
                            catalog_id.text = "{{ catalog." + catalog_name + ".id }}"

                for fields in list(fitems):
                    if fields.tag == 'field_id' and is_catalog:
                        fields.text = "{{ catalog." + catalog_name + ".obj_id }}"
                    if fields.tag == 'catalog':
                        for catalog_element in list(fields):
                            if catalog_element.tag == 'couch_id':
                                catalog_element.text = "{{ catalog." + catalog_name + ".obj_id }}"
                            if not is_catalog:
                                if catalog_element.tag == 'catalog_field_id':
                                    if catalog_element.text != None:
                                        catalog_element.text = "{{ catalog." + catalog_name + ".obj_id }}"
                            if catalog_element.tag == 'name':
                                catalog_element.text = "{{ catalog." + catalog_name + ".name }}"
    #tree.write(f'{MODULES_PATH}/{module_name}/items/catalogs/downloads/{form_name}.xml', encoding="utf-8", xml_declaration=True)
    file_name = f'{form_name}.xml'
    save_file(tree, module_name, 'catalog', file_name)
    return True

def save_file(tree, module_name, item_type, file_name):
    file_path = f'{MODULES_PATH}/{module_name}/items/{item_type}/_downloads'
    try:
        os.makedirs(file_path, exist_ok=True)
    except OSError as e:
        # Handle the error in case of any other OS related issues
        msg = f"Error creating directory {file_path} msg: {e}"
        raise(msg)
    print('saving file on .... ', f'{file_path}/{file_name}')
    tree.write(f'{file_path}/{file_name}', encoding="utf-8", xml_declaration=True)
    return True

def save_rule_xml(xml_data, form_name):
    global module_name
    tree = ET.ElementTree(ET.fromstring(xml_data))
    root = tree.getroot()
    form_id = root.find('form_id')
    form_id.text = "{{ form." + form_name + ".id }}"
    if root.findall("rules"):
        for rules in root.find('rules'):
            for r in list(rules):
                if r.tag == 'fields_ruled':
                    for frules in list(r):
                        etype = frules.find('type')
                        if etype.tag == 'type' and etype.text =='catalog':
                            field_id = frules.find('field_id')
                            catalog_field_id = field_id.text
                            # catalog_name = lkf_modules.get_item_name_obj_id(catalog_field_id, 'catalog')
                            catalog_name = get_item_name('catalogs', item_obj_id=catalog_field_id, element=field_id)
                            #print('catalog_field_id', catalog_field_id)
                            #print('catalog_name', catalog_name)
                            # cname = None
                            # for name in catalog_name:
                            #     cname = name.get('item_name')
                            if not catalog_name:
                                elable = frules.find('label')
                                catalog_name = elable.text
                            field_id.text = "{{ " + f"catalog.{catalog_name}.obj_id" + "}}"
                            #print('field txt', "{{ " + f"catalog.{catalog_name}.obj_id" + "}}")

    # tree.write(f'{MODULES_PATH}/{module_name}/items/forms/downloads/{form_name}_rules.xml', encoding="utf-8", xml_declaration=True)
    file_name = f'{form_name}_rules.xml'
    save_file(tree, module_name, 'forms', file_name)
    return True

def save_workflow_xml(xml_data, form_name):
    global module_name, items
    tree = ET.ElementTree(ET.fromstring(xml_data))
    root = tree.getroot()
    form_id = root.find('form_id')
    form_id.text = "{{ form." + form_name + ".id }}"
    workflows = root.find('workflows')
    for workflow in list(workflows):
        for w_items in workflow:
            for actions in w_items.iter('actions'):
                #seaches on every action type and replaces values
                for action in actions:
                    config = action.find('configuration')
                    body = config.find('body')
                    if hasattr(body,'text'):
                        body.text = "{% raw %} " + body.text + " {% endraw %}" 
                    subject = config.find('subject')
                    if hasattr(subject,'text'):
                        subject.text = "{% raw %} " + subject.text + " {% endraw %}" 
                    for script in config.iter('script'):
                        script_id = script.find('id')
                        script_name = get_item_name('scripts', script_id.text, script, attribute='name')
                        script_id.text = "{{ script." + script_name + ".id }}"
                        script_name_tag = script.find('name')
                        script_name_tag.text = "{{ script." + script_name + ".name }}"
                    for form in config.iter('form'):
                        form_id = form.find('id')
                        this_form_name = get_item_name('forms', form_id.text, form)
                        form_id.text = "{{ form." + this_form_name + ".id }}"
                        form_name_tag = form.find('name')
                        form_name_tag.text = "{{ form." + this_form_name + ".name }}"
                    itype = None
                    for catalog in config.iter('catalog'):
                        #FORM2CATALOG
                        if not itype:
                            for catalog_elem in list(catalog):
                                if catalog_elem.tag == 'itype':
                                    itype = catalog_elem.text
                        if itype == 'form':
                            form_id = catalog.find('form_id')
                            this_form_name = get_item_name('forms', form_id.text, catalog)
                            form_id.text = "{{ form." + this_form_name + ".id }}"
                        elif itype == 'catalog':
                            catalog_id = catalog.find('id')
                            catalog_name = get_item_name('catalogs', catalog_id.text, catalog, attribute='name')
                            catalog_id.text = "{{ catalog." + catalog_name + ".id }}"
                            catalog_name_tag = catalog.find('name')
                            catalog_name_tag.text = "{{ catalog." + catalog_name + ".name }}"
                            couch_id = catalog.find('couch_id')
                            couch_id.text = "{{ catalog." + catalog_name + ".obj_id }}"
                            resource_uri = catalog.find('resource_uri')
                            resource_uri.text = "/api/infosync/get_catalogs/" + "{{ catalog." + catalog_name + ".id }}" + "/"
                    for assign in config.iter('assignTo'):
                        catalog_field_id = assign.find('catalog_field_id')
                        if catalog_field_id and catalog_field_id.text:
                            catalog_name = get_item_name('catalogs', item_obj_id=catalog_field_id.text, element=catalog_field_id)
                            catalog_field_id.text = "{{ catalog." + catalog_name + ".obj_id }}"
                        #TODO DO: Si tiene un custom user , gravarlo en carpeta private
                        # for customUser in assign.iter('customUser'):
                        #     try:
                        #         user_id = customUser.find('id')
                        #         user_id.text = user_id.text
                        #     except:
                        #         print('no user id found on workflow')
                        #     user_first_name = customUser.find('first_name')
                        #     # user_first_name.text = settings.config["USER"]['first_name']
                        #     user_first_name.text = user_first_name.text

                        #     user_email = customUser.find('email')
                        #     # user_email.text = settings.config["USER"]['email']
                        #     user_email.text = user_email.text
                            
                        #     user_username = customUser.find('username')
                        #     # user_username.text = settings.config["USER"]['username']
                        #     user_username.text = user_username.text
                    for synched_catalogs in config.iter('synched_catalogs'):
                        for item in synched_catalogs.iter('item'):
                            catalog_id = item.find('id')
                            catalog_obj_id = item.find('couch_id')
                            catalog_name = get_item_name('catalogs', catalog_id.text, catalog_id, attribute='name')
                            catalog_id.text = "{{ catalog." + catalog_name + ".id }}"
                            catalog_obj_id.text = "{{ catalog." + catalog_name + ".obj_id }}"
            for rules in w_items.iter('rules'):
                for wf_fields in rules.iter('wf_fields'):
                    for triggers in wf_fields.iter('triggers'):
                        for trigger in triggers.iter('item'):
                            trigger_field = trigger.find('trigger_field')
                            for trig_cat in trigger_field.iter('catalog'):
                                cat_id = trig_cat.find('catalog_id')
                                if cat_id != None and cat_id.text:
                                    catalog_name = get_item_name('catalogs', cat_id.text, trig_cat, attribute='label' )
                                    cat_id.text = "{{ catalog." + catalog_name + ".id }}"
                                    catalog_field_id = trig_cat.find('catalog_field_id')
                                    catalog_field_id.text = "{{ catalog." + catalog_name + ".obj_id }}"
    
    #tree.write(f'{MODULES_PATH}/{module_name}/items/forms/downloads/{form_name}_workflow.xml', encoding="utf-8", xml_declaration=True)
    file_name = f'{form_name}_workflow.xml'
    save_file(tree, module_name, 'forms', file_name)
    return True

def set_module_items(set_modules):
    global items, modules, items_obj_id
    module_items = lkf_modules.fetch_installed_modules()
    for module in set_modules:
        modules[module] = modules.get(module,{ 
                    'items':{"forms":{},"catalogs":{}, "scripts":{}} ,
                    'items_obj_id':{"forms":{},"catalogs":{}, "scripts":{}} ,
                    })
        for itm in module_items:
            if itm.get('module') == module:
                if itm['item_type'] == 'form':
                    modules[module]['items']['forms'][itm['item_id']] = itm['item_name']
                if itm['item_type'] == 'script':
                    modules[module]['items']['scripts'][itm['item_id']] = itm['item_name']
                if itm['item_type'] == 'catalog':
                    modules[module]['items']['catalogs'][itm['item_id']] = itm['item_name']
                    if itm.get('item_obj_id'):
                        modules[module]['items_obj_id']['catalogs'][itm['item_obj_id']] = itm['item_name']
        items = modules[module]['items']
        items_obj_id = modules[module]['items_obj_id']
        return True

def strip_chaaracters(string):
    pattern = r'[^a-zA-Z0-9_]'
    string = string.replace(' ','_').replace('.py','')
    stripped_string = re.sub(pattern, '', string)
    stripped_string = stripped_string.replace('__','_')
    return stripped_string.lower()

def update_key(key):
    key = key.replace('$','amp_')
    if type(key) == str:
        is_int = False
        try:
            int(key[0])
            is_int = True
        except:
            pass
        if is_int:
            key = 'num_{}'.format(key)
    elif type(key) == int or type(key) == float:
        key = 'num_{}'.format(key)
    return key
