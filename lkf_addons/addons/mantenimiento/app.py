# -*- coding: utf-8 -*-
### Linkaform Modules / Archivo de Módulo ###
'''
Este archivo proporciona las funcionalidades modulares de LinkaForm. Con estas funcionalidades, 
podrás utilizar la plataforma LinkaForm de manera modular, como un Backend as a Service (BaaS).

Licencia BSD
Copyright (c) 2024 Infosync / LinkaForm.  
Todos los derechos reservados.

Se permite la redistribución y el uso en formas de código fuente y binario, con o sin modificaciones, siempre que se cumplan las siguientes condiciones:

1. Se debe conservar el aviso de copyright anterior, esta lista de condiciones y el siguiente descargo de responsabilidad en las redistribuciones del código fuente.
2. Se debe reproducir el aviso de copyright anterior, esta lista de condiciones y el siguiente descargo de responsabilidad en la documentación y/u otros materiales proporcionados con las distribuciones en formato binario.
3. Ni el nombre del Infosync ni los nombres de sus colaboradores pueden ser utilizados para respaldar o promocionar productos derivados de este software sin permiso específico previo por escrito.

Propósito
El propósito de este archivo es ser auto documentable y adaptable, facilitando la reutilización 
de gran parte del código en otros módulos simplemente copiando y pegando las secciones necesarias.

Instrucciones
1. Al copiar secciones de código, asegúrate de incluir la documentación correspondiente.
2. Al crear un nuevo archivo o módulo, copia las instrucciones y las generales aplicables a cada archivo.
3. Puedes basarte en la carpeta `_templates` o sus archivos para crear nuevos módulos.
'''

### Archivo de Modulo ###
import pytz
import logging
import tempfile
import os
import uuid
import simplejson, time
from bson import ObjectId
from datetime import datetime, timedelta
from copy import deepcopy
import urllib.parse

from linkaform_api import base
from lkf_addons.addons.base.app import Base

class Mantenimiento(Base):

    def __init__(self, settings, sys_argv=None, use_api=False, **kwargs):
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api, **kwargs)
        self.kwargs['MODULES'] = self.kwargs.get('MODULES',[])
        if self.__class__.__name__ not in kwargs:
            self.kwargs['MODULES'].append(self.__class__.__name__)
        # self.load(module='Product', **self.kwargs)
        # self.load(module='Product', module_class='Warehouse', import_as='WH', **self.kwargs)
        
        #Catalogos
        self.MANTENIMIENTO_CAT_CIUDAD_X_REGION = self.lkm.catalog_id('ciudades_por_region')
        self.MANTENIMIENTO_CAT_CIUDAD_X_REGION_ID = self.MANTENIMIENTO_CAT_CIUDAD_X_REGION.get('id')
        self.MANTENIMIENTO_CAT_CIUDAD_X_REGION_OBJ_ID = self.MANTENIMIENTO_CAT_CIUDAD_X_REGION.get('obj_id')
        
        self.MANTENIMIENTO_CAT_CLIENTES = self.lkm.catalog_id('clientes')
        self.MANTENIMIENTO_CAT_CLIENTES_ID = self.MANTENIMIENTO_CAT_CLIENTES.get('id')
        self.MANTENIMIENTO_CAT_CLIENTES_OBJ_ID = self.MANTENIMIENTO_CAT_CLIENTES.get('obj_id')

        self.MANTENIMIENTO_CAT_INSTRUMENTOS = self.lkm.catalog_id('instrumentos')
        self.MANTENIMIENTO_CAT_INSTRUMENTOS_ID = self.MANTENIMIENTO_CAT_INSTRUMENTOS.get('id')
        self.MANTENIMIENTO_CAT_INSTRUMENTOS_OBJ_ID = self.MANTENIMIENTO_CAT_INSTRUMENTOS.get('obj_id')

        self.MANTENIMIENTO_CAT_INV_DE_EQUIPOS = self.lkm.catalog_id('inventario_de_equipos')
        self.MANTENIMIENTO_CAT_INV_DE_EQUIPOS_ID = self.MANTENIMIENTO_CAT_INV_DE_EQUIPOS.get('id')
        self.MANTENIMIENTO_CAT_INV_DE_EQUIPOS_OBJ_ID = self.MANTENIMIENTO_CAT_INV_DE_EQUIPOS.get('obj_id')

        f = {
            'test_field':'66ce2441d63bb7a3871adeaf',
        }

        if hasattr(self, 'f'):
            self.f.update(f)
        else:
            print('vaa  A IGUALSAR')
            self.f = f

        mf = deepcopy(f)

        if hasattr(self, 'mf'):
            self.mf.update(mf)
        else:
            self.mf = mf

    def test_module(self):
        print('Entra en test module...')
        test_dic = {
            'id1': self.MANTENIMIENTO_CAT_CIUDAD_X_REGION_ID,
            'id2': self.MANTENIMIENTO_CAT_CLIENTES_ID,
            'id3': self.MANTENIMIENTO_CAT_INSTRUMENTOS_ID,
            'id4': self.MANTENIMIENTO_CAT_INV_DE_EQUIPOS_ID,
            # 'id5': self.Product.SKU_OBJ_ID,
            'id6': self.f['test_field'],
        }
        print(test_dic)