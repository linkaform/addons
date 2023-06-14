import xml.etree.ElementTree as ET
import simplejson, subprocess
import xml.dom.minidom




def file(file_path, file_name):
    f = open( "./{}/{}".format(file_path, file_name) )
    return simplejson.loads( f.read() )


def json_to_xml(json_data):
    # Create the root element of the XML tree
    root = ET.Element('lkf')
    # Function to recursively convert JSON data to XML elements
    def json_to_xml_elements(data, parent):
        if isinstance(data, dict):
            for key, value in data.items():
                element = ET.SubElement(parent, key)
                json_to_xml_elements(value, element)
        elif isinstance(data, list):
            for item in data:
                element = ET.SubElement(parent, 'item')
                json_to_xml_elements(item, element)
        else:
            if isinstance(data, str):
                x = str(data.encode('utf-8').decode('utf-8'))
                parent.text = x
            else:
                parent.text = str(data)
    # Convert JSON data to XML elements
    json_to_xml_elements(json_data, root)
    # Create an XML tree from the root element
    tree = ET.ElementTree(root)
    # Convert the XML tree to a string
    xml_str = ET.tostring(root, encoding='utf-8').decode()
    dom = xml.dom.minidom.parseString(xml_str)
    xml_str = dom.toprettyxml(indent="    ")
    return xml_str

# Convert JSON to XML


#file_path ='stock_move/items/catalogs'
file_path ='stock_move/items/forms'
file_name='wharehouse_inventory_move_workflow.json'

save_file = './{}/{}'.format(file_path, file_name.replace('.json', '.xml'))
json_data = file(file_path, file_name)
xml_output = json_to_xml(json_data)
with open(save_file, 'w') as file:
    file.write(xml_output)


