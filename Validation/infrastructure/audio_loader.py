"""Unified audio loading utility for validation — supports wav, mp3, flac, MIDI→wav."""
from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple

import numpy as np
import torch
from torch import Tensor

from Validation.config.constants import HOP_LENGTH, N_FFT, N_MELS, SAMPLE_RATE


def load_audio(
    path: str | Path,
    excerpt_s: Optional[float] = None,
    mono: bool = True,
    target_sr: int = SAMPLE_RATE,
) -> Tuple[np.ndarray, int]:
    """Load audio file to numpy array.

    Args:
        path: Path to audio file.
        excerpt_s: Max duration (None = full file).
        mono: Mix to mono if True.
        target_sr: Target sample rate.

    Returns:
        Tuple of (audio_array (N,) or (C,N), sample_rate).
    """
    import soundfile as sf
    import torchaudio

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {path}")

    try:
        data, sr = sf.read(str(path), dtype="float32")
        if mono and data.ndim == 2:
            data = data.mean(axis=1)
    except Exception:
        waveform, sr = torchaudio.load(str(path))
        if mono and waveform.shape[0] > 1:
            waveform = waveform.mean(dim=0, keepdim=True)
        data = waveform.squeeze(0).numpy()

    # Resample if needed
    if sr != target_sr:
        resampler = torchaudio.transforms.Resample(sr, target_sr)
        data = resampler(torch.from_numpy(data).unsqueeze(0)).squeeze(0).numpy()
        sr = target_sr

    # Truncate
    if excerpt_s is not None:
        max_samples = int(excerpt_s * sr)
        if data.shape[-1] > max_samples:
            data = data[..., :max_samples]

    return data, sr


def load_audio_tensor(
    path: str | Path,
    excerpt_s: Optional[float] = None,
    device: Optional[torch.device] = None,
) -> Tuple[Tensor, Tensor, float]:
    """Load audio and compute mel spectrogram (same as MI pipeline).

    Returns:
        Tuple of (waveform (1,N), mel (1,128,T), duration_s).
    """
    from Validation.infrastructure.mi_bridge import load_audio as _load
    return _load(path, excerpt_s, device)


def midi_to_audio(
    midi_path: str | Path,
    output_path: str | Path,
    sr: int = SAMPLE_RATE,
    sf2_path: Optional[str] = None,
) -> Path:
    """Synthesize MIDI to WAV using fluidsynth or pretty_midi.

    Args:
        midi_path: Path to MIDI file.
        output_path: Path for output WAV.
        sr: Sample rate.
        sf2_path: Optional SoundFont path.

    Returns:
        Path to synthesized WAV file.
    """
    import pretty_midi
    import soundfile as sf

    midi_path = Path(midi_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    midi = pretty_midi.PrettyMIDI(str(midi_path))
    audio = midi.fluidsynth(fs=sr, sf2_path=sf2_path)

    if audio.ndim == 2:
        audio = audio.mean(axis=0)

    # Normalize
    peak = np.abs(audio).max()
    if peak > 0:
        audio = audio / peak * 0.95

    sf.write(str(output_path), audio, sr)
    return output_path


def generate_tone(
    frequency: float,
    duration_s: float,
    sr: int = SAMPLE_RATE,
    amplitude: float = 0.5,
) -> np.ndarray:
    """Generate a pure sine tone.

    Returns:
        Audio array (N,) at the given sample rate.
    """
    t = np.arange(int(duration_s * sr)) / sr
    return (amplitude * np.sin(2 * np.pi * frequency * t)).astype(np.float32)


def generate_chord(
    frequencies: list[float],
    duration_s: float,
    sr: int = SAMPLE_RATE,
    amplitude: float = 0.3,
) -> np.ndarray:
    """Generate a chord from multiple sine tones.

    Returns:
        Audio array (N,) with mixed tones.
    """
    t = np.arange(int(duration_s * sr)) / sr
    signal = np.zeros_like(t, dtype=np.float32)
    for freq in frequencies:
        signal += amplitude * np.sin(2 * np.pi * freq * t).astype(np.float32)
    peak = np.abs(signal).max()
    if peak > 0:
        signal = signal / peak * 0.95
    return signal
