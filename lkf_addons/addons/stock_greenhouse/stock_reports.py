# -*- coding: utf-8 -*-

from datetime import timedelta, datetime
import math, simplejson, time
from copy import deepcopy

from .stock_utils import Stock

print('Cargando Reports')

from linkaform_api import base


class Reports(base.LKF_Report, Stock):


    def get_report_filters(self, filters=[]):
        print('report filters', filters)
        mango_query = {"selector":
            {"_id":
                {"$gt":None}
            },
            "limit":10000,
            "skip":0
        }
        if 'products' in filters:
            res = self.lkf_api.search_catalog( self.CATALOG_PRODUCT_ID, mango_query)
            self.json['productCode'] = [x.get(self.f['product_code']) for x in res]
        if 'warehouse' in filters:
            res = self.lkf_api.search_catalog( self.CATALOG_WAREHOUSE_ID, mango_query)
            self.json['warehouse'] = [x.get(self.f['warehouse']) for x in res]
        return True

    def get_product_kardex(self):
        data = self.data.get('data')
        product_code = data.get('product_code', [])
        lot_number = data.get('lot_number',[])
        date_options = data.get('date_options', "custom")
        print('date_options', date_options)
        if date_options == "custom":
        print('date_options', date_optionsdop)
            date_from = data.get('date_from')
            date_to = data.get('date_to')
        else:
            
        date_since = None
        if date_from:
            date_since = self.date_operation(date_from, '-', 1, 'day', date_format='%Y-%m-%d')
        warehouse = data.get('warehouse',[])
        if type(warehouse) == str and warehouse != '':
            warehouse = [warehouse,]
        move_type = None
        stock = self.get_product_stock(product_code, lot_number=lot_number, date_from=date_from, date_to=date_to)

        if not warehouse or warehouse == '':
            warehouse = self.get_warehouse('Stock')
        result = []
        for idx, wh in enumerate(warehouse):
            print(f'============ Warehouse: {wh} ==========================')

            if not date_from and not date_since:
                 initial_stock = {'actuals': 0}
            else:
                initial_stock = self.get_product_stock(product_code, lot_number=lot_number, date_from=date_from, date_to=date_since)
            moves = self.detail_stock_moves(wh, product_code=product_code, lot_number=lot_number)
            moves = self.detail_adjustment_moves(wh, product_code=product_code, lot_number=lot_number, **{'result':moves})
            moves = self.detail_production_moves(wh, product_code=product_code, lot_number=lot_number, **{'result':moves})
            moves = self.detail_scrap_moves(wh, product_code=product_code, lot_number=lot_number, **{'result':moves})
            warehouse_data = { "id":idx, "warehouse":wh, "qty_out_table":"Initial Balance", 
                "balance_table":initial_stock.get('actuals'),
                "serviceHistory": self.set_kardex_order(initial_stock.get('actuals'), moves)
                }
            result.append(warehouse_data)
            #scrap = self.detail_stock_move(wh)
            #todo_gradinscraping
            # print('moves=', moves)
        return result

    def print_moves(self, moves):
        for e, x in moves.items():
            print('x=',x)

    def set_kardex_order(self, initial_stock, moves):
        epochs = list(moves.keys())
        epochs.sort()
        balance = initial_stock
        res = []
        for e in epochs:
            lines = moves[e]
            for l in lines:
                balance += l.get('qty_in',0)
                balance -= l.get('qty_out',0)
                l['balance'] = balance
                l['_id'] = str(l.get('_id',""))
                res.append(l)
        return res


# var dataTable2 = [
#   {id:1, warehouse:"Warehouse 1", qty_out_table:"Initial Balance", balance_table: 0, serviceHistory:[
#       {date:"01/02/2016", product_code:"LNAFP", lot_number:12, warehouse_from: "Warehouse 1", warehouse_to: "Warehouse4", move_type:"In", unit: "pza", qty_ins: 200, qty_outs: 30, balance: 400},
#       {date:"07/02/2017", product_code:"LNAFP", lot_number:13, warehouse_from: "Warehouse 1", warehouse_to: "Warehouse4", move_type:"In", unit: "pza", qty_ins: 200, qty_outs: 30, balance: 400},
#   ]},
#   {id:2, warehouse:"Warehouse 2", qty_out_table:"Initial Balance", balance_table: 0, serviceHistory:[
#      {date:"22/05/2017", product_code:"LNAFP", lot_number:20, warehouse_from: "Warehouse 2", warehouse_to: "Warehouse4", move_type:"In", unit: "pza", qty_ins: 200, qty_outs: 30, balance: 400},
#      {date:"11/02/2018", product_code:"LNAFP", lot_number:25, warehouse_from: "Warehouse 2", warehouse_to: "Warehouse4", move_type:"In", unit: "pza", qty_ins: 200, qty_outs: 30, balance: 400},
#      {date:"04/04/2018", product_code:"LNAFP", lot_number:30, warehouse_from: "Warehouse 2", warehouse_to: "Warehouse4", move_type:"In", unit: "pza", qty_ins: 200, qty_outs: 30, balance: 400},
#   ]},
# ];
