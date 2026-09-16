from google import genai

from backend.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
)


class LLMService:
    def __init__(self):
        

        if not GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    def generate(self, prompt: str) -> str:
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        response = self.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        return response.text