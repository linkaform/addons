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

from linkaform_api.base import LKF_Base

### Objecto de Modulo ###
    '''
    Cada modulo puede tener N objetos, configurados en clases.
    Estos objetos deben de heredar de base.LKF_Base) y cualquier modulo dependiente
    Al hacer el super() del __init__(), heredamos las variables de configuracion de clase.

    Se pueden heredar funciones de cualquier clase heredada con el metodo super(). 
    '''
class Vehiculo(LKF_Base):

    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False):
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api)
        #use self.lkm.catalog_id() to get catalog id

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
        self.f.update(
            'tipo_vehiculo':'65f22098d1dc5e0b9529e89a'
            )
