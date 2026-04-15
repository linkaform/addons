# -*- coding: utf-8 -*-
### Linkaform Modules / Archivo de Módulo ###
'''
Este archivo define el modelo de datos del módulo Accesos.
Contiene los IDs de formularios, catálogos y campos (fields) usados por la clase Accesos.

Separado de app.py para mantener la configuración de datos desacoplada de la lógica de negocio.
'''

from lkf_addons.addons.base.app import Base
from lkf_addons.addons.employee.app import Employee
from lkf_addons.addons.activo_fijo.app import Vehiculo
from lkf_addons.addons.location.app import Location


### Modelo de Módulo ###
'''
AccesosModel agrupa la inicialización de IDs de formularios, catálogos y fields.
La clase Accesos en app.py hereda de esta clase para tener acceso a todas las variables
sin mezclarlas con la lógica de negocio.
'''

class AccesosModel(Employee, Location, Vehiculo, Base):

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
        self.CONFIGURACION_AREA_FORM = self.lkm.form_id('configuracion_de_area','id')
        self.CONFIGURACION_RECORRIDOS_FORM = self.lkm.form_id('configuracion_de_recorridos','id')
        self.CONF_PERFILES = self.lkm.form_id('configuracion_de_perfiles','id')
        self.PASE_ENTRADA = self.lkm.form_id('pase_de_entrada','id')
        self.PROGRAMAR_TAREAS = self.lkm.form_id('programar_tareas', 'id')
        self.PUESTOS_GUARDIAS = self.lkm.form_id('puestos_de_guardias','id')
        self.VISITA_AUTORIZADA = self.lkm.form_id('visita_autorizada','id')
        self.CONF_ACCESOS = self.lkm.form_id('configuracion_accesos','id')
        self.CONF_MODULO_SEGURIDAD = self.lkm.form_id('configuracion_modulo_seguridad','id')
        self.PAQUETERIA = self.lkm.form_id('paqueteria','id')
        self.BITACORA_RONDINES = self.lkm.form_id('bitacora_rondines','id')
        self.CHECK_UBICACIONES = self.lkm.form_id('check_ubicaciones','id')
        self.REGISTRO_ASISTENCIA = self.lkm.form_id('registro_de_asistencia','id')
        self.FORMATO_VACACIONES = self.lkm.form_id('formato_vacaciones_aviso','id')

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

        self.ACTIVOS_FIJOS_CAT = self.lkm.catalog_id('activos_fijos')
        self.ACTIVOS_FIJOS_CAT_ID = self.ACTIVOS_FIJOS_CAT.get('id')
        self.ACTIVOS_FIJOS_CAT_OBJ_ID = self.ACTIVOS_FIJOS_CAT.get('obj_id')

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

        self.CATEGORIAS_INCIDENCIAS = self.lkm.catalog_id('categora_incidentes')
        self.CATEGORIAS_INCIDENCIAS_ID = self.CATEGORIAS_INCIDENCIAS.get('id')
        self.CATEGORIAS_INCIDENCIAS_OBJ_ID = self.CATEGORIAS_INCIDENCIAS.get('obj_id')

        self.SUB_CATEGORIAS_INCIDENCIAS = self.lkm.catalog_id('subcategoras_incidentes')
        self.SUB_CATEGORIAS_INCIDENCIAS_ID = self.SUB_CATEGORIAS_INCIDENCIAS.get('id')
        self.SUB_CATEGORIAS_INCIDENCIAS_OBJ_ID = self.SUB_CATEGORIAS_INCIDENCIAS.get('obj_id')

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

        self.AREAS_DE_LAS_UBICACIONES_CAT = self.lkm.catalog_id('areas_de_las_ubicaciones')
        self.AREAS_DE_LAS_UBICACIONES_CAT_ID = self.AREAS_DE_LAS_UBICACIONES_CAT.get('id')
        self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID = self.AREAS_DE_LAS_UBICACIONES_CAT.get('obj_id')

        self.AREAS_DE_LAS_UBICACIONES_SALIDA = self.lkm.catalog_id('areas_de_las_ubicaciones_salidas')
        self.AREAS_DE_LAS_UBICACIONES_SALIDA_ID = self.AREAS_DE_LAS_UBICACIONES_SALIDA.get('id')
        self.AREAS_DE_LAS_UBICACIONES_SALIDA_OBJ_ID = self.AREAS_DE_LAS_UBICACIONES_SALIDA.get('obj_id')
        #----Dic Fields Forms

        ## Module Fields ##
        ''' 
        self.mf : Estos son los campos que deseas mantener solo dentro de este modulo.
        Asegúrese de utilizar `llave` y el `id` del campo ej.
        'nombre_campo': "1f2h3j4j5d6f7h8j9j1a",
        '''
        mf = {
            'acepto_aviso_datos_personales': '6827488724317731cb288117',
            'acepto_aviso_privacidad': '6825268e0663cce4b1bf0a17',
            'archivo_invitacion': '673773741b2adb2d05d99d63',
            'areas_grupo':'663cf9d77500019d1359eb9f',
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
            "catalogo_departamentos": "66a83a7fca3453e21ea08d16",
            'catalogo_persona_involucrada': '66ec6936fc1f0f3f111d818f',
            "catalogo_puestos": "66a83a7dee0b950748489ca1",
            "catalogo_ubicaciones": "66a83a77cfed7f342775c161",
            'codigo_qr':'6685da34f065523d8d09052b',
            'color_articulo': '663e4730724f688b3059eb3b',
            'color_vehiculo': '663e4691f54d395ed7f27465',
            'comentario_pase':'65e0a69a322b61fbf9ed23af',
            'commentario_area': '66af1a77d703592958dca5eb',
            'config_dia_de_acceso': '662c304fad7432d296d92584',
            'config_dias_acceso': '662c304fad7432d296d92585',
            'config_limitar_acceso': '6635380dc9b3e7db4d59eb49',
            'conservar_datos_por': '6827488724317731cb288118',
            'curp': '5ea0897550b8dfe1f4d83a9f',
            'departamento_empleado': '663bc4ed8a6b120eab4d7f1e',
            'dias_acceso_pase':'662c304fad7432d296d92585',
            'direccion': '663a7e0fe48382c5b1230902',
            'direccion_visita': '67466b79bd2dc53e9864ad62',
            'documento': '663e5470424ad55e32832eec',
            'documento_certificado': '66427511e93cc23f04f27467',
            'duracion': '65cbe03c6c78b071a59f481e',
            'email_empleado': '6653f3709c6d89925dc04b2f',
            'email_pase':'662c2937108836dec6d92581',
            'email_visita_a': '638a9a7767c332f5d459fc82',
            'email_vista': '5ea069562f8250acf7d83aca',
            'empresa':'65fc814fb170488cf4d44c51',
            'empresa_pase':'66357d5e4f00f9018ce97ce9',
            'estatus_del_recorrido': '6639b2744bb44059fc59eb62',
            'examen_certificado':'66297e1579900d9018c886ad',
            'fecha_cetrificado_caducidad': '66427511e93cc23f04f2746a',
            'fecha_cetrificado_expedicion': '66427511e93cc23f04f27469',
            'fecha_desde_hasta': '662c304fad7432d296d92583',
            'fecha_desde_visita': '662c304fad7432d296d92582',
            'fecha_entrada':'662c51eb194f1cb7a91e5aef',
            'fecha_hasta_pase':'662c304fad7432d296d92583',
            ##### REVISAR Y BORRAR ######
            'fecha_salida':'662c51eb194f1cb7a91e5af0',
            'field_note':'6647fadc96f80017ac388648',
            'foto':'5ea35de83ab7dad56c66e045',
            'foto_equipo':'698ca59f8797d7e10e57617d',
            'foto_vehiculo':'698ca60575c268aadf768c57',
            'grupo_areas_acceso':'663fed6cb8262fd454326cb3',
            'grupo_equipos':'663e446cadf967542759ebbb',
            'grupo_instrucciones_pase':'65e0a68a06799422eded24aa',
            "grupo_puestos": "663c015f3ac46d98e8f27495",
            'grupo_ubicaciones_pase':'6834e34fa6242006acedda0f',
            'grupo_vehiculos': '663e446cadf967542759ebba',
            'grupo_visitados': '663d4ba61b14fab90559ebb0',
            'guard_group':'663fae53fa005c70de59eb95',
            'id_grupo':'639b65dfaf316bacfc551ba2',
            'id_usuario':'638a9a99616398d2e392a9f5',
            'identificacion':'65ce34985fa9df3dbf9dd2d0',
            'locker_id':'66480101786e8cdb66e70124',
            'marca_articulo':'663e4730724f688b3059eb3a',
            'marca_vehiculo':'65f22098d1dc5e0b9529e89b',
            'modelo_articulo':'66b29872aa6b3e6c3c02baa6',
            'modelo_vehiculo':'65f22098d1dc5e0b9529e89c',
            'motivo':'66ad58a3a5515ee3174f2bb5',
            'nombre_area':'663e5d44f5b8a7ce8211ed0f',
            'nombre_area_salida':'663fb45992f2c5afcfe97ca8',
            'nombre_articulo': '663e4730724f688b3059eb39',
            'nombre_del_recorrido': '6645050d873fc2d733961eba',
            'nombre_empleado': '62c5ff407febce07043024dd',
            'nombre_estado': '663a7dd6e48382c5b12308ff',
            'nombre_grupo':'638a9ab3616398d2e392a9fa',
            'nombre_guardia_apoyo': '663bd36eb19b7fb7d9e97ccb',
            'nombre_pase':'662c2937108836dec6d92580',
            'nombre_perfil': '661dc67e901906b7e9b73bac',
            'nombre_permiso':'662962bb203407ab90c886e4',
            'nombre_ubicacion_salida': '663e5c57f5b8a7ce8211ed0b',
            'nombre_usuario':'638a9a7767c332f5d459fc81',
            'nombre_visita': '5ea0693a0c12d5a8e43d37df',
            'nota': '6647fadc96f80017ac388647',
            'nss': '67466b79bd2dc53e9864ad63',
            'numero_serie': '66426453f076652427832fd2',
            'placas_vehiculo':'663e4691f54d395ed7f27464',
            'puesto_empleado': '663bc4c79b8046ce89e97cf4',
            'qr_pase':'64ef5b5fff1bec97d2ca27b6',
            'requerimientos':'662962bb203407ab90c886e5',
            'rfc':'64ecc95271803179d68ee081',
            'status_area':'663e5e4bf5b8a7ce8211ed14',
            'status_cetrificado':'664275469d8fffff0a59eb30',
            'status_doc_cetrificado':'664275e32c12468d16cb97dc',
            'status_gafete':'663e530af52d352956832f72',
            'status_locker':'663961d5390b9ec511e97ca5',
            'status_visita':'5ea1bd280ae8bad095055e61',
            'telefono':'661ea59c15baf5666f32360e',
            'telefono_pase':'662c2937108836dec6d92582',
            'telefono_visita': '663ec042713049de31e97c93',
            'telefono_visita_a': '67be0c43a31e5161c47f2bba',
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
            'username': '6759e4a7a9a6e13c7b26da33',
            'vigencia_certificado':'662962bb203407ab90c886e6',
            'vigencia_certificado_en':'662962bb203407ab90c886e7',
            'walkin':'66c4261351cc14058b020d48',
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
            'area_catalog':f"{self.AREAS_DE_LAS_UBICACIONES_SALIDA_OBJ_ID}",
            'area_perdido':f"{self.mf['nombre_area_salida']}",
            'articulo_perdido':'6639aeeb97b12e6f4ccb9711',
            'articulo_seleccion': f"{self.mf['articulo']}",
            'articulo_seleccion_catalog':f"{self.TIPO_ARTICULOS_PERDIDOS_CAT_OBJ_ID}",
            'color_perdido':'66ce223e174f3f39c0020d65',
            'comentario_perdido':'6639affa5a9f58f5b5cb9706',
            'date_entrega_perdido':'6639affa5a9f58f5b5cb9708',
            'date_hallazgo_perdido':'6639ae65356a6efb4de97d29',
            'descripcion':'66ce2397c5c4d148311adf83',
            'estatus_perdido':'6639ae65356a6efb4de97d28',
            'foto_perdido':'6639aeeb97b12e6f4ccb9712',
            'foto_recibe_perdido':'66ce2675293aabefa3559486',
            'identificacion_recibe_perdido':'664415ce630b1fb22b07e15a',
            'locker_catalog':f"{self.LOCKERS_CAT_OBJ_ID}",
            'locker_perdido':f"{self.mf['locker_id']}",
            'quien_entrega':'66ce2646033c793281b2c414',
            'quien_entrega_catalog':f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}",
            #'quien_entrega_interno':f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_name']}",
            'quien_entrega_externo':'66ce2647033c793281b2c415',
            'quien_entrega_interno':f"{self.f['worker_name']}",
            'recibe_perdido':'6639affa5a9f58f5b5cb9707',
            'telefono_recibe_perdido':'664415ce630b1fb22b07e159',
            'tipo_articulo_catalog':f"{self.TIPO_ARTICULOS_PERDIDOS_CAT_OBJ_ID}",
            'tipo_articulo_perdido':f"{self.mf['tipo_de_articulo_perdido']}",
            'ubicacion_catalog':f"{self.AREAS_DE_LAS_UBICACIONES_SALIDA_OBJ_ID}",
            'ubicacion_perdido':f"{self.mf['ubicacion']}",
        }

        #- Para salida de bitacora y lista
        self.bitacora_fields = {
            'caseta_entrada':f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.mf['nombre_area']}",
            'caseta_salida':f"{self.AREAS_DE_LAS_UBICACIONES_SALIDA_OBJ_ID}.{self.mf['nombre_area_salida']}",
            "catalogo_pase_entrada": "66a83ad652d2643c97489d31",
            'codigo_qr':f"{self.mf['codigo_qr']}",
            'comentario':"66ba83cc079d8a54634711c1",
            'documento':f"{self.mf['documento']}",
            'email_empleado': f"{self.mf['email_empleado']}",
            'fecha_entrada':f"{self.mf['fecha_entrada']}",
            'fecha_salida':f"{self.mf['fecha_salida']}",
            "gafete_catalog": "66a83ace56d1e741159ce114",
            'grupo_comentario':"66ba83942fef3a4613a07e91",
            'nombre_area_salida':f"{self.mf['catalog_caseta_salida']}.{self.mf['nombre_area_salida']}",
            'nombre_visita':f"{self.mf['catalog_visita']}.{self.mf['nombre_visita']}",
            "pase_entrada": f"{self.PASE_ENTRADA_OBJ_ID}",
            'perfil_visita':f"{self.mf['catalog_visita']}.{self.mf['nombre_perfil']}",
            'puesto_empleado': f"{self.mf['puesto_empleado']}",
            'status_gafete':f"{self.mf['status_gafete']}",
            'status_visita':f"{self.mf['tipo_registro']}",
            'tipo_comentario':"66ba83cc079d8a54634711c2",
            'ubicacion':f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.mf['ubicacion']}",
            'visita':f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}",
            'visita_a':"663d4ba61b14fab90559ebb0",
            'visita_departamento_empleado': f"{self.mf['departamento_empleado']}",
            'visita_nombre_empleado': f"{self.mf['nombre_empleado']}",
            'visita_user_id_empleado':f"{self.mf['user_id_empleado']}",
        }
        
        self.checkin_fields = {
            'boot_checkin_date':'663bffc28d00553254f274e1',
            'boot_checkout_date':'663bffc28d00553254f274e2',
            'cat_area': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['area']}",
            'cat_created_by': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_name']}",
            'cat_employee_b': f"{self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID}.{self.f['worker_name_b']}",
            'cat_location': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['location']}",
            'checkin_date':'66a28f3ca6b0f085b1518caa',
            'checkin_image': '685ac4e836c1c936b97275ad',
            'checkin_position':'66a28f3ca6b0f085b1518ca9',
            'checkin_status':'66a28f3ca6b0f085b1518ca8',
            'checkin_type': '663bffc28d00553254f274e0',
            'checkout_date':'66a28f3ca6b0f085b1518cab',
            'commentario_checkin_caseta':'66a5b9bed0c44910177eb724',
            'created_by': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_name']}",
            'employee': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_name']}",
            'employee_position':'665f482cc9a2f8acf685c20b',
            'forzar_cierre':'66a5b9bed0c44910177eb723',
            'fotografia_cierre_turno':'68d384ef55840a75f2cb7e29',
            'fotografia_inicio_turno':'68d384ef55840a75f2cb7e28',
            'guard_group': mf['guard_group'],
            'nombre_suplente':'6927a1176c60848998a157a2'
        }
        #- Para salida de bitacora  de articulos consecionados y lista
        self.cons_f = {
            'area_catalog_concesion': f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}",
            'area_concesion': f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.663e5d44f5b8a7ce8211ed0f",
            '_area_concesion': "663e5d44f5b8a7ce8211ed0f",
            'cantidad_devolucion': '699fec1e0f178e858bbf1b92',
            'cantidad_equipo_concesion': '69799523aa75e6a4c99c4d3f',
            'cantidad_equipo_devuelto': '6979962e6eac7e391dbb244e',
            'cantidad_equipo_pendiente': '699fe2e679aaab897b504c65',
            'caseta_concesion':  f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.663e5d44f5b8a7ce8211ed0f",
            '_caseta_concesion':  "663e5d44f5b8a7ce8211ed0f",
            'categoria_equipo_concesion':  f"{self.ACTIVOS_FIJOS_CAT_OBJ_ID}.66ce23efc5c4d148311adf86",
            '_categoria_equipo_concesion': '66ce23efc5c4d148311adf86',
            'comentario_entrega': '69799523aa75e6a4c99c4d41',
            'costo_equipo_concesion': f"{self.ACTIVOS_FIJOS_CAT_OBJ_ID}.697991fffd83f49bb9fe074e",
            '_costo_equipo_concesion': "697991fffd83f49bb9fe074e",
            'entregado_por': '6979962e6eac7e391dbb2450',
            'equipo_catalog_concesion': f"{self.ACTIVOS_FIJOS_CAT_OBJ_ID}",
            'equipo_imagen_concesion': '6646393c3fa8b818265d0326',
            'estatus_equipo': '6979962e6eac7e391dbb244f',
            'evidencia': '6970914a3059168605ce10c8',
            'evidencia_devolucion': '6979962e6eac7e391dbb2444',
            'evidencia_entrega': '6979962e6eac7e391dbb2453',
            'fecha_cierre_concesion': '66469f47c0580e5ead07e39b',
            'fecha_concesion': '66469ef8c9d58517f85d035f',
            'fecha_devolucion_concesion': '699fed207a15d39b937d805c',
            'firma': '6979b0b4a2a5a141dfef9cc5',
            'grupo_equipos': '697991cb4298cbe60db6b883',
            'grupo_equipos_devolucion': '699fe58a0f178e858bbf1b91',
            'id_movimiento':'697b055eb9a8d97bb5614ee0',
            'id_movimiento_devolucion':'699fe63679aaab897b504c71',
            'identificacion_entrega': '6979962e6eac7e391dbb2452',
            'imagen_equipo_concesion': f"{self.ACTIVOS_FIJOS_CAT_OBJ_ID}.6646393c3fa8b818265d0326",
            '_imagen_equipo_concesion': "6646393c3fa8b818265d0326",
            'marca_equipo_concesion': '65f22098d1dc5e0b9529e89b',
            'nombre_equipo': f"{self.ACTIVOS_FIJOS_CAT_OBJ_ID}.66c192ef89463aa27fc1818b",
            '_nombre_equipo': "66c192ef89463aa27fc1818b",
            'observacion_concesion': '66469f47c0580e5ead07e39a',
            'persona_catalog_concesion': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}",
            'persona_email_concesion': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.mf['email_visita_a']}",
            '_persona_email_concesion': self.mf['email_visita_a'],
            'persona_email_otro': '697991ad1cfb3b3210269901',
            'persona_id_concesion': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.mf['id_usuario']}",
            '_persona_id_concesion': self.mf['id_usuario'],
            'persona_identificacion_otro': '697991ad1cfb3b3210269902',
            'persona_nombre_concesion': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.mf['nombre_empleado']}",
            '_persona_nombre_concesion': self.mf['nombre_empleado'],
            'persona_nombre_otro': '696fd2291527668d067cdb85',
            'quien_entrega': '6979962e6eac7e391dbb2451',
            'quien_entrega_company': '699feaa2a0e52f55fd5589a5',
            'status_concesion': '66469e193e6a703350f2e029',
            'status_concesion_equipo': '66469e193e6a703350f2e299',
            'subotal_concesion_equipo': '69799523aa75e6a4c99c4d40',
            'tipo_persona_solicita': '66469e5a3e6a703350f2e03a',
            'ubicacion_catalog_concesion': f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}",
            'ubicacion_concesion': f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.mf['ubicacion']}",
            '_ubicacion_concesion': self.mf['ubicacion'],
        }
        
        self.status_equipo_dict = {
            'complete':'completo',
            'damage':'dañado',
            'lost':'perdido',
        }
        #- Para creación , edición y lista de fallas
        self.fallas_fields = {
            'falla':'66397bae9e8b08289a59ec86',
            'falla_accion_realizada': '66f2dfb2c80d24e5e82332b3',
            'falla_caseta':f"{self.mf['nombre_area']}",
            'falla_catalog': f"{self.LISTA_FALLAS_CAT_OBJ_ID}",
            'falla_comentario_solucion':'66f2dfb2c80d24e5e82332b3',
            'falla_comentarios':'66397d8cfd99d7263f83303a',
            'falla_documento':'66f2df6b6917fe63f4233227',
            'falla_documento_solucion':'66f2dfb2c80d24e5e82332b6',
            'falla_estatus': '66397e2c59c2600b1df2742c',
            'falla_evidencia':'66f2df6b6917fe63f4233226',
            'falla_evidencia_solucion':'66f2dfb2c80d24e5e82332b5',
            'falla_fecha_hora': '66397d0cfd99d7263f833032',
            'falla_fecha_seguimiento':'679a485c66c5d089fa6b8ef9',
            'falla_folio_accion_correctiva':'66f2dfb2c80d24e5e82332b4',
            #Seguimientos
            'falla_grupo_seguimiento': '6799125d9f8d78842caa22af',
            'falla_objeto_afectado':'66ce2441d63bb7a3871adeaf',
            'falla_personas_involucradas':'66f2dfb2c80d24e5e82332b4',
            'falla_reporta_catalog':f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}",
            'falla_reporta_departamento': '663bc4ed8a6b120eab4d7f1e',
            'falla_reporta_nombre': '62c5ff407febce07043024dd',
            'falla_responsable_solucionar_catalog': f"{self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID}",
            'falla_responsable_solucionar_documento':'663bc4ed8a6b120eab4d7f1e',
            'falla_responsable_solucionar_nombre':'663bd36eb19b7fb7d9e97ccb',
            'falla_subconcepto': '679124a8483c5220455bcb99',
            'falla_tiempo_transcurrido':'68a667d24ac4254634d87f3e',
            'falla_ubicacion': f"{self.mf['ubicacion']}",
            'falla_ubicacion_catalog':f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}",
        }
        
        #- Para creación , edición y lista de incidencias
        self.incidence_fields = {
            #Campos en grupo repetitivo Seguimiento:
            'accion_correctiva_incidencia':'683de45ddcf6fcee78e61ed7',
            'acciones_tomadas':'66ec69a914bf1142b6a024e3',
            #Campos en grupo repetitivo acciones tomadas:
            # 'acciones_tomadas_incidencia':'66ec6987f251a9c2cef0126f',
            'acciones_tomadas_incidencia':'688bbd509b98fd9afaf2c401',
            'afectacion_patrimonial_incidencia':'688a9cbda7b2dd2b599ff381',
            'area_incidencia': '663e5d44f5b8a7ce8211ed0f',
            'area_incidencia_catalog': f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}",
            'area_incidencia_ver2':f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.mf['nombre_area']}",
            'atencion_medica':'688a9b96ccfd13dc0c12b189',
            'autoridad': '688bc5ef1037e90c4ccd4eb3',
            'cantidad':'66ec67e42bcc75c3a458778e',
            'categoria':'686807d46e41614d708f6fc9',
            'color': '684c3eaa04aaab135d7dfbb6',
            'color_cabello': '684c3e026d974f9625e11306',
            'color_piel':'684c3e026d974f9625e11305',
            'comentario_incidencia': '66397586aa8bbc0371e97c80',
            'comentarios':'688bfecfa1b4ecf477a6010a',
            'dano_incidencia':'66ec69144a27bb6151a0255a',
            'datos_deposito_incidencia':'66ec6793eb386ff970218f1f',
            'descripcion_afectacion':'688a9d52c1ce871f545b3b9d',
            'descripcion_fisica_vestimenta': '684c3e026d974f9625e11308',
            'documento':'68c305c624e99970e536dc45',
            'documento_incidencia':'66ec6846028e5550cbf012e1',
            'duracion_estimada': '688a9d52c1ce871f545b3b9c',
            'edad':'684c3e026d974f9625e11304',
            'estatura_aproximada': '684c3e026d974f9625e11307',
            'estatus': '68c04a6b213e28722aec0610',
            'estatus_afectacion':'68d4bba7c6e9e28b9e30e133',
            'evidencia':'68c305c624e99970e536dc44',
            'evidencia_incidencia':'66ec6846028e5550cbf012e0',
            'fecha_hora_incidencia': '66396efeb37283c921e97cdf',
            'fecha_inicio_seg':'683de45ddcf6fcee78e61ed9',
            'grupo_etario':'688a9b96ccfd13dc0c12b188',
            'incidencia': '663973809fa65cafa759eb97',
            'incidencia_catalog': f"{self.LISTA_INCIDENCIAS_CAT_OBJ_ID}",
            'incidencia_documento_solucion':'683de45ddcf6fcee78e61edc',
            'incidencia_evidencia_solucion':'683de45ddcf6fcee78e61edb',
            'incidencia_personas_involucradas':'684c3e026d974f9625e1130f',
            'incidente':'663973809fa65cafa759eb97',
            'info_coincide_con_videos': '684c3e026d974f9625e1130d',
            'llamo_a_policia': '688bbddbd40db062d071862f',
            'marca': '684c3eaa04aaab135d7dfbb4',
            'modelo': '684c3eaa04aaab135d7dfbb5',
            'monto_estimado': '688a9d52c1ce871f545b3b99',
            #Campos en grupo repetitivo personas involucradas:
            'nombre_completo': '66ec69239938c882f8222036',
            #Persona extraviada
            'nombre_completo_persona_extraviada':'684c3e026d974f9625e11303',
            'nombre_completo_responsable': '684c3e026d974f9625e11309',
            'notificacion_incidencia':'66ec6ae6c17763d760218e5e',
            'num_doc_identidad': '684c3e026d974f9625e1130b',
            'numero_folio_referencia': '688bc5ef1037e90c4ccd4eb4',
            'origen': '689e391c7ce783d3860f3f0e',
            'parentesco': '684c3e026d974f9625e1130a',
            'personas_involucradas_incidencia':'66ec69144a27bb6151a0255b',
            #Grupos Repetitivos
            'pertenencias_sustraidas': '684c3e6821796d7880117f23',
            #Robo de vehiculo
            'placas': '684c3eaa04aaab135d7dfbb3',
            'prioridad_incidencia':'66ec69144a27bb6151a0255c',
            'puesto':'68d6efb0a209c0144d6c3761',
            'reporta_incidencia': '62c5ff407febce07043024dd',
            'reporta_incidencia_catalog': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}", 
            'responsable': '688bbddbd40db062d0718630',
            'responsable_accion':'66ec69a914bf1142b6a024e2',
            'responsable_que_entrega': '688bb6ca2f094c5555b2097b',
            'retenido':'688bc5ef1037e90c4ccd4eb1',
            'rol':'66ec6936fc1f0f3f111d818f',
            'seguimientos_incidencia':'683de3cfcf4a5d248ffbaf89',
            'sexo':'688a9a59244b64c3c374c9e6',
            'sub_categoria': '686807a7ee7705c5c8eb181a',
            'tag':'688abce60cf2954b12f7bbe9',
            'tags':'6834e4e8b0ed467efade7972',
            'telefono': '684c3e026d974f9625e1130c',
            'tiempo_transcurrido': '688d1b7ad3268f1968d5ddf0',
            'tipo': '684c3eaa04aaab135d7dfbb2',
            #Campos en grupo repetitivo afectacion patrimonial:
            'tipo_afectacion': '688a9d52c1ce871f545b3b98',
            'tipo_dano_incidencia': '66ec6962ea3c921534b22c54',
            'tipo_deposito': '66ec67dc608b1faed7b22c45',
            'tipo_incidencia': '66ec667d7646541f2ea024de',
            'tipo_persona': '66ec6936fc1f0f3f111d818f',
            'total_deposito_incidencia':'66ec6821ea3c921534b22c30',
            'ubicacion_incidencia': f"{self.mf['ubicacion']}",
            'ubicacion_incidencia_catalog': f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}",
            #Robo de cableado
            'valor_estimado': '684c3e6821796d7880117f22',
        }
        
        #- Para creación , edición y lista de gafetes y lockers
        self.gafetes_fields = {
            'caseta_gafete':f"{self.UBICACIONES_CAT_OBJ_ID}.{self.mf['nombre_area']}",
            'catalog_gafete':'664fc6ec8d4dfb34de095586',
            'documento_gafete':'65e0b6f7a07a72e587124dc6',
            'gafete_id':'664803e6d79bc1dfd33885e1',
            'ubicacion_gafete':f"{self.UBICACIONES_CAT_OBJ_ID}.{self.mf['ubicacion']}",
            'visita_gafete':f"{self.mf['catalog_visita']}.{self.mf['nombre_visita']}",
        }
        
        self.lockers_fields = {
            'locker_id':'66480101786e8cdb66e70124',
            'status_locker':"663961d5390b9ec511e97ca5",
            'tipo_locker':'66ccfec6acaa16b31e5593a3',
        }
        #- Para creación , edición y lista de notas
        self.notes_fields = {
            'note':'6647fadc96f80017ac388647',
            'note_booth':f"{self.mf['nombre_area']}",
            'note_catalog_booth':f"{self.UBICACIONES_CAT_OBJ_ID}",
            'note_catalog_guard':f"{self.mf['catalog_guard']}",
            'note_catalog_guard_close':f"{self.mf['catalog_guard_close']}",
            'note_close_date':'6647fadc96f80017ac38864a',
            'note_comments':'6647fb38da07bf430e273ea2',
            'note_comments_group':'6647fb1874c1a87eb02a9037',
            'note_file':'6647fadc96f80017ac388648',
            'note_guard':f"{self.mf['nombre_empleado']}",
            'note_guard_close':f"{self.mf['nombre_guardia_apoyo']}",
            'note_open_date':'6647fadc96f80017ac388646',
            'note_pic':'6647fadc96f80017ac388649',
            'note_status':'6647f9eb6eefdb1840684dc1',
        }
        
        self.notes_project_fields = {
            'area': f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['area']}",
            'closed_by': f"{self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID}.{self.f['worker_name_b']}",
            'created_by': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_name']}",
            'location': f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['location']}",
            'support_guard':f"{self.CONF_AREA_EMPLEADOS_AP_CAT_OBJ_ID}.{self.f['worker_name_b']}",
        }
        
        self.pase_entrada_fields = {
            'acepto_aviso_datos_personales': '6827488724317731cb288117',
            'acepto_aviso_privacidad': '6825268e0663cce4b1bf0a17',
            'apple_wallet_pass': '682785fbedd82a9104287e25',
            'archivo_invitacion': '673773741b2adb2d05d99d63',
            'area':f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}",
            'catalog_area_pase':'664fc5f3bbbef12ae61b15e9',
            'catalogo_visitante_registrado': '66a83ad456d1e741159ce118',
            'comentario_pase':'65e0a69a322b61fbf9ed23af',
            'commentario_area':"66af1a77d703592958dca5eb",
            'conf_perfiles':f"{self.CONFIG_PERFILES_OBJ_ID}",
            'conservar_datos_por': '6827488724317731cb288118',
            'creado_desde':'698b6f3d13a551df2b2ecfcb',
            'curp_catalog_pase':f"{self.PASE_ENTRADA_OBJ_ID}.{self.mf['curp']}",
            'direccion_pase':f"{self.mf['catalog_ubicacion']}.{self.mf['direccion']}",
            'email':'662c2937108836dec6d92581',
            'email_catalog_pase':f"{self.PASE_ENTRADA_OBJ_ID}.{self.mf['email_vista']}",
            'email_pase':'662c2937108836dec6d92581',
            'empresa_pase_catalog':f"{self.PASE_ENTRADA_OBJ_ID}.{self.mf['empresa']}",
            'empresa_pase':'66357d5e4f00f9018ce97ce9',
            'favoritos':'674642e2d53ce9476994dd89',  
            'fecha_hasta_pase':'662c304fad7432d296d92583',
            'foto_pase':f"{self.PASE_ENTRADA_OBJ_ID}.{self.mf['foto']}",
            'foto_pase_id':f"{self.mf['foto']}",
            'google_wallet_pass_url': '6820df5a6cfcee960fb4275c',
            'grupo_areas_acceso':'663fed6cb8262fd454326cb3',
            'grupo_equipos':'663e446cadf967542759ebbb',
            'grupo_instrucciones_pase':'65e0a68a06799422eded24aa',
            'identificacion_pase':f"{self.PASE_ENTRADA_OBJ_ID}.{self.mf['identificacion']}",
            'identificacion_pase_id':f"{self.mf['identificacion']}",
            'motivo':f"{self.CONFIG_PERFILES_OBJ_ID}.{self.mf['motivo']}",
            'nombre':'662c2937108836dec6d92580',
            'nombre_area':f"{self.mf['nombre_area']}",
            'nombre_catalog_pase':f"{self.PASE_ENTRADA_OBJ_ID}.{self.mf['nombre_visita']}",
            'nombre_pase':'662c2937108836dec6d92580',
            'nombre_perfil':f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_name']}",
            'nombre_permiso':f"{self.CONFIG_PERFILES_OBJ_ID}.662962bb203407ab90c886e4",
            'nombre_tipo_pase':f"{self.CONFIG_PERFILES_OBJ_ID}.66297e1579900d9018c886ad",
            'nombre_visitante_registrado': '5ea0693a0c12d5a8e43d37df',
            'pdf_to_img': '682222d27e0ea505751e17b4',
            'perfil_pase':f"{self.CONFIG_PERFILES_OBJ_ID}.661dc67e901906b7e9b73bac",
            'perfil_pase_id':f"661dc67e901906b7e9b73bac",
            'qr_pase':'64ef5b5fff1bec97d2ca27b6',
            'requerimientos_pase':f"{self.CONFIG_PERFILES_OBJ_ID}.662962bb203407ab90c886e5",
            'status_pase':'66353daa223b8a43d7f274b5',
            'status_visita_pase':f"{self.PASE_ENTRADA_OBJ_ID}.{self.mf['status_visita']}",
            'telefono_catalog_pase':f"{self.PASE_ENTRADA_OBJ_ID}.{self.mf['telefono']}",
            'telefono_pase':'662c2937108836dec6d92582',
            'tipo_comentario':'66af1977ffb6fd75e769f457',
            'tipo_visita':"662c262cace163ca3ed3bb3a",
            'todas_las_areas':'68f9fdfbd9bf5cb7fd3caece',
            'ubicacion_pase':f"{self.mf['catalog_ubicacion']}.{self.mf['ubicacion']}",
            'ubicaciones':'6834e34fa6242006acedda0f',
            'vigencia_expresa_pase':f"{self.CONFIG_PERFILES_OBJ_ID}.662962bb203407ab90c886e7",
            'vigencia_pase':f"{self.CONFIG_PERFILES_OBJ_ID}.662962bb203407ab90c886e6",
            'visita_a':'663d4ba61b14fab90559ebb0',
            'walkin_email':'662c2937108836dec6d92581',
            'walkin_empresa':'66357d5e4f00f9018ce97ce9',
            'walkin_fotografia':'66c4d5b6d1095c4ce8b2c42a',
            'walkin_identificacion':'66c4d5b6d1095c4ce8b2c42b',
            'walkin_nombre':'662c2937108836dec6d92580',
            'walkin_telefono':'662c2937108836dec6d92582',
            'worker_department': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_department']}",
            'worker_position':   f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_position']}",    
        }
        
        self.pase_grupo_visitados ={
        }
        
        # self.pase_entrada_fields.update(self.pase_grupo_visitados)
        self.pase_grupo_areas = {
            'nombre_perfil':     f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.f['area']}",
        }
        
        # self.pase_entrada_fields.update(self.pase_grupo_areas)
        self.pase_grupo_vehiculos = {
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
            'ubicaciones': '6834e34fa6242006acedda0f',
            'miembros_grupo':'69d3fc307a74fbc034b3e65f',
            'miembros_grupo_nombre':'662c2937108836dec6d9258b',
            'miembros_grupo_email':'69d401692bab86e937e57106',
            'miembros_grupo_telefono':'69d401692bab86e937e57107',
            'miembros_grupo_pase':'69d401692bab86e937e57108',
        })

        self.conf_accesos_fields = {
            'grupos':f"{self.GRUPOS_CAT_OBJ_ID}",
            'menus':"6722472f162366c38ebe1c64",
            'usuario_cat':  f"{self.EMPLOYEE_OBJ_ID}",
        }

        self.conf_modulo_seguridad = {
            'datos_requeridos':"6769756fc728a0b63b8431ea",
            'envio_por':"6810180169eeaca9517baa5b",
            'grupo_requisitos':"676975321df93a68a609f9ce",
            'grupo_tipo_de_pase': '694055a57d064b380f010d7f',
            'ubicacion':"663e5c57f5b8a7ce8211ed0b",
            'ubicacion_cat':  f"{self.UBICACIONES_CAT_OBJ_ID}",
        }

        self.paquetes_fields = {
            'area_paqueteria':f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}.{self.mf['nombre_area']}",
            'descripcion_paqueteria':"67e4652619b4be1c5a76a485",
            'entregado_a_paqueteria':'67e4652619b4be1c5a76a489',
            'estatus_paqueteria': '67e4652619b4be1c5a76a488',
            'fecha_entregado_paqueteria': '67e4652619b4be1c5a76a487',
            'fecha_recibido_paqueteria': '67e4652619b4be1c5a76a486',
            'fotografia_paqueteria': "67e46624da3191c5ef4ab6d0",
            'guardado_en_paqueteria': f"{self.LOCKERS_CAT_OBJ_ID}.{self.mf['locker_id']}",
            'proveedor':'667468e3e577b8b98c852aaa',
            'proveedor_cat':f"{self.PROVEEDORES_CAT_OBJ_ID}",
            'quien_recibe_cat': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}",
            'quien_recibe_otro':"69c47a1ce96590f9dbf494b0",
            'quien_recibe_paqueteria':f"{self.mf['nombre_empleado']}",
            'ubicacion_paqueteria':f"{self.UBICACIONES_CAT_OBJ_ID}.{self.mf['ubicacion']}",
        }

        self.rondin_keys = {
            'accion_recurrencia': 'abcde00010000000a0000001',
            'areas': '6645052ef8bc829a5ccafaf5',
            'cada_cuantas_horas_se_repite': 'abcde0001000000000010013',
            'cada_cuantos_dias_se_repite': 'abcde0001000000000010017',
            'cada_cuantos_meses_se_repite': 'abcde0001000000000010019',
            'cada_cuantos_minutos_se_repite': 'abcde0001000000000010011',
            'cron_id':'abcde0001000000000011111',
            'cuanto_tiempo_de_anticipacion': 'abcde0002000000000010004',
            'cuanto_tiempo_de_anticipacion_expresado_en': 'abcde0002000000000010005',
            'duracion_estimada': '6854459836ea891d9d2be7d9',
            'en_que_hora_sucede': 'abcde0001000000000010012',
            'en_que_mes': 'abcde0001000000000010018',
            'en_que_minuto_sucede': 'abcde0001000000000010010',
            'en_que_semana_sucede': 'abcde0001000000000010015',
            'fecha1':'abcde000100000000000f000',
            'fecha2':'abcde000100000000000f001',
            'fecha_final_recurrencia': 'abcde0001000000000010099',
            'fecha_hora_programada': 'abcde0001000000000010001',
            'grupo_areas':'66462aa5d4a4af2eea07e0d1',
            'grupo_asignado': '638a9ab3616398d2e392a9fa',
            'grupo_asignado_rondin':'671055aaa487da57ba57b294',
            'id_grupo':'639b65dfaf316bacfc551ba2',
            'la_recurrencia_cuenta_con_fecha_final': '64374e47a208e5c0ff95e9bd',
            'la_tarea_es_de': 'abcde0001000000000010006',
            "link":'6927eb61d92ecf923b60a0de',
            'nombre_rondin': '6645050d873fc2d733961eba',
            'programar_anticipacion': 'abcde0002000000000010001',
            'que_dia_del_mes': 'abcde0001000000000010016',
            'que_dias_de_la_semana': 'abcde0001000000000010014',
            'se_repite_cada': 'abcde0001000000000010007',
            'status':'abcde00010000000a0000000',
            'sucede_cada': 'abcde0001000000000010008',
            'sucede_recurrencia': 'abcde0001000000000010009',
            'tiempo_para_ejecutar_tarea': 'abcde0001000000000010004',
            'tiempo_para_ejecutar_tarea_expresado_en': 'abcde0001000000000010005',
            'tipo_rondin':'69b9b98d2a02f4a0dd35f5c1',
            'ubicacion': '663e5c57f5b8a7ce8211ed0b',
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
            'areas_del_rondin': '66462aa5d4a4af2eea07e0d1',
            'duracion_rondin':'6639b47565d8e5c06fe97cf3',
            'duracion_traslado_area':'6760a9581e31b10a38a22f1f',
            'fecha_inspeccion_area':'6760a908a43b1b0e41abad6b',
            'fecha_programacion':'6760a8e68cef14ecd7f8b6fe',
            'fecha_inicio_rondin':'6818ea068a7f3446f1bae3b3',
            'grupo_areas_visitadas':'66462aa5d4a4af2eea07e0d1',
            'evidencia_incidencia':'66ec6846028e5550cbf012e0',
            'area_foto': '6763096aa99cee046ba766ad',
            'area_tag_id': '6762f7b0922cc2a2f57d4044',
            'tipo_de_area': '663e5e68f5b8a7ce8211ed18',
            'foto_evidencia_area': '681144fb0d423e25b42818d2',
            'foto_equipo':'698ca59f8797d7e10e57617d',
            'foto_vehiculo':'698ca60575c268aadf768c57',
            'grupo_incidencias_check': '681144fb0d423e25b42818d3',
            'comentario_check_area': '681144fb0d423e25b42818d4',
            'check_status': '681fa6a8d916c74b691e174b',
            'status_check_ubicacion': '68e41c904da05123bf9326ee',
            'incidente':'663973809fa65cafa759eb97',
            'categoria':'686807d46e41614d708f6fc9',
            'sub_categoria': '686807a7ee7705c5c8eb181a',
            'incidente_open': '6811455664dc22ecae83f75b',
            'incidente_comentario': '681145323d9b5fa2e16e35cb',
            'incidente_accion': '681145323d9b5fa2e16e35cc',
            'incidente_evidencia': '681145323d9b5fa2e16e35cd',
            'incidente_documento': '685063ba36910b2da9952697',
            'bitacora_rondin_incidencias': '686468a637d014b9e0ab5090',
            'fecha_hora_incidente_bitacora': '69000e4c43078234e5e08390',
            'area_incidente_bitacora': '69000e4c43078234e5e0838f',
            'comentario_incidente_bitacora': '681145323d9b5fa2e16e35cb',
            'id_usuario':'638a9a99616398d2e392a9f5',
            'nombre_area_salida':'663fb45992f2c5afcfe97ca8',
            'status_cron': 'abcde00010000000a0000000',
            'fecha_primer_evento':'abcde0001000000000010001',
            'fecha_final_recurrencia': 'abcde0001000000000010099',
            'geolocalizacion_area_ubicacion': '688bac1ecfdcf8b16eb209b5',
            'grupo_de_areas_recorrido': '6645052ef8bc829a5ccafaf5',
            'tipo_guardia': '68acee270f2af5e173b7f92e',
            'image_checkin': '6855e761adab5d93274da7d7',
            'foto_cierre_turno': '6879823d856f580aa0e05a3b',
            'fecha_cierre_turno': '6879828d0234f02649cad391',
            'personalizacion_pases': '695d2e1f6be562c3da95c4a7',
            'pases': '695d31b503ccc7766ac28507',
            'grupo_alertas': '695d35b618a37ea04899524f',
            'nombre_alerta': '695d36605f78faab793f497b',
            'accion_alerta': '695d36605f78faab793f497c',
            'llamar_num_alerta': '695d36605f78faab793f497d',
            'email_alerta': '695d36605f78faab793f497e'
        })