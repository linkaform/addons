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
        })
