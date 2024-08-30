# -*- coding: utf-8 -*-

from datetime import timedelta, datetime
import math, simplejson, time
from copy import deepcopy

from .stock_utils import Stock


from linkaform_api import base


class Reports(base.LKF_Report, Stock):


    def detail_adjustment_moves(self, warehouse=None, product_code=None, lot_number=None,  location=None, date_from=None, date_to=None, status='done', **kwargs):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.ADJUIST_FORM_ID,
            f"answers.{self.f['inv_adjust_status']}":{"$ne":"cancel"}
            }
        # print('adjustment', warehouse)
        inc_folio = kwargs.get("inc_folio")
        nin_folio = kwargs.get("nin_folio")
        if nin_folio:
            match_query.update({"folio": {"$ne":nin_folio }})
        if inc_folio:
            match_query_stage2 = {"$or": [
                {f"answers.{self.f['grading_group']}.{self.f['inv_adjust_grp_status']}": "done"},
                {"folio":inc_folio}
                ]}

        unwind_query = {}
        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field_id=f"{self.f['grading_date']}"))
        #Stage 1 Match
        # if status:
        #     match_query.update({f"answers.{self.f['inv_adjust_status']}":status})
        if warehouse:
            match_query.update({f"answers.{self.WAREHOUSE_LOCATION_OBJ_ID}.{self.f['warehouse']}":warehouse})      
        if location:
            match_query.update({f"answers.{self.WAREHOUSE_LOCATION_OBJ_ID}.{self.f['warehouse_location']}":location})
        query= [{'$match': match_query },]
        
        #Stage 2 Match

        if product_code:
            unwind_query.update({f"answers.{self.f['grading_group']}.{self.SKU_OBJ_ID }.{self.f['product_code']}":product_code})
        if lot_number:
            unwind_query.update({f"answers.{self.f['grading_group']}.{self.f['lot_number']}":lot_number})
        
        if unwind_query:
            query += [
            {'$unwind': f"$answers.{self.f['grading_group']}"},
            {'$match': unwind_query }
            ]

        query += [
            {'$project':
                {'_id': 1,
                    'folio': "$folio",
                    'created_at': "$created_at",
                    'date': f"$answers.{self.f['grading_date']}",
                    'warehouse': f"$answers.{self.WAREHOUSE_LOCATION_OBJ_ID}.{self.f['warehouse']}",
                    'location': f"$answers.{self.WAREHOUSE_LOCATION_OBJ_ID}.{self.f['warehouse_location']}",
                    'product_code': f"$answers.{self.f['grading_group']}.{self.SKU_OBJ_ID}.{self.f['product_code']}",
                    'lot_number': f"$answers.{self.f['grading_group']}.{self.f['product_lot']}",
                    'adjust_in':{ "$ifNull":[ 
                        f"$answers.{self.f['grading_group']}.{self.f['inv_adjust_grp_in']}",
                        0]},
                    'adjust_out': { "$ifNull":[
                        f"$answers.{self.f['grading_group']}.{self.f['inv_adjust_grp_out']}",
                        0]}
                    }
            },
            {'$project':
                {'_id': 1,
                'folio':'$folio',
                'created_at': "$created_at",
                'date':'$date',
                'product_code':'$product_code',
                'lot_number':'$lot_number',
                'move_type': { "$cond":[ 
                        {"$gt":[ f"$adjust_in" , 0]}, 
                        "In", 
                        "Out" ]},
                'warehouse_from':{ "$cond":[ 
                        {"$gt":[ f"$adjust_in" , 0]}, 
                        "Adujstment", 
                        "$warehouse" ]},
                'warehouse_location_from':{ "$cond":[ 
                        {"$gt":[ f"$adjust_in" , 0]}, 
                        "Adujstment", 
                        "$product_code" ]},
                'warehouse_to':{ "$cond":[ 
                        {"$gt":[ f"$adjust_in" , 0]}, 
                        "$warehouse", 
                        "Adujstment" ]},
                'warehouse_location_to':{ "$cond":[ 
                        {"$gt":[ f"$adjust_in" , 0]}, 
                        "$location", 
                        "Adujstment" ]},
                'qty_in': "$adjust_in",
                'qty_out': "$adjust_out",
                }
            },
            {'$sort': {'product_code': 1}}
            ]
        # print('adjustment query= ', simplejson.dumps(query, indent=4))
        res = self.cr.aggregate(query)
        move_type = kwargs.get('move_type')
        # print('move_type', move_type)
        if kwargs.get('result'):
            result = kwargs['result']
        else:
            result = {}
        for r in res:
            # print('r',r)
            if move_type == 'in':
                if r['warehouse_to'] != 'Adujstment':
                    continue
            if move_type == 'out':
                if r['warehouse_from'] != 'Adujstment':
                    continue
            r['created_at'] = str(r['created_at'])
            epoch = self.date_2_epoch(r.get('date'))
            result[epoch] = result.get(epoch,[])
            result[epoch].append(r)
        return result

    def detail_stock_moves(self, warehouse=None, move_type=[], product_code=None, lot_number=None,  location=None, date_from=None, date_to=None, status='done', **kwargs):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.STOCK_MOVE_FORM_ID,
            }
        inc_folio = kwargs.get("inc_folio")
        nin_folio = kwargs.get("nin_folio")
        if warehouse:
            if type(warehouse) == list:
                warehouse_from = warehouse[0]
                warehouse_to = warehouse[1].lower().replace(' ', '_')
            else:
                warehouse_from = warehouse
                warehouse_to = warehouse.lower().replace(' ', '_')

            if move_type =='out' or 'out' in move_type:
                match_query.update({f"answers.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['warehouse']}":warehouse_from})      
            if move_type =='in' or 'in' in move_type:
                match_query.update({f"answers.{self.f['move_new_location']}":warehouse_to})
            if not move_type:
                match_query.update(
                    {"$or":
                        [{f"answers.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['warehouse']}":warehouse_from},
                        {f"answers.{self.f['move_new_location']}":warehouse_to}
                        ]
                    })      
        if inc_folio:
            match_query.update({"folio":inc_folio})
        if nin_folio:
            match_query.update({"folio": {"$ne":nin_folio }})
        if product_code:
            match_query.update({f"answers.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['product_code']}":product_code})
        if lot_number:
            match_query.update({f"answers.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['product_lot']}":lot_number})
        if location:
            match_query.update({f"answers.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['product_code']}":location})
        if status:
            match_query.update({f"answers.{self.f['inv_adjust_status']}":status})
        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field_id=self.f['grading_date']))
        query= [{'$match': match_query },
            {'$project':
                {'_id': 1,
                    'folio': "$folio",
                    'created_at': "$created_at",
                    'date': f"$answers.{self.f['grading_date']}",
                    'product_code': f"$answers.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['product_code']}",
                    'lot_number': f"$answers.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['product_lot']}",
                    'warehouse_from': f"$answers.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['warehouse']}",
                    'warehouse_to':f"$answers.{self.f['move_new_location']}",
                    'move_type':{ "$cond":[ 
                        {"$eq":[ f"$answers.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['warehouse']}" , warehouse]}, 
                        "Out", 
                        "In" ]},
                    'qty':f"$answers.{self.f['inv_move_qty']}"
                    }
            },
            {'$project':
                {'_id': 1,
                    'folio': "$folio",
                    'created_at': "$created_at",
                    'date': "$date",
                    'product_code': "$product_code",
                    'lot_number': "$lot_number",
                    'warehouse_from': "$warehouse_from",
                    'warehouse_to': "$warehouse_to",
                    'move_type': "$move_type",
                    'qty_in' :{ "$cond":[ 
                        {"$eq":[ "$move_type" , "In"]}, 
                        "$qty", 
                        0 ]},
                    'qty_out' :{ "$cond":[ 
                        {"$eq":[ "$move_type" , "Out"]}, 
                       "$qty", 
                        0 ]},
                    }
            },
            {'$sort': {'date': 1}}
            ]
        print('query=', simplejson.dumps(query, indent=4))
        res = self.cr.aggregate(query)
        if kwargs.get('result'):
            result = kwargs['result']
        else:
            result = {}
        for r in res:
            r['created_at'] = str(r['created_at'])
            epoch = self.date_2_epoch(r.get('date'))
            r['warehouse_to'] = r['warehouse_to'].replace('_', ' ').title()
            result[epoch] = result.get(epoch,[])
            result[epoch].append(r)
        return result

    def detail_many_one_one(self, warehouse=None, product_code=None, lot_number=None,  location=None, date_from=None, date_to=None, status='done', **kwargs):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": {"$in":[self.STOCK_MANY_LOCATION_2_ONE,self.STOCK_MANY_LOCATION_OUT]}
            }
        unwind_query = {}
        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field_id=f"{self.f['grading_date']}"))
        #Stage 1 Match
        if product_code:
            match_query.update({f"answers.{self.SKU_OBJ_ID}.{self.f['product_code']}":product_code})
        if status:
            match_query.update({f"answers.{self.f['inv_adjust_status']}":status})
        
        query= [{'$match': match_query },]
        
        #Stage 2 Match
        if lot_number:
            unwind_query.update({f"answers.{self.f['move_group']}.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['product_lot']}":lot_number})  
        if warehouse:
            unwind_query.update({f"answers.{self.f['move_group']}.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['warehouse']}":warehouse})    
        if location:
            unwind_query.update({f"answers.{self.f['move_group']}.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['warehouse_location']}":location})    
        if unwind_query:
            query += [
            {'$unwind': f"$answers.{self.f['move_group']}"},
            {'$match': unwind_query }
            ]
        query += [
            {'$project':
                {'_id': 1,
                    'folio': "$folio",
                    'form_id':'$form_id',
                    'created_at': "$created_at",
                    'date': f"$answers.{self.f['grading_date']}",
                    'product_code': f"$answers.{self.SKU_OBJ_ID}.{self.f['product_code']}",
                    'lot_number': f"$answers.{self.f['move_group']}.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['product_lot']}",
                    'warehouse_from': f"$answers.{self.f['move_group']}.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['warehouse']}",
                    'warehouse_location_from': f"$answers.{self.f['move_group']}.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['warehouse_location']}",
                    'warehouse_to':f"$answers.{self.WAREHOUSE_LOCATION_DEST_OBJ_ID}.{self.f['warehouse_dest']}",
                    'warehouse_location_to':f"$answers.{self.WAREHOUSE_LOCATION_DEST_OBJ_ID}.{self.f['warehouse_location_dest']}",
                    'move_type':{ "$cond":[ 
                        {"$eq":[ f"$answers.{self.f['move_group']}.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['warehouse']}" , warehouse]}, 
                        "Out", 
                        "In" ]},
                    'qty':f"$answers.{self.f['move_group']}.{self.f['inv_move_qty']}"
                    }
            },
            {'$project':
                {'_id': 1,
                    'folio': "$folio",
                    'form_id':'$form_id',
                    'created_at': "$created_at",
                    'date': "$date",
                    'product_code': "$product_code",
                    'lot_number': "$lot_number",
                    'warehouse_from': "$warehouse_from",
                    'warehouse_location_from': "$warehouse_location_from",
                    'warehouse_to': "$warehouse_to",
                    'warehouse_location_to': "$warehouse_location_to",
                    'move_type': "$move_type",
                    'qty_in' :{ "$cond":[ 
                        {"$eq":[ "$move_type" , "In"]}, 
                        "$qty", 
                        0 ]},
                    'qty_out' :{ "$cond":[ 
                        {"$eq":[ "$move_type" , "Out"]}, 
                       "$qty", 
                        0 ]},
                    }
            },
            {'$sort': {'date': 1}}
            ]
        print('query=', simplejson.dumps(query, indent=4))
        res = self.cr.aggregate(query)
        if kwargs.get('result'):
            result = kwargs['result']
        else:
            result = {}

        for r in res:
            if r['form_id'] == self.STOCK_MANY_LOCATION_OUT:
                warehouse_to = 'Pull'
                warehouse_location_to = 'Greenhouse'
            r['created_at'] = str(r['created_at'])
            epoch = self.date_2_epoch(r.get('date'))
            if r.get('warehouse_to'):
                r['warehouse_to'] = r['warehouse_to'].replace('_', ' ').title()
            else:
                r['warehouse_to'] = warehouse_to

            if r.get('warehouse_location_to'):
                r['warehouse_to'] += f" / {r['warehouse_location_to']}"
            elif warehouse_location_to:
                r['warehouse_to'] += f" / {warehouse_location_to}"

            if r.get('warehouse_location_from'):
                r['warehouse_from'] += f" / {r['warehouse_location_from']}"

            result[epoch] = result.get(epoch,[])
            result[epoch].append(r)
        return result

    def detail_one_many_one(self, warehouse=None, product_code=None, lot_number=None,  location=None, date_from=None, date_to=None, status='done', **kwargs):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": {"$in":self.STOCK_ONE_MANY_ONE_FORMS}
            }
        unwind_query = {}
        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field_id=f"{self.f['grading_date']}"))
        #Stage 1 Match
        if status:
            match_query.update({f"answers.{self.f['inv_adjust_status']}":status})
        if warehouse:
            match_query.update({f"answers.{self.WAREHOUSE_LOCATION_OBJ_ID}.{self.f['warehouse']}":warehouse})    
        if location:
            match_query.update({f"answers.{self.WAREHOUSE_LOCATION_OBJ_ID}.{self.f['warehouse_location']}":location})    
        
        query= [{'$match': match_query },]
        
        #Stage 2 Match
        if product_code:
            unwind_query.update({f"answers.{self.f['move_group']}.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['product_code']}":product_code})
        if lot_number:
            unwind_query.update({f"answers.{self.f['move_group']}.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['product_lot']}":lot_number})  
        if unwind_query:
            query += [
            {'$unwind': f"$answers.{self.f['move_group']}"},
            {'$match': unwind_query }
            ]
        query += [
            {'$project':
                {'_id': 1,
                    'folio': "$folio",
                    'form_id':'$form_id',
                    'created_at': "$created_at",
                    'date': f"$answers.{self.f['grading_date']}",
                    'product_code': f"$answers.{self.SKU_OBJ_ID}.{self.f['product_code']}",
                    'lot_number': f"$answers.{self.f['move_group']}.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['product_lot']}",
                    'warehouse_from': f"$answers.{self.WAREHOUSE_LOCATION_OBJ_ID}.{self.f['warehouse']}",
                    'warehouse_location_from': f"$answers.{self.WAREHOUSE_LOCATION_OBJ_ID}.{self.f['warehouse_location']}",
                    'warehouse_to':f"$answers.{self.WAREHOUSE_LOCATION_DEST_OBJ_ID}.{self.f['warehouse_dest']}",
                    'warehouse_location_to':f"$answers.{self.WAREHOUSE_LOCATION_DEST_OBJ_ID}.{self.f['warehouse_location_dest']}",
                    'move_type':{ "$cond":[ 
                        {"$eq":[ f"$answers.{self.WAREHOUSE_LOCATION_OBJ_ID}.{self.f['warehouse']}" , warehouse]}, 
                        "Out", 
                        "In" ]},
                    'qty':f"$answers.{self.f['move_group']}.{self.f['move_group_qty']}"
                    }
            },
            {'$project':
                {'_id': 1,
                    'folio': "$folio",
                    'form_id':'$form_id',
                    'created_at': "$created_at",
                    'date': "$date",
                    'product_code': "$product_code",
                    'lot_number': "$lot_number",
                    'warehouse_from': "$warehouse_from",
                    'warehouse_location_from': "$warehouse_location_from",
                    'warehouse_to': "$warehouse_to",
                    'warehouse_location_to': "$warehouse_location_to",
                    'move_type': "$move_type",
                    'qty_in' :{ "$cond":[ 
                        {"$eq":[ "$move_type" , "In"]}, 
                        "$qty", 
                        0 ]},
                    'qty_out' :{ "$cond":[ 
                        {"$eq":[ "$move_type" , "Out"]}, 
                       "$qty", 
                        0 ]},
                    }
            },
            {'$sort': {'date': 1}}
            ]
        print('OMO query=', simplejson.dumps(query, indent=4))
        res = self.cr.aggregate(query)
        if kwargs.get('result'):
            result = kwargs['result']
        else:
            result = {}

        for r in res:
            print('r=',r)
            if r['form_id'] == self.STOCK_MANY_LOCATION_OUT:
                warehouse_to = 'Pull'
                warehouse_location_to = 'Greenhouse'
            r['created_at'] = str(r['created_at'])
            epoch = self.date_2_epoch(r.get('date'))
            if r.get('warehouse_to'):
                r['warehouse_to'] = r['warehouse_to'].replace('_', ' ').title()
            else:
                r['warehouse_to'] = warehouse_to

            if r.get('warehouse_location_to'):
                r['warehouse_to'] += f" / {r['warehouse_location_to']}"
            elif warehouse_location_to:
                r['warehouse_to'] += f" / {warehouse_location_to}"

            if r.get('warehouse_location_from'):
                r['warehouse_from'] += f" / {r['warehouse_location_from']}"

            result[epoch] = result.get(epoch,[])
            result[epoch].append(r)
        return result

    def detail_production_moves(self, warehouse=None, product_code=None, lot_number=None,  location=None, date_from=None, date_to=None, status='posted', **kwargs):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.PRODUCTION_FORM_ID,
            }
        match_query_stage2 = {}
        if date_from or date_to:
            match_query_stage2.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field_id=f"{self.f['production_group']}.{self.f['set_production_date']}"))
        if product_code:
            match_query.update({f"answers.{self.SKU_OBJ_ID}.{self.f['product_code']}":product_code})
        if lot_number:
            match_query.update({f"answers.{self.f['production_lote']}":lot_number})  
        if warehouse:
            match_query.update({f"answers.{self.WAREHOUSE_OBJ_ID}.{self.f['warehouse']}":warehouse})    
        if location:
            match_query_stage2.update({f"answers.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['product_lot_location']}":location})    
        if status:
            match_query_stage2.update({f"answers.{self.f['production_group']}.{self.f['production_status']}":status})
        query= [{'$match': match_query },
            {'$unwind': f"$answers.{self.f['production_group']}"},
            ]
        if match_query_stage2:
            query += [{'$match': match_query_stage2 }]
        query += [
            {'$project':
                {'_id': 1,
                    'folio':'$folio',
                    'date': f"$answers.{self.f['production_group']}.{self.f['set_production_date']}",
                    'product_code': f"$answers.{self.SKU_OBJ_ID}.{self.f['product_code']}",
                    'lot_number':f"$answers.{self.f['production_lote']}",
                    'total': f"$answers.{self.f['production_group']}.{self.f['set_total_produced']}",
                    }
            },
            {'$group':
                {'_id':
                    { 
                        'id': '$_id',
                        'product_code': '$product_code',
                        'date': '$date',
                        'lot_number': '$lot_number',
                        'folio': '$folio',
                      },
                  'total': {'$sum': '$total'},
                  }
            },
            {'$project':
                {'_id': '$_id.id',
                'product_code': '$_id.product_code',
                'date': '$_id.date',
                'lot_number': '$_id.lot_number',
                'folio': '$_id.folio',
                'qty_in': '$total',
                'move_type':'In',
                'warehouse_from':"Production",
                'warehouse_to':warehouse,
                }
            },
            {'$sort': {'date': 1}}
            ]
        res = self.cr.aggregate(query)
        if kwargs.get('result'):
            result = kwargs['result']
        else:
            result = {}
        for r in res:
            epoch = self.date_2_epoch(r.get('date'))
            result[epoch] = result.get(epoch,[])
            result[epoch].append(r)
        return result

    def detail_scrap_moves(self, warehouse=None, product_code=None, lot_number=None, location=None, date_from=None, date_to=None, status='done', **kwargs):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": {"$in":[self.SCRAP_FORM_ID, self.GRADING_FORM_ID]}
            }
        print('warehouse', warehouse)
        if product_code:
            match_query.update({f"answers.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['product_code']}":product_code})    
        if warehouse:
            match_query.update({f"answers.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['warehouse']}":warehouse})    
        if location:
            match_query.update({f"answers.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['product_lot_location']}":location})    
        if lot_number:
            match_query.update({f"answers.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['product_lot']}":lot_number})    
        if status:
            match_query.update({f"answers.{self.f['inv_scrap_status']}":status})
        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field_id=self.f['grading_date']))
        query= [
            {'$match': match_query },
            {'$project':
                {'_id': 1,
                    'date': f"$answers.{self.f['grading_date']}",
                    'created_at': "$created_at",
                    'product_code': f"$answers.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['product_code']}",
                    'lot_number': f"$answers.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['product_lot']}",
                    'warehouse_from': f"$answers.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['warehouse']}",
                    'scrap': f"$answers.{self.f['inv_scrap_qty']}",
                    'cuarentin': f"$answers.{self.f['inv_cuarentin_qty']}",
                    'warehouse_to':'Scrap',
                    }
            },
            {'$sort': {'date': 1}}
            ]
        res = self.cr.aggregate(query)
        move_type = kwargs.get('move_type')
        if kwargs.get('result'):
            result = kwargs['result']
        else:
            result = {}
        for r in res:
            r['created_at'] = str(r['created_at'])
            epoch = self.date_2_epoch(r.get('date'))
            result[epoch] = result.get(epoch,[])
            cuarentine = r.get('cuarentin',0)
            scrap = r.get('scrap',0)
            print('r=',r)
            print('scrap=',scrap)
            if cuarentine:
                r.update({
                    'warehouse_to': "Cuarentin",
                    'qty_out':cuarentine,
                    })
                result[epoch].append(r)
            if scrap:
                if move_type == 'in':
                    if r['warehouse_to'] != 'Scrap':
                        continue
                if move_type == 'out':
                    if r['warehouse_from'] != 'Scrap':
                        continue
                print('qty out', scrap)
                r.update({
                    'warehouse_to': "Scrap",
                    'qty_out':scrap,
                    })
                result[epoch].append(r)
        return result

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