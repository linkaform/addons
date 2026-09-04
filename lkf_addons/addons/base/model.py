# -*- coding: utf-8 -*-
### Linkaform Modules / Archivo de Módulo ###
'''
Este archivo define el modelo de datos del módulo Accesos.
Contiene los IDs de formularios, catálogos y campos (fields) usados por la clase Accesos.

Separado de app.py para mantener la configuración de datos desacoplada de la lógica de negocio.
'''
from linkaform_api import base

### Modelo de Módulo ###
'''
AccesosModel agrupa la inicialización de IDs de formularios, catálogos y fields.
La clase Accesos en app.py hereda de esta clase para tener acceso a todas las variables
sin mezclarlas con la lógica de negocio.
'''

class BaseModel(base.LKF_Base):

    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False, **kwargs):
        mf =  {
                'form_name':'5d810a982628de5556500d55',
                'form_id':'5d810a982628de5556500d56',
                'form_type':'ccccc0000000000000000002',
                }
        if hasattr(self, 'mf'):
            self.mf.update(mf)
        else:
            self.mf = mf
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api, **kwargs)
        #use self.lkm.catalog_id() to get catalog id
       #--Variables
        ### Forms ###
        '''
        `self.FORM_NAME = self.lkm.form_id('form_name',id)` ---> Aquí deberás guardar los `ID` de los formularios.
        Para ello deberás llamar el método `lkm.form_id` del objeto `lkm` (linkaform modules, por sus siglas).
        En `lkm` están todas las funciones generales de módulos.
        '''
        self.CONTACTO = self.lkm.form_id('contacto', 'id')
        self.CLIENTE = self.lkm.form_id('clientes', 'id')
        self.CONFIGURACIONES = self.lkm.form_id('configuraciones', 'id')
        self.ENVIO_DE_CORREOS = self.lkm.form_id('envio_de_correos', 'id')
        self.ROL = self.lkm.form_id('rol', 'id')
        self.USUARIOS_FORM = self.lkm.form_id('usuarios', 'id')
        ### Catálogos ###
        '''
        `self.CATALOG_NAME = self.lkm.catalog_id('catalog_name',id)` ---> Aquí deberás guardar los `ID` de los catálogos.
        Para ello deberás llamar el método `lkm.catalog_id` del objeto `lkm`(linkaform modules, por sus siglas).
        En `lkm` están todas las funciones generales de módulos).
        '''

        self.CATALOGO_FORMAS_CAT = self.lkm.catalog_id('catalogo_de_formas')
        self.CATALOGO_FORMAS_CAT_ID = self.CATALOGO_FORMAS_CAT.get('id')
        self.CATALOGO_FORMAS_CAT_OBJ_ID = self.CATALOGO_FORMAS_CAT.get('obj_id')

        self.CLIENTE_CAT = self.lkm.catalog_id('clientes')
        self.CLIENTE_CAT_ID = self.CLIENTE_CAT.get('id')
        self.CLIENTE_CAT_OBJ_ID = self.CLIENTE_CAT.get('obj_id')

        self.COMPANY = self.lkm.catalog_id('compaia')
        self.COMPANY_ID = self.COMPANY.get('id')
        self.COMPANY_OBJ_ID = self.COMPANY.get('obj_id')

        self.CONTACTO_CAT = self.lkm.catalog_id('contacto')
        self.CONTACTO_CAT_ID = self.CONTACTO_CAT.get('id')
        self.CONTACTO_CAT_OBJ_ID = self.CONTACTO_CAT.get('obj_id')

        self.COUNTRY = self.lkm.catalog_id('pais')
        self.COUNTRY_ID = self.COUNTRY.get('id')
        self.COUNTRY_OBJ_ID = self.COUNTRY.get('obj_id')

        self.ESTADO = self.lkm.catalog_id('estados')
        self.ESTADO_ID = self.ESTADO.get('id')
        self.ESTADO_OBJ_ID = self.ESTADO.get('obj_id')

        self.ROL_CAT = self.lkm.catalog_id('rol')
        self.ROL_CAT_ID = self.ROL_CAT.get('id')
        self.ROL_CAT_OBJ_ID = self.ROL_CAT.get('obj_id')

        self.TIMEZONE = self.lkm.catalog_id('timezone')
        self.TIMEZONE_ID = self.TIMEZONE.get('id')
        self.TIMEZONE_OBJ_ID = self.TIMEZONE.get('obj_id')

        self.USUARIOS = self.lkm.catalog_id('usuarios')
        self.USUARIOS_ID = self.USUARIOS.get('id')
        self.USUARIOS_OBJ_ID = self.USUARIOS.get('obj_id')

        self.GROUP = self.lkm.catalog_id('grupos')
        self.GROUP_ID = self.GROUP.get('id')
        self.GROUP_OBJ_ID = self.GROUP.get('obj_id')

        self.UOM = self.lkm.catalog_id('unidad_de_medida')
        self.UOM_ID = self.UOM.get('id')
        self.UOM_OBJ_ID = self.UOM.get('obj_id')


        ### Global Variables


        self.f.update( {
            'address':'663a7e0fe48382c5b1230902',
            'address2':'663a7f79e48382c5b123090a',
            'address_code':'ccca7e0fe48382c5b1230901',
            'address_geolocation':'663e5c8cf5b8a7ce8211ed0c',
            'address_image':'663a808be48382c5b123090d',
            'address_name':'663a7e0fe48382c5b1230901',
            'address_status':'663a7f67e48382c5b1230909',
            'address_type':'663a7f67e48382c5b1230908',
            'asignar_a':'abcde0001000000000020003',
            'asignar_de_grupo':'67ad6e90067960b5f2ce1e15',
            'cat_timezone':f'{self.TIMEZONE_OBJ_ID}.665e4f90c4cf32cb52ebe15c',
            'city':'6654187fc85ce22aaf8bb070',
            'client_code':'6711ea74b8514dc4fdfd917f',
            'config_group':'66ed0baac9aefada5b04b817',
            'country':'663a7ca6e48382c5b12308fa',
            'country_code':'663a7ca6e48382c5b12308fb',
            'country_ph_code':'663a7ca6e48382c5b12308fc',
            'email':'663a7ee1e48382c5b1230907',
            'email_contacto':'66bfd647cd15883ed163e9b5',
            'field_id_status':'5e32fbb498849f475cfbdca2',
            'group_id':'639b65dfaf316bacfc551ba2',
            'group_name':'638a9ab3616398d2e392a9fa',
            'grupo_roles':'6a46f1d3b89f9975dfd0bae8',
            'new_user_complete_name':'638a9a7767c332f5d459fc81',
            'new_user_email':'638a9a7767c332f5d459fc82',
            'new_user_id':'638a9a99616398d2e392a9f5',
            'new_user_phone':'67be0c43a31e5161c47f2bba',
            'new_user_position':'67be0c43a31e5161c47f2bbb',
            'new_user_status':'679d023876ad7f5ba642f4ed',
            'new_user_temp_password':'67be0b7896e72a692b4fa660',
            'new_user_username':'6759e4a7a9a6e13c7b26da33',
            'nombre_comercial':'667468e3e577b8b98c852aaa',
            'pagina_web':'66bfd66ecd15883ed163e9b7',
            'phone':'663a7ee1e48382c5b1230906',
            'phone2':'663a7ee1e48382c5b1232226',
            'razon_social':'6687f2f37b2c023e187d6252',
            'rfc_razon_social':'667468e3e577b8b98c852aab',
            'rol':'6a46f2730fc4d03a90da2209',
            'state':'663a7dd6e48382c5b12308ff',
            'state_code':'663a7dd6e48382c5b1230900',
            'telefono':'66bfd666cd15883ed163e9b6',
            'timezone':'665e4f90c4cf32cb52ebe15c',
            'uom':'669efc6f47920d1b51663d29',
            'uom_category':'669efbf447920d1b51663d28',
            'zip_code':'663a7ee1e48382c5b1230905',
        }
        )

        self.envio_correo_fields = {
            'email_from':"67169f72c736cc47794404f8",
            'email_to':"670d2e32756833542954716c",
            'enviado_desde':"6716a1067f394110d24404eb",
            'msj':"670d2d9d0337e410e4353550",
            "nombre": "670d2e32756833542954716b",
            'titulo':"67169f72c736cc47794404f9",
        }

        self.config_fields = {
            'demora':f'{self.f.get("demora")}',
            'lead_time':f'{self.f.get("lead_time")}',
            'dias_laborales_consumo':f'{self.f.get("dias_laborales_consumo")}',
            'factor_crecimiento_jit':f'{self.f.get("factor_crecimiento_jit")}',
            'factor_seguridad_jit':f'{self.f.get("factor_seguridad_jit")}',
            'uom':f'{self.UOM_OBJ_ID}.{self.f.get("uom")}',
            'procurment_location':f'{self.f.get("config_group")}',
            'warehouse_kind': '66ed0c88c9aefada5b04b818',
            # 'warehouse':f'{self.WAREHOUSE_OBJ_ID}.{self.f.get("warehouse")}',
            # 'location':f'{self.WAREHOUSE_OBJ_ID}.{self.f.get("location")}',
        }

        self.MENUS_CATALOG = self.lkm.catalog_id('elementos_menu')
        self.MENUS_CATALOG_ID = self.MENUS_CATALOG.get('id')
        self.MENUS_CATALOG_OBJ_ID = self.MENUS_CATALOG.get('obj_id')
        self.MENUS_FORM = self.lkm.form_id('configuracion_menus','id')

        self.menu_form_fields = {
            "username": "6759e4a7a9a6e13c7b26da33",
            "usuario_id": "638a9a99616398d2e392a9f5",
            "grupo_asignado": "638a9ab3616398d2e392a9fa",
            "grupo_id": "639b65dfaf316bacfc551ba2",
            "elementos": "69efaf4c4a59aa2591074f45",
            "menu": "69efaf883bcb25ed1458465d",
            "seccion": "69efaf883bcb25ed1458465e",
            "elemento": "69efaf883bcb25ed1458465f",
            "key": "69efb57c4a59aa2591074f4e",
            "plataforms": "69f27e8cdf4d7acc80f2e9b0"
        }

        self.menu_catalog_fields = {
            "catalog_menu_key": "69f28216c76fd3bed14949a2",
            "catalog_menu": "69efaf883bcb25ed1458465d",
            "catalog_menu_order": "69f27e8cdf4d7acc80f2e9a8",
            "catalog_menu_icon": "69f27e8cdf4d7acc80f2e9a9",
            "catalog_menu_columns": "69f27e8cdf4d7acc80f2e9aa",
            "catalog_seccion_key": "69f28216c76fd3bed14949a3",
            "catalog_seccion": "69efaf883bcb25ed1458465e",
            "catalog_seccion_order": "69f27e8cdf4d7acc80f2e9ab",
            "catalog_seccion_column": "69f27e8cdf4d7acc80f2e9ac",
            "catalog_seccion_href": "6a036ef020c6e62e1c3fdee6",
            "catalog_seccion_icon": "69f27e8cdf4d7acc80f2e9ad",
            "catalog_seccion_icon_color": "69f27e8cdf4d7acc80f2e9ae",
            "catalog_elemento": "69efaf883bcb25ed1458465f",
            "catalog_key": "69efb57c4a59aa2591074f4e",
            "catalog_type": "69efb3dcfc8545da78179bf9",
            "catalog_item_order": "69efb3dcfc8545da78179bfa",
            "catalog_href_web": "69efb3dcfc8545da78179bf8",
            "catalog_route_mobile": "69f27e8cdf4d7acc80f2e9af",
            "catalog_plataforms": "69f27e8cdf4d7acc80f2e9b0",
            "catalog_item_icon": "6a9206aa07b8a64f70abc72d",
            "catalog_seccion_description": "6a9206aa07b8a64f70abc72e"
        }

        self.f.update({
            'menus':'6722472f162366c38ebe1c64'
        })

        self.ARTICULOS_CONSECIONADOS = self.lkm.script_id('articulos_consecionados','id')
        self.ARTICULOS_PERDIDOS = self.lkm.script_id('articulos_perdidos','id')
        self.FALLAS = self.lkm.script_id('fallas','id')
        self.GET_STATS = self.lkm.script_id('get_stats','id')
        self.GAFETES_LOCKERS = self.lkm.script_id('gafetes_lockers','id')
        self.NOTAS = self.lkm.script_id('notes','id')
        self.PAQUETERIA = self.lkm.script_id('paqueteria','id')
        self.SCRIPT_TURNOS = self.lkm.script_id('script_turnos','id')
        self.SCRIPT_PASE_ACCESO = self.lkm.script_id('pase_de_acceso','id')
        self.SCRIPT_PASE_ACCESO_API = self.lkm.script_id('pase_de_acceso_use_api','id')
        self.SCRIPT_GOOGLE_WALLET = self.lkm.script_id('create_pass_google_wallet','id')
        self.SCRIPT_RONDINES = self.lkm.script_id('rondines','id')
        self.SCRIPT_TRANSPORTISTAS = self.lkm.script_id('transportistas','id')
        self.OFFLINE_SERVICES = self.lkm.script_id('offline_services','id')
        self.OCR_DOCS = self.lkm.script_id('ocr_docs','id')
        self.SCRIPT_MENUS = self.lkm.script_id('menus','id')
        self.FILTERS = self.lkm.script_id('filters','id')
        self.SCRIPT_INCIDENCIAS = self.lkm.script_id('incidencias','id')

        self.f.update({
            'duracion_rondin':'6639b47565d8e5c06fe97cf3',
            'duracion_traslado_area':'6760a9581e31b10a38a22f1f',
            'fecha_inspeccion_area':'6760a908a43b1b0e41abad6b',
            'fecha_inicio_rondin':'6760a8e68cef14ecd7f8b6fe',
            'status_user':'6639b2744bb44059fc59eb62',
            'nombre_recorrido':'6644fb97e14dcb705407e0ef',

            'option_checkin': '663bffc28d00553254f274e0',
            'image_checkin': '6855e761adab5d93274da7d7',
            'comment_checkout': '68798dd1205f333d8f53a1c7',
            'start_shift': '6879828d0234f02649cad390',
            'end_shift': '6879828d0234f02649cad391',
            'foto_end': '6879823d856f580aa0e05a3b',

            'dias_libres': '68bb20095035e61c5745de05',
            'nombre_horario': '68b6427cc8f94827ebfed695',
            'hora_entrada': '68b6427cc8f94827ebfed696',
            'hora_salida': '68b6427cc8f94827ebfed697',
            'tolerancia_retardo': '68b6427cc8f94827ebfed698',
            'retardo_maximo': '68b642e2bc17e2713cabe019',
            'grupo_turnos': '68b6427cc8f94827ebfed699',
            'horas_trabajadas': '68d6b0d5f7865907a86c37d7',
            'status_turn': '68d5bbb57691dec5a7640358',

            'tipo_guardia': '68acee270f2af5e173b7f92e',
            'nombre_guardia_suplente': '68acb67685a044b5fdd869b2',
            'estatus_guardia': '663bffc28d00553254f274e0',
            'foto_inicio_turno': '6855e761adab5d93274da7d7',
            'foto_cierre_turno': '6879823d856f580aa0e05a3b',
            'fecha_inicio_turno': '6879828d0234f02649cad390',
            'fecha_cierre_turno': '6879828d0234f02649cad391',
            'comentario_inicio_turno': '66a5b9bed0c44910177eb724',
            'comentario_cierre_turno': '68798dd1205f333d8f53a1c7',
            'nombre_horario': '68b6427cc8f94827ebfed695',
            'hora_entrada': '68b6427cc8f94827ebfed696',
            'hora_salida': '68b6427cc8f94827ebfed697',
            'dias_de_la_semana': '68b861ba34290efdd49ab24f',
            'tolerancia_retardo': '68b6427cc8f94827ebfed698',
            'retardo_maximo': '68b642e2bc17e2713cabe019',
            'grupo_ubicaciones_horario': '68b6427cc8f94827ebfed699',
            'dias_libres_empleado': '68bb20095035e61c5745de05',
            'duracion_estimada': '6854459836ea891d9d2be7d9',

            'grupo_comentarios_generales': '6927a0cdc03f0f8e5355437a',
            'grupo_comentarios_generales_fecha': '6927a0ea1c378cbd7f60a135',
            'grupo_comentarios_generales_texto': '6927a0ea1c378cbd7f60a136',
            'nombre_suplente': '6927a1176c60848998a157a2',
            'documento_check': '692a1b4e005c84ce5cd5167f',
            'datos_requeridos': '6769756fc728a0b63b8431ea',
            'envio_por': '6810180169eeaca9517baa5b',
            'configuracion_de_accesos': '696e6dda9517e760679e71eb',
            'tipo_de_notificacion': '699dfe3b82be0dbe0319d38c',
            'tipo_rondin': '69b9b98d2a02f4a0dd35f5c1'
        })

        self.ACCESOS_NOTAS = self.lkm.form_id('notas','id')
        self.CONFIGURACION_RECORRIDOS = self.lkm.catalog_id('configuracion_de_recorridos')
        self.CONFIGURACION_RECORRIDOS_ID = self.CONFIGURACION_RECORRIDOS.get('id')
        self.CONFIGURACION_RECORRIDOS_OBJ_ID = self.CONFIGURACION_RECORRIDOS.get('obj_id')
        self.REGISTRO_ASISTENCIA = self.lkm.form_id('registro_de_asistencia','id')
        self.FORMATO_VACACIONES = self.lkm.form_id('formato_vacaciones_aviso','id')
        self.USUARIOS_FORM = self.lkm.form_id('usuarios', 'id')
        self.ENVIO_DE_NOTIFICACIONES_FORM = self.lkm.form_id('envio_de_notificaciones', 'id')
        self.CONFIGURACION_DE_RECORRIDOS_FORM = self.lkm.form_id('configuracion_de_recorridos','id')
        self.CONF_MODULO_SEGURIDAD = self.lkm.form_id('configuracion_modulo_seguridad','id')
        self.BITACORA_TRANSPORTISTAS = self.lkm.form_id('bitacora_de_transportistas','id')
        # OJO: el slug real registrado en Linkaform es "configuracin..." (sin "ó") —
        # Linkaform le quitó el acento de forma imperfecta al generar el nombre técnico
        # a partir de "Configuración de Flujo de Transportistas". No "corregir" esto sin
        # antes confirmar el item_name real en LKFModules.
        self.CONFIGURACION_FLUJO_TRANSPORTISTAS = self.lkm.form_id('configuracin_de_flujo_de_transportistas','id')

        self.INSPECCION_ENTRADA_CTPAT_TRACTOR = self.lkm.form_id('inspeccion_de_entrada_ctpat_tractor_cabezal','id')
        self.INSPECCION_ENTRADA_CTPAT_REMOLQUE = self.lkm.form_id('inspeccion_de_entrada_ctpat_remolque','id')
        self.INSPECCION_ENTRADA_CTPAT_CONTENEDOR = self.lkm.form_id('inspeccion_de_entrada_ctpat_contenedor','id')
        self.INSPECCION_SELLO = self.lkm.form_id('inspeccion_de_sello','id')

        self.f.update({
            'areas_del_rondin': '66462aa5d4a4af2eea07e0d1',
            'comentario_area_rondin': '66462b9d7124d1540f962088',
            'comentario_check_area': '681144fb0d423e25b42818d4',
            'estatus_del_recorrido': '6639b2744bb44059fc59eb62',
            'fecha_hora_inspeccion_area': '6760a908a43b1b0e41abad6b',
            'fecha_programacion':'6760a8e68cef14ecd7f8b6fe',
            'fecha_hora_fin':'6760a8e68cef14ecd7f8b6ff',
            'foto_evidencia_area': '681144fb0d423e25b42818d2',
            'foto_evidencia_area_rondin': '66462b9d7124d1540f962087',
            'grupo_de_areas_recorrido': '6645052ef8bc829a5ccafaf5',
            'nombre_area':'663e5d44f5b8a7ce8211ed0f',
            'nombre_del_recorrido': '6645050d873fc2d733961eba',
            'nombre_del_recorrido_en_catalog': '6644fb97e14dcb705407e0ef',
            'ubicacion_recorrido': '663e5c57f5b8a7ce8211ed0b',
            'fecha_inicio_rondin': '6818ea068a7f3446f1bae3b3',
            'fecha_fin_rondin': '6760a8e68cef14ecd7f8b6ff',
            'check_status': '681fa6a8d916c74b691e174b',
            'grupo_incidencias_check': '681144fb0d423e25b42818d3',
            'incidente_open': '6811455664dc22ecae83f75b',
            'incidente_area': '663e5d44f5b8a7ce8211ed0f',
            'incidente_location': '663e5c57f5b8a7ce8211ed0b',
            'incidente_evidencia': '681145323d9b5fa2e16e35cd',
            'incidente_documento': '685063ba36910b2da9952697',
            'url_registro_rondin': '6750adb2936622aecd075607',
            'bitacora_rondin_incidencias': '686468a637d014b9e0ab5090',
            'personalizacion_pases': '695d2e1f6be562c3da95c4a7',
            'pases': '695d31b503ccc7766ac28507',
            'grupo_alertas': '695d35b618a37ea04899524f',
            'nombre_alerta': '695d36605f78faab793f497b',
            'accion_alerta': '695d36605f78faab793f497c',
            'llamar_num_alerta': '695d36605f78faab793f497d',
            'email_alerta': '695d36605f78faab793f497e',
            'free_day_start': '55887b7e01a4de2ea71c5ab4',
            'free_day_end': '55887b7e01a4de2ea71c5ab5',
            'free_day_type': '55887b7e01a4de2ea71c5ab2',
            'free_day_autorization': '55887b7e01a4de2ea71c5ab8',
            'grupo_incluir': '69974d3806cc6d6a17f8b1fa',
            'pases_incluir': '69974d55879296015c1cd8d2',
            'prefijo_telefonico':'6a221532db633d0cf4faf12f',
            'grupo_requisitos':"676975321df93a68a609f9ce",
        })

        self.envio_correo_fields.update({
            'phone_to': '699f302213e8f8740c465bfc',
            'tipo_de_notificacion': '699dfe3b82be0dbe0319d38c'
        })

        self.configuracion_area = {
            'area': '663e5d44f5b8a7ce8211ed0f',
            'create_area': '688a33d9e61fcd2c299ff39e',
            'comentarios': '68504a3fd3ebdc2e9b9869d2',
            'foto_area': '68487646684fe30a8f9f3ef4',
            'nombre_nueva_area': '688a33d9e61fcd2c299ff39f',
            'option': '68487646684fe30a8f9f3ef2',
            'status': '689a46342038ded0e949be07',
            'status_comment': '689a46342038ded0e949be08',
            'qr_area': '68487646684fe30a8f9f3ef3',
            'tag_id': '68487646684fe30a8f9f3ef3',
            'ubicacion': '663e5c57f5b8a7ce8211ed0b',
        }

        self.incidence_filter = {
            'reporta_incidencia': "",
            'fecha_hora_incidencia':"",
            'ubicacion_incidencia':"",
            'area_incidencia': "",
            'incidencia':"",
            'comentario_incidencia': "",
            'tipo_dano_incidencia': "",
            'dano_incidencia':"",
            'evidencia_incidencia': [],
            'documento_incidencia':[],
            'prioridad_incidencia':"",
            'notificacion_incidencia':"",
            'datos_deposito_incidencia': [],
            'tags':[],
            'categoria':"",
            'sub_categoria':"",
            'incidente':"",
            'nombre_completo_persona_extraviada':"",
            'edad':"",
            'color_piel':"",
            'color_cabello':"",
            'estatura_aproximada':"",
            'descripcion_fisica_vestimenta':"",
            'nombre_completo_responsable':"",
            'parentesco':"",
            'num_doc_identidad':"",
            'telefono':"",
            'info_coincide_con_videos':"",
            'responsable_que_entrega':"",
            'responsable_que_recibe':"",
            'afectacion_patrimonial_incidencia':[],
            'personas_involucradas_incidencia': [],
            'acciones_tomadas_incidencia':[],
            'seguimientos_incidencia':[],
            'valor_estimado':"",
            'pertenencias_sustraidas':"",
            'placas':"",
            'tipo':"",
            'marca':"",
            'modelo':"",
            'color':"",
        }

        self.check_area_filter = {
            "tag_id": "",
            "ubicacion": "",
            "area": "",
            "tipo_de_area": "",
            "foto_del_area": [],
            "evidencia_incidencia": [],
            "documento_incidencia": [],
            "incidencias": [],
            "comentario_check_area": "",
            "status_check_area": "",
        }

        self.f.update({
            'bitacora_rondin_url': '690cefdca2dff2f469da17e0',
            'cantidad_areas_inspeccionadas': '68a7b68a22ac030a67b7f8f8',
            'checked_at': '68a7b68a22ac030a67b7f8f8',
            'form_name':'5d810a982628de5556500d55',
            'form_id':'5d810a982628de5556500d56',
        })

        self.IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.heic'}

        self.pass_fields_transportista = {
            "tipo_de_operacion": "6a1ddb53f5a36ba1c7dd029c",

            "nombre_crea_el_pase": "6a20741046cc9cdddf3b3c07",
            "email_crea_el_pase": "6a20741046cc9cdddf3b3c08",
            "telefono_crea_el_pase": "6a20741046cc9cdddf3b3c09",

            "proveedor": "6a1ddb53f5a36ba1c7dd029d",
            "proveedor_email": "6a207762cd730fb838ce1bb1",
            "proveedor_telefono": "6a207762cd730fb838ce1bb2",

            "grupo_documentos_para_ocr": "6a2ae394b8e5ca8fd73705dc",
            "tipo_de_documento": "6a2ae3d8cf0be6f60c19f85d",
            "no_de_documento": "6a2ae3d8cf0be6f60c19f85e",
            "documento_para_ocr": "6a2ae3d8cf0be6f60c19f85f",

            "proveedor_cliente_material": "6a207762cd730fb838ce1bb4",
            "orden_de_compra": "6a1ddb53f5a36ba1c7dd02a0",
            "grupo_materiales": "6a2714954a54077ffa2394e6",
            "contenedor": "6a2714eeca6ac6897ef55d92",
            "sello":      "6a2714eeca6ac6897ef55d93",
            "tipo":       "6a2714eeca6ac6897ef55d94",
            "cantidad":   "6a2714eeca6ac6897ef55d95",
            "peso":       "6a2714eeca6ac6897ef55d96",
            "volumen":    "6a2714eeca6ac6897ef55d97",

            "direccion_de_recoleccion": "6a1ddb53f5a36ba1c7dd02a1",
            "fecha_pase_transportista_desde": "6a1ddcba20dadbb04a29b59f",
            "fecha_pase_transportista_hasta": "6a1f15aec19e655f79987c34",
            "hora_inicial": "6a1f15aec19e655f79987c36",
            "hora_final": "6a1f15aec19e655f79987c37",

            "lugar_de_recoleccion": "6a2079343d463b1222e5d794",
            "direccion_lugar_de_recoleccion": "6a2079343d463b1222e5d795",
            "fecha_de_recoleccion": "6a2079343d463b1222e5d796",
            "hora_inicial_recoleccion": "6a2079343d463b1222e5d797",
            "hora_final_recoleccion": "6a2079343d463b1222e5d798",
            "anden_recoleccion": "6a2079343d463b1222e5d799",
            "responsable": "6a2079343d463b1222e5d79a",
            "responsable_email": "6a2079343d463b1222e5d79b",
            "responsable_telefono": "6a2079343d463b1222e5d79c",
            "metodo_de_embarque": "6a2079343d463b1222e5d79d",
            "incoterm": "6a2079343d463b1222e5d79e",

            "url_del_pase_transportista": "6a20d4a39ebbf58470fe73b5",
            "qr_del_pase_transportista": "6a20a8e138dff4ad8155c325",
            "estado_transportista": "6a20bb99782fe54a2681fc56",
            "token_transportista": "6a20c1811b6edd566116f483",

            "conductor_foto_licencia": "6a2add8342320b4d1b66db84",
            "conductor_nombre": "6a2adc08877c6087f9c2326b",
            "conductor_no_licencia": "6a2adc08877c6087f9c2326c",
            "conductor_lugar_expedicion": "6a2adc08877c6087f9c2326d",
            "conductor_vigencia": "6a2adc08877c6087f9c2326e",
            "ayudante_foto_licencia": "6a2add8342320b4d1b66db85",
            "ayudante_nombre": "6a2adc08877c6087f9c2326f",
            "ayudante_no_licencia": "6a2adc08877c6087f9c23270",
            "ayudante_lugar_expedicion": "6a2adc08877c6087f9c23271",
            "ayudante_vigencia": "6a2adc08877c6087f9c23272",
            "vehiculo_tarjeta_circulacion": "6a2add8342320b4d1b66db86",
            "vehiculo_linea": "6a2add8342320b4d1b66db87",
            "vehiculo_tipo_unidad": "6a2add8342320b4d1b66db88",
            "vehiculo_marca": "6a2add8342320b4d1b66db89",
            "vehiculo_modelo": "6a2add8342320b4d1b66db8a",
            "vehiculo_year": "6a2add8342320b4d1b66db8b",
            "vehiculo_placas": "6a2add8342320b4d1b66db8c",
            "vehiculo_no_economico": "6a2add8342320b4d1b66db8d",
            "vehiculo_niv": "6a2add8342320b4d1b66db8e",
            "foto_contenedores": "6a2b045ed8034654f212c1bc",
            "grupo_contenedores": "6a2add8342320b4d1b66db8f",
            "contenedor_numero": "6a2addcfcee6b93e39ab8a51",
            "contenedor_sello": "6a2addcfcee6b93e39ab8a52",
            "contenedor_tipo": "6a2addcfcee6b93e39ab8a53",
        }

        self.bitacora_transportista_fields = {
            'estatus': '6a31921f07fb9cb5840d1f22',
            'fecha_hora_ingreso': '6a3bee0a7829a4ca9572d39e',
            'fecha_hora_descarga': '6a3bee0a7829a4ca9572d39f',
            'fecha_hora_terminado': '6a710409eaef5abc8b1a1a69',

            'grupo_fotos_y_documentos': '6a3bee0a7829a4ca9572d3a0',
            'tipo_de_documento': '6a3bee394a7a0748a6fc9a56',
            'documento': '6a3bee394a7a0748a6fc9a57',

            'num_de_pase': '6a31921f07fb9cb5840d1f23',
            'empresa_transportista': '6a31929d0bf8c5fc715d7424',
            'tipo_de_operacion': '6a31929d0bf8c5fc715d7425',
            'procedencia': '6a3193dccf1326ad4b7a9a52',
            'tipo_de_vehiculo': '6a3193dccf1326ad4b7a9a53',
            'placas_de_vehiculo': '6a31921f07fb9cb5840d1f24',
            'placas_de_vehiculo_tarjeta_circulacion': '6a5018081d7498e16bbb4b75',
            'marca_vehiculo': '6a4415c7b7ce8af39efb3aa8',
            'year_vehiculo': '6a4415c7b7ce8af39efb3aa9',
            'color_vehiculo': '6a4415c7b7ce8af39efb3aaa',
            'num_eco_num_rotulo': '6a3193dccf1326ad4b7a9a56',
            'conductor': '6a3193dccf1326ad4b7a9a57',
            'ayudante': '6a42cd6385b4d5aa41c2a922',
            'num_licencia': '6a3193dccf1326ad4b7a9a58',
            'vigencia_licencia': '6a42e2eab55463ad9f31abf3',
            'rfc_conductor': '6a42e5143f8adeaa55ef9a4a',
            'firma_conductor': '6a3193dccf1326ad4b7a9a5b',
            'anden_asignado': '6a31929d0bf8c5fc715d7427',

            'proveedor_cliente': '6a42dfd48e70db919887e4b0',
            'orden_de_compra': '6a42dfd48e70db919887e4b1',

            'grupo_materiales': '6a42c5e02196461994770602',
            'lugar_material': '6a42c7a7a1555d53d6b9194c', # Opciones: vehiculo, remolque, contenedor
            'no_referencia_material': '6a42c7a7a1555d53d6b9194d',
            'producto_material': '6a44091a4e3983d839de22ee',
            'lote_material': '6a4409523a38bb598a0a18a0',
            'cantidad_material': '6a42c7a7a1555d53d6b91950',
            'cantidad_fisica_material': '6a454fb37ddcb3993dd90107',
            'cantidad_buena_material': '6a6ac379fab960f8931dcc77',
            'cantidad_danada_material': '6a6ac35a71f64d908af42f69',
            'cantidad_faltante_material': '6a7a4ee0e6092a8d37f6d448',
            'peso_material': '6a42c7a7a1555d53d6b91951',
            'volumen_material': '6a42c7a7a1555d53d6b91952',

            'grupo_remolques': '6a31959ed11ece87f2b0052d',
            'tipo_remolque': '6a319693884bec802c94fa44',
            'no_referencia_remolque': '6a443aa0f4bede456259a441',
            'num_sello': '6a319693884bec802c94fa45',
            'num_caja_contenedor': '6a319693884bec802c94fa46',
            'placas_de_caja': '6a319693884bec802c94fa47',
            'color_remolque_contenedor': '6a440b059581538d55b3565e',
            'comentarios': '6a319693884bec802c94fa48',

            'grupo_sellos': '6a42c65c03f125df7ad28601',

            'grupo_desglose_empaque': '6a6a4abe639ed7cad54be377',
            'no_referencia_material_desglose': '6a6a4adc169fc82c5fae8668',
            'nivel_desglose': '6a6a4b64c6fd2eaaf5f8c0b6',
            'tipo_unidad_empaque_desglose': '6a6a4b64c6fd2eaaf5f8c0b7',
            'cantidad_desglose': '6a6a4b64c6fd2eaaf5f8c0b8',
            'cantidad_acumulada_desglose': '6a6a4b64c6fd2eaaf5f8c0b9',

            'grupo_inspecciones': '6a42a7068dcfbf362329a972',
            'tipo_inspeccion': '6a42c80b03f125df7ad2862b',
            'url_inspeccion': '6a42a71aec3f7153a3d2aea3',
        }

        self.conf_flujo_transportistas_fields = {
            'etapas_activas': '6a75056924f23eef843cd01b',
            'configuracion_de_inspecciones': '6a7509cd6e87e5935b853b7b',
            'tipo_de_inspeccion': '6a750a1afd4ed68d7c57c24d',
            'norma': '6a7e2c5c23fb366f1918dea8',
            'subtipo': '6a7e2c5c23fb366f1918dea9',
        }

        self.inspeccion_entrada_tractor_fields = {
            'fotos_y_documentos': '6a5fcf869160bd10e1b0b323',
            'tipo_de_documento': '6a5fe2b0a5af7dac33061ea9',
            'documento': '6a5fe2b0a5af7dac33061eaa',

            'defensa': '20e7950eaac0054dbb8ca133',  # 1. Defensa (Si/No/N.A)
            'defensa_comentarios': '7aa52ec9ded1f199a3bfa307',
            'defensa_evidencia': '529623abe2be9e64816dec78',

            'motor_caja_de_la_bateria_caja_y_filtros_de_aire': '2aa45df8132536520b2a2bdd',  # 2. Motor, caja de la bateria, caja y filtros de aire (Si/No/N.A)
            'motor_caja_de_la_bateria_caja_y_filtros_de_aire_comentarios': '4604526acf0bf06c658add75',
            'motor_caja_de_la_bateria_caja_y_filtros_de_aire_evidencia': '8f12a402e6094434d6028246',

            'llantas_y_rines_tractor_y_remolque': '4b58a0007c1730a1ff9cc56f',  # 3. Llantas y rines (tractor y remolque) (Si/No/N.A)
            'llantas_y_rines_tractor_y_remolque_comentarios': '8e2645d9b0117869c0b93bc1',
            'llantas_y_rines_tractor_y_remolque_evidencia': 'a9be932860ceeb9face9b24d',

            'piso_tractor': 'acba826a28a8d1d48b743b53',  # 4. Piso (tractor) (Si/No/N.A)
            'piso_tractor_comentarios': '5e5cc9112d6c74a8c0d96c6b',
            'piso_tractor_evidencia': '5e0e635e8e5e7788793dc632',

            'tanque_de_combustible': '72e1fe8cf4fad9736fbb141c',  # 5. Tanque de combustible (Si/No/N.A)
            'tanque_de_combustible_comentarios': 'ddd7b180bcb8a98c556c67ef',
            'tanque_de_combustible_evidencia': 'cef55b76f55eed057cf64cad',

            'cabina_dormitorio_puertas_y_compartimientos_de_herramientas_seccion_de_pasajero_y_techo': '83ceff5fda79787b48219268',  # 6. Cabina, dormitorio, puertas y compartimientos de herramientas, seccion de pasajero y techo (Si/No/N.A)
            'cabina_dormitorio_puertas_y_compartimientos_de_herramientas_seccion_de_pasajero_y_techo_comentarios': '700d1c62d264a6c3039f65c1',
            'cabina_dormitorio_puertas_y_compartimientos_de_herramientas_seccion_de_pasajero_y_techo_evidencia': '6cb1dd20ae67dff1e20b08bd',

            'tanque_de_aire': 'ac82529cb6081ee6327ee04f',  # 7. Tanque de aire (Si/No/N.A)
            'tanque_de_aire_comentarios': '9cdc267b92fe4c144de7c370',
            'tanque_de_aire_evidencia': 'e01e5ac0be30514b35bd3d13',

            'ejes_de_transmision': 'bcb4e55eddda4821b9db0304',  # 8. Ejes de transmision (Si/No/N.A)
            'ejes_de_transmision_comentarios': '8e5bc150c3791c9917314b92',
            'ejes_de_transmision_evidencia': '5b72adefa1c7c716e0f24941',

            'quinta_rueda': '3ad0cca2f6449042ad664cfd',  # 9. Quinta rueda (Si/No/N.A)
            'quinta_rueda_comentarios': 'cedf4d6e6f7120c152d9c0fb',
            'quinta_rueda_evidencia': '35ccd51789e6260465d17ea7',

            'chasis': 'd08cc0f655036b4fb2a09056',  # 10. Chasis (Si/No/N.A)
            'chasis_comentarios': 'db0dd2a781343effa2a7153d',
            'chasis_evidencia': 'e957e4cb96e1ef8f999a5938',

            'puertas_externa': '5c100788b4211b8122e4395c',  # 11. Puertas externa (Si/No/N.A)
            'puertas_externa_comentarios': '87fffff1f65ef97ddc4d23bf',
            'puertas_externa_evidencia': '666ce737007a5ccc57c9f369',

            'piso_externo_trailer_contenedor_caja': 'f87fd7be1133ee21cc723f7c',  # 12. Piso externo (trailer, contenedor, caja) (Si/No/N.A)
            'piso_externo_trailer_contenedor_caja_comentarios': 'de6dffa1def019fe589a329a',
            'piso_externo_trailer_contenedor_caja_evidencia': 'e7c54e4187ee035e6bb3be7b',

            'paredes_externa': 'fc63e8996ccf5c91a80c0e2f',  # 13. Paredes externa (Si/No/N.A)
            'paredes_externa_comentarios': '531d51796e724cc7f14cb496',
            'paredes_externa_evidencia': 'b2d3aaf29aa9374130881632',

            'pared_frontal_externa': '731b4abf0672038c57d8d516',  # 14. Pared frontal externa (Si/No/N.A)
            'pared_frontal_externa_comentarios': '1f3c15fb61a4a143f773809d',
            'pared_frontal_externa_evidencia': '56d9b00ce47ae297a64aa90b',

            'techo_externo': '8b18d4aa1d62615cacf2776f',  # 15. Techo externo (Si/No/N.A)
            'techo_externo_comentarios': '85df5aa6a444e9490f14ce86',
            'techo_externo_evidencia': '5b82b568466ceebc18d49dd3',

            'unidad_de_refrigeracion': '8b4e8a6dec2392c9f267e179',  # 16. Unidad de refrigeracion (Si/No/N.A)
            'unidad_de_refrigeracion_comentarios': '747090a5b505163130df82e4',
            'unidad_de_refrigeracion_evidencia': '5544eaaccb74e9d09b7e2f77',

            'escape_mofles': '48de45705387f226f6551c1b',  # 17. Escape / Mofles (Si/No/N.A)
            'escape_mofles_comentarios': '0307abb04ee4f8b3786cca23',
            'escape_mofles_evidencia': '32f0559232cbc31f5cc6a472',
        }

        self.inspeccion_entrada_ctpat_contenedor_fields = {
            'fotos_y_documentos': '6a5fde6455cec5f5e85ea2a0',
            'tipo_de_documento': '6a5fe2b0a5af7dac33061ea9',
            'documento': '6a5fe2b0a5af7dac33061eaa',

            'altura_interior': 'd412fb9f428dfc231c9bc3f0',  # Altura interior (text)
            'ancho_interior': '6477c73222d9b7e8dd1de3b9',  # Ancho interior (text)
            'longitud_interior': 'd7c19cbd2cfe6b19f848d697',  # Longitud interior (text)
            'exterior_parte_inferior_del_contenedor_bastidor_o_chasis': '4a819aa25c6e76080f76317a',  # Exterior / parte inferior del contenedor (bastidor o chasis) (checkbox: Todos/Suciedad/Plagas/Fauna)
            'puertas_interiores_exteriores': 'b4f2b497790d8fa30739ab05',  # Puertas interiores / exteriores (checkbox: Todos/Suciedad/Plagas/Fauna)
            'pared_interior_lado_derecho': 'c334bc2360c643779bdcd495',  # Pared interior lado derecho (checkbox: Todos/Suciedad/Plagas/Fauna)
            'pared_interior_lado_izquierdo': '4c90dcc67f8e9f029878502c',  # Pared interior lado izquierdo (checkbox: Todos/Suciedad/Plagas/Fauna)
            'pared_interior_frontal': '14aea746aadf15c99edb8592',  # Pared interior frontal (checkbox: Todos/Suciedad/Plagas/Fauna)
            'techo_cubierta_superior': 'bc75ab3fdb2258286b0b41c0',  # Techo / cubierta superior (checkbox: Todos/Suciedad/Plagas/Fauna)
            'piso_interior': '371a7d9c3ae8a40a32b3762a',  # Piso (interior) (checkbox: Todos/Suciedad/Plagas/Fauna)
        }

        self.inspeccion_entrada_ctpat_remolque_fields = {
            'fotos_y_documentos': '6a5fde3b04fdbbdbcfdfc2a2',
            'tipo_de_documento': '6a5fe2b0a5af7dac33061ea9',
            'documento': '6a5fe2b0a5af7dac33061eaa',

            'altura_interior': '6703c4acd45242ffb0eb0839',  # Altura interior (text)
            'ancho_interior': '7bfa6fe868c1cbec93a051e5',  # Ancho interior (text)
            'longitud_interior': '2624dc82316e99315084d385',  # Longitud interior (text)

            'tanque_de_aire': 'd1fae4d0b2ec9569fbcf8770',  # 1. Tanque de aire (Si/No)
            'tanque_de_aire_comentarios': 'd2bacb536ead1a15f56bbe6c',
            'tanque_de_aire_evidencia': '28538bb0340a0eccc15e150b',

            'ejes_de_transmision': 'd57c0e9a92f8b3b552f2b66a',  # 2. Ejes de transmision (Si/No)
            'ejes_de_transmision_comentarios': '9f6a0733c5c36bcc4e6051de',
            'ejes_de_transmision_evidencia': '089e40849794b1edbe667291',

            'quinta_rueda': 'aeed49c20dd20d18904ac28f',  # 3. Quinta rueda (Si/No)
            'quinta_rueda_comentarios': '481f00fd61a55c0b9aef99e4',
            'quinta_rueda_evidencia': 'c86cf900756ed0667122d999',

            'chasis': '9a6743b2e92e16e2b727e667',  # 4. Chasis (Si/No)
            'chasis_comentarios': '6aa6dabeb1430c92bf9c36a9',
            'chasis_evidencia': 'c420045f52f188fcbd616165',

            'puertas_externa': 'b0dca85ed86edd92560f634c',  # 5. Puertas externa (Si/No)
            'puertas_externa_comentarios': '3b85b7104be1df0dbe8762e7',
            'puertas_externa_evidencia': '608def717f6c6f14e1f8ab6e',

            'piso_externo_trailer_contenedor_caja': '2cb78278523b502800a47e2e',  # 6. Piso externo (trailer, contenedor, caja) (Si/No)
            'piso_externo_trailer_contenedor_caja_comentarios': '7bc7a9a7a58d45946c2e70a6',
            'piso_externo_trailer_contenedor_caja_evidencia': 'c16b8d4dfc22709c7785cc63',

            'paredes_externa': '198cf876dc13d7bd658a4cbd',  # 7. Paredes externa (Si/No)
            'paredes_externa_comentarios': '8a9af06c2c1045f46dfa44d2',
            'paredes_externa_evidencia': '8af47b03f950e87661b5835b',

            'pared_frontal_externa': '36b4b172e38a3dc1b8b226d1',  # 8. Pared frontal externa (Si/No)
            'pared_frontal_externa_comentarios': 'bb279c901f91c114d1220452',
            'pared_frontal_externa_evidencia': 'ddff798b400d03d48b9ef808',

            'techo_externo': 'bbc21e44dec3040d81e005f2',  # 9. Techo externo (Si/No)
            'techo_externo_comentarios': 'e2e3ae0dbf920b1c44502fbb',
            'techo_externo_evidencia': '59bf2262a664e2b16ba1a299',

            'unidad_de_refrigeracion': 'cbb1c127c08011c3d7d4c344',  # 10. Unidad de refrigeracion (Si/No)
            'unidad_de_refrigeracion_comentarios': '80ad083a0f6319e6fd63d681',
            'unidad_de_refrigeracion_evidencia': 'd0240215edecf39a02c5a891',

            'escape_mofles': '545c0b134ab1d2f11cef90a9',  # 11. Escape / Mofles (Si/No)
            'escape_mofles_comentarios': '736b1fe2e2609d47beef2a03',
            'escape_mofles_evidencia': 'b7618c209a113ef54ec2b58b',
        }

        self.inspeccion_de_sello_fields = {
            'numero_de_sello_fisico': 'ad57d9e43537244dc2f66280',  # Numero de sello fisico (text)
            'numero_de_sello_esperado_revisado': '22e2974e099b937e4c9c7094',  # Numero de sello esperado (revisado) (text)
            'tipo_de_sello_clasificacion_iso_17712': '1e534c51db80d867b1922c86',  # Tipo de sello (clasificacion ISO 17712) (radio: Indicative/Security/High Security)
            'matriz_vttt_marca_cada_accion_verificada': '92ab37dbe06381e6100f88f0',  # Matriz VTTT - Marca cada accion verificada (checkbox: View/Verify/Tug/Twist)
            '1_foto_del_sello': '1defc3e446a9ebd00c649dbc',  # 1. Foto del sello (images)
            '2_sello_colocado_en_las_puertas': '26f5f07d55f304e9015ae64d',  # 2. Sello colocado en las puertas (images)
            '3_puertas_completas_del_remolque': 'be928c48d8a6353077ec5eba',  # 3. Puertas completas del remolque (images)
            '4_placas_o_economico': 'd7479071e6aabdeaa10ce41b',  # 4. Placas o economico (images)
            '5_identificacion_del_operador': '718a0a37c5a6965b2127d2c0',  # 5. Identificacion del operador (images)
            'comentarios': '0e009f7829544463cbf89e1e',  # Comentarios (textarea)
        }
