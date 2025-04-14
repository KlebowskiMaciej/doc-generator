# xml_parser.py
import xml.etree.ElementTree as ET
from tqdm import tqdm

class XMLDocUpdater:
    def __init__(self, model, prompt_builder, logger):
        self.model = model
        self.prompt_builder = prompt_builder
        self.logger = logger

    def process_file(self, input_path: str, output_path: str):
        self.logger.info(f"Parsing XML file: {input_path}")
        tree = ET.parse(input_path)
        root = tree.getroot()

        methods = root.findall(".//BoMethod")
        params = root.findall(".//BoParameter")
        returns = root.findall(".//ReturnParameter")
        classes = root.findall(".//BoDataType")

        total = len(methods) + len(params) + len(returns) + len(classes)
        with tqdm(total=total, desc="Updating XML", unit="element") as pbar:
            for method in methods:
                self._update_method(method)
                pbar.update(1)
            for param in params:
                self._update_param(param)
                pbar.update(1)
            for ret in returns:
                self._update_param(ret)
                pbar.update(1)
            for cls in classes:
                self._update_class(cls)
                pbar.update(1)

        tree.write(output_path, encoding="utf-8", xml_declaration=True)
        self.logger.info(f"Wrote updated XML to: {output_path}")

    def _is_empty_description(self, element):
        desc_elem = element.find("Description")
        return desc_elem is not None and (desc_elem.text is None or not desc_elem.text.strip())

    def _update_method(self, method):
        if not self._is_empty_description(method):
            return
        name = method.findtext("Name")
        class_elem = method.find("../..")
        class_name = class_elem.findtext("ShortName") if class_elem is not None else "UnknownClass"
        self.logger.info(f"Updating method: {class_name}.{name}")
        prompt = self.prompt_builder.build_method_prompt(method_name=name, class_name=class_name)
        description = self.model.complete(prompt)
        method.find("Description").text = description

    def _update_param(self, param):
        if not self._is_empty_description(param):
            return
        name = param.findtext("Name")
        param_type = param.findtext("Type")
        method_elem = param.find("../../..")
        method_name = method_elem.findtext("Name") if method_elem is not None else "UnknownMethod"
        class_elem = method_elem.find("../..") if method_elem is not None else None
        class_name = class_elem.findtext("ShortName") if class_elem is not None else "UnknownClass"
        method_desc = method_elem.findtext("Description") if method_elem is not None else None
        self.logger.info(f"Updating parameter: {class_name}.{method_name}({name})")
        prompt = self.prompt_builder.build_param_prompt(method_name, name, param_type, class_name, method_desc)
        description = self.model.complete(prompt)
        param.find("Description").text = description

    def _update_class(self, cls):
        if self._is_empty_description(cls):
            class_name = cls.findtext("LocalName")
            self.logger.info(f"Updating class: {class_name}")
            prompt = self.prompt_builder.build_class_prompt(class_name)
            description = self.model.complete(prompt)
            cls.find("Description").text = description

        for field in cls.findall(".//BoField"):
            self._update_field(field, cls.findtext("LocalName"))

    def _update_field(self, field, class_name):
        if not self._is_empty_description(field):
            return
        name = field.findtext("Name")
        field_type = field.findtext("Type")
        self.logger.info(f"Updating field: {class_name}.{name}")
        prompt = self.prompt_builder.build_field_prompt(class_name, name, field_type)
        description = self.model.complete(prompt)
        field.find("Description").text = description
