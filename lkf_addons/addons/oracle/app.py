# -*- coding: utf-8 -*-


# -*- coding: utf-8 -*-

import cx_Oracle

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

from lkf_addons.addons.base.app import Base

### Objecto de Modulo ###
'''
    Cada modulo puede tener N objetos, configurados en clases.
    Estos objetos deben de heredar de base.LKF_Base) y cualquier modulo dependiente
    Al hacer el super() del __init__(), heredamos las variables de configuracion de clase.

    Se pueden heredar funciones de cualquier clase heredada con el metodo super(). 
'''

class Oracle(Base):

    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False, **kwargs):
        #use self.lkm.catalog_id() to get catalog id
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api)
        self.name =  __class__.__name__
        self.settings = settings
        self.ORACLE_HOST = self.settings.config['ORACLE_HOST']
        self.ORACLE_PORT = self.settings.config['ORACLE_PORT']
        self.ORACLE_SERVICE_NAME = self.settings.config.get('ORACLE_SERVICE_NAME')
        self.ORACLE_SID = self.settings.config.get('ORACLE_SID')
        self.ORACLE_USERNAME = self.settings.config['ORACLE_USERNAME']
        self.ORACLE_PASSWORD = self.settings.config['ORACLE_PASSWORD']
        self.oracle = self.connect_to_oracle()
        self.f={}

    def connect_to_oracle(self):
        print('=== Establishing Connection to Oracle ===')
        try:
            if self.ORACLE_SERVICE_NAME:
                dsn = cx_Oracle.makedsn(self.ORACLE_HOST, self.ORACLE_PORT, service_name=self.ORACLE_SERVICE_NAME)
            elif self.ORACLE_SID:
                dsn = cx_Oracle.makedsn(self.ORACLE_HOST, self.ORACLE_PORT, sid=self.ORACLE_SID) 
            else:
                self.LKFException("No se proporciono un service_name o sid")
            
            try:
                self.orcale_connection = cx_Oracle.connect(self.ORACLE_USERNAME, self.ORACLE_PASSWORD, dsn)
            except cx_Oracle.DatabaseError as e:
                error, = e.args
                print(f"Error code: {error.code}")
                print(f"Error message: {error.message}")
                print('Error',e)
                return None
                #return self.LKFException(f"Error code: {error.code} - {error.message}")
            return self.orcale_connection
        except  cx_Oracle.DatabaseError as e:
            error, = e.args
            print(f"Error code: {error.code}")
            print(f"Error message: {error.message}")
            print('Error=',e)
            return self.LKFException(f"Error code: {error.code} - {error.message}")

    def query_view(self, view_name, query=False, date_format=False):
        """
        Query a view in Oracle
        view_name: Name of the view
        query: Query to execute
        date_format: Boolean to format the date
        """
        result = []
        columns = []
        cursor = None
        try:
            cursor = self.orcale_connection.cursor()
            # Query to fetch data from the view
            if not query:
                query = f"SELECT * FROM {view_name}"
            if date_format:
                cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'DD/MM/RR'")
                cursor.execute("ALTER SESSION SET NLS_DATE_LANGUAGE = 'SPANISH'")
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            for row in rows:
                result.append(dict(zip(columns, row)))
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            print(f"Error querying view: {error.code} - {error.message}")
        finally:
            if cursor:
                cursor.close()
            else:
                self.LKFException('No cursor')
        return columns, result

    def search_views(self):
        try:
            cursor = self.orcale_connection.cursor()
            # Query to fetch the views
            cursor.execute("""
                SELECT view_name 
                FROM all_views 
                ORDER BY view_name
            """)
            views = cursor.fetchall()
            for view in views:
                print(view[0])
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            print(f"Error fetching views: {error.code} - {error.message}")
        finally:
            cursor.close()
