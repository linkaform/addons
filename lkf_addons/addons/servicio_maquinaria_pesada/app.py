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
        if status_hrs_trabajadas in start_end_hrs_trabajadas and self.current_record['answers'].get('6736968ee7be2602ca566376') == 'online':
            self.calculates_dates_group('c00000000000000000000003', status_hrs_trabajadas, start_end_hrs_trabajadas[0], start_end_hrs_trabajadas[1], self.f['field_id_inicio_actividad'], self.f['field_id_fin_actividad'])
        elif status_hrs_trabajadas in start_end_ida:
            self.calculates_dates_group('c00000000000000000000021', status_hrs_trabajadas, start_end_ida[0], start_end_ida[1], self.f['field_id_iniciar_ida'], self.f['field_id_terminar_ida'])
        elif status_hrs_trabajadas in start_end_regreso:
            self.calculates_dates_group('c00000000000000000000022', status_hrs_trabajadas, start_end_regreso[0], start_end_regreso[1], self.f['field_id_iniciar_regreso'], self.f['field_id_terminar_regreso'])

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
        Si la forma es Informe de servicio (119972) hay que pegar la fecha de actualizacion en el campo que corresponda
        """
        if with_status and self.current_record['answers'].get('6736968ee7be2602ca566376') == 'online':
            self.add_fecha_field()


        sys.stdout.write(simplejson.dumps({
            'status': 101,
            'replace_ans': self.current_record['answers']
        }))

    # ---- update_reasignado.py ----

    def update_reasignado(self):
        no_orden = self.answers.get('672e8edfd2f1f131c66505d9')
        id_forma = self.unlist( self.answers.get('672eb39a4d20582177b00a05', {}).get('672eb39a4d20582177b00a07') )
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
            '670f50c7f522b590fbfd91eb': self.answers.get('670f50c7f522b590fbfd91eb', {}), # usuario_asignado
            '672eb5efd1134f9aca98da36': self.answers.get('672eb5efd1134f9aca98da36') # tipo_de_asignacion
        })

        resp_update = self.lkf_api.patch_record(record_found)
        print('\n resp_update =',resp_update)

    # ---- get_data_gastos.py ----

    #---Query
    def get_query_informe_servicio_gastos(self, date_from = None, date_to = None):
        match_query = { 
            "form_id": {'$in': [119972, 120422]},
            "deleted_at":{"$exists":False},
            "answers.6675b286b258d3517a03e8c7": {
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
            {"$unwind": "$answers.6675b286b258d3517a03e8c7"},
            {"$project": {
                "_id":1,
                "folio":"$folio",
                "num_odt":"$answers.672e8edfd2f1f131c66505d9",
                "tecnico": {
                    "$cond": {
                        "if": { "$isArray": "$answers.666a160967bcb9e23b1cc967.66707634e674c20724d85969.62c5ff407febce07043024dd" },
                        "then": { "$arrayElemAt": ["$answers.666a160967bcb9e23b1cc967.66707634e674c20724d85969.62c5ff407febce07043024dd", 0] },
                        "else": "$answers.666a160967bcb9e23b1cc967.66707634e674c20724d85969.62c5ff407febce07043024dd"
                    }
                },
                "tipo_gasto":"$answers.6675b286b258d3517a03e8c7.6686ebc5e9dfa385bfabad81",
                "monto":"$answers.6675b286b258d3517a03e8c7.a00000000000000000000001",
                "comprobante": {
                    "$arrayElemAt": [
                        "$answers.6675b286b258d3517a03e8c7.6686ebc5e9dfa385bfabad83.file_url",
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
            "form_id": {'$in': [120576,124648,124649]},
            "deleted_at":{"$exists":False},
            "answers.6675b286b258d3517a03e8c7": {
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
            {"$unwind": "$answers.6675b286b258d3517a03e8c7"},
            {"$project": {
                "_id":1,
                "folio":"$folio",
                "tipo_gasto":"$answers.6675b286b258d3517a03e8c7.6686ebc5e9dfa385bfabad81",
                "monto":"$answers.6675b286b258d3517a03e8c7.a00000000000000000000001",
                "comprobante": {
                    "$arrayElemAt": [
                        "$answers.6675b286b258d3517a03e8c7.6686ebc5e9dfa385bfabad83.file_url",
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
                tecnico = set_tecnico[0].get('66707634e674c20724d85969',{}).get('62c5ff407febce07043024dd','')
                codigo_empleado = set_tecnico[0].get('66707634e674c20724d85969',{}).get('670f585bf844ff7bc357b1dc','')

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
                    date_start = item_set.get('c00000000000000000000001','')
                    date_end = item_set.get('c00000000000000000000002','')

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
                    date_start = item_set.get('c00000000000000000000004','')
                    date_end = item_set.get('c00000000000000000000005','')

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
                    date_start = item_set.get('c00000000000000000000006','')
                    date_end = item_set.get('c00000000000000000000007','')

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
                    date_start = item_set.get('c00000000000000000000001','')
                    date_end = item_set.get('c00000000000000000000002','')

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
                    date_start = item_set.get('c00000000000000000000004','')
                    date_end = item_set.get('c00000000000000000000005','')

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
                    date_start = item_set.get('c00000000000000000000006','')
                    date_end = item_set.get('c00000000000000000000007','')

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
                    date_start = item_set.get('c00000000000000000000001','')
                    date_end = item_set.get('c00000000000000000000002','')

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
                    date_start = item_set.get('c00000000000000000000004','')
                    date_end = item_set.get('c00000000000000000000005','')

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
                    date_start = item_set.get('c00000000000000000000006','')
                    date_end = item_set.get('c00000000000000000000007','')

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
                    date_start = item_set.get('c00000000000000000000001','')
                    date_end = item_set.get('c00000000000000000000002','')

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
                    date_start = item_set.get('c00000000000000000000004','')
                    date_end = item_set.get('c00000000000000000000005','')

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
                    date_start = item_set.get('c00000000000000000000006','')
                    date_end = item_set.get('c00000000000000000000007','')

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
            "form_id": 119972,
            "deleted_at": {"$exists": False},
        }
        if date_from!='':
            date_from = datetime.strptime(f"{date_from} 00:00:00", "%Y-%m-%d %H:%M:%S")

        if date_to!='':
            date_to = datetime.strptime(f"{date_to} 23:59:59", "%Y-%m-%d %H:%M:%S")

        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field='update_at_ajustada'))

        if num_order!='':
            match_query.update({"answers.672e8edfd2f1f131c66505d9":num_order})

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
                "no_orden":"$answers.672e8edfd2f1f131c66505d9",
                "cliente": {
                    "$cond": {
                        "if": { "$isArray": "$answers.670f50c71f4102516864159d.6687f2f37b2c023e187d6252" },
                        "then": { "$arrayElemAt": ["$answers.670f50c71f4102516864159d.6687f2f37b2c023e187d6252", 0] },
                        "else": "$answers.670f50c71f4102516864159d.6687f2f37b2c023e187d6252"
                    }
                },
                "option_data":"$answers.668309d89331539409abace1",
                "chasis_catalog": {
                    "$cond": {
                        "if": { "$isArray": "$answers.670f507af522b590fbfd918c.6646393c3fa8b818265d0325" },
                        "then": { "$arrayElemAt": ["$answers.670f507af522b590fbfd918c.6646393c3fa8b818265d0325", 0] },
                        "else": "$answers.670f507af522b590fbfd918c.6646393c3fa8b818265d0325"
                    }
                },
                "chasis_text":"$answers.66830c302315146a39b4f22d",
                "trabajo_realizado":"$answers.667489b66e98a08e9d03e955",
                "fecha_apertura":"$answers.666a160967bcb9e23b1cc963",
                "trabajo_atencion":"$answers.666a160967bcb9e23b1cc964",
                "set_horas_traslado":"$answers.c00000000000000000000021",
                "set_horas_trabajadas":"$answers.c00000000000000000000003",
                "set_horas_regreso":"$answers.c00000000000000000000022",
                "set_tecnico":"$answers.666a160967bcb9e23b1cc967",
            }},
            {"$sort": {"folio":1}}
        ]
        result = self.cr.aggregate(query)
        result_format = self.get_format_informe_servicio(result)
        return result_format

    def get_query_care_inspection(self, date_from, date_to):
        match_query = { 
            "form_id": 120576,
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
                        "if": { "$isArray": "$answers.670f50c71f4102516864159d.6687f2f37b2c023e187d6252" },
                        "then": { "$arrayElemAt": ["$answers.670f50c71f4102516864159d.6687f2f37b2c023e187d6252", 0] },
                        "else": "$answers.670f50c71f4102516864159d.6687f2f37b2c023e187d6252"
                    }
                },
                "tecnico": {
                    "$cond": {
                        "if": { "$isArray": "$answers.66707634e674c20724d85969.62c5ff407febce07043024dd" },
                        "then": { "$arrayElemAt": ["$answers.66707634e674c20724d85969.62c5ff407febce07043024dd", 0] },
                        "else": "$answers.66707634e674c20724d85969.62c5ff407febce07043024dd"
                    }
                },
                "codigo_empleado": {
                    "$cond": {
                        "if": { "$isArray": "$answers.66707634e674c20724d85969.670f585bf844ff7bc357b1dc" },
                        "then": { "$arrayElemAt": ["$answers.66707634e674c20724d85969.670f585bf844ff7bc357b1dc", 0] },
                        "else": "$answers.66707634e674c20724d85969.670f585bf844ff7bc357b1dc"
                    }
                },
                "option_data":"$answers.668309d89331539409abace1",
                "chasis_catalog": {
                    "$cond": {
                        "if": { "$isArray": "$answers.670f507af522b590fbfd918c.6646393c3fa8b818265d0325" },
                        "then": { "$arrayElemAt": ["$answers.670f507af522b590fbfd918c.6646393c3fa8b818265d0325", 0] },
                        "else": "$answers.670f507af522b590fbfd918c.6646393c3fa8b818265d0325"
                    }
                },
                "chasis_text":"$answers.66830c302315146a39b4f22d",
                "trabajo_realizado":"$answers.6679a8fa580fa539a803e908",
                "fecha_apertura":"$answers.666a160967bcb9e23b1cc963",
                "trabajo_atencion":"$answers.666a160967bcb9e23b1cc964",
                "set_horas_traslado":"$answers.c00000000000000000000021",
                "set_horas_trabajadas":"$answers.c00000000000000000000003",
                "set_horas_regreso":"$answers.c00000000000000000000022",
            }},
            {"$sort": {"folio":1}}
        ]
        result = self.cr.aggregate(query)
        result_format = self.get_format_care_inspection(result)
        return result_format

    def get_query_entrada_salida_equipos(self, date_from, date_to, num_order):
        match_query = { 
            "form_id": 120574,
            "deleted_at": {"$exists": False},
        }
        if date_from!='':
            date_from = datetime.strptime(f"{date_from} 00:00:00", "%Y-%m-%d %H:%M:%S")

        if date_to!='':
            date_to = datetime.strptime(f"{date_to} 23:59:59", "%Y-%m-%d %H:%M:%S")

        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field='update_at_ajustada'))

        if num_order!='':
            match_query.update({"answers.672e8edfd2f1f131c66505d9":num_order})

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
                "no_orden":"$answers.672e8edfd2f1f131c66505d9",
                "cliente": {
                    "$cond": {
                        "if": { "$isArray": "$answers.670f50c71f4102516864159d.6687f2f37b2c023e187d6252" },
                        "then": { "$arrayElemAt": ["$answers.670f50c71f4102516864159d.6687f2f37b2c023e187d6252", 0] },
                        "else": "$answers.670f50c71f4102516864159d.6687f2f37b2c023e187d6252"
                    }
                },
                "tecnico": {
                    "$cond": {
                        "if": { "$isArray": "$answers.66707634e674c20724d85969.62c5ff407febce07043024dd" },
                        "then": { "$arrayElemAt": ["$answers.66707634e674c20724d85969.62c5ff407febce07043024dd", 0] },
                        "else": "$answers.66707634e674c20724d85969.62c5ff407febce07043024dd"
                    }
                },
                "codigo_empleado": {
                    "$cond": {
                        "if": { "$isArray": "$answers.66707634e674c20724d85969.670f585bf844ff7bc357b1dc" },
                        "then": { "$arrayElemAt": ["$answers.66707634e674c20724d85969.670f585bf844ff7bc357b1dc", 0] },
                        "else": "$answers.66707634e674c20724d85969.670f585bf844ff7bc357b1dc"
                    }
                },
                "option_data":"$answers.668309d89331539409abace1",
                "chasis_catalog": {
                    "$cond": {
                        "if": { "$isArray": "$answers.670f507af522b590fbfd918c.6646393c3fa8b818265d0325" },
                        "then": { "$arrayElemAt": ["$answers.670f507af522b590fbfd918c.6646393c3fa8b818265d0325", 0] },
                        "else": "$answers.670f507af522b590fbfd918c.6646393c3fa8b818265d0325"
                    }
                },
                "chasis_text":"$answers.66830c302315146a39b4f22d",
                "trabajo_realizado":"$answers.6679a8fa580fa539a803e908",
                "fecha_apertura":"$answers.666a160967bcb9e23b1cc963",
                "trabajo_atencion":"$answers.666a160967bcb9e23b1cc964",
                "date_from":"$answers.c00000000000000000000001",
                "date_to":"$answers.c00000000000000000000002",
            }},
            {"$sort": {"folio":1}}
        ]
        result = self.cr.aggregate(query)
        result_format = self.get_format_salida_equipos(result)
        return result_format

    def get_query_gestion_post_venta(self, date_from, date_to):
        match_query = { 
            "form_id": 124648,
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
                        "if": { "$isArray": "$answers.670f50c71f4102516864159d.6687f2f37b2c023e187d6252" },
                        "then": { "$arrayElemAt": ["$answers.670f50c71f4102516864159d.6687f2f37b2c023e187d6252", 0] },
                        "else": "$answers.670f50c71f4102516864159d.6687f2f37b2c023e187d6252"
                    }
                },
                "tecnico": {
                    "$cond": {
                        "if": { "$isArray": "$answers.66707634e674c20724d85969.62c5ff407febce07043024dd" },
                        "then": { "$arrayElemAt": ["$answers.66707634e674c20724d85969.62c5ff407febce07043024dd", 0] },
                        "else": "$answers.66707634e674c20724d85969.62c5ff407febce07043024dd"
                    }
                },
                "codigo_empleado": {
                    "$cond": {
                        "if": { "$isArray": "$answers.66707634e674c20724d85969.670f585bf844ff7bc357b1dc" },
                        "then": { "$arrayElemAt": ["$answers.66707634e674c20724d85969.670f585bf844ff7bc357b1dc", 0] },
                        "else": "$answers.66707634e674c20724d85969.670f585bf844ff7bc357b1dc"
                    }
                },
                "option_data":"$answers.668309d89331539409abace1",
                "chasis_catalog": {
                    "$cond": {
                        "if": { "$isArray": "$answers.670f507af522b590fbfd918c.6646393c3fa8b818265d0325" },
                        "then": { "$arrayElemAt": ["$answers.670f507af522b590fbfd918c.6646393c3fa8b818265d0325", 0] },
                        "else": "$answers.670f507af522b590fbfd918c.6646393c3fa8b818265d0325"
                    }
                },
                "chasis_text":"$answers.66830c302315146a39b4f22d",
                "trabajo_realizado":"$answers.673e734f94d1ef23abb279ed",
                "fecha_apertura":"$answers.666a160967bcb9e23b1cc963",
                "trabajo_atencion":"$answers.666a160967bcb9e23b1cc964",
                "resumen_gestion":"$answers.670dc8de391a088440159491",
                "set_horas_traslado":"$answers.c00000000000000000000021",
                "set_horas_trabajadas":"$answers.c00000000000000000000003",
                "set_horas_regreso":"$answers.c00000000000000000000022",
            }},
            {"$sort": {"folio":1}}
        ]
        result = self.cr.aggregate(query)
        result_format = self.get_format_gestion_post_venta(result)
        return result_format

    def get_query_gestion_ventas(self, date_from, date_to):
        match_query = { 
            "form_id": 124649,
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
                        "if": { "$isArray": "$answers.670f50c71f4102516864159d.6687f2f37b2c023e187d6252" },
                        "then": { "$arrayElemAt": ["$answers.670f50c71f4102516864159d.6687f2f37b2c023e187d6252", 0] },
                        "else": "$answers.670f50c71f4102516864159d.6687f2f37b2c023e187d6252"
                    }
                },
                "tecnico": {
                    "$cond": {
                        "if": { "$isArray": "$answers.66707634e674c20724d85969.62c5ff407febce07043024dd" },
                        "then": { "$arrayElemAt": ["$answers.66707634e674c20724d85969.62c5ff407febce07043024dd", 0] },
                        "else": "$answers.66707634e674c20724d85969.62c5ff407febce07043024dd"
                    }
                },
                "codigo_empleado": {
                    "$cond": {
                        "if": { "$isArray": "$answers.66707634e674c20724d85969.670f585bf844ff7bc357b1dc" },
                        "then": { "$arrayElemAt": ["$answers.66707634e674c20724d85969.670f585bf844ff7bc357b1dc", 0] },
                        "else": "$answers.66707634e674c20724d85969.670f585bf844ff7bc357b1dc"
                    }
                },
                "option_data":"$answers.668309d89331539409abace1",
                "chasis_catalog": {
                    "$cond": {
                        "if": { "$isArray": "$answers.670f507af522b590fbfd918c.6646393c3fa8b818265d0325" },
                        "then": { "$arrayElemAt": ["$answers.670f507af522b590fbfd918c.6646393c3fa8b818265d0325", 0] },
                        "else": "$answers.670f507af522b590fbfd918c.6646393c3fa8b818265d0325"
                    }
                },
                "chasis_text":"$answers.66830c302315146a39b4f22d",
                "trabajo_realizado":"$answers.673e734f94d1ef23abb279ed",
                "fecha_apertura":"$answers.666a160967bcb9e23b1cc963",
                "trabajo_atencion":"$answers.666a160967bcb9e23b1cc964",
                "resumen_gestion":"$answers.670dc8de391a088440159491",
                "set_horas_traslado":"$answers.c00000000000000000000021",
                "set_horas_trabajadas":"$answers.c00000000000000000000003",
                "set_horas_regreso":"$answers.c00000000000000000000022",
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
            '672e8edfd2f1f131c66505d8' : date, 
            '672e8e711d0c3f0eb0650570':contac,
            '672e8e711d0c3f0eb0650571':phone,
            '673e734f94d1ef23abb279ed':job,
            '672eb39a4d20582177b00a05':{
                '672eb39a4d20582177b00a06':checklist,
            },
            '672eadbd8064d180dab0097e':'pendiente',
            '672e8edfd2f1f131c66505d9':order,
            '670f50c7f522b590fbfd91eb':{
                '638a9a7767c332f5d459fc81':user,
                '638a9a7767c332f5d459fc82':[user_email],
                '663bc4c79b8046ce89e97cf4':[user_job],
            },
            '670f50c71f4102516864159d':{
                '6687f2f37b2c023e187d6252':name_client,
                '667468e3e577b8b98c852aab':[ruc_client],
                '667468e3e577b8b98c852aaa':[company_name],
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
                '668309d89331539409abace1':'sí',
                '670f507af522b590fbfd918c':{
                    '6646393c3fa8b818265d0325':chasis,
                    '66beb10007981d4509575054':[marca],
                    '66beb11907981d4509575056':[modelo],
                    '66beb1b507981d4509575057':[categoria],
                    '66c192ef89463aa27fc1818b':[nombre],
                    '66c1758989463aa27fc1816e':[motor_1],
                    '6646393c3fa8b818265d0329':[status],
                    '66c1940b89463aa27fc1818c':[estado],
                }
            }
            dic_create.update(dic_answers)

        elif check_no!= '' and check_no =='on':
            item = information.get('inputTextItem','')
            brand = information.get('inputTextBrand','')
            model = information.get('InputTextModel','')
            serie = information.get('inputTextSerie','')

            dic_answers = {
                '668309d89331539409abace1':'no',
                '66830c302315146a39b4f22a':item,
                '66830c302315146a39b4f22b':brand,
                '66830c302315146a39b4f22c':model,
                '66830c302315146a39b4f22d':serie,
            }
            dic_create.update(dic_answers)

        #----Creation record
        metadata = self.lkf_api.get_metadata(125650)
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

        catalog_clientes = self.lkf_api.search_catalog( 124722, mango_query)
        for item in catalog_clientes:
           razon_social = item.get('6687f2f37b2c023e187d6252','')
           nombre_comercial = item.get('667468e3e577b8b98c852aaa','')
           ruc = item.get('667468e3e577b8b98c852aab','')
           dic_response['catalog_client'].append({
                'razon_social':razon_social,
                'nombre_comercial':nombre_comercial,
                'ruc':ruc,
            })

        catalog_equipos = self.lkf_api.search_catalog( 124709, mango_query)
        for item in catalog_equipos:
            chasis = item.get('6646393c3fa8b818265d0325','')
            status = item.get('672eadbd8064d180dab0097e','')
            marca = item.get('66beb10007981d4509575054','')
            modelo = item.get('66beb11907981d4509575056','')
            categoria = item.get('66beb1b507981d4509575057','')
            motor_1 = item.get('66c1758989463aa27fc1816e','')
            nombre_equipo = item.get('66c192ef89463aa27fc1818b','')
            estado = item.get('66c1940b89463aa27fc1818c','')
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

        catalog_checklist = self.lkf_api.search_catalog(125652, mango_query)
        for item in catalog_checklist:
            checklist = item.get('672eb39a4d20582177b00a06','')
            id_check = item.get('672eb39a4d20582177b00a07',0)
            dic_response['catalog_checklist'].append({
                'checklist':checklist,
                'id_check':id_check,
            })

        catalog_usuarios = self.lkf_api.search_catalog(124723, mango_query)
        for item in catalog_usuarios:
            nombre = item.get('638a9a7767c332f5d459fc81','')
            email = item.get('638a9a7767c332f5d459fc82','')
            puesto = item.get('663bc4c79b8046ce89e97cf4','')
            dic_response['catalog_usuarios'].append({
                'nombre':nombre,
                'email':email,
                'puesto':puesto,
            })

        return dic_response

    #---Query
    def get_query_events(self, gestor = None , cliente = None):
        match_query = { 
            "form_id": 125650,
            "deleted_at":{"$exists":False},
        }
        if gestor and '--' not in  gestor:
            match_query.update({"answers.670f50c7f522b590fbfd91eb.638a9a7767c332f5d459fc81": gestor})

        if cliente and '--' not in cliente:
            match_query.update({"answers.670f50c71f4102516864159d.6687f2f37b2c023e187d6252":cliente })

        query = [
            {"$match": match_query},
            {"$project": {
                "_id":1,
                "folio":"$folio",
                "fecha_servicio":"$answers.672e8edfd2f1f131c66505d8",
                "cliente":"$answers.670f50c71f4102516864159d.6687f2f37b2c023e187d6252",
                "contacto":"$answers.672e8e711d0c3f0eb0650570",
                "celular":"$answers.672e8e711d0c3f0eb0650571",
                "check_equipo":"$answers.668309d89331539409abace1",
                "catalog_serie":"$answers.670f507af522b590fbfd918c.6646393c3fa8b818265d0325",
                "input_equipo":"$answers.66830c302315146a39b4f22a",
                "input_marca":"$answers.66830c302315146a39b4f22b",
                "input_modelo":"$answers.66830c302315146a39b4f22c",
                "input_serie":"$answers.66830c302315146a39b4f22d",
                "trabajo_area":"$answers.673e734f94d1ef23abb279ed",
                "check_list":"$answers.672eb39a4d20582177b00a05.672eb39a4d20582177b00a06",
                "status":"$answers.672eadbd8064d180dab0097e",
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
