# -*- coding: utf-8 -*-
import sys, simplejson
from datetime import datetime, timedelta, date
import time
from copy import deepcopy
from pytz import timezone

from linkaform_api import settings, network, utils, lkf_models

from linkaform_api import base


def unlist(arg):
    if type(arg) == list and len(arg) > 0:
        return unlist(arg[0])
    return arg

class Expenses(base.LKF_Base):

    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False):
        # base.LKF_Base.__init__(self, settings, sys_argv=sys_argv)
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api)
        # self.lkf_api = utils.Cache(settings)
        # self.net = network.Network(settings)
        # self.cr = self.net.get_collections()
        # self.lkm = lkf_models.LKFModules(settings)
        # config['PROTOCOL'] = 'https'
        # config['HOST'] ='app.linkaform.com'
        # settings.config.update(config)
        # self.lkf_api_prod = utils.Cache(settings)
        self.name =  __class__.__name__
        self.settings = settings
        self.close_status = 'cerrada'
        self.status_id = '61041d15d9ee55ab14965bb6'
        self.CATALOG_SOL_VIAJE = self.lkm.catalog_id('solicitudes_de_gastos')
        self.CATALOG_SOL_VIAJE_ID = self.CATALOG_SOL_VIAJE.get('id')
        self.CATALOG_SOL_VIAJE_OBJ_ID = self.CATALOG_SOL_VIAJE.get('obj_id')
        self.CATALOG_RESP_AUT = self.lkm.catalog_id('responsables_de_autorizar_gastos')
        self.CATALOG_RESP_AUT_ID = self.CATALOG_RESP_AUT.get('id')
        self.CATALOG_RESP_AUT_OBJ_ID = self.CATALOG_RESP_AUT.get('obj_id')
        
        self.CATALOG_EMPLEADOS = self.lkm.catalog_id('catalogo_de_empleados')
        self.CATALOG_EMPLEADOS_ID = self.CATALOG_EMPLEADOS.get('id')
        self.CATALOG_EMPLEADOS_OBJ_ID = self.CATALOG_EMPLEADOS.get('obj_id')
        
        self.CATALOG_MONEDA = self.lkm.catalog_id('moneda')
        self.CATALOG_MONEDA_ID = self.CATALOG_MONEDA.get('id')
        self.CATALOG_MONEDA_OBJ_ID = self.CATALOG_MONEDA.get('obj_id') 

        self.CATALOG_CONCEPTO_GASTO = self.lkm.catalog_id('conceptos_de_gastos')
        self.CATALOG_CONCEPTO_GASTO_ID = self.CATALOG_CONCEPTO_GASTO.get('id')
        self.CATALOG_CONCEPTO_GASTO_OBJ_ID = self.CATALOG_CONCEPTO_GASTO.get('obj_id')

        self.CATALOG_DESTINOS = self.lkm.catalog_id('destinos')
        self.CATALOG_DESTINOS_ID = self.CATALOG_DESTINOS.get('id')
        self.CATALOG_DESTINOS_OBJ_ID = self.CATALOG_DESTINOS.get('obj_id')
        
        self.FORM_ID_SOLICITUD = self.lkm.form_id('solicitud_de_viticos','id')
        self.FORM_ID_AUTORIZACIONES = self.lkm.form_id('autorizacin_de_viaticos','id')
        self.FORM_ID_GASTOS_VIAJE = self.lkm.form_id('registros_de_gastos_de_viaje','id')
        self.FORM_BANK_TRANSACTIONS = self.lkm.form_id('entrega_de_efectivo','id')
        self.FORM_ID_GASTOS = self.lkm.form_id('registros_de_gastos_de_viaje','id') #CAMBIAR POR SOLO GASTOS
        self.FORM_SOLICITUD_VIATICOS_ID = self.lkm.form_id('solicitud_de_viticos','id') 
        self.FORM_REGISTRO_DE_GASTOS_DE_VIAJE = self.lkm.form_id('registros_de_gastos_de_viaje')['id']

        self.SOL_METADATA = {}
        self.SOL_CATALOG = {}
        self.SOL_DATA = {}
        if folio_solicitud:
            self.SOL_DATA = self.set_solicitud_data(folio_solicitud)
        self.f.update( {
            'allow_overdraft':'64dd637965b8662fabb5ac2d',
            'anticipo_efectivo':'649d02057880ff495300bcc0',
            'deposito_entregado':'544d5ad901a4de205f391111',
            'deposito_solicitado':'544d5ad901a4de205f392000',
            'approved_amount':'61041d15d9ee55ab14965bb7',
            'autorizador':'62bf232626827cd253f9db16',
            'cant_dias':'61041d15d9ee55ab14965bb5',
            'cat_cargo_empleado':'6092c0ebd8b748522446af27',
            'cat_destino':'610419b5d28657c73e36fcd4',
            'cat_destinos': '66107030fc70de34c53e622d',
            'cat_email_empleado':'6092c0ebd8b748522446af28',
            'cat_folio':'610419b5d28657c73e36fcd3',
            'cat_moneda':'62aa1fa92c20405af671d123',
            'cat_monto_total_aprobado':'610419e33a05c520d90814d3',
            'cat_nombre_empleado':'6092c0ebd8b748522446af26',
            'cat_status':'610419b5d28657c73e36fcd7',
            'close_on_overdraft':'64dd637965b8662fabb5ac2f',
            'concepto':'649b2a84dac4914e02aadb24',
            'date_from':'61041b50d9ee55ab14965ba2',
            'date_to':'61041b50d9ee55ab14965ba3',
            'destino_otro':'61041b50d9ee55ab14965ba0',
            'destino':'61041b50d9ee55ab14965000',
            'estatus_solicitud_autorizacion_uno':'62954ccb8e54c96dc34995a5',
            'estatus_solicitud_autorizacion':'64e7eb0b402ad68c2cd368f0',
            'expense_kind':'628cf516d69420342af2c7c8',
            'expense_total':'544d5ad901a4de205f3934ed',
            'fecha_gasto':'583d8e10b43fdd6a4887f55b',
            'fecha_salida':'610419b5d28657c73e36fcd5',
            'fecha_regreso':'610419b5d28657c73e36fcd6',
            'folio_solicitudes':'64e7f571402ad68c2cd36956',
            'gasto_ejecutado_efectivo':'649d02057880ff495311bcc0',
            'gasto_ejecutado_compania':'661a892ac628a5e9f5880955',
            'gasto_ejecutado':'629fb33a8758b5808890b22e',
            'grp_gasto_estatus':'62aa1fa92c20405af671d124',
            'grp_gasto_folio':'62aa1fa92c20405af671d120',
            'grp_gasto_moneda':'aaaa1fa92c20405af671d123',
            'grp_gasto_monto_aut':'627bf0d5c651931d3c7eedd3',
            'grp_gasto_monto_ex':'aaaa1fa92c20405af671d122',
            'grp_gasto_monto':'62aa1fa92c20405af671d122',
            'grp_gastos_viaje':'62aa1ed283d55ab39a49bd2d',
            'impuestos':'62914e2d855e9abc32eabc18',
            'metodo_pago':'5893798cb43fdd4b53ab6e1e',
            'pagado_por': '65a0925c6a3fdf3e32659bb8',
            'monto_anticipo_restante':'649d02057880ff495300bcc1',
            'monto_restante':'629fb33a8758b5808890b22f',
            'motivo':'650ce3ce7f5e7a3c7349aeaf',
            'overdraft_limit':'64dd637965b8662fabb5ac2e',
            'propina':'62914e2d855e9abc32eabc19',
            'reason_no_authorized':'6271bd58d96e7e7ab68d2c4b',
            'requested_amount':'61041b8370c14c09eff167ae',
            'status_gasto':'544d5b4e01a4de205e2b2169',
            'status_solicitud':'61041d15d9ee55ab14965bb6',
            'subtotal':'62914e2d855e9abc32eabc17',
            'tipo_solicitud':'649b512cbf4cc1fab1133b7a',
            'total_gasto_moneda_sol':'544d5ad901a4de205f391111',
        })

    def str_to_date(self, str_date):
        return datetime.strptime(str_date, '%Y-%m-%d')

    def do_solicitud_close(self, form, folio, status_id=None, force_close=False):
        #check if it can be close
        balance = self.get_balance(folio)
        print('En cierre de solicitud ... balance =', balance)
        # Se cierra la solicitud si el balance es igual a cero y no se permite sobre giro
        # o bien, si se fuerza el cierre
        if ( balance.get('balance') == 0 and self.SOL_DATA.get(self.f['allow_overdraft'], '') != 'si' ) or force_close:
            #Cierra Entrega de Efectivo
            query_answers = self.get_answer_value(f"{self.CATALOG_SOL_VIAJE_OBJ_ID}.{self.f['cat_folio']}", folio)
            res = self.get_records(self.FORM_BANK_TRANSACTIONS, query_answers=query_answers, select_columns=['folio'])
            folios_efectivo = [r['folio'] for r in res if r.get('folio')]
            #todo cambiar status id
            print('#todo cambiar status id')
            self.do_records_close(self.FORM_BANK_TRANSACTIONS, folios_efectivo, status_id=self.f['status_gasto'])

            #Cierra Registro de Gastos
            res = self.get_records(self.FORM_REGISTRO_DE_GASTOS_DE_VIAJE, query_answers=query_answers, select_columns=['folio'])
            folio_gastos = [r['folio'] for r in res if r.get('folio')]
            self.do_records_close(self.FORM_REGISTRO_DE_GASTOS_DE_VIAJE, folio_gastos, status_id=self.f['status_gasto'])

            #Cierra Solicitud
            self.do_records_close(form, folio)

            # Actualizo el catalogo
            if force_close:
                self.update_expense_catalog_values(folio)
    
            #Cierra Autorizacion
            #self.do_records_close(self.FORM_ID_AUTORIZACIONES, self.current_record.get('folio'))

            #else:
            # Registro de transaccion del banco en caso de que se haya gastado menos del anticipo en efectivo que se otorgó
            self.balance_solicitud(folio, balance)
        #print('balance', balancessop )
        #cierra solicitud
        #self.do_records_close(form, folio, status_id=None)

        
        #close deposits
        #g_authorization
        #close autorhization

    def do_solicitud_open(self, folio):
        return self.do_records_open(folio)

    def do_bank_transaction(self, folio, balance):
        print('do_bank_transaction')

    def update_bank_transaction(self, catalog_obj_id, field_id_folio, value_field_folio, new_deposito_solicitado):
        record_bank_transaction = self.cr.find_one({
            "form_id": self.FORM_BANK_TRANSACTIONS,
            "deleted_at": {'$exists': False},
            f"answers.{catalog_obj_id}.{field_id_folio}": value_field_folio,
            f"answers.{self.f['status_gasto']}": {'$nin': ['realizado', 'cancelado']}
        }, {'folio': 1, 'answers': 1, 'form_id': 1})
        if not record_bank_transaction:
            return False
        record_bank_transaction['answers'][self.f['deposito_solicitado']] = new_deposito_solicitado
        res_update = self.lkf_api.patch_record(record_bank_transaction)
        return res_update

    def review_devolucion_exists(self, fecha_anticipo, folio_viatico, cash_to_back):
        record_devolution  = self.cr.find_one({
            'form_id': self.FORM_BANK_TRANSACTIONS,
            'deleted_at': {'$exists': False},
            f'answers.{self.CATALOG_SOL_VIAJE_OBJ_ID}.{self.f["cat_folio"]}':folio_viatico,
            f'answers.{self.f["fecha_gasto"]}':fecha_anticipo,
            f'answers.{self.f["deposito_solicitado"]}':cash_to_back,
        }, {'folio': 1})
        return record_devolution

    def balance_solicitud(self, folio, balance):
        #Acomoda informacion para hacer el registro de la tranaccion del banco
        self.set_solicitud_data(folio)
        self.set_solicitud_catalog(folio)
        #self.SOL_DATA.get(self.f['approved_amount'])
        catalog = self.SOL_CATALOG
        catalog_obj_id = self.CATALOG_SOL_VIAJE_OBJ_ID
        print('catalog=',catalog)
        catalog_solicitud = {
            self.f['cat_folio']:catalog.get(self.f['cat_folio']),
            # self.f['cat_destino']:catalog.get(self.f['cat_destino']),
            self.f['cat_destinos']:catalog.get(self.f['cat_destinos']),
            # self.f['fecha_salida']:[catalog.get(self.f['fecha_salida']),],
            # self.f['fecha_regreso']:[catalog.get(self.f['fecha_regreso']),],
            # self.f['approved_amount']:[catalog.get(self.f['approved_amount']),]
        }

        catalog_employee_obj_id = self.CATALOG_EMPLEADOS_OBJ_ID
        print('solicitud=', self.SOL_DATA)
        print('catalog_employee_obj_id=', catalog_employee_obj_id)
        print('type', type(self.SOL_DATA))
        cash_balance = balance.get('cash_balance')
        print('cash_balance', cash_balance)

        if cash_balance:
            str_today = datetime.now( tz=timezone('America/Monterrey') ).strftime('%Y-%m-%d')
            # Antes de crear la Devolucion. Necesito revisar si ya existe un registro con el mismo:
            # Fecha de anticipo, folio de solicitud, motivo y anticipo solicitado
            exists_devolucion = self.review_devolucion_exists( str_today, folio, cash_balance )
            if exists_devolucion:
                print('Ya existe un registro de Devolucion... ya no se va a crear')
                return False
            # Probablemente esto sea correcto pero mejor revisar con JP
            answers = {
                self.f['fecha_gasto']: str_today,
                catalog_obj_id:catalog_solicitud,
                catalog_employee_obj_id:self.SOL_DATA.get(catalog_employee_obj_id),
                self.CATALOG_CONCEPTO_GASTO_OBJ_ID:{self.f['concepto']:'Deposito'},
                self.f['motivo']:'Devolucion',
                self.f['deposito_solicitado']:cash_balance,
                # self.f['metodo_pago'] : 'deposito_a_cuenta_o_tarjeta_de_debito',
                self.f['pagado_por'] : 'compañia',
                self.f['status_gasto'] :'en_proceso'
            }
            print('answers', answers)
            metadata = self.lkf_api.get_metadata(self.FORM_BANK_TRANSACTIONS)
            metadata.update({
                'properties': {
                    "device_properties":{
                        "system": "Script",
                        "process": "Devolucion de caja",
                        "folio":folio,
                        "archive": "expense_utils.py"
                    }
                },
            })
            metadata['answers'] = answers
            res = self.lkf_api.post_forms_answers(metadata)
            print('res=0',res)


    def create_expense_authorization(self, folio=None, autorizador={}):
        if not folio and not autorizador:
            msg_error_app.update({
                    "62bf232626827cd253f9db16":{
                        "msg": [f"Es requerido seleccionar un autorizador o folio de solicitud."], 
                        "label": "Nombre Autorizador", "error":[]},
                })
            raise Exception(simplejson.dumps(msg_error_app))
        # n = datetime.now( tz=timezone('America/Monterrey') )
        # from_date = n - timedelta(days=7)
        res_create = []
        metadata = self.lkf_api.get_metadata(self.FORM_ID_AUTORIZACIONES)
        new_records = self.get_autorization_data(folio=folio, autorizador=autorizador)
        metadata.update({
            'properties': {
                "device_properties":{
                    "system": "Script",
                    "process": "Autorización de Gastos",
                    "accion": 'Crear registro de Autorización',
                    "folio solicitud": "",
                    "archive": "solicitar_autorizacion.py"
                }
            },
        })
        for idx, new_record in enumerate(new_records):
            rec_folio = new_record.pop('folio')
            metadata['properties']['device_properties']['folio solicitud'] += rec_folio
            metadata.update({
                "answers":new_record
                })
            res_create.append(self.lkf_api.post_forms_answers(metadata))
            for res in res_create:
                if res.get('status_code') == 201 or True:
                    self.update_expense_status(new_record.get(self.f['grp_gastos_viaje']))
        print('rescreate-', res_create)
        return res_create
    
    def currency_converter(self, from_curreny, expense_date, to_curreny, amount):
        data = {
            "from":from_curreny, 
            "date":expense_date,
            "to":to_curreny,
            "amount":amount,
            "script_id":104621
            }
        try:
            amount_dict = self.lkf_api_prod.run_script(data)
            amount = amount_dict.get('json',{}).get('response',{}).get('amount')
            if not amount:
                if amount_dict.get('error'):
                    print("error", simplejson.dumps(amount.get('error')))
                amount = False
        except:
            amount = False
        return amount

    def expense_valid_status(self):
        return ['por_autorizar','en_autorizacion','en_proceso', 'autorizado', 'realizado','cerrada','close']

    def force_udpate(self, folios, data):
        set_answers = {}
        for key, value in data.items():
            set_answers.update({f'answers.{key}':value})
        res = self.cr.update_many( {
            'folio': {"$in":folios},
            'form_id': self.FORM_REGISTRO_DE_GASTOS_DE_VIAJE,
            'deleted_at': {'$exists': False}
            },
            {'$set':set_answers}
            )
        return res

    def get_autorizador(self, folio_solicitud=None):
        if self.SOL_DATA:
            record = self.SOL_DATA.get(self.CATALOG_RESP_AUT_OBJ_ID)
        auth_catalog = record.get('answers',{}).get(self.CATALOG_RESP_AUT_OBJ_ID)
        return auth_catalog
    
    def get_cant_days(self, date_from, date_to):
        from_dt = datetime.strptime(date_from, '%Y-%m-%d')
        to_dt = datetime.strptime(date_to, '%Y-%m-%d')
        cant_days = to_dt - from_dt
        return int(cant_days.days)

    def get_balance(self, folio):
        res = {}
        self.set_solicitud_data(folio)
        res['expenses'] = self.get_related_expenses(folio)
        res['cash_expenses'] = self.get_related_expenses(folio, cash_only=True)
        res['approved_amount'] = self.SOL_DATA.get(self.f['approved_amount'])
        res['deposits'] = self.query_get_transactions(folio)
        res['cash_balance'] = res['deposits'] - res['cash_expenses']
        res['balance'] = res['approved_amount'] - res['expenses']
        return res

    def get_total(self, answers):
        subtotal = answers.get(self.f['subtotal'], 0)
        impuesto = answers.get(self.f['impuestos'], 0)
        propina = answers.get(self.f['propina'], 0)
        expense_date = answers.get(self.f['fecha_gasto'], 0)
        expense_curreny = answers.get(self.CATALOG_MONEDA_OBJ_ID , {}).get(self.f['cat_moneda'])
        info_catalog = answers.get(self.CATALOG_SOL_VIAJE_OBJ_ID, {})
        folio = info_catalog.get(self.f['cat_folio'], '')
        record_folio =  self.current_record.get('folio')
        # destino = info_catalog.get(self.f['cat_destino'], '')
        destino = info_catalog.get(self.f['cat_destinos'], '')
        self.set_solicitud_data(folio)
        msg_error_app={}
        if not self.SOL_DATA:
            msg_error_app = {
                "6499b3586f2edb3da9155e3b":{"msg": [f"No se encontro en numero de solicitud {folio}, con destino: {destino} "], "label": "Numero de Solicitud", "error":[]},
            }
            raise Exception(simplejson.dumps(msg_error_app))
        sol_currency = self.SOL_DATA.get(self.CATALOG_MONEDA_OBJ_ID,{}).get(self.f['cat_moneda'])
        expense_total_currency = subtotal + impuesto + propina
        if expense_curreny != sol_currency:
            expense_total_sol = self.currency_converter(expense_curreny, expense_date, sol_currency, expense_total_currency)
            if isinstance(expense_total_sol, bool):
                expense_total_sol = 0
                answers[self.f['status_gasto']] = 'error'

        else:
            expense_total_sol = expense_total_currency
        approved_amount = self.SOL_DATA.get(self.f['approved_amount'])
        current_total_expense = self.get_related_expenses(folio, this_expense=expense_total_sol, folio_rec= record_folio)
        viaje_monto_restante = approved_amount - current_total_expense
        #TODO cerrar solicutud si se sobregira y asi esta la configuiracion
        if current_total_expense > approved_amount:
            if self.SOL_DATA.get(self.f['allow_overdraft']) == 'no':
                #DO NOT ALLOW OVERDRAFT!!!
                msg = f"El Total del gasto ${current_total_expense} no debe ser mayor al monto restante: {viaje_monto_restante}"
                msg_error_app = {
                    self.f['expense_total']:{
                    "msg": [msg], "label": "Subtotal", "error":[]},
                }
            else:
                #OVERDRAFT PERMITED
                overdraft_limit = self.SOL_DATA.get(self.f['overdraft_limit'],0)
                if overdraft_limit > 0:
                    if current_total_expense > (approved_amount + overdraft_limit):
                        msg = f"El Total del gasto ${current_total_expense} revasa el limite permitido: {approved_amount + overdraft_limit}"
                        msg_error_app = {
                            self.f['expense_total']:{
                            "msg": [msg], "label": "Subtotal", "error":[]},
                        }
                    elif current_total_expense == (approved_amount + overdraft_limit):
                        if self.SOL_DATA.get(self.f['close_on_overdraft']) == 'si':
                            self.do_solicitud_close(self.FORM_ID_SOLICITUD, folio, force_close=True)
        #         if self.f['close_on_overdraft'] == 'si':
        #             self.close_solicitud(expense_total_currency, )
        # elif current_total_expense == approved_amount:
        #     self.close_solicitud(expense_total_currency, )
        if msg_error_app:
            raise Exception(simplejson.dumps(msg_error_app))
        answers[self.f['expense_total']] = expense_total_currency
        answers[self.f['total_gasto_moneda_sol']] = expense_total_sol
        return answers

    def get_cash_expenses(self, expense_group):
        print('........ get_cash_expenses')
        cash_expense = 0
        company_expense = 0
        for expense in expense_group:
            status = expense.get(self.f['grp_gasto_estatus'])
            if status not in self.expense_valid_status():
                continue
            # payment_method = expense.get(self.f['metodo_pago'],'').lower()
            payment_method = expense.get(self.f['pagado_por'],'').lower()
            amount = expense.get(self.f['total_gasto_moneda_sol'],0)
            if status == 'autorizado':
                amount = expense.get(self.f['grp_gasto_monto_aut'],0)
            if amount == None:
                amount = 0
            print(f'-------------  amount = {amount} payment_method= {payment_method}')
            # if (payment_method.find('debito') >= 0 or payment_method.find('efectivo') >= 0)\
            # if payment_method == 'empleado' and amount > 0:
            #     cash_expense += amount
            if amount > 0:
                if payment_method == 'empleado':
                    cash_expense += amount
                else:
                    company_expense += amount
        return cash_expense, company_expense

    def get_related_expenses(self, folio_sol, this_expense=0, folio_rec=None, status=None, cash_only=False):
        #TODO QUERY ALL EXPENSES
        if not status:
            status = ['no_autorizado', 'cancelado']
        elif isinstance(status, str):
            status = [status, ]
        match_query  = {
                    'form_id': self.FORM_ID_GASTOS_VIAJE,
                    'deleted_at': {'$exists': False},
                    f'answers.{self.f["status_gasto"]}': {'$nin':status},
                }
        if folio_sol:
            match_query.update({
                f'answers.{self.CATALOG_SOL_VIAJE_OBJ_ID}.{self.f["cat_folio"]}':folio_sol,
                })
        if folio_rec:
            #excluir el gasto de este registro del quiery el gasto de este registro
            match_query.update({'folio':{'$ne':folio_rec}})
        if cash_only:
            # match_query.update( {"$or":[
            #     # {f'answers.self.f['metodo_pago']':'Efectivo - Debito'},
            #     {f'answers.{self.f["metodo_pago"]}':{ '$regex': 'efectivo', '$options': 'i',}},
            #     {f'answers.{self.f["metodo_pago"]}':{ '$regex': 'debito',   '$options': 'i',}},
            #     # {f'answers.5893798cb43fdd4b53ab6e1e':'Efectivo - Debito'},
            #     ]})
            match_query.update({
                f'answers.{self.f["pagado_por"]}': 'empleado'
            })
        records = self.cr.aggregate([
            {'$match': match_query },
            {'$project':{
                '_id':1,
                'expense_total': f'$answers.{self.f["total_gasto_moneda_sol"]}',
                'total_autorizado':{'$ifNull':[f'$answers.{self.f["grp_gasto_monto_aut"]}',f'$answers.{self.f["total_gasto_moneda_sol"]}']},
                'solicitud':f'$answers.{self.CATALOG_SOL_VIAJE_OBJ_ID}.{self.f["cat_folio"]}',
            }},
            {'$project':{
                '_id':1,
                'solicitud':'$solicitud',
                'expense_total': "$total_autorizado",
            }},
            {'$group':{
                '_id':{
                    'solicitud':'$solicitud'
                },
                'total':{'$sum':'$expense_total'}
            }}
            ])
        total = this_expense
        for r in records:
            total += r.get('total')
        return total

    def get_autorization_dates(self, records_to_process):
        date_from = None
        date_to = None
        for r in records_to_process:
            this_date = r.get(self.f['fecha_gasto'])
            if not date_from:
                date_from = r.get(self.f['fecha_gasto'])
                date_to = r.get(self.f['fecha_gasto'])
            if not date_from and not date_to:
                return date_from, date_to
            date_from = this_date if this_date < date_from else date_from
            date_to = this_date if this_date > date_to else date_to
        return date_from, date_to

    def get_solicitudes_autorizador(self, autorizador):
        name = autorizador.get(self.CATALOG_RESP_AUT_OBJ_ID,{}).get(self.f["autorizador"])
        match_query  = {
            'form_id': self.FORM_ID_SOLICITUD,
            'deleted_at': {'$exists': False},
            '$or':[
                {f'answers.{self.f["status_solicitud"]}':'autorizado'}, 
                {f'answers.{self.f["status_gasto"]}':'vencida'},
                {f'answers.{self.f["status_gasto"]}':'sobregirada'},
                ],
            f'answers.{self.CATALOG_RESP_AUT_OBJ_ID}.{self.f["autorizador"]}': name
            }
        query =[
            {'$match': match_query },
            {"$project":{
                    "_id":0,
                    'folio':"$folio", #folio
                    'employee':f"$answers.{self.CATALOG_EMPLEADOS_OBJ_ID}.{self.f['cat_nombre_empleado']}"
                    }
                },
            {'$group':{
                '_id':{
                    'employee':'$employee'
                },
                'folios':{'$push': '$folio'}
            }}
            ]
        records = self.cr.aggregate(query)
        return [r for r in records]        

    def get_folios_to_exclude(self, records_to_process):
        folios = []
        for r in records_to_process:
            if r.get(self.f['grp_gasto_folio']):
                folios.append(r[self.f['grp_gasto_folio']])
        folios_2_exclude = self.query_folios_to_exclude(folios)
        if folios_2_exclude:
            res = []
            for idx, r in enumerate(records_to_process):
                if r.get(self.f['grp_gasto_folio']) in folios_2_exclude:
                    continue
                res.append(r)
        else:
            res = records_to_process
        return res

    def get_autorization_data(self, folio=None, autorizador={}):
        # Preparo los registro a crear en la forma Autorización de Viáticos        
        records_to_process = []
        list_to_group = []
        record_to_create = []
        if folio:
            records_to_process = self.query_related_expenses_rec(folio)
            records_to_process = self.get_folios_to_exclude(records_to_process)
            if not records_to_process:
                print(f'No more records to process for this folio: {folio}')
                return []
            self.set_solicitud_data(folio)
            autorizador = self.get_autorizador()
            new_record = self.SOL_DATA
            new_record['folio'] = folio
            gasto_ejecutado = self.SOL_DATA.get(self.f['gasto_ejecutado'],0)
            gasto_efectivo = self.SOL_DATA.get(self.f['gasto_ejecutado_efectivo'],0)
            gasto_compania = self.SOL_DATA.get(self.f['gasto_ejecutado_compania'],0)
            anticipo_efectivo = self.SOL_DATA.get(self.f['anticipo_efectivo'],0)
            monto_anticipo_restante = anticipo_efectivo - gasto_efectivo
            date_from, date_to = self.get_autorization_dates(records_to_process)
            cant_days = self.get_cant_days(date_from, date_to) if (date_from and date_to) else 0
            if self.SOL_METADATA['form_id'] == self.FORM_ID_SOLICITUD:
                new_record.update({self.f['tipo_solicitud']:"viatico"})
            else:
                new_record.update({self.f['tipo_solicitud']:"gasto"})
            new_record.update({
                self.f['folio_solicitudes'] : folio,
                self.f['cat_monto_total_aprobado'] : self.SOL_DATA.get(self.f['approved_amount']),
                self.f['anticipo_efectivo'] : anticipo_efectivo,
                self.f['gasto_ejecutado'] : gasto_ejecutado,
                self.f['gasto_ejecutado_efectivo'] : gasto_efectivo,
                self.f['gasto_ejecutado_compania'] : gasto_compania,
                self.f['monto_anticipo_restante'] : monto_anticipo_restante,
                self.f['monto_restante'] : self.SOL_DATA.get(self.f['monto_restante']),
                self.f['date_from'] : date_from,
                self.f['date_to'] : date_to,
                self.f['cant_dias'] : cant_days,
                self.f['estatus_solicitud_autorizacion_uno'] : 'pendiente',
                self.f['estatus_solicitud_autorizacion'] : 'pendiente',
                self.f['grp_gastos_viaje'] : self.update_records(records_to_process),
                self.CATALOG_SOL_VIAJE_OBJ_ID: {
                    self.f['cat_folio']: folio,
                    # self.f['cat_destino']: [new_record.get(self.f['destino']).replace('_', ' ').title()],
                    self.f['cat_destinos']: [new_record.get(self.CATALOG_DESTINOS_OBJ_ID,{}).get(self.f['cat_destinos'])],
                    self.f['fecha_salida']: [new_record.get(self.f['date_from'])],
                    self.f['fecha_regreso']: [new_record.get(self.f['date_to'])],
                    self.f['cat_monto_total_aprobado']: [new_record.get(self.f['approved_amount'])]
                }
                })
            record_to_create.append(new_record)
        else:
            folios_by_employee = self.get_solicitudes_autorizador(autorizador)
            anticipo_efectivo = 0
            gasto_ejecutado = 0
            for employee, folios in folios_by_employee.items():
                new_record = {
                    self.CATALOG_EMPLEADOS_OBJ_ID : {self.f['cat_nombre_empleado']: employee},
                    self.f['tipo_solicitud']:"gasto",
                    self.f['folio_solicitudes'] : folios,
                    }
                for f in folios:
                    records_to_process.append(self.query_related_expenses_rec(f))
                    anticipo_efectivo += self.query_get_transactions(f)
                    gasto_ejecutado += self.get_related_expenses(f)


                if not records_to_process:
                    return []
                records_to_process = self.get_folios_to_exclude(records_to_process)
                gasto_efectivo, gasto_compania = self.get_cash_expenses(records_to_process)
                monto_anticipo_restante = anticipo_efectivo - gasto_efectivo
                date_from, date_to = self.get_autorization_dates(records_to_process)
                cant_days = self.get_cant_days(date_from, date_to)
                new_record.update({
                    self.f['anticipo_efectivo'] : anticipo_efectivo,
                    self.f['gasto_ejecutado'] : gasto_ejecutado,
                    self.f['gasto_ejecutado_efectivo'] : gasto_efectivo,
                    self.f['gasto_ejecutado_compania'] : gasto_compania,
                    self.f['monto_anticipo_restante'] : monto_anticipo_restante,
                    self.f['date_from'] : date_from,
                    self.f['date_to'] : date_to,
                    self.f['cant_dias'] : cant_days,
                    self.f['estatus_solicitud_autorizacion_uno'] : 'pendiente',
                    self.f['estatus_solicitud_autorizacion'] : 'pendiente',
                    self.f['grp_gastos_viaje'] : self.update_records(records_to_process)
                    })
                record_to_create.append(new_record)
        return record_to_create

    def query_related_expenses_rec(self, folio_sol=None, answers={}, status=[]):
        match_query  = {
            'form_id': {'$in': [self.FORM_ID_GASTOS_VIAJE, self.FORM_BANK_TRANSACTIONS]},
            'deleted_at': {'$exists': False},
            # '$or':[
            #     {f'answers.{self.f["status_gasto"]}':'por_autorizar'}, 
            #     {f'answers.{self.f["status_gasto"]}':'autorizado'},
            #     {f'answers.{self.f["status_gasto"]}':'realizado'},
            #     {f'answers.{self.f["status_gasto"]}':'error'},
            #     {f'answers.{self.f["status_gasto"]}':'en_autorizacion'},
            #     ]
            }
        status_update = {"$or":[]}
        for s in status:
            status_update["$or"].append({f'answers.{self.f["status_gasto"]}':s})
        if len(status_update["$or"]) > 0:
            match_query.update(status_update)

        if folio_sol:
            match_query.update({
                f'answers.{self.CATALOG_SOL_VIAJE_OBJ_ID}.610419b5d28657c73e36fcd3':folio_sol,
                })
        query =[
            {'$match': match_query },
            {"$project":{
                    "_id":0,
                    self.f['grp_gasto_folio']:"$folio", #folio
                    self.f['fecha_gasto']:f"$answers.{self.f['fecha_gasto']}", #fecha
                    self.f['grp_gasto_moneda']:f"$answers.{self.CATALOG_MONEDA_OBJ_ID}.{self.f['cat_moneda']}", #Moneda
                    self.f['grp_gasto_monto_ex']:f"$answers.{self.f['expense_total']}", #Monteo en Moneda del gasto
                    #"62aa1fa92c20405af671d122":"$answers.544d5ad901a4de205f391111", #Monto
                    self.f['grp_gasto_monto']:{"$cond" :[
                        {"$eq":["$form_id",self.FORM_BANK_TRANSACTIONS]},
                        {'$ifNull': [ {'$multiply': [f"$answers.{self.f['total_gasto_moneda_sol']}",-1]}, 0 ]},
                        {'$ifNull': [ f"$answers.{self.f['total_gasto_moneda_sol']}", 0 ] }]}, #Monto
                    self.f['total_gasto_moneda_sol']:{"$cond" :[
                        {"$eq":["$form_id",self.FORM_BANK_TRANSACTIONS]},
                        {'$multiply': [f"$answers.{self.f['total_gasto_moneda_sol']}",-1]},
                        f"$answers.{self.f['total_gasto_moneda_sol']}"]}, #Monto
                    self.f['grp_gasto_monto_aut']:{'$ifNull':[f"$answers.{self.f['grp_gasto_monto_aut']}",0]},#Monto Autorizado
                    f"{self.CATALOG_CONCEPTO_GASTO_OBJ_ID}.{self.f['concepto']}":f"$answers.{self.CATALOG_CONCEPTO_GASTO_OBJ_ID}.{self.f['concepto']}", #Concepto
                    self.f['grp_gasto_estatus']:f"$answers.{self.f['status_gasto']}", #Estatus
                    # self.f['metodo_pago']:f"$answers.{self.f['metodo_pago']}", #Metodo de Pgo
                    self.f['pagado_por']:f"$answers.{self.f['pagado_por']}", #Pagado por
                }
            },
            {"$sort":{f"answers.{self.f['fecha_gasto']}":1}}
            ]
        records = self.cr.aggregate(query )
        res  = []
        #TODO SI NO EXISTE EL REGISTRO OSEA ES UNO NUEVO HAY QUE AGREGAR EL SET DEL CURREN RECORD
        this_set = {}
        for r in records:
            res.append(r)
        if this_set:
            res.append(this_set)
        return res

    def query_folios_to_exclude(self, folios):
        match_query  = {
            'form_id':  self.FORM_ID_AUTORIZACIONES,
            'deleted_at': {'$exists': False},
            # '$or':[
            #      {f'answers.{self.f["estatus_solicitud_autorizacion"]}':'pendiente'}, 
            #      {f'answers.{self.f["estatus_solicitud_autorizacion"]}':'autorizado'}, 
            #      ]
            }
        query =[
            {'$match': match_query },
            {"$unwind":f"$answers.{self.f['grp_gastos_viaje']}"},
            {"$match":{
                f"answers.{self.f['grp_gastos_viaje']}.{self.f['grp_gasto_folio']}" : {"$in":folios}
                }
            },
            {"$project":{
                    "_id":0,
                    "folio":f"$answers.{self.f['grp_gastos_viaje']}.{self.f['grp_gasto_folio']}",
                }
            }
            ]
        records = self.cr.aggregate(query )
        return [r['folio'] for r in records]

    def query_folio_form(self, folios):
        query  = {
            'folio':  {"$in":folios},
            'deleted_at': {'$exists': False},
            }
        records = self.cr.find(query,{'form_id':1, 'folio':1} )
        return {r['folio']:r['form_id'] for r in records}

    def query_record_from_db(self, form_id, folio):
        query = {
            'form_id': form_id,
            'folio': folio,
            'deleted_at': {'$exists': False}
        }
        select_columns = {'folio':1,'user_id':1,'form_id':1,'answers':1}
        records = self.cr.find(query, select_columns)
        return [ x for x in records ] 
 
    def query_get_transactions(self, folio_sol):
        match_query  = {
            'form_id': self.FORM_BANK_TRANSACTIONS,
            f'answers.{self.f["status_gasto"]}':{"$ne": 'cancelado'},
            'deleted_at': {'$exists': False},
            }
        if folio_sol:
            match_query.update({
                f'answers.{self.CATALOG_SOL_VIAJE_OBJ_ID}.{self.f["cat_folio"]}':folio_sol,
                })

        # records = self.cr.find(match_query,{'answers':1, 'folio':1})
        query =[
            {'$match': match_query },
            {'$group':{
                '_id':{
                    'upfront':'cash'
                },
                'total':{'$sum':f'$answers.{self.f["deposito_entregado"]}'}
            }}
            ]
        records = self.cr.aggregate(query )
        total = 0
        for r in records:
            total += r.get('total',0)
        return total

    def set_solicitud_catalog(self, folio):
        # info_catalog = current_record['answers'].get(self.CATALOG_SOL_VIAJE_OBJ_ID, {})
        # destino_de_viaje = info_catalog.get('610419b5d28657c73e36fcd4', '')
        # folio = info_catalog.get('610419b5d28657c73e36fcd3', '')
        self.set_solicitud_data(folio)
        if not self.SOL_CATALOG:
            mango_query = {"selector":
                {"answers":
                    {"$and":[
                        {'610419b5d28657c73e36fcd3': {'$eq': folio}}
                ]}},
            "limit":1,
            "skip":0}
            res = self.lkf_api.search_catalog( self.CATALOG_SOL_VIAJE_ID, mango_query)
            if res and len(res) > 0:
                self.SOL_CATALOG = res[0]
                if self.SOL_CATALOG.get('created_at'):
                    self.SOL_CATALOG.pop('created_at')
                if self.SOL_CATALOG.get('updated_at'):
                    self.SOL_CATALOG.pop('updated_at')
            else:
                msg_error_app = {
                    "610419b5d28657c73e36fcd4":{
                        "msg": [f"No encontro alguna solucitid con el folio: {folio}"],
                        "label": "Destino de viaje",
                        "error":[]
                    }
                }
                raise Exception(simplejson.dumps(msg_error_app))
        return True

    def set_solicitud_data(self, folio, renew=False):
        if not self.SOL_DATA or renew:
            answers = self.query_record_from_db(self.FORM_ID_SOLICITUD, folio)
        
            if answers and len(answers):
                if answers[0].get('answers'):
                    self.SOL_DATA = answers[0].pop('answers')
                self.SOL_METADATA = answers[0]
        return True

    def update_autorization_records(self, answers):
        """
        Actualiza Datos de la autorizacion del gasto
        Realiza caluclos y actualiza los registros de gasto segun si fueron autorizados  o no
        """
        dict_records_to_update = {}
        form_id = self.FORM_REGISTRO_DE_GASTOS_DE_VIAJE
        # self.set_solicitud_data(folio)
        response = []
        for viatico in answers.get(self.f['grp_gastos_viaje'], []):
            folio_origen = viatico.get(self.f['grp_gasto_folio'], '')
            dict_records_to_update[folio_origen] = dict_records_to_update.get(folio_origen,{})
            # dict_records_to_update[folio_origen].update({
            #     'status': viatico.get(self.f['grp_gasto_estatus'], ''),
            #     'monto_autorizado': viatico.get(self.f['grp_gasto_monto_aut'], 0),
            #     'reason_no_authorized': viatico.get(self.f['reason_no_authorized'], None),
            #     'metodo_pago': viatico.get(self.f['metodo_pago'], None),
            # })
            dict_records_to_update[folio_origen].update(viatico)
        entregas_efevo = 0
        #atualiza los registros de gastos
        res = self.update_expense_data(dict_records_to_update, update=True)

        reproces = False
        for gasto in answers.get(self.f['grp_gastos_viaje'], []):
            #verifica que todo se haya actualizado de manera correcta
            folio_origen = gasto.get(self.f['grp_gasto_folio'], '')
            if res.get(folio_origen):
                if res[folio_origen]['status_code'] != 202:
                    gasto[self.f['grp_gasto_estatus']] = 'error'
                    dict_records_to_update.pop(folio_origen)
                    reproces = True

        if reproces:
            #reporoces si hubo algun error
            res = self.update_expense_data(dict_records_to_update, update=False)

        answers[self.f['anticipo_efectivo']] = res['anticipo_efectivo'] 
        answers[self.f['gasto_ejecutado']] = res['gasto_ejecutado_aprovado'] 
        answers[self.f['gasto_ejecutado_efectivo']] = res['gasto_ejecutado_efevo_aprovado'] 
        answers[self.f['gasto_ejecutado_compania']] = res['gasto_ejecutado_compania_aprovado'] 
        answers[self.f['monto_anticipo_restante']] = res['anticipo_efectivo'] - res['gasto_ejecutado_efevo_aprovado']
        answers[self.f['grp_gastos_viaje']] = res['grp_gastos_viaje']
        

        return answers

    def update_expense_catalog_values(self, folio):
        print('... ... Actualizando catalogo al estatus =', self.SOL_DATA.get(self.f['status_solicitud'],"").replace('_', ' ').title())
        self.set_solicitud_data(folio)
        self.set_solicitud_catalog(folio)
        catalog_data = {}
        catalog_data = self.lkf_api.get_catalog_metadata(catalog_id=self.CATALOG_SOL_VIAJE_ID)
        catalog_data['answers'] = deepcopy(self.SOL_CATALOG)
        if catalog_data['answers'].get('conn_settings'):
            catalog_data['answers'].pop('conn_settings')
        catalog_data.update({
            'catalog_id': self.CATALOG_SOL_VIAJE_ID,
            'record_id': catalog_data['answers'].pop('_id'),
            '_rev': catalog_data['answers'].pop('_rev'),
        })
        catalog_data['answers'].update({
            self.f['cat_monto_total_aprobado']: self.SOL_DATA.get(self.f['approved_amount'], 0), 
            self.f['anticipo_efectivo']: self.SOL_DATA.get(self.f['anticipo_efectivo'], 0), 
            self.f['gasto_ejecutado']: self.SOL_DATA.get(self.f['gasto_ejecutado'], 0), 
            self.f['gasto_ejecutado_efectivo']: self.SOL_DATA.get(self.f['gasto_ejecutado_efectivo'], 0), 
            self.f['gasto_ejecutado_compania']: self.SOL_DATA.get(self.f['gasto_ejecutado_compania'], 0), 
            self.f['monto_anticipo_restante']: self.SOL_DATA.get(self.f['monto_anticipo_restante'], 0), 
            self.f['monto_restante']: self.SOL_DATA.get(self.f['monto_restante'], 0), 
            self.f['expense_kind']: self.SOL_DATA.get(self.f['expense_kind']), 
            self.f['cat_status']: self.SOL_DATA.get(self.f['status_solicitud'],"").replace('_', ' ').title(), 
            })
        catalog_data['answers'].update(self.SOL_DATA.get(self.CATALOG_EMPLEADOS_OBJ_ID))
        #catalogo_metadata.update({'record_id': catalog_data.pop('_id'), '_rev': catalog_data['answers'].pop('_rev'), 'answers': catalog_data['answers']})
        res_update = self.lkf_api.bulk_patch_catalog([catalog_data,], self.CATALOG_SOL_VIAJE_ID)
        update_ok = False
        if res_update and len(res_update):
            res_update = res_update[0]
        if res_update.get('status_code',0) == 204:
                update_ok = True
        else: 
            raise Exception(simplejson.dumps(res_update))
        return update_ok

    def get_solicitu_folios(self, all_folios):
        res = {}
        records = self.get_records(
            form_id=self.FORM_ID_GASTOS_VIAJE, 
            folio=all_folios,
            select_columns=['folio',f"answers.{self.CATALOG_SOL_VIAJE_OBJ_ID}.{self.f['cat_folio']}"]
            )
        for r in records:
            folio_solicitud = r.get('answers',{}).get(self.CATALOG_SOL_VIAJE_OBJ_ID,{}).get(self.f['cat_folio'])
            res[r['folio']] = folio_solicitud
        return res

    def update_expense_data(self, dict_records_to_update, update=True):
        """

        """
        res = {}
        update_solicitud = []
        all_folios = list(dict_records_to_update.keys())
        folio_solicitud = self.get_solicitu_folios(all_folios)
        gasto_ejecutado_aprovado = 0
        gasto_ejecutado_efevo_aprovado = 0
        gasto_ejecutado_compania_aprovado = 0
        anticipo = 0
        #form_id = self.FORM_REGISTRO_DE_GASTOS_DE_VIAJE
        form_ids = self.query_folio_form(list(dict_records_to_update.keys()))
        for folio, gasto in dict_records_to_update.items():
            res[folio] = {}
            form_id = form_ids[folio]
            if gasto[self.f['grp_gasto_estatus']] == 'no_autorizado':
                gasto[self.f['grp_gasto_monto_aut']] = 0
            if gasto[self.f['grp_gasto_estatus']] == 'autorizado':
                # if gasto[self.f['metodo_pago']].find('efectivo') >= 0 or \
                #  gasto[self.f['metodo_pago']].find('debito') >= 0:
                if gasto.get(self.f['pagado_por']):
                    if form_id == self.FORM_BANK_TRANSACTIONS:
                        #si el monto es menor a 0 es un deposito
                        anticipo += gasto[self.f['grp_gasto_monto_aut']]  * -1
                    else:
                        #si el monto es menor a 0 es un deposito
                        if gasto[ self.f['pagado_por'] ] == 'empleado':
                            gasto_ejecutado_efevo_aprovado += gasto[self.f['grp_gasto_monto_aut']]
                        else:
                            gasto_ejecutado_compania_aprovado += gasto[self.f['grp_gasto_monto_aut']]
                        gasto_ejecutado_aprovado += gasto[self.f['grp_gasto_monto_aut']]
                else:
                    gasto_ejecutado_aprovado += gasto[self.f['grp_gasto_monto_aut']]
            res[folio]['form_id'] = form_ids[folio]
            if update:
                if folio_solicitud.get(folio):
                    solicitud = folio_solicitud[folio]
                    self.cache_set({
                            '_id': f'{folio}_authorized',
                            'solicitud': solicitud,
                            'folio': folio
                            })
                    if not solicitud in update_solicitud:
                        update_solicitud.append(solicitud)
                res_update = self.lkf_api.patch_multi_record(
                    {
                    self.f['status_gasto']: gasto[self.f['grp_gasto_estatus']],
                    self.f['grp_gasto_monto_aut']: gasto[self.f['grp_gasto_monto_aut']],#monto aturoizado
                    self.f['reason_no_authorized']: gasto.get(self.f['reason_no_authorized']),#motivo
                    }, form_ids[folio], folios=[folio])
                res[folio]['status_code'] = res_update.get('status_code')
        res['gasto_ejecutado_aprovado'] = gasto_ejecutado_aprovado
        res['gasto_ejecutado_efevo_aprovado'] = gasto_ejecutado_efevo_aprovado
        res['gasto_ejecutado_compania_aprovado'] = gasto_ejecutado_compania_aprovado
        res['anticipo_efectivo'] = anticipo
        res['grp_gastos_viaje'] = list(dict_records_to_update.values())
        for f_solicitud in update_solicitud:
            if update:
                self.update_solicitud(f_solicitud)
        return res

    def update_expense_status(self, expenses):
        folios = []
        for record in expenses:
            folio = record.get(self.f['grp_gasto_folio'])
            folios.append(folio)
        folios = [r[self.f['grp_gasto_folio']] for r in expenses if r.get(self.f['grp_gasto_folio'])]
        data = {self.f['status_gasto']: 'en_autorizacion'}
        result = []
        result = self.lkf_api.patch_multi_record(
            data,
            self.FORM_REGISTRO_DE_GASTOS_DE_VIAJE, folios=folios
            )
        self.force_udpate(folios, data)
        #TODO SI NO SE ACTUALIZA FORZAR EN BASE DE DATOS.
        return result

    def update_records(self, records_to_process):
        for record in records_to_process:
            record[self.f['grp_gasto_estatus']] = 'autorizado'
            record[self.f['grp_gasto_monto_aut']] = record.get(self.f['grp_gasto_monto'],)
        return records_to_process

    def update_solicitud(self, folio, run_validations=False, background=False):
        self.set_solicitud_data(folio)
        close_order = False
        # fecha_fin = self.SOL_DATA.get('610419b5d28657c73e36fcd6', '')
        #pedir balance
        expense_group = self.query_related_expenses_rec(folio)
        monto_aprobado = self.SOL_DATA.get(self.f['approved_amount'], 0)
        gasto_ejecutado  = self.get_related_expenses(folio)
        monto_restante = round(monto_aprobado - gasto_ejecutado,2)
        anticipo_efectivo = self.query_get_transactions(folio)
        gasto_efectivo, gasto_compania = self.get_cash_expenses(expense_group)
        print(f'--- --- --- --- gasto_efectivo = {gasto_efectivo} gasto_compania = {gasto_compania}')
        print(f'--- --- monto_aprobado = {monto_aprobado} - gasto_ejecutado = {gasto_ejecutado}')
        print(f'--- --- monto_restante = {monto_restante}')
        monto_anticipo_restante = anticipo_efectivo - gasto_efectivo
        self.set_solicitud_catalog(folio)
        if run_validations:
            close_order = self.valida_status_solicitud(folio, monto_restante)

        if self.SOL_DATA.get(self.f['allow_overdraft']) == 'si':
            close_order = False

        # destino = self.SOL_DATA.get(self.f['destino'])
        destino = self.SOL_DATA.get(self.CATALOG_DESTINOS_OBJ_ID, {}).get( self.f['cat_destinos'] )
        # if destino == 'otro':
        #     destino = self.SOL_DATA.get(self.f['destino_otro'])
            
        update_fields = {
            f'answers.{self.CATALOG_SOL_VIAJE_OBJ_ID}': {
                self.f['cat_folio']: folio,
                # self.f['cat_destino']: [ destino ],
                self.f['cat_destinos']: [ destino ],
            },
            f"answers.{self.f['anticipo_efectivo']}":anticipo_efectivo,
            f"answers.{self.f['monto_anticipo_restante']}":monto_anticipo_restante,
            f"answers.{self.f['monto_restante']}":monto_restante,
            f"answers.{self.f['gasto_ejecutado_efectivo']}":gasto_efectivo,
            f"answers.{self.f['gasto_ejecutado_compania']}":gasto_compania,
            f"answers.{self.f['gasto_ejecutado']}":gasto_ejecutado,
            f"answers.{self.f['grp_gastos_viaje']}":expense_group
            }
        if close_order:
            update_fields.update({
                f"answers.{self.f['status_solicitud']}":"en_aprobacion",
                })
            # if background:
            #     self.create_expense_authorization(folio)

        if self.cache_read({'cache.solicitud':folio, '_one':True}):
            self.do_solicitud_close(self.FORM_ID_SOLICITUD, folio)
            update_fields.update({self.f['status_solicitud']:self.close_status})
        #self.do_solicitud_close(self.FORM_ID_SOLICITUD, folio)

        update_db = self.cr.update_one({
            'folio': folio,
            'form_id': self.FORM_SOLICITUD_VIATICOS_ID,
            'deleted_at': {'$exists': False}
        },{'$set':update_fields})
        db_res = update_db.raw_result
        print('db_res =',db_res)
        update_ok = db_res.get('updatedExisting')
        if update_ok:
            print('entra al update_ok...')
            self.set_solicitud_data(folio, renew=True)
            self.SOL_DATA.update({ ii.split('answers.')[1]: vv for ii, vv in update_fields.items() if 'answers.' in ii })
            update_ok = self.update_expense_catalog_values(folio)
        if close_order and background:
            self.create_expense_authorization(folio)
        return update_ok

    def validar_fecha_vencida(self, fecha_gasto):
        date_fecha_gasto = datetime.strptime(fecha_gasto, '%Y-%m-%d')
        fecha_actual = datetime.now()
        diff_dates = fecha_actual - date_fecha_gasto
        return diff_dates.days > 15

    def validaciones_solicitud(self):
        print('... expense_utils base de addons')
        answers = self.current_record.get('answers')
        #destino = answers.get(self.f['destino'])
        destino = answers.get(self.CATALOG_DESTINOS_OBJ_ID, {}).get( self.f['cat_destinos'] )
        #answers[ self.f['destino_otro'] ] = destino.replace('_', ' ').title()
        answers[ self.f['cat_destinos'] ] = destino
        dia_salida = answers.get(self.f['date_from'])
        dia_regreso = answers.get(self.f['date_to'])
        msg_error_app = {}
        dia_salida_s = dia_salida.split('-')
        dia_regreso_s = dia_regreso.split('-')
        dia = date(int(dia_salida_s[0]),int(dia_salida_s[1]),int(dia_salida_s[2]))
        dia_r = date(int(dia_regreso_s[0]),int(dia_regreso_s[1]),int(dia_regreso_s[2]))
        cant_dias = (dia_r - dia).days + 1
        answers[self.f['cant_dias']] = cant_dias
        deposito_solicitado = answers.get(self.f['deposito_solicitado'])
        approved_amount = answers.get(self.f['approved_amount'])
        requested_amount = answers.get(self.f['requested_amount'])
        if approved_amount:
            if deposito_solicitado > approved_amount:
                msg_error_app.update({
                        self.f['deposito_solicitado']:{
                            "msg": [f"El anticipo solicitado: {deposito_solicitado} no puede ser mayor al monto aprovado {approved_amount}"], 
                            "label": "Anticipo Solicitado", "error":[]},
                    })
        else:
            if deposito_solicitado > requested_amount:
                msg_error_app.update({
                        self.f['deposito_solicitado']:{
                            "msg": [f"El anticipo solicitado: {deposito_solicitado} no puede ser mayor monto solicitado {requested_amount}"], 
                            "label": "Anticipo Solicitado", "error":[]},
                    })
        if cant_dias < 0:
            msg_error_app.update({
                    "61041b50d9ee55ab14965ba2":{
                        "msg": [f"La fecha de salida {dia_salida}, debe de ser mayor que la fecah de regreso{dia_regreso}."], 
                        "label": "Fecha de Salida", "error":[]},
                })
        if msg_error_app:
                raise Exception(simplejson.dumps(msg_error_app))
        
        return answers

    def valida_status_solicitud(self, folio, monto_restante, ):
        close = False
        date_to = self.SOL_DATA.get(self.f['date_to'], 0)
        to_dt = datetime.strptime(date_to, '%Y-%m-%d')
        delta_hr = (to_dt - datetime.today()).total_seconds()/3600
        if delta_hr > 24*30: #30 dias han transcurrido
            close = True
        self.set_solicitud_data(folio)
        current_status = self.SOL_DATA.get(self.f['status_solicitud'], '')
        if current_status != 'autorizado' and False:
            msg_error_app = {
                            self.f['status_solicitud']:{
                                "msg": [f"No se pueden ingresar gastos a una solicitud con status: {current_status}"],
                                "label": "Status Solicitud",
                                "error":[]
                            }
                        }
            raise Exception(simplejson.dumps(msg_error_app))

        if monto_restante <= 1:
            close = True
        # if close:
        #     self.create_expense_authorization(folio)
        return close
