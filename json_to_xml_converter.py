import json
import logging
import xml.etree.ElementTree as ET
from typing import Optional, Union
from xml.dom import minidom


class JsonToXml:
    def __init__(self, json_string: str) -> None:
        self.json_data = self.string_to_json(json_string)
        self.root = ET.Element("root")

    @staticmethod
    def string_to_json(json_string: str) -> Optional[Union[dict, list]]:
        result = ""
        try:
            result = json.loads(json_string)
        except json.decoder.JSONDecodeError as e:
            logging.error(f"Wrong json format, exception: \n{e}")
        except TypeError:
            result = json_string

        return result

    def add_node(
        self, tmp_root: ET.Element, element: Union[list, dict, str], xml_node_name: str
    ) -> None:
        tmp = ET.SubElement(tmp_root, xml_node_name)
        if isinstance(element, dict):
            self.to_xml(tmp, element)
        elif isinstance(element, list):
            self.to_xml(tmp, element, from_list=True)
        else:
            tmp.text = str(element)

    def to_xml(
        self, tmp_root: ET.Element, tmp_json: Union[list, dict], from_list: bool = False
    ) -> None:
        if from_list:
            for element in tmp_json:
                self.add_node(tmp_root, element, "element")
        else:
            for key in tmp_json:
                self.add_node(tmp_root, tmp_json[key], key)

    def json_to_xml(self) -> ET.Element:
        from_list = True if isinstance(self.json_data, list) else False
        self.to_xml(self.root, self.json_data, from_list)
        return self.root

    def pretty_print_json(self):
        print(json.dumps(self.json_data, indent=3))

    def __repr__(self):
        return minidom.parseString(ET.tostring(self.root)).toprettyxml(indent="   ")
