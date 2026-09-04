from enum import Enum

######################
# CONSTANTS
######################

# VERSION

VERSION = "2.0"

# UI

# Accent colours of the numbered step badges (macOS system colours)
PANEL1_COLOUR = (0, 122, 255)    # systemBlue
PANEL2_COLOUR = (48, 176, 199)   # systemTeal
PANEL3_COLOUR = (52, 199, 89)    # systemGreen

ICON_SCALE_SLIDER_MAX = 31
MAXIMUM_ICON_SCALE_VALUE = 2.0
MINIMUM_ICON_SCALE_VALUE = 0.1

# ICON GENERATION

FOLDER_SHADOW_INCREASE_FACTOR = 1.7
INNER_SHADOW_COLOUR_SCALING_FACTOR = 0.9

INNER_SHADOW_BLUR = 3
INNER_SHADOW_Y_OFFSET = 0.00293  # Percentage of height
OUTER_HIGHLIGHT_BLUR = 6
OUTER_HIGHLIGHT_Y_OFFSET = 0.00782  # Percentage of height

ICON_BOX_SCALING_FACTOR = 0.84


######################
# TYPES
######################

class IconGenerationMethod(Enum):
    NONE = 0
    IMAGE = 1
    TEXT = 2


class FolderStyle(Enum):
    big_sur_light = 0
    big_sur_dark = 1
    catalina = 2
    tahoe = 3

    def filename(self):
        """Filename of the icon in the assets folder

        :return: Filename
        """
        return {
            FolderStyle.big_sur_light: "big_sur_light.png",
            FolderStyle.big_sur_dark: "big_sur_dark.png",
            FolderStyle.catalina: "catalina.png",
            FolderStyle.tahoe: "tahoe.png",
        }[self]

    def display_name(self):
        """Name to display to the user

        :return: Name
        """
        return {
            FolderStyle.big_sur_light: "macOS Big Sur - Light mode",
            FolderStyle.big_sur_dark: "macOS Big Sur - Dark mode",
            FolderStyle.catalina: "macOS Catalina",
            FolderStyle.tahoe: "macOS Tahoe",
        }[self]

    def size(self) -> int:
        """Size of the folder in pixels (1 dimension only because square)

        :return: Size in pixels
        """
        return {
            FolderStyle.big_sur_light: 1024,
            FolderStyle.big_sur_dark: 1024,
            FolderStyle.catalina: 1024,
            FolderStyle.tahoe: 1024,
        }[self]

    def icon_box_percentages(self) -> tuple[float, float, float, float]:
        """Size of the rect in percentages which contains the region to
        draw the icon

        :return: Coordinate percentages (x1, y1, x2, y2)
        """
        return {
            FolderStyle.big_sur_light: (0.086, 0.29, 0.914, 0.777),
            FolderStyle.big_sur_dark: (0.086, 0.29, 0.914, 0.777),
            FolderStyle.catalina: (0.0668, 0.281, 0.9332, 0.770),
            FolderStyle.tahoe: (0.0668, 0.281, 0.9332, 0.770),
        }[self]

    def preview_crop_percentages(self) -> tuple[float, float, float, float]:
        """Minimum size of the rect in percentages which contains the
        folder for displaying in the preview image

        :return: Coordinate percentages (x1, y1, x2, y2)
        """
        return {
            FolderStyle.big_sur_light: (0, 0.0888, 1.0, 0.9276),
            FolderStyle.big_sur_dark: (0, 0.0888, 1.0, 0.9276),
            FolderStyle.catalina: (0, 0.0972, 1.0, 0.896),
            FolderStyle.tahoe: (0, 0.0972, 1.0, 0.896),
        }[self]

    def base_colour(self) -> tuple[int, int, int]:
        """The average colour of the folder where the icon is to be drawn

        :return: Colour (r, g, b)
        """
        return {
            FolderStyle.big_sur_light: (116, 208, 251),
            FolderStyle.big_sur_dark: (96, 208, 255),
            FolderStyle.catalina: (120, 210, 251),
            FolderStyle.tahoe: (120, 210, 251),
        }[self]

    def icon_colour(self) -> tuple[int, int, int]:
        """The average colour of the icon in default macOS folders

        :return: Colour (r, g, b)
        """
        return {
            FolderStyle.big_sur_light: (63, 170, 229),
            FolderStyle.big_sur_dark: (53, 160, 225),
            FolderStyle.catalina: (63, 170, 229),  # TODO set properly
            FolderStyle.tahoe: (63, 170, 229),  # TODO set properly
        }[self]


class TintColour(Enum):
    """Default colour palette for folder tints"""
    red = (195, 118, 124)
    melon = (195, 140, 136)
    orange = (195, 167, 148)
    yellow = (195, 181, 160)
    green = (173, 184, 156)
    teal = (139, 179, 165)
    lightblue = (139, 175, 187)
    purple = (152, 158, 179)
    cream = (195, 192, 184)
    white = (225, 224, 221)


class SFFont(Enum):
    ultralight = 1
    thin = 2
    light = 3
    regular = 4
    medium = 5
    semibold = 6
    bold = 7
    heavy = 8
    black = 9

    def filename(self):
        """Filename of the font in the assets/font folder

        :return: Filename
        """
        return {
            SFFont.ultralight: "SF-Pro-Rounded-Ultralight.otf",
            SFFont.thin: "SF-Pro-Rounded-Thin.otf",
            SFFont.light: "SF-Pro-Rounded-Light.otf",
            SFFont.regular: "SF-Pro-Rounded-Regular.otf",
            SFFont.medium: "SF-Pro-Rounded-Medium.otf",
            SFFont.semibold: "SF-Pro-Rounded-Semibold.otf",
            SFFont.bold: "SF-Pro-Rounded-Bold.otf",
            SFFont.heavy: "SF-Pro-Rounded-Heavy.otf",
            SFFont.black: "SF-Pro-Rounded-Black.otf",
        }[self]


DEFAULT_FONT = SFFont.bold
