"""
Transient shaping operators.

Unlike EQ (which just colors the spectrum), transient shaping modifies the
*temporal envelope* of sounds — making attacks sharper or softer. This is
what makes a transform feel like "the performance changed" rather than
"someone added a filter."

Modes:
  - intense: Boost transient regions (sharper attacks, more punch)
  - calm:    Soften transient regions (gentler attacks, longer sustain)
"""

from __future__ import annotations

import numpy as np
from Musical_Intelligence.hybrid.ops.stft_ops import (
    SR, N_FFT, HOP_LENGTH,
    temporal_smooth, clamp_gain,
)


def compute_onset_envelope(
    mag: np.ndarray,
    hop_length: int = HOP_LENGTH,
    sr: int = SR,
) -> np.ndarray:
    """
    Compute onset strength envelope from magnitude spectrogram.
    Uses half-wave rectified spectral flux (same method as R³ Group B).

    Args:
        mag: (n_freq, n_frames) magnitude spectrogram

    Returns:
        onset_env: (n_frames,) normalized onset envelope in [0, 1]
    """
    # Spectral flux: positive differences across frames
    diff = np.diff(mag, axis=1)
    flux = np.maximum(diff, 0).sum(axis=0)  # (n_frames - 1,)

    # Pad first frame
    onset_env = np.zeros(mag.shape[1], dtype=np.float32)
    onset_env[1:] = flux

    # Normalize to [0, 1]
    peak = onset_env.max()
    if peak > 0:
        onset_env = onset_env / peak

    return onset_env


def make_transient_envelope(
    onset_env: np.ndarray,
    mode: str,
    strength: float = 0.5,
    attack_frames: int = 3,
    sustain_frames: int = 8,
) -> np.ndarray:
    """
    Create a per-frame gain envelope based on transient positions.

    Args:
        onset_env:     (n_frames,) normalized onset envelope
        mode:          'intense' or 'calm'
        strength:      0.0 = no change, 1.0 = maximum effect
        attack_frames: Width of transient attack region (frames)
        sustain_frames: Width of sustain region after transient

    Returns:
        envelope: (n_frames,) multiplicative gain per frame
    """
    n_frames = len(onset_env)
    envelope = np.ones(n_frames, dtype=np.float32)

    # Find transient peaks (frames where onset > threshold)
    threshold = 0.3  # relative to max
    peaks = np.where(onset_env > threshold)[0]

    if len(peaks) == 0:
        return envelope

    if mode == "intense":
        # Boost around transients, slight compression elsewhere
        for peak_idx in peaks:
            weight = onset_env[peak_idx]
            # Attack boost region
            start = max(0, peak_idx - 1)
            end = min(n_frames, peak_idx + attack_frames)
            boost = 1.0 + strength * 0.8 * weight  # up to +80% at max strength
            envelope[start:end] = np.maximum(envelope[start:end], boost)

        # Gentle compression of non-transient regions
        non_transient_mask = onset_env < threshold * 0.5
        envelope[non_transient_mask] *= (1.0 - strength * 0.15)  # slight reduction

    elif mode == "calm":
        # Soften transients, extend sustain
        for peak_idx in peaks:
            weight = onset_env[peak_idx]
            # Soften attack
            start = max(0, peak_idx - 1)
            end = min(n_frames, peak_idx + attack_frames)
            reduction = 1.0 - strength * 0.5 * weight  # up to -50% at max strength
            envelope[start:end] = np.minimum(envelope[start:end], reduction)

            # Extend sustain (boost region after transient)
            sus_start = min(n_frames, peak_idx + attack_frames)
            sus_end = min(n_frames, peak_idx + attack_frames + sustain_frames)
            if sus_start < sus_end:
                # Gradual sustain boost
                sus_len = sus_end - sus_start
                sus_curve = np.linspace(1.0 + strength * 0.3, 1.0, sus_len)
                envelope[sus_start:sus_end] = np.maximum(
                    envelope[sus_start:sus_end], sus_curve
                )

    # Safety clamp
    envelope = clamp_gain(envelope)
    # Smooth to avoid clicks
    envelope = temporal_smooth(envelope, kernel_size=3)

    return envelope


def apply_transient_shaping(
    mag: np.ndarray,
    mode: str = "intense",
    strength: float = 0.5,
) -> np.ndarray:
    """
    Shape transients in a magnitude spectrogram.

    Args:
        mag:      (n_freq, n_frames) magnitude spectrogram
        mode:     'intense' or 'calm'
        strength: 0.0 = no change, 1.0 = maximum effect

    Returns:
        mag_shaped: Modified magnitude spectrogram
    """
    onset_env = compute_onset_envelope(mag)
    envelope = make_transient_envelope(onset_env, mode=mode, strength=strength)
    # Apply per-frame gain (broadcast over frequency bins)
    return mag * envelope[np.newaxis, :]


def apply_transient_shaping_stft(
    S: np.ndarray,
    mode: str = "intense",
    strength: float = 0.5,
) -> np.ndarray:
    """
    Apply transient shaping to complex STFT (preserves phase).

    Args:
        S:        Complex STFT (n_freq, n_frames)
        mode:     'intense' or 'calm'
        strength: 0.0 = no change, 1.0 = maximum effect

    Returns:
        S_shaped: Modified complex STFT
    """
    mag = np.abs(S)
    phase = np.angle(S)
    mag_shaped = apply_transient_shaping(mag, mode=mode, strength=strength)
    return (mag_shaped * np.exp(1j * phase)).astype(np.complex64)
