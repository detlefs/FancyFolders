# -*- mode: python ; coding: utf-8 -*-

import os

# SPECPATH is injected by PyInstaller: the directory containing this spec file.
ROOT = os.path.abspath(SPECPATH)

a = Analysis(
    [os.path.join(ROOT, 'fancyfolders', 'main.py')],
    pathex=[ROOT],
    binaries=[],
    datas=[(os.path.join(ROOT, "assets"), "assets")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    # Override with e.g. TARGET_ARCH=universal2 or x86_64 before running pyinstaller.
    target_arch=os.environ.get('TARGET_ARCH', 'arm64'),
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
app = BUNDLE(
    coll,
    name='Fancy Folders.app',
    version='2.0',
    icon=os.path.join(ROOT, "assets", "app_icon.icns"),
    bundle_identifier="ca.kfreitag.fancyfolders",
)

# note, need to do: .venv/bin/pyinstaller main.spec
