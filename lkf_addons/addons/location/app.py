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

from bson import ObjectId

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
            'area':'663e5d44f5b8a7ce8211ed0f',
            'area_salida':'663fb45992f2c5afcfe97ca8',
            'area_qr_code':'663e5e4bf5b8a7ce8211ed13',
            'area_state':'663e5e4bf5b8a7ce8211ed14',
            'area_status':'663e5e4bf5b8a7ce8211ed15',
            'location':'663e5c57f5b8a7ce8211ed0b',
            'location_id':'68101945f4996c72247baac4',
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
        # print('query=', simplejson.dumps(query, indent=4))
        res = self.cr.aggregate(query)
        area_address = {}
        for x in res:
            area_address = x
        if not area_address:
            area_address = self.get_location_address(location_name)
        return area_address
        
    def get_areas_by_location(self, location_name):
        """
        Obtiene todas las areas de una ubicacion
        return:
        lista de areas
        """
        match_query = {
            "deleted_at": {"$exists": False},
            "form_id": self.AREAS_DE_LAS_UBICACIONES,
        }
        if type(location_name) == str:
            match_query[f"answers.{self.UBICACIONES_CAT_OBJ_ID}.{self.f['location']}"] = location_name
        elif type(location_name) == list:
            match_query[f"answers.{self.UBICACIONES_CAT_OBJ_ID}.{self.f['location']}"] = {"$in": location_name}

        area_path = f"answers.{self.f['area']}"
        # ids_label_dct={'area':self.f['area']} fuerza a obtener el diccionarion con esos nombres 
        # paso un error que daba otro label
        data = self.format_cr(self.cr.find(match_query, {area_path: 1}).sort(area_path, 1),  ids_label_dct={'area':self.f['area']})
        result = set(x.get('area') for x in data if x.get('area'))
        result = list(result)
        return result

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

    def get_ubicacion_by_id(self, record_id):
        """ Obtiene el detalle de una única ubicación por su ID de registro
        (mismo shape de campos que produce get_location_address).
        Args:
            record_id: El _id del registro de la ubicación (form 'ubicaciones').
        Returns:
            dict con folio, record_id, ubicacion y los datos de contacto.
        Raises:
            LKFException 404 si no existe.
        """
        if not record_id:
            raise self.LKFException({'msg': 'record_id es requerido.', 'status_code': 400})

        query = [
            {'$match': {
                '_id': ObjectId(record_id),
                'form_id': self.UBICACIONES,
                'deleted_at': {'$exists': False},
            }},
            {'$project': {
                '_id': 1,
                'folio': '$folio',
                'location': f"$answers.{self.f['location']}",
                'address_name': f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['address_name']}",
                'address': {'$first': f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['address']}"},
                'address2': {'$first': f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['address2']}"},
                'address_type': {'$first': f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['address_type']}"},
                'address_geolocation': {'$first': f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['address_geolocation']}"},
                'state': {'$first': f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['state']}"},
                'city': {'$first': f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['city']}"},
                'zip_code': {'$first': f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['zip_code']}"},
                'country': {'$first': f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['country']}"},
                'phone': {'$first': f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['phone']}"},
                'email': {'$first': f"$answers.{self.CONTACTO_CAT_OBJ_ID}.{self.f['email']}"},
            }},
        ]
        response = self.format_cr(self.cr.aggregate(query))
        response = self.unlist(response)
        if not response:
            raise self.LKFException({'msg': 'Ubicación no encontrada', 'status_code': 404})

        location_name = response.get('location', '')
        response['areas_count'] = len(self.get_areas_by_location(location_name))
        response['record_id'] = str(response.get('_id', record_id))
        return response

    def get_catalog_ubicaciones_formatted(self, ubicacion):
        """ Regresa la ubicación (registro del form 'ubicaciones') en una lista
        de 0 o 1 elementos, mismo shape que get_ubicacion_by_id, para que el
        front la pueda tratar igual que get_catalog_areas_formatted (una
        petición por cada ubicación seleccionada en el top-nav).
        Args:
            ubicacion: nombre de la ubicación (ej. 'Planta Monterrey').
        Returns:
            list[dict]
        """
        location_data = self.get_location_address(ubicacion)
        if not location_data:
            return []
        location_data['record_id'] = str(location_data.get('_id', ''))
        location_data['areas_count'] = len(self.get_areas_by_location(ubicacion))
        return [location_data]

    def exists_ubicacion(self, nombre):
        query = [
            {'$match': {
                'deleted_at': {'$exists': False},
                'form_id': self.UBICACIONES,
                f"answers.{self.f['location']}": nombre,
            }},
            {'$project': {'_id': 1}},
            {'$limit': 1},
        ]
        res = self.format_cr(self.cr.aggregate(query))
        return True if res else False

    def create_new_ubicacion(self, nombre='', direccion='', colonia='', ciudad='',
                              estado='', pais='', codigo_postal='', telefono='',
                              email='', geolocalizacion=None):
        """ Crea un registro nuevo en el form 'ubicaciones'.
        Args:
            nombre: nombre de la ubicación (requerido).
            direccion, colonia, ciudad, estado, pais, codigo_postal, telefono,
                email, geolocalizacion: campos del catálogo Contacto.
        Returns:
            La respuesta directa de post_forms_answers, o None si ya existía
            una ubicación con ese nombre (idempotente, igual que create_new_area).
        """
        if not nombre:
            raise self.LKFException({'msg': 'El nombre de la ubicación es requerido.', 'status_code': 400})
        if self.exists_ubicacion(nombre):
            return None

        answers = {
            self.f['location']: nombre,
            self.CONTACTO_CAT_OBJ_ID: {
                self.f['address_name']: nombre,
                self.f['address']: direccion,
                self.f['address2']: colonia,
                self.f['city']: ciudad,
                self.f['zip_code']: codigo_postal,
                self.f['country']: pais,
                self.f['state']: estado,
                self.f['phone']: telefono,
                self.f['email']: email,
                self.f['address_geolocation']: geolocalizacion or {},
            },
        }

        metadata = self.lkf_api.get_metadata(form_id=self.UBICACIONES)
        metadata.update({
            'properties': {
                'device_properties': {
                    'system': 'Addons',
                    'process': 'Creacion de Ubicacion',
                    'accion': 'create_new_ubicacion',
                    'file': 'location/app.py',
                },
            },
            'answers': answers,
        })
        return self.lkf_api.post_forms_answers(metadata)

    def update_ubicacion(self, record_id='', nombre_actual='', nombre=None,
                          direccion=None, colonia=None, ciudad=None, estado=None,
                          pais=None, codigo_postal=None, telefono=None, email=None,
                          geolocalizacion=None):
        """ Actualiza los campos de contacto (y/o nombre) de una ubicación existente.
        Solo los kwargs distintos de None se sobreescriben; el resto conserva
        el valor actual del registro (patch parcial).
        Args:
            record_id: _id del registro a actualizar (o nombre_actual para localizarlo por nombre).
            nombre_actual: nombre vigente de la ubicación, usado para localizarla si no hay record_id.
            nombre, direccion, colonia, ciudad, estado, pais, codigo_postal,
                telefono, email, geolocalizacion: nuevos valores (opcionales).
        Returns:
            La respuesta directa de patch_multi_record.
        Raises:
            LKFException 400/404 si falta el identificador o no se encuentra.
        """
        if not record_id and not nombre_actual:
            raise self.LKFException({'msg': 'Se requiere record_id o nombre_actual de la ubicación.', 'status_code': 400})

        if record_id:
            current = self.get_ubicacion_by_id(record_id)
        else:
            current = self.get_location_address(nombre_actual)
            record_id = str(current.get('_id', ''))

        if not current:
            raise self.LKFException({'msg': 'Ubicación no encontrada.', 'status_code': 404})

        answers = {}
        if nombre and nombre != nombre_actual:
            answers[self.f['location']] = nombre

        overrides = {
            self.f['address']: direccion,
            self.f['address2']: colonia,
            self.f['city']: ciudad,
            self.f['zip_code']: codigo_postal,
            self.f['country']: pais,
            self.f['state']: estado,
            self.f['phone']: telefono,
            self.f['email']: email,
            self.f['address_geolocation']: geolocalizacion,
        }
        contacto_answers = {
            self.f['address_name']: nombre or current.get('address_name', ''),
            self.f['address']: current.get('address', ''),
            self.f['address2']: current.get('address2', ''),
            self.f['city']: current.get('city', ''),
            self.f['zip_code']: current.get('zip_code', ''),
            self.f['country']: current.get('country', ''),
            self.f['state']: current.get('state', ''),
            self.f['phone']: current.get('phone', ''),
            self.f['email']: current.get('email', ''),
            self.f['address_geolocation']: current.get('address_geolocation', ''),
        }
        for field_id, value in overrides.items():
            if value is not None:
                contacto_answers[field_id] = value
        answers[self.CONTACTO_CAT_OBJ_ID] = contacto_answers

        return self.lkf_api.patch_multi_record(answers=answers, form_id=self.UBICACIONES, record_id=[record_id])
