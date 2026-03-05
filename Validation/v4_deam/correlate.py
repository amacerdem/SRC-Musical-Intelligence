"""Time-lagged cross-correlation between MI and DEAM annotations."""
from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np

from Validation.infrastructure.alignment import time_lag_correlation
from Validation.infrastructure.stats import pearson_with_ci
from Validation.v4_deam.preprocess import align_and_trim


def correlate_song(
    mi_output: Dict[str, np.ndarray],
    valence_annotation: np.ndarray,
    arousal_annotation: np.ndarray,
) -> Dict[str, float]:
    """Compute correlation between MI and DEAM for one song.

    Args:
        mi_output: From run_mi_emotion.extract_valence_arousal().
        valence_annotation: Human valence ratings at 2Hz.
        arousal_annotation: Human arousal ratings at 2Hz.

    Returns:
        Dict with r_valence, r_arousal, p_valence, p_arousal, optimal_lags.
    """
    # Align lengths
    mi_val, ann_val = align_and_trim(mi_output["valence_2hz"], valence_annotation)
    mi_aro, ann_aro = align_and_trim(mi_output["arousal_2hz"], arousal_annotation)

    result = {}

    if len(mi_val) >= 10:
        r_v, p_v, ci_v = pearson_with_ci(mi_val, ann_val)
        result["r_valence"] = r_v
        result["p_valence"] = p_v
        result["ci_valence"] = ci_v

        # Time-lagged correlation (at 2Hz, max lag 5s)
        lag_v, max_r_v, _ = time_lag_correlation(mi_val, ann_val, max_lag_s=5.0, fps=2.0)
        result["optimal_lag_valence"] = lag_v
        result["max_r_valence"] = max_r_v

    if len(mi_aro) >= 10:
        r_a, p_a, ci_a = pearson_with_ci(mi_aro, ann_aro)
        result["r_arousal"] = r_a
        result["p_arousal"] = p_a
        result["ci_arousal"] = ci_a

        lag_a, max_r_a, _ = time_lag_correlation(mi_aro, ann_aro, max_lag_s=5.0, fps=2.0)
        result["optimal_lag_arousal"] = lag_a
        result["max_r_arousal"] = max_r_a

    return result


def aggregate_correlations(
    per_song: List[Dict[str, float]],
) -> Dict[str, float]:
    """Aggregate per-song correlations.

    Returns:
        Dict with mean/median r for valence and arousal.
    """
    val_rs = [s["r_valence"] for s in per_song if "r_valence" in s]
    aro_rs = [s["r_arousal"] for s in per_song if "r_arousal" in s]
    max_val_rs = [s["max_r_valence"] for s in per_song if "max_r_valence" in s]
    max_aro_rs = [s["max_r_arousal"] for s in per_song if "max_r_arousal" in s]
    opt_lag_val = [s["optimal_lag_valence"] for s in per_song if "optimal_lag_valence" in s]
    opt_lag_aro = [s["optimal_lag_arousal"] for s in per_song if "optimal_lag_arousal" in s]

    return {
        "n_songs": len(per_song),
        "mean_r_valence": float(np.mean(val_rs)) if val_rs else 0.0,
        "median_r_valence": float(np.median(val_rs)) if val_rs else 0.0,
        "std_r_valence": float(np.std(val_rs)) if val_rs else 0.0,
        "mean_r_arousal": float(np.mean(aro_rs)) if aro_rs else 0.0,
        "median_r_arousal": float(np.median(aro_rs)) if aro_rs else 0.0,
        "std_r_arousal": float(np.std(aro_rs)) if aro_rs else 0.0,
        "n_sig_valence_005": sum(1 for s in per_song if s.get("p_valence", 1) < 0.05),
        "n_sig_arousal_005": sum(1 for s in per_song if s.get("p_arousal", 1) < 0.05),
        "mean_max_r_valence": float(np.mean(max_val_rs)) if max_val_rs else 0.0,
        "mean_max_r_arousal": float(np.mean(max_aro_rs)) if max_aro_rs else 0.0,
        "mean_optimal_lag_valence": float(np.mean(opt_lag_val)) if opt_lag_val else 0.0,
        "mean_optimal_lag_arousal": float(np.mean(opt_lag_aro)) if opt_lag_aro else 0.0,
    }
