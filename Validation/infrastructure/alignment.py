"""Temporal alignment — resample MI frame rate to EEG/fMRI sampling rates."""
from __future__ import annotations

from typing import Optional, Tuple

import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import fftconvolve

from Validation.config.constants import FRAME_RATE


def resample_to_hz(
    features: np.ndarray,
    source_fps: float = FRAME_RATE,
    target_hz: float = 2.0,
) -> np.ndarray:
    """Resample MI features to a target sampling rate.

    Uses averaging for downsampling, interpolation for upsampling.

    Args:
        features: (T_src, D) or (T_src,) feature array.
        source_fps: Source frame rate (default: MI 172.27 Hz).
        target_hz: Target sampling frequency.

    Returns:
        Resampled array (T_target, D) or (T_target,).
    """
    is_1d = features.ndim == 1
    if is_1d:
        features = features[:, np.newaxis]

    T_src, D = features.shape
    duration_s = T_src / source_fps
    T_target = int(np.ceil(duration_s * target_hz))

    if T_target <= 0:
        return np.empty((0, D) if not is_1d else (0,))

    if target_hz < source_fps:
        # Downsample by averaging within windows
        result = np.zeros((T_target, D), dtype=features.dtype)
        for i in range(T_target):
            t_start = i / target_hz
            t_end = (i + 1) / target_hz
            frame_start = int(t_start * source_fps)
            frame_end = min(int(t_end * source_fps), T_src)
            if frame_start < frame_end:
                result[i] = features[frame_start:frame_end].mean(axis=0)
        resampled = result
    else:
        # Upsample by interpolation
        src_times = np.arange(T_src) / source_fps
        tgt_times = np.arange(T_target) / target_hz
        interp = interp1d(src_times, features, axis=0, kind="linear",
                          fill_value="extrapolate")
        resampled = interp(tgt_times)

    if is_1d:
        return resampled.squeeze(-1)
    return resampled


def resample_to_tr(
    features: np.ndarray,
    source_fps: float = FRAME_RATE,
    tr_seconds: float = 2.0,
) -> np.ndarray:
    """Downsample MI features to fMRI TR resolution.

    Averages MI frames within each TR window.

    Args:
        features: (T_src, D) feature array.
        source_fps: MI frame rate.
        tr_seconds: fMRI repetition time.

    Returns:
        (n_TRs, D) averaged features.
    """
    return resample_to_hz(features, source_fps, 1.0 / tr_seconds)


def resample_to_eeg(
    features: np.ndarray,
    source_fps: float = FRAME_RATE,
    eeg_sfreq: float = 128.0,
) -> np.ndarray:
    """Resample MI features to match EEG sampling frequency.

    Args:
        features: (T_src, D) feature array.
        source_fps: MI frame rate.
        eeg_sfreq: EEG sampling frequency.

    Returns:
        (T_eeg, D) resampled features.
    """
    return resample_to_hz(features, source_fps, eeg_sfreq)


def apply_hrf(
    features: np.ndarray,
    tr: float = 2.0,
    hrf_length: float = 32.0,
) -> np.ndarray:
    """Convolve MI features with canonical HRF for fMRI comparison.

    Uses the SPM double-gamma HRF.

    Args:
        features: (T, D) feature array at TR resolution.
        tr: Repetition time in seconds.
        hrf_length: HRF duration in seconds.

    Returns:
        (T, D) HRF-convolved features.
    """
    hrf = _spm_hrf(tr, hrf_length)

    if features.ndim == 1:
        return fftconvolve(features, hrf, mode="full")[:len(features)]

    T, D = features.shape
    result = np.zeros_like(features)
    for d in range(D):
        conv = fftconvolve(features[:, d], hrf, mode="full")
        result[:, d] = conv[:T]
    return result


def time_lag_correlation(
    signal_a: np.ndarray,
    signal_b: np.ndarray,
    max_lag_s: float = 10.0,
    fps: float = FRAME_RATE,
) -> Tuple[float, float, np.ndarray]:
    """Compute correlation at multiple time lags.

    Args:
        signal_a: First signal (T,).
        signal_b: Second signal (T,).
        max_lag_s: Maximum lag in seconds.
        fps: Sampling rate of both signals.

    Returns:
        Tuple of (optimal_lag_s, max_correlation, lag_correlation_array).
    """
    max_lag_frames = int(max_lag_s * fps)
    n = min(len(signal_a), len(signal_b))

    # Normalize
    a = (signal_a[:n] - signal_a[:n].mean()) / (signal_a[:n].std() + 1e-10)
    b = (signal_b[:n] - signal_b[:n].mean()) / (signal_b[:n].std() + 1e-10)

    lags = np.arange(-max_lag_frames, max_lag_frames + 1)
    correlations = np.zeros(len(lags))

    for i, lag in enumerate(lags):
        if lag >= 0:
            correlations[i] = np.mean(a[lag:] * b[:n - lag]) if lag < n else 0
        else:
            correlations[i] = np.mean(a[:n + lag] * b[-lag:]) if -lag < n else 0

    best_idx = np.argmax(np.abs(correlations))
    optimal_lag_s = lags[best_idx] / fps
    max_corr = correlations[best_idx]

    return optimal_lag_s, max_corr, correlations


def _spm_hrf(
    tr: float,
    length: float = 32.0,
) -> np.ndarray:
    """SPM canonical double-gamma HRF.

    Args:
        tr: Repetition time.
        length: HRF duration in seconds.

    Returns:
        HRF samples at TR resolution.
    """
    from scipy.stats import gamma as gamma_dist

    dt = tr
    t = np.arange(0, length, dt)

    # Double gamma parameters (SPM defaults)
    a1, b1 = 6.0, 1.0   # peak at 6s
    a2, b2 = 16.0, 1.0   # undershoot at 16s
    c = 1.0 / 6.0        # ratio of undershoot

    h = gamma_dist.pdf(t, a1, scale=b1) - c * gamma_dist.pdf(t, a2, scale=b2)

    # Normalize
    h = h / h.sum()
    return h
