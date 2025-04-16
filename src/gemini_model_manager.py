import os
import sys
import logging
import getpass
import google.generativeai as genai
from dotenv import load_dotenv

class GeminiModelManager:
    def __init__(self, gemini_model="gemini-2.5-pro-exp-03-25", max_tokens=900000):
        self.logger = logging.getLogger("GeminiModelManager")
        self.gemini_model = gemini_model
        self.max_tokens = max_tokens
        self.model = None
        self.api_key = self._ensure_api_key()
        self._configure_genai()

    def _ensure_api_key(self) -> str:
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("No GEMINI_API_KEY found in environment.")
            api_key = getpass.getpass("Please enter your Gemini API Key: ").strip()
            global_env_path = os.path.join(os.path.expanduser("~"), ".gemini_config.env")
            try:
                with open(global_env_path, "w", encoding="utf-8") as f:
                    f.write(f"GEMINI_API_KEY={api_key}\n")
                self.logger.info(f"Gemini API key stored in {global_env_path}")
            except Exception as e:
                self.logger.error(f"Failed to store Gemini API key: {e}", exc_info=True)
        return api_key

    def _configure_genai(self):
        try:
            genai.configure(api_key=self.api_key)
            self.logger.info("Successfully configured Google Generative AI.")
        except Exception as e:
            self.logger.error(f"Error configuring Google Generative AI: {e}", exc_info=True)

    def _initialize_model(self):
        if self.model is None:
            try:
                self.model = genai.GenerativeModel(self.gemini_model)
                self.logger.info(f"Gemini model '{self.gemini_model}' initialized.")
            except Exception as e:
                self.logger.error(f"Failed to initialize Gemini model: {e}", exc_info=True)
                raise RuntimeError("Error initializing Gemini model.") from e

    def generate_text(self, prompt: str) -> str:
        self._initialize_model()
        self.logger.info("Sending request to Gemini with temperature=0.3.")
        try:
            response = self.model.generate_content(
                prompt,
                temperature=0.3
            )
        except Exception as e:
            self.logger.error(f"Error communicating with Gemini API: {e}", exc_info=True)
            return f"ERROR: Communication with Gemini API failed: {e}"

        if not getattr(response, 'parts', None):
            if getattr(response, 'prompt_feedback', None) and getattr(response.prompt_feedback, 'block_reason', None):
                reason = response.prompt_feedback.block_reason.name
                self.logger.error(f"Gemini blocked the response. Reason: {reason}")
                return f"ERROR: Gemini blocked the response (Reason: {reason})."
            else:
                self.logger.warning("Gemini returned an empty response (no 'parts').")
                return "INFO: Gemini returned an empty response."

        full_text = "".join(part.text for part in response.parts)
        self.logger.info("Gemini response received successfully.")
        return full_text