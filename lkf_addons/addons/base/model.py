# -*- coding: utf-8 -*-
### Linkaform Modules / Archivo de Módulo ###
'''
Este archivo define el modelo de datos del módulo Accesos.
Contiene los IDs de formularios, catálogos y campos (fields) usados por la clase Accesos.

Separado de app.py para mantener la configuración de datos desacoplada de la lógica de negocio.
'''
from linkaform_api import base

### Modelo de Módulo ###
'''
AccesosModel agrupa la inicialización de IDs de formularios, catálogos y fields.
La clase Accesos en app.py hereda de esta clase para tener acceso a todas las variables
sin mezclarlas con la lógica de negocio.
'''

class BaseModel(base.LKF_Base):

    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False, **kwargs):
        mf =  {
                'form_name':'5d810a982628de5556500d55',
                'form_id':'5d810a982628de5556500d56',
                'form_type':'ccccc0000000000000000002',
                }
        if hasattr(self, 'mf'):
            self.mf.update(mf)
        else:
            self.mf = mf
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
        self.CONFIGURACIONES = self.lkm.form_id('configuraciones', 'id')
        self.ENVIO_DE_CORREOS = self.lkm.form_id('envio_de_correos', 'id')
        self.ROL = self.lkm.form_id('rol', 'id')
        self.USUARIOS_FORM = self.lkm.form_id('usuarios', 'id')
        ### Catálogos ###
        '''
        `self.CATALOG_NAME = self.lkm.catalog_id('catalog_name',id)` ---> Aquí deberás guardar los `ID` de los catálogos.
        Para ello deberás llamar el método `lkm.catalog_id` del objeto `lkm`(linkaform modules, por sus siglas).
        En `lkm` están todas las funciones generales de módulos).
        '''

        self.CATALOGO_FORMAS_CAT = self.lkm.catalog_id('catalogo_de_formas')
        self.CATALOGO_FORMAS_CAT_ID = self.CATALOGO_FORMAS_CAT.get('id')
        self.CATALOGO_FORMAS_CAT_OBJ_ID = self.CATALOGO_FORMAS_CAT.get('obj_id')

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

        self.ROL_CAT = self.lkm.catalog_id('rol')
        self.ROL_CAT_ID = self.ROL_CAT.get('id')
        self.ROL_CAT_OBJ_ID = self.ROL_CAT.get('obj_id')

        self.TIMEZONE = self.lkm.catalog_id('timezone')
        self.TIMEZONE_ID = self.TIMEZONE.get('id')
        self.TIMEZONE_OBJ_ID = self.TIMEZONE.get('obj_id')

        self.USUARIOS = self.lkm.catalog_id('usuarios')
        self.USUARIOS_ID = self.USUARIOS.get('id')
        self.USUARIOS_OBJ_ID = self.USUARIOS.get('obj_id')

        self.GROUP = self.lkm.catalog_id('grupos')
        self.GROUP_ID = self.GROUP.get('id')
        self.GROUP_OBJ_ID = self.GROUP.get('obj_id')

        self.UOM = self.lkm.catalog_id('unidad_de_medida')
        self.UOM_ID = self.UOM.get('id')
        self.UOM_OBJ_ID = self.UOM.get('obj_id')


        ### Global Variables


        self.f.update( {
            'address':'663a7e0fe48382c5b1230902',
            'address2':'663a7f79e48382c5b123090a',
            'address_code':'ccca7e0fe48382c5b1230901',
            'address_geolocation':'663e5c8cf5b8a7ce8211ed0c',
            'address_image':'663a808be48382c5b123090d',
            'address_name':'663a7e0fe48382c5b1230901',
            'address_status':'663a7f67e48382c5b1230909',
            'address_type':'663a7f67e48382c5b1230908',
            'asignar_a':'abcde0001000000000020003',
            'asignar_de_grupo':'67ad6e90067960b5f2ce1e15',
            'cat_timezone':f'{self.TIMEZONE_OBJ_ID}.665e4f90c4cf32cb52ebe15c',
            'city':'6654187fc85ce22aaf8bb070',
            'client_code':'6711ea74b8514dc4fdfd917f',
            'config_group':'66ed0baac9aefada5b04b817',
            'country':'663a7ca6e48382c5b12308fa',
            'country_code':'663a7ca6e48382c5b12308fb',
            'country_ph_code':'663a7ca6e48382c5b12308fc',
            'email':'663a7ee1e48382c5b1230907',
            'email_contacto':'66bfd647cd15883ed163e9b5',
            'field_id_status':'5e32fbb498849f475cfbdca2',
            'group_id':'639b65dfaf316bacfc551ba2',
            'group_name':'638a9ab3616398d2e392a9fa',
            'grupo_roles':'6a46f1d3b89f9975dfd0bae8',
            'new_user_complete_name':'638a9a7767c332f5d459fc81',
            'new_user_email':'638a9a7767c332f5d459fc82',
            'new_user_id':'638a9a99616398d2e392a9f5',
            'new_user_phone':'67be0c43a31e5161c47f2bba',
            'new_user_position':'67be0c43a31e5161c47f2bbb',
            'new_user_status':'679d023876ad7f5ba642f4ed',
            'new_user_temp_password':'67be0b7896e72a692b4fa660',
            'new_user_username':'6759e4a7a9a6e13c7b26da33',
            'nombre_comercial':'667468e3e577b8b98c852aaa',
            'pagina_web':'66bfd66ecd15883ed163e9b7',
            'phone':'663a7ee1e48382c5b1230906',
            'phone2':'663a7ee1e48382c5b1232226',
            'razon_social':'6687f2f37b2c023e187d6252',
            'rfc_razon_social':'667468e3e577b8b98c852aab',
            'rol':'6a46f2730fc4d03a90da2209',
            'state':'663a7dd6e48382c5b12308ff',
            'state_code':'663a7dd6e48382c5b1230900',
            'telefono':'66bfd666cd15883ed163e9b6',
            'timezone':'665e4f90c4cf32cb52ebe15c',
            'uom':'669efc6f47920d1b51663d29',
            'uom_category':'669efbf447920d1b51663d28',
            'zip_code':'663a7ee1e48382c5b1230905',
        }
        )

        self.envio_correo_fields = {
            'email_from':"67169f72c736cc47794404f8",
            'email_to':"670d2e32756833542954716c",
            'enviado_desde':"6716a1067f394110d24404eb",
            'msj':"670d2d9d0337e410e4353550",
            "nombre": "670d2e32756833542954716b",
            'titulo':"67169f72c736cc47794404f9",
        }

        self.config_fields = {
            'demora':f'{self.f.get("demora")}',
            'lead_time':f'{self.f.get("lead_time")}',
            'dias_laborales_consumo':f'{self.f.get("dias_laborales_consumo")}',
            'factor_crecimiento_jit':f'{self.f.get("factor_crecimiento_jit")}',
            'factor_seguridad_jit':f'{self.f.get("factor_seguridad_jit")}',
            'uom':f'{self.UOM_OBJ_ID}.{self.f.get("uom")}',
            'procurment_location':f'{self.f.get("config_group")}',
            'warehouse_kind': '66ed0c88c9aefada5b04b818',
            # 'warehouse':f'{self.WAREHOUSE_OBJ_ID}.{self.f.get("warehouse")}',
            # 'location':f'{self.WAREHOUSE_OBJ_ID}.{self.f.get("location")}',
        }
       
