from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class LlamaModel:
    def __init__(self, model_path: str):
        print("Loading model from", model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            device_map="auto",
            torch_dtype=torch.float32  # lub bfloat16 jeśli masz wsparcie
        )

    def complete(self, prompt: str, max_tokens: int = 256) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=0.5,
            top_p=0.95,
            do_sample=True,
            eos_token_id=self.tokenizer.eos_token_id
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True).replace(prompt, "").strip()
