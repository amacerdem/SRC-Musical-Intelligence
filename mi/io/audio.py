"""
AudioLoader — Load audio files to tensor.
"""

from __future__ import annotations

from pathlib import Path

import torch
from torch import Tensor

from ..core.config import MIConfig, MI_CONFIG


def load_audio(
    path: str | Path,
    config: MIConfig = MI_CONFIG,
) -> Tensor:
    """Load audio file to tensor.

    Args:
        path: path to audio file (wav, mp3, flac)
        config: MI configuration

    Returns:
        (1, samples) mono audio tensor at config.sample_rate
    """
    import soundfile as sf
    import numpy as np
    import torchaudio

    data, sr = sf.read(str(path), dtype="float32")
    # sf.read returns (samples,) for mono, (samples, channels) for stereo
    if data.ndim == 1:
        waveform = torch.from_numpy(data).unsqueeze(0)  # (1, samples)
    else:
        waveform = torch.from_numpy(data.T)  # (channels, samples)

    # Mono
    if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0, keepdim=True)

    # Resample if needed
    if sr != config.sample_rate:
        resampler = torchaudio.transforms.Resample(sr, config.sample_rate)
        waveform = resampler(waveform)

    return waveform
