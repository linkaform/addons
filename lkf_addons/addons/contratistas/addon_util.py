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
from linkaform_api import base

### Objeto o Clase de Módulo ###
'''
Cada módulo puede tener múltiples objetos, configurados en clases.
Estos objetos deben heredar de `base.LKF_Base` y de cualquier módulo dependiente necesario.
Al utilizar `super()` en el método `__init__()`, heredamos las variables de configuración de la clase.

Además, se pueden heredar funciones de cualquier clase antecesora usando el método `super()`.
'''

class ModuleName(base.LKF_Base):

    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False):
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api)

        #--Variables 
        ### Forms ###
        '''
        Use `self.FORM_NAME = self.lkm.form_id('form_name',id)` ---> Aquí deberás guardar los `ID` de los formularios. 
        Para ello deberás llamar el método `lkm.form_id` del objeto `lkm` (linkaform modules, por sus siglas).
        En `lkm` están todas las funciones generales de módulos. p.j
        '''

        #--Variables 
        ### Catálogos ###
        '''
        Use `self.CATALOG_NAME = self.lkm.catalog_id('catalog_name',id)` ---> Aquí deberás guardar los `ID` de los catálogos. 
        Para ello deberás llamar el método `lkm.catalog_id` del objeto `lkm`(linkaform modules, por sus siglas).
        En `lkm` están todas las funciones generales de módulos).
        '''
        self.f = {
            'key':'form_field_ObjectId()'
        }

    '''
    funciones internas: son funciones que solo se pueden mandar llamar dentro de este archivo. Si se hereda la clase
    esta función no puede ser invocada.

    pep-0008:
        _single_leading_underscore: 
        weak “internal use” indicator. E.g. from M import * does not import objects whose names start with an underscore.
    
    def _NAME(self, ):
    '''
    
