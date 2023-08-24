# -*- coding: utf-8 -*-
import sys, simplejson
from datetime import datetime, timedelta, date
import time
from copy import deepcopy
from pytz import timezone

from linkaform_api import settings, network, utils, lkf_models

from lkf_addons.lkf_base.base import LKF_Base


def unlist(arg):
    if type(arg) == list and len(arg) > 0:
        return unlist(arg[0])
    return arg

class Expenses(LKF_Base):

    def __init__(self, settings, folio_solicitud=None):
        LKF_Base.__init__(self, settings)
        # self.lkf_api = utils.Cache(settings)
        # self.net = network.Network(settings)
        # self.cr = self.net.get_collections()
        # self.lkm = lkf_models.LKFModules(settings)
        # config['PROTOCOL'] = 'https'
        # config['HOST'] ='app.linkaform.com'
        # settings.config.update(config)
        # self.lkf_api_prod = utils.Cache(settings)

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
        
        self.FORM_ID_SOLICITUD = self.lkm.form_id('solicitud_de_viticos','id')
        self.FORM_ID_AUTORIZACIONES = self.lkm.form_id('autorizacin_de_viaticos','id')
        self.FORM_ID_GASTOS_VIAJE = self.lkm.form_id('registros_de_gastos_de_viaje','id')
        self.FORM_ID_ENTREGA_EFECTIVO = self.lkm.form_id('entrega_de_efectivo','id')
        self.FORM_ID_GASTOS = self.lkm.form_id('registros_de_gastos_de_viaje','id') #CAMBIAR POR SOLO GASTOS
        self.FORM_SOLICITUD_VIATICOS_ID = self.lkm.form_id('solicitud_de_viticos','id') 
        self.FORM_REGISTRO_DE_GASTOS_DE_VIAJE = self.lkm.form_id('registros_de_gastos_de_viaje')['id']

        self.SOL_METADATA = {}
        self.SOL_CATALOG = {}
        self.SOL_DATA = {}
        if folio_solicitud:
            self.SOL_DATA = self.set_solicitud_data(folio_solicitud)
        self.fdict = {
            'cant_dias':'61041d15d9ee55ab14965bb5',
            'autorizador':'62bf232626827cd253f9db16',
            'destino':'61041b50d9ee55ab14965000',
            'fecha_salida':'61041b50d9ee55ab14965ba2',
            'fecha_regreso':'61041b50d9ee55ab14965ba3',
            'status_solicitud':'61041d15d9ee55ab14965bb6',
            'status_gasto':'544d5b4e01a4de205e2b2169',
            'approved_amount':'61041d15d9ee55ab14965bb7',
            'requested_amount':'61041b8370c14c09eff167ae',
            'anticipo_solicitado':'544d5ad901a4de205f392000',
            'anticipo_entregado':'544d5ad901a4de205f391111',
            'anticipo_efectivo':'649d02057880ff495300bcc0',
            'metodo_pago':'5893798cb43fdd4b53ab6e1e',
            'fecha_gasto':'583d8e10b43fdd6a4887f55b',
            'subtotal':'62914e2d855e9abc32eabc17',
            'impuestos':'62914e2d855e9abc32eabc18',
            'propina':'62914e2d855e9abc32eabc19',
            'expense_total':'544d5ad901a4de205f3934ed',
            'total_gasto_moneda_sol':'544d5ad901a4de205f391111',
            'gasto_ejecutado':'629fb33a8758b5808890b22e',
            'gasto_ejecutado_efectivo':'649d02057880ff495311bcc0',
            'monto_anticipo_restante':'649d02057880ff495300bcc1',
            'monto_restante':'629fb33a8758b5808890b22f',
            'expense_kind':'628cf516d69420342af2c7c8',
            'allow_overdraft':'64dd637965b8662fabb5ac2d',
            'overdraft_limit':'64dd637965b8662fabb5ac2e',
            'close_on_overdraft':'64dd637965b8662fabb5ac2f',
            'grp_gastos_viaje':'62aa1ed283d55ab39a49bd2d',
            'grp_gasto_folio':'62aa1fa92c20405af671d120',
            'grp_gasto_moneda':'aaaa1fa92c20405af671d123',
            'grp_gasto_monto_ex':'aaaa1fa92c20405af671d122',
            'grp_gasto_monto':'62aa1fa92c20405af671d122',
            'grp_gasto_monto_aut':'627bf0d5c651931d3c7eedd3',
            'grp_gasto_estatus':'62aa1fa92c20405af671d124',
            'cat_moneda':'62aa1fa92c20405af671d123',
            'cat_folio':'610419b5d28657c73e36fcd3',
            'cat_destino':'610419b5d28657c73e36fcd4',
            'cat_monto_total_aprobado':'610419e33a05c520d90814d3',
            'cat_status':'610419b5d28657c73e36fcd7',
            'cat_nombre_empleado':'6092c0ebd8b748522446af26',
            'cat_cargo_empleado':'6092c0ebd8b748522446af27',
            'cat_email_empleado':'6092c0ebd8b748522446af28',
            'tipo_solicitud':'649b512cbf4cc1fab1133b7a',
            'estatus_solicitud_autorizacion':'62954ccb8e54c96dc34995a5',
        }

    #Solicitud de Viaticos

    def get_cant_days(self, date_from, date_to):
        from_dt = datetime.strptime(date_from, '%Y-%m-%d')
        to_dt = datetime.strptime(date_to, '%Y-%m-%d')
        cant_days = to_dt - from_dt
        return int(cant_days.days)

    def update_solicitud_form_catalog(self, current_record ):
        #Actualza en el registro de la forma la solicitud creada....
        folio = current_record['folio']
        mango_query = {"selector":
        {"answers":
            {"$and":[
                {self.fdict['cat_folio']: {'$eq': folio}}
        ]}},
        "limit":1,
        "skip":0}
        catalog_data = self.lkm.catalog_id('solicitudes_de_gastos')
        catalog_id = catalog_data.get('id')
        catalog_obj_id = catalog_data.get('obj_id')
        date_from = current_record['answers'].get(self.fdict['fecha_salida'])
        date_to = current_record['answers'].get(self.fdict['fecha_regreso'])
        cant_dias = self.get_cant_days(date_from, date_to)
        for x in range(3):
            res = self.lkf_api.search_catalog( self.lkm.catalog_id('solicitudes_de_gastos', 'id'), mango_query, jwt_settings_key='JWT_KEY')
            if not res:
                time.sleep(x)
        if not res:
            print('todo crear registro de catalogo')
            print('no se encontro el registro res=',mango_query)
            return False
        for r in res:
            set_answers = {
                catalog_obj_id:{
                    self.fdict['cat_folio']: folio,
                    self.fdict['cat_destino']: [ r.get(self.fdict['cat_destino']) ],
                },
                self.fdict['cant_dias']:cant_dias
            }
        print('set_answers', set_answers)
        res_update = self.lkf_api.patch_multi_record(
                    set_answers, current_record['form_id'], folios=[folio])

        print('res_update', res_update)
        status_code = False
        for r in res_update.get('json',{}).get('objects',[]):
            this_rec = r.get(folio)
            status_code = this_rec.get('status_code')
            if status_code:
                break

        print('status_code', status_code)
        return status_code

    def validaciones_solicitud(self, answers):
        destino = answers.get(self.fdict['destino'])
        dia_salida = answers.get(self.fdict['fecha_salida'])
        dia_regreso = answers.get(self.fdict['fecha_regreso'])
        msg_error_app = {}
        dia_salida_s = dia_salida.split('-')
        dia_regreso_s = dia_regreso.split('-')
        dia = date(int(dia_salida_s[0]),int(dia_salida_s[1]),int(dia_salida_s[2]))
        dia_r = date(int(dia_regreso_s[0]),int(dia_regreso_s[1]),int(dia_regreso_s[2]))
        cant_dias = (dia_r - dia).days
        answers[self.fdict['cant_dias']] = cant_dias
        anticipo_solicitado = answers.get(self.fdict['anticipo_solicitado'])
        approved_amount = answers.get(self.fdict['approved_amount'])
        requested_amount = answers.get(self.fdict['requested_amount'])
        if approved_amount:
            if anticipo_solicitado > approved_amount:
                msg_error_app.update({
                        self.fdict['anticipo_solicitado']:{
                            "msg": [f"El anticipo solicitado: {anticipo_solicitado} no puede ser mayor al monto aprovado {approved_amount}"], 
                            "label": "Anticipo Solicitado", "error":[]},
                    })
        else:
            if anticipo_solicitado > requested_amount:
                msg_error_app.update({
                        self.fdict['anticipo_solicitado']:{
                            "msg": [f"El anticipo solicitado: {anticipo_solicitado} no puede ser mayor monto solicitado {requested_amount}"], 
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
            print('amount_dict', amount_dict)
            amount = amount_dict.get('json',{}).get('response',{}).get('amount')
            if not amount:
                if amount_dict.get('error'):
                    print("error", simplejson.dumps(amount.get('error')))
                amount = False
        except:
            amount = False
        print('amoutn', amount)
        return amount

    def get_total(self, answers):
        subtotal = answers.get(self.fdict['subtotal'], 0)
        impuesto = answers.get(self.fdict['impuestos'], 0)
        propina = answers.get(self.fdict['propina'], 0)
        expense_date = answers.get(self.fdict['fecha_gasto'], 0)
        expense_curreny = answers.get(self.CATALOG_MONEDA_OBJ_ID , {}).get(self.fdict['cat_moneda'])
        info_catalog = answers.get(self.CATALOG_SOL_VIAJE_OBJ_ID, {})
        folio = info_catalog.get(self.fdict['cat_folio'], '')
        destino = info_catalog.get(self.fdict['cat_destino'], '')
        self.set_solicitud_data(folio)
        if not self.SOL_DATA:
            msg_error_app = {
                "6499b3586f2edb3da9155e3b":{"msg": [f"No se encontro en numero de solicitud {folio}, con destino: {destino} "], "label": "Numero de Solicitud", "error":[]},
            }
            raise Exception(simplejson.dumps(msg_error_app))
        sol_currency = self.SOL_DATA.get(self.CATALOG_MONEDA_OBJ_ID,{}).get(self.fdict['cat_moneda'])
        expense_total_currency = subtotal + impuesto + propina
        if expense_curreny != sol_currency:
            expense_total_sol = self.currency_converter(expense_curreny, expense_date, sol_currency, expense_total_currency)
            if isinstance(expense_total_sol, bool):
                expense_total_sol = 0
                answers[self.fdict['status_gasto']] = 'error'

        else:
            expense_total_sol = expense_total_currency
        approved_amount = self.SOL_DATA.get(self.fdict['approved_amount'])
        current_total_expense = self.get_related_expenses(folio, expense_total_sol)
        if current_total_expense > approved_amount:
            if self.SOL_DATA.get(self.fdict['allow_overdraft']) == 'no':
                #DO NOT ALLOW OVERDRAFT!!!
                msg = f"El Total del gasto ${current_total_expense} no debe ser mayor al monto restante: {viaje_monto_restante}"
                msg_error_app = {
                    self.fdict['expense_total']:{
                    "msg": [msg], "label": "Subtotal", "error":[]},
                }
            else:
                #OVERDRAFT PERMITED
                overdraft_limit = self.SOL_DATA.get(self.fdict['overdraft_limit'],0)
                if overdraft_limit > 0:
                    if current_total_expense > (approved_amount + overdraft_limit):
                        msg = f"El Total del gasto ${current_total_expense} revasa el limite permitido: {approved_amount + overdraft_limit}"
                        msg_error_app = {
                            self.fdict['expense_total']:{
                            "msg": [msg], "label": "Subtotal", "error":[]},
                        }
                if self.fdict['close_on_overdraft'] == 'si':
                    self.close_solicitud(folio, status='overdraft')
        elif current_total_expense == approved_amount:
            self.close_solicitud(folio, status='overdraft')
        answers[self.fdict['expense_total']] = expense_total_currency
        answers[self.fdict['total_gasto_moneda_sol']] = expense_total_sol
        return answers

    def get_record_from_db(self, form_id, folio):
        query = {
            'form_id': form_id,
            'folio': folio,
            'deleted_at': {'$exists': False}
        }
        select_columns = {'folio':1,'user_id':1,'form_id':1,'answers':1}
        records = self.cr.find(query, select_columns)
        return [ x for x in records ] 

    def set_solicitud_data(self, folio, renew=False):
        if not self.SOL_DATA or renew:
            print('actualizaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
            answers = self.get_record_from_db(self.FORM_ID_SOLICITUD, folio)
            if answers and len(answers):
                if answers[0].get('answers'):
                    self.SOL_DATA = answers[0].pop('answers')
                self.SOL_METADATA = answers[0]
        return True

    def get_autorizador(self, folio_solicitud=None):
        if self.SOL_DATA:
            record = self.SOL_DATA.get(self.CATALOG_RESP_AUT_OBJ_ID)
        auth_catalog = record.get('answers',{}).get(self.CATALOG_RESP_AUT_OBJ_ID)
        return auth_catalog

    def validar_fecha_vencida(self, fecha_gasto):
        date_fecha_gasto = datetime.strptime(fecha_gasto, '%Y-%m-%d')
        fecha_actual = datetime.now()
        diff_dates = fecha_actual - date_fecha_gasto
        return diff_dates.days > 15

    def get_anticipo(self, folio_sol):
        match_query  = {
            'form_id': self.FORM_ID_ENTREGA_EFECTIVO,
            f'answers.{self.fdict["status_gasto"]}':'realizado',
            'deleted_at': {'$exists': False},
            }
        if folio_sol:
            match_query.update({
                f'answers.{self.CATALOG_SOL_VIAJE_OBJ_ID}.{self.fdict["cat_folio"]}':folio_sol,
                })

        # records = self.cr.find(match_query,{'answers':1, 'folio':1})
        query =[
            {'$match': match_query },
            {'$group':{
                '_id':{
                    'upfront':'cash'
                },
                'total':{'$sum':f'$answers.{self.fdict["anticipo_entregado"]}'}
            }}
            ]
        records = self.cr.aggregate(query )
        total = 0
        for r in records:
            total += r.get('total',0)
        return total

    def get_cash_expenses(self, expense_group):
        cash_expense = 0
        for expense in expense_group:
            payment_method = expense.get(self.fdict['metodo_pago'],'').lower()
            print('payment_method', payment_method)
            print('expense', expense)
            amount = expense.get(self.fdict['total_gasto_moneda_sol'],0)
            print('amount', amount)
            if ('debito' in payment_method or 'efectivo' in payment_method )\
                and amount > 0:
                print('amoutn', amount)
                cash_expense += amount
        print('cash_expense', cash_expense)
        return cash_expense

    ### Catalogo
    def set_solicitud_catalog(self, folio):
        # info_catalog = current_record['answers'].get(self.CATALOG_SOL_VIAJE_OBJ_ID, {})
        # destino_de_viaje = info_catalog.get('610419b5d28657c73e36fcd4', '')
        # print('info_catalog', info_catalog)
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

    def update_expense_catalog_values(self, folio):
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
            self.fdict['cat_monto_total_aprobado']: self.SOL_DATA.get(self.fdict['approved_amount'], 0), 
            self.fdict['anticipo_efectivo']: self.SOL_DATA.get(self.fdict['anticipo_efectivo'], 0), 
            self.fdict['gasto_ejecutado']: self.SOL_DATA.get(self.fdict['gasto_ejecutado'], 0), 
            self.fdict['gasto_ejecutado_efectivo']: self.SOL_DATA.get(self.fdict['gasto_ejecutado_efectivo'], 0), 
            self.fdict['monto_anticipo_restante']: self.SOL_DATA.get(self.fdict['monto_anticipo_restante'], 0), 
            self.fdict['monto_restante']: self.SOL_DATA.get(self.fdict['monto_restante'], 0), 
            self.fdict['expense_kind']: self.SOL_DATA.get(self.fdict['expense_kind']), 
            self.fdict['cat_status']: self.SOL_DATA.get(self.fdict['status_solicitud'],"").replace('_', ' ').title(), 
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

    ### Solicitud
    def valida_status_solicitud(self, folio):
        self.set_solicitud_data(folio)
        current_status = self.SOL_DATA.get(self.fdict['status_solicitud'], '')
        if current_status != 'autorizado':
            msg_error_app = {
                            self.fdict['status_solicitud']:{
                                "msg": [f"No se pueden ingresar gastos a una solicitud con status: {current_status}"],
                                "label": "Status Solicitud",
                                "error":[]
                            }
                        }
            raise Exception(simplejson.dumps(msg_error_app))
        # if current_status == 'Abierto' and self.validar_fecha_vencida( fecha_fin ):
        #     print('revisar este caso... si ya pasaron mas de 15 dias no debe de dejar guardar....')
        #     self.autorizacion_viaticos(folio)
        #     #crear autorizacion de viaticos
        #     info_to_set.update({self.fdict['cat_status']: 'Vencido'})
        # elif monto_restante < 0:
        #     # autorizacion_viaticos(folio)
        #     #crear autorizacion de viaticos
        #     info_to_set.update({
        #         self.fdict['cat_status']: 'Sobregirado'
        #     })
        # elif monto_restante == 0:
        #     self.autorizacion_viaticos(folio)
        #     #crear autorizacion de viaticos
        #     info_to_set.update({
        #         self.fdict['cat_status']: 'Cerrado'
        #     })
        return True

    def update_solicitud(self, folio, answers, run_validations=False):
        self.set_solicitud_data(folio)
        if run_validations:
            self.valida_status_solicitud(folio)
        # fecha_fin = self.SOL_DATA.get('610419b5d28657c73e36fcd6', '')
        expense_group = self.get_related_expenses_rec(folio)
        print('expense_group',expense_group)
        monto_aprobado = self.SOL_DATA.get(self.fdict['approved_amount'], 0)
        gasto_ejecutado  = self.get_related_expenses(folio)
        monto_restante = round(monto_aprobado - gasto_ejecutado,2)
        anticipo_efectivo = self.get_anticipo(folio)
        gasto_efectivo = self.get_cash_expenses(expense_group)
        print('gasto_efectivo=', gasto_efectivo)
        monto_anticipo_restante = anticipo_efectivo - gasto_efectivo
        self.set_solicitud_catalog(folio)
        update_db = self.cr.update_one({
            'folio': folio,
            'form_id': self.FORM_SOLICITUD_VIATICOS_ID,
            'deleted_at': {'$exists': False}
        },{'$set':{
            f'answers.{self.CATALOG_SOL_VIAJE_OBJ_ID}': {
                self.fdict['cat_folio']: folio,
                self.fdict['cat_destino']: [ self.SOL_DATA.get(self.fdict['cat_destino']) ],
            },
            f"answers.{self.fdict['anticipo_efectivo']}":anticipo_efectivo,
            f"answers.{self.fdict['monto_anticipo_restante']}":monto_anticipo_restante,
            f"answers.{self.fdict['monto_restante']}":monto_restante,
            f"answers.{self.fdict['gasto_ejecutado_efectivo']}":gasto_efectivo,
            f"answers.{self.fdict['gasto_ejecutado']}":gasto_ejecutado,
            f"answers.{self.fdict['grp_gastos_viaje']}":expense_group
            }
        })
        db_res = update_db.raw_result
        print('raw_result',db_res)
        update_ok = db_res.get('updatedExisting')
        if update_ok:
            self.set_solicitud_data(folio, renew=True)
            update_ok = self.update_expense_catalog_values(folio)
        return update_ok

    def get_related_expenses_rec(self, folio_sol=None, answers={}):
        match_query  = {
            'form_id': {'$in': [self.FORM_ID_GASTOS_VIAJE, self.FORM_ID_ENTREGA_EFECTIVO]},
            'deleted_at': {'$exists': False},
            # '$or':[
            #     {f'answers.{self.fdict["status_gasto"]}':'por_autorizar'}, 
            #     {f'answers.{self.fdict["status_gasto"]}':'autorizado'},
            #     {f'answers.{self.fdict["status_gasto"]}':'realizado'},
            #     {f'answers.{self.fdict["status_gasto"]}':'realizado'},
            #     {f'answers.{self.fdict["status_gasto"]}':'error'},
            #     {f'answers.{self.fdict["status_gasto"]}':'en_autorizacion'},
            #     ]
            }
        if folio_sol:
            match_query.update({
                f'answers.{self.CATALOG_SOL_VIAJE_OBJ_ID}.610419b5d28657c73e36fcd3':folio_sol,
                })
        print("self.FORM_ID_ENTREGA_EFECTIVO",self.FORM_ID_ENTREGA_EFECTIVO)
        # records = self.cr.find(match_query,{'answers':1, 'folio':1})
        query =[
            {'$match': match_query },
            {"$project":{
                    "_id":0,
                    self.fdict['grp_gasto_folio']:"$folio", #folio
                    self.fdict['fecha_gasto']:f"$answers.{self.fdict['fecha_gasto']}", #fecha
                    self.fdict['grp_gasto_moneda']:f"$answers.{self.CATALOG_MONEDA_OBJ_ID}.{self.fdict['cat_moneda']}", #Moneda
                    self.fdict['grp_gasto_monto_ex']:f"$answers.{self.fdict['expense_total']}", #Monteo en Moneda del gasto
                    #"62aa1fa92c20405af671d122":"$answers.544d5ad901a4de205f391111", #Monto
                    self.fdict['grp_gasto_monto']:{"$cond" :[
                        {"$eq":["$form_id",self.FORM_ID_ENTREGA_EFECTIVO]},
                        {'$multiply': [f"$answers.{self.fdict['total_gasto_moneda_sol']}",-1]},
                        f"$answers.{self.fdict['total_gasto_moneda_sol']}"]}, #Monto
                    self.fdict['total_gasto_moneda_sol']:{"$cond" :[
                        {"$eq":["$form_id",self.FORM_ID_ENTREGA_EFECTIVO]},
                        {'$multiply': [f"$answers.{self.fdict['total_gasto_moneda_sol']}",-1]},
                        f"$answers.{self.fdict['total_gasto_moneda_sol']}"]}, #Monto
                    self.fdict['grp_gasto_monto_aut']:f"$answers.{self.fdict['grp_gasto_monto_aut']}", #Monto Autorizado
                    f"{self.CATALOG_CONCEPTO_GASTO_OBJ_ID}.649b2a84dac4914e02aadb24":f"$answers.{self.CATALOG_CONCEPTO_GASTO_OBJ_ID}.649b2a84dac4914e02aadb24", #Concepto
                    self.fdict['grp_gasto_estatus']:f"$answers.{self.fdict['status_gasto']}", #Estatus
                    self.fdict['metodo_pago']:f"$answers.{self.fdict['metodo_pago']}", #Metodo de Pgo
                }
            },
            {"$sort":{f"answers.{self.fdict['fecha_gasto']}":1}}
            ]
        records = self.cr.aggregate(query )
        res  = []
        #TODO SI NO EXISTE EL REGISTRO OSEA ES UNO NUEVO HAY QUE AGREGAR EL SET DEL CURREN RECORD
        this_set = {}
        # if folio_sol:
        #     this_set ={
        #             "62aa1fa92c20405af671d120":"Pending", #folio
        #             "583d8e10b43fdd6a4887f55b":answers.get("583d8e10b43fdd6a4887f55b"), #fecha
        #             "aaaa1fa92c20405af671d123":answers.get(self.CATALOG_MONEDA_OBJ_ID,{}).get("62aa1fa92c20405af671d123"), #Moneda
        #             "aaaa1fa92c20405af671d122":answers.get("544d5ad901a4de205f3934ed"), #Monteo en Moneda Extranjera
        #             "62aa1fa92c20405af671d122":answers.get("544d5ad901a4de205f391111"), #Monto
        #             "627bf0d5c651931d3c7eedd3":answers.get("627bf0d5c651931d3c7eedd3"), #Monto Autorizado
        #             self.CATALOG_CONCEPTO_GASTO_OBJ_ID:{self.CATALOG_CONCEPTO_GASTO_OBJ_ID:answers.get(self.CATALOG_CONCEPTO_GASTO_OBJ_ID,{}).get("649b2a84dac4914e02aadb24")}, #Concepto
        #             "62aa1fa92c20405af671d124":answers.get("544d5b4e01a4de205e2b2169"), #Estatus
        #     }
        for r in records:
            res.append(r)
        if this_set:
            res.append(this_set)
        print('res=',res)
        return res

    def get_related_expenses(self, folio_sol, this_expense=0, folio_rec=None, status=None, cash_only=False):
        #TODO QUERY ALL EXPENSES
        if not status:
            status = ['por_autorizar', 'en_progreso', 'autorizado']
        elif isinstance(status, str):
            status = [status, ]
        match_query  = {
                    'form_id': self.FORM_ID_GASTOS_VIAJE,
                    'deleted_at': {'$exists': False},
                    f'answers.{self.fdict["status_gasto"]}': {'$in':status},
                }
        if folio_sol:
            match_query.update({
                f'answers.{self.CATALOG_SOL_VIAJE_OBJ_ID}.{self.fdict["cat_folio"]}':folio_sol,
                })
        if folio_rec:
            #excluir el gasto de este registro del quiery el gasto de este registro
            match_query.update({'folio':{'$ne':folio_rec}})
        if cash_only:
            match_query.update( {"$or":[
                # {f'answers.self.fdict['metodo_pago']':'Efectivo - Debito'},
                {f'answers.{self.fdict["metodo_pago"]}':{ '$regex': 'efectivo', '$options': 'i',}},
                {f'answers.{self.fdict["metodo_pago"]}':{ '$regex': 'debito',   '$options': 'i',}},
                # {f'answers.5893798cb43fdd4b53ab6e1e':'Efectivo - Debito'},
                ]})
        records = self.cr.aggregate([
            {'$match': match_query },
            {'$project':{
                '_id':1,
                'expense_total': f'$answers.{self.fdict["total_gasto_moneda_sol"]}',
                'total_autorizado':{'$ifNull':[f'$answers.{self.fdict["grp_gasto_monto_aut"]}',f'$answers.{self.fdict["total_gasto_moneda_sol"]}']},
                'solicitud':f'$answers.{self.CATALOG_SOL_VIAJE_OBJ_ID}.{self.fdict["cat_folio"]}',
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

    ### Autorizacion Gastos

    def get_autorization_dates(self, records_to_process):
        date_from = None
        date_to = None
        for r in records_to_process:
            this_date = r.get(self.fdict['fecha_gasto'])
            if not date_from:
                date_from = r.get(self.fdict['fecha_gasto'])
                date_to = r.get(self.fdict['fecha_gasto'])
            date_from = this_date if this_date < date_from else date_from
            date_to = this_date if this_date > date_to else date_to
        return date_from, date_to

    def get_solicitudes_autorizador(self, autorizador):
        name = autorizador.get(self.CATALOG_RESP_AUT_OBJ_ID,{}).get(self.fdict["autorizador"])
        match_query  = {
            'form_id': self.FORM_ID_SOLICITUD,
            'deleted_at': {'$exists': False},
            '$or':[
                {f'answers.{self.fdict["status_solicitud"]}':'autorizado'}, 
                {f'answers.{self.fdict["status_gasto"]}':'vencida'},
                {f'answers.{self.fdict["status_gasto"]}':'sobregirada'},
                ],
            f'answers.{self.CATALOG_RESP_AUT_OBJ_ID}.{self.fdict["autorizador"]}': name
            }
        query =[
            {'$match': match_query },
            {"$project":{
                    "_id":0,
                    'folio':"$folio", #folio
                    'employee':f"$answers.{self.CATALOG_EMPLEADOS_OBJ_ID}.{self.fdict['cat_nombre_empleado']}"
                    }
                },
            {'$group':{
                '_id':{
                    'employee':'$employee'
                },
                'folios':{'$push': '$folio'}
            }}
            ]
        print('query=', query)
        records = self.cr.aggregate(query)
        return [r for r in records]        

    def update_records(self, records_to_process):
        for record in records_to_process:
            record[self.fdict['grp_gasto_estatus']] = 'autorizado'
            record[self.fdict['grp_gasto_monto_aut']] = record.get(self.fdict['grp_gasto_monto'],)
            print('----------------------------')
            print('record=',record)
            print('----------------------------')
        return records_to_process

    def get_autorization_data(self,  folio=None, autorizador={}):
        # Preparo los registro a crear en la forma Autorización de Viáticos        
        records_to_process = []
        list_to_group = []
        record_to_create = []
        print('folio===', folio)
        if folio:
            records_to_process = self.get_related_expenses_rec(folio)
            print('records_to_process', records_to_process)
            if not records_to_process:
                return []
            self.set_solicitud_data(folio)
            autorizador = self.get_autorizador()
            new_record = self.SOL_DATA
            new_record['folio'] = folio
            gasto_ejecutado = self.SOL_DATA.get(self.fdict['gasto_ejecutado'],0)
            gasto_efectivo = self.SOL_DATA.get(self.fdict['gasto_ejecutado_efectivo'],0)
            anticipo_efectivo = self.SOL_DATA.get(self.fdict['anticipo_efectivo'],0)
            print('gasto_ejecutado=',gasto_ejecutado)
            print('gasto_efectivo=',gasto_efectivo)
            print('anticipo_efectivo=',anticipo_efectivo)
            monto_anticipo_restante = anticipo_efectivo - gasto_efectivo
            date_from, date_to = self.get_autorization_dates(records_to_process)
            cant_days = self.get_cant_days(date_from, date_to)
            if self.SOL_METADATA['form_id'] == self.FORM_ID_SOLICITUD:
                new_record.update({self.fdict['tipo_solicitud']:"viatico"})
            else:
                new_record.update({self.fdict['tipo_solicitud']:"gasto"})
            new_record.update({
                self.fdict['cat_monto_total_aprobado'] : self.SOL_DATA.get(self.fdict['approved_amount']),
                self.fdict['anticipo_efectivo'] : anticipo_efectivo,
                self.fdict['gasto_ejecutado'] : gasto_ejecutado,
                self.fdict['gasto_ejecutado_efectivo'] : gasto_efectivo,
                self.fdict['monto_anticipo_restante'] : monto_anticipo_restante,
                self.fdict['monto_restante'] : self.SOL_DATA.get(self.fdict['monto_restante']),
                self.fdict['fecha_salida'] : date_from,
                self.fdict['fecha_regreso'] : date_to,
                self.fdict['cant_dias'] : cant_days,
                self.fdict['estatus_solicitud_autorizacion'] : 'pendiente_por_autorizar',
                self.fdict['grp_gastos_viaje'] : self.update_records(records_to_process)
                })
            record_to_create.append(new_record)
        else:
            folios_by_employee = self.get_solicitudes_autorizador(autorizador)
            print('folios_by_employee', folios_by_employee)
            anticipo_efectivo = 0
            gasto_ejecutado = 0
            for employee, folios in folios_by_employee.items():
                print('employee', employee)
                print('folios', folios)
                new_record = {
                    self.CATALOG_EMPLEADOS_OBJ_ID : {self.fdict['cat_nombre_empleado']: employee},
                    self.fdict['tipo_solicitud']:"gasto"
                    }
                for f in folios:
                    records_to_process.append(self.get_related_expenses_rec(f))
                    anticipo_efectivo += self.get_anticipo(f)
                    gasto_ejecutado += self.get_related_expenses(f)

                if not records_to_process:
                    return []
                gasto_efectivo = self.get_cash_expenses(records_to_process)
                monto_anticipo_restante = anticipo_efectivo - gasto_efectivo
                date_from, date_to = self.get_autorization_dates(records_to_process)
                cant_days = self.get_cant_days(date_from, date_to)
                new_record.update({
                    self.fdict['anticipo_efectivo'] : anticipo_efectivo,
                    self.fdict['gasto_ejecutado'] : gasto_ejecutado,
                    self.fdict['gasto_ejecutado_efectivo'] : gasto_efectivo,
                    self.fdict['monto_anticipo_restante'] : monto_anticipo_restante,
                    self.fdict['fecha_salida'] : date_from,
                    self.fdict['fecha_regreso'] : date_to,
                    self.fdict['cant_dias'] : cant_days,
                    self.fdict['estatus_solicitud_autorizacion'] : 'pendiente_por_autorizar',
                    self.fdict['grp_gastos_viaje'] : self.update_records(records_to_process)
                    })
                record_to_create.append(new_record)
 
        return record_to_create

    def autorizacion_viaticos(self, folio=None, autorizador={}):
        print('folio===', folio)
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
                "answers":new_record,
                "folio":rec_folio + f'-{idx}'
                })
            print('metadata=',metadata)
            res_create.append(self.lkf_api.post_forms_answers(metadata))
            print(f'res_create= {idx} ==',res_create)
            for res in res_create:
                if res.get('status_code') == 201 or True:
                    self.update_expense_status(new_record.get(self.fdict['grp_gastos_viaje']))
        return res_create

    def force_udpate(self, folios, data):
        print('dir', dir(self.cr))
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
        print('folios', folios)
        print('data', data)
        print('resupdate', res)
        return res

    def update_expense_status(self, expenses):
        folios = []
        for record in expenses:
            folio = record.get(self.fdict['grp_gasto_folio'])
            print('folio=', folio)
            folios.append(folio)
        folios = [r[self.fdict['grp_gasto_folio']] for r in expenses if r.get(self.fdict['grp_gasto_folio'])]
        data = {self.fdict['status_gasto']: 'en_autorizacion'}
        result = []
        result = self.lkf_api.patch_multi_record(
            data,
            self.FORM_REGISTRO_DE_GASTOS_DE_VIAJE, folios=folios
            )
        print('update result=', result)
        self.force_udpate(folios, data)
        #TODO SI NO SE ACTUALIZA FORZAR EN BASE DE DATOS.
        return result

    def set_gasto_aprovado(self, dict_records_to_update, update=True):
        res = {}
        gasto_ejecutado_aprovado = 0
        gasto_ejecutado_efevo_aprovado = 0
        anticipo = 0
        form_id = self.FORM_REGISTRO_DE_GASTOS_DE_VIAJE
        for folio, gasto in dict_records_to_update.items():
            res[folio] = {}

            if gasto['status'] == 'no_autorizado':
                gasto['monto_autorizado'] = 0
            if gasto['status'] == 'autorizado':
                if 'efectivo' in gasto['metodo_pago'] or 'debito' in gasto['metodo_pago']:
                    if gasto['monto_autorizado'] > 0:
                        #si el monto es menor a 0 es un deposito
                        gasto_ejecutado_efevo_aprovado += gasto['monto_autorizado']
                        gasto_ejecutado_aprovado += gasto['monto_autorizado']
                    else:
                        #si el monto es menor a 0 es un deposito
                        anticipo += gasto['monto_autorizado']
                else:
                    gasto_ejecutado_aprovado += gasto['monto_autorizado']

            res[folio]['form_id'] = form_id
            if update:
                res_update = self.lkf_api.patch_multi_record(
                    {
                    self.fdict['status_gasto']: gasto['status'],
                    self.fdict['grp_gasto_monto_aut']: gasto['monto_autorizado'],#monto aturoizado
                    '6271bd58d96e7e7ab68d2c4b': gasto.get('motivo_no_autorizado'),#motivo
                    }, form_id, folios=[folio])
                res[folio]['status_code'] = res_update.get('status_code')
        res['gasto_ejecutado_aprovado'] = gasto_ejecutado_aprovado
        res['gasto_ejecutado_efevo_aprovado'] = gasto_ejecutado_efevo_aprovado
        res['anticipo'] = anticipo
        return res

    def update_autorization_records(self, answers):
        dict_records_to_update = {}
        form_id = self.FORM_REGISTRO_DE_GASTOS_DE_VIAJE
        # self.set_solicitud_data(folio)
        response = []
        for viatico in answers.get(self.fdict('grp_gastos_viaje'), []):
            folio_origen = viatico.get(self.fdict['grp_gasto_folio'], '')
            dict_records_to_update[folio_origen] = dict_records_to_update.get(folio_origen,{})
            dict_records_to_update[folio_origen] = {
                'status': viatico.get(self.fdict['grp_gasto_estatus'], ''),
                'monto_autorizado': viatico.get(self.fdict['grp_gasto_monto_aut'], 0),
                'motivo_no_autorizado': viatico.get('64a06441c375083cb0da8d4f', None),
                'metodo_pago': viatico.get(self.fdict['metodo_pago'], None),
            }
        entregas_efevo = 0
        res = self.set_gasto_aprovado(dict_records_to_update, update=True)

        print('dict_records_to_update',dict_records_to_update)
        print('res', res)
        reproces = False
        for viatico in answers.get(self.fdict('grp_gastos_viaje'), []):
            folio_origen = viatico.get(self.fdict['grp_gasto_folio'], '')
            if res.get(folio_origen):
                print('status code', res[folio_origen]['status_code'])
                if res[folio_origen]['status_code'] != 202:
                    viatico[self.fdict['grp_gasto_estatus']] = 'en_proceso'
                    dict_records_to_update.pop(folio_origen)
                    reproces = True

        if reproces:
            res = self.set_gasto_aprovado(dict_records_to_update, update=False)

        print('res2', res)
        answers[self.fdict['anticipo_efectivo']] = res['anticipo'] 
        answers[self.fdict['gasto_ejecutado']] = res['gasto_ejecutado_aprovado'] 
        answers['649d02057880ff495311bcc0'] = res['gasto_ejecutado_efevo_aprovado'] 
        answers[self.fdict['monto_anticipo_restante']] = res['anticipo'] - res['gasto_ejecutado_efevo_aprovado'] 

        return answers

