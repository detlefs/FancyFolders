"""Smoke check for folder icon generation. Run: .venv/bin/python test_icons.py"""

import os
import tempfile

from PIL import Image

from fancyfolders.constants import FolderStyle, IconGenerationMethod
from fancyfolders.imagetransformations import generate_folder_icon
from fancyfolders.utilities import ICON_SIZES, _icon_family_image, set_folder_icon


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
        # Original colours are kept verbatim when requested, engraved otherwise
        red = Image.new("RGBA", (200, 200), (255, 0, 0, 255))
        kept = generate_folder_icon(
            folder_style=FolderStyle.tahoe,
            generation_method=IconGenerationMethod.IMAGE, image=red,
            preserve_image_colours=True)
        centre = (512, 538)  # inside the icon bounding box
        check(kept.getpixel(centre) == (255, 0, 0, 255), "original colours not kept")

        engraved = generate_folder_icon(
            folder_style=FolderStyle.tahoe,
            generation_method=IconGenerationMethod.IMAGE, image=red)
        check(engraved.getpixel(centre) != (255, 0, 0, 255),
              "engraved icon should not contain the original colour")
    finally:
        os.chdir(cwd)

    # Writing an icon must succeed on a real folder and fail loudly otherwise
    folder = tempfile.mkdtemp()
    set_folder_icon(red, folder)
    check("Icon\r" in os.listdir(folder), "custom icon file was not written")
    sizes = [rep.pixelsWide() for rep in _icon_family_image(red).representations()]
    check(sorted(sizes) == sorted(ICON_SIZES), f"missing icon sizes: {sizes}")
    try:
        set_folder_icon(red, os.path.join(folder, "does not exist"))
        check(False, "setting the icon of a missing folder should raise")
    except OSError:
        pass

    print("ok")


if __name__ == "__main__":
    main()
