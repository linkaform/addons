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

from linkaform_api import base
from lkf_addons.addons.product.app import Product, Warehouse
from lkf_addons.addons.base.app import Base


### Objecto de Modulo ###
'''
Cada modulo puede tener N objetos, configurados en clases.
Estos objetos deben de heredar de base.LKF_Base) y cualquier modulo dependiente
Al hacer el super() del __init__(), heredamos las variables de configuracion de clase.
Se pueden heredar funciones de cualquier clase heredada con el metodo super(). 
'''
# class Stock(Employee, Warehouse, Product, base.LKF_Base):

from lkf_addons.addons.product.app import Product, Warehouse


class JIT(Product, base.LKF_Base):


    def __init__(self, settings, sys_argv=None, use_api=False, **kwargs):
        # from lkf_addons.addons.stock.app import Stock
        #base.LKF_Base.__init__(self, settings, sys_argv=sys_argv, use_api=use_api)
        self.mf = {}
        self.mf.update({
            'bom_group_qty_in':'66d8e09cb22bcdcc2f341e85',
            'bom_group_qty_out':'66da962859bec54a05c73e00',
            'bom_group_qty_throughput':'66da962859bec54a05c73e01',
            'bom_group_step':'66d8e7b0b22bcdcc2f341e88',
            'consumo_promedio_diario':'66ec770cc9aefada5b04b7a6',
            'fecha_demanda':'66ea6c28c9aefada5b04b76c',
            'input_goods_product_code':'71ef32bcdf0ec2ba73dec33d',
            'input_goods_product_name':'71ef32bcdf0ec2ba73dec33e',
            'input_goods_sku':'75dec64a3199f9a040829243',
            'raw_material_group':'66d8dff5b22bcdcc2f341e83',
            'safety_stock':'66ea62dac9aefada5b04b738',
            'min_stock':'66ea62dac9aefada5b04b739',
            'max_stock':'66ea62dac9aefada5b04b73a',
            'demanda_12_meses':'66ea6c61c9aefada5b04b76e',
            'procurment_date':'66da0c19b22bcdcc2f341f06',
            'procurment_method':'66d92acdb22bcdcc2f341ebf',
            'procurment_schedule_date':'66da538cb22bcdcc2f341f47',
            'procurment_qty':'66da3bddb22bcdcc2f341f08',
            'procurment_status':'66da0c19b22bcdcc2f341f07',
            'trigger':'66eb14ffc9aefada5b04b793',
            'reorder_point':'66ea62dac9aefada5b04b73b',
            })
        kwargs = kwargs.get('f',
            {
                'bom_name':'66d8e063b22bcdcc2f341e84',
                'bom_type':'66d8dfbcb22bcdcc2f341e81',
                'bom_status':'66e275891f6f133e363afb3f',
                'demora':'66ea62dac9aefada5b04b737',
                'lead_time':'66d8ee99b22bcdcc2f341e8a',
                'dias_laborales_consumo':'66ececbcc9aefada5b04b800',
                'factor_crecimiento_jit':'66ececbcc9aefada5b04b801',
                'factor_seguridad_jit':'66ececbcc9aefada5b04b802',
                'status':'620ad6247a217dbcb888d175',
                'tipo_almacen': '66ed0c88c9aefada5b04b818'
            }
            )
        from lkf_addons.addons.product.app import Product, Warehouse

        self.WH = Warehouse( settings, sys_argv=sys_argv, use_api=use_api, **kwargs)
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api, f=kwargs)
        # from lkf_addons.addons.stock.app import Stock
        # self.STOCK = Stock( settings, sys_argv=sys_argv, use_api=use_api, **kwargs)

        self.WH = Warehouse( settings, sys_argv=sys_argv, use_api=use_api, **kwargs)
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api, f=kwargs)
        #Formas
        self.BOM_ID = self.lkm.form_id('bom','id')
        self.DEMANDA_UTIMOS_12_MES = self.lkm.form_id('demanda_ultimos_12_meses','id')
        self.PROCURMENT = self.lkm.form_id('procurment_record','id')
        self.REGLAS_REORDEN = self.lkm.form_id('reglas_de_reorden','id')

        #Catalogos
        self.BOM_CAT = self.lkm.catalog_id('bom')
        self.BOM_CAT_ID = self.BOM_CAT.get('id')
        self.BOM_CAT_OBJ_ID = self.BOM_CAT.get('obj_id')

        self.INPUT_GOODS = self.lkm.catalog_id('input_goods_products')
        self.INPUT_GOODS_ID = self.INPUT_GOODS.get('id')
        self.INPUT_GOODS_OBJ_ID = self.INPUT_GOODS.get('obj_id')

        self.INPUT_GOODS_SKU = self.lkm.catalog_id('input_goods_sku')
        self.INPUT_GOODS_SKU_ID = self.INPUT_GOODS_SKU.get('id')
        self.INPUT_GOODS_SKU_OBJ_ID = self.INPUT_GOODS_SKU.get('obj_id')

    def ave_daily_demand(self):
        print('average daly cons', self.form_id)
        if self.form_id == self.DEMANDA_UTIMOS_12_MES:
            print('va por ultimos 12 meses>>>>>>')
            conf_data = self.get_config(*['dias_laborales_consumo', 'factor_crecimiento_jit'])
            dias_laborales_consumo = conf_data.get('dias_laborales_consumo',360)
            factor_crecimiento_jit = conf_data.get('factor_crecimiento_jit')
            demanda_12_meses = self.answers.get(self.mf['demanda_12_meses'])
            print('demanda_12_meses',demanda_12_meses)
            print('factor_crecimiento_jit',factor_crecimiento_jit)
            print('dias_laborales_consumo',dias_laborales_consumo)
            if demanda_12_meses:
                self.answers[self.mf['consumo_promedio_diario']] = f"{demanda_12_meses/dias_laborales_consumo:.2f}"
        return True

    def balance_warehouse(self, warehouse=None, location=None, product_code=None, sku=None, status='active'):
        product_rules = self.get_reorder_rules(
            warehouse=warehouse, 
            location=location, 
            product_code=product_code, 
            sku=sku, 
            status=status)

        res = []
        product_by_warehouse = {}
        for rule in product_rules:
            product_code = rule.get('product_code')
            sku = rule.get('sku')
            warehouse = rule.get('warehouse')
            product_by_warehouse[warehouse] = product_by_warehouse.get(warehouse,[])
            print('rule', rule)
            location = rule.get('warehouse_location')
            # product_stock = self.STOCK.get_product_stock(product_code, sku=sku,  warehouse=warehouse, location=location)
            product_stock = {'actuals':0}
            order_qty = self.exec_reorder_rules(rule, product_stock)
            if order_qty:
                ans = self.model_procurment(order_qty, product_code, sku, warehouse, location, procurment_method='buy')
                product_by_warehouse[warehouse].append(ans)
        response = self.upsert_procurment(product_by_warehouse)
        return response

    def calc_safety_stock(self, ave_daily_demand, lead_time, demora, safty_factor=1):
        print('ave_daily_demand',ave_daily_demand)
        print('lead_time',lead_time)
        print('safty_factor',safty_factor)
        #return round(ave_daily_demand * lead_time * safty_factor,2)
        return round(ave_daily_demand * demora * safty_factor,2)

    def calc_max_stock(self, ave_daily_demand, lead_time, safety_stock):
        return self.calc_min_stock(ave_daily_demand, lead_time, safety_stock) * 2

    def calc_min_stock(self, ave_daily_demand, lead_time, safety_stock):
        #return round((ave_daily_demand * lead_time) + safety_stock,2)
        return round((ave_daily_demand * lead_time) ,2)

    # def calc_reorder_point(self, ave_daily_demand, lead_time, safety_stock):
    #     return round((ave_daily_demand * lead_time) + safety_stock)

    def calc_reorder_point(self, min_stock, safety_stock):
        return round(min_stock + safety_stock)

    def create_procurment(self,  answers, **kwargs):
        metadata = self.lkf_api.get_metadata(self.PROCURMENT)
        properties = {
                "device_properties":{
                    "system": "Script",
                    "process": "Create Procurment", 
                    "accion": 'create_procurment', 
                    "folio from": self.folio, 
                    "archive": "jit/app.py",
                },
            }
        metadata.update({
            'properties': properties,
            'kwargs': kwargs,
            'answers': {}
            },
        )
        if type(answers) == dict:
            answers = [answers,]

        result = [dict(metadata, answers=answer) for answer in answers]
        response = self.lkf_api.post_forms_answers_list(result)
        print('response', response)
        return response

    def create_reorder_rule(self, answers, **kwargs):
        metadata = self.lkf_api.get_metadata(self.REGLAS_REORDEN)
        properties = {
                "device_properties":{
                    "system": "Script",
                    "process": "Create Reorder Rule", 
                    "accion": 'create_reorder_rule', 
                    "archive": "jit/app.py",
                },
            }
        metadata.update({
            'properties': properties,
            'kwargs': kwargs,
            'answers': {}
            },
        )
        if type(answers) == dict:
            answers = [answers,]

        result = [dict(metadata, answers=answer) for answer in answers]
        response = self.lkf_api.post_forms_answers_list(result)
        print('response=',response)
        return response

    def exec_reorder_rules(self, rule, product_stock):
        order_qty = 0
        reorder_point = rule.get('reorder_point',0)
        max_stock = rule.get('max_stock',0)
        actuals = product_stock.get('actuals',0)
        if actuals < reorder_point:
            order_qty = max_stock - actuals
        return order_qty
   
    def explote_kit(self, bom_lines, warehouse=None, location=None):
        res = []
        for line in bom_lines:
            move_status = line.get('inv_adjust_grp_status',None)
            if move_status == 'done':
                res.append(line)
                continue
            new_line = self.get_bom_products(line, warehouse, location, bom_type='kit')
            res += new_line
        return res

    def get_bom_products(self, bom_line, warehouse=None, location=None, bom_type='manufacture'):
        product_code = bom_line.get('product_code')
        sku = bom_line.get('sku')
        qty = bom_line.get('move_group_qty')
        bom_res = self.get_product_boms(product_code, sku, qty, warehouse=warehouse, location=location, bom_type=bom_type)
        if bom_res:
            return bom_res
        else:
            return [bom_line,]

    def get_product_boms(self, product_code, product_sku, qty=1, warehouse=None, location=None, bom_type='manufacture'):
        match_query ={ 
             'form_id': self.BOM_ID,  
             'deleted_at' : {'$exists':False},
             f'answers.{self.SKU_OBJ_ID}.{self.f["product_code"]}': product_code,
             f'answers.{self.SKU_OBJ_ID}.{self.f["product_sku"]}': product_sku,
             f'answers.{self.f["bom_type"]}': bom_type,
             f'answers.{self.f["bom_status"]}': 'active',
         } 
        query = [
            {'$match': match_query},
            {'$sort': {'created_at': 1}},
            {'$limit':1},
            {'$unwind':f'$answers.{self.mf["raw_material_group"]}'},
            {'$project':{
                    '_id':0,
                    'bom_name':f'$answers.{self.f["bom_name"]}',
                    'bom_type':f'$answers.{self.f["bom_type"]}',
                    'product_code':f'$answers.{self.mf["raw_material_group"]}.{self.INPUT_GOODS_SKU_OBJ_ID}.{self.mf["input_goods_product_code"]}',
                    'product_name':f'$answers.{self.mf["raw_material_group"]}.{self.INPUT_GOODS_SKU_OBJ_ID}.{self.mf["input_goods_product_name"]}',
                    'sku':f'$answers.{self.mf["raw_material_group"]}.{self.INPUT_GOODS_SKU_OBJ_ID}.{self.mf["input_goods_sku"]}',
                    'qty_in':f'$answers.{self.mf["raw_material_group"]}.{self.mf["bom_group_qty_in"]}',
                    'qty_out':f'$answers.{self.mf["raw_material_group"]}.{self.mf["bom_group_qty_out"]}',
                    'qty_throughput':f'$answers.{self.mf["raw_material_group"]}.{self.mf["bom_group_qty_throughput"]}',
                    'step':f'$answers.{self.mf["raw_material_group"]}.{self.mf["bom_group_step"]}',
            }},
            ]
        cr_res =  self.cr.aggregate(query)
        res = []
        for prod in cr_res:
            qty_in = prod.get('qty_in', 0)
            qty_out = prod.get('qty_out', 0)
            qty_throughput = qty_in - qty_out
            prod['product_name'] = self.unlist(prod.get('product_name',''))
            prod['qty'] = qty_throughput * qty
            res.append(prod)
        return res
    
    def get_procurments(self, warehouse=None, location=None, product_code=None, sku=None, status='programed', group_by=False):
        match_query ={ 
             'form_id': self.PROCURMENT,  
             'deleted_at' : {'$exists':False},
             f'answers.{self.mf["procurment_status"]}': status,
         }
        if product_code:
            match_query.update({
                f"answers.{self.SKU_OBJ_ID}.{self.f['product_code']}":product_code
                })
        if sku:
            match_query.update({
                f"answers.{self.SKU_OBJ_ID}.{self.f['sku']}":sku
                })
        if warehouse:
            match_query.update({
                f"answers.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.WH.f['warehouse']}":warehouse
                })
        if location:
            match_query.update({
                f"answers.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.WH.f['warehouse_location']}":location
                })
        query = [
            {'$match': match_query},
            {'$project':{
                    '_id':0,
                    'bom_name':f'$answers.{self.BOM_CAT_OBJ_ID}.{self.f["bom_name"]}',
                    'date':f'$answers.{self.mf["procurment_date"]}',
                    'date_schedule':f'$answers.{self.mf["procurment_schedule_date"]}',
                    'procurment_method':f'$answers.{self.mf["procurment_method"]}',
                    'procurment_qty':f'$answers.{self.mf["procurment_qty"]}',
                    'product_code':f'$answers.{self.SKU_OBJ_ID}.{self.f["product_code"]}',
                    'sku':f'$answers.{self.SKU_OBJ_ID}.{self.f["sku"]}',
                    'status':f'$answers.{self.f["status"]}',
                    'uom':f'$answers.{self.UOM_OBJ_ID}.{self.f["uom"]}',
                    'warehouse':f'$answers.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.WH.f["warehouse"]}',
                    'warehouse_location':f'$answers.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.WH.f["warehouse_location"]}',
            }},
            ]
        print('query=', simplejson.dumps(query, indent=3))
        return self.format_cr(self.cr.aggregate(query))

    def get_reorder_rules(self, warehouse=None, location=None, product_code=None, sku=None, status='active', group_by=False):
        match_query ={ 
             'form_id': self.REGLAS_REORDEN,  
             'deleted_at' : {'$exists':False},
             f'answers.{self.f["status"]}': status,
         }
        if product_code:
            match_query.update({
                f"answers.{self.SKU_OBJ_ID}.{self.f['product_code']}":product_code
                })
        if sku:
            match_query.update({
                f"answers.{self.SKU_OBJ_ID}.{self.f['sku']}":sku
                })
        if warehouse:
            match_query.update({
                f"answers.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.WH.f['warehouse']}":warehouse
                })
        if location:
            match_query.update({
                f"answers.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.WH.f['warehouse_location']}":location
                })
        query = [
            {'$match': match_query},
            {'$project':{
                    '_id':0,
                    'bom_name':f'$answers.{self.BOM_CAT_OBJ_ID}.{self.f["bom_name"]}',
                    'demora':f'$answers.{self.f["demora"]}',
                    'product_code':f'$answers.{self.SKU_OBJ_ID}.{self.f["product_code"]}',
                    'lead_time':f'$answers.{self.f["lead_time"]}',
                    'min_stock':f'$answers.{self.mf["min_stock"]}',
                    'max_stock':f'$answers.{self.mf["max_stock"]}',
                    'reorder_point':f'$answers.{self.mf["reorder_point"]}',
                    'safety_stock':f'$answers.{self.mf["safety_stock"]}',
                    'sku':f'$answers.{self.SKU_OBJ_ID}.{self.f["sku"]}',
                    'status':f'$answers.{self.f["status"]}',
                    'trigger':f'$answers.{self.mf["trigger"]}',
                    'uom':f'$answers.{self.UOM_OBJ_ID}.{self.f["uom"]}',
                    'warehouse':f'$answers.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.WH.f["warehouse"]}',
                    'warehouse_location':f'$answers.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.WH.f["warehouse_location"]}',
            }},
            ]
        return self.format_cr(self.cr.aggregate(query))

    def get_product_average_demand_by_warehouse(self):
        #TODO obtener de registros de formularios o de salidas de almacen
        match_query ={ 
             'form_id': self.DEMANDA_UTIMOS_12_MES,  
             'deleted_at' : {'$exists':False},
         } 
        query = [
            {'$match': match_query},
            {'$project':{
                    '_id':1,
                    'folio':'$folio',
                    'sku':f'$answers.{self.SKU_OBJ_ID}.{self.f["product_sku"]}',
                    'product_code':f'$answers.{self.SKU_OBJ_ID}.{self.f["product_code"]}',
                    'warehouse':f'$answers.{self.WH.WAREHOUSE_OBJ_ID}.{self.WH.f["warehouse"]}',
                    'demanda_12_meses':f'$answers.{self.mf["demanda_12_meses"]}',
                    'consumo_promedio_diario':f'$answers.{self.mf["consumo_promedio_diario"]}',
                    'fecha':f'$answers.{self.mf["fecha_demanda"]}',
                }
            },
            {'$sort':{'fecha':-1}},
            {'$group':{
                '_id':{
                    'product_code':'$product_code',
                    'sku':'$sku',
                    'warehouse':'$warehouse',
                },
                'folio':{'$first':'$folio'},
                'demanda_12_meses': {'$first': '$demanda_12_meses' },
                'consumo_promedio_diario':{'$first':'$consumo_promedio_diario'},
            }}
            ]
        return self.format_cr(self.cr.aggregate(query))

    def get_warehouse_config(self, key, value, get_key):
        config = self.get_config(*['procurment_location'])
        locations_config = config.get('procurment_location',[])
        res = None
        for wh in locations_config:
            if wh.get(key) and wh[key] == value:
                res = wh.get(get_key)
        return res

    def model_procurment(self, qty, product_code, sku, warehouse, location, uom=None, schedule_date=None, \
        bom=None, status='programed', procurment_method='buy'):
        print('location', location)
        print('location', locationds)
        answers = {}
        config = self.get_config(*['uom'])

        if not schedule_date:
            schedule_date = self.today_str()
        if not location:
            location = self.get_warehouse_config('tipo_almacen', 'abastacimiento', 'warehouse_location')
        if not uom:
            uom = config.get('uom')

        answers[self.SKU_OBJ_ID] = {}
        answers[self.SKU_OBJ_ID][self.f['product_code']] = product_code
        answers[self.SKU_OBJ_ID][self.f['sku']] = sku
        answers[self.UOM_OBJ_ID] = {}
        answers[self.UOM_OBJ_ID][self.f['uom']] = uom
        answers[self.WH.WAREHOUSE_LOCATION_OBJ_ID] = {}
        answers[self.WH.WAREHOUSE_LOCATION_OBJ_ID][self.WH.f['warehouse']] = warehouse
        answers[self.WH.WAREHOUSE_LOCATION_OBJ_ID][self.WH.f['warehouse_location']] = location
        answers[self.mf['procurment_date']] = self.today_str()
        answers[self.mf['procurment_method']] = procurment_method
        answers[self.mf['procurment_qty']] = qty
        answers[self.mf['procurment_status']] = status
        answers[self.mf['procurment_schedule_date']] = schedule_date

        return answers

    def model_reorder_point(self, product_code, sku, uom, warehouse, location, ave_daily_demand ):
        answers = {}
        config = self.get_config(*['lead_time', 'demora', 'factor_seguridad_jit','factor_crecimiento_jit','uom'])
        lead_time = config.get('lead_time')
        demora = config.get('demora')
        safety_factor = config.get('factor_seguridad_jit',1)
        factor_crecimiento_jit = config.get('factor_crecimiento_jit',1)
        answers[self.SKU_OBJ_ID] = {}
        answers[self.SKU_OBJ_ID][self.f['product_code']] = product_code
        answers[self.SKU_OBJ_ID][self.f['sku']] = sku
        if not uom:
            uom = config.get('uom')
        answers[self.UOM_OBJ_ID] = {}
        answers[self.UOM_OBJ_ID][self.f['uom']] = uom
        answers[self.WH.WAREHOUSE_LOCATION_OBJ_ID] = {}
        answers[self.WH.WAREHOUSE_LOCATION_OBJ_ID][self.WH.f['warehouse']] = warehouse
        answers[self.WH.WAREHOUSE_LOCATION_OBJ_ID][self.WH.f['warehouse_location']] = location
        answers[self.f['lead_time']] = lead_time
        answers[self.f['demora']] = demora
        answers[self.mf['safety_stock']] = self.calc_safety_stock(ave_daily_demand, lead_time, demora, safety_factor )
        answers[self.mf['min_stock']] = self.calc_min_stock(ave_daily_demand, lead_time, answers[self.mf['safety_stock']])
        answers[self.mf['max_stock']] = self.calc_max_stock(ave_daily_demand, lead_time, answers[self.mf['safety_stock']])
        # answers[self.mf['reorder_point']] = self.calc_reorder_point(ave_daily_demand, lead_time, answers[self.mf['safety_stock']])
        answers[self.mf['reorder_point']] = self.calc_reorder_point(answers[self.mf['min_stock']], answers[self.mf['safety_stock']])
        answers[self.mf['trigger']] = 'auto'
        answers[self.f['status']] = 'active'
        print('answers model_reorder_point', answers)
        return answers

    def upsert_procurment(self, product_by_warehouse, **kwargs):

        for wh, create_records in product_by_warehouse.items():
            print(f'----------------{wh}--------------------')
            existing_records = self.get_procurments(warehouse=wh)
            update_records = []
            # existing_skus = [prod['sku'] for prod in existing_procurments]
            for product in create_records[:]:
                if self.SKU_OBJ_ID in product:
                    product_code = product[self.SKU_OBJ_ID].get(self.f['product_code'])
                    sku = product[self.SKU_OBJ_ID].get(self.f['sku'])
                    for existing_record in existing_records:
                        if existing_record.get('product_code') == product_code and \
                            existing_record.get('sku') == sku:
                            update_records.append(product)
                            try:
                                create_records.remove(product)
                            except ValueError:
                                 print('allready removed')

            print('update_records', update_records)
            print('create_records', create_records)
            response = self.create_procurment(create_records, **kwargs)

        return response


    def upsert_reorder_point(self):
        if self.current_record:
            print('record, product base')
        records = self.get_product_average_demand_by_warehouse()
        product_by_warehouse = {}
        config = self.get_config(*['uom'])
        for rec in records:
            demanda_12_meses = rec.get('demanda_12_meses')
            consumo_promedio_diario = float(rec.get('consumo_promedio_diario'))
            product_code = rec.get('product_code')
            sku = rec.get('sku')
            warehouse = rec.get('warehouse')
            product_by_warehouse[warehouse] = product_by_warehouse.get(warehouse,[])
            location = rec.get('location')
            uom = rec.get('uom', config.get('uom'))
            ans = self.model_reorder_point(
                product_code, 
                sku,
                uom, 
                warehouse,
                location,
                consumo_promedio_diario,
                )

            product_by_warehouse[warehouse].append(ans)

        for wh, create_records in product_by_warehouse.items():
            print(f'----------------{wh}--------------------')
            update_records = []
            existing_products = self.get_reorder_rules(warehouse=wh)
            existing_skus = [prod['sku'] for prod in existing_products]
            #only_pr_skus = [prod['sku'] for prod in existing_products]
            for product in create_records[:]:
                if self.SKU_OBJ_ID in product:
                    product_code = product[self.SKU_OBJ_ID].get(self.f['product_code'])
                    sku = product[self.SKU_OBJ_ID].get(self.f['sku'])
                    for existing_product in existing_products:
                        if existing_product.get('product_code') == product_code and \
                            existing_product.get('sku') == sku:
                            update_records.append(product)
                            try:
                               create_records.remove(product)
                            except ValueError:
                                print('allready removed')

            print('create_records', create_records)
            print('update_records', update_records)
            response = self.create_reorder_rule(create_records)
            print('response', response)
            # repose_edit = self.update_reorder_rule(update_records)

        return True


# all_prod = [{'product_code':'a'},{'product_code':'b'},{'product_code':'a'},{'product_code':'c'},{'product_code':'b'}]
# products = []
# for rec in all_prod:
#     product_code = rec['product_code']
#     if product_code not in products:
#         products.append(product_code)

