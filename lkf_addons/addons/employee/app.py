# -*- coding: utf-8 -*-
import sys, simplejson

from linkaform_api import settings
from linkaform_api import base
from lkf_addons.addons.base.app import Base


class Employee(Base, base.LKF_Base):

    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False, **kwargs):
        # base.LKF_Base.__init__(self, settings, sys_argv=sys_argv)
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api, **kwargs)
        self.name =  __class__.__name__
        self.settings = settings
        # forms
        self.CONF_AREA_EMPLEADOS = self.lkm.form_id('configuracion_areas_y_empleados', 'id')
        self.CONF_DEPARTAMENTOS_PUESTOS = self.lkm.form_id('configuracion_de_departamentos_y_puestos', 'id')
        self.EMPLEADOS = self.lkm.form_id('empleados','id')
        # catalgos
        self.EMPLOYEE = self.lkm.catalog_id('employee')
        self.EMPLOYEE_ID = self.EMPLOYEE.get('id')
        self.EMPLOYEE_OBJ_ID = self.EMPLOYEE.get('obj_id')

        self.TEAM = self.lkm.catalog_id('teams')
        self.TEAM_ID = self.TEAM.get('id')
        self.TEAM_OBJ_ID = self.TEAM.get('obj_id')

        self.PUESTOS = self.lkm.catalog_id('puestos')
        self.PUESTOS_ID = self.PUESTOS.get('id')
        self.PUESTOS_OBJ_ID = self.PUESTOS.get('obj_id')

        self.DEPARTAMENTOS = self.lkm.catalog_id('departamentos')
        self.DEPARTAMENTOS_ID = self.DEPARTAMENTOS.get('id')
        self.DEPARTAMENTOS_OBJ_ID = self.DEPARTAMENTOS.get('obj_id')

        self.CONF_AREA_EMPLEADOS_CAT = self.lkm.catalog_id('configuracion_areas_y_empleados')
        self.CONF_AREA_EMPLEADOS_CAT_ID = self.CONF_AREA_EMPLEADOS_CAT.get('id')
        self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID = self.CONF_AREA_EMPLEADOS_CAT.get('obj_id')

        self.CONF_AREA_EMPLEADOS_AP_CAT = self.lkm.catalog_id('configuracion_areas_y_empleados_apoyo')
        self.CONF_AREA_EMPLEADOS_AP_CAT_ID = self.CONF_AREA_EMPLEADOS_AP_CAT.get('id')
        self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID = self.CONF_AREA_EMPLEADOS_AP_CAT.get('obj_id')

        self.EMPLEADOS_JEFES_DIRECTOS = self.lkm.catalog_id('empleados_jefes_directos')
        self.EMPLEADOS_JEFES_DIRECTOS_ID = self.EMPLEADOS_JEFES_DIRECTOS.get('id')
        self.EMPLEADOS_JEFES_DIRECTOS_OBJ_ID = self.EMPLEADOS_JEFES_DIRECTOS.get('obj_id')

        self.employee_fields = {
            'city':'6654187fc85ce22aaf8bb070',
            'address':'663a7e0fe48382c5b1230902',
            'areas_group':'663cf9d77500019d1359eb9f',
            'estatus_dentro_empresa':'663bcbe2274189281359eb77',
            'estatus_disponibilidad':'663bcbe2274189281359eb78',
            'cat_timezone':self.f['cat_timezone'],
            'user_id':'663bd32d7fb8869bbc4d7f7b',
            'user_id_jefes':'663bd466b19b7fb7d9e97cdc',
            'user_id_b':'663bd466b19b7fb7d9e97cdc',
            'username': '6653f3709c6d89925dc04b2e',
            'email':'6653f3709c6d89925dc04b2f',
            'area_default':'6653f2d49c6d89925dc04b27',
            'picture':'663bcbe2274189281359eb70',
            'rfc':'663bcbe2274189281359eb71',
            'curp':'663bcbe2274189281359eb72',
            'nss':'663bcbe2274189281359eb73',
            'fecha_nacimiento':'663bcbe2274189281359eb74',
            'genero':'663bcbe2274189281359eb75',
            'status_en_empresa':'663bcbe2274189281359eb77',
            'team_name':'62c5ff0162a70c261328845d',
            'telefono1':'66c3c17ece46780a6953aa29',
            'worker_name':'62c5ff407febce07043024dd',
            'worker_name_jefes':'663bd36eb19b7fb7d9e97ccb',
            'worker_department':'663bc4ed8a6b120eab4d7f1e',
            'worker_position':'663bc4c79b8046ce89e97cf4',
            'worker_name_b':'663bd36eb19b7fb7d9e97ccb',
                }

        self.f.update(self.employee_fields)

    def _get_match_q(self, field_id, value):
        if type(value) == list:
            res  = {f"answers.{field_id}": {'$in':value}}
        else:
            res  = {f"answers.{field_id}": value}
        return res

    def get_employee_data(self, name=None, user_id=None, username=None, email=None,  get_one=False):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.EMPLEADOS,
            }
        if name:
            match_query.update(self._get_match_q(self.f['worker_name'], name))
        if user_id:
            match_query.update(self._get_match_q(self.f['user_id'], user_id))
        if username:
            match_query.update(self._get_match_q(self.f['username'], username))
        if email:
            match_query.update(self._get_match_q(self.f['email'], email))            
        query = [
            {'$match': match_query },    
            {'$project': self.project_format(self.employee_fields)},
            {'$sort':{'worker_name':1}},
            ]
        return self.format_cr_result(self.cr.aggregate(query), get_one=get_one)

    def get_user_booth(self, search_default=True, **kwargs):
        if kwargs.get('user_id'):
            user_id = kwargs['user_id']
        else:
            user_id = self.user.get('user_id')
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.CONF_AREA_EMPLEADOS,
            f"answers.{self.EMPLOYEE_OBJ_ID}.{self.f['user_id']}":user_id
            }

        unwind = {'$unwind': f"$answers.{self.f['areas_group']}"}
        query= [
            {'$match': match_query },
            unwind,
            ]
        if search_default:
            query += [{'$match': {f"answers.{self.f['areas_group']}.{self.f['area_default']}":'default' }}]
        query += [
            {'$project':
                {'_id': 1,
                    'folio': "$folio",
                    'created_at': "$created_at",
                    'area': f"$answers.{self.f['areas_group']}.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['area']}",
                    'location': f"$answers.{self.f['areas_group']}.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['location']}",
                    'employee': f"$answers.{self.EMPLOYEE_OBJ_ID}.{self.f['worker_name']}",
                    'marcada_como': f"$answers.{self.f['areas_group']}.{self.f['area_default']}",
                    }
            }
            ]
        # print('query=', simplejson.dumps(query, indent=3))
        # print('area=', self.f['area'])
        res = self.format_cr(self.cr.aggregate(query))
        caseta = None
        user_booths = []
        for x in res:
            if x['marcada_como'] == 'default' and not caseta:
                caseta = x
            else:
                user_booths.append(x)
        if not caseta and search_default:
            caseta, user_booths_tmp = self.get_user_booth(search_default=False)
        if not search_default and not caseta:
            if user_booths:
                caseta = user_booths[0]
        if not caseta:
            msg = f'No existe caseta configurada para usuario id: {user_id}'
            self.LKFException(msg)
        return caseta, user_booths

    def get_employee_pic(self, user_id):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.EMPLEADOS,
            }
        match_query.update(self._get_match_q(self.f['user_id'], user_id))
        query = [
            {'$match': match_query },    
            {'$project':{ 
                        '_id':1,
                        'user_id':f"$answers.{self.employee_fields['user_id']}",
                        'pic_url':{"$first":f"$answers.{self.employee_fields['picture']}"}
                        }
            }
            ]
        users = self.format_cr_result(self.cr.aggregate(query))
        res = {}
        for usr in users:
            res[usr['user_id']] = usr.get('pic_url',usr.get('file_url',{}))
        return res

    def get_users_by_location_area(self, location_name=None, area_name=None, user_id=None, **kwargs):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.CONF_AREA_EMPLEADOS,
            }
        if user_id:
            field_id = f"{self.EMPLOYEE_OBJ_ID}.{self.f['user_id']}"
            match_query.update(self._get_match_q(field_id, user_id))
        unwind = {'$unwind': f"$answers.{self.f['areas_group']}"}
        query= [
            {'$match': match_query },
            unwind,
            ]
        unwind_query = {}
        if location_name:
            unwind_query.update({
                f"answers.{self.f['areas_group']}.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['location']}": location_name
                })
        if area_name:
            unwind_query.update({
                f"answers.{self.f['areas_group']}.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['area']}": area_name
                })
        if kwargs.get('position'):
            positions = kwargs.get('position')
            match_query.update({
                f"answers.{self.EMPLOYEE_OBJ_ID}.{self.f['worker_position']}":{"$in":positions}
                })
            #TODO BUSCAR SOLO LOS DE ESTE PUESTO
        if not unwind_query:
            msg = "You musts specify either Location Name, Area Name or both"
            return self.LKFException(msg)
        query += [{'$match': unwind_query }]
        query += [
            {'$project':
                {'_id': 1,
                    'folio': "$folio",
                    'created_at': "$created_at",
                    'area': f"$answers.{self.f['areas_group']}.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['area']}",
                    'location': f"$answers.{self.f['areas_group']}.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['location']}",
                    'name': f"$answers.{self.EMPLOYEE_OBJ_ID}.{self.f['worker_name']}",
                    'user_id': {'$first':f"$answers.{self.EMPLOYEE_OBJ_ID}.{self.f['user_id']}"},
                    'marcada_como': f"$answers.{self.f['areas_group']}.{self.f['area_default']}",
                    'position': {"$first":f"$answers.{self.EMPLOYEE_OBJ_ID}.{self.f['worker_position']}"},
                    }
                }
            ]
        # print('query=', simplejson.dumps(query, indent=3))
        return self.format_cr_result(self.cr.aggregate(query))
