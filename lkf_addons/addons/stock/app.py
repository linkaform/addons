# -*- coding: utf-8 -*-

from datetime import timedelta, datetime
import math, simplejson, time
from copy import deepcopy
from bson import ObjectId

from linkaform_api import base

# from lkf_addons.addons.employee.app import Employee
# from lkf_addons.addons.product.app import Product, Warehouse

# from lkf_addons.addons.jit.app import JIT
from lkf_addons.addons.base.app import Base


class Stock(Base):

    def __init__(self, settings, folio_solicitud=None, sys_argv=None, use_api=False, **kwargs):
        #base.LKF_Base.__init__(self, settings, sys_argv=sys_argv, use_api=use_api)
        super().__init__(settings, sys_argv=sys_argv, use_api=use_api, **kwargs)
        self.kwargs['MODULES'] = self.kwargs.get('MODULES',[])
        if self.__class__.__name__ not in kwargs:
            self.kwargs['MODULES'].append(self.__class__.__name__)
        # self.load('JIT', **self.kwargs)
        self.load(module='Product', **self.kwargs)
        self.load(module='Product', module_class='Warehouse', import_as='WH', **self.kwargs)
        # if not  self.__dict__.get('STOCK'):
        #     self.STOCK =True
        #     print('ssssssssshasattr', hasattr(self, 'JIT'))
        #     print('43242342342342343242342343242====',)
        #     self.JIT =True
        #     print('ssssssssssssssdir self', dir(self))
        #     self.JIT = JIT( settings, sys_argv=sys_argv, use_api=use_api, **kwargs)
        self.name =  __class__.__name__
        self.settings = settings

        self.STOCK_INVENTORY = self.lkm.catalog_id('stock_inventory',{} )
        self.STOCK_INVENTORY_ID = self.STOCK_INVENTORY.get('id')
        self.STOCK_INVENTORY_OBJ_ID = self.STOCK_INVENTORY.get('obj_id')

        # self.STOCK_INVENTORY = self.lkm.catalog_id('stock_inventory')
        # self.STOCK_INVENTORY_ID = self.STOCK_INVENTORY.get('id')
        ###### depricated ######
        self.CATALOG_INVENTORY = self.lkm.catalog_id('stock_inventory')
        self.CATALOG_INVENTORY_ID = self.CATALOG_INVENTORY.get('id')
        self.CATALOG_INVENTORY_OBJ_ID = self.CATALOG_INVENTORY.get('obj_id')
        ########################

        self.FORM_INVENTORY_ID = self.lkm.form_id('stock_inventory','id')
        self.ADJUIST_FORM_ID = self.lkm.form_id('stock_inventory_adjustment','id')
        self.STOCK_INVENTORY_ADJUSTMENT_ID = self.lkm.form_id('stock_inventory_adjustment','id')
        # self.STOCK_MOVE_FORM_ID = self.lkm.form_id('stock_inventory_move','id')
        # self.STOCK_MANY_LOCATION_OUT = self.lkm.form_id('stock_move_many_out','id')
        # self.MOVE_NEW_PRODUCTION_ID = self.lkm.form_id('stock_move_new_production','id')
        # self.PRODUCTION_FORM_ID = self.lkm.form_id('stock_production','id')
        self.SCRAP_FORM_ID = self.lkm.form_id('stock_scrapping','id')
        # self.STOCK_MANY_LOCATION_2_ONE = self.lkm.form_id('stock_move_many_one_one','id')
        # self.STOCK_MANY_ONE_ONE = self.lkm.form_id('stock_move_many_one_one','id')
        self.STOCK_ONE_MANY_ONE = self.lkm.form_id('stock_move_one_many_one','id')
        self.STOCK_IN_ONE_MANY_ONE = self.lkm.form_id('recepcion_de_materiales_de_proveedor','id')

        self.STOCK_ONE_MANY_ONE_FORMS = [
            self.STOCK_ONE_MANY_ONE,
            # self.STOCK_MANY_ONE_ONE,
            self.STOCK_IN_ONE_MANY_ONE
            ]

        if self.FORM_INVENTORY_ID:
            self.FORM_CATALOG_DIR = {
                self.FORM_INVENTORY_ID: self.CATALOG_INVENTORY_ID, #Inventory Flow (greenHouse)
                }

        self.container_per_rack = {
                'Baby Jar': 38,
                'baby_jar': 38,
                'Magenta Box': 24,
                'magenta_box': 24,
                'Box': 24,
                'box': 24,
                'Clam Shell': 8,
                'clam_shell': 8,
                'setis': 1,
                'Setis': 1,
            }

        self.SOL_METADATA = {}
        self.SOL_CATALOG = {}
        # self.f stands for field 
        # self.f is use to realte a human name to a objectId where the ObjectId
        # ex: self.f = {'key':'ObjectId'}

        self.f.update({
            'actual_eaches_on_hand':'620ad6247a217dbcb888d172',
            'actuals':'6441d33a153b3521f5b2afc9',
            'adjustments':'aaaaa0000000000000000000',
            'cat_stock_folio':'62c44f96dae331e750428732',
            'cuarentin':'6442e2fbc0dd855fe856fddd',
            'grading_date':'000000000000000000000111',
            'grading_flats':'644bf9a04b1761305b080013',
            'grading_group':'644bf7ccfa9830903f087867',
            'grading_move_type':'64d5550ec4909ab3c20c5806',
            'grading_ready_week':'644bf9a04b1761305b080011',
            'grading_ready_year':'644bf9a04b1761305b080012',
            'grading_ready_yearweek':'64edf8aeffeaaa1febca2a06',
            'grading_type':'653885f30d80af8e8de0fe79',
            'inv_adjust_comments':'64d05792c373f9b62f539d00',
            'inv_adjust_grp_comments':'ad00000000000000000ad400',
            'inv_adjust_grp_in':'ad00000000000000000ad100',
            'inv_adjust_grp_out':'ad00000000000000000ad200',
            'inv_adjust_grp_qty':'ad00000000000000000ad000',
            'inv_adjust_grp_status':'ad00000000000000000ad999',
            'inv_adjust_status':'6442e4537775ce64ef72dd6a',
            'inv_cuarentin_qty':'644bf9a04b1761305b080098',
            'inv_group_flats':'644bf6c2d281661b082b6349',
            'inv_group_readyweek':'644bf6c2d281661b082b6348',
            'inv_group':'644bf504f595b744814a4990',
            'inv_move_qty':'6442e4537775ce64ef72dd68',
            'inv_scrap_qty':'644bf9a04b1761305b080099',
            'inv_scrap_status':'644c1cb6dc502afa06c4423e',
            'inventory_status':'620ad6247a217dbcb888d175',
            'lot_number':'620a9ee0a449b98114f61d77',
            'media_lot':'62e948f79928ba006783dc5c',
            'media_name':'61ef43c226fd42cc223c98f7',
            'move_dest_folio':'ffff00000000000000000001',
            'move_group_qty':'6442e4cc45983bf1778ec17d',
            'move_group':'6442e4537775ce64ef72dd69',
            'move_in':'620ad6247a217dbcb888d000',
            'move_new_location':'644897497a16141f4e5ee0c3',
            'move_out':'620ad6247a217dbcb888d17e',
            'move_status':'62e9d296cf8d5b373b24e028',
            'move_qty_requested':'65e1169689c0e0790f8843f1',
            'new_location_containers':'6319404d1b3cefa880fefcc8',
            'new_location_group':'63193fc51b3cefa880fefcc7',
            'new_location_racks':'c24000000000000000000001',
            'per_container':'6205f73281bb36a6f157335b',
            'plant_contamin_code':'6441d33a153b3521f5b2afcb',
            'plant_conteiner_type':'620ad6247a217dbcb888d16f',
            'plant_cut_day':'620a9ee0a449b98114f61d76',
            'plant_cut_year':'620a9ee0a449b98114f61d75',
            'plant_cut_yearweek':'620a9ee0a449b98114f61d75',
            'plant_cycle':'620ad6247a217dbcb888d168',
            'plant_group':'620ad6247a217dbcb888d167',
            'plant_multiplication_rate':'645576e878f3060d1f7fc61b',
            'plant_next_cutweek':'6442e25f13879061894b4bb1',
            'plant_per_container':'620ad6247a217dbcb888d170',
            'plant_stage':'621007e60718d93b752312c4',
            'prod_qty_per_container':'6205f73281bb36a6f157335b',
            'product_code':'61ef32bcdf0ec2ba73dec33d',
            'product_container_type':'6441d33a153b3521f5b2afcb',
            'product_estimated_ready_date':'6442e25f13879061894b4bb1',
            'product_grading_pending':'644c36f1d20db114694a495a',
            'product_growth_week':'645576e878f3060d1f7fc61b',
            'product_lot_actuals':'6441d33a153b3521f5b2afc9',
            'product_lot_adjustments':'aaaaa0000000000000000000',
            'product_lot_created_week':'620a9ee0a449b98114f61d75',
            'product_lot_cuarentin':'6442e2fbc0dd855fe856fddd',
            'product_lot_location':'63c9f28ddaebf7e9b4522551',
            'product_lot_move_in':'620ad6247a217dbcb888d000',
            'product_lot_move_out':'620ad6247a217dbcb888d17e',
            'product_lot_per_scrap':'6442e25f13879061894b4bb3',
            'product_lot_produced':'6271dc35e84e2577579eafeb',
            'product_lot_proyected_qty':'6442e25f13879061894b4bb2',
            'product_lot_sales':'6442e2fbc0dd855fe856f1da',
            'product_lot_scrapped':'620ad6247a217dbcb888d16d',
            'product_lot':'620a9ee0a449b98114f61d77',
            'product_name':'61ef32bcdf0ec2ba73dec33e',
            'product_recipe':'61ef32bcdf0ec2ba73dec33c',
            'production_containers_in':'61f1fcf8c66d2990c8fc7cc2',
            'production_contamin_code':'ff0000000000000000000001',
            'production_cut_day':'620a9ee0a449b98114f61d76',
            'production_cut_week':'622bb9946d0d6fef17fe0842',
            'production_eaches_req':'642dbe5638a8255f77dcdad6',
            'production_estimated_hrs':'ab0000000000000000000111',
            'production_folio':'62fc62dfb26856412d2fe4ca',
            'production_group_estimated_hrs':'ab000000000000000000a111',
            'production_group':'61f1fab3ce39f01fe8a7ca8c',
            'production_left_overs':'61f1fd95ef44501511f7f161',
            'production_lote':'63f8f4cad090912501be306a',
            'production_multiplication_rate':'61f1fcf8c66d2990c8fc7cc8',
            'production_order_status':'62fbbf2587546d976e05dc7b',
            'production_per_container_in':'aa0000000000000000000001',
            'production_requier_containers':'62e4bc58d9814e169a3f6beb',
            'production_status':'62e9890c5dec95745c618fc3',
            'production_total_containers':'63f6de096468162a9a3c2ef4',
            'production_total_eaches':'63f6e1733b076aaf80ff4adb',
            'production_week':'62e8343e236c89c216a7cec3',
            'production_working_cycle':'cc0000000000000000000001',
            'production_working_group':'dd0000000000000000000001',
            'production_year':'61f1da41b112fe4e7fe8582f',
            'production':'6271dc35e84e2577579eafeb',
            'recipe_type':'63483f8e2c8c769718b102b1',
            'sku_package':'6209705080c17c97320e3382',
            'sku_container':'6209705080c17c97320e3382',
            'reicpe_end_week':'6209705080c17c97320e3381',
            'reicpe_growth_weeks':'6205f73281bb36a6f1573357',
            'reicpe_mult_rate':'6205f73281bb36a6f157334d',
            'reicpe_overage':'6205f73281bb36a6f1573353',
            'reicpe_per_container':'6205f73281bb36a6f157335b',
            'reicpe_productiviy':'6209705080c17c97320e337f',
            'reicpe_soil_type':'6209705080c17c97320e3383',
            'reicpe_stage':'6205f73281bb36a6f1573358',
            'reicpe_stage':'621fca56ee94313e8d8c5e2e',
            'reicpe_start_size':'6205f73281bb36a6f1573358',
            'reicpe_start_size':'621fca56ee94313e8d8c5e2e',
            'reicpe_start_week':'6209705080c17c97320e3380',
            'sales':'6442e2fbc0dd855fe856f1da',
            'scrap_perc':'6442e25f13879061894b4bb3',
            'scrapped':'620ad6247a217dbcb888d16d',
            'set_lunch_brake':'62c6017ff9f71e2a589fb679',
            'set_production_date_out':'61f1fcf8c66d2990c8fcccc6',
            'set_production_date':'61f1fcf8c66d2990c8fc7cc4',
            'set_products_per_hours':'61f1fcf8c66d2990c8fc7cc9',
            'set_total_hours':'61f1fcf8c66d2990c8fc7cc7',
            'set_total_produced':'61f1fcf8c66d2990c8fc7cc3',
            'status':'620ad6247a217dbcb888d175',
            'stock_status':'6442e4537775ce64ef72dd6a',
            'time_in':'61f1fcf8c66d2990c8fc7cc5',
            'time_out':'61f1fcf8c66d2990c8fc7cc6',
            'total_produced':'64ed5839a405d8f6378edf5f',
            'warehouse_dest':'65bdc71b3e183f49761a33b9',
            'warehouse_location_dest':'65c12749cfed7d3a0e1a341b',
            'warehouse_location':'65ac6fbc070b93e656bd7fbe',
            'warehouse_type':'6514f51b6cfe23860299abfa',
            'warehouse':'6442e4831198daf81456f274',
            'weekly_production_group':'62e4babc46ff76c5a6bee76c',
            'worker_name':'62c5ff407febce07043024dd',
            'worker_obj_id':'62c5ff243c63280985580087',
        })
       
        self.f.update(self.Product.f)

        self.f.update(self.WH.f)
        
    def add_dicts(self, dict1, dict2):
        for key in dict1:
            dict1[key] += dict2.get(key,0)
        return dict1

    def add_racks_and_containers(self, container_type, racks, containers):
        print('TODO: SETUP UOM MODULE')
        try:
            continers_per_rack = self.container_per_rack[container_type] 
        except:
            continers_per_rack = 1
        container_on_racks = racks * continers_per_rack
        qty = containers + container_on_racks
        return qty

    def do_scrap(self):
        answers = self.answers
        scrap_qty = answers.get(self.f['inv_scrap_qty'], 0)
        cuarentin_qty = answers.get(self.f['inv_cuarentin_qty'], 0)
        product_info = answers.get(self.STOCK_INVENTORY_OBJ_ID,{})
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
                        'warehouse': warehouse,
                        'record_id':self.record_id
                        })
        move_qty = scrap_qty + cuarentin_qty
        if move_qty > actuals:
            self.sync_catalog(folio_inventory)
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
        production_recipe = self.answers.get(self.f['product_recipe'], {})
        prod_status = self.answers.get(self.f['production_left_overs'],'')
        team = self.answers.get(self.TEAM_OBJ_ID).get(self.f['team_name'])
        qty_per_container = production_recipe.get(self.f['reicpe_per_container'], [])
        if qty_per_container:
            if type(qty_per_container) == list and qty_per_container[0]:
                qty_per_container = int( qty_per_container[0] )
            else:
                qty_per_container = int(qty_per_container)
        else:
            qty_per_container = 0
        from_stage = production_recipe.get(self.f['reicpe_start_size'])
        to_stage = production_recipe.get(self.f['reicpe_stage'])
        is_S2_to_S3 = True if from_stage == 'S2' and to_stage == 'S3' else False

        #inv_qty_per_container = 0
        total_left_overs = 0
        move_inventory = []
        per_container_selected = int(self.answers.get(self.f['production_per_container_in'],0 ))
        worked_containers = []
        total_picked_containers = 0

        total_container_out = 0
        total_container_out_progress = 0
        total_container_used = 0
        mult_out = 0
        mult_in = 0
        weighted_mult_rate = 0
        for production in self.answers.get(self.f['production_group'], []):
            """
            ##################################################
            # Calculate Total Hours
            ##################################################
            """
            production_status = production.get(self.f['production_status'],'progress')
            containers_in = float(production.get(self.f['production_containers_in'],0))
            containers_out = float(production.get(self.f['set_total_produced'],0))
            total_container_out += containers_out
            print('production_status', production_status)
            if production_status == 'progress':# or production_status == 'posted':
                date_in = production.get(self.f['set_production_date'])
                time_in = production.get(self.f['time_in'])
                date_out = production.get(self.f['set_production_date_out'], date_in)
                time_out = production.get(self.f['time_out'])
                print('dateout', date_out)
                print('time_out', time_out)
                cutter = production.get(self.EMPLOYEE_OBJ_ID,{}).get(self.f['worker_name'])
                d_time_in =  datetime.strptime('{} {}'.format(date_in,time_in), '%Y-%m-%d %H:%M:%S')
                d_time_out = datetime.strptime('{} {}'.format(date_out,time_out), '%Y-%m-%d %H:%M:%S')
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
                luch_brake = production.get(self.f['set_lunch_brake'])
                if luch_brake == 'sí':
                    total_hours -= 0.5
                production[self.f['set_total_hours']] = round(total_hours, 2) # Total Hours

                """
                ##################################################
                # Calculate Multiplication Rate
                ##################################################
                """
                total_container_used += containers_in
                mult_out +=  (containers_out * qty_per_container)
                mult_in +=  float( containers_in * per_container_selected )
                multiplication_rate = (containers_out * qty_per_container) / float( containers_in * per_container_selected )
                production[self.f['production_multiplication_rate']] = round(multiplication_rate, 2) # Multiplication Rate

                """
                ##################################################
                # Calculate Plants per Hour
                # Cuantas plantas se hacen por hora
                ##################################################
                """
                total_plants = qty_per_container * containers_out
                if total_hours <= 0:
                    t_in = d_time_in.strftime('%H:%M')
                    t_out = d_time_out.strftime('%H:%M')
                    msg = "Double check your time in {} and time out {} input, of {}.".format(t_in, t_out, cutter)
                    msg_error_app = {
                             self.f['time_in']: {"msg": [msg], "label": "Please check your Time In. ", "error": []},
                             self.f['time_out']: {"msg": [msg], "label": "Please check your Time Out. ", "error": []}
                         }
                    self.LKFException( simplejson.dumps( msg_error_app ) )
                plants_per_hour = total_plants / float(total_hours)

                production[self.f['set_products_per_hours']] = round(plants_per_hour, 2) # Plants per Hour

                """
                ##################################################
                # Genera registro para almacenar nueva produccion
                # Cambia status de produccion a posted
                ##################################################
                """
                total_container_out_progress += containers_out
                production[self.f['production_status']] = 'posted'

                # remainding_cont = 0
                weighted_mult_rate = round(mult_out/mult_in, 2)
        
        self.answers[self.f['total_produced']] = total_container_out
        
        if prod_status == 'finished':
            self.answers[self.f['production_order_status']] = 'done'
            #remainding_cont = total_picked_containers - total_container_used - total_left_overs
            # print('the math picked - used - left = 0 / {} - {} - {} = {}'.format(total_picked_containers,
            # total_container_used, total_left_overs ,remainding_cont ))

            # if remainding_cont != 0:
            #     msg = "There are {} container  remainding. Picked Containers {} - Containers IN {} - Left Overs {} != 0".format(remainding_cont,
            #         total_picked_containers, total_container_used, total_left_overs)
            #     msg_error_app = {
            #              "62e98cb229e764936db75244": {"msg": [msg], "label": "Please check your Left Overs. ", "error": []}
            #          }
            #     raise Exception( simplejson.dumps( msg_error_app ) )

        if total_container_out_progress > 0:
            new_prod_line = self.get_production_move(total_container_out_progress, weighted_mult_rate, d_time_out)
            response_create = self.create_production_move(new_prod_line)
            status_code = response_create.get('status_code')
            if status_code >= 400:
                msg_error_app = response_create.get('json', 'Error de Script favor de reportrar con Admin')
                self.LKFException( simplejson.dumps(msg_error_app) )

        """
        ##################################################
        # Si hay sobrantes Crea el registro
        ##################################################
        """
        # print('prod_status=',prod_status)
        # if prod_status == 'finished':
        #     #adjust_inventory_flow(worked_containers)
        #     #create_move_line(current_record, move_inventory)
        #     self.answers[self.f['production_status']] = 'done'
        #     sys.stdout.write(simplejson.dumps({
        #         'status': 101,
        #         'replace_ans': self.answers,
        #     }))
        # else:
        #     self.answers[self.f['production_status']] = 'in_progress'
        #     sys.stdout.write(simplejson.dumps({
        #         'status': 101,
        #         'replace_ans': self.answers
        #     }))

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
            print(stop)
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
                self.WAREHOUSE_OBJ_ID: {self.f['warehouse']:warehouse},
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
                    'warehouse': warehouse,
                    'record_id':self.record_id
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
                'warehouse': warehouse,
                'record_id':self.record_id
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

    def create_inventory_flow(self, answers):
        #data es un json con answers y folio. Que puede ser el current record
        # answers_to_new_record['620ad6247a217dbcb888d176'] = 'todo' # Post Status
        product_code, sku, lot_number, warehouse, location = self.get_product_lot_location(answers)
        print('product_code',product_code)
        print('warehouse',warehouse)
        print('location',location)
        print('lot_number',lot_number)
        print('sku',sku)
        product_exist = self.product_stock_exists(product_code, sku=sku,  lot_number=lot_number, warehouse=warehouse, location=location)
        print('product_exist',product_exist)
        if product_exist:
            # res = self.update_calc_fields(product_code, lot_number, warehouse, location=location)
            res = self.update_stock(answers=product_exist.get('answers'), form_id=product_exist.get('form_id'), folios=product_exist.get('folio') )
            return res
        else:
            print('NO EXISTE==================================')
            metadata = self.lkf_api.get_metadata(self.FORM_INVENTORY_ID)
            metadata.update({
                'properties': {
                    "device_properties":{
                        "system": "Script",
                        "process": answers.get('process', 'Inventory Move'),
                        "action": answers.get('action', 'Create record Inventory Flow'),
                        "from_folio":self.folio,
                        "script":"make_inventory_flow.py",
                        "module":"stock_lab",
                        "function": "create_inventory_flow",
                    }
                },
                'answers': answers
                })
        return {'new_record':metadata}

    def create_proudction_lot_number(self, prod_date=None, group=None, cycle=None):
        if not prod_date:
            year = today.strftime('%Y')
            day_num = today.strftime('%j')
        else:
            year = prod_date.strftime('%Y')
            day_num = prod_date.strftime('%j')
        if not group:
            group = self.answers.get(self.f['production_working_group'])
        if not cycle:
            cycle = self.answers.get(self.f['production_working_cycle'])
        lot_number = f"{year}{day_num}-{group}{cycle}"
        return lot_number

    def create_production_move(self, new_production):
        print('self.MOVE_NEW_PRODUCTION_ID')
        metadata = self.lkf_api.get_metadata(form_id=self.MOVE_NEW_PRODUCTION_ID, user_id=self.record_user_id )
        metadata.update({
            'properties': {
                "device_properties":{
                    "System": "Script",
                    "Module": "Stock Lab",
                    "Process": "Production Left Overs",
                    "Action": 'Return Inventroy',
                    "From Folio": self.folio,
                    "File": "stock_utils.py"
                }
            },
        })
        print('aqui va a asginmar el folio', self.folio)
        # metadata['folio'] = self.create_poruction_lot_number()
        metadata.update({'answers':new_production})
        response_create = self.lkf_api.post_forms_answers(metadata)
        return response_create

    def del_catalog_record(self, record_catalog, form_id):
        if record_catalog:
            for info_record_catalog in record_catalog:
                resp_delete = self.lkf_api.delete_catalog_record(
                    self.FORM_CATALOG_DIR[form_id], 
                    info_record_catalog.get('_id'), 
                    info_record_catalog.get('_rev'), 
                    jwt_settings_key='APIKEY_JWT_KEY')
                return resp_delete

    def do_scrap(self):
        answers = self.answers
        stock = self.get_stock_info_from_catalog_inventory()
        scrap_qty = answers.get(self.f['inv_scrap_qty'], 0)
        cuarentin_qty = answers.get(self.f['inv_cuarentin_qty'], 0)
        if scrap_qty or cuarentin_qty:
            move_qty = scrap_qty + cuarentin_qty
            self.validate_move_qty(stock['product_code'], stock['sku'], stock['lot_number'], stock['warehouse'], stock['warehouse_location'], move_qty, date_to=None)
            self.cache_set({
                        '_id': f"{stock['product_code']}_{stock['sku']}_{stock['lot_number']}_{stock['warehouse']}_{stock['warehouse_location']}",
                        'scrapped':scrap_qty,
                        'cuarentin':cuarentin_qty,
                        'lot_number':stock['lot_number'],
                        'product_code':stock['product_code'],
                        'sku':stock['sku'],
                        'warehouse': stock['warehouse'],
                        'warehouse_location': stock['warehouse_location'],
                        'record_id': self.record_id
                        })
        res = self.update_stock(answers={}, form_id=self.FORM_INVENTORY_ID, folios=stock['folio'] )
        return res.get(stock['folio'],{}) 
   
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

    def get_grading(self):
        match_query ={ 
         'form_id': self.GREENHOUSE_GRADING_ID,  
         'deleted_at' : {'$exists':False},
         f'answers.{self.STOCK_INVENTORY_OBJ_ID}.{self.f["cat_stock_folio"]}': self.folio
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

    def get_group_skus(self, products):
        search_codes = {}
        for product in products:
            product_code =  product.get('product_code')
            if not product_code:
                product_code = product[self.Product.SKU_OBJ_ID][self.f['product_code']]
            sku =  self.unlist(product.get('sku'))
            if not sku:
                sku = self.unlist(product[self.Product.SKU_OBJ_ID][self.f['sku']])
            search_codes[product_code] = search_codes.get(product_code, [])
            search_codes[product_code].append(sku)
            if sku not in search_codes[product_code]:
                search_codes[product_code].append(sku)
        skus = self.get_product_sku(search_codes)
        return skus

    def get_inventory_record_by_folio(self, folio=None, form_id=None ):
        #use to be get_inventory_flow
        if not folio:
            folio = self.folio
        if not form_id:
            form_id = self.form_id
        record_inventory = self.cr.find_one({
            'form_id': form_id,
            'deleted_at': {'$exists': False},
            'folio': folio
        }, {'answers': 1, 'folio': 1, 'form_id': 1, '_id': 1})
        return record_inventory

    def get_invtory_record_by_product(self, form_id, product_code, sku, lot_number, warehouse, location, **kwargs):
        #use to be get_record_greenhouse_inventory
        get_many = kwargs.get('get_many')
        query_warehouse_inventory = {
            'form_id': form_id,
            'deleted_at': {'$exists': False},
            f"answers.{self.Product.SKU_OBJ_ID}.{self.f['product_code']}": product_code,
            f"answers.{self.Product.SKU_OBJ_ID}.{self.f['sku']}": sku,
            f"answers.{self.f['product_lot']}": lot_number,
            f"answers.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.f['warehouse']}": warehouse,
            f"answers.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.f['warehouse_location']}": location,
        }
        if get_many:
            records = self.cr.find(query_warehouse_inventory, 
                {'folio': 1, 'answers': 1, 'form_id': 1, 'user_id': 1,'created_at':1}).sort('created_at')
            record = [x for x in records]
        else:
            record = self.cr.find_one(query_warehouse_inventory, {'folio': 1, 'answers': 1, 'form_id': 1, 'user_id': 1})
        return record
   
    def get_product_lot_location(self, answers=None):
        if not answers:
            answers = self.answers
        product_code = answers.get(self.Product.SKU_OBJ_ID,{}).get(self.f['product_code'])
        sku = answers.get(self.Product.SKU_OBJ_ID,{}).get(self.f['sku'])
        lot_number = answers.get(self.f['product_lot'])
        warehouse = answers.get(self.WH.WAREHOUSE_LOCATION_OBJ_ID,{}).get(self.f['warehouse'])
        location = answers.get(self.WH.WAREHOUSE_LOCATION_OBJ_ID,{}).get(self.f['warehouse_location'])
        return product_code, sku, lot_number, warehouse, location

    def get_product_recipe(self, all_codes, stage=[2,3,4], recipe_type='Main'):
        if type(all_codes) == str and all_codes:
            all_codes = [all_codes.upper(),]
        recipe = {}
        recipe_s2 = []
        recipe_s3 = []
        recipe_s4 = []
        stage = [2,] if stage == 'S2' else stage
        stage = [3,] if stage == 'S3' else stage
        stage = [4,] if stage == 'S4' else stage
        print('get_product_recipe=')
        print('stage=',stage)
        print('all_codes=',all_codes)
        if 2 in stage:
            mango_query = self.plant_recipe_query(all_codes, "S2", "S2", recipe_type)
            recipe_s2 = self.lkf_api.search_catalog(self.CATALOG_PRODUCT_RECIPE_ID, mango_query)
        if 3 in stage:
            mango_query = self.plant_recipe_query(all_codes, "S2", "S3", recipe_type)
            print('mango_query', mango_query)
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
                    'media_tray':this_recipe.get(self.f['sku_container']),
                    'per_container':this_recipe.get(self.f['reicpe_per_container']),
                    'S2_mult_rate':this_recipe.get(self.f['reicpe_mult_rate']),
                    'S2_overage':this_recipe.get(self.f['reicpe_overage']),
                    'plant_code':this_recipe.get(self.f['product_code'],),
                    'product_code':this_recipe.get(self.f['product_code'],),
                    'plant_name':this_recipe.get(self.f['product_name'],['',])[0],
                    'product_name':this_recipe.get(self.f['product_name'],['',])[0],
                    'start_week' : this_recipe.get(self.f['reicpe_start_week']),
                    'end_week' : this_recipe.get(self.f['reicpe_end_week']),
                    'start_size': this_recipe.get(self.f['reicpe_start_size']),
                    'stage': this_recipe.get(self.f['reicpe_stage']),
                    'recipe_type': this_recipe.get(self.f['recipe_type']),
                    })
        if recipe_s3  and not recipe:
            for this_recipe in recipe_s3:
                plant_code = this_recipe.get(self.f['product_code'])
                if not recipe.get(plant_code):
                    recipe[plant_code] = {}
                recipe[plant_code].update(
                    {'S3_growth_weeks':this_recipe.get(self.f['reicpe_growth_weeks']),
                    'cut_productivity':this_recipe.get(self.f['reicpe_productiviy']),
                    'media_tray':this_recipe.get(self.f['sku_container']),
                    'per_container':this_recipe.get(self.f['reicpe_per_container']),
                    'plant_code':this_recipe.get(self.f['product_code']),
                    'S3_mult_rate':this_recipe.get(self.f['reicpe_mult_rate']),
                    'S3_overage':this_recipe.get(self.f['reicpe_overage']),
                    'plant_code':this_recipe.get(self.f['product_code'],),
                    'plant_name':this_recipe.get(self.f['product_name'],['',])[0],
                    'product_code':this_recipe.get(self.f['product_code'],),
                    'product_name':this_recipe.get(self.f['product_name'],['',])[0],
                    'start_week' : this_recipe.get(self.f['reicpe_start_week']),
                    'end_week' : this_recipe.get(self.f['reicpe_end_week']),
                    'start_size': this_recipe.get(self.f['reicpe_start_size']),
                    'stage': this_recipe.get(self.f['reicpe_stage']),
                    'recipe_type': this_recipe.get(self.f['recipe_type']),
                    }
                    )
        if recipe_s4  and not recipe:
            for this_recipe in recipe_s4:
                plant_code = this_recipe.get(self.f['product_code'])
                if not recipe.get(plant_code):
                    recipe[plant_code] = []
                recipe[plant_code].append(
                    {'S4_growth_weeks':this_recipe.get(self.f['reicpe_growth_weeks']),
                    'media_tray':this_recipe.get(self.f['sku_container']),
                    'cut_productivity':this_recipe.get(self.f['reicpe_productiviy']),
                    'per_container':this_recipe.get(self.f['reicpe_per_container']),
                    'S4_mult_rate':this_recipe.get(self.f['reicpe_mult_rate']),
                    'S4_overage_rate':this_recipe.get(self.f['reicpe_overage']),
                    'S4_overage': this_recipe.get(self.f['reicpe_overage']),
                    'plant_code':this_recipe.get(self.f['product_code'],),
                    'plant_name':this_recipe.get(self.f['product_name'],['',])[0],
                    'product_code':this_recipe.get(self.f['product_code'],),
                    'product_name':this_recipe.get(self.f['product_name'],['',])[0],
                    'start_week' : this_recipe.get(self.f['reicpe_start_week']),
                    'end_week' : this_recipe.get(self.f['reicpe_end_week']),
                    'start_size': this_recipe.get(self.f['reicpe_start_size']),
                    'stage': this_recipe.get(self.f['reicpe_stage']),
                    'soil_type': this_recipe.get(self.f['reicpe_soil_type']),
                    'recipe_type': this_recipe.get(self.f['recipe_type']),
                    }
                    )
        if not recipe:
            return {}
        return recipe

    def ger_products_inventory(self, product_code, warehouse, status='active'):

        match_query ={ 
         'form_id': self.FORM_INVENTORY_ID,  
         'deleted_at' : {'$exists':False},
         } 

        if product_code:
            match_query.update({f"answers.{self.Product.SKU_OBJ_ID}.{self.f['product_code']}":{"$in":product_code}}) 
        if warehouse:
            match_query.update({f"answers.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.f['warehouse']}":warehouse}) 
        query = [
            {'$match': match_query},
            {'$project':{
                '_id':0,
                'product_code':f"$answers.{self.Product.SKU_OBJ_ID}.{self.f['product_code']}",
                'warehouse':f"$answers.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.f['warehouse']}",
                'actuals':f"$answers.{self.f['actual_eaches_on_hand']}",
            }},
            {'$group':{
                '_id':{
                    'product_code':'$product_code',
                    'warehouse':'$warehouse'
                },
                'actuals':{'$sum':'$actuals'}
            }},
            {"$project":{
                "_id":0,
                "product_code":"$_id.product_code",
                "warehouse":"$_id.warehouse",
                "actuals": "$actuals"
            }},
        ]
        
        print('query=',simplejson.dumps(query, indent=5))
        res = self.format_cr(self.cr.aggregate(query))
        return res

    def get_product_sku(self, all_codes):
        all_sku = []
        for sku, product_code in all_codes.items():
            if sku not in all_sku:
                all_sku.append(sku.upper())
        skus = {}
        mango_query = self.product_sku_query(all_sku)
        sku_finds = self.lkf_api.search_catalog(self.Product.SKU_ID, mango_query)
        for this_sku in sku_finds:
                product_code = this_sku.get(self.f['product_code'])
                skus[product_code] = skus.get(product_code, {})
                skus[product_code].update({
                    'sku':this_sku.get(self.f['sku']),
                    'product_name':this_sku.get(self.f['product_name']),
                    'product_category':this_sku.get(self.f['product_category']),
                    'product_type':this_sku.get(self.f['product_type']),
                    'product_department':this_sku.get(self.f['product_department']),
                    'sku_color':this_sku.get(self.f['sku_color']),
                    'sku_image':this_sku.get(self.f['sku_image'],),
                    'sku_note':this_sku.get(self.f['sku_note'],),
                    'sku_package':this_sku.get(self.f['sku_package'],),
                    'sku_per_package':this_sku.get(self.f['reicpe_per_container'],),
                    'sku_size' : this_sku.get(self.f['sku_size']),
                    'sku_source' : this_sku.get(self.f['sku_source']),
                    })
        return skus

    def get_product_stock(self, product_code, sku=None, lot_number=None, warehouse=None, location=None, date_from=None, date_to=None,  **kwargs):
        #GET INCOME PRODUCT
        # print(f'**************Get Stock: {product_code}****************')
        # print('product_code', product_code)
        # print('sku', sku)
        # print('lot_number', lot_number)
        # print('warehouse', warehouse)
        # print('location', location)
        lot_number = self.validate_value(lot_number)
        warehouse = self.validate_value(warehouse)
        location = self.validate_value(location)
        stock = {'actuals':0,'production':0, 'stock_in':0, 'stock_out':0, 'scrapped':0, 'cuarentin':0}
        if (product_code and warehouse and lot_number) or True:
            if location:
                cache_stock = self.cache_get({'_id':f"{product_code}_{sku}_{lot_number}_{warehouse}_{location}","_one":True, },**kwargs)
            else:
                cache_stock = self.cache_get({'_id':f"{product_code}_{sku}_{lot_number}_{warehouse}","_one":True, },**kwargs)
        kwargs.update(cache_stock.get('kwargs',{}))
        kwargs.update(cache_stock.get('cache',{}).get('kwargs',{}))
        if cache_stock.get('cache',{}).get('record_id'):
            kwargs.update({"record_id":cache_stock['cache']['record_id']})
        if date_from:
            initial_stock = self.get_product_stock(product_code, sku=sku, lot_number=lot_number, \
                warehouse=warehouse, location=location, date_to=date_from,  **kwargs)
            stock['actuals'] += initial_stock.get('actuals',0)
        stock['adjustments'] = self.stock_adjustments_moves( product_code=product_code, sku=sku, lot_number=lot_number, \
            warehouse=warehouse, location=location, date_from=date_from, date_to=date_to, **kwargs)
        # print('stock adjustments', stock['adjustments'])
        stock['move_in'] = self.stock_one_many_one( 'in', product_code=product_code, sku=sku, warehouse=warehouse, location=location, lot_number=lot_number, date_from=date_from, date_to=date_to, status='done', **kwargs)
        stock['move_out'] = self.stock_one_many_one( 'out', product_code=product_code, sku=sku, warehouse=warehouse, location=location, lot_number=lot_number, date_from=date_from, date_to=date_to, status='done', **kwargs)
        # print('stock move_in', stock['move_in'])
        # print('stock move_out', stock)
        # if stock['adjustments']:
        #     #date_from = stock['adjustments'][product_code]['date']
        #     stock['adjustments'] = stock['adjustments'][product_code]['total']
        # else:
        #     stock['adjustments'] = 0

        # stock['production'] = self.stock_production(date_from =date_from, date_to=date_to ,\
        #      product_code=product_code, sku=sku, lot_number=lot_number, warehouse=warehouse, location=location )
        # print('stock production....',stock['production'])
        # stock['move_in'] = self.stock_moves('in', product_code=product_code, lot_number=lot_number, sku=sku, \
        #     warehouse=warehouse, location=location, date_from=date_from, date_to=date_to, **kwargs)
        # #GET PRODUCT EXITS
        # print('stock IN....',stock['move_in'])

        # stock['move_out'] = self.stock_moves('out', product_code=product_code, sku=sku, lot_number=lot_number, \
        #     warehouse=warehouse, location=location, date_from=date_from, date_to=date_to, **kwargs)
        # print('stock OUT....',stock['move_out'])
        scrapped, cuarentin = self.stock_scrap(product_code=product_code, sku=sku, lot_number=lot_number, \
            warehouse=warehouse, location=location, date_from=date_from, date_to=date_to, status='done', **kwargs )  
        # print('stock scrapped',scrapped)  
        stock['scrapped'] = scrapped
        stock['cuarentin'] = cuarentin


        # stock['sales']  = stock_sales(product_code=product_code, lot_number=lot_number, warehouse=warehouse )
        sales=0
        stock['sales'] = sales
        # stock['adjustments'] += self.stock_adjustments_moves(product_code=product_code, lot_number=lot_number, \
        #     warehouse=warehouse , date_from=None, date_to=None)

        stock = self.add_dicts(stock, cache_stock.get('cache',{}))
        stock['stock_in'] = stock['production'] + stock['move_in']
        stock['stock_out'] = stock['scrapped'] + stock['move_out'] + stock['sales']  + stock['cuarentin']
        stock['actuals'] += stock['stock_in'] - stock['stock_out'] + stock['adjustments']
        #update_stock(stock)
        stock['scrap_perc']  = 0
        if stock.get('stock_in') and stock.get('scrapped'):
            stock['scrap_perc'] = round(stock.get('scrapped',0)/stock.get('stock_in',1),2)
        # print('stock=', stock)
        return stock
  
    def get_plant_recipe(self, all_codes, stage=[2,3,4], recipe_type='Main' ):
        return self.get_product_recipe(all_codes, stage=stage, recipe_type=recipe_type )

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

    def get_product_info(self, **kwargs):
        try:
            warehouse = self.answers[self.WAREHOUSE_OBJ_ID][self.f['warehouse']]
            plant_code = self.answers.get(self.f['product_recipe'], {}).get(self.f['product_code'], '')
        except Exception as e:
            print('**********************************************')
            self.LKFException('Warehosue and product code are requierd')
        yearWeek = str(self.answers[self.f['product_lot_created_week']])
        year = yearWeek[:4]
        week = yearWeek[4:]
        recipes = self.get_plant_recipe( [plant_code,], stage=[4, 'Ln72'] )
        recipe = self.select_S4_recipe(recipes[plant_code], week)
        grow_weeks = recipe.get('S4_growth_weeks')
        ready_date = self.answers.get(self.f['product_lot'])
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
        overage = recipe.get('S4_overage_rate',0)
        print('recipe', recipe)
        actual_flats_on_hand = product_stock['actuals']
        proyected_flats_on_hand = math.floor(( 1 - overage) * actual_flats_on_hand)
        lot_size = self.answers.get(self.f['product_lot_produced'],0)
        if lot_size == 0:
            perc_scrapped = 0
        else:
            perc_scrapped = round(scrapped / lot_size, 2)

        real_flats_proyected = lot_size - scrapped

        if real_flats_proyected < proyected_flats_on_hand:
            proyected_flats_on_hand = real_flats_proyected

        self.answers[self.f['product_lot_produced']] = product_stock['production']
        self.answers[self.f['product_lot_move_in']] = product_stock['move_in']
        self.answers[self.f['product_lot_scrapped']] = product_stock['scrapped']
        self.answers[self.f['product_lot_move_out']] = product_stock['move_out']
        self.answers[self.f['product_lot_sales']] = product_stock['sales']
        self.answers[self.f['product_lot_cuarentin']] = product_stock['cuarentin']
        self.answers[self.f['product_lot_actuals']] = product_stock['actuals']
        self.answers[self.f['product_lot_adjustments']] = product_stock['adjustments']

        self.answers[self.f['product_lot_per_scrap']] = perc_scrapped
        self.answers[self.f['product_lot_proyected_qty']] = proyected_flats_on_hand
        self.answers[self.f['product_lot_per_scrap']] = perc_scrapped       
        self.answers[self.f['product_lot']] = ready_date
        if self.answers[self.f['product_lot_actuals']] <= 0:
            self.answers[self.f['inventory_status']] = 'done'
        else:
            self.answers[self.f['inventory_status']] = 'active'
        self.answers.update({self.f['inv_group']:self.get_grading()})
        return self.answers
 
    def get_stock_info_form_answer(self, answers={}, data={}):
        if not answers:
            answers = self.answers
        product_info = answers.get(self.STOCK_INVENTORY_OBJ_ID, answers.get(self.Product.SKU_OBJ_ID,{}))
        data['product_code'] = data.get(self.f['product_code'],self.unlist(product_info.get(self.f['product_code'])))
        data['sku'] = data.get(self.f['sku'],self.unlist(product_info.get(self.f['sku'])))
        wh_info =  self.get_stock_info_from_catalog_wl(answers, data=data)
        whd_info = self.get_stock_info_from_catalog_wld(answers, data=data)

        # searchs first on the given data, if not it searches on the warehouse location 
        # catalogs located at first level
        # if not it searches on the product info at first level
        data['warehouse'] =  data.get('warehouse',
                            wh_info.get('warehouse',
                                    self.unlist(product_info.get(self.f['warehouse']))
                            ))
        data['warehouse_location'] = data.get(self.f['warehouse_location'],
                                    wh_info.get('warehouse_location',   
                                    self.unlist(product_info.get(self.f['warehouse_location']))
                                    ))
        data['warehouse_dest'] = data.get('warehouse_dest',
                                    whd_info.get('warehouse_dest',
                                    self.unlist(product_info.get(self.f['warehouse']))
                                    ))
        data['warehouse_location_dest'] = data.get(self.f['warehouse_location_dest'],
                                    whd_info.get('warehouse_location_dest',   
                                    self.unlist(product_info.get(self.f['warehouse_location_dest']))
                                    ))
        data['lot_number'] = data.get(self.f['lot_number'],
                            self.unlist(product_info.get(self.f['product_lot']))
                            )
        data['actuals'] = data.get(self.f['actuals'],
            self.unlist(product_info.get(self.f['product_lot_actuals']))
            )
        # print('container', self.f['container'])
        # data['container'] = data.get(self.f['container'],
        #     self.unlist(product_info.get(self.f['plant_conteiner_type']))
        #     )
        data['per_container'] = data.get(self.f['per_container'],
            self.unlist(product_info.get(self.f['plant_per_container']))
            )
        folio = self.unlist(product_info.get(self.f['cat_stock_folio']))
        if folio:
            data['folio'] = folio
        return data

    def get_stock_info_from_catalog_inventory(self, answers={}, data={}, **kwargs):
        if not answers:
            answers = self.answers
        res = deepcopy(data)
        print('data=',data)
        print('answers=',answers)
        res.update(self.get_stock_info_form_answer(answers=answers, data=res))
        print('res=',res)
        if not res.get('folio'):
            kwargs['require'] = kwargs.get('require',[])
            kwargs['require'].append('folio')
        if kwargs.get('require') or kwargs.get('get_record'):
            record = self.get_invtory_record_by_product(
                self.FORM_INVENTORY_ID,
                res['product_code'],  
                res['sku'],  
                res['lot_number'] ,
                res['warehouse'],
                res['warehouse_location'])
            res['record'] = record
            for key in kwargs['require']:
                if not record:
                    msg = "******************** Something went wrong, we couldn't a record for: ***********************"
                    msg += f"Product Code {res['product_code']} / SKU: {res['sku']} /"
                    msg += f"Warehouse: {res['warehouse']} / Location: {res['warehouse_location']}"
                    self.LKFException(msg)
                if record.get(key):
                    res[key] = record.get(key)
                else:
                    res[key] = self.search_4_key(record, key)
        return res

    def get_stock_info_from_catalog_wl(self, answers={}, data={}):
        if not answers:
            answers = self.answers
        res = {}
        wh_info = answers.get(self.WH.WAREHOUSE_LOCATION_OBJ_ID, {})
        if not wh_info:
            wh_info = self.get_stock_info_from_catalog_wl(answers=self.answers, data=data)
        res['warehouse'] = data.get('warehouse',wh_info.get(self.f['warehouse']))
        res['warehouse_location'] = data.get('warehouse_location', wh_info.get(self.f['warehouse_location']))
        return res

    def get_stock_info_from_catalog_wld(self, answers={}, data={}):
        if not answers:
            answers = self.answers
        res = {}
        print('answers', answers)
        wh_info = answers.get(self.WH.WAREHOUSE_LOCATION_DEST_OBJ_ID, {})
        if not wh_info:
            wh_info = self.get_stock_info_from_catalog_wld(answers=self.answers, data=data)
        res['warehouse_dest'] = data.get('warehouse_dest',wh_info.get(self.f['warehouse_dest']))
        res['warehouse_location_dest'] = data.get('warehouse_location_dest',wh_info.get(self.f['warehouse_location_dest']))
        return res

    def get_record_catalog_del(self):
        mango_query = {
            "selector":{"answers": {}},
            "limit":1000,
            "skip":0
            }
        product_code, sku, lot_number, warehouse, location = self.get_product_lot_location()
        query = {
            self.f['product_code']:product_code,
            self.f['sku']:sku,
            self.f['product_lot']:lot_number,
            self.f['warehouse']:warehouse,
            self.f['warehouse_location']:location,
        }
        mango_query['selector']['answers'].update(query)
        if False:
            #TODO gargabe collector
            mango_query['selector']['answers'].update({self.f['inventory_status']: "Done"})
        res = self.lkf_api.search_catalog( self.FORM_CATALOG_DIR[self.form_id], mango_query, jwt_settings_key='APIKEY_JWT_KEY')
        return res

    def get_record_catalog(self,  folio ):
        mango_query = {"selector":
            {"answers":
                {"$and":[
                    {self.f['cat_stock_folio']: {'$eq': folio}}
                ]}},
            "limit":1,
            "skip":0}
        res = self.lkf_api.search_catalog( self.STOCK_INVENTORY_ID, mango_query, jwt_settings_key='APIKEY_JWT_KEY')
        return res

    def get_grading_sublots(self, gradings):
        grading_rec = {}
        for grading in gradings:
            ready_year = grading.get(self.f['grading_ready_year'])
            ready_week = grading.get(self.f['grading_ready_week'])
            if not ready_year:
                msg = "Ready year es un campo requerido. "
                msg_error_app = {
                    self.f['grading_ready_year']: {
                        "msg": [msg],
                        "label": "Please check your Ready Year",
                        "error":[]
                    }
                }
                raise Exception( simplejson.dumps( msg_error_app ) )
            if not ready_week:
                msg = "Ready year es un campo requerido. "
                msg_error_app = {
                    self.f['grading_ready_year']: {
                        "msg": [msg],
                        "label": "Please check your Ready Year",
                        "error":[]
                    }
                }
                raise Exception( simplejson.dumps( msg_error_app ) )
            lot_number = int(f"{ready_year}{ready_week}")
            grading[self.f['grading_ready_yearweek']] = lot_number
            grading_rec[lot_number] = grading_rec.get(lot_number,0)
            grading_rec[lot_number] += grading[self.f['grading_flats']]
        return grading_rec

    def get_production_move(self, new_containers, weighted_mult_rate, production_date):
        res = {}

        res[self.Product.SKU_OBJ_ID ] = deepcopy(self.answers.get(self.Product.SKU_OBJ_ID, {}))
        res[self.Product.SKU_OBJ_ID ]['6205f73281bb36a6f1573357'] = 8
        soil_type = self.unlist(self.answers.get(self.Product.SKU_OBJ_ID,{}).get(self.f['reicpe_soil_type'],""))
        # res[self.Product.SKU_OBJ_ID ][self.f['reicpe_soil_type']] = soil_type
        res[self.TEAM_OBJ_ID] = self.answers.get( self.TEAM_OBJ_ID,{})
        res[self.MEDIA_LOT_OBJ_ID] = self.answers.get(self.MEDIA_LOT_OBJ_ID,{})

        res[self.f['set_production_date']] = str(production_date.strftime('%Y-%m-%d'))
        # prod_date = self.date_from_str(production_date)
        print('year', production_date.strftime('%Y'))
        res[self.f['plant_cut_year']] = int(production_date.strftime('%Y'))
        res[self.f['production_cut_week']] = int(production_date.strftime('%W'))
        res[self.f['production_cut_day']] = int(production_date.strftime('%j'))
        res[self.f['plant_group']] = self.answers.get(self.f['production_working_group'])
        res[self.f['plant_cycle']] = self.answers.get(self.f['production_working_cycle'])
        res[self.f['product_lot']] = self.create_proudction_lot_number(production_date)
        res[self.f['plant_contamin_code']] = self.answers.get(self.f['plant_contamin_code'])
        production_recipe = self.answers.get(self.f['product_recipe'], {})
        res[self.f['plant_stage']] = int(production_recipe.get(self.f['reicpe_start_size'])[1])
        res[self.f['plant_conteiner_type']] = self.unlist(production_recipe.get(self.f['sku_container'])).lower().replace(' ', '_')
        per_container = int(self.unlist(production_recipe.get(self.f['prod_qty_per_container'], [])))
        res[self.f['plant_per_container']] = per_container

        res[self.f['actuals']] = new_containers
        res[self.f['actual_eaches_on_hand']] = new_containers * per_container
        res[self.f['production_folio']] = self.folio
        res[self.f['production_multiplication_rate']] = weighted_mult_rate
        res[self.f['inventory_status']] = 'active' if res[self.f['plant_stage']] in (1,2,"1","2") else 'pull'
        res[self.f['move_status']] = 'to_do'
        print('res',res)
        return res

    def get_record_greenhouse_inventory(self, ready_date, planting_house, plant_code):
        query_greenhouse_inventory = {
            'form_id': self.FORM_INVENTORY_ID,
            'deleted_at': {'$exists': False},
            f"answers.{self.f['product_lot']}": int(ready_date),
            f"answers.{self.WAREHOUSE_OBJ_ID}.{self.f['warehouse']}": planting_house,
            f"answers.{self.f['product_recipe']}.{self.f['product_code']}": plant_code,
            #f"answers.{self.f['inventory_status']}": 'active'
        }
        record = self.cr.find_one(query_greenhouse_inventory, {'folio': 1, 'answers': 1, 'form_id': 1, 'user_id': 1})
        return record

    def get_stock_query(self, query_dict):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.FORM_INVENTORY_ID,
            }
        if query_dict.get('folio'):
            match_query.update({'folio':query_dict.get('folio')})
        match_query.update(self.get_product_map(query_dict, map_type='model_2_field_id'))
        return match_query

    def get_warehouse(self, warehouse_type=None):
        mango_query = {
            "selector":{"_id": {"$gt":None}},
            "limit":1000,
            "skip":0
            }
        if warehouse_type:
            mango_query['selector'] = {'answers':{self.f['warehouse_type']: warehouse_type}}
        res = self.lkf_api.search_catalog( self.WAREHOUSE_ID, mango_query)
        warehouse = [r[self.f['warehouse']] for r in res]
        return warehouse
  
    def get_plant_prodctivity(self, answers):
        group = answers.get(self.f['production_group'], [])
        total_hrs = 0
        total_containers = 0
        total_eaches = 0
        print('group', group)

        print('group', self.f['production_group'])
        for gset in group:
            product = gset.get(self.f['product_recipe'], {})

            eaches = gset.get(self.f['production_eaches_req'], 0)
            print('eaches', eaches)
            plt_container =  product.get(self.f['reicpe_per_container'],0)
            print('per_container', plt_container)
            if eaches:
                containers =  round(eaches/plt_container,0)
                gset[self.f['production_requier_containers']] = containers
                total_containers += containers
                total_eaches += eaches
            print('production_requier_containers', gset[self.f['production_requier_containers']])
            plant_per_hr = product.get(self.f['reicpe_productiviy'],[])
            if plant_per_hr and len(plant_per_hr) > 0:
                plant_per_hr = plant_per_hr[0]
            else:
                continue
            requier_cont = gset.get(self.f['production_requier_containers'],0)
            plants_needed =  int(plt_container) * int(requier_cont)
            set_hrs = round(float(plants_needed) / float(plant_per_hr), 1)
            total_hrs += set_hrs
            gset[self.f['production_group_estimated_hrs']] = round(set_hrs,2)

        answers[self.f['production_group']] =  group
        answers[self.f['production_estimated_hrs']] = round(total_hrs,2)
        print('total eaches', total_eaches)
        answers[self.f['production_total_eaches']] = total_eaches
        answers[self.f['production_total_containers']] = total_containers
        return answers

    def gradings_validations(self):
        answers = self.current_record.get('answers',{})

        gradings = answers[self.f['grading_group']]
        rec_date = answers[self.f['grading_date']]
        scrap_qty = answers.get(self.f['inv_scrap_qty'],0)
        grading_type = answers[self.f['grading_date']]
        plant_info = answers[self.STOCK_INVENTORY_OBJ_ID]
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
                        'warehouse': warehouse,
                        'record_id':self.record_id
                        })
            self.update_calc_fields(product_code, warehouse, lot_number)
        return answers

    def inventory_adjustment(self):
        products = self.answers.get(self.f['grading_group'])
        warehouse = self.answers[self.WH.WAREHOUSE_LOCATION_OBJ_ID][self.f['warehouse']]
        location_id = self.answers[self.WH.WAREHOUSE_LOCATION_OBJ_ID][self.f['warehouse_location']]
        adjust_date = self.answers[self.f['grading_date']]
        comments = self.answers.get(self.f['inv_adjust_comments'],'') 
        patch_records = []
        metadata = self.lkf_api.get_metadata(self.FORM_INVENTORY_ID)
        kwargs = {"force_lote":True, "inc_folio":self.folio }
        properties = {
                "device_properties":{
                    "system": "Script",
                    "process": "Inventroy Adjustment", 
                    "accion": 'Inventroy Adjustment', 
                    "folio carga": self.folio, 
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
        # for plant in plants:
        #     product_code = plant[self.Product.PRODUCT_OBJ_ID][self.f['product_code']]
        #     search_codes.append(product_code)


        # recipes = self.get_plant_recipe( search_codes, stage=[4, 'Ln72'] )
        # growth_weeks = 0
        latest_versions = versions = self.get_record_last_version(self.current_record)
        answers_version = latest_versions.get('answers',{})
        last_verions_products = {}
        if answers_version:
            version_products = answers_version.get(self.f['grading_group'])
            for ver_product in version_products:
                ver_product_code = ver_product[self.Product.SKU_OBJ_ID][self.f['product_code']]
                ver_sku = ver_product[self.Product.SKU_OBJ_ID][self.f['sku']]
                ver_lot_number = ver_product.get(self.f['product_lot'])
                if ver_lot_number:
                    last_verions_products[f'{ver_product_code}_{ver_sku}_{ver_lot_number}_{warehouse}_{location_id}'] = {
                        'product_code':ver_product_code,
                        'sku':ver_sku,
                        'lot_number':ver_lot_number,
                        'warehouse':warehouse,
                        'location':location_id
                    }
        skus = self.get_group_skus(products)
        not_found = []
        for idx, product in enumerate(products):
            product_code =  product[self.Product.SKU_OBJ_ID][self.f['product_code']]
            sku =  product[self.Product.SKU_OBJ_ID][self.f['sku']]
            product_name =  self.unlist(product[self.Product.SKU_OBJ_ID][self.f['product_name']])
            product[self.f['product_lot']] = product.get(self.f['product_lot'], 1) 
            lot_number = product[self.f['product_lot']]
            status = product[self.f['inv_adjust_grp_status']]
            adjust_qty = product.get(self.f['inv_adjust_grp_qty'])
            adjust_in = product.get(self.f['inv_adjust_grp_in'], 0)
            adjust_out = product.get(self.f['inv_adjust_grp_out'], 0)
            product_code = product[self.Product.SKU_OBJ_ID][self.f['product_code']]
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
                product[self.f['inv_adjust_grp_status']] = 'error'
                product[self.f['inv_adjust_grp_comments']] = msg
                continue
            if verify ==  0:
                msg = f"You must input an adjusted Qty on product {product_code}, lot number {lot_number}."
                product[self.f['inv_adjust_grp_status']] = 'error'
                product[self.f['inv_adjust_grp_comments']] = msg
                continue

            if last_verions_products.get(f'{sku}_{lot_number}_{warehouse}_{location_id}'):
                last_verions_products.pop(f'{sku}_{lot_number}_{warehouse}_{location_id}')
            exists = self.product_stock_exists(product_code=product_code, sku=sku, lot_number=lot_number, warehouse=warehouse, location=location_id)
            print('exists',exists )
            cache_id = f'{product_code}_{lot_number}_{warehouse}_{location_id}'
            self.cache_drop({"_id":cache_id})
            product_stock = self.get_product_stock(product_code, sku=sku, lot_number=lot_number, warehouse=warehouse, date_to=adjust_date, **{'nin_folio':self.folio})
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

            product[self.f['inv_adjust_grp_qty']] = adjust_qty
            product[self.f['inv_adjust_grp_in']] = adjust_in
            product[self.f['inv_adjust_grp_out']] = abs(adjust_out)


            if exists:
                answers = {self.f['plant_contamin_code']:product.get(self.f['plant_contamin_code']) }
                self.cache_set({
                        '_id': f'{product_code}_{sku}_{lot_number}_{warehouse}_{location_id}',
                        'adjustments': cache_adjustment,
                        'product_lot': lot_number,
                        'product_code':product_code,
                        'sku':sku,
                        'warehouse': warehouse,
                        'record_id':self.record_id
                        })

                response = self.update_stock(answers=answers, form_id=self.FORM_INVENTORY_ID, folios=exists['folio'])
                if not response:
                    comments += f'Error updating product {product_code} lot {lot_number}. '
                    product[self.f['inv_adjust_grp_status']] = 'error'
                else:
                    product[self.f['inv_adjust_grp_status']] = 'done'
                    product[self.f['inv_adjust_grp_comments']] = ""

            else:
                if skus.get(product_code) and len(skus[product_code]):
                    print('product', product)
                    answers = self.stock_inventory_model(product, skus[product_code])
                    answers.update({
                        self.WH.WAREHOUSE_LOCATION_OBJ_ID:{
                            self.f['warehouse']:warehouse,
                            self.f['warehouse_location']:location_id}
                            },
                        )
                    metadata['answers'] = answers
                    self.cache_set({
                            '_id': f'{product_code}_{sku}_{lot_number}_{warehouse}_{location_id}',
                            'adjustments': cache_adjustment,
                            'lot_number': lot_number,
                            'product_code':product_code,
                            'sku':sku,
                            'warehouse': warehouse,
                            'warehouse_location': location_id,
                            'record_id':self.record_id
                            })

                    response_sistema = self.lkf_api.post_forms_answers(metadata)
                    print('response_sistema',response_sistema)
                    try:
                        new_inv = self.get_record_by_id(response_sistema.get('id'))
                    except:
                        print('no encontro...')
                    status_code = response_sistema.get('status_code',404)
                    if status_code == 201:
                        product[self.f['inv_adjust_grp_status']] = 'done'
                        product[self.f['inv_adjust_grp_comments']] = "New Creation "
                    else:
                        error = response_sistema.get('json',{}).get('error', 'Unkown error')
                        product[self.f['inv_adjust_grp_status']] = 'error'
                        product[self.f['inv_adjust_grp_comments']] = f'Status Code: {status_code}, Error: {error}'
                else:
                    product[self.f['inv_adjust_grp_status']] = 'error'
                    product[self.f['inv_adjust_grp_comments']] = f'SKU not found'

        if last_verions_products:
            for key, value in last_verions_products.items():
                exist = self.product_stock_exists(
                    product_code=value['product_code'], sku=value['sku'], lot_number=value['lot_number'], warehouse=value['warehouse'], location=value['location'])
                if exist:
                    print('doble update o que....????')
                    response = self.update_stock(answers={}, form_id=self.FORM_INVENTORY_ID, folios=exist['folio'])

        self.answers[self.f['inv_adjust_status']] = 'done'
        if not_found:
            comments += f'Codes not found: {not_found}.'

        self.answers[self.f['inv_adjust_comments']] = comments
        return True

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

    def make_inventory_flow(self):
        ####
        #### Si la nueva ubicacion de almacen esta dentro de un grupo la saca y llama a la funcion nuevamente
        ####
        new_records_data = []
        result = []
        # fields_to_new_record = self.get_record_form_fields(self.FORM_INVENTORY_ID)
        if self.answers.get(self.f['new_location_group']):
            move_group = self.answers.pop(self.f['new_location_group'])
            container_type = self.answers.get(self.f['plant_conteiner_type'])
            container_on_racks = sum([int(x[self.f['new_location_racks']]) for x in move_group]) * self.container_per_rack[container_type]
            move_qty = sum([int(x[self.f['new_location_containers']]) for x in move_group]) + container_on_racks
            record_qty =  int(self.answers.get(self.f['actuals'],0))
            if record_qty != move_qty:
                msg_error_app = {
                    self.f['actuals']:
                        {"msg": ["There are {} Containers on the record, but you are trying to alocate {}".format(record_qty, move_qty)],
                        "label": "Containers on Hand", "error": []}
                }
                raise Exception( simplejson.dumps( msg_error_app ) )
            for location in move_group:
                if self.form_id == self.MOVE_NEW_PRODUCTION_ID:
                    production = True
                else:
                    production = False
                answers = deepcopy(self.answers)
                answers.update(self.set_inventroy_format(answers, location, production=production ))
                product_code = self.answers[self.Product.SKU_OBJ_ID][self.f['product_code']]
                sku = self.answers[self.Product.SKU_OBJ_ID][self.f['sku']]
                product_lot  = self.answers[self.f['product_lot']]
                warehouse = location[self.WH.WAREHOUSE_LOCATION_OBJ_ID][self.f['warehouse']]
                location_id = location[self.WH.WAREHOUSE_LOCATION_OBJ_ID][self.f['warehouse_location']]
                answers.update(self.set_up_containers_math(answers, record_qty, location, production=production ))
                production_qty  = answers.get(self.f['production'],0)
                
                self.cache_set({
                        '_id': f'{product_code}_{sku}_{product_lot}_{warehouse}_{location_id}',
                        'production':production_qty,
                        'product_lot':product_lot,
                        'product_code':product_code,
                        'sku':sku,
                        'warehouse': warehouse,
                        'record_id':self.record_id
                        })
                res = self.create_inventory_flow(answers)
                if res.get('new_record'):
                    new_records_data.append(res['new_record'])
                else:
                    result.append(res)

        else:
            print('************ empieza *******************')
            res = self.create_inventory_flow(answers)
            if res.get('new_record'):
                new_records_data = res['new_record']
            else:
                result.append(res)
            
            print('1new_records_data',new_records_data)
    
        if new_records_data:
            # for x in new_records_data:
            #     print('x=',simplejson.dumps(x, indent=4))

            res_create = self.lkf_api.post_forms_answers_list(new_records_data)
            return res_create
        return result

    def merge_stock_records(self):
        form_id = self.FORM_INVENTORY_ID
        product_code, sku, lot_number, warehouse, location = self.get_product_lot_location()
        res = self.get_invtory_record_by_product(form_id, product_code, sku,  lot_number, warehouse, location, **{'get_many':True})
        delete_records = []
        if len(res) >= 1:
            res.pop(0)
        for x in res:
            delete_records.append(x['_id'])
        if delete_records:
            print('aqui va a borrar *********************************************')
            res = self.lkf_api.delete_form_records(delete_records)
        return True

    def move_location(self):
        product_info = self.answers.get(self.STOCK_INVENTORY_OBJ_ID,{})
        # folio_inventory = product_info.get(self.f['cat_stock_folio'])
        # print('folio_inventory', folio_inventory)
        lot_number = product_info.get(self.f['product_lot'])
        product_code = product_info.get(self.f['product_code'])
        sku = product_info.get(self.f['sku'])
        from_warehouse = product_info.get(self.f['warehouse'])
        from_location = product_info.get(self.f['warehouse_location'])
        # record_inventory_flow = self.get_inventory_record_by_folio(folio_inventory, form_id=self.FORM_INVENTORY_ID )
        record_inventory_flow = self.get_invtory_record_by_product(
            self.FORM_INVENTORY_ID,
            product_code,  
            sku,  
            lot_number,
            from_warehouse,
            from_location)
        print('record_inventory_flow', record_inventory_flow)

        if not record_inventory_flow:
            self.LKFException(f"folio: {record_inventory_flow} is not a valid inventory record any more, please check your stock")
        from_folio = record_inventory_flow['folio']
        inv_record = record_inventory_flow.get('answers')
        #gets the invetory as it was on that date...
        date_to = self.answers[self.f['grading_date']]
        # This are the actuals as they were on that date not including this move.
        inv_move_qty = self.answers.get(self.f['inv_move_qty'])
        print('containers to move.....',inv_move_qty)
        cache_from_location ={
            '_id': f'{product_code}_{sku}_{lot_number}_{from_warehouse}_{from_location}',
            'move_out':inv_move_qty,
            'lot_number':lot_number,
            'product_code':product_code,
            'sku':sku,
            'warehouse': from_warehouse,
            'warehouse_location': from_location,
            'record_id': self.record_id
        }
        from_wl = f'{from_warehouse}__{from_location}'
        dest_group = self.answers.get(self.f['move_group'],[])
        self.validate_stock_move(from_wl, inv_move_qty, dest_group)
        self.validate_move_qty(product_code, sku, lot_number, from_warehouse, from_location, inv_move_qty, date_to=date_to)
        dest_folio = []
        dest_folio_update = []
        for dest_set in dest_group:
            to_wh_info = dest_set.get(self.WH.WAREHOUSE_LOCATION_DEST_OBJ_ID,{})
            qty_to_move = dest_set.get(self.f['move_group_qty'],0)
            to_warehouse = to_wh_info.get(self.f['warehouse_dest'])
            to_location = to_wh_info.get(self.f['warehouse_location_dest'])
            to_wl = f'{to_warehouse}__{to_location}'
            dest_warehouse_inventory = self.get_invtory_record_by_product(
                self.FORM_INVENTORY_ID, product_code, sku, lot_number, to_warehouse, to_location  )
            self.cache_set({
                '_id': f'{product_code}_{sku}_{lot_number}_{to_warehouse}_{to_location}',
                'move_in':qty_to_move,
                'lot_number':lot_number,
                'sku':sku,
                'product_code':product_code,
                'warehouse': to_warehouse,
                'warehouse_location': to_location,
                'record_id': self.record_id
                })
            if not dest_warehouse_inventory:
                #creates new record.
                new_inv_rec = deepcopy(inv_record)
                # stock = self.get_product_stock(product_code, warehouse=dest_warehouse, lot_number=product_lot, **{'keep_cache':True})
                # update_values = self.get_product_map(stock)
                new_inv_rec.update({
                    f"{self.WH.WAREHOUSE_LOCATION_OBJ_ID}": {
                        self.f['warehouse']:to_warehouse,
                        self.f['warehouse_location']:to_location},
                    f"{self.f['product_lot_actuals']}": qty_to_move,
                    f"{self.f['product_lot_move_in']}": qty_to_move,
                    f"{self.f['product_lot_move_out']}": 0,
                    self.f['inventory_status']: 'active',
                })

                metadata = self.lkf_api.get_metadata(self.FORM_INVENTORY_ID) 
                metadata.update({
                    'properties': {
                        "device_properties":{
                            "system": "Script",
                            "process": 'Inventory Move',
                            "action": 'Create Inventory Record',
                            "from_folio": self.folio,
                            "archive": "stock_utils.py"
                        }
                    }
                })
                #1 check if the hole lot is moving out ....
                # response, update_rec = update_origin_log(record_inventory_flow, inv_record, inv_move_qty, acctual_containers)
                # new_inv_rec.update(update_rec)
                metadata.update({'answers': new_inv_rec})
                print('new_inv_rec=',new_inv_rec)
                response = self.lkf_api.post_forms_answers(metadata, jwt_settings_key='USER_JWT_KEY')
                if response.get('status_code') > 299 or not response.get('status_code'):
                    msg_error_app = response.get('json', 'Error al acomodar producto , favor de contactar al administrador')
                    self.LKFException( simplejson.dumps(msg_error_app) )
                x = simplejson.loads(response['data'])
                dest_folio.append(x.get('folio'))
            else:
                # Adding up to an existing lot
                # response, update_rec = update_origin_log(record_inventory_flow, inv_record, inv_move_qty, acctual_containers)
                print('TODO=', dest_warehouse_inventory)
                dest_folio_update.append(dest_warehouse_inventory.get('folio'))
                print('dest_folio', dest_warehouse_inventory.get('folio'))

                # dest_warehouse_inventory['answers'][self.f['product_lot_actuals']] += inv_move_qty
                # response = lkf_api.patch_record(dest_warehouse_inventory, jwt_settings_key='USER_JWT_KEY')


        #este update stock revisarlo y se me hace 
        if dest_folio_update:
            self.update_stock(folios=dest_folio_update)
            dest_folio += dest_folio_update
        self.cache_set(cache_from_location)
        self.update_stock(folios=from_folio)
        return dest_folio

    def move_in(self):
        answer_label = self._labels()
        print('-----------------------------answers=', answer_label)
        warehouse = answer_label['warehouse']
        location = answer_label['warehouse_location']
        warehouse_to = answer_label['warehouse_dest']
        location_to = answer_label['warehouse_location_dest']
        move_lines = answer_label['move_group']
        # Información original del Inventory Flow
        status_code = 0
        move_locations = []
        folios = []
        # lots_in = {}
        data_from = {'warehouse':warehouse, 'warehouse_location':location}
        print('data_from', data_frodm)
        new_records_data = []
        skus = self.get_group_skus(move_lines)
        metadata = self.lkf_api.get_metadata(self.FORM_INVENTORY_ID)
        for idx, moves in enumerate(move_lines):
            move_line = self.answers[self.f['move_group']][idx]
            print('moves', moves)
            # product_code = info_product.get(self.f['product_code'])
            # sku = info_product.get(self.f['sku'])
            exists = self.product_stock_exists(
                product_code=moves['product_code'], 
                sku=moves['sku'], 
                lot_number=moves['product_lot'], 
                warehouse=warehouse_to, 
                location=location_to)
            print('exists', exists)
            cache_data = {
                        '_id': f"{moves['product_code']}_{moves['sku']}_{moves['product_lot']}_{warehouse_to}_{location_to}",
                        'move_in': moves['move_group_qty'],
                        'product_lot': moves['product_lot'],
                        'product_code':moves['product_code'],
                        'sku':moves['sku'],
                        'warehouse': warehouse_to,
                        'warehouse_location': location_to,
                        'record_id':self.record_id
                        }
            if exists:
                if self.folio:
                    cache_data.update({'kwargs': {'nin_folio':self.folio }})
                self.cache_set(cache_data)
                response = self.update_stock(answers=exists.get('answers',{}), form_id=self.FORM_INVENTORY_ID, folios=exists['folio'])
                if not response:
                    comments += f"Error updating product {moves['product_lot']} lot {moves['product_lot']}. "
                    move_line[self.f['inv_adjust_grp_status']] = 'error'
                else:
                    move_line[self.f['move_dest_folio']] = exists['folio']
                    move_line[self.f['inv_adjust_grp_status']] = 'done'
                    move_line[self.f['inv_adjust_grp_comments']] = ""
                    print('moves', move_line)

            else:
                print('moves', moves)
                answers = self.stock_inventory_model(moves, skus[moves['product_code']], labels=True)
                answers.update({
                    self.WH.WAREHOUSE_LOCATION_OBJ_ID:{
                        self.f['warehouse']:warehouse_to,
                        self.f['warehouse_location']:location_to},
                    self.f['product_lot']:moves['product_lot']
                        },
                    )
                metadata['answers'] = answers
               
                print('cache_data',cache_data)
                self.cache_set(cache_data)
                create_resp = self.lkf_api.post_forms_answers(metadata)
                print('response_sistema',create_resp)
                try:
                    new_inv = self.get_record_by_id(create_resp.get('id'))
                except:
                    print('no encontro...')
                status_code = create_resp.get('status_code',404)
                if status_code == 201:
                    folio = create_resp.get('json',{}).get('folio','')
                    move_line[self.f['inv_adjust_grp_status']] = 'done'
                    move_line[self.f['move_dest_folio']] = folio
                else:
                    error = create_resp.get('json',{}).get('error', 'Unkown error')
                    move_line[self.f['inv_adjust_grp_status']] = 'error'
                    move_line[self.f['inv_adjust_grp_comments']] = f'Status Code: {status_code}, Error: {error}'
        return True

    def move_one_many_one(self):
        move_lines = self.answers[self.f['move_group']]
        warehouse = self.answers[self.WH.WAREHOUSE_LOCATION_OBJ_ID][self.f['warehouse']]
        location = self.answers[self.WH.WAREHOUSE_LOCATION_OBJ_ID][self.f['warehouse_location']]
        warehouse_to = self.answers[self.WH.WAREHOUSE_LOCATION_DEST_OBJ_ID][self.f['warehouse_dest']]
        location_to = self.answers[self.WH.WAREHOUSE_LOCATION_DEST_OBJ_ID][self.f['warehouse_location_dest']]
        # Información original del Inventory Flow
        status_code = 0
        move_locations = []
        folios = []
        # lots_in = {}
        data_from = {'warehouse':warehouse, 'warehouse_location':location}
        new_records_data = []
        for moves in move_lines:
            info_product = moves.get(self.STOCK_INVENTORY_OBJ_ID, {})
            # product_code = info_product.get(self.f['product_code'])
            # sku = info_product.get(self.f['sku'])
            # lot_number = info_product.get(self.f['lot_number'])
            stock = self.get_stock_info_from_catalog_inventory(answers=moves, data=data_from , **{'get_record':True})
            ###################################
            product_code = stock.get('product_code')
            sku = stock.get('sku')
            lot_number = stock.get('lot_number')
            warehouse = stock.get('warehouse')
            location = stock.get('warehouse_location')
            folios.append(stock['folio'])
            ###################################

            moves[self.f['move_dest_folio']] = stock['folio']
            moves[self.f['inv_adjust_grp_status']] = 'done'
            
            set_location = f"{product_code}_{sku}_{lot_number}_{warehouse_to}_{location_to}"
            if set_location in move_locations:
                msg = "You are trying to move the same lot_number: {lot_number} twice from the same location. Please check"
                msg += f"warehouse: {stock['warehouse']} / Location: {stock['warehouse_location']}"
                msg_error_app = {
                    f"{self.f['warehouse_location']}": {
                        "msg": [msg],
                        "label": "Please check your selected location",
                        "error":[]
      
                    }
                }
                self.LKFException(msg_error_app)
            move_locations.append(set_location)
            if not stock.get('folio'):
                msg = "Stock record not found Please check availability for:"
                msg += f"Product Code: {product_code} / SKU: {sku} / Lot Number: {lot_number}"
                msg_error_app = {
                    f"{self.f['warehouse_location']}": {
                        "msg": [msg],
                        "label": "Please check your availability to this location",
                        "error":[]
      
                    }
                }
                self.LKFException(msg_error_app)
            # Información que modifica el usuario
            move_qty = moves.get(self.f['move_group_qty'],0)
            print('move_qty', move_qty)
            moves[self.f['inv_move_qty']] = move_qty
            self.validate_move_qty(product_code, sku, lot_number,  warehouse, location, move_qty)
            
            move_vals_from = {'_id': f"{product_code}_{sku}_{lot_number}_{warehouse}_{location}",
                        'move_out':move_qty,
                        'product_code':product_code,
                        'product_lot':lot_number,
                        'warehouse': warehouse,
                        'warehouse_location': location,
                        'record_id':self.record_id
                        }
            if self.folio:
                move_vals_from.update({'kwargs': {'nin_folio':self.folio }})
            move_vals_to = deepcopy(move_vals_from)
            move_vals_to.pop('move_out')
            move_vals_to.update(
                {
                '_id': set_location,
                'warehouse': warehouse_to,
                'warehouse_location': location_to,
                'from_folio':stock['folio'], 
                'move_in':move_qty,
                'move_qty':move_qty
            })
            # lots_in[set_location] = lots_in.get(set_location, move_vals_to) 
            print('setting cache to...', move_vals_to)
            self.cache_set(move_vals_to)
            print('setting cache form...', move_vals_from)
            self.cache_set(move_vals_from)
            new_lot = stock.get('record',{}).get('answers',{})
            warehouse_ans = self.swap_location_dest(self.answers[self.WH.WAREHOUSE_LOCATION_DEST_OBJ_ID])
            new_lot.update(warehouse_ans)
            new_records_data.append(self.create_inventory_flow(answers=new_lot))
        

        res ={}

        create_new_records = []
        for record in new_records_data:
            if record.get('new_record'):
                create_new_records.append(record['new_record'])
            else:
                print('YA EXISTE... record ya se actualizco usando cache', record)
        print('create_new_records=',create_new_records)
        print('TODO mover status a lineas de registro')
        res_create = self.lkf_api.post_forms_answers_list(create_new_records)
        #updates records from where stock was moved
        res = self.update_stock(answers={}, form_id=self.FORM_INVENTORY_ID, folios=folios)
        res ={}
        print('res_create', res_create)
        #res = self.update_stock(answers={}, form_id=self.FORM_INVENTORY_ID, folios=folios)
        return True

    def move_out_multi_location(self):
        move_lines = self.answers[self.f['move_group']]

        # Información original del Inventory Flow
        status_code = 0
        move_locations = []
        folios = []
        print('ans', self.answers)
        product_code = self.answers.get(self.Product.SKU_OBJ_ID,{}).get(self.f['product_code'])
        print('product_code1', product_code)
        for moves in move_lines:
            print('move........', moves)
            info_plant = moves.get(self.STOCK_INVENTORY_OBJ_ID, {})
            stock = {'product_code':product_code}
            stock = self.get_stock_info_from_catalog_inventory(answers=moves, data=stock)
            print('product_code........',product_code)
            lot_number = stock.get('lot_number')
            sku = stock.get('sku')
            warehouse = stock.get('warehouse')
            location = stock.get('warehouse_location')
            moves[self.f['move_dest_folio']] = stock['folio']
            set_location = f"{stock['warehouse']}__{stock['warehouse_location']}__{lot_number}"
            if set_location in move_locations:
                msg = "You are trying to move the same lot_number: {lot_number} twice from the same location. Please check"
                msg += f"warehouse: {stock['warehouse']} / Location: {stock['warehouse_location']}"
                msg_error_app = {
                    f"{self.f['warehouse_location']}": {
                        "msg": [msg],
                        "label": "Please check your selected location",
                        "error":[]
      
                    }
                }
                self.LKFException(msg_error_app)
            move_locations.append(set_location)
            if not stock.get('folio'):
                continue
            # Información que modifica el usuario
            move_qty = moves.get(self.f['inv_move_qty'], 0)
            print('move_qty=', move_qty)
            #record_inventory_flow = self.get_inventory_record_by_folio(folio=stock.get('folio'),form_id=self.FORM_INVENTORY_ID)
            self.validate_move_qty(product_code, sku, stock['lot_number'],  stock['warehouse'], stock['warehouse_location'], move_qty)
            if stock.get('folio'):
                folios.append(stock['folio'])
        self.cache_set({
                    '_id': f"{product_code}_{sku}_{stock['lot_number']}_{stock['warehouse']}_{stock['warehouse_location']}",
                    'move_out':move_qty,
                    'product_code':product_code,
                    'sku':sku,
                    'product_lot':stock['lot_number'],
                    'warehouse': stock['warehouse'],
                    'warehouse_location': stock['warehouse_location'],
                    'record_id':self.record_id
                    })
        print('fokios', folios)
        res = self.update_stock(answers={}, form_id=self.FORM_INVENTORY_ID, folios=folios)
        print('res',res)

            # if new_actual_containers_on_hand <= 0:
            #     record_inventory_flow['answers'].update({
            #         '620ad6247a217dbcb888d175': 'done'
            #     })

            # record_inventory_flow.update({
            #     'properties': {
            #         "device_properties":{
            #             "system": "SCRIPT",
            #             "process":"Inventory Move - Out",
            #             "accion":'Update record Inventory Flow',
            #             "archive":"inventory_move_scrap.py"
            #         }
            #     }
            # })
            # print('record_inventory_flow',record_inventory_flow['answers'])
            # # Se actualiza el Inventory Flow que está seleccionado en el campo del current record
            # res_update_inventory = lkf_api.patch_record( record_inventory_flow, jwt_settings_key='USER_JWT_KEY' )
            # print('res_update_inventory =',res_update_inventory)
            # if res_update_inventory.get('status_code',0) > status_code:
            #     status_code = res_update_inventory['status_code']
        return res
 
    def plant_recipe_query(self, all_codes, start_size, reicpe_stage, recipe_type='Main'):
        if not recipe_type:
            recipe_type='Main'
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
            if len(all_codes) == 1:
                mango_query['selector']['answers'].update({self.f['product_code']:  all_codes[0] })
            else:
                mango_query['selector']['answers'].update({self.f['product_code']: {"$in": all_codes},})
        return mango_query

    def product_stock_exists(self, product_code, sku, lot_number=None, warehouse=None, location=None,  status=None):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.FORM_INVENTORY_ID,
            f"answers.{self.Product.SKU_OBJ_ID}.{self.f['product_code']}": product_code,
            f"answers.{self.Product.SKU_OBJ_ID}.{self.f['sku']}": sku,
            }
        if warehouse:
            match_query.update({f"answers.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.f['warehouse']}":warehouse})      
        if location:
            match_query.update({f"answers.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.f['warehouse_location']}":location})
        if lot_number:
            match_query.update({f"answers.{self.f['product_lot']}":lot_number})
        if status:
            match_query.update({f"answers.{self.f['inventory_status']}":status})
        exist = self.cr.find_one(match_query)
        return exist

    def process_record_to_catalog(self, current_record ):
        # Obtengo los campos de la forma
        form_fields = self.lkf_api.get_form_id_fields(current_record['form_id'], jwt_settings_key='APIKEY_JWT_KEY')
        fields = form_fields[0]['fields']
        # Obtengo solo los índices que necesito de cada campo
        info_fields = [{k:n[k] for k in ('label','field_type','field_id','groups_fields','group','options','catalog_fields','catalog') if k in n} for n in fields]
        for field in info_fields:
            field_id = field.get('field_id', '')
            if field.get('field_type', '') == 'catalog-select':
                catalog_field_id = field.get('catalog', {}).get('catalog_field_id', '')
                self.answers[ field_id ] = self.answers.get(catalog_field_id, {}).get(field_id)

            elif field.get('field_type', '') == 'catalog-detail':
                catalog_field_id = field.get('catalog', {}).get('catalog_field_id', '')
                val_catalog_answers = self.answers.get(catalog_field_id, {}).get(field_id, [])
                if val_catalog_answers:
                    self.answers[ field_id ] = val_catalog_answers

        # Obtengo los campos del catalogo
        catalog_fields = self.lkf_api.get_catalog_id_fields( self.STOCK_INVENTORY_ID, jwt_settings_key='APIKEY_JWT_KEY' )
        info_catalog = catalog_fields.get('catalog', {})
        fields = info_catalog['fields']
        dict_idfield_typefield = { \
            f.get('field_id'): {\
                'field_type': f.get('field_type'), \
                'options': { o.get('value'): o.get('label') for o in f.get('options',[]) }\
            } for f in fields }

        dict_answers_to_catalog = {}
        for id_field in dict_idfield_typefield:
            if id_field in (self.f['product_recipe'], self.WAREHOUSE_OBJ_ID):
                continue
            val_in_record = self.answers.get( id_field, False )
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
        catalogo_metadata = self.lkf_api.get_catalog_metadata(catalog_id=self.STOCK_INVENTORY_ID)

        if record_catalog:
            info_record_catalog = record_catalog[0]

            if self.answers.get(self.f['product_lot_actuals'], 1) <= 0:
                # Se elimina el registro del catalogo
                response_delete_catalog = self.lkf_api.delete_catalog_record(self.STOCK_INVENTORY_ID, info_record_catalog.pop('_id'), info_record_catalog.pop('_rev'), jwt_settings_key='APIKEY_JWT_KEY')
                return True

            info_record_catalog.update(dict_answers_to_catalog)


            print('catalogo_metadata=', info_record_catalog)
            print('ready year week=', info_record_catalog.get('620a9ee0a449b98114f61d75'))
            catalogo_metadata.update({'record_id': info_record_catalog.pop('_id'), '_rev': info_record_catalog.pop('_rev'), 'answers': info_record_catalog})
            response_update_catalog = self.lkf_api.bulk_patch_catalog([catalogo_metadata,], self.STOCK_INVENTORY_ID, jwt_settings_key='APIKEY_JWT_KEY')
        else:
            catalogo_metadata.update({'answers': dict_answers_to_catalog})
            print('catalogo_metadata=', catalogo_metadata)
            res_crea_cat = self.lkf_api.post_catalog_answers(catalogo_metadata, jwt_settings_key='APIKEY_JWT_KEY')
        return True

    def product_sku_query(self, all_sku, recipe_type=None):
        if not recipe_type:
            #todo agregar recipe type que va a ser el stocking format
            recipe_type='Main'
        mango_query = {
            "selector": {
                "answers": {}
                    } ,
            "limit": 1000,
            "skip": 0
                    }
        if all_sku:
            if len(all_sku) == 1:
                mango_query['selector']['answers'].update({self.f['product_code']:  all_sku[0] })
            else:
                mango_query['selector']['answers'].update({self.f['product_code']: {"$in": all_sku},})
        return mango_query

    def select_S4_recipe(self, plant_recipe, plant_week):
        print('plant_recipe', plant_recipe)
        if type(plant_recipe) == dict:
            plant_recipe = [plant_recipe,]
        for recipe in plant_recipe:
            start_week = recipe.get('start_week')
            end_week = recipe.get('end_week')
            if int(plant_week) >= int(start_week) and int(plant_week) <= int(end_week):
                return recipe
        return {}

    def set_inventroy_format(self, answers, location, production=False ):
        return answers

    def stock_inventory_model(self, product, recipe, labels=False):
        if labels:
            product = self._lables_to_ids(product)
            print('>>>>product',product)
            res = {}
            res[self.Product.SKU_OBJ_ID ] = deepcopy(product)
        else:
            res =  deepcopy(product)
        res[self.Product.SKU_OBJ_ID ][self.f['sku_container']] = recipe['sku_package']
        res[self.Product.SKU_OBJ_ID ][self.f['per_container']] = recipe['sku_per_package']
        if type(recipe['product_name']) != list:
            res[self.Product.SKU_OBJ_ID ][self.f['product_name']] = [recipe['product_name'],]
        else:
            res[self.Product.SKU_OBJ_ID ][self.f['product_name']] = recipe['product_name']
        return res

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

    def set_up_containers_math(self, answers, record_qty , new_location, production=False):
        per_container = int(answers[self.f['plant_per_container']])
        container_type = answers[self.f['plant_conteiner_type']]
        racks = new_location.get(self.f['new_location_racks'],0)
        containers = new_location.get(self.f['new_location_containers'],0)
        move_qty = self.add_racks_and_containers(container_type, racks, containers)
        answers.update(new_location)
        answers[self.f['actuals']] = move_qty
        answers[self.f['actual_eaches_on_hand']] = move_qty * per_container
        if production:
            answers[self.f['production']] = move_qty # qty produced
            # answers[self.f['move_out']] = record_qty - move_qty # Relocated
        return answers

    def stock_one_many_one(self, move_type, product_code=None, sku=None, lot_number=None, warehouse=None, location=None, date_from=None, date_to=None, status='done', **kwargs):
        unwind =None
        if move_type not in ('in','out'):
            raise('Move type only accepts values "in" or "out" ')
        match_query = {
            "deleted_at":{"$exists":False},
            }
        match_query.update(self.stock_kwargs_query(**kwargs))
        query_forms = self.STOCK_ONE_MANY_ONE_FORMS
        if len(query_forms) > 1:
            form_query = {"form_id":{"$in":query_forms}}
        else:
            form_query = {"form_id":self.STOCK_ONE_MANY_ONE_FORMS[0]}
        match_query.update(form_query)
        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field_id=self.f['grading_date']))

        unwind = {'$unwind': '$answers.{}'.format(self.f['move_group'])}
        unwind_query = {}
        unwind_stage = []
        # print('move type.............', move_type)
        # print('warehouse', warehouse)
        # print('location', location)
        # print('product_code', product_code)
        # print('sku', sku)
        # print('lot_number', lot_number)
        if move_type =='in':
            if warehouse:
                match_query.update({f"answers.{self.WH.WAREHOUSE_LOCATION_DEST_OBJ_ID}.{self.f['warehouse_dest']}":warehouse})
            if location:
                match_query.update({f"answers.{self.WH.WAREHOUSE_LOCATION_DEST_OBJ_ID}.{self.f['warehouse_location_dest']}":location})        
        if move_type =='out':
            if warehouse:
                match_query.update({f"answers.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.f['warehouse']}":warehouse})
            if location:
                match_query.update({f"answers.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.f['warehouse_location']}":location})
       
        if product_code:
            p_code_query = {"$or":[
                {f"answers.{self.f['move_group']}.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['product_code']}":product_code},
                {f"answers.{self.f['move_group']}.{self.Product.SKU_OBJ_ID}.{self.f['product_code']}":product_code}
            ]
            }
            unwind_stage.append({'$match': p_code_query })
        if sku:
            sku_query = {"$or":[
                {f"answers.{self.f['move_group']}.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['sku']}":sku},
                {f"answers.{self.f['move_group']}.{self.Product.SKU_OBJ_ID}.{self.f['sku']}":sku}
            ]
            }
            unwind_stage.append({'$match': sku_query })
        if lot_number:
            lot_number_query = {"$or":[
                {f"answers.{self.f['move_group']}.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['lot_number']}":lot_number},
                {f"answers.{self.f['move_group']}.{self.Product.SKU_OBJ_ID}.{self.f['lot_number']}":lot_number},
                {f"answers.{self.f['move_group']}.{self.f['lot_number']}":lot_number}
            ]
            }
            unwind_stage.append({'$match': lot_number_query })
        if status:
            match_query.update({f"answers.{self.f['stock_status']}":status})
        if status:
            unwind_query.update({f"answers.{self.f['move_group']}.{self.f['inv_adjust_grp_status']}":status})
        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field_id=self.f['grading_date']))
        project = {'$project':
                {'_id': 1,
                    'product_code':{"$ifNull":[
                        f"$answers.{self.f['move_group']}.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_code']}",
                        f"$answers.{self.f['move_group']}.{self.Product.SKU_OBJ_ID}.{self.f['product_code']}",
                    ] } ,
                    'total': f"$answers.{self.f['move_group']}.{self.f['move_group_qty']}",
                    }
            }
        query= [{'$match': match_query }]
        query.append(unwind)
        if unwind_query:
            query.append({'$match': unwind_query })
        if unwind_stage:
            query += unwind_stage
        query.append(project)
        query += [
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

    def stock_adjustments(self, product_code=None, warehouse=None, location=None, lot_number=None, date_from=None, date_to=None, **kwargs):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.ADJUIST_FORM_ID,
            f"answers.{self.f['inv_adjust_status']}":{"$ne":"cancel"}
            }
        match_query.update(self.stock_kwargs_query(**kwargs))
        inc_folio = kwargs.pop("inc_folio") if kwargs.get("inc_folio") else None
        if warehouse:
            match_query.update({f"answers.{self.WAREHOUSE_OBJ_ID}.{self.f['warehouse']}":warehouse})      
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
            match_query_stage2.update({f"answers.{self.f['grading_group']}.{self.f['product_lot']}":int(lot_number)})
        if location:
            match_query_stage2.update({f"answers.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['product_lot_location']}":location})
        query= [{'$match': match_query }]
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

    def stock_adjustments_moves(self, product_code=None, sku=None, lot_number=None, warehouse=None, location=None, date_from=None, date_to=None, **kwargs):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.ADJUIST_FORM_ID,
            f"answers.{self.f['inv_adjust_status']}":{"$ne":"cancel"}
            }
        match_query.update(self.stock_kwargs_query(**kwargs))
        inc_folio = kwargs.pop("inc_folio") if kwargs.get("inc_folio") else None
        if warehouse:
            match_query.update({f"answers.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.f['warehouse']}":warehouse})   
        if location:
            match_query.update({f"answers.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.f['warehouse_location']}":location})      
        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field_id=self.f['grading_date']))
        match_query_stage2 = {}
        # match_query_stage2 = {f"answers.{self.f['grading_group']}.{self.f['inv_adjust_grp_status']}": "done"}
        if inc_folio:
            match_query_stage2 = {"$or": [
                {f"answers.{self.f['grading_group']}.{self.f['inv_adjust_grp_status']}": "done"},
                {"folio":inc_folio}
                ]}
        if product_code:
            match_query_stage2.update({f"answers.{self.f['grading_group']}.{self.Product.SKU_OBJ_ID}.{self.f['product_code']}":product_code})
        if sku:
            match_query_stage2.update({f"answers.{self.f['grading_group']}.{self.Product.SKU_OBJ_ID}.{self.f['sku']}":sku})
        if lot_number:
            match_query_stage2.update({f"answers.{self.f['grading_group']}.{self.f['product_lot']}":lot_number})
        query= [{'$match': match_query },
            {'$unwind': '$answers.{}'.format(self.f['grading_group'])},
            ]
        if match_query_stage2:
            query += [{'$match': match_query_stage2 }]
        query += [
            {'$project':
                {'_id': 1,
                    'product_code': f"$answers.{self.f['grading_group']}.{self.Product.PRODUCT_OBJ_ID}.{self.f['product_code']}",
                    'sku': f"$answers.{self.f['grading_group']}.{self.Product.PRODUCT_OBJ_ID}.{self.f['sku']}",
                    'adjust_in': f"$answers.{self.f['grading_group']}.{self.f['inv_adjust_grp_in']}",
                    'adjust_out': f"$answers.{self.f['grading_group']}.{self.f['inv_adjust_grp_out']}",
                    }
            },
            {'$group':
                {'_id':
                    { 
                    'product_code': '$product_code',
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
  
    def stock_kwargs_query(self, **kwargs):
        match_query = {}
        inc_folio = kwargs.get("inc_folio")
        nin_folio = kwargs.get("nin_folio")
        record_id = kwargs.get("record_id")

        if inc_folio:
            match_query.update({"folio":inc_folio})
        if nin_folio:
            match_query.update({"folio": {"$ne":nin_folio }})

        if record_id:
            match_query.update({"_id": {"$ne": ObjectId(record_id) }})
        return match_query
  
    def stock_in_dest_location_form_many(self, product_code=None, lot_number=None, warehouse=None, location=None, date_from=None, date_to=None, status='done', **kwargs):
        unwind =None
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.STOCK_MANY_LOCATION_2_ONE,
            }
        unwind_query = {}
        unwind = {'$unwind': '$answers.{}'.format(self.f['move_group'])}
        match_query.update(self.stock_kwargs_query(**kwargs))
        if status:
            match_query.update({f"answers.{self.f['inv_adjust_status']}":status})
        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field_id=self.f['grading_date']))
        if product_code:
            match_query.update({f"answers.{self.Product.SKU_OBJ_ID}.{self.f['product_code']}":product_code})
        if warehouse:
            match_query.update({f"answers.{self.WH.WAREHOUSE_LOCATION_DEST_OBJ_ID}.{self.f['warehouse_dest']}":warehouse})      
        if location:
            match_query.update({f"answers.{self.WH.WAREHOUSE_LOCATION_DEST_OBJ_ID}.{self.f['warehouse_location_dest']}":location})
        if lot_number:
            unwind_query.update({f"answers.{self.f['move_group']}.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['product_lot']}":lot_number})
        project = {'$project':
                {'_id': 1,
                    'product_code': f"$answers.{self.Product.SKU_OBJ_ID}.{self.f['product_code']}",
                    'total': f"$answers.{self.f['move_group']}.{self.f['inv_move_qty']}",
                    }
            }
        query= [{'$match': match_query }]
        query.append(unwind)
        query.append({'$match': unwind_query })
        query.append(project)
        query += [
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
        # print('query=', simplejson.dumps(query, indent=4))
        res = self.cr.aggregate(query)
        result = {}
        for r in res:
            pcode = r.get('product_code')
            result[pcode] = result.get(pcode, 0)        
            result[pcode] += r.get('total',0)
        if product_code:
            result = result.get(product_code,0)
        # print('SELECCION DE PLANTA', result)
        return result  

    def stock_moves(self, move_type, product_code=None, sku=None, lot_number=None, warehouse=None, location=None, date_from=None, date_to=None, status='done', **kwargs):
        unwind =None
        if move_type not in ('in','out'):
            raise('Move type only accepts values "in" or "out" ')
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.STOCK_MOVE_FORM_ID  
            }
        unwind_query = {}
        match_query.update(self.stock_kwargs_query(**kwargs))
        if product_code:
            match_query.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_code']}":product_code})
        if sku:
            match_query.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['sku']}":sku})
        if lot_number:
            match_query.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_lot']}":lot_number})
        if status:
            match_query.update({f"answers.{self.f['inv_adjust_status']}":status})
        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field_id=self.f['grading_date']))

        unwind = {'$unwind': '$answers.{}'.format(self.f['move_group'])}
        if move_type =='out':
            if warehouse:
                unwind_query.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['warehouse']}":warehouse})      
            if location:
                unwind_query.update({f"answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['warehouse_location']}":location})

        if move_type =='in':
            if warehouse:
                # warehouse = warehouse.lower().replace(' ', '_')
                unwind_query.update({f"answers.{self.f['move_group']}.{self.WH.WAREHOUSE_LOCATION_DEST_OBJ_ID}.{self.f['warehouse_dest']}":warehouse})    
            if location:
                unwind_query.update({f"answers.{self.f['move_group']}.{self.WH.WAREHOUSE_LOCATION_DEST_OBJ_ID}.{self.f['warehouse_location_dest']}":location})   
       
        project = {'$project':
                {'_id': 1,
                    'product_code': f"$answers.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_code']}",
                    'total': f"$answers.{self.f['move_group']}.{self.f['move_group_qty']}",
                    }
            }
        

        query= [{'$match': match_query }]
        if unwind:
            query.append(unwind)
            query.append({'$match': unwind_query })
        query.append(project)
        query += [
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
        # if move_type == 'out':
        #     print('query=', simplejson.dumps(query, indent=3))
        for r in res:
            pcode = r.get('product_code')
            result[pcode] = result.get(pcode, 0)        
            result[pcode] += r.get('total',0)
        if product_code:
            result = result.get(product_code,0)
            if move_type == 'out':
                result += self.stock_many_locations_out(
                    product_code=product_code,
                    sku=sku,
                    lot_number=lot_number,
                    warehouse=warehouse,
                    location=location,
                    date_from=date_from,
                    date_to=date_to,
                    status=status,
                    **kwargs
                )
                result += self.stock_many_locations_2_one(
                    product_code=product_code,
                    sku=sku,
                    lot_number=lot_number,
                    warehouse=warehouse,
                    location=location,
                    date_from=date_from,
                    date_to=date_to,
                    status=status,
                    **kwargs
                )
            if move_type == 'in':
                result += self.stock_in_dest_location_form_many(
                    product_code=product_code,
                    sku=sku,
                    lot_number=lot_number,
                    warehouse=warehouse,
                    location=location,
                    date_from=date_from,
                    date_to=date_to,
                    status=status,
                    **kwargs
                )
        return result 

    def stock_many_locations_out(self, product_code=None, sku=None, lot_number=None, warehouse=None, location=None, date_from=None, date_to=None, status='done', **kwargs):
        unwind =None
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.STOCK_MANY_LOCATION_OUT,
            }
        unwind_query = {}
        unwind = {'$unwind': '$answers.{}'.format(self.f['move_group'])}
        match_query.update(self.stock_kwargs_query(**kwargs))
        if status:
            match_query.update({f"answers.{self.f['inv_adjust_status']}":status})
        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field_id=self.f['grading_date']))
        if product_code:
            match_query.update({f"answers.{self.Product.SKU_OBJ_ID}.{self.f['product_code']}":product_code})
        if lot_number:
            unwind_query.update({f"answers.{self.f['move_group']}.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_lot']}":lot_number})
        if warehouse:
            unwind_query.update({f"answers.{self.f['move_group']}.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['warehouse']}":warehouse})      
        if location:
            unwind_query.update({f"answers.{self.f['move_group']}.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['warehouse_location']}":location})
        project = {'$project':
                {'_id': 1,
                    'product_code': f"$answers.{self.Product.SKU_OBJ_ID}.{self.f['product_code']}",
                    'total': f"$answers.{self.f['move_group']}.{self.f['inv_move_qty']}",
                    }
            }
        query= [{'$match': match_query }]
        query.append(unwind)
        query.append({'$match': unwind_query })
        query.append(project)
        query += [
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
        # print('query out=', simplejson.dumps(query, indent=4))
        res = self.cr.aggregate(query)
        result = {}
        for r in res:
            pcode = r.get('product_code')
            result[pcode] = result.get(pcode, 0)        
            result[pcode] += r.get('total',0)
        if product_code:
            result = result.get(product_code,0)
        print('result PULL OUT', result)
        return result  

    def stock_many_locations_2_one(self, product_code=None, sku=None, lot_number=None, warehouse=None, location=None, date_from=None, date_to=None, status='done', **kwargs):
        unwind =None
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.STOCK_MANY_LOCATION_2_ONE,
            }
        unwind_query = {}
        match_query.update(self.stock_kwargs_query(**kwargs))
        unwind = {'$unwind': '$answers.{}'.format(self.f['move_group'])}
        if status:
            match_query.update({f"answers.{self.f['inv_adjust_status']}":status})
        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field_id=self.f['grading_date']))
        if product_code:
            match_query.update({f"answers.{self.Product.SKU_OBJ_ID}.{self.f['product_code']}":product_code})
        if lot_number:
            unwind_query.update({f"answers.{self.f['move_group']}.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['product_lot']}":lot_number})
        if warehouse:
            unwind_query.update({f"answers.{self.f['move_group']}.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['warehouse']}":warehouse})      
        if location:
            unwind_query.update({f"answers.{self.f['move_group']}.{self.CATALOG_INVENTORY_OBJ_ID}.{self.f['warehouse_location']}":location})
        project = {'$project':
                {'_id': 1,
                    'product_code': f"$answers.{self.Product.SKU_OBJ_ID}.{self.f['product_code']}",
                    'total': f"$answers.{self.f['move_group']}.{self.f['inv_move_qty']}",
                    }
            }
        query= [{'$match': match_query }]
        query.append(unwind)
        query.append({'$match': unwind_query })
        query.append(project)
        query += [
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
        #print('query=', simplejson.dumps(query, indent=4))
        res = self.cr.aggregate(query)
        result = {}
        for r in res:
            pcode = r.get('product_code')
            result[pcode] = result.get(pcode, 0)        
            result[pcode] += r.get('total',0)
        if product_code:
            result = result.get(product_code,0)
        return result  

    def stock_production(self, date_from=None, date_to=None, product_code=None, warehouse=None, location=None, lot_number=None,  status='done', **kwargs):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.MOVE_NEW_PRODUCTION_ID,
            }
        match_query.update(self.stock_kwargs_query(**kwargs))
        match_query_stage2 = {}
        if date_from or date_to:
            match_query_stage2.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field_id=f"{self.f['set_production_date']}"))
        if product_code:
            match_query.update({f"answers.{self.Product.SKU_OBJ_ID}.{self.f['product_code']}":product_code})
        if status:
            match_query.update({f"answers.{self.f['move_status']}":status})
        if lot_number:
            match_query.update({f"answers.{self.f['product_lot']}":lot_number})  
        if warehouse:
            match_query_stage2.update({f"answers.{self.f['new_location_group']}.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.f['warehouse']}":warehouse})    
        if location:
            match_query_stage2.update({f"answers.{self.f['new_location_group']}.{self.WH.WAREHOUSE_LOCATION_OBJ_ID}.{self.f['warehouse_location']}":location})    
        query= [{'$match': match_query },
            {'$unwind': f"$answers.{self.f['new_location_group']}"},
            ]
        if match_query_stage2:
            query += [{'$match': match_query_stage2 }]
        query += [
            {'$project':
                {'_id': 1,
                    'product_code': f"$answers.{self.Product.SKU_OBJ_ID}.{self.f['product_code']}",
                    'container_type' : f"$answers.{self.f['plant_conteiner_type']}",
                    'racks' : f"$answers.{self.f['new_location_group']}.{self.f['new_location_racks']}",
                    'containers': f"$answers.{self.f['new_location_group']}.{self.f['new_location_containers']}",
                    }
            },
            {'$project':
                {'_id':1,
                    'product_code': "$product_code",
                    'containers': "$containers",                
                    'containers_on_rack' : { "$cond": 
                        [ 
                        {"$eq":["$container_type","baby_jar"]}, 
                        {"$multiply":["$racks", self.container_per_rack['baby_jar']]}, 
                        { "$cond": 
                            [ 
                            {"$eq":["$container_type","magenta_box"]}, 
                            {"$multiply":["$racks", self.container_per_rack['baby_jar']]}, 
                            { "$cond": 
                                [ 
                                {"$eq":["$container_type","clam_shell"]}, 
                                {"$multiply":["$racks", self.container_per_rack['clam_shell']]}, 
                                { "$cond": 
                                    [ 
                                    {"$eq":["$container_type","setis"]}, 
                                    {"$multiply":["$racks", self.container_per_rack['setis']]}, 
                                    0, 
                                 ]}, 
                             ]}, 
                         ]},
                     ]}

                }
            },
            {'$project':
                {'_id':1,
                'product_code': "$product_code",
                'total': {'$sum':['$containers','$containers_on_rack']}
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
        # print('query', simplejson.dumps(query, indent=4))
        res = self.cr.aggregate(query)
        result = {}
        # print('query=',simplejson.dumps(query,indent=4))
        for r in res:
            pcode = r.get('product_code')
            result[pcode] = result.get(pcode, 0)        
            result[pcode] += r.get('total',0)
        if product_code:
            result = result.get(product_code,0)
        return result

    def stock_supplier(self, date_from=None, date_to=None, product_code=None, warehouse=None, location=None, lot_number=None,  status='posted', **kwargs):
        match_query = {
            "deleted_at":{"$exists":False},
            "form_id": self.STOCK_MOVE_FORM_ID,
            }
        match_query.update(self.stock_kwargs_query(**kwargs))
        if product_code:
            match_query.update({f"answers.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['product_code']}":product_code})

        supplier_warehouse = self.get_warehouse(warehouse_type='Supplier')
        if supplier_warehouse:
            match_query.update({f"answers.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['warehouse']}":{"$in":supplier_warehouse}})
        if location:
            match_query.update({f"answers.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['product_code']}":location})
        if lot_number:
            match_query.update({f"answers.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['product_lot']}":lot_number})
        if status:
            match_query.update({f"answers.{self.f['inv_adjust_status']}":status})
        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field_id=self.f['grading_date']))
        query= [{'$match': match_query },
            {'$project':
                {'_id': 1,
                    'product_code': f"$answers.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['product_code']}",
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

    ### STOCK OUT'S

    def stock_scrap(self, product_code=None, warehouse=None, location=None, lot_number=None, date_from=None, date_to=None, status='done', **kwargs):
        match_query = {
            "deleted_at":{"$exists":False},
            # "form_id": {"$in":[self.SCRAP_FORM_ID, self.GRADING_FORM_ID]}
            "form_id": self.SCRAP_FORM_ID
            }
        match_query.update(self.stock_kwargs_query(**kwargs))
        if product_code:
            match_query.update({f"answers.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['product_code']}":product_code})
        if lot_number:
            match_query.update({f"answers.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['product_lot']}":lot_number})
        if warehouse:
            match_query.update({f"answers.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['warehouse']}":warehouse})      
        if location:
            match_query.update({f"answers.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['warehouse_location']}":location}) 
        if status:
            match_query.update({f"answers.{self.f['inv_scrap_status']}":status})
        if date_from or date_to:
            match_query.update(self.get_date_query(date_from=date_from, date_to=date_to, date_field_id=self.f['grading_date']))
        query= [
            {'$match': match_query },
            {'$project':
                {'_id': 1,
                    'product_code': f"$answers.{self.STOCK_INVENTORY_OBJ_ID}.{self.f['product_code']}",
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

        if product_code:
            result_scrap = result.get(product_code,{}).get('scrap',0)
            result_cuarentin = result.get(product_code,{}).get('cuarentin',0) 
            return result_scrap, result_cuarentin
        else:
            return 0, 0

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

    def swap_location_dest(self, from_location):
        res = {self.WH.WAREHOUSE_LOCATION_OBJ_ID:{}}
        res[self.WH.WAREHOUSE_LOCATION_OBJ_ID][self.f['warehouse']] = from_location[self.f['warehouse_dest']]
        res[self.WH.WAREHOUSE_LOCATION_OBJ_ID][self.f['warehouse_location']] = from_location[self.f['warehouse_location_dest']]
        return res

    def swap_location(self, from_location):
        res = {self.WH.WAREHOUSE_LOCATION_DEST_OBJ_ID:{}}
        res[self.WH.WAREHOUSE_LOCATION_DEST_OBJ_ID][self.f['warehouse_dest']] = from_location[self.f['warehouse']]
        res[self.WH.WAREHOUSE_LOCATION_DEST_OBJ_ID][self.f['warehouse_location_dest']] = from_location[self.f['warehouse_location']]
        return res

    def update_calc_fields(self, product_code, lot_number, warehouse, location, folio=None, map_type='model_2_field_id', **kwargs):
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
            'location':location,
        }
        print('----------------------------------------------------')
        print('product_code', product_code)
        print('warehouse', warehouse)
        print('lot_number', lot_number)
        print('location', location)
        stock = self.get_product_stock(product_code, warehouse=warehouse, lot_number=lot_number,location=location, **kwargs)
        print('stock111', stock)

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
            inv = self.get_invtory_record_by_product(self.FORM_INVENTORY_ID, product_code, sku, lot_number, warehouse, location)
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
                print('...folio', folio)
                self.sync_catalog(folio)
        try:
            return update_res.raw_result
        except:
            return update_res

    def update_log_grading(self):
        answers = self.current_record.get('answers',{})
        gradings = answers[self.f['grading_group']]
        rec_date = answers[self.f['grading_date']]
        grading_type = answers[self.f['grading_date']]
        plant_info = answers[self.STOCK_INVENTORY_OBJ_ID]
        product_lot = plant_info.get(self.f['product_lot'])
        product_code = plant_info.get(self.f['product_code'])
        warehouse = plant_info.get(self.f['warehouse'])
        product_stock = self.get_product_stock(product_code, warehouse=warehouse, lot_number=product_lot)
        grading_totals = self.get_grading_sublots(gradings)
        totals = sum(x for x in grading_totals.values())
        acctual_containers = product_stock['actuals']

    def update_stock(self, answers={}, form_id=None, folios="" ):
        print('patch stock folio', folios)
        if not answers:
            answers={"udpate":True}
        if not form_id:
            form_id = self.FORM_INVENTORY_ID
        if type(folios) in [str, ]:
            folios = [folios,]
        return self.lkf_api.patch_multi_record( answers=answers, form_id=form_id, folios=folios, threading=True )

    def validate_move_qty(self, product_code, sku, lot_number, warehouse, location, move_qty, date_to=None):
        inv = self.get_product_stock(product_code, sku=sku,lot_number=lot_number, warehouse=warehouse, location=location,  
            date_to=date_to, **{"nin_folio":self.folio})

        acctual_containers = inv.get('actuals')
        print('acctual_containers',acctual_containers)
        if acctual_containers == 0:
            msg = f"This lot {lot_number} has 0 containers left, if this is NOT the case first do a inventory adjustment"
            msg_error_app = {
                    f"{self.f['product_lot_actuals']}": {
                        "msg": [msg],
                        "label": "Please check your lot inventory",
                        "error":[]
      
                    }
                }
            #TODO set inventory as done
            self.LKFException( simplejson.dumps( msg_error_app ) )   

        if move_qty > acctual_containers:
        # if False:
            #trying to move more containeres that there are...
            cont_diff = move_qty - acctual_containers
            msg = f"There actually only {acctual_containers} containers and you are trying to move {move_qty} containers."
            msg += f"Check this out...! Your are trying to move {cont_diff} more containers than they are. "
            msg += f"If this is the case, please frist make an inventory adjustment of {cont_diff} "
            msg += f"On warehouse {warehouse} at location {location} and lot number {lot_number}"
            msg_error_app = {
                    f"{self.f['inv_move_qty']}": {
                        "msg": [msg],
                        "label": "Please check your Flats to move",
                        "error":[]
      
                    }
                }
            self.LKFException( simplejson.dumps( msg_error_app ) )
        return True
        
    def validate_stock_move(self, from_wl, qty, dest_group):
        qty_to_move = 0
        for dest_set in dest_group:
            to_wh_info = dest_set.get(self.WH.WAREHOUSE_LOCATION_DEST_OBJ_ID,{})
            qty_to_move += dest_set.get(self.f['move_group_qty'],0)
            to_warehouse = to_wh_info.get(self.f['warehouse_dest'])
            to_location = to_wh_info.get(self.f['warehouse_location_dest'])
            to_wl = f'{to_warehouse}__{to_location}'
            if from_wl == to_wl:
                msg = "You need to make the move to a new destination. "
                msg += "Your current from location is: {} and you destination location is:{}".format(
                    from_wl.replace('__', ' '), 
                    to_wl.replace('__', ' '))
                msg_error_app = {
                        f"{self.f['warehouse_location_dest']}": {
                            "msg": [msg],
                            "label": "Please check your destinations location",
                            "error":[]
          
                        }
                    }
                self.LKFException( simplejson.dumps( msg_error_app ) )

        if qty != qty_to_move:
            msg = "Your move out quantity and alocation must be the same "
            msg += f"Your are trying to move out: {qty} products and alocating on the new destination:{qty_to_move}"
            msg_error_app = {
                    f"{self.f['warehouse_location_dest']}": {
                        "msg": [msg],
                        "label": "Please check your destinations location",
                        "error":[]
      
                    }
                }
            self.LKFException( simplejson.dumps( msg_error_app ) )            
        return True

    def validate_value(self, value):
        if value == 'false' or value == 'null':
            return  False
        return value
