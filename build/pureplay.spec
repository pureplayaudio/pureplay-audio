# -*- mode: python ; coding: utf-8 -*-

import os
from PyInstaller.utils.hooks import collect_all

block_cipher = None

# =============================
# PATH BASE
# =============================

BASE_DIR = os.getcwd()
ENTRY_SCRIPT = os.path.join(BASE_DIR, "pureplay_run.py")

# =============================
# DEPENDENCIAS COMPLEJAS
# =============================

# Demucs
demucs_datas, demucs_binaries, demucs_hidden = collect_all("demucs")

# Torch
torch_datas, torch_binaries, torch_hidden = collect_all("torch")

# Torchaudio
torchaudio_datas, torchaudio_binaries, torchaudio_hidden = collect_all("torchaudio")

# SoundFile
sf_datas, sf_binaries, sf_hidden = collect_all("soundfile")

# NumPy (CRÍTICO)
numpy_datas, numpy_binaries, numpy_hidden = collect_all("numpy")

# =============================
# ANALYSIS
# =============================

a = Analysis(
    [ENTRY_SCRIPT],
    pathex=[BASE_DIR],
    binaries=(
        demucs_binaries
        + torch_binaries
        + torchaudio_binaries
        + sf_binaries
        + numpy_binaries
    ),
    datas=(
        demucs_datas
        + torch_datas
        + torchaudio_datas
        + sf_datas
        + numpy_datas
    ),
    hiddenimports=(
        demucs_hidden
        + torch_hidden
        + torchaudio_hidden
        + sf_hidden
        + numpy_hidden
    ),
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# =============================
# PYZ
# =============================

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

# =============================
# EXE
# =============================

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="pureplay",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # consola visible (QA / debug)
)

# =============================
# COLLECT (ONE-FOLDER)
# =============================

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="pureplay"
)