"""Smoke check for folder icon generation. Run: .venv/bin/python test_icons.py"""

import os
import tempfile

from PIL import Image

from fancyfolders.constants import FolderStyle, IconGenerationMethod
from fancyfolders.imagetransformations import generate_folder_icon, _render_colour_emoji
from fancyfolders.utilities import (
    ICON_SIZES, _icon_family_image, black_silhouette, is_greyscale,
    is_symbol_character, render_svg, set_folder_icon)


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
        # Emoji keep their own colours, plain text is still engraved
        check(_render_colour_emoji("A") is None, "a letter is not an emoji")
        check(_render_colour_emoji("\U0001f419") is not None, "emoji not rendered")
        emoji = generate_folder_icon(
            folder_style=FolderStyle.tahoe,
            generation_method=IconGenerationMethod.TEXT, text="\U0001f419")
        colours = set(emoji.convert("RGB").crop((300, 400, 724, 700)).get_flattened_data())
        check(len(colours) > 1000, f"emoji drawn without its colours: {len(colours)}")
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

    # Dropped SF Symbols are rendered from SVG, colour decides how they are used
    check(is_symbol_character("\U0010255d"), "symbol character not recognized")
    check(not is_symbol_character("A"), "a letter is not a symbol character")
    check(not is_symbol_character("\U0010255d\U0010255d"), "only single characters")

    svg = b'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 10">
        <rect width="20" height="10" opacity="0"/><rect x="5" y="2" width="10" height="6" %s/>
        </svg>'''
    mono = render_svg(svg % b'fill="black"')
    check(mono.size == (512, 308), f"wrong render size or crop: {mono.size}")
    check(is_greyscale(mono), "black symbol reported as coloured")
    check(not is_greyscale(render_svg(svg % b'fill="#007aff"')),
          "blue symbol reported as greyscale")
    check(render_svg(b"not an svg") is None, "invalid svg should not render")

    # Monochrome symbols come in any colour, engraving needs their silhouette
    white = render_svg(svg % b'fill="white"')
    silhouette = black_silhouette(white)
    visible = [c for c in silhouette.get_flattened_data() if c[3] > 0]
    check(len(visible) == len([c for c in white.get_flattened_data() if c[3] > 0]),
          "silhouette lost the shape")
    check(all(c[:3] == (0, 0, 0) for c in visible), "silhouette is not black")

    print("ok")


if __name__ == "__main__":
    main()
