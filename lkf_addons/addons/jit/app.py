# -*- coding: utf-8 -*-
### Linkaform Modules / Archivo de Modulo ###
'''

Licencia BSD
Copyright (c) 2024 Infosync / LinkaForm.  
Todos los derechos reservados.

Se permite la redistribución y el uso en formas de código fuente y binario, con o sin modificaciones, siempre que se cumplan las siguientes condiciones:

1. Se debe conservar el aviso de copyright anterior, esta lista de condiciones y el siguiente descargo de responsabilidad en las redistribuciones del código fuente.
2. Se debe reproducir el aviso de copyright anterior, esta lista de condiciones y el siguiente descargo de responsabilidad en la documentación y/u otros materiales proporcionados con las distribuciones en formato binario.
3. Ni el nombre del Infosync ni los nombres de sus colaboradores pueden ser utilizados para respaldar o promocionar productos derivados de este software sin permiso específico previo por escrito.

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
import simplejson, math
from copy import deepcopy

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

# class Base(Base):


#     def __init__(self, settings, sys_argv=None, use_api=False, **kwargs):
#         super().__init__(settings, sys_argv=sys_argv, use_api=use_api, f=kwargs)

#         self.config_fields = {
#             'demora':f'{self.f.get("demora")}',
#             'lead_time':f'{self.f.get("lead_time")}',
#             'dias_laborales_consumo':f'{self.f.get("dias_laborales_consumo")}',
#             'factor_crecimiento_jit':f'{self.f.get("factor_crecimiento_jit")}',
#             'factor_seguridad_jit':f'{self.f.get("factor_seguridad_jit")}',
#             'uom':f'{self.UOM_OBJ_ID}.{self.f.get("uom")}',
#             'procurment_location':f'{self.f.get("config_group")}',
#             'warehouse_kind': '66ed0c88c9aefada5b04b818',
#             # 'warehouse': f'{self.WH.f["config_wh_group"]}.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.WH.f["warehouse"]}',
#             # 'location': f'{self.WH.f["config_wh_group"]}.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.WH.f["warehouse_location"]}',
#         }

    # def get_config(self, *args, **kwargs):
    #     print('esta', esta)
    #     print('esta', estad)
    #     if not self.GET_CONFIG:
    #         match_query ={ 
    #              'form_id': self.CONFIGURACIONES,  
    #              'deleted_at' : {'$exists':False},
    #         } 
    #         if kwargs.get('query'):
    #             match_query.update(kwargs['query'])
    #         project_ids = self._project_format(self.config_fields)
    #         aggregate = [
    #             {'$match': match_query},
    #             {'$limit':kwargs.get('limit',1)},
    #             {'$project': project_ids },
    #             ]
    #         self.GET_CONFIG =  self.format_cr(self.cr.aggregate(aggregate) )
    #     result = {}
    #     for res in self.GET_CONFIG:
    #         result = {arg:res[arg] for arg in args if res.get(arg)}
    #     return result if result else None
        


# class JIT(Product, Warehouse, base.LKF_Base):
# from lkf_addons.addons.stock.app import Stock

class JIT(Base):


    def __init__(self, settings, sys_argv=None, use_api=False, **kwargs):

        # base.LKF_Base.__init__(self, settings, sys_argv=sys_argv, use_api=use_api)
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api, **kwargs)
        self.kwargs['MODULES'] = self.kwargs.get('MODULES',[])       
        if self.__class__.__name__ not in kwargs:
            self.kwargs['MODULES'].append(self.__class__.__name__)
        # self.load('Product', **self.kwargs)
        # self.load(module='Product', module_class='Warehouse', import_as='WH', **self.kwargs)
        # if not hasattr(self, 'STOCK'):
        #     print('hasattr', hasattr(self, 'STOCK'))
        #     self.JIT =True
        #     print('dir self', dir(self))
        #    self.STOCK = Stock( settings, sys_argv=sys_argv, use_api=use_api, **kwargs)
        f = {
            'alloctaion_group':'66da3bddb22bcdcc2f341f0b',
            'allocation_source_document':'66da48a1b22bcdcc2f341f2a',
            'allocation_source_document_type':'66da48a1b22bcdcc2f341f2b',
            'allocation_qty':'66da3e14b22bcdcc2f341f11',
            'allocation_proc_method':'673e20c55f1c35d02395a6d2',
            'dias_laborales_consumo':'66ececbcc9aefada5b04b800',
            'borrar_historial':'671fbd248e46aab662455b40',
            'bom_qty_min':'66d9c26cb22bcdcc2f341eef',
            'bom_qty_max':'66d9c26cb22bcdcc2f341ef0',
            'bom_qty_setp':'66d9c26cb22bcdcc2f341ef1',
            'bom_qty':'66d8dfd7b22bcdcc2f341e82',
            'bom_qty_out':'66d8dfd7b22bcdcc2f341e83',
            'bom_group_qty_in':'66d8e09cb22bcdcc2f341e85',
            'bom_group_qty_out':'66da962859bec54a05c73e00',
            'bom_group_qty_throughput':'66da962859bec54a05c73e01',
            'bom_group_step':'66d8e7b0b22bcdcc2f341e88',
            'bom_name':'66d8e063b22bcdcc2f341e84',
            'bom_type':'66d8dfbcb22bcdcc2f341e81',
            'bom_template_step':'66d8f293b22bcdcc2f341ea6',
            'bom_status':'66e275891f6f133e363afb3f',
            'bom_step':'66da9a3b59bec54a05c73e0a',
            'comments':'673261f0f652eb86b4204906',
            'consumo_promedio_diario':'66ec770cc9aefada5b04b7a6',
            'demanda_12_meses':'66ea6c61c9aefada5b04b76e',
            'demora':'66ea62dac9aefada5b04b737',
            'demand_date': '66d92fe6b22bcdcc2f341ed8',
            'demand_hour': '66d92fe6b22bcdcc2f341ed9',
            'factor_crecimiento_jit':'66ececbcc9aefada5b04b801',
            'factor_seguridad_jit':'66ececbcc9aefada5b04b802',
            'allocation_status':'673e20f75f1c35d02395a6d3',
            'fecha_demanda':'66ea6c28c9aefada5b04b76c',
            'input_goods_product_code':'71ef32bcdf0ec2ba73dec33d',
            'input_goods_product_name':'71ef32bcdf0ec2ba73dec33e',
            'input_goods_sku':'75dec64a3199f9a040829243',
            'lead_time':'66d8ee99b22bcdcc2f341e8a',
            'manufacture_lead_time':'66d8eed3b22bcdcc2f341e8b',
            'month': '6206b9ae8209a9677f9b8bd9',
            'min_stock':'66ea62dac9aefada5b04b739',
            'max_stock':'66ea62dac9aefada5b04b73a',
            'qty': '6206b9ae8209a9677f9b8bdb',
            'qty_allocated': '66da3bddb22bcdcc2f341f09',
            'qty_available': '66da3bddb22bcdcc2f341f0a',
            'procurment_date':'66da0c19b22bcdcc2f341f06',
            'procurment_method':'66d92acdb22bcdcc2f341ebf',
            'procurment_schedule_date':'66da538cb22bcdcc2f341f47',
            'procurment_status':'621cdeeec9c81e23bb6380fc',
            'jit_procurment_status':'66da0c19b22bcdcc2f341f07',
            'procurment_qty':'66da3bddb22bcdcc2f341f08',
            'qty': '6206b9ae8209a9677f9b8bdb',
            'status':'620ad6247a217dbcb888d175',
            'step_disposal':'66d8f324b22bcdcc2f341eaa',
            'step_harvest':'66d8f324b22bcdcc2f341ea9',
            'step_multiplication':'66d8f2f2b22bcdcc2f341ea7',
            'step_weeks':'66d8f2f2b22bcdcc2f341ea8',
            'safety_stock':'66ea62dac9aefada5b04b738',
            'standar_pack':'671b22d738a541183685d077',
            'tipo_almacen': '66ed0c88c9aefada5b04b818',
            'raw_material_group':'66d8dff5b22bcdcc2f341e83',
            'reorder_point':'66ea62dac9aefada5b04b73b',
            'rutas_group':'671b2266ecd538747985d0ac',
            'trigger':'66eb14ffc9aefada5b04b793',
            'year': '6206b9ae8209a9677f9b8bda',
            'family': '61ef32bcdf0ec2ba73dec343'
            }

        self.config_fields = {
            'demora':f'{self.f.get("demora")}',
            'lead_time':f'{self.f.get("lead_time")}',
            'dias_laborales_consumo':f'{self.f.get("dias_laborales_consumo")}',
            'factor_crecimiento_jit':f'{self.f.get("factor_crecimiento_jit")}',
            'factor_seguridad_jit':f'{self.f.get("factor_seguridad_jit")}',
            'uom':f'{self.UOM_OBJ_ID}.{self.f.get("uom")}',
            'procurment_location':f'{self.f.get("config_group")}',
            'warehouse_kind': '66ed0c88c9aefada5b04b818',
            # 'warehouse': f'{self.WH.f["config_wh_group"]}.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.WH.f["warehouse"]}',
            # 'location': f'{self.WH.f["config_wh_group"]}.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.WH.f["warehouse_location"]}',
        }

        if hasattr(self, 'f'):
            self.f.update(f)
        else:
            print('vaa  A IGUALSAR')
            self.f = f

        mf = deepcopy(f) #Backguard compability

        if hasattr(self, 'mf'):
            self.mf.update(mf)
        else:
            self.mf = mf
        
        self.config_fields = {
            'demora':f'{self.f.get("demora")}',
            'lead_time':f'{self.f.get("lead_time")}',
            'dias_laborales_consumo':f'{self.f.get("dias_laborales_consumo")}',
            'factor_crecimiento_jit':f'{self.f.get("factor_crecimiento_jit")}',
            'factor_seguridad_jit':f'{self.f.get("factor_seguridad_jit")}',
            'uom':f'{self.UOM_OBJ_ID}.{self.f.get("uom")}',
            'procurment_location':f'{self.f.get("config_group")}',
            'warehouse_kind': '66ed0c88c9aefada5b04b818',
            # 'warehouse': f'{self.WH.f["config_wh_group"]}.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.WH.f["warehouse"]}',
            # 'location': f'{self.WH.f["config_wh_group"]}.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.WH.f["warehouse_location"]}',
        }

        # kwargs = kwargs.get('f',f)

        from lkf_addons.addons.product.app import Product, Warehouse
        #super().__init__(settings, sys_argv=sys_argv, use_api=use_api, **kwargs)
        # from lkf_addons.addons.stock.app import Stock
        # self.STOCK = Stock( settings, sys_argv=sys_argv, use_api=use_api, **kwargs)

        self.BASE = Base( settings, sys_argv=sys_argv, use_api=use_api, **kwargs)
        self.WH = Warehouse( settings, sys_argv=sys_argv, use_api=use_api, **kwargs)
        #super().__init__(settings, sys_argv=sys_argv, use_api=use_api, **kwargs)
        #Formas
        self.BOM_ID = self.lkm.form_id('bom','id')
        self.BOM_TEMPLATE_ID = self.lkm.form_id('production_bom_template','id')
        self.DEMANDA_UTIMOS_12_MES = self.lkm.form_id('demanda_ultimos_12_meses','id')
        self.DEMANDA_PLAN = self.lkm.form_id('demand_plan','id')
        self.PROCURMENT = self.lkm.form_id('procurment_record','id')
        self.REGLAS_REORDEN = self.lkm.form_id('reglas_de_reorden','id')
        self.RUTAS_TRANSPASO = self.lkm.form_id('rutas_de_transpaso','id')
        self.CONFIGURACIONES_JIT = self.lkm.form_id('configuraciones_jit','id')

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


    # def get_config(self, *args, **kwargs):
    #     print('self config', self.GET_CONFIG)
    #     print('self config_fields', self.config_fields)
    #     if not self.GET_CONFIG:
    #         match_query ={ 
    #              'form_id': self.BASE.CONFIGURACIONES,  
    #              'deleted_at' : {'$exists':False},
    #         } 
    #         if kwargs.get('query'):
    #             match_query.update(kwargs['query'])
    #         print('self match_query', match_query)
    #         print('self elf.config_fields', self.config_fields)
    #         project_ids = self.project_format(self.config_fields)
    #         aggregate = [
    #             {'$match': match_query},
    #             {'$limit':kwargs.get('limit',1)},
    #             {'$project': project_ids },
    #             ]
    #         print('self aggregate', aggregate)
    #         print('self elf.config_fields', self.configd_fields)
    #         self.GET_CONFIG =  self.format_cr(self.cr.aggregate(aggregate) )
    #     result = {}
    #     for res in self.GET_CONFIG:
    #         result = {arg:res[arg] for arg in args if res.get(arg)}
    #     return result if result else None

    def ave_daily_demand(self):
        print('average daly cons', self.form_id)
        print('average daly mf=', self.mf)
        if self.form_id == self.DEMANDA_UTIMOS_12_MES:
            print('va por ultimos 12 meses>>>>>>')
            conf_data = self.get_config()
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
        self.load('Stock', **self.kwargs)
        product_rules = self.get_reorder_rules(
            warehouse=warehouse, 
            location=location, 
            product_code=product_code, 
            sku=sku, 
            status=status)

        res = []
        product_by_warehouse = {}
        product_codes = [r['product_code'] for r in  product_rules if r.get('product_code')]
        self.ROUTE_RULES = {x['product_code']:x for x in self.get_rutas_transpaso(product_codes) if x.get('product_code')}
        for rule in product_rules:
            product_code = rule.get('product_code')
            sku = rule.get('sku')
            warehouse = rule.get('warehouse')
            product_by_warehouse[warehouse] = product_by_warehouse.get(warehouse,[])
            location = rule.get('warehouse_location')
            product_stock = self.Stock.get_product_stock(product_code, sku=sku,  warehouse=warehouse, location=location)
            #product_stock = {'actuals':0}
            order_qty = self.exec_reorder_rules(rule, product_stock)
            if order_qty:
                ans = self.model_procurment(order_qty, product_code, sku, warehouse, location, procurment_method='buy')
                product_by_warehouse[warehouse].append(ans)
        response = self.upsert_procurment(product_by_warehouse)
        return response

    def calc_safety_stock(self, ave_daily_demand, lead_time, demora, safty_factor=1):
        #return round(ave_daily_demand * lead_time * safty_factor,2)
        return round(ave_daily_demand * demora * safty_factor,2)

    def calc_max_stock(self, ave_daily_demand, lead_time, safety_stock):
        return self.calc_min_stock(ave_daily_demand, lead_time, safety_stock) * 2

    def calc_min_stock(self, ave_daily_demand, lead_time, safety_stock):
        #return round((ave_daily_demand * lead_time) + safety_stock,2)
        return round((ave_daily_demand * lead_time) ,2)

    def calc_shipment_pack(self, requested_units, pack_size=1):
        # Calculate the number of full packs needed
        full_packs = math.ceil(requested_units / pack_size)
        # Return the total units to ship (full packs * pack size)
        return full_packs * pack_size

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
        return response

    def create_reorder_rule(self, answers, **kwargs):
        metadata = self.lkf_api.get_metadata(self.REGLAS_REORDEN)
        properties = {
                "device_properties":{
                    "system": "Script",
                    "process": "Create Reorder Rule", 
                    "accion": 'create_reorder_rule', 
                    "archive": "jit/app.py",
                    "script":"upsert_reorder_point.py"
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

    def get_bom(self, product_code, product_sku, qty=1, warehouse=None, location=None, bom_type='manufacture'):
        match_query ={ 
             'form_id': self.BOM_ID,  
             'deleted_at' : {'$exists':False},
             f'answers.{self.Product.SKU_OBJ_ID}.{self.Product.f["product_code"]}': product_code,
             f'answers.{self.Product.SKU_OBJ_ID}.{self.Product.f["product_sku"]}': product_sku,
             f'answers.{self.mf["bom_type"]}': bom_type,
             f'answers.{self.mf["bom_status"]}': 'active',
         } 
        query = [
            {'$match': match_query},
            {'$sort': {'created_at': 1}},
            {'$limit':1},
            {'$unwind':f'$answers.{self.mf["raw_material_group"]}'},
            {'$project':{
                    '_id':0,
                    'bom_name':f'$answers.{self.mf["bom_name"]}',
                    'bom_type':f'$answers.{self.mf["bom_type"]}',
                    'product_code':f'$answers.{self.Product.SKU_OBJ_ID}.{self.Product.f["product_code"]}',
                    'product_name':f'$answers.{self.Product.SKU_OBJ_ID}.{self.Product.f["product_sku"]}',
                    'sku':f'$answers.{self.Product.SKU_OBJ_ID}.{self.Product.f["product_name"]}',
                    'qty':f'$answers.{self.f["bom_qty"]}',
                    'qty_out':f'$answers.{self.f["bom_qty_out"]}',
                    'step':f'$answers.{self.f["bom_qty_setp"]}',
                    'lead_time':f'$answers.{self.f["lead_time"]}',
                    'manufacture_lead_time':f'$answers.{self.f["manufacture_lead_time"]}',
            }},
            ]
        cr_res =  self.format_cr(self.cr.aggregate(query))
        return cr_res
  
    def get_bom_template(self, product_code, product_sku, qty=1, warehouse=None, location=None):
        match_query ={ 
          'form_id': self.BOM_TEMPLATE_ID,  
          'deleted_at' : {'$exists':False},
          f'answers.{self.Product.SKU_OBJ_ID}.{self.Product.f["product_code"]}': product_code,
          f'answers.{self.mf["bom_status"]}': 'active',
        } 
        query = [
         {'$match': match_query},
         {'$sort': {'created_at': 1}},
         {'$limit':1},
         {'$unwind':f'$answers.{self.mf["bom_template_step"]}'},
         {'$project':{
                 '_id':0,
                 'bom_name':f'$answers.{self.mf["bom_name"]}',
                 'bom_type':f'$answers.{self.mf["bom_type"]}',
                 'product_code':f'$answers.{self.Product.SKU_OBJ_ID}.{self.Product.f["product_code"]}',
                 'product_name':f'$answers.{self.Product.SKU_OBJ_ID}.{self.Product.f["product_sku"]}',
                 'sku':f'$answers.{self.Product.SKU_OBJ_ID}.{self.Product.f["product_name"]}',
                 'starting_qty':f'$answers.{self.f["bom_qty"]}',
                 'starting_qty_out':f'$answers.{self.f["bom_qty_out"]}',
                 'starting_qty_max':f'$answers.{self.f["bom_qty_max"]}',
                 'starting_qty_min':f'$answers.{self.f["bom_qty_min"]}',
                 'step':f'$answers.{self.mf["bom_template_step"]}.{self.f["bom_qty_setp"]}',
                 'step2':2,
                 'step_lead_time_weeks':f'$answers.{self.mf["bom_template_step"]}.{self.f["step_weeks"]}',
                 'step_harvest':f'$answers.{self.mf["bom_template_step"]}.{self.f["step_harvest"]}',
                 'step_disposal':f'$answers.{self.mf["bom_template_step"]}.{self.f["step_disposal"]}',
                 'step_multiplication':f'$answers.{self.mf["bom_template_step"]}.{self.f["step_multiplication"]}',
                 'step_qty':f'$answers.{self.mf["bom_template_step"]}.{self.f["bom_qty_setp"]}',
                 'lead_time':f'$answers.{self.f["lead_time"]}',
                 'manufacture_lead_time':f'$answers.{self.f["manufacture_lead_time"]}',
         }},
         ]
        cr_res =  self.format_cr(self.cr.aggregate(query))
        return cr_res  

    def get_bom_products(self, bom_line, warehouse=None, location=None, bom_type='manufacture'):
        product_code = bom_line.get('product_code')
        sku = bom_line.get('sku')
        qty = bom_line.get('move_group_qty')
        bom_res = self.get_product_boms(product_code, sku, qty, warehouse=warehouse, location=location)
        if bom_res:
            return bom_res
        else:
            return [bom_line,]

    def get_product_boms(self, product_code, product_sku, qty=1, warehouse=None, location=None, bom_type='manufacture'):

        match_query ={ 
             'form_id': self.BOM_ID,  
             'deleted_at' : {'$exists':False},
             f'answers.{self.Product.SKU_OBJ_ID}.{self.Product.f["product_code"]}': product_code,
             f'answers.{self.Product.SKU_OBJ_ID}.{self.Product.f["product_sku"]}': product_sku,
             f'answers.{self.mf["bom_type"]}': bom_type,
             f'answers.{self.mf["bom_status"]}': 'active',
         } 
        query = [
            {'$match': match_query},
            {'$sort': {'created_at': 1}},
            {'$limit':1},
            {'$unwind':f'$answers.{self.mf["raw_material_group"]}'},
            {'$project':{
                    '_id':0,
                    'bom_name':f'$answers.{self.mf["bom_name"]}',
                    'bom_type':f'$answers.{self.mf["bom_type"]}',
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
    
    def get_procurments(self, warehouse=None, location=None, product_code=None, sku=None, status='programmed', group_by=False, \
        procurment_method=None):
        match_query = {
            'form_id': self.PROCURMENT,
            'deleted_at': {'$exists': False},
            
        }
        if status and status != 'programmed':
            match_query.update({f'answers.{self.mf["jit_procurment_status"]}': 'programmed'})
        else:
            match_query.update({
                '$or': [
                        {f'answers.{self.mf["jit_procurment_status"]}': 'programmed'},  # Matches "programmed"
                        {f'answers.{self.mf["jit_procurment_status"]}': {'$exists': False}}  # Matches missing key
                    ]
                })
        if type(product_code) == list:
            match_query.update({
                 f"answers.{self.Product.SKU_OBJ_ID}.{self.f['product_code']}": {"$in": product_code}
                })
        elif product_code:
            match_query.update({
                f"answers.{self.Product.SKU_OBJ_ID}.{self.f['product_code']}": product_code
                 })
        if sku:
            match_query.update({
                f"answers.{self.Product.SKU_OBJ_ID}.{self.f['sku']}":sku
                })
        if warehouse:
            match_query.update({
                f"answers.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.WH.f['warehouse']}":warehouse
                })
        if location:
            match_query.update({
                f"answers.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.WH.f['warehouse_location']}":location
                })
        if procurment_method:
            match_query.update({
                f"answers.{self.mf['procurment_method']}": procurment_method
                })
        query = [
            {'$match': match_query},
            {'$project':{
                    '_id':1,
                    'bom_name':f'$answers.{self.BOM_CAT_OBJ_ID}.{self.mf["bom_name"]}',
                    'date':f'$answers.{self.mf["procurment_date"]}',
                    'date_schedule':f'$answers.{self.mf["procurment_schedule_date"]}',
                    'procurment_method':f'$answers.{self.mf["procurment_method"]}',
                    'procurment_qty':f'$answers.{self.mf["procurment_qty"]}',
                    'product_code':f'$answers.{self.Product.SKU_OBJ_ID}.{self.f["product_code"]}',
                    'sku':f'$answers.{self.Product.SKU_OBJ_ID}.{self.f["sku"]}',
                    'status':f'$answers.{self.mf["status"]}',
                    'uom':f'$answers.{self.UOM_OBJ_ID}.{self.f["uom"]}',
                    'warehouse':f'$answers.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.WH.f["warehouse"]}',
                    'warehouse_location':f'$answers.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.WH.f["warehouse_location"]}',
            }},

            ]

        return self.format_cr(self.cr.aggregate(query))

    def get_reorder_rules(self, warehouse=None, location=None, product_code=None, sku=None, status='active', group_by=False, method=None):
        match_query ={ 
             'form_id': self.REGLAS_REORDEN,  
             'deleted_at' : {'$exists':False},
             f'answers.{self.mf["status"]}': status,
         }
        if product_code:
            match_query.update({
                f"answers.{self.Product.SKU_OBJ_ID}.{self.f['product_code']}":product_code
                })
        if sku:
            match_query.update({
                f"answers.{self.Product.SKU_OBJ_ID}.{self.f['sku']}":sku
                })
        if warehouse:
            match_query.update({
                f"answers.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.WH.f['warehouse']}":warehouse
                })
        if location:
            match_query.update({
                f"answers.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.WH.f['warehouse_location']}":location
                })
        if method:
            match_query.update({
                f"answers.{self.f['procurment_method']}": method
                })
        query = [
            {'$match': match_query},
            {'$project':{
                    '_id':0,
                    'bom_name':f'$answers.{self.BOM_CAT_OBJ_ID}.{self.mf["bom_name"]}',
                    'demora':f'$answers.{self.mf["demora"]}',
                    'product_code':f'$answers.{self.Product.SKU_OBJ_ID}.{self.f["product_code"]}',
                    'procurment_method':f'$answers.{self.f["procurment_method"]}',
                    'lead_time':f'$answers.{self.mf["lead_time"]}',
                    'min_stock':f'$answers.{self.mf["min_stock"]}',
                    'max_stock':f'$answers.{self.mf["max_stock"]}',
                    'reorder_point':f'$answers.{self.mf["reorder_point"]}',
                    'safety_stock':f'$answers.{self.mf["safety_stock"]}',
                    'sku':f'$answers.{self.Product.SKU_OBJ_ID}.{self.f["sku"]}',
                    'status':f'$answers.{self.mf["status"]}',
                    'trigger':f'$answers.{self.mf["trigger"]}',
                    'uom':f'$answers.{self.UOM_OBJ_ID}.{self.f["uom"]}',
                    'warehouse':f'$answers.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.WH.f["warehouse"]}',
                    'warehouse_location':f'$answers.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.WH.f["warehouse_location"]}',
            }},
            ]
        # print('query=', simplejson.dumps(query, indent=4))
        return self.format_cr(self.cr.aggregate(query))

    def get_rutas_transpaso(self, product_codes=None):
        match_query ={ 
             'form_id': self.RUTAS_TRANSPASO,  
             #'form_id': 125127,  
             'deleted_at' : {'$exists':False},
         } 

        if type(product_codes) == list:
            match_query.update({
                 f"answers.{self.Product.SKU_OBJ_ID}.{self.f['product_code']}": {"$in": product_codes}
                })
        elif product_codes:
            match_query.update({
                f"answers.{self.Product.SKU_OBJ_ID}.{self.f['product_code']}": product_codes
                 }) 
        query = [
            {'$match': match_query},
            {'$sort': {'created_at': 1}},
            # {'$limit':1},
            {'$unwind':f'$answers.{self.mf["rutas_group"]}'},
            {'$project':{
                    '_id':0,
                    'product_code':f'$answers.{self.Product.SKU_OBJ_ID}.{self.f["product_code"]}',
                    'sku':f'$answers.{self.Product.SKU_OBJ_ID}.{self.f["sku"]}',
                    'standar_pack':f'$answers.{self.mf["rutas_group"]}.{self.mf["standar_pack"]}',
                    'unit_of_measure':f'$answers.{self.mf["rutas_group"]}.{self.UOM_OBJ_ID}.{self.f["uom"]}',
                    'warehouse':f'$answers.{self.mf["rutas_group"]}.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.f["warehouse"]}',
                    'warehouse_location':f'$answers.{self.mf["rutas_group"]}.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.f["warehouse_location"]}',
                    'warehouse_dest':f'$answers.{self.mf["rutas_group"]}.{self.WH.WAREHOUSE_LOCATION_DEST_OBJ_ID}.{self.f["warehouse_dest"]}',
                    'warehouse_location_dest':f'$answers.{self.mf["rutas_group"]}.{self.WH.WAREHOUSE_LOCATION_DEST_OBJ_ID}.{self.f["warehouse_location_dest"]}',
            }},
            ]
        # print('rrrquery', simplejson.dumps(query,indent=4))
        res =  self.format_cr(self.cr.aggregate(query))
        return res
    
    def set_rutas_transpaso(self, product_code=None, update=False):
        if hasattr(self , 'ROUTE_RULES') and not update:
            return True
        data = self.get_rutas_transpaso(product_codes=product_code)
        self.ROUTE_RULES = {}
        for entry in data:
            product_code = entry['product_code']
            sku = entry['sku']
            warehouse = entry['warehouse']
            warehouse_location = entry['warehouse_location']
            warehouse_dest = entry['warehouse_dest']
            warehouse_location_dest = entry['warehouse_location_dest']
            standar_pack = entry['standar_pack']

            if product_code not in self.ROUTE_RULES:
                self.ROUTE_RULES[product_code] = {}

            if sku not in self.ROUTE_RULES[product_code]:
                self.ROUTE_RULES[product_code][sku] = {}

            if warehouse not in self.ROUTE_RULES[product_code][sku]:
                self.ROUTE_RULES[product_code][sku][warehouse] = {}

            if warehouse_location not in self.ROUTE_RULES[product_code][sku][warehouse]:
                self.ROUTE_RULES[product_code][sku][warehouse][warehouse_location] = {}

            if warehouse_dest not in self.ROUTE_RULES[product_code][sku][warehouse][warehouse_location]:
                self.ROUTE_RULES[product_code][sku][warehouse][warehouse_location][warehouse_dest] = {}

            if warehouse_location_dest not in self.ROUTE_RULES[product_code][sku][warehouse][warehouse_location][warehouse_dest]:
                self.ROUTE_RULES[product_code][sku][warehouse][warehouse_location][warehouse_dest][warehouse_location_dest] = {}

            self.ROUTE_RULES[product_code][sku][warehouse][warehouse_location][warehouse_dest][warehouse_location_dest] = {'standar_pack':standar_pack}
        return True

    def get_product_average_demand(self, procurement_method):
        #TODO obtener de registros de formularios o de salidas de almacen
        match_query ={ 
             'form_id': self.DEMANDA_UTIMOS_12_MES,  
             'deleted_at' : {'$exists':False},
             f'answers.{self.f["procurment_method"]}': procurement_method,
         } 
        query = [
            {'$match': match_query},
            {'$project':{
                    '_id':1,
                    'folio':'$folio',
                    'sku':f'$answers.{self.Product.SKU_OBJ_ID}.{self.f["product_sku"]}',
                    'product_code':f'$answers.{self.Product.SKU_OBJ_ID}.{self.f["product_code"]}',
                    'warehouse':f'$answers.{self.WH.WAREHOUSE_OBJ_ID}.{self.WH.f["warehouse"]}',
                    'demanda_12_meses':f'$answers.{self.f["demanda_12_meses"]}',
                    'consumo_promedio_diario': {
                        '$toDouble': f'$answers.{self.f["consumo_promedio_diario"]}'
                    },
                    'fecha':f'$answers.{self.f["fecha_demanda"]}',
                }
            },
            {'$sort':{'fecha':-1}},
            {'$group':{
                '_id':{
                    'product_code':'$product_code',
                    'sku':'$sku',
                },
                'demanda_12_meses': {'$sum': '$demanda_12_meses' },
                'consumo_promedio_diario':{'$sum':'$consumo_promedio_diario'},
            }}
            ]
        return query

    def get_product_average_demand_by_product(self, procurement_method):
        #TODO obtener de registros de formularios o de salidas de almacen
        query = self.get_product_average_demand(procurement_method)
        return self.format_cr(self.cr.aggregate(query))

    def get_product_average_demand_by_warehouse(self, procurement_method):
        #TODO obtener de registros de formularios o de salidas de almacen
        query = self.get_product_average_demand(procurement_method)
        query.pop(3)
        query.append({
            '$group':{
                '_id':{
                    'product_code':'$product_code',
                    'sku':'$sku',
                    'warehouse':'$warehouse',
                },
                'folio':{'$first':'$folio'},
                'demanda_12_meses': {'$first': '$demanda_12_meses' },
                'consumo_promedio_diario':{'$first':'$consumo_promedio_diario'},
            }}
            )
        return self.format_cr(self.cr.aggregate(query))

    def get_warehouse_config(self, key, value, get_key):
        config = self.get_config(*['procurment_location'])
        locations_config = config.get('procurment_location',[])
        res = None
        for wh in locations_config:
            wh['location'] = wh.get(self.f['warehouse_location'])
            wh['warehouse'] = wh.get(self.f['warehouse'])
            if wh.get(key) and wh[key] == value:
                res = wh.get(get_key)
        print('esto sigue siendo valido o hay que actualizar')
        return res

    def model_procurment(self, qty, product_code, sku, warehouse, location, uom=None, schedule_date=None, \
        bom=None, status='programmed', procurment_method='buy'):
        answers = {}
        config = self.get_config(*['uom'])

        if not schedule_date:
            schedule_date = self.today_str()
        if not location:
            location = self.get_warehouse_config('tipo_almacen', 'abastacimiento', 'warehouse_location')
        if not uom:
            uom = config.get('uom')
        standar_pack = self.ROUTE_RULES.get(str(product_code),{}).get('standar_pack',1)
        answers[self.Product.SKU_OBJ_ID] = {}
        answers[self.Product.SKU_OBJ_ID][self.f['product_code']] = product_code
        answers[self.Product.SKU_OBJ_ID][self.f['sku']] = sku
        answers[self.Product.SKU_OBJ_ID][self.f['familia']] = self.all_prod[sku]['familia']
        answers[self.Product.SKU_OBJ_ID][self.f['lninea']] = self.all_prod[sku]['lninea']
        answers[self.UOM_OBJ_ID] = {}
        answers[self.UOM_OBJ_ID][self.f['uom']] = uom
        answers[self.WH.WAREHOUSE_LOCATION_OBJ_ID] = {}
        answers[self.WH.WAREHOUSE_LOCATION_OBJ_ID][self.WH.f['warehouse']] = warehouse
        answers[self.WH.WAREHOUSE_LOCATION_OBJ_ID][self.WH.f['warehouse_location']] = location
        answers[self.mf['procurment_date']] = self.today_str()
        answers[self.mf['procurment_method']] = procurment_method
        answers[self.mf['procurment_qty']] = self.calc_shipment_pack(qty, standar_pack)
        answers[self.mf['procurment_status']] = status
        answers[self.mf['procurment_schedule_date']] = schedule_date

        return answers

    def model_reorder_point(self, product_code, sku, uom, warehouse, location, ave_daily_demand, method ):
        answers = {}
        config = self.get_config( *['lead_time', 'demora', 'factor_seguridad_jit','factor_crecimiento_jit','uom'])
        lead_time = config.get('lead_time')
        demora = config.get('demora')
        safety_factor = config.get('factor_seguridad_jit',1)
        factor_crecimiento_jit = config.get('factor_crecimiento_jit',1)
        answers[self.Product.SKU_OBJ_ID] = {}
        answers[self.Product.SKU_OBJ_ID][self.f['product_code']] = product_code
        answers[self.Product.SKU_OBJ_ID][self.f['sku']] = sku
        if not uom:
            uom = config.get('uom')
        answers[self.UOM_OBJ_ID] = {}
        answers[self.UOM_OBJ_ID][self.f['uom']] = uom
        answers[self.WH.WAREHOUSE_LOCATION_OBJ_ID] = {}
        answers[self.WH.WAREHOUSE_LOCATION_OBJ_ID][self.WH.f['warehouse']] = warehouse
        answers[self.WH.WAREHOUSE_LOCATION_OBJ_ID][self.WH.f['warehouse_location']] = location
        answers[self.f['procurment_method']] = method
        answers[self.config_fields['lead_time']] = lead_time
        answers[self.config_fields['demora']] = demora
        answers[self.mf['safety_stock']] = self.calc_safety_stock(ave_daily_demand, lead_time, demora, safety_factor )
        answers[self.mf['min_stock']] = self.calc_min_stock(ave_daily_demand, lead_time, answers[self.mf['safety_stock']])
        answers[self.mf['max_stock']] = self.calc_max_stock(ave_daily_demand, lead_time, answers[self.mf['safety_stock']])
        # answers[self.mf['reorder_point']] = self.calc_reorder_point(ave_daily_demand, lead_time, answers[self.mf['safety_stock']])
        answers[self.mf['reorder_point']] = self.calc_reorder_point(answers[self.mf['min_stock']], answers[self.mf['safety_stock']])
        answers[self.mf['trigger']] = 'auto'
        answers[self.mf['status']] = 'active'
        return answers

    def update_procurmet(self, records, **kwargs):
        return []

    def upsert_procurment(self, product_by_warehouse, **kwargs):

        response = {}
        for wh, create_records in product_by_warehouse.items():
            print(f'----------------{wh}--------------------')
            existing_records = self.get_procurments(warehouse=wh)
            update_records = []
            # existing_skus = [prod['sku'] for prod in existing_procurments]
            for product in create_records[:]:
                if self.Product.SKU_OBJ_ID in product:
                    product_code = product[self.Product.SKU_OBJ_ID].get(self.f['product_code'])
                    sku = product[self.Product.SKU_OBJ_ID].get(self.f['sku'])
                    for existing_record in existing_records:
                        if existing_record.get('product_code') == product_code and \
                            existing_record.get('sku') == sku:
                            update_records.append(product)
                            try:
                                create_records.remove(product)
                            except ValueError:
                                pass

            response = self.update_procurmet(update_records, **kwargs)
            response += self.create_procurment(create_records, **kwargs)

        return response

    def upsert_reorder_point(self):
        if self.current_record:
            print('record, product base')
        records = self.get_product_average_demand_by_warehouse(procurement_method='transfer')
        print(len(records), 'records found')
        product_by_warehouse = {}
        config = self.get_config(*['uom'])
        for rec in records:
            product_code = rec.get('product_code')
            demanda_12_meses = rec.get('demanda_12_meses',0)
            sku = rec.get('sku')
            if demanda_12_meses == 0 or not sku or not product_code:
                continue
            
            consumo_promedio_diario = float(rec.get('consumo_promedio_diario',0))
            warehouse = rec.get('warehouse')
            product_by_warehouse[warehouse] = product_by_warehouse.get(warehouse,[])
            location = rec.get('location')
            if not location:
                wh_config = self.WH.get_warehouse_config(warehouse, location_type='abastacimiento')
                location = wh_config.get('warehouse_location')
                if not location:
                    self.LKFException({"status_code":400, "msg":f"Se debe de configura una ubicacion de Abastecimiento para el almacen {warehouse}."})
            uom = rec.get('uom', config.get('uom'))
            ans = self.model_reorder_point(
                product_code, 
                sku,
                uom, 
                warehouse,
                location,
                consumo_promedio_diario,
                method='transfer'
                )
            product_by_warehouse[warehouse].append(ans)

        for wh, create_records in product_by_warehouse.items():
            update_records = []
            existing_products = self.get_reorder_rules(warehouse=wh)
            existing_skus = [prod['sku'] for prod in existing_products]
            #only_pr_skus = [prod['sku'] for prod in existing_products]
            for product in create_records[:]:
                if self.Product.SKU_OBJ_ID in product:
                    product_code = product[self.Product.SKU_OBJ_ID].get(self.f['product_code'])
                    sku = product[self.Product.SKU_OBJ_ID].get(self.f['sku'])
                    for existing_product in existing_products:
                        if existing_product.get('product_code') == product_code and \
                            existing_product.get('sku') == sku and \
                            existing_product.get('procurment_method') == 'transfer':
                            update_records.append(product)
                            try:
                               create_records.remove(product)
                            except ValueError:
                                pass

            response = self.create_reorder_rule(create_records)
            # repose_edit = self.update_reorder_rule(update_records)

        return True


# all_prod = [{'product_code':'a'},{'product_code':'b'},{'product_code':'a'},{'product_code':'c'},{'product_code':'b'}]
# products = []
# for rec in all_prod:
#     product_code = rec['product_code']
#     if product_code not in products:
#         products.append(product_code)
