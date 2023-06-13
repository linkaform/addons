
import xml.etree.ElementTree as ET
import json
from copy import deepcopy

xml_data = """<lkf>
  <templates />
  <catalog_id>102453</catalog_id>
  <confirmation />
  <description />
  <edit_public_records>False</edit_public_records>
  <fields>
    <item>
      <catalog_fields />
      <view_fields />
      <field_id>6474f861bbcd7572f293e1fc</field_id>
      <fav>True</fav>
      <relation_type>None</relation_type>
      <catalog />
      <key>None</key>
      <properties>
        <send_email>False</send_email>
        <custom>None</custom>
        <size>complete</size>
      </properties>
      <related_catalog>None</related_catalog>
      <field_type>text</field_type>
      <required>False</required>
      <related_catalog_key />
      <label>Codigo de Producto</label>
      <catalog_id>None</catalog_id>
      <options />
    </item>
    <item>
      <catalog_fields />
      <view_fields />
      <field_id>6474f861bbcd7572f293e1fd</field_id>
      <fav>True</fav>
      <relation_type>None</relation_type>
      <catalog />
      <key>None</key>
      <properties>
        <send_email>False</send_email>
        <custom>None</custom>
        <size>complete</size>
      </properties>
      <related_catalog>None</related_catalog>
      <field_type>text</field_type>
      <required>False</required>
      <related_catalog_key />
      <label>Nombre de Producto</label>
      <catalog_id>None</catalog_id>
      <options />
    </item>
    <item>
      <catalog_fields />
      <view_fields />
      <field_id>6474f819bbcd7572f293e1f8</field_id>
      <fav>None</fav>
      <relation_type>None</relation_type>
      <catalog>
        <catalog_fields />
        <filters />
        <view_index>0</view_index>
        <catalog_field_id>None</catalog_field_id>
        <catalog_id>102452</catalog_id>
        <view_fields>
          <item>6474f819bbcd7572f293e1f9</item>
        </view_fields>
        <name>Unidad de Medida</name>
      </catalog>
      <key>None</key>
      <properties />
      <related_catalog>None</related_catalog>
      <field_type>catalog</field_type>
      <required>False</required>
      <related_catalog_key />
      <label>Unidad de Medida</label>
      <catalog_id>None</catalog_id>
      <options />
    </item>
    <item>
      <field_type>catalog-select</field_type>
      <required>False</required>
      <field_id>6474f819bbcd7572f293e1f9</field_id>
      <label>Pieza</label>
      <catalog>
        <view_index>1</view_index>
        <catalog_fields />
        <last>False</last>
        <catalog_id>102452</catalog_id>
        <view_fields />
        <field_type>text</field_type>
        <catalog_field_id>6474f819bbcd7572f293e1f8</catalog_field_id>
        <filters />
      </catalog>
      <options />
      <properties />
    </item>
  </fields>
  <_rev>2-aea87b12ad987e78bd3f721a62dde758</_rev>
  <updated_at>2023-05-29T19:09:21.526113+00:00Z</updated_at>
  <sync>
    <element_request />
    <input_parameters />
  </sync>
  <advanced_options />
  <public>False</public>
  <catalog_pages>
    <item>
      <page_fields>
        <item>
          <catalog_fields />
          <view_fields />
          <field_id>6474f861bbcd7572f293e1fc</field_id>
          <fav>True</fav>
          <relation_type>None</relation_type>
          <catalog />
          <key>None</key>
          <properties>
            <send_email>False</send_email>
            <custom>None</custom>
            <size>complete</size>
          </properties>
          <related_catalog>None</related_catalog>
          <field_type>text</field_type>
          <required>False</required>
          <related_catalog_key />
          <label>Codigo de Producto</label>
          <catalog_id>None</catalog_id>
          <options />
        </item>
        <item>
          <catalog_fields />
          <view_fields />
          <field_id>6474f861bbcd7572f293e1fd</field_id>
          <fav>True</fav>
          <relation_type>None</relation_type>
          <catalog />
          <key>None</key>
          <properties>
            <send_email>False</send_email>
            <custom>None</custom>
            <size>complete</size>
          </properties>
          <related_catalog>None</related_catalog>
          <field_type>text</field_type>
          <required>False</required>
          <related_catalog_key />
          <label>Nombre de Producto</label>
          <catalog_id>None</catalog_id>
          <options />
        </item>
        <item>
          <catalog_fields />
          <view_fields />
          <field_id>6474f819bbcd7572f293e1f8</field_id>
          <fav>None</fav>
          <relation_type>None</relation_type>
          <catalog>
            <catalog_fields />
            <filters />
            <view_index>0</view_index>
            <catalog_field_id>None</catalog_field_id>
            <catalog_id>102452</catalog_id>
            <view_fields>
              <item>6474f819bbcd7572f293e1f9</item>
            </view_fields>
            <name>Unidad de Medida</name>
          </catalog>
          <key>None</key>
          <properties />
          <related_catalog>None</related_catalog>
          <field_type>catalog</field_type>
          <required>False</required>
          <related_catalog_key />
          <label>Unidad de Medida</label>
          <catalog_id>None</catalog_id>
          <options />
        </item>
        <item>
          <field_type>catalog-select</field_type>
          <required>False</required>
          <field_id>6474f819bbcd7572f293e1f9</field_id>
          <label>Pieza</label>
          <catalog>
            <view_index>1</view_index>
            <catalog_fields />
            <last>False</last>
            <catalog_id>102452</catalog_id>
            <view_fields />
            <field_type>text</field_type>
            <catalog_field_id>6474f819bbcd7572f293e1f8</catalog_field_id>
            <filters />
          </catalog>
          <options />
          <properties />
        </item>
      </page_fields>
      <page_description>None</page_description>
      <page_name>PAGE 1</page_name>
    </item>
  </catalog_pages>
  <filters />
  <sync_last_update>None</sync_last_update>
  <_id>6474f861bbcd7572f293e1fb</_id>
  <created_at>2023-05-29T19:09:21.526113+00:00Z</created_at>
  <name>Producto</name>
</lkf>"""

# def xml_to_json(xml_data):
#     # Create an ElementTree object from the XML data
#     tree = ET.ElementTree(ET.fromstring(xml_data))
#     # Function to recursively convert XML elements to JSON
#     def element_to_json(element):
#         data = {}
#         # Process attributes of the element
#         if element.attrib:
#             data["@attributes"] = element.attrib
#         # Process child elements of the element
#         if element.findall("*"):
#             for child in element:
#                 child_data = element_to_json(child)
#                 if child.tag in data:
#                     if isinstance(data[child.tag], list):
#                         data[child.tag].append(child_data)
#                     else:
#                         data[child.tag] = [data[child.tag], child_data]
#                 else:
#                     if isinstance(child_data, dict):
#                         print('child.tag', child.tag)
#                         print('keys', child_data.keys())
#                         for attrib in child.tag:
#                             if attrib == 'item':
#                                 print('attrib=',attrib)
#                                 print('==========================')
#                                 print('child_element', child_data[attrib])
#                                 print('child_element', attrib)
#                                 data[child.tag] = child_data[attrib]
#                             else:
#                                 data[child.tag] = child_data
#                     else:
#                         data[child.tag] = child_data
#         # Process text content of the element
#         if element.text:
#             text = element.text.strip()
#             if data:
#                 data["@text"] = text
#             else:
#                 data = text
#         return data
#     # Convert the root element to JSON
#     json_data = element_to_json(tree.getroot())
#     return json.dumps(json_data, indent=4)






# def xml_to_json2(xml_data):
#     # Create an ElementTree object from the XML data
#     tree = ET.ElementTree(ET.fromstring(xml_data))
#     # Function to recursively convert XML elements to JSON
#     def element_to_json(element):
#         data = {}
#         # Process attributes of the element
#         if element.attrib:
#             data["@attributes"] = element.attrib
#         # Process child elements of the element
#         if element.findall("*"):
#             for child in element:

#                 if child.tag == "item":
#                     if child.tag in data:
#                         if isinstance(data[child.tag], list):
#                             print('child.tag======1',child.tag)
#                             data[child.tag].append(element_to_json(child))
#                         else:
#                             print('child.tag======0****************',child.tag)
#                             print('child.tag======0*****>>>>>>>>>',data[child.tag])
#                             data[child.tag] = [data[child.tag], element_to_json(child)]
#                             #data[child.tag] = element_to_json(child)
#                     else:
#                         print('child.tag======0',child.tag)
#                         data[child.tag] = element_to_json(child)
#                 else:
#                     print('else, ', child.tag)
#                     if child.tag in data:
#                         if isinstance(data[child.tag], list):
#                             data[child.tag].append(element_to_json(child))
#                         else:
#                             data[child.tag] = [data[child.tag], element_to_json(child)]
#                     else:
#                         child_element = element_to_json(child)
#                         if isinstance(child_element, dict):
#                             for attrib in child_element:
#                                 if attrib == 'item':
#                                     print('attrib=',attrib)
#                                     print('==========================')
#                                     print('child_element', child_element[attrib])
#                                     print('child_element', attrib)
#                                     data[child.tag] = child_element[attrib]
#                                 else:
#                                     data[child.tag] = child_element
#                         else:
#                             data[child.tag] = child_element
#         # Process text content of the element
#         if element.text:
#             text = element.text.strip()
#             if data:
#                 data["@text"] = text
#             else:
#                 data = text
#         return data
#     # Convert the root element to JSON
#     json_data = element_to_json(tree.getroot())
#     return json.dumps(json_data, indent=4)

# # Example XML data
# xml_data2 = '''
# <root>
#     <name>John Doe</name>
#     <items>
#         <item>Apple</item>
#         <item>Banana</item>
#         <item>Orange</item>
#     </items>
# </root>
# '''




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

# Example XML data
xml_data2 = '''
<root>
    <name>John Doe</name>
    <items>
        <item>
          <name>Banana</name>
          <properties has_val="dos" send_mail="true">
                <send_email>False</send_email>
                <custom>None</custom>
                <size>complete</size>
          </properties>
          <catalog>
            <view_index>1</view_index>
            <catalog_fields />
            <last>False</last>
            <catalog_id>102452</catalog_id>
            <view_fields />
            <field_type>text</field_type>
            <catalog_field_id has_val="dos" send_mail="true">6474f819bbcd7572f293e1f8</catalog_field_id>
            <filters />
          </catalog>
        </item>
        <item>Orange</item>
        <item>Banana</item>
    </items>
</root>
'''

# Convert XML to JSON
json_output = xml_to_json3(xml_data)

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