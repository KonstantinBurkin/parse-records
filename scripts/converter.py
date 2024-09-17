import pandas as pd
import xml.etree.ElementTree as ET
from io import StringIO
import json


def xml_to_json(xml_file_path, json_file_path):
    # Read XML data from file
    with open(xml_file_path, 'r', encoding='utf-8') as file:
        xml_data = file.read()

    # Parse the XML data
    root = ET.fromstring(xml_data)
    
    # Function to convert the parsed XML element into a Python dictionary
    def elem_to_dict(elem):
        d = {}
        for child in elem:
            if child.tag not in d:
                d[child.tag] = elem_to_dict(child)
            else:
                if not isinstance(d[child.tag], list):
                    d[child.tag] = [d[child.tag]]
                d[child.tag].append(elem_to_dict(child))
        d.update({k: v for k, v in elem.attrib.items()})
        if elem.text and elem.text.strip():
            d['text'] = elem.text.strip()
        else:
            d.pop('text', None)  # Remove empty text fields
        return d
    
    # Convert the root element to a dictionary and save to JSON file
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json_data = elem_to_dict(root)
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)