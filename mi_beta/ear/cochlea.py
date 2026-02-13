"""Cochlea: audio waveform → mel spectrogram preprocessing."""

from __future__ import annotations

import torch
from torch import Tensor
import torchaudio.transforms as T

from ..core.config import MIBetaConfig, MI_BETA_CONFIG
from ..core.types import CochleaOutput


def audio_to_mel(
    waveform: Tensor,
    config: MIBetaConfig = MI_BETA_CONFIG,
) -> CochleaOutput:
    """Convert audio waveform to log-normalized mel spectrogram.

    Args:
        waveform: (B, samples) or (samples,) mono/stereo audio
        config: MI-Beta configuration

    Returns:
        CochleaOutput with mel=(B, 128, T), normalized to [0, 1]
    """
    # Ensure batch dimension
    if waveform.dim() == 1:
        waveform = waveform.unsqueeze(0)

    # Enforce mono by averaging channels if stereo
    if waveform.dim() == 3:
        waveform = waveform.mean(dim=1)

    B = waveform.shape[0]

    # MelSpectrogram transform
    mel_transform = T.MelSpectrogram(
        sample_rate=config.sample_rate,
        n_fft=config.n_fft,
        hop_length=config.hop_length,
        n_mels=config.n_mels,
        power=2.0,
    ).to(waveform.device)

    mel = mel_transform(waveform)  # (B, n_mels, T)

    # Log normalization
    mel = torch.log1p(mel)

    # Per-batch normalization to [0, 1]
    for b in range(B):
        max_val = mel[b].max()
        if max_val > 0:
            mel[b] = mel[b] / max_val

    return CochleaOutput(
        mel=mel,
        sample_rate=config.sample_rate,
        hop_length=config.hop_length,
    )
