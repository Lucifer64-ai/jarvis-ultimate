# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

from PyInstaller.utils.hooks import collect_all

# Collect all files from python-dotenv package
datas_dotenv, binaries_dotenv, hiddenimports_dotenv = collect_all('python_dotenv')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'dotenv',
        'dotenv.main',
        'python_dotenv',
        'openai',
        'requests',
        'aiohttp',
        'websockets',
        'psutil',
        'pyttsx3',
        'speech_recognition',
        'pyautogui',
        'plyer',
        'schedule',
        'sklearn',
        'numpy',
        'PIL',
        'pystray',
        'speedtest',
        'cpuinfo',
        'joblib',
    ] + hiddenimports_dotenv,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Add collected data and binaries
a.datas += datas_dotenv
a.binaries += binaries_dotenv

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='JARVIS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/jarvis.ico',
)
