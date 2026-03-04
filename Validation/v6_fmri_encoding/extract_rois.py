"""Extract BOLD signal from MI's 26 brain regions using nilearn.

Creates 6mm spherical ROIs at MI's MNI152 coordinates and extracts
mean BOLD per ROI per TR.
"""
from __future__ import annotations

from typing import Dict, List, Optional

import numpy as np

from Validation.config.constants import MNI_COORDINATES, REGION_NAMES


def extract_roi_signals(
    fmri_data: Dict,
    roi_radius_mm: float = 6.0,
) -> np.ndarray:
    """Extract BOLD signal from MI's 26 ROIs.

    Args:
        fmri_data: From preprocess_fmri.load_fmri_subject().
        roi_radius_mm: Sphere radius in mm.

    Returns:
        (n_TRs, 26) ROI time series.
    """
    from nilearn.maskers import NiftiSpheresMasker
    import nibabel as nib

    # Build NIfTI from fmri_data
    n_timepoints = fmri_data["data"].shape[0]
    shape = fmri_data["shape"]
    data_4d = fmri_data["data"].T.reshape(*shape, n_timepoints)
    img = nib.Nifti1Image(data_4d, fmri_data["affine"])

    # Get MNI coordinates for all 26 regions
    coords = [MNI_COORDINATES[name] for name in REGION_NAMES]

    # Extract each ROI individually to handle regions outside brain coverage
    n_regions = len(coords)
    roi_signals = np.zeros((n_timepoints, n_regions))

    for i, (name, coord) in enumerate(zip(REGION_NAMES, coords)):
        try:
            masker = NiftiSpheresMasker(
                seeds=[coord],
                radius=roi_radius_mm,
                standardize="zscore_sample",
                detrend=False,
            )
            signal = masker.fit_transform(img)  # (n_TRs, 1)
            roi_signals[:, i] = signal[:, 0]
        except ValueError:
            # Region outside brain coverage — leave as zeros
            print(f"[V6] Warning: ROI {name} at {coord} outside brain coverage")

    return roi_signals


def extract_roi_signals_from_nifti(
    nifti_path: str,
    roi_radius_mm: float = 6.0,
) -> np.ndarray:
    """Extract ROI signals directly from a NIfTI file.

    Args:
        nifti_path: Path to preprocessed NIfTI file.
        roi_radius_mm: Sphere radius.

    Returns:
        (n_TRs, 26) ROI time series.
    """
    from nilearn.maskers import NiftiSpheresMasker

    coords = [MNI_COORDINATES[name] for name in REGION_NAMES]

    n_regions = len(coords)
    import nibabel as nib
    img = nib.load(nifti_path)
    n_timepoints = img.shape[3]

    roi_signals = np.zeros((n_timepoints, n_regions))
    for i, (name, coord) in enumerate(zip(REGION_NAMES, coords)):
        try:
            masker = NiftiSpheresMasker(
                seeds=[coord],
                radius=roi_radius_mm,
                standardize="zscore_sample",
            )
            signal = masker.fit_transform(nifti_path)
            roi_signals[:, i] = signal[:, 0]
        except ValueError:
            print(f"[V6] Warning: ROI {name} at {coord} outside brain coverage")

    return roi_signals


def get_region_function_mapping() -> Dict[str, List[str]]:
    """Get the mapping from brain regions to MI cognitive functions.

    Returns:
        Dict mapping function name → list of associated region abbreviations.
    """
    return {
        "F1_Sensory": ["A1_HG", "STG", "MGB", "IC", "AN", "CN", "SOC"],
        "F2_Prediction": ["STG", "IFG", "dlPFC"],
        "F3_Attention": ["dlPFC", "ACC", "IFG"],
        "F4_Memory": ["hippocampus", "AG", "TP"],
        "F5_Emotion": ["amygdala", "insula", "vmPFC", "ACC"],
        "F6_Reward": ["VTA", "NAcc", "OFC", "caudate"],
        "F7_Motor": ["SMA", "PMC", "putamen", "caudate"],
        "F8_Learning": ["hippocampus", "caudate", "dlPFC"],
        "F9_Social": ["STS", "TP", "vmPFC"],
    }
