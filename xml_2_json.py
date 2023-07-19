
import xml.etree.ElementTree as ET
import json, simplejson
from copy import deepcopy

def file(file_path, file_name):
    f = open( "./{}/{}".format(file_path, file_name) )
    return  f.read() 

def get_same_properites(key, values):
    if values.get(key):
        update_vals = values.pop(key)
        values.update(update_vals)
    return values

def xml_to_json3(xml_data):
    # Create an ElementTree object from the XML data
    tree = ET.ElementTree(ET.fromstring(xml_data))
    # Function to recursively convert XML elements to JSON
    def element_to_json(element):
        data = {}
        # Process attributes of the element (excluding "item" elements)
        if element.tag != "item" and element.attrib:
            data[element.tag] = data.get(element.tag,{})
            data[element.tag].update(element.attrib)
            # data["@attributes"] = element.attrib
        # Process child elements of the element
        if element.findall("*"):
            for child in element:
                if child.tag == "item":
                    if child.tag in data:
                        if isinstance(data[child.tag], list):
                            data[child.tag].append(element_to_json(child))
                        else:
                            data[child.tag] = [data[child.tag], element_to_json(child)]
                    else:
                        data[child.tag] = [element_to_json(child)]
                else:
                    if child.tag in data:
                        if isinstance(data[child.tag], list):
                            data[child.tag].append(element_to_json(child))
                        else:
                            data[child.tag] = [data[child.tag], element_to_json(child)]
                    else:
                        res = element_to_json(child)
                        child_data = deepcopy(res)
                        if isinstance(child_data, dict):
                            for key, value in child_data.items():
                                if key == 'item':
                                    data[child.tag] = data.get(child.tag, [])
                                    data[child.tag] = value
                                else:
                                    data[child.tag] = data.get(child.tag, {})
                                    ch_data = get_same_properites(child.tag, res)
                                    data[child.tag] = ch_data
                        else:
                            data[child.tag] = child_data
        # Process text content of the element
        if element.text:
            text = element.text.strip()
            if data:
                if text:
                    data['value'] = text
                #Do not delete or move
                pass
            else:
                data = text
        return data
    # Convert the root element to JSON
    json_data = element_to_json(tree.getroot())
    return json.dumps(json_data, indent=4)

def transform_dict_values(data):
    return { k:(transform_values(v)) for k,v in data.items()}

def transform_values(value):
    #check if is boolean
    if value == 'False' or value == 'false' or value == False:
        value = False
    elif value == 'True' or value == 'true' or value == True:
        value = True
    elif value == 'None' or value == 'none' or value == None or not value:
        value = None
    elif value == '[]':
        return []
    elif value == '{}':
        return {}
    else:
        #checks if its a numeric value
        value = get_numeric(value)
    return value

def get_numeric(value):
    if isinstance(value, str):
        has_decimal = value.find('.')
        if has_decimal < 0:
            try:
                value = int(value)
            except ValueError:
                return value
        else:
            try:
                value = float(value)
            except:
                return value
    return value

def get_same_properites(key, values):
    if values.get(key):
        update_vals = values.pop(key)
        values.update(update_vals)
    return values

def xml_to_json(xml_data):
    #TODO AGUAS CON LOS ENTEROS
    # Create an ElementTree object from the XML data
    tree = ET.ElementTree(ET.fromstring(xml_data))
    # Function to recursively convert XML elements to JSON
    def element_to_json(element):
        data = {}
        # Process attributes of the element (excluding "item" elements)
        if element.tag != "item" and element.attrib:
            #TODO SPECIAL ATRIBUTS LIKE A VALUE IS A STRING NOT AN INTEGER
            data[element.tag] = data.get(element.tag,{})
            data[element.tag].update(element.attrib)
            # data["@attributes"] = element.attrib
        # Process child elements of the element
        if element.findall("*"):
            for child in element:
                if child.tag == "item":
                    if child.tag in data:
                        if isinstance(data[child.tag], list):
                            data[child.tag].append(element_to_json(child))
                        else:
                            data[child.tag] = [data[child.tag], element_to_json(child)]
                    else:
                        data[child.tag] = [element_to_json(child)]
                else:
                    if child.tag in data:
                        if isinstance(data[child.tag], list):
                            data[child.tag].append(element_to_json(child))
                        else:
                            data[child.tag] = [data[child.tag], element_to_json(child)]
                    else:
                        res = element_to_json(child)
                        child_data = deepcopy(res)
                        if isinstance(child_data, dict):
                            if not child_data:
                                data[child.tag] = ''
                            for key, value in child_data.items():
                                if key == 'item':
                                    data[child.tag] = data.get(child.tag, [])
                                    data[child.tag] = value
                                else:
                                    data[child.tag] = data.get(child.tag, {})
                                    ch_data = get_same_properites(child.tag, res)
                                    data[child.tag] = transform_dict_values(ch_data)
                        else:
                            data[child.tag] = transform_values(child_data)
        # Process text content of the element
        if element.text:
            text = element.text.strip()
            if data:
                if text:
                    data['value'] = text
                #Do not delete or move
                pass
            else:
                data = text
        return data
    # Convert the root element to JSON
    json_data = element_to_json(tree.getroot())
    return json_data


# Convert XML to JSON
file_path ='test/items/catalogs'
file_name='employees.xml'

xml_data = file(file_path, file_name)
print(xml_data)
json_output = xml_to_json(xml_data)

print(json_output)

# Example XML data

# Convert XML to JSON
# json_output = xml_to_json(xml_data)

# print(json_output)

# a = xml_to_json3(xml_data)
# print('a',a)
#xml_to_json(xml_data)
# Convert XML to JSON
# json_output = xml_to_json(xml_data)

# print(json_output)

#xml_to_json(xml_data)