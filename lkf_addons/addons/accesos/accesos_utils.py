# -*- coding: utf-8 -*-
import simplejson
from bson import ObjectId

from linkaform_api import base
from lkf_addons.addons.employee.employee_utils import Employee
from lkf_addons.addons.location.location_util import Location



class Accesos(Employee, Location, base.LKF_Base):

    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False):
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api)
        #--Variables Forms
        self.ACCESOS_NOTAS = self.lkm.form_id('notas','id')
        self.CHECKIN_CASETAS = self.lkm.form_id('checkin_checkout_casetas','id')
        self.last_check_in = []
        # self.FORM_ALTA_COLABORADORES = self.lkm.form_id('alta_de_colaboradores_visitantes','id')
        # self.FORM_ALTA_EQUIPOS = self.lkm.form_id('alta_de_equipos','id')
        # self.FORM_ALTA_VEHICULOS = self.lkm.form_id('alta_de_vehiculos','id')
        # #self.FORM_BITACORA = self.lkm.form_id('bitacora','id')
        # self.FORM_LOCKER = self.lkm.form_id('locker','id')
        #self.FORM_PASE_DE_ENTRADA = self.lkm.form_id('pase_de_entrada','id')
        #self.FORM_REGISTRO_PERMISOS = self.lkm.form_id('registro_de_permisos','id')

        # catalogos
        # self.AREAS_DE_LAS_UBICACIONES_CAT = self.lkm.catalog_id('areas_de_las_ubicaciones')
        # self.AREAS_DE_LAS_UBICACIONES_CAT_ID = self.AREAS_DE_LAS_UBICACIONES_CAT.get('id')
        # self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID = self.AREAS_DE_LAS_UBICACIONES_CAT.get('obj_id')
        #----Dic Fields Forms
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

        self.notes_project_fields = {
            'location': f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['location']}",
            'area': f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['area']}",
            'created_by': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_name']}",
            'closed_by': f"{self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID}.{self.f['worker_name_b']}",
            'support_guard':f"{self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID}.{self.f['worker_name_b']}",
        }

        self.notes_project_fields.update(self.notes_fields)
        
        self.f.update(self.notes_fields)
        self.f.update(self.checkin_fields)

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
        
    def is_boot_available(self, location, area):
        self.last_check_in = self.get_last_checkin(location, area)
        last_status = self.last_check_in.get('checkin_type')
        if last_status == 'entrada':
            return False
        else:
            return True

    def checkin_data(self, employee, location, area, checkin_type, timezone):
        if checkin_type == 'in':
            set_type = 'entrada'
        elif checkin_type == 'out':
            set_type = 'salida'
        checkin = {
            self.f['checkin_type']: set_type,
            self.f['checkin_date'] : self.today_str(employee.get('cat_timezone'), date_format='datetime'),
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

    def do_checkin(self, location, area, employee_list=[]):
        if not self.is_boot_available(location, area):
            msg = f"Can not login in to boot on location {location} at the area {area}."
            msg += f"Because '{self.last_check_in.get('employee')}' is logged in."
            # self.LKFException(msg)
        boot_config = self.get_users_by_location_area(location_name=location, area_name=area, user_id=self.user.get('user_id'))
        if not boot_config:
            msg = f"User can not login to this area : {area} at location: {location} ."
            msg += f"Please check your configuration."
            self.LKFException(msg)

        employee =  self.get_employee_data(email=self.user.get('email'), get_one=True)
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

