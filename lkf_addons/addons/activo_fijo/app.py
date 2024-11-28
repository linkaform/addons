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
    En este archivo de define las funciones generales del modulo. Estos seran nombrados por conveniencia
    app.py, si llegaras a tener mas de una app, puedes crear un folder llamado app o sencillamente guardarlos
    a primer nivel. Tambien puedes hacer archvios llamados por conveniencia o estandar:
    app_utils.py, utils.py, xxx_utils.py       
'''

from lkf_addons.addons.base.app import Base

### Objecto de Modulo ###
'''
    Cada modulo puede tener N objetos, configurados en clases.
    Estos objetos deben de heredar de base.LKF_Base) y cualquier modulo dependiente
    Al hacer el super() del __init__(), heredamos las variables de configuracion de clase.

    Se pueden heredar funciones de cualquier clase heredada con el metodo super(). 
'''
class Vehiculo(Base):

    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False, **kwargs):
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api)
        #--Variables 
        ### Forms ###
        '''
        Use `self.FORM_NAME = self.lkm.form_id('form_name',id)` ---> Aquí deberás guardar los `ID` de los formularios. 
        Para ello deberás llamar el método `lkm.form_id` del objeto `lkm` (linkaform modules, por sus siglas).
        En `lkm` están todas las funciones generales de módulos.
        '''
        
        #--Variables 
        ### Catálogos ###
        '''
        Use `self.CATALOG_NAME = self.lkm.catalog_id('catalog_name',id)` ---> Aquí deberás guardar los `ID` de los catálogos. 
        Para ello deberás llamar el método `lkm.catalog_id` del objeto `lkm`(linkaform modules, por sus siglas).
        En `lkm` están todas las funciones generales de módulos).
        '''


        #--Variables 
        # Module Globals#
        self.support_guard = 'guardia_de_apoyo'
        self.chife_guard = 'guardia_lider'
        # Forms #
        '''
        self.FORM_NAME = self.lkm.form_id('form_name',id)
        aqui deberas guardar el los ID de los formularios. 
        Para ello ocupas llamar el metodo lkm.form_id del objeto lkm(linkaform modules, por sus siglas, 
        en lkm estan todas las funcions generales de modulos).

        '''
        self.ACTIVOS_FIJOS = self.lkm.form_id('activos_fijos','id')

        # catalogos
        '''
        self.CATALOG_NAME = self.lkm.catalog_id('catalog_name',id)
        aqui deberas guardar el los ID de los catalogos. 
        Para ello ocupas llamar el metodo lkm.catalog_id del objeto lkm(linkaform modules, por sus siglas, 
        en lkm estan todas las funcions generales de modulos).

        '''


        self.ACTIVOS_FIJOS_CAT = self.lkm.catalog_id('activos_fijos')
        self.ACTIVOS_FIJOS_CAT_ID = self.ACTIVOS_FIJOS_CAT.get('id')
        self.ACTIVOS_FIJOS_CAT_OBJ_ID = self.ACTIVOS_FIJOS_CAT.get('obj_id')

        self.TIPO_DE_EQUIPO = self.lkm.catalog_id('tipo_de_equipos')
        self.TIPO_DE_EQUIPO_ID = self.TIPO_DE_EQUIPO.get('id')
        self.TIPO_DE_EQUIPO_OBJ_ID = self.TIPO_DE_EQUIPO.get('obj_id')

        self.TIPO_DE_VEHICULO = self.lkm.catalog_id('tipos_de_vehiculo')
        self.TIPO_DE_VEHICULO_ID = self.TIPO_DE_VEHICULO.get('id')
        self.TIPO_DE_VEHICULO_OBJ_ID = self.TIPO_DE_VEHICULO.get('obj_id')

        self.MARCA = self.lkm.catalog_id('marca')
        self.MARCA_ID = self.MARCA.get('id')
        self.MARCA_OBJ_ID = self.MARCA.get('obj_id')

        self.MODELO = self.lkm.catalog_id('modelo')
        self.MODELO_ID = self.MODELO.get('id')
        self.MODELO_OBJ_ID = self.MODELO.get('obj_id')

        ## Module Fields ##
        ''' self.mf : Estos son los campos que deseas mantener solo dentro de este modulo '''
        self.mf = {}

        ## Fields ##
        '''
            self.f : En esta vairable "fields", se almacenan todos los campos de todos lo modulos heredados.
            El orden de remplazo de ve afectado por el orden en que se hereda cada modulo. El orden que se otroga, es considerando
            que la vaiable se iguala en la base, y se va armando en tren de dependencias ej.
                Class A:
                Class B(A):
                Class C(B):
                Class D(C):

                x_obj = D()
                el orden de heredacion sera, primero carga A>B>C>D.
        '''
        self.f.update({
            'categoria_marca':'66beb1b507981d4509575057',
            'categoria':'66beb1b507981d4509575057',
            'estatus':'6646393c3fa8b818265d0329',
            'estado':'66c1940b89463aa27fc1818c',
            'fecha_horometro':'66c176ac89463aa27fc18172',
            'fecha_horometro_2':'66c176ac89463aa27fc18173',
            'fecha_kilometraje':'66c189f689463aa27fc18189',
            'fecha_kilometraje_2':'66c176dc89463aa27fc18175',
            'marca':'66beb10007981d4509575054',
            'marca_codigo':'6711e87ecbb5910b3ef1fc40',
            'modelo':'66beb11907981d4509575056',
            'modelo_codigo':'6711e911b652074034fd915c',
            'nombre_equipo':'66c192ef89463aa27fc1818b',
            'numero_de_serie_chasis':'6646393c3fa8b818265d0325',
            'numero_de_serie_motor1':'66c174ec89463aa27fc1816c',
            'numero_de_serie_motor2':'66c174ec89463aa27fc1816d',
            'tipo_vehiculo':'65f22098d1dc5e0b9529e89a',
            'tipo_equipo':'6639a9d9d38959539f59eb9f',
            'ultimo_horometro':'66c1758989463aa27fc1816e',
            'ultimo_horometro_2':'66c1758989463aa27fc1816f',
            'ultimo_kilometraje':'66c1758989463aa27fc18170',
            'ultimo_kilometraje2':'66c1758989463aa27fc18171',
            }
            )


