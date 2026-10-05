# coding: utf-8
import os
import re
import simplejson
import time
import wget
from pathlib import Path

from linkaform_api import utils, lkf_models
from linkaform_api.network import HTTP_TIMING

from lkf_addons import items

# Campo Excel de la forma Carga Universal Module (fijo, ver
# addons/base/items/forms/Base/carga_universal_module.xml).
FIELD_ID_XLS_CARGA_UNIVERSAL = '5e32fae308a46b2ea5fbde86'
# Campo "Nombre de la forma" (catalog-select) de la misma forma.
FIELD_ID_NOMBRE_FORMA = '5d810a982628de5556500d55'
FIELD_ID_ID_FORMA = '5d810a982628de5556500d56'
FIELD_ID_TIPO_FORMA = 'ccccc0000000000000000002'
FIELD_ID_STATUS_CARGA_UNIVERSAL = '5e32fbb498849f475cfbdca2'


class FormResource(items.Items):

    def data_files(self):
        # Los <algo>_data viven en <modulo>/data/ (al mismo nivel que items/),
        # en esa carpeta o en cualquier subcarpeta: el disenador del modulo las
        # organiza como quiera. Si el mismo archivo (misma ruta relativa) esta en
        # addons y en modules, gana modules.
        found = {}
        for base in (items.ADDONS_PATH, items.MODULES_PATH):
            data_dir = Path(base) / self.module / 'data'
            if not data_dir.is_dir():
                continue
            for path in sorted(data_dir.rglob('*_data.*')):
                if path.is_file() and path.suffix in ('.xml', '.json'):
                    found[str(path.relative_to(data_dir))] = path
        return list(found.values())

    def install_data(self):
        print('********************* Loading Data **************************')
        self.load_info(self.data_files())

    def load_info(self, data_files):
        # No existe un endpoint sheet_to_form (a diferencia de sheet_to_catalog,
        # ver CatalogResource.load_info en items/catalog_resource.py), asi que
        # se baja el sheet como xlsx y se sube a un registro real de Carga
        # Universal Module (post_forms_answers) con estatus 'cargar_documentos':
        # el workflow "Cargar doctos" de esa forma dispara el script del lado del
        # servidor y hace la carga. El estatus y los errores quedan en ese
        # registro, navegables en Linkaform. NO se corre carga_doctos aqui: seria
        # una segunda carga del mismo excel (registros duplicados).
        carga_universal_form_id = self.lkf.form_id('carga_universal_module', 'id')
        if not carga_universal_form_id:
            print("No se encontro la forma 'carga_universal_module' en esta cuenta "
                  "(LKFModules item_type=form); instala primero el modulo base: "
                  "lkfaddons.py install -m base -i forms")
            return False
        for data_file in data_files:
            full_file_name = data_file.name
            file_name = data_file.stem
            # Los <algo>_data son independientes de cualquier forma: cada archivo
            # lleva su propio registro de LKFModules (item_type=form_data,
            # item_name=nombre completo del archivo) donde se anota el "ya
            # cargado". La forma destino la indica el propio archivo.
            tracking_query = {
                'module': self.module,
                'item_type': 'form_data',
                'item_name': full_file_name,
            }
            module_info = dict(self.lkf.serach_module_item(dict(tracking_query)) or {})
            if module_info.get('load_data') is True:
                continue
            try:
                with open(data_file, "r") as file:
                    file_data = simplejson.loads(file.read())
            except FileNotFoundError:
                print(f'File not found {data_file}, continue')
                continue

            form_name = file_data['form_name']
            form_info = self.lkf.form_id(form_name) or {}
            form_id = form_info.get('id')
            # El catalogo muestra el nombre completo (item_full_name), no el slug.
            form_doc = self.lkf.serach_module_item({'item_type': 'form', 'item_id': form_id}) or {}
            form_full_name = form_doc.get('item_full_name') or form_name.replace('_', ' ').title()
            if not form_id:
                print(f"No se encontro la forma destino '{form_name}' (de {full_file_name}) en esta cuenta, se salta")
                continue

            match = re.search(r'/d/([a-zA-Z0-9_-]+)', file_data['spreadsheet_url'])
            sheet_id = match.group(1) if match else file_data['spreadsheet_url']
            export_url = 'https://docs.google.com/spreadsheets/d/{}/export?format=xlsx'.format(sheet_id)
            local_xlsx = '/tmp/sheet_{}.xlsx'.format(time.strftime('%Y_%m_%d_%H_%M_%S'))
            wget.download(export_url, local_xlsx)

            up_file = open(local_xlsx, 'rb')
            try:
                upload_res = self.lkf_api.post_upload_file(
                    data={'form_id': carga_universal_form_id, 'field_id': FIELD_ID_XLS_CARGA_UNIVERSAL},
                    up_file={'File': up_file})
            finally:
                up_file.close()
                os.remove(local_xlsx)
            upload_data = upload_res.get('data')
            if not isinstance(upload_data, dict) or 'file' not in upload_data:
                print(f'Error subiendo el xlsx de {file_name} a Carga Universal Module: '
                      f'status={upload_res.get("status_code")} respuesta={upload_data} '
                      f'form_id={carga_universal_form_id} field_id={FIELD_ID_XLS_CARGA_UNIVERSAL}')
                continue
            file_url = upload_data['file']
            answers = {FIELD_ID_XLS_CARGA_UNIVERSAL: {'file_name': local_xlsx.split('/')[-1], 'file_url': file_url}}
            # Carga Universal Module exige "Forma" (catalogo_de_formas, cuyo field_id
            # es el obj_id del catalogo en cada cuenta) y "Nombre de la forma"
            # (catalog-select hijo de ese catalogo): sin ellos el post da 400.
            catalogo_formas_obj_id = (self.lkf.catalog_id('catalogo_de_formas') or {}).get('obj_id')
            if not catalogo_formas_obj_id:
                print("No se encontro el catalogo 'catalogo_de_formas' en esta cuenta, se salta", full_file_name)
                continue
            # catalog-select va como string (nombre completo de la forma, el que
            # muestra el catalogo); los campos de detalle del catalogo van en lista.
            answers[catalogo_formas_obj_id] = {
                FIELD_ID_NOMBRE_FORMA: form_full_name,
                FIELD_ID_ID_FORMA: [form_id],
                FIELD_ID_TIPO_FORMA: [],
            }
            answers[FIELD_ID_STATUS_CARGA_UNIVERSAL] = 'cargar_documentos'

            metadata = self.lkf_api.get_metadata(form_id=carga_universal_form_id)
            metadata['answers'] = answers
            create_res = self.lkf_api.post_forms_answers(metadata)
            if create_res.get('status_code') not in (200, 201, 202, 204):
                print(f'Error creando el registro de Carga Universal Module para {file_name}: {create_res}')
                continue
            created = create_res.get('json') or {}
            record_id = created.get('_id') or created.get('id')

            print(f'Registro de Carga Universal Module creado para {full_file_name} (forma {form_name}): '
                  f'folio={created.get("folio")} id={record_id}. La carga la hace el workflow del lado del servidor.')

            now = int(time.time())
            set_data = {'load_data': True, 'updated_at': now}
            if not module_info:
                set_data['created_at'] = now
            self.lkf.update(tracking_query, set_data)

    def setup_workflows(self, conf_files, action, path=None, **kwargs):
        if not path:
            path = self.path
        for file_name in conf_files:
            file_name = file_name.split('.')[0]
            print('Installing Workflows: ', file_name)
            workflow_model = self.load_module_template_file(path, file_name)
            # res = self.lkf.install_workflows(module, workflow_model, 'update')
            if action == 'create':
            # if True:
                res = self.lkf_api.upload_workflows(workflow_model, 'POST')
            elif action =='update':
                res = self.lkf_api.upload_workflows(workflow_model, 'PATCH')
                if res.get('status_code') == 404:
                    res = self.lkf_api.upload_workflows(workflow_model, 'POST')
            #res = self.lkf_api.upload_workflows(workflow_model, 'PATCH')

    def setup_rules(self, conf_files, action, path=None):
        if not path:
            path = self.path
        for file_name in conf_files:
            file_name = file_name.split('.')[0]
            rules_model = self.load_module_template_file(path, file_name)
            print('Installing Rules: ',file_name )
            # res = self.lkf.install_workflows(module, workflow_model, 'update')
            if action == 'create':
                res = self.lkf_api.upload_rules(rules_model, 'POST')
            elif action =='update':
                #TODO porque da un 500?? dice como que form_id esta repetido
                res = self.lkf_api.upload_rules(rules_model, 'PATCH')
                if res.get('status_code') == 404:
                    res = self.lkf_api.upload_rules(rules_model, 'POST')
            #res = self.lkf_api.upload_rules(rules_model, 'PATCH')

    def install_forms(self, instalable_forms, **kwargs):
        print('********************* Installing Forms **************************')
        if instalable_forms.get('install_order') or instalable_forms.get('install_order') == []:
            install_order = instalable_forms.pop('install_order', [])
        else:
            install_order = []
        install_order += [x  for x in instalable_forms.keys() if x not in install_order]
        response = []
        print(f'Install Order ({len(install_order)}):')
        for i, name in enumerate(install_order, 1):
            print(f'  {i:3}. {name}')

        # install_order = ['green_house_inventory_move']
        for form_name in install_order:
            form_started_at = time.time() if HTTP_TIMING else None
            detail = instalable_forms[form_name]
            if detail.get('path'):
                this_path = '{}/{}'.format(self.path, detail['path'])
            else:
                this_path = self.path
            form_model = self.load_module_template_file(this_path, form_name)
            self.this_path = this_path
            item_info = {
                # 'created_by' : user,
                'module': self.module,
                # 'name': 'como lo ponomes',
                'item_type': 'form',
                'item_name':form_name,
            }
            item = self.lkf.serach_module_item(item_info)
            if kwargs.get('item_ids'):
                if item and item['item_id'] not in [int(x) for x in kwargs.get('item_ids',[])]:
                    continue    
            res = self.lkf.install_forms(self.module, form_name, form_model, local_path=detail.get('path'), **kwargs)
            if res.get('status') in ('update','create'):
                print('Installing Form: ' ,form_name)
            response.append(
                    {
                        'module':self.module,
                        'item_name': form_name,
                        'install_status':'installed',
                        'status_code': res.get('status_code'),
                        'error': res.get('json',{}).get('error'),
                        'lkf_response':res
                    }
                )
            if res.get('status') in ('update','create'):
                for config, conf_files in detail.items():
                    if config == 'workflow':
                        # res['status'] = 'create'
                        self.setup_workflows(conf_files, res['status'], this_path)
                    if config == 'rules':
                        self.setup_rules(conf_files, res['status'], this_path)
            elif res.get('status_code') == 400:
                print('Status Code 400:', res)
                error = res.get('json',{}).get('error','Please try again!!!')
                raise self.LKFException(f'Error installing form: {form_name}. Error msg {error}')
            if form_started_at is not None:
                # Total por forma (plantilla + form + workflows + rules), para separar
                # el tiempo del back del tiempo local de render/parseo del XML.
                print('[form] {:>7.2f}s  {} ({})'.format(
                    time.time() - form_started_at, form_name, res.get('status', 'sin cambios')))
        return response
 
    def get_form_modules(self, all_items, parent_path=None):
        data_file = []
        form_file = {}
        for file in all_items:
            if type(file) == dict:
                path = list(file.keys())[0]
                if parent_path:
                    path = '{}/{}'.format(parent_path, path)
                form_file.update(self.get_form_modules(list(file.values())[0], parent_path=path))
                continue
            file_ext = file.split('.')
            if len(file_ext) != 2:
                print('Not a supported file', file)
                continue
            file_name = file_ext[0]
            file_type = file_name.split('_')[-1]
            if file_type in ('data', 'demo'):
                # Los _data viven en <modulo>/data/ (ver data_files); _demo ya
                # no se soporta en formas.
                continue
            elif file_type in ('workflow', 'rules'):
                if file_name not in data_file:
                    data_file.append(file_name)
            else:
                form_file[file_name] = {'data':[],'workflow':[], 'rules':[] }
                if parent_path:
                    form_file[file_name].update({'path':parent_path})
        for item in list(form_file.keys()):
            for file_name in data_file:
                file_type = file_name.split('_')[-1]
                if file_name[:file_name.rfind('_')] == item:
                    #TODO hacer muylti extesion
                    form_file[item][file_type].append('{}.{}'.format(file_name, file_ext[1]))
        return form_file

    def instalable_forms(self, install_order=None, **kwargs):
        items_json = self.get_anddons_and_modules_items('forms')
        forms_data = self.get_form_modules(items_json)
        if install_order:
            forms_data['install_order'] = install_order
        else:
            forms_data['install_order'] = list(forms_data.keys())
        return forms_data