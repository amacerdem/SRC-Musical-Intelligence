"""Compute neural RDMs from fMRI multivoxel patterns."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
from scipy.spatial.distance import pdist, squareform


def compute_fmri_rdm(
    roi_patterns: np.ndarray,
    metric: str = "correlation",
) -> np.ndarray:
    """Compute RDM from fMRI multivoxel patterns.

    Args:
        roi_patterns: (N_stimuli, N_voxels) mean BOLD per stimulus.
        metric: Distance metric.

    Returns:
        (N, N) neural RDM.
    """
    distances = pdist(roi_patterns, metric=metric)
    return squareform(distances)


def extract_stimulus_patterns(
    fmri_data: np.ndarray,
    stimulus_onsets: np.ndarray,
    stimulus_durations: np.ndarray,
    tr: float,
    hrf_delay: float = 6.0,
) -> np.ndarray:
    """Extract mean BOLD pattern per stimulus.

    Averages BOLD signal within each stimulus window (shifted by HRF delay).

    Args:
        fmri_data: (n_TRs, n_voxels) fMRI data.
        stimulus_onsets: (N_stimuli,) onset times in seconds.
        stimulus_durations: (N_stimuli,) durations in seconds.
        tr: fMRI repetition time.
        hrf_delay: HRF peak delay in seconds.

    Returns:
        (N_stimuli, n_voxels) mean pattern per stimulus.
    """
    n_stimuli = len(stimulus_onsets)
    n_voxels = fmri_data.shape[1]
    patterns = np.zeros((n_stimuli, n_voxels))

    for i in range(n_stimuli):
        onset_s = stimulus_onsets[i] + hrf_delay
        offset_s = onset_s + stimulus_durations[i]

        tr_start = int(onset_s / tr)
        tr_end = int(offset_s / tr)

        tr_start = max(0, tr_start)
        tr_end = min(fmri_data.shape[0], tr_end)

        if tr_start < tr_end:
            patterns[i] = fmri_data[tr_start:tr_end].mean(axis=0)

    return patterns


def compute_roi_rdm(
    roi_signals: np.ndarray,
    stimulus_onsets: np.ndarray,
    stimulus_durations: np.ndarray,
    tr: float,
) -> np.ndarray:
    """Compute RDM from 26 ROI activation patterns.

    Args:
        roi_signals: (n_TRs, 26) ROI signals.
        stimulus_onsets: Stimulus onset times.
        stimulus_durations: Stimulus durations.
        tr: Repetition time.

    Returns:
        (N, N) RDM from ROI patterns.
    """
    patterns = extract_stimulus_patterns(
        roi_signals, stimulus_onsets, stimulus_durations, tr,
    )
    return compute_fmri_rdm(patterns, metric="correlation")
