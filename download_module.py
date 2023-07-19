# coding: utf-8

import xml.etree.ElementTree as ET
import xml.dom.minidom
from copy import deepcopy
import urllib.request, re

from uts import get_lkf_api, get_lkf_module

from linkaform_api import utils
import settings


from json_xml import json_to_xml

import simplejson

from settings import *

items = {
    "forms":{
        #stock
        # 98225:None,
        # 94880:None,
        # 94880:None,
        # 98233:None,
        # 98229:None,
        #test
        #104304:None,
        #Viaticos
        # 94192:None,
        # 69620:None,
        # 73387:None
        #Viaticos Local
        # 104478:None, # Autorizacion
        # 104492:None, # Entrga de anticipo
        # 104479:None, # Registro de gastos
        # 104480:None, # solicidud
        },
    "catalogs":{
        # 104534:None,
    },
    "scripts":{
        # 104489:None #expense util
    }
}

modules = {}

installed_items = {'catalogs': {},'scripts':{}, 'forms':{}}

def strip_chaaracters(string):
    pattern = r'[^a-zA-Z0-9_]'
    string = string.replace(' ','_').replace('.py','')
    stripped_string = re.sub(pattern, '', string)
    stripped_string = stripped_string.replace('__','_')
    return stripped_string.lower()

def get_item_name(item_type, item_id, element=None, attribute='name'):
    global items
    item_id = int(item_id)
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
            item_json = item_obj[0]
        item_name = item_json.get('name', 'no_name')
    item_name = strip_chaaracters(item_name)
    items[item_type][item_id] = item_name
    return item_name

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


    tree.write('./{}/items/forms/{}.xml'.format(module_name, form_name), encoding="utf-8", xml_declaration=True)
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
    tree.write('./{}/items/catalogs/{}.xml'.format(module_name, form_name), encoding="utf-8", xml_declaration=True)
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
                            catalog_name = lkf_modules.get_item_name_obj_id(catalog_field_id, 'catalog')
                            cname = None
                            for name in catalog_name:
                                cname = name.get('item_name')
                            if not cname:
                                elable = frules.find('label')
                                cname = elable.text
                            field_id.text = "{{ " + f"catalog.{cname}.obj_id" + "}}"

    

    tree.write('./{}/items/forms/{}_rules.xml'.format(module_name, form_name), encoding="utf-8", xml_declaration=True)
    return True

def save_workflow_xml(xml_data, form_name):
    global module_name
    tree = ET.ElementTree(ET.fromstring(xml_data))
    root = tree.getroot()
    form_id = root.find('form_id')
    form_id.text = "{{ form." + form_name + ".id }}"
    workflows = root.find('workflows')
    for workflow in list(workflows):
        for items in workflow:
            for actions in items.iter('actions'):
                for action in actions:
                    config = action.find('configuration')
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
                        for customUser in assign.iter('customUser'):
                            user_id = customUser.find('id')
                            user_id.text = str(settings.config["USER"]['id'])
                            user_first_name = customUser.find('first_name')
                            user_first_name.text = settings.config["USER"]['first_name']
                            user_email = customUser.find('email')
                            user_email.text = settings.config["USER"]['email']
                            user_username = customUser.find('username')
                            user_username.text = settings.config["USER"]['username']
            for rules in items.iter('rules'):
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
    
    tree.write('./{}/items/forms/{}_workflow.xml'.format(module_name, form_name), encoding="utf-8", xml_declaration=True)
    print('aqui guardo el workflow', './{}/items/forms/{}_workflow.xml'.format(module_name, form_name))
    return True

def get_forms(download_forms={}):
    global items
    if not download_forms:
        download_forms = deepcopy(items['forms'])
    for form_id in list(download_forms.keys()):
        form_name = get_item_name('forms', form_id)
        form_data_json = lkf_api.get_form_to_duplicate(form_id, jwt_settings_key='JWT_KEY')
        if form_data_json.get('fields'):
            form_data_json.pop('fields')
        try:
            form_data_xml = json_to_xml(form_data_json)
        except:
            # print('form_data_json=',simplejson.dumps(form_data_json, indent=4))
            print(stop)

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
    get_new_items('forms')

def download_file(url, destination):
    urllib.request.urlretrieve(url, destination)

def get_scripts(download_scritps={}):
    global items
    account_id = settings.config["ACCOUNT_ID"]
    global module_name
    if not download_scritps:
        download_scritps = deepcopy(items['scripts'])
    for script_id, script_name in download_scritps.items():
        script_data_json = lkf_api.get_item(script_id, 'script', jwt_settings_key='JWT_KEY')
        script_obj = script_data_json.get('data',[])
        if script_obj and len(script_obj) > 0:
            complete_name = script_obj[0].get('name')
            destination = './{}/items/scripts/{}'.format(module_name, complete_name)
            url = "https://f001.backblazeb2.com/file/app-linkaform/public-client-{}/scripts/{}".format(account_id, complete_name)
            print('url=',url)
            download_file(url, destination)
    return True

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

def get_catalogs(download_catalogs={}):
    global items, installed_items
    if not download_catalogs:
        download_catalogs = deepcopy(items['catalogs'])
    for catalog_id, catalog_name in download_catalogs.items():
        print(';catalog name', catalog_name)
        catalog_json = lkf_api.get_catalog_id_fields(catalog_id, jwt_settings_key='JWT_KEY')
        catalog_json = catalog_json.get('catalog')
        if catalog_json.get('fields'):
            catalog_json.pop('fields')
        # import simplejson
        # # print('catalog_json', simplejson.dumps(catalog_json, indent=4))  
        # cc = {
        #     "temp":[],
        #     "3dict_solo":{},
        #     "2test":"testxot",
        #     "5filters": {
        #         "6Liners": {
        #             "$and": [
        #                 {
        #                     "6205f73281bb36a6f1573358": {
        #                         "$eq": "Ln50"
        #                     }
        #                 },
        #                 {
        #                     "6205f73281bb36a6f1573358": {
        #                         "$eq": "Ln72"
        #                     }
        #                 }
        #             ]
        #         }
        #     },
        # }
        if catalog_json.get('filters'):
            print('stop')
            print('stop', stop)
        #     catalog_json.pop('filters')
        res = drop_hashKey(catalog_json)
        # print('res=',simplejson.dumps(res, indent=4))  
        catalog_data_xml = json_to_xml(res)
        # print('catalog_data_xml',catalog_data_xml)  
        save_catalog_xml(catalog_data_xml, catalog_name)
    installed_items['catalogs'].update(download_catalogs)
    get_new_items('catalogs')

def get_new_items(item_type):
    global items, installed_items
    new_items = deepcopy(items[item_type])
    for item_id in list(installed_items[item_type].keys()):
        new_items.pop(item_id)
    print('new_items', new_items)
    if new_items:
        if item_type == 'catalogs':
            get_catalogs(new_items)
        elif item_type == 'forms':
            get_forms(new_items)

def set_module_items():
    global items, modules
    module_items = lkf_modules.fetch_installed_modules()
    for itm in module_items:
        module = itm['module']
        modules[module] = modules.get(module,{ 'items':{"forms":{},"catalogs":{}, "scripts":{}} })
        if itm['item_type'] == 'form':
            modules[module]['items']['forms'][itm['item_id']] = itm['item_name']
        items = modules[module]['items']
    return True

if __name__ == "__main__":

    # settings.config["USERNAME"] = USERNAME
    # lkf_api = utils.Cache(settings)
    # user = lkf_api.get_jwt(api_key=settings.config['APIKEY'], get_user=True)
    # settings.config["JWT_KEY"] = user.get('jwt')
    # settings.config["ACCOUNT_ID"] = user['user']['parent_info']['id']
    # settings.config["USER"] = user['user']
    lkf_api = get_lkf_api()
    lkf_modules = get_lkf_module()
    set_module_items()
    for module_name in modules:
        print('module_name=', module_name)
        get_forms()
        get_catalogs()
        print('asi va items', items)
        #get_scripts()

