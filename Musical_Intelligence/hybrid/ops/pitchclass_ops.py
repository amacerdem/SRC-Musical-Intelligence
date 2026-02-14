"""
Pitch-class energy reweighting in STFT domain.

Changes the harmonic "feel" without full transcription:
  - Major/minor bias: boost/cut pitch classes associated with major vs. minor mode
  - Tension bias: boost dissonant intervals (tritone, minor 2nd), reduce stable tones

Implementation:
  1. Estimate key center from chroma
  2. Build 12-element gain vector g_pc from mode_bias and tension params
  3. Convert g_pc to STFT frequency mask (Gaussian combs across octaves)
  4. Apply to harmonic STFT magnitude (phase-preserving)
"""

from __future__ import annotations

import numpy as np
from Musical_Intelligence.hybrid.ops.stft_ops import SR, N_FFT

# ── Pitch-class intervals relative to key root ─────────────────────────

# Scale degree names (semitones above root)
#   0: root, 1: m2, 2: M2, 3: m3, 4: M3, 5: P4,
#   6: tritone, 7: P5, 8: m6, 9: M6, 10: m7, 11: M7

# Gains for mode bias (positive = major, negative = minor)
# These describe which pitch classes to boost/cut when shifting mode feel
MODE_BIAS_GAINS = {
    # Degree: (boost_when_major, boost_when_minor)
    # Relative to key root
    0: (0.0, 0.0),     # root: neutral
    1: (-0.3, 0.1),    # m2: avoid in major, slight in minor
    2: (0.1, 0.1),     # M2: neutral both
    3: (-0.4, 0.5),    # m3: KEY MINOR INDICATOR (boost minor, cut major)
    4: (0.5, -0.4),    # M3: KEY MAJOR INDICATOR (boost major, cut minor)
    5: (0.0, 0.0),     # P4: neutral
    6: (-0.2, 0.0),    # tritone: slight avoid major
    7: (0.1, 0.1),     # P5: always stable
    8: (-0.2, 0.3),    # m6: minor indicator
    9: (0.3, -0.2),    # M6: major indicator
    10: (-0.1, 0.2),   # m7: slight minor
    11: (0.2, -0.1),   # M7: slight major (leading tone)
}

# Gains for tension parameter
TENSION_GAINS = {
    0: -0.1,    # root: reduce when tense
    1: 0.3,     # m2: DISSONANT — boost for tension
    2: 0.0,     # M2: neutral
    3: 0.1,     # m3: slight tension
    4: -0.05,   # M3: slightly reduce (too bright for tension)
    5: 0.0,     # P4: neutral
    6: 0.4,     # tritone: MOST DISSONANT — big boost for tension
    7: -0.15,   # P5: reduce stability for tension
    8: 0.15,    # m6: moderate tension
    9: -0.05,   # M6: slight reduce
    10: 0.1,    # m7: moderate tension
    11: 0.0,    # M7: neutral
}


def build_pitchclass_gain(
    mode_bias: float = 0.0,
    tension: float = 0.0,
) -> np.ndarray:
    """
    Build 12-element gain vector for pitch-class reweighting.
    Gains are in dB, relative to root of the detected key.

    Args:
        mode_bias: -1 (minor) to +1 (major)
        tension:   0 (relaxed) to +1 (tense)

    Returns:
        g_pc: (12,) gain in dB per pitch class (relative to key root)
    """
    g_pc = np.zeros(12, dtype=np.float32)

    # Mode bias contribution
    if abs(mode_bias) > 0.01:
        for degree, (major_gain, minor_gain) in MODE_BIAS_GAINS.items():
            if mode_bias > 0:
                g_pc[degree] += mode_bias * major_gain
            else:
                g_pc[degree] += abs(mode_bias) * minor_gain

    # Tension contribution
    if abs(tension) > 0.01:
        for degree, t_gain in TENSION_GAINS.items():
            g_pc[degree] += tension * t_gain

    # Clamp to safe range: max ±4 dB per pitch class
    g_pc = np.clip(g_pc, -4.0, 4.0)

    return g_pc


def pitchclass_to_stft_mask(
    g_pc: np.ndarray,
    key_idx: int,
    n_fft: int = N_FFT,
    sr: int = SR,
    sigma_cents: float = 50.0,
) -> np.ndarray:
    """
    Convert pitch-class gains (dB) to STFT frequency bin mask (linear gain).

    Creates Gaussian combs around each pitch class's frequencies across
    all audible octaves, weighted by the gain vector.

    Args:
        g_pc:         (12,) gain in dB per pitch class (relative to key root)
        key_idx:      0-11 (C=0, C#=1, ...)
        n_fft:        FFT size
        sr:           Sample rate
        sigma_cents:  Gaussian width in cents (50 = moderate, 100 = wide)

    Returns:
        mask: (n_freq,) linear gain per frequency bin
    """
    n_freq = n_fft // 2 + 1
    mask = np.ones(n_freq, dtype=np.float32)
    freqs = np.arange(n_freq) * sr / n_fft  # Hz per bin

    # For each pitch class
    for degree in range(12):
        gain_db = g_pc[degree]
        if abs(gain_db) < 0.01:
            continue

        gain_linear = 10.0 ** (gain_db / 20.0) - 1.0  # deviation from unity
        # Actual pitch class index in chromatic scale
        pc = (key_idx + degree) % 12

        # Reference frequency for this pitch class (C0 ≈ 16.35 Hz)
        f_ref = 440.0 * 2.0 ** ((pc - 9) / 12.0)  # frequency of this PC at octave 4

        # Gaussian kernel around each octave of this pitch class
        for octave in range(-4, 5):  # octaves 0 through 8
            f_center = f_ref * (2.0 ** octave)
            if f_center < 30 or f_center > sr / 2:
                continue

            # Sigma in Hz (convert from cents)
            # 100 cents = 1 semitone, sigma_cents controls width
            sigma_hz = f_center * (2.0 ** (sigma_cents / 1200.0) - 1.0)
            sigma_bins = sigma_hz / (sr / n_fft)

            if sigma_bins < 0.1:
                continue

            # Gaussian kernel
            center_bin = f_center * n_fft / sr
            gaussian = np.exp(-0.5 * ((np.arange(n_freq) - center_bin) / sigma_bins) ** 2)

            # Add weighted contribution
            mask += gain_linear * gaussian

    # Clamp to safe range
    from Musical_Intelligence.hybrid.ops.stft_ops import clamp_gain
    mask = clamp_gain(mask)

    return mask


def apply_pitchclass_reweighting(
    S_harmonic: np.ndarray,
    key_idx: int,
    mode_bias: float = 0.0,
    tension: float = 0.0,
    strength: float = 1.0,
    n_fft: int = N_FFT,
    sr: int = SR,
    sigma_cents: float = 50.0,
) -> np.ndarray:
    """
    Apply pitch-class energy reweighting to harmonic STFT.
    Phase-preserving: only modifies magnitude.

    Args:
        S_harmonic:  Complex STFT of harmonic component (n_freq, n_frames)
        key_idx:     Detected key (0-11)
        mode_bias:   -1 (minor) to +1 (major)
        tension:     0 (relaxed) to +1 (tense)
        strength:    Overall effect strength (0-1)
        n_fft:       FFT size
        sr:          Sample rate
        sigma_cents: Gaussian width for pitch-class frequency matching

    Returns:
        S_modified: Modified harmonic STFT (phase-preserved)
    """
    if abs(mode_bias) < 0.01 and abs(tension) < 0.01:
        return S_harmonic

    # Build gain vector
    g_pc = build_pitchclass_gain(mode_bias, tension)

    # Scale by strength
    g_pc = g_pc * strength

    # Convert to STFT mask
    mask = pitchclass_to_stft_mask(g_pc, key_idx, n_fft, sr, sigma_cents)

    # Apply to magnitude, preserve phase
    mag = np.abs(S_harmonic)
    phase = np.angle(S_harmonic)
    mag_modified = mag * mask[:, np.newaxis]

    return (mag_modified * np.exp(1j * phase)).astype(np.complex64)


def compute_mode_correlation(
    chroma: np.ndarray,
    key_idx: int,
) -> tuple[float, float]:
    """
    Compute correlation of chroma with major and minor templates.
    Useful for measuring effect of mode_bias transform.

    Returns:
        major_corr: correlation with major template
        minor_corr: correlation with minor template
    """
    from Musical_Intelligence.hybrid.ops.structure_ops import MAJOR_TEMPLATE, MINOR_TEMPLATE

    chroma_mean = chroma.mean(axis=1)
    if chroma_mean.max() < 1e-6:
        return 0.0, 0.0

    chroma_mean = chroma_mean / (chroma_mean.max() + 1e-8)

    major_rotated = np.roll(MAJOR_TEMPLATE, key_idx)
    minor_rotated = np.roll(MINOR_TEMPLATE, key_idx)

    major_corr = float(np.corrcoef(chroma_mean, major_rotated)[0, 1])
    minor_corr = float(np.corrcoef(chroma_mean, minor_rotated)[0, 1])

    return major_corr, minor_corr
