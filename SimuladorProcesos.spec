# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['interfaz.py'],
    pathex=[],
    binaries=[],
    datas=[('Tandas', 'Tandas')],  # Incluir carpeta de tandas si existe
    hiddenimports=[
        'PIL._tkinter_finder',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'matplotlib.backends.backend_tkagg',
        'numpy',
        'tkinter',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SimuladorProcesos',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # False para no mostrar consola
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Aquí puedes agregar un ícono si tienes uno
)