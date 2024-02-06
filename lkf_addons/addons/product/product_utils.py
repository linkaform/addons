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
        self.f.update( {
            'product_code':'61ef32bcdf0ec2ba73dec33d',
            'product_name':'61ef32bcdf0ec2ba73dec33e',
            'product_category':'61ef32bcdf0ec2ba73dec342',
            'product_type':'61ef32bcdf0ec2ba73dec343',
            'product_recipe':'61ef32bcdf0ec2ba73dec33c',
            }
            )

    def una_funcion_product(self):
        return True
