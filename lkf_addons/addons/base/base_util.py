# -*- coding: utf-8 -*-

from linkaform_api import base


class Base(base.LKF_Base):

    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False):
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api)
        #use self.lkm.catalog_id() to get catalog id
        # forms
        self.CONTACTO = self.lkm.form_id('contacto', 'id')
        self.CLIENTE = self.lkm.form_id('clientes', 'id')
        # catalgos

        self.CLIENTE_CAT = self.lkm.catalog_id('clientes')
        self.CLIENTE_CAT_ID = self.CLIENTE_CAT.get('id')
        self.CLIENTE_CAT_OBJ_ID = self.CLIENTE_CAT.get('obj_id')

        self.COMPANY = self.lkm.catalog_id('compaia')
        self.COMPANY_ID = self.COMPANY.get('id')
        self.COMPANY_OBJ_ID = self.COMPANY.get('obj_id')

        self.CONTACTO_CAT = self.lkm.catalog_id('contacto')
        self.CONTACTO_CAT_ID = self.CONTACTO_CAT.get('id')
        self.CONTACTO_CAT_OBJ_ID = self.CONTACTO_CAT.get('obj_id')


        self.ESTADO = self.lkm.catalog_id('estados')
        self.ESTADO_ID = self.ESTADO.get('id')
        self.ESTADO_OBJ_ID = self.ESTADO.get('obj_id')

        self.COUNTRY = self.lkm.catalog_id('pais')
        self.COUNTRY_ID = self.COUNTRY.get('id')
        self.COUNTRY_OBJ_ID = self.COUNTRY.get('obj_id')

        self.TIMEZONE = self.lkm.catalog_id('timezone')
        self.TIMEZONE_ID = self.TIMEZONE.get('id')
        self.TIMEZONE_OBJ_ID = self.TIMEZONE.get('obj_id')

        self.f.update( {
            'address_name':'663a7e0fe48382c5b1230901',
            'address_image':'663a808be48382c5b123090d',
            'address_geolocation':'663e5c8cf5b8a7ce8211ed0c',
            'address_status':'6663a7f67e48382c5b1230909',
            'address_type':'663a7f67e48382c5b1230908',
            'address':'663a7e0fe48382c5b1230902',
            'address2':'663a7f79e48382c5b123090a',
            'country':'663a7ca6e48382c5b12308fa',
            'city':'6654187fc85ce22aaf8bb070',
            'nombre_comercial':'667468e3e577b8b98c852aaa',
            'razon_social':'6687f2f37b2c023e187d6252',
            'rfc_razon_social':'667468e3e577b8b98c852aab',
            'email':'66bfd647cd15883ed163e9b5',
            'telefono':'66bfd666cd15883ed163e9b6',
            'pagina_web':'66bfd66ecd15883ed163e9b7',
            'state':'663a7dd6e48382c5b12308ff',
            'state_code':'663a7dd6e48382c5b1230900',
            'email':'663a7ee1e48382c5b1230907',
            'phone':'663a7ee1e48382c5b1230906',
            'zip_code':'663a7ee1e48382c5b1230905',
            'timezone':'665e4f90c4cf32cb52ebe15c',
            'cat_timezone':f'{self.TIMEZONE_OBJ_ID}.665e4f90c4cf32cb52ebe15c',
        }
        )