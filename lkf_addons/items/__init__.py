
# coding: utf-8

import subprocess, simplejson, os, glob
from pathlib import Path
import xml.etree.ElementTree as ET

from linkaform_api import utils, lkf_models
from linkaform_api.lkf_object import LKFBase 

ADDONS_PATH = '/usr/local/lib/python3.10/site-packages/lkf_addons/addons'
MODULES_PATH = '/srv/scripts/addons/modules'

default_image = 'linkaform/python3_lkf:latest'


class LKFException(BaseException):
    def __init__(self, message, res=None):
        self.message = message + 'tset'

    def LKFException(self, msg):
        return BaseException(msg)

class Items(LKFException):

    def __init__(self, path, module, settings, load_data=False, load_demo=False, **kwargs):
        self.path = path
        self.module = module
        self.lkf_api = utils.Cache(settings)
        self.settings = settings
        self.lkf = lkf_models.LKFModules(self.settings)
        self.load_data = load_data
        self.load_demo = load_demo
        self.module_files = {}
        # self.LKFException()
        # self.lkf.get_installed_modues()

    def alter_element(self, position, search_element, new_element, target_item, index=None):
        if type(new_element) != list:
            new_element = list(new_element)
        if position == 'remove':
            search_element.remove(target_item)
        else:
            for elem in new_element:
                if position == 'after':
                    index += 1
                    search_element.insert(index, elem)
                elif position == 'before':
                    search_element.insert(index, elem)
                    index += 1
                elif position == 'replace':
                    index = list(search_element).index(target_item)
                    position = 'after'
                    search_element.remove(target_item)
                    search_element.insert(index, elem)
                else:
                    msg = f'Incorrect position: {position} , given.'
                    msg += ' Please check you inherit file and asure that position is set to before or after'
                    return self.LKFException(msg)
        return search_element

    # def apply_xml_inherits(self, itype, module_path, file_name, file_data, xml_file):
    #     print('seraching for inherit files...')
    #     print('file name', file_name)
    #     if '{}_inherit.xml'.format(file_name) in self.module_files[itype][module_path]:
    #         print('vamos a heredar....', file_name)
    #         inherit_xml = self.lkf.read_template_file(module_path, f'{file_name}.xml', file_data)
    #     print('file inherit_xml', inherit_xml)
    #     print('file name', file_named)

    def do_file_inherits(self, file_path, file_name, search_file_path, extension='xml'):
        modules_path = file_path.replace(ADDONS_PATH, MODULES_PATH)
        serach_inherit = f'{modules_path}/{file_name}_inherit*.{extension}'
        base_file_path = f'{search_file_path}/{file_name}.{extension}' 
        inherit_files = glob.glob(serach_inherit)
        if inherit_files:
            print('aqui estan los heredados', inherit_files)
            print('TODO AQUI HAY QUE BUSCAR EN LOS ARCHIVOS DE TODOS LOS MODULOS INSTALADOS....')
        for in_file in inherit_files:
            replace_childs = self.get_child_element_from_file(in_file, 'inherit')
            inherit_attr = self.get_inherit_attributes(in_file)
            base_file_path = self.add_new_item(base_file_path, replace_childs, inherit_attr, tmp_dir='_tmp')   
        return base_file_path

    def file_exists(self, file_path, file_name, extension):
        complete_path = '{}/{}.{}'.format(file_path, file_name, extension)
        return os.path.exists(complete_path)
        # print('migrate fuciotn to use os')
        # print('migrate fuciotn to use os', stop)
        # cmd = ['ls', '{}/{}.{}'.format(file_path, file_name, extension)]
        # process = subprocess.Popen(args=cmd,
        #     stdout=subprocess.PIPE,
        #     stderr=subprocess.PIPE)
        # output, error = process.communicate()
        # if output:
        #     return True

    def get_inherit_attributes(self, inherit_file_path):
        # Load the XML file
        tree = ET.parse(inherit_file_path)
        root = tree.getroot()
        # Find the 'inherit' element
        inherit = root.find('.//inherit')
        if inherit is None:
            msg = "No 'inherit' elemendddddddddddddddddddt found"
            return self.LKFException(msg)
        # Extract all attributes of the 'inherit' element
        attributes = inherit.attrib
        return attributes

    def add_new_item(self, file_path, new_element, inherit_attr, tmp_dir=True):
        # Load the XML file
        """
        Agrega nuevo elemento xml a docuemnto existente y lo guarda en carpeta tmp, siguiendo los atributios de inherit_attr.

        Parameters:
            file_path (str): The path to the XML file from which to extract the 'inherit' element attributes.
            new_element (Element): New element to inherit on the given position
            inherit_attr (dict):
                position: after, before, replace, remove
                search_element: Element in wich the fuction is going to search for a match
                in_element: If the element to search is inside an element
                search_text: if you need to search for a given element with a given text
                parent: indicates if all this happens inside a given attribute

        Returns:
            The xml file resulting of the juntion

        Raises:

        Example:
        """
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
        except Exception as e:
            msg = f'Bad xml format: {e}'
            print('msg', msg)
            return self.LKFException(msg)

        if not inherit_attr.get('search_element'):
            msg = f'Search_element is a requierd argument on inherit_att'
            print('msg', msg)
            return self.LKFException(msg)
        if not inherit_attr.get('position'):
            msg = f'Position is a requierd argument on inherit_att'
            print('msg', msg)
            return self.LKFException(msg)

        s_element = inherit_attr['search_element']
        position = inherit_attr['position']

        in_element = inherit_attr.get('in_element')
        # Find all 'item' elements under 'search_element' (this is where the items are nested)
        if inherit_attr.get('parent'):
            x = inherit_attr.get("parent")
            search_element = root.find(f'.//{x}')
            if search_element is None:
                msg =  "No 'page_fields' found"
                return self.LKFException(msg)
        else:
            search_element = root

        target_item = None
        if in_element:
            search_text = inherit_attr.get('search_text')
            if search_text:
                for item in search_element.findall(f'.//{inherit_attr.get("in_element")}'):
                    if item.find(f'./{s_element}').text == search_text:
                        target_item = item
                        break
                index = list(search_element).index(target_item)
            else:
                #sets new search element base on the in element
                search_element = search_element.find(f'.//{in_element}')
                target_item = search_element.find(s_element)
                index = list(search_element).index(target_item)
        else:
            target_item = search_element.find(f'.//{s_element}')
            index = list(search_element).index(target_item)


        if target_item is None:
            msg = f"No item with the attributes {inherit_attr} found"
            return self.LKFException(msg)

        # Insert the new element after the found target item
        search_element = self.alter_element(position, search_element, new_element, target_item, index=index)
        # Save the modified XML back to the file
        save_path = file_path.split('/')
        if tmp_dir and tmp_dir not in save_path:
            save_path.insert(-1, tmp_dir)
        save_path = '/'.join(save_path)
        self.create_folder_for_file_if_not_exists(save_path)
        tree.write(save_path, encoding='utf-8', xml_declaration=True)
        return save_path

    def alter_element(self, position, search_element, new_element, target_item, index=None):
        if type(new_element) != list:
            new_element = list(new_element)
        if position == 'remove':
            search_element.remove(target_item)
        else:
            for elem in new_element:
                if position == 'after':
                    index += 1
                    search_element.insert(index, elem)
                elif position == 'before':
                    search_element.insert(index, elem)
                    index += 1
                elif position == 'replace':
                    index = list(search_element).index(target_item)
                    position = 'after'
                    search_element.remove(target_item)
                    search_element.insert(index, elem)
                else:
                    msg = f'Incorrect position: {position} , given.'
                    msg += ' Please check you inherit file and asure that position is set to before or after'
                    return self.LKFException(msg)
        return search_element

    def create_folder_for_file_if_not_exists(self, file_path):
        """
        Creates a directory for the given file path if it does not exist.
        
        Parameters:
            file_path (str): The full file path including the filename.
        
        Returns:
            None
        """
        # Extract the directory part from the full file path
        directory = os.path.dirname(file_path)

        try:
            # Attempt to create the directory, ignoring the error if it already exists
            os.makedirs(directory, exist_ok=True)
            msg = f"Folder created for the file at: {directory}"
        except OSError as e:
            # Handle the error in case of any other OS related issues
            msg = f"Error: {e}"
            self.LKFException(msg)
        return True

    def file_path_to_load(self,  file_name, detail):
        if detail.get('path'):
            file_path = '{}/{}'.format(self.path, detail['path'])
        else:
            file_path = self.path
        modules_path = file_path.replace(ADDONS_PATH, MODULES_PATH)
        if self.file_exists(modules_path, file_name, 'py'):
            search_file_path = '{}/{}.{}'.format(modules_path, file_name, 'py')
        elif self.file_exists(file_path, file_name, 'py'):
            # print('los scripts que estan en addons path no se instalan ya que viven como libreria dentro del contendedr')
            # search_file_path = '{}/{}.{}'.format(file_path, file_name, 'py')
            search_file_path = None
        else:
            search_file_path = None
        return search_file_path

    def get_child_element(self, parent_xml, child_tag):
        """
        Retrieves the first child element with the specified tag from the given parent XML element.

        Parameters:
            parent_xml (ET.Element): The parent XML element from which to find the child.
            child_tag (str): The tag name of the child element to retrieve.

        Returns:
            ET.Element: The first child element with the specified tag. Returns None if no such child is found.

        Example:
            # Example XML structure
            xml_string = '''
            <root>
                <child1>Value1</child1>
                <child2>Value2</child2>
            </root>
            '''
            root = ET.fromstring(xml_string)
            child1 = get_child_element(root, 'child1')
            if child1 is not None:
                print(child1.text)  # Output: Value1
        """
        # Find the first child element with the specified tag
        child_element = parent_xml.find(child_tag)
        return child_element

    def get_child_element_from_file(self, file_path, child_tag):
        """
        Retrieves the first child element with the specified tag from the XML file.
        
        Parameters:
            file_path (str): The path to the XML file from which to find the child element.
            child_tag (str): The tag name of the child element to retrieve.
        
        Returns:
            ET.Element: The first child element with the specified tag. Returns None if no such child is found.
        
        Raises:
            FileNotFoundError: If the XML file does not exist at the specified path.
            ET.ParseError: If the XML file is not well-formed and cannot be parsed.
        
        Example:
            # Assuming 'example.xml' contains:
            # <root>
            #     <child1>Value1</child1>
            #     <child2>Value2</child2>
            # </root>
            child_element = get_child_element_from_file('example.xml', 'child1')
            if child_element is not None:
                print(child_element.text)  # Output: Value1
        """
        try:
            # Load the XML file
            tree = ET.parse(file_path)
            root = tree.getroot()
        except FileNotFoundError:
            raise FileNotFoundError("The file specified does not exist.")
        except ET.ParseError:
            raise ET.ParseError("Failed to parse XML. The file may not be well-formed.")

        # Find the first child element with the specified tag
        parent_element = root.find(child_tag)
        child_element = root.find(child_tag)
        if parent_element is not None:
            # Return all children of the found element
            return list(parent_element)

    # def get_inherit_attributes(self, inherit_file_path):
    #     # Load the XML file
    #     print('es est...............')
    #     tree = ET.parse(inherit_file_path)
    #     print('inherit_file_path',inherit_file_path)
    #     root = tree.getroot()
    #     # Find the 'inherit' element
    #     inherit = root.find('.//inherit')
    #     if inherit is None:
    #         msg = "No 'inherit' element found"
    #         return self.LKFException(msg)
    #     # Extract all attributes of the 'inherit' element
    #     attributes = inherit.attrib
    #     return attributes

    def load_module_template_file(self, file_path, file_name, file_data=None, inherit_attr={}):
        modules_path = file_path.replace(ADDONS_PATH, MODULES_PATH)
        if self.file_exists(modules_path, file_name, 'xml'):
            search_file_path = modules_path
        else:
            search_file_path = file_path
        xml_exists = self.file_exists(file_path, file_name, 'xml')
        json_file = None
        if xml_exists:
            full_file_path = self.do_file_inherits(file_path, file_name, search_file_path, 'xml')
            file_path = full_file_path.replace(f'{file_name}.xml','')
            json_file = self.lkf.read_template_file(file_path, f'{file_name}.xml', file_data)
            # json_file = self.read_xml_template(file_path, )
            json_file = self.lkf.lkf_api.xml_to_json(json_file)
        elif self.file_exists(search_file_path, file_name, 'xml'):
            json_file = self.lkf.read_template_file(search_file_path, f'{file_name}.xml', file_data)
            json_file = self.lkf.lkf_api.xml_to_json(json_file)
        elif self.file_exists(file_path, file_name, 'json'):
            json_file = open('./{}/{}.json'.format(file_path, file_name))
            json_file = simplejson.load(json_file)
        return json_file
            

        #     print(stop_and_cjheck)
        #     search_element = root

        # target_item = None
        # if in_element:
        #     search_text = inherit_attr.get('search_text')
        #     if search_text:
        #         for item in search_element.findall(f'.//{inherit_attr.get("in_element")}'):
        #             if item.find(f'./{s_element}').text == search_text:
        #                 target_item = item
        #                 break
        #         index = list(search_element).index(target_item)
        #     else:
        #         #sets new search element base on the in element
        #         search_element = search_element.find(f'.//{in_element}')
        #         target_item = search_element.find(s_element)
        #         index = list(search_element).index(target_item)
        # else:
        #     raise LKFException('No file with name: {} found, at path: {}'.format(file_name, file_path))

    def merge_addons_modules(self, list1, list2):
        result = []
        # Helper function to find if a dictionary exists in the result and returns its index
        def find_dict_in_list(dict_item, list_of_items):
            for index, item in enumerate(list_of_items):
                if isinstance(item, dict) and item.keys() == dict_item.keys():
                    return index
            return -1
        # Function to merge two dictionaries
        def merge_dicts(dict1, dict2):
            for key in dict2:
                if key in dict1:
                    # Assuming values in these dictionaries are lists
                    dict1[key] = list(set(dict1[key] + dict2[key]))
                else:
                    dict1[key] = dict2[key]
            return dict1
        # Add items from both lists into result
        for item in list1 + list2:
            if isinstance(item, dict):
                idx = find_dict_in_list(item, result)
                if idx >= 0:
                    result[idx] = merge_dicts(result[idx], item)
                else:
                    result.append(item)
            elif item not in result:
                result.append(item)
        return result

    def get_anddons_and_modules_items(self, itype, sub_dir=None):
        res_addons = self.get_all_items_json(itype, sub_dir=sub_dir, path=ADDONS_PATH)
        res_modules = self.get_all_items_json(itype, sub_dir=sub_dir, path=MODULES_PATH)
        addons_modules = self.merge_addons_modules(res_addons,res_modules)
        return addons_modules

    def get_all_items_json(self, itype, sub_dir=None, path=MODULES_PATH):
        search_path = f'{path}/{self.module}/items/{itype}/'
        if sub_dir:
            search_path += f'{sub_dir}/'
            # cmd[1] = cmd[1] + '{}/'.format(sub_dir)
        search_res = Path(search_path)
        try:
            output = [file.name for file in search_res.iterdir()]
        except:
            return []
        # process = subprocess.Popen(args=cmd,
        #     stdout=subprocess.PIPE,
        #     stderr=subprocess.PIPE)
        # ff = [file.name for file in path.iterdir() if file.is_file()]
        # output, error = process.communicate()
        res = []
        if output:
            for y in output:
                # y = x.decode('utf-8')
                if '_inherit' in y:
                    continue
                if y == 'i18n':
                    continue
                if y[:1] == '_':
                    continue
                    if y.find('.pyc') > 0:
                        continue 
                if y.find('.') < 0:
                    this_level = {y:[]}
                    if sub_dir:
                        l_sub_dir = '{}/{}'.format(sub_dir, y)
                    else:
                        l_sub_dir = y
                    this_level[y] += self.get_all_items_json(itype, path=path, sub_dir=l_sub_dir)
                    if this_level[y]:
                        res.append(this_level)
                if y.find('.json') > 0:
                    res.append(y)
                if y.find('.xml') > 0:
                    res.append(y)
                if y.find('.csv') > 0:
                    res.append(y)
                if y.find('.py') > 0:
                    res.append(y)
        return res

    def get_module_items(self):
        return self.lkf.get_module_items(self.module)

    def delete_item(self, item_id):
        return self.lkf_api.delete_item(item_id)

    def remove_module_items(self, remove_items):
        return self.lkf.remove_module_items(remove_items)