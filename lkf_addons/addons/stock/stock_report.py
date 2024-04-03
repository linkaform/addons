# -*- coding: utf-8 -*-

from datetime import timedelta, datetime
import math, simplejson, time
from copy import deepcopy

from .stock_utils import Stock


from linkaform_api import base


class Reports(base.LKF_Report, Stock):


    def get_report_filters(self, filters=[], product_code=None):
        mango_query = {"selector":
            {"_id":
                {"$gt":None}
            },
            "limit":10000,
            "skip":0
        }
        if 'products' in filters:
            res = self.lkf_api.search_catalog( self.PRODUCT_ID, mango_query)
            print('self.PRODUCT_OBJ_ID',self.PRODUCT_OBJ_ID)
            print('mango_query',mango_query)
            print('res',res)
            self.json['productCode'] = [x.get(self.f['product_code']) for x in res if x.get(self.f['product_code'])]
        if 'inventory' in filters:
            if product_code:
                mango_query['selector'] = {f"answers.{self.f['product_code']}":product_code}
            res = self.lkf_api.search_catalog( self.STOCK_INVENTORY_ID, mango_query)
            self.json['lotNumber'] = [x.get(self.f['product_lot']) for x in res if x.get(self.f['product_lot'])]
        if 'warehouse' in filters:
            res = self.lkf_api.search_catalog( self.WAREHOUSE_ID, mango_query)
            self.json['warehouse'] = [x.get(self.f['warehouse']) for x in res if x.get(self.f['warehouse'])]
        return True

    def get_product_kardex(self):
        data = self.data.get('data')
        product_code = data.get('product_code', [])
        lot_number = data.get('lot_number',[])
        date_options = data.get('date_options', "custom")
        if date_options == "custom":
            date_from = data.get('date_from')
            date_to = data.get('date_to')
        else:
            date_from, date_to = self.get_period_dates(date_options)
            #strips time from date
            if date_from:
                date_from = str(date_from)[:10]
            if date_to:
                date_to = str(date_to)[:10]
        date_since = None
        if date_from:
            date_since = self.date_operation(date_from, '-', 1, 'day', date_format='%Y-%m-%d')
        warehouse = data.get('warehouse',[])
        if type(warehouse) == str and warehouse != '':
            warehouse = [warehouse,]
        move_type = None
        if not product_code:
            self.LKFException('prduct code is missing...')
        stock = self.get_product_stock(product_code, lot_number=lot_number, date_from=date_from, date_to=date_to)
        print('stock', stock)
        if not warehouse or warehouse == '':
            warehouse = self.get_warehouse('Stock')
        result = []

        product_code = self.validate_value(product_code)
        lot_number = self.validate_value(lot_number)
        warehouse = self.validate_value(warehouse)
        date_since = self.validate_value(date_since)
        for idx, wh in enumerate(warehouse):
            if wh != 'Almacen Central':
                continue
            print(f'============ Warehouse: {wh} ==========================')

            if not date_from and not date_since:
                 initial_stock = {'actuals': 0}
            else:
                initial_stock = self.get_product_stock(product_code, warehouse=wh, lot_number=lot_number,  date_to=date_since)
            # print('initial_stock........',initial_stock)
            # print('acrrranca........')
            moves = self.detail_stock_moves(wh, product_code=product_code, lot_number=lot_number, date_from=date_from, date_to=date_to)
            moves = self.detail_adjustment_moves(wh, product_code=product_code, lot_number=lot_number, \
                date_from=date_from, date_to=date_to, **{'result':moves})
            moves = self.detail_production_moves(wh, product_code=product_code, lot_number=lot_number, \
                date_from=date_from, date_to=date_to, **{'result':moves})
            # moves = self.detail_many_one_one(wh, product_code=product_code, lot_number=lot_number, \
            #     date_from=date_from, date_to=date_to, **{'result':moves})
            # moves = self.detail_scrap_moves(wh, product_code=product_code, lot_number=lot_number, \
            #     date_from=date_from, date_to=date_to, **{'result':moves})
            # moves = self.detail_many_one_one(wh, product_code=product_code, lot_number=lot_number, \
            #     date_from=date_from, date_to=date_to, **{'result':moves})
            #todo scrap out many one many
            if moves:
                warehouse_data = { "id":idx, "warehouse":wh, "qty_out_table":"Initial", 
                    "balance_table":initial_stock.get('actuals'),
                    "serviceHistory": self.set_kardex_order(initial_stock.get('actuals'), moves)
                    }
                result.append(warehouse_data)
            #scrap = self.detail_stock_move(wh)
            #todo_gradinscraping
            # print('moves=', moves)
        return result, stock.get('actuals',)

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