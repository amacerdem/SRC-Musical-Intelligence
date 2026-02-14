"""
Harmonic density augmentation operators.

The cheapest way to achieve "composition changed" feeling WITHOUT
rewriting the composition: add pitch-shifted doublings of the
harmonic component at very low mix levels.

  Valence ↑:  +12 semitones (octave) + +7 semitones (fifth) → brighter, open
  Tension ↑:  +3 semitones (minor 3rd) + slight detune chorus → dark, tense
  Warmth ↑:   -12 semitones (sub-octave) at low mix → body, depth

CRITICAL: Apply ONLY to the harmonic component from HPSS.
          Applying to full signal → mud.
"""

from __future__ import annotations

import numpy as np
from Musical_Intelligence.hybrid.ops.stft_ops import SR, N_FFT, HOP_LENGTH


def pitch_shift_stft(
    S_harmonic: np.ndarray,
    n_steps: float,
    hop_length: int = HOP_LENGTH,
) -> np.ndarray:
    """
    Pitch-shift a harmonic STFT component by n_steps semitones.
    Uses librosa's phase vocoder for quality.

    Args:
        S_harmonic: Complex STFT (n_freq, n_frames) of harmonic component
        n_steps:    Semitones to shift (positive = up, negative = down)
        hop_length: STFT hop length

    Returns:
        S_shifted: Complex STFT of pitch-shifted harmonic
    """
    import librosa

    # Phase vocoder time-stretch, then resample to original length
    rate = 2.0 ** (-n_steps / 12.0)

    # Time-stretch via phase vocoder (changes speed, preserves pitch)
    S_stretched = librosa.phase_vocoder(S_harmonic, rate=rate, hop_length=hop_length)

    # Resample to original number of frames
    n_frames_orig = S_harmonic.shape[1]
    n_frames_new = S_stretched.shape[1]

    if n_frames_new == n_frames_orig:
        return S_stretched

    # Interpolate magnitude and phase separately to match original length
    from scipy.interpolate import interp1d

    mag = np.abs(S_stretched)
    phase = np.angle(S_stretched)

    x_new = np.linspace(0, 1, n_frames_new)
    x_orig = np.linspace(0, 1, n_frames_orig)

    mag_interp = interp1d(x_new, mag, axis=1, kind="linear", fill_value="extrapolate")(x_orig)
    phase_interp = interp1d(x_new, phase, axis=1, kind="linear", fill_value="extrapolate")(x_orig)

    return (mag_interp * np.exp(1j * phase_interp)).astype(np.complex64)


def pitch_shift_waveform(
    y_harmonic: np.ndarray,
    n_steps: float,
    sr: int = SR,
) -> np.ndarray:
    """
    Pitch-shift a harmonic waveform by n_steps semitones.

    Args:
        y_harmonic: Harmonic component waveform
        n_steps:    Semitones to shift
        sr:         Sample rate

    Returns:
        y_shifted: Pitch-shifted waveform (same length)
    """
    import librosa
    return librosa.effects.pitch_shift(
        y_harmonic, sr=sr, n_steps=n_steps
    ).astype(np.float32)


# ── Preset interval recipes ───────────────────────────────────────────

# Each recipe: list of (semitones, mix_level) pairs
HARMONIC_RECIPES = {
    # Valence ↑: bright, open (octave + fifth)
    "bright": [(12, 0.04), (7, 0.03)],

    # Valence ↓ / Tension ↑: dark, tense (minor 3rd + detune)
    "dark": [(3, 0.03), (0.15, 0.02)],  # 0.15 semitones = ~9 cent detune

    # Warmth ↑: body, depth (sub-octave)
    "warm": [(-12, 0.04)],

    # Tension ↑: dissonant intervals (tritone + minor 2nd)
    "tense": [(6, 0.02), (1, 0.015)],

    # Calm / Consonant: perfect intervals only (octave)
    "consonant": [(12, 0.03)],
}


def add_harmonic_doubles(
    y_harmonic: np.ndarray,
    recipe: str | list[tuple[float, float]] = "bright",
    strength: float = 1.0,
    sr: int = SR,
) -> np.ndarray:
    """
    Add pitch-shifted doublings to the harmonic component.

    Args:
        y_harmonic: Harmonic waveform from HPSS
        recipe:     Name from HARMONIC_RECIPES or list of (semitones, mix_level)
        strength:   Scales all mix levels (0.0 = no doubles, 1.0 = full recipe)
        sr:         Sample rate

    Returns:
        y_enriched: Harmonic component with added doublings
    """
    if isinstance(recipe, str):
        intervals = HARMONIC_RECIPES.get(recipe, HARMONIC_RECIPES["bright"])
    else:
        intervals = recipe

    y_enriched = y_harmonic.copy()

    for n_steps, mix_level in intervals:
        effective_mix = mix_level * strength
        if effective_mix < 0.001:
            continue  # Skip negligible contributions

        y_shifted = pitch_shift_waveform(y_harmonic, n_steps=n_steps, sr=sr)

        # Trim to same length (pitch shifting can change length slightly)
        n = min(len(y_enriched), len(y_shifted))
        y_enriched[:n] += effective_mix * y_shifted[:n]

    return y_enriched.astype(np.float32)


def add_harmonic_doubles_stft(
    S_harmonic: np.ndarray,
    recipe: str | list[tuple[float, float]] = "bright",
    strength: float = 1.0,
    hop_length: int = HOP_LENGTH,
) -> np.ndarray:
    """
    Add pitch-shifted doublings in STFT domain (phase-preserving).

    Args:
        S_harmonic: Complex STFT of harmonic component
        recipe:     Name from HARMONIC_RECIPES or list of (semitones, mix_level)
        strength:   Scales all mix levels
        hop_length: STFT hop length

    Returns:
        S_enriched: STFT with added harmonic doublings
    """
    if isinstance(recipe, str):
        intervals = HARMONIC_RECIPES.get(recipe, HARMONIC_RECIPES["bright"])
    else:
        intervals = recipe

    S_enriched = S_harmonic.copy()

    for n_steps, mix_level in intervals:
        effective_mix = mix_level * strength
        if effective_mix < 0.001:
            continue

        S_shifted = pitch_shift_stft(S_harmonic, n_steps=n_steps, hop_length=hop_length)

        # Ensure same shape
        n_frames = min(S_enriched.shape[1], S_shifted.shape[1])
        S_enriched[:, :n_frames] += effective_mix * S_shifted[:, :n_frames]

    return S_enriched.astype(np.complex64)
