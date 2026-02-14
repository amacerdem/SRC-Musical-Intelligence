"""
Phase-preserving STFT operations.

The #1 fix for "bozuk" audio: instead of Griffin-Lim (which invents phase),
preserve the original phase and only modify magnitude.

Pipeline:
    y → STFT → (mag, phase)
    modify mag
    S' = mag' * exp(j * phase)
    y' = iSTFT(S')
"""

from __future__ import annotations

import numpy as np

# ── Constants ──────────────────────────────────────────────────────────
SR = 44100
N_FFT = 2048
HOP_LENGTH = 256
WIN_LENGTH = N_FFT

# Safety limits (user spec: +6 dB max, -12 dB min)
GAIN_MAX_LINEAR = 10 ** (6.0 / 20.0)    # ~2.0
GAIN_MIN_LINEAR = 10 ** (-12.0 / 20.0)  # ~0.25


# ── Core STFT ──────────────────────────────────────────────────────────

def load_audio(path: str, sr: int = SR) -> np.ndarray:
    """Load audio file as mono float32 numpy array."""
    import soundfile as sf
    y, file_sr = sf.read(path, dtype="float32", always_2d=False)
    if y.ndim > 1:
        y = y.mean(axis=1)
    if file_sr != sr:
        import librosa
        y = librosa.resample(y, orig_sr=file_sr, target_sr=sr)
    return y


def save_audio(path: str, y: np.ndarray, sr: int = SR) -> None:
    """Save audio array to file."""
    import soundfile as sf
    sf.write(path, y, sr, subtype="FLOAT")


def stft_analyze(
    y: np.ndarray,
    n_fft: int = N_FFT,
    hop_length: int = HOP_LENGTH,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Decompose audio into magnitude and phase.

    Returns:
        mag:   (n_freq, n_frames) float32, non-negative
        phase: (n_freq, n_frames) float32, radians [-pi, pi]
    """
    import librosa
    S = librosa.stft(y, n_fft=n_fft, hop_length=hop_length, win_length=n_fft)
    mag = np.abs(S).astype(np.float32)
    phase = np.angle(S).astype(np.float32)
    return mag, phase


def stft_synthesize(
    mag: np.ndarray,
    phase: np.ndarray,
    hop_length: int = HOP_LENGTH,
) -> np.ndarray:
    """
    Reconstruct audio from magnitude + original phase.
    This is the key fix: NO Griffin-Lim, NO phase guessing.
    """
    import librosa
    S = mag * np.exp(1j * phase)
    y = librosa.istft(S, hop_length=hop_length, win_length=N_FFT)
    return y.astype(np.float32)


# ── Safety / Quality ──────────────────────────────────────────────────

def clamp_gain(gain: np.ndarray) -> np.ndarray:
    """Clamp gain curve to safe range [GAIN_MIN, GAIN_MAX]."""
    return np.clip(gain, GAIN_MIN_LINEAR, GAIN_MAX_LINEAR)


def soft_clip(y: np.ndarray, threshold: float = 0.95) -> np.ndarray:
    """Soft-clip (tanh limiter) to prevent true-peak overshoot."""
    mask = np.abs(y) > threshold
    if not mask.any():
        return y
    y_clipped = y.copy()
    y_clipped[mask] = threshold * np.tanh(y[mask] / threshold)
    return y_clipped


def loudness_normalize(y: np.ndarray, target_rms: float | None = None,
                       reference: np.ndarray | None = None) -> np.ndarray:
    """
    Match output loudness to reference or target RMS.
    Prevents transforms from changing overall level.
    """
    if reference is not None:
        target_rms = np.sqrt(np.mean(reference ** 2)) + 1e-8
    if target_rms is None:
        return y
    current_rms = np.sqrt(np.mean(y ** 2)) + 1e-8
    return y * (target_rms / current_rms)


def temporal_smooth(curve: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    """
    Low-pass smooth a per-frame parameter curve.
    Prevents abrupt gain jumps between frames.
    """
    if kernel_size <= 1:
        return curve
    kernel = np.ones(kernel_size) / kernel_size
    # Pad to preserve length
    pad = kernel_size // 2
    padded = np.pad(curve, pad, mode="edge")
    return np.convolve(padded, kernel, mode="valid")[:len(curve)]


def apply_spectral_gain(
    mag: np.ndarray,
    gain_curve: np.ndarray,
    strength: float = 1.0,
) -> np.ndarray:
    """
    Apply a frequency-domain gain curve to magnitude spectrogram.

    Args:
        mag:        (n_freq, n_frames)
        gain_curve: (n_freq,) linear gain per frequency bin
        strength:   0.0 = no change, 1.0 = full effect
    Returns:
        Modified magnitude (clamped to safe range).
    """
    # Interpolate between unity and target gain
    effective_gain = 1.0 + strength * (gain_curve - 1.0)
    effective_gain = clamp_gain(effective_gain)
    return mag * effective_gain[:, np.newaxis]


# ── Frequency envelope helpers ─────────────────────────────────────────

def freq_bin_hz(bin_idx: int, n_fft: int = N_FFT, sr: int = SR) -> float:
    """Convert FFT bin index to frequency in Hz."""
    return bin_idx * sr / n_fft


def hz_to_bin(hz: float, n_fft: int = N_FFT, sr: int = SR) -> int:
    """Convert Hz to nearest FFT bin index."""
    return int(round(hz * n_fft / sr))


def make_shelf_gain(
    n_freq: int,
    cutoff_hz: float,
    low_gain: float,
    high_gain: float,
    transition_hz: float = 500.0,
) -> np.ndarray:
    """
    Create a smooth shelf gain curve (low-shelf / high-shelf).

    Args:
        n_freq:        Number of frequency bins
        cutoff_hz:     Crossover frequency
        low_gain:      Linear gain below cutoff
        high_gain:     Linear gain above cutoff
        transition_hz: Width of smooth transition
    """
    freqs = np.linspace(0, SR / 2, n_freq)
    # Sigmoid transition
    x = (freqs - cutoff_hz) / (transition_hz / 4.0 + 1e-6)
    sigmoid = 1.0 / (1.0 + np.exp(-x))
    gain = low_gain + (high_gain - low_gain) * sigmoid
    return gain.astype(np.float32)


def make_bandpass_gain(
    n_freq: int,
    center_hz: float,
    bandwidth_hz: float,
    boost_db: float,
) -> np.ndarray:
    """
    Create a Gaussian bandpass gain curve.

    Args:
        n_freq:       Number of frequency bins
        center_hz:    Center frequency
        bandwidth_hz: Width (std dev in Hz)
        boost_db:     Peak boost in dB (positive = boost, negative = cut)
    """
    freqs = np.linspace(0, SR / 2, n_freq)
    boost_linear = 10 ** (boost_db / 20.0)
    envelope = np.exp(-0.5 * ((freqs - center_hz) / (bandwidth_hz + 1e-6)) ** 2)
    gain = 1.0 + (boost_linear - 1.0) * envelope
    return gain.astype(np.float32)


# ── Roundtrip verification ─────────────────────────────────────────────

def verify_roundtrip(y: np.ndarray, tolerance: float = 1e-3) -> dict:
    """
    Verify STFT → iSTFT roundtrip is near-identity.
    Returns correlation and max error.
    """
    mag, phase = stft_analyze(y)
    y_rt = stft_synthesize(mag, phase)
    # Trim to same length
    n = min(len(y), len(y_rt))
    y, y_rt = y[:n], y_rt[:n]

    correlation = float(np.corrcoef(y, y_rt)[0, 1])
    max_error = float(np.max(np.abs(y - y_rt)))
    rms_error = float(np.sqrt(np.mean((y - y_rt) ** 2)))

    return {
        "correlation": correlation,
        "max_error": max_error,
        "rms_error": rms_error,
        "pass": correlation > (1.0 - tolerance) and max_error < 0.01,
    }
