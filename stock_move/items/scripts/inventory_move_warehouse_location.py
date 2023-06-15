# -*- coding: utf-8 -*-
import sys, simplejson
from copy import deepcopy
from math import floor

from linkaform_api import settings, network, utils
from magnolia_settings import *
from account_utils import unlist, get_inventory_flow, get_record_greenhouse_inventory


INVENTORY_FORM_ID = 98225


# # def update_origin_log(record_inventory_flow, inv_record, flats_to_move, acctual_containers):
#     update_rec = {}
#     print('record_inventory_flow',record_inventory_flow)
#     print('record_inventory_flow',record_inventory_flowstp)
#     scrapped_qty = inv_record.get('620ad6247a217dbcb888d16d', 0)
#     sell = inv_record.get('6442e2fbc0dd855fe856f1da',0)
#     proyected = inv_record.get('6442e25f13879061894b4bb2', 0)
#     if flats_to_move < acctual_containers:
#         #Partial move
#         relocated_containers = inv_record.get('620ad6247a217dbcb888d17e', 0)
#         #SCRAPPED
#         new_lot_scrapped = floor((flats_to_move * scrapped_qty )/ acctual_containers)
#         old_scapped = scrapped_qty - new_lot_scrapped
#         #SELL
#         new_lot_sell = floor((flats_to_move * sell )/ acctual_containers)
#         old_sell = sell - new_lot_sell
#         #PROYECTED
#         new_lot_proyected = floor((flats_to_move * proyected )/ acctual_containers)
#         old_proyected = proyected - new_lot_proyected
#         old_actuals = acctual_containers - flats_to_move
#         relocated_containers += flats_to_move
#         print('inv_record', inv_record)
#         inv_record.update({
#             '6441d33a153b3521f5b2afc9': old_actuals, # Containers on hand
#             '620ad6247a217dbcb888d16d': old_scapped, # Scrapped Containers
#             '620ad6247a217dbcb888d17e': relocated_containers, # Scrapped Containers
#             '6442e2fbc0dd855fe856f1da': old_sell, # Sell Containers
#             '6442e25f13879061894b4bb2': old_proyected, # Proyected Containers
#             })
#         update_rec.update({
#                     '6441d33a153b3521f5b2afc9': flats_to_move, # Containers on hand
#                     '620ad6247a217dbcb888d16d': new_lot_scrapped, # Scrapped Containers
#                     '6442e2fbc0dd855fe856f1da': new_lot_sell, # Sell Containers
#                     '6442e25f13879061894b4bb2': new_lot_proyected, # Proyected Containers
#                 })  
#     else:
#         #Moving the hole lote
#         inv_record.update({
#             '6441d33a153b3521f5b2afc9': 0,
#             '620ad6247a217dbcb888d175': 'done', # Status
#             '620ad6247a217dbcb888d17e': flats_to_move, # Relocated Containers
#         })
#         update_rec.update({
#             '6441d33a153b3521f5b2afc9': flats_to_move, # Containers on hand
#             '620ad6247a217dbcb888d16d': scrapped_qty, # Scrapped Containers
#             '6442e2fbc0dd855fe856f1da': sell, # Sell Containers
#             '6442e25f13879061894b4bb2': proyected, # Proyected Containers
#         })  


#     #update origin folio
#     record_inventory_flow['answers'] = inv_record
#     record_inventory_flow['properties'] = {
#             "device_properties":{
#                 "system": "Script",
#                 "process": 'Green House Inventory Move',
#                 "action": 'Made a partial lot',
#                 "archive": "inventory_move_greenhouse_location.py"
#             }
#         }
#     response = lkf_api.patch_record(record_inventory_flow, jwt_settings_key='USER_JWT_KEY')
#     response = {'status_code':201}
#     print('response', response)
#     return response, update_rec

def move_location(current_record):
    current_answers = current_record['answers']
    plant_info = current_answers.get('6442cbafb1b1234eb68ec178',{})
    folio_inventory = plant_info.get('62c44f96dae331e750428732')
    ready_date = plant_info.get('620a9ee0a449b98114f61d77')
    plant_code = plant_info.get('61ef32bcdf0ec2ba73dec33d')
    record_inventory_flow = get_inventory_flow(folio_inventory, form_id=98225)
    inv_record = record_inventory_flow.get('answers')
    print('folio_inventory=', folio_inventory)
    print('record_inventory_flow=', record_inventory_flow)
    relocated_containers = sum( [s.get('6442e4cc45983bf1778ec17d', 0) for s in current_answers.get('6442e4537775ce64ef72dd69')] )
    flats_to_move = current_answers.get('6442e4537775ce64ef72dd68')
    acctual_containers = inv_record.get('6441d33a153b3521f5b2afc9',0)

    if acctual_containers == 0:
        msg = "This lot has no containers left, if this is NOT the case first do a inventory adjustment"
        msg_error_app = {
                "6441d33a153b3521f5b2afc9": {
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
                "6442e4537775ce64ef72dd68": {
                    "msg": [msg],
                    "label": "Please check your Flats to move",
                    "error":[]
  
                }
            }
        raise Exception( simplejson.dumps( msg_error_app ) )

    current_green_house = plant_info.get('6442e4831198daf81456f274')
    dest_gh_select = current_answers.get('644897497a16141f4e5ee0c3')
    dest_green_house = ""
    for x in dest_gh_select.split('_'):
        if dest_green_house:
            dest_green_house += " "
        dest_green_house += x.title()

    if current_green_house == dest_green_house:
        msg = "You need to make the move to a new destination. "
        msg += "Your current from location is: {} and you destination location is:{}".format(current_green_house, dest_green_house)
        msg_error_app = {
                "644897497a16141f4e5ee0c3": {
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
        msg += " for location {} and ready date {}".format(current_green_house, ready_date )
        msg_error_app = {
                "6442e4537775ce64ef72dd68": {
                    "msg": [msg],
                    "label": "Please check your Flats to move",
                    "error":[]
  
                }
            }
        raise Exception( simplejson.dumps( msg_error_app ) )

    print('searching fro', ready_date, dest_green_house, plant_code)
    dest_greenhouse_inventory = get_record_greenhouse_inventory(ready_date, dest_green_house, plant_code)
    dest_folio = None
    if not dest_greenhouse_inventory:
        new_inv_rec = deepcopy(inv_record)
        new_inv_rec.update({
            '6442e4831198daf81456f273': {'6442e4831198daf81456f274':dest_green_house},
            '6441d33a153b3521f5b2afc9': flats_to_move,
            '620ad6247a217dbcb888d175': 'active',
        })  
        metadata = lkf_api.get_metadata(INVENTORY_FORM_ID) 
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
        response = lkf_api.post_forms_answers(metadata, jwt_settings_key='USER_JWT_KEY')
        if response.get('status_code') > 299 or not response.get('status_code'):
            print('response=',response)
            msg_error_app = response.get('json', 'Error al acomodar producto , favor de contactar al administrador')
            raise Exception( simplejson.dumps(msg_error_app) )
        x = simplejson.loads(response['data'])
        dest_folio = x.get('folio')
    else:
        # Adding up to an existing lot
        # response, update_rec = update_origin_log(record_inventory_flow, inv_record, flats_to_move, acctual_containers)
        print('TODO=', dest_greenhouse_inventory)
        print('destinatnio folio', dest_greenhouse_inventory.get('folio'))
        dest_folio = dest_greenhouse_inventory.get('folio')
        # dest_greenhouse_inventory['answers']['6441d33a153b3521f5b2afc9'] += flats_to_move
        # response = lkf_api.patch_record(dest_greenhouse_inventory, jwt_settings_key='USER_JWT_KEY')
    return dest_folio

if __name__ == '__main__':
    print(sys.argv)
    current_record = simplejson.loads( sys.argv[1] )
    jwt_complete = simplejson.loads( sys.argv[2] )
    config['USER_JWT_KEY'] = jwt_complete['jwt'].split(' ')[1]
    settings.config.update(config)
    lkf_api = utils.Cache(settings)
    net = network.Network(settings)
    cr = net.get_collections()

    dest_folio = move_location(current_record)
    current_record['answers']['6442e4537775ce64ef72dd6a'] =  'done'
    current_record['answers']['ffff00000000000000000001'] =  dest_folio
    # sys.stdout.write(simplejson.dumps({
    #     'status': 206,
    #     'metadata':{'editable':False},
    #     'replace_ans': current_record['answers'],
    #     }))        
    sys.stdout.write(simplejson.dumps({
        'status': 206,
        # 'metadata':{'editable':False},
        'merge': {
            'answers': current_record['answers']},
        }))
