"""AudioLoader -- Load audio files to tensor."""
from __future__ import annotations
from pathlib import Path
import torch
from torch import Tensor
from ..core.config import MIBetaConfig, MI_BETA_CONFIG


def load_audio(path: str | Path, config: MIBetaConfig = MI_BETA_CONFIG) -> Tensor:
    import soundfile as sf
    import torchaudio
    data, sr = sf.read(str(path), dtype="float32")
    if data.ndim == 1:
        waveform = torch.from_numpy(data).unsqueeze(0)
    else:
        waveform = torch.from_numpy(data.T)
    if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0, keepdim=True)
    if sr != config.sample_rate:
        resampler = torchaudio.transforms.Resample(sr, config.sample_rate)
        waveform = resampler(waveform)
    return waveform
