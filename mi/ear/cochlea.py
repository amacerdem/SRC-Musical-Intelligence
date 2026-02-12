"""
Cochlea — Audio waveform to mel spectrogram.

Mimics the basilar membrane: frequency decomposition into
128 mel-frequency bins at 172.27 Hz frame rate.

Input:  waveform (B, samples) or (samples,) at any sample rate
Output: CochleaOutput with mel (B, 128, T)
"""

from __future__ import annotations

import torch
from torch import Tensor

from ..core.config import MIConfig, MI_CONFIG
from ..core.types import CochleaOutput


def audio_to_mel(
    waveform: Tensor,
    config: MIConfig = MI_CONFIG,
) -> CochleaOutput:
    """Convert audio waveform to log-mel spectrogram.

    Args:
        waveform: (B, samples) or (samples,) audio tensor
        config: MI configuration

    Returns:
        CochleaOutput with mel spectrogram (B, N_MELS, T)
    """
    import torchaudio.transforms as T

    # Ensure batch dimension
    if waveform.dim() == 1:
        waveform = waveform.unsqueeze(0)

    # Ensure mono
    if waveform.dim() == 3:
        waveform = waveform.mean(dim=1)

    B = waveform.shape[0]

    # Mel spectrogram transform
    mel_transform = T.MelSpectrogram(
        sample_rate=config.sample_rate,
        n_fft=config.n_fft,
        hop_length=config.hop_length,
        n_mels=config.n_mels,
        power=2.0,
    ).to(waveform.device)

    # Compute mel spectrogram: (B, n_mels, T)
    mel = mel_transform(waveform)

    # Log1p normalization (matches D0 pipeline convention)
    mel = torch.log1p(mel)

    # Normalize per-batch to [0, 1] range
    mel_max = mel.amax(dim=(-2, -1), keepdim=True).clamp(min=1e-8)
    mel = mel / mel_max

    return CochleaOutput(
        mel=mel,
        sample_rate=config.sample_rate,
        hop_length=config.hop_length,
    )
