"""VocoderWrapper -- Frozen Vocos vocoder for mel→waveform rendering.

Wraps the pre-trained Vocos model for inference-only mel-to-waveform
conversion. This is used during cycle loss computation (decode direction)
and at inference time.

Vocos (Siuzdak et al.) uses iSTFT-based reconstruction — ~70x faster
than BigVGAN with equivalent quality. ~0.2ms per frame on GPU.

The vocoder is ALWAYS FROZEN — never trained.
"""
from __future__ import annotations

from typing import Optional

import torch
import torch.nn as nn
from torch import Tensor


class VocoderWrapper(nn.Module):
    """Frozen Vocos vocoder wrapper.

    Provides mel → waveform conversion for the decode path.
    All parameters are frozen (never trained).

    Parameters
    ----------
    vocos_path : str, optional
        Path to pre-trained Vocos checkpoint. If None, uses a
        placeholder that returns zeros (for shape testing).
    sample_rate : int
        Output sample rate (default 44100).
    """

    def __init__(
        self,
        vocos_path: Optional[str] = None,
        sample_rate: int = 44100,
    ) -> None:
        super().__init__()
        self.sample_rate = sample_rate
        self._vocos = None

        if vocos_path is not None:
            self._load_vocos(vocos_path)

        # Freeze all parameters
        for param in self.parameters():
            param.requires_grad = False

    def _load_vocos(self, path: str) -> None:
        """Load pre-trained Vocos model."""
        try:
            from vocos import Vocos
            self._vocos = Vocos.from_pretrained(path)
            self._vocos.eval()
        except ImportError:
            pass  # Vocos not installed, use placeholder

    @torch.no_grad()
    def forward(self, mel: Tensor) -> Tensor:
        """Convert mel spectrogram to waveform.

        Parameters
        ----------
        mel : Tensor
            Shape ``(B, T, 128)`` mel spectrogram (time-first).

        Returns
        -------
        Tensor
            Shape ``(B, samples)`` waveform at sample_rate Hz.
        """
        if self._vocos is not None:
            # Vocos expects (B, n_mels, T)
            mel_transposed = mel.transpose(1, 2)
            return self._vocos(mel_transposed)

        # Placeholder: return zeros of approximate expected length
        B, T, D = mel.shape
        hop_length = 256
        samples = T * hop_length
        return torch.zeros(B, samples, device=mel.device, dtype=mel.dtype)

    def __repr__(self) -> str:
        status = "loaded" if self._vocos is not None else "placeholder"
        return f"VocoderWrapper(status={status}, sr={self.sample_rate})"
