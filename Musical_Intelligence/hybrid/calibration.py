"""
Closed-loop R³ feedback calibration.

Problem: A fixed-strength transform produces wildly different perceptual
results on different audio (a quiet piano vs. a loud orchestra).

Solution: Measure the R³ shift after each transform iteration and
auto-adjust strength until the target deltas are achieved.

Algorithm:
  1. Analyze original: R³(y_original)
  2. Set target: R³_target = R³_original + target_deltas
  3. Apply transform with initial strength
  4. Measure: R³(y_transformed)
  5. Compute error: how far from target
  6. Adjust strength proportionally
  7. Repeat 2-5 iterations (usually converges in 3)
"""

from __future__ import annotations

import numpy as np
import torch
from dataclasses import dataclass
from typing import Callable


@dataclass
class CalibrationResult:
    """Result of closed-loop calibration."""
    final_strength: float
    iterations: int
    r3_original: np.ndarray       # (T, 128)
    r3_transformed: np.ndarray    # (T, 128)
    r3_deltas_achieved: dict[int, float]  # idx → actual delta
    r3_deltas_target: dict[int, float]    # idx → target delta
    error_history: list[float]


def extract_r3_features(
    y: np.ndarray,
    sr: int = 44100,
    hop_length: int = 256,
    n_fft: int = 2048,
    n_mels: int = 128,
) -> np.ndarray:
    """
    Extract R³ features from a waveform.

    Returns:
        features: (T, 128) numpy array, values in [0, 1]
    """
    import torchaudio

    # Waveform → mel spectrogram
    y_tensor = torch.from_numpy(y).unsqueeze(0)  # (1, samples)
    mel_transform = torchaudio.transforms.MelSpectrogram(
        sample_rate=sr,
        n_fft=n_fft,
        hop_length=hop_length,
        n_mels=n_mels,
        power=2.0,
    )
    mel = mel_transform(y_tensor)  # (1, 128, T)

    # Log-scale and normalize to [0, 1]
    mel = torch.log1p(mel)
    mel_max = mel.max()
    if mel_max > 0:
        mel = mel / mel_max

    # Extract R³
    from Musical_Intelligence.ear.r3 import R3Extractor
    r3_ext = R3Extractor()
    audio_tensor = torch.from_numpy(y).float().unsqueeze(0)  # (1, N)
    r3_output = r3_ext.extract(mel, audio=audio_tensor, sr=sr)

    return r3_output.features[0].numpy()  # (T, 128)


def compute_r3_summary(features: np.ndarray) -> np.ndarray:
    """Compute mean R³ across time for stable comparison."""
    return features.mean(axis=0)  # (128,)


def compute_delta_error(
    r3_current: np.ndarray,
    r3_original: np.ndarray,
    target_deltas: dict[int, float],
) -> tuple[float, dict[int, float]]:
    """
    Compute how far the current R³ is from the target.

    Returns:
        total_error: Sum of squared errors across target dimensions
        achieved_deltas: Dict of actual deltas per target dimension
    """
    achieved = {}
    errors = []

    for idx, target_delta in target_deltas.items():
        actual_delta = float(r3_current[idx] - r3_original[idx])
        achieved[idx] = actual_delta
        error = (target_delta - actual_delta) ** 2
        errors.append(error)

    total_error = sum(errors) / (len(errors) + 1e-8)
    return total_error, achieved


def calibrate(
    y_original: np.ndarray,
    target_deltas: dict[int, float],
    transform_fn: Callable[[np.ndarray, float], np.ndarray],
    initial_strength: float = 0.5,
    max_iterations: int = 5,
    tolerance: float = 0.001,
    sr: int = 44100,
) -> tuple[np.ndarray, CalibrationResult]:
    """
    Closed-loop calibration: adjust transform strength until R³ targets are met.

    Args:
        y_original:       Original audio waveform
        target_deltas:    Dict mapping R³ index → desired delta
        transform_fn:     Function(y, strength) → y_transformed
        initial_strength: Starting strength (0-1)
        max_iterations:   Max calibration iterations
        tolerance:        Stop when error below this
        sr:               Sample rate

    Returns:
        y_final:   Calibrated transformed audio
        result:    CalibrationResult with diagnostics
    """
    if not target_deltas:
        r3_orig = extract_r3_features(y_original, sr=sr)
        return y_original, CalibrationResult(
            final_strength=0.0, iterations=0,
            r3_original=r3_orig, r3_transformed=r3_orig,
            r3_deltas_achieved={}, r3_deltas_target={},
            error_history=[0.0],
        )

    # Step 1: Analyze original
    r3_orig = extract_r3_features(y_original, sr=sr)
    r3_orig_summary = compute_r3_summary(r3_orig)

    strength = initial_strength
    error_history = []
    best_y = y_original
    best_error = float("inf")
    best_strength = strength

    for iteration in range(max_iterations):
        # Step 3: Transform
        y_transformed = transform_fn(y_original, strength)

        # Step 4: Measure
        r3_trans = extract_r3_features(y_transformed, sr=sr)
        r3_trans_summary = compute_r3_summary(r3_trans)

        # Step 5: Error
        error, achieved = compute_delta_error(
            r3_trans_summary, r3_orig_summary, target_deltas
        )
        error_history.append(error)

        if error < best_error:
            best_error = error
            best_y = y_transformed
            best_strength = strength

        if error < tolerance:
            break

        # Step 6: Adjust strength proportionally
        # If deltas are too small → increase strength
        # If deltas are too large → decrease strength
        scale_factors = []
        for idx, target_delta in target_deltas.items():
            actual_delta = achieved.get(idx, 0.0)
            if abs(actual_delta) > 1e-6 and abs(target_delta) > 1e-6:
                ratio = target_delta / actual_delta
                # Clamp ratio to avoid wild swings
                ratio = max(0.5, min(2.0, ratio))
                scale_factors.append(ratio)

        if scale_factors:
            avg_scale = np.mean(scale_factors)
            strength = max(0.05, min(1.0, strength * avg_scale))

    # Final measurement on best result
    r3_final = extract_r3_features(best_y, sr=sr)
    r3_final_summary = compute_r3_summary(r3_final)
    _, final_achieved = compute_delta_error(
        r3_final_summary, r3_orig_summary, target_deltas
    )

    return best_y, CalibrationResult(
        final_strength=best_strength,
        iterations=len(error_history),
        r3_original=r3_orig,
        r3_transformed=r3_final,
        r3_deltas_achieved=final_achieved,
        r3_deltas_target=target_deltas,
        error_history=error_history,
    )
