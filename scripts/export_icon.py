#!/usr/bin/env python3
"""Exports the custom icon of a folder as PNG files, one per icon size.

Usage: .venv/bin/python scripts/export_icon.py <folder> <destination directory>
"""

import argparse
import os
import sys

import Cocoa


def export_icon(folder: str, destination: str) -> list[str]:
    """Writes every representation of the folder's icon as a PNG file

    :param folder: Path to the folder whose icon should be exported
    :param destination: Directory to write the PNG files into
    :return: Paths of the written PNG files
    :raises OSError: If the folder has no custom icon or a PNG cannot be written
    """
    # NSWorkspace needs an absolute path; given a relative one it silently
    # hands back the generic document icon
    folder = os.path.abspath(folder)
    if not os.path.isdir(folder):
        raise OSError("'{}' is not a folder".format(folder))
    # A custom icon lives in an 'Icon\r' file; without it macOS would hand us
    # the generic folder icon, which is not what the user asked to export
    if not os.path.exists(os.path.join(folder, "Icon\r")):
        raise OSError("'{}' has no custom icon".format(folder))

    image = Cocoa.NSWorkspace.sharedWorkspace().iconForFile_(folder)
    if image is None:
        raise OSError("macOS returned no icon for '{}'".format(folder))

    os.makedirs(destination, exist_ok=True)
    name = os.path.basename(folder)

    # The icon's own representations are not bitmaps; the TIFF detour turns
    # every size into an NSBitmapImageRep, with duplicates for the retina
    # variants that render identically
    written = []
    seen = set()
    for rep in Cocoa.NSBitmapImageRep.imageRepsWithData_(
            image.TIFFRepresentation()):
        if rep.pixelsWide() in seen:
            continue
        seen.add(rep.pixelsWide())
        data = rep.representationUsingType_properties_(
            Cocoa.NSBitmapImageFileTypePNG, {})
        if data is None:
            raise OSError("Could not encode the {}px icon as PNG".format(
                rep.pixelsWide()))
        out = os.path.join(destination, "{}_{}.png".format(
            name, rep.pixelsWide()))
        if not data.writeToFile_atomically_(out, True):
            raise OSError("Could not write '{}'".format(out))
        written.append(out)

    if not written:
        raise OSError("The icon of '{}' has no bitmap representation".format(
            folder))
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", help="Folder whose custom icon to export")
    parser.add_argument("destination", help="Directory to write the PNGs into")
    args = parser.parse_args()

    try:
        for path in export_icon(args.folder, args.destination):
            print(path)
    except OSError as error:
        print("Error: {}".format(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
