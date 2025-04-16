import re

class CSharpParser:

    CLASS_PATTERN = re.compile(r'\bclass\s+(\w+)')
    METHOD_PATTERN = re.compile(
        r'(public|private|protected|internal|static|\s)*\s*([\w<>\[\]]+)\s+(\w+)\s*\(([^)]*)\)'
    )

    def parse_file(self, code_lines):
        classes = []
        current_class = None

        for i, line in enumerate(code_lines):
            class_match = self.CLASS_PATTERN.search(line)
            if class_match:
                class_name = class_match.group(1)
                current_class = {
                    'type': 'class',
                    'name': class_name,
                    'class_line_index': i,
                    'methods': []
                }
                classes.append(current_class)
                continue
            if current_class:
                method_match = self.METHOD_PATTERN.search(line)
                if method_match:
                    return_type = method_match.group(2)
                    method_name = method_match.group(3)
                    params_string = method_match.group(4).strip()

                    params_list = []
                    if params_string:
                        for param in params_string.split(','):
                            param = param.strip()
                            splitted = param.split()
                            if len(splitted) == 2:
                                ptype, pname = splitted
                            else:
                                ptype = splitted[0]
                                pname = " ".join(splitted[1:])
                            params_list.append((ptype, pname))

                    current_class['methods'].append({
                        'name': method_name,
                        'return_type': return_type,
                        'params': params_list,
                        'line_index': i
                    })

        return classes