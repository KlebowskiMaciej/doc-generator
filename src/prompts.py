class PromptBuilder:
    def build_param_prompt(self, method_name: str, param_name: str, param_type: str, class_name: str = None, method_desc: str = None) -> str:
        return f"""
In the `{class_name}` class, there is a method `{method_name}`{f' described as: "{method_desc}"' if method_desc else ''}.

This method takes a parameter named `{param_name}` of type `{param_type}`.

Write a technical documentation-style description for this parameter in the format of C# XML <Description>. Be concise, precise, and professional:
""".strip()

    def build_method_prompt(self, method_name: str, class_name: str = None) -> str:
        return f"""
There is a method named `{method_name}` in the `{class_name}` class.

Write a technical documentation-style description for this method in the format of C# XML <Description>. Be concise and clearly describe its purpose and behavior:
""".strip()

    def build_field_prompt(self, class_name: str, field_name: str, field_type: str) -> str:
        return f"""
The `{class_name}` class contains a field `{field_name}` of type `{field_type}`.

Write a technical documentation-style description for this field in the format of C# XML <Description>. Be concise and professional:
""".strip()

    def build_class_prompt(self, class_name: str) -> str:
        return f"""
A class named `{class_name}` is defined.

Write a brief and technical description of this class in the style of C# XML documentation:
""".strip()