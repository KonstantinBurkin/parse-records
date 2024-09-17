import xml.etree.ElementTree as ET
import json


class ParserRecordsToJson:
    """Class to read XML file and Save as JSON"""

    def produce(
        self,
        xml_file_path: str,
        json_file_path: str,
    ) -> None:
        """Read XML file and Save as JSON"""
        xml_data = self._read_xml(xml_file_path)
        root = self._parse_medical_record(xml_data)
        json_data = self._elem_to_dict(root)
        self._save_to_json(json_file_path, json_data)

    # Function to convert the parsed XML element into a Python dictionary
    def _elem_to_dict(
        self,
        elem: ET,
    ) -> dict:
        d = {}
        for child in elem:
            if child.tag not in d:
                d[child.tag] = self._elem_to_dict(child)
            else:
                if not isinstance(d[child.tag], list):
                    d[child.tag] = [d[child.tag]]
                d[child.tag].append(self._elem_to_dict(child))
        d.update(dict(elem.attrib.items()))
        if elem.text and elem.text.strip():
            d["text"] = elem.text.strip()
        else:
            d.pop("text", None)  # Remove empty text fields
        return d

    def _read_xml(
        self,
        xml_file_path: str,
    ) -> str:
        # Read XML data from file
        with open(xml_file_path, "r", encoding="utf-8") as xml_file:
            xml_data = xml_file.read()
        return xml_data

    def _parse_medical_record(
        self,
        xml_data: str,
    ) -> ET:
        # Parse the XML data
        root = ET.fromstring(xml_data)
        return root

    def _save_to_json(
        self,
        json_file_path: str,
        json_data: dict,
    ) -> None:
        """save file as json"""
        # Convert the root element to a dictionary and save to JSON file
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)
