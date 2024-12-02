# -*- coding: utf-8 -*-

from datetime import timedelta, datetime
import math, simplejson, time
from copy import deepcopy

from linkaform_api import base

from .app import JIT

print('carga base')

class Reports(JIT, base.LKF_Report):


    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False, **kwargs):
        #base.LKF_Base.__init__(self, settings, sys_argv=sys_argv, use_api=use_api)
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api, **kwargs)



    def test(self):
        print('test')

    def reorder_rules_warehouse(self, warehouse=None, product_code=None, status='active'):
        match_query = {
            'form_id': self.REGLAS_REORDEN,
            'deleted_at':{'$exists':False},
            f'answers.{self.mf["status"]}': status
        }
        if warehouse:
            match_query.update({ f"answers.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.WH.f['warehouse']}":warehouse})
        # if product_code:
        #     if product_code and type(product_code) == list:
        #         match_query.update({f"answers.{self.Product.SKU_OBJ_ID}.{self.f['product_code']}": {"$in":product_code}})
        #     elif product_code:
        #         match_query.update({f"answers.{self.Product.SKU_OBJ_ID}.{self.f['product_code']}": product_code})
        #Borrar
        match_query.update({
            f"answers.{self.Product.SKU_OBJ_ID}.{self.f['product_code']}": '750200301040'})
        query = [
            {"$match": match_query},
            {"$project": {
                "_id":1,
                "folio":"$folio",
                "product_code": "$answers.66dfc4d9a306e1ac7f6cd02c.61ef32bcdf0ec2ba73dec33d",
                "stock_maximum": "$answers.66ea62dac9aefada5b04b73a",
                "warehouse": f"$answers.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.f['warehouse']}",
                "location":  f"$answers.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.f['warehouse_location']}",
            }},
            {"$group":{
                "_id":{
                    "warehouse":"$warehouse",
                    "location":"$location",
                    "product_code":"$product_code",
                },
                "stock_maximum":{"$last":"$stock_maximum"}
            }},
            {"$project":{
                "_id":0,
                "warehouse":"$_id.warehouse",
                "location":"$_id.location",
                "product_code":"$_id.product_code",
                "stock_maximum": "$stock_maximum"
            }},
        ]
        results = self.format_cr(self.cr.aggregate(query))
        return results
