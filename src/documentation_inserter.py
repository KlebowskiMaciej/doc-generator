class DocumentationInserter:

    def insert_documentation(self, code_lines, classes, doc_map):
        updated_lines = list(code_lines)

        for cls in reversed(classes):
            class_name = cls['name']
            class_line_idx = cls['class_line_index']
            class_doc = doc_map[class_name]['summary']

            class_comment = self._xml_for_class(class_doc)
            updated_lines.insert(class_line_idx, class_comment)

            for method_info in reversed(cls['methods']):
                method_line_idx = method_info['line_index']
                mname = method_info['name']

                mdoc = doc_map[class_name]['methods'][mname]
                method_summary = mdoc['summary']
                param_docs = mdoc['params']
                returns_doc = mdoc['returns']

                method_comment = self._xml_for_method(method_summary, param_docs, returns_doc)
                updated_lines.insert(method_line_idx, method_comment)

        return updated_lines

    def _xml_for_class(self, summary: str) -> str:
        lines = []
        lines.append("/// <summary>")
        lines.append(f"/// {summary}")
        lines.append("/// </summary>\n")
        return "\n".join(lines)

    def _xml_for_method(self, summary: str, param_docs: dict, returns_doc: str or None) -> str:
        lines = []
        lines.append("/// <summary>")
        lines.append(f"/// {summary}")
        lines.append("/// </summary>")
        for pname, pdesc in param_docs.items():
            lines.append(f"/// <param name=\"{pname}\">{pdesc}</param>")
        if returns_doc:
            lines.append(f"/// <returns>{returns_doc}</returns>")
        lines.append("")  # pusta linia na końcu

        return "\n".join(lines) + "\n"