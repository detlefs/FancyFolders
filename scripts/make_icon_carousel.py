#!/usr/bin/env python3
"""Build the README carousel: a row of folder icons that swaps every 1.25s.

Mirrors readme_assets/white_background_smaller_carousel.gif (720x120, six
tiles) but keeps the alpha channel, so it is written as an APNG.
"""
import sys
from math import gcd
from pathlib import Path

from PIL import Image

TILE = 120
COLS = 6
FRAME_MS = 1250
SOURCE_SIZE = 1024  # which per-size PNG to downscale from


def icon_paths(src: Path) -> list[Path]:
    found = []
    for folder in sorted(p for p in src.iterdir() if p.is_dir()):
        icon = folder / f"{folder.name}_{SOURCE_SIZE}.png"
        if not icon.exists():
            sys.exit(f"missing {icon}")
        found.append(icon)
    if len(found) < COLS:
        sys.exit(f"need at least {COLS} icons, found {len(found)}")
    return found


def build(src: Path, out: Path) -> None:
    icons = [Image.open(p).convert("RGBA").resize((TILE, TILE), Image.LANCZOS)
             for p in icon_paths(src)]
    n = len(icons)
    # Shifting by COLS each frame, the row repeats after this many frames.
    n_frames = n // gcd(n, COLS)

    frames = []
    for f in range(n_frames):
        canvas = Image.new("RGBA", (TILE * COLS, TILE), (0, 0, 0, 0))
        for c in range(COLS):
            canvas.alpha_composite(icons[(f * COLS + c) % n], (c * TILE, 0))
        frames.append(canvas)

    out.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(out, save_all=True, append_images=frames[1:],
                   duration=FRAME_MS, loop=0, disposal=1, default_image=False)
    print(f"{out}: {len(frames)} frames of {n} icons, "
          f"{len(frames) * FRAME_MS / 1000:.1f}s, {out.stat().st_size / 1024:.0f} KiB")


if __name__ == "__main__":
    build(Path(sys.argv[1] if len(sys.argv) > 1 else "readme_assets/_new"),
          Path(sys.argv[2] if len(sys.argv) > 2 else "readme_assets/carousel.png"))
