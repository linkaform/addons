# -*- coding: utf-8 -*-
### Linkaform Modules / Archivo de Módulo ###
'''
Este archivo define el modelo de datos del módulo Servicio Maquinaria Pesada.
Contiene los IDs de formularios, catálogos y campos (fields) usados por la clase ServicioMaquinariaPesada.

Separado de app.py para mantener la configuración de datos desacoplada de la lógica de negocio.
'''

from lkf_addons.addons.base.app import Base


### Modelo de Módulo ###
'''
ServicioMaquinariaPesadaModel hereda SOLO de Base.
La clase ServicioMaquinariaPesada en app.py hereda de esta clase.

Para usar otro módulo (Employee, Location, Oracle...) no se hereda: se carga con
`self.load(module='Employee', **self.kwargs)` y el objeto queda en `self.Employee`.
'''

class ServicioMaquinariaPesadaModel(Base):

    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False, **kwargs):
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api, **kwargs)
        self.name = __class__.__name__
        self.settings = settings

        # Forms
        self.INFORME_SERVICIO = self.lkm.form_id('informe_de_servicio','id')
        self.INFORME_SERVICIO_TALLER = self.lkm.form_id('informe_de_servicio_en_taller','id')
        self.CARE_INSPECTION_CSR = self.lkm.form_id('care_inspection_oportunidades_comerciales_csr','id')
        self.CARE_INSPECTION_TECNICO = self.lkm.form_id('care_inspection_oportunidades_comerciales_tecnico','id')
        self.ENTRADA_SALIDA_EQUIPOS = self.lkm.form_id('entrada_y_salida_de_equipos','id')
        self.GESTION_COMERCIAL_POSTVENTA = self.lkm.form_id('informe_de_gestion_comercial_postventa','id')
        self.GESTION_COMERCIAL_VENTAS = self.lkm.form_id('informe_de_gestion_comercial_ventas','id')
        self.PROGRAMACION_SERVICIOS = self.lkm.form_id('programacion_de_servicios','id')

        # Catálogos (siempre los 3 atributos)
        self.CLIENTES_CAT = self.lkm.catalog_id('clientes')
        self.CLIENTES_CAT_ID = self.CLIENTES_CAT.get('id')
        self.CLIENTES_CAT_OBJ_ID = self.CLIENTES_CAT.get('obj_id')

        self.ACTIVOS_FIJOS_CAT = self.lkm.catalog_id('activos_fijos')
        self.ACTIVOS_FIJOS_CAT_ID = self.ACTIVOS_FIJOS_CAT.get('id')
        self.ACTIVOS_FIJOS_CAT_OBJ_ID = self.ACTIVOS_FIJOS_CAT.get('obj_id')

        self.USUARIOS_CAT = self.lkm.catalog_id('usuarios')
        self.USUARIOS_CAT_ID = self.USUARIOS_CAT.get('id')
        self.USUARIOS_CAT_OBJ_ID = self.USUARIOS_CAT.get('obj_id')

        self.FORMULARIOS_CAT = self.lkm.catalog_id('formularios')
        self.FORMULARIOS_CAT_ID = self.FORMULARIOS_CAT.get('id')
        self.FORMULARIOS_CAT_OBJ_ID = self.FORMULARIOS_CAT.get('obj_id')

        self.EMPLEADOS_CAT = self.lkm.catalog_id('empleados')
        self.EMPLEADOS_CAT_ID = self.EMPLEADOS_CAT.get('id')
        self.EMPLEADOS_CAT_OBJ_ID = self.EMPLEADOS_CAT.get('obj_id')

        # Fields (ids de campos usados por calcula_gastos / add_fecha_field)
        self.f.update({
            'field_group_gastos': '6675b286b258d3517a03e8c7',
            'field_select_tipo_gasto': '6686ebc5e9dfa385bfabad81',
            'field_monto_gasto': 'a00000000000000000000001',
            'field_total_gastos': '000000000000000000000006',
            'field_saldo': 'a00000000000000000000008',
            'field_anticipo': 'a00000000000000000000007',
            'field_kilometraje_total': 'b00000000000000000000003',
            'field_kilometraje_final': 'b00000000000000000000002',
            'field_kilometraje_inicial': 'b00000000000000000000001',
            'field_status_hrs_trabajadas': '6682fc2afc164dde9954c21c',
            'field_id_inicio_actividad': 'c00000000000000000000004',
            'field_id_fin_actividad': 'c00000000000000000000005',
            'field_id_iniciar_ida': 'c00000000000000000000001',
            'field_id_terminar_ida': 'c00000000000000000000002',
            'field_id_iniciar_regreso': 'c00000000000000000000006',
            'field_id_terminar_regreso': 'c00000000000000000000007',
            'razon_social': '6687f2f37b2c023e187d6252',
            'nombre_comercial': '667468e3e577b8b98c852aaa',
            'ruc': '667468e3e577b8b98c852aab',
            'chasis': '6646393c3fa8b818265d0325',
            'activo_estatus': '6646393c3fa8b818265d0329',
            'estatus': '672eadbd8064d180dab0097e',
            'nombre_completo': '62c5ff407febce07043024dd',
            'codigo_empleado': '670f585bf844ff7bc357b1dc',
            'equipo_registrado': '668309d89331539409abace1',
            'numero_orden': '672e8edfd2f1f131c66505d9',
            'especifique_equipo': '66830c302315146a39b4f22a',
            'especifique_marca': '66830c302315146a39b4f22b',
            'especifique_modelo': '66830c302315146a39b4f22c',
            'especifique_serie': '66830c302315146a39b4f22d',
            'grupo_horas_trabajadas': 'c00000000000000000000003',
            'grupo_traslado_ida': 'c00000000000000000000021',
            'grupo_traslado_regreso': 'c00000000000000000000022',
            'fecha_apertura': '666a160967bcb9e23b1cc963',
            'fecha_atencion': '666a160967bcb9e23b1cc964',
            'tecnicos_asignados': '666a160967bcb9e23b1cc967',
            'trabajo_a_realizar': '673e734f94d1ef23abb279ed',
            'tipo_de_informe': '672eb39a4d20582177b00a06',
            'id_formulario': '672eb39a4d20582177b00a07',
            'nombre_usuario': '638a9a7767c332f5d459fc81',
            'email_usuario': '638a9a7767c332f5d459fc82',
            'puesto_usuario': '663bc4c79b8046ce89e97cf4',
            'modo_registro_horas': '6736968ee7be2602ca566376',
            'tipo_asignacion': '672eb5efd1134f9aca98da36',
            'comprobante_gasto': '6686ebc5e9dfa385bfabad83',
            'comentarios_generales': '6679a8fa580fa539a803e908',
            'resumen_gestion': '670dc8de391a088440159491',
            'fecha_servicio': '672e8edfd2f1f131c66505d8',
            'nombre_contacto': '672e8e711d0c3f0eb0650570',
            'celular_contacto': '672e8e711d0c3f0eb0650571',
            'marca': '66beb10007981d4509575054',
            'modelo': '66beb11907981d4509575056',
            'categoria': '66beb1b507981d4509575057',
            'nombre_equipo': '66c192ef89463aa27fc1818b',
            'horometro_motor_1': '66c1758989463aa27fc1816e',
            'estado_equipo': '66c1940b89463aa27fc1818c',
            'detalle_trabajos_realizados': '667489b66e98a08e9d03e955',
        })
