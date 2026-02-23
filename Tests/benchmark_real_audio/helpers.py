"""Shared utilities for benchmark_real_audio tests.

Non-pytest helpers (constants, audio loading, memory tracking, timers)
that test modules can import directly.
"""
from __future__ import annotations

import gc
import pathlib
import sys
import time
import tracemalloc
from typing import Tuple

import torch
from torch import Tensor

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
_TEST_AUDIO_DIR = _PROJECT_ROOT / "Test-Audio"

if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

# ---------------------------------------------------------------------------
# Audio constants (canonical MI parameters)
# ---------------------------------------------------------------------------
SAMPLE_RATE = 44100
HOP_LENGTH = 256
N_MELS = 128
N_FFT = 2048
FRAME_RATE = SAMPLE_RATE / HOP_LENGTH  # 172.27 Hz

# Default excerpt: 30s to fit in 8GB RAM
DEFAULT_EXCERPT_S = 30.0

# ---------------------------------------------------------------------------
# Audio catalog — all files in Test-Audio/
# ---------------------------------------------------------------------------
AUDIO_CATALOG = {
    "bach": "Cello Suite No. 1 in G Major, BWV 1007 I. Prélude.wav",
    "swan": "Swan Lake Suite, Op. 20a_ I. Scene _Swan Theme_. Moderato - Pyotr Ilyich Tchaikovsky.wav",
    "herald": "Herald of the Change - Hans Zimmer.wav",
    "beethoven": "Beethoven - Pathetique Sonata Op13 I. Grave - Allegro.wav",
    "duel": "Duel of the Fates - Epic Version.wav",
    "enigma": "Enigma in The Veil-Eclipse-Segment I - Amaç Erdem.wav",
    "yang": "Yang.mp3",
}

# Genre categories for cross-genre analysis
GENRE_GROUPS = {
    "solo_acoustic": ["bach"],
    "orchestral": ["swan", "beethoven"],
    "film_epic": ["herald", "duel"],
    "contemporary": ["enigma", "yang"],
}

# R³ group boundaries
R3_GROUPS = {
    "A_consonance": (0, 7),
    "B_energy": (7, 12),
    "C_timbre": (12, 21),
    "D_change": (21, 25),
    "F_pitch_chroma": (25, 41),
    "G_rhythm_groove": (41, 51),
    "H_harmony": (51, 63),
    "J_timbre_extended": (63, 83),
    "K_modulation": (83, 97),
}

# Morph type labels
MORPH_NAMES = {
    0: "mean", 2: "std", 8: "velocity", 14: "periodicity", 18: "trend",
}
LAW_NAMES = {0: "memory(L0)", 1: "forward(L1)", 2: "integration(L2)"}


# ---------------------------------------------------------------------------
# Helper: load audio and compute mel
# ---------------------------------------------------------------------------
def load_audio_file(
    name: str,
    excerpt_s: float | None = DEFAULT_EXCERPT_S,
) -> Tuple[Tensor, Tensor, float]:
    """Load audio file, return (waveform, mel, duration_s).

    Returns:
        waveform: (1, N_samples) tensor
        mel: (1, 128, T) log1p-normalized mel spectrogram
        duration_s: actual duration in seconds
    """
    import soundfile as sf
    import numpy as np
    import torchaudio

    filename = AUDIO_CATALOG[name]
    filepath = _TEST_AUDIO_DIR / filename

    if not filepath.exists():
        raise FileNotFoundError(f"Audio file not found: {filepath}")

    # Use soundfile for WAV, torchaudio fallback for MP3
    try:
        data, sr = sf.read(str(filepath), dtype="float32")
        if data.ndim == 2:
            data = data.mean(axis=1)  # stereo → mono
        waveform = torch.from_numpy(data).unsqueeze(0)  # (1, N)
    except Exception:
        waveform, sr = torchaudio.load(str(filepath))
        if waveform.shape[0] > 1:
            waveform = waveform.mean(dim=0, keepdim=True)

    # Resample if needed
    if sr != SAMPLE_RATE:
        resampler = torchaudio.transforms.Resample(sr, SAMPLE_RATE)
        waveform = resampler(waveform)

    # Excerpt
    if excerpt_s is not None:
        max_samples = int(excerpt_s * SAMPLE_RATE)
        if waveform.shape[-1] > max_samples:
            waveform = waveform[:, :max_samples]

    duration_s = waveform.shape[-1] / SAMPLE_RATE

    # Mel spectrogram
    mel_transform = torchaudio.transforms.MelSpectrogram(
        sample_rate=SAMPLE_RATE,
        n_fft=N_FFT,
        hop_length=HOP_LENGTH,
        n_mels=N_MELS,
        power=2.0,
    )
    mel = mel_transform(waveform)  # (1, 128, T)
    mel = torch.log1p(mel)
    mel_max = mel.amax(dim=(-2, -1), keepdim=True).clamp(min=1e-8)
    mel = mel / mel_max

    return waveform, mel, duration_s


# ---------------------------------------------------------------------------
# Helper: memory tracking
# ---------------------------------------------------------------------------
class MemoryTracker:
    """Context manager for tracking peak memory usage."""

    def __init__(self):
        self.peak_mb = 0.0

    def __enter__(self):
        gc.collect()
        tracemalloc.start()
        return self

    def __exit__(self, *args):
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        self.peak_mb = peak / (1024 * 1024)
        gc.collect()


class Timer:
    """Context manager for timing."""

    def __init__(self):
        self.elapsed_s = 0.0

    def __enter__(self):
        self._start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.elapsed_s = time.perf_counter() - self._start
