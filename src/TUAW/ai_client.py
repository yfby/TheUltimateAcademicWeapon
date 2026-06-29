from __future__ import annotations

from google import genai
from google.genai import types
from PIL import Image

SYSTEM_INSTRUCTION = (
    "You are an expert academic tutor. "
    "Given an image of a problem (math, science, CS, etc.), "
    "solve it step by step. Show all reasoning clearly. "
    "If the image is not a problem, describe what you see and help however you can."
)


class AIClient:
    def __init__(self, api_key: str, model: str = "gemini-3.5-flash") -> None:
        self.model = model
        self.client = genai.Client(api_key=api_key)

    def solve(self, image: Image.Image, prompt: str = "Solve this.") -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=[image, prompt],
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
            ),
        )
        return response.text
