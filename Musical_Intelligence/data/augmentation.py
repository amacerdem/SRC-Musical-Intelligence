"""Audio augmentation for MI training data.

Provides augmentation transforms that operate on mel spectrograms
and raw waveforms. Used during training for regularisation.

Available augmentations:
- SpecAugment (time/frequency masking on mel)
- Time stretching (via waveform resampling)
- Gaussian noise injection
- Random gain scaling
"""
from __future__ import annotations

from typing import Optional

import torch
from torch import Tensor


class SpecAugment:
    """SpecAugment: frequency and time masking on mel spectrograms.

    Reference: Park et al. (2019) "SpecAugment".

    Parameters
    ----------
    freq_mask_param : int
        Maximum number of frequency bands to mask.
    time_mask_param : int
        Maximum number of time frames to mask.
    n_freq_masks : int
        Number of frequency masks to apply.
    n_time_masks : int
        Number of time masks to apply.
    """

    def __init__(
        self,
        freq_mask_param: int = 20,
        time_mask_param: int = 50,
        n_freq_masks: int = 2,
        n_time_masks: int = 2,
    ) -> None:
        self._freq_mask_param = freq_mask_param
        self._time_mask_param = time_mask_param
        self._n_freq_masks = n_freq_masks
        self._n_time_masks = n_time_masks

    def __call__(self, mel: Tensor) -> Tensor:
        """Apply SpecAugment to mel spectrogram.

        Parameters
        ----------
        mel : Tensor
            Shape ``(B, n_mels, T)`` or ``(n_mels, T)``.

        Returns
        -------
        Tensor
            Augmented mel with same shape.
        """
        was_2d = mel.dim() == 2
        if was_2d:
            mel = mel.unsqueeze(0)

        mel = mel.clone()
        B, F, T = mel.shape

        for _ in range(self._n_freq_masks):
            f = torch.randint(0, self._freq_mask_param + 1, (1,)).item()
            f0 = torch.randint(0, max(1, F - f), (1,)).item()
            mel[:, f0 : f0 + f, :] = 0.0

        for _ in range(self._n_time_masks):
            t = torch.randint(0, self._time_mask_param + 1, (1,)).item()
            t0 = torch.randint(0, max(1, T - t), (1,)).item()
            mel[:, :, t0 : t0 + t] = 0.0

        if was_2d:
            mel = mel.squeeze(0)
        return mel


class GaussianNoise:
    """Add Gaussian noise to a tensor.

    Parameters
    ----------
    std : float
        Standard deviation of the noise (default 0.01).
    """

    def __init__(self, std: float = 0.01) -> None:
        self._std = std

    def __call__(self, x: Tensor) -> Tensor:
        """Add Gaussian noise, clamping result to [0, 1]."""
        noise = torch.randn_like(x) * self._std
        return (x + noise).clamp(0.0, 1.0)


class RandomGain:
    """Randomly scale amplitude by a factor in [min_gain, max_gain].

    Parameters
    ----------
    min_gain : float
        Minimum gain factor (default 0.8).
    max_gain : float
        Maximum gain factor (default 1.2).
    """

    def __init__(self, min_gain: float = 0.8, max_gain: float = 1.2) -> None:
        self._min_gain = min_gain
        self._max_gain = max_gain

    def __call__(self, x: Tensor) -> Tensor:
        """Apply random gain, clamping result to [0, 1]."""
        gain = torch.empty(1, device=x.device).uniform_(
            self._min_gain, self._max_gain
        )
        return (x * gain).clamp(0.0, 1.0)


class MIAugmentationPipeline:
    """Composite augmentation pipeline for MI training.

    Applies SpecAugment on mel input, and optional noise/gain
    augmentations on feature-level tensors.

    Parameters
    ----------
    enable_spec_augment : bool
        Apply SpecAugment to mel (default True).
    enable_noise : bool
        Apply Gaussian noise to features (default False).
    enable_gain : bool
        Apply random gain to mel (default False).
    """

    def __init__(
        self,
        enable_spec_augment: bool = True,
        enable_noise: bool = False,
        enable_gain: bool = False,
        noise_std: float = 0.005,
    ) -> None:
        self._spec_augment = SpecAugment() if enable_spec_augment else None
        self._noise = GaussianNoise(std=noise_std) if enable_noise else None
        self._gain = RandomGain() if enable_gain else None

    def augment_mel(self, mel: Tensor) -> Tensor:
        """Augment mel spectrogram (B, 128, T)."""
        if self._gain is not None:
            mel = self._gain(mel)
        if self._spec_augment is not None:
            mel = self._spec_augment(mel)
        return mel

    def augment_features(self, features: Tensor) -> Tensor:
        """Augment feature tensor (B, T, D) with noise."""
        if self._noise is not None:
            features = self._noise(features)
        return features
