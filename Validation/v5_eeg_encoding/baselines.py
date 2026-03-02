"""Baseline models for EEG encoding comparison."""
from __future__ import annotations

from pathlib import Path
from typing import Dict

import numpy as np

from Validation.infrastructure.alignment import resample_to_eeg
from Validation.infrastructure.audio_loader import load_audio


def compute_envelope_baseline(
    audio_path: Path,
    eeg_sfreq: float = 64.0,
) -> np.ndarray:
    """Compute acoustic envelope baseline (broadband amplitude).

    Args:
        audio_path: Audio stimulus path.
        eeg_sfreq: Target EEG sampling frequency.

    Returns:
        (T, 1) envelope at EEG sampling rate.
    """
    from scipy.signal import hilbert

    audio, sr = load_audio(audio_path, mono=True)

    # Analytic signal → envelope
    analytic = hilbert(audio)
    envelope = np.abs(analytic)

    # Low-pass and downsample
    target_samples = int(len(audio) / sr * eeg_sfreq)
    if target_samples > 0:
        from scipy.signal import resample as scipy_resample
        envelope_ds = scipy_resample(envelope, target_samples)
    else:
        envelope_ds = envelope

    return envelope_ds[:, np.newaxis]


def compute_spectrogram_baseline(
    audio_path: Path,
    eeg_sfreq: float = 64.0,
    n_bands: int = 16,
) -> np.ndarray:
    """Compute spectral baseline (mel-band energies).

    Args:
        audio_path: Audio stimulus path.
        eeg_sfreq: Target sampling frequency.
        n_bands: Number of mel bands.

    Returns:
        (T, n_bands) mel-band energies at EEG sampling rate.
    """
    import librosa

    audio, sr = load_audio(audio_path, mono=True)

    # Mel spectrogram
    hop_length = int(sr / eeg_sfreq)  # target resolution
    mel = librosa.feature.melspectrogram(
        y=audio, sr=sr, n_mels=n_bands, hop_length=hop_length,
    )
    mel_db = librosa.power_to_db(mel, ref=np.max)

    return mel_db.T  # (T, n_bands)


def get_all_baselines(
    audio_path: Path,
    eeg_sfreq: float = 64.0,
) -> Dict[str, np.ndarray]:
    """Compute all baseline feature sets.

    Returns:
        Dict with 'envelope' (T,1) and 'spectrogram' (T,16).
    """
    return {
        "envelope": compute_envelope_baseline(audio_path, eeg_sfreq),
        "spectrogram": compute_spectrogram_baseline(audio_path, eeg_sfreq),
    }
