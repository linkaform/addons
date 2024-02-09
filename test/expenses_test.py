# -*- coding: utf-8 -*-
import time

from linkaform_api import utils, network, lkf_models
from linkaform_api import base

# from .conf import settings

#from conf import settings 

from account_settings import *

# settings.config.update(config)
# lkf_api = utils.Cache(settings)
# print('settings', settings.config)
# jwt_parent = lkf_api.get_jwt( api_key=settings.config['APIKEY'], user=settings.config['USERNAME'] )
# settings.config['JWT_KEY'] = jwt_parent
# # settings.config.update(config)
# lkf_api = utils.Cache(settings)
# net = network.Network(settings)
# cr = net.get_collections()
# lkm = lkf_models.LKFModules(settings)



lkf_obj = base.LKF_Base(settings)
lkm = lkf_obj.lkm
lkf_api = lkf_obj.lkf_api
cr = lkf_obj.cr

CATALOG_RESP_AUT = lkm.catalog_id('responsables_de_autorizar_gastos')
CATALOG_RESP_AUT_ID = CATALOG_RESP_AUT.get('id')
CATALOG_RESP_AUT_OBJ_ID = CATALOG_RESP_AUT.get('obj_id')
CATALOG_EMPLEADOS = lkm.catalog_id('catalogo_de_empleados')
CATALOG_EMPLEADOS_ID = CATALOG_EMPLEADOS.get('id')
CATALOG_EMPLEADOS_OBJ_ID = CATALOG_EMPLEADOS.get('obj_id')
CATALOG_MONEDA = lkm.catalog_id('moneda')
CATALOG_MONEDA_ID = CATALOG_MONEDA.get('id')
CATALOG_MONEDA_OBJ_ID = CATALOG_MONEDA.get('obj_id') 
CATALOG_SOLICITUD = lkm.catalog_id('solicitudes_de_gastos')
CATALOG_SOLICITUD_ID = CATALOG_SOLICITUD.get('id')
CATALOG_SOLICITUD_OBJ_ID = CATALOG_SOLICITUD.get('obj_id') 
CATALOG_CONCEPTO_GASTO = lkm.catalog_id('conceptos_de_gastos')
CATALOG_CONCEPTO_GASTO_ID = CATALOG_CONCEPTO_GASTO.get('id')
CATALOG_CONCEPTO_GASTO_OBJ_ID = CATALOG_CONCEPTO_GASTO.get('obj_id') 
FORM_SOLICITUD_VIATICOS  = lkm.form_id('solicitud_de_viticos','id')
FORM_REGISTROS_DE_GASTOS_DE_VIAJE  = lkm.form_id('registros_de_gastos_de_viaje','id')
FORM_AUTORIZACION_DE_VIATICOS = lkm.form_id('autorizacin_de_viaticos','id')
FORM_BANK_TRANSACTIONS = lkm.form_id('entrega_de_efectivo','id')

VARS = {'gasto':[]}
SOL = {}


class TestExpenses():

    def get_record_from_db(self, form_id, folio, extra_filters={}):
        query = {
            'form_id': form_id,
            'folio': folio,
            'deleted_at': {'$exists': False}
        }
        if not folio and extra_filters:
            query.pop('folio')
            query.update(extra_filters)
        select_columns = {'folio':1,'user_id':1,'form_id':1,'answers':1}
        record_found = cr.find(query, select_columns)
        return record_found
    
    def test_crea_solicitud(self):
        global VARS
        metadata = {
            "form_id":FORM_SOLICITUD_VIATICOS,
            "geolocation":[25.6583943,-100.3834899],"start_timestamp":1690262982.602,"end_timestamp":1690263046.524,
            "answers":{
                "61041d15d9ee55ab14965bb6":"solicitado",
                "64dd637965b8662fabb5ac2d": "no",
                "64dd637965b8662fabb5ac2f": "no",
                CATALOG_EMPLEADOS_OBJ_ID:{ #catalogo de empleados
                    "6092c0ebd8b748522446af26": "Obi-Wan Kenobi",
                    "6092c0ebd8b748522446af27": ["Jedi Master"],
                    "6092c0ebd8b748522446af28": ["obi@starwars.com"]},
                CATALOG_MONEDA_OBJ_ID:{ #catalogo de monedas
                    "62aa1fa92c20405af671d123":"MXN"},
                CATALOG_RESP_AUT_OBJ_ID:{ #catalogo de autorizadores
                    "62bf232626827cd253f9db16":"Yoda",
                    "62bf232626827cd253f9db17":["yoda@starwars.com"]},
                "61041b50d9ee55ab14965000": "mexico",
                "61041b50d9ee55ab14965ba1": "cita_cliente",
                "61041b50d9ee55ab14965ba2": "2023-12-19",
                "61041b50d9ee55ab14965ba3": "2023-12-23",
                "61041b50d9ee55ab14965ba4": "autobus",
                "61041c9a9242368dd3965da2": 1000,
                "61041b8370c14c09eff167ae": 5000,
                "544d5ad901a4de205f392000": 1500,
                "62ea709180209ea195b75221": {
                    "file_name": "Kenovi",
                    "file_url": "https://f001.backblazeb2.com/file/app-linkaform/public-client-20/108431/62ea709180209ea195b75221/65807f460f1a4c2a7ab74315.png"
                }
            },
            "folio":None,
            "properties":{
                "device_properties":{"system":"Testing"},
                }
            ,"geolocation_method":{"method":"HTML5","accuracy":1742.3649855282526}
            }

        res_create =  lkf_api.post_forms_answers(metadata)
        print('res_create',res_create)
        assert res_create['status_code'] == 201
        VARS['solicitud'] = {'id':res_create['json']['id'],'folio':res_create['json']['folio']}

    def test_aprueba_solicitud(self):
        #self.test_crea_solicitud()
        #global VARS
        metadata = {
            "form_id":FORM_SOLICITUD_VIATICOS,
            "geolocation":[25.6583943,-100.3834899],"start_timestamp":1690391904.746,"end_timestamp":1690391923.696,
            "answers":  {
                 "61041d15d9ee55ab14965bb6":"autorizado",
                CATALOG_EMPLEADOS_OBJ_ID:{ #catalogo de empleados
                    "6092c0ebd8b748522446af26": "Obi-Wan Kenobi",
                    "6092c0ebd8b748522446af27": ["Jedi Master"],
                    "6092c0ebd8b748522446af28": ["obi@starwars.com"]},
                CATALOG_MONEDA_OBJ_ID:{ #catalogo de monedas
                    "62aa1fa92c20405af671d123":"MXN"},
                CATALOG_RESP_AUT_OBJ_ID:{ #catalogo de autorizadores
                    "62bf232626827cd253f9db16":"Yoda",
                    "62bf232626827cd253f9db17":["yoda@starwars.com"]},
                "61041b50d9ee55ab14965000":"mexico",
                "61041b50d9ee55ab14965ba1":"cita_cliente",
                "61041b50d9ee55ab14965ba2":"2023-12-19",
                "61041b50d9ee55ab14965ba3": "2023-12-23",
                "61041b50d9ee55ab14965ba4":"autobus",
                "61041b8370c14c09eff167ae":5000,
                "649ccd3e7880ff495300bca5":0,
                "61041d15d9ee55ab14965bb7": 5000,
                "544d5ad901a4de205f392000": 1500,
                "61041b50d9ee55ab14965ba0": "Mexico",
                "61041c9a9242368dd3965da2": 1000,
                "61041d15d9ee55ab14965bb5": 5,
                "62ea709180209ea195b75221": {
                    "file_name": "Kenovi",
                    "file_url": "https://f001.backblazeb2.com/file/app-linkaform/public-client-20/108431/62ea709180209ea195b75221/65807f460f1a4c2a7ab74315.png"
                },
                "64dd637965b8662fabb5ac2d": "no",
                "64dd637965b8662fabb5ac2f": "no",
                "62aa1fa92c20405af671d124": None,
                "62ea709180209ea195b75222": {
                    "file_name": "Yoda",
                    "file_url": "https://f001.backblazeb2.com/file/app-linkaform/public-client-20/108431/62ea709180209ea195b75222/6580801c0f1a4c2a7ab74325.png"
                }

            },
            "_id":VARS['solicitud']['id'],
            "properties":{
                "device_properties":{"system":"Testing"},
                },
            "geolocation_method":{"method":"HTML5","accuracy":1742.3649855282526}}
        res_create =  lkf_api.patch_record(metadata)
        assert res_create['status_code'] == 202
        time.sleep(10)
        solnum = VARS['solicitud']['folio']
        sol_catalog = self.search_catalogo_solicitud(solnum)
        assert SOL[solnum]['folio'] ==  VARS['solicitud']['folio']

    def test_autoriza_anticipo_solicitado(self):
        #filter_by_folio = {'answers.64fa516c95f2011d20462578.610419b5d28657c73e36fcd3': VARS['solicitud']['folio']}
        record_anticipo_solicitado = self.get_record_from_db(FORM_BANK_TRANSACTIONS, VARS['solicitud']['folio'])
        for anticipo in record_anticipo_solicitado:
            anticipo['answers']['583d8e10b43fdd6a4887f55b'] = '2023-12-19'
            anticipo['answers']['544d5ad901a4de205f391111'] = anticipo['answers']['544d5ad901a4de205f392000']
            anticipo['answers']['544d5b4e01a4de205e2b2169'] = 'realizado'
            anticipo['properties'] = {"device_properties":{"system":"Testing"}}
            res_update = lkf_api.patch_record(anticipo)
            assert res_update['status_code'] == 202
            time.sleep(5)

    def test_registros_de_gasto(self):
        #global SOL
        total = 0
        total_empleado = 0
        CANT_GASTOS = 5
        for x in range(CANT_GASTOS):
            gasto = (x +1) * 100
            total_empleado += gasto
            res = self.create_registros_de_gasto(num=VARS['solicitud']['folio'], gasto=gasto, pagado_por="empleado")
            assert res['status_code'] == 201
            time.sleep(3)
        #time.sleep(8)
        total += total_empleado

        # Agrego un gasto para dejar en ceros
        gsto_copania = 3500
        res = self.create_registros_de_gasto(num=VARS['solicitud']['folio'], gasto=gsto_copania, pagado_por="compañia")
        assert res['status_code'] == 201
        total += gsto_copania
        CANT_GASTOS += 1
        time.sleep(3)

        solnum = VARS['solicitud']['folio']
        sol_catalog = self.search_catalogo_solicitud(solnum)

        # HASTA AQUI TODO EN ORDEN ME QUEDE HASTA DONDE SE CREAN LOS REGISTROS DE GASTOS
        # FALTA VALIDAR LO DE ABAJO

        print('sol', SOL)
        print('anticipo restante...',SOL[solnum]['monto_anticipo_restante'])
        print('anticipo_efectivo...',SOL[solnum]['anticipo_efectivo'])
        print('total...',total)
        assert SOL[solnum]['monto_anticipo_restante'] == SOL[solnum]['anticipo_efectivo'] - total_empleado
        assert SOL[solnum]['monto_restante'] == SOL[solnum]['monto_aprobado'] - total
        # res_update = self.cerrar_solicitud(SOL[solnum]['folio'])
        autorizacion = self.search_autorizacion(SOL[solnum]['folio'])
        # assert len(autorizacion) > 0
        metadata = lkf_api.get_metadata(FORM_AUTORIZACION_DE_VIATICOS)
        FOUND_GASTOS = 0
        for rec in autorizacion:
            print('aut_folio =',rec['folio'])
            self.autorize_expenses(rec)
            aut_ans = rec.get('answers')
            gastos = aut_ans.get('62aa1ed283d55ab39a49bd2d')
            desc = 1
            for gasto in gastos:
                if gasto['62aa1fa92c20405af671d122'] < 0:
                    continue
                FOUND_GASTOS +=1
                print('gastos....', FOUND_GASTOS)
                if desc == 2 or desc ==4:
                    status = 'no_autorizado'
                    gto_autorizdo = 0
                else:
                    status = 'autorizado'
                    gasto['627bf0d5c651931d3c7eedd3'] = round(gasto['62aa1fa92c20405af671d122'] * (1-(desc/10.1)),2)
                    gto_autorizdo = f'descuento de {(1-(desc/10.1))}'
                
                gasto['64a06441c375083cb0da8d4f'] = gto_autorizdo
                gasto['62aa1fa92c20405af671d124'] = status
                desc += 1
            aut_ans['62954ccb8e54c96dc34995a5'] = 'autorizado'
            # aut_ans['']
            # rec['_id'] = rec['id']
            print('\n\n\n\n\n')
            print('metadata=',metadata)
            update_aut = lkf_api.patch_record(rec)
            print('update_aut', update_aut)
        assert FOUND_GASTOS == CANT_GASTOS

    def search_catalogo_solicitud(self, num='1'):
        global SOL
        folio = VARS['solicitud']['folio']
        mango_query = {"selector":
        {"answers":
            {"$and":[
                {'610419b5d28657c73e36fcd3': {'$eq': folio}}
        ]}},
        "limit":1,
        "skip":0}
        print('mango_query', mango_query)
        print('CATALOG_SOLICITUD_ID', CATALOG_SOLICITUD_ID)
        res = lkf_api.search_catalog(CATALOG_SOLICITUD_ID, mango_query)
        print('res=', res)
        if len(res) > 0:
            res = res[0]
        else:
            retry = 0
            while retry < 4:
                print('retry', retry)
                time.sleep(1)
                res = lkf_api.search_catalog(CATALOG_SOLICITUD_ID, mango_query)
                if len(res) > 0:
                    res = res[0]
                    retry = 4
                else:
                    retry += 1
        if not res:
            assert 'Search Catalog Folio Not Found' == 'Not Found'
        SOL[num] = {}
        SOL[num]['folio'] = res.get('610419b5d28657c73e36fcd3')
        SOL[num]['destino'] = res.get('610419b5d28657c73e36fcd4')
        SOL[num]['fecha_salida'] = res.get('610419b5d28657c73e36fcd5')
        SOL[num]['fecha_regreso'] = res.get('610419b5d28657c73e36fcd6')
        SOL[num]['monto_aprobado'] = res.get('610419e33a05c520d90814d3',0)
        SOL[num]['anticipo_efectivo'] = res.get('649d02057880ff495300bcc0',0)
        SOL[num]['gasto_ejecutado'] = res.get('629fb33a8758b5808890b22e',0)
        SOL[num]['gasto_efevo'] = res.get('649d02057880ff495311bcc0',0)
        SOL[num]['monto_anticipo_restante'] = res.get('649d02057880ff495300bcc1',0)
        SOL[num]['monto_restante'] = res.get('629fb33a8758b5808890b22f',0)
        SOL[num]['tipo_solicitud'] = res.get('649b512cbf4cc1fab1133b7a')
        SOL[num]['status'] = res.get('610419b5d28657c73e36fcd7')
        return res

    def create_registros_de_gasto(self, num='1', gasto=100, pagado_por="empleado"):
        global SOL
        metadata = {
            "form_id":FORM_REGISTROS_DE_GASTOS_DE_VIAJE,
            "geolocation":[25.6583943,-100.3834899],
            "start_timestamp":1690407499.739,"end_timestamp":1690407732.544,
            "answers":{
                "62914e2d855e9abc32eabc17":gasto, #cantidad
                CATALOG_MONEDA_OBJ_ID:{"62aa1fa92c20405af671d123":"MXN"},
                "65a0925c6a3fdf3e32659bb8":pagado_por,
                "544d5b4e01a4de205e2b2169":"por_autorizar",
                CATALOG_SOLICITUD_OBJ_ID :{
                    "610419b5d28657c73e36fcd4":SOL[num]['destino'],
                    "610419b5d28657c73e36fcd3":SOL[num]['folio'],
                    "610419b5d28657c73e36fcd5":[SOL[num]['fecha_salida']],
                    "610419b5d28657c73e36fcd6":[SOL[num]['fecha_regreso']],
                    "610419e33a05c520d90814d3":[SOL[num]['monto_aprobado']],
                    "629fb33a8758b5808890b22e":[SOL[num]['gasto_ejecutado']],
                    "649d02057880ff495311bcc0":[SOL[num]['gasto_efevo']],
                    "649d02057880ff495300bcc1":[SOL[num]['monto_anticipo_restante']],
                    "629fb33a8758b5808890b22f":[SOL[num]['monto_restante']]
                },
                CATALOG_CONCEPTO_GASTO_OBJ_ID:{"649b2a84dac4914e02aadb24":"Comida"},
                "610420eea79102768d9659b4":[],
                "583d8e10b43fdd6a4887f55b":"2023-12-20",
                "610878f5bff8b3329fed6130":"cena",
                "62914e2d855e9abc32eabc16":"Purebas",
                "64e6474175eab52e0956ae3f":"Establecimiento  - {}".format(gasto),
            },
            "folio":None,
            "properties":{
                "device_properties":{"system":"Testing"},
                },
            "geolocation_method":{"method":"HTML5","accuracy":1742.3649855282526}
        }        
        res_create =  lkf_api.post_forms_answers(metadata)
        print('res_create gastos =',res_create)
        VARS['gasto'].append({'id':res_create['json']['id'],'folio':res_create['json']['folio']})
        return res_create

    def autorize_expenses(self, rec):
        print('dd')

    def cerrar_solicitud(self, folio):
        res_update = lkf_api.patch_multi_record(
            {'61041d15d9ee55ab14965bb6': 'en_aprobacion'}, 
            FORM_SOLICITUD_VIATICOS, folios=[folio], threading=True)
        return res_update

    def search_autorizacion(self, folio):
        aut_folio = f'{folio}-1'
        #print('aut_folio=', aut_folio)
        time.sleep(7)
        #get_rec= lkf_api.get_record_answer({"form_id":FORM_AUTORIZACION_DE_VIATICOS, 'folio':aut_folio})
        get_rec = self.get_record_from_db(FORM_AUTORIZACION_DE_VIATICOS, '', extra_filters={'answers.64fa516c95f2011d20462578.610419b5d28657c73e36fcd3': folio})
        return get_rec








