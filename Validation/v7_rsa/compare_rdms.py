"""Compare model RDMs via Spearman correlation and permutation tests."""
from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np
from scipy.spatial.distance import squareform
from scipy.stats import spearmanr

from Validation.infrastructure.stats import permutation_test


def rdm_correlation(
    rdm_a: np.ndarray,
    rdm_b: np.ndarray,
) -> Tuple[float, float]:
    """Spearman correlation between upper triangles of two RDMs.

    Args:
        rdm_a: (N, N) RDM.
        rdm_b: (N, N) RDM (same size).

    Returns:
        Tuple of (rho, p_value).
    """
    # Extract upper triangle (excluding diagonal)
    tri_a = squareform(rdm_a, checks=False)
    tri_b = squareform(rdm_b, checks=False)

    rho, p = spearmanr(tri_a, tri_b)
    return float(rho), float(p)


def rdm_permutation_test(
    rdm_a: np.ndarray,
    rdm_b: np.ndarray,
    n_permutations: int = 10_000,
) -> Tuple[float, float]:
    """Permutation test for RDM similarity.

    Returns:
        Tuple of (observed_rho, p_value).
    """
    tri_a = squareform(rdm_a, checks=False)
    tri_b = squareform(rdm_b, checks=False)

    return permutation_test(tri_a, tri_b, n_permutations, stat_func="spearman")


def compare_all_models(
    neural_rdm: np.ndarray,
    model_rdms: Dict[str, np.ndarray],
    n_permutations: int = 10_000,
) -> List[Dict]:
    """Compare multiple model RDMs against a neural RDM.

    Args:
        neural_rdm: Reference neural RDM.
        model_rdms: Dict mapping model_name → RDM.
        n_permutations: Permutation test iterations.

    Returns:
        List of comparison dicts sorted by correlation (descending).
    """
    comparisons = []

    for name, model_rdm in model_rdms.items():
        rho, p_param = rdm_correlation(neural_rdm, model_rdm)
        _, p_perm = rdm_permutation_test(neural_rdm, model_rdm, n_permutations)

        comparisons.append({
            "model_name": name,
            "spearman_rho": rho,
            "p_parametric": p_param,
            "p_permutation": p_perm,
        })

    # Sort by correlation
    comparisons.sort(key=lambda x: x["spearman_rho"], reverse=True)
    return comparisons


def noise_ceiling(
    subject_rdms: List[np.ndarray],
) -> Tuple[float, float]:
    """Estimate noise ceiling from multiple subjects.

    Lower bound: correlation of each subject with mean of OTHER subjects.
    Upper bound: correlation of each subject with mean of ALL subjects.

    Args:
        subject_rdms: List of per-subject RDMs.

    Returns:
        Tuple of (lower_ceiling, upper_ceiling).
    """
    n_subjects = len(subject_rdms)
    if n_subjects < 2:
        return (1.0, 1.0)

    mean_rdm = np.mean(subject_rdms, axis=0)

    upper_rs = []
    lower_rs = []

    for i in range(n_subjects):
        # Upper: correlation with mean of all
        rho_up, _ = rdm_correlation(subject_rdms[i], mean_rdm)
        upper_rs.append(rho_up)

        # Lower: correlation with mean of others
        others = [subject_rdms[j] for j in range(n_subjects) if j != i]
        mean_others = np.mean(others, axis=0)
        rho_low, _ = rdm_correlation(subject_rdms[i], mean_others)
        lower_rs.append(rho_low)

    return float(np.mean(lower_rs)), float(np.mean(upper_rs))
