# -*- coding: utf-8 -*-

from linkaform_api import base
from lkf_addons.addons.base.app import Base


class Product(Base, base.LKF_Base):

    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False):
        # base.LKF_Base.__init__(self, settings, sys_argv=sys_argv)
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api)
        self.name =  __class__.__name__
        self.settings = settings
        
        self.PRODUCT = self.lkm.catalog_id('product_catalog')
        print('selef', self.PRODUCT)
        self.PRODUCT_ID = self.PRODUCT.get('id')
        self.PRODUCT_OBJ_ID = self.PRODUCT.get('obj_id')

        try:
            self.SKU = self.lkm.catalog_id('sku_catalog')
            self.SKU_ID = self.SKU.get('id')
            self.SKU_OBJ_ID = self.SKU.get('obj_id')
        except:
            self.SKU = self.lkm.catalog_id('product_recipe')
            self.SKU_ID = self.SKU.get('id')
            self.SKU_OBJ_ID = self.SKU.get('obj_id')

        ###### Depricated ######
        try:
            self.PRODUCT_RECIPE = self.lkm.catalog_id('product_recipe')
            self.PRODUCT_RECIPE_ID = self.PRODUCT_RECIPE.get('id')
            self.PRODUCT_RECIPE_OBJ_ID = self.PRODUCT_RECIPE.get('obj_id')
        except:
            self.PRODUCT_RECIPE_ID = self.SKU.get('id')
            self.PRODUCT_RECIPE_OBJ_ID = self.SKU.get('obj_id')

        self.f.update( {
            'product_code':'61ef32bcdf0ec2ba73dec33d',
            'product_name':'61ef32bcdf0ec2ba73dec33e',
            'product_category':'61ef32bcdf0ec2ba73dec342',
            'product_type':'61ef32bcdf0ec2ba73dec343',
            'product_recipe':'61ef32bcdf0ec2ba73dec33c',
            'product_sku':'65dec64a3199f9a040829243',
            'product_department':'621fc992a7ebfd603a8c5e2e',
            'sku':'65dec64a3199f9a040829243',
            'sku_color':'621fca56ee94313e8d8c5e2e',
            'sku_image':'65dec64a3199f9a040829244',
            'sku_note':'6205f73281bb36a6f157335c',
            'sku_package':'6209705080c17c97320e3382',
            'sku_percontainer':'6205f73281bb36a6f157335b',
            'sku_size':'6205f73281bb36a6f1573358',
            'sku_source':'6205f73281bb36a6f157335a',
            }
            )

    def una_funcion_product(self):
        return True

    def get_product(self, product_code):
        return self.get_product_field(self, product_code, pfield='*')

    def get_product_field(self, product_code, pfield='product_name'):
        product_field = None
        mango_query = {
            "selector": {
                "answers": {
                    self.f['product_code']: {"$eq": product_code},
                    } ,
                },
            "limit": 1,
            "skip": 0
                }
        record = self.lkf_api.search_catalog(self.PRODUCT_ID, mango_query)
        if record and len(record) > 0:
            rec = record[0]
            if product_field == '*':
                return rec
            product_field = rec.get(self.f[pfield])
        return product_field



class Warehouse(Base ,base.LKF_Base):


    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False):
        # base.LKF_Base.__init__(self, settings, sys_argv=sys_argv)
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api)
        self.name =  __class__.__name__
        self.settings = settings

        self.WAREHOUSE = self.lkm.catalog_id('warehouse')
        self.WAREHOUSE_ID = self.WAREHOUSE.get('id')
        self.WAREHOUSE_OBJ_ID = self.WAREHOUSE.get('obj_id')

        self.WAREHOUSE_LOCATION = self.lkm.catalog_id('warehouse_locations')
        self.WAREHOUSE_LOCATION_ID = self.WAREHOUSE_LOCATION.get('id')
        self.WAREHOUSE_LOCATION_OBJ_ID = self.WAREHOUSE_LOCATION.get('obj_id')

        self.WAREHOUSE_DEST = self.lkm.catalog_id('warehouse_destination')
        self.WAREHOUSE_DEST_ID = self.WAREHOUSE_LOCATION.get('id')
        self.WAREHOUSE_DEST_OBJ_ID = self.WAREHOUSE_LOCATION.get('obj_id')


        self.WAREHOUSE_LOCATION_DEST = self.lkm.catalog_id('warehouse_location_destination')
        self.WAREHOUSE_LOCATION_DEST_ID = self.WAREHOUSE_LOCATION_DEST.get('id')
        self.WAREHOUSE_LOCATION_DEST_OBJ_ID = self.WAREHOUSE_LOCATION_DEST.get('obj_id')


        self.f.update( {
            'warehouse':'6442e4831198daf81456f274',
            'warehouse_dest':'65bdc71b3e183f49761a33b9',
            'warehouse_location':'65ac6fbc070b93e656bd7fbe',
            'warehouse_location_dest':'65c12749cfed7d3a0e1a341b',
            'warehouse_type':'6514f51b6cfe23860299abfa',
            'warehouse_type_dest':'65bdc74a9c6a5b1adf424b5b',
            }
        )

    def get_all_stock_warehouse(self):
        return self.get_warehouse(warehouse_type='Stock')

    def get_warehouse(self, warehouse_type=None):
        mango_query = {
            "selector":{"_id": {"$gt":None}},
            "limit":1000,
            "skip":0
            }
        if warehouse_type:
            mango_query['selector'] = {'answers':{self.f['warehouse_type']: warehouse_type}}
        res = self.lkf_api.search_catalog( self.CATALOG_WAREHOUSE_ID, mango_query)
        warehouse = [r[self.f['warehouse']] for r in res]
        return warehouse

    def warehouse_type(self, warehouse_name):
        answers = {f"{self.f['warehouse']}":warehouse_name}
        print('==== Consultando el catalogo')
        print('WAREHOUSE_ID =',self.WAREHOUSE_ID)
        print('answers =',answers)
        catalog_record = self.lkf_api.search_catalog_answers(self.WAREHOUSE_ID, answers,  jwt_settings_key='APIKEY_JWT_KEY',**{'limit':1})
        if not catalog_record:
            self.LKFException(f"Warehouse: {warehouse_name}, not found or dont have the correct access, please check with you admin")
        wh_type = catalog_record.get(f"{self.f['warehouse_type']}")
        return wh_type