from json_xml import json_to_xml

res= {'templates': [], 'confirmation': {'message': '¡Su información fue capturada!', 'button_message': 'Mandar/respuestas', 'redirect_url': 'default'}, 'description': '', '_rev': '13-ef1e8df6bb1f87ff0f7df11125e2aaa1', 'updated_at': '2020-08-17T22:31:23.421660+00:00Z', 'sync': {'element_request': {}, 'input_parameters': []}, 'filters': {'client_6/doritos': None, 'doritos': {'amp_and': [{'c17f50bb9d9754fefc79e003': {'amp_eq': 'Doritos'}}]}, 'Prueba_': {'amp_and': [{'c17f50bb9d9754fefc79e002': {'amp_eq': 'Coca Cola'}}]}, 'Pepsi': {'amp_and': [{'c17f50bb9d9754fefc79e002': {'amp_eq': 'Pepsi Cola'}}]}, 'Prueba': {'amp_and': [{'c17f50bb9d9754fefc79e002': {'amp_eq': 'Pepsi Cola'}}]}, 'prueba': {'amp_and': [{'c17f50bb9d9754fefc79e002': {'amp_eq': 'Coca Cola'}}]}}, 'name': 'Productos', 'edit_public_records': False }



catalog_data_xml = json_to_xml(res)
