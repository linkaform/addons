# -*- coding: utf-8 -*-
### Linkaform Modules / Archivo de Modulo ###
'''
Archivo para utilizar las funcionalidades modulares de LinkaForm.
Con estas funcionalides podras utilizar la plafaorma de LinkaForm de 
manera modular, como un Backend as a Service o BaaS.
Este es un codigo es lincenciado bajo la licencia GPL3 (https://www.gnu.org/licenses/gpl-3.0.html)
El codigo es auto documentable y adaptable. Con la idea de que puedas reutilizar
gran parte del codigo en otros modulos, copiando y pegando en los nuevo modulos.
Al hacer esto, FAVOR de al copiar secciones de codigo, COPIAR CON TODO Y SU DOCUMENTACION.
Al hacer un documento nuevo o modulo nuevo, puedes copiarte de la carpeta _templates o de sus archivos,
pero cada que hagas un nuevo archivo, favor de copiar estas instrucciones y las generales que apliquen a 
cada archivo.
'''

### Archivo de Modulo ###
'''
En este archivo de define las funciones generales del modulo. Estos seran nombrados por conveniencia
app.py, si llegaras a tener mas de una app, puedes crear un folder llamado app o sencillamente guardarlos
a primer nivel. Tambien puedes hacer archvios llamados por conveniencia o estandar:
app_utils.py, utils.py, xxx_utils.py       
'''

from linkaform_api import base

### Objecto de Modulo ###
'''
Cada modulo puede tener N objetos, configurados en clases.
Estos objetos deben de heredar de base.LKF_Base) y cualquier modulo dependiente
Al hacer el super() del __init__(), heredamos las variables de configuracion de clase.
Se pueden heredar funciones de cualquier clase heredada con el metodo super(). 
'''
# class Stock(Employee, Warehouse, Product, base.LKF_Base):

class JIT(base.LKF_Base):


    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False):
        #base.LKF_Base.__init__(self, settings, sys_argv=sys_argv, use_api=use_api)
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api)

        print('lokf', self.lkm)
        self.BOM_ID = self.lkm.form_id('bom','id')

    def explote_kit(self, product):
        print('EXPOLTE')
        print('TODO BUSCAR EL PRODUCTO DESTRDO DE LOS BOMS Y REGRESAR EL LISTADO DE PRODUCTOS.')
        print('EXPOLTE',D)
