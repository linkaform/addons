# -*- coding: utf-8 -*-
import sys, simplejson, math
from datetime import timedelta, datetime

from linkaform_api import settings, network, utils

from account_utils import get_plant_recipe, select_S4_recipe, get_record_greenhouse_inventory
from magnolia_settings import *


INVENTORY_FORM_ID = 98225



def calculates_inventory_greenhouse(plant_info, planting_house, ready_date, plant_data ):
    #plant_data is an object with the following keys 'qty','recipe', 'planted_date'
    global current_record
    plant_code = plant_info['61ef32bcdf0ec2ba73dec33d']
    greenhouse_inventory = get_record_greenhouse_inventory(ready_date, planting_house, plant_code)

    plant_yearWeek = plant_data.get('plant_date').strftime('%Y%W')
    qty_produced = plant_data.get('qty',0)
    container_type = plant_data.get('container_type')
    qty_per_container = plant_data.get('qty_per_container')
    S4_overage = plant_data.get('recipe').get('S4_overage', 0)
    qty_proyected = math.floor(qty_produced * (1 - S4_overage))
    print('plant_info', plant_info)

    if not greenhouse_inventory:

        answers_to_record = {
            '6271dc35e84e2577579eafeb': qty_produced,
            '6442e25f13879061894b4bb1': ready_date, # Estiated Ready Week
            '620a9ee0a449b98114f61d77': ready_date,
            #'620ad6247a217dbcb888d170': qty_per_container,
            '6441d33a153b3521f5b2afc9': qty_produced, # Containers on hand
            '6442e25f13879061894b4bb2': qty_proyected , # Proyected Containers on hand
            '620a9ee0a449b98114f61d75': int(plant_yearWeek),
            '61ef32bcdf0ec2ba73dec33c': plant_info,
            '6442e4831198daf81456f273': {'6442e4831198daf81456f274':planting_house},
            '620ad6247a217dbcb888d175': 'active',
            '644c36f1d20db114694a495a': 'grading_pending'
        }
        if container_type:
            answers_to_record.update({'6441d33a153b3521f5b2afcb':container_type})
        print('greenhouse_inventory',greenhouse_inventory)

        metadata = lkf_api.get_metadata(INVENTORY_FORM_ID)
        metadata.update({
            'properties': {
                "device_properties":{
                    "system": "Script",
                    "process": 'GreenHouse Inventory',
                    "action": 'Upsert Inventory GreenHouse',
                    "from_folio": current_record.get('folio',''),
                    "archive": "calculates_production_greenhouse.py"
                }
            },
            'answers': answers_to_record
        })
        resp_create = lkf_api.post_forms_answers(metadata, jwt_settings_key='USER_JWT_KEY')
        print('resp_create =',resp_create)
        return resp_create

    new_qty_produced = qty_produced + greenhouse_inventory['answers'].get('6271dc35e84e2577579eafeb', 0)
    new_qty_proyected = qty_proyected + greenhouse_inventory['answers'].get('6442e25f13879061894b4bb2', 0)
    new_qty_flats = qty_produced + greenhouse_inventory['answers'].get('6441d33a153b3521f5b2afc9', 0)
    
    greenhouse_inventory['answers']['6271dc35e84e2577579eafeb'] = new_qty_produced
    greenhouse_inventory['answers']['6442e25f13879061894b4bb2'] = new_qty_proyected
    greenhouse_inventory['answers']['6441d33a153b3521f5b2afc9'] = new_qty_flats
    print('greenhouse_inventory=', greenhouse_inventory)
    resp_update = lkf_api.patch_record(greenhouse_inventory, jwt_settings_key='USER_JWT_KEY')
    print('resp_update =',resp_update)
    return resp_update

def calculates_production_greenhouse():
    global current_record
    if not current_record.get('answers'):
        current_record = lkf_api.read_current_record_from_txt( current_record['answers_url'] )
    planting_house = current_record['answers'].get('6442e4831198daf81456f273', {}).get('6442e4831198daf81456f274')
    plant_info = current_record['answers'].get('61ef32bcdf0ec2ba73dec33c', {})
    plant_code = plant_info.get('61ef32bcdf0ec2ba73dec33d')

    new_production = {}
    recipes = None
    for production in current_record['answers'].get('61f1fab3ce39f01fe8a7ca8c', []):
        production_status = production.get('62e9890c5dec95745c618fc3','progress')
        if production_status == 'progress':

            time_in = production.get('61f1fcf8c66d2990c8fc7cc5')
            time_out = production.get('61f1fcf8c66d2990c8fc7cc6')
            cutter = production.get('62c5ff243c63280985580087',{}).get('62c5ff407febce07043024dd')
            d_time_in = datetime.strptime(time_in, '%H:%M:%S')
            d_time_out = datetime.strptime(time_out, '%H:%M:%S')
            secs = (d_time_out - d_time_in).total_seconds()
            if secs < 0:
                msg = "The time in and time out for the production set of the cutter: {}, is wrong.".format(cutter)
                msg += " It was capture that see started at {} and finished at {}, having a difference of {} seconds.".format(time_in,
                    time_out, secs)
                msg_error_app = {
                         "61f1fcf8c66d2990c8fc7cc5": {"msg": [msg], "label": "Please time in. ", "error": []},
                         "61f1fcf8c66d2990c8fc7cc6": {"msg": [msg], "label": "Please time out. ", "error": []},
                     }
                raise Exception( simplejson.dumps( msg_error_app ) )

            total_hours = secs / 60.0**2
            lunch_brake = production.get('62c6017ff9f71e2a589fb679')
            if lunch_brake == 'sí' or lunch_brake == 'yes':
                total_hours -= 0.5

            production['61f1fcf8c66d2990c8fc7cc7'] = round(total_hours, 2) 
            containers_out = production['61f1fcf8c66d2990c8fc7cc3']

            if total_hours <= 0:
                t_in = d_time_in.strftime('%H:%M')
                t_out = d_time_out.strftime('%H:%M')
                msg = "Double check your time in {} and time out {} input, of {}.".format(t_in, t_out, cutter)
                msg_error_app = {
                         "61f1fcf8c66d2990c8fc7cc5": {"msg": [msg], "label": "Please check your Time In. Was there a lunch brake? ", "error": []},
                         "61f1fcf8c66d2990c8fc7cc6": {"msg": [msg], "label": "Please check your Time Out. Was there a lunch brake?", "error": []}
                     }
                raise Exception( simplejson.dumps( msg_error_app ) )
            
            if not recipes:
                recipes = get_plant_recipe([plant_code,], stage=[4, 'Ln72',])
          
            qty_per_container = recipes.get('6205f73281bb36a6f157335b', [])
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



            production['61f1fcf8c66d2990c8fc7cc9'] = round(flats_per_hour, 2) # Plants per Hour
            production['62e9890c5dec95745c618fc3'] = 'posted'
            plant_date = production['61f1fcf8c66d2990c8fc7cc4']
            plant_date = datetime.strptime(plant_date, '%Y-%m-%d')
            week = plant_date.strftime('%W')
            recipe = select_S4_recipe(recipes[plant_code], week)
            grow_weeks = recipe.get('S4_growth_weeks')
            ready_date = plant_date + timedelta(weeks=grow_weeks)
            ready_date = int(ready_date.strftime('%Y%W'))
            plan_defults = {
                'qty':0,
                'plant_date':plant_date, 
                'qty_per_container':qty_per_container,
                'container_type':container_type,
                'recipe':recipe}
            new_production[ready_date] = new_production.get(ready_date, plan_defults)
            new_production[ready_date]['qty'] += containers_out


    res = []
    for ready_date, plant_data in new_production.items():
        res.append(calculates_inventory_greenhouse(plant_info, planting_house, ready_date, plant_data))
    return res



if __name__ == '__main__':
    print(sys.argv)
    current_record = simplejson.loads( sys.argv[1] )
    data = simplejson.loads( sys.argv[2] )
    config['USER_JWT_KEY'] = data["jwt"].split(' ')[1]
    USER_ID = current_record['user_id']
    settings.config.update(config)
    net = network.Network(settings)
    cr = net.get_collections()
    # ------------------------------------------------------------------------------
    lkf_api = utils.Cache(settings)
    response = calculates_production_greenhouse()
    print('response', response)
    status_code = 0
    res = {}
    for r in response:
        scode = r.get('status_code')
        if scode > 299:
            res['json'] = r.get('json')
        if scode > status_code:
            status_code = scode
    res['status_code'] = status_code

    if status_code > 299:
        msg_error_app = res.get('json', 'Error de Script favor de reportrar con Admin')
        raise Exception( simplejson.dumps(msg_error_app) )
    else:
        sys.stdout.write(simplejson.dumps({
            'status': 101,
            'replace_ans': current_record['answers']
        }))