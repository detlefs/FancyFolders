<!-- PROJECT LOGO -->

<br />

<div align="center">

  <img src="readme_assets/scaled_down_icon.png" alt="Logo" width="150" height="150">

  <h1>Fancy Folders</h1>

</div>

> **Fork notice:** This is a modified version of
> [kfreitag1/FancyFolders](https://github.com/kfreitag1/FancyFolders), maintained by
> Detlef Schneider since August 2026. Changes include the Tahoe folder style, full icon-family
> output, emoji and SVG symbol rendering, and arm64 builds. Like the original, it is released
> under the GPL v3.

**Fancy Folders** is a macOS application for creating customized folder icons from SF symbols, text, or images.

- Drag and drop to set the icon and output folder
- Customize the icon scale, thickness, and colour
- Save the icon!

<div align="center">

![](readme_assets/carousel.png)

</div>

## Get started

<h3><a href="https://github.com/detlefs/FancyFolders/releases/latest">:floppy_disk: Download latest Fancy Folders release</a></h3>

***Note:** Please follow the first launch instructions in order to use the app. This is needed for all apps produced by [unidentified developers](https://support.apple.com/en-ca/guide/mac-help/mh40616/mac), i.e. those without Apple developer accounts.*

<h3><a href="https://developer.apple.com/sf-symbols/">:floppy_disk: Download latest SF Symbols</a></h3>

## Features

<div align="center">

![](readme_assets/demonstration.gif)

</div>

- Drag to set icon
  - From the **SF Symbols** app *(recommended)*
  - From an image (eg. from Google images)
  - From an image file (eg .jpg or .png file)
  - Type in text in the input field
  - Type or paste emoji. Emoji are drawn in their own colours. Note, text and emoji cannot be mixed
- Dropped SF Symbols are taken as vector art, so they always match the
rendering mode set in the SF Symbols app, including multicolour, and work
with symbols of any SF Symbols version
- An SF Symbol can also be dropped on the icon text field to combine it with
your own text. It is then drawn from the SF Pro fonts bundled with the app,
which are updated to the latest version before each release, so a very new
symbol may need a newer release to show up
- Tick "Keep original image colours" to place an image on top of the folder
instead of engraving it into it
- Drag to set the output folder
- Choose the folder style to match your macOS version: Tahoe *(default)*, Big Sur in light or dark mode, or Catalina. Note: Catalina and Tahoe icons are in fact the same. Separated here only for ease of use
- Choose a folder tint colour from the list or select a custom colour
- Click "Save Icon" to save the folder to the output folder, or to make a new folder with the icon in the chosen directory
  - Icons are written in every macOS icon size, so they stay as sharp as possible down to the  
  16px list view

## Scripts

Helper scripts in `scripts/`, not needed to use the app:

- `update_fonts.sh` — replaces the bundled SF Pro Rounded fonts in `assets/fonts`
with Apple's current release, so newly added SF Symbols render in the icon text field
- `export_icon.py` — exports a folder's custom icon as one PNG per icon size,
useful to check what was actually written:
`.venv/bin/python scripts/export_icon.py <folder> <destination directory>`

## Licence

Fancy Folders is released under the [GPL v3 Licence](https://www.gnu.org/licenses/gpl-3.0.en.html). Fonts used in this project and the SF symbols app are the property of Apple and are not included within this licence.

## Special thanks

Kieran Freitag, who wrote the original Fancy Folders this fork builds on.

From the original readme: *"My lovely girlfriend Kelsey who had to put up with me while I made this"* :heart: