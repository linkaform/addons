# -*- coding: utf-8 -*-

from datetime import timedelta, datetime
import math, simplejson, time
from copy import deepcopy

from linkaform_api import base

print('Cargando Stock..')

class Stock(base.LKF_Base):

    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False):
        #base.LKF_Base.__init__(self, settings, sys_argv=sys_argv, use_api=use_api)
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api)
        self.name =  __class__.__name__
        self.settings = settings
        
        self.CATALOG_WAREHOUSE = self.lkm.catalog_id('warehouse')
        self.CATALOG_WAREHOUSE_ID = self.CATALOG_WAREHOUSE.get('id')
        self.CATALOG_WAREHOUSE_OBJ_ID = self.CATALOG_WAREHOUSE.get('obj_id')

        self.CATALOG_INVENTORY = self.lkm.catalog_id('green_house_inventory')
        self.CATALOG_INVENTORY_ID = self.CATALOG_INVENTORY.get('id')
        self.CATALOG_INVENTORY_OBJ_ID = self.CATALOG_INVENTORY.get('obj_id')

        self.CATALOG_PRODUCT_RECIPE = self.lkm.catalog_id('plant_recipe')
        self.CATALOG_PRODUCT_RECIPE_OBJ_ID = self.CATALOG_PRODUCT_RECIPE.get('obj_id')
        self.CATALOG_PRODUCT_RECIPE_ID = self.CATALOG_PRODUCT_RECIPE.get('id')
        
        self.CATALOG_PRODUCT = self.lkm.catalog_id('plant_catalog')
        self.CATALOG_PRODUCT_OBJ_ID = self.CATALOG_PRODUCT.get('obj_id')
        self.CATALOG_PRODUCT_ID = self.CATALOG_PRODUCT.get('id')

        self.FORM_INVENTORY_ID = self.lkm.form_id('green_house_inventroy','id')
        self.PRODUCTION_FORM_ID = self.lkm.form_id('greenhouse_production','id')
        self.STOCK_MOVE_FORM_ID = self.lkm.form_id('green_house_inventory_move','id')
        self.SCRAP_FORM_ID = self.lkm.form_id('green_house_scrapping','id')
        self.GRADING_FORM_ID = self.lkm.form_id('green_house_grading','id')
        self.ADJUIST_FORM_ID = self.lkm.form_id('green_house_inventory_adjustment','id')
        self.GREENHOUSE_GRADING_ID = self.lkm.form_id('green_house_grading','id')


        self.FORM_CATALOG_DIR = {
            81503:80755, #Inventory Flow (lab): Catalog Invetory Lab #TODO
            self.FORM_INVENTORY_ID:self.CATALOG_INVENTORY_ID, #Inventory Flow (greenHouse)
            }
        # self.CATALOG_SOL_VIAJE_ID = self.CATALOG_SOL_VIAJE.get('id')
        # self.CATALOG_SOL_VIAJE_OBJ_ID = self.CATALOG_SOL_VIAJE.get('obj_id')
        # self.FORM_ID_SOLICITUD = self.lkm.form_id('solicitud_de_viticos','id')

        self.SOL_METADATA = {}
        self.SOL_CATALOG = {}
        # self.f stands for field 
        # self.f is use to realte a human name to a objectId where the ObjectId
        # ex: self.f = {'key':'ObjectId'}

        self.f = {
            #'warehouse_catalog_obj_id':'6442e4831198daf81456f273',
            'warehouse_type':'6514f51b6cfe23860299abfa',
            'warehouse':'6442e4831198daf81456f274',
            'product_recipe':'61ef32bcdf0ec2ba73dec33c',
            'product_code':'61ef32bcdf0ec2ba73dec33d',
            'product_name':'61ef32bcdf0ec2ba73dec33e',
            'product_estimated_ready_date':'6442e25f13879061894b4bb1',
            'product_lot_created_week':'620a9ee0a449b98114f61d75',
            'product_growth_week':'645576e878f3060d1f7fc61b',
            'product_grading_pending':'644c36f1d20db114694a495a',
            'product_container_type':'6441d33a153b3521f5b2afcb',
            'product_lot':'620a9ee0a449b98114f61d77',
            'product_lot_produced':'6271dc35e84e2577579eafeb',
            'product_lot_move_in':'620ad6247a217dbcb888d000',
            'product_lot_scrapped':'620ad6247a217dbcb888d16d',
            'product_lot_move_out':'620ad6247a217dbcb888d17e',
            'product_lot_sales':'6442e2fbc0dd855fe856f1da',
            'product_lot_cuarentin':'6442e2fbc0dd855fe856fddd',
            'product_lot_actuals':'6441d33a153b3521f5b2afc9',
            'product_lot_adjustments':'aaaaa0000000000000000000',
            'production':'6271dc35e84e2577579eafeb',
            'scrap_perc':'6442e25f13879061894b4bb3',
            'scrapped':'620ad6247a217dbcb888d16d',
            'move_in':'620ad6247a217dbcb888d000',
            'move_out':'620ad6247a217dbcb888d17e',
            'sales':'6442e2fbc0dd855fe856f1da',
            'status':'620ad6247a217dbcb888d175',
            'cuarentin':'6442e2fbc0dd855fe856fddd',
            'actuals':'6441d33a153b3521f5b2afc9',
            'adjustments':'aaaaa0000000000000000000',
            'product_lot_per_scrap':'6442e25f13879061894b4bb3',
            'product_lot_proyected_qty':'6442e25f13879061894b4bb2',
            'product_lot_location':'63c9f28ddaebf7e9b4522551',
            'inventory_status':'620ad6247a217dbcb888d175',
            'prod_qty_per_container':'6205f73281bb36a6f157335b',
            'production_lote':'63f8f4cad090912501be306a',
            'production_year':'61f1da41b112fe4e7fe8582f',
            'production_week':'62e8343e236c89c216a7cec3',
            'production_group':'61f1fab3ce39f01fe8a7ca8c',
            'production_status':'62e9890c5dec95745c618fc3',
            'time_in':'61f1fcf8c66d2990c8fc7cc5',
            'time_out':'61f1fcf8c66d2990c8fc7cc6',
            'worker_obj_id':'62c5ff243c63280985580087',
            'worker_name':'62c5ff407febce07043024dd',
            'set_lunch_brake':'62c6017ff9f71e2a589fb679',
            'set_total_produced':'61f1fcf8c66d2990c8fc7cc3',
            'set_total_hours':'61f1fcf8c66d2990c8fc7cc7',
            'set_products_per_hours':'61f1fcf8c66d2990c8fc7cc9',
            'set_production_date':'61f1fcf8c66d2990c8fc7cc4',
            'total_produced':'64ed5839a405d8f6378edf5f',
            'reicpe_growth_weeks':'6205f73281bb36a6f1573357',
            'reicpe_productiviy':'6209705080c17c97320e337f',
            'reicpe_container':'6209705080c17c97320e3382',
            'reicpe_per_container':'6205f73281bb36a6f157335b',
            'reicpe_mult_rate':'6205f73281bb36a6f157334d',
            'reicpe_overage':'6205f73281bb36a6f1573353',
            'reicpe_start_week':'6209705080c17c97320e3380',
            'reicpe_end_week':'6209705080c17c97320e3381',
            'reicpe_start_size':'6205f73281bb36a6f1573358',
            'reicpe_stage':'621fca56ee94313e8d8c5e2e',
            'reicpe_soil_type':'6209705080c17c97320e3383',
            'recipe_type':'63483f8e2c8c769718b102b1',
            'cat_stock_folio':'62c44f96dae331e750428732',
            'grading_group':'644bf7ccfa9830903f087867',
            'grading_move_type':'64d5550ec4909ab3c20c5806',
            'grading_ready_year':'644bf9a04b1761305b080012',
            'grading_ready_week':'644bf9a04b1761305b080011',
            'grading_ready_yearweek':'64edf8aeffeaaa1febca2a06',
            'grading_flats':'644bf9a04b1761305b080013',
            'grading_date':'000000000000000000000111',
            'grading_type':'653885f30d80af8e8de0fe79',
            'move_dest_folio':'ffff00000000000000000001',
            'move_group':'6442e4537775ce64ef72dd69',
            'move_new_location':'644897497a16141f4e5ee0c3',
            'move_group_qty':'6442e4cc45983bf1778ec17d',
            'inv_group':'644bf504f595b744814a4990',
            'inv_group_readyweek':'644bf6c2d281661b082b6348',
            'inv_group_flats':'644bf6c2d281661b082b6349',
            'inv_adjust_status':'6442e4537775ce64ef72dd6a',
            'inv_adjust_grp_status':'ad00000000000000000ad999',
            'inv_adjust_grp_qty':'ad00000000000000000ad000',
            'inv_adjust_grp_in':'ad00000000000000000ad100',
            'inv_adjust_grp_out':'ad00000000000000000ad200',
            'inv_adjust_comments':'64d05792c373f9b62f539d00',
            'inv_adjust_grp_comments':'ad00000000000000000ad400',
            'inv_scrap_status':'644c1cb6dc502afa06c4423e',
            'inv_scrap_qty':'644bf9a04b1761305b080099',
            'inv_cuarentin_qty':'644bf9a04b1761305b080098',
            'inv_move_qty':'6442e4537775ce64ef72dd68',
        }

    def add_dicts(self, dict1, dict2):
        for key in dict1:
            dict1[key] += dict2.get(key,0)
        return dict1

    def do_scrap(self, record):
        answers = record.get('answers')
        scrap_qty = answers.get(self.f['inv_scrap_qty'], 0)
        cuarentin_qty = answers.get(self.f['inv_cuarentin_qty'], 0)
        product_info = answers.get(self.CATALOG_INVENTORY_OBJ_ID,{})
        folio_inventory = product_info.get(self.f['cat_stock_folio'])
        product_code = product_info.get(self.f['product_code'])
        warehouse = product_info.get(self.f['warehouse'])
        product_lot = product_info.get(self.f['product_lot'])
        stock_record = self.get_inventory_record_by_folio(folio_inventory, self.FORM_INVENTORY_ID)
        actuals = stock_record.get('answers',{}).get(self.f['product_lot_actuals'])
        if scrap_qty or cuarentin_qty:
            self.cache_set({
                        '_id': f'{product_code}_{product_lot}_{warehouse}',
                        'scrapped':scrap_qty,
                        'cuarentin':cuarentin_qty,
                        'product_lot':product_lot,
                        'product_code':product_code,
                        'warehouse': warehouse
                        })
        move_qty = scrap_qty + cuarentin_qty
        if move_qty > actuals:
            msg = f"You are trying to move {move_qty} units, and on the stock there is only {actuals}, please check you numbers"
            msg_error_app = {
                    f"{self.f['inv_scrap_qty']}": {
                        "msg": [msg],
                        "label": "Please check your lot inventory",
                        "error":[]
      
                    }
                }
            raise Exception( simplejson.dumps( msg_error_app ) )  
        return self.update_calc_fields(product_code, warehouse, product_lot, folio=folio_inventory)

    def calc_actuals(self, stock):
        stock_in  = stock.get('production', 0 ) + stock.get('move_in')
        stock_out  = stock.get('move_out', 0 ) + stock.get('sales') + stock.get('scrapped') + stock.get('cuarentin')
        actuals = stock_in - stock_out + stock.get('adjustments')
        return actuals

    def calculates_production_warehouse(self):
        current_record = self.current_record
        if not current_record.get('answers'):
            print('el registro es borrado.....')
        planting_house = current_record['answers'].get(self.CATALOG_WAREHOUSE_OBJ_ID, {}).get(self.f['warehouse'])
        plant_info = current_record['answers'].get(self.f['product_recipe'], {})
        plant_code = plant_info.get(self.f['product_code'])
        lot_number = current_record['answers'].get(self.f['production_lote'], {})

        new_production = {}
        recipes = None

        recipes = self.get_plant_recipe([plant_code,], stage=[4, 'Ln72',])
        week = current_record['answers'].get(self.f['production_week'])
        year = current_record['answers'].get(self.f['production_year'])
        if not week or not year:
            return []
        production_date = time.strptime('{} {} 1'.format(year, week), '%Y %W %w')
        production_date = datetime.fromtimestamp(time.mktime(production_date))
        recipe = self.select_S4_recipe(recipes[plant_code], week)
        grow_weeks = recipe.get('S4_growth_weeks')
        ready_date = production_date + timedelta(weeks=grow_weeks)
        lot_number = int(ready_date.strftime('%Y%W'))

        total_produced =0
        #64ed5839a405d8f6378edf5f
        force_lot = False
        for production in current_record['answers'].get(self.f['production_group'], []):
            production_status = production.get(self.f['production_status'],'progress')
            if production_status == 'progress':
                force_lot = True

            total_hours = self.calc_work_hours(production)
            production[self.f['set_total_hours']] = round(total_hours, 2)

            total_produced += production[self.f['set_total_produced']]
            if production_status == 'progress':
                containers_out = production[self.f['set_total_produced']]
            else:
                containers_out = 0



          
            qty_per_container = recipes.get(self.f['prod_qty_per_container'], [])
            if qty_per_container:
                if type(qty_per_container) == list and qty_per_container[0]:
                    qty_per_container = int( qty_per_container[0] )
                else:
                    qty_per_container = int(qty_per_container)
            else:
                qty_per_container = 0 

            container_type = None
            if qty_per_container:
                container_type = 'ln{}'.format(qty_per_container)
            

            #equivalent units
            total_eu = 1 * containers_out 
            flats_per_hour = total_eu / float(total_hours)



            production[self.f['set_products_per_hours']] = round(flats_per_hour, 2) # Plants per Hour
            production[self.f['production_status']] = 'posted'
            plant_date = production[self.f['set_production_date']]
            plant_date = datetime.strptime(plant_date, '%Y-%m-%d')


            production[self.f['product_lot']] = lot_number
            plan_defults = {
                'qty':0,
                'plant_date':plant_date, 
                'qty_per_container':qty_per_container,
                'container_type':container_type,
                'recipe':recipe}
            new_production[lot_number] = new_production.get(lot_number, plan_defults)
            new_production[lot_number]['qty'] += containers_out

        res = []
        self.current_record['answers'][self.f['total_produced']] = total_produced
        for lot_number, plant_data in new_production.items():
            res.append(self.calculates_inventory_greenhouse(plant_info, planting_house, lot_number, plant_data, grow_weeks, force_lot=force_lot))
        return res

    def calculates_inventory_greenhouse(self, plant_info, warehouse, ready_date, plant_data, grow_weeks, force_lot=False ):
        #plant_data is an object with the following keys 'qty','recipe', 'planted_date'
        plant_code = plant_info[self.f['product_code']]
        greenhouse_inventory = self.get_record_greenhouse_inventory(ready_date, warehouse, plant_code)

        plant_yearWeek = plant_data.get('plant_date').strftime('%Y%W')
        qty_produced = plant_data.get('qty',0)
        container_type = plant_data.get('container_type')
        qty_per_container = plant_data.get('qty_per_container')
        S4_overage = plant_data.get('recipe').get('S4_overage', 0)
        qty_proyected = math.floor(qty_produced * (1 - S4_overage))
        if not greenhouse_inventory:

            answers_to_record = {
                self.f['product_lot_produced']: qty_produced,
                self.f['product_estimated_ready_date']: ready_date, # Estimated Ready Week
                self.f['product_lot']: ready_date,
                #'620ad6247a217dbcb888d170': qty_per_container,
                self.f['product_lot_actuals']: qty_produced, # Containers on hand
                self.f['product_lot_proyected_qty']: qty_proyected , # Proyected Containers on hand
                self.f['product_lot_created_week']: int(plant_yearWeek),
                self.f['product_recipe']: plant_info,
                self.f['product_growth_week']: grow_weeks,
                self.CATALOG_WAREHOUSE_OBJ_ID: {self.f['warehouse']:warehouse},
                self.f['inventory_status']: 'active',
                self.f['product_grading_pending']: 'grading_pending'
            }
            if container_type:
                answers_to_record.update({self.f['product_container_type']:container_type})
            metadata = self.lkf_api.get_metadata(self.FORM_INVENTORY_ID)
            if force_lot:
                #metadata['kwargs'] = {'production':qty_produced}
                self.cache_set({
                    '_id': f'{plant_code}_{ready_date}_{warehouse}',
                    'production':qty_produced,
                    'product_lot':ready_date,
                    'product_code':plant_code,
                    'warehouse': warehouse
                    })
            metadata.update({
                'properties': {
                    "device_properties":{
                        "system": "Script",
                        "process": 'GreenHouse Inventory',
                        "action": 'Upsert Inventory GreenHouse',
                        "from_folio": self.current_record.get('folio',''),
                        "archive": "calculates_production_greenhouse.py"
                    }
                },
                'answers': answers_to_record
            })

            resp_create = self.lkf_api.post_forms_answers(metadata, jwt_settings_key='APIKEY_JWT_KEY')
            return resp_create
        new_qty_produced = qty_produced + greenhouse_inventory['answers'].get(self.f['product_lot_produced'], 0)
        new_qty_proyected = qty_proyected + greenhouse_inventory['answers'].get(self.f['product_lot_proyected_qty'], 0)
        new_qty_flats = qty_produced + greenhouse_inventory['answers'].get(self.f['product_lot_actuals'], 0)
        
        greenhouse_inventory['answers'][self.f['product_lot_produced']] = new_qty_produced
        greenhouse_inventory['answers'][self.f['product_lot_proyected_qty']] = new_qty_proyected
        greenhouse_inventory['answers'][self.f['product_lot_actuals']] = new_qty_flats
        if force_lot:
            self.cache_set({
                '_id': f'{plant_code}_{ready_date}_{warehouse}',
                'production':qty_produced,
                'product_lot':ready_date,
                'product_code':plant_code,
                'warehouse': warehouse
                })
            #greenhouse_inventory['properties'] = {'kwargs':{'production':qty_produced}}
            #greenhouse_inventory['kwargs'] = {'production':qty_produced}
        resp_update = self.lkf_api.patch_record(greenhouse_inventory, jwt_settings_key='APIKEY_JWT_KEY')
        return resp_update

    def calc_work_hours(self, data):
        time_in = data.get(self.f['time_in'])
        time_out = data.get(self.f['time_out'])
        cutter = data.get(self.f['worker_obj_id'],{}).get(self.f['worker_name'])
        d_time_in = datetime.strptime(time_in, '%H:%M:%S')
        d_time_out = datetime.strptime(time_out, '%H:%M:%S')
        secs = (d_time_out - d_time_in).total_seconds()
        if secs < 0:
            msg = "The time in and time out for the production set of the cutter: {}, is wrong.".format(cutter)
            msg += " It was capture that see started at {} and finished at {}, having a difference of {} seconds.".format(time_in,
                time_out, secs)
            msg_error_app = {
                     self.f['time_in']: {"msg": [msg], "label": "Please time in. ", "error": []},
                     self.f['time_out']: {"msg": [msg], "label": "Please time out. ", "error": []},
                 }
            raise Exception( simplejson.dumps( msg_error_app ) )

        total_hours = secs / 60.0**2
        lunch_brake = data.get(self.f['set_lunch_brake'])
        if lunch_brake == 'sí' or lunch_brake == 'yes':
            total_hours -= 0.5

        if total_hours <= 0:
            t_in = d_time_in.strftime('%H:%M')
            t_out = d_time_out.strftime('%H:%M')
            msg = "Double check your time in {} and time out {} input, of {}.".format(t_in, t_out, cutter)
            msg_error_app = {
                     self.f['time_in']: {"msg": [msg], "label": "Please check your Time In. Was there a lunch brake? ", "error": []},
                     self.f['time_out']: {"msg": [msg], "label": "Please check your Time Out. Was there a lunch brake?", "error": []}
                 }
            raise Exception( simplejson.dumps( msg_error_app ) )
        return total_hours

    def date_2_str(self, value):
        res=None
        try:
            res = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                res = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
            except ValueError:
                res = datetime.strptime(value, '%Y-%m-%d')
        return res

    def del_catalog_record(self, record_catalog, form_id):
        if record_catalog:
            for info_record_catalog in record_catalog:
                resp_delete = self.lkf_api.delete_catalog_record(
                    self.FORM_CATALOG_DIR[form_id], 
                    info_record_catalog.get('_id'), 
                    info_record_catalog.get('_rev'), 
                    jwt_settings_key='APIKEY_JWT_KEY')
                return resp_delete

    def get_folios_match(self, inc_folio=None, exclude_folio=None):
        if inc_folio and exclude_folio:
            query = {"$and":[
                {"folio": self.list_str_match(inc_folio)},
                {"folio": self.list_str_not_match(inc_folio)},
                ]}
        elif inc_folio and not exclude_folio:
            query = {"folio": self.list_str_match(inc_folio)}
        elif not inc_folio and exclude_folio:
            query = {"folio": self.list_str_not_match(inc_folio)}
        else:
            raise Exception('No folio providen for query')
        return query

    def get_grading(self, folio, answers):
        match_query ={ 
         'form_id': self.GREENHOUSE_GRADING_ID,  
         'deleted_at' : {'$exists':False},
         f'answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f["cat_stock_folio"]}': folio
         } 
        query = [
            {'$match': match_query},
            {'$unwind':f'$answers.{self.f["grading_group"]}'},
            {'$match':{f'answers.{self.f["grading_group"]}.{self.f["grading_move_type"]}':'grading'}},
            {'$project':{
                '_id':0,
                'date':f'$answers.{self.f["grading_date"]}',
                'ready_yearweek':f'$answers.{self.f["grading_group"]}.{self.f["inv_group_readyweek"]}',
                'flats':f'$answers.{self.f["grading_group"]}.{self.f["grading_flats"]}',
            }},
            {'$sort':{'date':1}},
            {'$group':{
                '_id':{
                    'date':'$date',
                    'ready_yearweek':'$ready_yearweek'
                },
                'flats':{'$first':'$flats'}
            }},
            {'$project':{
            '_id':0,
            self.f['inv_group_readyweek']:'$_id.ready_yearweek',
            self.f['inv_group_flats']:'$flats',
            }}

        ]
        
        #print('query=',simplejson.dumps(query, indent=5))
        res = self.cr.aggregate(query)
        return [r for r in res]

    def get_plant_recipe(self, all_codes, stage=[2,3,4], recipe_type='Main'):
        if type(all_codes) == str and all_codes:
            all_codes = [all_codes.upper(),]
        recipe = {}
        recipe_s2 = []
        recipe_s3 = []
        recipe_s4 = []
        if 2 in stage:
            mango_query = self.plant_recipe_query(all_codes, "S2", "S2", recipe_type)
            recipe_s2 = self.lkf_api.search_catalog(self.CATALOG_PRODUCT_RECIPE_ID, mango_query)
        if 3 in stage:
            mango_query = self.plant_recipe_query(all_codes, "S3", "S2", recipe_type)
            recipe_s3 = self.lkf_api.search_catalog(self.CATALOG_PRODUCT_RECIPE_ID, mango_query)
        if 4 in stage:
            if 'Ln72' in stage:
                mango_query = self.plant_recipe_query(all_codes, "Ln72", "S4", recipe_type)
            else:
                mango_query = self.plant_recipe_query(all_codes, "S4", "S3", recipe_type)
            recipe_s4 = self.lkf_api.search_catalog(self.CATALOG_PRODUCT_RECIPE_ID, mango_query, jwt_settings_key='APIKEY_JWT_KEY')
        if recipe_s2 and not recipe:
            for this_recipe in recipe_s2:
                plant_code = this_recipe.get(self.f['product_code'])
                if not recipe.get(plant_code):
                    recipe[plant_code] = {}
                recipe[plant_code].update({
                    'S2_growth_weeks':this_recipe.get(self.f['reicpe_growth_weeks']),
                    'cut_productivity':this_recipe.get(self.f['reicpe_productiviy']),
                    'media_tray':this_recipe.get(self.f['reicpe_container']),
                    'per_container':this_recipe.get(self.f['reicpe_per_container']),
                    'S2_mult_rate':this_recipe.get(self.f['reicpe_mult_rate']),
                    'S2_overage':this_recipe.get(self.f['reicpe_overage']),
                    'plant_code':this_recipe.get(self.f['product_code'],),
                    'plant_name':this_recipe.get(self.f['product_name'],['',])[0],
                    'start_week' : this_recipe.get(self.f['reicpe_start_week']),
                    'end_week' : this_recipe.get(self.f['reicpe_end_week']),
                    'start_size': this_recipe.get(self.f['reicpe_start_size']),
                    'stage': this_recipe.get(self.f['reicpe_stage']),
                    })
        if recipe_s3  and not recipe:
            for this_recipe in recipe_s3:
                plant_code = this_recipe.get(self.f['product_code'])
                if not recipe.get(plant_code):
                    recipe[plant_code] = {}
                recipe[plant_code].update(
                    {'S3_growth_weeks':this_recipe.get(self.f['reicpe_growth_weeks']),
                    'cut_productivity':this_recipe.get(self.f['reicpe_productiviy']),
                    'media_tray':this_recipe.get(self.f['reicpe_container']),
                    'per_container':this_recipe.get(self.f['reicpe_per_container']),
                    'plant_code':this_recipe.get(self.f['product_code']),
                    'S3_mult_rate':this_recipe.get(self.f['reicpe_mult_rate']),
                    'S3_overage':this_recipe.get(self.f['reicpe_overage']),
                    'plant_code':this_recipe.get(self.f['product_code'],),
                    'plant_name':this_recipe.get(self.f['product_name'],['',])[0],
                    'start_week' : this_recipe.get(self.f['reicpe_start_week']),
                    'end_week' : this_recipe.get(self.f['reicpe_end_week']),
                    'start_size': this_recipe.get(self.f['reicpe_start_size']),
                    'stage': this_recipe.get(self.f['reicpe_stage']),
                    }
                    )
        if recipe_s4  and not recipe:
            for this_recipe in recipe_s4:
                plant_code = this_recipe.get(self.f['product_code'])
                if not recipe.get(plant_code):
                    recipe[plant_code] = []
                recipe[plant_code].append(
                    {'S4_growth_weeks':this_recipe.get(self.f['reicpe_growth_weeks']),
                    'media_tray':this_recipe.get(self.f['reicpe_container']),
                    'cut_productivity':this_recipe.get(self.f['reicpe_productiviy']),
                    'per_container':this_recipe.get(self.f['reicpe_per_container']),
                    'S4_mult_rate':this_recipe.get(self.f['reicpe_mult_rate']),
                    'S4_overage_rate':this_recipe.get(self.f['reicpe_overage']),
                    'S4_overage': this_recipe.get(self.f['reicpe_overage']),
                    'plant_code':this_recipe.get(self.f['product_code'],),
                    'plant_name':this_recipe.get(self.f['product_name'],['',])[0],
                    'start_week' : this_recipe.get(self.f['reicpe_start_week']),
                    'end_week' : this_recipe.get(self.f['reicpe_end_week']),
                    'start_size': this_recipe.get(self.f['reicpe_start_size']),
                    'stage': this_recipe.get(self.f['reicpe_stage']),
                    'soil_type': this_recipe.get(self.f['reicpe_soil_type'])
                    }
                    )
        if not recipe:
            return {}
        return recipe
    
    def get_product_map(self, values_dict, map_type='model_2_field_id'):
        '''
        values_dict: has the values of the stock model
        fdict: has the fields:field_id realation of lkf forms

        example:
        values_dict = {'product_code':'LNAFP', 'stock_qty': 100, 'scrap':10, lot_num:'202305'} 
        fdict = {'product_code':'ad0000000000000000cc0000', 
                   'stock_qty': 'ad0000000000000000cc0111', '
                   'scrap':'ad0000000000000000cc0222', 
                   'lot_num':'ad0000000000000000cc333'} 
        '''
        fdict = deepcopy(self.f)
        res = {}
        if map_type == 'model_2_field_id':
            for key, value in values_dict.items():
                field_id = fdict.get(key)
                if field_id:
                    res['answers.{}'.format(field_id)] = value
        elif map_type == 'field_id_2_model':
            fdict =  { v:k for k,v in fdict.items()}
            for key, value in values_dict.items():
                if isinstance(value, dict):
                    res.update(self.get_product_map(values_dict[key], map_type=map_type))
                else:
                    field_id = fdict.get(key)
                    if field_id:
                        res[field_id] = value
        return res

    def get_product_stock(self, product_code, warehouse=None, location=None, lot_number=None, date_from=None, date_to=None,  **kwargs):
        #GET INCOME PRODUCT
        stock = {}
        stock['adjustments'] = self.stock_adjustments_moves( product_code=product_code, lot_number=lot_number, \
            warehouse=warehouse , date_from=None, date_to=None, **kwargs)
        # if stock['adjustments']:
        #     #date_from = stock['adjustments'][product_code]['date']
        #     stock['adjustments'] = stock['adjustments'][product_code]['total']
        # else:
        #     stock['adjustments'] = 0

        stock['production'] = self.stock_production(date_from =date_from, date_to=date_to ,\
             product_code=product_code, lot_number=lot_number, warehouse=warehouse )
        stock['move_in'] = self.stock_moves('in', product_code=product_code, warehouse=warehouse, location=location, \
            lot_number=lot_number, date_from=date_from, date_to=date_to, **kwargs)
        #GET PRODUCT EXITS

        stock['move_out'] = self.stock_moves('out', product_code=product_code, warehouse=warehouse, location=location, \
            lot_number=lot_number, date_from=date_from, date_to=date_to, **kwargs)
        scrapped, cuarentin = self.stock_scrap(product_code=product_code, warehouse=warehouse, location=location, \
            lot_number=lot_number, date_from=date_from, date_to=date_to, status='done', **kwargs )    
        stock['scrapped'] = scrapped
        stock['cuarentin'] = cuarentin


        # stock['sales']  = stock_sales(product_code=product_code, lot_number=lot_number, warehouse=warehouse )
        sales=0
        stock['sales'] = sales
        # stock['adjustments'] += self.stock_adjustments_moves(product_code=product_code, lot_number=lot_number, \
        #     warehouse=warehouse , date_from=None, date_to=None)
        if (product_code and warehouse and lot_number) or True:
            cache_stock = self.cache_get({'_id':f"{product_code}_{lot_number}_{warehouse}","_one":True, },**kwargs)
            print('cache stock', cache_stock)
        stock = self.add_dicts(stock, cache_stock.get('cache',{}))
        stock['stock_in'] = stock['production'] + stock['move_in']
        stock['stock_out'] = stock['scrapped'] + stock['move_out'] + stock['sales']  + stock['cuarentin']
        stock['actuals'] = stock['stock_in'] - stock['stock_out'] + stock['adjustments']
        #update_stock(stock)
        stock['scrap_perc']  = 0
        if stock.get('stock_in') and stock.get('scrapped'):
            stock['scrap_perc'] = round(stock.get('scrapped',0)/stock.get('stock_in',1),2)
        return stock

    def get_product_info(self, answers, folio=None,  **kwargs):
        warehouse = answers[self.CATALOG_WAREHOUSE_OBJ_ID][self.f['warehouse']]
        plant_code = answers.get(self.f['product_recipe'], {}).get(self.f['product_code'], '')
        yearWeek = str(answers[self.f['product_lot_created_week']])
        year = yearWeek[:4]
        week = yearWeek[4:]
        recipes = self.get_plant_recipe( [plant_code,], stage=[4, 'Ln72'] )
        recipe = self.select_S4_recipe(recipes[plant_code], week)
        grow_weeks = recipe.get('S4_growth_weeks')
        ready_date = answers.get(self.f['product_lot'])
        # if kwargs.get('kwargs',{}).get("force_lote") and answers.get(self.f['product_lot']):
        #     ready_date = answers.get(self.f['product_lot'])
        #     print('FOORCE LOTEEEEE')
        # else:
        #     if not folio and not ready_date:
        #         plant_date = datetime.strptime('%04d-%02d-1'%(int(year), int(week)), '%Y-%W-%w')
        #         ready_date = plant_date + timedelta(weeks=grow_weeks)
        #         ready_date = int(ready_date.strftime('%Y%W'))
        #     else:
        #         ready_date = answers[self.f['product_lot']]

        product_stock = self.get_product_stock(plant_code, warehouse=warehouse, lot_number=ready_date, kwargs=kwargs.get('kwargs',{}) )
        print('product_stock=', product_stock)
        scrapped = product_stock['scrapped']
        overage = recipes[plant_code][0].get('S4_overage_rate')
        actual_flats_on_hand = product_stock['actuals']
        proyected_flats_on_hand = math.floor(( 1 - overage) * actual_flats_on_hand)
        lot_size = self.current_record['answers'].get(self.f['product_lot_produced'],0)
        if lot_size == 0:
            perc_scrapped = 0
        else:
            perc_scrapped = round(scrapped / lot_size, 2)

        real_flats_proyected = lot_size - scrapped

        if real_flats_proyected < proyected_flats_on_hand:
            proyected_flats_on_hand = real_flats_proyected

        answers[self.f['product_lot_produced']] = product_stock['production']
        answers[self.f['product_lot_move_in']] = product_stock['move_in']
        answers[self.f['product_lot_scrapped']] = product_stock['scrapped']
        answers[self.f['product_lot_move_out']] = product_stock['move_out']
        answers[self.f['product_lot_sales']] = product_stock['sales']
        answers[self.f['product_lot_cuarentin']] = product_stock['cuarentin']
        answers[self.f['product_lot_actuals']] = product_stock['actuals']
        answers[self.f['product_lot_adjustments']] = product_stock['adjustments']

        answers[self.f['product_lot_per_scrap']] = perc_scrapped
        answers[self.f['product_lot_proyected_qty']] = proyected_flats_on_hand
        answers[self.f['product_lot_per_scrap']] = perc_scrapped       
        answers[self.f['product_lot']] = ready_date
        if answers[self.f['product_lot_actuals']] <= 0:
            answers[self.f['inventory_status']] = 'done'
        else:
            answers[self.f['inventory_status']] = 'active'
        answers.update({self.f['inv_group']:self.get_grading(folio, answers)})
        return answers

    def get_inventory_record_by_folio(self, folio, form_id ):
        #use to be get_inventory_flow
        record_inventory = self.cr.find_one({
            'form_id': form_id,
            'deleted_at': {'$exists': False},
            'folio': folio
        }, {'answers': 1, 'folio': 1, 'form_id': 1, '_id': 1})
        return record_inventory

    def get_invtory_record_by_product(self, form_id, ready_date, planting_house, plant_code):
        #use to be get_record_greenhouse_inventory
        query_greenhouse_inventory = {
            'form_id': form_id,
            'deleted_at': {'$exists': False},
            f"answers.{self.f['product_lot']}": int(ready_date),
            f"answers.{self.CATALOG_WAREHOUSE_OBJ_ID}.{self.f['warehouse']}": planting_house,
            f"answers.{self.CATALOG_PRODUCT_RECIPE_OBJ_ID}.{self.f['product_code']}": plant_code,
        }
        record = self.cr.find_one(query_greenhouse_inventory, {'folio': 1, 'answers': 1, 'form_id': 1, 'user_id': 1})
        return record

    def get_record_catalog_del(self, form_id, folio=None):
        mango_query = {
            "selector":{"answers": {}},
            "limit":1000,
            "skip":0
            }
        if folio:
            mango_query['selector']['answers'].update({self.f['cat_stock_folio']:folio})
        else:
            mango_query['selector']['answers'].update({self.f['inventory_status']: "Done"})
            
        res = self.lkf_api.search_catalog( self.FORM_CATALOG_DIR[form_id], mango_query, jwt_settings_key='APIKEY_JWT_KEY')
        return res

    def get_record_catalog(self,  folio ):
        mango_query = {"selector":
            {"answers":
                {"$and":[
                    {self.f['cat_stock_folio']: {'$eq': folio}}
                ]}},
            "limit":1,
            "skip":0}
        res = self.lkf_api.search_catalog( self.CATALOG_INVENTORY_ID, mango_query, jwt_settings_key='APIKEY_JWT_KEY')
        return res

    def get_stock_query(self, query_dict):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.FORM_INVENTORY_ID,
            }
        if query_dict.get('folio'):
            match_query.update({'folio':query_dict.get('folio')})
        match_query.update(self.get_product_map(query_dict, map_type='model_2_field_id'))
        return match_query

    def get_grading_sublots(self, gradings):
        grading_rec = {}
        for grading in gradings:
            lot_number = int(f"{grading.get(self.f['grading_ready_year'])}{grading.get(self.f['grading_ready_week'])}")
            grading[self.f['grading_ready_yearweek']] = lot_number
            grading_rec[lot_number] = grading_rec.get(lot_number,0)
            grading_rec[lot_number] += grading[self.f['grading_flats']]
        return grading_rec

    def get_record_greenhouse_inventory(self, ready_date, planting_house, plant_code):
        query_greenhouse_inventory = {
            'form_id': self.FORM_INVENTORY_ID,
            'deleted_at': {'$exists': False},
            f"answers.{self.f['product_lot']}": int(ready_date),
            f"answers.{self.CATALOG_WAREHOUSE_OBJ_ID}.{self.f['warehouse']}": planting_house,
            f"answers.{self.f['product_recipe']}.{self.f['product_code']}": plant_code,
            #f"answers.{self.f['inventory_status']}": 'active'
        }
        record = self.cr.find_one(query_greenhouse_inventory, {'folio': 1, 'answers': 1, 'form_id': 1, 'user_id': 1})
        return record

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
  
    def gradings_validations(self):
        answers = self.current_record.get('answers',{})
        gradings = answers[self.f['grading_group']]
        rec_date = answers[self.f['grading_date']]
        scrap_qty = answers.get(self.f['inv_scrap_qty'],0)
        grading_type = answers[self.f['grading_date']]
        plant_info = answers[self.CATALOG_INVENTORY_OBJ_ID]
        lot_number = plant_info.get(self.f['product_lot'])
        product_code = plant_info.get(self.f['product_code'])
        warehouse = plant_info.get(self.f['warehouse'])
        product_stock = self.get_product_stock(product_code, warehouse=warehouse, lot_number=lot_number, date_to=rec_date)
        grading_totals = self.get_grading_sublots(gradings)
        totals = sum(x for x in grading_totals.values())
        totals += scrap_qty
        acctual_containers = product_stock['actuals']

        # if acctual_containers != totals:
        #Validations
        total_hours = self.calc_work_hours(answers)
        print('total_hours=', total_hours)
        self.current_record['answers'][self.f['set_total_hours']] = round(total_hours, 2)

        if grading_type == 'complete'  and totals != acctual_containers:
            #trying to move more containeres that there are...
            msg = "Al realizar un grading completo, no debe de existir diferencia entre la cantidad total de flats de lote y del grading "
            msg += "La cantidad de total de flats reportadas es de: {} y la cantdidad flats del lote es de: {}. ".format(totals, acctual_containers)
            if scrap_qty:
                msg += "Mas {} flats de scrap. ".format(scrap_qty)
            msg += "Hay una diferencia de : {} favor de corregir".format(acctual_containers - totals)
            msg_error_app = {
                    "6441d33a153b3521f5b2afc9": {
                        "msg": [msg],
                        "label": "Please check your Actual Containers on Hand",
                        "error":[]
      
                    }
                }
            raise Exception( simplejson.dumps( msg_error_app ) )

        if totals > acctual_containers:
            #trying to move more containeres that there are...
            msg = "El total de flats que se le esta realizando grading es mayor a la cantidad acutal del lote."
            msg += "La cantidad de total de flats reportadas es de: {} y la cantdidad flats del lote es de: {}. ".format(totals, acctual_containers)
            if scrap_qty:
                msg += "Mas {} flats de scrap. ".format(scrap_qty)            
            msg += "Hay una diferencia de : {} favor de corregir".format(acctual_containers - totals)
            msg_error_app = {
                    "6441d33a153b3521f5b2afc9": {
                        "msg": [msg],
                        "label": "Please check your Actual Containers on Hand",
                        "error":[]
      
                    }
                }
            raise Exception( simplejson.dumps( msg_error_app ) )
        if scrap_qty:
            self.cache_set({
                        '_id': f'{product_code}_{lot_number}_{warehouse}',
                        'scrapped': scrap_qty,
                        'product_lot': lot_number,
                        'product_code':product_code,
                        'warehouse': warehouse
                        })
            self.update_calc_fields(product_code, warehouse, lot_number)
        return answers

    def inventory_adjustment(self, folio, record):
        answers = record['answers']
        plants = answers.get(self.f['grading_group'])
        print('answers=',answers)
        warehouse = answers[self.CATALOG_WAREHOUSE_OBJ_ID][self.f['warehouse']]
        adjust_date = answers[self.f['grading_date']]
        comments = record['answers'].get(self.f['inv_adjust_comments'],'') 
        patch_records = []
        metadata = self.lkf_api.get_metadata(self.FORM_INVENTORY_ID)
        kwargs = {"force_lote":True, "inc_folio":folio }
        properties = {
                "device_properties":{
                    "system": "Script",
                    "process": "Inventroy Adjustment", 
                    "accion": 'Inventroy Adjustment', 
                    "folio carga": folio, 
                    "archive": "green_house_adjustment.py",
                },
                    "kwargs": kwargs 
            }
        metadata.update({
            'properties': properties,
            'kwargs': kwargs,
            'answers': {}
            },
        )
        search_codes = []
        # for plant in plants:
        #     product_code = plant[self.CATALOG_PRODUCT_OBJ_ID][self.f['product_code']]
        #     search_codes.append(product_code)


        # recipes = self.get_plant_recipe( search_codes, stage=[4, 'Ln72'] )
        # growth_weeks = 0
        latest_versions = versions = self.get_record_last_version(record)
        answers_version = latest_versions.get('answers',{})
        last_verions_products = {}
        if answers_version:
            version_products = answers_version.get(self.f['grading_group'])
            for ver_product in version_products:
                ver_lot_number = ver_product[self.f['product_lot']]
                ver_product_code = ver_product[self.CATALOG_PRODUCT_OBJ_ID][self.f['product_code']]
                last_verions_products[f'{ver_product_code}_{warehouse}_{ver_lot_number}'] = {
                    'product_code':ver_product_code,
                    'lot_number':ver_lot_number,
                    'warehouse':warehouse
                }
        for plant in plants:
            product_code =  plant[self.CATALOG_PRODUCT_OBJ_ID][self.f['product_code']]
            search_codes.append(product_code)
        recipes = self.get_plant_recipe( search_codes, stage=[4, 'Ln72'] )
        growth_weeks = 0

        not_found = []
        for idx, plant in enumerate(plants):
            status = plant[self.f['inv_adjust_grp_status']]
            lot_number = plant[self.f['product_lot']]
            adjust_qty = plant.get(self.f['inv_adjust_grp_qty'])
            adjust_in = plant.get(self.f['inv_adjust_grp_in'], 0)
            adjust_out = plant.get(self.f['inv_adjust_grp_out'], 0)
            product_code = plant[self.CATALOG_PRODUCT_OBJ_ID][self.f['product_code']]
            verify = 0
            if adjust_qty or adjust_qty ==0:
                verify +=1
                adjust_in = 0
                adjust_out = 0
            if adjust_in:
                verify +=1
            if adjust_out:
                verify +=1
            if verify > 1:
                msg = f"You can have only ONE input on product {product_code} lot number {lot_number}."
                msg +=  "Either the Actual Qty, the Adjusted In or the Adjusted Out."
                plant[self.f['inv_adjust_grp_status']] = 'error'
                plant[self.f['inv_adjust_grp_comments']] = msg
                continue
            if verify ==  0:
                msg = f"You must input an adjusted Qty on product {product_code}, lot number {lot_number}."
                plant[self.f['inv_adjust_grp_status']] = 'error'
                plant[self.f['inv_adjust_grp_comments']] = msg
                continue

            if last_verions_products.get(f'{product_code}_{warehouse}_{lot_number}'):
                last_verions_products.pop(f'{product_code}_{warehouse}_{lot_number}')
            exist = self.product_stock_exists(product_code=product_code, warehouse=warehouse, lot_number=lot_number)

            if exist:
                print('plant code', product_code)
                print('plant warehouse', warehouse)
                print('plant lot_number', lot_number)
                print('plant adjust_date', adjust_date)
                product_stock = self.get_product_stock(product_code, warehouse=warehouse, lot_number=lot_number, date_to=adjust_date, **{'nin_folio':folio})
                print('product_stock',product_stock)
                actuals = product_stock.get('actuals',0)
                if adjust_qty or adjust_qty == 0:
                    cache_adjustment = adjust_qty - actuals
                    if actuals < adjust_qty:
                        adjust_in = adjust_qty - actuals 
                    elif actuals > adjust_qty:
                        adjust_out = adjust_qty - actuals
                    else:
                        adjust_in  = 0
                        adjust_out = 0
                elif adjust_in:
                    cache_adjustment = adjust_in
                    adjust_out = None
                    adjust_qty = None
                elif adjust_out:
                    cache_adjustment = adjust_out * -1
                    adjust_in = None
                    adjust_qty = None

                self.cache_set({
                        '_id': f'{product_code}_{lot_number}_{warehouse}',
                        'adjustments': cache_adjustment,
                        'product_lot': lot_number,
                        'product_code':product_code,
                        'warehouse': warehouse
                        })
                plant[self.f['inv_adjust_grp_qty']] = adjust_qty
                plant[self.f['inv_adjust_grp_in']] = adjust_in
                plant[self.f['inv_adjust_grp_out']] = abs(adjust_out)
                response = self.update_calc_fields(product_code, warehouse, lot_number, folio=exist['folio'], **{'nin_folio':folio} )
                if not response:
                    comments += f'Error updating product {product_code} lot {lot_number}. '
                    plant[self.f['inv_adjust_grp_status']] = 'error'
                else:
                    plant[self.f['inv_adjust_grp_status']] = 'done'
                    plant[self.f['inv_adjust_grp_comments']] = ""

            else:
                if recipes.get(product_code) and len(recipes[product_code]):
                    growth_weeks = recipes[product_code][0]['S4_growth_weeks']
                    soli_type = recipes[product_code][0].get('soil_type','RIVERBLEND')
                    start_size = recipes[product_code][0].get('recipes','Ln72')

                    yearWeek = plant.get(self.f['product_lot_created_week'])
                    if not yearWeek:
                        ready_date = lot_number
                        year = str(ready_date)[:4]
                        week = str(ready_date)[4:]
                        plant_ready_date = datetime.strptime('%04d-%02d-1'%(int(year), int(week)), '%Y-%W-%w')
                        yearWeek = plant_ready_date - timedelta(weeks=growth_weeks)
                        yearWeek = int(yearWeek.strftime('%Y%W'))

                    else:
                        not_found.append(product_code)
                        plant[self.f['inv_adjust_grp_status']] = 'not_found'
                        continue                
                    answers = {
                        self.CATALOG_PRODUCT_RECIPE_OBJ_ID:{
                            self.f['product_code']:product_code,
                            self.f['reicpe_start_size']:start_size,
                            self.f['reicpe_soil_type']:soli_type,
                            },
                        self.f['product_lot_created_week']:yearWeek,
                        self.f['product_lot']:lot_number,
                        self.f['product_growth_week']:growth_weeks,
                        self.f['status']:"active",
                        self.CATALOG_WAREHOUSE_OBJ_ID:{self.f['warehouse']:warehouse}
                            }
                    metadata['answers'] = answers
                    print('setting caches....', adjust_qty + adjust_in - adjust_out)
                    self.cache_set({
                            '_id': f'{product_code}_{lot_number}_{warehouse}',
                            'adjustments': adjust_qty + adjust_in - adjust_out,
                            'product_lot': lot_number,
                            'product_code':product_code,
                            'warehouse': warehouse
                            })
                    response_sistema = self.lkf_api.post_forms_answers(metadata)
                    # self.update_calc_fields(product_code, warehouse, lot_number)
                    print('response_sistema=',response_sistema)
                    try:
                        new_inv = self.get_record_by_id(response_sistema.get('id'))
                        print('new_inv=', new_inv)
                    except:
                        print('no encontro...')
                    status_code = response_sistema.get('status_code',404)
                    if status_code == 201:
                        plant[self.f['inv_adjust_grp_status']] = 'done'
                        plant[self.f['inv_adjust_grp_comments']] = "New Creation "
                    else:
                        error = response_sistema.get('json',{}).get('error', 'Unkown error')
                        plant[self.f['inv_adjust_grp_status']] = 'error'
                        plant[self.f['inv_adjust_grp_comments']] = f'Status Code: {status_code}, Error: {error}'
                else:
                        plant[self.f['inv_adjust_grp_status']] = 'error'
                        plant[self.f['inv_adjust_grp_comments']] = f'Recipe not found'

        if last_verions_products:
            for key, value in last_verions_products.items():
                self.update_calc_fields(value['product_code'], value['warehouse'], value['lot_number'])

        record_id = record['_id']['$oid']
        record['answers'][self.f['inv_adjust_status']] = 'done'
        if not_found:
            comments += f'Codes not found: {not_found}.'

        record['answers'][self.f['inv_adjust_comments']] = comments
        self.lkf_api.patch_record(record, record_id)

    def list_str_match(self, folio):
        if type(folio) == list:
            return {"$in":folio}
        else:
            return folio

    def list_str_not_match(self, folio):
        if type(folio) == list:
            return {"$nin":folio}
        else:
            return {"$ne":folio}

    def move_location(self, current_record):
        current_answers = current_record['answers']
        plant_info = current_answers.get(self.CATALOG_INVENTORY_OBJ_ID,{})
        folio_inventory = plant_info.get(self.f['cat_stock_folio'])
        product_lot = plant_info.get(self.f['product_lot'])
        product_code = plant_info.get(self.f['product_code'])
        warehouse = plant_info.get(self.f['warehouse'])
        record_inventory_flow = self.get_inventory_record_by_folio(folio_inventory, form_id=self.FORM_INVENTORY_ID )
        inv_record = record_inventory_flow.get('answers')
        #gets the invetory as it was on that date...
        inv = self.get_product_stock(product_code, warehouse=warehouse, lot_number=product_lot, 
            date_to=current_answers[self.f['grading_date']], **{"nin_folio":current_record.get('folio')})
        # This are the actuals as they were on that date not including this move.
        acctual_containers = inv.get('actuals')
        relocated_containers = sum( [s.get(self.f['move_group_qty'], 0) for s in current_answers.get(self.f['move_group'])] )
        flats_to_move = current_answers.get(self.f['inv_move_qty'])

        if acctual_containers == 0:
            msg = "This lot has no containers left, if this is NOT the case first do a inventory adjustment"
            msg_error_app = {
                    f"{self.f['product_lot_actuals']}": {
                        "msg": [msg],
                        "label": "Please check your lot inventory",
                        "error":[]
      
                    }
                }
            #TODO set inventory as done
            raise Exception( simplejson.dumps( msg_error_app ) )        
        if relocated_containers != flats_to_move:
            msg = "Flats to move out {} containers and the sum of relocatated container is: {}. ".format(flats_to_move, relocated_containers)
            msg += "This 2 numbers must be the same!"
            msg_error_app = {
                    f"{self.f['inv_move_qty']}": {
                        "msg": [msg],
                        "label": "Please check your Flats to move",
                        "error":[]
      
                    }
                }
            raise Exception( simplejson.dumps( msg_error_app ) )

        current_green_house = plant_info.get(self.f['warehouse'])
        dest_gh_select = current_answers.get(self.f['move_new_location'])
        dest_warehouse = ""
        for x in dest_gh_select.split('_'):
            if dest_warehouse:
                dest_warehouse += " "
            dest_warehouse += x.title()

        if current_green_house == dest_warehouse:
            msg = "You need to make the move to a new destination. "
            msg += "Your current from location is: {} and you destination location is:{}".format(current_green_house, dest_warehouse)
            msg_error_app = {
                    f"{self.f['move_new_location']}": {
                        "msg": [msg],
                        "label": "Please check your Flats to move",
                        "error":[]
      
                    }
                }
            raise Exception( simplejson.dumps( msg_error_app ) )

        if flats_to_move > acctual_containers:
        # if False:
            #trying to move more containeres that there are...
            cont_diff = flats_to_move - acctual_containers
            msg = "On lot folio: {}, there actually only {} containers and you are trying to move {} containers.".format(folio_inventory, acctual_containers, flats_to_move)
            msg += "Check this out...! Your are trying to move {}, more containers than they are. ".format(cont_diff)
            msg += "If this is the case, please frist make an inventory adjustment of {} ".format(cont_diff)
            msg += " for location {} and ready date {}".format(current_green_house, product_lot )
            msg_error_app = {
                    f"{self.f['inv_move_qty']}": {
                        "msg": [msg],
                        "label": "Please check your Flats to move",
                        "error":[]
      
                    }
                }
            raise Exception( simplejson.dumps( msg_error_app ) )


        dest_warehouse_inventory = self.get_invtory_record_by_product(self.FORM_INVENTORY_ID, product_lot, dest_warehouse, product_code)
        dest_folio = None
        self.cache_set({
            '_id': f'{product_code}_{product_lot}_{dest_warehouse}',
            'move_in':flats_to_move,
            'product_lot':product_lot,
            'product_code':product_code,
            'warehouse': dest_warehouse
            })
        if not dest_warehouse_inventory:
            #creates new record.
            new_inv_rec = deepcopy(inv_record)
            # stock = self.get_product_stock(product_code, warehouse=dest_warehouse, lot_number=product_lot, **{'keep_cache':True})
            # update_values = self.get_product_map(stock)
            new_inv_rec.update({
                f"{self.CATALOG_WAREHOUSE_OBJ_ID}": {self.f['warehouse']:dest_warehouse},
                f"{self.f['product_lot_actuals']}": flats_to_move,
                f"{self.f['product_lot_move_in']}": flats_to_move,
                f"{self.f['product_lot_move_out']}": 0,
                self.f['inventory_status']: 'active',
            })

            metadata = self.lkf_api.get_metadata(self.FORM_INVENTORY_ID) 
            metadata.update({
                'properties': {
                    "device_properties":{
                        "system": "Script",
                        "process": 'Green House Inventory Move',
                        "action": 'Create record Inventory GreenHouse',
                        "from_folio": current_record.get('folio',''),
                        "archive": "inventory_move_greenhouse_location.py"
                    }
                }
            })
            #1 check if the hole lot is moving out ....
            # response, update_rec = update_origin_log(record_inventory_flow, inv_record, flats_to_move, acctual_containers)
            # new_inv_rec.update(update_rec)
            metadata.update({'answers': new_inv_rec})
            response = self.lkf_api.post_forms_answers(metadata, jwt_settings_key='USER_JWT_KEY')
            if response.get('status_code') > 299 or not response.get('status_code'):
                msg_error_app = response.get('json', 'Error al acomodar producto , favor de contactar al administrador')
                raise Exception( simplejson.dumps(msg_error_app) )
            x = simplejson.loads(response['data'])
            dest_folio = x.get('folio')
        else:
            # Adding up to an existing lot
            # response, update_rec = update_origin_log(record_inventory_flow, inv_record, flats_to_move, acctual_containers)
            print('TODO=', dest_warehouse_inventory)
            dest_folio = dest_warehouse_inventory.get('folio')
            self.update_calc_fields(product_code,  dest_warehouse, product_lot, folio=dest_folio)
            # dest_warehouse_inventory['answers'][self.f['product_lot_actuals']] += flats_to_move
            # response = lkf_api.patch_record(dest_warehouse_inventory, jwt_settings_key='USER_JWT_KEY')
        return dest_folio

    def plant_recipe_query(self, all_codes, start_size, reicpe_stage, recipe_type='Main'):
        mango_query = {
            "selector": {
                "answers": {
                    self.f['reicpe_start_size']: {"$eq": start_size},
                    self.f['recipe_type']: {"$eq": recipe_type},
                    self.f['reicpe_stage']: {"$eq": reicpe_stage}}
                    } ,
            "limit": 1000,
            "skip": 0
                    }
        if all_codes:
            mango_query['selector']['answers'].update({self.f['product_code']: {"$in": all_codes},})
        return mango_query

    def process_record_to_catalog(self, current_record ):
        answers = current_record['answers']
        # Obtengo los campos de la forma
        form_fields = self.lkf_api.get_form_id_fields(current_record['form_id'], jwt_settings_key='APIKEY_JWT_KEY')
        fields = form_fields[0]['fields']
        # Obtengo solo los índices que necesito de cada campo
        info_fields = [{k:n[k] for k in ('label','field_type','field_id','groups_fields','group','options','catalog_fields','catalog') if k in n} for n in fields]
        for field in info_fields:
            field_id = field.get('field_id', '')
            if field.get('field_type', '') == 'catalog-select':
                catalog_field_id = field.get('catalog', {}).get('catalog_field_id', '')
                answers[ field_id ] = answers.get(catalog_field_id, {}).get(field_id)

            elif field.get('field_type', '') == 'catalog-detail':
                catalog_field_id = field.get('catalog', {}).get('catalog_field_id', '')
                val_catalog_answers = answers.get(catalog_field_id, {}).get(field_id, [])
                if val_catalog_answers:
                    answers[ field_id ] = val_catalog_answers

        # Obtengo los campos del catalogo
        catalog_fields = self.lkf_api.get_catalog_id_fields( self.CATALOG_INVENTORY_ID, jwt_settings_key='APIKEY_JWT_KEY' )
        info_catalog = catalog_fields.get('catalog', {})
        fields = info_catalog['fields']
        #print('fields=',fields)
        dict_idfield_typefield = { \
            f.get('field_id'): {\
                'field_type': f.get('field_type'), \
                'options': { o.get('value'): o.get('label') for o in f.get('options',[]) }\
            } for f in fields }

        #print('dict_idfield_typefield=',dict_idfield_typefield)
        dict_answers_to_catalog = {}
        for id_field in dict_idfield_typefield:
            if id_field in (self.f['product_recipe'], self.CATALOG_WAREHOUSE_OBJ_ID):
                continue
            val_in_record = answers.get( id_field, False )
            val_in_record_org = val_in_record
            if val_in_record or val_in_record == 0:
                info_field_cat = dict_idfield_typefield[ id_field ]
                if info_field_cat.get('options', False):
                    val_in_record = info_field_cat['options'].get( val_in_record, None )
                    if not val_in_record:
                        if type(val_in_record) != str:
                            continue
                        val_in_record_org.replace('_', ' ')
                        val_in_record_org = val_in_record_org.title()
                        val_in_record = info_field_cat['options'].get( val_in_record_org, None )
                elif info_field_cat.get('field_type') == 'catalog-select':
                    if isinstance(val_in_record, list) and val_in_record:
                        val_in_record = val_in_record[0]
                dict_answers_to_catalog.update({ id_field: val_in_record })

        dict_answers_to_catalog.update({
            self.f['cat_stock_folio']: current_record['folio']
        })
        record_catalog = self.get_record_catalog( current_record['folio'] )
        catalogo_metadata = self.lkf_api.get_catalog_metadata(catalog_id=self.CATALOG_INVENTORY_ID)

        if record_catalog:
            info_record_catalog = record_catalog[0]

            if answers.get(self.f['product_lot_actuals'], 1) <= 0:
                # Se elimina el registro del catalogo
                response_delete_catalog = self.lkf_api.delete_catalog_record(self.CATALOG_INVENTORY_ID, info_record_catalog.pop('_id'), info_record_catalog.pop('_rev'), jwt_settings_key='APIKEY_JWT_KEY')
                return True

            info_record_catalog.update(dict_answers_to_catalog)


            catalogo_metadata.update({'record_id': info_record_catalog.pop('_id'), '_rev': info_record_catalog.pop('_rev'), 'answers': info_record_catalog})
            response_update_catalog = self.lkf_api.bulk_patch_catalog([catalogo_metadata,], self.CATALOG_INVENTORY_ID, jwt_settings_key='APIKEY_JWT_KEY')
        else:
            catalogo_metadata.update({'answers': dict_answers_to_catalog})
            res_crea_cat = self.lkf_api.post_catalog_answers(catalogo_metadata, jwt_settings_key='APIKEY_JWT_KEY')
        return True

    def product_stock_exists(self, product_code, warehouse, location=None, lot_number=None, status=None):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.FORM_INVENTORY_ID,
            f"answers.{self.CATALOG_PRODUCT_RECIPE_OBJ_ID}.{self.f['product_code']}": product_code,
            }
        match_query.update({f"answers.{self.CATALOG_WAREHOUSE_OBJ_ID}.{self.f['warehouse']}":warehouse})      
        if location:
            match_query.update({f"answers.{self.f['product_lot_location']}":location})
        if lot_number:
            match_query.update({f"answers.{self.f['product_lot']}":lot_number})
        if status:
            match_query.update({f"answers.{self.f['inventory_status']}":status})
        exist = self.cr.find_one(match_query)
        return exist

    def select_S4_recipe(self, plant_recipe, plant_week):
        for recipe in plant_recipe:
            start_week = recipe.get('start_week')
            end_week = recipe.get('end_week')
            if int(plant_week) >= int(start_week) and int(plant_week) <= int(end_week):
                return recipe
        return {}

    def set_lot_ready_week(self, lot_ready_week, gradin_totals):
        lot_ready_week = str(lot_ready_week)
        week = int(lot_ready_week[-2:])
        year = int(lot_ready_week[:4])
        ready_week = datetime.strptime('%04d-%02d-1' % (year, week), '%Y-%W-%w')
        # ready_week = this_date.strftime('%Y%W')
        sets = []
        for week, qty in gradin_totals.items():
            week_type = week.split('_')
            if len(week_type)  == 2:
                if week_type[0] == 'on':
                    delta_weeks = 0 
                else:
                    try:
                        delta_weeks = int(week_type[0]) * -1
                    except:
                        delta_weeks = int(week_type[1]) 
                new_week = ready_week + timedelta(weeks=delta_weeks)
                new_week = new_week.strftime('%Y%W')
                tset ={
                 self.f['inv_group_readyweek']: int(new_week) ,
                 self.f['inv_group_flats']: qty
                }
                sets.append(tset)
        return sets

    def stock_adjustments(self, product_code=None, warehouse=None, location=None, lot_number=None, date_from=None, date_to=None, **kwargs):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.ADJUIST_FORM_ID,
            f"answers.{self.f['inv_adjust_status']}":{"$ne":"cancel"}
            }
        # inc_folio = kwargs.get("kwargs",{}).get("inc_folio")
        # exclude_folio = kwargs.get("kwargs",{}).get("exclude_folio")
        inc_folio = None
        exclude_folio = None
        if warehouse:
            match_query.update({f"answers.{self.CATALOG_WAREHOUSE_OBJ_ID}.{self.f['warehouse']}":warehouse})      
        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field_id=self.f['grading_date']))

        match_query_stage2 = {f"answers.{self.f['grading_group']}.{self.f['inv_adjust_grp_status']}": "done"}
        if inc_folio:
            match_query_stage2 = {"$or": [
                {f"answers.{self.f['grading_group']}.{self.f['inv_adjust_grp_status']}": "done"},
                get_folios_match(inc_folio = inc_folio)
                ]}
        if product_code:
            match_query_stage2.update({f"answers.{self.f['grading_group']}.{self.CATALOG_PRODUCT_OBJ_ID}.{self.f['product_code']}":product_code})
        if lot_number:
            match_query_stage2.update({f"answers.{self.f['grading_group']}.{self.f['product_lot']}":lot_number})
        if location:
            match_query_stage2.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_lot_location']}":location})
        query= [{'$match': match_query }]
        if exclude_folio:
            query += [{'$match': get_folios_match(exclude_folio=exclude_folio) }]
        query += [
            {'$unwind': '$answers.{}'.format(self.f['grading_group'])},
            ]
        if match_query_stage2:
            query += [{'$match': match_query_stage2 }]

        query += [
            {'$project':
                {'_id': 1,
                    'product_code': f"$answers.{self.f['grading_group']}.{self.CATALOG_PRODUCT_OBJ_ID}.{self.f['product_code']}",
                    'date': f"$answers.{self.f['grading_date']}",
                    'adjust': f"$answers.{self.f['grading_group']}.{self.f['inv_adjust_grp_qty']}",
                    }
            },
            {'$sort': {'date': 1}},
            {'$group':
                {'_id':
                    { 'product_code': '$product_code',
                      },
                  'date': {'$last': '$date'},
                  'adjust': {'$last': '$adjust'},
                  }
            },
            {'$project':
                {'_id': 0,
                'product_code': '$_id.product_code',
                'date': '$date',
                'total': '$adjust'
                }
            },
            {'$sort': {'product_code': 1}}
            ]
        res = self.cr.aggregate(query)
        result = {}
        for r in res:
            pcode = r.get('product_code')
            result[pcode] = result.get(pcode, {'total':0,'date':''})        
            result[pcode]['date'] = r.get('date',0)
            result[pcode]['total'] = r.get('total',0)
        return result  

    def stock_adjustments_moves(self, product_code=None, warehouse=None, location=None, lot_number=None, date_from=None, date_to=None, **kwargs):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.ADJUIST_FORM_ID,
            f"answers.{self.f['inv_adjust_status']}":{"$ne":"cancel"}
            }
        inc_folio = kwargs.get("inc_folio")
        nin_folio = kwargs.get("nin_folio")
        if warehouse:
            match_query.update({f"answers.{self.CATALOG_WAREHOUSE_OBJ_ID}.{self.f['warehouse']}":warehouse})      
        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field_id=self.f['grading_date']))
        match_query_stage2 = {}
        # match_query_stage2 = {f"answers.{self.f['grading_group']}.{self.f['inv_adjust_grp_status']}": "done"}
        if nin_folio:
            match_query.update({"folio": {"$ne":nin_folio }})
        if inc_folio:
            match_query_stage2 = {"$or": [
                {f"answers.{self.f['grading_group']}.{self.f['inv_adjust_grp_status']}": "done"},
                {"folio":inc_folio}
                ]}
        if product_code:
            match_query_stage2.update({f"answers.{self.f['grading_group']}.{self.CATALOG_PRODUCT_OBJ_ID }.{self.f['product_code']}":product_code})
        if lot_number:
            match_query_stage2.update({f"answers.{self.f['grading_group']}.{self.f['product_lot']}":lot_number})
        if location:
            match_query_stage2.update({f"answers.{self.CATALOG_PRODUCT_OBJ_ID}.{self.f['product_lot_location']}":location})
        query= [{'$match': match_query },
            {'$unwind': '$answers.{}'.format(self.f['grading_group'])},
            ]
        if match_query_stage2:
            query += [{'$match': match_query_stage2 }]
        query += [
            {'$project':
                {'_id': 1,
                    'product_code': f"$answers.{self.f['grading_group']}.{self.CATALOG_PRODUCT_OBJ_ID}.{self.f['product_code']}",
                    'adjust_in': f"$answers.{self.f['grading_group']}.{self.f['inv_adjust_grp_in']}",
                    'adjust_out': f"$answers.{self.f['grading_group']}.{self.f['inv_adjust_grp_out']}",
                    }
            },
            {'$group':
                {'_id':
                    { 'product_code': '$product_code',
                      },
                  'adjust_in': {'$sum': '$adjust_in'},
                  'adjust_out': {'$sum': '$adjust_out'},
                  }
            },
            {'$project':
                {'_id': 0,
                'product_code': '$_id.product_code',
                'total': {'$subtract' : ['$adjust_in', '$adjust_out' ]}
                }
            },
            {'$sort': {'product_code': 1}}
            ]
        res = self.cr.aggregate(query)
        result = 0
        for r in res:
            result = r.get('total', 0)        
        return result  

    def stock_production(self, date_from=None, date_to=None, product_code=None, warehouse=None, location=None, lot_number=None,  status='posted', **kwargs):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.PRODUCTION_FORM_ID,
            }
        match_query_stage2 = {}
        if date_from or date_to:
            match_query_stage2.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field_id=f"{self.f['production_group']}.{self.f['set_production_date']}"))
        if product_code:
            match_query.update({f"answers.{self.CATALOG_PRODUCT_RECIPE_OBJ_ID}.{self.f['product_code']}":product_code})
        if lot_number:
            match_query.update({f"answers.{self.f['production_lote']}":lot_number})  
        if warehouse:
            match_query.update({f"answers.{self.CATALOG_WAREHOUSE_OBJ_ID}.{self.f['warehouse']}":warehouse})    
        if location:
            match_query_stage2.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_lot_location']}":location})    
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
                    'product_code': f"$answers.{self.CATALOG_PRODUCT_RECIPE_OBJ_ID}.{self.f['product_code']}",
                    'total': f"$answers.{self.f['production_group']}.{self.f['set_total_produced']}",
                    }
            },
            {'$group':
                {'_id':
                    { 'product_code': '$product_code',
                      },
                  'total': {'$sum': '$total'},
                  }
            },
            {'$project':
                {'_id': 0,
                'product_code': '$_id.product_code',
                'total': '$total',
                }
            },
            {'$sort': {'product_code': 1}}
            ]
        res = self.cr.aggregate(query)
        result = {}
        for r in res:
            pcode = r.get('product_code')
            result[pcode] = result.get(pcode, 0)        
            result[pcode] += r.get('total',0)
        if product_code:
            result = result.get(product_code,0)
        return result  

    def stock_moves(self, move_type, product_code=None, warehouse=None, location=None, lot_number=None, date_from=None, date_to=None, status='done', **kwargs):
        if move_type not in ('in','out'):
            raise('Move type only accepts values "in" or "out" ')
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.STOCK_MOVE_FORM_ID,
            }
        inc_folio = kwargs.get("inc_folio")
        nin_folio = kwargs.get("nin_folio")
        if inc_folio:
            match_query.update({"folio":inc_folio})
        if nin_folio:
            match_query.update({"folio": {"$ne":nin_folio }})
        if product_code:
            match_query.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_code']}":product_code})
        if move_type =='out':
            if warehouse:
                match_query.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['warehouse']}":warehouse})      
        if move_type =='in':
            if warehouse:
                warehouse = warehouse.lower().replace(' ', '_')
                match_query.update({f"answers.{self.f['move_new_location']}":warehouse})    
        if location:
            match_query.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_code']}":location})
        if lot_number:
            match_query.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_lot']}":lot_number})
        if status:
            match_query.update({f"answers.{self.f['inv_adjust_status']}":status})
        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field_id=self.f['grading_date']))
        query= [{'$match': match_query },
            {'$project':
                {'_id': 1,
                    'product_code': f"$answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_code']}",
                    'total': f"$answers.{self.f['inv_move_qty']}",
                    }
            },

            {'$group':
                {'_id':
                    { 'product_code': '$product_code',
                      },
                  'total': {'$sum': '$total'},
                  }
            },
            {'$project':
                {'_id': 0,
                'product_code': '$_id.product_code',
                'total': '$total',
                }
            },
            {'$sort': {'product_code': 1}}
            ]
        res = self.cr.aggregate(query)
        result = {}
        for r in res:
            pcode = r.get('product_code')
            result[pcode] = result.get(pcode, 0)        
            result[pcode] += r.get('total',0)
        if product_code:
            result = result.get(product_code,0)
        return result  

    def detail_stock_moves(self, warehouse, move_type=None, product_code=None, lot_number=None,  location=None, date_from=None, date_to=None, status='done', **kwargs):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.STOCK_MOVE_FORM_ID,
            }
        inc_folio = kwargs.get("inc_folio")
        nin_folio = kwargs.get("nin_folio")
        warehouse_out = warehouse.lower().replace(' ', '_')
        if move_type =='out':
            match_query.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['warehouse']}":warehouse})      
        elif move_type =='in':
            match_query.update({f"answers.{self.f['move_new_location']}":warehouse_out})
        else:
            match_query.update(
                {"$or":
                    [{f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['warehouse']}":warehouse},
                    {f"answers.{self.f['move_new_location']}":warehouse_out}
                    ]
                })      
        if inc_folio:
            match_query.update({"folio":inc_folio})
        if nin_folio:
            match_query.update({"folio": {"$ne":nin_folio }})
        if product_code:
            match_query.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_code']}":product_code})
        if lot_number:
            match_query.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_lot']}":int(lot_number)})
        if location:
            match_query.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_code']}":location})
        if status:
            match_query.update({f"answers.{self.f['inv_adjust_status']}":status})
        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field_id=self.f['grading_date']))
        query= [{'$match': match_query },
            {'$project':
                {'_id': 1,
                    'folio': "$folio",
                    'date': f"$answers.{self.f['grading_date']}",
                    'product_code': f"$answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_code']}",
                    'lot_number': f"$answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_lot']}",
                    'warehouse_from': f"$answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['warehouse']}",
                    'warehouse_to':f"$answers.{self.f['move_new_location']}",
                    'move_type':{ "$cond":[ 
                        {"$eq":[ f"$answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['warehouse']}" , warehouse]}, 
                        "Out", 
                        "In" ]},
                    'qty':f"$answers.{self.f['inv_move_qty']}"
                    }
            },
            {'$project':
                {'_id': 1,
                    'folio': "$folio",
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
        res = self.cr.aggregate(query)
        if kwargs.get('result'):
            result = kwargs['result']
        else:
            result = {}
        for r in res:
            epoch = self.date_2_epoch(r.get('date'))
            r['warehouse_to'] = r['warehouse_to'].replace('_', ' ').title()
            result[epoch] = result.get(epoch,[])
            result[epoch].append(r)
        return result

    def detail_adjustment_moves(self, warehouse, product_code=None, lot_number=None,  location=None, date_from=None, date_to=None, status='done', **kwargs):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.ADJUIST_FORM_ID,
            f"answers.{self.f['inv_adjust_status']}":{"$ne":"cancel"}
            }

        inc_folio = kwargs.get("inc_folio")
        nin_folio = kwargs.get("nin_folio")
        if warehouse:
            match_query.update({f"answers.{self.CATALOG_WAREHOUSE_OBJ_ID}.{self.f['warehouse']}":warehouse})      
        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field_id=self.f['grading_date']))
        match_query_stage2 = {f"answers.{self.f['grading_group']}.{self.f['inv_adjust_grp_status']}": "done"}
        if nin_folio:
            match_query.update({"folio": {"$ne":nin_folio }})
        if inc_folio:
            match_query_stage2 = {"$or": [
                {f"answers.{self.f['grading_group']}.{self.f['inv_adjust_grp_status']}": "done"},
                {"folio":inc_folio}
                ]}
        if product_code:
            match_query_stage2.update({f"answers.{self.f['grading_group']}.{self.CATALOG_PRODUCT_OBJ_ID }.{self.f['product_code']}":product_code})
        if lot_number:
            match_query_stage2.update({f"answers.{self.f['grading_group']}.{self.f['product_lot']}":int(lot_number)})
        if location:
            match_query_stage2.update({f"answers.{self.CATALOG_PRODUCT_OBJ_ID}.{self.f['product_lot_location']}":location})
        query= [{'$match': match_query },
            {'$unwind': '$answers.{}'.format(self.f['grading_group'])},
            ]
        if match_query_stage2:
            query += [{'$match': match_query_stage2 }]
        query += [
            {'$project':
                {'_id': 1,
                    'folio': "$folio",
                    'date': f"$answers.{self.f['grading_date']}",
                    'product_code': f"$answers.{self.f['grading_group']}.{self.CATALOG_PRODUCT_OBJ_ID}.{self.f['product_code']}",
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
                        warehouse ]},
                'warehouse_to':{ "$cond":[ 
                        {"$gt":[ f"$adjust_in" , 0]}, 
                        warehouse, 
                        "Adujstment" ]},
                'qty_in': "$adjust_in",
                'qty_out': "$adjust_out",
                }
            },
            {'$sort': {'product_code': 1}}
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

    def detail_production_moves(self, warehouse, product_code=None, lot_number=None,  location=None, date_from=None, date_to=None, status='posted', **kwargs):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.PRODUCTION_FORM_ID,
            }
        match_query_stage2 = {}
        print('lot_number', lot_number)
        if date_from or date_to:
            match_query_stage2.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field_id=f"{self.f['production_group']}.{self.f['set_production_date']}"))
        if product_code:
            match_query.update({f"answers.{self.CATALOG_PRODUCT_RECIPE_OBJ_ID}.{self.f['product_code']}":product_code})
        if lot_number:
            match_query.update({f"answers.{self.f['production_lote']}":int(lot_number)})  
        if warehouse:
            match_query.update({f"answers.{self.CATALOG_WAREHOUSE_OBJ_ID}.{self.f['warehouse']}":warehouse})    
        if location:
            match_query_stage2.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_lot_location']}":location})    
        if status:
            match_query_stage2.update({f"answers.{self.f['production_group']}.{self.f['production_status']}":status})
        query= [{'$match': match_query },
            {'$unwind': f"$answers.{self.f['production_group']}"},
            ]
        if match_query_stage2:
            query += [{'$match': match_query_stage2 }]
        print(simplejson.dumps(query))
        query += [
            {'$project':
                {'_id': 1,
                    'folio':'$folio',
                    'date': f"$answers.{self.f['production_group']}.{self.f['set_production_date']}",
                    'product_code': f"$answers.{self.CATALOG_PRODUCT_RECIPE_OBJ_ID}.{self.f['product_code']}",
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

    def detail_scrap_moves(self, warehouse, product_code=None, lot_number=None, location=None, date_from=None, date_to=None, status='done', **kwargs):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.SCRAP_FORM_ID,
            }
        if product_code:
            match_query.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_code']}":product_code})    
        if warehouse:
            match_query.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['warehouse']}":warehouse})    
        if location:
            match_query.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_lot_location']}":location})    
        if lot_number:
            match_query.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_lot']}":int(lot_number)})    
        if status:
            match_query.update({f"answers.{self.f['inv_scrap_status']}":status})
        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field_id=self.f['grading_date']))
        query= [
            {'$match': match_query },
            {'$project':
                {'_id': 1,
                    'date': f"$answers.{self.f['grading_date']}",
                    'product_code': f"$answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_code']}",
                    'lot_number': f"$answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_lot']}",
                    'scrap': f"$answers.{self.f['inv_scrap_qty']}",
                    'cuarentin': f"$answers.{self.f['inv_cuarentin_qty']}",
                    'warehouse_from':warehouse,
                    'move_type':"Out"
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
            cuarentine = r.get('cuarentin',0)
            scrap = r.get('scrap',0)
            if cuarentine:
                r.update({
                    'warehouse_to': "Cuarentin",
                    'qty_out':cuarentine,
                    })
                result[epoch].append(r)
            if scrap:
                r.update({
                    'warehouse_to': "Scrap",
                    'qty_out':scrap,
                    })
                result[epoch].append(r)
        return result

    ### STOCK OUT'S

    def stock_scrap(self, product_code, warehouse=None, location=None, lot_number=None, date_from=None, date_to=None, status='done', **kwargs):
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
            match_query.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_lot']}":lot_number})    
        if status:
            match_query.update({f"answers.{self.f['inv_scrap_status']}":status})
        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field_id=self.f['grading_date']))
        query= [
            {'$match': match_query },
            {'$project':
                {'_id': 1,
                    'product_code': f"$answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_code']}",
                    'scrap': f"$answers.{self.f['inv_scrap_qty']}",
                    'cuarentin': f"$answers.{self.f['inv_cuarentin_qty']}",
                    }
            },

            {'$group':
                {'_id':
                    { 'product_code': '$product_code',
                      },
                  'total_scrap': {'$sum': '$scrap'},
                  'total_cuarentin': {'$sum': '$cuarentin'}
                  }
            },
            {'$project':
                {'_id': 0,
                'product_code': '$_id.product_code',
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
            result[pcode] = result.get(pcode, {'scrap':0,'cuarentin':0})        
            result[pcode]['scrap'] += r.get('total_scrap',0)
            result[pcode]['cuarentin'] += r.get('total_cuarentin',0)
        result_scrap = result.get(product_code,{}).get('scrap',0)
        result_cuarentin = result.get(product_code,{}).get('cuarentin',0) 
        return result_scrap, result_cuarentin

    def stock_update(self, folio):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.FORM_INVENTORY_ID,
            "folio":folio
            }
        record = self.cr.find_one(match_query, {'answers':1})
        answers = record.get('answers')
        if answers:
            res = self.get_product_map(answers, 'field_id_2_model')
            self.update_calc_fields( product_code=res.get('product_code'), warehouse=res.get('warehouse'), \
                lot_number=res.get('product_lot'), location=res.get('location'))
        return record

    def sync_catalog(self, folio):
        record = self.get_inventory_record_by_folio(folio, self.FORM_INVENTORY_ID)
        self.process_record_to_catalog( record )

    def update_calc_fields(self, product_code, warehouse, lot_number, folio=None, location=None, map_type='model_2_field_id', **kwargs):
        '''
        stock = {
            'production':'Production',
            'move_in':'move_in',
            'move_out':'move_out',
            'scrapped':'scrapped',
            'cuarentin':'cuarentin',
            'sales':'sales',
            'adjustments':'adjustments',
            'actuals':'actuals',
        }
        '''
        query_dict = {
            'product_code':product_code,
            'warehouse':warehouse,
            'product_lot':lot_number,
        }
        if location:
            query_dict.update({'location':location,})

        stock = self.get_product_stock(product_code, warehouse=warehouse, lot_number=lot_number, **kwargs)
        #production = self.stock_production( product_code=product_code, lot_number=lot_number)
        #scrap , cuarentine = self.stock_scrap( product_code=product_code, lot_number=lot_number, status='done')
        # if production:
        #     stock['scrap_perc'] = round(stock.get('scrapped',0)/stock.get('production',1),2)
        if stock['actuals'] <= 0:
            stock['status'] = 'done'
        else:
            stock['status'] = 'active'
        update_values = self.get_product_map(stock)
        if not folio:
            inv = self.get_invtory_record_by_product(self.FORM_INVENTORY_ID, lot_number, warehouse, product_code)
            if inv:
                folio = inv.get('folio')
        if not folio:
            return None
        query_dict = {'from_id':self.FORM_INVENTORY_ID, 'folio':folio}
        match_query = self.get_stock_query(query_dict)
       # get_match_query = get_product_map(, query_dict, map_type='model_2_field_id')
        update_res = self.cr.update_one(match_query, {'$set':update_values})
        if update_res.acknowledged:
            if folio:
                self.sync_catalog(folio)
        return update_res

    def update_log_grading(self):
        answers = self.current_record.get('answers',{})
        gradings = answers[self.f['grading_group']]
        rec_date = answers[self.f['grading_date']]
        grading_type = answers[self.f['grading_date']]
        plant_info = answers[self.CATALOG_INVENTORY_OBJ_ID]
        product_lot = plant_info.get(self.f['product_lot'])
        product_code = plant_info.get(self.f['product_code'])
        warehouse = plant_info.get(self.f['warehouse'])
        product_stock = self.get_product_stock(product_code, warehouse=warehouse, lot_number=product_lot)
        print('product_stock=',product_stock)
        grading_totals = self.get_grading_sublots(gradings)
        totals = sum(x for x in grading_totals.values())
        print('totals',totals)
        acctual_containers = product_stock['actuals']