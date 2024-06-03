# -*- coding: utf-8 -*-
import sys, simplejson

from linkaform_api import settings
from linkaform_api import base
#from lkf_addons.addons.base.base_util import Base


class Employee(base.LKF_Base):

    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False):
        # base.LKF_Base.__init__(self, settings, sys_argv=sys_argv)
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api)
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

        self.CONF_AREA_EMPLEADOS_CAT = self.lkm.catalog_id('configuracion_areas_y_empleados')
        self.CONF_AREA_EMPLEADOS_CAT_ID = self.CONF_AREA_EMPLEADOS_CAT.get('id')
        self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID = self.CONF_AREA_EMPLEADOS_CAT.get('obj_id')

        self.CONF_AREA_EMPLEADOS_AP_CAT = self.lkm.catalog_id('configuracion_areas_y_empleados_apoyo')
        self.CONF_AREA_EMPLEADOS_AP_CAT_ID = self.CONF_AREA_EMPLEADOS_AP_CAT.get('id')
        self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID = self.CONF_AREA_EMPLEADOS_AP_CAT.get('obj_id')

        self.employee_fields = {
            'worker_name':'62c5ff407febce07043024dd',
            'worker_name_apoyo':'663bd36eb19b7fb7d9e97ccb',
            'team_name':'62c5ff0162a70c261328845d',
            'areas_group':'663cf9d77500019d1359eb9f',
            'user_id':'663bd32d7fb8869bbc4d7f7b',
            'username': '6653f3709c6d89925dc04b2e',
            'email':'6653f3709c6d89925dc04b2f',
            'area_default':'6653f2d49c6d89925dc04b27',
            'picutre':'663bcbe2274189281359eb70',
            'rfc':'663bcbe2274189281359eb71',
            'curp':'663bcbe2274189281359eb72',
            'nss':'663bcbe2274189281359eb73',
            'fecha_nacimiento':'663bcbe2274189281359eb74',
            'genero':'663bcbe2274189281359eb75',
            'status_en_empresa':'663bcbe2274189281359eb77',
                }

        self.f.update(self.employee_fields)

    def _get_match_q(self, field_id, value):
        if type(value) == list:
            res  = {f"answers.{field_id}": {'$in':value}}
        else:
            res  = {f"answers.{field_id}": value}
        return res


    def get_employee_data(self, name=None, user_id=None, username=None, email=None):
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
            {'$project': self.proyect_format(self.employee_fields)},
            {'$sort':{'worker_name':1}},
            ]
        return self.format_cr_result(self.cr.aggregate(query))

    def get_user_boot(self, search_default=True, **kwargs):
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
                    'marcada_como': f"$answers.{self.f['areas_group']}.{self.f['area_default']}"
                    }
            }
            ]
        res = self.cr.aggregate(query)
        caseta = None
        for x in res:
            caseta = x
            if caseta:
                break
        if not caseta and search_default:
            caseta = self.get_user_boot(search_default=False)
        return caseta

    def get_users_by_location_area(self, location_name=None, area_name=None, **kwargs):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.CONF_AREA_EMPLEADOS,
            }

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
        if not unwind_query:
            mgs = "You musts specify either Location Name, Area Name or both"
            return self.LKFException(msg)
        query += [{'$match': unwind_query }]
        query += [
            {'$project':
                {'_id': 1,
                    'folio': "$folio",
                    'created_at': "$created_at",
                    'area': f"$answers.{self.f['areas_group']}.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['area']}",
                    'location': f"$answers.{self.f['areas_group']}.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['location']}",
                    'employee': f"$answers.{self.EMPLOYEE_OBJ_ID}.{self.f['worker_name']}",
                    'user_id': {'$first':f"$answers.{self.EMPLOYEE_OBJ_ID}.{self.f['user_id']}"},
                    'marcada_como': f"$answers.{self.f['areas_group']}.{self.f['area_default']}"
                    }
                }
            ]
        res = self.cr.aggregate(query)
        return [x for x in res]