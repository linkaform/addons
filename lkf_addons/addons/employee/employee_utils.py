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
import sys, simplejson

from linkaform_api import settings
from linkaform_api import base
from lkf_addons.addons.base.base_util import Base

### Objeto o Clase de Módulo ###
'''
Cada módulo puede tener múltiples objetos, configurados en clases.
Estos objetos deben heredar de `base.LKF_Base` y de cualquier módulo dependiente necesario.
Al utilizar `super()` en el método `__init__()`, heredamos las variables de configuración de la clase.

Además, se pueden heredar funciones de cualquier clase antecesora usando el método `super()`.
'''

class Employee(Base, base.LKF_Base):

    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False):
        # base.LKF_Base.__init__(self, settings, sys_argv=sys_argv)
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api)
        self.name =  __class__.__name__
        self.settings = settings

        #--Variables 
        ### Forms ###
        '''
        Use `self.FORM_NAME = self.lkm.form_id('form_name',id)` ---> Aquí deberás guardar los `ID` de los formularios. 
        Para ello deberás llamar el método `lkm.form_id` del objeto `lkm` (linkaform modules, por sus siglas).
        En `lkm` están todas las funciones generales de módulos.
        '''
        self.CONF_AREA_EMPLEADOS = self.lkm.form_id('configuracion_areas_y_empleados', 'id')
        self.CONF_DEPARTAMENTOS_PUESTOS = self.lkm.form_id('configuracion_de_departamentos_y_puestos', 'id')
        self.EMPLEADOS = self.lkm.form_id('empleados','id')

        #--Variables 
        ### Catálogos ###
        '''
        Use `self.CATALOG_NAME = self.lkm.catalog_id('catalog_name',id)` ---> Aquí deberás guardar los `ID` de los catálogos. 
        Para ello deberás llamar el método `lkm.catalog_id` del objeto `lkm`(linkaform modules, por sus siglas).
        En `lkm` están todas las funciones generales de módulos).
        '''
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

        self.EMPLEADOS_JEFES_DIRECTOS = self.lkm.catalog_id('empleados_jefes_directos')
        self.EMPLEADOS_JEFES_DIRECTOS_ID = self.EMPLEADOS_JEFES_DIRECTOS.get('id')
        self.EMPLEADOS_JEFES_DIRECTOS_OBJ_ID = self.EMPLEADOS_JEFES_DIRECTOS.get('obj_id')

        ## Module Fields ##
        ''' 
        self.mf : Estos son los campos que deseas mantener solo dentro de este modulo.
        Asegúrese de utilizar `llave` y el `id` del campo ej.
        'nombre_campo': "1f2h3j4j5d6f7h8j9j1a",
        '''
        self.employee_fields = {
            'worker_name':'62c5ff407febce07043024dd',
            'worker_department':'663bc4ed8a6b120eab4d7f1e',
            'worker_position':'663bc4c79b8046ce89e97cf4',
            'worker_name_b':'663bd36eb19b7fb7d9e97ccb',
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
            'cat_timezone':self.f['cat_timezone'],
        }

        ### Fields ###
        '''
        `self.f`: En esta variable "fields", se almacenan todos los campos de todos los módulos heredados.
        El orden de reemplazo se ve afectado por el orden en que se hereda cada módulo. El orden que se otorga, es considerando
        que la variable se iguala en la base, y se va armando en tren de dependencias ej.

            Class A:
            Class B(A):
            Class C(B):
            Class D(C):

            x_obj = D()
            el orden de herencia será, primero carga A > B > C > D.
        '''

        self.f.update(self.employee_fields)

    '''
    funciones internas: son funciones que solo se pueden mandar llamar dentro de este archivo. Si se hereda la clase
    esta función no puede ser invocada.

    pep-0008:
        _single_leading_underscore: 
        weak “internal use” indicator. E.g. from M import * does not import objects whose names start with an underscore.
    '''

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
            {'$project': self.proyect_format(self.employee_fields)},
            {'$sort':{'worker_name':1}},
            ]
        print('match_query', match_query)
        return self.format_cr_result(self.cr.aggregate(query), get_one=get_one)

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
        # print('query=', simplejson.dumps(query, indent=3))
        # print('area=', self.f['area'])
        res = self.cr.aggregate(query)
        caseta = None
        for x in res:
            caseta = x
            if caseta:
                break
        if not caseta and search_default:
            caseta = self.get_user_boot(search_default=False)
        return caseta

    def get_users_by_location_area(self, location_name=None, area_name=None, user_id=None, **kwargs):
        print('location_name', location_name)
        print('area_name', area_name)
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.CONF_AREA_EMPLEADOS,
            }
        if user_id:
            match_query.update({
                f"answers.{self.EMPLOYEE_OBJ_ID}.{self.f['user_id']}":user_id
                })
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
                    'employee': f"$answers.{self.EMPLOYEE_OBJ_ID}.{self.f['worker_name']}",
                    'user_id': {'$first':f"$answers.{self.EMPLOYEE_OBJ_ID}.{self.f['user_id']}"},
                    'marcada_como': f"$answers.{self.f['areas_group']}.{self.f['area_default']}"
                    }
                }
            ]
        print('query=', simplejson.dumps(query, indent=4))
        print('query=', self.cr)
        res = self.cr.aggregate(query)
        return [x for x in res]