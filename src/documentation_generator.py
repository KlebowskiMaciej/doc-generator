import re

def cleanup_repetitions(text: str) -> str:
    text = re.sub(r'\b(\w+)( \1){2,}\b', r'\1', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()

class DocumentationGenerator:
    def __init__(self, model_manager):
        self.model_manager = model_manager

    def generate_for_classes(self, classes):
        doc_map = {}
        for cls in classes:
            class_name = cls['name']
            class_summary = self._generate_class_summary(class_name)
            methods_map = {}

            for method_info in cls['methods']:
                method_name = method_info['name']
                return_type = method_info['return_type']
                params = method_info['params']

                method_summary = self._generate_method_summary(method_name, return_type, len(params))
                param_docs = {}
                for (ptype, pname) in params:
                    param_docs[pname] = self._generate_param_description(pname, ptype)

                returns_doc = None
                if return_type.lower() != "void":
                    returns_doc = self._generate_return_description(method_name, return_type)

                methods_map[method_name] = {
                    'summary': method_summary,
                    'params': param_docs,
                    'returns': returns_doc
                }

            doc_map[class_name] = {
                'summary': class_summary,
                'methods': methods_map
            }

        return doc_map

    def _generate_class_summary(self, class_name: str) -> str:
        example_class_doc = (
            "EXAMPLE:\n"
            "Class 'OrderService': 'Handles order creation and tracking in an e-commerce system.'\n"
        )
        prompt = (
            f"{example_class_doc}\n"
            f"Write a concise summary for a C# class named '{class_name}'. "
            "Avoid repetitive filler like 'this is a class in C#'. "
            "Focus on possible functionality or purpose. "
            "Output only a short plain text summary."
        )
        raw_output = self.model_manager.generate_text(prompt)
        return cleanup_repetitions(raw_output)

    def _generate_method_summary(self, method_name: str, return_type: str, param_count: int) -> str:
        example_method_doc = (
            "EXAMPLE:\n"
            "Method 'CalculateTax' returns 'decimal', has 2 params (income, rate): 'Computes the tax on a given income.'\n"
        )
        prompt = (
            f"{example_method_doc}\n"
            f"Now summarize a C# method named '{method_name}' that returns '{return_type}' "
            f"and has {param_count} parameter(s). Keep it brief and human-readable. "
            "Avoid stating 'in C#' or repeating code details. "
            "Output only a short plain text summary."
        )
        raw_output = self.model_manager.generate_text(prompt)
        return cleanup_repetitions(raw_output)

    def _generate_param_description(self, param_name: str, param_type: str) -> str:
        # Krótki "few-shot" przykład
        example_param_doc = (
            "EXAMPLE:\n"
            "Parameter 'rate': 'Specifies the tax rate to apply.'\n"
        )
        prompt = (
            f"{example_param_doc}\n"
            f"Provide a concise description for a parameter '{param_name}' of type '{param_type}'. "
            "Highlight its role or usage. "
            "Avoid filler words. Output only the description text."
        )
        raw_output = self.model_manager.generate_text(prompt)
        return cleanup_repetitions(raw_output)

    def _generate_return_description(self, method_name: str, return_type: str) -> str:
        example_return_doc = (
            "EXAMPLE:\n"
            "Method 'CalculateTax' (return type: decimal): 'The calculated tax amount.'\n"
        )
        prompt = (
            f"{example_return_doc}\n"
            f"For method '{method_name}', returning '{return_type}', write a short explanation "
            "of what is returned. No filler. Output only the explanation text."
        )
        raw_output = self.model_manager.generate_text(prompt)
        return cleanup_repetitions(raw_output)