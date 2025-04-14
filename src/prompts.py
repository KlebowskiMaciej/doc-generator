# prompts.py
class PromptBuilder:
    def build_param_prompt(self, method_name: str, param_name: str, param_type: str, class_name: str = None,
                           method_desc: str = None) -> str:
        return f"{param_name} ({param_type}): used in {method_name} of {class_name}. Short, clear phrase only."

    def build_method_prompt(self, method_name: str, class_name: str = None) -> str:
        return f"{method_name} in {class_name}: one-line description, no boilerplate, no 'method'."

    def build_field_prompt(self, class_name: str, field_name: str, field_type: str) -> str:
        return f"Short, clear phrase describing {field_name} ({field_type}) in {class_name}. No boilerplate."

    def build_class_prompt(self, class_name: str) -> str:
        return f"Short phrase describing the purpose of '{class_name}' type."

    # Podobnie dla pozostałych