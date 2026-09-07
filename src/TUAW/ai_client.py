from __future__ import annotations

from config import Config
from google import genai
from google.genai import types
from PIL import Image


class TaskType:
    AUTO = "auto"
    QA = "qa"
    CODING = "coding"
    MATH = "math"


_TASK_MAP: dict[str, str] = {
    t: t for t in [TaskType.AUTO, TaskType.QA, TaskType.CODING, TaskType.MATH]
}


class AIClient:
    def __init__(self, api_key: str, config: Config | None = None) -> None:
        config = config or Config()
        self.model = config.ai.model
        self._temperature = config.ai.temperature
        self._default_task = _TASK_MAP.get(config.ai.default_task, TaskType.AUTO)
        self._default_language = config.ai.default_language
        self._prompts = config.prompts
        self.client = genai.Client(api_key=api_key)

    def solve(
        self,
        image: Image.Image,
        task: str | None = None,
        extra_context: str | None = None,
        language: str | None = None,
    ) -> str:
        task = task or self._default_task
        language = language or self._default_language

        prompt_cfg = getattr(self._prompts, task)
        system_instruction = prompt_cfg.system_instruction
        prompt = prompt_cfg.prompt

        if language and task in (TaskType.CODING, TaskType.AUTO):
            prompt += f" The language is {language}."

        contents: list = [image]
        if extra_context:
            contents.append(f"Additional context:\n{extra_context}")
        contents.append(prompt)

        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=self._temperature,
            ),
        )
        return response.text.strip()
