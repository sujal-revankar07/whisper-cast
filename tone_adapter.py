'''
import google.generativeai as genai
from .utils import load_config, logger
import os

class ToneAdapter:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError("GEMINI_API_KEY not set")
        genai.configure(api_key=api_key)

        cfg     = load_config()
        self.tones   = cfg["tone_adaptation"]["available_tones"]
        self.prompts = cfg["prompts"]
        self.temp    = cfg["tone_adaptation"]["temperature"]
        self.model   = genai.GenerativeModel("gemini-1.5-flash")
        self.current = self.tones[0]

    def cycle(self) -> str:
        idx = (self.tones.index(self.current) + 1) % len(self.tones)
        self.current = self.tones[idx]
        logger.info("Tone switched → %s", self.current)
        return self.current

    def adapt(self, text: str) -> str:
        prompt = self.prompts[self.current].format(text=text)
        response = self.model.generate_content(
            prompt,
            generation_config=dict(temperature=self.temp, max_output_tokens=256),
        )
        return response.text.strip()'''
