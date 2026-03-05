"""EEG preprocessing for NMED-T data (MAT or MNE formats).

NMED-T MAT structure (songXX_Imputed.mat):
  - 'data': (subjects, channels, timepoints) cleaned EEG at 125 Hz
  - 128 EEG channels, 20 subjects, variable song length
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

import numpy as np


def load_nmedt_mat(
    mat_path: Path,
    subject_idx: int = 0,
    sfreq_source: float = 125.0,
    sfreq_target: float = 64.0,
) -> Dict:
    """Load one subject's EEG from an NMED-T MAT file.

    Args:
        mat_path: Path to songXX_Imputed.mat file.
        subject_idx: Subject index (0-19) within the MAT file.
        sfreq_source: Original sampling frequency (NMED-T = 125 Hz).
        sfreq_target: Target after downsampling.

    Returns:
        Dict with 'eeg' (n_times, n_channels), 'sfreq', 'subject_id', 'song_id'.
    """
    from scipy.io import loadmat
    from scipy.signal import resample_poly

    mat = loadmat(str(mat_path), squeeze_me=True)

    # Find the EEG data variable (common names in NMED-T)
    data = None
    for key in ("data", "EEG", "eeg", "cleanData", "imputed"):
        if key in mat:
            data = np.array(mat[key])
            break

    if data is None:
        # Try first non-metadata key
        for key in mat:
            if not key.startswith("_"):
                v = mat[key]
                if isinstance(v, np.ndarray) and v.ndim >= 2:
                    data = v
                    break

    if data is None:
        raise ValueError(f"No EEG data found in {mat_path}")

    # Handle various shapes: (subjects, channels, time) or (channels, time)
    if data.ndim == 3:
        if subject_idx >= data.shape[0]:
            raise IndexError(f"Subject {subject_idx} out of range (max {data.shape[0] - 1})")
        eeg = data[subject_idx]  # (channels, time)
    elif data.ndim == 2:
        eeg = data  # (channels, time) — single subject
    else:
        raise ValueError(f"Unexpected data shape: {data.shape}")

    # Ensure (channels, time) — channels should be smaller dim
    if eeg.shape[0] > eeg.shape[1]:
        eeg = eeg.T  # was (time, channels), transpose

    # Band-pass filter 1–40 Hz (simple butterworth)
    from scipy.signal import butter, sosfiltfilt
    sos = butter(4, [1.0, 40.0], btype="bandpass", fs=sfreq_source, output="sos")
    eeg = sosfiltfilt(sos, eeg, axis=1)

    # Re-reference to average
    eeg = eeg - eeg.mean(axis=0, keepdims=True)

    # Downsample: 125 Hz → 64 Hz  (resample_poly uses rational approximation)
    if sfreq_target < sfreq_source:
        from math import gcd
        up = int(sfreq_target)
        down = int(sfreq_source)
        g = gcd(up, down)
        eeg = resample_poly(eeg, up // g, down // g, axis=1)

    eeg = eeg.T  # → (n_times, n_channels)

    song_id = mat_path.stem.replace("_Imputed", "")

    return {
        "eeg": eeg.astype(np.float64),
        "sfreq": sfreq_target,
        "ch_names": [f"EEG{i:03d}" for i in range(eeg.shape[1])],
        "subject_id": f"sub-{subject_idx + 1:02d}",
        "song_id": song_id,
    }


def load_eeg_subject(
    subject_dir: Path,
    subject_id: str,
    sfreq_target: float = 64.0,
) -> Dict:
    """Load and preprocess EEG data for one subject (MNE format).

    Pipeline:
    1. Load raw EEG (128 channels, 125 Hz)
    2. Band-pass filter 0.1–40 Hz
    3. Re-reference to average
    4. Downsample to target frequency

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
