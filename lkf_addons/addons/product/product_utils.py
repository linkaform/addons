# -*- coding: utf-8 -*-

from linkaform_api import base


class Product(base.LKF_Base):

    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False):
        # base.LKF_Base.__init__(self, settings, sys_argv=sys_argv)
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api)
        self.name =  __class__.__name__
        self.settings = settings

        self.PRODUCT = self.lkm.catalog_id('product_catalog')
        self.PRODUCT_ID = self.PRODUCT.get('id')
        self.PRODUCT_OBJ_ID = self.PRODUCT.get('obj_id')

        self.PRODUCT_RECIPE = self.lkm.catalog_id('product_recipe')
        self.PRODUCT_RECIPE_ID = self.PRODUCT_RECIPE.get('id')
        self.PRODUCT_RECIPE_OBJ_ID = self.PRODUCT_RECIPE.get('obj_id')

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
            'product_code':'61ef32bcdf0ec2ba73dec33d',
            'product_name':'61ef32bcdf0ec2ba73dec33e',
            'product_category':'61ef32bcdf0ec2ba73dec342',
            'product_type':'61ef32bcdf0ec2ba73dec343',
            'product_recipe':'61ef32bcdf0ec2ba73dec33c',
            'warehouse':'6442e4831198daf81456f274',
            'warehouse_dest':'65bdc71b3e183f49761a33b9',
            'warehouse_location':'65ac6fbc070b93e656bd7fbe',
            'warehouse_location_dest':'65c12749cfed7d3a0e1a341b',
            'warehouse_type':'6514f51b6cfe23860299abfa',
            'warehouse_type_dest':'65bdc74a9c6a5b1adf424b5b',
            }
            )

    def una_funcion_product(self):
        return True
