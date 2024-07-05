# -*- coding: utf-8 -*-
### Linkaform Modules / Archivo de Modulo ###
'''
Archivo para utilizar las funcionalidades modulares de LinkaForm.
Con estas funcionalides podras utilizar la plafaorma de LinkaForm de 
manera modular, como un Backend as a Service o BaaS.
Este es un codigo es lincenciado bajo la licencia GPL3 (https://www.gnu.org/licenses/gpl-3.0.html)
El codigo es auto documentable y adaptable. Con la idea de que puedas reutilizar
gran parte del codigo en otros modulos, copiando y pegando en los nuevo modulos.
Al hacer esto, FAVOR de al copiar secciones de codigo, COPIAR CON TODO Y SU DOCUMENTACION.
Al hacer un documento nuevo o modulo nuevo, puedes copiarte de la carpeta _templates o de sus archivos,
pero cada que hagas un nuevo archivo, favor de copiar estas instrucciones y las generales que apliquen a 
cada archivo.
'''

### Archivo de Modulo ###
'''
En este archivo de define las funciones generales del modulo. Estos seran nombrados por conveniencia
app.py, si llegaras a tener mas de una app, puedes crear un folder llamado app o sencillamente guardarlos
a primer nivel. Tambien puedes hacer archvios llamados por conveniencia o estandar:
app_utils.py, utils.py, xxx_utils.py       
'''

import simplejson
from bson import ObjectId

from linkaform_api import base
from lkf_addons.addons.employee.employee_utils import Employee
from lkf_addons.addons.location.location_util import Location


### Objeto o Clase de Modulo ###
'''
Cada modulo puede tener N objetos, configurados en clases.
Estos objetos deben de heredar de base.LKF_Base) y cualquier modulo dependiente.
Al hacer el super() del __init__(), heredamos las variables de configuracion de clase.

Se pueden heredar funciones de cualquier clase heredada con el metodo super(). 
'''
class Accesos(Employee, Location, base.LKF_Base):

    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False):
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api)
        #--Variables 
        # Forms #
        '''
        self.FORM_NAME = self.lkm.form_id('form_name',id)
        aqui deberas guardar el los ID de los formularios. 
        Para ello ocupas llamar el metodo lkm.form_id del objeto lkm(linkaform modules, por sus siglas, 
        en lkm estan todas las funcions generales de modulos).

        '''
        self.ACCESOS_NOTAS = self.lkm.form_id('notas','id')
        self.CHECKIN_CASETAS = self.lkm.form_id('checkin_checkout_casetas','id')
        self.PASE_ENTRADA = self.lkm.form_id('pase_de_entrada','id')
        self.VISITA_AUTORIZADA = self.lkm.form_id('visita_autorizada','id')
        self.BITACORA_ACCESOS = self.lkm.form_id('bitacora_de_entradas_y_salidas','id')
        self.BITACORA_INCIDENCIAS = self.lkm.form_id('bitacora_de_incidencias','id')
        self.PUESTOS_GUARDIAS = self.lkm.form_id('puestos_de_guardias','id')

        
        self.last_check_in = []
        # self.FORM_ALTA_COLABORADORES = self.lkm.form_id('alta_de_colaboradores_visitantes','id')
        # self.FORM_ALTA_EQUIPOS = self.lkm.form_id('alta_de_equipos','id')
        # self.FORM_ALTA_VEHICULOS = self.lkm.form_id('alta_de_vehiculos','id')
        # #self.FORM_BITACORA = self.lkm.form_id('bitacora','id')
        # self.FORM_LOCKER = self.lkm.form_id('locker','id')
        #self.FORM_PASE_DE_ENTRADA = self.lkm.form_id('pase_de_entrada','id')
        #self.FORM_REGISTRO_PERMISOS = self.lkm.form_id('registro_de_permisos','id')

        # catalogos
        '''
        self.CATALOG_NAME = self.lkm.catalog_id('catalog_name',id)
        aqui deberas guardar el los ID de los catalogos. 
        Para ello ocupas llamar el metodo lkm.catalog_id del objeto lkm(linkaform modules, por sus siglas, 
        en lkm estan todas las funcions generales de modulos).

        '''
        self.VISITA_AUTORIZADA_CAT = self.lkm.catalog_id('visita_autorizada')
        self.VISITA_AUTORIZADA_CAT_ID = self.VISITA_AUTORIZADA_CAT.get('id')
        self.VISITA_AUTORIZADA_CAT_OBJ_ID = self.VISITA_AUTORIZADA_CAT.get('obj_id')
        self.PASE_ENTRADA_CAT = self.lkm.catalog_id('pase_de_entrada')
        self.PASE_ENTRADA_ID = self.PASE_ENTRADA_CAT.get('id')
        self.PASE_ENTRADA_OBJ_ID = self.PASE_ENTRADA_CAT.get('obj_id')

        self.CONFIG_PERFILES = self.lkm.catalog_id('configuracion_de_perfiles')
        self.CONFIG_PERFILES_ID = self.CONFIG_PERFILES.get('id')
        self.CONFIG_PERFILES_OBJ_ID = self.CONFIG_PERFILES.get('obj_id')
        # self.CONF_PERFIL = self.lkm.catalog_id('configuracion_de_perfiles','id')
        # self.CONF_PERFIL_ID = self.CONF_PERFIL.get('id')
        # self.CONF_PERFIL_OBJ_ID = self.CONF_PERFIL.get('obj_id')


        # self.AREAS_DE_LAS_UBICACIONES_CAT = self.lkm.catalog_id('areas_de_las_ubicaciones')
        # self.AREAS_DE_LAS_UBICACIONES_CAT_ID = self.AREAS_DE_LAS_UBICACIONES_CAT.get('id')
        # self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID = self.AREAS_DE_LAS_UBICACIONES_CAT.get('obj_id')
        #----Dic Fields Forms

        ## Module Fields ##
        ''' self.mf : Estos son los campos que deseas mantener solo dentro de este modulo '''
        mf = {
            'bitacora_salida':'662c51eb194f1cb7a91e5af0',
            'bitacora_entrada':'662c51eb194f1cb7a91e5aef',
            'catalog_caseta':'66566d60d4619218b880cf04',
            'catalog_caseta_salida':'66566d60464fe63529d1c543',
            'catalog_guard':'664fc645276795e17ea76dc4',
            'catalog_guard_close':'664fc64242c59486fadd0a27',
            'catalog_ubicacion':'664fc5d9860deae4c20954e2',
            'catalog_visita':'664fc6f5d6078682a4dd0ab3',
            'caseta':'663e5d44f5b8a7ce8211ed0f',
            'caseta_salida':'663fb45992f2c5afcfe97ca8',
            'config_dia_de_acceso': "662c304fad7432d296d92584",
            'config_limitar_acceso': "6635380dc9b3e7db4d59eb49",
            'config_dias_acceso': "662c304fad7432d296d92585",
            'codigo_qr':'6685da34f065523d8d09052b',
            'curp': "5ea0897550b8dfe1f4d83a9f",
            'documento': "663e5470424ad55e32832eec",
            'email_vsita': "5ea069562f8250acf7d83aca",
            'empresa':'64ecc95271803179d68ee081',
            'fecha_desde_visita': "662c304fad7432d296d92582",
            'fecha_entrada': "662c51eb194f1cb7a91e5aef",
            'fecha_hasta_visita': "662c304fad7432d296d92583",
            'field_note':'6647fadc96f80017ac388648',
            'foto':'5ea35de83ab7dad56c66e045',
            'gafete':'663e530af52d352956832f72',
            'guard_group':'663fae53fa005c70de59eb95',
            'grupo_visitados': "663d4ba61b14fab90559ebb0",
            'identificacion':'65ce34985fa9df3dbf9dd2d0',
            'nota': "6647fadc96f80017ac388647",
            'nombre_guardia': "62c5ff407febce07043024dd",
            'nombre_visita': "5ea0693a0c12d5a8e43d37df",
            'nombre_perfil': "661dc67e901906b7e9b73bac",
            'nombre_guardia_apoyo': "663bd36eb19b7fb7d9e97ccb",
            'rfc':"64ecc95271803179d68ee081",
            'status_visita':'5ea1bd280ae8bad095055e61',
            'telefono':'661ea59c15baf5666f32360e',
            'tipo_de_guardia': "6684484fa5fd62946c12e006",
            'tipo_registro': "66358a5e50e5c61267832f90",
            'tipo_visita_pase': "662c304fad7432d296d92581",
            'ubicacion': "663e5c57f5b8a7ce8211ed0b",


        }
        self.mf = mf
        ## Form Fields ##
        '''
        self.form_name : En esta seccion podras agrupar todos los campos ya sea por forma o como dease
        enviarls hacia tus servicios, en el caso de las busquedas de mongo, pudes hacer las busquedas de
        Manera Anidada Por lo cual podras agrupar separadas por punto, ej.663d4ba61b14fab90559ebb0.665f482cc9a2f8acf685c20b
        y asi podras hacer la busquedas directo en la base de datos.

        Estos campos podras agregarlos asi directo a self.f , donde se agurpan todos los fields de los modulos heredados

        '''

       
        #- Para salida de bitacora y lista
        self.bitacora_fields = {
            'nombre_visita':f"{self.mf['catalog_visita']}.{self.mf['nombre_visita']}",
            'perfil_visita':f"{self.mf['catalog_visita']}.{self.mf['nombre_perfil']}",
            'status_visita':f"{self.mf['tipo_registro']}",
            'ubicacion':f"{self.mf['catalog_ubicacion']}.{self.mf['ubicacion']}",
            'caseta_entrada':f"{self.mf['catalog_caseta']}.{self.mf['caseta']}",
            'gafete':f"{self.mf['gafete']}",
            'codigo_qr':f"{self.mf['codigo_qr']}",
            'documento':f"{self.mf['documento']}",
            'caseta_salida':f"{self.mf['catalog_caseta_salida']}.{self.mf['caseta_salida']}",
            'bitacora_salida':f"{self.mf['bitacora_salida']}",
            'bitacora_entrada':f"{self.mf['bitacora_entrada']}",
        }
        self.checkin_fields = {
            'checkin_type': '663bffc28d00553254f274e0',
            'checkin_date':'663bffc28d00553254f274e1',
            'checkout_date':'663bffc28d00553254f274e2',
            'guard_group': mf['guard_group'],
            'employee_position':'665f482cc9a2f8acf685c20b',
            'cat_created_by': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_name']}",
            'created_by': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_name']}",
            'employee': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_name']}",
            'cat_location': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['location']}",
            'cat_area': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['area']}",
            'cat_employee_b': f"{self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID}.{self.f['worker_name_b']}",
        }
        #- Para creación , edición y lista de incidencias
        self.incidence_fields = {
            'date_incidence':'66396efeb37283c921e97cdf',
            'catalog_incidence':'664fc6c7276795e17ea76dc9',
            'incidence':'663973809fa65cafa759eb97',
            'comments':'66397586aa8bbc0371e97c80',
        }
        #- Para creación , edición y lista de notas
        self.notes_fields = {
            'note_status':'6647f9eb6eefdb1840684dc1',
            'note_open_date':'6647fadc96f80017ac388646',
            'note_close_date':'6647fadc96f80017ac38864a',
            'note_catalog_booth':f"{self.mf['catalog_caseta']}",
            'note_booth':f"{self.mf['caseta']}",
            'note_catalog_guard':f"{self.mf['catalog_guard']}",
            'note_guard':f"{self.mf['nombre_guardia']}",
            'note_catalog_guard_close':f"{self.mf['catalog_guard_close']}",
            'note_guard_close':f"{self.mf['nombre_guardia_apoyo']}",
            'note':'6647fadc96f80017ac388647',
            'note_file':'6647fadc96f80017ac388648',
            'note_pic':'6647fadc96f80017ac388649',
            'note_comments_group':'6647fb1874c1a87eb02a9037',
            'note_comments':'6647fb38da07bf430e273ea2',
        }
        self.notes_project_fields = {
            'location': f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['location']}",
            'area': f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['area']}",
            'created_by': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_name']}",
            'closed_by': f"{self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID}.{self.f['worker_name_b']}",
            'support_guard':f"{self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID}.{self.f['worker_name_b']}",
        }
        self.pase_entrada_fields = {}
        self.pase_grupo_visitados:{
            'nombre_perfil':     f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_name']}",
            'worker_department': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_department']}",
            'worker_position':   f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_position']}",        
        }
        # self.pase_entrada_fields.update(self.pase_grupo_visitados)
        self.pase_grupo_areas:{
            'nombre_perfil':     f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['area']}",
        }
        # self.pase_entrada_fields.update(self.pase_grupo_areas)
        self.pase_grupo_vehiculos:{
            'nombre_perfil':     f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['area']}",
            'tipo_vehiuclo':   f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_position']}",        
        }
        # self.pase_entrada_fields.update(self.pase_grupo_vehiculos)
        self.pase_entrada_fields.update({
            'ubicacion': f"{self.UBICACIONES_CAT_OBJ_ID}.{self.f['location']}",
            'nombre_visita': f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{mf['nombre_visita']}",
            'email_vsita': f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{self.mf['email_vsita']}",
            'curp': self.unlist(f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{mf['curp']}"),
            'rfc': f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{mf['rfc']}",
            'telefono': f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{mf['telefono']}",
            'foto': f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{mf['foto']}",
            'identificacion': f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{mf['identificacion']}",
            'empresa': f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{mf['empresa']}",
            'status_visita': f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{mf['status_visita']}",
            'nombre_perfil': f"{self.CONFIG_PERFILES_OBJ_ID}.{mf['nombre_perfil']}",
            'grupo_visitados': self.mf['grupo_visitados'],
            #'nombre_perfil': f"{self.mf['grupo_visitados']}{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_name']}",
            'worker_department': f"{self.mf['grupo_visitados']}{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_department']}",
            'worker_position': f"{self.mf['grupo_visitados']}{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_position']}",
            'tipo_visita_pase': self.mf['tipo_visita_pase'],
            'grupo_visitados': self.mf['grupo_visitados'],
            'fecha_desde_visita': self.mf['fecha_desde_visita'],
            'fecha_hasta_visita': self.mf['fecha_hasta_visita'],
            'config_dia_de_acceso': self.mf['config_dia_de_acceso'],
            'config_limitar_acceso': self.mf['config_limitar_acceso'],
            'config_dias_acceso': self.mf['config_dias_acceso'],
        })

        self.notes_project_fields.update(self.notes_fields)
        self.bitacora_acceos = {}
        ## Fields ##
        '''
        self.f : En esta vairable "fields", se almacenan todos los campos de todos lo modulos heredados.
        El orden de remplazo de ve afectado por el orden en que se hereda cada modulo. El orden que se otroga, es considerando
        que la vaiable se iguala en la base, y se va armando en tren de dependencias ej.
            Class A:
            Class B(A):
            Class C(B):
            Class D(C):

            x_obj = D()
            el orden de heredacion sera, primero carga A>B>C>D.
        '''
        self.f.update(self.notes_fields)
        self.f.update(self.checkin_fields)

    '''
    _funciones internas: son funciones que solo se pueden mandar llamar dentro de este archivo. Si se hereda la clase
    esta funcion no puede ser invocada.
    pep-0008:
        _single_leading_underscore: 
        weak “internal use” indicator. E.g. from M import * does not import objects whose names start with an underscore.
    '''
    def create_incidence(self, data_incidences):
        #---Define Metadata
        metadata = self.lkf_api.get_metadata(form_id=self.BITACORA_INCIDENCIAS)
        metadata.update({
            "properties": {
                "device_properties":{
                    "System": "Script",
                    "Module": "Accesos",
                    "Process": "Creación de incidencias",
                    "Action": "create_incidence",
                    "File": "accesos/app.py"
                }
            },
        })
        #---Define Answers
        answers = {}
        for key, value in data_incidences.items():
            if  key == 'ubicacion_incidence':
                dic_prev = answers.get(self.mf['catalog_caseta'],{})
                dic_prev[self.mf['ubicacion']] = value 
                answers[self.mf['catalog_caseta']] = dic_prev
            elif  key == 'area_incidence':
                dic_prev = answers.get(self.mf['catalog_caseta'],{})
                dic_prev[self.mf['caseta']] = value 
                answers[self.mf['catalog_caseta']] = dic_prev
            elif  key == 'note_guard':
                answers[self.mf['catalog_guard']] = {self.mf['nombre_guardia']:value}
            elif  key == 'incidence':
                answers[self.incidence_fields['catalog_incidence']] = {self.incidence_fields['incidence']:value}
            else:
                answers.update({f"{self.incidence_fields[key]}":value})
        metadata.update({'answers':answers})
        return self.lkf_api.post_forms_answers(metadata)

    def create_note(self, data_notes):
        '''
        '''
        #---Define Metadata
        metadata = self.lkf_api.get_metadata(form_id=self.ACCESOS_NOTAS)
        metadata.update({
            "properties": {
                "device_properties":{
                    "System": "Script",
                    "Module": "Accesos",
                    "Process": "Creación de notas",
                    "Action": "Create Note",
                    "File": "accesos/app.py"
                }
            },
        })
        #---Define Answers
        answers = {}
        for key, value in data_notes.items():
            if key == 'note_comments':
                answers[self.notes_fields['note_comments_group']] = answers.get(self.notes_fields['note_comments_group'],[])
                for comment in value:
                    answers[self.notes_fields['note_comments_group']].append({self.notes_fields['note_comments']:comment})
            elif  key == 'note_booth':
                answers[self.notes_fields['note_catalog_booth']] = {self.notes_fields['note_booth']:value}
            elif  key == 'note_guard':
                answers[self.notes_fields['note_catalog_guard']] = {self.notes_fields['note_guard']:value}
            else:
                answers.update({f"{self.notes_fields[key]}":value})

        metadata.update({'answers':answers})
        #print('answers', simplejson.dumps(metadata, indent=4))
        return self.lkf_api.post_forms_answers(metadata)
        #print('response_create',response_create)

    def delete_notes(self, folio):
        response = self.get_record_by_folio(folio, self.ACCESOS_NOTAS, select_columns={'_id':1,})
        if response.get('_id'):
            return self.lkf_api.patch_record_list({
                "deleted_objects": ["/api/infosync/form_answer/"+str(response['_id'])+"/"],
            })
        else:
            self.LKFException('No se encontro el folio correspondiente')


    def delete_incidence(self, folio):
        response = self.get_record_by_folio(folio, self.BITACORA_INCIDENCIAS, select_columns={'_id':1,})
        if response.get('_id'):
            return self.lkf_api.patch_record_list({
                "deleted_objects": ["/api/infosync/form_answer/"+str(response['_id'])+"/"],
            })
        else:
            self.LKFException('No se encontro el folio correspondiente')

    def _do_access(self, access_pass, location, area, vehiculo, equipo):
        '''
        Registra el acceso del pase de entra a ubicacion
        solo puede ser ejecutado despues de revisar los accesos
        '''
        employee =  self.get_employee_data(email=self.user.get('email'), get_one=True)
        metadata = self.lkf_api.get_metadata(form_id=self.BITACORA_ACCESOS)
        metadata.update({
            'properties': {
                "device_properties":{
                    "System": "Script",
                    "Module": "Accesos",
                    "Process": "Ingreso de Personal",
                    "Action": 'Do Access',
                    "File": "accesos/app.py"
                }
            },
        })
        # metadata['folio'] = self.create_poruction_lot_number()
        print('access_pass', access_pass)
        pase = {
                f"{self.mf['nombre_visita']}": access_pass['nombre_visita'],
                f"{self.mf['curp']}":access_pass['curp'],
                f"{self.mf['nombre_perfil']}": access_pass['nombre_perfil'],
                f"{self.mf['email_vsita']}":access_pass['email_vsita'],
                f"{self.mf['foto']}":access_pass['foto'],
                f"{self.mf['identificacion']}":access_pass['identificacion'],
                f"{self.mf['empresa']}":access_pass['empresa'],
                f"{self.mf['status_visita']}":access_pass['status_visita'],
                }
        answers = {
            f"{self.mf['tipo_registro']}": 'entrada',
            f"{self.UBICACIONES_CAT_OBJ_ID}":{f"{self.f['location']}":location},
            f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}":{f"{self.f['area']}":area},
            f"{self.PASE_ENTRADA_OBJ_ID}":pase,
            f"{self.mf['codigo_qr']}":access_pass['_id'],
            f"{self.mf['fecha_entrada']}":self.today_str(employee.get('timezone', 'America/Monterrey'), date_format='datetime'),
        }
        # print('answers', simplejson.dumps(answers, indent=4))
        metadata.update({'answers':answers})
        print('answers', simplejson.dumps(metadata, indent=4))
        response_create = self.lkf_api.post_forms_answers(metadata)
        print('response_create',response_create)

    def do_access(self, qr_code, location, area, vehiculo, equipo):
        '''
        Valida pase de entrada y crea registro de entrada al pase
        '''
        print('me quede ahceidno la vaildacion y el registro de entrada')
        if not qr_code and not location and not area:
            return False
        access_pass = self.search_pass(qr_code)
        if self.validate_access_pass_location(qr_code):
            self.LKFException("En usuario ya se encuentra dentro de una ubicacion")
        val_certificados = self.validate_certificados(qr_code, location)
        pass_dates = self.validate_pass_dates(access_pass)
        res = self._do_access(access_pass,  location, area, vehiculo, equipo)

    def do_checkin(self, location, area, employee_list=[]):
        if not self.is_boot_available(location, area):
            msg = f"Can not login in to boot on location {location} at the area {area}."
            msg += f"Because '{self.last_check_in.get('employee')}' is logged in."
            self.LKFException(msg)
        boot_config = self.get_users_by_location_area(location_name=location, area_name=area, user_id=self.user.get('user_id'))
        print('boot_config', boot_config)
        if not boot_config:
            msg = f"User can not login to this area : {area} at location: {location} ."
            msg += f"Please check your configuration."
            self.LKFException(msg)

        employee =  self.get_employee_data(email=self.user.get('email'), get_one=True)
        user_data = self.lkf_api.get_user_by_id(self.user.get('user_id'))
        employee['timezone'] = user_data.get('timezone','America/Monterrey')
        if not employee:
            msg = f"Ningun empleado encontrado con email: {self.user.get('email')}"
            self.LKFException(msg)
        timezone = employee.get('cat_timezone')
        data = self.lkf_api.get_metadata(self.CHECKIN_CASETAS)
        checkin = self.checkin_data(employee, location, area, 'in', timezone)
        checkin = self.checkout_employees(checkin=checkin, employee_list=employee_list, replace=True)
        data.update({
                'properties': {
                    "device_properties":{
                        "system": "Modulo Acceos",
                        "process": 'Checkin-Checkout',
                        "action": 'do_checkin',
                        "archive": "accesos_utils.py"
                    }
                },
                'answers': checkin
            })
        resp_create = self.lkf_api.post_forms_answers(data)
        #TODO agregar nombre del Guardia Quien hizo el checkin
        if resp_create.get('status_code') == 201:
            resp_create['json'].update({'boot_status':{'guard_on_duty':user_data['name']}})
        return resp_create

    def do_checkout(self, checkin_id=None, location=None, area=None, guards=[]):
        print('--start checkout--')
        # self.get_answer(keys)
        if checkin_id:
            print('--start checkin_id--', checkin_id)
            checkin_record = self.get_checkin_by_id(_id=checkin_id)
            print('checkin_record', checkin_record)
            area = checkin_record.get('cat_area', area)
            location = checkin_record.get('cat_location', location)
            guards = checkin_record.get('guard_group')
        if self.is_boot_available(location, area):
            msg = f"Can not make a CHEKOUG on a boot that hasn't checkin. Location: {location} at the area {area}."
            msg += f"You need first to checkin."
            self.LKFException(msg)
        employee =  self.get_employee_data(email=self.user.get('email'), get_one=True)
        timezone = employee.get('cat_timezone')
        data = self.lkf_api.get_metadata(self.CHECKIN_CASETAS)
        checkin = self.checkin_data(employee, location, area, 'out', timezone)
        checkin = self.checkout_employees(checkin=checkin, employee_list=guards, replace=False)
        data.update({
                'properties': {
                    "device_properties":{
                        "system": "Modulo Acceos",
                        "process": 'Checkin-Checkout',
                        "action": 'do_checkout',
                        "archive": "accesos_utils.py"
                    }
                },
                'answers': checkin
            })
        resp_create = self.lkf_api.post_forms_answers(data)
        print('resp_create',resp_create)
        return resp_create

    def checkin_data(self, employee, location, area, checkin_type, timezone):
        if checkin_type == 'in':
            set_type = 'entrada'
        elif checkin_type == 'out':
            set_type = 'salida'
        checkin = {
            self.f['checkin_type']: set_type,
            self.f['checkin_date'] : self.today_str(employee.get('timezone', 'America/Monterrey'), date_format='datetime'),
            self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID : {
                self.f['location']: location,
                self.f['area']: area, 
                self.f['worker_name']: employee.get('worker_name'),
            },

        }
        if checkin_type == 'in':
            checkin.update({self.f['guard_group']:[
                {self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID:{
                    self.f['worker_name_b']: employee.get('worker_name'),
                    },
                self.f['employee_position']: 'jefe_en_guardia'
                }
                ]
                })
        else:
            checkin.update({self.f['guard_group']:[]})
        return checkin

    def do_out(self, qr):
        '''
            Realiza el cambio de estatus de la forma de bitacora, relacionada a la salida, como parametro
            es necesesario enviar el nombre del visitante que es el unico dato qu se encuentra en la forma
        '''
        response = False
        last_check_out = self.get_last_user_move(qr)
        if last_check_out.get('folio'):
            folio = last_check_out.get('folio',0)
            if self.user_in_facility(status_visita=last_check_out.get('status_visita')):
                answers = {
                    f"{self.mf['tipo_registro']}":'salida',
                }
                response = self.lkf_api.patch_multi_record( answers=answers, form_id=self.BITACORA_ACCESOS, folios=[folio])
        if not response:
            self.LKFException("El usuario se encuentra fuera de la ubicacion.")
        return response            

    def config_get_guards_positions(self):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.PUESTOS_GUARDIAS,
            }        
        unwind = {'$unwind': f"$answers.{self.f['guard_group']}"}
        query = [
            {'$match': match_query },
            {'$unwind': f"$answers.{self.f['guard_group']}"},
            {'$project':{
                "_id":0,
                'tipo_de_guardia': f"$answers.{self.f['guard_group']}.{self.mf['tipo_de_guardia']}",
                'puesto': f"$answers.{self.f['guard_group']}.{self.PUESTOS_OBJ_ID}.{self.f['worker_position']}"
                }
            },
            {'$unwind': f"$tipo_de_guardia"},
            {'$group':{
                '_id':{
                    'tipo_de_guardia':'$tipo_de_guardia'
                    },
                'puestos': {'$addToSet':'$puesto'}
                }
            },
            {'$project':{
                "_id":0,
                'tipo_de_guardia': '$_id.tipo_de_guardia',
                'puestos': '$puestos',
                }
            },
            {'$sort': {'tipo_de_guardia':1}}
            ]
        return self.format_cr_result(self.cr.aggregate(query))

    def get_access_pass(self, qr_code):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.CHECKIN_CASETAS,
            }
        if _id:
            match_query.update({"_id":ObjectId(_id)})

    def get_access_notes(self, location_name, area_name):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.ACCESOS_NOTAS,
            f"answers.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['location']}":location_name,
            f"answers.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['area']}":area_name
            }
        query = [
            {'$match': match_query },
            {'$project': self.proyect_format(self.notes_project_fields)},
            {'$sort':{self.f['note_open_date']:1}}
            ]
        return self.format_cr_result(self.cr.aggregate(query))

    def get_booth_status(self, booth_area, location):
        last_chekin = self.get_last_checkin(location, booth_area)
        booth_status = {
            "status":'Disponible',
            "guard_on_dutty":'',
            "user_id":'',
            "stated_at":'',
            }
        if last_chekin.get('checkin_type') == 'entrada':
            #todo
            #user_id 
            booth_status['status'] = 'No Disponible'
            booth_status['guard_on_dutty'] = last_chekin.get('employee') 
            booth_status['stated_at'] = last_chekin.get('checkin_date')
            booth_status['checkin_id'] = last_chekin['_id']

        return booth_status

    def get_booth_stats(self, booth_area, location):
        res ={
                "in_invitees":11,
                "articulos_concesionados":12,
                "incidentes_pendites": 13,
                "vehiculos_estacionados": 14,
                "gefetes_pendientes": 15,
            }
        return res

    def get_checkin_by_id(self, _id=None, folio=None):
        if not _id or not folio:
            msg = "An _id or a folio is requierd to get the record"
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.CHECKIN_CASETAS,
            }
        if _id:
            match_query.update({"_id":ObjectId(_id)})
        elif folio:
            match_query.update({"folio":folio})
        query = [
            {'$match': match_query },
            {'$project': self.proyect_format(self.checkin_fields)},
            {'$sort':{'updated_at':-1}},
            {'$limit':1}
            ]
        return self.format_cr_result(self.cr.aggregate(query), get_one=True)
 
    def get_last_checkin(self, location, area):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.CHECKIN_CASETAS,
            f"answers.{self.checkin_fields['cat_location']}":location,
            f"answers.{self.checkin_fields['cat_area']}":area,
            }
        query = [
            {'$match': match_query },
            {'$project': self.proyect_format(self.checkin_fields)},
            {'$sort':{'updated_at':-1}},
            {'$limit':1}
            ]
        return self.format_cr_result(self.cr.aggregate(query), get_one=True)

    def get_last_user_move(self, qr):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.BITACORA_ACCESOS,
            f"answers.{self.bitacora_fields['codigo_qr']}":qr,
        }
        query = [
            {'$match': match_query },
            {'$project': {
                'updated_at':'$updated_at',
                'folio':'$folio',
                'status_visita': f"$answers.{self.bitacora_fields['status_visita']}"
                }},
            {'$sort':{'updated_at':-1}},
            {'$limit':1}
        ]
        res = self.cr.find(
            match_query, 
            {'folio':'$folio', 'status_visita': f"$answers.{self.bitacora_fields['status_visita']}"}
            ).sort('updated_at', -1).limit(1)
        return self.format_cr_result(res, get_one=True)
        # return self.format_cr_result(self.cr.aggregate(query), get_one=True)

    def get_list_bitacora(self, location, area):
        response = []
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.BITACORA_ACCESOS,
            f"answers.{self.bitacora_fields['ubicacion']}":location,
            f"answers.{self.bitacora_fields['caseta_entrada']}":area,
        }
        query = [
            {'$match': match_query },
            {'$project': self.proyect_format(self.bitacora_fields)},
            {'$sort':{'folio':-1}},
        ]
        response.append(self.format_cr_result(self.cr.aggregate(query), get_one=True))
        return response

    def get_list_incidences(self, location, area):
        response = []
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.BITACORA_INCIDENCIAS,
            f"answers.{self.mf['catalog_caseta']}.{self.mf['ubicacion']}":location,
            f"answers.{self.mf['catalog_caseta']}.{self.mf['caseta']}":area,
        }
        query = [
            {'$match': match_query },
            {'$project': {
                "folio": "$folio",
                "date_incidence": f"$answers.{self.incidence_fields['date_incidence']}",
                "location": f"$answers.{self.mf['catalog_caseta']}.{self.mf['ubicacion']}",
                "area": f"$answers.{self.mf['catalog_caseta']}.{self.mf['caseta']}",
                "incidence": f"$answers.{self.incidence_fields['catalog_incidence']}.{self.incidence_fields['incidence']}",
                "comments": f"$answers.{self.incidence_fields['comments']}",
                "guard": f"$answers.{self.mf['catalog_guard']}.{self.mf['nombre_guardia']}",
            }},
            {'$sort':{'folio':-1}},
        ]
        #print('answers', simplejson.dumps(query, indent=4))
        response.append(self.format_cr_result(self.cr.aggregate(query), get_one=True))
        #print('Response',response)
        return response

    def get_list_notes(self, area):
        '''
        Función para crear nota, psandole los datos de area para filtrar las notas de la caseta

        '''
        response = []
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.ACCESOS_NOTAS,
            f"answers.{self.notes_fields['note_catalog_booth']}.{self.notes_fields['note_booth']}":area,
        }
        query = [
            {'$match': match_query },
            {'$project': {
                "folio":"$folio",
                "note_status": f"$answers.{self.notes_fields['note_status']}",
                "note_open_date": f"$answers.{self.notes_fields['note_open_date']}",
                "note_close_date": f"$answers.{self.notes_fields['note_close_date']}",
                "note_booth": f"$answers.{self.notes_fields['note_catalog_booth']}.{self.notes_fields['note_booth']}",
                "note_guard": f"$answers.{self.notes_fields['note_catalog_guard']}.{self.notes_fields['note_guard']}",
                "note_guard_close": f"$answers.{self.notes_fields['note_catalog_guard_close']}.{self.notes_fields['note_guard_close']}",
                "note": f"$answers.{self.notes_fields['note']}",
                "note_file": f"$answers.{self.notes_fields['note_file']}",
                "note_pic": f"$answers.{self.notes_fields['note_pic']}",
                "note_comments_group": f"$answers.{self.notes_fields['note_comments_group']}",
            }},
            {'$sort':{'folio':-1}},
        ]
        #print('answers', simplejson.dumps(query, indent=4))
        response.append(self.format_cr_result(self.cr.aggregate(query), get_one=True))
        return response

    def get_user_booths_availability(self):
        default_booth , user_booths = self.get_user_booth(search_default=False)
        for booth in user_booths:
            booth_area = booth.get('area')
            location = booth.get('location')
            booth_status = self.get_booth_status(booth_area, location)
            booth['status'] = booth_status.get('status', 'Disponible')
        return user_booths

    def get_user_last_checkin(self, user_id=False):
        if not user_id:
            user_id = self.user.get('user_id')
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.CHECKIN_CASETAS,
            "created_by_id": user_id
            }
        query = [
            {'$match': match_query },
            {'$project': self.proyect_format(self.checkin_fields)},
            {'$sort':{'updated_at':-1}},
            {'$limit':1}
            ]
        return self.format_cr_result(self.cr.aggregate(query), get_one=True)

    def get_user_guards(self, location_employees):
        for employee in location_employees:
            if employee.get('user_id',0) == self.user.get('user_id'):
                    return employee
        self.LKFException(f"El usuario con id {self.user['user_id']}, no se ecuentra configurado como guardia")

    def user_in_facility(self, status_visita):
        """
        Si envias un registro con entrada quiere regresa Verdadero, si 
        """
        print('status_visita=',status_visita)
        if status_visita in ('entrada'):
            return True
        else:
            return False

    def is_boot_available(self, location, area):
        self.last_check_in = self.get_last_checkin(location, area)
        last_status = self.last_check_in.get('checkin_type')
        if last_status == 'entrada':
            return False
        else:
            return True

    def checkout_employees(self, checkin={}, employee_list=[], replace=True):
        if not replace:
            checkin[self.f['guard_group']] = employee_list
        elif employee_list and replace:
            checkin[self.f['guard_group']] += [
                {self.f['employee_position']:'guardiad_de_apoyo',
                 self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID:
                   {self.f['worker_name_b']:guard.get('name'),
                   }} 
                    for guard in employee_list ]
        return checkin

    def update_incidence(self, data_incidences, folio):
        '''
            Realiza una actualización sobre cualquier nota, actualizando imagenes, status etc
        '''
        answers = {}
        for key, value in data_incidences.items():
            if  key == 'ubicacion_incidence':
                dic_prev = answers.get(self.mf['catalog_caseta'],{})
                dic_prev[self.mf['ubicacion']] = value 
                answers[self.mf['catalog_caseta']] = dic_prev
            elif  key == 'area_incidence':
                dic_prev = answers.get(self.mf['catalog_caseta'],{})
                dic_prev[self.mf['caseta']] = value 
                answers[self.mf['catalog_caseta']] = dic_prev
            elif  key == 'note_guard':
                answers[self.mf['catalog_guard']] = {self.mf['nombre_guardia']:value}
            elif  key == 'incidence':
                answers[self.incidence_fields['catalog_incidence']] = {self.incidence_fields['incidence']:value}
            else:
                answers.update({f"{self.incidence_fields[key]}":value})
        if answers or folio:
            return self.lkf_api.patch_multi_record( answers = answers, form_id=self.BITACORA_INCIDENCIAS, folios=[folio])
        else:
            self.LKFException('No se mandarón parametros para actualizar')

    def update_guard_status(self, guard):
        last_checkin = self.get_user_last_checkin(guard['user_id'])
        status_turn = 'Turno Cerrado'
        if last_checkin.get('checkin_type') == 'entrada':
            status_turn = 'Turno Abierto'

        guard['turn_start_datetime'] =  last_checkin.get('checkin_date','')
        guard['status_turn'] =  status_turn
        return guard

    def update_notes(self, data_notes, folio):
        '''
            Realiza una actualización sobre cualquier nota, actualizando imagenes, status etc
        '''
        answers = {}
        for key, value in data_notes.items():
            if key == 'list_comments':
                answers.update({-1:{f"{self.notes_fields[key]}": value}})
            elif  key == 'note_booth':
                answers[self.notes_fields['note_catalog_booth']] = {self.notes_fields['note_booth']:value}
            elif  key == 'note_guard':
                answers[self.notes_fields['note_catalog_guard']] = {self.notes_fields['note_guard']:value}
            else:
                answers.update({f"{self.notes_fields[key]}":value})
        if answers or folio:
            return self.lkf_api.patch_multi_record( answers = answers, form_id=self.ACCESOS_NOTAS, folios=[folio])
        else:
            self.LKFException('No se mandarón parametros para actualizar')
        
    def search_pass(self, qr_code=None, location=None):
        if not qr_code and not location:
            msg = "Debes de proveer qr_code o location"
            self.LKFException(msg)
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.PASE_ENTRADA,
            }
        if qr_code:
            match_query.update({"_id":ObjectId(qr_code)})
        if location:
            match_query.update({f"answers.{self.UBICACIONES_CAT_OBJ_ID}.{self.f['location']}":location})
        query = [
            {'$match': match_query },
            {'$project': self.proyect_format(self.pase_entrada_fields)},
            {'$sort':{'updated_at':-1}},
            {'$limit':1}
            ]
        return self.format_cr_result(self.cr.aggregate(query), get_one=True)

    def search_access_pass(self, qr_code=None, location=None):
        """
        Busca pases de acceso
        Si se entega el puro qr_code, se entrega la info de QR code
        Si se entrega el qr_code con location y area, te valida si el qr es valido para dicha area
        Si NO entregas el qr_code, te regresa todos los qr de dicha area y ubicacion
        Si no entregas nada, te regrea un warning...
        """
        print('-------------- search_access_pass')
        complete_qr = {}
        # location = 'Planta Monterrey'
        # print('match_query', simplejson.dumps(query, indent=4))
        complete_qr['pass'] = {
            'tipo': 'Contratista Tipo XZ',
            'status':'Vigente',
            'fecha_expedicion':'2024-01-15',
            'fecha_expiracion':'2026-01-15',
        }
        complete_qr['validaciones'] = {
            'accion_ingreso':'Entrada',
            'location': self.search_pass(qr_code=qr_code, location=location),
            'errores':[{"tipo":'Certificado','comunicacion':'Vencido','fecha':'2024-05-25'}]
        }
        complete_qr['portador'] = self.search_pass(qr_code=qr_code)
        complete_qr['comentarios'] = [{"msg":"Comentario 1"}, {"msg":"Comentario 2"}]
        loction = 'Nombre de la ubicacion'
        area = 'Nombre de la area'
        complete_qr['accesos'] = [
            {"nombre":"Cuarto de Maquinas", "location":location, "area":area, "status":"Permitido"},
            {"nombre":"Piso 1", "location":location, "area":area, "status":"Permitido"},
            {"nombre":"Piso 2", "location":location, "area":area, "status":"Permitido"},
            {"nombre":"Piso 15-35", "location":location, "area":area, "status":"Permitido"},
            ]
        complete_qr['certificaiones'] = [
            {"nombre":"Examen de Alturas","status":"Aprovado", "expiracion":"2024-09-15"}, 
            {"nombre":"Licencia de Manejar","status":"Expirado", "expiracion":"2023-09-15"}, 
            ]
        complete_qr['ultimo_acceso'] = [
            {"nombre_visita":"Juan Rulfo","location":location,"fecha":"2024-09-15T15:05", "duration": 5683}, 
            {"nombre_visita":"Gabriel Garcia Marquez","location":location,"fecha":"2024-09-15T21:33", "duration": 600 }, 
            ]
        complete_qr['equipo'] = [
            {"tipo":"Computadora", "marca":"Lenovo","modelo":"T42S", "serie": "u4568", "color":"Negra"}, 
            {"tipo":"Herramienta", "marca":"Truper","modelo":"Pinza", "serie": "N/A", "color":"Naranja"}, 
            ]
        complete_qr['vehiculos'] = [
            {"tipo":"Camion", "marca":"Volvo","modelo":"Modelo T", "placa": "TZ-58996-S", "color":"Azul"}, 
            {"tipo":"Auto", "marca":"Ford","modelo":"Fiesta", "placa": "ZF-M4M0N", "color":"Blanco"}, 
            ]

        print('aqui voy tnego q buscar el q r code....')
        print('si me das pura location y area', )


        return complete_qr

    def get_shift_data(self, search_default=True):
        """
        Obtiene informacion del turno del usuario logeado
        """
        load_shift_json = { }
        username = self.user.get('username')
        user_id = self.user.get('user_id')
        default_booth , user_booths = self.get_user_booth(search_default=False)
        location = default_booth.get('location')
        if not default_booth:
            return self.LKFException({"status_code":400, "msg":'No booth found or configure for user'})
        booth_area = default_booth['area']
        booth_location = default_booth['location']
        booth_addres = self.get_area_address(booth_location, booth_area)
        guards_positions = self.config_get_guards_positions()
        location_employees = {}
        for guard_type in guards_positions:
            puesto = guard_type['tipo_de_guardia']
            location_employees[puesto] = location_employees.get(puesto,
                self.get_users_by_location_area(booth_location, booth_area, **{'position': guard_type['puestos']})
                )
            if guard_type['tipo_de_guardia'] == 'guardia_de_apoyo':
                support_positions = guard_type['puestos']
        guard = self.get_user_guards(location_employees['guardia'])
        notes = self.get_access_notes(booth_location, booth_area)
        load_shift_json["location"] = {
            "name":  booth_location,
            "area": booth_area,
            "city": booth_addres.get('city'),
            "state": booth_addres.get('state'),
            "address": booth_addres.get('address'),
            }
        load_shift_json["booth_stats"] = self.get_booth_stats( booth_area, location)
        load_shift_json["booth_status"] = self.get_booth_status(booth_area, location)
        load_shift_json["support_guards"] = location_employees['guardia_de_apoyo']
        load_shift_json["guard"] = self.update_guard_status(guard)
        load_shift_json["notes"] = notes
        load_shift_json["user_booths"] = user_booths
        return load_shift_json

    def validate_access_pass_location(self, qr_code):
        #TODO
        last_move = self.get_last_user_move(qr_code)
        print('last_move', last_move)
        if self.user_in_facility(last_move['status_visita']):
            return True
        return False

    def validate_certificados(self, qr_code, location):
        return True

    def validate_pass_dates(self, access_pass):
        return True
