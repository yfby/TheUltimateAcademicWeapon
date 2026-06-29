from __future__ import annotations

from typing import Callable

from pynput import keyboard

_ON_ACTIVATE = Callable[[], None]


def start_listener(on_activate: _ON_ACTIVATE) -> keyboard.Listener:
    hotkey = keyboard.HotKey(
        keyboard.HotKey.parse("<ctrl>+<alt>"),
        on_activate,
    )

    def on_press(key: keyboard.Key | keyboard.KeyCode | None) -> None:
        hotkey.press(listener.canonical(key))

    def on_release(key: keyboard.Key | keyboard.KeyCode | None) -> None:
        hotkey.release(listener.canonical(key))

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.daemon = True
    listener.start()
    return listener
