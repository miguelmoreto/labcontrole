# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['LabControl3.py'],
    pathex=[],
    binaries=[],
    datas=[('MainWindow.ui', '.'), ('HelpWindow.ui', '.'), ('matplotlibwidget.py', '.'), ('./help/*', './help')],
    hiddenimports=['PyQt5.sip', 'numpy.core.multiarray'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['sqlalchemy'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='LabControl3',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    contents_directory='.',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='LabControl3',
)
