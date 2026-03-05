"""Statistical helpers for validation — correlation, permutation, CI, corrections."""
from __future__ import annotations

from typing import Tuple

import numpy as np
from scipy import stats
from scipy.stats import pearsonr, spearmanr


def pearson_with_ci(
    x: np.ndarray,
    y: np.ndarray,
    alpha: float = 0.05,
) -> Tuple[float, float, Tuple[float, float]]:
    """Pearson r with p-value and bootstrap 95% CI.

    Returns:
        Tuple of (r, p_value, (ci_lower, ci_upper)).
    """
    r, p = pearsonr(x, y)
    ci = _bootstrap_ci(x, y, stat_func=_pearson_r, alpha=alpha)
    return r, p, ci


def spearman_with_ci(
    x: np.ndarray,
    y: np.ndarray,
    alpha: float = 0.05,
) -> Tuple[float, float, Tuple[float, float]]:
    """Spearman rho with p-value and bootstrap 95% CI.

    Returns:
        Tuple of (rho, p_value, (ci_lower, ci_upper)).
    """
    rho, p = spearmanr(x, y)
    ci = _bootstrap_ci(x, y, stat_func=_spearman_r, alpha=alpha)
    return rho, p, ci


def permutation_test(
    x: np.ndarray,
    y: np.ndarray,
    n_permutations: int = 10_000,
    stat_func: str = "pearson",
    seed: int = 42,
) -> Tuple[float, float]:
    """Non-parametric permutation test for correlation significance.

    Args:
        x, y: Input arrays.
        n_permutations: Number of permutations.
        stat_func: 'pearson' or 'spearman'.
        seed: Random seed for reproducibility.

    Returns:
        Tuple of (observed_stat, p_value).
    """
    rng = np.random.default_rng(seed)
    func = _pearson_r if stat_func == "pearson" else _spearman_r

    observed = func(x, y)
    count = 0
    for _ in range(n_permutations):
        y_perm = rng.permutation(y)
        if abs(func(x, y_perm)) >= abs(observed):
            count += 1

    p_value = (count + 1) / (n_permutations + 1)
    return observed, p_value


def bonferroni_correction(
    p_values: np.ndarray,
    alpha: float = 0.05,
) -> Tuple[np.ndarray, np.ndarray]:
    """Bonferroni multiple comparison correction.

    Returns:
        Tuple of (corrected_p_values, reject_mask).
    """
    p_values = np.asarray(p_values)
    n = len(p_values)
    corrected = np.minimum(p_values * n, 1.0)
    reject = corrected < alpha
    return corrected, reject


def fdr_correction(
    p_values: np.ndarray,
    alpha: float = 0.05,
) -> Tuple[np.ndarray, np.ndarray]:
    """Benjamini-Hochberg FDR correction.

    Returns:
        Tuple of (corrected_p_values, reject_mask).
    """
    p_values = np.asarray(p_values)
    n = len(p_values)
    sorted_idx = np.argsort(p_values)
    sorted_p = p_values[sorted_idx]

    # BH correction
    corrected = np.empty(n)
    corrected[sorted_idx] = np.minimum(
        sorted_p * n / (np.arange(n) + 1),
        1.0,
    )
    # Enforce monotonicity
    for i in range(n - 2, -1, -1):
        corrected[sorted_idx[i]] = min(
            corrected[sorted_idx[i]],
            corrected[sorted_idx[i + 1]] if i + 1 < n else 1.0,
        )

    reject = corrected < alpha
    return corrected, reject


def effect_size_cohen_d(
    group1: np.ndarray,
    group2: np.ndarray,
) -> float:
    """Cohen's d for between-group comparison (pooled SD)."""
    n1, n2 = len(group1), len(group2)
    var1, var2 = group1.var(ddof=1), group2.var(ddof=1)
    pooled_sd = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    if pooled_sd == 0:
        return 0.0
    return (group1.mean() - group2.mean()) / pooled_sd


def cross_validated_r2(
    X: np.ndarray,
    y: np.ndarray,
    n_splits: int = 5,
    alpha: float = 1.0,
    seed: int = 42,
) -> Tuple[float, np.ndarray]:
    """K-fold cross-validated R² using Ridge regression.

    Args:
        X: Feature matrix (n_samples, n_features).
        y: Target vector (n_samples,) or (n_samples, n_targets).
        n_splits: Number of CV folds.
        alpha: Ridge regularization.
        seed: Random seed.

    Returns:
        Tuple of (mean_r2, per_fold_r2).
    """
    from sklearn.linear_model import Ridge
    from sklearn.model_selection import KFold, cross_val_score

    model = Ridge(alpha=alpha)
    cv = KFold(n_splits=n_splits, shuffle=True, random_state=seed)
    scores = cross_val_score(model, X, y, cv=cv, scoring="r2")
    return scores.mean(), scores


def mutual_information(
    x: np.ndarray,
    y: np.ndarray,
    n_bins: int = 20,
) -> float:
    """Estimate mutual information between two variables via binning.

    Returns:
        Mutual information in nats.
    """
    hist_2d, _, _ = np.histogram2d(x, y, bins=n_bins)
    pxy = hist_2d / hist_2d.sum()
    px = pxy.sum(axis=1)
    py = pxy.sum(axis=0)

    # Avoid log(0)
    mask = pxy > 0
    mi = np.sum(pxy[mask] * np.log(pxy[mask] / (px[:, None] * py[None, :])[mask]))
    return float(mi)


def fisher_z_mean_ci(
    r_values: np.ndarray,
    n_values: np.ndarray,
    alpha: float = 0.05,
) -> tuple[float, float, float]:
    """Compute Fisher-z weighted mean correlation with CI.

    Properly averages correlation coefficients via arctanh transform,
    weighted by sample size. Returns back-transformed mean and CI.

    Args:
        r_values: Array of Pearson r values.
        n_values: Array of per-sample N values.
        alpha: Significance level for CI.

    Returns:
        Tuple of (mean_r, ci_lower, ci_upper) in r-space.
    """
    r_values = np.asarray(r_values, dtype=np.float64)
    n_values = np.asarray(n_values, dtype=np.float64)

    # Clamp r to avoid arctanh(±1) = ±inf
    r_clamp = np.clip(r_values, -0.9999, 0.9999)
    z_values = np.arctanh(r_clamp)
    weights = n_values - 3  # Fisher z variance ≈ 1/(n-3)
    weights = np.maximum(weights, 1)

    z_mean = np.average(z_values, weights=weights)
    se_z = 1.0 / np.sqrt(np.sum(weights))

    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_lower = z_mean - z_crit * se_z
    z_upper = z_mean + z_crit * se_z

    return float(np.tanh(z_mean)), float(np.tanh(z_lower)), float(np.tanh(z_upper))


# ── Internal helpers ──

def _pearson_r(x: np.ndarray, y: np.ndarray) -> float:
    return float(np.corrcoef(x, y)[0, 1])


def _spearman_r(x: np.ndarray, y: np.ndarray) -> float:
    return float(spearmanr(x, y).statistic)


def _bootstrap_ci(
    x: np.ndarray,
    y: np.ndarray,
    stat_func,
    alpha: float = 0.05,
    n_bootstrap: int = 5000,
    seed: int = 42,
) -> Tuple[float, float]:
    """Bootstrap confidence interval for a correlation statistic."""
    rng = np.random.default_rng(seed)
    n = len(x)
    boot_stats = np.empty(n_bootstrap)

    for i in range(n_bootstrap):
        idx = rng.integers(0, n, size=n)
        boot_stats[i] = stat_func(x[idx], y[idx])

    lower = np.percentile(boot_stats, 100 * alpha / 2)
    upper = np.percentile(boot_stats, 100 * (1 - alpha / 2))
    return float(lower), float(upper)
