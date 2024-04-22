
# coding: utf-8

import subprocess, simplejson

from linkaform_api import utils, lkf_models

default_image = 'linkaform/python3_lkf:latest'


class LKFException(BaseException):
    def __init__(self, message, res=None):
        self.message = message + 'tset'

    def LKFException(self, msg):
        return BaseException(msg)

class Items(LKFException):

    def __init__(self, path, module, settings, load_data=False, load_demo=False):
        self.path = path
        self.module = module
        self.lkf_api = utils.Cache(settings)
        self.settings = settings
        self.lkf = lkf_models.LKFModules(self.settings)
        self.load_data = load_data
        self.load_demo = load_demo
        # self.LKFException()
        # self.lkf.get_installed_modues()

    def load_items_file(file_type, file, extension):
        print('TODO DO READ FILE TYPE, FILES AND EXTENSIONS')
        print('and load file to lkf on it respective module')

    def file_exists(self, file_path, file_name, extension):
        cmd = ['ls', '{}/{}.{}'.format(file_path, file_name, extension)]
        process = subprocess.Popen(args=cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        output, error = process.communicate()
        if output:
            return True
        else:
            return False

    def load_module_template_file(self, file_path, file_name, file_data=None):
        xml_exists = self.file_exists(file_path, file_name, 'xml')
        if xml_exists:
            print('file_data',file_data)
            json_file = self.lkf.read_template_file(file_path, f'{file_name}.xml', file_data)
            # json_file = self.read_xml_template(file_path, )
        elif self.file_exists(file_path, file_name, 'json'):
            json_file = open('./{}/{}.json'.format(file_path, file_name))
            json_file = simplejson.load(json_file)
        else:
            raise LKFException('No file with name: {} found, at path: {}'.format(file_name, file_path))
        return json_file

    def get_all_items_json(self, itype, sub_dir=None):
        # module = __name__.replace('.','/')
        # cmd = ['ls', './{}/{}/'.format(module, itype)]
        cmd = ['ls',  '/srv/scripts/addons/modules/{}/items/{}/'.format(self.module, itype)]
        if sub_dir:
            cmd[1] = cmd[1] + '{}/'.format(sub_dir)
        process = subprocess.Popen(args=cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        output, error = process.communicate()
        res = []
        if output:
            output = output.split()
            for x in output:
                y = x.decode('utf-8')
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
                    this_level[y] += self.get_all_items_json(itype, sub_dir=l_sub_dir)
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