# -*- coding: utf-8 -*-
'''
Licencia BSD
Copyright (c) 2024 Infosync / LinkaForm.  
Todos los derechos reservados.

Se permite la redistribución y el uso en formas de código fuente y binario, con o sin modificaciones, siempre que se cumplan las siguientes condiciones:

1. Se debe conservar el aviso de copyright anterior, esta lista de condiciones y el siguiente descargo de responsabilidad en las redistribuciones del código fuente.
2. Se debe reproducir el aviso de copyright anterior, esta lista de condiciones y el siguiente descargo de responsabilidad en la documentación y/u otros materiales proporcionados con las distribuciones en formato binario.
3. Ni el nombre del Infosync ni los nombres de sus colaboradores pueden ser utilizados para respaldar o promocionar productos derivados de este software sin permiso específico previo por escrito.

'''

import sys, simplejson, re

from linkaform_api import settings
from lkf_addons.addons.base.app import Base


class Employee(Base):

    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False, **kwargs):
        # base.LKF_Base.__init__(self, settings, sys_argv=sys_argv)
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api, **kwargs)
        
        self.kwargs['MODULES'] = self.kwargs.get('MODULES',[])       
        if self.__class__.__name__ not in kwargs:
            self.kwargs['MODULES'].append(self.__class__.__name__)
        
        self.load('Location', **self.kwargs)

        self.name =  __class__.__name__
        self.settings = settings
        # forms
        self.CONF_AREA_EMPLEADOS = self.lkm.form_id('configuracion_areas_y_empleados', 'id')
        self.CONF_DEPARTAMENTOS_PUESTOS = self.lkm.form_id('configuracion_de_departamentos_y_puestos', 'id')
        self.EMPLEADOS = self.lkm.form_id('empleados','id')
        # catalgos
        self.EMPLOYEE = self.lkm.catalog_id('empleados')
        if not self.EMPLOYEE:
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

        self.CONF_DEPARTAMENTOS_PUESTOS_CAT = self.lkm.catalog_id('configuracion_de_departamentos_y_puestos')
        self.CONF_DEPARTAMENTOS_PUESTOS_CAT_ID = self.CONF_DEPARTAMENTOS_PUESTOS_CAT.get('id')
        self.CONF_DEPARTAMENTOS_PUESTOS_CAT_OBJ_ID = self.CONF_DEPARTAMENTOS_PUESTOS_CAT.get('obj_id')



        self.EMPLEADOS_JEFES_DIRECTOS = self.lkm.catalog_id('empleados_jefes_directos')
        self.EMPLEADOS_JEFES_DIRECTOS_ID = self.EMPLEADOS_JEFES_DIRECTOS.get('id')
        self.EMPLEADOS_JEFES_DIRECTOS_OBJ_ID = self.EMPLEADOS_JEFES_DIRECTOS.get('obj_id')

        self.employee_fields = {
            'address': '663a7e0fe48382c5b1230902',
            'area_default': '6653f2d49c6d89925dc04b27',
            'areas_group': '663cf9d77500019d1359eb9f',
            'cat_timezone': self.f['cat_timezone'],
            'city': '6654187fc85ce22aaf8bb070',
            'company': f"{self.COMPANY_OBJ_ID}.663a8153e48382c5b1230918",
            'curp': '663bcbe2274189281359eb72',
            'department_code': '670f571af57af9032464176e',
            'email': '6653f3709c6d89925dc04b2f',
            'estatus_dentro_empresa': '663bcbe2274189281359eb77',
            'estatus_disponibilidad': '663bcbe2274189281359eb78',
            'fecha_nacimiento': '663bcbe2274189281359eb74',
            'genero': '663bcbe2274189281359eb75',
            'genero_jefes': '663bd5c0b6e749213859eb6f',
            'nss': '663bcbe2274189281359eb73',
            'picture': '663bcbe2274189281359eb70',
            'picture_jefes': '663bd4f719b0aab097e97cde',
            'puesto': self.CONF_DEPARTAMENTOS_PUESTOS_CAT_OBJ_ID,
            'rfc': '663bcbe2274189281359eb71',
            'status_en_empresa': '663bcbe2274189281359eb77',
            'team_name': '62c5ff0162a70c261328845d',
            'telefono1': '663bd32d7fb8869bbc4d7f72',
            'telefono2': '663bd32d7fb8869bbc4d7f71',
            'user_id': '663bd32d7fb8869bbc4d7f7b',
            'user_id_b': '663bd466b19b7fb7d9e97cdc',
            'user_id_id': '638a9a99616398d2e392a9f5',
            'user_id_jefes': '663bd466b19b7fb7d9e97cdc',
            'username': '6653f3709c6d89925dc04b2e',
            'usuario': self.USUARIOS_OBJ_ID,
            'usuario_email': f"{self.USUARIOS_OBJ_ID}.638a9a7767c332f5d459fc82",
            'usuario_telefono': f"{self.USUARIOS_OBJ_ID}.67be0c43a31e5161c47f2bba",
            'usuario_id': f"{self.USUARIOS_OBJ_ID}.638a9a99616398d2e392a9f5",
            'worker_code': '670f585bf844ff7bc357b1dc',
            'worker_code_jefes': '671a8fbae68fe659567224b0',
            'worker_department': '663bc4ed8a6b120eab4d7f1e',
            'worker_name': '62c5ff407febce07043024dd',
            'worker_name_b': '663bd36eb19b7fb7d9e97ccb',
            'worker_name_jefes': '663bd36eb19b7fb7d9e97ccb',
            'worker_position': '663bc4c79b8046ce89e97cf4',
            'worker_position_code': '670f57c281ad62446e641602',
                }

        f = {
            'area':'663e5d44f5b8a7ce8211ed0f',
            'areas_grupo': '663cf9d77500019d1359eb9f',
            'departamento_empleado': '663bc4ed8a6b120eab4d7f1e',
            'grupo_puestos': '663c015f3ac46d98e8f27495',
            'location': '663e5c57f5b8a7ce8211ed0b',
            'nombre_area': '663e5d44f5b8a7ce8211ed0f',
            'nombre_area_salida': '663fb45992f2c5afcfe97ca8',
            'nombre_empleado': '62c5ff407febce07043024dd',
            'nombre_guardia_apoyo': '663bd36eb19b7fb7d9e97ccb',
            'puesto_empleado': '663bc4c79b8046ce89e97cf4',
            'ubicacion': '663e5c57f5b8a7ce8211ed0b',
        }
        if hasattr(self, 'f'):
            self.f.update(f)
        else:
            print('vaa  A IGUALSAR')
            self.f = f

        self.f.update(self.employee_fields)

    def _get_match_q(self, field_id, value):
        if type(value) == list:
            res  = {f"answers.{field_id}": {'$in':value}}
        else:
            res  = {f"answers.{field_id}": value}
        return res

    def get_employee_data(self, name=None, user_id=None, username=None, email=None, phone=None, get_one=False):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.EMPLEADOS,
            }
        if name:
            match_query.update(self._get_match_q(self.f['worker_name'], name))
        if user_id:
            match_query.update(self._get_match_q(f"{self.USUARIOS_OBJ_ID}.{self.employee_fields['user_id_id']}", user_id))
        if username:
            match_query.update(self._get_match_q(self.f['username'], username))
        if email:
            match_query.update(self._get_match_q(self.employee_fields['usuario_email'], email))
        if phone:
            phone = re.sub(r'\D', '', phone)
            phone = phone[-10:]
            match_query.update(
                {
                "$or": [
                    {f"answers.{self.employee_fields['telefono1']}": {"$regex": phone}},
                    {f"answers.{self.employee_fields['telefono2']}": {"$regex": phone}},
                    {f"answers.{self.employee_fields['usuario_telefono']}": {"$regex": phone}},
                    ]
                }
                )
        query = [
            {'$match': match_query },    
            {'$project': self.project_format(self.employee_fields)},
            {'$sort':{'worker_name':1}},
            ]
        res = self.format_cr_result(self.cr.aggregate(query), get_one=get_one)
        return res 

    def get_user_booth(self, search_default=True, turn_areas=True, **kwargs):
        if kwargs.get('user_id'):
            user_id = kwargs['user_id']
        else:
            user_id = self.user.get('user_id')
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.CONF_AREA_EMPLEADOS,
            f"answers.{self.EMPLOYEE_OBJ_ID}.{self.employee_fields['user_id_id']}":user_id
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
                    'area': f"$answers.{self.f['areas_group']}.{self.Location.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['area']}",
                    'location': f"$answers.{self.f['areas_group']}.{self.Location.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['location']}",
                    'employee': f"$answers.{self.EMPLOYEE_OBJ_ID}.{self.f['worker_name']}",
                    'marcada_como': f"$answers.{self.f['areas_group']}.{self.f['area_default']}",
                    }
            }
            ]
        res = self.format_cr(self.cr.aggregate(query))
        caseta = None
        user_booths = []
        for x in res:
            if not x.get('area') and not turn_areas:
                selector = {}
                selector.update({f"answers.{self.f['ubicacion']}": x.get('location')})

                if not selector:
                    selector = {"_id": {"$gt": None}}

                fields = ["_id", f"answers.{self.f['nombre_area']}"]

                mango_query = {
                    "selector": selector,
                    "fields": fields,
                    "limit": 1000
                }

                row_catalog = self.lkf_api.search_catalog(self.Location.AREAS_DE_LAS_UBICACIONES_CAT_ID, mango_query)
                if row_catalog:
                    for r in row_catalog:
                        res.append({
                            'area': r.get(self.f['nombre_area']),
                            'location': x.get('location'),
                            'employee': x.get('employee'),
                            'marcada_como': 'normal',
                        })
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
        match_query.update(self._get_match_q(f"{self.USUARIOS_OBJ_ID}.{self.employee_fields['user_id_id']}", user_id))
        query = [
            {'$match': match_query },    
            {'$project':{ 
                        '_id':1,
                        'user_id':f"$answers.{self.USUARIOS_OBJ_ID}.{self.employee_fields['user_id_id']}",
                        'pic_url':{"$first":f"$answers.{self.employee_fields['picture']}"}
                        }
            }
            ]
        users = self.format_cr_result(self.cr.aggregate(query))
        res = {}
        for usr in users:
            if type(usr['user_id']) == list:
                usr['user_id'] = usr['user_id'][0]
            res[usr['user_id']] = usr.get('pic_url',usr.get('file_url',{}))
        return res

    def get_users_by_location_area(self, location_name=None, area_name=None, user_id=None, **kwargs):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.CONF_AREA_EMPLEADOS,
            }
        if user_id:
            field_id = f"{self.EMPLOYEE_OBJ_ID}.{self.employee_fields['user_id_id']}"
            match_query.update(self._get_match_q(field_id, user_id))
        unwind = {'$unwind': f"$answers.{self.f['areas_group']}"}
        query= [
            {'$match': match_query },
            unwind,
            ]
        unwind_query = {}
        if location_name:
            if type(location_name) == str:
                unwind_query.update({
                    f"answers.{self.f['areas_group']}.{self.Location.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['location']}": location_name
                    })
            elif type(location_name) == list:
                unwind_query.update({
                    f"answers.{self.f['areas_group']}.{self.Location.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['location']}": {"$in": location_name}
                    })
        if area_name:
            unwind_query.update({
                f"answers.{self.f['areas_group']}.{self.Location.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['area']}": area_name
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
                    'area': f"$answers.{self.f['areas_group']}.{self.Location.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['area']}",
                    'location': f"$answers.{self.f['areas_group']}.{self.Location.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['location']}",
                    'name': f"$answers.{self.EMPLOYEE_OBJ_ID}.{self.f['worker_name']}",
                    'user_id': {'$first':f"$answers.{self.EMPLOYEE_OBJ_ID}.{self.employee_fields['user_id_id']}"},
                    'marcada_como': f"$answers.{self.f['areas_group']}.{self.f['area_default']}",
                    'position': {"$first":f"$answers.{self.EMPLOYEE_OBJ_ID}.{self.f['worker_position']}"},
                    }
                }
            ]
        return self.format_cr_result(self.cr.aggregate(query))
