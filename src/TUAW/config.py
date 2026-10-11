from __future__ import annotations

import dataclasses
import json
from dataclasses import dataclass, field
from pathlib import Path

_DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "config.json"


@dataclass
class ClipboardIndicators:
    initialized: str = ""
    analysis: str = ""
    exit: str = ""


@dataclass
class AIConfig:
    model: str = "gemini-3.8-flash"
    temperature: float = 0.2
    default_task: str = "auto"
    default_language: str | None = None


@dataclass
class HotkeyConfig:
    keys: str = "ctrl+alt"


@dataclass
class PromptConfig:
    system_instruction: str = ""
    prompt: str = ""


@dataclass
class PromptsConfig:
    auto: PromptConfig = field(default_factory=PromptConfig)
    qa: PromptConfig = field(default_factory=PromptConfig)
    coding: PromptConfig = field(default_factory=PromptConfig)
    math: PromptConfig = field(default_factory=PromptConfig)


@dataclass
class Config:
    clipboard_indicators: ClipboardIndicators = field(
        default_factory=ClipboardIndicators
    )
    ai: AIConfig = field(default_factory=AIConfig)
    hotkey: HotkeyConfig = field(default_factory=HotkeyConfig)
    prompts: PromptsConfig = field(default_factory=PromptsConfig)


def _build(cls: type, raw: dict) -> object:
    fields = {f.name for f in dataclasses.fields(cls)}
    return cls(**{k: v for k, v in raw.items() if k in fields})


def _build_prompt_config(data: dict | None) -> PromptConfig:
    if not data:
        return PromptConfig()
    return _build(PromptConfig, data)


def _build_prompts_config(raw: dict) -> PromptsConfig:
    return PromptsConfig(
        auto=_build_prompt_config(raw.get("auto")),
        qa=_build_prompt_config(raw.get("qa")),
        coding=_build_prompt_config(raw.get("coding")),
        math=_build_prompt_config(raw.get("math")),
    )


def _validate(config: Config) -> None:
    if not 0.0 <= config.ai.temperature <= 2.0:
        raise ValueError(f"temperature must be 0.0-2.0, got {config.ai.temperature}")

    valid_tasks = {"auto", "qa", "coding", "math"}
    if config.ai.default_task not in valid_tasks:
        raise ValueError(
            f"default_task must be one of {valid_tasks}, got {config.ai.default_task!r}"
        )

    if not config.hotkey.keys.strip():
        raise ValueError("hotkey.keys must not be empty")


def load_config(path: str | Path | None = None) -> Config:
    config_path = Path(path) if path else _DEFAULT_CONFIG_PATH

    raw: dict = {}
    if config_path.is_file():
        with open(config_path) as f:
            raw = json.load(f)

    config = Config(
        clipboard_indicators=_build(
            ClipboardIndicators, raw.get("clipboard_indicators", {})
        ),
        ai=_build(AIConfig, raw.get("ai", {})),
        hotkey=_build(HotkeyConfig, raw.get("hotkey", {})),
        prompts=_build_prompts_config(raw.get("prompts", {})),
    )

    _validate(config)
    return config
