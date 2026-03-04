"""Nilearn fMRI preprocessing pipeline for music listening data."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

import numpy as np


def load_fmri_subject(
    bids_dir: Path,
    subject_id: str,
    task: str = "music",
) -> Dict:
    """Load and preprocess fMRI data for one subject (BIDS format).

    Pipeline:
    1. Load NIfTI from BIDS directory
    2. Apply smoothing (6mm FWHM)
    3. High-pass filter (128s)
    4. Z-score normalize

    Args:
        bids_dir: BIDS dataset root.
        subject_id: Subject ID (e.g. 'sub-01').
        task: Task name in BIDS.

    Returns:
        Dict with 'data' (n_timepoints, n_voxels), 'affine', 'tr', 'subject_id'.
    """
    import nibabel as nib
    from nilearn.image import clean_img, smooth_img

    # Find functional file
    func_dir = bids_dir / subject_id / "func"
    if not func_dir.exists():
        raise FileNotFoundError(f"No func dir for {subject_id}")

    nii_files = list(func_dir.glob(f"*task-{task}*bold.nii*"))
    if not nii_files:
        # Try without task filter
        nii_files = list(func_dir.glob("*bold.nii*"))
    if not nii_files:
        raise FileNotFoundError(f"No BOLD files for {subject_id}")

    nii_path = nii_files[0]

    # Load
    img = nib.load(str(nii_path))

    # Determine TR from header or sidecar JSON
    tr = img.header.get_zooms()[3] if len(img.header.get_zooms()) > 3 else 2.0

    # Smooth (6mm FWHM)
    img_smooth = smooth_img(img, fwhm=6)

    # Clean (high-pass filter, detrend, standardize)
    img_clean = clean_img(
        img_smooth,
        detrend=True,
        standardize="zscore_sample",
        high_pass=1 / 128.0,
        t_r=tr,
    )

    data = img_clean.get_fdata()
    # Reshape to 2D: (n_timepoints, n_voxels)
    n_timepoints = data.shape[3]
    data_2d = data.reshape(-1, n_timepoints).T

    return {
        "data": data_2d,
        "affine": img.affine,
        "tr": float(tr),
        "subject_id": subject_id,
        "shape": data.shape[:3],
    }


def load_all_subjects(
    bids_dir: Path,
    task: str = "music",
    max_subjects: Optional[int] = None,
) -> List[Dict]:
    """Load fMRI for all subjects."""
    subjects = []
    sub_dirs = sorted(d for d in bids_dir.iterdir()
                      if d.is_dir() and d.name.startswith("sub"))

    if max_subjects:
        sub_dirs = sub_dirs[:max_subjects]

    for sub_dir in sub_dirs:
        try:
            data = load_fmri_subject(bids_dir, sub_dir.name, task)
            subjects.append(data)
            print(f"[V6] Loaded {sub_dir.name}: {data['data'].shape}")
        except Exception as e:
            print(f"[V6] Error loading {sub_dir.name}: {e}")

    return subjects
