#!/bin/bash
# Updates the bundled SF Pro Rounded fonts from Apple's current SF Pro
# release, so that newly added SF Symbols render in the icon text field.
# Only the fonts already in assets/fonts are replaced.
set -euo pipefail

DMG_URL="https://devimages-cdn.apple.com/design/resources/download/SF-Pro.dmg"
FONT_DIR="$(cd "$(dirname "$0")" && pwd)/assets/fonts"

work="$(mktemp -d)"
mount=""
cleanup() {
    [ -n "$mount" ] && hdiutil detach "$mount" -quiet || true
    rm -rf "$work"
}
trap cleanup EXIT

echo "Downloading $DMG_URL"
curl -fL --progress-bar -o "$work/SF-Pro.dmg" "$DMG_URL"

mount="$work/mount"
mkdir "$mount"
hdiutil attach "$work/SF-Pro.dmg" -mountpoint "$mount" -nobrowse -quiet

pkg="$(find "$mount" -name "*.pkg" -maxdepth 2 | head -1)"
[ -n "$pkg" ] || { echo "No installer package in the disk image" >&2; exit 1; }
pkgutil --expand-full "$pkg" "$work/pkg"

updated=0
for font in "$FONT_DIR"/*.otf; do
    name="$(basename "$font")"
    new="$(find "$work/pkg" -name "$name" | head -1)"
    if [ -z "$new" ]; then
        echo "Missing in the new release, keeping the old one: $name" >&2
        continue
    fi
    cmp -s "$new" "$font" || { cp "$new" "$font"; echo "Updated $name"; }
    updated=$((updated + 1))
done

echo "Checked $updated font(s) in $FONT_DIR"
