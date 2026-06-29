from __future__ import annotations

import mss
from PIL import Image

from .capture import Region


def capture_region(region: Region) -> Image.Image:
    x1, y1, x2, y2 = region.normalized
    with mss.MSS() as sct:
        monitor = {"left": x1, "top": y1, "width": x2 - x1, "height": y2 - y1}
        shot = sct.grab(monitor)
        return Image.frombuffer("RGB", shot.size, shot.bgra, "raw", "BGRX")


if __name__ == "__main__":
    from .capture import select_region

    region = select_region()
    if region:
        img = capture_region(region.normalized)
        img.save("screenshot.png")
        print(f"Saved screenshot ({region.width}x{region.height})")
