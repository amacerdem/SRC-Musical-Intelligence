"""Audio preprocessing utilities for the MI training pipeline.

Provides audio loading, resampling, and mel spectrogram extraction
with the canonical MI parameters (sr=44100, hop=256, n_mels=128).

Usage::

    mel = load_and_preprocess("track.wav")
    # mel: (1, 128, T) log1p-normalised mel spectrogram
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple, Union

import torch
from torch import Tensor

from Musical_Intelligence.training.model.mi_space_layout import (
    HOP_LENGTH,
    N_FFT,
    N_MELS,
    SAMPLE_RATE,
)


def load_audio(
    path: Union[str, Path],
    target_sr: int = SAMPLE_RATE,
    mono: bool = True,
) -> Tuple[Tensor, int]:
    """Load an audio file and resample to target sample rate.

    Parameters
    ----------
    path : str or Path
        Path to audio file (.wav, .flac, .mp3, etc.).
    target_sr : int
        Target sample rate (default 44100).
    mono : bool
        If True, mix to mono (default True).

    Returns
    -------
    waveform : Tensor
        Shape ``(1, samples)`` for mono.
    sr : int
        Actual sample rate (always ``target_sr``).
    """
    import torchaudio

    waveform, sr = torchaudio.load(str(path))

    # Mix to mono if needed
    if mono and waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0, keepdim=True)

    # Resample if needed
    if sr != target_sr:
        resampler = torchaudio.transforms.Resample(sr, target_sr)
        waveform = resampler(waveform)

    return waveform, target_sr


def compute_mel(
    waveform: Tensor,
    sr: int = SAMPLE_RATE,
    n_fft: int = N_FFT,
    hop_length: int = HOP_LENGTH,
    n_mels: int = N_MELS,
    log1p_normalize: bool = True,
) -> Tensor:
    """Compute mel spectrogram from waveform.

    Parameters
    ----------
    waveform : Tensor
        Shape ``(B, samples)`` or ``(1, samples)``.
    sr : int
        Sample rate.
    n_fft : int
        FFT window size.
    hop_length : int
        Hop length in samples.
    n_mels : int
        Number of mel bins.
    log1p_normalize : bool
        If True, apply log1p and normalise to [0, 1].

    Returns
    -------
    Tensor
        Shape ``(B, n_mels, T)`` mel spectrogram.
    """
    import torchaudio

    mel_transform = torchaudio.transforms.MelSpectrogram(
        sample_rate=sr,
        n_fft=n_fft,
        hop_length=hop_length,
        n_mels=n_mels,
        power=2.0,
    ).to(waveform.device)

    mel = mel_transform(waveform)  # (B, n_mels, T)

    if log1p_normalize:
        mel = torch.log1p(mel)
        mel_max = mel.amax(dim=(-2, -1), keepdim=True).clamp(min=1e-8)
        mel = mel / mel_max

    return mel


def load_and_preprocess(
    path: Union[str, Path],
    target_sr: int = SAMPLE_RATE,
    max_duration_s: Optional[float] = None,
) -> Tensor:
    """Load audio file and return preprocessed mel spectrogram.

    Parameters
    ----------
    path : str or Path
        Path to audio file.
    target_sr : int
        Target sample rate (default 44100).
    max_duration_s : float or None
        If set, truncate audio to this duration in seconds.

    Returns
    -------
    Tensor
        Shape ``(1, 128, T)`` log1p-normalised mel spectrogram.
    """
    waveform, sr = load_audio(path, target_sr=target_sr)

    if max_duration_s is not None:
        max_samples = int(max_duration_s * sr)
        if waveform.shape[-1] > max_samples:
            waveform = waveform[:, :max_samples]

    return compute_mel(waveform, sr=sr)


def frames_to_seconds(n_frames: int) -> float:
    """Convert frame count to seconds."""
    return n_frames * HOP_LENGTH / SAMPLE_RATE


def seconds_to_frames(seconds: float) -> int:
    """Convert seconds to frame count."""
    return int(seconds * SAMPLE_RATE / HOP_LENGTH)
