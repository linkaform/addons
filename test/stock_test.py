# -*- coding: utf-8 -*-
import time, simplejson
from datetime import datetime, timedelta
from linkaform_api import utils, network, base
from account_settings import *

lkf_obj = base.LKF_Base(settings)
lkm = lkf_obj.lkm
lkf_api = lkf_obj.lkf_api
VARS = {}

FORM_RECEPCION_MATERIALES = lkm.form_id('recepcion_de_materiales_de_proveedor','id')
FORM_INVENTORY_ADJUSTMENT = lkm.form_id('stock_inventory_adjustment','id')
FORM_MOVE_ONE_MANY_ONE = lkm.form_id('stock_move_one_many_one','id')

CATALOG_WAREHOUSE_LOCATION = lkm.catalog_id('warehouse_locations')
CATALOG_WAREHOUSE_LOCATION_OBJ_ID = CATALOG_WAREHOUSE_LOCATION.get('obj_id')

CATALOG_WAREHOUSE_LOCATION_DEST = lkm.catalog_id('warehouse_location_destination')
CATALOG_WAREHOUSE_LOCATION_DEST_OBJ_ID = CATALOG_WAREHOUSE_LOCATION_DEST.get('obj_id')

CATALOG_STOCK_INVENTORY = lkm.catalog_id('stock_inventory')
CATALOG_STOCK_INVENTORY_OBJ_ID = CATALOG_STOCK_INVENTORY.get('obj_id')

CATALOG_SKU = lkm.catalog_id('sku_catalog')
CATALOG_SKU_OBJ_ID = CATALOG_SKU.get('obj_id')

fecha = datetime.now()
fecha_salida = fecha + timedelta(days=1)
fecha = fecha.strftime('%Y-%m-%d')
fecha_salida = fecha_salida.strftime('%Y-%m-%d')

class TestStocks():
    def test_crea_recepcion_materiales(self):
        metadata = {
            "form_id": FORM_RECEPCION_MATERIALES,"geolocation": [],"start_timestamp": 1715787608.475,"end_timestamp": 1715788138.316,
            "answers": {
                CATALOG_WAREHOUSE_LOCATION_OBJ_ID: {
                    "6442e4831198daf81456f274": "Proveedores",
                    "65ac6fbc070b93e656bd7fbe": "Proveedor de Piezas"
                },
                CATALOG_WAREHOUSE_LOCATION_DEST_OBJ_ID: {
                    "65bdc71b3e183f49761a33b9": "Almacen Central",
                    "65c12749cfed7d3a0e1a341b": "Refacciones Mantenimiento"
                },
                "6442e4537775ce64ef72dd69": [
                    {
                        CATALOG_SKU_OBJ_ID: {
                            "61ef32bcdf0ec2ba73dec33d": "MM-C14",
                            "65dec64a3199f9a040829243": "MM-C14-10M",
                            "61ef32bcdf0ec2ba73dec33e": [
                                "Manguera 1/4"
                            ],
                            "6205f73281bb36a6f157335b": [
                                1
                            ]
                        },
                        "620a9ee0a449b98114f61d77": "L001",
                        "ad00000000000000000ad999": "todo",
                        "6442e4cc45983bf1778ec17d": 20,
                    }
                ],
                "6442e4537775ce64ef72dd6a": "to_do",
                "000000000000000000000111": fecha
            },
            "folio":None,"properties":{ "device_properties":{"system":"Testing"} }
        }
        res_create =  lkf_api.post_forms_answers(metadata)
        print('res_create',res_create)
        assert res_create['status_code'] == 201
        time.sleep(15)
    
    def test_create_inventory_adjustment(self):
        metadata = {
            "form_id": FORM_INVENTORY_ADJUSTMENT,"geolocation": [],"start_timestamp": 1715787608.475,"end_timestamp": 1715788138.316,
            "answers": {
                "6442e4537775ce64ef72dd6a": "todo",
                CATALOG_WAREHOUSE_LOCATION_OBJ_ID: {
                    "6442e4831198daf81456f274": "Almacen Central",
                    "65ac6fbc070b93e656bd7fbe": "Refacciones Mantenimiento"
                },
                "644bf7ccfa9830903f087867": [
                    {
                        CATALOG_SKU_OBJ_ID: {
                            "61ef32bcdf0ec2ba73dec33d": "MM-C14",
                            "65dec64a3199f9a040829243": "MM-C14-10M",
                            "61ef32bcdf0ec2ba73dec33e": [
                                "Manguera 1/4"
                            ],
                            "6205f73281bb36a6f1573358": [
                                "S1"
                            ],
                            "621fca56ee94313e8d8c5e2e": [
                                "Negro"
                            ]
                        },
                        "ad00000000000000000ad999": "todo",
                        "620a9ee0a449b98114f61d77": "L1",
                        "ad00000000000000000ad000": 20,
                        "ad00000000000000000ad100": 20
                    }
                ],
                "000000000000000000000111": f"{fecha} 21:29:30"
            },
            "folio":None,"properties":{ "device_properties":{"system":"Testing"} }
        }
        res_create =  lkf_api.post_forms_answers(metadata)
        print('res_create',res_create)
        assert res_create['status_code'] == 201
        time.sleep(15)

    def test_create_salida_multi_a_una_ubicacion(self):
        metadata = {
            "form_id": FORM_MOVE_ONE_MANY_ONE,"geolocation": [],"start_timestamp": 1715787608.475,"end_timestamp": 1715788138.316,
            "answers": {
                CATALOG_WAREHOUSE_LOCATION_OBJ_ID: {
                    "6442e4831198daf81456f274": "Almacen Central",
                    "65ac6fbc070b93e656bd7fbe": "Refacciones Mantenimiento"
                },
                CATALOG_WAREHOUSE_LOCATION_DEST_OBJ_ID: {
                    "65bdc71b3e183f49761a33b9": "Produccion",
                    "65c12749cfed7d3a0e1a341b": "Maquina Blanca"
                },
                "6442e4537775ce64ef72dd69": [
                    {
                        CATALOG_STOCK_INVENTORY_OBJ_ID: {
                            "61ef32bcdf0ec2ba73dec33d": "MM-C14",
                            "65dec64a3199f9a040829243": "MM-C14-10M",
                            "620a9ee0a449b98114f61d77": "L1",
                            "61ef32bcdf0ec2ba73dec33e": [
                                "Manguera 1/4"
                            ],
                            "6441d33a153b3521f5b2afc9": [
                                20
                            ],
                            "621fca56ee94313e8d8c5e2e": [],
                            "621fc992a7ebfd603a8c5e2e": [],
                            "6205f73281bb36a6f1573358": [],
                            "61ef32bcdf0ec2ba73dec342": [],
                            "6205f73281bb36a6f157335b": [
                                1
                            ],
                            "6209705080c17c97320e3382": [],
                            "61ef32bcdf0ec2ba73dec343": []
                        },
                        "65e1169689c0e0790f8843f1": 5,
                        "6442e4cc45983bf1778ec17d": 5
                    }
                ],
                "000000000000000000000111": fecha_salida,
                "6442e4537775ce64ef72dd6a": "to_do"
            },
            "folio":None,"properties":{ "device_properties":{"system":"Testing"} }
        }
        res_create =  lkf_api.post_forms_answers(metadata)
        print('res_create',res_create)
        assert res_create['status_code'] == 201
        time.sleep(15)