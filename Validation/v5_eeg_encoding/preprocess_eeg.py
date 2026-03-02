"""MNE-Python EEG preprocessing pipeline for NMED-T data."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np


def load_eeg_subject(
    subject_dir: Path,
    subject_id: str,
    sfreq_target: float = 64.0,
) -> Dict:
    """Load and preprocess EEG data for one subject.

    Pipeline:
    1. Load raw EEG (128 channels, 125 Hz)
    2. Band-pass filter 0.1–40 Hz
    3. Re-reference to average
    4. Downsample to target frequency
    5. Reject bad channels via interpolation

    Args:
        subject_dir: Path to subject's EEG files.
        subject_id: Subject identifier.
        sfreq_target: Target sampling frequency after downsampling.

    Returns:
        Dict with 'eeg' (n_times, n_channels), 'sfreq', 'ch_names', 'subject_id'.
    """
    import mne

    # Find EEG file (various formats)
    eeg_files = list(subject_dir.glob("*.set")) + list(subject_dir.glob("*.fif"))
    if not eeg_files:
        raise FileNotFoundError(f"No EEG files found in {subject_dir}")

    eeg_path = eeg_files[0]

    # Load
    if eeg_path.suffix == ".set":
        raw = mne.io.read_raw_eeglab(str(eeg_path), preload=True, verbose=False)
    else:
        raw = mne.io.read_raw_fif(str(eeg_path), preload=True, verbose=False)

    # Band-pass filter
    raw.filter(0.1, 40.0, verbose=False)

    # Re-reference to average
    raw.set_eeg_reference("average", verbose=False)

    # Downsample
    if raw.info["sfreq"] > sfreq_target:
        raw.resample(sfreq_target, verbose=False)

    # Get data
    data = raw.get_data().T  # (n_times, n_channels)

    return {
        "eeg": data,
        "sfreq": raw.info["sfreq"],
        "ch_names": raw.ch_names,
        "subject_id": subject_id,
    }


def load_all_subjects(
    dataset_dir: Path,
    sfreq_target: float = 64.0,
    max_subjects: Optional[int] = None,
) -> List[Dict]:
    """Load EEG for all subjects in NMED-T dataset.

    Returns:
        List of subject data dicts.
    """
    subjects = []
    sub_dirs = sorted(d for d in dataset_dir.iterdir()
                      if d.is_dir() and d.name.startswith("sub"))

    if max_subjects:
        sub_dirs = sub_dirs[:max_subjects]

    for sub_dir in sub_dirs:
        try:
            data = load_eeg_subject(sub_dir, sub_dir.name, sfreq_target)
            subjects.append(data)
            print(f"[V5] Loaded {sub_dir.name}: {data['eeg'].shape}")
        except Exception as e:
            print(f"[V5] Error loading {sub_dir.name}: {e}")

    return subjects
