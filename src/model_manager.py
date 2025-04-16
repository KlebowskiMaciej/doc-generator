import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from src.config import Config

class ModelManager:
    def __init__(self):
        self._tokenizer = None
        self._model = None

    def load_model(self):
        if self._tokenizer is None or self._model is None:
            print(f"[ModelManager] Loading model: {Config.MODEL_NAME}")
            self._tokenizer = AutoTokenizer.from_pretrained(Config.MODEL_NAME)
            self._model = AutoModelForSeq2SeqLM.from_pretrained(Config.MODEL_NAME)
            print("[ModelManager] Model loaded successfully.")

    def generate_text(self, prompt: str) -> str:
        if self._tokenizer is None or self._model is None:
            raise ValueError("Model not loaded. Call load_model() first.")

        input_ids = self._tokenizer.encode(prompt, return_tensors="pt")

        with torch.no_grad():
            outputs = self._model.generate(
                input_ids,
                max_length=Config.MAX_LENGTH,
                num_beams=Config.NUM_BEAMS,
                early_stopping=Config.EARLY_STOPPING
            )

        text = self._tokenizer.decode(outputs[0], skip_special_tokens=True)
        return text.strip()