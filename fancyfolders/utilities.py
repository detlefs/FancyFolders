from colorsys import hsv_to_rgb, rgb_to_hsv
from io import BytesIO
import os
import sys
from typing import Optional, cast

import Cocoa
from PIL.Image import Image, Resampling
from PIL.ImageQt import fromqimage
from PySide6.QtCore import QByteArray, Qt
from PySide6.QtGui import QImage, QPainter
from PySide6.QtSvg import QSvgRenderer


#######################
# COLOUR UTILITIES
#######################


def divided_colour(starting_colour: tuple[int, int, int],
                   final_colour: tuple[int, int, int]) -> tuple[int, int, int]:
    """Divides colours? TODO figure out what this is again

    :param starting_colour: Starting colour (r, g, b)
    :param final_colour: Final colour (r, g, b)
    :return: Divided colour (r, g, b)
    """
    colour_channels = zip(starting_colour, final_colour)
    return cast(tuple[int, int, int],
                tuple([clamp(int(((255 * final) / start)), 0, 255)
                       for start, final in colour_channels]))


def rgb_int_to_hsv(rgb_colour: tuple[int, int, int]) -> tuple[float, float, float]:
    """Converts an int based rgb colour to a float hsv

    :param rgb_colour: Colour to convert (r, g, b)
    :return: Converted colour (h, s, v)
    """
    float_colours = [colour / 255 for colour in rgb_colour]
    return rgb_to_hsv(*float_colours)


def hsv_to_rgb_int(hsv_colour: tuple[float, float, float]) -> tuple[int, int, int]:
    """Converts a float based hsv colour to an int rgb

    :param hsv_colour: Colour to convert (h, s, v)
    :return: Converted colour (r, g, b)
    """
    float_colours = hsv_to_rgb(*hsv_colour)
    return cast(tuple[int, int, int],
                tuple([int(colour * 255) for colour in float_colours]))


#######################
# FILESYSTEM UTILITIES
#######################

def get_internal_font_location(font_filename: str) -> str:
    base_pathname = internal_resource_path("assets/fonts")
    return os.path.join(base_pathname, font_filename)


def internal_resource_path(relative_path: str) -> str:
    """Get absolute path to internal app resource, works for dev and for
    the app created through PyInstaller

    :param relative_path: Relative filepath to resource
    :return: Absolute filepath to resource
    """

    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base_path, relative_path)


# Sizes macOS keeps in an icon family. Providing all of them avoids Finder
# having to downscale the single large icon for list and column views
ICON_SIZES = (16, 32, 128, 256, 512, 1024)


def _icon_family_image(pil_image: Image) -> "Cocoa.NSImage":
    """Builds an NSImage containing one representation per macOS icon size

    :param pil_image: PIL Image of the folder icon
    :return: NSImage with one bitmap representation per icon size
    :raises OSError: If the image data cannot be read
    """
    largest = max(ICON_SIZES)
    ns_image = Cocoa.NSImage.alloc().initWithSize_(
        Cocoa.NSMakeSize(largest, largest))

    for size in ICON_SIZES:
        # Need to hand the API PNG data, so render each size to a byte buffer
        buffered = BytesIO()
        pil_image.resize((size, size), Resampling.LANCZOS).save(
            buffered, format="PNG")

        representation = Cocoa.NSBitmapImageRep.imageRepWithData_(
            buffered.getvalue())
        if representation is None:
            raise OSError(
                "Could not read the generated folder icon image data")
        representation.setSize_(Cocoa.NSMakeSize(size, size))
        ns_image.addRepresentation_(representation)

    return ns_image


def set_folder_icon(pil_image: Image, path: str) -> None:
    """Sets the icon of the file/directory at the specified path to the
    provided image using the native macOS API, interfaced through PyObjC

    :param pil_image: PIL Image of the folder icon to set
    :param path: Absolute path to the folder
    :raises OSError: If the image data cannot be read or macOS refuses to
        write the icon (missing permissions, read-only volume, ...)
    """
    ns_image = _icon_family_image(pil_image)

    workspace = Cocoa.NSWorkspace.sharedWorkspace()
    if not workspace.setIcon_forFile_options_(ns_image, path, 0):
        raise OSError("macOS refused to set the icon of '{}'".format(path))

    # Finder normally picks the new icon up through the filesystem change,
    # but already open windows and the icon cache can keep showing the old one
    workspace.noteFileSystemChanged_(path)


def generate_unique_folder_filename(directory: str) -> str:
    """Generates a unique folder name in the 'untitled folder' format, in the
    specified directory. I.e. if the folder already exists, increment the number
    and try again

    :param directory: Directory to search for folders in
    :return: Unique folder name
    """
    index = 1
    while True:
        new_folder_name = "untitled folder" + \
            ("" if index == 1 else " {}".format(index))
        path = os.path.join(directory, new_folder_name)

        if not os.path.exists(path):
            os.mkdir(path)
            break
        index += 1
    return path

#######################
# SF SYMBOL UTILITIES
#######################

# SF Symbols glyphs live in the plane 16 private use area
SYMBOL_CHARACTER_RANGE = (0x100000, 0x10FFFD)

# Symbols are drawn at the size of the largest folder icon
SYMBOL_RENDER_SIZE = 1024


def is_symbol_character(text: str) -> bool:
    """Whether the text is a single SF Symbols character

    :param text: Text to check
    :return: Is it a symbol character?
    """
    if len(text) != 1:
        return False
    low, high = SYMBOL_CHARACTER_RANGE
    return low <= ord(text) <= high


def dragged_symbol_svg() -> Optional[bytes]:
    """Reads the SVG that macOS puts on the drag pasteboard for a dragged SF
    Symbol. Qt filters that flavour out of the drop event, so it has to be
    read through the native API instead

    :return: SVG data, or None if the drag carried no SVG
    """
    pasteboard = Cocoa.NSPasteboard.pasteboardWithName_(
        Cocoa.NSPasteboardNameDrag)
    data = pasteboard.dataForType_("public.svg-image")
    if data is None:
        return None
    return bytes(data)


def render_svg(svg: bytes, size: int = SYMBOL_RENDER_SIZE) -> Optional[Image]:
    """Rasterizes SVG data, cropped to the drawing it contains

    :param svg: SVG data
    :param size: Size of the longest side in pixels
    :return: PIL Image (RGBA), or None if the data is not valid SVG
    """
    renderer = QSvgRenderer(QByteArray(svg))
    if not renderer.isValid():
        return None

    default_size = renderer.defaultSize()
    scale = size / max(default_size.width(), default_size.height())
    image = QImage(round(default_size.width() * scale),
                   round(default_size.height() * scale),
                   QImage.Format_RGBA8888)
    image.fill(Qt.transparent)

    painter = QPainter(image)
    renderer.render(painter)
    painter.end()

    drawing = fromqimage(image).convert("RGBA")
    ink_box = drawing.getbbox()
    if ink_box is None:
        return None
    return drawing.crop(ink_box)


def black_silhouette(image: Image) -> Image:
    """Recolours an image to black, keeping its shape. A monochrome symbol can
    be drawn in any colour, white included, but engraving it into the folder
    uses the brightness of the image, so only its silhouette may survive

    :param image: PIL Image (RGBA)
    :return: PIL Image (RGBA), black on transparent
    """
    silhouette = image.convert("RGBA")
    shape = silhouette.getchannel("A")
    silhouette.paste((0, 0, 0, 255), (0, 0) + silhouette.size)
    silhouette.putalpha(shape)
    return silhouette


def is_greyscale(image: Image) -> bool:
    """Whether every visible pixel of the image is a shade of grey

    :param image: PIL Image (RGBA)
    :return: Is the image free of colour?
    """
    return all(red == green == blue
               for red, green, blue, alpha in image.convert(
                   "RGBA").get_flattened_data() if alpha > 0)


#######################
# MATH UTILITIES
#######################


def clamp(n, min_value, max_value):
    return min(max(n, min_value), max_value)


def interpolate_int_to_float_with_midpoint(
        value: int, pre_min: int, pre_max: int, post_min: float,
        post_mid: float, post_max: float) -> float:

    pre_mid = int((pre_max - pre_min)/2) + 1

    if value == pre_mid:
        return post_mid
    elif value < pre_mid:
        return interpolate(value, pre_min, pre_mid, post_min, post_mid)
    elif value > pre_mid:
        return interpolate(value, pre_mid, pre_max, post_mid, post_max)


def interpolate(value, pre_min, pre_max, post_min, post_max):
    return ((post_max - post_min) * value + pre_max * post_min - pre_min * post_max) / (pre_max - pre_min)
