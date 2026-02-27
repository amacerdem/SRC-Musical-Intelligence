"""MI-Lab backend configuration — paths, constants, audio catalog."""
from __future__ import annotations

import json
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BACKEND_DIR = Path(__file__).resolve().parent
LAB_DIR = BACKEND_DIR.parent
PROJECT_ROOT = LAB_DIR.parent
AUDIO_DIR = PROJECT_ROOT / "Test-Audio"
EXPERIMENTS_DIR = LAB_DIR / "experiments"

# ---------------------------------------------------------------------------
# Audio constants (canonical MI parameters)
# ---------------------------------------------------------------------------
SAMPLE_RATE = 44100
HOP_LENGTH = 256
N_MELS = 128
N_FFT = 2048
FRAME_RATE = SAMPLE_RATE / HOP_LENGTH  # 172.265625 Hz

DEFAULT_EXCERPT_S = 30.0

# ---------------------------------------------------------------------------
# Audio catalog — maps short names to filenames in Test-Audio/
# ---------------------------------------------------------------------------
AUDIO_CATALOG: dict[str, str] = {
    "bach": "Cello Suite No. 1 in G Major, BWV 1007 I. Prélude.wav",
    "swan": "Swan Lake Suite, Op. 20a_ I. Scene _Swan Theme_. Moderato - Pyotr Ilyich Tchaikovsky.wav",
    "herald": "Herald of the Change - Hans Zimmer.wav",
    "beethoven": "Beethoven - Pathetique Sonata Op13 I. Grave - Allegro.wav",
    "duel": "Duel of the Fates - Epic Version.wav",
    "enigma": "Enigma in The Veil-Eclipse-Segment I - Amaç Erdem.wav",
    "yang": "Yang.mp3",
}

# ---------------------------------------------------------------------------
# MIDI test audio catalog — loaded from metadata.json
# ---------------------------------------------------------------------------
MIDI_AUDIO_DIR = AUDIO_DIR / "micro_beliefs" / "f1_midi"
_MIDI_METADATA_PATH = MIDI_AUDIO_DIR / "metadata.json"


def _load_midi_catalog() -> dict[str, dict]:
    """Load MIDI test audio catalog with metadata.

    Keys like 'midi/csg/04_V7_I_resolution' map to metadata dicts
    with an added 'path' field pointing to the WAV file.
    """
    if not _MIDI_METADATA_PATH.exists():
        return {}
    with open(_MIDI_METADATA_PATH, encoding="utf-8") as f:
        raw = json.load(f)
    catalog: dict[str, dict] = {}
    for relay_key, meta in raw.items():
        # relay_key is like "csg/04_V7_I_resolution"
        catalog_name = f"midi/{relay_key}"
        catalog[catalog_name] = {
            **meta,
            "path": MIDI_AUDIO_DIR / meta["relay"] / meta["filename"],
        }
    return catalog


MIDI_CATALOG: dict[str, dict] = _load_midi_catalog()
