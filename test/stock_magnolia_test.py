# -*- coding: utf-8 -*-
import time, simplejson
from datetime import datetime, timedelta
from linkaform_api import utils, network, base
from account_settings import *

lkf_obj = base.LKF_Base(settings)
lkm = lkf_obj.lkm
lkf_api = lkf_obj.lkf_api
cr = lkf_obj.cr

CATALOG_WAREHOUSE_LOCATION = lkm.catalog_id('warehouse_locations')
CATALOG_WAREHOUSE_LOCATION_ID = CATALOG_WAREHOUSE_LOCATION.get('id')
CATALOG_WAREHOUSE_LOCATION_OBJ_ID = CATALOG_WAREHOUSE_LOCATION.get('obj_id')

CATALOG_WAREHOUSE_LOCATION_DEST = lkm.catalog_id('warehouse_location_destination')
CATALOG_WAREHOUSE_LOCATION_DEST_ID = CATALOG_WAREHOUSE_LOCATION_DEST.get('id')
CATALOG_WAREHOUSE_LOCATION_DEST_OBJ_ID = CATALOG_WAREHOUSE_LOCATION_DEST.get('obj_id')


CATALOG_PRODUCT_RECIPE = lkm.catalog_id('product_recipe')
CATALOG_PRODUCT_RECIPE_ID = CATALOG_PRODUCT_RECIPE.get('id')
CATALOG_PRODUCT_RECIPE_OBJ_ID = CATALOG_PRODUCT_RECIPE.get('obj_id')

FORM_LAB_INVENTORY_ADJUSTMENT = lkm.form_id('lab_inventory_adjustment','id')

CATALOG_TEAMS = lkm.catalog_id('teams')
CATALOG_TEAMS_ID = CATALOG_TEAMS.get('id')
CATALOG_TEAMS_OBJ_ID = CATALOG_TEAMS.get('obj_id')

FORM_WEEKLY_PRODUCTION_PLAN_LAB = lkm.form_id('weekly_production_plan_lab', 'id')

# Catalogo Warehouse Location Destination no lo encontre entre los xml

CATALOG_LAB_INVENTORY = lkm.catalog_id('lab_inventory')
CATALOG_LAB_INVENTORY_ID = CATALOG_LAB_INVENTORY.get('id')
CATALOG_LAB_INVENTORY_OBJ_ID = CATALOG_LAB_INVENTORY.get('obj_id')

FORM_LAB_WORK_ORDERS = lkm.form_id('lab_workorders_seleccion_de_planta', 'id')
FORM_LAB_INVENTORY_MOVE = lkm.form_id('lab_inventory_move', 'id')
FORM_LAB_INVENTORY_OUT = lkm.form_id('lab_inventory_out_pull', 'id')
FORM_DAILY_PRODUCTION_SHEET = lkm.form_id('lab_production', 'id')
FORM_LAB_MOVE_NEW_PRODUCTION = lkm.form_id('lab_move_new_production', 'id')

CATALOG_MEDIA_LOT = lkm.catalog_id('media_lot')
CATALOG_MEDIA_LOT_ID = CATALOG_MEDIA_LOT.get('id')
CATALOG_MEDIA_LOT_OBJ_ID = CATALOG_MEDIA_LOT.get('obj_id')

CATALOG_EMPLOYEE = lkm.catalog_id('employee')
CATALOG_EMPLOYEE_ID = CATALOG_EMPLOYEE.get('id')
CATALOG_EMPLOYEE_OBJ_ID = CATALOG_EMPLOYEE.get('obj_id')

VARS = {}

class TestStock():

    def test_crea_lab_inventory_adjustment(self):
        global VARS
        metadata = {
            "form_id":FORM_LAB_INVENTORY_ADJUSTMENT,
            "geolocation":[25.6583943,-100.3834899],"start_timestamp":1690262982.602,"end_timestamp":1690263046.524,
            "answers":{
                "6442e4537775ce64ef72dd6a": "todo",
                CATALOG_WAREHOUSE_LOCATION_OBJ_ID: {
                    "6442e4831198daf81456f274": "Lab C",
                    "65ac6fbc070b93e656bd7fbe": "103"
                },
                "644bf7ccfa9830903f087867": [
                    {
                        CATALOG_PRODUCT_RECIPE_OBJ_ID: {
                            "61ef32bcdf0ec2ba73dec33d": "LNAFP",
                            "6205f73281bb36a6f1573358": "S2",
                            "6209705080c17c97320e3382": "Baby Jar",
                            "6205f73281bb36a6f157335b": 10
                        },
                        "ad00000000000000000ad999": "todo",
                        "620a9ee0a449b98114f61d75": 2023,
                        "620a9ee0a449b98114f61d76": 300,
                        "620ad6247a217dbcb888d168": "G1",
                        "620ad6247a217dbcb888d167": 6,
                        "6441d33a153b3521f5b2afcb": "white",
                        "ad00000000000000000ad000": 300
                    },
                    {
                        CATALOG_PRODUCT_RECIPE_OBJ_ID: {
                            "61ef32bcdf0ec2ba73dec33d": "LNAFP",
                            "6205f73281bb36a6f1573358": "S3",
                            "6209705080c17c97320e3382": "Magenta Box",
                            "6205f73281bb36a6f157335b": 30
                        },
                        "ad00000000000000000ad999": "todo",
                        "620a9ee0a449b98114f61d75": 2024,
                        "620a9ee0a449b98114f61d76": 50,
                        "620ad6247a217dbcb888d168": "E8",
                        "620ad6247a217dbcb888d167": 4,
                        "6441d33a153b3521f5b2afcb": "white",
                        "ad00000000000000000ad000": 150
                    }
                ],
                "000000000000000000000111": "2024-05-02 21:00:16"
            },
            "folio":None,
            "properties":{ "device_properties":{"system":"Testing"} }
            ,"geolocation_method":{"method":"HTML5","accuracy":1742.3649855282526}
        }
        res_create =  lkf_api.post_forms_answers(metadata)
        print('res_create',res_create)
        assert res_create['status_code'] == 201
        time.sleep(15)

    def test_crea_weekly_production_plan_lab(self):
        metadata = {
            "form_id": FORM_WEEKLY_PRODUCTION_PLAN_LAB,
            "geolocation": [18.1403648,-97.0817536],"start_timestamp": 1714706899.431,"end_timestamp": 1714707111.066,
            "answers": {
                "61f1da41b112fe4e7fe8582f": 2024,
                "62e4bd2ed9814e169a3f6bef": "execute",
                "61f1fab3ce39f01fe8a7ca8c": [
                    {
                        CATALOG_PRODUCT_RECIPE_OBJ_ID: {
                            "61ef32bcdf0ec2ba73dec33d": "LNAFP",
                            "621fca56ee94313e8d8c5e2e": "S2",
                            "6205f73281bb36a6f1573358": "S2",
                            "63483f8e2c8c769718b102b1": "Main",
                            "6205f73281bb36a6f1573357": 8,
                            "6209705080c17c97320e3382": "Baby Jar",
                            "6205f73281bb36a6f157335b": 10,
                            "61ef32bcdf0ec2ba73dec33e": [
                                "Nandina domestica nana Firepower"
                            ],
                            "6209705080c17c97320e337f": [
                                150
                            ],
                            "6205f73281bb36a6f157335d": []
                        },
                        CATALOG_TEAMS_OBJ_ID: {
                            "62c5ff0162a70c261328845d": "Team 1"
                        },
                        "642dbe5638a8255f77dcdad6": 200
                    },
                    {
                        CATALOG_PRODUCT_RECIPE_OBJ_ID: {
                            "61ef32bcdf0ec2ba73dec33d": "LNAFP",
                            "621fca56ee94313e8d8c5e2e": "S2",
                            "6205f73281bb36a6f1573358": "S3",
                            "63483f8e2c8c769718b102b1": "Main",
                            "6205f73281bb36a6f1573357": 8,
                            "6209705080c17c97320e3382": "Magenta Box",
                            "6205f73281bb36a6f157335b": 30,
                            "61ef32bcdf0ec2ba73dec33e": [
                                "Nandina domestica nana Firepower"
                            ],
                            "6209705080c17c97320e337f": [
                                130
                            ],
                            "6205f73281bb36a6f157335d": []
                        },
                        CATALOG_TEAMS_OBJ_ID: {
                            "62c5ff0162a70c261328845d": "Team 2"
                        },
                        "642dbe5638a8255f77dcdad6": 220
                    }
                ],
                "61f1da41b112fe4e7fe85830": 10
            },
            "folio": None,
            "properties":{ "device_properties":{"system":"Testing"} },
            "geolocation_method": {"method": "HTML5","accuracy": 585833.4094839195}
        }
        res_create =  lkf_api.post_forms_answers(metadata)
        print('res_create',res_create)
        assert res_create['status_code'] == 201
        time.sleep(15)

    def test_crea_workorders_sel_planta(self):
        metadata = {
            "form_id": FORM_LAB_WORK_ORDERS,
            "geolocation": [18.1431011,-97.0821267],"start_timestamp": 1715362749.851,"end_timestamp": 1715365484.552,
            "answers": {
                "6442e4537775ce64ef72dd6a": "to_do",
                CATALOG_PRODUCT_RECIPE_OBJ_ID: {
                    "61ef32bcdf0ec2ba73dec33d": "LNAFP",
                    "61ef32bcdf0ec2ba73dec33e": [
                        "Firepower Nandina",
                        "Firepower' Nandina",
                        "Nandina domestica nana Firepower"
                    ]
                },
                "6442e4537775ce64ef72dd69": [
                    {
                        CATALOG_LAB_INVENTORY_OBJ_ID: {
                            "6205f73281bb36a6f1573358": "S2",
                            "620a9ee0a449b98114f61d76": 300,
                            "6442e4831198daf81456f274": "Lab C",
                            "65ac6fbc070b93e656bd7fbe": "103",
                            "620a9ee0a449b98114f61d77": "202343-6G1",
                            "6441d33a153b3521f5b2afc9": [],
                            "620ad6247a217dbcb888d16f": [],
                            "620ad6247a217dbcb888d170": []
                        },
                        "6319404d1b3cefa880fefcc8": 40,
                        "c24000000000000000000001": 0
                    }
                ],
                CATALOG_WAREHOUSE_LOCATION_DEST_OBJ_ID: {
                    "65bdc71b3e183f49761a33b9": "Team 1",
                    "65c12749cfed7d3a0e1a341b": "Team Leader"
                },
                "63f8e128694361f17f7b59d4": 40,
                "000000000000000000000111": "2024-05-10 11:39:10"
            },
            "folio": None,
            "properties":{ "device_properties":{"system":"Testing"} },
            "geolocation_method": {"method": "HTML5","accuracy": 1286.0279589285738}
        }
        res_create =  lkf_api.post_forms_answers(metadata)
        print('res_create',res_create)
        assert res_create['status_code'] == 201
        time.sleep(15)

    def test_update_daily_production_sheet_v2(self):
        query_daily = {
            'answers.62fbbf2587546d976e05dc7b': 'in_progress',
            f'answers.{CATALOG_PRODUCT_RECIPE_OBJ_ID}.61ef32bcdf0ec2ba73dec33d': 'LNAFP',
            f'answers.{CATALOG_PRODUCT_RECIPE_OBJ_ID}.621fca56ee94313e8d8c5e2e': 'S2',
            f'answers.{CATALOG_PRODUCT_RECIPE_OBJ_ID}.6205f73281bb36a6f1573358': 'S2',
            'answers.61f1da41b112fe4e7fe8582f': 2024,
            'answers.62e8343e236c89c216a7cec3': 10
        }
        record_daily_production = lkf_obj.get_record_from_db(form_id=FORM_DAILY_PRODUCTION_SHEET, query_answers=query_daily, select_columns=['folio','form_id','answers'])
        print('FORM_DAILY_PRODUCTION_SHEET =',FORM_DAILY_PRODUCTION_SHEET)
        print('query_daily =',simplejson.dumps(query_daily, indent=4))
        print('CATALOG_PRODUCT_RECIPE_OBJ_ID =',CATALOG_PRODUCT_RECIPE_OBJ_ID)
        assert record_daily_production != {}
        record_daily_production['answers'].update({
            "aa0000000000000000000001": 30,
            "6441d33a153b3521f5b2afcb": "clean",
            "cc0000000000000000000001": "G3",
            "dd0000000000000000000001": 5,
            CATALOG_MEDIA_LOT_OBJ_ID: {
                "61ef43c226fd42cc223c98f7": "FI III",
                "65b538f49d2b7d901c1671eb": "57 B"
            },
            "62aa0c34c9394a715c9fbd1f": "no",
            "61f1fab3ce39f01fe8a7ca8c": [{
                CATALOG_EMPLOYEE_OBJ_ID: {
                    "62c5ff407febce07043024dd": "Alexia Piche"
                },
                "61f1fcf8c66d2990c8fc7cc2": 10,
                "61f1fcf8c66d2990c8fc7cc3": 20,
                "61f1fcf8c66d2990c8fc7cc4": "2024-05-10",
                "61f1fcf8c66d2990c8fc7cc5": "18:15:00",
                "61f1fcf8c66d2990c8fcccc6": "2024-05-10",
                "61f1fcf8c66d2990c8fc7cc6": "19:15:00",
                "62c6017ff9f71e2a589fb679": "no",
                "62e9890c5dec95745c618fc3": "progress"
            },{
                CATALOG_EMPLOYEE_OBJ_ID: {
                    "62c5ff407febce07043024dd": "Alfonso Reyes"
                },
                "61f1fcf8c66d2990c8fc7cc2": 10,
                "61f1fcf8c66d2990c8fc7cc3": 30,
                "61f1fcf8c66d2990c8fc7cc4": "2024-05-10",
                "61f1fcf8c66d2990c8fc7cc5": "18:45:00",
                "61f1fcf8c66d2990c8fcccc6": "2024-05-10",
                "61f1fcf8c66d2990c8fc7cc6": "20:45:00",
                "62c6017ff9f71e2a589fb679": "no",
                "62e9890c5dec95745c618fc3": "progress"
            }],
            "64ed5839a405d8f6378edf5f": 0,
            "61f1fd95ef44501511f7f161": "next_day",
            "62fbbf2587546d976e05dc7b": "in_progress"
        })
        resp_update = lkf_api.patch_record(record_daily_production)
        print('resp_update',resp_update)
        assert resp_update['status_code'] == 202
        VARS['daily_production'] = {'folio': record_daily_production['folio']}
        time.sleep(30)

    def test_update_inventory_move_new_lot_production(self): # Min. 7
        query_inv_move = {
            'answers.62fc62dfb26856412d2fe4ca': VARS['daily_production']['folio']
        }
        print('*** *** *** query_inv_move=',query_inv_move)
        record_inv_move_new_lot = lkf_obj.get_record_from_db(form_id=FORM_LAB_MOVE_NEW_PRODUCTION, query_answers=query_inv_move, select_columns=['folio','form_id','answers'])
        assert record_inv_move_new_lot != {}
        record_inv_move_new_lot['answers'].update({
            "63193fc51b3cefa880fefcc7": [{
                CATALOG_WAREHOUSE_LOCATION_OBJ_ID: {
                    "6442e4831198daf81456f274": "Lab B",
                    "65ac6fbc070b93e656bd7fbe": "1"
                },
                "c24000000000000000000001": 0,
                "6319404d1b3cefa880fefcc8": 30
            },{
                CATALOG_WAREHOUSE_LOCATION_OBJ_ID: {
                    "6442e4831198daf81456f274": "Lab B",
                    "65ac6fbc070b93e656bd7fbe": "2"
                },
                "c24000000000000000000001": 0,
                "6319404d1b3cefa880fefcc8": 20
            }]
        })
        # print(record_inv_move_new_lot)
        # assert record_inv_move_new_lot.get('folio') == 'asdfasdf'
        time.sleep(90)
        resp_update = lkf_api.patch_record(record_inv_move_new_lot)
        print('resp_update',resp_update)
        assert resp_update['status_code'] == 202
        time.sleep(10)

    def test_lab_inventory_move(self):
        metadata = {
            "form_id": 113822,
            "geolocation": [18.1431011,-97.0821267],"start_timestamp": 1715726240.972,"end_timestamp": 1715726442.227,
            "answers": {
                "6442e4537775ce64ef72dd6a": "to_do",
                CATALOG_LAB_INVENTORY_OBJ_ID: {
                    "6442e4831198daf81456f274": "Team 1",
                    "65ac6fbc070b93e656bd7fbe": "Team Leader",
                    "61ef32bcdf0ec2ba73dec33d": "LNAFP",
                    "620a9ee0a449b98114f61d76": 300,
                    "620a9ee0a449b98114f61d77": "202343-6G1",
                    "61ef32bcdf0ec2ba73dec33e": [
                        "Nandina domestica nana Firepower"
                    ],
                    "6441d33a153b3521f5b2afc9": []
                },
                "6442e4537775ce64ef72dd69": [
                    {
                        CATALOG_WAREHOUSE_LOCATION_DEST_OBJ_ID: {
                            "65bdc71b3e183f49761a33b9": "Lab C",
                            "65c12749cfed7d3a0e1a341b": "103"
                        },
                        "6442e4cc45983bf1778ec17d": 5
                    }
                ],
                "000000000000000000000111": "2024-05-14 16:37:21",
                "6442e4537775ce64ef72dd68": 5
            },
            "folio": None,
            "properties":{ "device_properties":{"system":"Testing"} },
            "geolocation_method": {"method": "HTML5","accuracy": 1286.0279589285738}
        }
        res_create =  lkf_api.post_forms_answers(metadata)
        print('res_create',res_create)
        assert res_create['status_code'] == 201
        time.sleep(10)

    '''
    # Produccion etapa 3
    '''
    def test_crea_workorders_sel_planta__etapa3(self):
        metadata = {
            "form_id": FORM_LAB_WORK_ORDERS,
            "geolocation": [18.1431011,-97.0821267],"start_timestamp": 1715727681.745,"end_timestamp": 1715727801.331,
            "answers": {
                "6442e4537775ce64ef72dd6a": "to_do",
                CATALOG_PRODUCT_RECIPE_OBJ_ID: {
                    "61ef32bcdf0ec2ba73dec33d": "LNAFP",
                    "61ef32bcdf0ec2ba73dec33e": [
                        "Firepower Nandina",
                        "Firepower' Nandina",
                        "Nandina domestica nana Firepower"
                    ]
                },
                "6442e4537775ce64ef72dd69": [
                    {
                        CATALOG_LAB_INVENTORY_OBJ_ID: {
                            "6205f73281bb36a6f1573358": "S3",
                            "620a9ee0a449b98114f61d76": 50,
                            "6442e4831198daf81456f274": "Lab C",
                            "65ac6fbc070b93e656bd7fbe": "103",
                            "620a9ee0a449b98114f61d77": "202408-4E8",
                            "6441d33a153b3521f5b2afc9": [],
                            "620ad6247a217dbcb888d16f": [],
                            "620ad6247a217dbcb888d170": []
                        },
                        "c24000000000000000000001": 0,
                        "6319404d1b3cefa880fefcc8": 50
                    }
                ],
                CATALOG_WAREHOUSE_LOCATION_DEST_OBJ_ID: {
                    "65bdc71b3e183f49761a33b9": "Team 2",
                    "65c12749cfed7d3a0e1a341b": "Team Leader"
                },
                "000000000000000000000111": "2024-05-14 17:01:22",
                "63f8e128694361f17f7b59d4": 50
            },
            "folio": None,
            "properties":{ "device_properties":{"system":"Testing"} },
            "geolocation_method": {"method": "HTML5","accuracy": 1286.0279589285738}
        }
        res_create =  lkf_api.post_forms_answers(metadata)
        print('res_create',res_create)
        assert res_create['status_code'] == 201
        time.sleep(15)

    def test_update_daily_production_sheet_v2__etapa3(self):
        query_daily = {
            'answers.62fbbf2587546d976e05dc7b': 'in_progress',
            f'answers.{CATALOG_PRODUCT_RECIPE_OBJ_ID}.61ef32bcdf0ec2ba73dec33d': 'LNAFP',
            f'answers.{CATALOG_PRODUCT_RECIPE_OBJ_ID}.621fca56ee94313e8d8c5e2e': 'S2',
            f'answers.{CATALOG_PRODUCT_RECIPE_OBJ_ID}.6205f73281bb36a6f1573358': 'S3',
            'answers.61f1da41b112fe4e7fe8582f': 2024,
            'answers.62e8343e236c89c216a7cec3': 10
        }
        record_daily_production = lkf_obj.get_record_from_db(form_id=FORM_DAILY_PRODUCTION_SHEET, query_answers=query_daily, select_columns=['folio','form_id','answers'])
        print('FORM_DAILY_PRODUCTION_SHEET =',FORM_DAILY_PRODUCTION_SHEET)
        print('query_daily =',simplejson.dumps(query_daily, indent=4))
        print('CATALOG_PRODUCT_RECIPE_OBJ_ID =',CATALOG_PRODUCT_RECIPE_OBJ_ID)
        assert record_daily_production != {}
        record_daily_production['answers'].update({
            "aa0000000000000000000001": 30,
            "6441d33a153b3521f5b2afcb": "clean",
            "cc0000000000000000000001": "A2",
            "dd0000000000000000000001": 5,
            CATALOG_MEDIA_LOT_OBJ_ID: {
                "61ef43c226fd42cc223c98f7": "NII PPM",
                "65b538f49d2b7d901c1671eb": "58 B"
            },
            "62aa0c34c9394a715c9fbd1f": "no",
            "61f1fab3ce39f01fe8a7ca8c": [{
                CATALOG_EMPLOYEE_OBJ_ID: {
                    "62c5ff407febce07043024dd": "Lizeth castillo"
                },
                "61f1fcf8c66d2990c8fc7cc2": 10,
                "61f1fcf8c66d2990c8fc7cc3": 15,
                "61f1fcf8c66d2990c8fc7cc4": "2024-05-14",
                "61f1fcf8c66d2990c8fc7cc5": "18:15:00",
                "61f1fcf8c66d2990c8fcccc6": "2024-05-14",
                "61f1fcf8c66d2990c8fc7cc6": "19:15:00",
                "62c6017ff9f71e2a589fb679": "no",
                "62e9890c5dec95745c618fc3": "progress"
            },{
                CATALOG_EMPLOYEE_OBJ_ID: {
                    "62c5ff407febce07043024dd": "Lucy Reyes"
                },
                "61f1fcf8c66d2990c8fc7cc2": 15,
                "61f1fcf8c66d2990c8fc7cc3": 30,
                "61f1fcf8c66d2990c8fc7cc4": "2024-05-14",
                "61f1fcf8c66d2990c8fc7cc5": "18:45:00",
                "61f1fcf8c66d2990c8fcccc6": "2024-05-14",
                "61f1fcf8c66d2990c8fc7cc6": "20:45:00",
                "62c6017ff9f71e2a589fb679": "no",
                "62e9890c5dec95745c618fc3": "progress"
            }],
            "64ed5839a405d8f6378edf5f": 0,
            "61f1fd95ef44501511f7f161": "next_day",
            "62fbbf2587546d976e05dc7b": "in_progress"
        })
        resp_update = lkf_api.patch_record(record_daily_production)
        print('resp_update',resp_update)
        assert resp_update['status_code'] == 202
        VARS['daily_production'] = {'folio': record_daily_production['folio']}
        time.sleep(30)

    def test_update_inventory_move_new_lot_production__etapa3(self): # Min. 7
        query_inv_move = {
            'answers.62fc62dfb26856412d2fe4ca': VARS['daily_production']['folio']
        }
        print('*** *** *** query_inv_move=',query_inv_move)
        record_inv_move_new_lot = lkf_obj.get_record_from_db(form_id=FORM_LAB_MOVE_NEW_PRODUCTION, query_answers=query_inv_move, select_columns=['folio','form_id','answers'])
        assert record_inv_move_new_lot != {}
        record_inv_move_new_lot['answers'].update({
            "63193fc51b3cefa880fefcc7": [{
                CATALOG_WAREHOUSE_LOCATION_OBJ_ID: {
                    "6442e4831198daf81456f274": "Lab B",
                    "65ac6fbc070b93e656bd7fbe": "10"
                },
                "c24000000000000000000001": 0,
                "6319404d1b3cefa880fefcc8": 45
            }]
        })
        # print(record_inv_move_new_lot)
        # assert record_inv_move_new_lot.get('folio') == 'asdfasdf'
        time.sleep(90)
        resp_update = lkf_api.patch_record(record_inv_move_new_lot)
        print('resp_update',resp_update)
        assert resp_update['status_code'] == 202
        time.sleep(10)

    def test_lab_inventory_move__etapa3(self):
        metadata = {
            "form_id": 113822,
            "geolocation": [18.1431011,-97.0821267],"start_timestamp": 1715729975.94,"end_timestamp": 1715730061.339,
            "answers": {
                "6442e4537775ce64ef72dd6a": "to_do",
                CATALOG_LAB_INVENTORY_OBJ_ID: {
                    "6442e4831198daf81456f274": "Team 2",
                    "65ac6fbc070b93e656bd7fbe": "Team Leader",
                    "61ef32bcdf0ec2ba73dec33d": "LNAFP",
                    "620a9ee0a449b98114f61d76": 50,
                    "620a9ee0a449b98114f61d77": "202408-4E8",
                    "61ef32bcdf0ec2ba73dec33e": [
                        "Nandina domestica nana Firepower"
                    ],
                    "6441d33a153b3521f5b2afc9": []
                },
                "6442e4537775ce64ef72dd69": [
                    {
                        CATALOG_WAREHOUSE_LOCATION_DEST_OBJ_ID: {
                            "65bdc71b3e183f49761a33b9": "Lab C",
                            "65c12749cfed7d3a0e1a341b": "103"
                        },
                        "6442e4cc45983bf1778ec17d": 10
                    }
                ],
                "000000000000000000000111": "2024-05-14 17:39:36",
                "6442e4537775ce64ef72dd68": 10
            },
            "folio": None,
            "properties":{ "device_properties":{"system":"Testing"} },
            "geolocation_method": {"method": "HTML5","accuracy": 1286.0279589285738}
        }
        res_create =  lkf_api.post_forms_answers(metadata)
        print('res_create',res_create)
        assert res_create['status_code'] == 201
        time.sleep(15)

    def test_pull_out(self):
        metadata = {
            "form_id": 113820,
            "geolocation": [18.1431011,-97.0821267],"start_timestamp": 1715730497.947,"end_timestamp": 1715730665.414,
            "answers": {
                "6442e4537775ce64ef72dd6a": "to_do",
                CATALOG_PRODUCT_RECIPE_OBJ_ID: {
                    "61ef32bcdf0ec2ba73dec33d": "LNAFP",
                    "61ef32bcdf0ec2ba73dec33e": [
                        "Firepower Nandina",
                        "Firepower' Nandina",
                        "Nandina domestica nana Firepower"
                    ]
                },
                "6442e4537775ce64ef72dd69": [
                    {
                        CATALOG_LAB_INVENTORY_OBJ_ID: {
                            "6442e4831198daf81456f274": "Lab B",
                            "65ac6fbc070b93e656bd7fbe": "10",
                            "620a9ee0a449b98114f61d76": 135,
                            "620a9ee0a449b98114f61d77": "202420-5A2",
                            "6441d33a153b3521f5b2afc9": [
                                45
                            ],
                            "620ad6247a217dbcb888d16f": [],
                            "620ad6247a217dbcb888d170": []
                        },
                        "6442e4537775ce64ef72dd68": 10
                    }
                ],
                "000000000000000000000111": "2024-05-14 17:48:18",
                "63f8e128694361f17f7b59d4": 10
            },
            "folio": None,
            "properties":{ "device_properties":{"system":"Testing"} },
            "geolocation_method": {"method": "HTML5","accuracy": 1286.0279589285738}
        }
        res_create =  lkf_api.post_forms_answers(metadata)
        print('res_create',res_create)
        assert res_create['status_code'] == 201
        time.sleep(15)

    def test_pull_out__all(self):
        metadata = {
            "form_id": 113820,"geolocation": [18.1431011,-97.0821267],"start_timestamp": 1715731945.22,"end_timestamp": 1715732193.035,
            "answers": {
                "6442e4537775ce64ef72dd6a": "to_do",
                CATALOG_PRODUCT_RECIPE_OBJ_ID: {
                    "61ef32bcdf0ec2ba73dec33d": "LNAFP",
                    "61ef32bcdf0ec2ba73dec33e": [
                        "Firepower Nandina",
                        "Firepower' Nandina",
                        "Nandina domestica nana Firepower"
                    ]
                },
                "6442e4537775ce64ef72dd69": [
                    {
                        CATALOG_LAB_INVENTORY_OBJ_ID: {
                            "6442e4831198daf81456f274": "Lab B",
                            "65ac6fbc070b93e656bd7fbe": "10",
                            "620a9ee0a449b98114f61d76": 135,
                            "620a9ee0a449b98114f61d77": "202420-5A2",
                            "6441d33a153b3521f5b2afc9": [
                                45
                            ],
                            "620ad6247a217dbcb888d16f": [],
                            "620ad6247a217dbcb888d170": []
                        },
                        "6442e4537775ce64ef72dd68": 35
                    }
                ],
                "000000000000000000000111": "2024-05-14 21:12:25",
                "63f8e128694361f17f7b59d4": 35
            },
            "folio": None,
            "properties":{ "device_properties":{"system":"Testing"} },
            "geolocation_method": {"method": "HTML5","accuracy": 1286.0279589285738}
        }
        res_create =  lkf_api.post_forms_answers(metadata)
        print('res_create',res_create)
        assert res_create['status_code'] == 201