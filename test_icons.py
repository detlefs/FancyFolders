"""Smoke check for folder icon generation. Run: .venv/bin/python test_icons.py"""

import os
import tempfile

from fancyfolders.constants import FolderStyle, IconGenerationMethod
from fancyfolders.imagetransformations import generate_folder_icon


def generate(style):
    return generate_folder_icon(
        folder_style=style, generation_method=IconGenerationMethod.TEXT,
        text="A", icon_scale=1.0)


def main():
    # Assets must resolve independently of the working directory
    os.chdir(tempfile.gettempdir())

    baseline = {style: generate(style) for style in FolderStyle}
    for style, image in baseline.items():
        assert image.size == (style.size(), style.size()), style

    # Each style must use its own icon box, not a hardcoded one
    original = FolderStyle.icon_box_percentages
    FolderStyle.icon_box_percentages = lambda self: (0.4, 0.4, 0.6, 0.6)
    try:
        for style in FolderStyle:
            assert generate(style).tobytes() != baseline[style].tobytes(), style
    finally:
        FolderStyle.icon_box_percentages = original

    print("ok")


if __name__ == "__main__":
    main()
