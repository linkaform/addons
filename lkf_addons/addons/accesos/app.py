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
from tkinter import NO
import pytz
import logging
import tempfile
import os
import uuid
import simplejson, time
from bson import ObjectId
from datetime import datetime, timedelta, time, date
import time as time_module
from copy import deepcopy
from math import ceil
import urllib.parse
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import requests
import jwt

from linkaform_api import base
from lkf_addons.addons.employee.app import Employee
from lkf_addons.addons.activo_fijo.app import Vehiculo
from lkf_addons.addons.location.app import Location
import arrow

from pdf2image import convert_from_bytes
from zipfile import ZipFile
### Objeto o Clase de Módulo ###
'''
Cada módulo puede tener múltiples objetos, configurados en clases.
Estos objetos deben heredar de `base.LKF_Base` y de cualquier módulo dependiente necesario.
Al utilizar `super()` en el método `__init__()`, heredamos las variables de configuración de la clase.

Además, se pueden heredar funciones de cualquier clase antecesora usando el método `super()`.
'''

class Accesos(Employee, Location, Vehiculo, base.LKF_Base):

    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False, **kwargs):
        #--Variables
        # Module Globals#
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api, **kwargs)
        self.support_guard = 'guardia_de_apoyo'
        self.chife_guard = 'guardia_lider'
        # Forms #
        '''
        Use `self.FORM_NAME = self.lkm.form_id('form_name',id)` ---> Aquí deberás guardar los `ID` de los formularios. 
        Para ello deberás llamar el método `lkm.form_id` del objeto `lkm` (linkaform modules, por sus siglas).
        En `lkm` están todas las funciones generales de módulos.
        '''
        self.ACCESOS_NOTAS = self.lkm.form_id('notas','id')
        self.BITACORA_ACCESOS = self.lkm.form_id('bitacora_de_entradas_y_salidas','id')
        self.BITACORA_OBJETOS_PERDIDOS = self.lkm.form_id('bitacora_objetos_perdidos','id')
        self.BITACORA_FALLAS = self.lkm.form_id('bitacora_de_fallas','id')
        self.BITACORA_INCIDENCIAS = self.lkm.form_id('bitacora_de_incidencias','id')
        self.BITACORA_GAFETES_LOCKERS = self.lkm.form_id('bitacora_de_gafetes_y_lockers','id')
        self.CARGA_PERMISOS_VISITANTES = self.lkm.form_id('carga_de_permisos_de_visitantes','id')
        self.CHECKIN_CASETAS = self.lkm.form_id('checkin_checkout_casetas','id')
        self.CONCESSIONED_ARTICULOS = self.lkm.form_id('concesion_de_activos_unico','id')
        self.CONF_PERFILES = self.lkm.form_id('configuracion_de_perfiles','id')
        self.PASE_ENTRADA = self.lkm.form_id('pase_de_entrada','id')
        self.PUESTOS_GUARDIAS = self.lkm.form_id('puestos_de_guardias','id')
        self.VISITA_AUTORIZADA = self.lkm.form_id('visita_autorizada','id')
        self.CONF_ACCESOS = self.lkm.form_id('configuracion_accesos','id')
        self.CONF_MODULO_SEGURIDAD = self.lkm.form_id('configuracion_modulo_seguridad','id')
        self.PAQUETERIA = self.lkm.form_id('paqueteria','id')

        self.last_check_in = []
        # self.FORM_ALTA_COLABORADORES = self.lkm.form_id('alta_de_colaboradores_visitantes','id')
        # self.FORM_ALTA_EQUIPOS = self.lkm.form_id('alta_de_equipos','id')
        # self.FORM_ALTA_VEHICULOS = self.lkm.form_id('alta_de_vehiculos','id')
        # self.FORM_BITACORA = self.lkm.form_id('bitacora','id')
        # self.FORM_LOCKER = self.lkm.form_id('locker','id')
        # self.FORM_PASE_DE_ENTRADA = self.lkm.form_id('pase_de_entrada','id')
        # self.FORM_REGISTRO_PERMISOS = self.lkm.form_id('registro_de_permisos','id')

        #--Variables 
        ### Catálogos ###
        '''
        Use `self.CATALOG_NAME = self.lkm.catalog_id('catalog_name',id)` ---> Aquí deberás guardar los `ID` de los catálogos. 
        Para ello deberás llamar el método `lkm.catalog_id` del objeto `lkm`(linkaform modules, por sus siglas).
        En `lkm` están todas las funciones generales de módulos).
        '''

        self.CONFIGURACION_GAFETES_LOCKERS = self.lkm.catalog_id('configuracion_de_gafetes_y_lockers')
        self.CONFIGURACION_GAFETES_LOCKERS_ID = self.CONFIGURACION_GAFETES_LOCKERS.get('id')
        self.CONFIGURACION_GAFETES_LOCKERS_OBJ_ID = self.CONFIGURACION_GAFETES_LOCKERS.get('obj_id')

        self.CONFIGURACION_RECORRIDOS = self.lkm.catalog_id('configuracion_de_recorridos')
        self.CONFIGURACION_RECORRIDOS_ID = self.CONFIGURACION_RECORRIDOS.get('id')
        self.CONFIGURACION_RECORRIDOS_OBJ_ID = self.CONFIGURACION_RECORRIDOS.get('obj_id')

        self.CONFIG_PERFILES = self.lkm.catalog_id('configuracion_de_perfiles')
        self.CONFIG_PERFILES_ID = self.CONFIG_PERFILES.get('id')
        self.CONFIG_PERFILES_OBJ_ID = self.CONFIG_PERFILES.get('obj_id')

        self.DEFINICION_PERMISOS = self.lkm.catalog_id('definicion_de_permisos')
        self.DEFINICION_PERMISOS_ID = self.DEFINICION_PERMISOS.get('id')
        self.DEFINICION_PERMISOS_OBJ_ID = self.DEFINICION_PERMISOS.get('obj_id')

        self.GAFETES_CAT = self.lkm.catalog_id('gafetes')
        self.GAFETES_CAT_ID = self.GAFETES_CAT.get('id')
        self.GAFETES_CAT_OBJ_ID = self.GAFETES_CAT.get('obj_id')

        self.LOCKERS_CAT = self.lkm.catalog_id('lockers')
        self.LOCKERS_CAT_ID = self.LOCKERS_CAT.get('id')
        self.LOCKERS_CAT_OBJ_ID = self.LOCKERS_CAT.get('obj_id')

        self.PERFILES = self.lkm.catalog_id('perfiles')
        self.PERFILES_ID = self.PERFILES.get('id')
        self.PERFILES_OBJ_ID = self.PERFILES.get('obj_id')

        self.PASE_ENTRADA_CAT = self.lkm.catalog_id('pase_de_entrada')
        self.PASE_ENTRADA_ID = self.PASE_ENTRADA_CAT.get('id')
        self.PASE_ENTRADA_OBJ_ID = self.PASE_ENTRADA_CAT.get('obj_id')

        self.TIPO_ARTICULOS_PERDIDOS_CAT = self.lkm.catalog_id('lista_de_objetos')
        self.TIPO_ARTICULOS_PERDIDOS_CAT_ID = self.TIPO_ARTICULOS_PERDIDOS_CAT.get('id')
        self.TIPO_ARTICULOS_PERDIDOS_CAT_OBJ_ID = self.TIPO_ARTICULOS_PERDIDOS_CAT.get('obj_id')
        
        self.VISITA_AUTORIZADA_CAT = self.lkm.catalog_id('visita_autorizada')
        self.VISITA_AUTORIZADA_CAT_ID = self.VISITA_AUTORIZADA_CAT.get('id')
        self.VISITA_AUTORIZADA_CAT_OBJ_ID = self.VISITA_AUTORIZADA_CAT.get('obj_id')

        self.LISTA_INCIDENCIAS_CAT = self.lkm.catalog_id('lista_de_incidentes')
        self.LISTA_INCIDENCIAS_CAT_ID = self.LISTA_INCIDENCIAS_CAT.get('id')
        self.LISTA_INCIDENCIAS_CAT_OBJ_ID = self.LISTA_INCIDENCIAS_CAT.get('obj_id')

        self.LISTA_INCIDENCIAS_CAT = self.lkm.catalog_id('lista_de_incidentes')
        self.LISTA_INCIDENCIAS_CAT_ID = self.LISTA_INCIDENCIAS_CAT.get('id')
        self.LISTA_INCIDENCIAS_CAT_OBJ_ID = self.LISTA_INCIDENCIAS_CAT.get('obj_id')

        self.LISTA_FALLAS_CAT = self.lkm.catalog_id('lista_de_fallas')
        self.LISTA_FALLAS_CAT_ID = self.LISTA_FALLAS_CAT.get('id')
        self.LISTA_FALLAS_CAT_OBJ_ID = self.LISTA_FALLAS_CAT.get('obj_id')

        self.GRUPOS_CAT = self.lkm.catalog_id('grupos')
        self.GRUPOS_CAT_ID = self.GRUPOS_CAT.get('id')
        self.GRUPOS_CAT_OBJ_ID = self.GRUPOS_CAT.get('obj_id')

        self.PROVEEDORES_CAT = self.lkm.catalog_id('proveedores')
        self.PROVEEDORES_CAT_ID = self.PROVEEDORES_CAT.get('id')
        self.PROVEEDORES_CAT_OBJ_ID = self.PROVEEDORES_CAT.get('obj_id')

        self.load(module='Employee', **self.kwargs)

        # self.CONF_PERFIL = self.lkm.catalog_id('configuracion_de_perfiles','id')
        # self.CONF_PERFIL_ID = self.CONF_PERFIL.get('id')
        # self.CONF_PERFIL_OBJ_ID = self.CONF_PERFIL.get('obj_id')


        # self.AREAS_DE_LAS_UBICACIONES_CAT = self.lkm.catalog_id('areas_de_las_ubicaciones')
        # self.AREAS_DE_LAS_UBICACIONES_CAT_ID = self.AREAS_DE_LAS_UBICACIONES_CAT.get('id')
        # self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID = self.AREAS_DE_LAS_UBICACIONES_CAT.get('obj_id')
        #----Dic Fields Forms

        ## Module Fields ##
        ''' 
        self.mf : Estos son los campos que deseas mantener solo dentro de este modulo.
        Asegúrese de utilizar `llave` y el `id` del campo ej.
        'nombre_campo': "1f2h3j4j5d6f7h8j9j1a",
        '''
        mf = {
            'articulo':'66ce2441d63bb7a3871adeaf',
            'areas_grupo':'663cf9d77500019d1359eb9f',
            'archivo_invitacion': '673773741b2adb2d05d99d63',
            #LOS CATALOGOS NO SE CCLASIFICAN COMO CAMPOS            
            'catalog_area_pase':'664fc5f3bbbef12ae61b15e9',
            'catalog_caseta':'66566d60d4619218b880cf04',
            'catalog_caseta_salida':'66566d60464fe63529d1c543',
            'catalog_estado':'664fc5b3276795e17ea76dbd',
            'catalog_guard':'664fc645276795e17ea76dc4',
            'catalog_guard_close':'664fc64242c59486fadd0a27',
            'catalog_tipo_pase':'664fc6e81d1a1fcda334b587',
            'catalog_ubicacion':'664fc5d9860deae4c20954e2',
            "catalogo_ubicaciones": "66a83a77cfed7f342775c161",
            'catalog_visita':'664fc6f5d6078682a4dd0ab3',
            'catalogo_persona_involucrada': '66ec6936fc1f0f3f111d818f',
            "catalogo_departamentos": "66a83a7fca3453e21ea08d16",
            "catalogo_puestos": "66a83a7dee0b950748489ca1",
            ##### REVISAR Y BORRAR ######

            'fecha_salida':'662c51eb194f1cb7a91e5af0',
            'fecha_entrada':'662c51eb194f1cb7a91e5aef',
            'comentario_pase':'65e0a69a322b61fbf9ed23af',
            'commentario_area': '66af1a77d703592958dca5eb',
            'color_vehiculo': '663e4691f54d395ed7f27465',
            'color_articulo': '663e4730724f688b3059eb3b',
            'codigo_qr':'6685da34f065523d8d09052b',
            'config_dias_acceso': '662c304fad7432d296d92585',
            'config_limitar_acceso': '6635380dc9b3e7db4d59eb49',
            'config_dia_de_acceso': '662c304fad7432d296d92584',
            'curp': '5ea0897550b8dfe1f4d83a9f',
            'departamento_empleado': '663bc4ed8a6b120eab4d7f1e',
            'dias_acceso_pase':'662c304fad7432d296d92585',
            'documento': '663e5470424ad55e32832eec',
            'documento_certificado': '66427511e93cc23f04f27467',
            'direccion': '663a7e0fe48382c5b1230902',
            'direccion_visita': '67466b79bd2dc53e9864ad62',
            'duracion': '65cbe03c6c78b071a59f481e',
            'email_empleado': '6653f3709c6d89925dc04b2f',
            'email_pase':'662c2937108836dec6d92581',
            'email_vista': '5ea069562f8250acf7d83aca',
            'empresa':'65fc814fb170488cf4d44c51',
            'empresa_pase':'66357d5e4f00f9018ce97ce9',
            'examen_certificado':'66297e1579900d9018c886ad',
            'fecha_hasta_pase':'662c304fad7432d296d92583',
            'fecha_desde_visita': '662c304fad7432d296d92582',
            'fecha_desde_hasta': '662c304fad7432d296d92583',
            'fecha_cetrificado_expedicion': '66427511e93cc23f04f27469',
            'fecha_cetrificado_caducidad': '66427511e93cc23f04f2746a',
            'field_note':'6647fadc96f80017ac388648',
            'foto':'5ea35de83ab7dad56c66e045',
            'status_gafete':'663e530af52d352956832f72',
            'status_locker':'663961d5390b9ec511e97ca5',
            'grupo_equipos':'663e446cadf967542759ebbb',
            'grupo_areas_acceso':'663fed6cb8262fd454326cb3',
            'grupo_instrucciones_pase':'65e0a68a06799422eded24aa',
            'guard_group':'663fae53fa005c70de59eb95',
            "grupo_puestos": "663c015f3ac46d98e8f27495",
            'grupo_visitados': '663d4ba61b14fab90559ebb0',
            'grupo_vehiculos': '663e446cadf967542759ebba',
            'grupo_ubicaciones_pase':'6834e34fa6242006acedda0f',
            'identificacion':'65ce34985fa9df3dbf9dd2d0',
            'id_grupo':'639b65dfaf316bacfc551ba2',
            'id_usuario':'638a9a99616398d2e392a9f5',
            'locker_id':'66480101786e8cdb66e70124',
            'marca_vehiculo':'65f22098d1dc5e0b9529e89b',
            'marca_articulo':'663e4730724f688b3059eb3a',
            'modelo_articulo':'66b29872aa6b3e6c3c02baa6',
            'modelo_vehiculo':'65f22098d1dc5e0b9529e89c',
            'motivo':'66ad58a3a5515ee3174f2bb5',
            'nombre_pase':'662c2937108836dec6d92580',
            'nota': '6647fadc96f80017ac388647',
            'nombre_area':'663e5d44f5b8a7ce8211ed0f',
            'nombre_area_salida':'663fb45992f2c5afcfe97ca8',
            'nombre_ubicacion_salida': '663e5c57f5b8a7ce8211ed0b',
            'nombre_articulo': '663e4730724f688b3059eb39',
            'nombre_estado': '663a7dd6e48382c5b12308ff',
            'nombre_empleado': '62c5ff407febce07043024dd',
            'nombre_guardia_apoyo': '663bd36eb19b7fb7d9e97ccb',
            'nombre_grupo':'638a9ab3616398d2e392a9fa',
            'nombre_perfil': '661dc67e901906b7e9b73bac',
            'nombre_permiso':'662962bb203407ab90c886e4',
            'numero_serie': '66426453f076652427832fd2',
            'nombre_visita': '5ea0693a0c12d5a8e43d37df',
            'nombre_pase':'662c2937108836dec6d92580',
            'nombre_usuario':'638a9a7767c332f5d459fc81',
            'nss': '67466b79bd2dc53e9864ad63',
            'placas_vehiculo':'663e4691f54d395ed7f27464',
            'puesto_empleado': '663bc4c79b8046ce89e97cf4',
            'qr_pase':'64ef5b5fff1bec97d2ca27b6',
            'requerimientos':'662962bb203407ab90c886e5',
            'rfc':'64ecc95271803179d68ee081',
            'status_area':'663e5e4bf5b8a7ce8211ed14',
            'status_doc_cetrificado':'664275e32c12468d16cb97dc',
            'status_cetrificado':'664275469d8fffff0a59eb30',
            'status_visita':'5ea1bd280ae8bad095055e61',
            'telefono_pase':'662c2937108836dec6d92582',
            'telefono':'661ea59c15baf5666f32360e',
            'telefono_visita': '663ec042713049de31e97c93',
            'tipo_de_articulo_perdido':'66ce23efc5c4d148311adf86',
            'tipo_de_comentario':'66af1977ffb6fd75e769f457',
            'tipo_de_guardia': '6684484fa5fd62946c12e006',
            'tipo_equipo': '663e4730724f688b3059eb38',
            'tipo_locker': '66ccfec6acaa16b31e5593a3',
            'tipo_registro': '66358a5e50e5c61267832f90',
            #'tipo_equipo':'6639a9d9d38959539f59eb9f',
            'tipo_vehiculo': '65f22098d1dc5e0b9529e89a',
            'tipo_visita_pase': '662c304fad7432d296d92581',
            'ubicacion': '663e5c57f5b8a7ce8211ed0b',
            'user_id_empleado': '663bd32d7fb8869bbc4d7f7b',
            'vigencia_certificado':'662962bb203407ab90c886e6',
            'vigencia_certificado_en':'662962bb203407ab90c886e7',
            'walkin':'66c4261351cc14058b020d48',
            'email_visita_a': '638a9a7767c332f5d459fc82',
            'telefono_visita_a': '67be0c43a31e5161c47f2bba',
            'acepto_aviso_privacidad': '6825268e0663cce4b1bf0a17',
            'acepto_aviso_datos_personales': '6827488724317731cb288117',
            'conservar_datos_por': '6827488724317731cb288118'
        }
        self.mf = mf
        ## Form Fields ##
        '''
        `self.form_name`: En esta sección podrás agrupar todos los campos ya sea por forma o como desees enviarlos hacia tus servicios. 
        En el caso de las búsquedas de Mongo, puedes hacer las búsquedas de manera anidada. Por lo cual podrás agrupar separadas por punto,
        ej. 663d4ba61b14fab90559ebb0.665f482cc9a2f8acf685c20b y así podrás hacer las búsquedas directo en la base de datos.

        Estos campos podrás agregarlos directamente a `self.f`, donde se agrupan todos los `fields` de los módulos heredados.
        '''
        #- Para salida de bitacora  de articulos perdidos y lista
        self.perdidos_fields = {
            'estatus_perdido':'6639ae65356a6efb4de97d28',
            'date_hallazgo_perdido':'6639ae65356a6efb4de97d29',
            'ubicacion_catalog':f"{self.AREAS_DE_LAS_UBICACIONES_SALIDA_OBJ_ID}",
            'ubicacion_perdido':f"{self.mf['ubicacion']}",
            'area_catalog':f"{self.AREAS_DE_LAS_UBICACIONES_SALIDA_OBJ_ID}",
            'area_perdido':f"{self.mf['nombre_area_salida']}",
            'color_perdido':'66ce223e174f3f39c0020d65',
            'articulo_perdido':'6639aeeb97b12e6f4ccb9711',
            'tipo_articulo_catalog':f"{self.TIPO_ARTICULOS_PERDIDOS_CAT_OBJ_ID}",
            'tipo_articulo_perdido':f"{self.mf['tipo_de_articulo_perdido']}",
            'articulo_seleccion_catalog':f"{self.TIPO_ARTICULOS_PERDIDOS_CAT_OBJ_ID}",
            'articulo_seleccion': f"{self.mf['articulo']}",
            'foto_perdido':'6639aeeb97b12e6f4ccb9712',
            'descripcion':'66ce2397c5c4d148311adf83',
            'comentario_perdido':'6639affa5a9f58f5b5cb9706',
            'quien_entrega_catalog':f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}",
            'quien_entrega_interno':f"{self.f['worker_name']}",
            'quien_entrega':'66ce2646033c793281b2c414',
            #'quien_entrega_interno':f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_name']}",
            'quien_entrega_externo':'66ce2647033c793281b2c415',
            'recibe_perdido':'6639affa5a9f58f5b5cb9707',
            'telefono_recibe_perdido':'664415ce630b1fb22b07e159',
            'identificacion_recibe_perdido':'664415ce630b1fb22b07e15a',
            'foto_recibe_perdido':'66ce2675293aabefa3559486',
            'date_entrega_perdido':'6639affa5a9f58f5b5cb9708',
            'locker_catalog':f"{self.LOCKERS_CAT_OBJ_ID}",
            'locker_perdido':f"{self.mf['locker_id']}"
        }

        #- Para salida de bitacora y lista
        self.bitacora_fields = {
            "pase_entrada": f"{self.PASE_ENTRADA_OBJ_ID}",
            'fecha_salida':f"{self.mf['fecha_salida']}",
            'fecha_entrada':f"{self.mf['fecha_entrada']}",
            'caseta_entrada':f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.mf['nombre_area']}",
            'caseta_salida':f"{self.AREAS_DE_LAS_UBICACIONES_SALIDA_OBJ_ID}.{self.mf['nombre_area_salida']}",
            'codigo_qr':f"{self.mf['codigo_qr']}",
            'documento':f"{self.mf['documento']}",
            'comentario':"66ba83cc079d8a54634711c1",
            'status_gafete':f"{self.mf['status_gafete']}",
            'grupo_comentario':"66ba83942fef3a4613a07e91",
            'nombre_visita':f"{self.mf['catalog_visita']}.{self.mf['nombre_visita']}",
            'nombre_area_salida':f"{self.mf['catalog_caseta_salida']}.{self.mf['nombre_area_salida']}",
            'perfil_visita':f"{self.mf['catalog_visita']}.{self.mf['nombre_perfil']}",
            'status_visita':f"{self.mf['tipo_registro']}",
            'tipo_comentario':"66ba83cc079d8a54634711c2",
            'ubicacion':f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.mf['ubicacion']}",
            'visita_a':"663d4ba61b14fab90559ebb0",
            'visita':f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}",
            'visita_nombre_empleado': f"{self.mf['nombre_empleado']}",
            'visita_user_id_empleado':f"{self.mf['user_id_empleado']}",
            'visita_departamento_empleado': f"{self.mf['departamento_empleado']}",
            'puesto_empleado': f"{self.mf['puesto_empleado']}",
            'email_empleado': f"{self.mf['email_empleado']}",
            "catalogo_pase_entrada": "66a83ad652d2643c97489d31",
            "gafete_catalog": "66a83ace56d1e741159ce114",
        }
        self.checkin_fields = {
            'boot_checkin_date':'663bffc28d00553254f274e1',
            'boot_checkout_date':'663bffc28d00553254f274e2',
            'commentario_checkin_caseta':'66a5b9bed0c44910177eb724',
            'checkin_status':'66a28f3ca6b0f085b1518ca8',
            'checkin_date':'66a28f3ca6b0f085b1518caa',
            'checkout_date':'66a28f3ca6b0f085b1518cab',
            'checkin_type': '663bffc28d00553254f274e0',
            'checkin_position':'66a28f3ca6b0f085b1518ca9',
            'forzar_cierre':'66a5b9bed0c44910177eb723',
            'guard_group': mf['guard_group'],
            'checkin_image': '685ac4e836c1c936b97275ad',
            'employee_position':'665f482cc9a2f8acf685c20b',
            'cat_created_by': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_name']}",
            'created_by': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_name']}",
            'employee': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_name']}",
            'cat_location': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['location']}",
            'cat_area': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['area']}",
            'cat_employee_b': f"{self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID}.{self.f['worker_name_b']}",
        }
        #- Para salida de bitacora  de articulos consecionados y lista
        self.consecionados_fields = {
            'status_concesion':'66469e193e6a703350f2e029',
            'ubicacion_catalog_concesion': f"{self.UBICACIONES_CAT_OBJ_ID}",
            'ubicacion_concesion':f"{self.UBICACIONES_CAT_OBJ_ID}.{self.mf['ubicacion']}",
            'solicita_concesion':'66469e5a3e6a703350f2e03a',
            'persona_catalog_concesion':f"{self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID}",
            'persona_nombre_concesion':f"{self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID}.{self.mf['nombre_guardia_apoyo']}",
            'area_catalog_concesion':f"{self.AREAS_DE_LAS_UBICACIONES_SALIDA_OBJ_ID}",
            'caseta_concesion':f"{self.AREAS_DE_LAS_UBICACIONES_SALIDA_OBJ_ID}.{self.mf['nombre_area_salida']}",
            'fecha_concesion':'66469ef8c9d58517f85d035f',
            'equipo_catalog_concesion':f"{self.ACTIVOS_FIJOS_CAT_OBJ_ID}",
            'equipo_imagen_concesion':'6646393c3fa8b818265d0326',
            'area_concesion':'663e5d44f5b8a7ce8211ed0f',
            'equipo_concesion':'6646373dda020fe797cafa20',
            'observacion_concesion':'66469f47c0580e5ead07e39a',
            'fecha_devolucion_concesion':'66469f47c0580e5ead07e39b',
        }
        #- Para creación , edición y lista de fallas
        self.fallas_fields = {
            'falla_estatus': '66397e2c59c2600b1df2742c',
            'falla_fecha_hora': '66397d0cfd99d7263f833032',
            'falla_reporta_catalog':f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}",
            'falla_reporta_nombre': '62c5ff407febce07043024dd',
            'falla_reporta_departamento': '663bc4ed8a6b120eab4d7f1e',
            'falla_ubicacion_catalog':f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}",
            'falla_ubicacion': f"{self.mf['ubicacion']}",
            'falla_caseta':f"{self.mf['nombre_area']}",
            'falla_catalog': f"{self.LISTA_FALLAS_CAT_OBJ_ID}",
            'falla':'66397bae9e8b08289a59ec86',
            'falla_objeto_afectado':'66ce2441d63bb7a3871adeaf',
            'falla_comentarios':'66397d8cfd99d7263f83303a',
            'falla_evidencia':'66f2df6b6917fe63f4233226',
            'falla_documento':'66f2df6b6917fe63f4233227',
            'falla_responsable_solucionar_catalog': f"{self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID}",
            'falla_responsable_solucionar_nombre':'663bd36eb19b7fb7d9e97ccb',
            'falla_responsable_solucionar_documento':'663bc4ed8a6b120eab4d7f1e',
            'falla_comentario_solucion':'66f2dfb2c80d24e5e82332b3',
            'falla_folio_accion_correctiva':'66f2dfb2c80d24e5e82332b4',
            'falla_grupo_seguimiento': '6799125d9f8d78842caa22af',
            'falla_inicio_seguimiento': '679a485c66c5d089fa6b8ef9',
            'falla_fin_seguimiento': '679a485c66c5d089fa6b8efa',
            'falla_evidencia_solucion':'66f2dfb2c80d24e5e82332b5',
            'falla_documento_solucion':'66f2dfb2c80d24e5e82332b6',
            'falla_fecha_hora_solucion':'66fae1f1d4e5e97eb12170ef',
            'falla_subconcepto': '679124a8483c5220455bcb99'
        }
        #- Para creación , edición y lista de incidencias
        self.incidence_fields = {
            'reporta_incidencia_catalog': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}", 
            'reporta_incidencia': '62c5ff407febce07043024dd',
            'fecha_hora_incidencia': '66396efeb37283c921e97cdf',
            'ubicacion_incidencia_catalog': f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}",
            'ubicacion_incidencia': f"{self.mf['ubicacion']}",
            'area_incidencia_catalog': f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}",
            'area_incidencia': '663e5d44f5b8a7ce8211ed0f',
            'incidencia_catalog': f"{self.LISTA_INCIDENCIAS_CAT_OBJ_ID}",
            'incidencia': '663973809fa65cafa759eb97',
            'tipo_incidencia': '66ec667d7646541f2ea024de',
            'comentario_incidencia': '66397586aa8bbc0371e97c80',
            'tipo_dano_incidencia': '66ec6962ea3c921534b22c54',
            'dano_incidencia':'66ec69144a27bb6151a0255a',
            'personas_involucradas_incidencia':'66ec69144a27bb6151a0255b',
            'acciones_tomadas_incidencia':'66ec6987f251a9c2cef0126f',
            'evidencia_incidencia':'66ec6846028e5550cbf012e0',
            'documento_incidencia':'66ec6846028e5550cbf012e1',
            'prioridad_incidencia':'66ec69144a27bb6151a0255c',
            'notificacion_incidencia':'66ec6ae6c17763d760218e5e',
            'tipo_persona': '66ec6936fc1f0f3f111d818f',
            'responsable_accion':'66ec69a914bf1142b6a024e2',
            'acciones_tomadas':'66ec69a914bf1142b6a024e3',
            'area_incidencia_ver2':f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.mf['nombre_area']}",
            'total_deposito_incidencia':'66ec6821ea3c921534b22c30',
            'datos_deposito_incidencia':'66ec6793eb386ff970218f1f',
            'tipo_deposito': '66ec67dc608b1faed7b22c45',
            'cantidad':'66ec67e42bcc75c3a458778e',
            'tags':'6834e4e8b0ed467efade7972',
            'tag':'6834e5220bacdbe44ede794f',
            'grupo_seguimiento_incidencia': '683de3cfcf4a5d248ffbaf89',
            # 'accion_correctiva_incidencia': '683de45ddcf6fcee78e61ed7',
            # 'comentario_accion_correctiva_incidencia': '683de45ddcf6fcee78e61ed8',
            # 'fecha_inicio_accion_correctiva_incidencia': '683de45ddcf6fcee78e61ed9',
            # 'fecha_fin_accion_correctiva_incidencia': '683de45ddcf6fcee78e61eda',
            # 'evidencia_accion_correctiva_incidencia': '683de45ddcf6fcee78e61edb',
            # 'documento_accion_correctiva_incidencia': '683de45ddcf6fcee78e61edc',

            'categoria':'6848893f4f18021ab10c6a12',
            'sub_categoria': '68488a6c5cf05798e09f3eec',
            'incidente':'663973809fa65cafa759eb97',
            #Persona extraviada
            'nombre_completo_persona_extraviada':'684c3e026d974f9625e11303',
            'edad':'684c3e026d974f9625e11304',
            'color_piel':'684c3e026d974f9625e11305',
            'color_cabello': '684c3e026d974f9625e11306',
            'estatura_aproximada': '684c3e026d974f9625e11307',
            'descripcion_fisica_vestimenta': '684c3e026d974f9625e11308',
            'nombre_completo_responsable': '684c3e026d974f9625e11309',
            'parentesco': '684c3e026d974f9625e1130a',
            'num_doc_identidad': '684c3e026d974f9625e1130b',
            'telefono': '684c3e026d974f9625e1130c',
            'info_coincide_con_videos': '684c3e026d974f9625e1130d',
            'responsable_que_entrega': '684c3e026d974f9625e1130e',
            'responsable_que_recibe': '684c3e026d974f9625e1130f',
            #Robo de cableado
            'valor_estimado': '684c3e6821796d7880117f22',
            'pertenencias_sustraidas': '684c3e6821796d7880117f23',
            #Robo de vehiculo
            'placas': '684c3eaa04aaab135d7dfbb3',
            'tipo': '684c3eaa04aaab135d7dfbb2',
            'marca': '684c3eaa04aaab135d7dfbb4',
            'modelo': '684c3eaa04aaab135d7dfbb5',
            'color': '684c3eaa04aaab135d7dfbb6',

            #Grupos Repetitivos
            'personas_involucradas_incidencia':'66ec69144a27bb6151a0255b',
            'acciones_tomadas_incidencia':'66ec6987f251a9c2cef0126f',
            'seguimientos_incidencia':'683de3cfcf4a5d248ffbaf89',
            'afectacion_patrimonial_incidencia':'689a939e0365c9bf344fb108',

            #Campos en grupo repetitivo Seguimiento:
            'accion_correctiva_incidencia':'683de45ddcf6fcee78e61ed7',
            'incidencia_personas_involucradas':'689a94e0fdddc884ad49be1b',
            'fecha_inicio_seg':'683de45ddcf6fcee78e61ed9',
            'incidencia_documento_solucion':'683de45ddcf6fcee78e61edc',
            'incidencia_evidencia_solucion':'683de45ddcf6fcee78e61edb',
            #Campos en grupo repetid    ivo personas involucradas:
            'nombre_completo': '66ec69239938c882f8222036',
            'rol':'689a92f436426ef5290121a6',
            'sexo':'689a92f436426ef5290121a7',
            'grupo_etario':'689a92f436426ef5290121a8',
            'atencion_medica':'689a92f436426ef5290121a9',
            'retenido':'689a92f436426ef5290121aa',
            'comentarios':'689a92f436426ef5290121ab',
            #Campos en grupo repetitivo acciones tomadas:
            'acciones_tomadas': '66ec69a914bf1142b6a024e3',
            'llamo_a_policia': '689a9380fa74370bb5546070',
            'autoridad': '66ec69a914bf1142b6a024e2',
            'numero_folio_referencia': '689a9380fa74370bb5546071',
            'responsable': '689a9380fa74370bb5546072',
            #Campos en grupo repetitivo afectacion patrimonial:
            'tipo_afectacion': '689a9f297a657196d50121b5',
            'monto_estimado': '689a940357ae87d51a393878',
            'duracion_estimada': '689a940357ae87d51a393879',
        }
        #- Para creación , edición y lista de gafetes y lockers
        self.gafetes_fields = {
            'caseta_gafete':f"{self.UBICACIONES_CAT_OBJ_ID}.{self.mf['nombre_area']}",
            'documento_gafete':'65e0b6f7a07a72e587124dc6',
            'gafete_id':'664803e6d79bc1dfd33885e1',
            'catalog_gafete':'664fc6ec8d4dfb34de095586',
            'ubicacion_gafete':f"{self.UBICACIONES_CAT_OBJ_ID}.{self.mf['ubicacion']}",
            'visita_gafete':f"{self.mf['catalog_visita']}.{self.mf['nombre_visita']}",
        }
        self.lockers_fields = {
            'locker_id':'66480101786e8cdb66e70124',
            'tipo_locker':'66ccfec6acaa16b31e5593a3',
            'status_locker':"663961d5390b9ec511e97ca5",
        }
        #- Para creación , edición y lista de notas
        self.notes_fields = {
            'note_status':'6647f9eb6eefdb1840684dc1',
            'note_open_date':'6647fadc96f80017ac388646',
            'note_close_date':'6647fadc96f80017ac38864a',
            'note_catalog_booth':f"{self.UBICACIONES_CAT_OBJ_ID}",
            'note_booth':f"{self.mf['nombre_area']}",
            'note_catalog_guard':f"{self.mf['catalog_guard']}",
            'note_guard':f"{self.mf['nombre_empleado']}",
            'note_catalog_guard_close':f"{self.mf['catalog_guard_close']}",
            'note_guard_close':f"{self.mf['nombre_guardia_apoyo']}",
            'note':'6647fadc96f80017ac388647',
            'note_file':'6647fadc96f80017ac388648',
            'note_pic':'6647fadc96f80017ac388649',
            'note_comments_group':'6647fb1874c1a87eb02a9037',
            'note_comments':'6647fb38da07bf430e273ea2',
        }
        self.notes_project_fields = {
            'location': f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['location']}",
            'area': f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['area']}",
            'created_by': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_name']}",
            'closed_by': f"{self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID}.{self.f['worker_name_b']}",
            'support_guard':f"{self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID}.{self.f['worker_name_b']}",
        }
        self.pase_entrada_fields = {
            'area':f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}",
            'grupo_areas_acceso':'663fed6cb8262fd454326cb3',
            'comentario_pase':'65e0a69a322b61fbf9ed23af',
            'commentario_area':"66af1a77d703592958dca5eb",
            'catalog_area_pase':'664fc5f3bbbef12ae61b15e9',
            'catalogo_visitante_registrado': '66a83ad456d1e741159ce118',
            'curp_catalog_pase':f"{self.PASE_ENTRADA_OBJ_ID}.{self.mf['curp']}",
            'nombre_permiso':f"{self.CONFIG_PERFILES_OBJ_ID}.662962bb203407ab90c886e4",
            'email_catalog_pase':f"{self.PASE_ENTRADA_OBJ_ID}.{self.mf['email_vista']}",
            'empresa_pase':f"{self.PASE_ENTRADA_OBJ_ID}.{self.mf['empresa']}",
            'email':'662c2937108836dec6d92581',
            'nombre':'662c2937108836dec6d92580',
            'direccion_pase':f"{self.mf['catalog_ubicacion']}.{self.mf['direccion']}",
            'foto_pase':f"{self.PASE_ENTRADA_OBJ_ID}.{self.mf['foto']}",
            'foto_pase_id':f"{self.mf['foto']}",
            'identificacion_pase':f"{self.PASE_ENTRADA_OBJ_ID}.{self.mf['identificacion']}",
            'identificacion_pase_id':f"{self.mf['identificacion']}",
            'archivo_invitacion': '673773741b2adb2d05d99d63',
            'motivo':f"{self.CONFIG_PERFILES_OBJ_ID}.{self.mf['motivo']}",
            'nombre_area':f"{self.mf['nombre_area']}",
            'nombre_catalog_pase':f"{self.PASE_ENTRADA_OBJ_ID}.{self.mf['nombre_visita']}",
            'nombre_tipo_pase':f"{self.CONFIG_PERFILES_OBJ_ID}.66297e1579900d9018c886ad",
            'nombre_perfil':f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_name']}",
            'nombre_visitante_registrado': '5ea0693a0c12d5a8e43d37df',
            'pdf_to_img': '682222d27e0ea505751e17b4',
            'perfil_pase':f"{self.CONFIG_PERFILES_OBJ_ID}.661dc67e901906b7e9b73bac",
            'perfil_pase_id':f"661dc67e901906b7e9b73bac",
            'requerimientos_pase':f"{self.CONFIG_PERFILES_OBJ_ID}.662962bb203407ab90c886e5",
            'status_pase':'66353daa223b8a43d7f274b5',
            'status_visita_pase':f"{self.PASE_ENTRADA_OBJ_ID}.{self.mf['status_visita']}",
            'telefono_catalog_pase':f"{self.PASE_ENTRADA_OBJ_ID}.{self.mf['telefono']}",
            'ubicacion_pase':f"{self.mf['catalog_ubicacion']}.{self.mf['ubicacion']}",
            'email_pase':'662c2937108836dec6d92581',
            'empresa_pase':'66357d5e4f00f9018ce97ce9',
            'grupo_equipos':'663e446cadf967542759ebbb',
            'google_wallet_pass_url': '6820df5a6cfcee960fb4275c',
            'apple_wallet_pass': '682785fbedd82a9104287e25',
            'fecha_hasta_pase':'662c304fad7432d296d92583',
            'grupo_instrucciones_pase':'65e0a68a06799422eded24aa',
            'nombre_pase':'662c2937108836dec6d92580',
            'qr_pase':'64ef5b5fff1bec97d2ca27b6',
            'telefono_pase':'662c2937108836dec6d92582',
            'tipo_visita':"662c262cace163ca3ed3bb3a",
            'tipo_comentario':'66af1977ffb6fd75e769f457',
            'visita_a':'663d4ba61b14fab90559ebb0',
            'conf_perfiles':f"{self.CONFIG_PERFILES_OBJ_ID}",
            'vigencia_pase':f"{self.CONFIG_PERFILES_OBJ_ID}.'662962bb203407ab90c886e6",
            'vigencia_expresa_pase':f"{self.CONFIG_PERFILES_OBJ_ID}.662962bb203407ab90c886e7",
            'worker_department': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_department']}",
            'walkin_email':'662c2937108836dec6d92581',
            'walkin_empresa':'66357d5e4f00f9018ce97ce9',
            'walkin_fotografia':'66c4d5b6d1095c4ce8b2c42a',
            'walkin_identificacion':'66c4d5b6d1095c4ce8b2c42b',
            'walkin_nombre':'662c2937108836dec6d92580',
            'walkin_telefono':'662c2937108836dec6d92582',
            'worker_position':   f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_position']}",    
            'favoritos':'674642e2d53ce9476994dd89',  
            'acepto_aviso_privacidad': '6825268e0663cce4b1bf0a17',
            'acepto_aviso_datos_personales': '6827488724317731cb288117',
            'conservar_datos_por': '6827488724317731cb288118',
            'ubicaciones':'6834e34fa6242006acedda0f'
        }
        self.pase_grupo_visitados:{
        }
        # self.pase_entrada_fields.update(self.pase_grupo_visitados)
        self.pase_grupo_areas:{
            'nombre_perfil':     f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['area']}",
        }
        # self.pase_entrada_fields.update(self.pase_grupo_areas)
        self.pase_grupo_vehiculos:{
            'nombre_perfil':     f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['area']}",
            'tipo_vehiuclo':   f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_position']}",        
        }
        # self.pase_entrada_fields.update(self.pase_grupo_vehiculos)
        self.pase_entrada_fields.update({
            'ubicacion_cat': f"{self.UBICACIONES_CAT_OBJ_ID}",
            'ubicacion_nombre':self.mf['ubicacion'],
            'ubicacion': f"{self.UBICACIONES_CAT_OBJ_ID}.{self.f['location']}",
            'nombre_visita': f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{mf['nombre_visita']}",
            'email_vista': f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{self.mf['email_vista']}",
            'curp': self.unlist(f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{mf['curp']}"),
            'rfc': f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{mf['rfc']}",
            'telefono': f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{mf['telefono']}",
            'foto': f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{mf['foto']}",
            'identificacion': f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{mf['identificacion']}",
            'empresa': f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{mf['empresa']}",
            'status_visita': f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{mf['status_visita']}",
            'nombre_perfil': f"{self.CONFIG_PERFILES_OBJ_ID}.{mf['nombre_perfil']}",
            #'nombre_perfil': f"{self.mf['grupo_visitados']}{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_name']}",
            'worker_department': f"{self.mf['grupo_visitados']}{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_department']}",
            'worker_position': f"{self.mf['grupo_visitados']}{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_position']}",
            'catalago_autorizado_por': f"{self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID}",
            'autorizado_por': self.mf['nombre_guardia_apoyo'],
            'tipo_visita_pase': self.mf['tipo_visita_pase'],
            'grupo_visitados': self.mf['grupo_visitados'],
            'fecha_desde_visita': self.mf['fecha_desde_visita'],
            'fecha_desde_hasta': self.mf['fecha_desde_hasta'],
            'config_dia_de_acceso': self.mf['config_dia_de_acceso'],
            'config_limitar_acceso': self.mf['config_limitar_acceso'],
            'config_dias_acceso': self.mf['config_dias_acceso'],
            'area_catalog_normal':  f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}",
            'area_catalog':  f"{self.AREAS_DE_LAS_UBICACIONES_SALIDA_OBJ_ID}",
            'area': '663fb45992f2c5afcfe97ca8',
            'tema_cita':'67329875978e6460083c5648',
            'descripcion': '67329875978e6460083c5649',
            'link':'6732aa1189fc6b0ae27e3824',
            'enviar_correo':'6732a153496e3b26d18e7ee1',
            'enviar_correo_pre_registro':'6734c6d5254e9a61df8e7f51',
            'created_by': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_name']}",
            'comentario_area_pase':self.mf['commentario_area'],
            'ubicaciones': '6834e34fa6242006acedda0f'
        })

        self.conf_accesos_fields = {
            'usuario_cat':  f"{self.EMPLOYEE_OBJ_ID}",
            'grupos':f"{self.GRUPOS_CAT_OBJ_ID}",
            'menus':"6722472f162366c38ebe1c64",
        }

        self.conf_modulo_seguridad = {
            'ubicacion_cat':  f"{self.UBICACIONES_CAT_OBJ_ID}",
            'ubicacion':"663e5c57f5b8a7ce8211ed0b",
            'grupo_requisitos':"676975321df93a68a609f9ce",
            'datos_requeridos':"6769756fc728a0b63b8431ea",
            'envio_por':"6810180169eeaca9517baa5b",
        }

        self.paquetes_fields = {
            'ubicacion_paqueteria':f"{self.UBICACIONES_CAT_OBJ_ID}.{self.mf['ubicacion']}",
            'area_paqueteria':f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.mf['nombre_area']}",
            'fotografia_paqueteria': "67e46624da3191c5ef4ab6d0",
            'descripcion_paqueteria':"67e4652619b4be1c5a76a485",
            'quien_recibe_cat': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}",
            'quien_recibe_paqueteria':f"{self.mf['nombre_empleado']}",
            'guardado_en_paqueteria': f"{self.LOCKERS_CAT_OBJ_ID}.{self.mf['locker_id']}",
            'fecha_recibido_paqueteria': '67e4652619b4be1c5a76a486',
            'fecha_entregado_paqueteria': '67e4652619b4be1c5a76a487',
            'estatus_paqueteria': '67e4652619b4be1c5a76a488',
            'entregado_a_paqueteria':'67e4652619b4be1c5a76a489',
            'proveedor_cat':f"{self.PROVEEDORES_CAT_OBJ_ID}",
            'proveedor':'667468e3e577b8b98c852aaa',
        }

        self.notes_project_fields.update(self.notes_fields)
        self.bitacora_acceos = {}
        ## Fields ##
        '''
        `self.f`: En esta variable "fields", se almacenan todos los campos de todos los módulos heredados.
        El orden de reemplazo se ve afectado por el orden en que se hereda cada módulo. El orden que se otorga, es considerando
        que la variable se iguala en la base, y se va armando en tren de dependencias ej.

            Class A:
            Class B(A):
            Class C(B):
            Class D(C):

            x_obj = D()
            el orden de herencia será, primero carga A > B > C > D.
        '''

        self.f.update(self.notes_fields)
        self.f.update(self.checkin_fields)
        self.f.update({
            'duracion_rondin':'6639b47565d8e5c06fe97cf3',
            'duracion_traslado_area':'6760a9581e31b10a38a22f1f',
            'fecha_inspeccion_area':'6760a908a43b1b0e41abad6b',
            'fecha_programacion':'6760a8e68cef14ecd7f8b6fe',
            'fecha_inicio_rondin':'6818ea068a7f3446f1bae3b3',
            'grupo_areas_visitadas':'66462aa5d4a4af2eea07e0d1',
        })

    '''
    funciones internas: son funciones que solo se pueden mandar llamar dentro de este archivo. Si se hereda la clase
    esta función no puede ser invocada.

    pep-0008:
        _single_leading_underscore: 
        weak “internal use” indicator. E.g. from M import * does not import objects whose names start with an underscore.
    '''

    def _do_access(self, access_pass, location, area, data):
        '''
        Registra el acceso del pase de entrada a ubicación.
        solo puede ser ejecutado después de revisar los accesos
        '''
        employee =  self.get_employee_data(email=self.user.get('email'), get_one=True)
        metadata = self.lkf_api.get_metadata(form_id=self.BITACORA_ACCESOS)
        metadata.update({
            'properties': {
                "device_properties":{
                    "System": "Script",
                    "Module": "Accesos",
                    "Process": "Ingreso de Personal",
                    "Action": 'Do Access',
                    "File": "accesos/app.py"
                }
            },
        })
        # metadata['folio'] = self.create_poruction_lot_number()

        try:
            pase = {
                    f"{self.mf['nombre_visita']}": access_pass['nombre'],
                    f"{self.mf['curp']}":access_pass['curp'],
                    ### Campos Select
                    f"{self.mf['empresa']}":[access_pass.get('empresa'),],
                    f"{self.pase_entrada_fields['perfil_pase_id']}": [access_pass['tipo_de_pase'],],
                    # f"{self.pase_entrada_fields['status_pase']}":[access_pass['estatus'],],
                    f"{self.pase_entrada_fields['status_pase']}":['Activo',],
                    f"{self.pase_entrada_fields['foto_pase_id']}": access_pass.get("foto",[]), #[access_pass['foto'],], #.get('foto','')
                    f"{self.pase_entrada_fields['identificacion_pase_id']}": access_pass.get("identificacion",[]) #[access_pass['identificacion'],], #.get('identificacion','')
                    }
        except Exception as e:
            self.LKFException({"msg":f"Error al crear registro ingreso, no se encontro: {e}"}) 

        answers = {
            f"{self.mf['tipo_registro']}": 'entrada',
            f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}":{
                f"{self.f['location']}":location,
                f"{self.f['area']}":area
                },
            f"{self.PASE_ENTRADA_OBJ_ID}":pase,
            f"{self.mf['codigo_qr']}": str(access_pass['_id']),
            f"{self.mf['fecha_entrada']}":self.today_str(employee.get('timezone', 'America/Monterrey'), date_format='datetime'),
        }
        vehiculos = data.get('vehiculo',[])
        if vehiculos:
            list_vehiculos = []
            for item in vehiculos:
                if item:
                    tipo = item.get('tipo','')
                    marca = item.get('marca','')
                    modelo = item.get('modelo','')
                    estado = item.get('estado','')
                    placas = item.get('placas','')
                    color = item.get('color','')
                    list_vehiculos.append({
                        self.TIPO_DE_VEHICULO_OBJ_ID:{
                            self.mf['tipo_vehiculo']:tipo,
                            self.mf['marca_vehiculo']:marca,
                            self.mf['modelo_vehiculo']:modelo,
                        },
                        self.ESTADO_OBJ_ID:{
                            self.mf['nombre_estado']:estado,
                        },
                        self.mf['placas_vehiculo']:placas,
                        self.mf['color_vehiculo']:color,
                    })
            answers[self.mf['grupo_vehiculos']] = list_vehiculos  

        equipos = data.get('equipo',[])

        if equipos:
            list_equipos = []
            for item in equipos:
                tipo = item.get('tipo','').lower().replace(' ', '_')
                nombre = item.get('nombre','')
                marca = item.get('marca','')
                modelo = item.get('modelo','')
                color = item.get('color','')
                serie = item.get('serie','')
                list_equipos.append({
                    self.mf['tipo_equipo']:tipo,
                    self.mf['nombre_articulo']:nombre,
                    self.mf['marca_articulo']:marca,
                    self.mf['modelo_articulo']:modelo,
                    self.mf['color_articulo']:color,
                    self.mf['numero_serie']:serie,
                })
            answers[self.mf['grupo_equipos']] = list_equipos

        gafete = data.get('gafete',{})
        if gafete:
            gafete_ans = {}
            gafete_ans[self.GAFETES_CAT_OBJ_ID] = {self.gafetes_fields['gafete_id']:gafete.get('gafete_id')}
            gafete_ans[self.LOCKERS_CAT_OBJ_ID] = {self.mf['locker_id']:gafete.get('locker_id')}
            gafete_ans[self.mf['documento']] = gafete.get('documento_garantia')
            answers.update(gafete_ans)
            self.update_gafet_status(answers)


        comment = data.get('comentario_acceso',[])
        if comment:
            comment_list = []
            for c in comment:
                comment_list.append(
                    {
                        self.bitacora_fields['comentario']:c.get('comentario_pase'),
                        self.bitacora_fields['tipo_comentario'] :c.get('tipo_de_comentario').lower().replace(' ', '_')
                    }
                )
            answers.update({self.bitacora_fields['grupo_comentario']:comment_list})

        visit_list = data.get('visita_a',[])
        if visit_list:
            visit_list2 = []
            for c in visit_list:
                visit_list2.append(
                   { f"{self.bitacora_fields['visita']}":{ 
                       self.bitacora_fields['visita_nombre_empleado']:c.get('nombre'),
                       self.mf['id_usuario'] :[c.get('user_id')],
                       self.bitacora_fields['visita_departamento_empleado']:[c.get('departamento')],
                       self.bitacora_fields['puesto_empleado']:[c.get('puesto')],
                       self.mf['email_visita_a'] :[c.get('email')]
                   }}
                )
            answers.update({self.bitacora_fields['visita_a']:visit_list2})

        metadata.update({'answers':answers})
        response_create = self.lkf_api.post_forms_answers(metadata)
        return response_create
     
    def assets_access_pass(self, location):
        ### Areas
        catalog_id = self.AREAS_DE_LAS_UBICACIONES_CAT_ID
        form_id = self.PASE_ENTRADA
        group_level = 2
        options = {
              "group_level": group_level,
              "startkey": [
                location
              ],
              "endkey": [
                f"{location}\n",
                {}
              ]
            }
        areas = self.lkf_api.catalog_view(catalog_id, form_id, options) 
        ### Aquien Visita
        catalog_id = self.CONF_AREA_EMPLEADOS_CAT_ID
        visita_a = self.lkf_api.catalog_view(catalog_id, form_id, options) 
        # visita_a = [r.get('key')[group_level-1] for r in visita_a]
        ### Pases de accesos
        res = {
            'Areas': areas,
            'Visita_a': visita_a,
            'Perfiles': self.get_pefiles_walkin(location),
        }
        return res

    def assing_gafete(self, data_gafete, id_bitacora, tipo_movimiento):
        answers={}
        answers_return={}
        for key, value in data_gafete.items():
            if key == "gafete_id":
                answers[self.GAFETES_CAT_OBJ_ID] = {self.gafetes_fields['gafete_id']:data_gafete.get('gafete_id')}
                # answers_return[self.GAFETES_CAT_OBJ_ID] = {self.gafetes_fields['gafete_id']:""}
            elif key == "locker_id":
                answers[self.LOCKERS_CAT_OBJ_ID] = {self.mf['locker_id']:data_gafete.get('locker_id')}
                # answers_return[self.LOCKERS_CAT_OBJ_ID] = {self.mf['locker_id']:""}

            if  key == 'ubicacion' or key == 'area':
                if data_gafete['ubicacion'] and not data_gafete['area']:
                    answers[self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID]={self.f['location']:data_gafete.get('ubicacion')}
                    # answers_return[self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID]={self.f['location']:data_gafete.get('ubicacion')}
                elif data_gafete['area'] and not data_gafete['ubicacion']:
                    answers[self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID]={self.f['area']:data_gafete.get('area', "")}
                    # answers_return[self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID]={self.f['area']:data_gafete.get('area', "")}
                elif data_gafete['area'] and data_gafete['ubicacion']: 
                    answers[self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID] = {self.f['location']:data_gafete.get('ubicacion'),self.f['area']:data_gafete.get('area', "")}
                    # answers_return[self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID] = {self.f['location']:data_gafete.get('ubicacion'),self.f['area']:data_gafete.get('area', "")}
            elif key == "status_gafete":
                answers[self.mf['status_gafete']]=data_gafete.get('status_gafete')
                # answers_return[self.mf['status_gafete']]=data_gafete.get('status_gafete')
            elif key == "documento":
                answers[self.mf['documento']] = data_gafete.get('documento')
                # answers_return[self.mf['documento']] = data_gafete.get('documento')
        if answers or answers_return:
            # ans={}
            # if tipo_movimiento=="salida":
            #     ans=answers_return
            # else:
            #     ans=answers
            res= self.lkf_api.patch_multi_record( answers = answers, form_id=self.BITACORA_ACCESOS, record_id=[id_bitacora])
            if res.get('status_code') == 201 or res.get('status_code') == 202:
                answers[self.mf['tipo_registro']] = tipo_movimiento.lower()
                res_gaf = self.update_gafet_status(answers)
                if res_gaf.get('status_code') == 201 or res_gaf.get('status_code') == 202:
                    return res
        else:
            self.LKFException('No se mandarón parametros para actualizar')

    def delete_article_concessioned(self, folio):
        list_records = []
        if len(folio) > 0:
            for element in folio:
                response = self.get_record_by_folio(element, self.CONCESSIONED_ARTICULOS, select_columns={'_id':1,})
                if response.get('_id'):
                    list_records.append("/api/infosync/form_answer/"+str(response['_id'])+"/")
                else:
                    self.LKFException('No se encontro el folio correspondiente')
        else:
            self.LKFException('Lista de folios vacia, ingrese folio')

        if len(list_records) > 0:
            return self.check_status_code(self.lkf_api.patch_record_list({"deleted_objects": list_records,}))
        else:
            self.LKFException('No se encontro los folios correspondiente')
            
    def delete_article_lost(self, folio):
        list_records = []
        if len(folio) > 0:
            for element in folio:
                response = self.get_record_by_folio(element, self.BITACORA_OBJETOS_PERDIDOS, select_columns={'_id':1,})
                if response.get('_id'):
                    list_records.append("/api/infosync/form_answer/"+str(response['_id'])+"/")
                else:
                    self.LKFException('No se encontro el folio correspondiente')
        else:
            self.LKFException('Lista de folios vacia, ingrese folio')

        if len(list_records) > 0:
            return self.check_status_code(self.lkf_api.patch_record_list({"deleted_objects": list_records,}))
        else:
            self.LKFException('No se encontro los folios correspondiente')

    def delete_failure(self, folio):
        list_records = []
        if len(folio) > 0:
            for element in folio:
                response = self.get_record_by_folio(element, self.BITACORA_FALLAS, select_columns={'_id':1,})
                if response.get('_id'):
                    list_records.append("/api/infosync/form_answer/"+str(response['_id'])+"/")
                else:
                    self.LKFException('No se encontro el folio correspondiente')
        else:
            self.LKFException('Lista de folios vacia, ingrese folio')

        if len(list_records) > 0:
            return self.check_status_code(self.lkf_api.patch_record_list({"deleted_objects": list_records,}))
        else:
            self.LKFException('No se encontro los folios correspondiente')

    def delete_incidence(self, folio):
        list_records = []
        if len(folio) > 0:
            for element in folio:
                response = self.get_record_by_folio(element, self.BITACORA_INCIDENCIAS, select_columns={'_id':1,})
                if response.get('_id'):
                    list_records.append("/api/infosync/form_answer/"+str(response['_id'])+"/")
                else:
                    self.LKFException('No se encontro el folio correspondiente')
        else:
            self.LKFException('Lista de folios vacia, ingrese folio')

        if len(list_records) > 0:
            return self.check_status_code(self.lkf_api.patch_record_list({"deleted_objects": list_records,}))
        else:
            self.LKFException('No se encontro los folios correspondiente')

    def delete_notes(self, folio):
        list_records = []
        if len(folio) > 0:
            for element in folio:
                response = self.get_record_by_folio(element, self.ACCESOS_NOTAS, select_columns={'_id':1,})
                if response.get('_id'):
                    list_records.append("/api/infosync/form_answer/"+str(response['_id'])+"/")
                else:
                    self.LKFException('No se encontro el folio correspondiente')
        else:
            self.LKFException('Lista de folios vacia, ingrese folio')

        if len(list_records) > 0:
            return self.check_status_code(self.lkf_api.patch_record_list({"deleted_objects": list_records,}))
        else:
            self.LKFException('No se encontro los folios correspondiente')

    def deliver_badge(self, folio):
        answers = {
            self.gafetes_fields['status_gafete']:'recibir_gafete',
        }
        if folio:
            return self.lkf_api.patch_multi_record( answers = answers, form_id=self.BITACORA_GAFETES_LOCKERS, folios=[folio])
        else:
            self.LKFException('No se mandarón parametros para actualizar')

    def delete_paquete(self, folio):
        print("del", folio)

    def do_access(self, qr_code, location, area, data):
        '''
        Valida pase de entrada y crea registro de entrada al pase
        '''
        access_pass = self.get_detail_access_pass(qr_code)
        if not qr_code and not location and not area:
            return False
        total_entradas = self.get_count_ingresos(qr_code)
        
        diasDisponibles = access_pass.get("limitado_a_dias", [])
        dias_semana = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        tz = pytz.timezone("America/Mexico_City")
        hoy = datetime.now(tz)
        dia_semana = hoy.weekday()
        nombre_dia = dias_semana[dia_semana]

        if access_pass.get('estatus',"") == 'vencido':
            self.LKFException({'msg':"El pase esta vencido, edita la información o genera uno nuevo.","title":'Revisa la Configuración'})
        elif access_pass.get('estatus', '') == 'proceso':
            self.LKFException({'msg':"El pase no se ha sido completado aun, informa al usuario que debe completarlo primero.","title":'Requisitos faltantes'})

        if diasDisponibles:
            if nombre_dia not in diasDisponibles:
                dias_capitalizados = [dia.capitalize() for dia in diasDisponibles]

                if len(dias_capitalizados) > 1:
                    dias_formateados = ', '.join(dias_capitalizados[:-1]) + ' y ' + dias_capitalizados[-1]
                else:
                    dias_formateados = dias_capitalizados[0]

                self.LKFException({
                        'msg': f"Este pase no te permite ingresar hoy {nombre_dia.capitalize()}. Solo tiene acceso los siguientes dias: {dias_formateados}",
                        "title":'Aviso'
                    })
        
        limite_acceso = access_pass.get('limite_de_acceso')
        if len(total_entradas) > 0 and limite_acceso and int(limite_acceso) > 0:
            if total_entradas['total_records']>= int(limite_acceso) :
                self.LKFException({'msg':"Se ha completado el limite de entradas disponibles para este pase, edita el pase o crea uno nuevo.","title":'Revisa la Configuración'})
        
        timezone = pytz.timezone('America/Mexico_City')
        fecha_actual = datetime.now(timezone).replace(microsecond=0)
        fecha_caducidad = access_pass.get('fecha_de_caducidad')
        fecha_obj_caducidad = datetime.strptime(fecha_caducidad, "%Y-%m-%d %H:%M:%S")
        fecha_caducidad = timezone.localize(fecha_obj_caducidad)

        # Se agregan 15 minutos como margen de tolerancia
        fecha_caducidad_con_margen = fecha_caducidad + timedelta(minutes=15)

        if fecha_caducidad_con_margen < fecha_actual:
            self.LKFException({'msg':"El pase esta vencido, ya paso su fecha de vigencia.","title":'Advertencia'})
        
        if location not in access_pass.get("ubicacion",[]):
            msg = f"La ubicación {location}, no se encuentra en el pase. Pase valido para las siguientes ubicaciones: {access_pass.get('ubicacion',[])}."
            self.LKFException({'msg':msg,"title":'Revisa la Configuración'})
        
        if self.validate_access_pass_location(qr_code, location):
            self.LKFException("En usuario ya se encuentra dentro de una ubicacion")
        val_certificados = self.validate_certificados(qr_code, location)

        
        pass_dates = self.validate_pass_dates(access_pass)
        comentario_pase =  data.get('comentario_pase',[])
        if comentario_pase:
            values = {self.pase_entrada_fields['grupo_instrucciones_pase']:{
                -1:{
                self.pase_entrada_fields['comentario_pase']:comentario_pase,
                self.mf['tipo_de_comentario']:'caseta'
                }
            }
            }
            # self.update_pase_entrada(values, record_id=[str(access_pass['_id']),])
        res = self._do_access(access_pass, location, area, data)
        return res

    def do_checkin(self, location, area, employee_list=[], check_in_manual={}):
        # Realiza el check-in en una ubicación y área específica.

        if not self.is_boot_available(location, area):
            msg = f"Can not login in to boot on location {location} at the area {area}."
            msg += f"Because '{self.last_check_in.get('employee')}' is logged in."
            self.LKFException(msg)
        if employee_list:
            user_id = [self.user.get('user_id'),] + [x['user_id'] for x in employee_list]
        else:
            user_id = self.user.get('user_id')
        boot_config = self.get_users_by_location_area(
            location_name=location, 
            area_name=area, 
            user_id=user_id)
        if not boot_config:
            msg = f"User can not login to this area : {area} at location: {location} ."
            msg += f"Please check your configuration."
            self.LKFException(msg)
        else:
            allowed_users = [x['user_id'] for x in boot_config]
            if type(user_id) == int:
                user_id=[user_id]
            common_values = list(set(user_id) & set(allowed_users))
            not_allowed = [value for value in user_id if value not in common_values]
        if not_allowed:
            msg = f"Usuarios con ids {not_allowed}. "
            msg += f"No estan permitidos de hacer checking en esta area : {area} de la ubicacion {location} ."
            self.LKFException({'msg':msg,"title":'Error de Configuracion'})

        validate_status = self.get_employee_checkin_status(user_id)
        not_allowed = [uid for uid, u_data in validate_status.items() if u_data['status'] =='in']
        if not_allowed:
            msg = f"El usuario(s) con ids {not_allowed}. Se encuentran actualmente logeado en otra caseta."
            msg += f"Es necesario primero salirse de cualquier caseta antes de querer entrar a una casta"
            self.LKFException({'msg':msg,"title":'Accion Requerida!!!'})

        employee = self.get_employee_data(email=self.user.get('email'), get_one=True)
        user_data = self.lkf_api.get_user_by_id(self.user.get('user_id'))
        employee['timezone'] = user_data.get('timezone','America/Monterrey')
        employee['name'] = employee['worker_name']
        employee['position'] = self.chife_guard
        if not employee:
            msg = f"Ningun empleado encontrado con email: {self.user.get('email')}"
            self.LKFException(msg)
        timezone = employee.get('cat_timezone', employee.get('timezone', 'America/Monterrey'))
        data = self.lkf_api.get_metadata(self.CHECKIN_CASETAS)
        now_datetime =self.today_str(timezone, date_format='datetime')
        checkin = self.checkin_data(employee, location, area, 'in', now_datetime)
        employee_list.insert(0,employee)
        checkin = self.check_in_out_employees('in', now_datetime, checkin=checkin, employee_list=employee_list)
        data.update({
                'properties': {
                    "device_properties":{
                        "system": "Modulo Accesos",
                        "process": 'Checkin-Checkout',
                        "action": 'do_checkin',
                        "archive": "accesos_utils.py"
                    }
                },
                'answers': checkin
            })
        if check_in_manual:
            checkin.update({
                self.checkin_fields['checkin_image']: check_in_manual.get('image', []),
                self.checkin_fields['commentario_checkin_caseta']: check_in_manual.get('comment', '')
            })
        resp_create = self.lkf_api.post_forms_answers(data)
        #TODO agregar nombre del Guardia Quien hizo el checkin
        if resp_create.get('status_code') == 201:
            resp_create['json'].update({'boot_status':{'guard_on_duty':user_data['name']}})
        return resp_create

    def do_checkout_aux_guard(self, checkin_id=None, location=None, area=None, guards=[], forzar=False, comments=False):
        """
        Realiza el checkout de los guardias auxiliares especificados en guards.
        """
        employee = self.get_employee_data(email=self.user.get('email'), get_one=True)
        timezone = employee.get('cat_timezone', employee.get('timezone', 'America/Monterrey'))
        now_datetime = self.today_str(timezone, date_format='datetime')
        last_chekin = {}

        # Solo buscamos el último checkin de los guards especificados
        if not checkin_id and guards:
            last_chekin = self.get_guard_last_checkin(guards)
            checkin_id = last_chekin.get('_id')

        if not checkin_id:
            self.LKFException({
                "msg": "No encontramos un checking valido del cual podemos hacer checkout...", 
                "title": "Una Disculpa!!!"
            })

        record = self.get_record_by_id(checkin_id)
        checkin_answers = record['answers']
        folio = record['folio']

        # Realiza el checkout solo de los guards especificados
        data = self.lkf_api.get_metadata(self.CHECKIN_CASETAS)
        checkin_answers = self.check_in_out_employees('out', now_datetime, checkin=checkin_answers, employee_list=guards)
        data['answers'] = checkin_answers
        response = self.lkf_api.patch_record(data=data, record_id=checkin_id)
        return response

    def do_checkout(self, checkin_id=None, location=None, area=None, guards=[], forzar=False, comments=False):
        # self.get_answer(keys)
        employee =  self.get_employee_data(email=self.user.get('email'), get_one=True)
        timezone = employee.get('cat_timezone', employee.get('timezone', 'America/Monterrey'))
        now_datetime =self.today_str(timezone, date_format='datetime')
        last_chekin = {}
        if not checkin_id:
            if guards:
                last_chekin = self.get_guard_last_checkin(guards)
            elif location or area:
                last_chekin = self.get_last_checkin(location, area)
            checkin_id = last_chekin.get('_id')
        if not checkin_id:
            self.LKFException({
                "msg":"No encontramos un checking valido del cual podemos hacer checkout...", 
                "title":"Una Disculpa!!!"})
        record = self.get_record_by_id(checkin_id)
        checkin_answers = record['answers']
        folio = record['folio']
        area = checkin_answers.get(self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID,{}).get(self.f['area'])
        location = checkin_answers.get(self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID,{}).get(self.f['location'])
        rec_guards = checkin_answers.get(self.checkin_fields['guard_group'])
        if not guards:
            checkin_answers[self.checkin_fields['commentario_checkin_caseta']] = \
                checkin_answers.get(self.checkin_fields['commentario_checkin_caseta'],'')
            # Si no especifica guardas va a cerrar toda la casta
            checkin_answers[self.checkin_fields['checkin_type']] = 'cierre'
            checkin_answers[self.checkin_fields['boot_checkout_date']] = now_datetime
            checkin_answers[self.checkin_fields['forzar_cierre']] = 'regular'
            if comments:
                checkin_answers[self.checkin_fields['commentario_checkin_caseta']] += comments + ' '
            if forzar:
                checkin_answers[self.checkin_fields['commentario_checkin_caseta']] += f"Cerrado por: {employee.get('worker_name')}"
                checkin_answers[self.checkin_fields['forzar_cierre']] = 'forzar'
        if self.is_boot_available(location, area):
            msg = f"Can not make a CHEKOUT on a boot that hasn't checkin. Location: {location} at the area {area}."
            msg += f"You need to checkin first."
            self.LKFException(msg)
        if not checkin_id:
            msg = f"No checking found for this  Location: {location} at the area {area}."
            msg += f"You need to checkin first."
            self.LKFException(msg)

        data = self.lkf_api.get_metadata(self.CHECKIN_CASETAS)
        checkin_answers = self.check_in_out_employees('out', now_datetime, checkin=checkin_answers, employee_list=guards)
        # response = self.lkf_api.patch_multi_record( answers=checkin, form_id=self.CHECKIN_CASETAS, folios=[folio,])
        data['answers'] = checkin_answers

        #Verificar si el guardia es un guardia de apoyo para hacer su checkout correctamente
        check_aux_guard = self.check_in_aux_guard()
        if check_aux_guard:
            for user_id_aux, each_user in check_aux_guard.items():
                if user_id_aux == self.unlist(employee.get('usuario_id')) and each_user.get('checkin_position') == 'guardia_de_apoyo':
                    resp = self.do_checkout_aux_guard(guards=[self.unlist(employee.get('usuario_id'))], location=location, area=area)
                    return resp

        response = self.lkf_api.patch_record( data=data, record_id=checkin_id)
        if response.get('status_code') == 401:
            return self.LKFException({
                "title":"Error de Configuracion",
                "msg":"El guardia NO tiene permisos sobre el formulario de cierre de casetas"})
        return response

    def do_out(self, qr, location, area, gafete_id=None):
        '''
            Realiza el cambio de estatus de la forma de bitacora, relacionada a la salida, como parametro
            es necesesario enviar el nombre del visitante que es el unico dato qu se encuentra en la forma
        '''
        response = False
        last_check_out = self.get_last_user_move(qr, location)
        print("last", last_check_out)
        if last_check_out.get('status_gafete') and last_check_out.get('status_gafete')!= "entregado":
            self.LKFException({"status_code":400, "msg":f"Se necesita liberar el gafete antes de regitrar la salida"})
        if not location:
            self.LKFException({"status_code":400, "msg":f"Se requiere especificar una ubicacion de donde se realizara la salida."})
        if not area:
            self.LKFException({"status_code":400, "msg":f"Se requiere especificar el area de donde se realizara la salida."})
        if last_check_out.get('ubicacion_entrada') != location:
            self.LKFException({"status_code":400, "msg":f"Este usuario ingreso en {location} y no puede salir en {last_check_out.get('ubicacion_entrada')}."})
        if last_check_out.get('folio'):
            folio = last_check_out.get('folio',0)
            checkin_date_str = last_check_out.get('checkin_date')
            checkin_date = self.date_from_str(checkin_date_str)
            tz_mexico = pytz.timezone('America/Mexico_City')
            now = datetime.now(tz_mexico)
            fecha_hora_str = now.strftime("%Y-%m-%d %H:%M:%S")
            duration = time_module.strftime('%H:%M:%S', time_module.gmtime(
                self.date_2_epoch(fecha_hora_str) - self.date_2_epoch(checkin_date_str)
            ))
            if self.user_in_facility(status_visita=last_check_out.get('status_visita')):
                answers = {
                    f"{self.mf['tipo_registro']}":'salida',
                    f"{self.mf['fecha_salida']}":fecha_hora_str,
                    f"{self.mf['duracion']}":duration,
                    f"{self.AREAS_DE_LAS_UBICACIONES_SALIDA_OBJ_ID}": {
                        f"{self.mf['nombre_area_salida']}": area,
                    },

                }
                response = self.lkf_api.patch_multi_record( answers=answers, form_id=self.BITACORA_ACCESOS, folios=[folio])
        if not response:
            self.LKFException({"status_code":400, "msg":f"El usuario no se encuentra dentro de la Ubicacion: {location}."})
        return response            

    def do_validacion_certificado(self, cert, detail=False):
        res = {}
        nombre = cert['nombre_permiso']
        status_doc = cert.get('status_doc_cetrificado', 'vencido')
        status = cert.get('status_cetrificado', 'pendiente')
        if detail:
            data = {}
            data['documento'] = status_doc
            data['autorizacion'] = status
        if status_doc.lower() == 'activo' and status.lower() == 'autorizado':
            if detail:
                data['status'] = 'Autorizado'
            else:
                res = "Autorizado"
        else:
            if detail:
                data['status'] = 'NO Autorizado'
            else:
                res = "NO Autroizado"
        if detail:
            res[nombre] = data
        return res

    def calcula_total_depositos(self):
        depositos = self.answers.get(self.incidence_fields['datos_deposito_incidencia'],[])
        return sum([x[self.incidence_fields['cantidad']] for x in depositos])

    def catalogos_pase_area(self, location_name):
        user_id= self.user.get("user_id")
        res={
            "areas_by_location" : self.get_areas_by_location(location_name)
        }
        return res

    def catalogos_pase_location(self):
        user_id= self.user.get("user_id")
        res = {}
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.CONF_AREA_EMPLEADOS,
        }
        if user_id:
            match_query[f"answers.{self.EMPLOYEE_OBJ_ID}.{self.employee_fields['user_id_id']}"] = user_id

        query = [
            {'$match': match_query },
            {'$unwind': f"$answers.{self.mf['areas_grupo']}"},
            {'$project': {
                'area':f"$answers.{self.mf['areas_grupo']}.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.mf['ubicacion']}",
                'set_as':f"$answers.{self.mf['areas_grupo']}.{self.Employee.f['area_default']}",
            }},
            {'$group': {
                '_id': {
                    'set_as': '$set_as',
                    'area': '$area',
                },
            }},
            {'$project': {
                '_id':0,
                'area':'$_id.area',
                'set_as':'$_id.set_as',
            }}
        ]
        response = self.cr.aggregate(query)
        res = {'ubicaciones_user':[],'ubicaciones_default':[]}
        for x in response:
            if x.get('area') not in res['ubicaciones_user']:
                res['ubicaciones_user'].append(x.get('area'))
            if x.get('set_as')  == 'default':
                if x.get('area') not in res['ubicaciones_default']:
                    res['ubicaciones_default'].append(x.get('area'))
        return res

    def catalagos_pase_no_jwt(self, qr_code):
        cat_vehiculos= self.catalogo_vehiculos({})
        cat_estados= self.catalogo_estados({})
        pass_selected= self.get_pass_custom(qr_code)
        res={"cat_vehiculos":cat_vehiculos, "cat_estados":cat_estados, "pass_selected":pass_selected}
        return res

    def catalogo_categoria(self, options={}):
        catalog_id = self.ESTADO_ID
        form_id = self.PASE_ENTRADA
        group_level = options.get('group_level',1)
        return self.catalogo_view(catalog_id, form_id)

    def catalogo_estados(self, options={}):
        catalog_id = self.ESTADO_ID
        form_id = self.PASE_ENTRADA
        return self.catalogo_view(catalog_id, form_id)

    def catalogo_incidencias(self, cat="", sub_cat=""):
        catalog_id = self.LISTA_INCIDENCIAS_CAT_ID
        form_id = self.BITACORA_INCIDENCIAS
        options={}
        search=""
        if cat and sub_cat:
            options = {
                "group_level": 3,
                "startkey": [cat,sub_cat],
                "endkey": [cat, f"{sub_cat}\n"]
            }
            search="incidence"
        else:
            if cat and not sub_cat:
                options = {
                    "group_level": 2,
                    "startkey": [cat],
                    "endkey": [f"{cat}\n"]
                }
                search="sub_catalog"
            if sub_cat and not cat:
                options = {
                    "group_level": 3,
                    "startkey": [sub_cat],
                    "endkey": [f"{sub_cat}\n"]
                }
                search="incidence"

        res = self.lkf_api.catalog_view(catalog_id, form_id, options)
        formatted= {
            "selected":cat, 
            "data":res, 
            "type": search
        }
        if res == [None] and cat and not sub_cat:
            res_obj = self.catalogo_incidencias(cat="", sub_cat= cat)
            formatted["selected"] = cat
            formatted["data"] = res_obj["data"] 
            formatted["type"] = "incidence"
        print("formatedo", simplejson.dumps(formatted, indent=4))
        return formatted

    def catalogo_vehiculos(self, options={}):
        catalog_id = self.TIPO_DE_VEHICULO_ID
        form_id = self.PASE_ENTRADA
        res= self.catalogo_view(catalog_id, form_id, options=options)
        return res

    def catalogo_view(self, catalog_id, form_id, options={}, detail=False):
        catalog_id = catalog_id
        form_id = form_id
        res = self.lkf_api.catalog_view(catalog_id, form_id, options)
        if detail:
            if res and len(res) > 0:
                res = self._labels(res[0])
                res = {k:v[0] for k,v in res.items() if len(v)>0}
        return res

    def catalogo_config_area_empleado(self, bitacora, location=''):
        #TODO Verificar si objetos perdidos tambien necesita solo los empleados de una location
        #TODO Mejorar funcion, de momento funcional
        catalog_id = self.CONF_AREA_EMPLEADOS_CAT_ID
        if bitacora == 'Objetos Perdidos':
            form_id= self.BITACORA_OBJETOS_PERDIDOS
            response = self.lkf_api.catalog_view(catalog_id, form_id)
        elif bitacora == 'Incidencias':
            form_id= self.BITACORA_INCIDENCIAS
            if location:
                options = {
                    "group_level": 2,
                    "startkey": [
                        location
                    ],
                    "endkey": [
                        f"{location}\n",
                    ]
                }
            else:
                form_id= self.BITACORA_OBJETOS_PERDIDOS
                options = {}
            response = self.lkf_api.catalog_view(catalog_id, form_id, options) 
        return response

    def catalogo_config_area_empleado_apoyo(self):
        catalog_id = self.CONF_AREA_EMPLEADOS_AP_CAT_ID
        form_id= self.BITACORA_FALLAS
        return self.lkf_api.catalog_view(catalog_id, form_id) 

    def catalogo_tipo_concesion(self,location="", tipo=""):
        catalog_id = self.ACTIVOS_FIJOS_CAT_ID
        form_id= self.CONCESSIONED_ARTICULOS
        options={}
        if location and tipo:
            options = {
                "group_level": 3,
                "startkey": [location,tipo],
                "endkey": [location, f"{tipo}\n"]
            }
        else:
            if location and not tipo:
                options = {
                    "group_level": 2,
                    "startkey": [location],
                    "endkey": [f"{location}\n"]
                }
            elif tipo and not location:
                self.LKFException('Location es requerido')
        response= self.catalogo_view(catalog_id, form_id, options)
        return response

    def catalogo_falla(self, tipo=""):
        options={}
        if tipo:
            options = {
                'startkey': [tipo],
                'endkey': [f"{tipo}\n",{}],
                'group_level':2
            }
        catalog_id = self.LISTA_FALLAS_CAT_ID
        form_id = self.BITACORA_FALLAS
        return self.catalogo_view(catalog_id, form_id, options)

    def catalogo_tipo_articulo(self, tipo=""):
        options={}
        if tipo:
            options = {
                'startkey': [tipo],
                'endkey': [f"{tipo}\n",{}],
                'group_level':2
            }
        catalog_id = self.TIPO_ARTICULOS_PERDIDOS_CAT_ID
        form_id = self.BITACORA_OBJETOS_PERDIDOS
        return self.catalogo_view(catalog_id, form_id, options)

    def check_status_code(self, data_response):
        for item in data_response:
            if 'status_code' in item[1]:
                return {'status_code':item[1]['status_code']}
            else:
                return {'status_code':'400'}

    def check_in_out_employees(self,  checkin_type, check_datetime, checkin={}, employee_list=[], **kwargs):
        checkin_status = 'entrada' if checkin_type == 'in' else 'salida'
        date_id = 'checkin_date' if checkin_type == 'in' else 'checkout_date'
        checkin[self.f['guard_group']] = checkin.get(self.f['guard_group'],[])
        if checkin_type == 'out':
            for guard in checkin[self.f['guard_group']]:
                user_id = int(self.unlist(guard.get(self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID,{})\
                    .get(self.employee_fields['user_id_jefes'],0)))
                if guard[self.checkin_fields['checkin_status']] != checkin_status:
                    if not employee_list:
                        guard[self.checkin_fields['checkin_status']] = checkin_status
                        guard[self.checkin_fields[date_id]] = check_datetime                    
                    elif user_id in employee_list:
                        guard[self.checkin_fields['checkin_status']] = checkin_status
                        guard[self.checkin_fields[date_id]] = check_datetime
        elif employee_list:
            for idx, guard in enumerate(employee_list):
                empl_cat = {}
                empl_cat[self.f['worker_name_b']] = guard.get('name')
                if isinstance(guard.get('usuario_id'), list):
                    empl_cat[self.f['user_id_b']] = [(guard.get('usuario_id', [])[0]),]
                else:
                    empl_cat[self.f['user_id_b']] = [guard.get('user_id'),]
                guard_data = {
                        self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID : empl_cat,
                        self.checkin_fields['checkin_position']:'guardiad_de_apoyo',
                        self.checkin_fields['checkin_status']:checkin_status,
                        self.checkin_fields[date_id]:check_datetime,
                       }
                if kwargs.get('employee_type'):
                    guard_data.update({self.checkin_fields['checkin_position']: kwargs['employee_type'] })
                elif idx == 0:
                    guard_data.update({self.checkin_fields['checkin_position']: self.chife_guard})
                else:
                    guard_data.update({self.checkin_fields['checkin_position']: self.support_guard})
                checkin[self.f['guard_group']] += [guard_data,]
        return checkin

    def checkin_data(self, employee, location, area, checkin_type, now_datetime):
        set_type = self.set_boot_status(checkin_type)
        checkin = {
            self.f['checkin_type']: set_type,
            self.f['boot_checkin_date'] : now_datetime,
            self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID : {
                self.f['location']: location,
                self.f['area']: area, 
                self.f['worker_name']: employee.get('worker_name'),
            },

        }
        return checkin

    def config_get_guards_positions(self):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.PUESTOS_GUARDIAS,
            }        
        unwind = {'$unwind': f"$answers.{self.f['guard_group']}"}
        query = [
            {'$match': match_query },
            {'$unwind': f"$answers.{self.f['guard_group']}"},
            {'$project':{
                "_id":0,
                'tipo_de_guardia': f"$answers.{self.f['guard_group']}.{self.mf['tipo_de_guardia']}",
                'puesto': f"$answers.{self.f['guard_group']}.{self.PUESTOS_OBJ_ID}.{self.f['worker_position']}"
                }
            },
            {'$unwind': f"$tipo_de_guardia"},
            {'$group':{
                '_id':{
                    'tipo_de_guardia':'$tipo_de_guardia'
                    },
                'puestos': {'$addToSet':'$puesto'}
                }
            },
            {'$project':{
                "_id":0,
                'tipo_de_guardia': '$_id.tipo_de_guardia',
                'puestos': '$puestos',
                }
            },
            {'$sort': {'tipo_de_guardia':1}}
            ]
        return self.format_cr_result(self.cr.aggregate(query))

    def create_article_concessioned(self, data_articles):
        #---Define Metadata
        metadata = self.lkf_api.get_metadata(form_id=self.CONCESSIONED_ARTICULOS)
        metadata.update({
            "properties": {
                "device_properties":{
                    "System": "Script",
                    "Module": "Accesos",
                    "Process": "Creación de Concesion Unica",
                    "Action": "create_article_concessioned",
                    "File": "accesos/app.py"
                }
            },
        })
        #---Define Answers
        answers = {}
        for key, value in data_articles.items():
            if  key =='status_concesion':
                answers[self.consecionados_fields['status_concesion']] = value
            if  key == 'solicita_concesion':
                answers[self.consecionados_fields['solicita_concesion']] = value
            elif  key == 'persona_nombre_concesion':
                answers[self.consecionados_fields['persona_catalog_concesion']] = { self.mf['nombre_guardia_apoyo'] : value}
            elif  key == 'caseta_concesion':
                answers[self.consecionados_fields['area_catalog_concesion']] = { self.mf['nombre_area_salida']: value}
            elif  key == 'ubicacion_concesion':
                answers[self.consecionados_fields['ubicacion_catalog_concesion']] = { self.mf['ubicacion']: value}
            elif  key == 'area_concesion':
                answers[self.consecionados_fields['equipo_catalog_concesion']] =   { self.consecionados_fields['area_concesion']: value}
            elif  key == 'equipo_concesion':
                answers[self.consecionados_fields['equipo_catalog_concesion']] =   { self.consecionados_fields['equipo_concesion']: value}
            else:
                answers.update({f"{self.consecionados_fields[key]}":value})

        metadata.update({'answers':answers})
        return self.lkf_api.post_forms_answers(metadata)

    def create_article_lost(self, data_articles):
        #---Define Metadata
        metadata = self.lkf_api.get_metadata(form_id=self.BITACORA_OBJETOS_PERDIDOS)
        metadata.update({
            "properties": {
                "device_properties":{
                    "System": "Script",
                    "Module": "Accesos",
                    "Process": "Creación de Bitacora Articulo Perdido",
                    "Action": "create_article_lose",
                    "File": "accesos/app.py"
                }
            },
        })
        employee = self.get_employee_data(email=self.user.get('email'), get_one=True)
        #---Define Answers
        answers = {}
        for key, value in data_articles.items():
            if  key == 'tipo_articulo_perdido' or key == 'articulo_seleccion':
                if data_articles['tipo_articulo_perdido'] and not data_articles['articulo_seleccion']:
                    answers[self.perdidos_fields['tipo_articulo_catalog']] = {
                        self.perdidos_fields['tipo_articulo_perdido']: data_articles['tipo_articulo_perdido']
                        }
                elif data_articles['articulo_seleccion'] and not data_articles['tipo_articulo_perdido']:
                    answers[self.perdidos_fields['tipo_articulo_catalog']] = {
                        self.perdidos_fields['articulo_seleccion']: data_articles['articulo_seleccion']
                        }
                elif data_articles['articulo_seleccion'] and data_articles['tipo_articulo_perdido']: 
                    answers[self.perdidos_fields['tipo_articulo_catalog']] = {
                    self.perdidos_fields['tipo_articulo_perdido']:data_articles['tipo_articulo_perdido'],
                    self.perdidos_fields['articulo_seleccion']:data_articles['articulo_seleccion']}

            elif  key == 'ubicacion_perdido' or key == 'area_perdido':
                if data_articles['ubicacion_perdido'] and not data_articles['area_perdido']:
                    answers[self.perdidos_fields['ubicacion_catalog']] = {self.perdidos_fields['ubicacion_perdido']:data_articles['ubicacion_perdido']}
                elif data_articles['area_perdido'] and not data_articles['ubicacion_perdido']:
                    answers[self.perdidos_fields['ubicacion_catalog']] = {self.perdidos_fields['area_perdido']:data_articles['area_perdido']}
                elif data_articles['area_perdido'] and data_articles['ubicacion_perdido']: 
                    answers[self.perdidos_fields['ubicacion_catalog']] = {self.perdidos_fields['ubicacion_perdido']:data_articles['ubicacion_perdido'],
                    self.perdidos_fields['area_perdido']:data_articles['area_perdido']}
            elif key == 'quien_entrega_interno':
                answers[self.perdidos_fields['quien_entrega_catalog']] = {self.perdidos_fields['quien_entrega_interno']:value}
            elif key == 'locker_perdido':
                answers[self.perdidos_fields['locker_catalog']] = {self.perdidos_fields['locker_perdido']:value}
            else:
                answers.update({f"{self.perdidos_fields[key]}":value})
        metadata.update({'answers':answers})
        res=self.lkf_api.post_forms_answers(metadata)
        return res

    def create_badge(self, data_badge):
        #---Define Metadata
        metadata = self.lkf_api.get_metadata(form_id=self.BITACORA_GAFETES_LOCKERS)
        metadata.update({
            "properties": {
                "device_properties":{
                    "System": "Script",
                    "Module": "Accesos",
                    "Process": "Creación de gafete",
                    "Action": "create_badge",
                    "File": "accesos/app.py"
                }
            },
        })
        #---Define Answers
        answers = {}
        for key, value in data_badge.items():
            if  key == 'ubicacion_gafete':
                answers[self.UBICACIONES_CAT_OBJ_ID] = {self.mf['ubicacion']:value}
            elif  key == 'caseta_gafete':
                answers[self.UBICACIONES_CAT_OBJ_ID] = {self.mf['nombre_area']:value}
            elif  key == 'visita_gafete':
                answers[self.mf['catalog_visita']] = {self.mf['nombre_visita']:value}
            elif  key == 'gafete_id':
                answers[self.GAFETES_CAT_OBJ_ID] = {self.gafetes_fields['gafete_id']:value}
            else:
                answers.update({f"{self.gafetes_fields[key]}":value})

        metadata.update({'answers':answers})
        return self.lkf_api.post_forms_answers(metadata)
    
    def upload_ics(self, id_forma_seleccionada, id_field, ics_content={}, meetings=[]):
        temp_dir = tempfile.gettempdir()  # Obtener el directorio temporal
        temp_file_path = os.path.join(temp_dir, "invite.ics")  # Crear la ruta para invite.ics

        #Creacion del invite.ics
        invite_content = self._get_ics_file(meetings=meetings)
        ics_data = invite_content.get(1)
        ics_content = ics_data.decode('utf-8')

        with open(temp_file_path, mode='w', encoding='utf-8') as temp_file:
            temp_file.write(ics_content)

        rb_file = open(temp_file_path, 'rb')  # Abrir el archivo para subirlo
        dir_file = {'File': rb_file}
        
        try:
            upload_data = {'form_id': id_forma_seleccionada, 'field_id': id_field}
            upload_url = self.lkf_api.post_upload_file(data=upload_data, up_file=dir_file)
            rb_file.close()
        except Exception as e:
            rb_file.close()
            os.remove(temp_file_path)
            print("Error al subir el archivo:", e)
            return {"error": "Fallo al subir el archivo"}

        try:
            file_url = upload_url['data']['file']
            update_file = {'file_name': "invite.ics", 'file_url': file_url}
        except KeyError:
            print('No se pudo obtener la URL del archivo')
            update_file = {"error": "Fallo al obtener la URL del archivo"}
        finally:
            os.remove(temp_file_path)  # Borrar el archivo temporal

        return update_file

    def create_enviar_msj(self, data_msj, data_cel_msj=None, folio=None):
        if not data_msj.get('enviado_desde'):
            data_msj['enviado_desde'] = 'Modulo de Accesos'
        return self.send_email_by_form(data_msj)
    
    def send_msj_pase(self, data_cel_msj=None, pre_sms=False, account=''):
        """
        Envía un mensaje de texto a un número de celular con información personalizada sobre un pase de invitación.

        Este método genera un mensaje en función de los datos proporcionados en `data_cel_msj`. 
        Si `pre_sms` es `True`, indica que se enviara un mensaje pre-registro para completar el pase. 
        En caso contrario, incluirá el mensaje de cuando se completa el pase.

        Args:
            data_cel_msj (dict): Un diccionario con los datos necesarios para personalizar el mensaje. 
                Las claves esperadas son:
                    - 'nombre' (str): Nombre de la persona invitada.
                    - 'visita_a' (str): Nombre de la persona o entidad que invita.
                    - 'ubicacion' (str): Ubicación del evento o visita.
                    - 'link' (str): Enlace para completar el registro.
                    - 'fecha_desde' (str): Fecha de inicio de la invitación.
                    - 'fecha_hasta' (str): Fecha de finalización de la invitación.
                    - 'numero' (str): Número de teléfono al que se enviará el mensaje.
            pre_sms (bool): Si es `True`, se genera un mensaje con instrucciones de registro.
                            Si es `False`, se genera un mensaje de pase completado.

        Returns:
            dict: Un diccionario con el código de estado del envío. Por ejemplo:
                - {'status_code': 200} si el mensaje fue enviado exitosamente.
        """

        fecha_str_desde = data_cel_msj.get('fecha_desde', '')
        fecha_str_hasta = data_cel_msj.get('fecha_hasta', '')

        fecha_desde = datetime.strptime(fecha_str_desde, "%Y-%m-%d %H:%M:%S")
        if fecha_str_hasta:
            fecha_hasta = datetime.strptime(fecha_str_hasta, "%Y-%m-%d %H:%M:%S")

        mensaje=''
        if pre_sms:
            msg = f"Hola {data_cel_msj.get('nombre', '')}, {data_cel_msj.get('visita_a', '')} "
            msg += f"te invita a {data_cel_msj.get('ubicacion', '')} y creo un pase para ti."
            msg += f" Completa tus datos de registro aquí: {data_cel_msj.get('link', '')}"
            mensaje = msg
        else:
            if account == 'milenium':
                get_pdf_url = self.get_pdf(data_cel_msj.get('qr_code', ''), template_id=553)
                get_pdf_url = get_pdf_url.get('data', '').get('download_url', '')
            else:
                get_pdf_url = self.get_pdf(data_cel_msj.get('qr_code', ''))
                get_pdf_url = get_pdf_url.get('data', '').get('download_url', '')
            msg = f"Estimado {data_cel_msj.get('nombre', '')}, {data_cel_msj.get('visita_a', '')}"

            if data_cel_msj.get('fecha_desde', '') and not data_cel_msj.get('fecha_hasta', ''):
                fecha_desde_format = fecha_desde.strftime("%d/%m/%Y a las %H:%M")
                msg += f", te invita a {data_cel_msj.get('ubicacion', '')} el {fecha_desde_format}."
            elif data_cel_msj.get('fecha_desde', '') and data_cel_msj.get('fecha_hasta', ''):
                fecha_desde_format = fecha_desde.strftime("%d/%m/%Y")
                fecha_hasta_format = fecha_hasta.strftime("%d/%m/%Y")
                msg += f", te invita a {data_cel_msj.get('ubicacion', '')} "
                msg += f"del {fecha_desde_format} al {fecha_hasta_format}."

            msg += f" Descarga tu pase: {get_pdf_url}"
            mensaje = msg
        phone_to = data_cel_msj.get('numero', '')
        res =self.lkf_api.send_sms(phone_to, mensaje, use_api_key=True)
        if res:
            return {'status_code':200}
        
    def check_out_all_users(self):
        match_query_visitas = {
            "deleted_at": {"$exists": False},
            "form_id": self.BITACORA_ACCESOS,
            f"answers.{self.PASE_ENTRADA_OBJ_ID}.{self.pase_entrada_fields['status_pase']}": {"$in": ["Activo"]},
            f"answers.{self.bitacora_fields['status_visita']}": "entrada",
        }

        proyect_fields_visitas = {
            '_id': 1,
            'folio': f"$folio",
            'fecha_entrada': f"$answers.{self.mf['fecha_entrada']}",
            'estatus': f"$answers.{self.bitacora_fields['status_visita']}",
        }

        query_visitas = [
            {'$match': match_query_visitas},
            {'$project': proyect_fields_visitas},
        ]

        data = self.format_cr(self.cr.aggregate(query_visitas))

        lista_filtrada = []
        zona_horaria = pytz.timezone('America/Mexico_City')
        fecha_actual = datetime.now(zona_horaria)

        for item in data:
            fecha_entrada_sin_zona = datetime.strptime(item['fecha_entrada'], '%Y-%m-%d %H:%M:%S')
            fecha_entrada = zona_horaria.localize(fecha_entrada_sin_zona)

            diferencia = fecha_actual - fecha_entrada
    
            if diferencia.total_seconds() > 7200:
                lista_filtrada.append(item)

        if lista_filtrada:
            res = self.set_checkout_all_users(lista_filtrada)
        else:
            res = 'No hay registros para hacer checkout...'
        return res

    def set_checkout_all_users(self, data):
        folio_list = []
        for item in data:
            folio_list.append(item['folio'])

        tz_mexico = pytz.timezone('America/Mexico_City')
        now = datetime.now(tz_mexico)
        fecha_hora_str = now.strftime("%Y-%m-%d %H:%M:%S")
        duration = '02:00:00'
        answers = {
            f"{self.bitacora_fields['status_visita']}":'salida',
            f"{self.mf['fecha_salida']}":fecha_hora_str,
            f"{self.mf['duracion']}":duration,
        }

        response = self.lkf_api.patch_multi_record( answers=answers, form_id=self.BITACORA_ACCESOS, folios=folio_list)
        return response

    def create_enviar_msj_pase(self, folio=None):
        access_pass={"enviar_correo": ["enviar_sms"]}
        res_update= self.update_pass(access_pass=access_pass, folio=folio)
        return res_update

    def create_enviar_correo(self, folio=None, envio=[]):
        access_pass={"enviar_correo": envio}
        res_update= self.update_pass(access_pass=access_pass, folio=folio)
        return res_update
     
    def create_failure(self, data_failures):
        #---Define Metadata
        metadata = self.lkf_api.get_metadata(form_id=self.BITACORA_FALLAS)
        metadata.update({
            "properties": {
                "device_properties":{
                    "System": "Script",
                    "Module": "Accesos",
                    "Process": "Creación de fallas",
                    "Action": "create_failure",
                    "File": "accesos/app.py"
                }
            },
        })
        #---Define Answers
        answers = {}
        for key, value in data_failures.items():
            if key == 'falla_ubicacion' or key == 'falla_caseta':
                if data_failures['falla_ubicacion'] and not data_failures['falla_caseta']:
                    answers[self.fallas_fields['falla_ubicacion_catalog']] = {self.fallas_fields['falla_ubicacion']:data_failures['falla_ubicacion']}
                elif data_failures['falla_caseta'] and not data_failures['falla_ubicacion']:
                    answers[self.fallas_fields['falla_ubicacion_catalog']] = {self.fallas_fields['falla_caseta']:data_failures['falla_caseta']}
                elif data_failures['falla_caseta'] and data_failures['falla_ubicacion']: 
                    answers[self.fallas_fields['falla_ubicacion_catalog']] = {self.fallas_fields['falla_ubicacion']:data_failures['falla_ubicacion'],
                    self.fallas_fields['falla_caseta']:data_failures['falla_caseta']}
            elif key == 'falla' or key== 'falla_objeto_afectado':
                answers[self.fallas_fields['falla_catalog']] = {self.fallas_fields['falla']:data_failures['falla'],
                self.fallas_fields['falla_subconcepto']:data_failures['falla_objeto_afectado']}
            elif key == 'falla_reporta_nombre':
                answers[self.fallas_fields['falla_reporta_catalog']] = {self.fallas_fields['falla_reporta_nombre']:value}
            elif key == 'falla_responsable_solucionar_nombre':
                answers[self.fallas_fields['falla_responsable_solucionar_catalog']] = {self.fallas_fields['falla_responsable_solucionar_nombre']:value}
            else:
                answers.update({f"{self.fallas_fields[key]}":value})
        metadata.update({'answers':answers})
        return self.lkf_api.post_forms_answers(metadata)

    def create_incidence(self, data_incidences):
        #---Define Metadata
        metadata = self.lkf_api.get_metadata(form_id=self.BITACORA_INCIDENCIAS)
        metadata.update({
            "properties": {
                "device_properties":{
                    "System": "Script",
                    "Module": "Accesos",
                    "Process": "Creación de incidencias",
                    "Action": "create_incidence",
                    "File": "accesos/app.py"
                }
            },
        })
        print( "Entrando a crear" ,simplejson.dumps(data_incidences, indent=4))
        #---Define Answers
        answers = {}
        answers[self.incidence_fields['incidencia_catalog']]={}
        for key, value in data_incidences.items():
            if key == 'categoria':
                answers[self.incidence_fields['incidencia_catalog']].update({
                    self.incidence_fields['categoria']:data_incidences['categoria']
                })
            elif key == 'sub_categoria':
                answers[self.incidence_fields['incidencia_catalog']].update({
                    self.incidence_fields['sub_categoria']: data_incidences['sub_categoria']
                })
            elif key == 'incidente':
                answers[self.incidence_fields['incidencia_catalog']].update({
                    self.incidence_fields['incidente']: data_incidences['incidente']
                })

            elif key == 'ubicacion_incidencia' or key == 'area_incidencia':
                if data_incidences['ubicacion_incidencia'] and not data_incidences['area_incidencia']:
                    answers[self.incidence_fields['ubicacion_incidencia_catalog']] = {self.incidence_fields['ubicacion_incidencia']:data_incidences['ubicacion_incidencia']}
                elif data_incidences['area_incidencia'] and not data_incidences['ubicacion_incidencia']:
                    answers[self.incidence_fields['ubicacion_incidencia_catalog']] = {self.incidence_fields['area_incidencia']:data_incidences['area_incidencia']}
                elif data_incidences['area_incidencia'] and data_incidences['ubicacion_incidencia']: 
                    answers[self.incidence_fields['ubicacion_incidencia_catalog']] = {self.incidence_fields['ubicacion_incidencia']:data_incidences['ubicacion_incidencia'],
                    self.incidence_fields['area_incidencia']:data_incidences['area_incidencia']}
            elif key == 'reporta_incidencia':
                answers[self.incidence_fields['reporta_incidencia_catalog']] = {self.incidence_fields['reporta_incidencia']:value}
            elif key == 'personas_involucradas_incidencia':
                personas = data_incidences.get('personas_involucradas_incidencia',[])
                if personas:
                    personas_list = []
                    for c in personas:
                        print( "personas listas",c)
                        personas_list.append(
                            {
                                self.incidence_fields['nombre_completo']:c.get('nombre_completo'),
                                self.incidence_fields['rol'] :c.get('rol'),
                                self.incidence_fields['sexo'] :c.get('sexo'),
                                self.incidence_fields['grupo_etario'] :c.get('grupo_etario'),
                                self.incidence_fields['atencion_medica'] :c.get('atencion_medica'),
                                self.incidence_fields['retenido'] :c.get('retenido'),
                                self.incidence_fields['comentarios'] :c.get('comentarios')
                            }
                        )
                    answers.update({self.incidence_fields['personas_involucradas_incidencia']:personas_list})
            elif key == 'acciones_tomadas_incidencia':
                acciones = data_incidences.get('acciones_tomadas_incidencia',[])
                if acciones:
                    acciones_list = []
                    for c in acciones:
                        acciones_list.append(
                            {
                                self.incidence_fields['acciones_tomadas']:c.get('acciones_tomadas'),
                                self.incidence_fields['llamo_a_policia'] :c.get('llamo_a_policia'),
                                self.incidence_fields['autoridad'] :c.get('autoridad'),
                                self.incidence_fields['numero_folio_referencia'] :c.get('numero_folio_referencia'),
                                self.incidence_fields['responsable'] :c.get('responsable'),
                            }
                        )
                    answers.update({self.incidence_fields['acciones_tomadas_incidencia']:acciones_list})
            elif key == 'seguimientos_incidencia':
                seg = data_incidences.get('seguimientos_incidencia',[])
                if seg:
                    seg_list = []
                    for c in seg:
                        seg_list.append(
                            {
                                self.incidence_fields['accion_correctiva_incidencia']:c.get('accion_correctiva_incidencia'),
                                self.incidence_fields['incidencia_personas_involucradas'] :c.get('incidencia_personas_involucradas'),
                                self.incidence_fields['fecha_inicio_seg'] :c.get('fechaInicioIncidenciaCompleta'),
                                self.incidence_fields['incidencia_documento_solucion'] :c.get('incidencia_documento_solucion'),
                                self.incidence_fields['incidencia_evidencia_solucion'] :c.get('incidencia_evidencia_solucion')
                            }
                        )
                    answers.update({self.incidence_fields['seguimientos_incidencia']:seg_list})
            elif key == 'afectacion_patrimonial_incidencia':
                ap = data_incidences.get('afectacion_patrimonial_incidencia',[])
                if ap:
                    ap_list = []
                    for c in ap:
                        ap_list.append(
                            {
                                self.incidence_fields['tipo_afectacion']:c.get('tipo_afectacion'),
                                self.incidence_fields['monto_estimado'] :c.get('monto_estimado'),
                                self.incidence_fields['duracion_estimada'] :c.get('duracion_estimada')
                            }
                        )
                    answers.update({self.incidence_fields['afectacion_patrimonial_incidencia']:ap_list})

            elif key == 'datos_deposito_incidencia':
                depositos = data_incidences.get('datos_deposito_incidencia',[])
                if depositos:
                    depositos_list = []
                    for c in depositos:
                        depositos_list.append(
                            {
                                self.incidence_fields['tipo_deposito']:c.get('tipo_deposito').lower().replace(" ","_"),
                                self.incidence_fields['cantidad'] :c.get('cantidad')
                            }
                        )
                    answers.update({self.incidence_fields['datos_deposito_incidencia']:depositos_list})
            elif key == 'tags':
                tags = data_incidences.get('tags',[])
                if tags:
                    tag_list = []
                    for c in tags:
                        tag_list.append(
                            {
                                self.incidence_fields['tag']:c,
                            }
                        )
                    answers.update({self.incidence_fields['tags']:tag_list})
            elif key == 'prioridad_incidencia':
                answers[self.incidence_fields['prioridad_incidencia']] = f"{value}".lower()
            else:
                answers.update({f"{self.incidence_fields[key]}":value})
        print("categorias", simplejson.dumps(answers, indent=4))
        metadata.update({'answers':answers})
        return self.lkf_api.post_forms_answers(metadata)

    def create_note(self, location, area, data_notes):
        '''
        '''
        #---Define Metadata
        metadata = self.lkf_api.get_metadata(form_id=self.ACCESOS_NOTAS)
        metadata.update({
            "properties": {
                "device_properties":{
                    "System": "Script",
                    "Module": "Accesos",
                    "Process": "Creación de notas",
                    "Action": "Create Note",
                    "File": "accesos/app.py"
                }
            },
        })
        #---Define Answers
        employee = self.get_employee_data(email=self.user.get('email'), get_one=True)
        answers = {
            f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}":{
                self.f['location']:location,
                self.f['area']:area
            },
            f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}":{
                self.f['worker_name']:employee['worker_name'],
            }
                }
        #----Assign Values Keys
        for key, value in data_notes.items():
            if key == 'note_comments':
                answers[self.notes_fields['note_comments_group']] = answers.get(self.notes_fields['note_comments_group'],[])
                for comment in value:
                    answers[self.notes_fields['note_comments_group']].append({self.notes_fields['note_comments']:comment})
            elif  key == 'note_booth':
                answers[self.notes_fields['note_catalog_booth']] = {self.notes_fields['note_booth']:value}
            elif  key == 'note_guard':
                answers[self.notes_fields['note_catalog_guard']] = {self.notes_fields['note_guard']:value}
            else:
                answers.update({f"{self.notes_fields[key]}":value})
        #----Assign Time
        timezone = employee.get('cat_timezone', employee.get('timezone', 'America/Monterrey'))

        fecha_hora_str =self.today_str(timezone, date_format='datetime')
        answers.update({f"{self.notes_fields['note_open_date']}":fecha_hora_str})
        metadata.update({'answers':answers})
        return self.lkf_api.post_forms_answers(metadata)

    def _get_ics_file(self, meetings=[]):
        _logger = logging.getLogger(__name__)

        """Returns iCalendar file for the event invitation.
        :param meetings: List of meetings (each meeting is a dictionary with the required fields).
        :returns: A dict of .ics file content for each meeting.
        """
        result = {}

        def ics_datetime(idate, allday=False, tz_name='UTC'):
            if idate:
                tz = pytz.timezone(tz_name)
                if allday:
                    return idate
                else:
                    return tz.localize(idate)
            return False

        try:
            import vobject
        except ImportError:
            _logger.warning("The `vobject` Python module is not installed, so iCal file generation is unavailable. Please install the `vobject` Python module")
            return result

        for meeting in meetings:
            cal = vobject.iCalendar()

            cal.add('method').value = 'REQUEST'
            
            event = cal.add('vevent')

            if not meeting.get("start") or not meeting.get("stop"):
                raise ValueError("First you have to specify the date of the invitation.")
            
            event.add('created').value = ics_datetime(datetime.now())
            event.add('dtstart').value = ics_datetime(meeting["start"], meeting.get("allday", False), tz_name='America/Mexico_City')
            event.add('dtend').value = ics_datetime(meeting["stop"], meeting.get("allday", False), tz_name='America/Mexico_City')
            event.add('summary').value = meeting["name"]
            if meeting.get("description"):
                event.add('description').value = meeting["description"]
            if meeting.get("location"):
                location_value = meeting["location"]
                if isinstance(location_value, list):
                    location_value = self.format_ubicaciones_to_google_pass(location_value)
                event.add('location').value = location_value
            if meeting.get("rrule"):
                event.add('rrule').value = meeting["rrule"]

            if meeting.get("alarm_ids"):
                for alarm in meeting["alarm_ids"]:
                    valarm = event.add('valarm')
                    interval = alarm["interval"]
                    duration = alarm["duration"]
                    trigger = valarm.add('TRIGGER')
                    trigger.params['related'] = ["START"]
                    if interval == 'days':
                        delta = timedelta(days=duration)
                    elif interval == 'hours':
                        delta = timedelta(hours=duration)
                    elif interval == 'minutes':
                        delta = timedelta(minutes=duration)
                    trigger.value = delta
                    valarm.add('DESCRIPTION').value = alarm.get("name", "Default Alarm")

            # Agregar organizador
            organizer = event.add('organizer')
            organizer.params['CN'] = [meeting['organizer_name']]
            organizer.value = f"MAILTO:{meeting['organizer_email']}"
            
            # Agregar los asistentes (attendees)
            for attendee_data in meeting.get("attendee_ids", []):
                attendee = event.add('attendee')
                attendee.value = "mailto:" + attendee_data.get("email", "")
                
                # Configuración de los parámetros de los asistentes
                attendee.params['CN'] = [attendee_data.get("name", "Unknown")]
                attendee.params['RS'] = ["OPT-PARTICIPANT"]
                attendee.params['CUTYPE'] = ["INDIVIDUAL"]
                attendee.params['ROLE'] = ["REQ-PARTICIPANT"]
                attendee.params['PARTSTAT'] = ["NEEDS-ACTION"]
                attendee.params['RSVP'] = ["TRUE"]
            
            result[meeting["id"]] = cal.serialize().encode('utf-8')

        return result

    def create_access_pass(self, location, access_pass):
        #---Define Metadata
        metadata = self.lkf_api.get_metadata(form_id=self.PASE_ENTRADA)
        metadata.update({
            "properties": {
                "device_properties":{
                    "System": "Script",
                    "Module": "Accesos",
                    "Process": "Creación de pase",
                    "Action": "create_access_pass",
                    "File": "accesos/app.py"
                }
            },
        })

        #---Define Answers
        answers = {}
        perfil_pase = access_pass.get('perfil_pase')
        location_name = access_pass.get('ubicacion')
        if not location:
            location = location_name
        address = self.get_location_address(location_name=location_name)
        access_pass['direccion'] = [address.get('address', '')]
        user_data = self.lkf_api.get_user_by_id(self.user.get('user_id'))
        timezone = user_data.get('timezone','America/Monterrey')
        now_datetime =self.today_str(timezone, date_format='datetime')
        employee = self.get_employee_data(email=self.user.get('email'), get_one=True)
        company = employee.get('company', 'Soter')
        nombre_visita_a = employee.get('worker_name')

        if(access_pass.get('site', '') == 'accesos'):
            nombre_visita_a = access_pass.get('visita_a')
            access_pass['ubicaciones'] = [location]

        answers[self.UBICACIONES_CAT_OBJ_ID] = {}
        # answers[self.UBICACIONES_CAT_OBJ_ID][self.f['location']] = location
        if access_pass.get('custom') == True :
            answers[self.pase_entrada_fields['tipo_visita_pase']] = access_pass.get('tipo_visita_pase',"")
            answers[self.pase_entrada_fields['fecha_desde_visita']] = access_pass.get('fecha_desde_visita',"")
            answers[self.pase_entrada_fields['fecha_desde_hasta']] = access_pass.get('fecha_desde_hasta',"")
            answers[self.pase_entrada_fields['config_dia_de_acceso']] = access_pass.get('config_dia_de_acceso',"")
            answers[self.pase_entrada_fields['config_dias_acceso']] = access_pass.get('config_dias_acceso',"")
            answers[self.pase_entrada_fields['catalago_autorizado_por']] =  {self.pase_entrada_fields['autorizado_por']:nombre_visita_a}
            answers[self.pase_entrada_fields['status_pase']] = access_pass.get('status_pase',"").lower()
            answers[self.pase_entrada_fields['empresa_pase']] = access_pass.get('empresa',"")
            # answers[self.pase_entrada_fields['ubicacion_cat']] = {self.mf['ubicacion']:access_pass['ubicacion'], self.mf['direccion']:access_pass.get('direccion',"")}
            answers[self.pase_entrada_fields['tema_cita']] = access_pass.get('tema_cita',"") 
            answers[self.pase_entrada_fields['descripcion']] = access_pass.get('descripcion',"") 
            answers[self.pase_entrada_fields['config_limitar_acceso']] = access_pass.get('config_limitar_acceso',"") 

        else:
            answers[self.mf['fecha_desde_visita']] = now_datetime
            answers[self.mf['tipo_visita_pase']] = 'fecha_fija'
        answers[self.pase_entrada_fields['tipo_visita']] = 'alta_de_nuevo_visitante'
        answers[self.pase_entrada_fields['walkin_nombre']] = access_pass.get('nombre')
        answers[self.pase_entrada_fields['walkin_email']] = access_pass.get('email', '')
        answers[self.pase_entrada_fields['walkin_empresa']] = access_pass.get('empresa')
        answers[self.pase_entrada_fields['walkin_fotografia']] = access_pass.get('foto')
        answers[self.pase_entrada_fields['walkin_identificacion']] = access_pass.get('identificacion')
        answers[self.pase_entrada_fields['walkin_telefono']] = access_pass.get('telefono', '')
        answers[self.pase_entrada_fields['status_pase']] = access_pass.get('status_pase',"").lower()
        
        if access_pass.get('ubicaciones'):
            ubicaciones = access_pass.get('ubicaciones',[])
            if ubicaciones:
                ubicaciones_list = []
                for ubi in ubicaciones:
                    ubicaciones_list.append(
                        {
                            self.pase_entrada_fields['ubicacion_cat']:{ self.mf["ubicacion"] : ubi}
                        }
                    )
                answers.update({self.pase_entrada_fields['ubicaciones']:ubicaciones_list})
                
        if access_pass.get('comentarios'):
            comm = access_pass.get('comentarios',[])
            if comm:
                comm_list = []
                for c in comm:
                    comm_list.append(
                        {
                            self.pase_entrada_fields['comentario_pase']:c.get('comentario_pase'),
                            self.pase_entrada_fields['tipo_comentario'] :c.get('tipo_comentario').lower()
                        }
                    )
                answers.update({self.pase_entrada_fields['grupo_instrucciones_pase']:comm_list})

        if access_pass.get('areas'):
            areas = access_pass.get('areas',[])
            if areas:
                areas_list = []
                for c in areas:
                    areas_list.append(
                        {
                            self.pase_entrada_fields['commentario_area']:c.get('commentario_area'),
                            self.pase_entrada_fields['area_catalog_normal'] :{self.mf['nombre_area']: c.get('nombre_area')}
                        }
                    )
                answers.update({self.pase_entrada_fields['grupo_areas_acceso']:areas_list})
        #Visita A
        answers[self.mf['grupo_visitados']] = []
        visita_a = access_pass.get('visita_a')
        visita_set = {
            self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID:{
                self.mf['nombre_empleado'] : nombre_visita_a,
                }
            }
        options_vistia = {
              "group_level": 3,
              "startkey": [location, nombre_visita_a],
              "endkey": [location, f"{nombre_visita_a}\n",{}],
            }
        cat_visita = self.catalogo_view(self.CONF_AREA_EMPLEADOS_CAT_ID, self.PASE_ENTRADA, options_vistia)
        if len(cat_visita) > 0:
            cat_visita =  {key: [value,] for key, value in cat_visita[0].items() if value}
        else:
            selector = {}
            selector.update({f"answers.{self.mf['nombre_empleado']}": nombre_visita_a})
            fields = ["_id", f"answers.{self.mf['nombre_empleado']}", f"answers.{self.mf['email_visita_a']}", f"answers.{self.mf['id_usuario']}"]

            mango_query = {
                "selector": selector,
                "fields": fields,
                "limit": 1
            }

            row_catalog = self.lkf_api.search_catalog(self.CONF_AREA_EMPLEADOS_CAT_ID, mango_query)
            if row_catalog:
                visita_set[self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID].update({
                    self.mf['nombre_empleado']: nombre_visita_a,
                    self.mf['email_visita_a']: [row_catalog[0].get(self.mf['email_visita_a'], "")],
                    self.mf['id_usuario']: [row_catalog[0].get(self.mf['id_usuario'], "")],
                })

        visita_set[self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID].update(cat_visita)
        answers[self.mf['grupo_visitados']].append(visita_set)

        # Perfil de Pase
        answers[self.CONFIG_PERFILES_OBJ_ID] = {
            self.mf['nombre_perfil'] : perfil_pase,
        }
        options = {
              "group_level": 2,
              "startkey": [perfil_pase],
              "endkey": [f"{perfil_pase}\n",{}],
            }
        cat_perfil = self.catalogo_view(self.CONFIG_PERFILES_ID, self.PASE_ENTRADA, options)
        if len(cat_perfil) > 0:
            # SE AGREGO ESTA PARTE DEL IF PARA CUANDO SE CREAN PASES DE ENTRADA DESDE SOTER, ya que se ocupa que motivo sea un array
            # CUSTOM == TRUE significa que el pase fue creado desde soter en la pantalla pase.html
            if access_pass.get('custom') == True :
                cat_perfil[0][self.mf['motivo']]= [cat_perfil[0].get(self.mf['motivo'])]
            else:
                cat_perfil[0][self.mf['motivo']]= ["Reunión"]
            cat_perfil = cat_perfil[0]
        answers[self.CONFIG_PERFILES_OBJ_ID].update(cat_perfil)
        if answers[self.CONFIG_PERFILES_OBJ_ID].get(self.mf['nombre_permiso']) and \
           type(answers[self.CONFIG_PERFILES_OBJ_ID][self.mf['nombre_permiso']]) == str:
            answers[self.CONFIG_PERFILES_OBJ_ID][self.mf['nombre_permiso']] = [answers[self.CONFIG_PERFILES_OBJ_ID][self.mf['nombre_permiso']],]

        #---Valor
        metadata.update({'answers':answers})
        res = self.lkf_api.post_forms_answers(metadata)
        qrcode_to_google_pass = ''
        id_forma = ''
        if res.get("status_code") ==200 or res.get("status_code")==201:
            qrcode_to_google_pass = res.get('json', {}).get('id', '')
            link_info=access_pass.get('link', "")
            docs=""
            
            if link_info:
                for index, d in enumerate(link_info["docs"]): 
                    if(d == "agregarIdentificacion"):
                        docs+="iden"
                    elif(d == "agregarFoto"):
                        docs+="foto"
                    if index==0 :
                        docs+="-"
                link_pass= f"{link_info['link']}?id={res.get('json')['id']}&user={link_info['creado_por_id']}&docs={docs}"
                id_forma = self.PASE_ENTRADA
                id_campo = self.pase_entrada_fields['archivo_invitacion']

                tema_cita = access_pass.get("tema_cita")
                descripcion = access_pass.get("descripcion")
                fecha_desde_visita = access_pass.get("fecha_desde_visita")
                fecha_desde_hasta = access_pass.get("fecha_desde_hasta")
                creado_por_email = access_pass.get("link", {}).get("creado_por_email")
                ubicacion = access_pass.get("ubicacion")
                nombre = access_pass.get("nombre")
                visita_a = access_pass.get("visita_a")
                email = access_pass.get("email")

                start_datetime = datetime.strptime(fecha_desde_visita, "%Y-%m-%d %H:%M:%S")

                if not fecha_desde_hasta:
                    stop_datetime = start_datetime + timedelta(hours=1)
                    meeting = [
                        {
                            "id": 1,
                            "start": start_datetime,
                            "stop": stop_datetime,
                            "name": tema_cita,
                            "description": descripcion,
                            "location": ubicacion,
                            "allday": False,
                            "rrule": None,
                            "alarm_ids": [{"interval": "minutes", "duration": 10, "name": "Reminder"}],
                            'organizer_name': visita_a,
                            'organizer_email': creado_por_email,
                            "attendee_ids": [{"email": email, "nombre": nombre}, {"email": creado_por_email, "nombre": visita_a}],
                        }
                    ]

                    try:
                        respuesta_ics = self.upload_ics(id_forma, id_campo, meetings=meeting)
                    except Exception as e:
                        print(f"Error al generar o subir el archivo ICS: {e}")
                        respuesta_ics = {}

                    file_name = respuesta_ics.get('file_name', '')
                    file_url = respuesta_ics.get('file_url', '')

                    access_pass_custom={
                        "link":link_pass,
                        "enviar_correo_pre_registro": access_pass.get("enviar_correo_pre_registro",[]),
                        "archivo_invitacion": [
                            {
                                "file_name": f"{file_name}",
                                "file_url": f"{file_url}"
                            }
                        ]
                    }
                else:
                    access_pass_custom={
                        "link":link_pass,
                        "enviar_correo_pre_registro": access_pass.get("enviar_correo_pre_registro",[])
                    }

                data_to_google_pass = {
                    "nombre": access_pass.get("nombre"),
                    "visita_a": access_pass.get("visita_a"),
                    "ubicacion": access_pass.get("ubicaciones"),
                    "address": address.get('address'),
                    "empresa": company,
                    "all_data": access_pass
                }

                id_campo_pdf_to_img = self.pase_entrada_fields['pdf_to_img']
                pdf = self.lkf_api.get_pdf_record(qrcode_to_google_pass, template_id = 491, name_pdf='Pase de Entrada', send_url=True)
                pdf_url = pdf.get('json', {}).get('download_url')

                google_wallet_pass_url = self.create_class_google_wallet(data=data_to_google_pass, qr_code=qrcode_to_google_pass)
                pass_img_url = self.upload_pdf_as_image(id_forma, id_campo_pdf_to_img, pdf_url)
                pass_img_file_name = pass_img_url.get('file_name')
                pass_img_file_url = pass_img_url.get('file_url')
                
                access_pass_custom.update({
                    "google_wallet_pass_url": google_wallet_pass_url,
                    "pdf_to_img": [
                        {
                            "file_name": pass_img_file_name,
                            "file_url": pass_img_file_url
                        }
                    ]
                })
                
                self.update_pass(access_pass=access_pass_custom, folio=res.get("json")["id"])
            
        return res
    
    def create_visita_autorizada(self, visita_autorizada_obj, pase_obj={}):
        pase_info = pase_obj
        #---Define Metadata
        metadata = self.lkf_api.get_metadata(form_id=self.VISITA_AUTORIZADA)
        metadata.update({
            "properties": {
                "device_properties":{
                    "System": "Script",
                    "Module": "Accesos",
                    "Process": "Creación de visita autorizada",
                    "Action": "create_visita_autorizada",
                    "File": "accesos/app.py"
                }
            },
        })

        #---Define Answers
        answers = {}
        nombre_completo = visita_autorizada_obj.get('nombre_completo', '')
        curp = visita_autorizada_obj.get('curp', '')
        direccion = visita_autorizada_obj.get('direccion', '')
        nss = visita_autorizada_obj.get('nss', '')

        email = pase_info.get('email', '')
        telefono = pase_info.get('telefono', '')
        fotografia = pase_info.get('fotografia',[])
        identificacion = pase_info.get('identificacion',[])
        
        answers[self.mf['nombre_visita']] = nombre_completo
        answers[self.mf['curp']] = curp
        answers[self.mf['email_vista']] = email
        answers[self.mf['telefono_visita']] = telefono
        answers[self.mf['foto']] = fotografia
        answers[self.mf['identificacion']] = identificacion
        answers[self.mf['direccion_visita']] = direccion
        answers[self.mf['nss']] = nss

        metadata.update({'answers':answers})
        res = self.lkf_api.post_forms_answers(metadata)
        if res.get("status_code") ==200 or res.get("status_code")==201:
            print(res)
        else:
            print("Error al ejecutar el post_forms_answers en create_visita_autorizada")
        return res

    def format_seguimiento_fallas(self, data):
        res = []
        for r in data:
            row = {}
            row['accion_correctiva'] = r.get(self.fallas_fields['falla_folio_accion_correctiva'],'')
            row['comentario'] = r.get(self.fallas_fields['falla_comentario_solucion'],'')
            row['evidencia'] = r.get(self.fallas_fields['falla_evidencia_solucion'],'')
            row['documento'] = r.get(self.fallas_fields['falla_documento_solucion'],'')
            row['fecha_inicio'] = r.get(self.fallas_fields['falla_inicio_seguimiento'],'')
            row['fecha_fin'] = r.get(self.fallas_fields['falla_fin_seguimiento'],'')
            res.append(row)
        return res

    def format_seguimiento_incidencias(self, data):
        res = []
        for r in data:
            row = {}
            row['accion_correctiva_incidencia'] = r.get(self.incidence_fields['accion_correctiva_incidencia'],'')
            row['incidencia_personas_involucradas'] = r.get(self.incidence_fields['incidencia_personas_involucradas'],'')
            row['fecha_inicio_seg'] = r.get(self.incidence_fields['fecha_inicio_seg'],'')
            row['incidencia_documento_solucion'] = r.get(self.incidence_fields['documento_accion_correctiva_incidencia'],'')
            row['incidencia_evidencia_solucion'] = r.get(self.incidence_fields['evidencia_accion_correctiva_incidencia'],'')
            res.append(row)
        return res
    
    def format_tags_incidencias(self, data):
        res = []
        for r in data:
            tag = r.get(self.incidence_fields['tag'], '')
            if tag:
                res.append(tag)
        return res

    def format_personas_involucradas(self, data):
        res = []
        for r in data:
            row = {}
            row['nombre_completo'] = r.get(self.incidence_fields['nombre_completo'],'')
            row['rol'] = r.get(self.incidence_fields['rol'],'')
            row['sexo'] = r.get(self.incidence_fields['sexo'],'')
            row['grupo_etario'] = r.get(self.incidence_fields['grupo_etario'],'')
            row['atencion_medica'] = r.get(self.incidence_fields['atencion_medica'],'')
            row['retenido'] = r.get(self.incidence_fields['retenido'],'')
            res.append(row)
        return res

    def format_datos_deposito(self, data):
        res = []
        for r in data:
            row = {}
            row['tipo_deposito'] = r.get(self.incidence_fields['tipo_deposito'],'').title().replace('_', ' ')
            row['cantidad'] = r.get(self.incidence_fields['cantidad'],'')
            res.append(row)
        return res

    def format_acciones(self, data):
        res = []
        for r in data:
            row = {}
            row['acciones_tomadas'] = r.get(self.incidence_fields['acciones_tomadas'],'')
            row['llamo_a_policia'] = r.get(self.incidence_fields['llamo_a_policia'],'')
            row['autoridad'] = r.get(self.incidence_fields['autoridad'],'')
            row['numero_folio_referencia'] = r.get(self.incidence_fields['numero_folio_referencia'],'')
            row['responsable'] = r.get(self.incidence_fields['responsable'],'')
            res.append(row)
        return res
    def format_afectacion_patrimonial(self, data):
        res = []
        for r in data:
            row = {}
            row['tipo_afectacion'] = r.get(self.incidence_fields['tipo_afectacion'],'')
            row['monto_estimado'] = r.get(self.incidence_fields['monto_estimado'],'')
            row['duracion_estimada'] = r.get(self.incidence_fields['duracion_estimada'],'')
            res.append(row)
        return res

    def format_comentarios(self, data):
        res = []
        for r in data:
            row = {}
            row['comentario'] = r.get(self.bitacora_fields['comentario'],'')
            row['tipo_comentario'] = r.get(self.bitacora_fields['tipo_comentario'],'').title()
            res.append(row)
        return res

    def format_equipos(self, data):
        res = []
        for r in data:
            row = {}
            row['modelo_articulo'] = r.get(self.mf['modelo_articulo'],'')
            row['marca_articulo'] = r.get(self.mf['marca_articulo'],'')
            row['numero_serie'] = r.get(self.mf['numero_serie'],'')
            row['nombre_articulo'] = r.get(self.mf['nombre_articulo'],'')
            row['tipo_equipo'] = r.get(self.mf['tipo_equipo'],'Computo').title()
            row['color_articulo'] = r.get(self.mf['color_articulo'],'').title()
            res.append(row)
        return res

    def format_gafete(self, data):
        res = []
        for r in data:
            row = {}
            row['_id'] = r.get('_id')
            row['ubicacion'] = r.get(self.f['location'])
            row['gafete_id'] = r.get(self.gafetes_fields['gafete_id'])
            row['status'] = r.get(self.mf['status_gafete'])
            row['area'] = r.get(self.f['area'])
            res.append(row)
        return res

    def format_lockers(self, data):
        res = []
        for r in data:
            row = {}
            row['_id'] = r.get('_id')
            row['ubicacion'] = r.get(self.f['location'])
            row['locker_id'] = r.get(self.mf['locker_id'])
            row['status'] = r.get(self.mf['status_locker'])
            row['tipo_locker'] = r.get(self.mf['tipo_locker'])
            row['area'] = r.get(self.f['area'])
            res.append(row)
        return res

    def format_perfil_pase(self, perfil_pase, id_user=None, empresa=None):
        certificaciones = []
        if not perfil_pase.get('nombre_permiso') :
            return {}
        for idx, name in enumerate(perfil_pase.get('nombre_permiso',[])):
            cert = {}
            cert['nombre_certificacion'] = name
            vigencia = perfil_pase.get('vigencia_certificado',[])
            if len(vigencia) >= (idx+1):
                cert.update({'vigencia':vigencia[idx]})
            tipo_vigencia = perfil_pase.get('vigencia_certificado_en',[])
            if len(tipo_vigencia) >= (idx+1):
                cert.update({'tipo_vigencia':tipo_vigencia[idx]})
            if id_user:
                z = self.get_valiaciones_certificado(name, id_user, empresa)
                cert['status'] = z
            certificaciones.append(cert)
        return certificaciones

    def format_vehiculos(self, data):
        res = []
        for v in data:
            row = {}
            row['color'] = v.get(self.mf['color_vehiculo'],'').title()
            row['placas'] = v.get(self.mf['placas_vehiculo'],'')
            row['tipo'] = v.get('tipo_vehiculo','')
            row['marca_vehiculo'] = v.get(self.mf['marca_vehiculo'],'')
            row['modelo_vehiculo'] = v.get(self.mf['modelo_vehiculo'],'')
            row['nombre_estado'] = v.get('state','')
            res.append(row)
        return res

    def format_vehiculos_simple(self, data):
        res = []
        for v in data:
            row = {}
            row['color'] = v.get('color_vehiculo','') or v.get('color','') or  v.get(self.mf['color_vehiculo'],'')or ''
            row['placas'] = v.get('placas_vehiculo','') or v.get('placas','')  or v.get(self.mf['placas_vehiculo'],'')or  ''
            row['tipo'] = v.get('tipo_vehiculo','') or v.get('tipo','') or v.get(self.mf['tipo_vehiculo'],'') or ''
            row['marca'] = v.get('marca_vehiculo','') or v.get(self.mf['marca_vehiculo'],'') or ''
            row['modelo'] = v.get('modelo_vehiculo','') or v.get(self.mf['modelo_vehiculo'],'') or ''
            row['estado'] = v.get('nombre_estado','')or v.get('state','') or v.get(self.mf['nombre_estado'],'') or ''
            res.append(row)
        return res

    def format_equipos_simple(self, data):
        res = []
        for r in data:
            row = {}
            row['modelo'] = r.get('modelo_articulo','')  or r.get(self.mf['marca_articulo'],'') or ''
            row['marca'] = r.get('marca_articulo','') or r.get(self.mf['marca_articulo'],'') or ''
            row['serie'] = r.get('numero_serie','') or r.get(self.mf['numero_serie'],'') or''
            row['nombre'] = r.get('nombre_articulo','') or r.get(self.mf['nombre_articulo'],'') or ''
            row['tipo'] = r.get('tipo_equipo','').title() or r.get(self.mf['tipo_equipo'],'') or ''
            row['color'] = r.get('color_articulo','').title() or r.get(self.mf['color_articulo'],'') or ''
            res.append(row)
        return res

    def format_vehiculos_last_move(self, data):
        res = []
        for v in data:
            row = {}
            row['color_vehiculo'] = v.get('color','').title()
            row['placas_vehiculo'] = v.get('placas','')
            row['tipo_vehiculo'] = v.get('tipo','')
            row['marca_vehiculo'] = v.get('marca_vehiculo','')
            row['modelo_vehiculo'] = v.get('modelo_vehiculo','')
            row['nombre_estado'] = v.get('nombre_estado','')
            res.append(row)
        return res

    def format_visita(self, data):
        res = []
        for r in data:
            row = {}
            row['user_id']=self.unlist(r.get('user_id',[])) or ""
            row['nombre']=self.unlist(r.get('note_guard',[])) or ""
            row['departamento']=self.unlist(r.get('worker_department',[])) or ""
            row['posicion']=self.unlist(r.get('worker_position',[])) or ""
            row['email']=self.unlist(r.get('email',[])) or ""
            res.append(row)
        return res

    def get_access_pass(self, qr_code):
        # Obtiene el pase de acceso con el código QR.

        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.CHECKIN_CASETAS,
            }
        if _id:
            match_query.update({"_id":ObjectId(_id)})

    def get_access_notes(self, location_name, area_name):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.ACCESOS_NOTAS,
            f"answers.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['location']}":location_name,
            f"answers.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['area']}":area_name
            }
        query = [
            {'$match': match_query },
            {'$project': self.project_format(self.notes_project_fields)},
            {'$sort':{self.f['note_open_date']:1}}
            ]
        return self.format_cr_result(self.cr.aggregate(query))

    def get_booths_guards(self, location=None, area=None, solo_disponibles=False, **kwargs):
        res = {}
        if not area:
            default_booth , user_booths = self.get_user_booth(search_default=False)
            location = default_booth.get('location')
            area = default_booth.get('area')
        guards_positions = self.config_get_guards_positions()
        if not guards_positions:
            self.LKFException({"status_code":400, "msg":'No Existen puestos de guardias configurados.'})
        for guard_type in guards_positions:
            puesto = guard_type['tipo_de_guardia']
            if kwargs.get('position') and kwargs['position'] != puesto:
                continue
            res[puesto] = res.get(puesto,
                self.get_users_by_location_area(location, area, **{'position': guard_type['puestos']})
                )
        uids = []
        for pos, user in res.items():
            uids += [x['user_id'] for x in user]
        
        pics = self.get_employee_pic(uids)
        for pos, user in res.items():
            for x in user:
                if x['user_id'] in list(pics.keys()):
                    x['picture'] = pics[x['user_id']]
        if solo_disponibles:
            uids = []
            disponibles = []
            for pos, user in res.items():
                for x in user:
                    if x['user_id'] not in uids:
                        uids.append(x['user_id'])
            active_employees = self.get_employee_checkin_status(uids)
            uids = []    
            for uid, user_st in active_employees.items():
                uids.append(uid)
                user_status = user_st.get('status')
                if user_st.get('status') == 'out':
                    disponibles.append(uid)
            res_disp = {}
            for pos, user in res.items():
                for x in user:
                    if x['user_id'] in disponibles:
                        res_disp[pos] = res_disp.get(pos,[])
                        res_disp[pos].append(x)
                    elif x['user_id'] not in uids:
                        res_disp[pos] = res_disp.get(pos,[])
                        res_disp[pos].append(x)
            res = res_disp
        return res

    def get_booth_status(self, booth_area, location):
        last_chekin = self.get_last_checkin(location, booth_area)
        booth_status = {
            "status":'Disponible',
            "guard_on_dutty":'',
            "user_id":'',
            "stated_at":'',
            }
        if last_chekin.get('checkin_type') in ['entrada','apertura']:
            #todo
            #user_id 
            booth_status['status'] = 'No Disponible'
            booth_status['guard_on_dutty'] = last_chekin.get('employee') 
            booth_status['stated_at'] = last_chekin.get('boot_checkin_date')
            booth_status['checkin_id'] = last_chekin['_id']
        return booth_status

    def get_booth_stats(self, booth_area, location):
        res ={
                "in_invitees":11,
                "articulos_concesionados":12,
                "incidentes_pendites": 13,
                "vehiculos_estacionados": 14,
                "gefetes_pendientes": 15,
            }
        return res
    
    def get_page_stats(self, booth_area, location, page=''):
        timezone = pytz.timezone('America/Mexico_City')
        today = datetime.now(timezone).strftime("%Y-%m-%d")        
        res={}

        if page == 'Turnos':
            #Visitas dentro, Gafetes pendientes y Vehiculos estacionados
            query_visitas = [
                {'$match': {
                    "deleted_at": {"$exists": False},
                    "form_id": self.BITACORA_ACCESOS,
                    f"answers.{self.bitacora_fields['status_visita']}": "entrada",
                    f"answers.{self.PASE_ENTRADA_OBJ_ID}.{self.pase_entrada_fields['status_pase']}": {"$in": ["Activo"]},
                    f"answers.{self.bitacora_fields['caseta_entrada']}": booth_area,
                    f"answers.{self.bitacora_fields['ubicacion']}": location,
                    f"answers.{self.mf['fecha_entrada']}": {"$gte": f"{today} 00:00:00", "$lte": f"{today} 23:59:59"}
                }},
                {'$project': {
                    '_id': 1,
                    'vehiculos': {"$ifNull": [f"$answers.{self.mf['grupo_vehiculos']}", []]},
                    'id_gafete': f"$answers.{self.GAFETES_CAT_OBJ_ID}.{self.gafetes_fields['gafete_id']}",
                    'status_gafete': f"$answers.{self.mf['status_gafete']}"
                }},
                {'$group': {
                    '_id': None,
                    'total_visitas_dentro': {'$sum': 1},
                    'total_vehiculos_dentro': {'$sum': {'$size': '$vehiculos'}},
                    'gafetes_info': {
                        '$push': {
                            'id_gafete':'$id_gafete',
                            'status_gafete':'$status_gafete'
                        }
                    }
                }}
            ]

            resultado = self.format_cr(self.cr.aggregate(query_visitas))
            total_vehiculos_dentro = resultado[0]['total_vehiculos_dentro'] if resultado else 0
            total_visitas_dentro = resultado[0]['total_visitas_dentro'] if resultado else 0
            gafetes_info = resultado[0]['gafetes_info'] if resultado else []
            gafetes_pendientes = sum(1
                for gafete in gafetes_info
                    if gafete.get('id_gafete') and gafete.get('status_gafete', '').lower() != 'entregado'
            )
            
            res['total_vehiculos_dentro'] = total_vehiculos_dentro
            res['in_invitees'] = total_visitas_dentro
            res['gafetes_pendientes'] = gafetes_pendientes

            #Articulos concesionados
            query_concesionados = [
                {'$match': {
                    "deleted_at": {"$exists": False},
                    "form_id": self.CONCESSIONED_ARTICULOS,
                    f"answers.{self.UBICACIONES_CAT_OBJ_ID}.{self.mf['ubicacion']}": location,
                }},
                {'$project': {
                    '_id': 1,
                }},
                {'$group': {
                    '_id': None,
                    'articulos_concesionados': {'$sum': 1}
                }}
            ]

            resultado = self.format_cr(self.cr.aggregate(query_concesionados))
            articulos_concesionados = resultado[0]['articulos_concesionados'] if resultado else 0
            
            res['articulos_concesionados'] = articulos_concesionados

            #Incidentes pendientes
            query_incidentes = [
                {'$match': {
                    "deleted_at": {"$exists": False},
                    "form_id": self.BITACORA_INCIDENCIAS,
                    f"answers.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.incidence_fields['area_incidencia']}": booth_area,
                    f"answers.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.incidence_fields['ubicacion_incidencia']}": location
                }},
                {'$project': {
                    '_id': 1,
                    'acciones_tomadas_incidencia': f"$answers.{self.incidence_fields['acciones_tomadas_incidencia']}",
                }},
                {'$group': {
                    '_id': None,
                    'incidentes_pendientes': {'$sum': {'$cond': [{'$or': [{'$eq': [{'$size': {'$ifNull': ['$acciones_tomadas_incidencia', []]}}, 0]},{'$eq': ['$acciones_tomadas_incidencia', None]}]}, 1, 0]}}
                }}
            ]

            resultado = self.format_cr(self.cr.aggregate(query_incidentes))
            incidentes_pendientes = resultado[0]['incidentes_pendientes'] if resultado else 0
            
            res['incidentes_pendites'] = incidentes_pendientes

            #Fallas pendientes
            query_fallas = [
                {'$match': {
                    "deleted_at": {"$exists": False},
                    "form_id": self.BITACORA_FALLAS,
                    f"answers.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.fallas_fields['falla_caseta']}": booth_area,
                    f"answers.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.fallas_fields['falla_ubicacion']}": location,
                    f"answers.{self.fallas_fields['falla_estatus']}": 'abierto',
                    # f"answers.{self.incidence_fields['fecha_hora_incidencia']}": {"$gte": today,"$lt": f"{today}T23:59:59"}
                }},
                {'$project': {
                    '_id': 1,
                }},
                {'$group': {
                    '_id': None,
                    'fallas_pendientes': {'$sum': 1}
                }}
            ]

            resultado = self.format_cr(self.cr.aggregate(query_fallas))
            fallas_pendientes = resultado[0]['fallas_pendientes'] if resultado else 0

            res['fallas_pendientes'] = fallas_pendientes

        elif page == 'Accesos' or page == 'Bitacoras':
            #Visitas en el dia, personal dentro, vehiculos dentro, salidas registradas y personas dentro
            match_query_one = {
                "deleted_at": {"$exists": False},
                "form_id": self.BITACORA_ACCESOS,
                f"answers.{self.PASE_ENTRADA_OBJ_ID}.{self.pase_entrada_fields['status_pase']}": {"$in": ["Activo"]},
                f"answers.{self.bitacora_fields['ubicacion']}": location,
            }

            match_query_two = {
                "deleted_at": {"$exists": False},
                "form_id": self.BITACORA_ACCESOS,
                f"answers.{self.PASE_ENTRADA_OBJ_ID}.{self.pase_entrada_fields['status_pase']}": {"$in": ["Activo"]},
                f"answers.{self.bitacora_fields['ubicacion']}": location,
                f"answers.{self.mf['fecha_entrada']}": {"$gte": f"{today} 00:00:00", "$lte": f"{today} 23:59:59"}
            }

            if not booth_area == 'todas' and booth_area:
                match_query_one.update({
                    f"answers.{self.bitacora_fields['caseta_entrada']}": booth_area,
                })
                match_query_two.update({
                    f"answers.{self.bitacora_fields['caseta_entrada']}": booth_area,
                })

            query_visitas = [
                {'$match': match_query_one},
                {'$project': {
                    '_id': 1,
                    'vehiculos': {"$ifNull": [f"$answers.{self.mf['grupo_vehiculos']}", []]},
                    'equipos': {"$ifNull": [f"$answers.{self.mf['grupo_equipos']}", []]},
                    'perfil': f"$answers.{self.PASE_ENTRADA_OBJ_ID}.{self.mf['nombre_perfil']}",
                    'status_visita': f"$answers.{self.bitacora_fields['status_visita']}",
                    'fecha_salida': f"$answers.{self.mf['fecha_salida']}"
                }},
                {'$group': {
                    '_id': None,
                    'visitas_en_dia': {'$sum': 1},
                    'total_vehiculos_dentro': {
                        '$sum': {
                            '$cond': {
                                'if': {'$eq': ['$status_visita', 'entrada']},
                                'then': {'$size': '$vehiculos'},
                                'else': 0
                            }
                        }
                    },
                    'total_equipos_dentro': {
                        '$sum': {
                            '$cond': {
                                'if': {'$eq': ['$status_visita', 'entrada']},
                                'then': {'$size': '$equipos'},
                                'else': 0
                            }
                        }
                    },
                    'detalle_visitas': {
                        '$push': {
                            'perfil': '$perfil',
                            'status_visita': '$status_visita',
                            'fecha_salida': '$fecha_salida'
                        }
                    }
                }}
            ]

            query_visitas_dia = [
                {'$match': match_query_two},
                {'$project': {
                    '_id': 1,
                    'vehiculos': {"$ifNull": [f"$answers.{self.mf['grupo_vehiculos']}", []]},
                    'equipos': {"$ifNull": [f"$answers.{self.mf['grupo_equipos']}", []]},
                    'perfil': f"$answers.{self.PASE_ENTRADA_OBJ_ID}.{self.mf['nombre_perfil']}",
                    'status_visita': f"$answers.{self.bitacora_fields['status_visita']}"
                }},
                {'$group': {
                    '_id': None,
                    'visitas_en_dia': {'$sum': 1},
                    'total_vehiculos_dentro': {
                        '$sum': {
                            '$cond': {
                                'if': {'$eq': ['$status_visita', 'entrada']},
                                'then': {'$size': '$vehiculos'},
                                'else': 0
                            }
                        }
                    },
                    'total_equipos_dentro': {
                        '$sum': {
                            '$cond': {
                                'if': {'$eq': ['$status_visita', 'entrada']},
                                'then': {'$size': '$equipos'},
                                'else': 0
                            }
                        }
                    },
                    'detalle_visitas': {
                        '$push': {
                            'perfil': '$perfil',
                            'status_visita': '$status_visita'
                        }
                    }
                }}
            ]

            resultado = self.format_cr(self.cr.aggregate(query_visitas))
            today_salida = f"{today} 00:00:00"
            resultado_dia = self.format_cr(self.cr.aggregate(query_visitas_dia))

            total_vehiculos_dentro = resultado[0]['total_vehiculos_dentro'] if resultado else 0
            total_equipos_dentro = resultado[0]['total_equipos_dentro'] if resultado else 0
            detalle_visitas_todas = resultado[0]['detalle_visitas'] if resultado else []
            visitas_en_dia = resultado_dia[0]['visitas_en_dia'] if resultado_dia else 0

            personal_dentro = 0
            salidas = 0
            personas_dentro = 0

            for visita in detalle_visitas_todas:
                status_visita = visita['status_visita'].lower()

                if status_visita == "entrada":
                    personas_dentro += 1
                    
                if visita.get('fecha_salida') and visita.get('fecha_salida') >= today_salida:
                    salidas += 1

            res['total_vehiculos_dentro'] = total_vehiculos_dentro
            res['total_equipos_dentro'] = total_equipos_dentro
            res['visitas_en_dia'] = visitas_en_dia
            res['personal_dentro'] = personal_dentro
            res['salidas_registradas'] = salidas
            res['personas_dentro'] = personas_dentro

            query_paqueteria = [
                {'$match': {
                    "deleted_at": {"$exists": False},
                    "form_id": self.PAQUETERIA,
                    f"answers.{self.paquetes_fields['estatus_paqueteria']}": "guardado",
                    f"answers.{self.paquetes_fields['fecha_recibido_paqueteria']}": {"$gte": f"{today} 00:00:00", "$lte": f"{today} 23:59:59"}
                }},
                {'$project': {
                    '_id': 1,
                }},
                {'$group': {
                    '_id': None,
                    'paquetes_recibidos': {'$sum': 1},
                }}
            ]

            resultado_paquetes = self.format_cr(self.cr.aggregate(query_paqueteria))
            paquetes_recibidos = resultado_paquetes[0]['paquetes_recibidos'] if resultado_paquetes else 0

            res['paquetes_recibidos'] = paquetes_recibidos

        elif page == 'Incidencias':
            #Incidentes por dia, por semana y por mes
            now = datetime.now(pytz.timezone("America/Mexico_City"))
            today_date = now.date()
            user_data = self.lkf_api.get_user_by_id(self.user.get('user_id'))
            zona = user_data.get('timezone','America/Monterrey')
            dateFromWeek, dateToWeek = self.get_range_dates('this_week', zona)

            match_query_incidentes = {
                "deleted_at": {"$exists": False},
                "form_id": self.BITACORA_INCIDENCIAS,
            }

            if location:
                match_query_incidentes.update({
                    f"answers.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.incidence_fields['ubicacion_incidencia']}": location,
                })
            if booth_area:
                match_query_incidentes.update({
                    f"answers.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.incidence_fields['area_incidencia']}": booth_area,
                })

            query_incidentes = [
                {'$match': match_query_incidentes},
                {'$addFields': {
                    'fecha_incidencia': {
                        '$dateFromString': {
                            'dateString': f"$answers.{self.incidence_fields['fecha_hora_incidencia']}",
                            'format': "%Y-%m-%d %H:%M:%S"
                        }
                    }
                }},
                {'$facet': {
                    'por_dia': [
                        {'$match': {
                            'fecha_incidencia': {
                                '$gte': datetime.combine(today_date, time.min),
                                '$lte': datetime.combine(today_date, time.max)
                            }
                        }},
                        {'$count': 'incidentes_x_dia'}
                    ],
                    'por_semana': [
                        {'$match': {
                            'fecha_incidencia': {
                                '$gte': dateFromWeek,
                                '$lte': dateToWeek
                            }
                        }},
                        {'$group': {
                            '_id': {
                                'year': {'$isoWeekYear': '$fecha_incidencia'},
                                'week': {'$isoWeek': '$fecha_incidencia'}
                            },
                            'incidentes_x_semana': {'$sum': 1}
                        }}
                    ],
                    'por_mes': [
                        {'$match': {
                            'fecha_incidencia': {
                                '$gte': datetime.combine(today_date.replace(day=1), time.min),
                                '$lte': datetime.combine(today_date, time.max)
                            }
                        }},
                        {'$group': {
                            '_id': {
                                'year': {'$year': '$fecha_incidencia'},
                                'month': {'$month': '$fecha_incidencia'}
                            },
                            'incidentes_x_mes': {'$sum': 1}
                        }}
                    ]
                }}
            ]

            resultado = self.format_cr(self.cr.aggregate(query_incidentes))[0]

            res['incidentes_x_dia'] = resultado['por_dia'][0]['incidentes_x_dia'] if resultado['por_dia'] else 0
            res['incidentes_x_semana'] = resultado['por_semana'][0]['incidentes_x_semana'] if resultado['por_semana'] else 0
            res['incidentes_x_mes'] = resultado['por_mes'][0]['incidentes_x_mes'] if resultado['por_mes'] else 0

            match_query_fallas = {
                "deleted_at": {"$exists": False},
                "form_id": self.BITACORA_FALLAS,
                f"answers.{self.fallas_fields['falla_estatus']}": 'abierto',
            }

            if location:
                match_query_fallas.update({
                    f"answers.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.fallas_fields['falla_ubicacion']}": location,
                })
            if booth_area:
                match_query_fallas.update({
                    f"answers.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.fallas_fields['falla_caseta']}": booth_area,
                })

            #Fallas pendientes
            query_fallas = [
                {'$match': match_query_fallas},
                {'$project': {
                    '_id': 1,
                }},
                {'$group': {
                    '_id': None,
                    'fallas_pendientes': {'$sum': 1}
                }}
            ]

            resultado = self.format_cr(self.cr.aggregate(query_fallas))
            fallas_pendientes = resultado[0]['fallas_pendientes'] if resultado else 0

            res['fallas_pendientes'] = fallas_pendientes
        elif page == 'Articulos':
            #Articulos concesionados pendientes
            query_concesionados = [
                {'$match': {
                    "deleted_at": {"$exists": False},
                    "form_id": self.CONCESSIONED_ARTICULOS,
                    f"answers.{self.UBICACIONES_CAT_OBJ_ID}.{self.mf['ubicacion']}": location,
                    f"answers.{self.consecionados_fields['status_concesion']}": "abierto",
                }},
                {'$project': {
                    '_id': 1,
                }},
                {'$group': {
                    '_id': None,
                    'articulos_concesionados_pendientes': {'$sum': 1}
                }}
            ]

            resultado = self.format_cr(self.cr.aggregate(query_concesionados))
            articulos_concesionados_pendientes = resultado[0]['articulos_concesionados_pendientes'] if resultado else 0
            
            res['articulos_concesionados_pendientes'] = articulos_concesionados_pendientes

            #Articulos perdidos
            query_perdidos = [
                {'$match': {
                    "deleted_at": {"$exists": False},
                    "form_id": self.BITACORA_OBJETOS_PERDIDOS,
                    f"answers.{self.AREAS_DE_LAS_UBICACIONES_SALIDA_OBJ_ID}.{self.perdidos_fields['ubicacion_perdido']}": location,
                    f"answers.{self.AREAS_DE_LAS_UBICACIONES_SALIDA_OBJ_ID}.{self.perdidos_fields['area_perdido']}": booth_area,
                }},
                {'$project': {
                    '_id': 1,
                    'status_perdido': f"$answers.{self.perdidos_fields['estatus_perdido']}",
                }},
                {'$group': {
                    '_id': None,
                    'perdidos_info': {
                        '$push': {
                            'status_perdido':'$status_perdido'
                        }
                    }
                }}
            ]

            resultado = self.format_cr(self.cr.aggregate(query_perdidos))
            perdidos_info = resultado[0]['perdidos_info'] if resultado else []

            articulos_perdidos = 0
            for perdido in perdidos_info:
                status_perdido = perdido.get('status_perdido', '').lower()
                if status_perdido not in ['entregado', 'donado']:
                    articulos_perdidos += 1

            res['articulos_perdidos'] = articulos_perdidos

            match_query_paqueteria = {
                "deleted_at": {"$exists": False},
                "form_id": self.PAQUETERIA,
                f"answers.{self.paquetes_fields['estatus_paqueteria']}": "guardado",
            }

            if location:
                match_query_paqueteria.update({
                    f"answers.{self.paquetes_fields['ubicacion_paqueteria']}": location,
                })
            if booth_area and not booth_area == "todas" and not booth_area == "":
                match_query_paqueteria.update({
                    f"answers.{self.paquetes_fields['area_paqueteria']}": booth_area,
                })

            query_paqueteria = [
                {'$match': match_query_paqueteria },
                {'$project': {
                    '_id': 1,
                }},
                {'$group': {
                    '_id': None,
                    'paquetes_recibidos': {'$sum': 1},
                }}
            ]

            resultado_paquetes = self.format_cr(self.cr.aggregate(query_paqueteria))
            paquetes_recibidos = resultado_paquetes[0]['paquetes_recibidos'] if resultado_paquetes else 0

            res['paquetes_recibidos'] = paquetes_recibidos

        elif page == 'Notas':
            #Notas
            match_query = {
                "deleted_at": {"$exists": False},
                "form_id": self.ACCESOS_NOTAS,
                f"answers.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.mf['ubicacion']}": location,
            }

            if booth_area and not booth_area == "todas" and not booth_area == "":
                match_query.update({
                    f"answers.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.mf['nombre_area']}": booth_area,
                })
                
            query_notas = [
                {'$match': match_query},
                {'$project': {
                    '_id': 1,
                    'nota_status': f"$answers.{self.notes_fields['note_status']}",
                    'fecha_apertura': f"$answers.{self.notes_fields['note_open_date']}",
                    'fecha_cierre': f"$answers.{self.notes_fields['note_close_date']}"
                }},
            ]

            notas = self.format_cr(self.cr.aggregate(query_notas))
            notas_del_dia = 0
            notas_abiertas = 0
            notas_cerradas = 0

            for nota in notas:
                if(nota.get('nota_status') == 'abierto'):
                    notas_abiertas += 1
                if(nota.get('fecha_apertura') >= f"{today} 00:00:00" and nota.get('fecha_apertura') <= f"{today} 23:59:59"):
                    notas_del_dia += 1
                if(nota.get('fecha_cierre') and nota.get('nota_status') == 'cerrado'):
                   notas_cerradas += 1

            res['notas_abiertas'] = notas_abiertas
            res['notas_del_dia'] = notas_del_dia
            res['notas_cerradas'] = notas_cerradas

        return res

    def get_certificacion(self, certificacion, id_user, empresa=None):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.CARGA_PERMISOS_VISITANTES,
            f"answers.{self.DEFINICION_PERMISOS_OBJ_ID}.{self.mf['nombre_permiso']}":certificacion,
            f"answers.{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{self.mf['curp']}":id_user,
        }
        if empresa:
            match_query.update(
                {f"answers.{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{self.mf['empresa']}":empresa}
            )
        result  =self.format_cr(self.cr.find(match_query,{'answers':1}), get_one=True)
        result  = self._labels(result, self.mf)
        return result

    def get_config_accesos(self):
        response = []
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.CONF_ACCESOS,
            f"answers.{self.EMPLOYEE_OBJ_ID}.{self.employee_fields['user_id_id']}":self.user['user_id'],
        }
        query = [
            {'$match': match_query },
            {'$project': {
                "usuario":f"$answers.{self.conf_accesos_fields['usuario_cat']}",
                "grupos":f"$answers.{self.conf_accesos_fields['grupos']}",
                "menus": f"$answers.{self.conf_accesos_fields['menus']}",
            }},
            {'$limit':1},
        ]
        return self.format_cr_result(self.cr.aggregate(query),  get_one=True)

    def get_config_modulo_seguridad(self, ubicaciones=[]):
        #TODO Verificar por que se envia asi la lista
        if isinstance(ubicaciones, list) and ubicaciones and isinstance(ubicaciones[0], dict):
            ubicaciones = [u.get('name') or u.get('id') for u in ubicaciones]
        requerimientos = set()
        envios = set()
        match_query = {
            "deleted_at": {"$exists": False},
            "form_id": self.CONF_MODULO_SEGURIDAD,
        }
        query = [
            {'$match': match_query},
            {'$sort': {'updated_at': -1}},
            {'$limit': 1},
            {'$project': {
                "grupo_requisitos": f"$answers.{self.conf_modulo_seguridad['grupo_requisitos']}",
            }},
        ]
    
        raw_result = self.format_cr_result(self.cr.aggregate(query))
        for raw in raw_result:
            for grupo in raw.get('grupo_requisitos', []):
                #TODO Verficiar el cambio de key
                ubicacion = grupo.get('incidente_location', grupo.get('ubicacion_recorrido', ''))
                if ubicacion in ubicaciones:
                    reqs = grupo.get(self.conf_modulo_seguridad['datos_requeridos'], [])
                    if isinstance(reqs, list):
                        requerimientos.update(reqs)
                    envs = grupo.get(self.conf_modulo_seguridad['envio_por'], [])
                    if isinstance(envs, list):
                        envios.update(envs)
                    if requerimientos == {"identificacion", "fotografia"} and envios == {"correo", "sms"}:
                        break
            if requerimientos == {"identificacion", "fotografia"} and envios == {"correo", "sms"}:
                break
    
        return {
            "ubicaciones": ubicaciones,
            "requerimientos": list(requerimientos),
            "envios": list(envios)
        }

    def get_count_ingresos(self, qr_code):
        total_entradas=""
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.BITACORA_ACCESOS,
            f"answers.{self.mf['codigo_qr']}":qr_code
        }
        query = [
            {'$match': match_query },
            {'$project': {
                'folio':'$folio',
                }
            },
            {'$count': 'total_records'}
        ]
        total_entradas = self.format_cr_result(self.cr.aggregate(query))
        if total_entradas:
            total_entradas = total_entradas.pop()
        return total_entradas

    def get_detail_access_pass(self, qr_code):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.PASE_ENTRADA,
            "_id":ObjectId(qr_code),
        }
        query = [
            {'$match': match_query },
            {'$project': 
                {'_id':1,
                'folio': f"$folio",
                'ubicacion': f"$answers.{self.mf['grupo_ubicaciones_pase']}.{self.UBICACIONES_CAT_OBJ_ID}.{self.f['location']}",
                'nombre': {"$ifNull":[
                    f"$answers.{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{self.mf['nombre_visita']}",
                    f"$answers.{self.mf['nombre_pase']}"]},
                'estatus': f"$answers.{self.pase_entrada_fields['status_pase']}",
                'empresa': {"$ifNull":[
                     f"$answers.{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{self.mf['empresa']}",
                     f"$answers.{self.mf['empresa_pase']}"]},
                'email':  {"$ifNull":[
                    f"$answers.{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{self.mf['email_vista']}",
                    f"$answers.{self.mf['email_pase']}"]},
                'telefono': {"$ifNull":[
                    f"$answers.{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{self.mf['telefono']}",
                    f"$answers.{self.mf['telefono_pase']}"]},
                'curp': f"$answers.{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{self.mf['curp']}",
                'fecha_de_expedicion': f"$answers.{self.mf['fecha_desde_visita']}",
                'fecha_de_caducidad':{'$ifNull':[
                    f"$answers.{self.mf['fecha_desde_hasta']}",
                    f"$answers.{self.mf['fecha_desde_visita']}",
                    ]
                    },
                'foto': {'$ifNull':[
                    f"$answers.{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{self.mf['foto']}",
                    f"$answers.{self.pase_entrada_fields['walkin_fotografia']}"]},
                'limite_de_acceso': f"$answers.{self.mf['config_limitar_acceso']}",
                'config_dia_de_acceso': f"$answers.{self.mf['config_dia_de_acceso']}",
                'identificacion': {'$ifNull':[
                    f"$answers.{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{self.mf['identificacion']}",
                    f"$answers.{self.pase_entrada_fields['walkin_identificacion']}"]},
                'limitado_a_dias':f"$answers.{self.mf['config_dias_acceso']}",
                'motivo_visita':f"$answers.{self.CONFIG_PERFILES_OBJ_ID}.{self.mf['motivo']}",
                'perfil_pase':f"$answers.{self.CONFIG_PERFILES_OBJ_ID}",
                'tipo_de_pase':f"$answers.{self.pase_entrada_fields['perfil_pase']}",
                'tipo_de_comentario': f"$answers.{self.mf['tipo_de_comentario']}",
                'visita_a_nombre':
                     f"$answers.{self.mf['grupo_visitados']}.{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.mf['nombre_empleado']}",
                'visita_a_puesto': 
                    f"$answers.{self.mf['grupo_visitados']}.{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.mf['puesto_empleado']}",
                'visita_a_departamento':
                    f"$answers.{self.mf['grupo_visitados']}.{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.mf['departamento_empleado']}",
                'visita_a_user_id':
                    f"$answers.{self.mf['grupo_visitados']}.{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.mf['user_id_empleado']}",
                'visita_a_email':
                    f"$answers.{self.mf['grupo_visitados']}.{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.mf['email_visita_a']}",
                'visita_a_telefono':
                    f"$answers.{self.mf['grupo_visitados']}.{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.mf['telefono_visita_a']}",
                'grupo_areas_acceso': f"$answers.{self.mf['grupo_areas_acceso']}",
                # 'grupo_commentario_area': f"$answers.{self.mf['grupo_commentario_area']}",
                'grupo_equipos': f"$answers.{self.mf['grupo_equipos']}",
                'grupo_vehiculos': f"$answers.{self.mf['grupo_vehiculos']}",
                'grupo_instrucciones_pase': f"$answers.{self.mf['grupo_instrucciones_pase']}",
                'comentario': f"$answers.{self.mf['grupo_instrucciones_pase']}",
                'codigo_qr': f"$answers.{self.mf['codigo_qr']}",
                'qr_pase': f"$answers.{self.mf['qr_pase']}",
                'tema_cita': f"$answers.{self.pase_entrada_fields['tema_cita']}",
                'descripcion': f"$answers.{self.pase_entrada_fields['descripcion']}",
                'link': f"$answers.{self.pase_entrada_fields['link']}",
                'google_wallet_pass_url': f"$answers.{self.pase_entrada_fields['google_wallet_pass_url']}",
                'apple_wallet_pass': f"$answers.{self.pase_entrada_fields['apple_wallet_pass']}",
                'pdf_to_img': f"$answers.{self.pase_entrada_fields['pdf_to_img']}",
                'acepto_aviso_privacidad': f"$answers.{self.pase_entrada_fields['acepto_aviso_privacidad']}",
                'acepto_aviso_datos_personales': f"$answers.{self.pase_entrada_fields['acepto_aviso_datos_personales']}",
                'conservar_datos_por': f"$answers.{self.pase_entrada_fields['conservar_datos_por']}",
                'ubicaciones': f"$answers.{self.pase_entrada_fields['ubicaciones']}"                
                },
            },
            {'$sort':{'folio':-1}},
        ]
        res = self.cr.aggregate(query)
        x = {}
        for x in res:
            visita_a =[]
            x['_id'] = str(x.pop('_id'))
            v = x.pop('visita_a_nombre') if x.get('visita_a_nombre') else []
            d = x.get('visita_a_departamento',[])
            p = x.get('visita_a_puesto',[])
            e =  x.get('visita_a_user_id',[])
            u =  x.get('visita_a_email',[])
            f =  x.get('visita_a_telefono',[])
            x['empresa'] = self.unlist(x.get('empresa',''))
            x['email'] =self.unlist(x.get('email',''))
            x['telefono'] = self.unlist(x.get('telefono',''))
            x['curp'] = self.unlist(x.get('curp',''))
            x['motivo_visita'] = self.unlist(x.get('motivo_visita',''))
            for idx, nombre in enumerate(v):
                emp = {'nombre':nombre}
                if d:
                    emp.update({'departamento':d[idx].pop(0) if d[idx] else ""})
                if p:
                    emp.update({'puesto':p[idx].pop(0) if p[idx] else ""})
                if e:
                    emp.update({'user_id':e[idx].pop(0) if e[idx] else ""})
                if u:
                    emp.update({'email': u[idx].pop(0) if u[idx] else ""})
                if f:
                    emp.update({'telefono': f[idx].pop(0) if f[idx] else ""})
                visita_a.append(emp)
            x['visita_a'] = visita_a
            perfil_pase = x.pop('perfil_pase') if x.get('perfil_pase') else []
            perfil_pase = self._labels(perfil_pase, self.mf)
            if x.get('fecha_de_caducidad') == "":
                x['fecha_de_caducidad'] = x.get('fecha_de_expedicion')
            if perfil_pase:
                x['tipo_de_pase'] = perfil_pase.pop('nombre_perfil')
                empresa = x.get('empresa')
                x['certificaciones'] = self.format_perfil_pase(perfil_pase, x['curp'], empresa)
            x['grupo_areas_acceso'] = self._labels_list(x.pop('grupo_areas_acceso',[]), self.mf)
            x['grupo_instrucciones_pase'] = self._labels_list(x.pop('grupo_instrucciones_pase',[]), self.mf)
            x['grupo_equipos'] = self._labels_list(x.pop('grupo_equipos',[]), self.mf)
            x['grupo_vehiculos'] = self._labels_list(x.pop('grupo_vehiculos',[]), self.mf)
            x['ubicacion'] = x.get('ubicacion', [])
            ubicaciones = x.get('ubicaciones', [])
            ubicaciones_format = []
            for ubicacion in ubicaciones:
                ubicaciones_format.append(ubicacion.get(self.UBICACIONES_CAT_OBJ_ID, {}).get(self.mf['ubicacion'], ''))
            x['ubicaciones'] = ubicaciones_format
        if not x:
            self.LKFException({'title':'Advertencia', 'msg':'Este pase fue eliminado o no pertenece a esta organizacion.'})
        return x

    def get_ids_labels(self, data):
        return data

    def get_employee_checkin_status(self, user_ids, as_shift=False,  **kwargs):
        query = []
        if kwargs.get('user_id'):
            user_id = kwargs['user_id']
        else:
            user_id = self.user.get('user_id')
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.CHECKIN_CASETAS,
            }
        unwind = {'$unwind': f"$answers.{self.f['guard_group']}"}
        query = [{'$match': match_query }, unwind ]

        unwind_query = {f"answers.{self.f['guard_group']}.{self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID}.{self.f['user_id_jefes']}": {"$exists":True}}
        if as_shift:
            match_query.update({'created_by_id':user_id})
            query = [
                {'$match': match_query },
                {'$sort':{'created_at':-1}},
                {'$limit':1},
                unwind
                ]
        else:
            if type(user_ids) == list:
                unwind_query.update({f"answers.{self.f['guard_group']}.{self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID}.{self.f['user_id_jefes']}": {"$in": user_ids}})
            else:
                unwind_query.update({f"answers.{self.f['guard_group']}.{self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID}.{self.f['user_id_jefes']}": user_ids })
        query += [ {'$match': unwind_query }]
        query += [
            {'$project':
                {'_id': 1,
                    'folio': "$folio",
                    'created_at': "$created_at",
                    'name': f"$answers.{self.f['guard_group']}.{self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID}.{self.f['worker_name_jefes']}",
                    'user_id': {"$first":f"$answers.{self.f['guard_group']}.{self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID}.{self.f['user_id_jefes']}"},
                    'location': f"$answers.{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.mf['ubicacion']}",
                    'area': f"$answers.{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.mf['nombre_area']}",
                    'checkin_date': f"$answers.{self.f['guard_group']}.{self.f['checkin_date']}",
                    'checkout_date': f"$answers.{self.f['guard_group']}.{self.f['checkout_date']}",
                    'checkin_status': f"$answers.{self.f['guard_group']}.{self.f['checkin_status']}",
                    'checkin_position': f"$answers.{self.f['guard_group']}.{self.f['checkin_position']}",
                    }
            },
            {'$sort':{'updated_at':-1}},
            {'$group':{
                '_id':{
                    'user_id':'$user_id',
                    },
                'name':{'$last':'$name'},
                'location':{'$last':'$location'},
                'area':{'$last':'$area'},
                'checkin_date':{'$last':'$checkin_date'},
                'checkout_date':{'$last':'$checkout_date'},
                'checkin_status':{'$last':'$checkin_status'},
                'checkin_position':{'$last':'$checkin_position'},

            }},
            {'$project':{
                '_id':0,
                'user_id':'$_id.user_id',
                'name':'$name',
                'location':'$location',
                'area':'$area',
                'checkin_date':'$checkin_date',
                'checkout_date':'$checkout_date',
                'checkin_status': {'$cond': [ {'$eq':['$checkin_status','entrada']},'in','out']}, 
                'checkin_position':'$checkin_position',

            }}
            ]
        data = self.format_cr(self.cr.aggregate(query))
        res = {}
        for rec in data:
            status = 'in' if rec.get('checkin_status') in ['in','entrada'] else 'out'
            res[int(rec.get('user_id',0))] = {
                'status':status, 
                'name': rec.get('name'), 
                'user_id': rec.get('user_id'), 
                'location':rec.get('location'),
                'area':rec.get('area'),
                'checkin_date':rec.get('checkin_date'),
                'checkout_date':rec.get('checkout_date'),
                'checkin_position':rec.get('checkin_position')
                }
        return res

    def get_checkin_by_id(self, _id=None, folio=None):
        # Obtiene el registro de check-in por ID o folio.

        if not _id or not folio:
            msg = "An _id or a folio is required to get the record"
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.CHECKIN_CASETAS,
            }
        if _id:
            match_query.update({"_id":ObjectId(_id)})
        elif folio:
            match_query.update({"folio":folio})
        query = [
            {'$match': match_query },
            {'$project': self.proyect_format(self.checkin_fields)},
            {'$sort':{'updated_at':-1}},
            {'$limit':1}
            ]
        return self.format_cr_result(self.cr.aggregate(query), get_one=True)
 
    def get_last_checkin(self, location, area):
        # Obtiene el último registro de check-in por ubicación y área.

        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.CHECKIN_CASETAS,
            f"answers.{self.checkin_fields['cat_location']}":location,
            f"answers.{self.checkin_fields['cat_area']}":area,
            }
        query = [
            {'$match': match_query },
            {'$project': self.project_format(self.checkin_fields)},
            {'$sort':{'created_at':-1}},
            {'$limit':1}
            ]
        return self.format_cr_result(self.cr.aggregate(query), get_one=True)

    def get_guard_last_checkin(self, user_ids):
        '''
            Se realiza busqued del ulisto registro de checkin de un usuario
        '''
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.CHECKIN_CASETAS,
            }
        unwind_query = {}
        if user_ids and type(user_ids) == list:
            if len(user_ids) == 1:
                #hace la busqueda por directa, para optimizar recuros
                user_ids = user_ids[0]
            else:
                #hace busqueda en lista de opciones
                match_query.update({
                    f"answers.{self.f['guard_group']}.{self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID}.{self.f['user_id_jefes']}":{'$in':user_ids}
                    })
        if user_ids and type(user_ids) == int:
            unwind_query.update({
                f"answers.{self.f['guard_group']}.{self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID}.{self.f['user_id_jefes']}":user_ids
                })
        if not unwind_query:
            return self.LKFException({"msg":f"Algo salio mal al intentar buscar el checkin del los ids: {user_id}"})
        query = [
            {'$match': match_query },
            {'$unwind': f"$answers.{self.f['guard_group']}"},
            {'$match':unwind_query},
            {'$project': self.project_format(self.checkin_fields)},
            {'$sort':{'created_at':-1}},
            {'$limit':1}
            ]
        return self.format_cr_result(self.cr.aggregate(query), get_one=True)

    def get_last_user_move(self, qr, location):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.BITACORA_ACCESOS,
            f"answers.{self.mf['codigo_qr']}":qr,
        }
        res = self.cr.find(
            match_query, 
            {
                'folio':'$folio', 
                'status_visita': f"$answers.{self.bitacora_fields['status_visita']}",
                'checkin_date': f"$answers.{self.bitacora_fields['fecha_entrada']}",
                'checkout_date': f"$answers.{self.bitacora_fields['fecha_salida']}",
                'gafete_id': f"$answers.{self.GAFETES_CAT_OBJ_ID}.{self.gafetes_fields['gafete_id']}",
                'gafete_id': f"$answers.{self.GAFETES_CAT_OBJ_ID}.{self.gafetes_fields['gafete_id']}",
                'locker_id': f"$answers.{self.LOCKERS_CAT_OBJ_ID}.{self.mf['locker_id']}",
                'ubicacion_entrada': f"$answers.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.mf['ubicacion']}",
                'status_gafete':f"$answers.{self.bitacora_fields['status_gafete']}"
                }
            ).sort('updated_at', -1).limit(1)
        return self.format_cr(res, get_one=True)
        # return self.format_cr_result(self.cr.aggregate(query), get_one=True)

    def get_list_article_lost(self, location, area, status=None, dateFrom="", dateTo="", filterDate=""):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.BITACORA_OBJETOS_PERDIDOS,
        }
        if location:
             match_query[f"answers.{self.AREAS_DE_LAS_UBICACIONES_SALIDA_OBJ_ID}.{self.mf['ubicacion']}"] = location
        if area:
             match_query[f"answers.{self.AREAS_DE_LAS_UBICACIONES_SALIDA_OBJ_ID}.{self.mf['nombre_area_salida']}"] = area
        if status:
             match_query[f"answers.{self.perdidos_fields['estatus_perdido']}"] = status

        user_data = self.lkf_api.get_user_by_id(self.user.get('user_id'))
        zona = user_data.get('timezone','America/Monterrey')

        if filterDate != "range":
            dateFrom, dateTo = self.get_range_dates(filterDate,zona)

            if dateFrom:
                dateFrom = str(dateFrom)
            if dateTo:
                dateTo = str(dateTo)
        if dateFrom and dateTo:
            match_query.update({
                f"answers.{self.perdidos_fields['date_hallazgo_perdido']}": {"$gte": dateFrom,"$lte": dateTo},
            })
        elif dateFrom:
            match_query.update({
                f"answers.{self.perdidos_fields['date_hallazgo_perdido']}": {"$gte": dateFrom}
            })
        elif dateTo:
            match_query.update({
                f"answers.{self.perdidos_fields['date_hallazgo_perdido']}": {"$lte": dateTo}
            })

        query = [
            {'$match': match_query },
            #{'$project': self.proyect_format(self.perdidos_fields)},
            {'$project': {
                "folio":"$folio",
                'estatus_perdido':f"$answers.{self.perdidos_fields['estatus_perdido']}",
                'date_hallazgo_perdido':f"$answers.{self.perdidos_fields['date_hallazgo_perdido']}",
                'ubicacion_perdido':f"$answers.{self.perdidos_fields['ubicacion_catalog']}.{self.perdidos_fields['ubicacion_perdido']}",
                'area_perdido': f"$answers.{self.perdidos_fields['area_catalog']}.{self.perdidos_fields['area_perdido']}",
                'color_perdido':f"$answers.{self.perdidos_fields['color_perdido']}",
                'articulo_perdido':f"$answers.{self.perdidos_fields['articulo_perdido']}",
                'tipo_articulo_perdido':f"$answers.{self.perdidos_fields['tipo_articulo_catalog']}.{self.perdidos_fields['tipo_articulo_perdido']}",
                'articulo_seleccion':f"$answers.{self.perdidos_fields['articulo_seleccion_catalog']}.{self.perdidos_fields['articulo_seleccion']}",
                'foto_perdido':f"$answers.{self.perdidos_fields['foto_perdido']}",
                'descripcion':f"$answers.{self.perdidos_fields['descripcion']}",
                'comentario_perdido':f"$answers.{self.perdidos_fields['comentario_perdido']}",
                'quien_entrega_interno':f"$answers.{self.perdidos_fields['quien_entrega_catalog']}.{self.perdidos_fields['quien_entrega_interno']}",
                'quien_entrega':f"$answers.{self.perdidos_fields['quien_entrega']}",
                'quien_entrega_externo':f"$answers.{self.perdidos_fields['quien_entrega_externo']}",
                'recibe_perdido':f"$answers.{self.perdidos_fields['recibe_perdido']}",
                'telefono_recibe_perdido':f"$answers.{self.perdidos_fields['telefono_recibe_perdido']}",
                'identificacion_recibe_perdido':f"$answers.{self.perdidos_fields['identificacion_recibe_perdido']}",
                'foto_recibe_perdido':f"$answers.{self.perdidos_fields['foto_recibe_perdido']}",
                'date_entrega_perdido':f"$answers.{self.perdidos_fields['date_entrega_perdido']}",
                'locker_perdido':f"$answers.{self.perdidos_fields['locker_catalog']}.{self.perdidos_fields['locker_perdido']}" 
            }},
            {'$sort':{'folio':-1}},
        ]
        if not filterDate:
            query.append(
                {"$limit":25}
            )
        pr= self.format_cr_result(self.cr.aggregate(query))
        return self.format_cr_result(self.cr.aggregate(query))

    def get_list_article_concessioned(self, location="", area="", status="", dateFrom="", dateTo="", filterDate=""):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.CONCESSIONED_ARTICULOS,
        }
        if location:
             match_query[f"answers.{self.AREAS_DE_LAS_UBICACIONES_SALIDA_OBJ_ID}.{self.perdidos_fields['ubicacion_perdido']}"] = location
        if area:
             match_query[f"answers.{self.AREAS_DE_LAS_UBICACIONES_SALIDA_OBJ_ID}.{self.mf['nombre_area_salida']}"] = area
        if status:
             match_query[f"answers.{self.consecionados_fields['status_concesion']}"] = status

        user_data = self.lkf_api.get_user_by_id(self.user.get('user_id'))
        zona = user_data.get('timezone','America/Monterrey')

        if filterDate != "range":
            dateFrom, dateTo = self.get_range_dates(filterDate,zona)

            if dateFrom:
                dateFrom = str(dateFrom)
            if dateTo:
                dateTo = str(dateTo)
        if dateFrom and dateTo:
            match_query.update({
                f"answers.{self.consecionados_fields['fecha_concesion']}": {"$gte": dateFrom,"$lte": dateTo},
            })
        elif dateFrom:
            match_query.update({
                f"answers.{self.consecionados_fields['fecha_concesion']}": {"$gte": dateFrom}
            })
        elif dateTo:
            match_query.update({
                f"answers.{self.consecionados_fields['fecha_concesion']}": {"$lte": dateTo}
            })

        query = [
            {'$match': match_query },
            {'$project': {
                "_id" : "$_id",
                "folio": "$folio",
                'status_concesion':f"$answers.{self.consecionados_fields['status_concesion']}",
                'ubicacion_concesion':f"$answers.{self.consecionados_fields['ubicacion_concesion']}",
                'solicita_concesion':f"$answers.{self.consecionados_fields['solicita_concesion']}",
                'persona_nombre_concesion':f"$answers.{self.consecionados_fields['persona_nombre_concesion']}",
                'caseta_concesion':f"$answers.{self.consecionados_fields['caseta_concesion']}",
                'fecha_concesion':f"$answers.{self.consecionados_fields['fecha_concesion']}",
                'equipo_imagen_concesion':f"$answers.{self.consecionados_fields['equipo_imagen_concesion']}",
                'area_concesion':f"$answers.{self.consecionados_fields['area_concesion']}",
                'equipo_concesion':f"$answers.{self.consecionados_fields['equipo_concesion']}",
                'observacion_concesion':f"$answers.{self.consecionados_fields['observacion_concesion']}",
                'fecha_devolucion_concesion':f"$answers.{self.consecionados_fields['fecha_devolucion_concesion']}",
            }},
            {'$sort':{'folio':-1}},
        ]
        return self.format_cr_result(self.cr.aggregate(query))

    def get_gafetes(self, status='Disponible', location=None, area=None, gafete_id=None, limit=1000, skip=0):
        selector = {}
        if status:
            selector.update({f"answers.{self.mf['status_gafete']}":status})
        if location:
            selector.update({f"answers.{self.f['location']}":location})
        if area:
            selector.update({f"answers.{self.f['area']}":area})
        if gafete_id:
            selector.update({f"answers.{self.gafetes_fields['gafete_id']}":gafete_id})
        if not selector:
            selector = {"_id":{"$gt":None}}
        mango_query = {
            "selector": selector,
            "limit":limit,
            "skip":skip
        }
        return self.format_gafete(self.lkf_api.search_catalog( self.GAFETES_CAT_ID, mango_query))

    def get_lockers(self, status='Disponible', location=None, area=None, tipo_locker='Locker', locker_id=None, limit=1000, skip=0):
        selector = {}
        if status:
            selector.update({f"answers.{self.mf['status_locker']}":status})
        if location:
            selector.update({f"answers.{self.f['location']}":location})
        if area:
            selector.update({f"answers.{self.f['area']}":area})
        if tipo_locker:
            selector.update({f"answers.{self.mf['tipo_locker']}":tipo_locker})
        if locker_id:
            selector.update({f"answers.{self.mf['locker_id']}":locker_id})
        if not selector:
            selector = {"_id":{"$gt":None}}
        mango_query = {
            "selector": selector,
            "limit":limit,
            "skip":skip
        }
        return self.format_lockers(self.lkf_api.search_catalog( self.LOCKERS_CAT_ID, mango_query))

    def get_list_bitacora(self, location=None, area=None, prioridades=[], dateFrom='', dateTo='', limit=10, offset=0):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.BITACORA_ACCESOS
        }
        if location:
            match_query.update({f"answers.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.mf['ubicacion']}":location})
        if area:
            match_query.update({f"answers.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.mf['nombre_area']}":area})
        if prioridades:
            match_query[f"answers.{self.bitacora_fields['status_visita']}"] = {"$in": prioridades}

        if dateFrom and dateTo:
            dateFrom = f"{dateFrom} 00:00:00"
            dateTo = f"{dateTo} 23:59:59"
            match_query.update({
                f"answers.{self.mf['fecha_entrada']}": {"$gte": dateFrom, "$lte": dateTo},
            })
        elif dateFrom:
            dateFrom = f"{dateFrom} 00:00:00"
            match_query.update({
                f"answers.{self.mf['fecha_entrada']}": {"$gte": dateFrom}
            })
        elif dateTo:
            dateTo = f"{dateTo} 23:59:59"
            match_query.update({
                f"answers.{self.mf['fecha_entrada']}": {"$lte": dateTo}
            })

        proyect_fields ={
            '_id': 1,
            'folio': "$folio",
            'created_at': "$created_at",
            'updated_at': "$updated_at",
            'a_quien_visita':f"$answers.{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.mf['nombre_empleado']}",
            'documento': f"$answers.{self.mf['documento']}",
            'caseta_entrada':f"$answers.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.mf['nombre_area']}",
            'codigo_qr':f"$answers.{self.mf['codigo_qr']}",
            'comentarios':f"$answers.{self.bitacora_fields['grupo_comentario']}",
            'fecha_salida':f"$answers.{self.mf['fecha_salida']}",
            'fecha_entrada':f"$answers.{self.mf['fecha_entrada']}",
            'foto_url': {"$arrayElemAt": [f"$answers.{self.PASE_ENTRADA_OBJ_ID}.{self.mf['foto']}.file_url", 0]},
            'equipos':f"$answers.{self.mf['grupo_equipos']}",
            'grupo_areas_acceso': f"$answers.{self.mf['grupo_areas_acceso']}",
            'id_gafet': f"$answers.{self.GAFETES_CAT_OBJ_ID}.{self.gafetes_fields['gafete_id']}",
            'id_locker': f"$answers.{self.LOCKERS_CAT_OBJ_ID}.{self.lockers_fields['locker_id']}",
            'identificacion':  {"$first":f"$answers.{self.PASE_ENTRADA_OBJ_ID}.{self.mf['identificacion']}"},
            'pase_id':{"$toObjectId":f"$answers.{self.mf['codigo_qr']}"},
            'motivo_visita':f"$answers.{self.CONFIG_PERFILES_OBJ_ID}.{self.mf['motivo']}",
            'nombre_area_salida':f"$answers.{self.AREAS_DE_LAS_UBICACIONES_SALIDA_OBJ_ID}.{self.mf['nombre_area_salida']}",
            'nombre_visitante':f"$answers.{self.PASE_ENTRADA_OBJ_ID}.{self.mf['nombre_visita']}",
            'contratista':f"$answers.{self.PASE_ENTRADA_OBJ_ID}.{self.mf['empresa']}",
            'perfil_visita':{'$arrayElemAt': [f"$answers.{self.PASE_ENTRADA_OBJ_ID}.{self.mf['nombre_perfil']}",0]},
            'status_gafete':f"$answers.{self.mf['status_gafete']}",
            'status_visita':f"$answers.{self.mf['tipo_registro']}",
            'ubicacion':f"$answers.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.mf['ubicacion']}",
            'vehiculos':f"$answers.{self.mf['grupo_vehiculos']}",
            'visita_a': f"$answers.{self.mf['grupo_visitados']}"
            }
        lookup = {
         'from': 'form_answer',
         'localField': 'pase_id',
         'foreignField': '_id',
         "pipeline": [
                {'$match':{
                    "deleted_at":{"$exists":False},
                    "form_id": self.PASE_ENTRADA,
                    }
                },
                {'$project':{
                    "_id":0, 
                    'motivo_visita':f"$answers.{self.CONFIG_PERFILES_OBJ_ID}.{self.mf['motivo']}",
                    'grupo_areas_acceso': f"$answers.{self.mf['grupo_areas_acceso']}",                    
                    }
                },
                ],
         'as': 'pase',
        }
        query = [
            {'$match': match_query },
            {'$project': proyect_fields},
            {'$lookup': lookup},
        ]
        if dateFrom:
            query.append(
                {'$sort':{'folio':1}},
            )
        else:
            query.append(
                {'$sort':{'folio':-1}},
            )

        query.append({'$skip': offset})
        query.append({'$limit': limit})

        records = self.format_cr(self.cr.aggregate(query))
        count_query = [
            {'$match': match_query},
            {'$count': 'total'}
        ]

        count_result = self.format_cr(self.cr.aggregate(count_query))
        total_count = count_result[0]['total'] if count_result else 0
        total_pages = ceil(total_count / limit) if limit else 1
        current_page = (offset // limit) + 1 if limit else 1

        for r in records:
            pase = r.pop('pase')
            r.pop('pase_id')
            if len(pase) > 0 :
                pase = pase[0]
                r['motivo_visita'] = self.unlist(pase.get('motivo_visita',''))
                r['grupo_areas_acceso'] = self._labels_list(pase.get('grupo_areas_acceso',[]), self.mf)
            r['id_gafet'] = r.get('id_gafet','')
            r['status_visita'] = r.get('status_visita','').title().replace('_', ' ')
            r['contratista'] = self.unlist(r.get('contratista',[]))
            r['status_gafete'] = r.get('status_gafete','').title().replace('_', ' ')
            r['documento'] = r.get('documento','')
            r['grupo_areas_acceso'] = self._labels_list(r.pop('grupo_areas_acceso',[]), self.mf)
            r['comentarios'] = self.format_comentarios(r.get('comentarios',[]))
            r['vehiculos'] = self.format_vehiculos(r.get('vehiculos',[]))
            r['equipos'] = self.format_equipos(r.get('equipos',[]))
            r['visita_a'] = self.format_visita(r.get('visita_a',[]))
        bitacora = {
            'records': records,
            'total_records': total_count,
            'total_pages': total_pages,
            'actual_page': current_page
        }
        return bitacora

    def get_list_fallas(self, location=None, area=None,status=None, folio=None, dateFrom="", dateTo="", filterDate=""):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.BITACORA_FALLAS,
        }
        if location:
            match_query[f"answers.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.fallas_fields['falla_ubicacion']}"] = location
        if area:
            match_query[f"answers.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.fallas_fields['falla_caseta']}"] = area
        if status:
            match_query[f"answers.{self.fallas_fields['falla_estatus']}"] = status
        if folio:
            match_query.update({"folio":folio})

        user_data = self.lkf_api.get_user_by_id(self.user.get('user_id'))
        zona = user_data.get('timezone','America/Monterrey')

        if filterDate != "range":
            dateFrom, dateTo = self.get_range_dates(filterDate,zona)

            if dateFrom:
                dateFrom = str(dateFrom)
            if dateTo:
                dateTo = str(dateTo)

        if dateFrom and dateTo:
            match_query.update({
                f"answers.{self.fallas_fields['falla_fecha_hora']}": {"$gte": dateFrom, "$lte": dateTo},
            })
        elif dateFrom:
            match_query.update({
                f"answers.{self.fallas_fields['falla_fecha_hora']}": {"$gte": dateFrom}
            })
        elif dateTo:
            match_query.update({
                f"answers.{self.fallas_fields['falla_fecha_hora']}": {"$lte": dateTo}
            })

        query = [
            {'$match': match_query },
            {'$project': {
                "folio": "$folio",
                'falla_estatus': f"$answers.{self.fallas_fields['falla_estatus']}",
                'falla_fecha_hora': f"$answers.{self.fallas_fields['falla_fecha_hora']}",
                'falla_reporta_nombre': f"$answers.{self.fallas_fields['falla_reporta_catalog']}.{self.fallas_fields['falla_reporta_nombre']}",
                'falla_reporta_departamento': f"$answers.{self.fallas_fields['falla_reporta_catalog']}.{self.fallas_fields['falla_reporta_departamento']}",
                'falla_ubicacion': f"$answers.{self.fallas_fields['falla_ubicacion_catalog']}.{self.fallas_fields['falla_ubicacion']}",
                'falla_caseta':f"$answers.{self.fallas_fields['falla_ubicacion_catalog']}.{self.fallas_fields['falla_caseta']}",
                'falla':f"$answers.{self.fallas_fields['falla_catalog']}.{self.fallas_fields['falla']}",
                'falla_objeto_afectado':f"$answers.{self.LISTA_FALLAS_CAT_OBJ_ID}.{self.fallas_fields['falla_subconcepto']}",
                'falla_comentarios':f"$answers.{self.fallas_fields['falla_comentarios']}",
                'falla_evidencia': f"$answers.{self.fallas_fields['falla_evidencia']}",
                'falla_documento':f"$answers.{self.fallas_fields['falla_documento']}",
                'falla_responsable_solucionar_nombre':f"$answers.{self.fallas_fields['falla_responsable_solucionar_catalog']}.{self.fallas_fields['falla_responsable_solucionar_nombre']}",
                'falla_responsable_solucionar_documento':f"$answers.{self.fallas_fields['falla_responsable_solucionar_catalog']}.{self.fallas_fields['falla_responsable_solucionar_documento']}",
                'falla_comentario_solucion':f"$answers.{self.fallas_fields['falla_comentario_solucion']}",
                'falla_folio_accion_correctiva':f"$answers.{self.fallas_fields['falla_folio_accion_correctiva']}",
                'falla_evidencia_solucion':f"$answers.{self.fallas_fields['falla_evidencia_solucion']}",
                'falla_documento_solucion':f"$answers.{self.fallas_fields['falla_documento_solucion']}",
                'falla_fecha_hora_solucion':f"$answers.{self.fallas_fields['falla_fecha_hora_solucion']}",
                'falla_grupo_seguimiento':f"$answers.{self.fallas_fields['falla_grupo_seguimiento']}",
            }},
            {'$sort':{'folio':-1}},
        ]
        result = self.format_cr_result(self.cr.aggregate(query))
        for r in result:
            if r:
                r['falla_grupo_seguimiento_formated'] = self.format_seguimiento_fallas(r.get('falla_grupo_seguimiento',[]))
                r.pop('falla_grupo_seguimiento', None)
        return result

    def get_list_incidences(self, location, area, prioridades=[], dateFrom="", dateTo="", filterDate="", folio=None):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.BITACORA_INCIDENCIAS,
        }
        if location:
             match_query[f"answers.{self.incidence_fields['ubicacion_incidencia_catalog']}.{self.incidence_fields['ubicacion_incidencia']}"] = location
        if area:
             match_query[f"answers.{self.incidence_fields['area_incidencia_catalog']}.{self.incidence_fields['area_incidencia']}"] = area
        if prioridades:
            match_query[f"answers.{self.incidence_fields['prioridad_incidencia']}"] = {"$in": prioridades}
        if folio:
            match_query.update({"folio":folio})
       
        user_data = self.lkf_api.get_user_by_id(self.user.get('user_id'))
        zona = user_data.get('timezone','America/Monterrey')

        if filterDate != "range":
            dateFrom, dateTo = self.get_range_dates(filterDate,zona)

            if dateFrom:
                dateFrom = str(dateFrom)
            if dateTo:
                dateTo = str(dateTo)

        if dateFrom and dateTo:
            match_query.update({
                f"answers.{self.incidence_fields['fecha_hora_incidencia']}": {"$gte": dateFrom,"$lte": dateTo},
            })
        elif dateFrom:
            match_query.update({
                f"answers.{self.incidence_fields['fecha_hora_incidencia']}": {"$gte": dateFrom}
            })
        elif dateTo:
            match_query.update({
                f"answers.{self.incidence_fields['fecha_hora_incidencia']}": {"$lte": dateTo}
            })

        query = [
            {'$match': match_query },
            {'$project': {
                'folio': '$folio',
                'reporta_incidencia': f"$answers.{self.incidence_fields['reporta_incidencia_catalog']}.{self.incidence_fields['reporta_incidencia']}",
                'fecha_hora_incidencia':f"$answers.{self.incidence_fields['fecha_hora_incidencia']}",
                'ubicacion_incidencia': f"$answers.{self.incidence_fields['ubicacion_incidencia_catalog']}.{self.incidence_fields['ubicacion_incidencia']}",
                'area_incidencia': f"$answers.{self.incidence_fields['area_incidencia_catalog']}.{self.incidence_fields['area_incidencia']}",
                'incidencia': f"$answers.{self.incidence_fields['incidencia_catalog']}.{self.incidence_fields['incidencia']}",
                'tipo_incidencia': f"$answers.{self.incidence_fields['tipo_incidencia']}",
                'comentario_incidencia': f"$answers.{self.incidence_fields['comentario_incidencia']}",
                'tipo_dano_incidencia': f"$answers.{self.incidence_fields['tipo_dano_incidencia']}",
                'dano_incidencia':f"$answers.{self.incidence_fields['dano_incidencia']}",

                'evidencia_incidencia':f"$answers.{self.incidence_fields['evidencia_incidencia']}",
                'documento_incidencia':f"$answers.{self.incidence_fields['documento_incidencia']}",
                'prioridad_incidencia':f"$answers.{self.incidence_fields['prioridad_incidencia']}",
                'notificacion_incidencia':f"$answers.{self.incidence_fields['notificacion_incidencia']}",
                'total_deposito_incidencia':f"$answers.{self.incidence_fields['total_deposito_incidencia']}",
                'datos_deposito_incidencia':f"$answers.{self.incidence_fields['datos_deposito_incidencia']}",
                
                'tags':f"$answers.{self.incidence_fields['tags']}",

                'nombre_completo_persona_extraviada':f"$answers.{self.incidence_fields['nombre_completo_persona_extraviada']}",
                'edad':f"$answers.{self.incidence_fields['edad']}",
                'color_piel':f"$answers.{self.incidence_fields['color_piel']}",
                'color_cabello': f"$answers.{self.incidence_fields['color_cabello']}",
                'estatura_aproximada':f"$answers.{self.incidence_fields['estatura_aproximada']}",
                'descripcion_fisica_vestimenta':f"$answers.{self.incidence_fields['descripcion_fisica_vestimenta']}",
                'nombre_completo_responsable': f"$answers.{self.incidence_fields['nombre_completo_responsable']}",
                'parentesco': f"$answers.{self.incidence_fields['parentesco']}",
                'num_doc_identidad': f"$answers.{self.incidence_fields['num_doc_identidad']}",
                'telefono': f"$answers.{self.incidence_fields['telefono']}",
                'info_coincide_con_videos': f"$answers.{self.incidence_fields['info_coincide_con_videos']}",
                'responsable_que_entrega': f"$answers.{self.incidence_fields['responsable_que_entrega']}",
                'responsable_que_recibe':f"$answers.{self.incidence_fields['responsable_que_recibe']}",
                #Robo de cableado
                'valor_estimado': f"$answers.{self.incidence_fields['valor_estimado']}",
                'pertenencias_sustraidas': f"$answers.{self.incidence_fields['pertenencias_sustraidas']}",
                #Robo de vehiculo
                'placas': f"$answers.{self.incidence_fields['placas']}",
                'tipo': f"$answers.{self.incidence_fields['tipo']}",
                'marca':f"$answers.{self.incidence_fields['marca']}",
                'modelo':f"$answers.{self.incidence_fields['modelo']}",
                'color': f"$answers.{self.incidence_fields['color']}",

                'categoria':f"$answers.{self.incidence_fields['incidencia_catalog']}.{self.incidence_fields['categoria']}",
                'sub_categoria':f"$answers.{self.incidence_fields['incidencia_catalog']}.{self.incidence_fields['sub_categoria']}",
                'incidente':f"$answers.{self.incidence_fields['incidencia_catalog']}.{self.incidence_fields['incidente']}",

                #Grupos repetitivos
                'personas_involucradas_incidencia':f"$answers.{self.incidence_fields['personas_involucradas_incidencia']}",
                'afectacion_patrimonial_incidencia':f"$answers.{self.incidence_fields['afectacion_patrimonial_incidencia']}",
                'acciones_tomadas_incidencia':f"$answers.{self.incidence_fields['acciones_tomadas_incidencia']}",
                'seguimientos_incidencia':f"$answers.{self.incidence_fields['seguimiento_incidencia']}",
                }
            },
            {'$sort':{'folio':-1}}
        ]
        result = self.format_cr_result(self.cr.aggregate(query))
        result = self.format_cr(result)
        for r in result:
            r['personas_involucradas_incidencia'] = self.format_personas_involucradas(r.get('personas_involucradas_incidencia',[]))
            r['acciones_tomadas_incidencia'] = self.format_acciones(r.get('acciones_tomadas_incidencia',[]))
            r['afectacion_patrimonial_incidencia'] = self.format_afectacion_patrimonial(r.get('afectacion_patrimonial_incidencia',[]))
            r['datos_deposito_incidencia'] = self.format_datos_deposito(r.get('datos_deposito_incidencia',[]))
            r['seguimientos_incidencia'] = self.format_seguimiento_incidencias(r.get('seguimientos_incidencia',[]))
            r['tags'] = self.format_tags_incidencias(r.get('tags',[]))
            r['prioridad_incidencia'] = r.get('prioridad_incidencia',[]).title()
        # print("resultados", simplejson.dumps(result, indent=4))
        return result

    def get_list_notes(self, location, area, status=None, limit=10, offset=0, dateFrom="", dateTo=""):
        '''
        Función para obtener las notas, puedes pasarle un area, una ubicacion, un estatus, una fecha desde
        y una fecha hasta
        '''
        response = []
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.ACCESOS_NOTAS,
            f"answers.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['location']}":location
        }
        if area and not area == 'todas':
            match_query.update({
                f"answers.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['area']}":area
            })
        if status != 'dia':
            match_query.update({f"answers.{self.notes_fields['note_status']}":status})
        if dateFrom and dateTo:
            if dateFrom == dateTo:
                if "T" not in dateFrom:
                    dateFrom += " 00:00:00"
                    dateTo += " 23:59:59"
            else:
                if "T" not in dateFrom:
                    dateFrom += " 00:00:00"
                if "T" not in dateTo:
                    dateTo += " 23:59:59"

            match_query.update({
                f"answers.{self.notes_fields['note_open_date']}": {"$gte": dateFrom, "$lte": dateTo}
            })
        elif dateFrom:
            if "T" not in dateFrom:
                dateFrom += " 00:00:00"
            match_query.update({
                f"answers.{self.notes_fields['note_open_date']}": {"$gte": dateFrom}
            })
        elif dateTo:
            if "T" not in dateTo:
                dateTo += " 23:59:59"
            match_query.update({
                f"answers.{self.notes_fields['note_open_date']}": {"$lte": dateTo}
            })
        query = [
            {'$match': match_query },
            {'$project': {
                "folio":"$folio",
                "created_by_name": f"$created_by_name",
                "created_by_id": f"$created_by_id",
                "created_by_email": f"$created_by_email",
                "note_status": f"$answers.{self.notes_fields['note_status']}",
                "note_open_date": f"$answers.{self.notes_fields['note_open_date']}",
                "note_close_date": f"$answers.{self.notes_fields['note_close_date']}",
                "note_booth": f"$answers.{self.notes_fields['note_catalog_booth']}.{self.notes_fields['note_booth']}",
                "note_guard": f"$answers.{self.notes_fields['note_catalog_guard']}.{self.notes_fields['note_guard']}",
                "note_guard_close": f"$answers.{self.notes_fields['note_catalog_guard_close']}.{self.notes_fields['note_guard_close']}",
                "note": f"$answers.{self.notes_fields['note']}",
                "note_file": f"$answers.{self.notes_fields['note_file']}",
                "note_pic": f"$answers.{self.notes_fields['note_pic']}",
                "note_comments": f"$answers.{self.notes_fields['note_comments_group']}",
            }},
            {'$sort':{'folio':-1}},
        ]
        
        query.append({'$skip': offset})
        query.append({'$limit': limit})
        
        records = self.format_cr(self.cr.aggregate(query))

        count_query = [
            {'$match': match_query},
            {'$count': 'total'}
        ]

        count_result = self.format_cr(self.cr.aggregate(count_query))
        total_count = count_result[0]['total'] if count_result else 0
        total_pages = ceil(total_count / limit) if limit else 1
        current_page = (offset // limit) + 1 if limit else 1

        notes = {
            'records': records,
            'total_records': total_count,
            'total_pages': total_pages,
            'actual_page': current_page
        }

        return notes

    def get_lista_pase(self, location, status='activo', inActive="true"):
        status_value = self.pase_entrada_fields.get('status_pase', '')
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.PASE_ENTRADA,
        }
        

        if inActive =="true":
              match_query[f"answers.{self.pase_entrada_fields['status_pase']}"] =  {"$ne": "activo"}
        else:
             match_query[f"answers.{self.pase_entrada_fields['status_pase']}"] = status

        proyect_fields = {'_id':1,
            'folio': f"$folio",
            'ubicacion': f"$answers.{self.mf['grupo_ubicaciones_pase']}.{self.UBICACIONES_CAT_OBJ_ID}.{self.f['location']}",
            'nombre': {"$ifNull":[
                f"$answers.{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{self.mf['nombre_visita']}",
                f"$answers.{self.mf['nombre_pase']}"]},
            'estatus':f"$answers.{self.pase_entrada_fields['status_pase']}",
            'empresa': {"$ifNull":[
                 f"$answers.{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{self.mf['empresa']}",
                 f"$answers.{self.pase_entrada_fields['walkin_empresa']}"]},
            'foto': {"$ifNull":[
                f"$answers.{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{self.mf['foto']}",
                f"$answers.{self.pase_entrada_fields['walkin_fotografia']}"]},
            }
        query = [
            {'$match': match_query },
            {'$unwind': f"$answers.{self.mf['grupo_ubicaciones_pase']}"},
            {'$match': {f"answers.{self.mf['grupo_ubicaciones_pase']}.{self.UBICACIONES_CAT_OBJ_ID}.{self.f['location']}":location}},
            {'$project': proyect_fields},
            {'$sort':{'_id':-1}},
        ]
        records = self.format_cr(self.cr.aggregate(query))
        for rec in records:
            rec['qr_code'] = rec['_id']
            rec['empresa'] = self.unlist(rec.get('empresa',[]))
        return  records

    def get_list_last_user_move(self, qr, limit=100, status=False):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.BITACORA_ACCESOS,
            f"answers.{self.mf['codigo_qr']}":qr,
        }

        if status == 'in':
            status = 'entrada'
        elif status == 'out':
            status = 'salida'
        elif status == 'deny':
            status = 'acceso_denegado'
        if status:
            match_query.update({
                f"answers.{self.bitacora_fields['status_visita']}": status
                })
        res = self.cr.find(
            match_query, 
            {
                'pase_status': f"$answers.{self.PASE_ENTRADA_OBJ_ID}.{self.pase_entrada_fields['status_pase']}",
                'comentarios': f"$answers.{self.bitacora_fields['grupo_comentario']}",
                'checkin_date': f"$answers.{self.bitacora_fields['fecha_entrada']}",
                'checkout_date': f"$answers.{self.bitacora_fields['fecha_salida']}",
                'duration':f"$answers.{self.mf['duracion']}",
                'equipos':f"$answers.{self.mf['grupo_equipos']}",
                'equipos':f"$answers.{self.mf['grupo_equipos']}",
                'folio':'$folio', 
                'fecha':f"$answers.{self.mf['fecha_entrada']}",
                'status_visita': f"$answers.{self.bitacora_fields['status_visita']}",
                'gafete_id': f"$answers.{self.GAFETES_CAT_OBJ_ID}.{self.gafetes_fields['gafete_id']}",
                'locker_id': f"$answers.{self.LOCKERS_CAT_OBJ_ID}.{self.mf['locker_id']}",
                'visita_a':f"$answers.{self.bitacora_fields['visita_a']}",
                #Vehiculos
                'vehiculos':f"$answers.{self.mf['grupo_vehiculos']}",
            }
            ).sort('updated_at', -1).limit(limit)

        result = self.format_cr(res)
        for r in result:
            r['vehiculos'] = self.format_vehiculos(r.get('vehiculos',[]))
            # r['equipos'] = self.format_equipos(r.get('equipos',[]))
            r['comentarios'] = self.format_comentarios(r.get('comentarios',[]))
            r['visita_a']= self.format_visita(r.get('visita_a',[]))
            # r['status_pase'] = r.get(self.pase_entrada_fields['status_pase'],'')
            # if r.get('comentario'):
            #     coment=[]
            #     for c in r['comentario']:
            #         row = {
            #             'comentario':c.get(self.bitacora_fields['comentario']),
            #             'tipo_comentario':c.get(self.bitacora_fields['tipo_comentario'])
            #         }
            #     coment.append(row)
            #     r['comentario'] = coment
            equipos = r.get('equipos', [])
            if equipos:  # Verifica si la lista de equipos no está vacía
                r['equipos'] = self.format_equipos(equipos)
            else:
                r['equipos'] = []  # O alguna otra lógica que desees aplicar si está vacía
                match_query2 = {
                    "deleted_at":{"$exists":False},
                    "form_id": self.PASE_ENTRADA,
                    f"answers.{self.mf['codigo_qr']}":qr,
                }
                res2= self.cr.find(
                match_query2, 
                {
                    'equipos':f"$answers.{self.mf['grupo_equipos']}",
                }).sort('updated_at', -1).limit(limit)
                result2 = self.format_cr(res2)
                for r2 in result2:
                    r['equipos'] = self.format_equipos(r2.get('equipos',[]))
        return result

    def get_pefiles_walkin(self, location):
        query = {
            "deleted_at":{"$exists":False},
            "form_id": self.CONF_PERFILES,
            f"answers.{self.PERFILES_OBJ_ID}.{self.mf['walkin']}":'Si'
        }
        format_filed = {
            'perfil': f"$answers.{self.PERFILES_OBJ_ID}.{self.mf['nombre_perfil']}",
            'ubicacion': f"$answers.{self.UBICACIONES_CAT_OBJ_ID}.{self.f['location']}"
            } 
        res = []
        for r in self.cr.find(query,format_filed):
            if r.get('perfil'):
                if location:
                    if r.get('ubicacion'): 
                        if r['ubicacion'] == location:
                            if r['perfil'] not in res:
                                res.append(r['perfil'])
                    else:
                        if r['perfil'] not in res:
                            res.append(r['perfil'])
                else:
                    if r['perfil'] not in res:
                        res.append(r['perfil'])
        return res
    
    def get_my_pases(self, tab_status, limit=10, skip=0, search_name=None):
        employee = self.get_employee_data(email=self.user.get('email'), get_one=True)
        user_data = self.lkf_api.get_user_by_id(self.user.get('user_id'))
        employee['timezone'] = user_data.get('timezone','America/Monterrey')
        fecha_hoy = datetime.now(pytz.timezone(employee.get('timezone'))).replace(microsecond=0).astimezone(pytz.utc).replace(tzinfo=None)
        fecha_hoy_formateada = fecha_hoy.strftime('%Y-%m-%d %H:%M:%S')
        match_query = {
            'form_id':self.PASE_ENTRADA,
            'deleted_at':{'$exists':False},
            f"answers.{self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID}.{self.pase_entrada_fields['autorizado_por']}":employee.get('worker_name'),
        }

        if tab_status == "Favoritos":
            match_query.update({f"answers.{self.pase_entrada_fields['favoritos']}":'si'})
        elif tab_status == "Activos":
            match_query.update({f"answers.{self.pase_entrada_fields['status_pase']}":'activo'})
        elif tab_status == "Vencidos":
            match_query.update({f"answers.{self.pase_entrada_fields['status_pase']}":'vencido'})

        if search_name:
            match_query.update({
                f"$or": [
                    {f"answers.{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{self.mf['nombre_visita']}": {"$regex": search_name, "$options": "i"}},
                    {f"answers.{self.mf['nombre_pase']}": {"$regex": search_name, "$options": "i"}}
                ]
            })
        # Conteo total de registros
        count_query = [
            {"$match": match_query},
            {"$count": "total"}
        ]
        count_result = self.format_cr(self.cr.aggregate(count_query))
        total_count = count_result[0]['total'] if count_result else 0
        current_page = (skip // limit) + 1
        total_pages = ceil(total_count / limit) if limit else 1

        query = [ 
            {"$match":match_query},
            {'$project':
                {
                    '_id': 1,
                    'folio': "$folio",
                    'favoritos':f"$answers.{self.pase_entrada_fields['favoritos']}",
                    'ubicacion': f"$answers.{self.mf['grupo_ubicaciones_pase']}.{self.UBICACIONES_CAT_OBJ_ID}.{self.f['location']}",
                    # 'ubicacion': f"$answers.{self.UBICACIONES_CAT_OBJ_ID}.{self.mf['ubicacion']}",
                    'nombre': {"$ifNull":[
                        f"$answers.{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{self.mf['nombre_visita']}",
                        f"$answers.{self.mf['nombre_pase']}"]},
                    'estatus': f"$answers.{self.pase_entrada_fields['status_pase']}",
                    'empresa': {"$ifNull":[
                         f"$answers.{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{self.mf['empresa']}",
                         f"$answers.{self.mf['empresa_pase']}"]},
                    'email':  {"$ifNull":[
                        f"$answers.{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{self.mf['email_vista']}",
                        f"$answers.{self.mf['email_pase']}"]},
                    'telefono': {"$ifNull":[
                        f"$answers.{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{self.mf['telefono']}",
                        f"$answers.{self.mf['telefono_pase']}"]},
                    'fecha_desde_visita': f"$answers.{self.mf['fecha_desde_visita']}",
                    'fecha_desde_hasta':{'$ifNull':[
                        f"$answers.{self.mf['fecha_desde_hasta']}",
                        f"$answers.{self.mf['fecha_desde_visita']}"]
                        },
                    'identificacion': {'$ifNull':[
                        f"$answers.{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{self.mf['identificacion']}",
                        f"$answers.{self.pase_entrada_fields['walkin_identificacion']}"]},
                    'foto': {'$ifNull':[
                        f"$answers.{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{self.mf['foto']}",
                        f"$answers.{self.pase_entrada_fields['walkin_fotografia']}"]},
                    'visita_a_nombre':
                        f"$answers.{self.mf['grupo_visitados']}.{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.mf['nombre_empleado']}",
                    'visita_a_puesto': 
                        f"$answers.{self.mf['grupo_visitados']}.{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.mf['puesto_empleado']}",
                    'visita_a_departamento':
                        f"$answers.{self.mf['grupo_visitados']}.{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.mf['departamento_empleado']}",
                    'visita_a_user_id':
                        f"$answers.{self.mf['grupo_visitados']}.{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.mf['user_id_empleado']}",
                    'visita_a_email':
                        f"$answers.{self.mf['grupo_visitados']}.{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['email']}",
                    'motivo_visita':f"$answers.{self.CONFIG_PERFILES_OBJ_ID}.{self.mf['motivo']}",
                    'tipo_de_pase':f"$answers.{self.pase_entrada_fields['perfil_pase']}",
                    'tema_cita':f"$answers.{self.pase_entrada_fields['tema_cita']}",
                    'descripcion':f"$answers.{self.pase_entrada_fields['descripcion']}",
                    'tipo_visita': f"$answers.{self.pase_entrada_fields['tipo_visita']}",
                    'limite_de_acceso': f"$answers.{self.mf['config_limitar_acceso']}",
                    'config_dia_de_acceso': f"$answers.{self.mf['config_dia_de_acceso']}",
                    'identificacion': {'$ifNull':[
                        f"$answers.{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{self.mf['identificacion']}",
                        f"$answers.{self.pase_entrada_fields['walkin_identificacion']}"]},
                    'limitado_a_dias':f"$answers.{self.mf['config_dias_acceso']}",
                    'perfil_pase':f"$answers.{self.CONFIG_PERFILES_OBJ_ID}",
                    'tipo_de_comentario': f"$answers.{self.mf['tipo_de_comentario']}",
                    'tipo_fechas_pase': f"$answers.{self.mf['tipo_visita_pase']}",
                    'enviar_correo_pre_registro': f"$answers.{self.pase_entrada_fields['enviar_correo_pre_registro']}",
                    'enviar_correo': f"$answers.{self.pase_entrada_fields['enviar_correo']}",
                    'grupo_areas_acceso': f"$answers.{self.mf['grupo_areas_acceso']}",
                    'grupo_equipos': f"$answers.{self.mf['grupo_equipos']}",
                    'grupo_vehiculos': f"$answers.{self.mf['grupo_vehiculos']}",
                    'grupo_instrucciones_pase': f"$answers.{self.mf['grupo_instrucciones_pase']}",
                    'comentario_area_pase':f"$answers.{self.mf['grupo_areas_acceso']}.{self.pase_entrada_fields['commentario_area']}",
                    'archivo_invitacion': f"$answers.{self.mf['archivo_invitacion']}",
                    'codigo_qr': f"$answers.{self.mf['codigo_qr']}",
                    'qr_pase': f"$answers.{self.mf['qr_pase']}",
                    'link':f"$answers.{self.pase_entrada_fields['link']}",
                    'perfil_pase': f"$answers.{self.mf['nombre_perfil']}",
                    'status_pase': f"$answers.{self.pase_entrada_fields['status_pase']}",
                    'pdf_to_img': f"$answers.{self.pase_entrada_fields['pdf_to_img']}"
                }
            },
            {'$sort':{'_id':-1}},
        ]
        query.append({'$skip': skip})
        query.append({'$limit': limit})
        records = self.format_cr(self.cr.aggregate(query))

        for x in records:
            qr_code = x.get('_id')
            total_entradas = self.get_count_ingresos(qr_code)
            if total_entradas:
                x['total_entradas'] = total_entradas.get('total_records')
            else:
                x['total_entradas'] = 0
            visita_a =[]
            v = x.pop('visita_a_nombre') if x.get('visita_a_nombre') else []
            d = x.get('visita_a_departamento',[])
            p = x.get('visita_a_puesto',[])
            e =  x.get('visita_a_user_id',[])
            u =  x.get('visita_a_email',[])

            for idx, nombre in enumerate(v):
                emp = {'nombre':nombre}
                if d:
                    emp.update({'departamento':d[idx].pop(0) if d[idx] else ""})
                if p:
                    emp.update({'puesto':p[idx].pop(0) if p[idx] else ""})
                if e:
                    emp.update({'user_id':e[idx].pop(0) if e[idx] else ""})
                if u:
                    emp.update({'email': u[idx].pop(0) if u[idx] else ""})
                visita_a.append(emp)
            if x['tipo_de_pase'] == 'Visita General' or x['tipo_de_pase'] == 'visita general':
                x['visita_a'] = visita_a
                x['favoritos'] = x.get('favoritos', [""]) if x.get('favoritos') else ""
                x['motivo_visita'] = x.get('motivo_visita', [""]) if x.get('motivo_visita') else ""
                x['email'] = x.get('email', [""]) if x.get('email') else ""
                x['empresa'] = x.get('empresa', [""]) if x.get('empresa') else ""
                x['telefono'] = x.get('telefono', [""]) if x.get('telefono') else ""
                # x['pdf'] = self.lkf_api.get_pdf_record(x['_id'], template_id = 447, name_pdf='Pase de Entrada', send_url=True)
            else:
                print("empresa email telefono",  x.get('empresa'))
                x['visita_a'] = visita_a
                x['favoritos'] = x.get('favoritos') or ""
                x['motivo_visita'] =x.get('motivo_visita') or ""
                x['email']= x.get('email') or ""
                x['empresa']= x.get('empresa') or ""
                x['telefono']= x.get('telefono') or ""
                # x['pdf'] = self.lkf_api.get_pdf_record(x[' # for idx, dic in enumerate(x['grupo_areas_acceso']):
            # x['comentario_area_pase']=x.pop('comentario_area_pase',[])
           

                # for key in list(item.keys()):
                #     if key in id_to_name_mapping:
                #         # Reemplaza el id hexadecimal por su nombre en el diccionario
                #         item[self.pase_entrada_fields['commentario_area']] = item.pop(key)

            for visita in x.get('visita_a', []):
                visita['departamento'] = visita['departamento'][0] if isinstance(visita.get('departamento'), list) and visita.get('departamento') else visita.get('departamento', "")
                visita['puesto'] = visita['puesto'][0] if isinstance(visita.get('puesto'), list) and visita.get('puesto') else visita.get('puesto', "")
                visita['user_id'] = visita['user_id'][0] if isinstance(visita.get('user_id'), list) and visita.get('user_id') else visita.get('user_id', "")
                visita['email'] = visita['email'][0] if isinstance(visita.get('email'), list) and visita.get('email') else visita.get('email', "")

            x['visita_a'] = [visita]
            x['status_pase'] = x.get('estatus', "")
            x['grupo_areas_acceso'] = self._labels_list(x.pop('grupo_areas_acceso',[]), self.mf)
            x['grupo_instrucciones_pase'] = self._labels_list(x.pop('grupo_instrucciones_pase',[]), self.mf)

            
            x['grupo_vehiculos'] = self.format_vehiculos_simple(x.pop('grupo_vehiculos',[]))
            x['grupo_equipos'] = self.format_equipos_simple(x.pop('grupo_equipos',[]))
            x['comentarios'] = x['grupo_instrucciones_pase']

            comentarios = []
            for item in x.pop('comentarios', []):
                comentario_pase = item.get('comentario_pase', '') 
                tipo_comentario = item.get('tipo_de_comentario', '')
                comentarios.append({
                    'comentario_pase': comentario_pase,
                    'tipo_comentario': tipo_comentario
                })
            x['comentarios'] = comentarios

            x.pop('visita_a_nombre', None)
            x.pop('visita_a_departamento', None)
            x.pop('visita_a_puesto', None)
            x.pop('visita_a_user_id', None)
            x.pop('visita_a_email', None)
        print("data", simplejson.dumps(records, indent=4))
        return  {
            "records": records,
            "total_records": total_count,
            "total_pages": total_pages,
            "actual_page": current_page,
            "records_on_page": len(records)
        }

    def get_pdf(self, qr_code, template_id=491, name_pdf='Pase de Entrada'):
        return self.lkf_api.get_pdf_record(qr_code, template_id = template_id, name_pdf =name_pdf, send_url=True)

    def get_pass_custom(self,qr_code):
        pass_selected= self.get_detail_access_pass(qr_code=qr_code)
        answers={}
        for key, value in pass_selected.items():
            if key == 'nombre' or \
               key == 'email' or \
               key == 'telefono' or \
               key == 'visita_a' or \
               key == 'ubicacion' or \
               key == 'fecha_de_expedicion' or \
               key == 'fecha_de_caducidad' or \
               key == "qr_pase" or \
               key =="_id" or \
               key == "estatus" or \
               key == "foto" or \
               key == "identificacion" or \
               key == "grupo_equipos" or \
               key == "grupo_vehiculos" or \
               key == "google_wallet_pass_url":
                answers[key] = value
        answers['folio']= pass_selected.get("folio")
        return answers

    def get_paquetes(self, location= "", area="", status="", dateFrom="", dateTo="", filterDate=""):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.PAQUETERIA,
        }
        if location:
             match_query[f"answers.{self.paquetes_fields['ubicacion_paqueteria']}"] = location
        if area:
             match_query[f"answers.{self.paquetes_fields['area_paqueteria']}"] = area
        if status:
             match_query[f"answers.{self.paquetes_fields['estatus_paqueteria']}"] = status

        user_data = self.lkf_api.get_user_by_id(self.user.get('user_id'))
        zona = user_data.get('timezone','America/Monterrey')

        if filterDate != "range":
            dateFrom, dateTo = self.get_range_dates(filterDate,zona)

            if dateFrom:
                dateFrom = str(dateFrom)
            if dateTo:
                dateTo = str(dateTo)
        if dateFrom and dateTo:
            match_query.update({
                f"answers.{self.paquetes_fields['fecha_recibido_paqueteria']}": {"$gte": dateFrom, "$lte": dateTo},
            })
        elif dateFrom:
            match_query.update({
                f"answers.{self.paquetes_fields['fecha_recibido_paqueteria']}": {"$gte": dateFrom}
            })
        elif dateTo:
           match_query.update({
                f"answers.{self.paquetes_fields['fecha_recibido_paqueteria']}": {"$lte": dateTo}
            })

        query = [
            {'$match': match_query },
            {'$project': {
                "folio":"$folio",
                "_id":"$_id",
                'ubicacion_paqueteria':f"$answers.{self.paquetes_fields['ubicacion_paqueteria']}",
                'area_paqueteria': f"$answers.{self.paquetes_fields['area_paqueteria']}",
                'fotografia_paqueteria':f"$answers.{self.paquetes_fields['fotografia_paqueteria']}",
                'descripcion_paqueteria':f"$answers.{self.paquetes_fields['descripcion_paqueteria']}",
                'quien_recibe_paqueteria':f"$answers.{self.paquetes_fields['quien_recibe_cat']}.{self.paquetes_fields['quien_recibe_paqueteria']}",
                'guardado_en_paqueteria': f"$answers.{self.paquetes_fields['guardado_en_paqueteria']}",
                'fecha_recibido_paqueteria': f"$answers.{self.paquetes_fields['fecha_recibido_paqueteria']}",
                'fecha_entregado_paqueteria': f"$answers.{self.paquetes_fields['fecha_entregado_paqueteria']}",
                'estatus_paqueteria': f"$answers.{self.paquetes_fields['estatus_paqueteria']}",
                'entregado_a_paqueteria': f"$answers.{self.paquetes_fields['entregado_a_paqueteria']}",
                'proveedor': f"$answers.{self.paquetes_fields['proveedor_cat']}.{self.paquetes_fields['proveedor']}",
            }},
            {'$sort':{'folio':-1}},
        ]
        if not filterDate:
            query.append(
                {"$limit":25}
            )
        pr= self.format_cr_result(self.cr.aggregate(query))
        for x in pr:
            status = x.get('estatus_paqueteria', [])
            x['estatus_paqueteria'] = status.pop() if status else ""
        return pr
    
    def get_range_dates(self, period, zona):
        now = arrow.now(zona) 
        start_date = None
        end_date = None

        if period == 'today':
            start_date = now.floor('day')
            end_date = now.floor('day').shift(days=+1).shift(seconds=-1)
        elif period == 'yesterday':
            now = now.shift(days=-1)
            start_date = now.floor('day')
            end_date = now.floor('day').shift(days=+1).shift(seconds=-1)
        elif period == 'this_week':
            start_date = now.floor('week')
            end_date = now.ceil('week').shift(days=+1).shift(seconds=-1)
        elif period == 'last_week':
            start_date = now.shift(weeks=-1).floor('week')
            end_date = start_date.ceil('week').shift(seconds=-1)
        elif period == 'last_fifteen_days':
            start_date = now.shift(days=-15).floor('day')
            end_date = now.shift(days=+1).floor('day').shift(seconds=-1)
        elif period == 'this_month':
            start_date = now.floor('month')  # El primer día del mes
            end_date = now.ceil('month').shift(days=+1).shift(seconds=-1)
        elif period == 'last_month':
            start_date = now.replace(day=1, month=now.month-1, year=now.year).floor('day')
            end_date = start_date.shift(months=+1).shift(seconds=-1)
        elif period == 'this_year':
            start_date = now.replace(month=1, day=1, year=now.year).floor('day')
            end_date = now.shift(days=+1).floor('day').shift(seconds=-1)
        elif period == 'last_year':
            start_date = now.replace(month=1, day=1, year=now.year-1).floor('day')
            end_date = now.replace(month=12, day=31, year=now.year-1).shift(seconds=-1)

        if isinstance(start_date, arrow.Arrow):
            start_date = start_date.datetime.replace(tzinfo=None)

        if isinstance(end_date, arrow.Arrow):
            end_date = end_date.datetime.replace(tzinfo=None)

        return start_date, end_date

    def get_user_booths_availability(self, turn_areas=True):
        '''
        Regresa las castas configurados por usuario y su stats
        TODO, se puede mejorar la parte de la obtencion de la direccion para hacerlo en 1 sola peticion
        '''
        default_booth , user_booths = self.get_user_booth(search_default=False, turn_areas=turn_areas)
        user_booths.insert(0, default_booth)
        user_booths_with_area = []
        for booth in user_booths:
            booth_area = booth.get('area')
            if booth_area:
                location = booth.get('location')
                booth_status = self.get_booth_status(booth_area, location)
                booth['status'] = booth_status.get('status', 'Disponible')
                booth_address = self.get_area_address(location, booth_area)
                booth_address.pop('_id')
                booth_address.pop('folio')
                booth.update(booth_address)
                user_booths_with_area.append(booth)
        return user_booths_with_area

    def get_user_contacts(self):
        user_id = self.user['user_id']
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.PASE_ENTRADA,
            "created_by_id": user_id
            }

        query = [
            {'$match': match_query },
            {'$group':{
                '_id':{
                    'nombre':f"$answers.{self.pase_entrada_fields['walkin_nombre']}"
                    },
                'email': {'$last':f"$answers.{self.pase_entrada_fields['walkin_email']}"},
                'empresa': {'$last':f"$answers.{self.pase_entrada_fields['walkin_empresa']}"},
                'fotografia': {'$last':f"$answers.{self.pase_entrada_fields['walkin_fotografia']}"},
                'identificacion': {'$last':f"$answers.{self.pase_entrada_fields['walkin_identificacion']}"},
                'telefono': {'$last':f"$answers.{self.pase_entrada_fields['walkin_telefono']}"},
                }
            },
            {"$project":{
                "nombre":"$_id.nombre",
                "email":"$email",
                "empresa":"$empresa",
                "fotografia":"$fotografia",
                "identificacion":"$identificacion",
                "telefono":"$telefono",
            }},
            {'$sort':{'nombre':-1}},
            ]
        return self.format_cr(self.cr.aggregate(query))        
    
    def check_in_aux_guard(self):
        match_query = {
            "deleted_at": {"$exists": False},
            "form_id": self.CHECKIN_CASETAS,
        }
        query = [
            {'$match': match_query},
            {'$unwind': f"$answers.{self.f['guard_group']}"},
            {'$project': {
                '_id': 1,
                'folio': "$folio",
                'created_at': "$created_at",
                'name': f"$answers.{self.f['guard_group']}.{self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID}.{self.f['worker_name_jefes']}",
                'user_id': {"$first": f"$answers.{self.f['guard_group']}.{self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID}.{self.f['user_id_jefes']}"},
                'location': f"$answers.{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.mf['ubicacion']}",
                'area': f"$answers.{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.mf['nombre_area']}",
                'checkin_date': f"$answers.{self.f['guard_group']}.{self.f['checkin_date']}",
                'checkout_date': f"$answers.{self.f['guard_group']}.{self.f['checkout_date']}",
                'checkin_status': f"$answers.{self.f['guard_group']}.{self.f['checkin_status']}",
                'checkin_position': f"$answers.{self.f['guard_group']}.{self.f['checkin_position']}",
            }},
            {'$sort': {'updated_at': -1}},
            {'$group': {
                '_id': {'user_id': '$user_id'},
                'name': {'$last': '$name'},
                'location': {'$last': '$location'},
                'area': {'$last': '$area'},
                'checkin_date': {'$last': '$checkin_date'},
                'checkout_date': {'$last': '$checkout_date'},
                'checkin_status': {'$last': '$checkin_status'},
                'checkin_position': {'$last': '$checkin_position'},
            }},
            {'$project': {
                '_id': 0,
                'user_id': '$_id.user_id',
                'name': '$name',
                'location': '$location',
                'area': '$area',
                'checkin_date': '$checkin_date',
                'checkout_date': '$checkout_date',
                'checkin_status': {'$cond': [{'$eq': ['$checkin_status', 'entrada']}, 'in', 'out']},
                'checkin_position': '$checkin_position',
            }},
        ]
        data = self.format_cr(self.cr.aggregate(query))
        res = {}
        for rec in data:
            status = 'in' if rec.get('checkin_status') in ['in', 'entrada'] else 'out'
            res[int(rec.get('user_id', 0))] = {
                'status': status,
                'name': rec.get('name'),
                'user_id': rec.get('user_id'),
                'location': rec.get('location'),
                'area': rec.get('area'),
                'checkin_date': rec.get('checkin_date'),
                'checkout_date': rec.get('checkout_date'),
                'checkin_position': rec.get('checkin_position')
            }
        return res

    def get_shift_data(self, booth_location=None, booth_area=None, search_default=True):
        """
        Obtiene informacion del turno del usuario logeado
        """

        load_shift_json = { }
        username = self.user.get('username')
        user_id = self.user.get('user_id')
        config_accesos_user="" #get_config_accesos(user_id)
        user_status = self.get_employee_checkin_status(user_id, as_shift=True,  available=False)
        this_user = user_status.get(user_id)
        if not this_user:
            this_user =  self.get_employee_data(email=self.user.get('email'), get_one=True)
            this_user['name'] = this_user.get('worker_name','')
        user_booths = []
        guards_positions = self.config_get_guards_positions()
        if not guards_positions:
            self.LKFException({"status_code":400, "msg":'No Existen puestos de guardias configurados.'})

        if this_user and this_user.get('status') == 'out':
            check_aux_guard = self.check_in_aux_guard()

            for user_id_aux, each_user in check_aux_guard.items():
                if user_id_aux == user_id:
                    this_user = each_user
                    this_user['status'] = 'in' if each_user.get('status') == 'in' else 'out'
                    this_user['location'] = each_user.get('location')
                    this_user['area'] = each_user.get('area')
                    this_user['checkin_date'] = each_user.get('checkin_date')
                    this_user['checkout_date'] = each_user.get('checkout_date')
                    this_user['checkin_position'] = each_user.get('checkin_position')

        if this_user and this_user.get('status') == 'in':
            location_employees = {self.chife_guard:{},self.support_guard:[]}
            booth_area = this_user['area']
            booth_location = this_user['location']
            for u_id, each_user in user_status.items():
                if u_id == user_id:
                    location_employees[self.support_guard].append(each_user)
                    guard = each_user
                else:
                    if each_user.get('status') == 'in':
                        location_employees[self.support_guard].append(each_user)
        else:
            # location_employees = {}
            default_booth , user_booths = self.get_user_booth(search_default=False)
            # location = default_booth.get('location')
            if not booth_location:
                booth_area = default_booth.get('area')
            if not booth_location:
                booth_location = default_booth.get('location')
            if not default_booth:
                return self.LKFException({"status_code":400, "msg":'No booth found or configure for user'})
            location_employees = self.get_booths_guards(booth_location, booth_area, solo_disponibles=True)
            guard = self.get_user_guards(location_employees=location_employees)
            if not guard:
                return self.LKFException({
                    "status_code":400, 
                    "msg":f"Usuario {self.user['user_id']} no confgurado como guardia, favor de revisar su configuracion."}) 
        location_employees = self.set_employee_pic(location_employees)
        booth_address = self.get_area_address(booth_location, booth_area)
        notes = self.get_list_notes(booth_location, booth_area, status='abierto')
        load_shift_json["location"] = {
            "name":  booth_location,
            "area": booth_area,
            "city": booth_address.get('city'),
            "state": booth_address.get('state'),
            "address": booth_address.get('address'),
            }
        # guards_online = self.get_guards_booths(booth_location, booth_area)
        load_shift_json["booth_stats"] = self.get_page_stats( booth_area, booth_location, "Turnos")
        load_shift_json["booth_status"] = self.get_booth_status(booth_area, booth_location)
        # load_shift_json["support_guards"] = location_employees[self.support_guard]
        load_shift_json["support_guards"] = location_employees.get(self.support_guard, "")
        load_shift_json["guard"] = self.update_guard_status(guard, this_user)
        load_shift_json["notes"] = notes
        load_shift_json["user_booths"] = user_booths
        load_shift_json['config_accesos_user']=config_accesos_user
        # load_shift_json["guards_online"] = guards_online
        return load_shift_json

    def get_user_last_checkin(self, user_id=False):
        if not user_id:
            user_id = self.user.get('user_id')
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.CHECKIN_CASETAS,
            "created_by_id": user_id
            }
        query = [
            {'$match': match_query },
            {'$project': self.proyect_format(self.checkin_fields)},
            {'$sort':{'updated_at':-1}},
            {'$limit':1}
            ]
        return self.format_cr_result(self.cr.aggregate(query), get_one=True)

    def get_user_guards(self, location_employees=[]):
        location_guards = []
        for clave in ["guardia_de_apoyo", "guardia_lider"]:
            if location_employees.get(clave):
                for usuario in location_employees[clave]:
                    if usuario.get("user_id") == self.user.get('user_id'):
                        location_guards = location_employees[clave]
                
        location_employees = location_guards

        for employee in location_employees:
            if employee.get('user_id',0) == self.user.get('user_id'):
                    return employee
        self.LKFException(f"El usuario con id {self.user['user_id']}, no se ecuentra configurado como guardia")

    def get_guards_booths(self, location, area):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.CHECKIN_CASETAS,
            f"answers.{self.mf['catalog_guard']}.{self.mf['ubicacion']}":location,
            f"answers.{self.mf['catalog_guard']}.{self.mf['nombre_area']}":area,
            f"answers.{self.checkin_fields['checkin_type']}":'apertura',
        }
        query = [
            {'$match': match_query },
            {'$project': {
                "_id": 1,
                "folio": "$folio",
                "name": f"$answers.{self.mf['guard_group']}.{self.mf['catalog_guard_close']}.{self.mf['nombre_guardia_apoyo']}",
            }},
            {'$sort':{'folio':-1}},
            {'$limit':1},
        ]
        #return self.format_cr_result(self.format_cr_result(self.cr.aggregate(query)))
        response = self.format_cr_result(self.format_cr_result(self.cr.aggregate(query)))
        if len(response) == 1:
            list_guards = response[0].get('name',[])
            return list_guards
        else:
            return []

    def get_valiaciones_certificado(self, certificacion, id_user, empresa=None, detail=False):
        cert = self.get_certificacion(certificacion, id_user, empresa=empresa)
        if cert:
            return self.do_validacion_certificado(cert, detail=detail)
        else:
            return 'No Encontrado'

    def user_in_facility(self, status_visita):
        """
        Si envias un registro con entrada quiere regresa Verdadero, si 
        """
        if not status_visita:
            return False
        elif status_visita in ('entrada'):
            return True
        else:
            return False

    def is_boot_available(self, location, area):
        # Verifica si el boot está disponible para check-in.

        self.last_check_in = self.get_last_checkin(location, area)
        last_status = self.last_check_in.get('checkin_type')
        if last_status in ['entrada','apertura']:
            return False
        else:
            return True

    def set_checkout_employees(self, checkin={}, employee_list=[], replace=True):
        # Establece los empleados para check-out.
        
        if not replace:
            checkin[self.f['guard_group']] = employee_list
        elif employee_list and replace:
            checkin[self.f['guard_group']] += [
                {self.f['employee_position']:'guardiad_de_apoyo',
                 self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID:
                   {self.f['worker_name_b']:guard.get('name'),
                   }} 
                    for guard in employee_list ]
        return checkin

    def search_pass(self, qr_code=None, location=None):
        # Busca el pase de acceso con el código QR o ubicación

        if not qr_code and not location:
            msg = "Debes de proveer qr_code o location"
            self.LKFException(msg)
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.PASE_ENTRADA,
            }
        if qr_code:
            match_query.update({"_id":ObjectId(qr_code)})
        if location:
            match_query.update({f"answers.{self.UBICACIONES_CAT_OBJ_ID}.{self.f['location']}":location})
        query = [
            {'$match': match_query },
            {'$project': self.proyect_format(self.mf)},
            {'$sort':{'updated_at':-1}},
            {'$limit':1}
            ]
        return self.format_cr_result(self.cr.aggregate(query), get_one=True)

    def search_access_pass(self, qr_code=None, location=None):
        """
        Busca pases de acceso
        Si se entega el puro qr_code, se entrega la info de QR code
        Si se entrega el qr_code con location y area, te valida si el qr es valido para dicha area
        Si NO entregas el qr_code, te regresa todos los qr de dicha area y ubicacion
        Si no entregas nada, te regrea un warning...
        """
        last_move = {}
        if self.validate_value_id(qr_code):
            last_moves = self.get_list_last_user_move(qr_code, limit=10)
            if len(last_moves) > 0:
                last_move = last_moves[0]
            # else:
            #     self.LKFException({"msg":"No se econtro ninguan entrada con pase "+ qr_code})
            # print('last_moves=',simplejson.dumps(last_moves, indent=3))
            #last_move = self.get_last_user_move(qr_code, location)
            gafete_info = {}
            access_pass = self.get_detail_access_pass(qr_code)
            if not last_move or last_move.get('status_visita') == 'salida':
                tipo_movimiento = 'Entrada'
                access_pass['grupo_vehiculos'] = self.format_vehiculos_simple(access_pass.get('grupo_vehiculos',[]))
                access_pass['grupo_equipos'] = self.format_equipos_simple(access_pass.get('grupo_equipos',[]))
                print("entrada",access_pass['grupo_vehiculos'])
            else:
                gafete_info['gafete_id'] = last_move.get('gafete_id')
                gafete_info['locker_id'] = last_move.get('locker_id')
                access_pass['grupo_vehiculos'] = self.format_vehiculos_simple(last_move.get('vehiculos',[]))
                access_pass['grupo_equipos'] = self.format_equipos_simple(last_move.get('equipos',[]))
                tipo_movimiento = 'Salida'
                print("salida", access_pass['grupo_vehiculos'],access_pass['grupo_equipos'])
                print("last_move", simplejson.dumps(last_move, indent=4))
            #---Last Access
            access_pass['ultimo_acceso'] = last_moves
            access_pass['tipo_movimiento'] = tipo_movimiento
            access_pass['gafete_id'] = gafete_info.get('gafete_id')
            access_pass['locker_id'] = gafete_info.get("locker_id")
            access_pass['status_pase']= self.unlist(access_pass.get('estatus',"")).title() or "" 
            access_pass['limitado_a_dias']= access_pass.get('limitado_a_dias','')
            access_pass['limitado_a_acceso']= access_pass.get('limite_de_acceso','')
            access_pass['config_dia_de_acceso']=access_pass.get('config_dia_de_acceso',"").replace("_", " ")
            total_entradas = self.get_count_ingresos(qr_code)
            access_pass['total_entradas'] = total_entradas.get('total_records') if total_entradas else "0"
            if access_pass.get('grupo_areas_acceso'):
                for area in access_pass['grupo_areas_acceso']:
                    area['status'] = self.get_area_status(access_pass['ubicacion'], area['nombre_area'])
            return access_pass
        else:
            return self.LKFException({"status_code":400, "msg":'El parametro para QR, no es valido'})

    def search_pass_by_status(self, status, query_update=None):
        match_query = {
            'form_id':self.PASE_ENTRADA,
            'deleted_at':{'$exists':False},
            f"answers.{self.pase_entrada_fields['status_pase']}":status,
        }
        if query_update:
            match_query.update(query_update)

        query = [ 
            {"$match":match_query},
            {'$project':
                {
                    '_id': 1,
                    'folio': "$folio",
                    'favoritos':f"$answers.{self.pase_entrada_fields['favoritos']}",
                    'ubicacion': f"$answers.{self.UBICACIONES_CAT_OBJ_ID}.{self.mf['ubicacion']}",
                    'nombre': {"$ifNull":[
                        f"$answers.{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{self.mf['nombre_visita']}",
                        f"$answers.{self.mf['nombre_pase']}"]},
                    'estatus': f"$answers.{self.pase_entrada_fields['status_pase']}",
                    'empresa': {"$ifNull":[
                         f"$answers.{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{self.mf['empresa']}",
                         f"$answers.{self.mf['empresa_pase']}"]},
                    'email':  {"$ifNull":[
                        f"$answers.{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{self.mf['email_vista']}",
                        f"$answers.{self.mf['email_pase']}"]},
                    'telefono': {"$ifNull":[
                        f"$answers.{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{self.mf['telefono']}",
                        f"$answers.{self.mf['telefono_pase']}"]},
                    'fecha_desde_visita': f"$answers.{self.mf['fecha_desde_visita']}",
                    'fecha_desde_hasta':{'$ifNull':[
                        f"$answers.{self.mf['fecha_desde_hasta']}",
                        f"$answers.{self.mf['fecha_desde_visita']}"]
                        },
                    'identificacion': {'$ifNull':[
                        f"$answers.{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{self.mf['identificacion']}",
                        f"$answers.{self.pase_entrada_fields['walkin_identificacion']}"]},
                    'foto': {'$ifNull':[
                        f"$answers.{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{self.mf['foto']}",
                        f"$answers.{self.pase_entrada_fields['walkin_fotografia']}"]},
                    'visita_a_nombre':
                        f"$answers.{self.mf['grupo_visitados']}.{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.mf['nombre_empleado']}",
                    'visita_a_puesto': 
                        f"$answers.{self.mf['grupo_visitados']}.{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.mf['puesto_empleado']}",
                    'visita_a_departamento':
                        f"$answers.{self.mf['grupo_visitados']}.{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.mf['departamento_empleado']}",
                    'visita_a_user_id':
                        f"$answers.{self.mf['grupo_visitados']}.{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.mf['user_id_empleado']}",
                    'visita_a_email':
                        f"$answers.{self.mf['grupo_visitados']}.{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.mf['email_empleado']}",
                    'motivo_visita':f"$answers.{self.CONFIG_PERFILES_OBJ_ID}.{self.mf['motivo']}",
                    'tipo_de_pase':f"$answers.{self.pase_entrada_fields['perfil_pase']}",
                    'tema_cita':f"$answers.{self.pase_entrada_fields['tema_cita']}",
                    'descripcion':f"$answers.{self.pase_entrada_fields['descripcion']}",
                    'tipo_visita': f"$answers.{self.pase_entrada_fields['tipo_visita']}",
                    'limite_de_acceso': f"$answers.{self.mf['config_limitar_acceso']}",
                    'config_dia_de_acceso': f"$answers.{self.mf['config_dia_de_acceso']}",
                    'identificacion': {'$ifNull':[
                        f"$answers.{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{self.mf['identificacion']}",
                        f"$answers.{self.pase_entrada_fields['walkin_identificacion']}"]},
                    'limitado_a_dias':f"$answers.{self.mf['config_dias_acceso']}",
                    'perfil_pase':f"$answers.{self.CONFIG_PERFILES_OBJ_ID}",
                    'tipo_de_comentario': f"$answers.{self.mf['tipo_de_comentario']}",
                    'tipo_fechas_pase': f"$answers.{self.mf['tipo_visita_pase']}",
                    'enviar_correo_pre_registro': f"$answers.{self.pase_entrada_fields['enviar_correo_pre_registro']}",
                    'enviar_correo': f"$answers.{self.pase_entrada_fields['enviar_correo']}",
                    'grupo_areas_acceso': f"$answers.{self.mf['grupo_areas_acceso']}",
                    'grupo_equipos': f"$answers.{self.mf['grupo_equipos']}",
                    'grupo_vehiculos': f"$answers.{self.mf['grupo_vehiculos']}",
                    'grupo_instrucciones_pase': f"$answers.{self.mf['grupo_instrucciones_pase']}",
                    'comentario': f"$answers.{self.mf['grupo_instrucciones_pase']}",
                    'comentario_area_pase':f"$answers.{self.mf['commentario_area']}",
                }
            },
            {'$sort':{'_id':-1}},
            # {'$limit':10}
        ]
        return self.format_cr(self.cr.aggregate(query))

    def set_boot_status(self, checkin_type):
        if checkin_type == 'in':
            set_boot_status = 'apertura'
        elif checkin_type == 'out':
            set_boot_status = 'cierre'
        return set_boot_status

    def set_employee_pic(self, employees):
        employee_ids = []
        for a, x in employees.items():
            if type(x) == list:
                for y in x:
                    employee_ids.append(y['user_id'])
            else:
                if x:
                    employee_ids.append(x['user_id'])
        pics = self.get_employee_pic(employee_ids)
        for a, x in employees.items():
            if type(x) == list:
                for y in x:
                    u_id = y['user_id']
                    if pics.get(u_id):
                        y['picture'] = pics[u_id]
            else:
                if x:
                    u_id = int(x['user_id'])
                    if pics.get(u_id):
                        x['picture'] = pics[u_id]
                    employee_ids.append(x['user_id'])
        return employees

    def update_article_concessioned(self, data_articles, folio):
        answers = {}
        for key, value in data_articles.items():
            if  key == 'ubicacion_concesion' or key == 'area_concesion':
                if data_articles['ubicacion_concesion'] and not data_articles['area_concesion']:
                    answers[self.consecionados_fields['ubicacion_catalog_concesion']] = {self.mf['ubicacion']:data_articles['ubicacion_concesion']}
                elif data_articles['area_concesion'] and not data_articles['ubicacion_concesion']:
                    answers[self.consecionados_fields['ubicacion_catalog_concesion']] = {self.mf['nombre_area_salida']:data_articles['area_concesion']}
                elif data_articles['area_concesion'] and data_articles['ubicacion_concesion']: 
                    answers[self.consecionados_fields['ubicacion_catalog_concesion']] = {self.mf['ubicacion']:data_articles['ubicacion_concesion'],
                    self.mf['nombre_area_salida']:data_articles['area_concesion']}
            elif  key == 'persona_nombre_concesion':
                answers[self.consecionados_fields['persona_catalog_concesion']] = { self.mf['nombre_guardia_apoyo'] : value}
            elif  key == 'caseta_concesion':
                answers[self.consecionados_fields['area_catalog_concesion']] = { self.mf['nombre_area_salida']: value}
            elif  key == 'area_concesion':
                dic_prev = answers.get(self.consecionados_fields['equipo_catalog_concesion'],{})
                dic_prev[self.consecionados_fields['area_concesion']] = value 
                answers[self.consecionados_fields['equipo_catalog_concesion']] = dic_prev
            elif  key == 'equipo_concesion':
                dic_prev = answers.get(self.consecionados_fields['equipo_catalog_concesion'],{})
                dic_prev[self.consecionados_fields['equipo_concesion']] = value 
                answers[self.consecionados_fields['equipo_catalog_concesion']] = dic_prev
            else:
                answers.update({f"{self.consecionados_fields[key]}":value})
        if answers or folio:
            return self.lkf_api.patch_multi_record( answers = answers, form_id=self.CONCESSIONED_ARTICULOS, folios=[folio])
        else:
            self.LKFException('No se mandarón parametros para actualizar')

    def update_article_lost(self, data_articles, folio):
        answers = {}
        employee = self.get_employee_data(email=self.user.get('email'), get_one=True)
        #---Define Answers
        date_entrega_perdido=""
        answers = {}
        for key, value in data_articles.items():
            if key == 'list_comments' or key == 'note_comments':
                answers.update({self.notes_fields['note_comments_group']:{-1:{f"{self.notes_fields[key]}": value}}})
            elif  key == 'tipo_articulo_perdido' or key == 'articulo_seleccion':
                if data_articles['tipo_articulo_perdido'] and not data_articles['articulo_seleccion']:
                    answers[self.perdidos_fields['tipo_articulo_catalog']] = {
                        self.perdidos_fields['tipo_articulo_perdido']: data_articles['tipo_articulo_perdido']
                        }
                elif data_articles['articulo_seleccion'] and not data_articles['tipo_articulo_perdido']:
                    answers[self.perdidos_fields['tipo_articulo_catalog']] = {
                        self.perdidos_fields['articulo_seleccion']: data_articles['articulo_seleccion']
                        }
                elif data_articles['articulo_seleccion'] and data_articles['tipo_articulo_perdido']: 
                    answers[self.perdidos_fields['tipo_articulo_catalog']] = {
                    self.perdidos_fields['tipo_articulo_perdido']:data_articles['tipo_articulo_perdido'],
                    self.perdidos_fields['articulo_seleccion']:data_articles['articulo_seleccion']}
            elif  key == 'ubicacion_perdido' or key == 'area_perdido':
                if data_articles['ubicacion_perdido'] and not data_articles['area_perdido']:
                    answers[self.perdidos_fields['ubicacion_catalog']] = {self.perdidos_fields['ubicacion_perdido']:data_articles['ubicacion_perdido']}
                elif data_articles['area_perdido'] and not data_articles['ubicacion_perdido']:
                    answers[self.perdidos_fields['ubicacion_catalog']] = {self.perdidos_fields['area_perdido']:data_articles['area_perdido']}
                elif data_articles['area_perdido'] and data_articles['ubicacion_perdido']: 
                    answers[self.perdidos_fields['ubicacion_catalog']] = {self.perdidos_fields['ubicacion_perdido']:data_articles['ubicacion_perdido'],
                    self.perdidos_fields['area_perdido']:data_articles['area_perdido']}
            elif key == 'quien_entrega_interno':
                answers[self.perdidos_fields['quien_entrega_catalog']] = {self.perdidos_fields['quien_entrega_interno']:value}
            elif key == 'locker_perdido':
                answers[self.perdidos_fields['locker_catalog']] = {self.perdidos_fields['locker_perdido']:value}
            elif key == 'estatus_perdido' and (value == 'donado' or value == 'entregado'):
                timezone = employee.get('cat_timezone', employee.get('timezone', 'America/Monterrey'))
                date_entrega_perdido =self.today_str(timezone, date_format='datetime')
                answers.update({
                    f"{self.perdidos_fields['date_entrega_perdido']}":date_entrega_perdido})
                answers.update({
                    f"{self.perdidos_fields['estatus_perdido']}":value})
            else:
                answers.update({f"{self.perdidos_fields[key]}":value})
        if answers or folio:
            res= self.lkf_api.patch_multi_record( answers = answers, form_id=self.BITACORA_OBJETOS_PERDIDOS, folios=[folio])
            if res.get('status_code') == 201 or res.get('status_code') == 202:
                res['json'].update({'date_entrega_perdido':date_entrega_perdido})
                return res
            else: 
                return res
        else:
            self.LKFException('No se mandarón parametros para actualizar')

    def update_failure(self, data_failures, folio):
        employee = self.get_employee_data(email=self.user.get('email'), get_one=True)
        answers = {}
        falla_fecha_hora_solucion=""
        for key, value in data_failures.items():
            if key == 'falla_ubicacion' or key == 'falla_caseta':
                if data_failures['falla_ubicacion'] and not data_failures['falla_caseta']:
                    answers[self.fallas_fields['falla_ubicacion_catalog']] = {self.fallas_fields['falla_ubicacion']:data_failures['falla_ubicacion']}
                elif data_failures['falla_caseta'] and not data_failures['falla_ubicacion']:
                    answers[self.fallas_fields['falla_ubicacion_catalog']] = {self.fallas_fields['falla_caseta']:data_failures['falla_caseta']}
                elif data_failures['falla_caseta'] and data_failures['falla_ubicacion']: 
                    answers[self.fallas_fields['falla_ubicacion_catalog']] = {self.fallas_fields['falla_ubicacion']:data_failures['falla_ubicacion'],
                    self.fallas_fields['falla_caseta']:data_failures['falla_caseta']}
            elif key == 'falla' or key== 'falla_objeto_afectado':
                answers[self.fallas_fields['falla_catalog']] = {self.fallas_fields['falla']:data_failures['falla'],
                self.fallas_fields['falla_subconcepto']:data_failures['falla_objeto_afectado']}
            elif key == 'falla_reporta_nombre':
                answers[self.fallas_fields['falla_reporta_catalog']] = {self.fallas_fields['falla_reporta_nombre']:value}
            elif key == 'falla_responsable_solucionar_nombre':
                answers[self.fallas_fields['falla_responsable_solucionar_catalog']] = {self.fallas_fields['falla_responsable_solucionar_nombre']:value}
            elif key == 'falla_estatus' and  value == 'resuelto':
                timezone = employee.get('cat_timezone', employee.get('timezone', 'America/Monterrey'))
                falla_fecha_hora_solucion =self.today_str(timezone, date_format='datetime')
                answers.update({
                    f"{self.fallas_fields['falla_fecha_hora_solucion']}":falla_fecha_hora_solucion})
                answers.update({
                    f"{self.fallas_fields['falla_estatus']}":value})
            else:
                answers.update({f"{self.fallas_fields[key]}":value})
        if answers or folio:
            res = self.lkf_api.patch_multi_record( answers = answers, form_id=self.BITACORA_FALLAS, folios=[folio])
            if res.get('status_code') == 201 or res.get('status_code') == 202:
                res['json'].update({'falla_fecha_hora_solucion':falla_fecha_hora_solucion})
                return res
            else:
                return res
        else:
            self.LKFException('No se mandarón parametros para actualizar')

    def update_failure_seguimiento(self, location=None, area=None, status=None, folio=None, falla_grupo_seguimiento=None):
        employee = self.get_employee_data(email=self.user.get('email'), get_one=True)
        failure_selected = self.get_list_fallas(location, area, folio=folio)
        if failure_selected:
            failure_selected = failure_selected[0]
        else:
            self.LKFException('No hay una falla registrada.')
        print('failure_selecteddddddddd', failure_selected)
        qr_code = failure_selected.get('_id')
        falla_nuevo_grupo = failure_selected.get('falla_grupo_seguimiento_formated', [])
        falla_nuevo_grupo_con_ids = []
        for falla in falla_nuevo_grupo:
            falla = {
                self.fallas_fields['falla_comentario_solucion']: falla.get('comentario'),
                self.fallas_fields['falla_folio_accion_correctiva']: falla.get('accion_correctiva'),
                self.fallas_fields['falla_evidencia_solucion']: falla.get('evidencia'),
                self.fallas_fields['falla_documento_solucion']: falla.get('documento'),
                self.fallas_fields['falla_inicio_seguimiento']: falla.get('fecha_inicio'),
                self.fallas_fields['falla_fin_seguimiento']: falla.get('fecha_fin'),    
            }
            falla_nuevo_grupo_con_ids.append(falla)

        falla_seg = {
            "falla_estatus": status,
            "falla_fecha_hora": failure_selected.get('falla_fecha_hora', ''),
            "falla_reporta_nombre": failure_selected.get('falla_reporta_nombre', ''),
            "falla_ubicacion": failure_selected.get('falla_ubicacion', ''),
            "falla_caseta": failure_selected.get('falla_caseta', ''),
            "falla": failure_selected.get('falla', ''),
            "falla_objeto_afectado": failure_selected.get('falla_objeto_afectado', ''),
            "falla_comentarios": failure_selected.get('falla_comentarios', ''),
            "falla_evidencia": failure_selected.get('falla_evidencia', []),
            "falla_documento": failure_selected.get('falla_documento', []),
            "falla_responsable_solucionar_nombre": failure_selected.get('falla_responsable_solucionar_nombre', ''),
            "falla_grupo_seguimiento": falla_grupo_seguimiento,
        }

        answers = {}
        falla_fecha_hora_solucion = ''

        if status == 'resuelto':
            timezone = employee.get('cat_timezone', employee.get('timezone', 'America/Monterrey'))
            falla_fecha_hora_solucion =self.today_str(timezone, date_format='datetime')
            answers.update({
                f"{self.fallas_fields['falla_fecha_hora_solucion']}": falla_fecha_hora_solucion
            })

        for key, value in falla_seg.items():
            if key == 'falla_reporta_nombre':
                answers.update({
                    self.fallas_fields['falla_reporta_catalog']: {
                        self.fallas_fields['falla_reporta_nombre']: value
                    }
                })
            elif key == 'falla_ubicacion':
                answers.update({
                    self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID: {
                        self.fallas_fields['falla_ubicacion']: falla_seg.get('falla_ubicacion'),
                        self.fallas_fields['falla_caseta']: falla_seg.get('falla_caseta')
                    }
                })
            elif key == 'falla':
                answers.update({
                    self.LISTA_FALLAS_CAT_OBJ_ID: {
                        self.fallas_fields['falla']: falla_seg.get('falla'),
                        self.fallas_fields['falla_subconcepto']: falla_seg.get('falla_objeto_afectado')
                    }
                })
            elif key == 'falla_responsable_solucionar_nombre':
                answers.update({
                    self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID: {
                        self.fallas_fields['falla_responsable_solucionar_nombre']: value
                    }
                })
            elif key == 'falla_grupo_seguimiento':
                fallas_seguimiento = [falla_seg.get('falla_grupo_seguimiento',{})]
                if fallas_seguimiento:
                    list_fallas_seguimiento = []
                    for item in fallas_seguimiento:
                        falla_folio = item.get('falla_folio_accion_correctiva','')
                        falla_comentario = item.get('falla_comentario_solucion','')
                        falla_foto_evidencia = item.get('falla_evidencia_solucion','')
                        falla_documento = item.get('falla_documento_solucion','')
                        falla_inicio_incidencia = item.get('fechaInicioFallaCompleta','')
                        falla_fin_incidencia = item.get('fechaFinFallaCompleta','')
                        list_fallas_seguimiento.append({
                            self.fallas_fields['falla_folio_accion_correctiva']:falla_folio,
                            self.fallas_fields['falla_comentario_solucion']:falla_comentario,
                            self.fallas_fields['falla_evidencia_solucion']:falla_foto_evidencia,
                            self.fallas_fields['falla_documento_solucion']:falla_documento,
                            self.fallas_fields['falla_inicio_seguimiento']:falla_inicio_incidencia,
                            self.fallas_fields['falla_fin_seguimiento']:falla_fin_incidencia,
                        })
                    falla_nuevo_grupo_con_ids.append(list_fallas_seguimiento[0])
                    answers[self.fallas_fields['falla_grupo_seguimiento']] = falla_nuevo_grupo_con_ids
            else:
                answers.update({f"{self.fallas_fields[key]}":value})

        if answers or folio:
            metadata = self.lkf_api.get_metadata(form_id=self.BITACORA_FALLAS)
            metadata.update(self.get_record_by_folio(folio, self.BITACORA_FALLAS, select_columns={'_id':1}, limit=1))

            metadata.update({
                    'properties': {
                        "device_properties":{
                            "system": "Addons",
                            "process":"Actualizacion de Falla", 
                            "accion":'update_failure_seguimiento', 
                            "folio": folio, 
                            "archive": "fallas.py"
                        }
                    },
                    'answers': answers,
                    '_id': qr_code
                })
            print(simplejson.dumps(metadata, indent=3))
            res= self.net.patch_forms_answers(metadata)
            if res.get('status_code') == 201 or res.get('status_code') == 202:
                res['json'].update({'falla_fecha_hora_solucion':falla_fecha_hora_solucion})
                return res
            else:
                return res
        else:
            self.LKFException('No se mandarón parametros para actualizar')

    def update_incidence_seguimiento(self, folio, incidencia_grupo_seguimiento, location=None, area=None):
        """
        Actualiza el seguimiento de una incidencia existente.
        folio: Folio de la incidencia a actualizar.
        incidencia_grupo_seguimiento: Lista de diccionarios con los datos del seguimiento.
        """
        incidence_selected = self.get_list_incidences(location, area, folio=folio)
        if incidence_selected:
            incidence_selected = incidence_selected[0]
        else:
            self.LKFException('No hay una incidencia registrada.')
        qr_code = incidence_selected.get('_id')
        incidencia_nuevo_grupo = incidence_selected.get('grupo_seguimiento_incidencia', [])
        incidencia_nuevo_grupo_con_ids = []
        for incidencia in incidencia_nuevo_grupo:
            incidencia = {
                self.incidence_fields['comentario_accion_correctiva_incidencia']: incidencia.get('comentario'),
                self.incidence_fields['accion_correctiva_incidencia']: incidencia.get('accion_correctiva'),
                self.incidence_fields['evidencia_accion_correctiva_incidencia']: incidencia.get('evidencia'),
                self.incidence_fields['documento_accion_correctiva_incidencia']: incidencia.get('documento'),
                self.incidence_fields['fecha_inicio_seg']: incidencia.get('fecha_inicio'),
                self.incidence_fields['fecha_fin_accion_correctiva_incidencia']: incidencia.get('fecha_fin'),    
            }
            incidencia_nuevo_grupo_con_ids.append(incidencia)
        print("cat", incidence_selected)
        incidencia_seg = {
            "incidencia_reporta_nombre": incidence_selected.get('reporta_incidencia', {}),
            "fecha_hora_incidencia": incidence_selected.get('fecha_hora_incidencia', ''),
            "incidencia_ubicacion": incidence_selected.get('ubicacion_incidencia', ''),
            "area_incidencia": incidence_selected.get('area_incidencia', ''),
            "incidencia": incidence_selected.get('incidencia', ''),
            "tipo_incidencia": incidence_selected.get('tipo_incidencia', ''),
            "comentario_incidencia": incidence_selected.get('comentario_incidencia', ''),
            "tipo_dano_incidencia": incidence_selected.get('tipo_dano_incidencia', []),
            "dano_incidencia": incidence_selected.get('dano_incidencia', ''),
            "personas_involucradas_incidencia": incidence_selected.get('personas_involucradas_incidencia', []),
            "acciones_tomadas_incidencia": incidence_selected.get('acciones_tomadas_incidencia', []),
            "evidencia_incidencia": incidence_selected.get('evidencia_incidencia', []),
            "documento_incidencia": incidence_selected.get('documento_incidencia', []),
            "prioridad_incidencia": incidence_selected.get('prioridad_incidencia', '').lower(),
            "notificacion_incidencia": incidence_selected.get('notificacion_incidencia', ''),
            "tags": incidence_selected.get('tags', []),
            "datos_deposito_incidencia": incidence_selected.get('datos_deposito_incidencia', []),
            "total_deposito_incidencia": incidence_selected.get('total_deposito_incidencia', []),
            "incidencia_grupo_seguimiento": incidencia_grupo_seguimiento,
            "categoria": incidence_selected.get("categoria", ''),
            "sub_categoria": incidence_selected.get("sub_categoria", ''),
            "incidente": incidence_selected.get("incidente", ''),
        }

        answers = {}

        for key, value in incidencia_seg.items():
            if key == 'categoria':
                answers[self.incidence_fields['incidencia_catalog']].update({
                    self.incidence_fields['categoria']: value
                })
            if key == 'sub_categoria':
                answers[self.incidence_fields['incidencia_catalog']].update({
                    self.incidence_fields['sub_categoria']: value
                })
            if key == 'incidente':
                answers[self.incidence_fields['incidencia_catalog']].update({
                    self.incidence_fields['incidente']: value
                })
            if key == 'incidencia_reporta_nombre':
                answers.update({
                    self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID: {
                        self.incidence_fields['reporta_incidencia']: value
                    }
                })
            elif key == 'incidencia_ubicacion' or key == 'area_incidencia':
                answers.update({
                    self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID: {
                        self.mf['ubicacion']: incidencia_seg.get('incidencia_ubicacion'),
                        self.mf['nombre_area']: incidencia_seg.get('area_incidencia')
                    }
                })
            elif key == 'incidencia':
                answers.update({
                    self.LISTA_INCIDENCIAS_CAT_OBJ_ID: {
                        self.incidence_fields['incidencia']: incidencia_seg.get('incidencia'),
                    }
                })
            elif key == 'personas_involucradas_incidencia':
                personas = incidencia_seg.get('personas_involucradas_incidencia',[])
                if personas:
                    personas_list = []
                    for c in personas:
                        personas_list.append(
                            {
                                self.incidence_fields['nombre_completo']:c.get('nombre_completo'),
                                self.incidence_fields['tipo_persona'] :c.get('tipo_persona')
                            }
                        )
                    answers.update({self.incidence_fields['personas_involucradas_incidencia']:personas_list})
            elif key == 'acciones_tomadas_incidencia':
                acciones = incidencia_seg.get('acciones_tomadas_incidencia',[])
                if acciones:
                    acciones_list = []
                    for c in acciones:
                        acciones_list.append(
                            {
                                self.incidence_fields['responsable_accion']:c.get('responsable_accion'),
                                self.incidence_fields['acciones_tomadas']:c.get('acciones_tomadas'),
                            }
                        )
                    answers.update({self.incidence_fields['acciones_tomadas_incidencia']:acciones_list})
            elif key == 'datos_deposito_incidencia':
                depositos = incidencia_seg.get('datos_deposito_incidencia',[])
                if depositos:
                    depositos_list = []
                    for c in depositos:
                        depositos_list.append(
                            {
                                self.incidence_fields['tipo_deposito']:c.get('tipo_deposito').lower(),
                                self.incidence_fields['cantidad']:c.get('cantidad'),
                            }
                        )
                    answers.update({self.incidence_fields['datos_deposito_incidencia']:depositos_list})
            elif key == 'tags':
                tags = incidencia_seg.get('tags',[])
                tags=["Accidente", "urgente"]
                if tags:
                    tags_list = []
                    for c in tags:
                        print("tags", c)

                        tags_list.append(
                            {
                                self.incidence_fields['tag']:c,
                            }
                        )
                    answers.update({self.incidence_fields['tags']:tags_list})
            elif key == 'incidencia_grupo_seguimiento':
                incidencias_seguimiento = [incidencia_seg.get('incidencia_grupo_seguimiento',{})]
                if incidencias_seguimiento:
                    list_incidencias_seguimiento = []
                    for item in incidencias_seguimiento:
                        print(item)
                        incidencia_folio = item.get('accion_correctiva_incidencia','')
                        incidencia_comentario = item.get('incidencia_comentario_solucion','')
                        incidencia_foto_evidencia = item.get('incidencia_evidencia_solucion','')
                        incidencia_documento = item.get('incidencia_documento_solucion','')
                        incidencia_inicio_incidencia = item.get('fechaInicioIncidenciaCompleta','')
                        incidencia_fin_incidencia = item.get('fechaFinIncidenciaCompleta','')
                        list_incidencias_seguimiento.append({
                            self.incidence_fields['accion_correctiva_incidencia']:incidencia_folio,
                            self.incidence_fields['comentario_accion_correctiva_incidencia']:incidencia_comentario,
                            self.incidence_fields['evidencia_accion_correctiva_incidencia']:incidencia_foto_evidencia,
                            self.incidence_fields['documento_accion_correctiva_incidencia']:incidencia_documento,
                            self.incidence_fields['fecha_inicio_seg']:incidencia_inicio_incidencia,
                            self.incidence_fields['fecha_fin_accion_correctiva_incidencia']:incidencia_fin_incidencia,
                        })
                    incidencia_nuevo_grupo_con_ids.append(list_incidencias_seguimiento[0])
                    answers[self.incidence_fields['grupo_seguimiento_incidencia']] = incidencia_nuevo_grupo_con_ids
            else:
                answers.update({f"{self.incidence_fields[key]}":value})

        if answers or folio:
            metadata = self.lkf_api.get_metadata(form_id=self.BITACORA_INCIDENCIAS)
            metadata.update(self.get_record_by_folio(folio, self.BITACORA_INCIDENCIAS, select_columns={'_id':1}, limit=1))

            metadata.update({
                    'properties': {
                        "device_properties":{
                            "system": "Addons",
                            "process":"Actualizacion de Incidencia", 
                            "accion":'update_incidence_seguimiento', 
                            "folio": folio, 
                            "archive": "incidencias.py"
                        }
                    },
                    'answers': answers,
                    '_id': qr_code
                })
            print(simplejson.dumps(metadata, indent=3))
            res= self.net.patch_forms_answers(metadata)
            if res.get('status_code') == 201 or res.get('status_code') == 202:
                return res
            else:
                return res
        else:
            self.LKFException('No se mandarón parametros para actualizar') 

    def update_incidence(self, data_incidences, folio):
        '''
            Realiza una actualización sobre cualquier nota, actualizando imagenes, status etc
        '''
        answers = {}
        for key, value in data_incidences.items():
            if key == 'categoria':
                answers[self.incidence_fields['incidencia_catalog']].update({
                    self.incidence_fields['categoria']:data_incidences['categoria']
                })
            if key == 'sub_categoria':
                answers[self.incidence_fields['incidencia_catalog']].update({
                    self.incidence_fields['sub_categoria']: data_incidences['sub_categoria']
                })
            if key == 'incidente':
                answers[self.incidence_fields['incidencia_catalog']].update({
                    self.incidence_fields['incidente']: data_incidences['incidente']
                })
            if  key == 'ubicacion_incidencia' or key == 'area_incidencia':
                if data_incidences['ubicacion_incidencia'] and not data_incidences['area_incidencia']:
                    answers[self.incidence_fields['ubicacion_incidencia_catalog']] = {self.incidence_fields['ubicacion_incidencia']:data_incidences['ubicacion_incidencia']}
                elif data_incidences['area_incidencia'] and not data_incidences['ubicacion_incidencia']:
                    answers[self.incidence_fields['ubicacion_incidencia_catalog']] = {self.incidence_fields['area_incidencia']:data_incidences['area_incidencia']}
                elif data_incidences['area_incidencia'] and data_incidences['ubicacion_incidencia']: 
                    answers[self.incidence_fields['ubicacion_incidencia_catalog']] = {self.incidence_fields['ubicacion_incidencia']:data_incidences['ubicacion_incidencia'],
                    self.incidence_fields['area_incidencia']:data_incidences['area_incidencia']}
            elif  key == 'reporta_incidencia':
                answers[self.incidence_fields['reporta_incidencia_catalog']] = {self.incidence_fields['reporta_incidencia']:value}
            elif  key == 'incidencia':
                answers[self.incidence_fields['incidencia_catalog']] = {self.incidence_fields['incidencia']:value}
            elif key == 'personas_involucradas_incidencia':
                personas = data_incidences.get('personas_involucradas_incidencia',[])
                if personas:
                    personas_list = []
                    for c in personas:
                        personas_list.append(
                            {
                                self.incidence_fields['nombre_completo']:c.get('nombre_completo'),
                                self.incidence_fields['rol'] :c.get('rol'),
                                self.incidence_fields['sexo'] :c.get('sexo'),
                                self.incidence_fields['grupo_etario'] :c.get('grupo_etario'),
                                self.incidence_fields['atencion_medica'] :c.get('atencion_medica'),
                                self.incidence_fields['retenido'] :c.get('retenido'),
                                self.incidence_fields['comentarios'] :c.get('comentarios')
                            }
                        )
                    answers.update({self.incidence_fields['personas_involucradas_incidencia']:personas_list})
            elif key == 'acciones_tomadas_incidencia':
                acciones = data_incidences.get('acciones_tomadas_incidencia',[])
                if acciones:
                    acciones_list = []
                    for c in acciones:
                        acciones_list.append(
                            {
                                self.incidence_fields['acciones_tomadas']:c.get('acciones_tomadas'),
                                self.incidence_fields['llamo_a_policia'] :c.get('llamo_a_policia'),
                                self.incidence_fields['autoridad'] :c.get('autoridad'),
                                self.incidence_fields['numero_folio_referencia'] :c.get('numero_folio_referencia'),
                                self.incidence_fields['responsable'] :c.get('responsable')
                            }
                        )
                    answers.update({self.incidence_fields['acciones_tomadas_incidencia']:acciones_list})
            elif key == 'seguimientos_incidencias':
                seg = data_incidences.get('seguimientos_incidencias',[])
                if seg:
                    seg_list = []
                    for c in seg:
                        seg_list.append(
                            {
                                self.incidence_fields['accion_correctiva_incidencia']:c.get('accion_correctiva_incidencia'),
                                self.incidence_fields['incidencia_personas_involucradas'] :c.get('incidencia_personas_involucradas'),
                                self.incidence_fields['fecha_inicio_sig'] :c.get('fechaInicioIncidenciaCompleta'),
                                self.incidence_fields['incidencia_documento_solucion'] :c.get('incidencia_documento_solucion'),
                                self.incidence_fields['incidencia_evidencia_solucion'] :c.get('incidencia_evidencia_solucion')
                            }
                        )
                    answers.update({self.incidence_fields['seguimientos_incidencias']:seg_list})
            elif key == 'afectacion_patrimonial_incidencia':
                ap = data_incidences.get('afectacion_patrimonial_incidencias',[])
                if ap:
                    ap_list = []
                    for c in ap:
                        ap_list.append(
                            {
                                self.incidence_fields['tipo_afectacion']:c.get('tipo_afectacion'),
                                self.incidence_fields['monto_estimado'] :c.get('monto_estimado'),
                                self.incidence_fields['duracion_estimada'] :c.get('duracion_estimada')
                            }
                        )
                    answers.update({self.incidence_fields['afectacion_patrimonial_incidencia']:ap_list})

            elif key == 'datos_deposito_incidencia':
                acciones = data_incidences.get('datos_deposito_incidencia',[])
                if acciones:
                    acciones_list = []
                    for c in acciones:
                        acciones_list.append(
                            {
                                self.incidence_fields['tipo_deposito']:c.get('tipo_deposito').lower().replace(" ","_"),
                                self.incidence_fields['cantidad'] :c.get('cantidad')
                            }
                        )
                    answers.update({self.incidence_fields['datos_deposito_incidencia']:acciones_list})
            elif key == 'prioridad_incidencia':
                answers[self.incidence_fields['prioridad_incidencia']] = f"{value}".lower()
            else:
                answers.update({f"{self.incidence_fields[key]}":value})
        if answers or folio:
            metadata = self.lkf_api.get_metadata(form_id=self.BITACORA_INCIDENCIAS)
            metadata.update(self.get_record_by_folio(folio, self.BITACORA_INCIDENCIAS, select_columns={'_id':1}, limit=1))
            metadata.update({
                    'properties': {
                        "device_properties":{
                            "system": "Addons",
                            "process":"Actualizacion de Incidencias", 
                            "accion":'update_incidence', 
                            "folio": folio, 
                            "archive": "incidencias.py"
                        }
                    },
                    'answers': answers
                })
            return self.net.patch_forms_answers(metadata)
            # return self.lkf_api.patch_multi_record( answers = answers, form_id=self.BITACORA_INCIDENCIAS, folios=[folio])
        else:
            self.LKFException('No se mandarón parametros para actualizar')

    def update_gafet_status(self, answers={}):
        if not answers:
            answers = self.answers

        status = None
        tipo_movimiento=None
        tipo_movimiento = answers.get(self.mf['tipo_registro'])
        res = {}
        location=""
        area=""
        if tipo_movimiento == "entrada":
            status = "En Uso"
        elif tipo_movimiento == 'salida':
            status = "Disponible"
        if status :
            gafete_id = answers[self.GAFETES_CAT_OBJ_ID][self.gafetes_fields['gafete_id']]
            locker_id = answers[self.LOCKERS_CAT_OBJ_ID][self.mf['locker_id']]
            if self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID in answers:
                if self.f['area'] in answers[self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID]:
                    area = answers[self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID][self.f['area']]
                if self.f['location'] in answers[self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID]:
                    location = answers[self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID][self.f['location']]
            
            gafete = self.get_gafetes(status=None, location=location, area=area, gafete_id=gafete_id)

            print("heloooo", gafete, gafete_id, status,tipo_movimiento)

            if len(gafete) > 0 :
                gafete = gafete[0]
                res = self.lkf_api.update_catalog_multi_record({self.mf['status_gafete']: status}, self.GAFETES_CAT_ID, record_id=[gafete['_id']])
            self.update_locker_status(tipo_movimiento, location, area, tipo_locker='Identificaciones', locker_id=locker_id)

        return res

    def update_guard_status(self, guard, this_user):
        # last_checkin = self.get_user_last_checkin(guard['user_id'])
        status_turn = 'Turno Cerrado'
        if this_user.get('status') == 'in':
            status_turn = 'Turno Abierto'

        guard['turn_start_datetime'] =  this_user.get('checkin_date')
        guard['status_turn'] =  status_turn
        return guard

    def update_guards_checkin(self, data_guard, record_id, location, area):
        user_data = self.lkf_api.get_user_by_id(self.user.get('user_id'))

        timezone = user_data.get('timezone','America/Monterrey')
        now_datetime =self.today_str(timezone, date_format='datetime')
        response = []
        checkin = self.check_in_out_employees('in', now_datetime, checkin={}, 
            employee_list=data_guard, **{'employee_type':self.support_guard})
        for idx, employee in enumerate(checkin.get(self.mf['guard_group'],[])):
            user_id = employee[self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID].get(self.f['user_id_jefes'])
            validate_status = self.get_employee_checkin_status(user_id)
            not_allowed = [uid for uid, u_data in validate_status.items() if u_data['status'] =='in']
            if not_allowed:
                msg = f"El usuario(s) con ids {not_allowed}. Se encuentran actualmente logeado en otra caseta."
                msg += f"Es necesario primero salirse de cualquier caseta antes de querer entrar a una casta"
                self.LKFException({'msg':msg,"title":'Accion Requerida!!!'})
            # checkin = self.checkin_data(employee, location, area, 'in', now_datetime)
            answers = {}
            answers[self.mf['guard_group']] = {'-1':employee}
            response.append(self.lkf_api.patch_multi_record( answers = answers, form_id=self.CHECKIN_CASETAS, record_id=[record_id]))
        return response

    def update_locker_status(self, tipo_movimiento, location, area, tipo_locker, locker_id):
        res = {}
        if tipo_movimiento == "entrada":
            status = "En Uso"
        elif tipo_movimiento == 'salida':
            status = "Disponible"

        locker = self.get_lockers(status=None, location=location, area=area, tipo_locker=tipo_locker, locker_id=locker_id)
        if len(locker) > 0 :
            locker = locker[0]
            res = self.lkf_api.update_catalog_multi_record({self.mf['status_locker']: status}, self.LOCKERS_CAT_ID, record_id=[locker['_id']])
        return res

    def update_notes(self, data_notes, folio):
        '''
            Realiza una actualización sobre cualquier nota, actualizando imagenes, status etc
        '''
        answers = {}
        #----Assign Value
        for key, value in data_notes.items():
            if not value:
                continue
            if key == 'list_comments' or key == 'note_comments':
                answers.update({self.notes_fields['note_comments_group']:{-1:{f"{self.notes_fields[key]}": value}}})
            elif  key == 'note_booth':
                answers[self.notes_fields['note_catalog_booth']] = {self.notes_fields['note_booth']:value}
            elif  key == 'note_guard':
                answers[self.notes_fields['note_catalog_guard']] = {self.notes_fields['note_guard']:value}
            else:
                answers.update({f"{self.notes_fields[key]}":value})
        #----Assign Time
        if data_notes.get('note_status','') == 'cerrado':
            employee = self.get_employee_data(email=self.user.get('email'), get_one=True)
            timezone = employee.get('cat_timezone', employee.get('timezone', 'America/Monterrey'))
            fecha_hora_str =self.today_str(timezone, date_format='datetime')
            answers.update({
                f"{self.notes_fields['note_close_date']}":fecha_hora_str,
                self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID :{
                    self.employee_fields['worker_name_b']:employee['worker_name'],
                    }
                }
                )

        if answers or folio:
            return self.lkf_api.patch_multi_record( answers = answers, form_id=self.ACCESOS_NOTAS, folios=[folio])
        else:
            self.LKFException('No se mandarón parametros para actualizar')

    def update_bitacora_entrada(self, data, record_id=None, folio=None):
        '''
            Realiza una actualización sobre cualquier nota, actualizando imagenes, status etc
        '''
        answers = {}
        action = data.get('action', 'create')
        equipos = data.get('equipos', data.get('equipo'))
        if equipos:
            tipo = equipos.get('tipo','').lower().replace(' ', '_')
            nombre = equipos.get('nombre','')
            marca = equipos.get('marca','')
            modelo = equipos.get('modelo','')
            color = equipos.get('color','')
            serie = equipos.get('serie','')
            ans = {
                self.mf['tipo_equipo']:tipo,
                self.mf['nombre_articulo']:nombre,
                self.mf['marca_articulo']:marca,
                self.mf['modelo_articulo']:modelo,
                self.mf['color_articulo']:color,
                self.mf['numero_serie']:serie,
            }
            if action == 'create':
                answers[self.mf['grupo_equipos']]  = {-1: ans }
            elif action == 'edit':
                answers[self.mf['grupo_equipos']]  = {data.get('set_number',0): ans }

        vehiculos = data.get('vehiculo',[])
        if vehiculos:
            tipo = vehiculos.get('tipo', vehiculos.get('tipo',''))
            marca = vehiculos.get('marca','')
            modelo = vehiculos.get('modelo','')
            estado = vehiculos.get('estado','')
            placas = vehiculos.get('placas',vehiculos.get('placas_vehiculo',''))
            color = vehiculos.get('color',vehiculos.get('color_vehiculo',''))
            ans = {
                    self.TIPO_DE_VEHICULO_OBJ_ID:{
                        self.mf['tipo_vehiculo']:tipo,
                        self.mf['marca_vehiculo']:marca,
                        self.mf['modelo_vehiculo']:modelo,
                    },
                    self.ESTADO_OBJ_ID:{
                        self.mf['nombre_estado']:estado,
                    },
                    self.mf['placas_vehiculo']:placas,
                    self.mf['color_vehiculo']:color,
                    }
            if action == 'create':
                answers[self.mf['grupo_vehiculos']]  = {-1: ans }
            elif action == 'edit':
                answers[self.mf['grupo_vehiculos']]  = {data.get('set_number',0): ans }
        #TODO UPDATE GAFET

        if not record_id and not folio:
            self.LKFException({'msg':'Se requiere el folio o el id del registro a editar'})
        if record_id:
            res =  self.lkf_api.patch_multi_record( answers = answers, form_id=self.BITACORA_ACCESOS, record_id=[record_id,])
        elif folio:
             res = self.lkf_api.patch_multi_record( answers = answers, form_id=self.BITACORA_ACCESOS, folios=[folio,])
        else:
            self.LKFException({'msg':'Faltan datos para acutalizar pase de entrada'})
        return res
        
    def update_bitacora_entrada_many(self, data, record_id=None, folio=None):
        answers = {}
        action = data.get('action', 'create')
        equipos = data.get('equipos', data.get('equipo'))
        if equipos:
            for i, equipo in enumerate(equipos):  # Iterar sobre cada equipo
                tipo = equipo.get('tipo_equipo', '').lower().replace(' ', '_')
                nombre = equipo.get('nombre_articulo', '')
                marca = equipo.get('marca_articulo', '')
                modelo = equipo.get('modelo_articulo', '')
                color = equipo.get('color_articulo', '')
                serie = equipo.get('numero_serie', '')
                ans = {
                    self.mf['tipo_equipo']: tipo,
                    self.mf['nombre_articulo']: nombre,
                    self.mf['marca_articulo']: marca,
                    self.mf['modelo_articulo']: modelo,
                    self.mf['color_articulo']: color,
                    self.mf['numero_serie']: serie,
                }
                
                if action == 'create':
                    # Usar -1 para nuevos registros en 'create'
                    answers[self.mf['grupo_equipos']] = answers.get(self.mf['grupo_equipos'], {})
                    answers[self.mf['grupo_equipos']][-1] = ans
                elif action == 'edit':
                    # Usar el número de conjunto especificado en 'edit'
                    set_number = data.get('set_number', 0)
                    answers[self.mf['grupo_equipos']] = answers.get(self.mf['grupo_equipos'], {})
                    answers[self.mf['grupo_equipos']][set_number] = ans

        # Procesar los vehículos
        vehiculos = data.get('vehiculo', [])
        if vehiculos:
            for i, vehiculo in enumerate(vehiculos):  # Iterar sobre cada vehículo
                tipo = vehiculo.get('tipo_vehiculo', vehiculo.get('tipo', ''))
                marca = vehiculo.get('marca_vehiculo', '')
                modelo = vehiculo.get('modelo_vehiculo', '')
                estado = vehiculo.get('nombre_estado', '')
                placas = vehiculo.get('placas', vehiculo.get('placas_vehiculo', ''))
                color = vehiculo.get('color', vehiculo.get('color_vehiculo', ''))
                
                ans = {
                    self.TIPO_DE_VEHICULO_OBJ_ID: {
                        self.mf['tipo_vehiculo']: tipo,
                        self.mf['marca_vehiculo']: marca,
                        self.mf['modelo_vehiculo']: modelo,
                    },
                    self.ESTADO_OBJ_ID: {
                        self.mf['nombre_estado']: estado,
                    },
                    self.mf['placas_vehiculo']: placas,
                    self.mf['color_vehiculo']: color,
                }

                if action == 'create':
                    # Usar -1 para nuevos registros en 'create'
                    answers[self.mf['grupo_vehiculos']] = answers.get(self.mf['grupo_vehiculos'], {})
                    answers[self.mf['grupo_vehiculos']][-1] = ans
                elif action == 'edit':
                    # Usar el número de conjunto especificado en 'edit'
                    set_number = data.get('set_number', 0)
                    answers[self.mf['grupo_vehiculos']] = answers.get(self.mf['grupo_vehiculos'], {})
                    answers[self.mf['grupo_vehiculos']][set_number] = ans
                #TODO UPDATE GAFET

        if not record_id and not folio:
            self.LKFException({'msg':'Se requiere el folio o el id del registro a editar'})
        if record_id:
            res =  self.lkf_api.patch_multi_record( answers = answers, form_id=self.BITACORA_ACCESOS, record_id=[record_id,])
        elif folio:
             res = self.lkf_api.patch_multi_record( answers = answers, form_id=self.BITACORA_ACCESOS, folios=[folio,])
        else:
            self.LKFException({'msg':'Faltan datos para acutalizar pase de entrada'})
        return res

    def update_pass(self, access_pass,folio=None):
        pass_selected= self.get_detail_access_pass(qr_code=folio)
        qr_code= folio
        _folio= pass_selected.get("folio")
        answers={}
        for key, value in access_pass.items():
            if key == 'grupo_vehiculos':
                answers[self.mf['grupo_vehiculos']]={}
                index=1
                for index, item in enumerate(access_pass.get('grupo_vehiculos',[])):
                    tipo = item.get('tipo','')
                    marca = item.get('marca','')
                    modelo = item.get('modelo','')
                    estado = item.get('estado','')
                    placas = item.get('placas','')
                    color = item.get('color','')
                    obj={
                        self.TIPO_DE_VEHICULO_OBJ_ID:{
                            self.mf['tipo_vehiculo']:tipo,
                            self.mf['marca_vehiculo']:marca,
                            self.mf['modelo_vehiculo']:modelo,
                        },
                        self.ESTADO_OBJ_ID:{
                            self.mf['nombre_estado']:estado,
                        },
                        self.mf['placas_vehiculo']:placas,
                        self.mf['color_vehiculo']:color,
                    }
                    answers[self.mf['grupo_vehiculos']][-index]=obj
            elif key == 'grupo_equipos':
                answers[self.mf['grupo_equipos']]={}
                index=1
                for index, item in enumerate(access_pass.get('grupo_equipos',[])):
                    nombre = item.get('nombre','')
                    marca = item.get('marca','')
                    color = item.get('color','')
                    tipo = item.get('tipo','')
                    serie = item.get('serie','')
                    modelo = item.get('modelo','')
                    obj={
                        self.mf['tipo_equipo']:tipo.lower(),
                        self.mf['nombre_articulo']:nombre,
                        self.mf['marca_articulo']:marca,
                        self.mf['numero_serie']:serie,
                        self.mf['color_articulo']:color,
                        self.mf['modelo_articulo']:modelo,
                    }
                    answers[self.mf['grupo_equipos']][-index]=obj
            elif key == 'status_pase':
                answers.update({f"{self.pase_entrada_fields[key]}":value.lower()})
            elif key == 'archivo_invitacion':
                answers.update({f"{self.pase_entrada_fields[key]}": value})
            elif key == "google_wallet_pass_url":
                answers.update({f"{self.pase_entrada_fields[key]}": value})
            elif key == "apple_wallet_pass":
                answers.update({f"{self.pase_entrada_fields[key]}": value})
            elif key == "pdf_to_img":
                answers.update({f"{self.pase_entrada_fields[key]}": value})
            elif key == 'favoritos':
                answers.update({f"{self.pase_entrada_fields[key]}": [value]})  
            elif key == 'conservar_datos_por':
                answers.update({f"{self.pase_entrada_fields[key]}": value.replace(" ", "_")})      
            else:
                answers.update({f"{self.pase_entrada_fields[key]}":value})

        print("ans", simplejson.dumps(answers, indent=4))
        # print(ans)
       
        employee = self.get_employee_data(email=self.user.get('email'), get_one=True)
        if answers:
            res= self.lkf_api.patch_multi_record( answers = answers, form_id=self.PASE_ENTRADA, record_id=[qr_code])
            if res.get('status_code') == 201 or res.get('status_code') == 202 and folio:
                if employee.get('usuario_id', [])[0] == 7742:
                    pdf = self.lkf_api.get_pdf_record(qr_code, template_id = 553, name_pdf='Pase de Entrada', send_url=True)
                else:
                    pdf = self.lkf_api.get_pdf_record(qr_code, template_id = 491, name_pdf='Pase de Entrada', send_url=True)
                res['json'].update({'qr_pase':pass_selected.get("qr_pase")})
                res['json'].update({'telefono':pass_selected.get("telefono")})
                res['json'].update({'enviar_a':pass_selected.get("nombre")})
                res['json'].update({'enviar_de':employee.get('worker_name')})
                res['json'].update({'enviar_de_correo':employee.get('email')})
                res['json'].update({'ubicacion':pass_selected.get('ubicacion')})
                res['json'].update({'fecha_desde':pass_selected.get('fecha_de_expedicion')})
                res['json'].update({'fecha_hasta':pass_selected.get('fecha_de_caducidad')})
                res['json'].update({'asunto':pass_selected.get('tema_cita')})
                res['json'].update({'descripcion':pass_selected.get('descripcion')})
                res['json'].update({'pdf_to_img': pass_selected.get('pdf_to_img')})
                res['json'].update({'pdf': pdf})
                return res
            else: 
                return res
        else:
            self.LKFException('No se mandarón parametros para actualizar')

    def update_full_pass(self, access_pass,folio=None, qr_code=None, location=None):
        answers = {}
        perfil_pase = access_pass.get('perfil_pase', 'Visita General')
        user_data = self.lkf_api.get_user_by_id(self.user.get('user_id'))
        timezone = user_data.get('timezone','America/Monterrey')
        now_datetime =self.today_str(timezone, date_format='datetime')
        answers[self.mf['grupo_visitados']] = []
        # answers[self.UBICACIONES_CAT_OBJ_ID] = {}
        # answers[self.UBICACIONES_CAT_OBJ_ID][self.f['location']] = location
        answers[self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID] = {}
        answers[self.CONFIG_PERFILES_OBJ_ID] = {}
        answers[self.VISITA_AUTORIZADA_CAT_OBJ_ID] = {}
        # answers[self.pase_entrada_fields['qr_pase']] = []

        for key, value in access_pass.items():
            if key == 'grupo_vehiculos':
                vehiculos = access_pass.get('grupo_vehiculos',[])
                if vehiculos:
                    list_vehiculos = []
                    for item in vehiculos:
                        tipo = item.get('tipo_vehiculo','')
                        marca = item.get('marca_vehiculo','')
                        modelo = item.get('modelo_vehiculo','')
                        estado = item.get('state','')
                        placas = item.get('placas_vehiculo','')
                        color = item.get('color_vehiculo','')
                        list_vehiculos.append({
                            self.TIPO_DE_VEHICULO_OBJ_ID:{
                                self.mf['tipo_vehiculo']:tipo,
                                self.mf['marca_vehiculo']:marca,
                                self.mf['modelo_vehiculo']:modelo,
                            },
                            self.ESTADO_OBJ_ID:{
                                self.mf['nombre_estado']:estado,
                            },
                            self.mf['placas_vehiculo']:placas,
                            self.mf['color_vehiculo']:color,
                        })
                    answers[self.mf['grupo_vehiculos']] = list_vehiculos  
            elif key == 'grupo_equipos':
                equipos = access_pass.get('grupo_equipos',[])
                if equipos:
                    list_equipos = []
                    for item in equipos:
                        tipo = item.get('tipo_equipo','').lower().replace(' ', '_')
                        nombre = item.get('nombre_articulo','')
                        marca = item.get('marca_articulo','')
                        modelo = item.get('modelo_articulo','')
                        color = item.get('color_articulo','')
                        serie = item.get('numero_serie','')
                        list_equipos.append({
                            self.mf['tipo_equipo']:tipo,
                            self.mf['nombre_articulo']:nombre,
                            self.mf['marca_articulo']:marca,
                            self.mf['modelo_articulo']:modelo,
                            self.mf['color_articulo']:color,
                            self.mf['numero_serie']:serie,
                        })
                    answers[self.mf['grupo_equipos']] = list_equipos
            elif key == 'grupo_instrucciones_pase':
                acciones = access_pass.get('grupo_instrucciones_pase',[])
                if acciones:
                    acciones_list = []
                    for c in acciones:
                        acciones_list.append(
                            {
                                self.pase_entrada_fields['tipo_comentario']:c.get('tipo_comentario'),
                                self.pase_entrada_fields['comentario_pase'] :c.get('comentario_pase')
                            }
                        )
                    answers.update({self.pase_entrada_fields['grupo_instrucciones_pase']:acciones_list})
            elif key == 'grupo_areas_acceso':
                acciones = access_pass.get('grupo_areas_acceso',[])
                if acciones:
                    acciones_list = []
                    for c in acciones:
                        acciones_list.append(
                            {
                                self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID : {
                                    self.pase_entrada_fields['nombre_area']:c.get('nombre_area')
                                } ,
                                self.pase_entrada_fields['commentario_area'] :c.get('commentario_area')
                            }
                        )
                    answers.update({self.pase_entrada_fields['grupo_areas_acceso']:acciones_list})
            elif key == 'autorizado_por':
                answers[self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID] = {
                    self.mf['nombre_guardia_apoyo'] : access_pass.get('autorizado_por', ''),
                }
            elif key == 'link':
                link_info=access_pass.get('link', '')
                if link_info:
                    docs=""
                    for index, d in enumerate(link_info["docs"]): 
                        if(d == "agregarIdentificacion"):
                            docs+="iden"
                        elif(d == "agregarFoto"):
                            docs+="foto"
                        if index==0 :
                            docs+="-"
                    link_pass= f"{link_info['link']}?id={link_info['qr_code']}&user={link_info['creado_por_id']}&docs={docs}"

                answers.update({f"{self.pase_entrada_fields[key]}":link_pass}) 
            elif key == 'ubicacion':
                # answers[self.pase_entrada_fields['ubicacion_cat']] = {self.mf['ubicacion']:access_pass['ubicacion']}
                ubicaciones = access_pass.get('ubicacion',[])
                if ubicaciones:
                    ubicaciones_list = []
                    for ubi in ubicaciones:
                        ubicaciones_list.append(
                            {
                                self.pase_entrada_fields['ubicacion_cat']:{ self.mf["ubicacion"] : ubi}
                            }
                        )
                    answers.update({self.pase_entrada_fields['ubicaciones']:ubicaciones_list})
            elif key == 'visita_a': 
                #Visita A
                answers[self.mf['grupo_visitados']] = []
                visita_a = access_pass.get('visita_a')
                visita_set = {
                    self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID:{
                        self.mf['nombre_empleado'] : visita_a,
                        }
                    }
                options_vistia = {
                      "group_level": 3,
                      "startkey": [location, visita_a],
                      "endkey": [location, f"{visita_a}\n",{}],
                    }
                cat_visita = self.catalogo_view(self.CONF_AREA_EMPLEADOS_CAT_ID, self.PASE_ENTRADA, options_vistia)
                if len(cat_visita) > 0:
                    cat_visita =  {key: [value,] for key, value in cat_visita[0].items() if value}
                visita_set[self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID].update(cat_visita)
                answers[self.mf['grupo_visitados']].append(visita_set)
            elif key == 'perfil_pase':
                # Perfil de Pase
                answers[self.CONFIG_PERFILES_OBJ_ID] = {}
                answers[self.CONFIG_PERFILES_OBJ_ID] = {
                    self.mf['nombre_perfil'] : perfil_pase,
                }
                options = {
                      "group_level": 2,
                      "startkey": [perfil_pase],
                      "endkey": [f"{perfil_pase}\n",{}],
                    }
                cat_perfil = self.catalogo_view(self.CONFIG_PERFILES_ID, self.PASE_ENTRADA, options)
                if len(cat_perfil) > 0:
                    cat_perfil[0][self.mf['motivo']]= [cat_perfil[0].get(self.mf['motivo'])]
                    cat_perfil = cat_perfil[0]
                answers[self.CONFIG_PERFILES_OBJ_ID].update(cat_perfil)
                if answers[self.CONFIG_PERFILES_OBJ_ID].get(self.mf['nombre_permiso']) and \
                   type(answers[self.CONFIG_PERFILES_OBJ_ID][self.mf['nombre_permiso']]) == str:
                    answers[self.CONFIG_PERFILES_OBJ_ID][self.mf['nombre_permiso']] = [answers[self.CONFIG_PERFILES_OBJ_ID][self.mf['nombre_permiso']],]
            elif key == 'archivo_invitacion':
                # id_forma = 121736
                id_forma = self.PASE_ENTRADA
                # id_campo = '673773741b2adb2d05d99d63'
                id_campo = self.pase_entrada_fields['archivo_invitacion']
                tema_cita = access_pass.get("tema_cita")
                descripcion = access_pass.get("descripcion")
                fecha_desde_visita = access_pass.get("fecha_desde_visita")
                fecha_desde_hasta = access_pass.get("fecha_desde_hasta")
                creado_por_email = access_pass.get("link", {}).get("creado_por_email")
                ubicacion = access_pass.get("ubicacion",'')
                nombre = access_pass.get("nombre_pase",'')
                visita_a = access_pass.get("visita_a",'')
                email = access_pass.get("email_pase",'')

                start_datetime = datetime.strptime(fecha_desde_visita, "%Y-%m-%d %H:%M:%S")

                if not fecha_desde_hasta:
                    stop_datetime = start_datetime + timedelta(hours=1)
                else:
                    stop_datetime = datetime.strptime(fecha_desde_hasta, "%Y-%m-%d %H:%M:%S")

                meeting = [
                    {
                        "id": 1,
                        "start": start_datetime,
                        "stop": stop_datetime,
                        "name": tema_cita,
                        "description": descripcion,
                        "location": ubicacion,
                        "allday": False,
                        "rrule": None,
                        "alarm_ids": [{"interval": "minutes", "duration": 10, "name": "Reminder"}],
                        'organizer_name': visita_a,
                        'organizer_email': creado_por_email,
                        "attendee_ids": [{"email": email, "nombre": nombre}, {"email": creado_por_email, "nombre": visita_a}],
                    }
                ]
                respuesta_ics = self.upload_ics(id_forma, id_campo, meetings=meeting)
                file_name = respuesta_ics.get('file_name', '')
                file_url = respuesta_ics.get('file_url', '')

                archivo_invitacion= [
                    {
                        "file_name": f"{file_name}",
                        "file_url": f"{file_url}"
                    }
                ]
                answers.update({f"{self.pase_entrada_fields[key]}": archivo_invitacion})
            else:
                answers.update({f"{self.pase_entrada_fields[key]}":value})

        if answers or folio:
            metadata = self.lkf_api.get_metadata(form_id=self.PASE_ENTRADA)
            metadata.update(self.get_record_by_folio(folio, self.PASE_ENTRADA, select_columns={'_id':1}, limit=1))

            metadata.update({
                    'properties': {
                        "device_properties":{
                            "system": "Addons",
                            "process":"Actualizacion de Pase de Entrada", 
                            "accion":'update_full_pass', 
                            "folio": folio, 
                            "archive": "pase_acceso.py"
                        }
                    },
                    'answers': answers,
                    '_id': qr_code
                })
            res= self.net.patch_forms_answers(metadata)
            return res
            # return self.lkf_api.patch_multi_record( answers = answers, form_id=self.BITACORA_INCIDENCIAS, folios=[folio,])
        else:
            self.LKFException('No se mandarón parametros para actualizar')

    def update_active_pass(self, folio=None, qr_code=None, update_obj={}):
        pass_selected= self.get_detail_access_pass(qr_code=qr_code)
        if not pass_selected.get('fecha_de_caducidad'):
            tipo_visita_pase = 'fecha_fija'
        else:
            tipo_visita_pase = 'rango_de_fechas'

        access_pass = {
            "autorizado_por": pass_selected.get('visita_a', '')[0].get('nombre'),
            "config_dias_acceso": pass_selected.get('limitado_a_dias', []),
            "config_limitar_acceso": pass_selected.get('limite_de_acceso'),
            "descripcion": pass_selected.get('descripcion', ''),
            "email_pase": pass_selected.get('email', ''),
            "enviar_correo": [],
            "enviar_correo_pre_registro": [],
            "fecha_desde_hasta": pass_selected.get('fecha_de_caducidad', ''),
            "fecha_desde_visita": pass_selected.get('fecha_de_expedicion', ''),
            "grupo_areas_acceso": pass_selected.get('grupo_areas_acceso', []),
            "grupo_equipos": update_obj.get('grupo_equipos'),
            "grupo_instrucciones_pase": pass_selected.get('grupo_instrucciones_pase', []),
            "grupo_vehiculos": update_obj.get('grupo_vehiculos'),
            "link": {
                "creado_por_email": update_obj.get('user_email', ''),
                "docs": [],
                "creado_por_id": pass_selected.get('visita_a', '')[0].get('creado_por_id', ''),
                "link": pass_selected.get('link', ''),
                "qr_code": pass_selected.get('_id', '')
            },
            "nombre_pase": pass_selected.get('nombre', ''),
            "perfil_pase": pass_selected.get('tipo_de_pase', ''),
            "qr_pase": pass_selected.get('qr_pase', []),
            "status_pase": pass_selected.get('estatus', ''),
            "telefono_pase": pass_selected.get('telefono', ''),
            "tema_cita": pass_selected.get('tema_cita', ''),
            "tipo_visita": 'alta_de_nuevo_visitante',
            "tipo_visita_pase": tipo_visita_pase,
            "ubicacion": pass_selected.get('ubicacion', ''),
            "visita_a": pass_selected.get('visita_a')[0].get('nombre'),
            "walkin_fotografia": update_obj.get('foto', []),
            "walkin_identificacion": update_obj.get('identificacion', []),
            "archivo_invitacion": [],
        }

        location = access_pass.get('ubicacion', '')

        answers = {}
        perfil_pase = access_pass.get('perfil_pase', 'Visita General')
        user_data = self.lkf_api.get_user_by_id(self.user.get('user_id'))
        timezone = user_data.get('timezone','America/Monterrey')
        now_datetime =self.today_str(timezone, date_format='datetime')
        answers[self.mf['grupo_visitados']] = []
        answers[self.UBICACIONES_CAT_OBJ_ID] = {}
        answers[self.UBICACIONES_CAT_OBJ_ID][self.f['location']] = location
        answers[self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID] = {}
        answers[self.CONFIG_PERFILES_OBJ_ID] = {}
        answers[self.VISITA_AUTORIZADA_CAT_OBJ_ID] = {}

        cont = 0
        for key, value in access_pass.items():
            cont += 1
            if key == 'grupo_vehiculos':
                vehiculos = access_pass.get('grupo_vehiculos',[])
                if vehiculos:
                    list_vehiculos = []
                    for item in vehiculos:
                        tipo = item.get('tipo_vehiculo','')
                        marca = item.get('marca_vehiculo','')
                        modelo = item.get('modelo_vehiculo','')
                        estado = item.get('nombre_estado','')
                        placas = item.get('placas_vehiculo','')
                        color = item.get('color_vehiculo','')
                        list_vehiculos.append({
                            self.TIPO_DE_VEHICULO_OBJ_ID:{
                                self.mf['tipo_vehiculo']:tipo,
                                self.mf['marca_vehiculo']:marca,
                                self.mf['modelo_vehiculo']:modelo,
                            },
                            self.ESTADO_OBJ_ID:{
                                self.mf['nombre_estado']:estado,
                            },
                            self.mf['placas_vehiculo']:placas,
                            self.mf['color_vehiculo']:color,
                        })
                    answers[self.mf['grupo_vehiculos']] = list_vehiculos  
            elif key == 'grupo_equipos':
                equipos = access_pass.get('grupo_equipos',[])
                if equipos:
                    list_equipos = []
                    for item in equipos:
                        tipo = item.get('tipo_equipo','').lower().replace(' ', '_')
                        nombre = item.get('nombre_articulo','')
                        marca = item.get('marca_articulo','')
                        modelo = item.get('modelo_articulo','')
                        color = item.get('color_articulo','')
                        serie = item.get('numero_serie','')
                        list_equipos.append({
                            self.mf['tipo_equipo']:tipo,
                            self.mf['nombre_articulo']:nombre,
                            self.mf['marca_articulo']:marca,
                            self.mf['modelo_articulo']:modelo,
                            self.mf['color_articulo']:color,
                            self.mf['numero_serie']:serie,
                        })
                    answers[self.mf['grupo_equipos']] = list_equipos
            elif key == 'grupo_instrucciones_pase':
                acciones = access_pass.get('grupo_instrucciones_pase',[])
                if acciones:
                    acciones_list = []
                    for c in acciones:
                        acciones_list.append(
                            {
                                self.pase_entrada_fields['tipo_comentario']:c.get('tipo_de_comentario').lower(),
                                self.pase_entrada_fields['comentario_pase'] :c.get('comentario_pase')
                            }
                        )
                    answers.update({self.pase_entrada_fields['grupo_instrucciones_pase']:acciones_list})
            elif key == 'grupo_areas_acceso':
                acciones = access_pass.get('grupo_areas_acceso',[])
                if acciones:
                    acciones_list = []
                    for c in acciones:
                        acciones_list.append(
                            {
                                self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID : {
                                    self.pase_entrada_fields['nombre_area']:c.get('nombre_area')
                                } ,
                                self.pase_entrada_fields['commentario_area'] :c.get('commentario_area')
                            }
                        )
                    answers.update({self.pase_entrada_fields['grupo_areas_acceso']:acciones_list})
            elif key == 'autorizado_por':
                answers[self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID] = {
                    self.mf['nombre_guardia_apoyo'] : access_pass.get('autorizado_por', ''),
                }
            elif key == 'link':
                link_info=access_pass.get('link', '')
                if link_info:
                    docs=""
                    for index, d in enumerate(link_info["docs"]): 
                        if(d == "agregarIdentificacion"):
                            docs+="iden"
                        elif(d == "agregarFoto"):
                            docs+="foto"
                        if index==0 :
                            docs+="-"
                    link_pass= f"{link_info['link']}"
                answers.update({f"{self.pase_entrada_fields[key]}":link_pass}) 
            elif key == 'ubicacion':
                answers[self.pase_entrada_fields['ubicacion_cat']] = {self.mf['ubicacion']:access_pass['ubicacion']}
            elif key == 'visita_a': 
                answers[self.mf['grupo_visitados']] = []
                visita_a = access_pass.get('visita_a')
                visita_set = {
                    self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID:{
                        self.mf['nombre_empleado'] : visita_a,
                        }
                    }
                options_vistia = {
                      "group_level": 3,
                      "startkey": [location, visita_a],
                      "endkey": [location, f"{visita_a}\n",{}],
                    }
                cat_visita = self.catalogo_view(self.CONF_AREA_EMPLEADOS_CAT_ID, self.PASE_ENTRADA, options_vistia)
                if len(cat_visita) > 0:
                    cat_visita =  {key: [value,] for key, value in cat_visita[0].items() if value}
                visita_set[self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID].update(cat_visita)
                answers[self.mf['grupo_visitados']].append(visita_set)
            elif key == 'perfil_pase':
                answers[self.CONFIG_PERFILES_OBJ_ID] = {}
                answers[self.CONFIG_PERFILES_OBJ_ID] = {
                    self.mf['nombre_perfil'] : perfil_pase,
                }
                options = {
                      "group_level": 2,
                      "startkey": [perfil_pase],
                      "endkey": [f"{perfil_pase}\n",{}],
                    }
                cat_perfil = self.catalogo_view(self.CONFIG_PERFILES_ID, self.PASE_ENTRADA, options)
                if len(cat_perfil) > 0:
                    cat_perfil[0][self.mf['motivo']]= [cat_perfil[0].get(self.mf['motivo'])]
                    cat_perfil = cat_perfil[0]
                answers[self.CONFIG_PERFILES_OBJ_ID].update(cat_perfil)
                if answers[self.CONFIG_PERFILES_OBJ_ID].get(self.mf['nombre_permiso']) and \
                   type(answers[self.CONFIG_PERFILES_OBJ_ID][self.mf['nombre_permiso']]) == str:
                    answers[self.CONFIG_PERFILES_OBJ_ID][self.mf['nombre_permiso']] = [answers[self.CONFIG_PERFILES_OBJ_ID][self.mf['nombre_permiso']],]
            elif key == 'archivo_invitacion':
                # id_forma = 121736
                id_forma = self.PASE_ENTRADA
                # id_campo = '673773741b2adb2d05d99d63'
                id_campo = self.pase_entrada_fields['archivo_invitacion']
                tema_cita = access_pass.get("tema_cita")
                descripcion = access_pass.get("descripcion")
                fecha_desde_visita = access_pass.get("fecha_desde_visita")
                fecha_desde_hasta = access_pass.get("fecha_desde_hasta")
                creado_por_email = access_pass.get("link", {}).get("creado_por_email")
                ubicacion = access_pass.get("ubicacion",'')
                nombre = access_pass.get("nombre_pase",'')
                visita_a = access_pass.get("visita_a",'')
                email = access_pass.get("email_pase",'')

                start_datetime = datetime.strptime(fecha_desde_visita, "%Y-%m-%d %H:%M:%S")

                if not fecha_desde_hasta:
                    stop_datetime = start_datetime + timedelta(hours=1)
                else:
                    stop_datetime = datetime.strptime(fecha_desde_hasta, "%Y-%m-%d %H:%M:%S")

                meeting = [
                    {
                        "id": 1,
                        "start": start_datetime,
                        "stop": stop_datetime,
                        "name": tema_cita,
                        "description": descripcion,
                        "location": ubicacion,
                        "allday": False,
                        "rrule": None,
                        "alarm_ids": [{"interval": "minutes", "duration": 10, "name": "Reminder"}],
                        'organizer_name': visita_a,
                        'organizer_email': creado_por_email,
                        "attendee_ids": [{"email": email, "nombre": nombre}, {"email": creado_por_email, "nombre": visita_a}],
                    }
                ]
                respuesta_ics = self.upload_ics(id_forma, id_campo, meetings=meeting)
                file_name = respuesta_ics.get('file_name', '')
                file_url = respuesta_ics.get('file_url', '')

                archivo_invitacion= [
                    {
                        "file_name": f"{file_name}",
                        "file_url": f"{file_url}"
                    }
                ]
                answers.update({f"{self.pase_entrada_fields[key]}": archivo_invitacion})
            else:
                answers.update({f"{self.pase_entrada_fields[key]}":value})

        if answers or folio:
            metadata = self.lkf_api.get_metadata(form_id=self.PASE_ENTRADA)
            metadata.update(self.get_record_by_folio(folio, self.PASE_ENTRADA, select_columns={'_id':1}, limit=1))

            metadata.update({
                    'properties': {
                        "device_properties":{
                            "system": "Addons",
                            "process":"Actualizacion de Pase de Entrada", 
                            "accion":'update_full_pass', 
                            "folio": folio, 
                            "archive": "pase_acceso.py"
                        }
                    },
                    'answers': answers,
                    '_id': qr_code
                })
            res= self.net.patch_forms_answers(metadata)
            return res
        else:
            self.LKFException('No se mandarón parametros para actualizar')

    def update_pass_status(self):
        query_update = {}
        user_data = self.lkf_api.get_user_by_id(self.user.get('user_id'))
        timezone = user_data.get('timezone','America/Monterrey')
        today = self.today_str(tz_name=timezone, date_format="datetime")
        query_update = {
            "$and": [{
                "$or":[{
                    f"answers.{self.pase_entrada_fields['fecha_desde_visita']}":{
                        "$lte":today
                        }
                    },
                    {
                        f"answers.{self.pase_entrada_fields['fecha_desde_hasta']}":{
                            "$lte":today
                        },
                    }
                ]
                }]
            }
        records_ = self.search_pass_by_status('activo', query_update)
        records = [ObjectId(req["_id"]) for req in records_]
        update_query= {f"answers.{self.pase_entrada_fields['status_pase']}":"vencido"}
        # return self.cr.update_many({
        #         'form_id':self.PASE_ENTRADA,
        #         'deleted_at':{'$exists':False},
        #         '_id':{
        #             "$in":records
        #         }
        #     }, {"$set": update_query})
    
        res = self.cr.update_many({
                'form_id':self.PASE_ENTRADA,
                'deleted_at':{'$exists':False},
                '_id':{
                    "$in":records
                }
            }, {"$set": update_query})
        
        return res.matched_count
        # print("records=",stop)

    def update_paquete(self, data_paquete_actualizar, folio):
        answers = {}
        for key, value in data_paquete_actualizar.items():
            if  key == 'area_paqueteria':
                answers[self.consecionados_fields['area_paqueteria']] = value
            elif key == 'ubicacion_paqueteria':
                answers[self.consecionados_fields['ubicacion_paqueteria']] = value
            elif key == 'quien_recibe_paqueteria':
                answers[self.paquetes_fields['quien_recibe_catalogo']] = {self.paquetes_fields['quien_recibe_paqueteria']:value}
            else:
                answers.update({f"{self.paquetes_fields[key]}":value})
        if answers or folio:
            return self.lkf_api.patch_multi_record( answers = answers, form_id=self.PAQUETERIA, folios=[folio])
        else:
            self.LKFException('No se mandarón parametros para actualizar')

    def validate_access_pass_location(self, qr_code, location):
        #TODO
        last_move = self.get_last_user_move(qr_code, location)
        if self.user_in_facility(last_move.get('status_visita')):
            return True
        return False

    def validate_certificados(self, qr_code, location):
        # Valida los certificados del pase de acceso.
        return True

    def validate_pass_dates(self, access_pass):
        # Valida las fechas del pase de acceso
        return True

    def validate_value_id(self, qr_code):
        try:
            ObjectId(qr_code)
            return True
        except Exception as e:
            return False

    def vehiculo_tipo(self):
        return self.catalogo_vehiculos()
    
    def vehiculo_marca(self, tipo):
        options = {
            'startkey': [tipo,],
            'endkey': [f"{tipo}\n",{}],
            'group_level':2
        }
        return self.catalogo_vehiculos(options)

    def vehiculo_modelo(self, tipo, marca):
        options = {
            'startkey': [tipo,marca],
            'endkey': [f"{tipo}, {marca}\n",{}],
            'group_level':3
        }
        return self.catalogo_vehiculos(options)

    def visita_a(self, location):
        form_id = self.PASE_ENTRADA
        catalog_id = self.CONF_AREA_EMPLEADOS_CAT_ID
        options = {
            'startkey': [location],
            'endkey': [f"{location}\n",{}],
            'group_level':2
        }
        return self.catalogo_view(catalog_id, form_id, options)

    def visita_a_detail(self, location, visita_a):
        form_id = self.PASE_ENTRADA
        catalog_id = self.CONF_AREA_EMPLEADOS_CAT_ID
        options = {
            'startkey': [location, visita_a],
            'endkey': [location,f"{visita_a}\n",{}],
            'group_level':3
        }
        return self.catalogo_view(catalog_id, form_id, options, detail=True)
    

    def send_email_and_sms(self, data):
        answers = {}
        phone_to = data['phone_to']
        mensaje = data['mensaje']
        titulo = 'Aviso desde Soter - Accesos'

        metadata = self.lkf_api.get_metadata(form_id=self.ENVIO_DE_CORREOS)
        metadata.update({
            "properties": {
                "device_properties":{
                    "System": "Addons",
                    "Process": "Creación de envio de correo",
                    "Action": "send_email_and_sms",
                }
            },
        })

        #---Define Answers
        answers.update({
            f"{self.envio_correo_fields['email_from']}": data['email_from'],
            f"{self.envio_correo_fields['titulo']}": titulo,
            f"{self.envio_correo_fields['nombre']}": data['nombre'],
            f"{self.envio_correo_fields['email_to']}": data['email_to'],
            f"{self.envio_correo_fields['msj']}": mensaje,
            f"{self.envio_correo_fields['enviado_desde']}": 'Accesos Aviso',
        })

        metadata.update({'answers': answers})

        email_status = 'Correo: No se realizo la peticion.'
        email_response = self.lkf_api.post_forms_answers(metadata)
        if email_response.get('status_code') == 201:
            email_status = 'Correo: Enviado correctamente'
        else:
            email_status = 'Correo: Hubo un error...'

        message_status = 'Mensaje: No se realizo la peticion.'
        if phone_to:
            sms_response = self.lkf_api.send_sms(phone_to, mensaje, use_api_key=True)
            if hasattr(sms_response, "status") and sms_response.status in ["queued", "sent", "delivered"]:
                message_status = 'Mensaje: Enviado correctamente'
            else:
                message_status = 'Mensaje: Hubo un error...'
        
        return {
            "email_status": email_status,
            "message_status": message_status
        }

    def create_class_google_wallet(self, data, qr_code):
        ISSUER_ID = '3388000000022924601'
        CLASS_ID = f'{ISSUER_ID}.ProdPassClass'

        google_wallet_creds = self.lkf_api.get_user_google_wallet(use_api_key=True, jwt_settings_key=False)
        QR_CODE_VALUE = qr_code
        OBJECT_ID = f'{ISSUER_ID}.pase-entrada-{QR_CODE_VALUE}-{uuid.uuid4()}'

        credentials_data = google_wallet_creds.get('data', {})
        private_key = credentials_data.get('private_key')
        client_email = credentials_data.get('client_email')

        credentials = service_account.Credentials.from_service_account_info(
            credentials_data,
            scopes=['https://www.googleapis.com/auth/wallet_object.issuer']
        )

        auth_req = Request()
        credentials.refresh(auth_req)
        access_token = credentials.token

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }

        class_url = f'https://walletobjects.googleapis.com/walletobjects/v1/genericClass/{CLASS_ID}'
        class_check = requests.get(class_url, headers={'Authorization': f'Bearer {access_token}'})
        
        if class_check.status_code != 200:
            class_body = {
                "id": CLASS_ID,
            }
            response = requests.post(
                'https://walletobjects.googleapis.com/walletobjects/v1/genericClass',
                headers=headers,
                json=class_body
            )
            print("Status code:", response.status_code)
            print("Response text:", response.text)

        response = self.create_pass_google_wallet(OBJECT_ID, CLASS_ID, QR_CODE_VALUE, data, headers, client_email, private_key)
        return response

    def create_pass_google_wallet(self, object_id, class_id, qr_code, data, headers, client_email, private_key):
        nombre = data.get('nombre', '')
        ubicaciones_list = data.get('ubicacion', '')
        format_ubicacion = self.format_ubicaciones_to_google_pass(ubicaciones_list)
        address = data.get('address', '')
        visita_a = data.get('visita_a', '')
        empresa = data.get('empresa', '')
        num_accesos = data.get('all_data', {}).get('config_limitar_acceso', 1)
        fecha_desde = data.get('all_data', {}).get('fecha_desde_visita', '')
        fecha_hasta = data.get('all_data', {}).get('fecha_hasta_visita', '')
        if not fecha_hasta:
            fecha_hasta = fecha_desde

        object_body = {
            "id": object_id,
            "classId": class_id,
            "state": "ACTIVE",
            "genericType": "GENERIC_TYPE_UNSPECIFIED",
            "cardTitle": {
                "defaultValue": {
                    "language": "es-MX",
                    "value": empresa
                }
            },
            "subheader": {
                "defaultValue": {
                    "language": "es-MX",
                    "value": 'Pase de Entrada'
                }
            },
            "header": {
                "defaultValue": {
                    "language": "es-MX",
                    "value": f'Visita a: {visita_a}'
                }
            },
            "logo": {
                "sourceUri": {
                    "uri": "https://f001.backblazeb2.com/file/app-linkaform/public-client-126/68600/6076166dfd84fa7ea446b917/2025-05-12T08:19:51.png"
                }
            },
            "hexBackgroundColor": "#FFFFFF",
            "groupingInfo": {
                "sortIndex": 1,
                "groupingId": "pase_de_entrada",
            },
            "textModulesData": [
                {
                    "id": "ubicacion",
                    "header": "UBICACION",
                    "body": format_ubicacion
                },
                {
                    "id": "fecha_entrada",
                    "header": "FECHA ENTRADA",
                    "body": fecha_desde
                },
                {
                    "id": "fecha_salida",
                    "header": "FECHA SALIDA",
                    "body": fecha_hasta
                },
                {
                    "id": "accesos",
                    "header": "ACCESOS",
                    "body": num_accesos
                },
                {
                    "id": "vehiculos",
                    "header": "VEHICULOS",
                    "body": "1"
                },
                {
                    "id": "equipos",
                    "header": "EQUIPOS",
                    "body": "1"
                }
            ],
            "barcode": {
                "type": "QR_CODE",
                "value": qr_code,
                "alternateText": "Muestra tu QR para ingresar"
            },
        }

        requests.post(
            'https://walletobjects.googleapis.com/walletobjects/v1/genericObject',
            headers=headers,
            json=object_body
        )

        jwt_payload = {
            "iss": client_email,
            "aud": "google",
            "origins": [],
            "typ": "savetowallet",
            "payload": {
                "genericObjects": [
                    {"id": object_id}
                ]
            }
        }

        signed_jwt = jwt.encode(jwt_payload, private_key, algorithm='RS256')
        save_url = f'https://pay.google.com/gp/v/save/{signed_jwt}'
        print('Agrega tu pase con este link:', save_url)

        return save_url
    
    def format_ubicaciones_to_google_pass(self, ubicaciones_list):
        if not ubicaciones_list:
            return ''
        if len(ubicaciones_list) == 1:
            return self.unlist(ubicaciones_list)
        if len(ubicaciones_list) == 2:
            return f"{ubicaciones_list[0]} y {ubicaciones_list[1]}"
        return ', '.join(ubicaciones_list[:-1]) + ' y ' + ubicaciones_list[-1]

    def upload_pdf_as_image(self, id_forma_seleccionada, id_field, pdf_url, convert_all=False):
        # 1. Descargar PDF desde la URL
        try:
            response = requests.get(pdf_url)
            response.raise_for_status()
        except Exception as e:
            print("Error al descargar el PDF:", e)
            return {"error": "Fallo al descargar el PDF"}

        # 2. Convertir PDF a imágenes
        try:
            images = convert_from_bytes(response.content, dpi=150)
        except Exception as e:
            print("Error al convertir el PDF:", e)
            return {"error": "Fallo al convertir el PDF"}

        temp_dir = tempfile.gettempdir()

        if convert_all and len(images) > 1:
            # 3a. Guardar todas las imágenes en un archivo ZIP
            zip_path = os.path.join(temp_dir, "converted_images.zip")
            with ZipFile(zip_path, 'w') as zipf:
                for i, img in enumerate(images):
                    img_path = os.path.join(temp_dir, f"page_{i+1}.png")
                    img.save(img_path, "PNG")
                    zipf.write(img_path, arcname=f"page_{i+1}.png")
                    os.remove(img_path)
            file_to_upload_path = zip_path
            filename = "converted_images.zip"
        else:
            # 3b. Guardar solo la primera imagen como PNG
            img_path = os.path.join(temp_dir, "converted_image.png")
            images[0].save(img_path, "PNG")
            file_to_upload_path = img_path
            filename = "converted_image.png"

        rb_file = open(file_to_upload_path, 'rb')
        dir_file = {'File': rb_file}

        try:
            upload_data = {'form_id': id_forma_seleccionada, 'field_id': id_field}
            upload_url = self.lkf_api.post_upload_file(data=upload_data, up_file=dir_file)
            rb_file.close()
        except Exception as e:
            rb_file.close()
            os.remove(file_to_upload_path)
            print("Error al subir el archivo:", e)
            return {"error": "Fallo al subir el archivo"}

        try:
            file_url = upload_url['data']['file']
            update_file = {'file_name': filename, 'file_url': file_url}
        except KeyError:
            print('No se pudo obtener la URL del archivo')
            update_file = {"error": "Fallo al obtener la URL del archivo"}
        finally:
            os.remove(file_to_upload_path)

        return update_file