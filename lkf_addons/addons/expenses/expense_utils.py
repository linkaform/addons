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

    def __init__(self, settings, folio_solicitud=None, sys_argv=None):
        base.LKF_Base.__init__(self, settings, sys_argv=sys_argv)
        # self.lkf_api = utils.Cache(settings)
        # self.net = network.Network(settings)
        # self.cr = self.net.get_collections()
        # self.lkm = lkf_models.LKFModules(settings)
        # config['PROTOCOL'] = 'https'
        # config['HOST'] ='app.linkaform.com'
        # settings.config.update(config)
        # self.lkf_api_prod = utils.Cache(settings)

        self.CATALOG_SOL_VIAJE = self.lkm.catalog_id('solicitudes_de_gastos')
        print('self.lkm',self.lkm)
        print(' self.CATALOG_SOL_VIAJE .lkm', self.CATALOG_SOL_VIAJE )
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
            'destino_otro':'61041b50d9ee55ab14965ba0',
            'date_from':'61041b50d9ee55ab14965ba2',
            'date_to':'61041b50d9ee55ab14965ba3',
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
            'estatus_solicitud_autorizacion_uno':'62954ccb8e54c96dc34995a5',
            'estatus_solicitud_autorizacion':'64e7eb0b402ad68c2cd368f0',
            'reason_no_authorized':'6271bd58d96e7e7ab68d2c4b',
            'folio_solicitudes':'64e7f571402ad68c2cd36956'
        }

    #Solicitud de Viaticos

    def expense_valid_status(self):
        return ['por_autorizar','en_autorizacion','en_proceso', 'autorizado', 'realizado','cerrada']
    
    def get_cant_days(self, date_from, date_to):
        from_dt = datetime.strptime(date_from, '%Y-%m-%d')
        to_dt = datetime.strptime(date_to, '%Y-%m-%d')
        cant_days = to_dt - from_dt
        return int(cant_days.days)

    def validaciones_solicitud(self, answers):
        destino = answers.get(self.fdict['destino'])
        answers[ self.fdict['destino_otro'] ] = destino.replace('_', ' ').title()
        dia_salida = answers.get(self.fdict['date_from'])
        dia_regreso = answers.get(self.fdict['date_to'])
        msg_error_app = {}
        dia_salida_s = dia_salida.split('-')
        dia_regreso_s = dia_regreso.split('-')
        dia = date(int(dia_salida_s[0]),int(dia_salida_s[1]),int(dia_salida_s[2]))
        dia_r = date(int(dia_regreso_s[0]),int(dia_regreso_s[1]),int(dia_regreso_s[2]))
        cant_dias = (dia_r - dia).days + 1
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
        viaje_monto_restante = approved_amount - current_total_expense
        print('current_total_expense=',current_total_expense)
        print('approved_amount=',approved_amount)
        #TODO cerrar solicutud si se sobregira y asi esta la configuiracion
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
        #         if self.fdict['close_on_overdraft'] == 'si':
        #             self.close_solicitud(expense_total_currency, )
        # elif current_total_expense == approved_amount:
        #     self.close_solicitud(expense_total_currency, )
        answers[self.fdict['expense_total']] = expense_total_currency
        answers[self.fdict['total_gasto_moneda_sol']] = expense_total_sol
        return answers

    def query_record_from_db(self, form_id, folio):
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
            answers = self.query_record_from_db(self.FORM_ID_SOLICITUD, folio)
        
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

    def query_get_anticipo(self, folio_sol):
        match_query  = {
            'form_id': self.FORM_ID_ENTREGA_EFECTIVO,
            f'answers.{self.fdict["status_gasto"]}':{"$ne": 'cancelado'},
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
            status = expense.get(self.fdict['grp_gasto_estatus'])
            if status not in self.expense_valid_status():
                continue
            payment_method = expense.get(self.fdict['metodo_pago'],'').lower()
            amount = expense.get(self.fdict['total_gasto_moneda_sol'],0)
            if status == 'autorizado':
                amount = expense.get(self.fdict['grp_gasto_monto_aut'],0)
            if (payment_method.find('debito') >= 0 or payment_method.find('efectivo') >= 0)\
                and amount > 0:
                cash_expense += amount
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
            print('CATALOG_SOL_VIAJE_ID', self.CATALOG_SOL_VIAJE_ID)
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
        print('catalog_data=',simplejson.dumps(catalog_data, indent=4))
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

    def close_solicitud(self, cash_balance, expense_group, force=False):
        close = False
        if not force:
            date_to = self.SOL_DATA.get(self.fdict['date_to'], 0)
            to_dt = datetime.strptime(date_to, '%Y-%m-%d')
            delta_hr = (to_dt - datetime.today()).total_seconds()/3600
            if delta_hr < 24:
                return False
        if cash_balance >  -1 and cash_balance < 1:
            close = True
            for g in expense_group:
                if g[self.fdict['grp_gasto_estatus']] != 'autorizado' and \
                 g[self.fdict['grp_gasto_estatus']] != 'no_autorizado':
                 close = False 
                 break
        return close

    def update_solicitud(self, folio, run_validations=False):
        self.set_solicitud_data(folio)
        if run_validations:
            #self.valida_status_solicitud(folio)
            print('ya no se corre esta validacion')
        # fecha_fin = self.SOL_DATA.get('610419b5d28657c73e36fcd6', '')
        expense_group = self.query_related_expenses_rec(folio)
        monto_aprobado = self.SOL_DATA.get(self.fdict['approved_amount'], 0)
        gasto_ejecutado  = self.get_related_expenses(folio)
        monto_restante = round(monto_aprobado - gasto_ejecutado,2)
        anticipo_efectivo = self.query_get_anticipo(folio)
        # print('anticipo_efectivo', anticipo_efectivod)
        gasto_efectivo = self.get_cash_expenses(expense_group)
        monto_anticipo_restante = anticipo_efectivo - gasto_efectivo
        self.set_solicitud_catalog(folio)
        close_order = self.close_solicitud(monto_anticipo_restante, expense_group)
        destino = self.SOL_DATA.get(self.fdict['destino'])
        if destino == 'otro':
            destino = self.SOL_DATA.get(self.fdict['destino_otro'])
            
        update_fields = {
            f'answers.{self.CATALOG_SOL_VIAJE_OBJ_ID}': {
                self.fdict['cat_folio']: folio,
                self.fdict['cat_destino']: [ destino ],
            },
            f"answers.{self.fdict['anticipo_efectivo']}":anticipo_efectivo,
            f"answers.{self.fdict['monto_anticipo_restante']}":monto_anticipo_restante,
            f"answers.{self.fdict['monto_restante']}":monto_restante,
            f"answers.{self.fdict['gasto_ejecutado_efectivo']}":gasto_efectivo,
            f"answers.{self.fdict['gasto_ejecutado']}":gasto_ejecutado,
            f"answers.{self.fdict['grp_gastos_viaje']}":expense_group
            }
        if close_order:
            update_fields.update({
                f"answers.{self.fdict['status_solicitud']}":"cerrada",
                })
        update_db = self.cr.update_one({
            'folio': folio,
            'form_id': self.FORM_SOLICITUD_VIATICOS_ID,
            'deleted_at': {'$exists': False}
        },{'$set':update_fields})
        db_res = update_db.raw_result
        update_ok = db_res.get('updatedExisting')
        print('update_ok', update_ok)
        if update_ok:
            self.set_solicitud_data(folio, renew=True)
            update_ok = self.update_expense_catalog_values(folio)
        return update_ok

    def query_related_expenses_rec(self, folio_sol=None, answers={}, status=[]):
        match_query  = {
            'form_id': {'$in': [self.FORM_ID_GASTOS_VIAJE, self.FORM_ID_ENTREGA_EFECTIVO]},
            'deleted_at': {'$exists': False},
            # '$or':[
            #     {f'answers.{self.fdict["status_gasto"]}':'por_autorizar'}, 
            #     {f'answers.{self.fdict["status_gasto"]}':'autorizado'},
            #     {f'answers.{self.fdict["status_gasto"]}':'realizado'},
            #     {f'answers.{self.fdict["status_gasto"]}':'error'},
            #     {f'answers.{self.fdict["status_gasto"]}':'en_autorizacion'},
            #     ]
            }
        status_update = {"$or":[]}
        for s in status:
            status_update["$or"].append({f'answers.{self.fdict["status_gasto"]}':s})
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
        for r in records:
            res.append(r)
        if this_set:
            res.append(this_set)
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
        return records_to_process

    def query_folios_to_exclude(self, folios):
        match_query  = {
            'form_id':  self.FORM_ID_AUTORIZACIONES,
            'deleted_at': {'$exists': False},
            # '$or':[
            #      {f'answers.{self.fdict["estatus_solicitud_autorizacion"]}':'pendiente'}, 
            #      {f'answers.{self.fdict["estatus_solicitud_autorizacion"]}':'autorizado'}, 
            #      ]
            }
        query =[
            {'$match': match_query },
            {"$unwind":f"$answers.{self.fdict['grp_gastos_viaje']}"},
            {"$match":{
                f"answers.{self.fdict['grp_gastos_viaje']}.{self.fdict['grp_gasto_folio']}" : {"$in":folios}
                }
            },
            {"$project":{
                    "_id":0,
                    "folio":f"$answers.{self.fdict['grp_gastos_viaje']}.{self.fdict['grp_gasto_folio']}",
                }
            }
            ]
        records = self.cr.aggregate(query )
        return [r['folio'] for r in records]

    def get_folios_to_exclude(self, records_to_process):
        folios = []
        for r in records_to_process:
            if r.get(self.fdict['grp_gasto_folio']):
                folios.append(r[self.fdict['grp_gasto_folio']])
        folios_2_exclude = self.query_folios_to_exclude(folios)
        if folios_2_exclude:
            res = []
            for idx, r in enumerate(records_to_process):
                if r.get(self.fdict['grp_gasto_folio']) in folios_2_exclude:
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
        print('folio===2', folio)
        if folio:
            records_to_process = self.query_related_expenses_rec(folio)
            records_to_process = self.get_folios_to_exclude(records_to_process)
            print('records_to_process', records_to_process)
            if not records_to_process:
                print(f'No more records to process for this folio: {folio}')
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
                self.fdict['folio_solicitudes'] : folio,
                self.fdict['cat_monto_total_aprobado'] : self.SOL_DATA.get(self.fdict['approved_amount']),
                self.fdict['anticipo_efectivo'] : anticipo_efectivo,
                self.fdict['gasto_ejecutado'] : gasto_ejecutado,
                self.fdict['gasto_ejecutado_efectivo'] : gasto_efectivo,
                self.fdict['monto_anticipo_restante'] : monto_anticipo_restante,
                self.fdict['monto_restante'] : self.SOL_DATA.get(self.fdict['monto_restante']),
                self.fdict['date_from'] : date_from,
                self.fdict['date_to'] : date_to,
                self.fdict['cant_dias'] : cant_days,
                self.fdict['estatus_solicitud_autorizacion_uno'] : 'pendiente',
                self.fdict['estatus_solicitud_autorizacion'] : 'pendiente',
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
                    self.fdict['tipo_solicitud']:"gasto",
                    self.fdict['folio_solicitudes'] : folios,
                    }
                for f in folios:
                    records_to_process.append(self.query_related_expenses_rec(f))
                    anticipo_efectivo += self.query_get_anticipo(f)
                    gasto_ejecutado += self.get_related_expenses(f)


                if not records_to_process:
                    return []
                records_to_process = self.get_folios_to_exclude(records_to_process)
                gasto_efectivo = self.get_cash_expenses(records_to_process)
                monto_anticipo_restante = anticipo_efectivo - gasto_efectivo
                date_from, date_to = self.get_autorization_dates(records_to_process)
                cant_days = self.get_cant_days(date_from, date_to)
                new_record.update({
                    self.fdict['anticipo_efectivo'] : anticipo_efectivo,
                    self.fdict['gasto_ejecutado'] : gasto_ejecutado,
                    self.fdict['gasto_ejecutado_efectivo'] : gasto_efectivo,
                    self.fdict['monto_anticipo_restante'] : monto_anticipo_restante,
                    self.fdict['date_from'] : date_from,
                    self.fdict['date_to'] : date_to,
                    self.fdict['cant_dias'] : cant_days,
                    self.fdict['estatus_solicitud_autorizacion_uno'] : 'pendiente',
                    self.fdict['estatus_solicitud_autorizacion'] : 'pendiente',
                    self.fdict['grp_gastos_viaje'] : self.update_records(records_to_process)
                    })
                record_to_create.append(new_record)
        return record_to_create

    def create_expense_authorization(self, folio=None, autorizador={}):
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
                "answers":new_record
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
            folios.append(folio)
        folios = [r[self.fdict['grp_gasto_folio']] for r in expenses if r.get(self.fdict['grp_gasto_folio'])]
        data = {self.fdict['status_gasto']: 'en_autorizacion'}
        result = []
        result = self.lkf_api.patch_multi_record(
            data,
            self.FORM_REGISTRO_DE_GASTOS_DE_VIAJE, folios=folios
            )
        self.force_udpate(folios, data)
        #TODO SI NO SE ACTUALIZA FORZAR EN BASE DE DATOS.
        return result

    def query_folio_form(self, folios):
        query  = {
            'folio':  {"$in":folios},
            'deleted_at': {'$exists': False},
            }
        records = self.cr.find(query,{'form_id':1, 'folio':1} )
        return {r['folio']:r['form_id'] for r in records}

    def update_expense_data(self, dict_records_to_update, update=True):
        res = {}
        gasto_ejecutado_aprovado = 0
        gasto_ejecutado_efevo_aprovado = 0
        anticipo = 0
        #form_id = self.FORM_REGISTRO_DE_GASTOS_DE_VIAJE
        form_ids = self.query_folio_form(list(dict_records_to_update.keys()))
        print('form_ids', form_ids)
        for folio, gasto in dict_records_to_update.items():
            res[folio] = {}
            form_id = form_ids[folio]
            if gasto[self.fdict['grp_gasto_estatus']] == 'no_autorizado':
                gasto[self.fdict['grp_gasto_monto_aut']] = 0
            if gasto[self.fdict['grp_gasto_estatus']] == 'autorizado':
                if gasto[self.fdict['metodo_pago']].find('efectivo') >= 0 or \
                 gasto[self.fdict['metodo_pago']].find('debito') >= 0:
                    if form_id == self.FORM_ID_ENTREGA_EFECTIVO:
                        #si el monto es menor a 0 es un deposito
                        anticipo += gasto[self.fdict['grp_gasto_monto_aut']]  * -1
                        print('anticipooooooooooooooo', anticipo)
                    else:
                        #si el monto es menor a 0 es un deposito
                        gasto_ejecutado_efevo_aprovado += gasto[self.fdict['grp_gasto_monto_aut']]
                        gasto_ejecutado_aprovado += gasto[self.fdict['grp_gasto_monto_aut']]
                else:
                    gasto_ejecutado_aprovado += gasto[self.fdict['grp_gasto_monto_aut']]

            res[folio]['form_id'] = form_ids[folio]
            print('acutalizanod forma', form_ids[folio])
            print('acutalizanod folio', folio)
            if update:
                print('update info', {
                    self.fdict['status_gasto']: gasto[self.fdict['grp_gasto_estatus']],
                    self.fdict['grp_gasto_monto_aut']: gasto[self.fdict['grp_gasto_monto_aut']],#monto aturoizado
                    self.fdict['reason_no_authorized']: gasto.get(self.fdict['reason_no_authorized']),#motivo
                    })
                res_update = self.lkf_api.patch_multi_record(
                    {
                    self.fdict['status_gasto']: gasto[self.fdict['grp_gasto_estatus']],
                    self.fdict['grp_gasto_monto_aut']: gasto[self.fdict['grp_gasto_monto_aut']],#monto aturoizado
                    self.fdict['reason_no_authorized']: gasto.get(self.fdict['reason_no_authorized']),#motivo
                    }, form_ids[folio], folios=[folio])
                print('res_update', res_update)
                res[folio]['status_code'] = res_update.get('status_code')
        res['gasto_ejecutado_aprovado'] = gasto_ejecutado_aprovado
        res['gasto_ejecutado_efevo_aprovado'] = gasto_ejecutado_efevo_aprovado
        res['anticipo_efectivo'] = anticipo
        res['grp_gastos_viaje'] = list(dict_records_to_update.values())
        return res

    def update_autorization_records(self, answers):
        dict_records_to_update = {}
        form_id = self.FORM_REGISTRO_DE_GASTOS_DE_VIAJE
        # self.set_solicitud_data(folio)
        response = []
        for viatico in answers.get(self.fdict['grp_gastos_viaje'], []):
            folio_origen = viatico.get(self.fdict['grp_gasto_folio'], '')
            dict_records_to_update[folio_origen] = dict_records_to_update.get(folio_origen,{})
            # dict_records_to_update[folio_origen].update({
            #     'status': viatico.get(self.fdict['grp_gasto_estatus'], ''),
            #     'monto_autorizado': viatico.get(self.fdict['grp_gasto_monto_aut'], 0),
            #     'reason_no_authorized': viatico.get(self.fdict['reason_no_authorized'], None),
            #     'metodo_pago': viatico.get(self.fdict['metodo_pago'], None),
            # })
            dict_records_to_update[folio_origen].update(viatico)
        entregas_efevo = 0
        res = self.update_expense_data(dict_records_to_update, update=True)

        reproces = False
        for viatico in answers.get(self.fdict['grp_gastos_viaje'], []):
            folio_origen = viatico.get(self.fdict['grp_gasto_folio'], '')
            if res.get(folio_origen):
                print('status code', res[folio_origen]['status_code'])
                if res[folio_origen]['status_code'] != 202:
                    viatico[self.fdict['grp_gasto_estatus']] = 'error'
                    dict_records_to_update.pop(folio_origen)
                    reproces = True

        if reproces:
            res = self.update_expense_data(dict_records_to_update, update=False)

        answers[self.fdict['anticipo_efectivo']] = res['anticipo_efectivo'] 
        answers[self.fdict['gasto_ejecutado']] = res['gasto_ejecutado_aprovado'] 
        answers[self.fdict['gasto_ejecutado_efectivo']] = res['gasto_ejecutado_efevo_aprovado'] 
        answers[self.fdict['monto_anticipo_restante']] = res['anticipo_efectivo'] - res['gasto_ejecutado_efevo_aprovado']
        answers[self.fdict['grp_gastos_viaje']] = res['grp_gastos_viaje']

        return answers

