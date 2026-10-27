# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path


project_dir = Path(SPECPATH)

a = Analysis(
    [str(project_dir / "xpad.py")],
    pathex=[str(project_dir)],
    binaries=[],
    datas=[],
    hiddenimports=["pynput.keyboard._win32", "pynput.mouse._win32", "win32timezone"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="xpad",
    console=True,
    debug=False,
    strip=False,
    upx=False,
    icon=[str(project_dir / "joystick.ico")],
)
