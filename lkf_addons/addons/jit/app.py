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
from lkf_addons.addons.stock.app import Stock
from lkf_addons.addons.base.app import Base


### Objecto de Modulo ###
'''
Cada modulo puede tener N objetos, configurados en clases.
Estos objetos deben de heredar de base.LKF_Base) y cualquier modulo dependiente
Al hacer el super() del __init__(), heredamos las variables de configuracion de clase.
Se pueden heredar funciones de cualquier clase heredada con el metodo super(). 
'''
# class Stock(Employee, Warehouse, Product, base.LKF_Base):

class JIT(Stock, base.LKF_Base):


    def __init__(self, settings, sys_argv=None, use_api=False):
        #base.LKF_Base.__init__(self, settings, sys_argv=sys_argv, use_api=use_api)
        self.mf = {}
        self.mf.update({
            'bom_group_qty_in':'66d8e09cb22bcdcc2f341e85',
            'bom_group_qty_out':'66da962859bec54a05c73e00',
            'bom_group_qty_throughput':'66da962859bec54a05c73e01',
            'bom_group_step':'66d8e7b0b22bcdcc2f341e88',
            'demora':'66ea62dac9aefada5b04b737',
            'input_goods_product_code':'71ef32bcdf0ec2ba73dec33d',
            'input_goods_product_name':'71ef32bcdf0ec2ba73dec33e',
            'input_goods_sku':'75dec64a3199f9a040829243',
            'raw_material_group':'66d8dff5b22bcdcc2f341e83',
            'lead_time':'66d8ee99b22bcdcc2f341e8a',
            'demora':'66ea62dac9aefada5b04b737',
            'security_stock':'66ea62dac9aefada5b04b738',
            'min_stock':'66ea62dac9aefada5b04b739',
            'max_stock':'66ea62dac9aefada5b04b73a',
            'procurment_date':'66da0c19b22bcdcc2f341f06',
            'procurment_method':'66d92acdb22bcdcc2f341ebf',
            'procurment_schedule_date':'66da538cb22bcdcc2f341f47',
            'procurment_qty':'66da3bddb22bcdcc2f341f08',
            'procurment_status':'66da0c19b22bcdcc2f341f07',
            'trigger':'66eb14ffc9aefada5b04b793',
            'reorder_point':'66ea62dac9aefada5b04b73b',
            })
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api)

        self.BOM_ID = self.lkm.form_id('bom','id')
        self.PROCURMENT = self.lkm.form_id('procurment_record','id')
        self.REGLAS_REORDEN = self.lkm.form_id('reglas_de_reorden','id')

        self.BOM_CAT = self.lkm.catalog_id('bom')
        self.BOM_CAT_ID = self.BOM_CAT.get('id')
        self.BOM_CAT_OBJ_ID = self.BOM_CAT.get('obj_id')

        self.INPUT_GOODS = self.lkm.catalog_id('input_goods_products')
        self.INPUT_GOODS_ID = self.INPUT_GOODS.get('id')
        self.INPUT_GOODS_OBJ_ID = self.INPUT_GOODS.get('obj_id')

        self.INPUT_GOODS_SKU = self.lkm.catalog_id('input_goods_sku')
        self.INPUT_GOODS_SKU_ID = self.INPUT_GOODS_SKU.get('id')
        self.INPUT_GOODS_SKU_OBJ_ID = self.INPUT_GOODS_SKU.get('obj_id')

        self.f.update({
            'bom_name':'66d8e063b22bcdcc2f341e84',
            'bom_type':'66d8dfbcb22bcdcc2f341e81',
            'bom_status':'66e275891f6f133e363afb3f',
            'status':'620ad6247a217dbcb888d175',
            })


    def balance_warehouse(self, warehouse=None, location=None, product_code=None, product_sku=None, status='active'):
        product_rules = self.get_reorder_rules(
            warehouse=warehouse, 
            location=location, 
            product_code=product_code, 
            product_sku=product_sku, 
            status=status)

        res = []
        for rule in product_rules:
            print('rule',rule)
            product_code = rule.get('product_code')
            sku = rule.get('sku')
            warehouse = rule.get('warehouse')
            location = rule.get('warehouse_location')
            product_stock = self.get_product_stock(product_code, sku=sku,  warehouse=warehouse, location=location)
            print('product_stock',product_stock)
            order_qty = self.exec_reorder_rules(rule, product_stock)
            if order_qty:
                self.upsert_procurment(order_qty, product_code, sku, warehouse, location)
        print(stop)
        return True

    def create_procurment(self, qty, product_code, sku, warehouse, location, **kwargs):
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
        answers = self.procurment_model(qty, product_code, sku, warehouse, location, procurment_method='transfer')
        metadata['answers'].update(answers)
        response = self.lkf_api.post_forms_answers(metadata)
        print('respose', response)
        return response


    def exec_reorder_rules(self, rule, product_stock):
        order_qty = 0
        reorder_point = rule.get('reorder_point',0)
        max_stock = rule.get('max_stock',0)
        actuals = product_stock.get('actuals',0)
        if actuals < reorder_point:
            order_qty = max_stock - actuals
        return order_qty
   
    def procurment_model(self, qty, product_code, sku, warehouse, location, schedule_date=None, \
        bom=None, status='programed', procurment_method='buy'):
        print('today', dir(self))
        print('today', )
        if not schedule_date:
            schedule_date = self.today_str()
        answers = {}
        answers[self.SKU_OBJ_ID] = {}
        answers[self.SKU_OBJ_ID][self.f['product_code']] = product_code
        answers[self.SKU_OBJ_ID][self.f['sku']] = sku
        answers[self.WAREHOUSE_LOCATION_OBJ_ID] = {}
        answers[self.WAREHOUSE_LOCATION_OBJ_ID][self.f['warehouse']] = warehouse
        answers[self.WAREHOUSE_LOCATION_OBJ_ID][self.f['warehouse_location']] = location
        answers[self.mf['procurment_date']] = self.today_str()
        answers[self.mf['procurment_method']] = procurment_method
        answers[self.mf['procurment_qty']] = qty
        answers[self.mf['procurment_status']] = status
        answers[self.mf['procurment_schedule_date']] = schedule_date
        print('procumrent model', answers)
        return answers

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
        print('bom_lines', bom_line)
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
        print('res',res)
        return res

    def get_reorder_rules(self, warehouse=None, location=None, product_code=None, product_sku=None, status='active'):
        match_query ={ 
             'form_id': self.REGLAS_REORDEN,  
             'deleted_at' : {'$exists':False},
             f'answers.{self.f["status"]}': status,
         }
        if product_code:
            match_query.update({
                f"answers.{self.SKU_OBJ_ID}.{self.f['product_code']}":product_code
                })
        if product_sku:
            match_query.update({
                f"answers.{self.SKU_OBJ_ID}.{self.f['sku']}":product_sku
                })
        if warehouse:
            match_query.update({
                f"answers.{self.WAREHOUSE_LOCATION_OBJ_ID}.{self.f['warehouse']}":warehouse
                })
        if location:
            match_query.update({
                f"answers.{self.WAREHOUSE_LOCATION_OBJ_ID}.{self.f['warehouse_location']}":location
                })
        query = [
            {'$match': match_query},
            {'$project':{
                    '_id':0,
                    'bom_name':f'$answers.{self.BOM_CAT_OBJ_ID}.{self.f["bom_name"]}',
                    'demora':f'$answers.{self.mf["demora"]}',
                    'product_code':f'$answers.{self.SKU_OBJ_ID}.{self.f["product_code"]}',
                    'lead_time':f'$answers.{self.mf["lead_time"]}',
                    'min_stock':f'$answers.{self.mf["min_stock"]}',
                    'max_stock':f'$answers.{self.mf["max_stock"]}',
                    'reorder_point':f'$answers.{self.mf["reorder_point"]}',
                    'security_stock':f'$answers.{self.mf["security_stock"]}',
                    'sku':f'$answers.{self.SKU_OBJ_ID}.{self.f["sku"]}',
                    'status':f'$answers.{self.f["status"]}',
                    'trigger':f'$answers.{self.mf["trigger"]}',
                    'uom':f'$answers.{self.UOM_OBJ_ID}.{self.f["uom"]}',
                    'warehouse':f'$answers.{self.WAREHOUSE_LOCATION_OBJ_ID}.{self.f["warehouse"]}',
                    'warehouse_location':f'$answers.{self.WAREHOUSE_LOCATION_OBJ_ID}.{self.f["warehouse_location"]}',
            }},

            ]
        return self.format_cr(self.cr.aggregate(query))


    def upsert_procurment(self, qty, product_code, sku, warehouse, location, **kwargs):
        if True:
            self.create_procurment(qty, product_code, sku, warehouse, location, **kwargs)