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
'''
Este archivo define las funciones generales del módulo. Por conveniencia, se nombra `app.py`. 

Si tienes más de una aplicación, puedes:
    a. Crear una carpeta llamada `app`.
    b. Guardar los archivos a nivel raíz.
    c. Nombrar los archivos por conveniencia o estándar: `app_utils.py`, `utils.py`, `xxx_utils.py`.
'''

# Importaciones necesarias
from lkf_addons.addons.base.app import Base

### Objeto o Clase de Módulo ###
'''
Cada módulo puede tener múltiples objetos, configurados en clases.
Estos objetos deben heredar de `base.LKF_Base` y de cualquier módulo dependiente necesario.
Al utilizar `super()` en el método `__init__()`, heredamos las variables de configuración de la clase.

Además, se pueden heredar funciones de cualquier clase antecesora usando el método `super()`.
'''

class Produccion_PCI(Base):
    
    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False):
        # base.LKF_Base.__init__(self, settings, sys_argv=sys_argv)
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api)

        self.ORDEN_SERVICIO_FIBRA = self.lkm.form_id('orden_de_servicio_metro_ftthiasa','id')
        self.ORDEN_SERVICIO_COBRE = self.lkm.form_id('orden_de_servicio_metro_cobreiasa','id')
        self.ORDEN_SERVICIO_FIBRA_OCCIDENTE = self.lkm.form_id('orden_de_servicio_occidente_ftthiasa','id')
        self.ORDEN_SERVICIO_COBRE_OCCIDENTE = self.lkm.form_id('orden_de_servicio_occidente_cobreiasa','id')
        self.ORDEN_SERVICIO_FIBRA_NORTE = self.lkm.form_id('orden_de_servicio_norte_ftthiasa','id')
        self.ORDEN_SERVICIO_COBRE_NORTE = self.lkm.form_id('orden_de_servicio_norte_cobreiasa','id')
        self.ORDEN_SERVICIO_FIBRA_SURESTE = self.lkm.form_id('orden_de_servicio_sur_ftthiasa','id')
        self.ORDEN_SERVICIO_COBRE_SURESTE = self.lkm.form_id('orden_de_servicio_sur_cobreiasa','id')

        # Aqui los ids de las formas de liberacion
        self.FORMA_LIBERACION_FIBRA = self.lkm.form_id('liberacin_de_pagos_socio', 'id')
        self.FORMA_LIBERACION_FIBRA_SURESTE = self.lkm.form_id('liberacin_de_pagos_sur_socio', 'id')
        self.FORMA_LIBERACION_FIBRA_NORTE = self.lkm.form_id('liberacin_de_pagos_norte_socio', 'id')
        self.FORMA_LIBERACION_FIBRA_OCCIDENTE = self.lkm.form_id('liberacin_de_pagos_occidente_socio', 'id')
        self.FORMA_LIBERACION_COBRE = self.lkm.form_id('liberacin_de_pagos_cobre_socio', 'id')
        self.FORMA_LIBERACION_COBRE_SURESTE = self.lkm.form_id('liberacin_de_pagos_sur_cobre_socio', 'id')
        self.FORMA_LIBERACION_COBRE_NORTE = self.lkm.form_id('liberacin_de_pagos_norte_cobre_socio', 'id')
        self.FORMA_LIBERACION_COBRE_OCCIDENTE = self.lkm.form_id('liberacin_de_pagos_occidente_cobre_socio', 'id')

        # Aqui los ids de las formas de orden de compra
        self.FORMA_ORDEN_COMPRA_FIBRA = self.lkm.form_id('orden_compra_contratista_ftth_metro_socio', 'id')
        self.FORMA_ORDEN_COMPRA_FIBRA_SURESTE = self.lkm.form_id('orden_compra_contratista_ftth_sur_socio', 'id')
        self.FORMA_ORDEN_COMPRA_FIBRA_NORTE = self.lkm.form_id('orden_compra_contratista_ftth_norte_socio', 'id')
        self.FORMA_ORDEN_COMPRA_FIBRA_OCCIDENTE = self.lkm.form_id('orden_compra_contratista_ftth_occidente_socio', 'id')
        self.FORMA_ORDEN_COMPRA_COBRE = self.lkm.form_id('orden_compra_contratista_cobre_metro_socio', 'id')
        self.FORMA_ORDEN_COMPRA_COBRE_SURESTE = self.lkm.form_id('orden_compra_contratista_cobre_sur_socio', 'id')
        self.FORMA_ORDEN_COMPRA_COBRE_NORTE = self.lkm.form_id('orden_compra_contratista_cobre_norte_socio', 'id')
        self.FORMA_ORDEN_COMPRA_COBRE_OCCIDENTE = self.lkm.form_id('orden_compra_contratista_cobre_occidente_socio', 'id')

    def get_metadata_properties(self, name_script, accion, process='', folio_carga=''):
        dict_properties = {
            'device_properties': {
                'system': 'SCRIPT',
                'process': process,
                'accion': accion,
                'archive': name_script
            }
        }
        if folio_carga:
            dict_properties['device_properties']['folio carga'] = folio_carga
        return dict_properties
