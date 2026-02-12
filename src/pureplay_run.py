import os
import sys
import re
import torch
import torchaudio
import numpy as np
import soundfile as sf

from demucs.apply import apply_model
from demucs.pretrained import get_model
from demucs.audio import AudioFile

# =============================
# PATH BASE (CORRECTO PARA EXE)
# =============================

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_DIR = os.path.join(BASE_DIR, "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =============================
# PERFILES DISPONIBLES
# =============================

PROFILE_MAP = {
    "vocals": "vocals",
    "bass": "bass",
    "drums": "drums",
    "other": "other",
    "groove": "groove",
    "karaoke": "karaoke",
}

ALL_SOURCES = ["vocals", "bass", "drums", "other"]

# =============================
# UTILIDADES
# =============================

def error_exit(msg):
    print(f"[ERROR] {msg}")
    sys.exit(1)

def sanitize_filename(name: str) -> str:
    """
    Limpia el nombre para usarlo como prefijo de archivo.
    - Reemplaza espacios por _
    - Elimina caracteres raros
    """
    name = name.strip().replace(" ", "_")
    name = re.sub(r"[^A-Za-z0-9_\-]", "", name)
    return name

def find_input_audio():
    files = [
        f for f in os.listdir(INPUT_DIR)
        if f.lower().endswith((".wav", ".mp3", ".flac"))
    ]

    if not files:
        error_exit("No se encontró audio en la carpeta input/")
    if len(files) > 1:
        error_exit("Solo debe haber un archivo de audio en input/")

    return os.path.join(INPUT_DIR, files[0])

def normalize(audio, target=0.98):
    peak = np.max(np.abs(audio))
    if peak == 0:
        return audio
    return audio / peak * target

def write_wav(path, audio, sr):
    audio = normalize(audio)
    sf.write(path, audio.T, sr, subtype="PCM_24")

# =============================
# MAIN
# =============================

def main():
    if len(sys.argv) != 2:
        error_exit("Uso: pureplay.exe <perfil>")

    profile = sys.argv[1].lower()
    if profile not in PROFILE_MAP:
        error_exit(f"Perfil inválido: {profile}")

    audio_path = find_input_audio()

    # Prefijo basado en el nombre del audio
    input_name = os.path.splitext(os.path.basename(audio_path))[0]
    safe_prefix = sanitize_filename(input_name)
    prefix = f"{safe_prefix}_"

    print("[INFO] Cargando modelo Demucs...")
    model = get_model(name="htdemucs")
    model.eval()

    print("[INFO] Cargando audio...")
    wav = AudioFile(audio_path).read(
        streams=0,
        samplerate=model.samplerate,
        channels=model.audio_channels,
    )
    wav = wav.to(torch.float32)

    print("[INFO] Separando audio...")
    with torch.no_grad():
        sources_tensor = apply_model(model, wav[None])[0]

    sources = {
        src: sources_tensor[i].cpu().numpy()
        for i, src in enumerate(model.sources)
    }

    sr = model.samplerate

    # =============================
    # PERFIL: GROOVE
    # =============================

    if profile == "groove":
        mix = sources["bass"] + sources["drums"]
        out_path = os.path.join(
            OUTPUT_DIR,
            f"{prefix}groove.wav"
        )
        write_wav(out_path, mix, sr)
        print("[OK] Archivo generado:", out_path)
        return

    # =============================
    # PERFIL: KARAOKE
    # =============================

    if profile == "karaoke":
        mix = sources["drums"] + sources["bass"] + sources["other"]
        out_path = os.path.join(
            OUTPUT_DIR,
            f"{prefix}karaoke.wav"
        )
        write_wav(out_path, mix, sr)
        print("[OK] Archivo generado:", out_path)
        return

    # =============================
    # PERFILES INDIVIDUALES
    # =============================

    # Instrument only
    out_only = os.path.join(
        OUTPUT_DIR,
        f"{prefix}{profile}_only.wav"
    )
    write_wav(out_only, sources[profile], sr)

    # Playalong
    playalong = sum(
        sources[src] for src in ALL_SOURCES if src != profile
    )
    out_play = os.path.join(
        OUTPUT_DIR,
        f"{prefix}{profile}_playalong.wav"
    )
    write_wav(out_play, playalong, sr)

    print("[OK] Archivos generados:")
    print(out_only)
    print(out_play)

# =============================
# ENTRYPOINT
# =============================

if __name__ == "__main__":
    main()