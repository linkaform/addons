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

from linkaform_api import base
from lkf_addons.addons.base.app import Base


class Location(Base):

    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False, **kwargs):
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api)

        self.kwargs['MODULES'] = self.kwargs.get('MODULES',[])       
        if self.__class__.__name__ not in kwargs:
            self.kwargs['MODULES'].append(self.__class__.__name__)

        #use self.lkm.catalog_id() to get catalog id
        # forms
        self.AREAS_DE_LAS_UBICACIONES = self.lkm.form_id('areas_de_las_ubicaciones', 'id')
        self.UBICACIONES = self.lkm.form_id('ubicaciones', 'id')
        # catalgos
        self.UBICACIONES_CAT = self.lkm.catalog_id('ubicaciones')
        self.UBICACIONES_CAT_ID = self.UBICACIONES_CAT.get('id')
        self.UBICACIONES_CAT_OBJ_ID = self.UBICACIONES_CAT.get('obj_id')

        self.AREAS_DE_LAS_UBICACIONES_CAT = self.lkm.catalog_id('areas_de_las_ubicaciones')
        self.AREAS_DE_LAS_UBICACIONES_CAT_ID = self.AREAS_DE_LAS_UBICACIONES_CAT.get('id')
        self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID = self.AREAS_DE_LAS_UBICACIONES_CAT.get('obj_id')

        self.AREAS_DE_LAS_UBICACIONES_SALIDA = self.lkm.catalog_id('areas_de_las_ubicaciones_salidas')
        self.AREAS_DE_LAS_UBICACIONES_SALIDA_ID = self.AREAS_DE_LAS_UBICACIONES_SALIDA.get('id')
        self.AREAS_DE_LAS_UBICACIONES_SALIDA_OBJ_ID = self.AREAS_DE_LAS_UBICACIONES_SALIDA.get('obj_id')

        self.TIPO_AREA = self.lkm.catalog_id('tipo_de_areas')
        self.TIPO_AREA_ID = self.TIPO_AREA.get('id')
        self.TIPO_AREA_OBJ_ID = self.TIPO_AREA.get('obj_id')

        self.f.update( {
            'location':'663e5c57f5b8a7ce8211ed0b',
            'location_id':'68101945f4996c72247baac4',
            'area':'663e5d44f5b8a7ce8211ed0f',
            'area_state':'663e5e4bf5b8a7ce8211ed14',
            'area_status':'663e5e4bf5b8a7ce8211ed15',
            'area_qr_code':'663e5e4bf5b8a7ce8211ed13',
            'new_city': '6654187fc85ce22aaf8bb070'
        }
        )

    def get_location_address(self, location_name):
        location_address = {}
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.UBICACIONES,
            f"answers.{self.f['location']}":location_name
            }
        query = [
            {'$match': match_query },
            {'$project':
                {'_id': 1,
                    'folio': "$folio",
                    'location': f"$answers.{self.f['location']}",
                    'address_name': f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['address_name']}",
                    'address': {'$first':f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['address']}"},
                    'address2': {'$first':f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['address2']}"},
                    'address_type': {'$first':f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['address_type']}"},
                    'address_geolocation': {'$first':f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['address_geolocation']}"},
                    'state': {'$first':f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['state']}"},
                    'city': {'$first':f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['city']}"},
                    'zip_code': {'$first':f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['zip_code']}"},
                    'country': {'$first':f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['country']}"},
                    'phone': {'$first':f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['phone']}"},
                    'email': {'$first':f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['email']}"},
                    }
            }
            ]
        res = self.cr.aggregate(query)
        for x in res:
            location_address = x
        return location_address

    def get_area_address(self, location_name, area_name):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.AREAS_DE_LAS_UBICACIONES,
            f"answers.{self.UBICACIONES_CAT_OBJ_ID}.{self.f['location']}":location_name,
            f"answers.{self.f['area']}":area_name
            }
        query = [
            {'$match': match_query },
            {'$project':
                {'_id': 1,
                    'folio': "$folio",
                    'area': f"$answers.{self.f['area']}",
                    'location': f"$answers.{self.UBICACIONES_CAT_OBJ_ID}.{self.f['location']}",
                    'address_name': f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['address_name']}",
                    'address': {'$cond': [
                        {'$isArray': f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['address']}"},
                        {'$first':  f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['address']}"},
                        f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['address']}"
                    ]},
                    'address2': {'$cond': [
                        {'$isArray': f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['address2']}"},
                        {'$first':  f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['address2']}"},
                        f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['address2']}"
                    ]},
                    'address_type': {'$cond': [
                        {'$isArray': f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['address_type']}"},
                        {'$first':  f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['address_type']}"},
                        f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['address_type']}"
                    ]},
                    'address_geolocation': {'$cond': [
                        {'$isArray': f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['address_geolocation']}"},
                        {'$first':  f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['address_geolocation']}"},
                        f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['address_geolocation']}"
                    ]},
                    'state': {'$cond': [
                        {'$isArray': f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['state']}"},
                        {'$first':  f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['state']}"},
                        f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['state']}"
                    ]},
                    'city': {'$cond': [
                        {'$isArray': f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['new_city']}"},
                        {'$first':  f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['new_city']}"},
                        f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['new_city']}"
                    ]},
                    'zip_code': {'$cond': [
                        {'$isArray': f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['zip_code']}"},
                        {'$first':  f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['zip_code']}"},
                        f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['zip_code']}"
                    ]},
                    'country': {'$cond': [
                        {'$isArray': f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['country']}"},
                        {'$first':  f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['country']}"},
                        f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['country']}"
                    ]},
                    'phone': {'$cond': [
                        {'$isArray': f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['phone']}"},
                        {'$first':  f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['phone']}"},
                        f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['phone']}"
                    ]},
                    'email': {'$cond': [
                        {'$isArray': f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['email']}"},
                        {'$first':  f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['email']}"},
                        f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['email']}"
                    ]},
                }
            }
            ]
        import simplejson
        # print('query=', simplejson.dumps(query, indent=4))
        res = self.cr.aggregate(query)
        area_address = {}
        for x in res:
            area_address = x
        if not area_address:
            area_address = self.get_location_address(location_name)
        return area_address
        
    def get_areas_by_location(self, location_name):
        options={}
        if location_name:
            options = {
                'startkey': [location_name],
                'endkey': [f"{location_name}\n",{}],
                'group_level':2
            }
        catalog_id = self.AREAS_DE_LAS_UBICACIONES_CAT_ID
        form_id = self.PASE_ENTRADA
        return self.catalogo_view(catalog_id, form_id, options)

    def get_areas_by_location_salidas(self, location_name):
        options={}
        catalog_id = self.AREAS_DE_LAS_UBICACIONES_SALIDA_ID
        form_id = self.PASE_ENTRADA
        group_level = options.get('group_level',1)
        return self.catalogo_view(catalog_id, form_id, options=options)

    def get_area_status(self, location, area, state='activa'):
        if not isinstance(location, list):
            location = [location]
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.AREAS_DE_LAS_UBICACIONES,
            f"answers.{self.UBICACIONES_CAT_OBJ_ID}.{self.f['location']}": {"$in": location},
            f"answers.{self.f['area']}":area,
            f"answers.{self.f['area_state']}":state,
        }
        response = self.format_cr(self.cr.find(match_query, {f"answers.{self.f['area_status']}":1}), get_one=True)
        res = response.get('area_status', 'No Configurada')
        return res.title()


    def get_area_record_by_name(self, name, select_cols=[], get_one=True):
        """ Busca area por nombre y regresa registros que cumplan con el nombre. 
        Si se le solicita select_cols, solo regresa las columnas solicitadas
        Args:
            name: Nombre del area
            select_cols (opcional): lista de nombres o id de los campos deseados
            get_one (ocpional): La funcion regresa 1 dato al menos que se indique false
        Returns:
            record id directo del cr de la base de datos
        """        
        select_c = {}
        if select_cols:
            for c in select_cols:
                try:
                    ObjectId(c)
                    is_field_id = True
                except:
                    is_field_id = False
                r = f'answers.{c}' if is_field_id else c
                select_c[r] = 1
        name_id = self.f['area']
        if select_c:
            cr_res = self.cr.find({
                        'deleted_at': {'$exists': False},
                        'form_id': self.AREAS_DE_LAS_UBICACIONES,
                        f'answers.{name_id}':name
                        }, select_c)
        else:
            cr_res = self.cr.find({
                        'deleted_at': {'$exists': False},
                        'form_id': self.AREAS_DE_LAS_UBICACIONES,
                        f'answers.{name_id}':name
                        })
        return self.format_cr(cr_res, get_one=get_one)

    def update_status_habitacion(self, name, status):
        """ Esta funcion actualiza el status de una areas segun su nombre
        Args:
            name: nombre del area 
            status: nuevo status
        Returns:
            El resultado directo del patch
        """
        status_id = self.f['area_state']
        answers = {self.f['area_state']:status}
        record_id = self.get_area_record_by_name(name, ['folio']).get('_id')
        return self.lkf_api.patch_multi_record( answers = answers, form_id=self.AREAS_DE_LAS_UBICACIONES, record_id=[record_id])
