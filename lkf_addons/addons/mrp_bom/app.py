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

Licencia BSD
Copyright (c) 2024 Infosync / LinkaForm.  
Todos los derechos reservados.

Se permite la redistribución y el uso en formas de código fuente y binario, con o sin modificaciones, siempre que se cumplan las siguientes condiciones:

1. Se debe conservar el aviso de copyright anterior, esta lista de condiciones y el siguiente descargo de responsabilidad en las redistribuciones del código fuente.
2. Se debe reproducir el aviso de copyright anterior, esta lista de condiciones y el siguiente descargo de responsabilidad en la documentación y/u otros materiales proporcionados con las distribuciones en formato binario.
3. Ni el nombre del Infosync ni los nombres de sus colaboradores pueden ser utilizados para respaldar o promocionar productos derivados de este software sin permiso específico previo por escrito.

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
class Name_Your_Object(LKF_Base)