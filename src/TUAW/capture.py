from __future__ import annotations

from dataclasses import dataclass

from pynput import keyboard, mouse


@dataclass
class Region:
    x1: int
    y1: int
    x2: int
    y2: int

    @property
    def width(self) -> int:
        return abs(self.x2 - self.x1)

    @property
    def height(self) -> int:
        return abs(self.y2 - self.y1)

    @property
    def normalized(self) -> tuple[int, int, int, int]:
        return (
            min(self.x1, self.x2),
            min(self.y1, self.y2),
            max(self.x1, self.x2),
            max(self.y1, self.y2),
        )


def _canonical_key(key: keyboard.Key | keyboard.KeyCode | None) -> str:
    if isinstance(key, keyboard.Key):
        return key.name
    if isinstance(key, keyboard.KeyCode):
        return key.char or str(key.vk)
    return ""


def _parse_hotkey(keys: str) -> list[str]:
    return [k.strip().lower() for k in keys.split("+")]


def select_region(hotkey_str: str = "ctrl+alt") -> Region | None:
    """Block until the user holds hotkey + moves mouse to select a region.

    Hold the hotkey, move the mouse to define a rectangle, release to confirm.
    Returns the selected Region, or None if cancelled (Esc).
    """
    hotkey_parts = _parse_hotkey(hotkey_str)
    held_keys: set[str] = set()

    mouse_start: tuple[int, int] | None = None
    mouse_current: tuple[int, int] | None = None
    selecting = False
    result: Region | None = None

    ml: mouse.Listener | None = None
    kl: keyboard.Listener | None = None

    def hotkey_held() -> bool:
        return all(p in held_keys for p in hotkey_parts)

    def build_region() -> Region | None:
        if mouse_start and mouse_current:
            x1, y1 = mouse_start
            x2, y2 = mouse_current
            r = Region(x1, y1, x2, y2)
            return r if r.width > 5 and r.height > 5 else None
        return None

    def finalize() -> None:
        nonlocal selecting, mouse_start, mouse_current, result
        selecting = False
        result = build_region()
        mouse_start = None
        mouse_current = None
        if ml is not None:
            ml.stop()
        if kl is not None:
            kl.stop()

    def on_key_press(key: keyboard.Key | keyboard.KeyCode | None) -> bool | None:
        nonlocal selecting
        held_keys.add(_canonical_key(key))
        if key == keyboard.Key.esc:
            result = None
            finalize()
            return False
        if hotkey_held() and mouse_start is not None:
            selecting = True
        return None

    def on_key_release(key: keyboard.Key | keyboard.KeyCode | None) -> bool | None:
        nonlocal selecting
        held_keys.discard(_canonical_key(key))
        if not hotkey_held() and selecting:
            finalize()
        return None

    def on_mouse_move(x: int, y: int) -> None:
        nonlocal selecting, mouse_start, mouse_current
        if hotkey_held():
            if not selecting:
                mouse_start = (x, y)
                mouse_current = (x, y)
                selecting = True
            else:
                mouse_current = (x, y)

    ml = mouse.Listener(on_move=on_mouse_move)
    kl = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
    ml.start()
    kl.start()
    ml.join()
    kl.stop()

    return result
