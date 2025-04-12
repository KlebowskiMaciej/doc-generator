
import xml.etree.ElementTree as ET

class XMLDocUpdater:
    def __init__(self, model, prompt_builder):
        self.model = model
        self.prompt_builder = prompt_builder

    def process_file(self, input_path: str, output_path: str):
        tree = ET.parse(input_path)
        root = tree.getroot()

        # Metody
        for method in root.findall(".//BoMethod"):
            self._update_method(method)

        # Parametry
        for param in root.findall(".//BoParameter"):
            self._update_param(param)

        # ReturnParameter
        for ret in root.findall(".//ReturnParameter"):
            self._update_param(ret)

        # Klasy
        for cls in root.findall(".//BoDataType"):
            self._update_class(cls)

        tree.write(output_path, encoding="utf-8", xml_declaration=True)

    def _update_method(self, method):
        name = method.findtext("Name")
        class_elem = method.find("../..")  # BoInterface
        class_name = class_elem.findtext("ShortName") if class_elem is not None else "UnknownClass"
        desc_elem = method.find("Description")
        if desc_elem is None or not desc_elem.text or not desc_elem.text.strip():
            prompt = self.prompt_builder.build_method_prompt(method_name=name, class_name=class_name)
            description = self.model.complete(prompt)
            if desc_elem is None:
                desc_elem = ET.SubElement(method, "Description")
            desc_elem.text = description

    def _update_param(self, param):
        name = param.findtext("Name")
        param_type = param.findtext("Type")
        method_elem = param.find("../../..")  # BoMethod
        method_name = method_elem.findtext("Name") if method_elem is not None else "UnknownMethod"
        class_elem = method_elem.find("../..") if method_elem is not None else None
        class_name = class_elem.findtext("ShortName") if class_elem is not None else "UnknownClass"
        method_desc = method_elem.findtext("Description") if method_elem is not None else None

        desc_elem = param.find("Description")
        if desc_elem is None or not desc_elem.text or not desc_elem.text.strip():
            prompt = self.prompt_builder.build_param_prompt(method_name, name, param_type, class_name, method_desc)
            description = self.model.complete(prompt)
            if desc_elem is None:
                desc_elem = ET.SubElement(param, "Description")
            desc_elem.text = description

    def _update_class(self, cls):
        class_name = cls.findtext("LocalName")
        desc_elem = cls.find("Description")
        if desc_elem is None or not desc_elem.text or not desc_elem.text.strip():
            prompt = self.prompt_builder.build_class_prompt(class_name)
            description = self.model.complete(prompt)
            if desc_elem is None:
                desc_elem = ET.SubElement(cls, "Description")
            desc_elem.text = description

        # Pola
        for field in cls.findall(".//BoField"):
            self._update_field(field, class_name)

    def _update_field(self, field, class_name):
        name = field.findtext("Name")
        field_type = field.findtext("Type")
        desc_elem = field.find("Description")
        if desc_elem is None or not desc_elem.text or not desc_elem.text.strip():
            prompt = self.prompt_builder.build_field_prompt(class_name, name, field_type)
            description = self.model.complete(prompt)
            if desc_elem is None:
                desc_elem = ET.SubElement(field, "Description")
            desc_elem.text = description
