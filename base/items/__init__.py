
# coding: utf-8

import subprocess, simplejson

from linkaform_api import utils, lkf_models

default_image = 'linkaform/python3_lkf:latest'

print('------------------------')

class LKFException(BaseException):
    def __init__(self, message, res=None):
        self.message = message + 'tset'

    def LKFException(self, msg):
        return BaseException(msg)

class Items(LKFException):
    def __init__(self, path, module, settings):
        self.path = path
        self.module = module
        self.lkf_api = utils.Cache(settings)
        self.settings = settings
        self.lkf = lkf_models.LKFModules(self.settings)
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
        print('file_path=', file_path)
        print('file_name=', file_name)
        print('file_data=', file_data)
        if xml_exists:
            json_file = self.lkf.read_template_file(file_path, f'{file_name}.xml', file_data)
            # json_file = self.read_xml_template(file_path, )
        elif self.file_exists(file_path, file_name, 'json'):
            json_file = open('./{}/{}.json'.format(file_path, file_name))
            json_file = simplejson.load(json_file)
        else:
            raise LKFException('No file with name: {} found, at path: {}'.format(file_name, file_path))
        return json_file

    def get_all_items_json(self, itype):
        # module = __name__.replace('.','/')
        # cmd = ['ls', './{}/{}/'.format(module, itype)]
        cmd = ['ls', './{}/items/{}'.format(self.module, itype)]
        print('cmd=',cmd)
        process = subprocess.Popen(args=cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        output, error = process.communicate()
        res = []
        if output:
            output = output.split()
            for x in output:
                y = x.decode('utf-8')
                if y.find('.json') > 0:
                    res.append(y)
                if y.find('.xml') > 0:
                    res.append(y)
                if y.find('.csv') > 0:
                    res.append(y)
                if y.find('.py') > 0:
                    if y == '__init__.py':
                        continue
                    if y.find('_resource.py') > 0:
                        continue
                    if y.find('.pyc') > 0:
                        continue 
                    res.append(y)
        return res

