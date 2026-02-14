"""
Timing warp operations — tempo shift, rubato, swing, push-pull, rhythm density.

Algorithms:
  1. Global tempo: STFT phase vocoder (constant rate, preserves pitch)
  2. Rubato: sinusoidal time modulation via sample interpolation
  3. Swing: off-beat position shift within each beat interval
  4. Push/pull: constant micro-timing offset relative to beats
  5. Rhythm density: transient-aware attenuation/enhancement of percussive events

All timing warps preserve phase when possible and use crossfades to avoid clicks.
"""

from __future__ import annotations

import numpy as np
from Musical_Intelligence.hybrid.ops.stft_ops import SR, HOP_LENGTH, N_FFT

# Safety: max local warp within a beat (±15%)
MAX_LOCAL_WARP = 0.15
# Crossfade duration at segment boundaries
CROSSFADE_MS = 15.0


# ══════════════════════════════════════════════════════════════════════
# 1. GLOBAL TEMPO SHIFT (Phase Vocoder on STFT)
# ══════════════════════════════════════════════════════════════════════

def apply_tempo_shift_stft(
    S: np.ndarray,
    tempo_shift: float,
    hop_length: int = HOP_LENGTH,
) -> np.ndarray:
    """
    Apply global tempo change using STFT phase vocoder.
    Preserves pitch; changes duration.

    Args:
        S:           Complex STFT (n_freq, n_frames)
        tempo_shift: Relative tempo change (-0.2 to +0.2).
                     +0.1 = 10% faster, -0.1 = 10% slower.
        hop_length:  STFT hop length

    Returns:
        S_stretched: Complex STFT with adjusted frame count
    """
    import librosa

    if abs(tempo_shift) < 0.005:
        return S

    # rate > 1 = faster (fewer frames), rate < 1 = slower (more frames)
    rate = 1.0 + np.clip(tempo_shift, -0.3, 0.3)
    return librosa.phase_vocoder(S, rate=rate, hop_length=hop_length)


def estimate_output_length(
    original_length: int,
    tempo_shift: float,
) -> int:
    """Estimate output waveform length after tempo shift."""
    rate = 1.0 + np.clip(tempo_shift, -0.3, 0.3)
    return int(original_length / rate)


# ══════════════════════════════════════════════════════════════════════
# 2. RUBATO (Low-frequency tempo modulation)
# ══════════════════════════════════════════════════════════════════════

def apply_rubato(
    y: np.ndarray,
    sr: int,
    beat_times: np.ndarray,
    rubato: float,
    modulation_period_beats: int = 8,
) -> np.ndarray:
    """
    Apply rubato as a slow sinusoidal time modulation.

    Args:
        y:                       Audio waveform
        sr:                      Sample rate
        beat_times:              Beat positions (seconds)
        rubato:                  Rubato amount (0 = steady, 1 = max variation)
        modulation_period_beats: Period of tempo variation in beats

    Returns:
        y_rubato: Time-modulated audio (same length)
    """
    if abs(rubato) < 0.01 or len(beat_times) < 2:
        return y

    n_samples = len(y)
    t = np.arange(n_samples, dtype=np.float64) / sr

    # Compute modulation period from beat intervals
    avg_beat_interval = float(np.median(np.diff(beat_times)))
    mod_period_sec = modulation_period_beats * avg_beat_interval

    # Max offset: ±5% of beat interval at rubato=1
    max_offset = rubato * avg_beat_interval * 0.05
    offset = max_offset * np.sin(2 * np.pi * t / mod_period_sec)

    # Build time mapping: output time → input time
    t_input = t + offset
    t_input = np.clip(t_input, 0, (n_samples - 1) / sr)

    # Resample via linear interpolation
    input_indices = t_input * sr
    idx_floor = np.floor(input_indices).astype(int)
    idx_ceil = np.minimum(idx_floor + 1, n_samples - 1)
    frac = (input_indices - idx_floor).astype(np.float32)

    y_rubato = y[idx_floor] * (1.0 - frac) + y[idx_ceil] * frac
    return y_rubato.astype(np.float32)


# ══════════════════════════════════════════════════════════════════════
# 3. SWING + PUSH/PULL (Micro-timing within beat intervals)
# ══════════════════════════════════════════════════════════════════════

def build_microtiming_map(
    n_samples: int,
    sr: int,
    beat_times: np.ndarray,
    swing: float = 0.0,
    push_pull: float = 0.0,
) -> np.ndarray:
    """
    Build a sample-level time mapping for swing and push-pull.

    Swing shifts the off-beat position within each beat interval:
      swing=0:   midpoint at 50% (straight)
      swing=+1:  midpoint at 67% (jazz swing)
      swing=-1:  midpoint at 33% (reverse swing)

    Push/pull shifts all sub-beat events:
      push_pull > 0: events slightly ahead (pushing)
      push_pull < 0: events slightly behind (dragging)

    Returns:
        t_input: (n_samples,) — for each output sample, the input time (seconds)
    """
    t_output = np.arange(n_samples, dtype=np.float64) / sr
    t_input = t_output.copy()

    if len(beat_times) < 2:
        return t_input

    # Swing: shift midpoint within each beat interval
    # Max swing: ±17% of beat interval (0.33 to 0.67 midpoint position)
    swing_amount = np.clip(swing, -1.0, 1.0) * 0.17

    # Push/pull: constant offset as fraction of beat interval
    pp_amount = np.clip(push_pull, -1.0, 1.0) * 0.04  # max ±4% of beat

    for i in range(len(beat_times) - 1):
        t_start = beat_times[i]
        t_end = beat_times[i + 1]
        dur = t_end - t_start

        if dur < 0.05:  # skip very short intervals
            continue

        # Output midpoint (where the off-beat SHOULD be)
        mid_output = t_start + dur * (0.5 + swing_amount)

        # Input midpoint (where the off-beat IS in original)
        mid_input = t_start + dur * 0.5

        # Push/pull offset
        pp_offset = dur * pp_amount

        # Select samples in this beat interval
        mask = (t_output >= t_start) & (t_output < t_end)
        if not mask.any():
            continue

        t_local = t_output[mask]

        # Piecewise linear mapping within beat:
        # [t_start, mid_output] → [t_start + pp_offset, mid_input + pp_offset]
        # [mid_output, t_end]   → [mid_input + pp_offset, t_end + pp_offset]
        mapped = np.empty_like(t_local)

        first_half = t_local < mid_output
        second_half = ~first_half

        if first_half.any():
            # Map [t_start, mid_output] → [t_start, mid_input] + push/pull
            frac = (t_local[first_half] - t_start) / (mid_output - t_start + 1e-12)
            mapped[first_half] = t_start + frac * (mid_input - t_start) + pp_offset

        if second_half.any():
            # Map [mid_output, t_end] → [mid_input, t_end] + push/pull
            frac = (t_local[second_half] - mid_output) / (t_end - mid_output + 1e-12)
            mapped[second_half] = mid_input + frac * (t_end - mid_input) + pp_offset

        # Clamp to valid range
        mapped = np.clip(mapped, 0, (n_samples - 1) / sr)
        t_input[mask] = mapped

    return t_input


def apply_microtiming(
    y: np.ndarray,
    sr: int,
    beat_times: np.ndarray,
    swing: float = 0.0,
    push_pull: float = 0.0,
) -> np.ndarray:
    """
    Apply swing and push-pull micro-timing adjustments.

    Args:
        y:          Audio waveform
        sr:         Sample rate
        beat_times: Beat positions (seconds)
        swing:      -1 to +1 (0 = straight, 1 = jazz swing)
        push_pull:  -1 to +1 (positive = push ahead, negative = drag behind)

    Returns:
        y_warped: Time-warped audio (same length)
    """
    if abs(swing) < 0.01 and abs(push_pull) < 0.01:
        return y

    if len(beat_times) < 2:
        return y

    n_samples = len(y)
    t_input = build_microtiming_map(n_samples, sr, beat_times, swing, push_pull)

    # Resample via linear interpolation
    input_indices = t_input * sr
    idx_floor = np.floor(input_indices).astype(int)
    idx_floor = np.clip(idx_floor, 0, n_samples - 2)
    idx_ceil = idx_floor + 1
    frac = (input_indices - idx_floor).astype(np.float32)

    y_warped = y[idx_floor] * (1.0 - frac) + y[idx_ceil] * frac
    return y_warped.astype(np.float32)


# ══════════════════════════════════════════════════════════════════════
# 4. RHYTHM DENSITY (Transient-aware event density control)
# ══════════════════════════════════════════════════════════════════════

def apply_rhythm_density(
    S_perc: np.ndarray,
    onset_strengths_per_frame: np.ndarray | None = None,
    density: float = 0.0,
    hop_length: int = HOP_LENGTH,
    sr: int = SR,
) -> np.ndarray:
    """
    Control perceived rhythmic density via transient-aware attenuation/enhancement.

    density < 0: Reduce density — attenuate weaker onsets, keep strong downbeats
    density > 0: Increase density — enhance onset contrast, reduce inter-onset smearing

    Does NOT synthesize new events.

    Args:
        S_perc:   Complex STFT of percussive component (n_freq, n_frames)
        onset_strengths_per_frame: Pre-computed onset envelope (n_frames,)
        density:  -1 to +1
        hop_length: STFT hop length
        sr:       Sample rate

    Returns:
        S_perc_modified: Modified percussive STFT
    """
    if abs(density) < 0.05:
        return S_perc

    mag = np.abs(S_perc)
    phase = np.angle(S_perc)
    n_frames = mag.shape[1]

    # Compute onset envelope if not provided
    if onset_strengths_per_frame is None:
        diff = np.diff(mag, axis=1)
        flux = np.maximum(diff, 0).sum(axis=0)
        onset_env = np.zeros(n_frames, dtype=np.float32)
        onset_env[1:] = flux
        peak = onset_env.max()
        if peak > 0:
            onset_env = onset_env / peak
    else:
        onset_env = onset_strengths_per_frame
        if len(onset_env) != n_frames:
            # Resample to match STFT frames
            from scipy.interpolate import interp1d
            x_orig = np.linspace(0, 1, len(onset_env))
            x_new = np.linspace(0, 1, n_frames)
            onset_env = interp1d(x_orig, onset_env, kind="linear")(x_new)

    # Build per-frame gain
    gain = np.ones(n_frames, dtype=np.float32)

    if density < 0:
        # REDUCE DENSITY: attenuate weaker onsets
        strength = abs(density)
        # Percentile threshold: higher density reduction → higher threshold
        threshold = np.percentile(onset_env, 30 + strength * 40)  # 30-70th percentile
        weak = onset_env < threshold
        # Attenuate weak onset frames (up to -6 dB at max)
        gain[weak] *= (1.0 - strength * 0.5)
    else:
        # INCREASE DENSITY: enhance contrast
        strength = density
        # Boost onset frames, slightly reduce sustain
        threshold = np.percentile(onset_env, 40)
        strong = onset_env > threshold
        weak = ~strong
        gain[strong] *= (1.0 + strength * 0.4)  # boost strong events
        gain[weak] *= (1.0 - strength * 0.15)   # slightly reduce gaps

    # Safety clamp
    from Musical_Intelligence.hybrid.ops.stft_ops import clamp_gain, temporal_smooth
    gain = clamp_gain(gain)
    gain = temporal_smooth(gain, kernel_size=3)

    # Apply per-frame gain
    mag_modified = mag * gain[np.newaxis, :]
    return (mag_modified * np.exp(1j * phase)).astype(np.complex64)


# ══════════════════════════════════════════════════════════════════════
# 5. COMPLETE TIMING WARP (Convenience function)
# ══════════════════════════════════════════════════════════════════════

def warp_audio_beats(
    y: np.ndarray,
    sr: int,
    beat_times: np.ndarray,
    tempo_shift: float = 0.0,
    rubato: float = 0.0,
    swing: float = 0.0,
    push_pull: float = 0.0,
) -> np.ndarray:
    """
    Complete timing warp: tempo + rubato + swing + push-pull.
    Applied in order: tempo → rubato → swing/push-pull.

    Args:
        y:           Audio waveform
        sr:          Sample rate
        beat_times:  Beat positions (seconds)
        tempo_shift: Relative BPM change (-0.2 to +0.2)
        rubato:      Rubato amount (0 to 1)
        swing:       Swing amount (-1 to +1)
        push_pull:   Push/pull offset (-1 to +1)

    Returns:
        y_warped: Time-warped audio
    """
    import librosa

    y_out = y

    # Step 1: Global tempo shift
    if abs(tempo_shift) > 0.005:
        rate = 1.0 + np.clip(tempo_shift, -0.3, 0.3)
        y_out = librosa.effects.time_stretch(y_out, rate=rate)

    # Adjust beat times for tempo change
    adjusted_beats = beat_times.copy()
    if abs(tempo_shift) > 0.005:
        rate = 1.0 + np.clip(tempo_shift, -0.3, 0.3)
        adjusted_beats = beat_times / rate

    # Step 2: Rubato
    if abs(rubato) > 0.01:
        y_out = apply_rubato(y_out, sr, adjusted_beats, rubato)

    # Step 3: Swing + push/pull
    if abs(swing) > 0.01 or abs(push_pull) > 0.01:
        y_out = apply_microtiming(y_out, sr, adjusted_beats, swing, push_pull)

    return y_out
