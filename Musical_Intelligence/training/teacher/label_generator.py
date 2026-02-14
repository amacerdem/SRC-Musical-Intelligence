"""LabelGenerator -- Batch label generation from audio files.

Provides utilities for generating MI Teacher labels from raw audio,
including mel spectrogram extraction and batched processing.

Usage::

    generator = LabelGenerator()
    output = generator.from_waveform(waveform, sr=44100)
    # output: TeacherOutput with mel, r3, h3_dense, c3
"""
from __future__ import annotations

from typing import Optional

import torch
from torch import Tensor

from Musical_Intelligence.training.model.mi_space_layout import (
    HOP_LENGTH,
    N_FFT,
    N_MELS,
    SAMPLE_RATE,
)
from Musical_Intelligence.training.teacher.mi_teacher import MITeacher, TeacherOutput


class LabelGenerator:
    """Generates MI Teacher labels from raw waveforms.

    Wraps MITeacher with audio preprocessing (mel spectrogram extraction).
    Suitable for offline pre-computation of training labels.
    """

    def __init__(self, teacher: Optional[MITeacher] = None) -> None:
        self._teacher = teacher or MITeacher()

    # ------------------------------------------------------------------
    # Audio -> Mel
    # ------------------------------------------------------------------

    @staticmethod
    def waveform_to_mel(
        waveform: Tensor,
        sr: int = SAMPLE_RATE,
        n_fft: int = N_FFT,
        hop_length: int = HOP_LENGTH,
        n_mels: int = N_MELS,
    ) -> Tensor:
        """Convert raw waveform to log-mel spectrogram.

        Parameters
        ----------
        waveform : Tensor
            Shape ``(B, samples)`` or ``(samples,)`` raw audio.
        sr : int
            Sample rate (default 44100).
        n_fft : int
            FFT window size (default 2048).
        hop_length : int
            Hop length in samples (default 256).
        n_mels : int
            Number of mel bins (default 128).

        Returns
        -------
        Tensor
            Shape ``(B, 128, T)`` log-mel spectrogram, log1p normalised
            to ``[0, 1]``.
        """
        import torchaudio

        if waveform.dim() == 1:
            waveform = waveform.unsqueeze(0)

        mel_transform = torchaudio.transforms.MelSpectrogram(
            sample_rate=sr,
            n_fft=n_fft,
            hop_length=hop_length,
            n_mels=n_mels,
            power=2.0,
        ).to(waveform.device)

        mel = mel_transform(waveform)  # (B, n_mels, T)

        # Log1p normalisation to [0, 1]
        mel = torch.log1p(mel)
        mel_max = mel.amax(dim=(-2, -1), keepdim=True).clamp(min=1e-8)
        mel = mel / mel_max

        return mel

    # ------------------------------------------------------------------
    # Waveform -> TeacherOutput
    # ------------------------------------------------------------------

    @torch.no_grad()
    def from_waveform(
        self,
        waveform: Tensor,
        sr: int = SAMPLE_RATE,
    ) -> TeacherOutput:
        """Generate labels from a raw waveform.

        Parameters
        ----------
        waveform : Tensor
            Shape ``(B, samples)`` or ``(samples,)`` raw audio at ``sr`` Hz.
        sr : int
            Sample rate (default 44100).

        Returns
        -------
        TeacherOutput
            Labels at every MI pipeline layer.
        """
        mel = self.waveform_to_mel(waveform, sr=sr)
        return self._teacher.compute(mel)

    # ------------------------------------------------------------------
    # Repr
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return f"LabelGenerator(teacher={self._teacher})"
