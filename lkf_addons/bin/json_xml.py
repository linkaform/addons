import xml.etree.ElementTree as ET
import simplejson, subprocess
import xml.dom.minidom




def file(file_path, file_name):
    f = open( "./{}/{}".format(file_path, file_name) )
    return simplejson.loads( f.read() )


def json_to_xml(json_data):
    # Create the root element of the XML tree
    root = ET.Element('lkf')
    for hashKey in root.iter('$$hashKey'):
        root.remove(hashKey)
    # Function to recursively convert JSON data to XML elements
    def json_to_xml_elements(data, parent):
        for hashKey in parent.iter('$$hashKey'):
             parent.remove(hashKey)
        if isinstance(data, dict):
            if data:
                for key, value in data.items():
                    new_val = {}
                    if key == 'pdfName':
                        if '{{' in value:
                            value = "{% raw %} " + value + " {% endraw %} "
                    if key == '$$hashKey':
                        parent.remove(ET.SubElement(parent, key))
                        continue
                    if key =='filters':
                        if isinstance(value, dict):
                            new_val = {}
                            for k, v in value.items():
                                if k and '/' in k:
                                    new_val.update({k.replace('/','__slash__'):v})
                                else:
                                    new_val.update({k:v})
                        if new_val:
                            value = new_val
                    element = ET.SubElement(parent, key)
                    json_to_xml_elements(value, element)
            else:
                parent.text = '{}'
        elif isinstance(data, list):
            if data == []:
                parent.text = '[]'
            for item in data:
                element = ET.SubElement(parent, 'item')
                json_to_xml_elements(item, element)

        else:
            if isinstance(data, str):
                x = str(data.encode('utf-8').decode('utf-8'))
                if x:
                    parent.text = x
                else:
                    parent.text = ''
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


# #file_path ='stock_move/items/catalogs'
# file_path ='test/items/catalogs'
# file_name='employees.json'

# save_file = './{}/{}'.format(file_path, file_name.replace('.json', '.xml'))
# json_data = file(file_path, file_name)
# # xml_output = json_to_xml(json_data)
# # with open(save_file, 'w') as file:
# #     file.write(xml_output)


