"""Ridge regression encoding models for fMRI ROI prediction."""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import numpy as np

from Validation.infrastructure.stats import cross_validated_r2


def fit_encoding_model(
    features: np.ndarray,
    roi_signals: np.ndarray,
    n_splits: int = 5,
    alpha: float = 100.0,
) -> Dict:
    """Fit encoding model: MI features → fMRI ROI signals.

    Args:
        features: (T, D) MI feature matrix (HRF-convolved, TR-resampled).
        roi_signals: (T, 26) ROI BOLD signals.
        n_splits: CV folds.
        alpha: Ridge regularization.

    Returns:
        Dict with 'r2_per_roi' (26,), 'mean_r2', 'significant_rois'.
    """
    # Align lengths
    n = min(features.shape[0], roi_signals.shape[0])
    X = features[:n]
    Y = roi_signals[:n]

    r2_per_roi = np.zeros(Y.shape[1])

    for roi in range(Y.shape[1]):
        y = Y[:, roi]
        if np.std(y) < 1e-10:
            continue
        mean_r2, fold_r2s = cross_validated_r2(X, y, n_splits=n_splits, alpha=alpha)
        r2_per_roi[roi] = mean_r2

    return {
        "r2_per_roi": r2_per_roi,
        "mean_r2": float(r2_per_roi.mean()),
        "max_r2": float(r2_per_roi.max()),
        "significant_rois": int(np.sum(r2_per_roi > 0)),
        "n_features": features.shape[1],
        "n_timepoints": n,
    }


def compare_feature_sets(
    feature_sets: Dict[str, np.ndarray],
    roi_signals: np.ndarray,
) -> Dict[str, Dict]:
    """Compare encoding accuracy across MI feature sets.

    Args:
        feature_sets: Dict mapping name → (T, D) features.
        roi_signals: (T, 26) ROI signals.

    Returns:
        Dict mapping name → encoding results.
    """
    results = {}
    for name, features in feature_sets.items():
        print(f"[V6] Fitting encoding model: {name} ({features.shape[1]}D)...")
        results[name] = fit_encoding_model(features, roi_signals)
        print(f"  → mean R² = {results[name]['mean_r2']:.4f}, "
              f"significant ROIs = {results[name]['significant_rois']}/26")

    return results
