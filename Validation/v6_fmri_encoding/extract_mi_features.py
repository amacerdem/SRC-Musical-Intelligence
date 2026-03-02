"""Extract MI features resampled to fMRI TR resolution."""
from __future__ import annotations

from pathlib import Path
from typing import Dict

import numpy as np

from Validation.infrastructure.alignment import apply_hrf, resample_to_tr
from Validation.infrastructure.mi_bridge import MIBridge


def extract_features_for_fmri(
    bridge: MIBridge,
    audio_path: Path,
    tr: float = 2.0,
    excerpt_s: float = 300.0,
) -> Dict[str, np.ndarray]:
    """Run MI and resample features to fMRI TR, with HRF convolution.

    Args:
        bridge: MI pipeline bridge.
        audio_path: Stimulus audio path.
        tr: fMRI repetition time.
        excerpt_s: Max duration.

    Returns:
        Dict with HRF-convolved features at TR resolution:
        - 'r3': (T, 97)
        - 'beliefs': (T, 131)
        - 'ram': (T, 26)
        - 'neuro': (T, 4)
        - 'full': (T, 258)
    """
    result = bridge.run(audio_path, excerpt_s=excerpt_s)

    features = {}

    # Resample to TR, then convolve with HRF
    for name, data in [
        ("r3", result.r3),
        ("beliefs", result.beliefs),
        ("ram", result.ram),
        ("neuro", result.neuro),
    ]:
        resampled = resample_to_tr(data, tr_seconds=tr)
        features[name] = apply_hrf(resampled, tr=tr)

    # Full concatenated
    full = np.concatenate([result.r3, result.beliefs, result.ram, result.neuro], axis=1)
    full_resampled = resample_to_tr(full, tr_seconds=tr)
    features["full"] = apply_hrf(full_resampled, tr=tr)

    return features
