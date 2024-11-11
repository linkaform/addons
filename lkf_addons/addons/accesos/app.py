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

import simplejson, time
from bson import ObjectId
from datetime import datetime
from copy import deepcopy

from linkaform_api import base
from lkf_addons.addons.employee.app import Employee
from lkf_addons.addons.activo_fijo.app import Vehiculo
from lkf_addons.addons.location.app import Location

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
        # self.CONF_ACCESOS = self.lkm.form_id('configuracion_accesos','id')
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

        self.TIPO_ARTICULOS_PERDIDOS_CAT = self.lkm.catalog_id('tipo_de_articulos_perdidos')
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
            #LOS CATALOGOS NO SE CCLASIFICAN COMO CAMPOS            
            'catalog_area_pase':'664fc5f3bbbef12ae61b15e9',
            'catalog_caseta':'66566d60d4619218b880cf04',
            'catalog_caseta_salida':'66566d60464fe63529d1c543',
            'catalog_estado':'664fc5b3276795e17ea76dbd',
            'catalog_guard':'664fc645276795e17ea76dc4',
            'catalog_guard_close':'664fc64242c59486fadd0a27',
            'catalog_tipo_pase':'664fc6e81d1a1fcda334b587',
            'catalog_ubicacion':'664fc5d9860deae4c20954e2',
            'catalog_visita':'664fc6f5d6078682a4dd0ab3',
            'catalogo_persona_involucrada': '66ec6936fc1f0f3f111d818f',
            ##### REVISAR Y BORRAR ######

            'fecha_salida':'662c51eb194f1cb7a91e5af0',
            'fecha_entrada':'662c51eb194f1cb7a91e5aef',
            'comentario_pase':'65e0a69a322b61fbf9ed23af',
            'nombre_area':'663e5d44f5b8a7ce8211ed0f',
            'nombre_area_salida':'663fb45992f2c5afcfe97ca8',
            'color_vehiculo': '663e4691f54d395ed7f27465',
            'color_articulo': '663e4730724f688b3059eb3b',
            'config_dia_de_acceso': '662c304fad7432d296d92584',
            'config_limitar_acceso': '6635380dc9b3e7db4d59eb49',
            'config_dias_acceso': '662c304fad7432d296d92585',
            'codigo_qr':'6685da34f065523d8d09052b',
            'curp': '5ea0897550b8dfe1f4d83a9f',
            'departamento_empleado': '663bc4ed8a6b120eab4d7f1e',
            'dias_acceso_pase':'662c304fad7432d296d92585',
            'documento': '663e5470424ad55e32832eec',
            'documento_certificado': '66427511e93cc23f04f27467',
            'direccion': '663a7e0fe48382c5b1230902',
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
            'commentario_area': '66af1a77d703592958dca5eb',
            'grupo_instrucciones_pase':'65e0a68a06799422eded24aa',
            'guard_group':'663fae53fa005c70de59eb95',
            'grupo_visitados': '663d4ba61b14fab90559ebb0',
            'grupo_vehiculos': '663e446cadf967542759ebba',
            'identificacion':'65ce34985fa9df3dbf9dd2d0',
            'locker_id':'66480101786e8cdb66e70124',
            'marca_vehiculo':'65f22098d1dc5e0b9529e89b',
            'marca_articulo':'663e4730724f688b3059eb3a',
            'modelo_articulo':'66b29872aa6b3e6c3c02baa6',
            'modelo_vehiculo':'65f22098d1dc5e0b9529e89c',
            'motivo':'66ad58a3a5515ee3174f2bb5',
            'nombre_pase':'662c2937108836dec6d92580',
            'nota': '6647fadc96f80017ac388647',
            'nombre_articulo': '663e4730724f688b3059eb39',
            'nombre_estado': '663a7dd6e48382c5b12308ff',
            'nombre_empleado': '62c5ff407febce07043024dd',
            'nombre_guardia_apoyo': '663bd36eb19b7fb7d9e97ccb',
            'nombre_perfil': '661dc67e901906b7e9b73bac',
            'nombre_permiso':'662962bb203407ab90c886e4',
            'numero_serie': '66426453f076652427832fd2',
            'nombre_visita': '5ea0693a0c12d5a8e43d37df',
            'nombre_pase':'662c2937108836dec6d92580',
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
            'tipo_de_articulo_perdido':'66ce23efc5c4d148311adf86',
            'tipo_de_comentario':'66af1977ffb6fd75e769f457',
            'tipo_de_guardia': '6684484fa5fd62946c12e006',
            'tipo_equipo': '663e4730724f688b3059eb38',
            'tipo_locker': '66ccfec6acaa16b31e5593a3',
            'tipo_registro': '66358a5e50e5c61267832f90',
            'tipo_vehiculo': '65f22098d1dc5e0b9529e89a',
            'tipo_visita_pase': '662c304fad7432d296d92581',
            'ubicacion': '663e5c57f5b8a7ce8211ed0b',
            'user_id_empleado': '663bd32d7fb8869bbc4d7f7b',
            'vigencia_certificado':'662962bb203407ab90c886e6',
            'vigencia_certificado_en':'662962bb203407ab90c886e7',
            'walkin':'66c4261351cc14058b020d48'

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
            'ubicacion_concesion':f"{self.mf['catalog_ubicacion']}.{self.mf['ubicacion']}",
            'solicita_concesion':'66469e5a3e6a703350f2e03a',
            'persona_catalog_concesion':'664fc64242c59486fadd0a27',
            'persona_nombre_concesion':'663bd36eb19b7fb7d9e97ccb',
            'caseta_concesion':f"{self.mf['catalog_caseta_salida']}.{self.mf['nombre_area_salida']}",
            'fecha_concesion':'66469ef8c9d58517f85d035f',
            'equipo_catalog_concesion':'664fc678860deae4c20954e7',
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
            'falla_evidencia_solucion':'66f2dfb2c80d24e5e82332b5',
            'falla_documento_solucion':'66f2dfb2c80d24e5e82332b6',
            'falla_fecha_hora_solucion':'66fae1f1d4e5e97eb12170ef'
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
            'nombre_completo': '66ec69239938c882f8222036',
            'responsable_accion':'66ec69a914bf1142b6a024e2',
            'acciones_tomadas':'66ec69a914bf1142b6a024e3',
            'area_incidencia_ver2':f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.mf['nombre_area']}",
            'total_deposito_incidencia':'66ec6821ea3c921534b22c30',
            'datos_deposito_incidencia':'66ec6793eb386ff970218f1f',
            'tipo_deposito': '66ec67dc608b1faed7b22c45',
            'cantidad':'66ec67e42bcc75c3a458778e'
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
            'curp_catalog_pase':f"{self.PASE_ENTRADA_OBJ_ID}.{self.mf['curp']}",
            'nombre_permiso':f"{self.CONFIG_PERFILES_OBJ_ID}.662962bb203407ab90c886e4",
            'email_catalog_pase':f"{self.PASE_ENTRADA_OBJ_ID}.{self.mf['email_vista']}",
            'empresa_pase':f"{self.PASE_ENTRADA_OBJ_ID}.{self.mf['empresa']}",
            'direccion_pase':f"{self.mf['catalog_ubicacion']}.{self.mf['direccion']}",
            'foto_pase':f"{self.PASE_ENTRADA_OBJ_ID}.{self.mf['foto']}",
            'foto_pase_id':f"{self.mf['foto']}",
            'identificacion_pase':f"{self.PASE_ENTRADA_OBJ_ID}.{self.mf['identificacion']}",
            'identificacion_pase_id':f"{self.mf['identificacion']}",
            'motivo':f"{self.CONFIG_PERFILES_OBJ_ID}.{self.mf['motivo']}",
            'nombre_area':f"{self.mf['nombre_area']}",
            'nombre_catalog_pase':f"{self.PASE_ENTRADA_OBJ_ID}.{self.mf['nombre_visita']}",
            'nombre_tipo_pase':f"{self.CONFIG_PERFILES_OBJ_ID}.66297e1579900d9018c886ad",
            'nombre_perfil':f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_name']}",
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
            'fecha_hasta_pase':'662c304fad7432d296d92583',
            'grupo_instrucciones_pase':'65e0a68a06799422eded24aa',
            'nombre_pase':'662c2937108836dec6d92580',
            'qr_pase':'64ef5b5fff1bec97d2ca27b6',
            'telefono_pase':'662c2937108836dec6d92582',
            'tipo_visita':"662c262cace163ca3ed3bb3a",
            'tipo_comentario':'66af1977ffb6fd75e769f457',
            'visita_a':'663d4ba61b14fab90559ebb0',
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
        })

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
                    f"{self.pase_entrada_fields['foto_pase_id']}":[access_pass['foto'],],
                    f"{self.pase_entrada_fields['identificacion_pase_id']}":[access_pass['identificacion'],],
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

        equipos = data.get('equipo',[])

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
                       self.bitacora_fields['visita_user_id_empleado'] :[c.get('user_id')],
                       self.bitacora_fields['visita_departamento_empleado']:[c.get('departamento')],
                       self.bitacora_fields['puesto_empleado']:[c.get('puesto')],
                       self.bitacora_fields['email_empleado'] :[c.get('email')]
                   }}
                )
            print("VISIITAAAA",visit_list2)
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
        print('areas=',areas)
        ### Aquien Visita
        catalog_id = self.CONF_AREA_EMPLEADOS_CAT_ID
        visita_a = self.lkf_api.catalog_view(catalog_id, form_id, options) 
        # visita_a = [r.get('key')[group_level-1] for r in visita_a]
        print('visita_a=',visita_a)
        ### Pases de accesos
        res = {
            'Areas': areas,
            'Visita_a': visita_a,
            'Perfiles': self.get_pefiles_walkin(location),
        }
        # print('visita_a=',visita_a)
        return res

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

    def do_access(self, qr_code, location, area, data):
        '''
        Valida pase de entrada y crea registro de entrada al pase
        '''
        print('me quede ahceidno la vaildacion y el registro de entrada')

        if not qr_code and not location and not area:
            return False

        # access_pass = self.search_pass(qr_code)
        if self.validate_access_pass_location(qr_code, location):
            self.LKFException("En usuario ya se encuentra dentro de una ubicacion")
        val_certificados = self.validate_certificados(qr_code, location)
        access_pass = self.get_detail_access_pass(qr_code)
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

    def do_checkin(self, location, area, employee_list=[]):
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
        resp_create = self.lkf_api.post_forms_answers(data)
        #TODO agregar nombre del Guardia Quien hizo el checkin
        if resp_create.get('status_code') == 201:
            resp_create['json'].update({'boot_status':{'guard_on_duty':user_data['name']}})
        return resp_create

    def do_checkout(self, checkin_id=None, location=None, area=None, guards=[], forzar=False, comments=False):
        # self.get_answer(keys)
        employee =  self.get_employee_data(email=self.user.get('email'), get_one=True)
        timezone = employee.get('cat_timezone', employee.get('timezone', 'America/Monterrey'))
        now_datetime =self.today_str(timezone, date_format='datetime')
        print('location', location)
        print('area', area)
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
        response = self.lkf_api.patch_record( data=data, record_id=checkin_id)
        print('response', response)
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
        print("last_check_out=", last_check_out)
        print("gafete_id",gafete_id)
        if last_check_out.get('gafete_id') and not gafete_id:
            self.LKFException({"status_code":400, "msg":f"Se necesita liberar el gafete antes de regitrar la salida"})
        if not location:
            self.LKFException({"status_code":400, "msg":f"Se requiere especificar una ubicacion de donde se raelizara la salida."})
        if not area:
            self.LKFException({"status_code":400, "msg":f"Se requiere especificar el area de donde se realizara la salida."})
        if last_check_out.get('folio'):
            folio = last_check_out.get('folio',0)
            checkin_date_str = last_check_out.get('checkin_date')
            checkin_date = self.date_from_str(checkin_date_str)
            now = datetime.now()
            fecha_hora_str = now.strftime("%Y-%m-%d %H:%M:%S")
            duration = time.strftime('%H:%M:%S', time.gmtime( self.date_2_epoch(fecha_hora_str) - self.date_2_epoch(checkin_date_str)))
            if self.user_in_facility(status_visita=last_check_out.get('status_visita')):
                answers = {
                    f"{self.mf['tipo_registro']}":'salida',
                    f"{self.mf['fecha_salida']}":fecha_hora_str,
                    f"{self.mf['duracion']}":duration,
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

    def catalago_area_location(self, location_name):
        return self.get_areas_by_location(location_name)

    def catalogo_categoria(self, options={}):
        catalog_id = self.ESTADO_ID
        form_id = self.PASE_ENTRADA
        group_level = options.get('group_level',1)
        return self.catalogo_view(catalog_id, form_id)

    def catalogo_estados(self, options={}):
        catalog_id = self.ESTADO_ID
        form_id = self.PASE_ENTRADA
        group_level = options.get('group_level',1)
        return self.catalogo_view(catalog_id, form_id)

    def catalogo_incidencias(self):
        catalog_id = self.LISTA_INCIDENCIAS_CAT_ID
        form_id = self.BITACORA_INCIDENCIAS
        res=self.catalogo_view(catalog_id, form_id)
        return res

    def catalogo_vehiculos(self, options={}):
        catalog_id = self.TIPO_DE_VEHICULO_ID
        form_id = self.PASE_ENTRADA
        group_level = options.get('group_level',1)
        return self.catalogo_view(catalog_id, form_id, options=options)

    def catalogo_view(self, catalog_id, form_id, options={}, detail=False):
        catalog_id = catalog_id
        form_id = form_id
        group_level = options.get('group_level',1)
        res = self.lkf_api.catalog_view(catalog_id, form_id, options)
        if detail:
            if res and len(res) > 0:
                res = self._labels(res[0])
                res = {k:v[0] for k,v in res.items() if len(v)>0}
        return res

    def catalogo_config_area_empleado(self):
        catalog_id = self.CONF_AREA_EMPLEADOS_CAT_ID
        form_id= self.BITACORA_OBJETOS_PERDIDOS
        return self.lkf_api.catalog_view(catalog_id, form_id) 

    def catalogo_config_area_empleado_apoyo(self):
        catalog_id = self.CONF_AREA_EMPLEADOS_AP_CAT_ID
        form_id= self.BITACORA_FALLAS
        return self.lkf_api.catalog_view(catalog_id, form_id) 

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
            if  key == 'ubicacion_concesion':
                answers[self.mf['catalog_ubicacion']] = { self.mf['ubicacion'] : value}
            elif  key == 'nombre_concesion':
                answers[self.consecionados_fields['persona_catalog_concesion']] = { self.consecionados_fields['persona_nombre_concesion'] : value}
            elif  key == 'caseta_concesion':
                answers[self.mf['catalog_caseta_salida']] = { self.mf['nombre_area_salida']: value}
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
            if key == 'tipo_articulo_perdido':
                print("value", value)
                answers[self.perdidos_fields['tipo_articulo_catalog']] = {self.perdidos_fields['tipo_articulo_perdido']:value}
            elif key == 'articulo_seleccion':
                answers[self.perdidos_fields['articulo_seleccion_catalog']] = {self.perdidos_fields['articulo_seleccion']:value}
            elif  key == 'ubicacion_perdido' or key == 'area_perdido':
                if data_articles['ubicacion_perdido'] and not data_articles['area_perdido']:
                    answers[self.perdidos_fields['ubicacion_catalog']] = {self.perdidos_fields['ubicacion_perdido']:data_articles['ubicacion_perdido']}
                elif data_articles['area_perdido'] and not data_articles['ubicacion_perdido']:
                    answers[self.perdidos_fields['ubicacion_catalog']] = {self.perdidos_fields['area_perdido']:data_articles['area_perdido']}
                elif data_articles['area_perdido'] and data_articles['ubicacion_perdido']: 
                    answers[self.perdidos_fields['ubicacion_catalog']] = {self.perdidos_fields['ubicacion_perdido']:data_articles['ubicacion_perdido'],
                    self.perdidos_fields['area_perdido']:data_articles['area_perdido']}
            # elif key == 'ubicacion_perdido':
            #     answers[self.perdidos_fields['ubicacion_catalog']] = {self.perdidos_fields['ubicacion_perdido']:value}
            # elif key == 'area_perdido':
            #     answers[self.perdidos_fields['area_catalog']] = {self.perdidos_fields['area_perdido']:value}
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
        print('answers', simplejson.dumps(metadata, indent=4))
        return self.lkf_api.post_forms_answers(metadata)
    
    def create_enviar_msj(self, data_msj, data_cel_msj=None):
        data_msj['enviado_desde'] = 'Modulo de Accesos'
        return self.send_email_by_form(data_msj)

    def create_enviar_msj_pase(self, data_msj, data_cel_msj=None, folio=None):
        # access_pass={status_pase:"Activo"}
        # resUp= update_pass(self, access_pass, None)
        data_msj['enviado_desde'] = 'Modulo de Accesos'
        # pass_selected= self.get_detail_access_pass(qr_code=folio)

        # print("PASE", pass_selected)

        # empresa=pass_selected.get("empresa","Linkaform")
        # visita= pass_selected.get('visita_a', "")
        # fecha_expedicion=pass_selected.get("fecha_de_expedicion")
        # data_msj['msj']= f"Hola, un nuevo pase de entrada se ha creado para ti, has sido invitado por {visita}./n Ubicacion: {empresa}./n Fecha y hora: {fecha_expedicion}. Saludos."
        resEm= self.send_email_by_form(data_msj)
        # resUp.get('status_code') == 201

        return resEm
     

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
                self.fallas_fields['falla_objeto_afectado']:data_failures['falla_objeto_afectado']}
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
        #---Define Answers
        answers = {}
        for key, value in data_incidences.items():
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
                                self.incidence_fields['tipo_persona'] :c.get('tipo_persona')
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
                                self.incidence_fields['responsable_accion']:c.get('responsable_accion'),
                                self.incidence_fields['acciones_tomadas'] :c.get('acciones_tomadas')
                            }
                        )
                    answers.update({self.incidence_fields['acciones_tomadas_incidencia']:acciones_list})
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
            elif key == 'prioridad_incidencia':
                answers[self.incidence_fields['prioridad_incidencia']] = f"{value}".lower()
            else:
                answers.update({f"{self.incidence_fields[key]}":value})
        print('answers', simplejson.dumps(answers, indent=4))
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
        user_data = self.lkf_api.get_user_by_id(self.user.get('user_id'))
        timezone = user_data.get('timezone','America/Monterrey')
        now_datetime =self.today_str(timezone, date_format='datetime')

        answers[self.UBICACIONES_CAT_OBJ_ID] = {}
        answers[self.UBICACIONES_CAT_OBJ_ID][self.f['location']] = location
        if access_pass.get('custom') == True :
            answers[self.pase_entrada_fields['tipo_visita_pase']] = access_pass.get('tipo_visita_pase',"")
            answers[self.pase_entrada_fields['fecha_desde_visita']] = access_pass.get('fecha_desde_visita',"")
            answers[self.pase_entrada_fields['fecha_desde_hasta']] = access_pass.get('fecha_desde_hasta',"")
            answers[self.pase_entrada_fields['config_dia_de_acceso']] = access_pass.get('config_dia_de_acceso',"")
            answers[self.pase_entrada_fields['config_dias_acceso']] = access_pass.get('config_dias_acceso',"")
            answers[self.pase_entrada_fields['catalago_autorizado_por']] =  {self.pase_entrada_fields['autorizado_por']:access_pass.get('visita_a',"")}
            answers[self.pase_entrada_fields['status_pase']] = access_pass.get('status_pase',"").lower()

        else:
            answers[self.mf['fecha_desde_visita']] = now_datetime
            answers[self.mf['tipo_visita_pase']] = 'fecha_fija'
        answers[self.pase_entrada_fields['tipo_visita']] = 'alta_de_nuevo_visitante'
        answers[self.pase_entrada_fields['walkin_nombre']] = access_pass.get('nombre')
        answers[self.pase_entrada_fields['walkin_email']] = access_pass.get('email')
        answers[self.pase_entrada_fields['walkin_empresa']] = access_pass.get('empresa')
        answers[self.pase_entrada_fields['walkin_fotografia']] = access_pass.get('foto')
        answers[self.pase_entrada_fields['walkin_identificacion']] = access_pass.get('identificacion')
        answers[self.pase_entrada_fields['walkin_telefono']] = access_pass.get('telefono')
        
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
                            self.pase_entrada_fields['area'] :{self.pase_entrada_fields['nombre_area']: c.get('nombre_area')}
                        }
                    )
                answers.update({self.pase_entrada_fields['grupo_areas_acceso']:areas_list})
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
        print('perfil_pase', cat_perfil)
        if len(cat_perfil) > 0:
            cat_perfil = cat_perfil[0]
        answers[self.CONFIG_PERFILES_OBJ_ID].update(cat_perfil)
        if answers[self.CONFIG_PERFILES_OBJ_ID].get(self.mf['nombre_permiso']) and \
           type(answers[self.CONFIG_PERFILES_OBJ_ID][self.mf['nombre_permiso']]) == str:
            answers[self.CONFIG_PERFILES_OBJ_ID][self.mf['nombre_permiso']] = [answers[self.CONFIG_PERFILES_OBJ_ID][self.mf['nombre_permiso']],]


        # elif key == 'grupo_vehiculos':
        #         list_vehiculos = []
        #         for item in value:
        #             tipo = item.get('tipo','')
        #             marca = item.get('marca','')
        #             modelo = item.get('modelo','')
        #             estado = item.get('estado','')
        #             placas = item.get('placas','')
        #             color = item.get('color','')
        #             list_vehiculos.append({
        #                 self.TIPO_DE_VEHICULO_OBJ_ID:{
        #                     self.mf['tipo_vehiculo']:tipo,
        #                     self.mf['marca_vehiculo']:marca,
        #                     self.mf['modelo_vehiculo']:modelo,
        #                 },
        #                 self.ESTADO_OBJ_ID:{
        #                     self.mf['nombre_estado']:estado,
        #                 },
        #                 self.mf['placas_vehiculo']:placas,
        #                 self.mf['color_vehiculo']:color,
        #             })
        #         answers[self.mf['grupo_vehiculos']] = list_vehiculos  
        #     elif key == 'grupo_equipos':
        #         list_equipos = []
        #         for item in value:
        #             nombre = item.get('nombre','')
        #             marca = item.get('marca','')
        #             color = item.get('color','')
        #             tipo = item.get('tipo','')
        #             serie = item.get('serie','')
        #             list_equipos.append({
        #                 self.mf['tipo_equipo']:tipo,
        #                 self.mf['nombre_articulo']:nombre,
        #                 self.mf['marca_articulo']:marca,
        #                 self.mf['numero_serie']:serie,
        #                 self.mf['color_articulo']:color,
        #             })
        #         answers[self.mf['grupo_equipos']] = list_equipos  
        #---Valor

        metadata.update({'answers':answers})
        print('answers', simplejson.dumps(metadata, indent=4))
        res = self.lkf_api.post_forms_answers(metadata)
        return res

    def format_personas_involucradas(self, data):
        res = []
        for r in data:
            row = {}
            row['nombre_completo'] = r.get(self.incidence_fields['nombre_completo'],'')
            row['tipo_persona'] = r.get(self.incidence_fields['tipo_persona'],'')
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
            row['responsable_accion'] = r.get(self.incidence_fields['responsable_accion'],'')
            row['acciones_tomadas'] = r.get(self.incidence_fields['acciones_tomadas'],'')
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
            row['tipo_equipo'] = r.get(self.mf['tipo_equipo'],'').title()
            row['color_articulo'] = r.get(self.mf['color_articulo'],'').title()
            res.append(row)
        return res

    def format_gafete(self, data):
        print("data=",data)
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
            print("DATAAAA", v.get(self.TIPO_DE_VEHICULO_OBJ_ID,{}).get(self.mf['tipo_vehiculo'],''))
            row['color'] = v.get(self.mf['color_vehiculo'],'').title()
            row['placas'] = v.get(self.mf['placas_vehiculo'],'')
            row['tipo'] = v.get('tipo_vehiculo','')
            row['marca_vehiculo'] = v.get(self.mf['marca_vehiculo'],'')
            row['modelo_vehiculo'] = v.get(self.mf['modelo_vehiculo'],'')
            row['nombre_estado'] = v.get('state','')
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
            print('puwsto', puesto)
            print('kwargs', kwargs)
            if kwargs.get('position') and kwargs['position'] != puesto:
                print('continue')
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

    def get_certificacion(self, certificacion, id_user, empresa=None):
        print("CERTII",certificacion ,id_user,empresa)
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

    def get_detail_access_pass(self, qr_code):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.PASE_ENTRADA,
            "_id":ObjectId(qr_code),
        }
        # print('match_query',match_query)
        query = [
            {'$match': match_query },
            {'$project': 
                {'_id':1,
                'folio': f"$folio",
                'ubicacion': f"$answers.{self.UBICACIONES_CAT_OBJ_ID}.{self.f['location']}",
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
                    f"$answers.{self.mf['grupo_visitados']}.{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.mf['email_empleado']}",
                'grupo_areas_acceso': f"$answers.{self.mf['grupo_areas_acceso']}",
                # 'grupo_commentario_area': f"$answers.{self.mf['grupo_commentario_area']}",
                'grupo_equipos': f"$answers.{self.mf['grupo_equipos']}",
                'grupo_vehiculos': f"$answers.{self.mf['grupo_vehiculos']}",
                'grupo_instrucciones_pase': f"$answers.{self.mf['grupo_instrucciones_pase']}",
                'comentario': f"$answers.{self.mf['grupo_instrucciones_pase']}",
                'codigo_qr': f"$answers.{self.mf['codigo_qr']}",
                'qr_pase': f"$answers.{self.mf['qr_pase']}"
                },
            },
            {'$sort':{'folio':-1}},
        ]
        print('query', query)
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
            print("ESTATUSSS", x.get('estatus',''))
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
                visita_a.append(emp)
            x['visita_a'] = visita_a
            perfil_pase = x.pop('perfil_pase') if x.get('perfil_pase') else []
            perfil_pase = self._labels(perfil_pase, self.mf)
            if perfil_pase:
                x['tipo_de_pase'] = perfil_pase.pop('nombre_perfil')
                empresa = x.get('empresa')
                x['certificaciones'] = self.format_perfil_pase(perfil_pase, x['curp'], empresa)
            x['grupo_areas_acceso'] = self._labels_list(x.pop('grupo_areas_acceso',[]), self.mf)
            x['grupo_instrucciones_pase'] = self._labels_list(x.pop('grupo_instrucciones_pase',[]), self.mf)
            x['grupo_equipos'] = self._labels_list(x.pop('grupo_equipos',[]), self.mf)
            x['grupo_vehiculos'] = self._labels_list(x.pop('grupo_vehiculos',[]), self.mf)
        if not x:
            self.LKFException({'msg':'Pase de Entrda no econtrado'})
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
        # print('checkin query=', simplejson.dumps(query, indent=4))
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
                'locker_id': f"$answers.{self.LOCKERS_CAT_OBJ_ID}.{self.mf['locker_id']}",
                }
            ).sort('updated_at', -1).limit(1)
        return self.format_cr(res, get_one=True)
        # return self.format_cr_result(self.cr.aggregate(query), get_one=True)

    def get_list_article_lost(self, location, area, status=None):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.BITACORA_OBJETOS_PERDIDOS,
            # f"answers.{self.perdidos_fields['ubicacion_perdido']}":location,
            # f"answers.{self.perdidos_fields['area_perdido']}":area,
        }
        if location:
             match_query[f"answers.{self.AREAS_DE_LAS_UBICACIONES_SALIDA_OBJ_ID}.{self.perdidos_fields['ubicacion_perdido']}"] = location
        if area:
             match_query[f"answers.{self.AREAS_DE_LAS_UBICACIONES_SALIDA_OBJ_ID}.{self.perdidos_fields['area_perdido']}"] = area
        if status:
             match_query[f"answers.{self.perdidos_fields['estatus_perdido']}"] = status
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
        pr= self.format_cr_result(self.cr.aggregate(query))
        print('answers', simplejson.dumps(pr, indent=4))
        return self.format_cr_result(self.cr.aggregate(query))

    def get_list_article_concessioned(self, location):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.CONCESSIONED_ARTICULOS,
            # f"answers.{self.consecionados_fields['ubicacion_concesion']}":location,
        }
        query = [
            {'$match': match_query },
            {'$project': {
                "folio": "$folio",
                "status_concesion": f"$answers.{self.consecionados_fields['status_concesion']}",
                "ubicacion_concesion": f"$answers.{self.consecionados_fields['ubicacion_concesion']}",
                "solicita_concesion": f"$answers.{self.consecionados_fields['solicita_concesion']}",
                "nombre_concesion": f"$answers.{self.consecionados_fields['persona_catalog_concesion']}.{self.consecionados_fields['persona_nombre_concesion']}",
                "caseta_concesion": f"$answers.{self.consecionados_fields['caseta_concesion']}",
                "fecha_concesion": f"$answers.{self.consecionados_fields['fecha_concesion']}",
                "area_concesion": f"$answers.{self.consecionados_fields['equipo_catalog_concesion']}.{self.consecionados_fields['area_concesion']}",
                "equipo_concesion": f"$answers.{self.consecionados_fields['equipo_catalog_concesion']}.{self.consecionados_fields['equipo_concesion']}",
                "imagen_concesion": f"$answers.{self.consecionados_fields['equipo_catalog_concesion']}.{self.consecionados_fields['equipo_imagen_concesion']}",
                "observacion_concesion": f"$answers.{self.consecionados_fields['observacion_concesion']}",
                "fecha_devolucion_concesion": f"$answers.{self.consecionados_fields['fecha_devolucion_concesion']}",
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
        print('mango_query', simplejson.dumps(mango_query, indent=4))
        print('GAFETES_CAT_ID',self.GAFETES_CAT_ID)
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
        print('mango query', simplejson.dumps(mango_query))
        return self.format_lockers(self.lkf_api.search_catalog( self.LOCKERS_CAT_ID, mango_query))

    def get_list_bitacora(self, location=None, area=None, prioridades=[]):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.BITACORA_ACCESOS
        }
        if location:
            match_query.update({f"answers.{self.bitacora_fields['ubicacion']}":location})
        if area:
            match_query.update({f"answers.{self.bitacora_fields['caseta_entrada']}":area})
        if prioridades:
            match_query[f"answers.{self.bitacora_fields['status_visita']}"] = {"$in": prioridades}


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
            'foto': {"$first":f"$answers.{self.PASE_ENTRADA_OBJ_ID}.{self.mf['foto']}"},
            'equipos':f"$answers.{self.mf['grupo_equipos']}",
            'grupo_areas_acceso': f"$answers.{self.mf['grupo_areas_acceso']}",
            'id_gafet': f"$answers.{self.GAFETES_CAT_OBJ_ID}.{self.gafetes_fields['gafete_id']}",
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
            {'$sort':{'folio':-1}},
        ]
        records = self.format_cr(self.cr.aggregate(query))
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
            r['documento'] = r.get('documento','').title().replace('_', ' ')
            r['grupo_areas_acceso'] = self._labels_list(r.pop('grupo_areas_acceso',[]), self.mf)
            r['comentarios'] = self.format_comentarios(r.get('comentarios',[]))
            r['vehiculos'] = self.format_vehiculos(r.get('vehiculos',[]))
            r['equipos'] = self.format_equipos(r.get('equipos',[]))
            r['visita_a'] = self.format_visita(r.get('visita_a',[]))
        return  records

    def get_list_fallas(self, location=None, area=None,status=None):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.BITACORA_FALLAS,
        }
        if location:
            match_query[f"answers.{self.fallas_fields['falla_ubicacion_catalog']}.{self.fallas_fields['falla_ubicacion']}"] = location
        if area:
            match_query[f"answers.{self.fallas_fields['falla_ubicacion_catalog']}.{self.fallas_fields['falla_caseta']}"] = area
        if status:
            match_query[f"answers.{self.fallas_fields['falla_estatus']}"] = status

        print("match_query", status)
        ERRO
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
                'falla_objeto_afectado':f"$answers.{self.fallas_fields['falla_catalog']}.{self.fallas_fields['falla_objeto_afectado']}",
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
            }},
            {'$sort':{'folio':-1}},
        ]
        print('answers', simplejson.dumps(query, indent=4))
        return self.format_cr_result(self.cr.aggregate(query))

    def get_list_incidences(self, location, area, prioridades=[]):
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


        print('location',match_query)
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
                'personas_involucradas_incidencia':f"$answers.{self.incidence_fields['personas_involucradas_incidencia']}",
                'acciones_tomadas_incidencia':f"$answers.{self.incidence_fields['acciones_tomadas_incidencia']}",
                'evidencia_incidencia':f"$answers.{self.incidence_fields['evidencia_incidencia']}",
                'documento_incidencia':f"$answers.{self.incidence_fields['documento_incidencia']}",
                'prioridad_incidencia':f"$answers.{self.incidence_fields['prioridad_incidencia']}",
                'notificacion_incidencia':f"$answers.{self.incidence_fields['notificacion_incidencia']}",
                'total_deposito_incidencia':f"$answers.{self.incidence_fields['total_deposito_incidencia']}",
                'datos_deposito_incidencia':f"$answers.{self.incidence_fields['datos_deposito_incidencia']}",
            }},
            {'$sort':{'folio':-1}},
        ]
        result = self.format_cr_result(self.cr.aggregate(query))
        result = self.format_cr(result)
        for r in result:
            r['personas_involucradas_incidencia'] = self.format_personas_involucradas(r.get('personas_involucradas_incidencia',[]))
            r['acciones_tomadas_incidencia'] = self.format_acciones(r.get('acciones_tomadas_incidencia',[]))
            r['datos_deposito_incidencia'] = self.format_datos_deposito(r.get('datos_deposito_incidencia',[]))
            r['prioridad_incidencia'] = r.get('prioridad_incidencia',[]).title()
        
        print('result', simplejson.dumps(result, indent=4))
        return result

    def get_list_notes(self, location, area, status=None):
        '''
        Función para crear nota, psandole los datos de area para filtrar las notas de la caseta

        '''
        response = []
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.ACCESOS_NOTAS,
            # f"answers.{self.notes_fields['note_catalog_booth']}.{self.notes_fields['note_booth']}":area,
            f"answers.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['location']}":location,
            f"answers.{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['area']}":area
        }
        if status:
            match_query.update({f"answers.{self.notes_fields['note_status']}":status})
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
        # print('answers', simplejson.dumps(query, indent=4))
        return self.format_cr(self.cr.aggregate(query))

    def get_lista_pase(self, location, status='activo', inActive="true"):
        status_value = self.pase_entrada_fields.get('status_pase', '')
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.PASE_ENTRADA,
            f"answers.{self.UBICACIONES_CAT_OBJ_ID}.{self.f['location']}":location,
        }

        if inActive =="true":
              match_query[f"answers.{self.pase_entrada_fields['status_pase']}"] =  {"$ne": "activo"}
        else:
             match_query[f"answers.{self.pase_entrada_fields['status_pase']}"] = status

        proyect_fields = {'_id':1,
            'folio': f"$folio",
            'ubicacion': f"$answers.{self.UBICACIONES_CAT_OBJ_ID}.{self.f['location']}",
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
            {'$project': proyect_fields},
            {'$sort':{'folio':-1}},
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

        print("MATCH QUERY",res)
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
            #         print('c=',c)
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
                print("result2", result2)
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
        
    def get_user_booths_availability(self):
        '''
        Regresa las castas configurados por usuario y su stats
        TODO, se puede mejorar la parte de la obtencion de la direccion para hacerlo en 1 sola peticion
        '''
        default_booth , user_booths = self.get_user_booth(search_default=False)
        user_booths.insert(0, default_booth)
        for booth in user_booths:
            booth_area = booth.get('area')
            location = booth.get('location')
            booth_status = self.get_booth_status(booth_area, location)
            booth['status'] = booth_status.get('status', 'Disponible')
            booth_address = self.get_area_address(location, booth_area)
            booth_address.pop('_id')
            booth_address.pop('folio')
            booth.update(booth_address)
        return user_booths

    def get_shift_data(self, booth_location=None, booth_area=None, search_default=True):
        """
        Obtiene informacion del turno del usuario logeado
        """
        load_shift_json = { }
        username = self.user.get('username')
        user_id = self.user.get('user_id')
        user_status = self.get_employee_checkin_status(user_id, as_shift=True,  available=False)
        this_user = user_status.get(user_id)
        if not this_user:
            this_user =  self.get_employee_data(email=self.user.get('email'), get_one=True)
            this_user['name'] = this_user.get('worker_name','')
        user_booths = []
        guards_positions = self.config_get_guards_positions()
        if not guards_positions:
            self.LKFException({"status_code":400, "msg":'No Existen puestos de guardias configurados.'})
        if this_user and this_user.get('status') == 'in':
            location_employees = {self.chife_guard:{},self.support_guard:[]}
            booth_area = this_user['area']
            booth_location = this_user['location']
            print('user_status', user_status)
            for u_id, each_user in user_status.items():
                print('uid', u_id)
                print('each_user', each_user)
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
                booth_area = default_booth['area']
            if not booth_location:
                booth_location = default_booth['location']
            if not default_booth:
                return self.LKFException({"status_code":400, "msg":'No booth found or configure for user'})
            location_employees = self.get_booths_guards(booth_location, booth_area, solo_disponibles=True)
            guard = self.get_user_guards(location_employees.get(self.chife_guard,[]))
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
        load_shift_json["booth_stats"] = self.get_booth_stats( booth_area, booth_location)
        load_shift_json["booth_status"] = self.get_booth_status(booth_area, booth_location)
        load_shift_json["support_guards"] = location_employees[self.support_guard]
        load_shift_json["guard"] = self.update_guard_status(guard, this_user)
        load_shift_json["notes"] = notes
        load_shift_json["user_booths"] = user_booths
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

    def get_user_guards(self, location_employees):
        print('location_employees', location_employees)
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
        print('answers', simplejson.dumps(query, indent=4))
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
        print('status_visita=',status_visita)
        if not status_visita:
            return False
        elif status_visita in ('entrada'):
            print('true..')
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
                access_pass['grupo_vehiculos'] = access_pass.get('grupo_vehiculos',[])
                access_pass['grupo_equipos'] = access_pass.get('grupo_equipos',[])
            else:
                gafete_info['gafete_id'] = last_move.get('gafete_id')
                gafete_info['locker_id'] = last_move.get('locker_id')
                access_pass['grupo_vehiculos'] = self.format_vehiculos_last_move(last_move.get('vehiculos',[]))
                access_pass['grupo_equipos'] = last_move.get('equipos',[])
                tipo_movimiento = 'Salida'
            #---Last Access
            access_pass['ultimo_acceso'] = last_moves
            access_pass['tipo_movimiento'] = tipo_movimiento
            access_pass['gafete_id'] = gafete_info.get('gafete_id')
            access_pass['locker_id'] = gafete_info.get("locker_id")
            access_pass['status_pase']= self.unlist(access_pass.get('estatus',"")).title() or "" 
            access_pass['limitado_a_dias']= access_pass.get('limitado_a_dias','')
            access_pass['limitado_a_acceso']= access_pass.get('limite_de_acceso','')
            access_pass['config_dia_de_acceso']=access_pass.get('config_dia_de_acceso',"").replace("_", " ")
            if access_pass.get('grupo_areas_acceso'):
                for area in access_pass['grupo_areas_acceso']:
                    area['status'] = self.get_area_status(access_pass['ubicacion'], area['nombre_area'])
            return access_pass
        else:
            return self.LKFException({"status_code":400, "msg":'El parametro para QR, no es valido'})

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
                    employee_ids.append(int(y['user_id']))
            else:
                print('x=',x)
                if x:
                    employee_ids.append(int(x['user_id']))
        pics = self.get_employee_pic(employee_ids)
        for a, x in employees.items():
            if type(x) == list:
                for y in x:
                    u_id = int(y['user_id'])
                    if pics.get(u_id):
                        y['picture'] = pics[u_id]
            else:
                if x:
                    u_id = int(x['user_id'])
                    if pics.get(u_id):
                        x['picture'] = pics[u_id]
                    employee_ids.append(int(x['user_id']))
        return employees

    def update_article_concessioned(self, data_articles, folio):
        answers = {}
        for key, value in data_articles.items():
            if  key == 'ubicacion_concesion':
                answers[self.mf['catalog_ubicacion']] = { self.mf['ubicacion'] : value}
            elif  key == 'nombre_concesion':
                answers[self.consecionados_fields['persona_catalog_concesion']] = { self.consecionados_fields['persona_nombre_concesion'] : value}
            elif  key == 'caseta_concesion':
                answers[self.mf['catalog_caseta_salida']] = { self.mf['nombre_area_salida']: value}
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
            if key == 'tipo_articulo_perdido':
                answers[self.perdidos_fields['tipo_articulo_catalog']] = {self.perdidos_fields['tipo_articulo_perdido']:value}
            elif key == 'articulo_seleccion':
                answers[self.perdidos_fields['articulo_seleccion_catalog']] = {self.perdidos_fields['articulo_seleccion']:value}
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
                print('answers', simplejson.dumps(res, indent=4))
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
                self.fallas_fields['falla_objeto_afectado']:data_failures['falla_objeto_afectado']}
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

    def update_incidence(self, data_incidences, folio):
        '''
            Realiza una actualización sobre cualquier nota, actualizando imagenes, status etc
        '''
        answers = {}
        for key, value in data_incidences.items():
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
                                self.incidence_fields['tipo_persona'] :c.get('tipo_persona')
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
                                self.incidence_fields['responsable_accion']:c.get('responsable_accion'),
                                self.incidence_fields['acciones_tomadas'] :c.get('acciones_tomadas')
                            }
                        )
                    answers.update({self.incidence_fields['acciones_tomadas_incidencia']:acciones_list})
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
            # return self.lkf_api.patch_multi_record( answers = answers, form_id=self.BITACORA_INCIDENCIAS, folios=[folio,])
        else:
            self.LKFException('No se mandarón parametros para actualizar')

    def update_gafet_status(self, answers={}):
        if not answers:
            answers = self.answers
        status = None
        tipo_movimiento=None
        tipo_movimiento = answers.get(self.mf['tipo_registro'])
        res = {}
        if tipo_movimiento == "entrada":
            status = "En Uso"
        elif tipo_movimiento == 'salida':
            status = "Disponible"
        if status :
            gafete_id = answers[self.GAFETES_CAT_OBJ_ID][self.gafetes_fields['gafete_id']]
            locker_id = answers[self.LOCKERS_CAT_OBJ_ID][self.mf['locker_id']]
            location = answers[self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID][self.f['location']]
            area = answers[self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID][self.f['area']]
            gafete = self.get_gafetes(status=None, location=location, area=area, gafete_id=gafete_id)
            if len(gafete) > 0 :
                gafete = gafete[0]
                res = self.lkf_api.update_catalog_multi_record({self.mf['status_gafete']: status}, self.GAFETES_CAT_ID, record_id=[gafete['_id']])
            print('locker_id',locker_id)
            print('tipo_movimiento',tipo_movimiento)
            self.update_locker_status(tipo_movimiento, location, area, tipo_locker='Identificaciones', locker_id=locker_id)
        return res

    def update_guard_status(self, guard, this_user):
        # last_checkin = self.get_user_last_checkin(guard['user_id'])
        status_turn = 'Turno Cerrado'
        print('this_user', this_user)
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
            print('validate_status',validate_status)
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

        print('locker_id',locker_id)
        locker = self.get_lockers(status=None, location=location, area=area, tipo_locker=tipo_locker, locker_id=locker_id)
        print('locker',locker)
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
            print('answers', simplejson.dumps(answers, indent=4))
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
            tipo = equipos.get('tipo_equipo','').lower().replace(' ', '_')
            nombre = equipos.get('nombre_articulo','')
            marca = equipos.get('marca_articulo','')
            modelo = equipos.get('modelo_articulo','')
            color = equipos.get('color_articulo','')
            serie = equipos.get('numero_serie','')
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
            tipo = vehiculos.get('tipo_vehiculo', vehiculos.get('tipo',''))
            marca = vehiculos.get('marca_vehiculo','')
            modelo = vehiculos.get('modelo_vehiculo','')
            estado = vehiculos.get('nombre_estado','')
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
        
    def update_pass(self, access_pass,folio=None):
        pass_selected= self.get_detail_access_pass(qr_code=folio)
        qr_code= folio
        _folio= pass_selected.get("folio")
        answers={}
        for key, value in access_pass.items():
            if key == 'grupo_vehiculos':
                list_vehiculos ={}
                index=1
                print("ENUM", enumerate(access_pass.get('grupo_vehiculos',[])))
                    # index+=1
                for index, item in enumerate(access_pass.get('grupo_vehiculos',[])):
                    print("INDEX", index)
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
                    list_vehiculos[f"-{index}"] = obj
                answers[self.mf['grupo_vehiculos']] = list_vehiculos  
            elif key == 'grupo_equipos':
                list_equipos = {}
                index=1
                    # index+=1
                for index, item in enumerate(access_pass.get('grupo_equipos',[])):
                    nombre = item.get('nombre','')
                    marca = item.get('marca','')
                    color = item.get('color','')
                    tipo = item.get('tipo','')
                    serie = item.get('serie','')
                    obj={
                        self.mf['tipo_equipo']:tipo.lower(),
                        self.mf['nombre_articulo']:nombre,
                        self.mf['marca_articulo']:marca,
                        self.mf['numero_serie']:serie,
                        self.mf['color_articulo']:color,
                    }
                    list_equipos[f"-{index}"] = obj
                answers[self.mf['grupo_equipos']] = list_equipos
            else:
                answers.update({f"{self.pase_entrada_fields[key]}":value})
        employee = self.get_employee_data(email=self.user.get('email'), get_one=True)
        if answers:
            res= self.lkf_api.patch_multi_record( answers = answers, form_id=self.PASE_ENTRADA, record_id=[qr_code])
            if res.get('status_code') == 201 or res.get('status_code') == 202 and folio:
                pdf = self.lkf_api.get_pdf_record(qr_code, template_id = 447, name_pdf='Pase de Entrada', send_url=True)
                print("PASE DE ENTRADA", pass_selected)
                res['json'].update({'qr_pase':pass_selected.get("qr_pase")})
                res['json'].update({'telefono':pass_selected.get("telefono")})
                res['json'].update({'enviar_a':pass_selected.get("nombre")})
                res['json'].update({'enviar_de':employee.get('worker_name')})
                res['json'].update({'pdf': pdf})
                return res
            else: 
                return res
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