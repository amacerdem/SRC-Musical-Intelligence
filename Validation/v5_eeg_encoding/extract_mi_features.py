"""Extract MI features for EEG encoding models."""
from __future__ import annotations

from pathlib import Path
from typing import Dict

import numpy as np

from Validation.infrastructure.alignment import resample_to_eeg
from Validation.infrastructure.mi_bridge import MIBridge


def extract_features_for_eeg(
    bridge: MIBridge,
    audio_path: Path,
    eeg_sfreq: float = 64.0,
    excerpt_s: float = 300.0,
) -> Dict[str, np.ndarray]:
    """Run MI and resample features to match EEG sampling frequency.

    Returns feature sets at different MI layers for nested model comparison.

    Args:
        bridge: MI pipeline bridge.
        audio_path: Path to stimulus audio.
        eeg_sfreq: EEG sampling frequency.
        excerpt_s: Max audio duration.

    Returns:
        Dict with feature matrices at EEG sampling rate:
        - 'envelope': (T, 1) acoustic envelope
        - 'r3': (T, 97) R³ spectral features
        - 'beliefs': (T, 131) C³ beliefs
        - 'ram': (T, 26) region activations
        - 'neuro': (T, 4) neurochemical state
        - 'full': (T, 258) all MI features concatenated
    """
    result = bridge.run(audio_path, excerpt_s=excerpt_s)

    features = {}

    # Acoustic envelope baseline (mean energy across R³ B group)
    energy = result.r3[:, 7:12].mean(axis=1, keepdims=True)  # B group = energy
    features["envelope"] = resample_to_eeg(energy, eeg_sfreq=eeg_sfreq)

    # R³ features
    features["r3"] = resample_to_eeg(result.r3, eeg_sfreq=eeg_sfreq)

    # C³ beliefs
    features["beliefs"] = resample_to_eeg(result.beliefs, eeg_sfreq=eeg_sfreq)

    # RAM
    features["ram"] = resample_to_eeg(result.ram, eeg_sfreq=eeg_sfreq)

    # Neurochemical state
    features["neuro"] = resample_to_eeg(result.neuro, eeg_sfreq=eeg_sfreq)

    # Full MI feature set
    full = np.concatenate([result.r3, result.beliefs, result.ram, result.neuro], axis=1)
    features["full"] = resample_to_eeg(full, eeg_sfreq=eeg_sfreq)

    return features
