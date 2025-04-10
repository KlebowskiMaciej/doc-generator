from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import re

class CSDocGenerator:
    def __init__(self, model_name="bigcode/starcoderbase"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float32)

    def generate_doc(self, code_snippet):
        prompt = f"Generate XML documentation (<summary>, <param>) for the following C# method or class:\n\n{code_snippet}\n\nXML Documentation:\n"
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=8192)
        output_ids = self.model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=250,
            do_sample=False,
            temperature=0.2
        )
        generated_text = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        documentation = generated_text.split("XML Documentation:")[1].strip()
        return documentation

    def insert_docs_to_code(self, code_content):
        def replacer(match):
            code_snippet = match.group(0)
            doc_comment = self.generate_doc(code_snippet)
            return f"{doc_comment}\n{code_snippet}"

        pattern = r"(public|private|protected|internal).*\\(.*\\)[\\s\\S]*?\\{"
        documented_code = re.sub(pattern, replacer, code_content)
        return documented_code
