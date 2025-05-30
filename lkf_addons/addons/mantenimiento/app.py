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
        
        f = {
            'nick_eco': '67d258ea799fb700b898120f',
            'placa': '67d258ea799fb700b8981214',
            'marca_campo': '67d258ea799fb700b8981211',
            'modelo_campo': '67d258ea799fb700b8981210',
            'fecha_de_instalacion': '6646393c3fa8b818265d0327',
            'imagen_del_equipo': '6646393c3fa8b818265d0326',
            'hora_inicio_instalacion': '67c8c67734cc8b94bc183eca',
            'hora_final_instalacion': '67d218329d65ba66bf981253',
            'total_minutos_instalacion': '67d218329d65ba66bf981254',
            'cliente_instalacion': '66bfc0accd15883ed163e9b0',
            'mobile_id_instalacion': '67e2eddf63e826145d5a045d',
            's_n': '67e2eddf63e826145d5a045e',
            'p_n': '67e2eddf63e826145d5a045f',
            'imei': '67e2eddf63e826145d5a0460',
            'sim': '67e2eddf63e826145d5a0461',
            'activo_mobile_id': '67f80cb9190938b5447c1533',
            'activo_s_n': '67f80cb9190938b5447c1534',
            'activo_p_n': '67f80cb9190938b5447c1535',
            'activo_imei': '67f80cb9190938b5447c1536',
            'activo_sim': '67f80cb9190938b5447c1537'
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
