from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import platform

class LlamaModel:
    def __init__(self, model_path: str, logger):
        self.logger = logger
        self.logger.info(f"Loading model from {model_path}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)

        is_mac_m1 = platform.system() == "Darwin" and torch.backends.mps.is_available()

        if is_mac_m1:
            device = torch.device("mps")
            self.logger.info("Using Apple M1 Metal (MPS) backend")
        else:
            device = torch.device("cpu")
            self.logger.info("Using CPU backend")

        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float32
        ).to(device)

        self.device = device

    def complete(self, prompt: str, max_tokens: int = 256) -> str:
        messages = [{"role": "user", "content": prompt}]
        prompt_text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

        self.logger.info(f"Generating description for prompt:\n{prompt_text}")
        inputs = self.tokenizer(prompt_text, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=0.5,
            top_p=0.95,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id,
            eos_token_id=self.tokenizer.eos_token_id
        )
        result = self.tokenizer.decode(outputs[0], skip_special_tokens=True).replace(prompt_text, "").strip()
        self.logger.info(f"Generated raw model output: {result}")

        cleaned = self.clean_response(result)
        self.logger.info(f"Cleaned description: {cleaned}")
        return cleaned

    def clean_response(self, text: str, max_words: int = 12) -> str:
        import re
        text = re.sub(r"<\|user\|>.*", "", text, flags=re.DOTALL)
        text = re.sub(r"(?i)\b(description|represents|parameter|field|method|class)\b[:\-\s]*", "", text).strip()
        return " ".join(text.split()[:max_words])