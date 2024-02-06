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
            res = self.lkf_api.search_catalog( self.CATALOG_PRODUCT_ID, mango_query)
            self.json['productCode'] = [x.get(self.f['product_code']) for x in res]
        if 'inventory' in filters:
            if product_code:
                mango_query['selector'] = {f"answers.{self.f['product_code']}":product_code}
            res = self.lkf_api.search_catalog( self.CATALOG_INVENTORY_ID, mango_query)
            self.json['lotNumber'] = [x.get(self.f['product_lot']) for x in res]

        if 'warehouse' in filters:
            res = self.lkf_api.search_catalog( self.CATALOG_WAREHOUSE_ID, mango_query)
            self.json['warehouse'] = [x.get(self.f['warehouse']) for x in res]
        return True

    def get_inventory_moves(self):
        """
        Return all the movments done on given warehouse, by given product on given dates

        params
        data = self.data.get('data')
        warehouse_to: 
        warehouse_from:
        product_code:
        lot_number:
        date_options:
        date_from:
        date_to
        """
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
        warehouse_from = data.get('warehouse_from')
        warehouse_to = data.get('warehouse_to')
        ####
        print('warehouse_from', warehouse_from)
        print('warehouse_to', warehouse_to)
        print('date_from', date_from)
        print('date_since', date_since)
        moves = {}
        if warehouse_from and warehouse_to:
            moves = self.detail_stock_moves(warehouse=[warehouse_from, warehouse_to], move_type=['out','in'], product_code=product_code, \
                    lot_number=lot_number, date_from=date_from, date_to=date_to)
            if warehouse_from == "Adujstment":
                moves = self.detail_adjustment_moves(product_code=product_code, lot_number=lot_number, \
                    date_from=date_from, date_to=date_to, **{'result':moves, 'move_type':'out'})
            elif warehouse_from == "Scrap":
                print('sarc scrap')
                moves = self.detail_scrap_moves(product_code=product_code, lot_number=lot_number, \
                    date_from=date_from, date_to=date_to, **{'result':moves, 'move_type':'out'})
            if warehouse_to == "Adujstment":
                moves = self.detail_adjustment_moves(warehouse= warehouse_from, product_code=product_code, lot_number=lot_number, \
                    date_from=date_from, date_to=date_to, **{'result':moves, 'move_type':'in'})
            elif warehouse_to == "Scrap":
                print('sarc scrap')
                moves = self.detail_scrap_moves(warehouse_from, product_code=product_code, lot_number=lot_number, \
                    date_from=date_from, date_to=date_to, **{'result':moves, 'move_type':'in'})
        elif warehouse_from and not warehouse_to:
            print('>>>>>>>>>>>>>>>>>>>>FROOOOOOM ONLY')
            if warehouse_from == "Adujstment":
                moves = self.detail_adjustment_moves(product_code=product_code, lot_number=lot_number, \
                    date_from=date_from, date_to=date_to, **{'result':moves})
            elif warehouse_from == "Scrap":
                moves = self.detail_scrap_moves(product_code=product_code, lot_number=lot_number, \
                    date_from=date_from, date_to=date_to, **{'result':moves})
            else:
                moves = self.detail_stock_moves(warehouse=warehouse_from, move_type='out', product_code=product_code, \
                    lot_number=lot_number, date_from=date_from, date_to=date_to)
                #TODO SE ONLY TO
                moves = self.detail_scrap_moves(warehouse_from, product_code=product_code, lot_number=lot_number, \
                    date_from=date_from, date_to=date_to, **{'result':moves, 'move_type':'in'})
                moves = self.detail_adjustment_moves(warehouse=warehouse_from, product_code=product_code, lot_number=lot_number, \
                    date_from=date_from, date_to=date_to, **{'result':moves, 'move_type':'in'})
        elif warehouse_to and not warehouse_from:
            print(34334)
            if warehouse_to == "Adujstment":
                moves = self.detail_adjustment_moves(product_code=product_code, lot_number=lot_number, \
                    date_from=date_from, date_to=date_to, **{'result':moves})
            elif warehouse_to == "Scrap":
                moves = self.detail_scrap_moves(product_code=product_code, lot_number=lot_number, \
                    date_from=date_from, date_to=date_to, **{'result':moves})
            else:
                moves = self.detail_stock_moves(warehouse=warehouse_to, move_type='in', product_code=product_code, lot_number=lot_number, date_from=date_from, date_to=date_to)
                moves = self.detail_adjustment_moves(warehouse=warehouse_to, product_code=product_code, lot_number=lot_number, \
                    date_from=date_from, date_to=date_to, **{'result':moves, 'move_type':'out'})
                moves = self.detail_scrap_moves(warehouse_to, product_code=product_code, lot_number=lot_number, \
                    date_from=date_from, date_to=date_to, **{'result':moves, 'move_type':'out'})
        else:
            print(34)
            moves = self.detail_stock_moves(product_code=product_code, lot_number=lot_number, date_from=date_from, date_to=date_to)
            moves = self.detail_adjustment_moves(product_code=product_code, lot_number=lot_number, \
                date_from=date_from, date_to=date_to, **{'result':moves})
            moves = self.detail_scrap_moves(product_code=product_code, lot_number=lot_number, \
                date_from=date_from, date_to=date_to, **{'result':moves})
        return moves

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
        print('product_code=', product_code)
        if not product_code:
            raise ('prduct code is missing...')
        stock = self.get_product_stock(product_code, lot_number=lot_number, date_from=date_from, date_to=date_to)

        if not warehouse or warehouse == '':
            warehouse = self.get_warehouse('Stock')
        result = []
        for idx, wh in enumerate(warehouse):
            print(f'============ Warehouse: {wh} ==========================')

            if not date_from and not date_since:
                 initial_stock = {'actuals': 0}
            else:
                initial_stock = self.get_product_stock(product_code, warehouse=wh, lot_number=lot_number,  date_to=date_since)
            moves = self.detail_stock_moves(wh, product_code=product_code, lot_number=lot_number, date_from=date_from, date_to=date_to)
            moves = self.detail_adjustment_moves(wh, product_code=product_code, lot_number=lot_number, \
                date_from=date_from, date_to=date_to, **{'result':moves})
            moves = self.detail_production_moves(wh, product_code=product_code, lot_number=lot_number, \
                date_from=date_from, date_to=date_to, **{'result':moves})
            moves = self.detail_scrap_moves(wh, product_code=product_code, lot_number=lot_number, \
                date_from=date_from, date_to=date_to, **{'result':moves})
            warehouse_data = { "id":idx, "warehouse":wh, "qty_out_table":"Initial", 
                "balance_table":initial_stock.get('actuals'),
                "serviceHistory": self.set_kardex_order(initial_stock.get('actuals'), moves)
                }
            result.append(warehouse_data)
            #scrap = self.detail_stock_move(wh)
            #todo_gradinscraping
            # print('moves=', moves)
        return result, stock.get('actuals',)

    def get_scrap_report(self):
        self.scrap_by_product = {}
        self.scrap_by_warehouse = {}
        self.scrap_by_reason = {}
        self.scrap_by_week = {}
        self.warehouse_by_week = {}
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
        if not warehouse or warehouse == '':
            warehouse = self.get_warehouse('Stock')
            self.scrap_by_week = self.stock_scrap_by_week(product_code=product_code, \
                lot_number=lot_number, date_from=date_from, date_to=date_to, status='done')
            self.warehouse_by_week = self.warehouse_scrap_by_week(product_code=product_code,  \
                lot_number=lot_number, date_from=date_from, date_to=date_to, status='done')
        else:
            self.scrap_by_week = self.stock_scrap_by_week(product_code=product_code, warehouse=warehouse, \
                lot_number=lot_number, date_from=date_from, date_to=date_to, status='done')
            self.warehouse_by_week = self.warehouse_scrap_by_week(product_code=product_code, warehouse=warehouse, \
                lot_number=lot_number, date_from=date_from, date_to=date_to, status='done')
            
        for idx, wh in enumerate(warehouse):
            
            scrap = self.stock_scrap_by_reason(product_code=product_code, warehouse=wh, \
                lot_number=lot_number, date_from=date_from, date_to=date_to, status='done')
            self.update_scrap_data(scrap, product_code, wh)

        self.set_scrap_percentage(lot_number=lot_number, date_from=date_from, date_to=date_to)
        return True

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

    def set_scrap_percentage(self, lot_number=None, date_from=None, date_to=None, warehouse=None):
        for product_code, scrap_data in self.scrap_by_product.items():
            stock_init = self.get_product_stock(product_code, lot_number=lot_number, date_to=date_from )
            stock_production = self.stock_production(product_code=product_code, lot_number=lot_number, \
                date_from=date_from, date_to=date_to, warehouse=warehouse )
            #TODO agregar entras de proveedores
            # stock_supplier = self.stock_supplier(date_from=date_from, date_to=date_from, product_code=product_code, \
            #      warehouse=warehouse, lot_number=lot_number)
            stock_actuals = stock_init.get('actuals', 0 ) + stock_production
            self.scrap_by_product[product_code].update({
                'actuals': stock_actuals, 
                'scrap_per': round(scrap_data.get('scrap',0) / stock_actuals,4)
                })
        for warehouse, product_scrap in self.scrap_by_warehouse.items():
            for product_code, scrap_data in product_scrap['products'].items():
                stock = self.get_product_stock(product_code, lot_number=lot_number, date_from=date_from, date_to=date_to )
                actuals = stock['actuals']

                self.scrap_by_warehouse[warehouse]['actuals'] += actuals
                scrap_qty = scrap_data['scrap']
                self.scrap_by_warehouse[warehouse]['products'][product_code].update({
                    'actuals':actuals, 
                    'scrap_per': round(scrap_qty / actuals,4)
                    })

            self.scrap_by_warehouse[warehouse]['scrap_per'] = round(
                self.scrap_by_warehouse[warehouse]['scrap'] / self.scrap_by_warehouse[warehouse]['actuals'],4)

    def stock_scrap_by_reason(self, product_code=None, warehouse=None, location=None, lot_number=None, date_from=None, date_to=None, status='done', **kwargs):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": {"$in":[self.SCRAP_FORM_ID, self.GRADING_FORM_ID]}
            }
        if product_code:
            match_query.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_code']}":product_code})    
        if warehouse:
            match_query.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['warehouse']}":warehouse})    
        if location:
            match_query.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_lot_location']}":location})    
        if lot_number:
            match_query.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_lot']}": int(lot_number)})    
        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field_id=self.f['grading_date']))
        query= [
            {'$match': match_query },
            {'$project':
                {'_id': 1,
                    'product_code': f"$answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_code']}",
                    "reason": {
                        "$cond": [
                            {"$eq": ["$form_id", self.GRADING_FORM_ID]},
                            "Grading",
                            {"$ifNull":[
                                "$answers.64ef91d300ccfc8da7751c47.64ef91d300ccfc8da7751c49",
                                "N/A"]
                            }
                        ]
                        },
                    'scrap': f"$answers.{self.f['inv_scrap_qty']}",
                    'cuarentin': f"$answers.{self.f['inv_cuarentin_qty']}",
                    }
            },

            {'$group':
                {'_id':
                    { 
                    'product_code': '$product_code',
                    'reason': '$reason',
                      },
                  'total_scrap': {'$sum': '$scrap'},
                  'total_cuarentin': {'$sum': '$cuarentin'}
                  }
            },
            {'$project':
                {'_id': 0,
                'product_code': '$_id.product_code',
                'reason': '$_id.reason',
                'total_scrap': '$total_scrap',
                'total_cuarentin': '$total_cuarentin'
                }
            },
            {'$sort': {'product_code': 1}}
            ]
        res = self.cr.aggregate(query)
        result = {}
        for r in res:
            pcode = r.get('product_code')
            reason = r.get('reason')        
            result[pcode] = result.get(pcode, {'scrap':0,'cuarentin':0,'reason':{}})
            result[pcode]['scrap'] += r.get('total_scrap',0)
            result[pcode]['cuarentin'] += r.get('total_cuarentin',0)
            result[pcode]['reason'][reason] = result[pcode]['reason'].get(reason,0)
            result[pcode]['reason'][reason] += r.get('total_scrap',0)
        return result

    def stock_scrap_by_week(self, product_code=None, warehouse=[], location=None, lot_number=None, date_from=None, date_to=None, status='done', **kwargs):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": {"$in":[self.SCRAP_FORM_ID, self.GRADING_FORM_ID]}
            }
        if product_code:
            match_query.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_code']}":product_code})    
        if warehouse:
            match_query.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['warehouse']}": {"$in":warehouse}})    
        if location:
            match_query.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_lot_location']}":location})    
        if lot_number:
            match_query.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_lot']}": int(lot_number)})    
        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field_id=self.f['grading_date']))
        query= [
            {'$match': match_query },
            {'$project':
                {'_id': 1,
                    'week': {'$week':{'$dateFromString':{'dateString': f"$answers.{self.f['grading_date']}"}}},
                    'year': {'$year':{'$dateFromString':{'dateString': f"$answers.{self.f['grading_date']}"}}},
                    'product_code': f"$answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_code']}",
                    'scrap': f"$answers.{self.f['inv_scrap_qty']}",
                    'cuarentin': f"$answers.{self.f['inv_cuarentin_qty']}",
                    }
            },

            {'$group':
                {'_id':
                    { 
                    'week':'$week',
                    'year':'$year',
                    'product_code': '$product_code',
                    #'reason': '$reason',
                      },
                  'total_scrap': {'$sum': '$scrap'},
                  'total_cuarentin': {'$sum': '$cuarentin'}
                  }
            },
            {'$project':
                {'_id': 0,
                'week': '$_id.week',
                'year': '$_id.year',
                'product_code': '$_id.product_code',
                'reason': '$_id.reason',
                'total_scrap': '$total_scrap',
                'total_cuarentin': '$total_cuarentin'
                }
            },
            {'$sort': {'week': 1}}
            ]
        res = self.cr.aggregate(query)
        result = {}
        result_by_week = {}
        for r in res:
            year_week = int(f"{r['year']}{r['week']}")
            pcode = r.get('product_code')
            reason = r.get('reason')       
            
            result_by_week[year_week] = result_by_week.get(year_week,{'scrap':0, 'cuarentin':0, 'products':{},'reason':{}})
            result_by_week[year_week]['scrap'] += r.get('total_scrap',0)
            result_by_week[year_week]['cuarentin'] += r.get('total_cuarentin',0)

            result_by_week[year_week]['products'][pcode] = result_by_week[year_week]['products'].get(pcode, {'scrap':0,'cuarentin':0})
            result_by_week[year_week]['products'][pcode]['scrap'] += r.get('total_scrap',0)
            result_by_week[year_week]['products'][pcode]['cuarentin'] += r.get('total_cuarentin',0)

            result_by_week[year_week]['reason'][reason] = result_by_week[year_week]['reason'].get(reason, {'scrap':0,'cuarentin':0})
            result_by_week[year_week]['reason'][reason]['scrap'] += r.get('total_scrap',0)
            result_by_week[year_week]['reason'][reason]['cuarentin'] += r.get('total_cuarentin',0)

            # result[pcode] = result.get(pcode, {'scrap':0,'cuarentin':0,'reason':{}})
            # result[pcode]['scrap'] += r.get('total_scrap',0)
            # result[pcode]['cuarentin'] += r.get('total_cuarentin',0)

            # result[pcode]['reason'][reason] = result[pcode]['reason'].get(reason,0)
            # result[pcode]['reason'][reason] += r.get('total_scrap',0)
        return result_by_week

    def warehouse_scrap_by_week(self, product_code=None, warehouse=[], location=None, lot_number=None, date_from=None, date_to=None, status='done', **kwargs):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": {"$in":[self.SCRAP_FORM_ID, self.GRADING_FORM_ID]}
            }
        if product_code:
            match_query.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_code']}":product_code})    
        if warehouse:
            match_query.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['warehouse']}":{'$in':warehouse}})    
        if location:
            match_query.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_lot_location']}":location})    
        if lot_number:
            match_query.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_lot']}": int(lot_number)})    
        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field_id=self.f['grading_date']))
        query= [
            {'$match': match_query },
            {'$project':
                {'_id': 1,
                    'week': {'$week':{'$dateFromString':{'dateString': f"$answers.{self.f['grading_date']}"}}},
                    'year': {'$year':{'$dateFromString':{'dateString': f"$answers.{self.f['grading_date']}"}}},
                    'warehouse': f"$answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['warehouse']}",
                    # "reason": {
                    #     "$cond": [
                    #         {"$eq": ["$form_id", self.GRADING_FORM_ID]},
                    #         "Grading",
                    #         {"$ifNull":[
                    #             "$answers.64ef91d300ccfc8da7751c47.64ef91d300ccfc8da7751c49",
                    #             "N/A"]
                    #         }
                    #     ]
                    #    },
                    'scrap': f"$answers.{self.f['inv_scrap_qty']}",
                    'cuarentin': f"$answers.{self.f['inv_cuarentin_qty']}",
                    }
            },

            {'$group':
                {'_id':
                    { 
                    'week':'$week',
                    'year':'$year',
                    'warehouse': '$warehouse',
                    #'reason': '$reason',
                      },
                  'total_scrap': {'$sum': '$scrap'},
                  'total_cuarentin': {'$sum': '$cuarentin'}
                  }
            },
            {'$project':
                {'_id': 0,
                'week': '$_id.week',
                'year': '$_id.year',
                'warehouse': '$_id.warehouse',
                'reason': '$_id.reason',
                'total_scrap': '$total_scrap',
                'total_cuarentin': '$total_cuarentin'
                }
            },
            {'$sort': {'week': 1}}
            ]
        res = self.cr.aggregate(query)
        result = {}
        result_by_week = {}
        for r in res:
            year_week = int(f"{r['year']}{r['week']}")
            pcode = r.get('product_code')
            reason = r.get('reason')        
            warehouse = r.get('warehouse')        
            ### group by year_week
            result_by_week[year_week] = result_by_week.get(year_week,{'scrap':0, 'cuarentin':0, 'warehouse':{}})
            result_by_week[year_week]['scrap'] += r.get('total_scrap',0)
            result_by_week[year_week]['cuarentin'] += r.get('total_cuarentin',0)
            ### group by year_week , warehouse
            result_by_week[year_week]['warehouse'][warehouse] = result_by_week[year_week]['warehouse'].get(warehouse, {'scrap':0,'cuarentin':0})
            result_by_week[year_week]['warehouse'][warehouse]['scrap'] += r.get('total_scrap',0)
            result_by_week[year_week]['warehouse'][warehouse]['cuarentin'] += r.get('total_cuarentin',0)

            # result[pcode] = result.get(pcode, {'scrap':0,'cuarentin':0,'reason':{}})
            # result[pcode]['scrap'] += r.get('total_scrap',0)
            # result[pcode]['cuarentin'] += r.get('total_cuarentin',0)
            # result[pcode]['reason'][reason] = result[pcode]['reason'].get(reason,0)
            # result[pcode]['reason'][reason] += r.get('total_scrap',0)
        return result_by_week

    def update_scrap_data(self, data, product_code=None, warehouse=None):
        """
        Arrages scrap data and sets in 3 dictionaris
        on self scrap_by_product, scrap_by_warehouse and scrap_by_reason = {} 

        params: data (scrap info returned by stock_scarp funtcion)
        params: product_code
        params: warehouse
        """
        # if type(data) == tuple and product_code:
        #     data = {product_code:{'scrap': data[0], 'cuarentin': data[1]}}
        # elif type(data) == tuple and not product_code:
        #     raise ('prduct code is missing...')
        for product_code, prod_data in data.items():
            reasons = prod_data.get('reason')
            self.scrap_by_product[product_code] = self.scrap_by_product.get(product_code,{'scrap': 0, 'cuarentin': 0,'reason':{}})
            self.scrap_by_product[product_code]['scrap'] += prod_data['scrap']
            self.scrap_by_product[product_code]['cuarentin'] += prod_data['cuarentin']
            ## Wahrehouse
            self.scrap_by_warehouse[warehouse] = self.scrap_by_warehouse.get(warehouse, 
                {'scrap': 0, 'cuarentin': 0, 'actuals':0, 'products':{}, 'reason':{}
                })
            self.scrap_by_warehouse[warehouse]['scrap'] += prod_data['scrap']
            self.scrap_by_warehouse[warehouse]['cuarentin'] += prod_data['cuarentin']
            self.scrap_by_warehouse[warehouse]['products'][product_code] = \
                self.scrap_by_warehouse[warehouse]['products'].get(product_code , {'scrap': 0, 'cuarentin': 0, 'actuals':0, 'reason':{}})
            self.scrap_by_warehouse[warehouse]['products'][product_code]['scrap'] += prod_data['scrap']
            self.scrap_by_warehouse[warehouse]['products'][product_code]['cuarentin'] += prod_data['cuarentin']
            #sets reasons            
            for reason, res_qty in reasons.items():
                self.scrap_by_reason[reason] = self.scrap_by_reason.get(reason,{'scrap':0,'product':{} })
                self.scrap_by_reason[reason]['scrap'] += res_qty
                self.scrap_by_reason[reason]['product'][product_code] = self.scrap_by_reason[reason]['product'].get(product_code,0)
                self.scrap_by_reason[reason]['product'][product_code] += res_qty
                
                self.scrap_by_product[product_code]['reason'][reason] = self.scrap_by_product[product_code]['reason'].get(reason,0)
                self.scrap_by_product[product_code]['reason'][reason] += res_qty
                
                self.scrap_by_warehouse[warehouse]['reason'][reason] = self.scrap_by_warehouse[warehouse]['reason'].get(reason,0)
                self.scrap_by_warehouse[warehouse]['reason'][reason] += res_qty
                self.scrap_by_warehouse[warehouse]['products'][product_code]['reason'][reason] = \
                    self.scrap_by_warehouse[warehouse]['products'][product_code]['reason'].get(reason,0)
                self.scrap_by_warehouse[warehouse]['products'][product_code]['reason'][reason] += res_qty

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
