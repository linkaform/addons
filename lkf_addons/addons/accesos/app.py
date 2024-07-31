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

import simplejson
from bson import ObjectId
from datetime import datetime
from copy import deepcopy

from linkaform_api import base
from lkf_addons.addons.employee.app import Employee
from lkf_addons.addons.location.location_util import Location

### Objeto o Clase de Modulo ###
'''
Cada modulo puede tener N objetos, configurados en clases.
Estos objetos deben de heredar de base.LKF_Base) y cualquier modulo dependiente.
Al hacer el super() del __init__(), heredamos las variables de configuracion de clase.

Se pueden heredar funciones de cualquier clase heredada con el metodo super(). 
'''
class Accesos(Employee, Location, base.LKF_Base):

    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False):
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api)
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
        self.ACCESOS_NOTAS = self.lkm.form_id('notas','id')
        self.CHECKIN_CASETAS = self.lkm.form_id('checkin_checkout_casetas','id')
        self.CONCESSIONED_ARTICULOS = self.lkm.form_id('concesion_de_activos_unico','id')
        self.PASE_ENTRADA = self.lkm.form_id('pase_de_entrada','id')
        self.VISITA_AUTORIZADA = self.lkm.form_id('visita_autorizada','id')
        self.BITACORA_ACCESOS = self.lkm.form_id('bitacora_de_entradas_y_salidas','id')
        self.BITACORA_ARTICULOS_PERDIDOS = self.lkm.form_id('bitacora_articulos_perdidos','id')
        self.BITACORA_FALLAS = self.lkm.form_id('bitacora_de_fallas','id')
        self.BITACORA_INCIDENCIAS = self.lkm.form_id('bitacora_de_incidencias','id')
        self.BITACORA_GAFETES_LOCKERS = self.lkm.form_id('bitacora_de_gafetes_y_lockers','id')
        self.PUESTOS_GUARDIAS = self.lkm.form_id('puestos_de_guardias','id')

        
        self.last_check_in = []
        # self.FORM_ALTA_COLABORADORES = self.lkm.form_id('alta_de_colaboradores_visitantes','id')
        # self.FORM_ALTA_EQUIPOS = self.lkm.form_id('alta_de_equipos','id')
        # self.FORM_ALTA_VEHICULOS = self.lkm.form_id('alta_de_vehiculos','id')
        # #self.FORM_BITACORA = self.lkm.form_id('bitacora','id')
        # self.FORM_LOCKER = self.lkm.form_id('locker','id')
        #self.FORM_PASE_DE_ENTRADA = self.lkm.form_id('pase_de_entrada','id')
        #self.FORM_REGISTRO_PERMISOS = self.lkm.form_id('registro_de_permisos','id')

        # catalogos
        '''
        self.CATALOG_NAME = self.lkm.catalog_id('catalog_name',id)
        aqui deberas guardar el los ID de los catalogos. 
        Para ello ocupas llamar el metodo lkm.catalog_id del objeto lkm(linkaform modules, por sus siglas, 
        en lkm estan todas las funcions generales de modulos).

        '''
        self.VISITA_AUTORIZADA_CAT = self.lkm.catalog_id('visita_autorizada')
        self.VISITA_AUTORIZADA_CAT_ID = self.VISITA_AUTORIZADA_CAT.get('id')
        self.VISITA_AUTORIZADA_CAT_OBJ_ID = self.VISITA_AUTORIZADA_CAT.get('obj_id')
        self.PASE_ENTRADA_CAT = self.lkm.catalog_id('pase_de_entrada')
        self.PASE_ENTRADA_ID = self.PASE_ENTRADA_CAT.get('id')
        self.PASE_ENTRADA_OBJ_ID = self.PASE_ENTRADA_CAT.get('obj_id')

        self.CONFIG_PERFILES = self.lkm.catalog_id('configuracion_de_perfiles')
        self.CONFIG_PERFILES_ID = self.CONFIG_PERFILES.get('id')
        self.CONFIG_PERFILES_OBJ_ID = self.CONFIG_PERFILES.get('obj_id')
        # self.CONF_PERFIL = self.lkm.catalog_id('configuracion_de_perfiles','id')
        # self.CONF_PERFIL_ID = self.CONF_PERFIL.get('id')
        # self.CONF_PERFIL_OBJ_ID = self.CONF_PERFIL.get('obj_id')


        # self.AREAS_DE_LAS_UBICACIONES_CAT = self.lkm.catalog_id('areas_de_las_ubicaciones')
        # self.AREAS_DE_LAS_UBICACIONES_CAT_ID = self.AREAS_DE_LAS_UBICACIONES_CAT.get('id')
        # self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID = self.AREAS_DE_LAS_UBICACIONES_CAT.get('obj_id')
        #----Dic Fields Forms

        ## Module Fields ##
        ''' self.mf : Estos son los campos que deseas mantener solo dentro de este modulo '''
        mf = {
            'bitacora_salida':'662c51eb194f1cb7a91e5af0',
            'bitacora_entrada':'662c51eb194f1cb7a91e5aef',
            'catalog_caseta':'66566d60d4619218b880cf04',
            'catalog_caseta_salida':'66566d60464fe63529d1c543',
            'catalog_estado':'664fc5b3276795e17ea76dbd',
            'catalog_guard':'664fc645276795e17ea76dc4',
            'catalog_guard_close':'664fc64242c59486fadd0a27',
            'catalog_pase':'664fc6f0c9f60bd52034b5b1',
            'catalog_tipo_pase':'664fc6e81d1a1fcda334b587',
            'catalog_ubicacion':'664fc5d9860deae4c20954e2',
            'catalog_vehiculo':'664fc6748afb6c746d34b6bf',
            'catalog_visita':'664fc6f5d6078682a4dd0ab3',
            'caseta':'663e5d44f5b8a7ce8211ed0f',
            'caseta_salida':'663fb45992f2c5afcfe97ca8',
            'color_vehiculo': "663e4691f54d395ed7f27465",
            'color_articulo': "663e4730724f688b3059eb3b",
            'config_dia_de_acceso': "662c304fad7432d296d92584",
            'config_limitar_acceso': "6635380dc9b3e7db4d59eb49",
            'config_dias_acceso': "662c304fad7432d296d92585",
            'codigo_qr':'6685da34f065523d8d09052b',
            'curp': "5ea0897550b8dfe1f4d83a9f",
            'documento': "663e5470424ad55e32832eec",
            'direccion': "663a7e0fe48382c5b1230902",
            'duracion': "65cbe03c6c78b071a59f481e",
            'email_vsita': "5ea069562f8250acf7d83aca",
            'empresa':'64ecc95271803179d68ee081',
            'fecha_desde_visita': "662c304fad7432d296d92582",
            'fecha_entrada': "662c51eb194f1cb7a91e5aef",
            'fecha_hasta_visita': "662c304fad7432d296d92583",
            'field_note':'6647fadc96f80017ac388648',
            'foto':'5ea35de83ab7dad56c66e045',
            'gafete':'663e530af52d352956832f72',
            'guard_group':'663fae53fa005c70de59eb95',
            'grupo_visitados': "663d4ba61b14fab90559ebb0",
            'identificacion':'65ce34985fa9df3dbf9dd2d0',
            'marca_vehiculo':'65f22098d1dc5e0b9529e89b',
            'marca_articulo':'663e4730724f688b3059eb3a',
            'modelo_vehiculo':'65f22098d1dc5e0b9529e89c',
            'nota': "6647fadc96f80017ac388647",
            'nombre_articulo': "663e4730724f688b3059eb39",
            'nombre_estado': "663a7dd6e48382c5b12308ff",
            'nombre_guardia': "62c5ff407febce07043024dd",
            'nombre_visita': "5ea0693a0c12d5a8e43d37df",
            'nombre_perfil': "661dc67e901906b7e9b73bac",
            'nombre_guardia_apoyo': "663bd36eb19b7fb7d9e97ccb",
            'numero_serie': "66426453f076652427832fd2",
            'placas_vehiculo':'663e4691f54d395ed7f27464',
            'rfc':"64ecc95271803179d68ee081",
            'status_visita':'5ea1bd280ae8bad095055e61',
            'telefono':'661ea59c15baf5666f32360e',
            'tipo_de_guardia': "6684484fa5fd62946c12e006",
            'tipo_equipo': "663e4730724f688b3059eb38",
            'tipo_registro': "66358a5e50e5c61267832f90",
            'tipo_vehiculo': "65f22098d1dc5e0b9529e89a",
            'tipo_visita_pase': "662c304fad7432d296d92581",
            'ubicacion': "663e5c57f5b8a7ce8211ed0b",
            'status_area':"663e5e4bf5b8a7ce8211ed14",
        }
        self.mf = mf
        ## Form Fields ##
        '''
        self.form_name : En esta seccion podras agrupar todos los campos ya sea por forma o como dease
        enviarls hacia tus servicios, en el caso de las busquedas de mongo, pudes hacer las busquedas de
        Manera Anidada Por lo cual podras agrupar separadas por punto, ej.663d4ba61b14fab90559ebb0.665f482cc9a2f8acf685c20b
        y asi podras hacer la busquedas directo en la base de datos.

        Estos campos podras agregarlos asi directo a self.f , donde se agurpan todos los fields de los modulos heredados

        '''
        #- Para salida de bitacora  de articulos perdidos y lista
        self.perdidos_fields = {
            'status_perdido':'6639ae65356a6efb4de97d28',
            'date_hallazgo_perdido':'6639ae65356a6efb4de97d29',
            'ubicacion_perdido':f"{self.mf['catalog_caseta']}.{self.mf['ubicacion']}",
            'area_perdido':f"{self.mf['catalog_caseta']}.{self.mf['caseta']}",
            'articulo_perdido':'6639aeeb97b12e6f4ccb9711',
            'photo_perdido':'6639aeeb97b12e6f4ccb9712',
            'comments_perdido':'6639affa5a9f58f5b5cb9706',
            'guard_perdido':f"{self.mf['catalog_guard']}.{self.mf['nombre_guardia']}",
            'recibe_perdido':'6639affa5a9f58f5b5cb9707',
            'phone_recibe_perdido':'664415ce630b1fb22b07e159',
            'identification_perdido':'664415ce630b1fb22b07e15a',
            'date_entrega_perdido':'6639affa5a9f58f5b5cb9708',
        }
        #- Para salida de bitacora y lista
        self.bitacora_fields = {
            'nombre_visita':f"{self.mf['catalog_visita']}.{self.mf['nombre_visita']}",
            'perfil_visita':f"{self.mf['catalog_visita']}.{self.mf['nombre_perfil']}",
            'status_visita':f"{self.mf['tipo_registro']}",
            'ubicacion':f"{self.mf['catalog_ubicacion']}.{self.mf['ubicacion']}",
            'caseta_entrada':f"{self.mf['catalog_caseta']}.{self.mf['caseta']}",
            'gafete':f"{self.mf['gafete']}",
            'codigo_qr':f"{self.mf['codigo_qr']}",
            'documento':f"{self.mf['documento']}",
            'caseta_salida':f"{self.mf['catalog_caseta_salida']}.{self.mf['caseta_salida']}",
            'bitacora_salida':f"{self.mf['bitacora_salida']}",
            'bitacora_entrada':f"{self.mf['bitacora_entrada']}",
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
            'caseta_concesion':f"{self.mf['catalog_caseta_salida']}.{self.mf['caseta_salida']}",
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
            'falla_status': '66397e2c59c2600b1df2742c',
            'falla_fecha': '66397d0cfd99d7263f833032',
            'falla_ubicacion':f"{self.mf['catalog_ubicacion']}.{self.mf['ubicacion']}",
            'falla_caseta':f"{self.mf['catalog_caseta']}.{self.mf['caseta']}",
            'falla_catalog':'664fc6c08d4dfb34de095584',
            'falla':'66397bae9e8b08289a59ec86',
            'falla_comments':'66397d8cfd99d7263f83303a',
            'falla_guard':f"{self.mf['catalog_guard']}.{self.mf['nombre_guardia']}",
            'falla_guard_solution':f"{self.mf['catalog_guard_close']}.{self.mf['nombre_guardia_apoyo']}",
            'falla_fecha_solucion':'663998f8df1f40254af27430',

        }
        #- Para creación , edición y lista de incidencias
        self.incidence_fields = {
            'date_incidence':'66396efeb37283c921e97cdf',
            'catalog_incidence':'664fc6c7276795e17ea76dc9',
            'incidence':'663973809fa65cafa759eb97',
            'comments_incidence':'66397586aa8bbc0371e97c80',
        }
        #- Para creación , edición y lista de gafetes y lockers
        self.gafetes_fields = {
            'status_gafete':'663961d5390b9ec511e97ca5',
            'ubicacion_gafete':f"{self.mf['catalog_ubicacion']}.{self.mf['ubicacion']}",
            'caseta_gafete':f"{self.mf['catalog_caseta']}.{self.mf['caseta']}",
            'visita_gafete':f"{self.mf['catalog_visita']}.{self.mf['nombre_visita']}",
            'catalog_gafete':'664fc6ec8d4dfb34de095586',
            'id_gafete':'664803e6d79bc1dfd33885e1',
            'documento_gafete':'65e0b6f7a07a72e587124dc6',
        }
        #- Para creación , edición y lista de notas
        self.notes_fields = {
            'note_status':'6647f9eb6eefdb1840684dc1',
            'note_open_date':'6647fadc96f80017ac388646',
            'note_close_date':'6647fadc96f80017ac38864a',
            'note_catalog_booth':f"{self.mf['catalog_caseta']}",
            'note_booth':f"{self.mf['caseta']}",
            'note_catalog_guard':f"{self.mf['catalog_guard']}",
            'note_guard':f"{self.mf['nombre_guardia']}",
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
            'visitante_pase':'662c262cace163ca3ed3bb3a',
            'ubicacion_pase':f"{self.mf['catalog_ubicacion']}.{self.mf['ubicacion']}",
            'direccion_pase':f"{self.mf['catalog_ubicacion']}.{self.mf['direccion']}",
            'nombre_catalog_pase':f"{self.mf['catalog_pase']}.{self.mf['nombre_visita']}",
            'email_catalog_pase':f"{self.mf['catalog_pase']}.{self.mf['email_vsita']}",
            'curp_catalog_pase':f"{self.mf['catalog_pase']}.{self.mf['curp']}",
            'telefono_catalog_pase':f"{self.mf['catalog_pase']}.{self.mf['telefono']}",
            'foto_pase':f"{self.mf['catalog_pase']}.{self.mf['foto']}",
            'identificacion_pase':f"{self.mf['catalog_pase']}.{self.mf['identificacion']}",
            'empresa_pase':f"{self.mf['catalog_pase']}.{self.mf['empresa']}",
            'status_visita_pase':f"{self.mf['catalog_pase']}.{self.mf['status_visita']}",
            'nombre_pase':'662c2937108836dec6d92580',
            'email_pase':'662c2937108836dec6d92581',
            'telefono_pase':'662c2937108836dec6d92582',
            'empresa_pase':'66357d5e4f00f9018ce97ce9',
            'perfil_pase':f"{self.mf['catalog_tipo_pase']}.661dc67e901906b7e9b73bac",
            'certificacion_pase':f"{self.mf['catalog_tipo_pase']}.662962bb203407ab90c886e4",
            'requerimientos_pase':f"{self.mf['catalog_tipo_pase']}.662962bb203407ab90c886e5",
            'vigencia_pase':f"{self.mf['catalog_tipo_pase']}.'662962bb203407ab90c886e6",
            'vigencia_expresa_pase':f"{self.mf['catalog_tipo_pase']}.662962bb203407ab90c886e7",
            'nombre_tipo_pase':f"{self.mf['catalog_tipo_pase']}.66297e1579900d9018c886ad",
            'visita_a_pase':'663d4ba61b14fab90559ebb0',
            'visita_de_pase':'662c304fad7432d296d92581',
            'fecha_desde_pase':'662c304fad7432d296d92582',
            'fecha_hasta_pase':'662c304fad7432d296d92583',
            'num_dias_pase':'662c304fad7432d296d92584',
            'limit_num_dias_pase':'6635380dc9b3e7db4d59eb49',
            'dias_acceso_pase':'662c304fad7432d296d92585',
            'dias_acceso_pase':'662c304fad7432d296d92585',
            'areas_group_pase':'663fed6cb8262fd454326cb3',
            'vehiculos_group_pase':'663e446cadf967542759ebba',
            'equipo_group_pase':'663e446cadf967542759ebbb',
            'instrucciones_group_pase':'65e0a68a06799422eded24aa',
            'status_pase':'66353daa223b8a43d7f274b5',
            'qr_pase':'64ef5b5fff1bec97d2ca27b6',
            'comentario_pase':'65e0a69a322b61fbf9ed23af',
            'catalog_area_pase':'664fc5f3bbbef12ae61b15e9',
        }
        self.pase_grupo_visitados:{
            'nombre_perfil':     f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_name']}",
            'worker_department': f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_department']}",
            'worker_position':   f"{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_position']}",        
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
            'email_vsita': f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{self.mf['email_vsita']}",
            'curp': self.unlist(f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{mf['curp']}"),
            'rfc': f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{mf['rfc']}",
            'telefono': f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{mf['telefono']}",
            'foto': f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{mf['foto']}",
            'identificacion': f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{mf['identificacion']}",
            'empresa': f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{mf['empresa']}",
            'status_visita': f"{self.VISITA_AUTORIZADA_CAT_OBJ_ID}.{mf['status_visita']}",
            'nombre_perfil': f"{self.CONFIG_PERFILES_OBJ_ID}.{mf['nombre_perfil']}",
            'grupo_visitados': self.mf['grupo_visitados'],
            #'nombre_perfil': f"{self.mf['grupo_visitados']}{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_name']}",
            'worker_department': f"{self.mf['grupo_visitados']}{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_department']}",
            'worker_position': f"{self.mf['grupo_visitados']}{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.f['worker_position']}",
            'tipo_visita_pase': self.mf['tipo_visita_pase'],
            'grupo_visitados': self.mf['grupo_visitados'],
            'fecha_desde_visita': self.mf['fecha_desde_visita'],
            'fecha_hasta_visita': self.mf['fecha_hasta_visita'],
            'config_dia_de_acceso': self.mf['config_dia_de_acceso'],
            'config_limitar_acceso': self.mf['config_limitar_acceso'],
            'config_dias_acceso': self.mf['config_dias_acceso'],
        })

        self.notes_project_fields.update(self.notes_fields)
        self.bitacora_acceos = {}
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
        self.f.update(self.notes_fields)
        self.f.update(self.checkin_fields)

    '''
    _funciones internas: son funciones que solo se pueden mandar llamar dentro de este archivo. Si se hereda la clase
    esta funcion no puede ser invocada.
    pep-0008:
        _single_leading_underscore: 
        weak “internal use” indicator. E.g. from M import * does not import objects whose names start with an underscore.
    '''

    def _do_access(self, access_pass, location, area, vehiculo, equipo):
        '''
        Registra el acceso del pase de entra a ubicacion
        solo puede ser ejecutado despues de revisar los accesos
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
        print('access_pass', access_pass)
        pase = {
                f"{self.mf['nombre_visita']}": access_pass['nombre_visita'],
                f"{self.mf['curp']}":access_pass['curp'],
                f"{self.mf['nombre_perfil']}": access_pass['nombre_perfil'],
                f"{self.mf['email_vsita']}":access_pass['email_vsita'],
                f"{self.mf['foto']}":access_pass['foto'],
                f"{self.mf['identificacion']}":access_pass['identificacion'],
                f"{self.mf['empresa']}":access_pass['empresa'],
                f"{self.mf['status_visita']}":access_pass['status_visita'],
                }
        answers = {
            f"{self.mf['tipo_registro']}": 'entrada',
            f"{self.UBICACIONES_CAT_OBJ_ID}":{f"{self.f['location']}":location},
            f"{self.AREAS_DE_LAS_UBICACIONES_CAT_OBJ_ID}":{f"{self.f['area']}":area},
            f"{self.PASE_ENTRADA_OBJ_ID}":pase,
            f"{self.mf['codigo_qr']}":access_pass['_id'],
            f"{self.mf['fecha_entrada']}":self.today_str(employee.get('timezone', 'America/Monterrey'), date_format='datetime'),
        }
        metadata.update({'answers':answers})
        response_create = self.lkf_api.post_forms_answers(metadata)
        print('response_create',response_create)

    def check_status_code(self, data_response):
        for item in data_response:
            if 'status_code' in item[1]:
                return {'status_code':item[1]['status_code']}
            else:
                return {'status_code':'400'}

    def check_in_out_employees(self,  checkin_type, check_datetime, checkin={}, employee_list=[]):
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
                if idx == 0:
                    guard_data.update({self.checkin_fields['checkin_position']: self.chife_guard})
                else:
                    guard_data.update({self.checkin_fields['checkin_position']: self.support_guard})
                checkin[self.f['guard_group']] += [guard_data,]
        return checkin

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
                answers[self.mf['catalog_caseta_salida']] = { self.mf['caseta_salida']: value}
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
        metadata = self.lkf_api.get_metadata(form_id=self.BITACORA_ARTICULOS_PERDIDOS)
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
        #---Define Answers
        answers = {}
        for key, value in data_articles.items():
            if  key == 'ubicacion_perdido':
                dic_prev = answers.get(self.mf['catalog_caseta'],{})
                dic_prev[self.mf['ubicacion']] = value 
                answers[self.mf['catalog_caseta']] = dic_prev
            elif  key == 'area_perdido':
                dic_prev = answers.get(self.mf['catalog_caseta'],{})
                dic_prev[self.mf['caseta']] = value 
                answers[self.mf['catalog_caseta']] = dic_prev
            elif  key == 'guard_perdido':
                answers[self.mf['catalog_guard']] = {self.mf['nombre_guardia']:value}
            else:
                answers.update({f"{self.perdidos_fields[key]}":value})
        metadata.update({'answers':answers})
        return self.lkf_api.post_forms_answers(metadata)

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
                answers[self.mf['catalog_ubicacion']] = {self.mf['ubicacion']:value}
            elif  key == 'caseta_gafete':
                answers[self.mf['catalog_caseta']] = {self.mf['caseta']:value}
            elif  key == 'visita_gafete':
                answers[self.mf['catalog_visita']] = {self.mf['nombre_visita']:value}
            elif  key == 'id_gafete':
                answers[self.gafetes_fields['catalog_gafete']] = {self.gafetes_fields['id_gafete']:value}
            else:
                answers.update({f"{self.gafetes_fields[key]}":value})

        metadata.update({'answers':answers})
        print('answers', simplejson.dumps(metadata, indent=4))
        return self.lkf_api.post_forms_answers(metadata)

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
            if  key == 'falla_ubicacion':
                dic_prev = answers.get(self.mf['catalog_caseta'],{})
                dic_prev[self.mf['ubicacion']] = value 
                answers[self.mf['catalog_caseta']] = dic_prev
            elif  key == 'falla_area':
                dic_prev = answers.get(self.mf['catalog_caseta'],{})
                dic_prev[self.mf['caseta']] = value 
                answers[self.mf['catalog_caseta']] = dic_prev
            elif  key == 'falla':
                answers[self.fallas_fields['falla_catalog']] = {self.fallas_fields['falla']:value}
            elif  key == 'falla_guard':
                answers[self.mf['catalog_guard']] = {self.mf['nombre_guardia']:value}
            elif  key == 'falla_guard_solution':
                answers[self.mf['catalog_guard_close']] = {self.mf['nombre_guardia_apoyo']:value}
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
            if  key == 'ubicacion_incidence':
                dic_prev = answers.get(self.mf['catalog_caseta'],{})
                dic_prev[self.mf['ubicacion']] = value 
                answers[self.mf['catalog_caseta']] = dic_prev
            elif  key == 'area_incidence':
                dic_prev = answers.get(self.mf['catalog_caseta'],{})
                dic_prev[self.mf['caseta']] = value 
                answers[self.mf['catalog_caseta']] = dic_prev
            elif  key == 'guard_incident':
                answers[self.mf['catalog_guard']] = {self.mf['nombre_guardia']:value}
            elif  key == 'incidence':
                answers[self.incidence_fields['catalog_incidence']] = {self.incidence_fields['incidence']:value}
            else:
                answers.update({f"{self.incidence_fields[key]}":value})
        metadata.update({'answers':answers})
        return self.lkf_api.post_forms_answers(metadata)

    def create_note(self, data_notes):
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
        answers = {}
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
        now = datetime.now()
        fecha_hora_str = now.strftime("%Y-%m-%d %H:%M:%S")
        answers.update({f"{self.notes_fields['note_open_date']}":fecha_hora_str})

        metadata.update({'answers':answers})
        print('answers', simplejson.dumps(answers, indent=4))
        return self.lkf_api.post_forms_answers(metadata)

    def create_pase(self, data_pase):
        #---Define Metadata
        metadata = self.lkf_api.get_metadata(form_id=self.PASE_ENTRADA)
        metadata.update({
            "properties": {
                "device_properties":{
                    "System": "Script",
                    "Module": "Accesos",
                    "Process": "Creación de pase",
                    "Action": "create_pase",
                    "File": "accesos/app.py"
                }
            },
        })
        #---Define Answers
        answers = {}
        for key, value in data_pase.items():
            if key == 'ubicacion_pase':
                answers[self.mf['catalog_ubicacion']] = {self.mf['ubicacion']:value}
            elif key == 'perfil_pase':
                answers[self.mf['catalog_tipo_pase']] = {self.mf['nombre_perfil']:value}
            elif key == 'visita_a_pase':
                list_visit = []
                for item in value:
                    nombre = item.get('nombre_completo','')
                    list_visit.append({self.mf['catalog_guard']:{self.mf['nombre_guardia']:nombre}})
                answers[self.mf['grupo_visitados']] = list_visit
            elif key == 'authorized_pase':
                answers[self.mf['catalog_guard_close']] = {self.mf['nombre_guardia_apoyo']:value}
            elif key == 'areas_group_pase':
                list_areas = []
                for item in value:
                    list_areas.append({self.mf['catalog_caseta']:{self.mf['caseta']:item}})
                answers[self.pase_entrada_fields['areas_group_pase']] = list_areas
            elif key == 'vehiculos_group_pase':
                list_vehiculos = []
                for item in value:
                    tipo = item.get('tipo','')
                    marca = item.get('marca','')
                    modelo = item.get('modelo','')
                    estado = item.get('estado','')
                    placas = item.get('placas','')
                    color = item.get('color','')
                    list_vehiculos.append({
                        self.mf['catalog_vehiculo']:{
                            self.mf['tipo_vehiculo']:tipo,
                            self.mf['marca_vehiculo']:marca,
                            self.mf['modelo_vehiculo']:modelo,
                        },
                        self.mf['catalog_estado']:{
                            self.mf['nombre_estado']:estado,
                        },
                        self.mf['placas_vehiculo']:placas,
                        self.mf['color_vehiculo']:color,
                    })
                answers[self.pase_entrada_fields['vehiculos_group_pase']] = list_vehiculos  
            elif key == 'equipo_group_pase':
                list_equip = []
                for item in value:
                    nombre = item.get('nombre','')
                    marca = item.get('marca','')
                    color = item.get('color','')
                    tipo = item.get('tipo','')
                    serie = item.get('serie','')
                    list_vehiculos.append({
                        self.mf['tipo_equipo']:tipo,
                        self.mf['nombre_articulo']:nombre,
                        self.mf['marca_articulo']:marca,
                        self.mf['numero_serie']:serie,
                        self.mf['color_articulo']:color,
                    })
            elif key == 'instrucciones_group_pase':
                list_comments = []
                for item in value:
                    list_comments.append({self.pase_entrada_fields['comentario_pase']:item})
                answers[self.pase_entrada_fields['instrucciones_group_pase']] = list_comments
            else:
                answers.update({f"{self.pase_entrada_fields[key]}":value})
        #---Valor
        metadata.update({'answers':answers})
        #print('answers', simplejson.dumps(metadata, indent=4))
        print('Respuesta',self.lkf_api.post_forms_answers(metadata))

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
                response = self.get_record_by_folio(element, self.BITACORA_ARTICULOS_PERDIDOS, select_columns={'_id':1,})
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

    def do_access(self, qr_code, location, area, vehiculo, equipo):
        '''
        Valida pase de entrada y crea registro de entrada al pase
        '''
        print('me quede ahceidno la vaildacion y el registro de entrada')
        if not qr_code and not location and not area:
            return False
        access_pass = self.search_pass(qr_code)
        if self.validate_access_pass_location(qr_code):
            self.LKFException("En usuario ya se encuentra dentro de una ubicacion")
        val_certificados = self.validate_certificados(qr_code, location)
        pass_dates = self.validate_pass_dates(access_pass)
        res = self._do_access(access_pass,  location, area, vehiculo, equipo)

    def do_checkin(self, location, area, employee_list=[]):
        # if not self.is_boot_available(location, area):
        #     msg = f"Can not login in to boot on location {location} at the area {area}."
        #     msg += f"Because '{self.last_check_in.get('employee')}' is logged in."
        #     self.LKFException(msg)
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
        # if not_allowed:
        #     msg = f"Usuarios con ids {not_allowed}. "
        #     msg += f"No estan permitidos de hacer checking en esta area : {area} de la ubicacion {location} ."
        #     self.LKFException({'msg':msg,"title":'Error de Configuracion'})

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
                        "system": "Modulo Acceos",
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

    def do_out(self, qr):
        '''
            Realiza el cambio de estatus de la forma de bitacora, relacionada a la salida, como parametro
            es necesesario enviar el nombre del visitante que es el unico dato qu se encuentra en la forma
        '''
        response = False
        last_check_out = self.get_last_user_move(qr)
        if last_check_out.get('folio'):
            folio = last_check_out.get('folio',0)
            if self.user_in_facility(status_visita=last_check_out.get('status_visita')):
                answers = {
                    f"{self.mf['tipo_registro']}":'salida',
                }
                response = self.lkf_api.patch_multi_record( answers=answers, form_id=self.BITACORA_ACCESOS, folios=[folio])
        if not response:
            self.LKFException("El usuario se encuentra fuera de la ubicacion.")
        return response            

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

    def get_access_pass(self, qr_code):
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
            {'$project': self.proyect_format(self.notes_project_fields)},
            {'$sort':{self.f['note_open_date']:1}}
            ]
        return self.format_cr_result(self.cr.aggregate(query))

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

    def get_detail_user(self, qr_code):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.PASE_ENTRADA,
            "_id":ObjectId(qr_code),
        }
        print('match_query',match_query)
        query = [
            {'$match': match_query },
            {'$project': self.proyect_format(self.pase_entrada_fields)},
            {'$sort':{'folio':-1}},
        ]
        result = self.format_cr_result(self.cr.aggregate(query))
        if len(result) == 1:
            return result[0]
        else:
            return {} 

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
                    'area': f"$answers.{self.CONF_AREA_EMPLEADOS_CAT_OBJ_ID}.{self.mf['caseta']}",
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

    def get_information_catalog(self, id_catalog):
        match_query = {
            'deleted_at':{"$exists":False},
        }

        mango_query = {"selector":
            {"answers":
                {"$and":[match_query]}
            },
            "limit":10000
        }
        res = self.lkf_api.search_catalog(id_catalog, mango_query)
        
    def get_checkin_by_id(self, _id=None, folio=None):
        if not _id or not folio:
            msg = "An _id or a folio is requierd to get the record"
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
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.CHECKIN_CASETAS,
            f"answers.{self.checkin_fields['cat_location']}":location,
            f"answers.{self.checkin_fields['cat_area']}":area,
            }
        query = [
            {'$match': match_query },
            {'$project': self.proyect_format(self.checkin_fields)},
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
            {'$project': self.proyect_format(self.checkin_fields)},
            {'$sort':{'created_at':-1}},
            {'$limit':1}
            ]
        return self.format_cr_result(self.cr.aggregate(query), get_one=True)

    def get_last_user_move(self, qr):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.BITACORA_ACCESOS,
            f"answers.{self.bitacora_fields['codigo_qr']}":qr,
        }
        res = self.cr.find(
            match_query, 
            {'folio':'$folio', 'status_visita': f"$answers.{self.bitacora_fields['status_visita']}",}
            ).sort('updated_at', -1).limit(1)
        return self.format_cr_result(res, get_one=True)
        # return self.format_cr_result(self.cr.aggregate(query), get_one=True)

    def get_list_article_lost(self, location, area):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.BITACORA_ARTICULOS_PERDIDOS,
            f"answers.{self.perdidos_fields['ubicacion_perdido']}":location,
            f"answers.{self.perdidos_fields['area_perdido']}":area,
        }
        query = [
            {'$match': match_query },
            {'$project': self.proyect_format(self.perdidos_fields)},
            {'$sort':{'folio':-1}},
        ]
        #print('answers', simplejson.dumps(query, indent=4))
        return self.format_cr_result(self.cr.aggregate(query))

    def get_list_article_concessioned(self, location):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.CONCESSIONED_ARTICULOS,
            f"answers.{self.consecionados_fields['ubicacion_concesion']}":location,
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

    def get_list_badge(self, location):
        response = []
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.BITACORA_GAFETES_LOCKERS,
            f"answers.{self.gafetes_fields['ubicacion_gafete']}":location,
        }
        query = [
            {'$match': match_query },
            {'$project': {
                "status_gafete": f"$answers.{self.gafetes_fields['status_gafete']}",
                "ubicacion_gafete": f"$answers.{self.gafetes_fields['ubicacion_gafete']}",
                "caseta_gafete": f"$answers.{self.gafetes_fields['caseta_gafete']}",
                "visita_gafete": f"$answers.{self.gafetes_fields['visita_gafete']}",
                "id_gafete": f"$answers.{self.gafetes_fields['catalog_gafete']}.{self.gafetes_fields['id_gafete']}",
                "documento_gafete": f"$answers.{self.gafetes_fields['documento_gafete']}",
            }},
            {'$sort':{'folio':-1}},
        ]
        return self.format_cr_result(self.cr.aggregate(query))

    def get_list_bitacora(self, location, area):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.BITACORA_ACCESOS,
            f"answers.{self.bitacora_fields['ubicacion']}":location,
            f"answers.{self.bitacora_fields['caseta_entrada']}":area,
        }
        query = [
            {'$match': match_query },
            {'$project': self.proyect_format(self.bitacora_fields)},
            {'$sort':{'folio':-1}},
        ]
        return self.format_cr_result(self.cr.aggregate(query))

    def get_list_fallas(self, location, area):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.BITACORA_FALLAS,
            f"answers.{self.mf['catalog_caseta']}.{self.mf['ubicacion']}":location,
            f"answers.{self.mf['catalog_caseta']}.{self.mf['caseta']}":area,
        }
        query = [
            {'$match': match_query },
            {'$project': {
                "folio": "$folio",
                "falla_status": f"$answers.{self.fallas_fields['falla_status']}",
                "falla_fecha": f"$answers.{self.fallas_fields['falla_fecha']}",
                "falla_ubicacion": f"$answers.{self.mf['catalog_caseta']}.{self.mf['ubicacion']}",
                "falla_area": f"$answers.{self.mf['catalog_caseta']}.{self.mf['caseta']}",
                "falla": f"$answers.{self.fallas_fields['falla_catalog']}.{self.fallas_fields['falla']}",
                "falla_comments": f"$answers.{self.fallas_fields['falla_comments']}",
                "falla_guard": f"$answers.{self.mf['catalog_guard']}.{self.mf['nombre_guardia']}",
                "falla_guard_solution": f"$answers.{self.mf['catalog_guard_close']}.{self.mf['nombre_guardia_apoyo']}",
                "falla_fecha_solucion": f"$answers.{self.fallas_fields['falla_fecha_solucion']}",
            }},
            {'$sort':{'folio':-1}},
        ]
        # print('answers', simplejson.dumps(query, indent=4))
        return self.format_cr_result(self.cr.aggregate(query))

    def get_list_incidences(self, location, area):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.BITACORA_INCIDENCIAS,
            f"answers.{self.mf['catalog_caseta']}.{self.mf['ubicacion']}":location,
            f"answers.{self.mf['catalog_caseta']}.{self.mf['caseta']}":area,
        }
        query = [
            {'$match': match_query },
            {'$project': {
                "folio": "$folio",
                "date_incidence": f"$answers.{self.incidence_fields['date_incidence']}",
                "ubicacion_incidence": f"$answers.{self.mf['catalog_caseta']}.{self.mf['ubicacion']}",
                "area_incidence": f"$answers.{self.mf['catalog_caseta']}.{self.mf['caseta']}",
                "incidence": f"$answers.{self.incidence_fields['catalog_incidence']}.{self.incidence_fields['incidence']}",
                "comments_incidence": f"$answers.{self.incidence_fields['comments_incidence']}",
                "guard_incident": f"$answers.{self.mf['catalog_guard']}.{self.mf['nombre_guardia']}",
            }},
            {'$sort':{'folio':-1}},
        ]
        return self.format_cr_result(self.cr.aggregate(query))

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
        print('answers', simplejson.dumps(query, indent=4))
        return self.format_cr_result(self.cr.aggregate(query))

    def get_list_last_user_move(self, qr):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.BITACORA_ACCESOS,
            f"answers.{self.bitacora_fields['codigo_qr']}":qr,
        }
        res = self.cr.find(
            match_query, 
            {
                'status_visita': f"$answers.{self.bitacora_fields['status_visita']}",
                'nombre_visita':f"$answers.{self.mf['catalog_visita']}.{self.mf['nombre_visita']}",
                'location':f"$answers.{self.mf['catalog_ubicacion']}.{self.mf['ubicacion']}",
                'fecha':f"$answers.{self.mf['bitacora_entrada']}",
                'duration':f"$answers.{self.mf['duracion']}",
            }
            ).sort('updated_at', -1).limit(10000)

        return self.format_cr_result(res)
    
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
            res[puesto] = res.get(puesto,
                self.get_users_by_location_area(location, area, **{'position': guard_type['puestos']})
                )
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

    def get_shift_data(self, search_default=True):
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
            for u_id, each_user in user_status.items():
                if u_id == user_id:
                    location_employees[self.support_guard] = [each_user,]
                    guard = each_user
                else:
                    if each_user.get('status') == 'in':
                        location_employees[self.support_guard].append(each_user)

        else:
            # location_employees = {}
            default_booth , user_booths = self.get_user_booth(search_default=False)
            # location = default_booth.get('location')
            booth_area = default_booth['area']
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
        # aver = self.get_booth_status(booth_area, booth_location)
        # print('aver', aver)

            # if guard_type['tipo_de_guardia'] == self.guardia_de_apoyo:
            #     support_positions = guard_type['puestos']
        # notes = self.get_access_notes(booth_location, booth_area)
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
            f"answers.{self.mf['catalog_guard']}.{self.mf['caseta']}":area,
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
        self.last_check_in = self.get_last_checkin(location, area)
        last_status = self.last_check_in.get('checkin_type')
        if last_status in ['entrada','apertura']:
            return False
        else:
            return True

    def update_article_concessioned(self, data_articles, folio):
        answers = {}
        for key, value in data_articles.items():
            if  key == 'ubicacion_concesion':
                answers[self.mf['catalog_ubicacion']] = { self.mf['ubicacion'] : value}
            elif  key == 'nombre_concesion':
                answers[self.consecionados_fields['persona_catalog_concesion']] = { self.consecionados_fields['persona_nombre_concesion'] : value}
            elif  key == 'caseta_concesion':
                answers[self.mf['catalog_caseta_salida']] = { self.mf['caseta_salida']: value}
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
        for key, value in data_articles.items():
            if  key == 'ubicacion_perdido':
                dic_prev = answers.get(self.mf['catalog_caseta'],{})
                dic_prev[self.mf['ubicacion']] = value 
                answers[self.mf['catalog_caseta']] = dic_prev
            elif  key == 'area_perdido':
                dic_prev = answers.get(self.mf['catalog_caseta'],{})
                dic_prev[self.mf['caseta']] = value 
                answers[self.mf['catalog_caseta']] = dic_prev
            elif  key == 'guard_perdido':
                answers[self.mf['catalog_guard']] = {self.mf['nombre_guardia']:value}
            else:
                answers.update({f"{self.perdidos_fields[key]}":value})

        if answers or folio:
            return self.lkf_api.patch_multi_record( answers = answers, form_id=self.BITACORA_ARTICULOS_PERDIDOS, folios=[folio])
        else:
            self.LKFException('No se mandarón parametros para actualizar')

    def update_failure(self, data_failures, folio):
        answers = {}
        for key, value in data_failures.items():
            if  key == 'falla_ubicacion':
                dic_prev = answers.get(self.mf['catalog_caseta'],{})
                dic_prev[self.mf['ubicacion']] = value 
                answers[self.mf['catalog_caseta']] = dic_prev
            elif  key == 'falla_area':
                dic_prev = answers.get(self.mf['catalog_caseta'],{})
                dic_prev[self.mf['caseta']] = value 
                answers[self.mf['catalog_caseta']] = dic_prev
            elif  key == 'falla':
                answers[self.fallas_fields['falla_catalog']] = {self.fallas_fields['falla']:value}
            elif  key == 'falla_guard':
                answers[self.mf['catalog_guard']] = {self.mf['nombre_guardia']:value}
            elif  key == 'falla_guard_solution':
                answers[self.mf['catalog_guard_close']] = {self.mf['nombre_guardia_apoyo']:value}
            else:
                answers.update({f"{self.fallas_fields[key]}":value})

        if answers or folio:
            return self.lkf_api.patch_multi_record( answers = answers, form_id=self.BITACORA_FALLAS, folios=[folio])
        else:
            self.LKFException('No se mandarón parametros para actualizar')

    def update_incidence(self, data_incidences, folio):
        '''
            Realiza una actualización sobre cualquier nota, actualizando imagenes, status etc
        '''
        answers = {}
        for key, value in data_incidences.items():
            if  key == 'ubicacion_incidence':
                dic_prev = answers.get(self.mf['catalog_caseta'],{})
                dic_prev[self.mf['ubicacion']] = value 
                answers[self.mf['catalog_caseta']] = dic_prev
            elif  key == 'area_incidence':
                dic_prev = answers.get(self.mf['catalog_caseta'],{})
                dic_prev[self.mf['caseta']] = value 
                answers[self.mf['catalog_caseta']] = dic_prev
            elif  key == 'guard_incident':
                answers[self.mf['catalog_guard']] = {self.mf['nombre_guardia']:value}
            elif  key == 'incidence':
                answers[self.incidence_fields['catalog_incidence']] = {self.incidence_fields['incidence']:value}
            else:
                answers.update({f"{self.incidence_fields[key]}":value})
        if answers or folio:
            return self.lkf_api.patch_multi_record( answers = answers, form_id=self.BITACORA_INCIDENCIAS, folios=[folio])
        else:
            self.LKFException('No se mandarón parametros para actualizar')

    def update_guard_status(self, guard, this_user):
        # last_checkin = self.get_user_last_checkin(guard['user_id'])
        status_turn = 'Turno Cerrado'
        print('this_user', this_user)
        if this_user.get('status') == 'in':
            status_turn = 'Turno Abierto'

        guard['turn_start_datetime'] =  this_user.get('checkin_date')
        guard['status_turn'] =  status_turn
        return guard

    def update_guards_booths(self, data_guard, folio):
        response = []
        for item in data_guard:
            answers = {}
            answers[self.mf['guard_group']] = {'-1':{ self.mf['catalog_guard_close']: {self.mf['nombre_guardia_apoyo']: item}}}
            response.append(self.lkf_api.patch_multi_record( answers = answers, form_id=self.CHECKIN_CASETAS, folios=[folio]))
        return response

    def update_notes(self, data_notes, folio):
        '''
            Realiza una actualización sobre cualquier nota, actualizando imagenes, status etc
        '''
        answers = {}
        #----Assign Value
        for key, value in data_notes.items():
            if key == 'list_comments':
                answers.update({-1:{f"{self.notes_fields[key]}": value}})
            elif  key == 'note_booth':
                answers[self.notes_fields['note_catalog_booth']] = {self.notes_fields['note_booth']:value}
            elif  key == 'note_guard':
                answers[self.notes_fields['note_catalog_guard']] = {self.notes_fields['note_guard']:value}
            else:
                answers.update({f"{self.notes_fields[key]}":value})
        #----Assign Time
        if data_notes.get('note_status','') == 'cerrado':
            now = datetime.now()
            fecha_hora_str = now.strftime("%Y-%m-%d %H:%M:%S")
            answers.update({f"{self.notes_fields['note_close_date']}":fecha_hora_str})
        if answers or folio:
            print('answers', simplejson.dumps(answers, indent=4))
            return self.lkf_api.patch_multi_record( answers = answers, form_id=self.ACCESOS_NOTAS, folios=[folio])
        else:
            self.LKFException('No se mandarón parametros para actualizar')
        
    def search_pass(self, qr_code=None, location=None):
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
            {'$project': self.proyect_format(self.pase_entrada_fields)},
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
        print('-------------- search_access_pass')
        if self.validate_value_id(qr_code):
            complete_qr = {}
            data_information = self.get_detail_user(qr_code);
            complete_qr['pass'] = {
                'tipo': data_information.get('perfil_pase',''),
                'status':data_information.get('status_pase',''),
                'fecha_expedicion':data_information.get('fecha_desde_pase',''),
                'fecha_expiracion':data_information.get('fecha_hasta_pase',''),
            }
            complete_qr['validaciones'] = {
                #---Se tiene que validar que movimiento se esta haciendo
                'accion_ingreso':'Salida' if self.validate_access_pass_location(qr_code) else 'Entrada',
                'location': self.search_pass(qr_code=qr_code, location=location),
                #---Se tiene que validar que errores pueden existir dentro de la data del pase
                'errores':[
                    #{"tipo":'Certificado','comunicacion':'Vencido','fecha':'2024-05-25'}
                ]
            }
            complete_qr['portador'] = self.search_pass(qr_code=qr_code)
            #---Comentarios
            complete_qr['comentarios'] = []
            if  data_information.get('instrucciones_group_pase'):
                for item in data_information.get('instrucciones_group_pase'):
                    complete_qr['comentarios'].append(item[self.pase_entrada_fields['comentario_pase']])
            #---Accessos
            complete_qr['accesos'] = []
            if  data_information.get('areas_group_pase'):
                for item in data_information.get('areas_group_pase'):
                    area = ''
                    status_area = ''
                    if self.mf['catalog_caseta'] in item and self.mf['caseta'] in item[self.mf['catalog_caseta']]:
                        area = item[self.mf['catalog_caseta']][self.mf['caseta']]
                    if self.mf['catalog_caseta'] in item and self.mf['caseta'] in item[self.mf['catalog_caseta']]:
                        status_area = item[self.mf['catalog_caseta']][self.mf['status_area']]
                    if type(status_area) == list:
                        status_area = status_area[0]
                    complete_qr['accesos'].append({"area":area, "status":status_area})
            #---Last Access
            complete_qr['ultimo_acceso'] = []
            response_last_move = self.get_list_last_user_move(qr_code);
            for item in response_last_move:
                complete_qr['ultimo_acceso'].append({
                    'nombre_visita':item.get('nombre_visita',''),
                    'location':item.get('location',''),
                    'fecha':item.get('fecha',''),
                    'duration':item.get('duration','0'),
                })
            #---List Equip
            complete_qr['equipo'] = []
            if  data_information.get('equipo_group_pase'):
                for item in data_information.get('equipo_group_pase'):
                    complete_qr['equipo'].append({
                        'tipo': item[self.mf['tipo_equipo']],
                        'marca': item[self.mf['nombre_articulo']],
                        'modelo': item[self.mf['marca_articulo']],
                        'serie': item[self.mf['numero_serie']],
                        'color': item[self.mf['color_articulo']],
                    })
            #---List Equip
            complete_qr['vehiculos'] = []
            if  data_information.get('vehiculos_group_pase'):
                for item in data_information.get('vehiculos_group_pase'):
                    complete_qr['vehiculos'].append({
                        'tipo':item[self.mf['catalog_vehiculo']][self.mf['tipo_vehiculo']],
                        'marca':item[self.mf['catalog_vehiculo']][self.mf['marca_vehiculo']],
                        'modelo':item[self.mf['catalog_vehiculo']][self.mf['modelo_vehiculo']],
                        'placa':item[self.mf['placas_vehiculo']],
                        'color':item[self.mf['color_vehiculo']],
                    })
            #print('aqui voy tnego q buscar el q r code....')
            #print('si me das pura location y area', )
            #print('complete_qr', simplejson.dumps(complete_qr, indent=4))
            #print('=====================================================')
            return complete_qr
        else:
            return self.LKFException({"status_code":400, "msg":'El parametro para qr, no es valido'})

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

    def validate_access_pass_location(self, qr_code):
        #TODO
        last_move = self.get_last_user_move(qr_code)
        print('last_move', last_move)
        if self.user_in_facility(last_move.get('status_visita')):
            print('asqqq')
            return True
        return False

    def validate_certificados(self, qr_code, location):
        return True

    def validate_pass_dates(self, access_pass):
        return True

    def validate_value_id(self, qr_code):
        try:
            ObjectId(qr_code)
            return True
        except:
            return False