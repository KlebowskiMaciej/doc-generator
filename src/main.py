from xml_parser import XMLDocUpdater
from model_engine import LlamaModel
from prompts import PromptBuilder
import os
import sys
import shutil
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)
logger = logging.getLogger("xml-doc-filler")

def get_default_model_id() -> str:
    return "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

def main():
    if len(sys.argv) < 2:
        logger.error("Usage: python main.py <path_to_xml>")
        sys.exit(1)

    input_path = sys.argv[1]
    if not os.path.isfile(input_path):
        logger.error(f"File does not exist: {input_path}")
        sys.exit(1)

    logger.info(f"Processing input XML: {input_path}")

    model_path = get_default_model_id()
    logger.info(f"Using model: {model_path}")

    model = LlamaModel(model_path=model_path, logger=logger)
    prompt_builder = PromptBuilder()
    updater = XMLDocUpdater(model=model, prompt_builder=prompt_builder, logger=logger)

    tmp_output_path = input_path + ".tmp"
    logger.info("Generating updated XML file...")
    updater.process_file(input_path, tmp_output_path)

    shutil.move(tmp_output_path, input_path)
    logger.info(f"Successfully updated file: {input_path}")

if __name__ == "__main__":
    main()