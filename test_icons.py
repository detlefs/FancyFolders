"""Smoke check for folder icon generation. Run: .venv/bin/python test_icons.py"""

import os
import tempfile

from fancyfolders.constants import FolderStyle, IconGenerationMethod
from fancyfolders.imagetransformations import generate_folder_icon


def generate(style):
    return generate_folder_icon(
        folder_style=style, generation_method=IconGenerationMethod.TEXT,
        text="A", icon_scale=1.0)


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    # Assets must resolve independently of the working directory
    cwd = os.getcwd()
    os.chdir(tempfile.gettempdir())
    try:
        baseline = {style: generate(style) for style in FolderStyle}
        for style, image in baseline.items():
            check(image.size == (style.size(), style.size()), f"wrong size: {style}")

        # Each style must use its own icon box, not a hardcoded one
        original = FolderStyle.icon_box_percentages
        FolderStyle.icon_box_percentages = lambda self: (0.4, 0.4, 0.6, 0.6)
        try:
            for style in FolderStyle:
                check(generate(style).tobytes() != baseline[style].tobytes(),
                      f"icon box ignored: {style}")
        finally:
            FolderStyle.icon_box_percentages = original
    finally:
        os.chdir(cwd)

    print("ok")


if __name__ == "__main__":
    main()
