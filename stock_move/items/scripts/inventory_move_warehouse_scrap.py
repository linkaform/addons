# -*- coding: utf-8 -*-
import sys, simplejson
from linkaform_api import settings, network, utils
from magnolia_settings import *
from account_utils import unlist, get_inventory_flow

def get_answer_catalog_field( answer_field ):
    if type(answer_field) == list and answer_field:
        return answer_field[0]
    return answer_field


def move_location(current_record):
    current_answers = current_record['answers']
    move_lines = current_answers['6310c609bbb3788e5f7ffa46']
    move_type = current_answers['62e9cecfa7d81a71e4b4e6da']

    # Información original del Inventory Flow
    for moves in move_lines:
        info_plant = moves.get('6442cbafb1b1234eb68ec178', {})
        per_container = get_answer_catalog_field( info_plant.get('620ad6247a217dbcb888d170', 0) )
        folio_plant = get_answer_catalog_field( info_plant.get('62c44f96dae331e750428732') )
        if not folio_plant:
            continue
        # Información que modifica el usuario
        containers_out = moves.get('62e9cc6b36cb6821c274eb9c', 0)
        record_inventory_flow = get_inventory_flow(folio_plant, form_id=98225)
        # Consulto el Inventory Flow del registro
        answers = record_inventory_flow.get('answers')
        relocated_containers = abs(answers.get('620ad6247a217dbcb888d17e', 0))
        discard_containers = abs(answers.get('620ad6247a217dbcb888d16d', 0))
        shipped_containers = abs(answers.get('620ad6247a217dbcb888d16e', 0))
        actual_containers_on_hand = int(  answers.get('6441d33a153b3521f5b2afca', 0))
        new_actual_containers_on_hand = actual_containers_on_hand - containers_out
        # print('folio_plant', folio_plant)
        # print('containers_out', containers_out)
        # print('discard_containers', discard_containers)
        # print('actual_containers_on_hand', actual_containers_on_hand)
        # print('new_actual_containers_on_hand', new_actual_containers_on_hand)

        if move_type =='scrap':
            discard_containers = discard_containers + containers_out
        elif move_type == 'pull':
            shipped_containers = shipped_containers + containers_out
        elif move_type == 'sell':
            shipped_containers = shipped_containers + containers_out

        if not per_container:
            per_container = answers.get('620ad6247a217dbcb888d170', 0)

        record_inventory_flow['answers'].update({
            '620ad6247a217dbcb888d17e' : relocated_containers,
            '620ad6247a217dbcb888d16d' : discard_containers,
            '620ad6247a217dbcb888d16e' : shipped_containers,
            '6441d33a153b3521f5b2afca': new_actual_containers_on_hand, # Actual Containers on hand
            '620ad6247a217dbcb888d172': per_container * new_actual_containers_on_hand # Actual Eaches on Hand
        })

        if new_actual_containers_on_hand <= 0:
            record_inventory_flow['answers'].update({
                '620ad6247a217dbcb888d175': 'done'
            })

        record_inventory_flow.update({
            'properties': {
                "device_properties":{
                    "system": "SCRIPT",
                    "process":"Green House - Out",
                    "accion":'Update record Inventory House Inventory',
                    "archive":"inventory_move_greenhouse.py"
                }
            }
        })

        # Se actualiza el Inventory Flow que está seleccionado en el campo del current record
        res_update_inventory = lkf_api.patch_record( record_inventory_flow, jwt_settings_key='USER_JWT_KEY' )
        print('res_update_inventory =',res_update_inventory)

if __name__ == '__main__':
    print(sys.argv)
    current_record = simplejson.loads( sys.argv[1] )
    jwt_complete = simplejson.loads( sys.argv[2] )
    config['USER_JWT_KEY'] = jwt_complete['jwt'].split(' ')[1]
    settings.config.update(config)
    lkf_api = utils.Cache(settings)
    net = network.Network(settings)
    cr = net.get_collections()

    move_location(current_record)
    current_record['answers']['62e9d296cf8d5b373b24e028'] =  'done'
    sys.stdout.write(simplejson.dumps({
        'status': 101,
        'metadata':{'editable':False},
        'replace_ans': current_record['answers'],
        }))
