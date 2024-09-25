# -*- coding: utf-8 -*-
### Linkaform Modules / Archivo de Módulo ###
'''
Este archivo proporciona las funcionalidades modulares de LinkaForm. Con estas funcionalidades, 
podrás utilizar la plataforma LinkaForm de manera modular, como un Backend as a Service (BaaS).

Licencia
Este código está licenciado bajo la licencia GPL3 (https://www.gnu.org/licenses/gpl-3.0.html).

Propósito
El propósito de este archivo es ser auto documentable y adaptable, facilitando la reutilización 
de gran parte del código en otros módulos simplemente copiando y pegando las secciones necesarias.

Instrucciones
1. Al copiar secciones de código, asegúrate de incluir la documentación correspondiente.
2. Al crear un nuevo archivo o módulo, copia las instrucciones y las generales aplicables a cada archivo.
3. Puedes basarte en la carpeta `_templates` o sus archivos para crear nuevos módulos.
'''

### Archivo de Modulo ###
'''
Este archivo define las funciones generales del módulo. Por conveniencia, se nombra `app.py`. 

Si tienes más de una aplicación, puedes:
    a. Crear una carpeta llamada `app`.
    b. Guardar los archivos a nivel raíz.
    c. Nombrar los archivos por conveniencia o estándar: `app_utils.py`, `utils.py`, `xxx_utils.py`.
'''

# Importaciones necesarias
import simplejson
import re, os, zipfile, wget, random, shutil, datetime

from linkaform_api import base


class Base(base.LKF_Base):

    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False, **kwargs):
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api, **kwargs)
        #use self.lkm.catalog_id() to get catalog id
       #--Variables 
        ### Forms ###
        '''
        `self.FORM_NAME = self.lkm.form_id('form_name',id)` ---> Aquí deberás guardar los `ID` de los formularios. 
        Para ello deberás llamar el método `lkm.form_id` del objeto `lkm` (linkaform modules, por sus siglas).
        En `lkm` están todas las funciones generales de módulos.
        '''
        self.CONTACTO = self.lkm.form_id('contacto', 'id')
        self.CLIENTE = self.lkm.form_id('clientes', 'id')
        #self.CONFIGURACIONES = self.lkm.form_id('configuraciones', 'id')
        ### Catálogos ###
        '''
        `self.CATALOG_NAME = self.lkm.catalog_id('catalog_name',id)` ---> Aquí deberás guardar los `ID` de los catálogos. 
        Para ello deberás llamar el método `lkm.catalog_id` del objeto `lkm`(linkaform modules, por sus siglas).
        En `lkm` están todas las funciones generales de módulos).
        '''
        self.CLIENTE_CAT = self.lkm.catalog_id('clientes')
        self.CLIENTE_CAT_ID = self.CLIENTE_CAT.get('id')
        self.CLIENTE_CAT_OBJ_ID = self.CLIENTE_CAT.get('obj_id')

        self.COMPANY = self.lkm.catalog_id('compaia')
        self.COMPANY_ID = self.COMPANY.get('id')
        self.COMPANY_OBJ_ID = self.COMPANY.get('obj_id')

        self.CONTACTO_CAT = self.lkm.catalog_id('contacto')
        self.CONTACTO_CAT_ID = self.CONTACTO_CAT.get('id')
        self.CONTACTO_CAT_OBJ_ID = self.CONTACTO_CAT.get('obj_id')

        self.COUNTRY = self.lkm.catalog_id('pais')
        self.COUNTRY_ID = self.COUNTRY.get('id')
        self.COUNTRY_OBJ_ID = self.COUNTRY.get('obj_id')

        self.ESTADO = self.lkm.catalog_id('estados')
        self.ESTADO_ID = self.ESTADO.get('id')
        self.ESTADO_OBJ_ID = self.ESTADO.get('obj_id')

        self.TIMEZONE = self.lkm.catalog_id('timezone')
        self.TIMEZONE_ID = self.TIMEZONE.get('id')
        self.TIMEZONE_OBJ_ID = self.TIMEZONE.get('obj_id')

        self.UOM = self.lkm.catalog_id('unidad_de_medida')
        self.UOM_ID = self.UOM.get('id')
        self.UOM_OBJ_ID = self.UOM.get('obj_id')

        ### Global Variables
        self.GET_CONFIG = {}
        
        self.f.update( {
            'address_name':'663a7e0fe48382c5b1230901',
            'address_image':'663a808be48382c5b123090d',
            'address_geolocation':'663e5c8cf5b8a7ce8211ed0c',
            'address_status':'6663a7f67e48382c5b1230909',
            'address_type':'663a7f67e48382c5b1230908',
            'address':'663a7e0fe48382c5b1230902',
            'address2':'663a7f79e48382c5b123090a',
            'cat_timezone':f'{self.TIMEZONE_OBJ_ID}.665e4f90c4cf32cb52ebe15c',
            'config_group':'66ed0baac9aefada5b04b817',
            'country':'663a7ca6e48382c5b12308fa',
            'city':'6654187fc85ce22aaf8bb070',
            'email':'663a7ee1e48382c5b1230907',
            'email_contacto':'66bfd647cd15883ed163e9b5',
            'nombre_comercial':'667468e3e577b8b98c852aaa',
            'pagina_web':'66bfd66ecd15883ed163e9b7',
            'phone':'663a7ee1e48382c5b1230906',
            'razon_social':'6687f2f37b2c023e187d6252',
            'rfc_razon_social':'667468e3e577b8b98c852aab',
            'state':'663a7dd6e48382c5b12308ff',
            'state_code':'663a7dd6e48382c5b1230900',
            'telefono':'66bfd666cd15883ed163e9b6',
            'timezone':'665e4f90c4cf32cb52ebe15c',
            'uom':'669efc6f47920d1b51663d29',
            'uom_category':'669efbf447920d1b51663d28',
            'zip_code':'663a7ee1e48382c5b1230905',
        }
        )

        self.config_fields = {
            'demora':f'{self.f.get("demora")}',
            'lead_time':f'{self.f.get("lead_time")}',
            'dias_laborales_consumo':f'{self.f.get("dias_laborales_consumo")}',
            'factor_crecimiento_jit':f'{self.f.get("factor_crecimiento_jit")}',
            'factor_seguridad_jit':f'{self.f.get("factor_seguridad_jit")}',
            'uom':f'{self.UOM_OBJ_ID}.{self.f.get("uom")}',
            'procurment_location':f'{self.f.get("config_group")}',
            'warehouse_kind': '66ed0c88c9aefada5b04b818',
        }


    def _project_format(self, data):
        return self.project_format(data)

    def get_config(self, *args, **kwargs):
        if not self.GET_CONFIG:
            match_query ={ 
                 'form_id': self.CONFIGURACIONES,  
                 'deleted_at' : {'$exists':False},
            } 
            if kwargs.get('query'):
                match_query.update(kwargs['query'])
            project_ids = self._project_format(self.config_fields)
            aggregate = [
                {'$match': match_query},
                {'$limit':kwargs.get('limit',1)},
                {'$project': project_ids },
                ]
            self.GET_CONFIG =  self.format_cr(self.cr.aggregate(aggregate) )
        result = {}
        for res in self.GET_CONFIG:
            result = {arg:res[arg] for arg in args if res.get(arg)}
        return result if result else None
        

from linkaform_api import  upload_file

#fields_no_update = ['post_status', 'next_cut_week', 'cut_week', 'cycle_group', 'ready_year_week']

class CargaUniversal(base.LKF_Base):


    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False):
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api)

        self.CATALOGO_FORMAS_CAT = self.lkm.catalog_id('catalogo_de_formas')
        self.CATALOGO_FORMAS_CAT_ID = self.CATALOGO_FORMAS_CAT.get('id')
        self.CATALOGO_FORMAS_CAT_OBJ_ID = self.CATALOGO_FORMAS_CAT.get('obj_id')


        self.f.update({
            'field_id_xls':'5e32fae308a46b2ea5fbde86', 
            'field_id_catalog_form_detail':'5d810a982628de5556500d56',
            'field_id_zip':'5e32fa34a6d1e315fe80f845', 
            'field_id_status':'5e32fbb498849f475cfbdca2', 
            'field_id_error_records':'5e32fbb498849f475cfbdca3', 
            'field_id_comentarios':'5e32fbb498849f475cfbdca4', 
            'fields_no_update':[]
        })


        self.field_id_comentarios = self.f['field_id_comentarios']
        self.field_id_catalog_form = self.CATALOGO_FORMAS_CAT_OBJ_ID
        self.field_id_catalog_form_detail = self.f['field_id_catalog_form_detail']
        self.field_id_error_records = self.f['field_id_error_records']
        self.field_id_status = self.f['field_id_status']
        self.field_id_xls = self.f['field_id_xls']
        self.field_id_zip = self.f['field_id_zip']
        self.fields_no_update = self.f['fields_no_update']
        self.upfile = upload_file.LoadFile(settings)

    def crea_directorio_temporal(self, nueva_ruta):
        try:
            if not os.path.exists(str(nueva_ruta)):
                os.makedirs(str(nueva_ruta),0o777)
                os.chdir(str(nueva_ruta))
            else:
                shutil.rmtree(nueva_ruta)
                os.makedirs(str(nueva_ruta),0o777)
                os.chdir(str(nueva_ruta))
            return True
        except Exception as e:
            print('############ error al crear directorio temporal=',str(e))
            return False

    def arregla_msg_error_sistema(self, response):
        try:
            msg_err_arr = []
            data_str_err = ''
            if response.get('status_code', 0) == 400:
                data_str_err = "Formato incorrecto:"
            for msg_fin in response.get('json',{}):
                info_json = response['json'][msg_fin]
                msgs = info_json.get('msg', [])
                if msgs:
                    msg_err = self.strip_special_characters(msgs[0])
                    label_err = info_json.get('label')
                    msg_err_arr.append(str(msg_err+':'+label_err))
                else:
                    for i_err in info_json:
                        info_i = info_json[i_err]
                        for id_group in info_i:
                            info_group = info_i[id_group]
                            msg_err = self.strip_special_characters(info_group['msg'][0])
                            label_err = info_group['label']
                            msg_err_arr.append('SET {0}:: {1} - {2}'.format(i_err, msg_err, label_err))
            if msg_err_arr:
                data_str_err = self.list_to_str(msg_err_arr)
        except Exception as e:
            print('response', response)
            print('Exception =  ', e)
            data_str_err = "Ocurrió un error desconocido favor de contactar a soporte"
            error_json = response.get('json',{}).get('error','')
            if error_json:
                data_str_err = error_json
        return data_str_err

    def query_busca_records(self, form_id, folio):
        if type(folio) == list:
            query = {'form_id':  form_id, 'deleted_at' : {'$exists':False},
                'folio':{'$in':folio}}
        else:
            query = {'form_id':  form_id, 'deleted_at' : {'$exists':False},
                'folio':self.strip_special_characters(folio)}
        select_columns = {'folio':1,'user_id':1,'form_id':1, 'answers':1,'_id':1,'connection_id':1}
        return query, select_columns

    def strip_special_characters(self, value, underscore = False):
        res = ''
        try:
            res = str(value)
        except UnicodeEncodeError:
            try:
                res = str(value.decode('utf-8'))
            except AttributeError:
                res = str(value)
        except:
            res = value

        if underscore:
            res = res.replace(' ','_').lower()
        return res

    def get_records_existentes(self, form_id, folios, extra_params={}):
        query, select_columns = self.query_busca_records(form_id, folios)
        if extra_params:
            query.update(extra_params)
        record = self.cr.find(query, select_columns)
        existentes = {rec['folio']:rec for rec in record}
        return existentes

    def update_status_record(self,  current_record, record_id, status, msg_comentarios='' ):
        if not record_id:
            if status == 'carga_terminada':
                return {'msg': msg_comentarios}
            return {'error': msg_comentarios}
        current_record['answers'][self.field_id_status] = status
        if msg_comentarios:
            current_record['answers'][self.field_id_comentarios] = msg_comentarios
        self.lkf_api.patch_record(current_record, record_id)
        return False

    def make_header_dict(self, header):
        ### Return the directory with
        ### the column name : column number
        header_dict = {}
        for position in range(len(header)):
            text_col = header[position].lower().replace(' ' ,'_')
            if text_col == 'folio' and position > 0:
                text_col = 'folio__enCampo'
            header_dict[text_col] = position
        return header_dict

    def upload_docto(self, nueva_ruta, file_to_load, id_forma_seleccionada, id_field):
        file_link, file_name = os.path.split(file_to_load)
        rb_file = open(nueva_ruta+file_name,'rb')
        dir_file = {'File': rb_file}
        try:
            upload_data = {'form_id': id_forma_seleccionada, 'field_id':id_field}
            upload_url = self.lkf_api.post_upload_file(data=upload_data, up_file=dir_file)
            rb_file.close()
        except Exception as e:
            rb_file.close()
        try:
            file_url = upload_url['data']['file']
            update_file = {'file_name':file_to_load, 'file_url':file_url}
        except Exception as e:
            print('------- error al subir el docto:',e)
            update_file = {"error":"Fallo al subir el archivo"}
        return update_file

    def procesa_zip(self, current_record, record_id):
        ruta_destino = "/tmp/"
        filetmp = random.randint(0, 1000)
        nuevo_directorio = "cargafiles_"+str(filetmp)+"/"
        nueva_ruta = ruta_destino + nuevo_directorio
        directorio_temporal = self.crea_directorio_temporal(nueva_ruta)
        if directorio_temporal:
            os.chdir(nueva_ruta)
            ruta_zip = current_record['answers'][self.field_id_zip]['file_url']
            fileoszip = wget.download(ruta_zip,nueva_ruta)
            path, file = os.path.split(fileoszip)
            archivo_zip = zipfile.ZipFile(nueva_ruta+file)
            for archivo in archivo_zip.namelist():
                archivo_zip.extract(archivo, nueva_ruta)
            archivo_zip.close()
            return nueva_ruta, archivo_zip, file
        else:
            print("-------- error: No se pudo generar el directorio temporal")
            return self.update_status_record(current_record, record_id, 'error', msg_comentarios='Ocurrió un error inesperado, favor de contactar a soporte')

    def procesa_row(self, pos_field_dict, record, files_dir, nueva_ruta, id_forma_seleccionada, answers, p, dict_catalogs):
        error = []
        grupo_repetitivo = {}
        fields_to_find_catalog = {}
        for pos in pos_field_dict:
            field = pos_field_dict[pos]
            #print('---------- field label = {} default_value = {}'.format(field['label'], field.get('default_value')))
            if not record[pos] and field.get('default_value'):
                record[pos] = field['default_value']
            if record[pos] or record[pos]==0:
                if field['field_type'] in ('images','file'):
                    res_upload_docto = self.upload_docto(nueva_ruta, record[pos], id_forma_seleccionada, field['field_id'])
                    print("+++ res_upload_docto:",res_upload_docto)
                    if res_upload_docto.get('error'):
                        error.append('Ocurrió un error al cargar el documento %s'%(str(record[pos])))
                    else:
                        if field['field_type'] == 'images':
                            field_add = {field['field_id']: [res_upload_docto]}
                        else:
                            field_add = {field['field_id']: res_upload_docto}
                        if field['group']:
                            group_id = field.get('group').get('group_id')
                            if not grupo_repetitivo.get(group_id):
                                grupo_repetitivo.update({group_id: {}})
                            grupo_repetitivo[group_id].update(field_add)
                        else:
                            answers.update(field_add)
                elif field['field_type'] == 'catalog-select':
                    catalog_field_id = field.get('catalog',{}).get('catalog_field_id','')
                    if not fields_to_find_catalog.get(catalog_field_id):
                        fields_to_find_catalog.update({catalog_field_id:[]})
                    fields_to_find_catalog[catalog_field_id].append({field['field_id']: {'$eq': record[pos]}})
                else:
                    if field['field_type'] == "date":
                        try:
                            record[pos] = record[pos].strftime("%Y-%m-%d")
                        except:
                            try:
                                if not re.match(r"(\d{4}-\d{2}-\d{2})", record[pos]):
                                    error.append('Formato de fecha incorrecto: '+field['label'])
                            except:
                                error.append('Formato de fecha incorrecto: '+field['label'])
                    elif field['field_type'] == "datetime":
                        try:
                            record[pos] = record[pos].strftime("%Y-%m-%d %H:%M:%S")
                        except:
                            if not re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", record[pos]):
                                error.append('Formato de fecha y hora incorrecto: '+field['label'])
                    elif field['field_type'] == "time":
                        try:
                            record[pos] = record[pos].strftime("%H:%M:%S")
                        except:
                            if not re.match(r"(\d{2}:\d{2}:\d{2})", record[pos]):
                                error.append('Formato de hora incorrecto: '+field['label'])
                    elif field['field_type'] == "email":
                        email_validate = re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", record[pos])
                        if not email_validate:
                            error.append('La estructura del email no es correcta: '+field['label'])
                    elif field['field_type'] == "checkbox":
                        optsXls = [opCheck.lower().strip().replace(' ', '_') for opCheck in str(record[pos]).split(',')]
                        optsAcepted = [ option['value'] for option in field['options'] ]
                        esta_en_opciones = True
                        for opxls in optsXls:
                            if opxls not in optsAcepted:
                                esta_en_opciones = False
                                break
                        if esta_en_opciones:
                            str_opts = ''
                            str_opts += ', '.join([a for a in optsXls if a])
                            record[pos] = str_opts
                        else:
                            error.append('Alguna de las opciones no esta dentro de los valores definidos: '+field['label'])
                    elif field['field_type'] in ["radio","select"]:
                        record_value = record[pos].lower().replace(' ' ,'_')
                        esta_en_opciones = False
                        for option in field['options']:
                            if record_value == option['value']:
                                esta_en_opciones = True
                                break
                        if esta_en_opciones:
                            record[pos] = record_value
                        else:
                            error.append('La opcion no esta dentro de los valores definidos: '+field['label'])
                    elif field['field_type'] in ["text", "textarea", "description"]:
                        #if isinstance(record[pos], types.UnicodeType):
                        try:
                            record[pos] = record[pos].decode('utf-8')
                        except:
                            pass
                    elif field['field_type'] == "integer":
                        try:
                            record[pos] = int(record[pos])
                        except:
                            error.append('No es posible convertir una cadena a entero: '+field['label'])
                    elif field['field_type'] == "decimal":
                        try:
                            record[pos] = float(record[pos])
                        except:
                            error.append('No es posible convertir una cadena a decimal: '+field['label'])
                    # if isinstance(pos, types.IntType):
                    #     if isinstance(record[pos], types.UnicodeType):
                    #         record[pos] = record[pos].decode('utf-8')
                    if field['group']:
                        group_id = field.get('group').get('group_id')
                        if not grupo_repetitivo.get(group_id):
                            grupo_repetitivo.update({group_id: {}})
                        grupo_repetitivo[group_id].update(self.lkf_api.make_infosync_json(record[pos], field, best_effort=True))
                    else:
                        answers.update(self.lkf_api.make_infosync_json(record[pos], field, best_effort=True))
        if fields_to_find_catalog:
            for id_cat in dict_catalogs:
                cont_cat = dict_catalogs[id_cat]
                filter_catalog = fields_to_find_catalog.get(id_cat,[])
                filter_in_catalog = cont_cat.get('catalog',{}).get('filters',{})
                if filter_in_catalog:
                    #print("----- filter_in_catalog:",filter_in_catalog)
                    filter_catalog.extend(filter_in_catalog['$and'])
                if filter_catalog:
                    catalog_id = cont_cat.get('catalog',{}).get('catalog_id','')
                    #print("+++++ filter_catalog:",filter_catalog)
                    #row_catalog = cat_utils.get_row_by_selector(catalog_id, {'$and':filter_catalog})
                    mango_query = {"selector":
                        {"answers":
                            {"$and":filter_catalog}
                        },
                        "limit":20,"skip":0}
                    row_catalog = self.lkf_api.search_catalog( catalog_id, mango_query )
                    #print("+++++ row_catalog:",row_catalog)
                    if row_catalog:
                        catalog_fields = cont_cat.get('catalog_fields',[])
                        view_fields = cont_cat.get('catalog',{}).get('view_fields',[])
                        dict_row_catalog = row_catalog[0]
                        dict_record_catalog_to_save = {}
                        for id_field_catalog in dict_row_catalog:
                            content_catalog = dict_row_catalog[id_field_catalog]
                            if id_field_catalog in view_fields:
                                dict_record_catalog_to_save.update({id_field_catalog: content_catalog})
                            elif id_field_catalog in catalog_fields:
                                if type(content_catalog) == list and content_catalog and type(content_catalog[0]) == dict and content_catalog[0].get('file_url'):
                                    content_catalog = content_catalog[0]
                                dict_record_catalog_to_save.update({id_field_catalog: [content_catalog]})
                        if cont_cat['group']:
                            group_id = cont_cat.get('group').get('group_id')
                            if not grupo_repetitivo.get(group_id):
                                grupo_repetitivo.update({group_id: {}})
                            grupo_repetitivo[group_id].update({id_cat:dict_record_catalog_to_save})
                        else:
                            answers.update({id_cat:dict_record_catalog_to_save})
                    else:
                        print('----- No se encontro info en el catalogo con el filtro = ',mango_query)
                        error.append('No se encontro informacion en el catalogo '+cont_cat['label'])
        if grupo_repetitivo:
            for id_g in grupo_repetitivo:
                cont_g = grupo_repetitivo[id_g]
                if answers.get(id_g):
                    answers[id_g].append(cont_g)
                else:
                    answers.update({id_g: [cont_g]})
        if error:
            #print("---------error:",error)
            msg_errores_row = ''
            #msg_errores_row += ', '.join([str(a) for a in error if a])
            for a in error:
                if a:
                    # if isinstance(a, types.UnicodeType):
                    #     a = a.decode('utf-8')
                    msg_errores_row += (a+', ')
            answers.update({'error': 'Registro con errores'})
            if not answers.get('dict_errors'):
                answers.update({'dict_errors':{}})
            answers['dict_errors'].update({p: msg_errores_row})
        return answers

    def get_diff_values(self, current_values, new_values, ids_to_compare):
        values_to_update = {}
        for i in ids_to_compare:
            v1 = current_values.get(i)
            if type(v1) == str:
                v1 = str(v1.encode('utf-8'))
            v2 = new_values.get(i)
            if v2 and (v1 != v2):
                values_to_update.update({i: v2})
        return values_to_update

    def crea_actualiza_record(self, metadata, existing_records, error_records, records, sets_in_row, dict_records_to_multi, dict_records_copy, ids_fields_no_update):
        if metadata.get('answers',{}).get('error',''):
            print('----- sets_in_row',sets_in_row)
            dict_errors = metadata.get('answers',{}).get('dict_errors',{})
            for g in sets_in_row:
                s = sets_in_row[g]
                error_records.append(records[g]+[dict_errors.get(g,''),])
                for dentro_grupo in s:
                    error_records.append(records[dentro_grupo]+[dict_errors.get(dentro_grupo,''),])
            proceso = 'error'
        else:
            folio = metadata.get('folio','')
            
            if folio and existing_records.get(folio):
                info_to_send = existing_records[folio]

                # Reviso si hubo diferencia entre el registro y los nuevos valores
                ids_to_validate_update = list( set(metadata['answers'].keys()) - set(ids_fields_no_update) )
                values_to_update = self.get_diff_values( info_to_send.get('answers',{}), metadata['answers'], ids_to_validate_update)

                if values_to_update:
                    #dict_records_copy['update'][ folio ] = sets_in_row
                    info_to_send.update({
                        'geolocation': metadata.get('geolocation',[]),
                        'geolocation_method': metadata.get('geolocation_method',{}),
                        'properties': metadata.get('properties',{})
                        })
                    info_to_send['answers'].update( metadata['answers'] )
                    print("***************** record to update", info_to_send)
                    #info_to_send.update({'folios': [folio,]})

                    # if info_to_send.get('user_id'):
                    #     info_to_send.pop('user_id')
                    # if info_to_send.get('form_id'):
                    #     info_to_send.pop('form_id')

                    # dict_records_to_multi['update'].append(info_to_send)
                    # response_sistema = {'status_code': 0}
                    # proceso = ''
                    response_sistema = self.lkf_api.patch_record(info_to_send)
                    print("----- response actualizar registro:", response_sistema)
                    proceso = 'actualizados'
                else:
                    proceso = 'no_update'
                    response_sistema = {'status_code': 0}
            else:
                #print("***************** record to create", metadata)
                new_sets_in_row = {}
                for g, s in sets_in_row.items():
                    #s = sets_in_row[g]
                    len_recs = len( dict_records_copy['create'] )
                    dict_records_copy['create'].append(records[g])
                    new_sets_in_row[len_recs] = []
                    for dentro_grupo in s:
                        new_sets_in_row[len_recs].append( len( dict_records_copy['create'] ) )
                        dict_records_copy['create'].append(records[dentro_grupo])
                metadata.update({
                    'sets_in_row': new_sets_in_row
                })
                dict_records_to_multi['create'].append(metadata)
                response_sistema = {'status_code': 0}
                proceso = ''
                # response_sistema = self.lkf_api.post_forms_answers(metadata)
                # print("----- response crear registro:", response_sistema)
                # proceso = 'creados'
            if response_sistema.get('status_code') > 300:
                proceso = 'error'
                msg_error_sistema = self.arregla_msg_error_sistema(response_sistema)
                for g in sets_in_row:
                    s = sets_in_row[g]
                    error_records.append(records[g]+[msg_error_sistema,])
                    for dentro_grupo in s:
                        error_records.append(records[dentro_grupo]+['',])
        return proceso

    def get_repeated_ids_in_filter(self, filters_catalog):
        dict_counts = {}
        for ff in filters_catalog:
            kk = list(ff.keys())[0]
            if not dict_counts.get(kk):
                dict_counts[kk] = 0
            dict_counts[kk] += 1
        return [ ii for ii in dict_counts if dict_counts[ii] > 1 ]

    def carga_doctos(self, form_id_to_load=None, read_excel_from=None):
        if self.record_id:
            self.update_status_record(self.current_record, self.record_id, 'procesando')
        global error_records
        error_records = []
        #try:
        if True:
            """
            Obtengo los renglones y las cabeceras del excel
            """
            if not self.current_record:
                self.current_record = {'folio': 'ApiLKF', 'answers': {}}
                print('**** leyendo el archivo Excel =',read_excel_from)
                header, records = self.upfile.read_file(file_name=read_excel_from)
            else:
                answer_file = self.current_record['answers'][self.field_id_xls]
                file_url = answer_file[0]['file_url'] if type(answer_file) == list else answer_file['file_url']
                print('********************** file_url=',file_url)
                header, records = self.upfile.read_file(file_url=file_url)
            """
            Obtengo la información de la forma seleccionada del catálogo
            """
            if not form_id_to_load:
                field_forma = self.current_record['answers'][self.field_id_catalog_form]
                id_forma_seleccionada = field_forma[self.field_id_catalog_form_detail][0]
            else:
                id_forma_seleccionada = form_id_to_load
            form_fields = self.lkf_api.get_form_id_fields(id_forma_seleccionada)
            if not form_fields:
                return self.update_status_record(self.current_record, self.record_id, 'error', msg_comentarios='No se encontró la forma %s'%(str(id_forma_seleccionada)))
            else:
                fields = form_fields[0]['fields']
                #print("+++++ fields:",fields)
                # Obtengo solo los índices que necesito de cada campo
                info_fields = [{k:n[k] for k in ('label','field_type','field_id','groups_fields','group','options','catalog_fields','catalog','default_value') if k in n} for n in fields]
                #print("+++++ info_fields:",info_fields)
                # Obtengo dentro de las opciones avanzadas si el registro necesita un Folio o es automatico
                advanced_options = form_fields[0]['advanced_options']
                folio_manual = advanced_options.get('folio',{}).get('manual',False)
            """
            Empiezo a trabajar la carga de los documentos
            """
            # procesando el archivo zip de carga
            if self.current_record.get('answers',{}).get(self.field_id_zip,{}):
                print('lllllllllllllleva zip')
                print(self.current_record['answers'])
                nueva_ruta, archivo_zip, file = self.procesa_zip(self.current_record, self.record_id)
                files_dir = os.listdir(nueva_ruta)
            else:
                nueva_ruta = ''
                files_dir = []
            #print("+++ files_dir:",files_dir)
            # header_dict contiene un diccionario con las cabeceras del xls y su posición, por ejemplo {cabecera1: 0}, los espacios se reemplazan por _
            header_dict = self.make_header_dict(header)
            #print("------- header_dict=",header_dict)
            # Valido que si el folio es manual venga una columna Folio en la primera columna del excel
            if folio_manual and (not header_dict.get('folio') or header_dict['folio'] > 0):
                return self.update_status_record(self.current_record, self.record_id, 'error', msg_comentarios='La forma tiene configurado el Folio manual y el archivo de carga no cuenta con la columna Folio')
            # Si el archivo de carga trae en la primera columna el campo "Folio" obtengo la lista y consulto si existen registros con ese folio en la forma correspondiente
            existing_records = {}
            if header_dict.get('folio') and header_dict['folio'] == 0:
                folios = [self.strip_special_characters(rec[0]) for rec in records if rec[0]]
                existing_records = self.get_records_existentes(id_forma_seleccionada, folios)
                #print("---------- existing_records:",existing_records)
            #print("++++ header_dict:",header_dict)
            # pos_field_dict contiene un diccionario con la posición del campo dentro de los registros del excel
            pos_field_dict = {header_dict[f['label'].lower().replace(' ','_')]:f for f in info_fields
                if f['label'].lower() != 'folio'
                and f['field_type'] not in ('catalog','catalog-select','catalog-detail')
                and f['label'].lower().replace(' ','_') in header_dict.keys()}
            #print 'pos_field_dict=',pos_field_dict

            ids_fields_no_update = [f['field_id'] for f in info_fields if f.get('label', '').lower().replace(' ','_') in self.fields_no_update]
            #print 'ids_fields_no_update=',ids_fields_no_update
            if header_dict.get('folio__enCampo'):
                pos_field_dict.update({header_dict['folio__enCampo']:f for f in info_fields if f['label'].lower() == 'folio' and not f['group']})
            #print("++++ pos_field_dict:",pos_field_dict)
            # Verifico si la carga tiene algún campo que sea de tipo Documento o Imagen
            fields_files = [pos_field_dict[p] for p in pos_field_dict if pos_field_dict[p]['field_type'] in ('file','images')]
            #print("++++ fields_files:",fields_files)
            # Obtengo un diccionario de los campos que son de tipo Catálogo
            dict_catalogs = {f['field_id']:f for f in info_fields if f['field_type']=='catalog'}
            dict_grupos = {f['field_id']:f['label'].lower().replace(' ','_') for f in info_fields if f['groups_fields']}
            #print("+++++ dict_grupos:",dict_grupos)
            #print("+++++ dict_catalogs:",dict_catalogs)
            for idc in dict_catalogs:
                ccat = dict_catalogs[idc]
                filters = ccat.get('catalog',{}).get('filters','')
                if filters:
                    info_catalog = self.lkf_api.get_catalog_id_fields(ccat.get('catalog',{}).get('catalog_id',0))
                    dict_filters = info_catalog.get('catalog',{}).get('filters',{})
                    #print('+++++ dict_filters',dict_filters)
                    ccat['catalog']['filters'] = dict_filters.get(filters, {})

                    # Reviso si hay campos repetidos en el filtro para entonces armar los $or
                    if dict_filters.get(filters):
                        list_repeated_fields = self.get_repeated_ids_in_filter(dict_filters.get(filters, {}).get('$and', []))
                        if list_repeated_fields:
                            print('list_repeated_fields =====',list_repeated_fields)
                            new_and = []
                            fields_or = {}
                            #dict_filters[filters]['$and'].append({'6205f73281bb36a6f1500000': {'$eq': 'Test01'}})
                            for rr in dict_filters.get(filters, {}).get('$and', []):
                                rr_idfield = list(rr.keys())[0]
                                if rr_idfield in list_repeated_fields:
                                    if not fields_or.get(rr_idfield):
                                        fields_or[rr_idfield] = {'$or': []}
                                    fields_or[rr_idfield]['$or'].append(rr[rr_idfield])
                                else:
                                    new_and.append(rr)
                            print('........... fields_or=',fields_or)
                            for fff in fields_or:
                                new_and.append({fff: fields_or[fff]})
                            print('........... new_and=',new_and)
                            ccat['catalog']['filters'] = {'$and':new_and}
            #print("----- dict_catalogs con filtro:", dict_catalogs)
            # Reviso si existen grupos repetitivos en el archivo de carga
            fields_groups = { f['field_id']: f['label'] for f in info_fields if f['field_type'] == 'group' }
            fields_for_sets = {}
            fields_for_catalog = {}

            dict_group_catalogs_inside = {}
            for f in info_fields:
                if f.get('group', False):
                    g_id = f['group']['group_id']
                    if f['field_type'] == 'catalog':
                        if not dict_group_catalogs_inside.get(g_id):
                            dict_group_catalogs_inside[g_id] = {}
                        if not dict_group_catalogs_inside[g_id].get( f['field_id'] ):
                            dict_group_catalogs_inside[g_id][ f['field_id'] ] = []
                    elif f['field_type'] == 'catalog-select':
                        dict_group_catalogs_inside[g_id][ f['catalog']['catalog_field_id'] ].append( f['label'] )
                    else:
                        if not fields_for_sets.get(g_id, False):
                            fields_for_sets[g_id] = []
                        fields_for_sets[g_id].append(f['label'])
                if f['field_type'] == 'catalog-select' and f.get('catalog', False):
                    c_id = f['catalog']['catalog_field_id']
                    if not fields_for_catalog.get(c_id, False):
                        fields_for_catalog[c_id] = []
                    fields_for_catalog[c_id].append(f['label'])

            list_groups = []
            for _g_id in dict_group_catalogs_inside:
                if not fields_for_sets.get(_g_id):
                    fields_for_sets[_g_id] = []
                for _c_id in dict_group_catalogs_inside[_g_id]:
                    _label_catalog = dict_catalogs[_c_id]['label']
                    for _label_select in dict_group_catalogs_inside[_g_id][_c_id]:
                        fields_for_sets[_g_id].append( '{}: {}'.format( _label_catalog, _label_select ) )
            print('+++++++++++++++++++++++ dict_group_catalogs_inside=',simplejson.dumps(dict_group_catalogs_inside,indent=4))
            print('++++ fields_for_sets=',fields_for_sets)
            print('++++ fields_for_catalog=',fields_for_catalog)
            for g in fields_groups:
                for s in fields_for_sets.get(g, []):
                    list_groups.append(u'{}:_{}'.format(fields_groups[g].lower().replace(' ', '_'), s.lower().replace(' ', '_')))
            list_catalogs = []
            for c in dict_catalogs:
                for d in fields_for_catalog.get(c, []):
                    list_catalogs.append(u'{}:_{}'.format(dict_catalogs[c]['label'].lower().replace(' ', '_'), d.lower().replace(' ', '_')))
            print('list_groups=',list_groups)
            print('list_catalogs=',list_catalogs)

            grupos_en_excel = {h:header_dict[h] for h in header_dict if h in list_groups}
            print('++++ grupos_en_excel', grupos_en_excel)
            #catalogs_en_excel = {h:header_dict[h] for h in header_dict if h in list_catalogs}
            catalogs_en_excel = {}
            for h in header_dict:
                pos_h = header_dict[h]
                if ':_' in h:
                    if h in list_catalogs:
                        catalogs_en_excel.update({ h: pos_h })
                    else:
                        list_h = h.split(':_')
                        if len(list_h) == 3:
                            to_eval_in_group = list_h[0] + ':_' + list_h[2]
                            if to_eval_in_group in list_groups:
                                catalogs_en_excel.update({
                                    '{}:_{}'.format(list_h[1], list_h[2]): pos_h
                                })
            print('++++ catalogs_en_excel', catalogs_en_excel)
            grupos_en_excel.update( catalogs_en_excel )
            if grupos_en_excel:
                pos_field_dict_grupos = {}
                for grupo_campo in grupos_en_excel:
                    pos = grupos_en_excel[grupo_campo]
                    list_grupos = grupo_campo.split(":_")
                    label_campo = list_grupos[len(list_grupos)-1]
                    #pos_field_dict_grupos.update( {pos:f for f in info_fields if label_campo == f['label'].lower().replace(' ','_') and (f['group'] or f['field_type']=='catalog-select')} )
                    for f in info_fields:
                        f_label = f['label'].lower().replace(' ','_')
                        if f['field_type']=='catalog-select':# and label_campo == f_label:
                            label_catalog = dict_catalogs[f['catalog']['catalog_field_id']]['label'].lower().replace(' ','_')
                            if (label_catalog+':_'+f_label) in grupo_campo:
                                pos_field_dict_grupos.update({pos:f})
                        if f['group']:
                            label_grupo = dict_grupos[f['group']['group_id']]
                            if grupo_campo == label_grupo+':_'+f_label:
                                pos_field_dict_grupos.update({pos:f})
                pos_field_dict.update(pos_field_dict_grupos)
            #print("------ pos_field_dict:",pos_field_dict)
            # Creo una lista con las posiciones de los campos que no son Grupos, me servirá para crear o aun no el registro
            not_groups = [header_dict[h] for h in header_dict if h not in list_groups and h != 'folio']
            print("++++ not_groups",not_groups)
            # Metadatos de la forma donde se creará el registro
            metadata_form = self.lkf_api.get_metadata(form_id=id_forma_seleccionada )
            # Necesito un diccionario que agrupe los registros que se crearán y los que están en un grupo repetitivo y pertenecen a uno principal
            group_records = {i:[] for i,r in enumerate(records) if [r[j] for j in not_groups if r[j]]}
            grupo = None
            for i, r in enumerate(records):
                if grupo == None:
                    continue
                if [r[j] for j in not_groups if r[j]]:
                    grupo = i
                else:
                    group_records[grupo].append(i)
            print("++++ group_records",group_records)
            # Obtengo una lista de campos que son de tipo file o images
            file_records = [i for i in pos_field_dict if pos_field_dict[i]['field_type'] in ('file','images')]
            print("++++ file_records",file_records)
            # Agrego información de la carga
            metadata_form.update({'properties': {"device_properties":{"system": "SCRIPT","process":"Carga Universal", "accion":'CREA Y ACTUALIZA REGISTROS DE CUALQUIER FORMA', "folio carga":self.current_record['folio'], "archive":"carga_documentos_a_forma.py"}}})
            print("***** Empezando con la carga de documentos *****")
            resultado = {'creados':0,'error':0,'actualizados':0, 'no_update':0}
            answers = {}
            total_rows = len(records)
            subgrupo_errors = []
            dict_records_to_multi = {'create': [], 'update': []}
            dict_records_copy = {'create': [], 'update': {}}
            list_cols_for_upload = list( pos_field_dict.keys() )
            print('list_cols_for_upload =',list_cols_for_upload)
            metadata = None
            for p, record in enumerate(records):
                print("=========================================== >> Procesando renglon:",p)
                if p in subgrupo_errors:
                    error_records.append(record+['',])
                    continue
                # Recorro la lista de campos de tipo documento para determinar si el contenido en esa posición está dentro del zip de carga
                no_en_zip = [record[i] for i in file_records if record[i] and record[i] not in files_dir]
                new_record = [record[i] for i in not_groups if record[i] and i in list_cols_for_upload]
                if new_record and p != 0:
                    if metadata.get('answers',{}):
                        proceso = self.crea_actualiza_record(metadata, existing_records, error_records, records, sets_in_row, dict_records_to_multi, dict_records_copy, ids_fields_no_update)
                        if proceso:
                            resultado[proceso] += 1
                    answers = {}
                if new_record:
                    sets_in_row = {p: group_records[p]}
                if no_en_zip:
                    docs_no_found = ''
                    docs_no_found += ', '.join([str(a) for a in no_en_zip if a])
                    error_records.append(record+['Los documentos %s no se encontraron en el Zip'%(docs_no_found),])
                    resultado['error'] += 1
                    if new_record:
                        subgrupo_errors = group_records[p]
                        metadata = metadata_form.copy()
                        metadata.update({'answers': {}})
                    continue
                answers = self.procesa_row(pos_field_dict, record, files_dir, nueva_ruta, id_forma_seleccionada, answers, p, dict_catalogs)
                if new_record:
                    if folio_manual and not record[0]:
                        error_records.append(record+['La forma tiene configurado el folio manual por lo que el registro requiere un número de Folio'])
                        resultado['error'] += 1
                        subgrupo_errors = group_records[p]
                        continue
                    metadata = metadata_form.copy()
                    metadata.update({'answers': answers})
                    if folio_manual or (header_dict.get('folio') and header_dict['folio'] == 0):
                        metadata.update({'folio':str(record[0])})
                if p == total_rows-1:
                    if metadata == None:
                        metadata = metadata_form.copy()
                        metadata.update({'answers': answers})
                        sets_in_row = {
                            0: list(group_records.keys())
                        }
                    proceso = self.crea_actualiza_record(metadata, existing_records, error_records, records, sets_in_row, dict_records_to_multi, dict_records_copy, ids_fields_no_update)
                    if proceso:
                        resultado[proceso] += 1
            print('***************dict_records_to_multi update=',dict_records_to_multi['update'])
            #print('***************dict_records_copy=',dict_records_copy)
            #dict_sets_in_row = {}
            if dict_records_to_multi['create']:
                dict_sets_in_row = {x: list_create['sets_in_row'] for x, list_create in enumerate(dict_records_to_multi['create'])}
                response_multi_post = self.lkf_api.post_forms_answers_list(dict_records_to_multi['create'])
                print('===== response_multi_post:', response_multi_post)
                for x, dict_res in enumerate(response_multi_post):
                    sets_in_row = dict_sets_in_row[x]
                    res_status = dict_res.get('status_code', 300)
                    if res_status < 300:
                        resultado['creados'] += 1
                    else:
                        resultado['error'] += 1
                        msg_error_sistema = self.arregla_msg_error_sistema(dict_res)
                        for g in sets_in_row:
                            s = sets_in_row[g]
                            error_records.append(dict_records_copy['create'][g]+[msg_error_sistema,])
                            for dentro_grupo in s:
                                error_records.append(dict_records_copy['create'][dentro_grupo]+['',])
            if dict_records_to_multi['update']:
                #dict_sets_in_row = {x: list_create['sets_in_row'] for x, list_create in enumerate(dict_records_to_multi['update'])}
                response_bulk_patch = self.lkf_api.bulk_patch(dict_records_to_multi['update'], id_forma_seleccionada, threading=True)
                print('===== response_bulk_patch=',response_bulk_patch)
                for f in response_bulk_patch:
                    dict_res = response_bulk_patch[ f ]
                    sets_in_row = dict_records_copy['update'][f]
                    res_status = dict_res.get('status_code', 300)
                    if res_status < 300:
                        resultado['actualizados'] += 1
                    else:
                        resultado['error'] += 1
                        msg_error_sistema = self.arregla_msg_error_sistema(dict_res)
                        for g in sets_in_row:
                            s = sets_in_row[g]
                            error_records.append(records[g]+[msg_error_sistema,])
                            for dentro_grupo in s:
                                error_records.append(records[dentro_grupo]+['',])
            try:
                if files_dir:
                    # Elimino todos los archivos después de que ya los procesé
                    for file_cargado in files_dir:
                        os.remove(os.path.join(nueva_ruta, file_cargado))
                    #os.remove(nueva_ruta+file)
                    shutil.rmtree(nueva_ruta)
            except Exception as e:
                print("********************* exception borrado",e)
                return False
            if not resultado['error']:
                if self.current_record['answers'].get(self.field_id_error_records):
                    sin_file_error = self.current_record['answers'].pop(self.field_id_error_records)
                if not resultado['creados'] and not resultado['actualizados']:
                    return self.update_status_record(self.current_record, self.record_id, 'error', msg_comentarios='Registros Creados: %s, Actualizados: %s, No actualizados por información igual: %s'%(str(resultado['creados']), str(resultado['actualizados']), str(resultado['no_update'])))
                else:
                    return self.update_status_record(self.current_record, self.record_id, 'carga_terminada', msg_comentarios='Registros Creados: %s, Actualizados: %s, No actualizados por información igual: %s'%(str(resultado['creados']), str(resultado['actualizados']), str(resultado['no_update'])))
            else:
                if error_records:
                    if self.record_id:
                        self.current_record['answers'].update( self.lkf_api.make_excel_file(header + ['error',], error_records, self.current_record['form_id'], self.field_id_error_records) )
                    else:
                        error_file = self.lkf_api.make_excel_file(header + ['error',], error_records, None, self.field_id_error_records, is_tmp=True)
                        dict_respuesta = {
                            'error': 'Registros Creados: {}, Actualizados: {}, Erroneos: {}, No actualizados por información igual: {}'.format( resultado['creados'], resultado['actualizados'], resultado['error'], resultado['no_update'] )
                        }
                        dict_respuesta.update(error_file)
                        return dict_respuesta
                return self.update_status_record(self.current_record, self.record_id, 'error', msg_comentarios='Registros Creados: %s, Actualizados: %s, Erroneos: %s, No actualizados por información igual: %s'%(str(resultado['creados']), str(resultado['actualizados']), str(resultado['error']), str(resultado['no_update'])))
            return True
        # except Exception as e:
        #     print("------------------- error:",e)
        #     return self.update_status_record(current_record, record_id, 'error', msg_comentarios='Ocurrió un error inesperado, favor de contactar a soporte')