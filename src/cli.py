import argparse
import sys

from src.model_manager import ModelManager
from src.gemini_model_manager import GeminiModelManager
from src.csharp_parser import CSharpParser
from src.documentation_generator import DocumentationGenerator
from src.documentation_inserter import DocumentationInserter

def main():
    parser = argparse.ArgumentParser(description="XML documentation generator for .NET C# files.")
    parser.add_argument("file_path", type=str, help="Path to the .cs file")
    parser.add_argument("--gemini", action="store_true", help="Use Gemini API instead of the local model")
    args = parser.parse_args()

    file_path = args.file_path
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code_content = f.read()
    except FileNotFoundError:
        print(f"ERROR: File not found: {file_path}")
        sys.exit(1)

    if args.gemini:
        model_manager = GeminiModelManager()
        updated_code = gemini_document_entire_code(model_manager, code_content)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_code)
        print(f"[OK] Gemini documentation generated in file: {file_path}")
    else:
        code_lines = code_content.splitlines(True)
        parser_obj = CSharpParser()
        classes = parser_obj.parse_file(code_lines)
        if not classes:
            print("INFO: No classes found in the file.")
            sys.exit(0)

        local_model = ModelManager()
        local_model.load_model()
        doc_gen = DocumentationGenerator(local_model)
        doc_map = doc_gen.generate_for_classes(classes)

        inserter = DocumentationInserter()
        updated_lines = inserter.insert_documentation(code_lines, classes, doc_map)
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(updated_lines)
        print(f"[OK] Documentation (local mode) has been generated in file: {file_path}")

def gemini_document_entire_code(model_manager: GeminiModelManager, code: str) -> str:
    prompt = (
        "You are an expert C# developer. "
        "Rewrite the following code by adding XML documentation comments (<summary>, <param>, <returns>, etc.) "
        "for every class, method, enum, struct, interface, and field. "
        "Keep the original code structure intact. Return only the updated code.\n\n"
        f"{code}\n"
    )
    result = model_manager.generate_text(prompt)
    return result

if __name__ == "__main__":
    main()