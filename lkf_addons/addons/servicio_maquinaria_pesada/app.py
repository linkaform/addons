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

# Importaciones necesarias
import sys, simplejson, pytz
from datetime import datetime, timedelta, date

from .model import ServicioMaquinariaPesadaModel

### Objeto o Clase de Módulo ###
'''
Cada módulo puede tener múltiples objetos, configurados en clases.
Estos objetos deben heredar de `base.LKF_Base` y de cualquier módulo dependiente necesario.
Al utilizar `super()` en el método `__init__()`, heredamos las variables de configuración de la clase.

Además, se pueden heredar funciones de cualquier clase antecesora usando el método `super()`.
'''

class ServicioMaquinariaPesada(ServicioMaquinariaPesadaModel):

    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False, **kwargs):
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api, **kwargs)

    # ---- add_fecha_to_field.py ----

    # ---- calcula_gastos.py ----

    def get_optios_and_fields_subtotales(self):
        form_fields = self.lkf_api.get_form_id_fields( self.current_record['form_id'] )
        if not form_fields:
            raise Exception(simplejson.dumps({'folio': {'msg': 'Error en el script al obtener los campos de la forma', 'label': 'Folio', 'error': []}}))
        # Leer la estructura de la forma para obtener las opciones del campo Tipo de gasto dentro del grupo repetitivo
        fields = form_fields[0]['fields']
        options_subtotales = []
        # Con esas opciones buscar los campos de subtotal donde se va a colocar el resultado
        fields_subtotales = {}
        with_total_kilometraje = False
        with_status_to_dates = False
        for field in fields:
            if field['field_id'] == self.f['field_select_tipo_gasto']:
                options_subtotales = [ o['value'] for o in field.get('options', []) ]
            elif field['field_id'] == self.f['field_kilometraje_total']:
                with_total_kilometraje = True
            elif field['field_id'] == self.f['field_status_hrs_trabajadas']:
                with_status_to_dates = True
            if not field.get('group') and not field.get('catalog') and 'subtotal' in field['label'].lower():
                opt_subtotal = field['label'].lower().replace('subtotal', '').strip()
                opt_subtotal = opt_subtotal.replace(' ', '_')
                fields_subtotales[ opt_subtotal ] = field['field_id']
        return options_subtotales, fields_subtotales, with_total_kilometraje, with_status_to_dates

    def get_status_on_db(self):
        if not self.current_record.get('folio'):
            return ''
        rec_db = self.cr.find_one({
            'folio': self.current_record['folio'],
            'form_id': self.current_record['form_id'],
            'deleted_at': {'$exists': False}
        },{f'answers.{self.f['field_status_hrs_trabajadas']}': 1})
        if not rec_db:
            return ''
        return rec_db.get('answers', {}).get(self.f['field_status_hrs_trabajadas'], '')

    def get_str_date_updated(self):
        timestamp = self.current_record['end_timestamp']
        guayaquil_tz = pytz.timezone(self.current_record['timezone'])
        fecha_utc = datetime.utcfromtimestamp(timestamp)
        fecha_guayaquil = fecha_utc.replace(tzinfo=pytz.utc).astimezone(guayaquil_tz)
        return fecha_guayaquil.strftime('%Y-%m-%d %H:%M:%S')

    def msg_error_app(self, f_id, f_label, msg_error):
        raise Exception(simplejson.dumps({
            f_id: { 'msg': [msg_error], 'label': f_label, 'error': [] }
        }))

    def get_item_to_update(self, actividades, contiene, no_contiene):
        item_found = [i for i, elem in enumerate(actividades) if elem.get(contiene) and not elem.get(no_contiene)]
        if not item_found:
            return None
        return item_found[-1]

    def calculates_dates_group(self, field_id_to_group, status_hrs, status_start, status_end, field_inicio, field_fin):
        # Puede ser inicio/fin de las actividades
        group_actividades = self.current_record['answers'].get(field_id_to_group, [])
        """
        Validaciones para Iniciar una Actividad
        """
        if status_hrs == status_start:
            # Si ya hay actividades con informacion, Debo validar que la última que tiene una fecha de inicio ya tenga una fecha fin
            if any(group_actividades):
                # Reviso si alguna actividad que se inicio pero aun no se termina
                item = self.get_item_to_update(group_actividades, field_inicio, field_fin)
                if item is not None:
                    self.msg_error_app(self.f['field_status_hrs_trabajadas'], 'Status de horas trabajadas', 'No se puede iniciar una actividad ya que aun no se cierra la última')
            # En el último item se integra el inicio de la actividad
            group_actividades[-1].update({ field_inicio: self.get_str_date_updated() })
        elif status_hrs == status_end:
            """
            Validaciones para el Termino de la actividad
            """
            # Si todas las actividades estan vacias, entonces ninguna se ha iniciado
            if not any(group_actividades):
                self.msg_error_app(self.f['field_status_hrs_trabajadas'], 'Status de horas trabajadas', 'No se han iniciado actividades')
            # Reviso si hay casos donde se ya se finalizaron todas las que tambien se iniciaron
            if all(field_inicio in elem and field_fin in elem for elem in group_actividades if elem):
                self.msg_error_app(self.f['field_status_hrs_trabajadas'], 'Status de horas trabajadas', 'Ya has finalizado todas las actividades')
            # Obtengo el item donde se va a cerrar la actividad
            item = self.get_item_to_update(group_actividades, field_inicio, field_fin)
            group_actividades[item][field_fin] = self.get_str_date_updated()
        # Limpiar los sets que estan vacios
        self.current_record['answers'][field_id_to_group] = [elem for elem in group_actividades if elem]

    def add_fecha_field(self):
        status_hrs_trabajadas_db = self.get_status_on_db()
        status_hrs_trabajadas = self.current_record['answers'].get(self.f['field_status_hrs_trabajadas'], '')
        if status_hrs_trabajadas_db == status_hrs_trabajadas:
            print('Status de horas trabajadas esta igual... no se calcula la hora')
            return True

        start_end_hrs_trabajadas = ('iniciar_actividad', 'terminar_actividad')
        start_end_ida = ('iniciar_ida', 'terminar_ida')
        start_end_regreso = ('iniciar_regreso', 'terminar_regreso')
        if status_hrs_trabajadas in start_end_hrs_trabajadas and self.current_record['answers'].get(self.f['modo_registro_horas']) == 'online':
            self.calculates_dates_group(self.f['grupo_horas_trabajadas'], status_hrs_trabajadas, start_end_hrs_trabajadas[0], start_end_hrs_trabajadas[1], self.f['field_id_inicio_actividad'], self.f['field_id_fin_actividad'])
        elif status_hrs_trabajadas in start_end_ida:
            self.calculates_dates_group(self.f['grupo_traslado_ida'], status_hrs_trabajadas, start_end_ida[0], start_end_ida[1], self.f['field_id_iniciar_ida'], self.f['field_id_terminar_ida'])
        elif status_hrs_trabajadas in start_end_regreso:
            self.calculates_dates_group(self.f['grupo_traslado_regreso'], status_hrs_trabajadas, start_end_regreso[0], start_end_regreso[1], self.f['field_id_iniciar_regreso'], self.f['field_id_terminar_regreso'])

    def calcula_gastos(self):
        opts, fields_subtotales, with_kilometraje, with_status = self.get_optios_and_fields_subtotales()
        print('fields_subtotales =',fields_subtotales)
        # Dejarlo funcionando dinamico para que busque el campo subtotal que le corresponda segun la opción y pegar ahi la sumatoria de los montos
        dict_opts_subts = { op: 0 for op in opts }
        for gasto in self.current_record['answers'].get(self.f['field_group_gastos'], []):
            tipo_gasto = gasto.get(self.f['field_select_tipo_gasto'], '')
            monto_gasto = gasto.get(self.f['field_monto_gasto'], 0)
            print(f'tipo_gasto = {tipo_gasto} monto_gasto = {monto_gasto}')
            if dict_opts_subts.get(tipo_gasto) or dict_opts_subts.get(tipo_gasto) == 0:
                dict_opts_subts[tipo_gasto] += monto_gasto
        print(dict_opts_subts)
        total_gastos = 0
        for subtotal_description, subtotal_value in dict_opts_subts.items():
            # if subtotal_value:
            total_gastos += subtotal_value
            self.current_record['answers'][ fields_subtotales[subtotal_description] ] = subtotal_value
        self.current_record['answers'][self.f['field_total_gastos']] = total_gastos
        self.current_record['answers'][self.f['field_saldo']] = self.current_record['answers'].get(self.f['field_anticipo'], 0) - total_gastos

        # Si la forma tiene el campo Total Kilometraje, tambien se deben hacer los calculos
        if with_kilometraje:
            self.current_record['answers'][self.f['field_kilometraje_total']] = self.current_record['answers'].get(self.f['field_kilometraje_final'],0) - self.current_record['answers'].get(self.f['field_kilometraje_inicial'],0)


        """
        Si la forma es Informe de servicio hay que pegar la fecha de actualizacion en el campo que corresponda
        """
        if with_status and self.current_record['answers'].get(self.f['modo_registro_horas']) == 'online':
            self.add_fecha_field()


        sys.stdout.write(simplejson.dumps({
            'status': 101,
            'replace_ans': self.current_record['answers']
        }))

    # ---- update_reasignado.py ----

    def update_reasignado(self):
        no_orden = self.answers.get(self.f['numero_orden'])
        id_forma = self.unlist( self.answers.get(self.FORMULARIOS_CAT_OBJ_ID, {}).get(self.f['id_formulario']) )
        print(f'-- No de orden = {no_orden} ID de la Forma = {id_forma}')

        # Se debe tener el folio y el id de la forma donde se buscara el registro
        if not no_orden or not id_forma:
            print('Se requiere el numero de orden y el id de la forma para continuar')
            return False

        # Se busca el registro con el folio y la forma
        record_found = self.get_record_from_db( int(id_forma), str(no_orden) )
        if not record_found:
            print('No se encontro el registro en la forma con el folio seleccionados')
            return False

        # Se va a actualizar el registro encontrado
        print('\n\n++ ++ record_found =',record_found)

        record_found['answers'].update({
            self.USUARIOS_CAT_OBJ_ID: self.answers.get(self.USUARIOS_CAT_OBJ_ID, {}), # usuario_asignado
            self.f['tipo_asignacion']: self.answers.get(self.f['tipo_asignacion']) # tipo_de_asignacion
        })

        resp_update = self.lkf_api.patch_record(record_found)
        print('\n resp_update =',resp_update)

    # ---- get_data_gastos.py ----

    #---Query
    def get_query_informe_servicio_gastos(self, date_from = None, date_to = None):
        match_query = { 
            "form_id": {'$in': [self.INFORME_SERVICIO, self.INFORME_SERVICIO_TALLER]},
            "deleted_at":{"$exists":False},
            f"answers.{self.f['field_group_gastos']}": {
                "$exists": True,
                "$ne": [],
            }
        }

        if date_from!='':
            date_from = datetime.strptime(f"{date_from} 00:00:00", "%Y-%m-%d %H:%M:%S")

        if date_to!='':
            date_to = datetime.strptime(f"{date_to} 23:59:59", "%Y-%m-%d %H:%M:%S")

        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field='created_at_ajustada'))

        query = [
            { "$addFields": {
                "created_at_ajustada": {
                    "$dateAdd": {
                        "startDate": "$created_at",
                        "unit": "minute",
                        "amount": "$tz_offset"
                    }
                }
            }},
            {"$match": match_query},
            {"$unwind": f"$answers.{self.f['field_group_gastos']}"},
            {"$project": {
                "_id":1,
                "folio":"$folio",
                "num_odt":f"$answers.{self.f['numero_orden']}",
                "tecnico": {
                    "$cond": {
                        "if": { "$isArray": f"$answers.{self.f['tecnicos_asignados']}.{self.EMPLEADOS_CAT_OBJ_ID}.{self.f['nombre_completo']}" },
                        "then": { "$arrayElemAt": [f"$answers.{self.f['tecnicos_asignados']}.{self.EMPLEADOS_CAT_OBJ_ID}.{self.f['nombre_completo']}", 0] },
                        "else": f"$answers.{self.f['tecnicos_asignados']}.{self.EMPLEADOS_CAT_OBJ_ID}.{self.f['nombre_completo']}"
                    }
                },
                "tipo_gasto":f"$answers.{self.f['field_group_gastos']}.{self.f['field_select_tipo_gasto']}",
                "monto":f"$answers.{self.f['field_group_gastos']}.{self.f['field_monto_gasto']}",
                "comprobante": {
                    "$arrayElemAt": [
                        f"$answers.{self.f['field_group_gastos']}.{self.f['comprobante_gasto']}.file_url",
                        0
                    ]
                }
            }},
            {"$sort": {"folio":1}}
        ]
        result = self.cr.aggregate(query)

        #----Format
        list_return = []
        for item in result:
            print('item=',item)
            list_return.append({
                'folio':item.get('folio',''),
                'num_odt':item.get('num_odt',''),
                'tecnico':item.get('tecnico',''),
                'tipo_gasto':item.get('tipo_gasto',''),
                'monto':item.get('monto',''),
                'comprobante':item.get('comprobante',''),
            })
        return list_return

    #---Query
    def get_query_comercial(self, date_from = None, date_to = None):
        match_query = { 
            "form_id": {'$in': [self.CARE_INSPECTION_CSR, self.GESTION_COMERCIAL_POSTVENTA, self.GESTION_COMERCIAL_VENTAS]},
            "deleted_at":{"$exists":False},
            f"answers.{self.f['field_group_gastos']}": {
                "$exists": True,
                "$ne": [],
            }
        }

        if date_from!='':
            date_from = datetime.strptime(f"{date_from} 00:00:00", "%Y-%m-%d %H:%M:%S")

        if date_to!='':
            date_to = datetime.strptime(f"{date_to} 23:59:59", "%Y-%m-%d %H:%M:%S")

        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field='created_at_ajustada'))


        query = [
            { "$addFields": {
                "created_at_ajustada": {
                    "$dateAdd": {
                        "startDate": "$created_at",
                        "unit": "minute",
                        "amount": "$tz_offset"
                    }
                }
            }},
            {"$match": match_query},
            {"$unwind": f"$answers.{self.f['field_group_gastos']}"},
            {"$project": {
                "_id":1,
                "folio":"$folio",
                "tipo_gasto":f"$answers.{self.f['field_group_gastos']}.{self.f['field_select_tipo_gasto']}",
                "monto":f"$answers.{self.f['field_group_gastos']}.{self.f['field_monto_gasto']}",
                "comprobante": {
                    "$arrayElemAt": [
                        f"$answers.{self.f['field_group_gastos']}.{self.f['comprobante_gasto']}.file_url",
                        0
                    ]
                }
            }},
            {"$sort": {"folio":1}}
        ]
        result = self.cr.aggregate(query)

        #----Format
        list_return = []
        for item in result:
            print('item=',item)
            list_return.append({
                'folio':item.get('folio',''),
                'tipo_gasto':item.get('tipo_gasto',''),
                'monto':item.get('monto',''),
                'comprobante':item.get('comprobante',''),
            })
        return list_return

    # ---- get_data_hours.py ----

    #---- Format
    def get_format_informe_servicio(self, data):
        data_response = []
        for item_record in data:
            dic_base = {
                'folio': item_record.get('folio',''),
                'no_orden': item_record.get('no_orden',''),
                'cliente': item_record.get('cliente',''),
                'trabajo_realizado': item_record.get('trabajo_realizado',''),
                'fecha_apertura': item_record.get('fecha_apertura',''),
                'fecha_atencion': item_record.get('trabajo_atencion',''),
            }
            #----Chasis
            option_data = item_record.get('option_data','')
            chasis_catalog = item_record.get('chasis_catalog','')
            chasis_text = item_record.get('chasis_text','')

            if option_data == 'Sí' or option_data == 'sí':
                dic_base['num_chasis'] = chasis_catalog
            elif option_data == 'No' or option_data == 'no':
                dic_base['num_chasis'] = chasis_text

            #----Tecnician
            tecnico = ''
            codigo_empleado = ''
            set_tecnico = item_record.get('set_tecnico','')
            if len(set_tecnico) > 0:
                tecnico = set_tecnico[0].get(self.EMPLEADOS_CAT_OBJ_ID,{}).get(self.f['nombre_completo'],'')
                codigo_empleado = set_tecnico[0].get(self.EMPLEADOS_CAT_OBJ_ID,{}).get(self.f['codigo_empleado'],'')

            dic_base['tecnico'] = tecnico

            if len(codigo_empleado) == 1:
                dic_base['codigo_empleado'] = codigo_empleado[0]
            else:
                dic_base['codigo_empleado'] = codigo_empleado

            #----Hours
            set_horas_traslado = item_record.get('set_horas_traslado',[])
            set_horas_trabajadas = item_record.get('set_horas_trabajadas',[])
            set_horas_regreso   = item_record.get('set_horas_regreso',[])


            if len(set_horas_traslado) > 0:
                for item_set in set_horas_traslado:
                    dic_item = dic_base.copy()  
                    date_start = item_set.get(self.f['field_id_iniciar_ida'],'')
                    date_end = item_set.get(self.f['field_id_terminar_ida'],'')

                    if date_start and date_end:
                        date_start = date_start.replace("/", "-")
                        if isinstance(date_start, str):
                            date_start_format = datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S")

                        date_end = date_end.replace("/", "-")
                        if isinstance(date_end, str):
                            date_end_format = datetime.strptime(date_end, "%Y-%m-%d %H:%M:%S")

                        diff = date_end_format - date_start_format
                        total_seconds = diff.total_seconds()
                        total_minutes = int(total_seconds // 60)

                        hours = total_minutes // 60
                        minutes = total_minutes % 60

                        time_job = f"{hours:02d}:{minutes:02d}"
                        hour_job = round(total_seconds / 3600, 2)

                        dic_item['fecha_inicio'] = date_start
                        dic_item['fecha_fin'] = date_end
                        dic_item['tiempo_trabajo'] = time_job
                        dic_item['horas_trabajo'] = hour_job
                        dic_item['tipo_hora'] = ''
                        dic_item['tipo_hora'] = 'Horas Traslado'
                        data_response.append(dic_item)

            if len(set_horas_trabajadas) > 0:
                for item_set in set_horas_trabajadas:
                    dic_item = dic_base.copy()  
                    date_start = item_set.get(self.f['field_id_inicio_actividad'],'')
                    date_end = item_set.get(self.f['field_id_fin_actividad'],'')

                    if date_start and date_end:

                        date_start = date_start.replace("/", "-")
                        if isinstance(date_start, str):
                            date_start_format = datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S")

                        date_end = date_end.replace("/", "-")
                        if isinstance(date_end, str):
                            date_end_format = datetime.strptime(date_end, "%Y-%m-%d %H:%M:%S")

                        diff = date_end_format - date_start_format
                        total_seconds = diff.total_seconds()
                        total_minutes = int(total_seconds // 60)

                        hours = total_minutes // 60
                        minutes = total_minutes % 60

                        time_job = f"{hours:02d}:{minutes:02d}"
                        hour_job = round(total_seconds / 3600, 2)

                        dic_item['fecha_inicio'] = date_start
                        dic_item['fecha_fin'] = date_end
                        dic_item['tiempo_trabajo'] = time_job
                        dic_item['horas_trabajo'] = hour_job
                        dic_item['tipo_hora'] = ''
                        dic_item['tipo_hora'] = 'Horas Trabajadas'
                        data_response.append(dic_item)

            if len(set_horas_regreso) > 0:
                for item_set in set_horas_regreso:
                    dic_item = dic_base.copy()  
                    date_start = item_set.get(self.f['field_id_iniciar_regreso'],'')
                    date_end = item_set.get(self.f['field_id_terminar_regreso'],'')

                    if date_start and date_end:

                        date_start = date_start.replace("/", "-")
                        if isinstance(date_start, str):
                            date_start_format = datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S")

                        date_end = date_end.replace("/", "-")
                        if isinstance(date_end, str):
                            date_end_format = datetime.strptime(date_end, "%Y-%m-%d %H:%M:%S")

                        diff = date_end_format - date_start_format
                        total_seconds = diff.total_seconds()
                        total_minutes = int(total_seconds // 60)

                        hours = total_minutes // 60
                        minutes = total_minutes % 60

                        time_job = f"{hours:02d}:{minutes:02d}"
                        hour_job = round(total_seconds / 3600, 2)

                        dic_item['fecha_inicio'] = date_start
                        dic_item['fecha_fin'] = date_end
                        dic_item['tiempo_trabajo'] = time_job
                        dic_item['horas_trabajo'] = hour_job
                        dic_item['tipo_hora'] = ''
                        dic_item['tipo_hora'] = 'Horas Regreso'
                        data_response.append(dic_item)


        return data_response

    def get_format_care_inspection(self, data):
        data_response = []
        for item_record in data:
            dic_base = {
                'folio': item_record.get('folio',''),
                'cliente': item_record.get('cliente',''),
                'trabajo_realizado': item_record.get('trabajo_realizado',''),
                'fecha_apertura': item_record.get('fecha_apertura',''),
                'trabajo_atencion': item_record.get('trabajo_atencion',''),
                'tecnico':item_record.get('tecnico',''),
                'codigo_empleado':item_record.get('codigo_empleado',''),
            }
            #----Chasis
            option_data = item_record.get('option_data','')
            chasis_catalog = item_record.get('chasis_catalog','')
            chasis_text = item_record.get('chasis_text','')

            if option_data == 'Sí' or option_data == 'sí':
                dic_base['num_chasis'] = chasis_catalog
            elif option_data == 'No' or option_data == 'no':
                dic_base['num_chasis'] = chasis_text

            #----Hours
            set_horas_traslado = item_record.get('set_horas_traslado',[])
            set_horas_trabajadas = item_record.get('set_horas_trabajadas',[])
            set_horas_regreso   = item_record.get('set_horas_regreso',[])

            if len(set_horas_traslado) > 0:
                for item_set in set_horas_traslado:
                    dic_item = dic_base.copy() 
                    date_start = item_set.get(self.f['field_id_iniciar_ida'],'')
                    date_end = item_set.get(self.f['field_id_terminar_ida'],'')

                    if date_start and date_end:
                        date_start = date_start.replace("/", "-")
                        if isinstance(date_start, str):
                            date_start_format = datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S")

                        date_end = date_end.replace("/", "-")
                        if isinstance(date_end, str):
                            date_end_format = datetime.strptime(date_end, "%Y-%m-%d %H:%M:%S")

                        diff = date_end_format - date_start_format
                        total_seconds = diff.total_seconds()
                        total_minutes = int(total_seconds // 60)

                        hours = total_minutes // 60
                        minutes = total_minutes % 60

                        time_job = f"{hours:02d}:{minutes:02d}"
                        hour_job = round(total_seconds / 3600, 2)

                        dic_item['fecha_inicio'] = date_start
                        dic_item['fecha_fin'] = date_end
                        dic_item['tiempo_trabajo'] = time_job
                        dic_item['horas_trabajo'] = hour_job
                        dic_item['tipo_hora'] = 'Horas Traslado'
                        data_response.append(dic_item)

            if len(set_horas_trabajadas) > 0:
                for item_set in set_horas_trabajadas:
                    dic_item = dic_base.copy() 
                    date_start = item_set.get(self.f['field_id_inicio_actividad'],'')
                    date_end = item_set.get(self.f['field_id_fin_actividad'],'')

                    if date_start and date_end:

                        date_start = date_start.replace("/", "-")
                        if isinstance(date_start, str):
                            date_start_format = datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S")

                        date_end = date_end.replace("/", "-")
                        if isinstance(date_end, str):
                            date_end_format = datetime.strptime(date_end, "%Y-%m-%d %H:%M:%S")

                        diff = date_end_format - date_start_format
                        total_seconds = diff.total_seconds()
                        total_minutes = int(total_seconds // 60)

                        hours = total_minutes // 60
                        minutes = total_minutes % 60

                        time_job = f"{hours:02d}:{minutes:02d}"
                        hour_job = round(total_seconds / 3600, 2)

                        dic_item['fecha_inicio'] = date_start
                        dic_item['fecha_fin'] = date_end
                        dic_item['tiempo_trabajo'] = time_job
                        dic_item['horas_trabajo'] = hour_job
                        dic_item['tipo_hora'] = 'Horas Trabajadas'
                        data_response.append(dic_item)

            if len(set_horas_regreso) > 0:
                for item_set in set_horas_regreso:
                    dic_item = dic_base.copy() 
                    date_start = item_set.get(self.f['field_id_iniciar_regreso'],'')
                    date_end = item_set.get(self.f['field_id_terminar_regreso'],'')

                    if date_start and date_end:

                        date_start = date_start.replace("/", "-")
                        if isinstance(date_start, str):
                            date_start_format = datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S")

                        date_end = date_end.replace("/", "-")
                        if isinstance(date_end, str):
                            date_end_format = datetime.strptime(date_end, "%Y-%m-%d %H:%M:%S")

                        diff = date_end_format - date_start_format
                        total_seconds = diff.total_seconds()
                        total_minutes = int(total_seconds // 60)

                        hours = total_minutes // 60
                        minutes = total_minutes % 60

                        time_job = f"{hours:02d}:{minutes:02d}"
                        hour_job = round(total_seconds / 3600, 2)

                        dic_item['fecha_inicio'] = date_start
                        dic_item['fecha_fin'] = date_end
                        dic_item['tiempo_trabajo'] = time_job
                        dic_item['horas_trabajo'] = hour_job
                        dic_item['tipo_hora'] = 'Horas Regreso'
                        data_response.append(dic_item)

        return data_response

    def get_format_salida_equipos(self, data):
        data_response = []
        for item_record in data:

            dic_base = {
                'folio': item_record.get('folio',''),
                'cliente': item_record.get('cliente',''),
                'trabajo_realizado': item_record.get('trabajo_realizado',''),
                'fecha_apertura': item_record.get('fecha_apertura',''),
                'trabajo_atencion': item_record.get('trabajo_atencion',''),
                'tecnico':item_record.get('tecnico',''),
                'codigo_empleado':item_record.get('codigo_empleado',''),
            }
            #----Chasis
            option_data = item_record.get('option_data','')
            chasis_catalog = item_record.get('chasis_catalog','')
            chasis_text = item_record.get('chasis_text','')

            if option_data == 'Sí' or option_data == 'sí':
                dic_base['num_chasis'] = chasis_catalog
            elif option_data == 'No' or option_data == 'no':
                dic_base['num_chasis'] = chasis_text

            #----Hours
            date_start = item_record.get('date_from','')
            date_end = item_record.get('date_to','')

            if date_start and date_end:
                date_start = date_start.replace("/", "-")
                if isinstance(date_start, str):
                    date_start_format = datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S")

                date_end = date_end.replace("/", "-")
                if isinstance(date_end, str):
                    date_end_format = datetime.strptime(date_end, "%Y-%m-%d %H:%M:%S")

                diff = date_end_format - date_start_format
                total_seconds = diff.total_seconds()
                total_minutes = int(total_seconds // 60)

                hours = total_minutes // 60
                minutes = total_minutes % 60

                time_job = f"{hours:02d}:{minutes:02d}"
                hour_job = round(total_seconds / 3600, 2)

                dic_base['fecha_inicio'] = date_start
                dic_base['fecha_fin'] = date_end
                dic_base['tiempo_trabajo'] = time_job
                dic_base['horas_trabajo'] = hour_job
                dic_base['tipo_hora'] = 'Horas Trabajadas'
                data_response.append(dic_base)
        return data_response

    def get_format_gestion_post_venta(self, data):
        data_response = []
        for item_record in data:
            dic_base = {
                'folio': item_record.get('folio',''),
                'cliente': item_record.get('cliente',''),
                'trabajo_realizado': item_record.get('trabajo_realizado',''),
                'fecha_apertura': item_record.get('fecha_apertura',''),
                'trabajo_atencion': item_record.get('trabajo_atencion',''),
                'tecnico':item_record.get('tecnico',''),
                'codigo_empleado':item_record.get('codigo_empleado',''),
                'resumen_gestion':item_record.get('resumen_gestion',''),
            }
            #----Chasis
            option_data = item_record.get('option_data','')
            chasis_catalog = item_record.get('chasis_catalog','')
            chasis_text = item_record.get('chasis_text','')

            if option_data == 'Sí' or option_data == 'sí':
                dic_base['num_chasis'] = chasis_catalog
            elif option_data == 'No' or option_data == 'no':
                dic_base['num_chasis'] = chasis_text

            #----Hours
            set_horas_traslado = item_record.get('set_horas_traslado',[])
            set_horas_trabajadas = item_record.get('set_horas_trabajadas',[])
            set_horas_regreso   = item_record.get('set_horas_regreso',[])

            if len(set_horas_traslado) > 0:
                for item_set in set_horas_traslado:
                    dic_item = dic_base.copy()
                    date_start = item_set.get(self.f['field_id_iniciar_ida'],'')
                    date_end = item_set.get(self.f['field_id_terminar_ida'],'')

                    if date_start and date_end:
                        date_start = date_start.replace("/", "-")
                        if isinstance(date_start, str):
                            date_start_format = datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S")

                        date_end = date_end.replace("/", "-")
                        if isinstance(date_end, str):
                            date_end_format = datetime.strptime(date_end, "%Y-%m-%d %H:%M:%S")

                        diff = date_end_format - date_start_format
                        total_seconds = diff.total_seconds()
                        total_minutes = int(total_seconds // 60)

                        hours = total_minutes // 60
                        minutes = total_minutes % 60

                        time_job = f"{hours:02d}:{minutes:02d}"
                        hour_job = round(total_seconds / 3600, 2)

                        dic_item['fecha_inicio'] = date_start
                        dic_item['fecha_fin'] = date_end
                        dic_item['tiempo_trabajo'] = time_job
                        dic_item['horas_trabajo'] = hour_job
                        dic_item['tipo_hora'] = 'Horas Traslado'
                        data_response.append(dic_item)

            if len(set_horas_trabajadas) > 0:
                for item_set in set_horas_trabajadas:
                    dic_item = dic_base.copy()
                    date_start = item_set.get(self.f['field_id_inicio_actividad'],'')
                    date_end = item_set.get(self.f['field_id_fin_actividad'],'')

                    if date_start and date_end:

                        date_start = date_start.replace("/", "-")
                        if isinstance(date_start, str):
                            date_start_format = datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S")

                        date_end = date_end.replace("/", "-")
                        if isinstance(date_end, str):
                            date_end_format = datetime.strptime(date_end, "%Y-%m-%d %H:%M:%S")

                        diff = date_end_format - date_start_format
                        total_seconds = diff.total_seconds()
                        total_minutes = int(total_seconds // 60)

                        hours = total_minutes // 60
                        minutes = total_minutes % 60

                        time_job = f"{hours:02d}:{minutes:02d}"
                        hour_job = round(total_seconds / 3600, 2)

                        dic_item['fecha_inicio'] = date_start
                        dic_item['fecha_fin'] = date_end
                        dic_item['tiempo_trabajo'] = time_job
                        dic_item['horas_trabajo'] = hour_job
                        dic_item['tipo_hora'] = 'Horas Trabajadas'
                        data_response.append(dic_item)

            if len(set_horas_regreso) > 0:
                for item_set in set_horas_regreso:
                    dic_item = dic_base.copy()
                    date_start = item_set.get(self.f['field_id_iniciar_regreso'],'')
                    date_end = item_set.get(self.f['field_id_terminar_regreso'],'')

                    if date_start and date_end:

                        date_start = date_start.replace("/", "-")
                        if isinstance(date_start, str):
                            date_start_format = datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S")

                        date_end = date_end.replace("/", "-")
                        if isinstance(date_end, str):
                            date_end_format = datetime.strptime(date_end, "%Y-%m-%d %H:%M:%S")

                        diff = date_end_format - date_start_format
                        total_seconds = diff.total_seconds()
                        total_minutes = int(total_seconds // 60)

                        hours = total_minutes // 60
                        minutes = total_minutes % 60

                        time_job = f"{hours:02d}:{minutes:02d}"
                        hour_job = round(total_seconds / 3600, 2)

                        dic_item['fecha_inicio'] = date_start
                        dic_item['fecha_fin'] = date_end
                        dic_item['tiempo_trabajo'] = time_job
                        dic_item['horas_trabajo'] = hour_job
                        dic_item['tipo_hora'] = 'Horas Regreso'
                        data_response.append(dic_item)

        return data_response

    def get_format_gestion_ventas(self, data):
        data_response = []
        for item_record in data:
            dic_base = {
                'folio': item_record.get('folio',''),
                'cliente': item_record.get('cliente',''),
                'trabajo_realizado': item_record.get('trabajo_realizado',''),
                'fecha_apertura': item_record.get('fecha_apertura',''),
                'trabajo_atencion': item_record.get('trabajo_atencion',''),
                'tecnico':item_record.get('tecnico',''),
                'codigo_empleado':item_record.get('codigo_empleado',''),
                'resumen_gestion':item_record.get('resumen_gestion',''),
            }
            #----Chasis
            option_data = item_record.get('option_data','')
            chasis_catalog = item_record.get('chasis_catalog','')
            chasis_text = item_record.get('chasis_text','')

            if option_data == 'Sí' or option_data == 'sí':
                dic_base['num_chasis'] = chasis_catalog
            elif option_data == 'No' or option_data == 'no':
                dic_base['num_chasis'] = chasis_text

            #----Hours
            set_horas_traslado = item_record.get('set_horas_traslado',[])
            set_horas_trabajadas = item_record.get('set_horas_trabajadas',[])
            set_horas_regreso   = item_record.get('set_horas_regreso',[])

            if len(set_horas_traslado) > 0:
                for item_set in set_horas_traslado:
                    dic_item = dic_base.copy()
                    date_start = item_set.get(self.f['field_id_iniciar_ida'],'')
                    date_end = item_set.get(self.f['field_id_terminar_ida'],'')

                    if date_start and date_end:
                        date_start = date_start.replace("/", "-")
                        if isinstance(date_start, str):
                            date_start_format = datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S")

                        date_end = date_end.replace("/", "-")
                        if isinstance(date_end, str):
                            date_end_format = datetime.strptime(date_end, "%Y-%m-%d %H:%M:%S")

                        diff = date_end_format - date_start_format
                        total_seconds = diff.total_seconds()
                        total_minutes = int(total_seconds // 60)

                        hours = total_minutes // 60
                        minutes = total_minutes % 60

                        time_job = f"{hours:02d}:{minutes:02d}"
                        hour_job = round(total_seconds / 3600, 2)

                        dic_item['fecha_inicio'] = date_start
                        dic_item['fecha_fin'] = date_end
                        dic_item['tiempo_trabajo'] = time_job
                        dic_item['horas_trabajo'] = hour_job
                        dic_item['tipo_hora'] = 'Horas Traslado'
                        data_response.append(dic_item)

            if len(set_horas_trabajadas) > 0:
                for item_set in set_horas_trabajadas:
                    dic_item = dic_base.copy()
                    date_start = item_set.get(self.f['field_id_inicio_actividad'],'')
                    date_end = item_set.get(self.f['field_id_fin_actividad'],'')

                    if date_start and date_end:

                        date_start = date_start.replace("/", "-")
                        if isinstance(date_start, str):
                            date_start_format = datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S")

                        date_end = date_end.replace("/", "-")
                        if isinstance(date_end, str):
                            date_end_format = datetime.strptime(date_end, "%Y-%m-%d %H:%M:%S")

                        diff = date_end_format - date_start_format
                        total_seconds = diff.total_seconds()
                        total_minutes = int(total_seconds // 60)

                        hours = total_minutes // 60
                        minutes = total_minutes % 60

                        time_job = f"{hours:02d}:{minutes:02d}"
                        hour_job = round(total_seconds / 3600, 2)

                        dic_item['fecha_inicio'] = date_start
                        dic_item['fecha_fin'] = date_end
                        dic_item['tiempo_trabajo'] = time_job
                        dic_item['horas_trabajo'] = hour_job
                        dic_item['tipo_hora'] = 'Horas Trabajadas'
                        data_response.append(dic_item)

            if len(set_horas_regreso) > 0:
                for item_set in set_horas_regreso:
                    dic_item = dic_base.copy()
                    date_start = item_set.get(self.f['field_id_iniciar_regreso'],'')
                    date_end = item_set.get(self.f['field_id_terminar_regreso'],'')

                    if date_start and date_end:

                        date_start = date_start.replace("/", "-")
                        if isinstance(date_start, str):
                            date_start_format = datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S")

                        date_end = date_end.replace("/", "-")
                        if isinstance(date_end, str):
                            date_end_format = datetime.strptime(date_end, "%Y-%m-%d %H:%M:%S")

                        diff = date_end_format - date_start_format
                        total_seconds = diff.total_seconds()
                        total_minutes = int(total_seconds // 60)

                        hours = total_minutes // 60
                        minutes = total_minutes % 60

                        time_job = f"{hours:02d}:{minutes:02d}"
                        hour_job = round(total_seconds / 3600, 2)

                        dic_item['fecha_inicio'] = date_start
                        dic_item['fecha_fin'] = date_end
                        dic_item['tiempo_trabajo'] = time_job
                        dic_item['horas_trabajo'] = hour_job
                        dic_item['tipo_hora'] = 'Horas Regreso'
                        data_response.append(dic_item)

        return data_response

    #---- Query
    def get_query_informe_servicio_hours(self, date_from, date_to, num_order):
        match_query = { 
            "form_id": self.INFORME_SERVICIO,
            "deleted_at": {"$exists": False},
        }
        if date_from!='':
            date_from = datetime.strptime(f"{date_from} 00:00:00", "%Y-%m-%d %H:%M:%S")

        if date_to!='':
            date_to = datetime.strptime(f"{date_to} 23:59:59", "%Y-%m-%d %H:%M:%S")

        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field='update_at_ajustada'))

        if num_order!='':
            match_query.update({f"answers.{self.f['numero_orden']}":num_order})

        query = [
            { "$addFields": {
                "update_at_ajustada": {
                    "$dateAdd": {
                        "startDate": "$updated_at",
                        "unit": "minute",
                        "amount": "$tz_offset"
                    }
                }
            }},
            {"$match": match_query},
            {"$project": {
                "_id":1,
                "folio":"$folio",
                "update_at_ajustada":"$update_at_ajustada",
                "no_orden":f"$answers.{self.f['numero_orden']}",
                "cliente": {
                    "$cond": {
                        "if": { "$isArray": f"$answers.{self.CLIENTES_CAT_OBJ_ID}.{self.f['razon_social']}" },
                        "then": { "$arrayElemAt": [f"$answers.{self.CLIENTES_CAT_OBJ_ID}.{self.f['razon_social']}", 0] },
                        "else": f"$answers.{self.CLIENTES_CAT_OBJ_ID}.{self.f['razon_social']}"
                    }
                },
                "option_data":f"$answers.{self.f['equipo_registrado']}",
                "chasis_catalog": {
                    "$cond": {
                        "if": { "$isArray": f"$answers.{self.ACTIVOS_FIJOS_CAT_OBJ_ID}.{self.f['chasis']}" },
                        "then": { "$arrayElemAt": [f"$answers.{self.ACTIVOS_FIJOS_CAT_OBJ_ID}.{self.f['chasis']}", 0] },
                        "else": f"$answers.{self.ACTIVOS_FIJOS_CAT_OBJ_ID}.{self.f['chasis']}"
                    }
                },
                "chasis_text":f"$answers.{self.f['especifique_serie']}",
                "trabajo_realizado":f"$answers.{self.f['detalle_trabajos_realizados']}",
                "fecha_apertura":f"$answers.{self.f['fecha_apertura']}",
                "trabajo_atencion":f"$answers.{self.f['fecha_atencion']}",
                "set_horas_traslado":f"$answers.{self.f['grupo_traslado_ida']}",
                "set_horas_trabajadas":f"$answers.{self.f['grupo_horas_trabajadas']}",
                "set_horas_regreso":f"$answers.{self.f['grupo_traslado_regreso']}",
                "set_tecnico":f"$answers.{self.f['tecnicos_asignados']}",
            }},
            {"$sort": {"folio":1}}
        ]
        result = self.cr.aggregate(query)
        result_format = self.get_format_informe_servicio(result)
        return result_format

    def get_query_care_inspection(self, date_from, date_to):
        match_query = { 
            "form_id": self.CARE_INSPECTION_CSR,
            "deleted_at": {"$exists": False},
        }
        if date_from!='':
            date_from = datetime.strptime(f"{date_from} 00:00:00", "%Y-%m-%d %H:%M:%S")

        if date_to!='':
            date_to = datetime.strptime(f"{date_to} 23:59:59", "%Y-%m-%d %H:%M:%S")

        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field='update_at_ajustada'))

        query = [
            { "$addFields": {
                "update_at_ajustada": {
                    "$dateAdd": {
                        "startDate": "$updated_at",
                        "unit": "minute",
                        "amount": "$tz_offset"
                    }
                }
            }},
            {"$match": match_query},
            {"$project": {
                "_id":1,
                "folio":"$folio",
                "cliente": {
                    "$cond": {
                        "if": { "$isArray": f"$answers.{self.CLIENTES_CAT_OBJ_ID}.{self.f['razon_social']}" },
                        "then": { "$arrayElemAt": [f"$answers.{self.CLIENTES_CAT_OBJ_ID}.{self.f['razon_social']}", 0] },
                        "else": f"$answers.{self.CLIENTES_CAT_OBJ_ID}.{self.f['razon_social']}"
                    }
                },
                "tecnico": {
                    "$cond": {
                        "if": { "$isArray": f"$answers.{self.EMPLEADOS_CAT_OBJ_ID}.{self.f['nombre_completo']}" },
                        "then": { "$arrayElemAt": [f"$answers.{self.EMPLEADOS_CAT_OBJ_ID}.{self.f['nombre_completo']}", 0] },
                        "else": f"$answers.{self.EMPLEADOS_CAT_OBJ_ID}.{self.f['nombre_completo']}"
                    }
                },
                "codigo_empleado": {
                    "$cond": {
                        "if": { "$isArray": f"$answers.{self.EMPLEADOS_CAT_OBJ_ID}.{self.f['codigo_empleado']}" },
                        "then": { "$arrayElemAt": [f"$answers.{self.EMPLEADOS_CAT_OBJ_ID}.{self.f['codigo_empleado']}", 0] },
                        "else": f"$answers.{self.EMPLEADOS_CAT_OBJ_ID}.{self.f['codigo_empleado']}"
                    }
                },
                "option_data":f"$answers.{self.f['equipo_registrado']}",
                "chasis_catalog": {
                    "$cond": {
                        "if": { "$isArray": f"$answers.{self.ACTIVOS_FIJOS_CAT_OBJ_ID}.{self.f['chasis']}" },
                        "then": { "$arrayElemAt": [f"$answers.{self.ACTIVOS_FIJOS_CAT_OBJ_ID}.{self.f['chasis']}", 0] },
                        "else": f"$answers.{self.ACTIVOS_FIJOS_CAT_OBJ_ID}.{self.f['chasis']}"
                    }
                },
                "chasis_text":f"$answers.{self.f['especifique_serie']}",
                "trabajo_realizado":f"$answers.{self.f['comentarios_generales']}",
                "fecha_apertura":f"$answers.{self.f['fecha_apertura']}",
                "trabajo_atencion":f"$answers.{self.f['fecha_atencion']}",
                "set_horas_traslado":f"$answers.{self.f['grupo_traslado_ida']}",
                "set_horas_trabajadas":f"$answers.{self.f['grupo_horas_trabajadas']}",
                "set_horas_regreso":f"$answers.{self.f['grupo_traslado_regreso']}",
            }},
            {"$sort": {"folio":1}}
        ]
        result = self.cr.aggregate(query)
        result_format = self.get_format_care_inspection(result)
        return result_format

    def get_query_entrada_salida_equipos(self, date_from, date_to, num_order):
        match_query = { 
            "form_id": self.ENTRADA_SALIDA_EQUIPOS,
            "deleted_at": {"$exists": False},
        }
        if date_from!='':
            date_from = datetime.strptime(f"{date_from} 00:00:00", "%Y-%m-%d %H:%M:%S")

        if date_to!='':
            date_to = datetime.strptime(f"{date_to} 23:59:59", "%Y-%m-%d %H:%M:%S")

        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field='update_at_ajustada'))

        if num_order!='':
            match_query.update({f"answers.{self.f['numero_orden']}":num_order})

        query = [
            { "$addFields": {
                "update_at_ajustada": {
                    "$dateAdd": {
                        "startDate": "$updated_at",
                        "unit": "minute",
                        "amount": "$tz_offset"
                    }
                }
            }},
            {"$match": match_query},
            {"$project": {
                "_id":1,
                "folio":"$folio",
                "no_orden":f"$answers.{self.f['numero_orden']}",
                "cliente": {
                    "$cond": {
                        "if": { "$isArray": f"$answers.{self.CLIENTES_CAT_OBJ_ID}.{self.f['razon_social']}" },
                        "then": { "$arrayElemAt": [f"$answers.{self.CLIENTES_CAT_OBJ_ID}.{self.f['razon_social']}", 0] },
                        "else": f"$answers.{self.CLIENTES_CAT_OBJ_ID}.{self.f['razon_social']}"
                    }
                },
                "tecnico": {
                    "$cond": {
                        "if": { "$isArray": f"$answers.{self.EMPLEADOS_CAT_OBJ_ID}.{self.f['nombre_completo']}" },
                        "then": { "$arrayElemAt": [f"$answers.{self.EMPLEADOS_CAT_OBJ_ID}.{self.f['nombre_completo']}", 0] },
                        "else": f"$answers.{self.EMPLEADOS_CAT_OBJ_ID}.{self.f['nombre_completo']}"
                    }
                },
                "codigo_empleado": {
                    "$cond": {
                        "if": { "$isArray": f"$answers.{self.EMPLEADOS_CAT_OBJ_ID}.{self.f['codigo_empleado']}" },
                        "then": { "$arrayElemAt": [f"$answers.{self.EMPLEADOS_CAT_OBJ_ID}.{self.f['codigo_empleado']}", 0] },
                        "else": f"$answers.{self.EMPLEADOS_CAT_OBJ_ID}.{self.f['codigo_empleado']}"
                    }
                },
                "option_data":f"$answers.{self.f['equipo_registrado']}",
                "chasis_catalog": {
                    "$cond": {
                        "if": { "$isArray": f"$answers.{self.ACTIVOS_FIJOS_CAT_OBJ_ID}.{self.f['chasis']}" },
                        "then": { "$arrayElemAt": [f"$answers.{self.ACTIVOS_FIJOS_CAT_OBJ_ID}.{self.f['chasis']}", 0] },
                        "else": f"$answers.{self.ACTIVOS_FIJOS_CAT_OBJ_ID}.{self.f['chasis']}"
                    }
                },
                "chasis_text":f"$answers.{self.f['especifique_serie']}",
                "trabajo_realizado":f"$answers.{self.f['comentarios_generales']}",
                "fecha_apertura":f"$answers.{self.f['fecha_apertura']}",
                "trabajo_atencion":f"$answers.{self.f['fecha_atencion']}",
                "date_from":f"$answers.{self.f['field_id_iniciar_ida']}",
                "date_to":f"$answers.{self.f['field_id_terminar_ida']}",
            }},
            {"$sort": {"folio":1}}
        ]
        result = self.cr.aggregate(query)
        result_format = self.get_format_salida_equipos(result)
        return result_format

    def get_query_gestion_post_venta(self, date_from, date_to):
        match_query = { 
            "form_id": self.GESTION_COMERCIAL_POSTVENTA,
            "deleted_at": {"$exists": False},
        }
        if date_from!='':
            date_from = datetime.strptime(f"{date_from} 00:00:00", "%Y-%m-%d %H:%M:%S")

        if date_to!='':
            date_to = datetime.strptime(f"{date_to} 23:59:59", "%Y-%m-%d %H:%M:%S")

        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field='update_at_ajustada'))

        query = [
            { "$addFields": {
                "update_at_ajustada": {
                    "$dateAdd": {
                        "startDate": "$updated_at",
                        "unit": "minute",
                        "amount": "$tz_offset"
                    }
                }
            }},
            {"$match": match_query},
            {"$project": {
                "_id":1,
                "folio":"$folio",
                "cliente": {
                    "$cond": {
                        "if": { "$isArray": f"$answers.{self.CLIENTES_CAT_OBJ_ID}.{self.f['razon_social']}" },
                        "then": { "$arrayElemAt": [f"$answers.{self.CLIENTES_CAT_OBJ_ID}.{self.f['razon_social']}", 0] },
                        "else": f"$answers.{self.CLIENTES_CAT_OBJ_ID}.{self.f['razon_social']}"
                    }
                },
                "tecnico": {
                    "$cond": {
                        "if": { "$isArray": f"$answers.{self.EMPLEADOS_CAT_OBJ_ID}.{self.f['nombre_completo']}" },
                        "then": { "$arrayElemAt": [f"$answers.{self.EMPLEADOS_CAT_OBJ_ID}.{self.f['nombre_completo']}", 0] },
                        "else": f"$answers.{self.EMPLEADOS_CAT_OBJ_ID}.{self.f['nombre_completo']}"
                    }
                },
                "codigo_empleado": {
                    "$cond": {
                        "if": { "$isArray": f"$answers.{self.EMPLEADOS_CAT_OBJ_ID}.{self.f['codigo_empleado']}" },
                        "then": { "$arrayElemAt": [f"$answers.{self.EMPLEADOS_CAT_OBJ_ID}.{self.f['codigo_empleado']}", 0] },
                        "else": f"$answers.{self.EMPLEADOS_CAT_OBJ_ID}.{self.f['codigo_empleado']}"
                    }
                },
                "option_data":f"$answers.{self.f['equipo_registrado']}",
                "chasis_catalog": {
                    "$cond": {
                        "if": { "$isArray": f"$answers.{self.ACTIVOS_FIJOS_CAT_OBJ_ID}.{self.f['chasis']}" },
                        "then": { "$arrayElemAt": [f"$answers.{self.ACTIVOS_FIJOS_CAT_OBJ_ID}.{self.f['chasis']}", 0] },
                        "else": f"$answers.{self.ACTIVOS_FIJOS_CAT_OBJ_ID}.{self.f['chasis']}"
                    }
                },
                "chasis_text":f"$answers.{self.f['especifique_serie']}",
                "trabajo_realizado":f"$answers.{self.f['trabajo_a_realizar']}",
                "fecha_apertura":f"$answers.{self.f['fecha_apertura']}",
                "trabajo_atencion":f"$answers.{self.f['fecha_atencion']}",
                "resumen_gestion":f"$answers.{self.f['resumen_gestion']}",
                "set_horas_traslado":f"$answers.{self.f['grupo_traslado_ida']}",
                "set_horas_trabajadas":f"$answers.{self.f['grupo_horas_trabajadas']}",
                "set_horas_regreso":f"$answers.{self.f['grupo_traslado_regreso']}",
            }},
            {"$sort": {"folio":1}}
        ]
        result = self.cr.aggregate(query)
        result_format = self.get_format_gestion_post_venta(result)
        return result_format

    def get_query_gestion_ventas(self, date_from, date_to):
        match_query = { 
            "form_id": self.GESTION_COMERCIAL_VENTAS,
            "deleted_at": {"$exists": False},
        }
        if date_from!='':
            date_from = datetime.strptime(f"{date_from} 00:00:00", "%Y-%m-%d %H:%M:%S")

        if date_to!='':
            date_to = datetime.strptime(f"{date_to} 23:59:59", "%Y-%m-%d %H:%M:%S")

        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field='update_at_ajustada'))

        query = [
            { "$addFields": {
                "update_at_ajustada": {
                    "$dateAdd": {
                        "startDate": "$updated_at",
                        "unit": "minute",
                        "amount": "$tz_offset"
                    }
                }
            }},
            {"$match": match_query},
            {"$project": {
                "_id":1,
                "folio":"$folio",
                "update_at_ajustada":"$update_at_ajustada",
                "cliente": {
                    "$cond": {
                        "if": { "$isArray": f"$answers.{self.CLIENTES_CAT_OBJ_ID}.{self.f['razon_social']}" },
                        "then": { "$arrayElemAt": [f"$answers.{self.CLIENTES_CAT_OBJ_ID}.{self.f['razon_social']}", 0] },
                        "else": f"$answers.{self.CLIENTES_CAT_OBJ_ID}.{self.f['razon_social']}"
                    }
                },
                "tecnico": {
                    "$cond": {
                        "if": { "$isArray": f"$answers.{self.EMPLEADOS_CAT_OBJ_ID}.{self.f['nombre_completo']}" },
                        "then": { "$arrayElemAt": [f"$answers.{self.EMPLEADOS_CAT_OBJ_ID}.{self.f['nombre_completo']}", 0] },
                        "else": f"$answers.{self.EMPLEADOS_CAT_OBJ_ID}.{self.f['nombre_completo']}"
                    }
                },
                "codigo_empleado": {
                    "$cond": {
                        "if": { "$isArray": f"$answers.{self.EMPLEADOS_CAT_OBJ_ID}.{self.f['codigo_empleado']}" },
                        "then": { "$arrayElemAt": [f"$answers.{self.EMPLEADOS_CAT_OBJ_ID}.{self.f['codigo_empleado']}", 0] },
                        "else": f"$answers.{self.EMPLEADOS_CAT_OBJ_ID}.{self.f['codigo_empleado']}"
                    }
                },
                "option_data":f"$answers.{self.f['equipo_registrado']}",
                "chasis_catalog": {
                    "$cond": {
                        "if": { "$isArray": f"$answers.{self.ACTIVOS_FIJOS_CAT_OBJ_ID}.{self.f['chasis']}" },
                        "then": { "$arrayElemAt": [f"$answers.{self.ACTIVOS_FIJOS_CAT_OBJ_ID}.{self.f['chasis']}", 0] },
                        "else": f"$answers.{self.ACTIVOS_FIJOS_CAT_OBJ_ID}.{self.f['chasis']}"
                    }
                },
                "chasis_text":f"$answers.{self.f['especifique_serie']}",
                "trabajo_realizado":f"$answers.{self.f['trabajo_a_realizar']}",
                "fecha_apertura":f"$answers.{self.f['fecha_apertura']}",
                "trabajo_atencion":f"$answers.{self.f['fecha_atencion']}",
                "resumen_gestion":f"$answers.{self.f['resumen_gestion']}",
                "set_horas_traslado":f"$answers.{self.f['grupo_traslado_ida']}",
                "set_horas_trabajadas":f"$answers.{self.f['grupo_horas_trabajadas']}",
                "set_horas_regreso":f"$answers.{self.f['grupo_traslado_regreso']}",
            }},
            {"$sort": {"folio":1}}
        ]
        result = self.cr.aggregate(query)
        result_format = self.get_format_gestion_ventas(result)
        return result_format

    # ---- script_event_records.py ----

    #---Records
    def created_record(self, information):
        #--Value Informatio General
        date = information.get('eventDate','')
        contac = information.get('inputNameContac','')
        phone = information.get('inputPhone','')
        job = information.get('inputTextJob','')
        checklist = information.get('inputCheck','')
        order = information.get('inputTextOrden','')
        user = information.get('inputUser','')
        user_job = information.get('dicUser',{}).get('puesto','')
        user_email = information.get('dicUser',{}).get('email','')
        name_client = information.get('dicClient',{}).get('nombre_comercial','')
        ruc_client = information.get('dicClient',{}).get('ruc','')
        company_name = information.get('dicClient',{}).get('razon_social','')

        dic_create = {
            self.f['fecha_servicio'] : date, 
            self.f['nombre_contacto']:contac,
            self.f['celular_contacto']:phone,
            self.f['trabajo_a_realizar']:job,
            self.FORMULARIOS_CAT_OBJ_ID:{
                self.f['tipo_de_informe']:checklist,
            },
            self.f['estatus']:'pendiente',
            self.f['numero_orden']:order,
            self.USUARIOS_CAT_OBJ_ID:{
                self.f['nombre_usuario']:user,
                self.f['email_usuario']:[user_email],
                self.f['puesto_usuario']:[user_job],
            },
            self.CLIENTES_CAT_OBJ_ID:{
                self.f['razon_social']:name_client,
                self.f['ruc']:[ruc_client],
                self.f['nombre_comercial']:[company_name],
            }
        }


        #--Value Information Item
        check_yes = information.get('checkItemYes','')
        check_no = information.get('checkItemNo','')

        if check_yes!= '' and check_yes =='on':
            chasis = information.get('dicItem',{}).get('chasis','')
            marca = information.get('dicItem',{}).get('marca','')
            modelo = information.get('dicItem',{}).get('modelo','')
            categoria = information.get('dicItem',{}).get('categoria','')
            nombre = information.get('dicItem',{}).get('nombre_equipo','')
            motor_1 = information.get('dicItem',{}).get('motor_1','')
            status = information.get('dicItem',{}).get('status','')
            estado = information.get('dicItem',{}).get('estado','')
            dic_answers = {
                self.f['equipo_registrado']:'sí',
                self.ACTIVOS_FIJOS_CAT_OBJ_ID:{
                    self.f['chasis']:chasis,
                    self.f['marca']:[marca],
                    self.f['modelo']:[modelo],
                    self.f['categoria']:[categoria],
                    self.f['nombre_equipo']:[nombre],
                    self.f['horometro_motor_1']:[motor_1],
                    self.f['activo_estatus']:[status],
                    self.f['estado_equipo']:[estado],
                }
            }
            dic_create.update(dic_answers)

        elif check_no!= '' and check_no =='on':
            item = information.get('inputTextItem','')
            brand = information.get('inputTextBrand','')
            model = information.get('InputTextModel','')
            serie = information.get('inputTextSerie','')

            dic_answers = {
                self.f['equipo_registrado']:'no',
                self.f['especifique_equipo']:item,
                self.f['especifique_marca']:brand,
                self.f['especifique_modelo']:model,
                self.f['especifique_serie']:serie,
            }
            dic_create.update(dic_answers)

        #----Creation record
        metadata = self.lkf_api.get_metadata(self.PROGRAMACION_SERVICIOS)
        metadata['answers'] = dic_create
        resp_create = self.lkf_api.post_forms_answers_list(metadata)
        status_request = '400'
        if len(resp_create) == 1:
            status_request = resp_create[0].get('status_code','400')
        return status_request

    def get_information_catalogs(self):
        dic_response = {
            'catalog_client':[],
            'catalog_items':[],
            'catalog_checklist':[],
            'catalog_usuarios':[],
        }

        mango_query = {"selector":
            {"answers":
                {"$and":[{ 'deleted_at':{"$exists":False},}]}
            },
            "limit":10000,
            "skip":0
        }

        catalog_clientes = self.lkf_api.search_catalog(self.CLIENTES_CAT_ID, mango_query)
        for item in catalog_clientes:
           razon_social = item.get(self.f['razon_social'],'')
           nombre_comercial = item.get(self.f['nombre_comercial'],'')
           ruc = item.get(self.f['ruc'],'')
           dic_response['catalog_client'].append({
                'razon_social':razon_social,
                'nombre_comercial':nombre_comercial,
                'ruc':ruc,
            })

        catalog_equipos = self.lkf_api.search_catalog(self.ACTIVOS_FIJOS_CAT_ID, mango_query)
        for item in catalog_equipos:
            chasis = item.get(self.f['chasis'],'')
            status = item.get(self.f['estatus'],'')
            marca = item.get(self.f['marca'],'')
            modelo = item.get(self.f['modelo'],'')
            categoria = item.get(self.f['categoria'],'')
            motor_1 = item.get(self.f['horometro_motor_1'],'')
            nombre_equipo = item.get(self.f['nombre_equipo'],'')
            estado = item.get(self.f['estado_equipo'],'')
            dic_response['catalog_items'].append({
                'chasis':chasis,
                'status':status,
                'marca':marca,
                'modelo':modelo,
                'categoria':categoria,
                'motor_1':motor_1,
                'nombre_equipo':nombre_equipo,
                'estado':estado,
            })

        catalog_checklist = self.lkf_api.search_catalog(self.FORMULARIOS_CAT_ID, mango_query)
        for item in catalog_checklist:
            checklist = item.get(self.f['tipo_de_informe'],'')
            id_check = item.get(self.f['id_formulario'],0)
            dic_response['catalog_checklist'].append({
                'checklist':checklist,
                'id_check':id_check,
            })

        catalog_usuarios = self.lkf_api.search_catalog(self.USUARIOS_CAT_ID, mango_query)
        for item in catalog_usuarios:
            nombre = item.get(self.f['nombre_usuario'],'')
            email = item.get(self.f['email_usuario'],'')
            puesto = item.get(self.f['puesto_usuario'],'')
            dic_response['catalog_usuarios'].append({
                'nombre':nombre,
                'email':email,
                'puesto':puesto,
            })

        return dic_response

    #---Query
    def get_query_events(self, gestor = None , cliente = None):
        match_query = { 
            "form_id": self.PROGRAMACION_SERVICIOS,
            "deleted_at":{"$exists":False},
        }
        if gestor and '--' not in  gestor:
            match_query.update({f"answers.{self.USUARIOS_CAT_OBJ_ID}.{self.f['nombre_usuario']}": gestor})

        if cliente and '--' not in cliente:
            match_query.update({f"answers.{self.CLIENTES_CAT_OBJ_ID}.{self.f['razon_social']}":cliente })

        query = [
            {"$match": match_query},
            {"$project": {
                "_id":1,
                "folio":"$folio",
                "fecha_servicio":f"$answers.{self.f['fecha_servicio']}",
                "cliente":f"$answers.{self.CLIENTES_CAT_OBJ_ID}.{self.f['razon_social']}",
                "contacto":f"$answers.{self.f['nombre_contacto']}",
                "celular":f"$answers.{self.f['celular_contacto']}",
                "check_equipo":f"$answers.{self.f['equipo_registrado']}",
                "catalog_serie":f"$answers.{self.ACTIVOS_FIJOS_CAT_OBJ_ID}.{self.f['chasis']}",
                "input_equipo":f"$answers.{self.f['especifique_equipo']}",
                "input_marca":f"$answers.{self.f['especifique_marca']}",
                "input_modelo":f"$answers.{self.f['especifique_modelo']}",
                "input_serie":f"$answers.{self.f['especifique_serie']}",
                "trabajo_area":f"$answers.{self.f['trabajo_a_realizar']}",
                "check_list":f"$answers.{self.FORMULARIOS_CAT_OBJ_ID}.{self.f['tipo_de_informe']}",
                "status":f"$answers.{self.f['estatus']}",
            }},
            {"$sort": {"fecha_servicio":1}}
        ]
        result = self.cr.aggregate(query)
        result_format = self.format_query_events(result)
        return result_format

    def format_query_events(self, data):
        list_response = []
        for item in data:
            folio = item.get('folio','')
            fecha_servicio = item.get('fecha_servicio','')
            cliente = item.get('cliente','')

            contacto = item.get('contacto','')
            celular = item.get('celular','')
            check_equipo = item.get('check_equipo','')
            catalog_serie = item.get('catalog_serie','')
            input_equipo = item.get('input_equipo','')
            input_marca = item.get('input_marca','')
            input_modelo = item.get('input_modelo','')
            input_serie = item.get('input_serie','')
            trabajo_area = item.get('trabajo_area','')
            check_list = item.get('check_list','')
            status = item.get('status','').title()

            list_response.append({
                'id':folio,
                'title':cliente,
                'start':fecha_servicio,
                'allDay': 'true',
                'editable':'false',
                'extendedProps': {       
                    'contacto':contacto,
                    'celular':celular,
                    'check_equipo':check_equipo,
                    'catalog_serie':catalog_serie,
                    'input_equipo':input_equipo,
                    'input_marca':input_marca,
                    'input_modelo':input_modelo,
                    'input_serie':input_serie,
                    'trabajo_area':trabajo_area,
                    'check_list':check_list,
                    'status':status,
                }
            })

        return list_response
