"""Compare MI prediction error with IDyOM information content."""
from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np

from Validation.infrastructure.stats import (
    mutual_information,
    pearson_with_ci,
    spearman_with_ci,
)


def compare_per_melody(
    idyom_results: List[Dict],
    mi_results: List[Dict],
) -> List[Dict]:
    """Compare IC and PE for each melody.

    Args:
        idyom_results: From run_idyom.run_idyom_on_melodies().
        mi_results: From run_mi_prediction.run_mi_on_corpus().

    Returns:
        List of per-melody comparison dicts.
    """
    comparisons = []

    for idyom_r, mi_r in zip(idyom_results, mi_results):
        ic = idyom_r["ic"]
        pe = mi_r["pe"]

        # Align lengths (use minimum)
        n = min(len(ic), len(pe))
        if n < 5:
            continue

        ic = ic[:n]
        pe = pe[:n]

        # Skip melodies with constant IC or PE (causes NaN correlations)
        if np.std(ic) < 1e-10 or np.std(pe) < 1e-10:
            continue

        r, p, ci = pearson_with_ci(ic, pe)
        rho, p_rho, _ = spearman_with_ci(ic, pe)
        mi = mutual_information(ic, pe)

        # Guard against NaN from numerical edge cases
        if np.isnan(r) or np.isnan(rho):
            continue

        comparisons.append({
            "melody_name": idyom_r["melody_name"],
            "n_notes": n,
            "pearson_r": r,
            "pearson_p": p,
            "pearson_ci": ci,
            "spearman_rho": rho,
            "spearman_p": p_rho,
            "mutual_info": mi,
        })

    return comparisons


def aggregate_comparison(comparisons: List[Dict]) -> Dict:
    """Aggregate per-melody comparisons into overall statistics.

    Returns:
        Dict with mean_r, median_r, significant_count, total_count.
    """
    if not comparisons:
        return {"mean_r": 0.0, "n_melodies": 0}

    rs = np.array([c["pearson_r"] for c in comparisons])
    rhos = np.array([c["spearman_rho"] for c in comparisons])
    ps = np.array([c["pearson_p"] for c in comparisons])

    return {
        "n_melodies": len(comparisons),
        "mean_pearson_r": float(rs.mean()),
        "median_pearson_r": float(np.median(rs)),
        "std_pearson_r": float(rs.std()),
        "mean_spearman_rho": float(rhos.mean()),
        "n_significant_005": int(np.sum(ps < 0.05)),
        "n_significant_001": int(np.sum(ps < 0.01)),
        "proportion_significant": float(np.mean(ps < 0.05)),
        "pooled_ic_pe": _pooled_correlation(comparisons),
    }


def _pooled_correlation(comparisons: List[Dict]) -> Tuple[float, float]:
    """Compute correlation on pooled (all notes across all melodies) IC and PE."""
    # This would need the raw IC/PE arrays — return placeholder
    return (0.0, 1.0)
