# -*- mode: python ; coding: utf-8 -*-

added_files = [
('src/back_end/categories/*.json',   '.'),
('src/back_end/parsing/*.json',   '.'),
('src/back_end/profiles/*.json',   '.'),
]



a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=added_files,
    hiddenimports=['pandas_gbq'],
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
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['src/assets/images/logo.icns']
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
    name='main.app',
    icon='src/assets/images/logo.icns',
    bundle_identifier=None,
    version='1.1.2'
)
