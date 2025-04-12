from xml_parser import XMLDocUpdater
from model_engine import LlamaModel
from prompts import PromptBuilder
import os
import sys
import shutil
from pathlib import Path


def resolve_model_path():
    model_dir = os.getenv("MODEL_DIR", "models/Mistral-7B-Instruct-v0.3")
    if not os.path.isdir(model_dir):
        raise FileNotFoundError(
            f"Model not found in expected directory: {model_dir}\n"
            f"To download, use:\n"
            f"  huggingface-cli login\n"
            f"  huggingface-cli download mistralai/Mistral-7B-Instruct-v0.3 --local-dir {model_dir} --local-dir-use-symlinks False"
        )
    return model_dir


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_xml>")
        sys.exit(1)

    input_path = sys.argv[1]
    if not os.path.isfile(input_path):
        print(f"File does not exist: {input_path}")
        sys.exit(1)

    model_path = resolve_model_path()

    # Inicjalizacja
    model = LlamaModel(model_path=model_path)
    prompt_builder = PromptBuilder()
    updater = XMLDocUpdater(model=model, prompt_builder=prompt_builder)

    # Przetwarzanie
    tmp_output_path = input_path + ".tmp"
    updater.process_file(input_path, tmp_output_path)

    # Nadpisz oryginalny plik
    shutil.move(tmp_output_path, input_path)
    print(f"Updated file: {input_path}")


if __name__ == "__main__":
    main()