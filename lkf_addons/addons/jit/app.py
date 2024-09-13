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

### Objecto de Modulo ###
'''
Cada modulo puede tener N objetos, configurados en clases.
Estos objetos deben de heredar de base.LKF_Base) y cualquier modulo dependiente
Al hacer el super() del __init__(), heredamos las variables de configuracion de clase.
Se pueden heredar funciones de cualquier clase heredada con el metodo super(). 
'''
# class Stock(Employee, Warehouse, Product, base.LKF_Base):

class JIT(base.LKF_Base):


    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False):
        #base.LKF_Base.__init__(self, settings, sys_argv=sys_argv, use_api=use_api)
        self.mf = {}
        self.mf.update({
            'bom_group_qty_in':'66d8e09cb22bcdcc2f341e85',
            'bom_group_qty_out':'66da962859bec54a05c73e00',
            'bom_group_qty_throughput':'66da962859bec54a05c73e01',
            'bom_group_step':'66d8e7b0b22bcdcc2f341e88',
            'input_goods_product_code':'71ef32bcdf0ec2ba73dec33d',
            'input_goods_product_name':'71ef32bcdf0ec2ba73dec33e',
            'input_goods_sku':'75dec64a3199f9a040829243',
            'raw_material_group':'66d8dff5b22bcdcc2f341e83',
            })

        super().__init__(settings, sys_argv=sys_argv, use_api=use_api)

        self.BOM_ID = self.lkm.form_id('bom','id')

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

            })



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
