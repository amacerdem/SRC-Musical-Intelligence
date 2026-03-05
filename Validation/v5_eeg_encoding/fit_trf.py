"""Fit temporal response functions (TRFs) predicting EEG from MI features.

Uses ridge regression with cross-validation to fit encoding models
that predict EEG responses from MI feature time series.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import numpy as np


def fit_trf(
    features: np.ndarray,
    eeg: np.ndarray,
    sfreq: float,
    tmin: float = 0.0,
    tmax: float = 0.25,
    alphas: Optional[List[float]] = None,
    n_splits: int = 5,
) -> Dict:
    """Fit a multivariate temporal response function.

    Uses lagged regression: predicts EEG(t) from features(t-tmin:t-tmax).

    Args:
        features: (T, D) stimulus feature matrix.
        eeg: (T, C) EEG data matrix.
        sfreq: Sampling frequency.
        tmin: Minimum lag in seconds (negative = pre-stimulus).
        tmax: Maximum lag in seconds.
        alphas: Ridge regularization values to try.
        n_splits: CV folds.

    Returns:
        Dict with 'r2_per_channel', 'mean_r2', 'weights', 'best_alpha'.
    """
    from sklearn.linear_model import RidgeCV
    from sklearn.model_selection import KFold
    from sklearn.preprocessing import StandardScaler

    if alphas is None:
        alphas = [1e-1, 1e0, 1e1, 1e2, 1e3, 1e4]

    # Create lagged feature matrix
    X_lagged = _create_lagged_matrix(features, sfreq, tmin, tmax)

    # PCA when lagged features > 500 (prevents timeout on 258D × 17 lags)
    n_lagged_raw = X_lagged.shape[1]
    if n_lagged_raw > 500:
        from sklearn.decomposition import PCA
        max_comp = min(50, X_lagged.shape[0] // 5, n_lagged_raw)
        if max_comp > 0:
            X_lagged = StandardScaler().fit_transform(X_lagged)
            X_lagged = PCA(n_components=max_comp).fit_transform(X_lagged)

    # Align lengths
    n = min(X_lagged.shape[0], eeg.shape[0])
    X = X_lagged[:n]
    y = eeg[:n]

    # Standardize features for Ridge
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # Cross-validated ridge regression
    cv = KFold(n_splits=n_splits, shuffle=False)
    r2_per_channel = np.zeros(y.shape[1])
    best_alpha_val = alphas[0]

    for ch in range(y.shape[1]):
        y_ch = y[:, ch]
        fold_r2s = []

        for train_idx, test_idx in cv.split(X):
            model = RidgeCV(alphas=alphas)
            model.fit(X[train_idx], y_ch[train_idx])
            y_pred = model.predict(X[test_idx])
            if ch == 0:
                best_alpha_val = float(model.alpha_)

            ss_res = np.sum((y_ch[test_idx] - y_pred) ** 2)
            ss_tot = np.sum((y_ch[test_idx] - y_ch[test_idx].mean()) ** 2)
            r2 = 1 - ss_res / max(ss_tot, 1e-10)
            fold_r2s.append(r2)

        r2_per_channel[ch] = np.mean(fold_r2s)

    return {
        "r2_per_channel": r2_per_channel,
        "mean_r2": float(r2_per_channel.mean()),
        "best_alpha": best_alpha_val,
        "n_features": features.shape[1],
        "n_lagged_features": n_lagged_raw,
        "n_timepoints": n,
    }


def compare_models(
    feature_sets: Dict[str, np.ndarray],
    eeg: np.ndarray,
    sfreq: float,
) -> Dict[str, Dict]:
    """Compare encoding models with different feature sets.

    Args:
        feature_sets: Dict mapping model_name → (T, D) features.
        eeg: (T, C) EEG data.
        sfreq: Sampling frequency.

    Returns:
        Dict mapping model_name → fit results.
    """
    results = {}
    for name, features in feature_sets.items():
        print(f"[V5] Fitting TRF model: {name} ({features.shape[1]}D)...")
        results[name] = fit_trf(features, eeg, sfreq)
        print(f"  → mean R² = {results[name]['mean_r2']:.4f}")

    return results


def _create_lagged_matrix(
    features: np.ndarray,
    sfreq: float,
    tmin: float,
    tmax: float,
) -> np.ndarray:
    """Create time-lagged feature matrix for TRF fitting.

    Args:
        features: (T, D) feature matrix.
        sfreq: Sampling frequency.
        tmin: Minimum lag (seconds).
        tmax: Maximum lag (seconds).

    Returns:
        (T', D*n_lags) lagged matrix.
    """
    lag_min = int(tmin * sfreq)
    lag_max = int(tmax * sfreq)
    lags = np.arange(lag_min, lag_max + 1)

    T, D = features.shape
    n_lags = len(lags)

    # Pad features
    pad_before = max(0, -lag_min)
    pad_after = max(0, lag_max)
    padded = np.pad(features, ((pad_before, pad_after), (0, 0)), mode="edge")

    # Create lagged matrix
    X_lagged = np.zeros((T, D * n_lags))
    for i, lag in enumerate(lags):
        start = pad_before + lag
        X_lagged[:, i * D:(i + 1) * D] = padded[start:start + T]

    return X_lagged
