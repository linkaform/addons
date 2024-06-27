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
            'grupo_visitados': "663d4ba61b14fab90559ebb0",
            'tipo_visita_pase': "662c304fad7432d296d92581",
            'fecha_desde_visita': "662c304fad7432d296d92582",
            'fecha_hasta_visita': "662c304fad7432d296d92583",
            'config_dia_de_acceso': "662c304fad7432d296d92584",
            'config_limitar_acceso': "6635380dc9b3e7db4d59eb49",
            'config_dias_acceso': "662c304fad7432d296d92585",
        }
        self.mf =mf
        ## Form Fields ##
        '''
        self.form_name : En esta seccion podras agrupar todos los campos ya sea por forma o como dease
        enviarls hacia tus servicios, en el caso de las busquedas de mongo, pudes hacer las busquedas de
        Manera Anidada Por lo cual podras agrupar separadas por punto, ej.663d4ba61b14fab90559ebb0.665f482cc9a2f8acf685c20b
        y asi podras hacer la busquedas directo en la base de datos.

        Estos campos podras agregarlos asi directo a self.f , donde se agurpan todos los fields de los modulos heredados

        '''

        self.notes_fields = {
            'note_status':'6647f9eb6eefdb1840684dc1',
            'note_open_date':'6647fadc96f80017ac388646',
            'note_close_date':'6647fadc96f80017ac38864a',
            'note':'6647fadc96f80017ac388647',
            'note_file':'6647fadc96f80017ac388648',
            'note_pic':'6647fadc96f80017ac388649',
            'note_pic':'6647fadc96f80017ac388649',
            'note_comments_group':'6647fb1874c1a87eb02a9037',
            'note_comments':'6647fb38da07bf430e273ea2',
        }
        self.checkin_fields = {
            'checkin_type': '663bffc28d00553254f274e0',
            'checkin_date':'663bffc28d00553254f274e1',
            'checkout_date':'663bffc28d00553254f274e2',
            'guard_group':'663fae53fa005c70de59eb95',
            'employee_position':'665f482cc9a2f8acf685c20b',
            'cat_created_by': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_name']}",
            'created_by': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_name']}",
            'employee': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_name']}",
            'cat_location': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['location']}",
            'cat_area': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['area']}",
            'cat_employee_b': f"{self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID}.{self.f['worker_name_b']}",
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
            'nombre_visita': f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.5ea0693a0c12d5a8e43d37df",
            'email_vsita': f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.5ea069562f8250acf7d83aca",
            'curp': f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.5ea0897550b8dfe1f4d83a9f",
            'telefono': f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.661ea59c15baf5666f32360e",
            'foto': f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.5ea35de83ab7dad56c66e045",
            'identificacion': f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.65ce34985fa9df3dbf9dd2d0",
            'empresa': f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.64ecc95271803179d68ee081",
            'status_visita': f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.5ea1bd280ae8bad095055e61",
            # 'nombre_perfil': f"{self.PERFIL_ENTRADA_OBJ_ID}.661dc67e901906b7e9b73bac",
            'grupo_visitados': self.mf['grupo_visitados'],
            'nombre_perfil': f"{self.mf['grupo_visitados']}{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_name']}",
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
        self.notes_project_fields = {
            'location': f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['location']}",
            'area': f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['area']}",
            'created_by': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_name']}",
            'closed_by': f"{self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID}.{self.f['worker_name_b']}",
            'support_guard':f"{self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID}.{self.f['worker_name_b']}",
        }

        self.notes_project_fields.update(self.notes_fields)
        
        
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
    def _do_access(self, access_pass):
        '''
        Registra el acceso del pase de entra a ubicacion
        solo puede ser ejecutado despues de revisar los accesos
        '''
        print('creating reacord')
        print('creating reacord', access_pass)
        self.lkf_api.get_metadata(form_id=self.BITACORA_ACCESOS)



    def do_access(self, qr_code, location, area):
        '''
        Valida pase de entrada y crea registro de entrada al pase
        '''
        print('me quede ahceidno la vaildacion y el registro de entrada')
        print('falta agregar a la forma, con que vehiuclo y equipos entra')
        if not qr_code and not location and not area:
            return False
        access_pass = self.search_pass(qr_code)
        val_location = self.validate_access_pass_location(access_pass)
        val_certificados = self.validate_certificados(qr_code, location)
        pass_dates = self.validate_pass_dates(access_pass)
        res = self._do_access(access_pass)

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
        checkin = self.set_checkout_employees(checkin=checkin, employee_list=employee_list, replace=True)
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
        checkin = self.set_checkout_employees(checkin=checkin, employee_list=guards, replace=False)
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

    def get_access_pass(self, qr_code):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.CHECKIN_CASETAS,
            }
        if _id:
            match_query.update({"_id":ObjectId(_id)})

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

    def is_boot_available(self, location, area):
        self.last_check_in = self.get_last_checkin(location, area)
        print('last_check_in', self.last_check_in)
        last_status = self.last_check_in.get('checkin_type')
        if last_status == 'entrada':
            return False
        else:
            return True

    def set_checkout_employees(self, checkin={}, employee_list=[], replace=True):
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
        qr_code = '66563787d2f0b4fb84768be5'
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

    def validate_access_pass_location(self, access_pass, location, ):
        if access_pass:
            return True
        else:
            return False

    def validate_certificados(self, qr_code, location):
        return True

    def validate_pass_dates(self, access_pass):
        return True
