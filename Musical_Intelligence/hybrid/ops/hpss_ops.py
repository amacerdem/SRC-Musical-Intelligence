"""
Harmonic-Percussive Source Separation (HPSS).

Separates audio into harmonic (pitched) and percussive (transient) components
so transforms can target each independently:
  - Valence/Warmth/Brightness → operate on harmonic
  - Arousal/Intensity         → operate on percussive + transients

Without this separation, every transform feels like "just a filter."
"""

from __future__ import annotations

import numpy as np
from Musical_Intelligence.hybrid.ops.stft_ops import (
    SR, N_FFT, HOP_LENGTH,
    stft_analyze, stft_synthesize,
)


def hpss_stft(
    S_complex: np.ndarray,
    kernel_size: int = 31,
    margin: float = 1.0,
) -> tuple[np.ndarray, np.ndarray]:
    """
    HPSS on complex STFT using median filtering (Fitzgerald 2010).

    Args:
        S_complex: Complex STFT (n_freq, n_frames)
        kernel_size: Median filter window (odd integer)
        margin: Separation margin (1.0 = standard, >1.0 = harder separation)

    Returns:
        S_harmonic:  Complex STFT of harmonic component
        S_percussive: Complex STFT of percussive component
    """
    from scipy.ndimage import median_filter

    mag = np.abs(S_complex)
    phase = np.angle(S_complex)

    # Median filter along time axis → captures harmonic (steady) content
    H = median_filter(mag, size=(1, kernel_size))
    # Median filter along frequency axis → captures percussive (broadband) content
    P = median_filter(mag, size=(kernel_size, 1))

    # Soft masks (Wiener-like)
    H_margin = H ** (2 * margin)
    P_margin = P ** (2 * margin)
    total = H_margin + P_margin + 1e-10

    mask_h = H_margin / total
    mask_p = P_margin / total

    S_harmonic = (mag * mask_h) * np.exp(1j * phase)
    S_percussive = (mag * mask_p) * np.exp(1j * phase)

    return S_harmonic.astype(np.complex64), S_percussive.astype(np.complex64)


def hpss_split(
    y: np.ndarray,
    kernel_size: int = 31,
    margin: float = 1.0,
    n_fft: int = N_FFT,
    hop_length: int = HOP_LENGTH,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Split audio into harmonic, percussive, and residual components.

    Returns:
        y_harmonic:   Harmonic (pitched/tonal) component
        y_percussive: Percussive (transient/noise) component
        y_residual:   Residual (what neither filter captures)
    """
    import librosa

    S = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
    S_h, S_p = hpss_stft(S, kernel_size=kernel_size, margin=margin)

    y_h = librosa.istft(S_h, hop_length=hop_length, length=len(y))
    y_p = librosa.istft(S_p, hop_length=hop_length, length=len(y))
    y_r = y - y_h - y_p

    return y_h.astype(np.float32), y_p.astype(np.float32), y_r.astype(np.float32)


def hpss_recombine(
    y_harmonic: np.ndarray,
    y_percussive: np.ndarray,
    y_residual: np.ndarray | None = None,
) -> np.ndarray:
    """Recombine HPSS components into final audio."""
    y = y_harmonic + y_percussive
    if y_residual is not None:
        y = y + y_residual
    return y.astype(np.float32)


def apply_spectral_transform_harmonic(
    S_harmonic: np.ndarray,
    gain_curve: np.ndarray,
    strength: float = 1.0,
) -> np.ndarray:
    """
    Apply frequency-domain gain to harmonic STFT only.
    Preserves phase; only modifies magnitude.

    Args:
        S_harmonic: Complex STFT of harmonic component (n_freq, n_frames)
        gain_curve: (n_freq,) linear gain per frequency bin
        strength:   0.0 = no change, 1.0 = full effect
    """
    from Musical_Intelligence.hybrid.ops.stft_ops import clamp_gain

    mag = np.abs(S_harmonic)
    phase = np.angle(S_harmonic)

    effective_gain = 1.0 + strength * (gain_curve - 1.0)
    effective_gain = clamp_gain(effective_gain)

    mag_modified = mag * effective_gain[:, np.newaxis]
    return (mag_modified * np.exp(1j * phase)).astype(np.complex64)
