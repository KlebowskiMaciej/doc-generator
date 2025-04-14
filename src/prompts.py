# prompts.py
class PromptBuilder:
    def build_param_prompt(self, method_name: str, param_name: str, param_type: str, class_name: str = None, method_desc: str = None) -> str:
        return f"""
Generate a one-line description for the parameter '{param_name}' (type: {param_type}) used in method '{method_name}' of class '{class_name}'.
Avoid using words like 'parameter', 'represents', or 'Description:'. Output only the clean sentence to be placed inside <Description>.
""".strip()

    def build_method_prompt(self, method_name: str, class_name: str = None) -> str:
        return f"""
Generate a one-line description for the method '{method_name}' in class '{class_name}'.
Avoid using words like 'method', 'represents', or 'Description:'. Output only the clean sentence to be placed inside <Description>.
""".strip()

    def build_field_prompt(self, class_name: str, field_name: str, field_type: str) -> str:
        return f"""
Generate a one-line description for the field '{field_name}' (type: {field_type}) in class '{class_name}'.
Avoid using words like 'field', 'represents', or 'Description:'. Output only the clean sentence to be placed inside <Description>.
""".strip()

    def build_class_prompt(self, class_name: str) -> str:
        return f"""
Generate a one-line description for the class '{class_name}'.
Avoid using words like 'class', 'represents', or 'Description:'. Output only the clean sentence to be placed inside <Description>.
""".strip()