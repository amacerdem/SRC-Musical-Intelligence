"""Scale-matched exponential temporal weighting for multi-horizon prediction.

Implements the core weighting function for C³ v2.0 multi-scale prediction:

    w(h, Δ) = exp(-α |h - Δ|)

where h is an evidence horizon index and Δ is the prediction target horizon.

The weight peaks when evidence and prediction are at the same temporal scale
(h = Δ) and decays exponentially with index distance.  Since H³ horizons are
quasi-log spaced, index distance approximates log-time distance.

Usage:
    weights = scale_matched_weights(target_h=18, evidence_horizons=CONSONANCE_HORIZONS)
    trend_sum = sum(w * h3_trend[h] for h, w in weights.items())
"""
from __future__ import annotations

import math
from typing import Dict, Sequence

from ...ear.h3.constants.horizons import HORIZON_MS

# ---------------------------------------------------------------------------
# Horizon seconds lookup (derived from HORIZON_MS)
# ---------------------------------------------------------------------------
HORIZON_SECONDS: tuple[float, ...] = tuple(ms / 1000.0 for ms in HORIZON_MS)

# ---------------------------------------------------------------------------
# Representative horizons for multi-scale prediction
# ---------------------------------------------------------------------------
# 8 horizons, 2 per perceptual band, covering musical timescales from
# note attack (46 ms) to movement structure (414 s).
#
#   Micro:  H5  (46 ms, note attack)     H7  (250 ms, eighth note)
#   Meso:   H10 (400 ms, moderate beat)   H13 (600 ms, standard beat)
#   Macro:  H18 (2 s, measure @ 120 BPM)  H21 (8 s, passage)
#   Ultra:  H24 (36 s, section)            H28 (414 s, movement)
CONSONANCE_HORIZONS: tuple[int, ...] = (5, 7, 10, 13, 18, 21, 24, 28)

# Default decay rate for 8-horizon sparse set.
# α=0.3 gives ~49% at target, ~20% at ±3 indices, ~5% at ±8.
# For denser horizon sets (16 or 32), increase to ~0.6-1.2.
DEFAULT_ALPHA: float = 0.3


# ---------------------------------------------------------------------------
# Core weighting function
# ---------------------------------------------------------------------------

def scale_matched_weights(
    target_h: int,
    evidence_horizons: Sequence[int],
    alpha: float = DEFAULT_ALPHA,
) -> Dict[int, float]:
    """Compute scale-matched exponential weights.

    For a prediction at horizon ``target_h`` (Δ), evidence from horizon ``h``
    is weighted by ``exp(-α |h - Δ|)``.

    * Peak at ``h = target_h`` (exact timescale match).
    * Exponential increase from ``h = 0`` toward ``target_h``.
    * Sharp drop past ``target_h``.

    Args:
        target_h: H³ horizon index for the prediction target.
        evidence_horizons: Horizon indices used as evidence sources.
        alpha: Decay rate.  Higher → sharper peak.

    Returns:
        Normalized weight dict ``{horizon_idx: weight}``.
        Weights sum to 1.0.
    """
    raw: Dict[int, float] = {}
    for h in evidence_horizons:
        raw[h] = math.exp(-alpha * abs(h - target_h))

    total = sum(raw.values())
    if total < 1e-12:
        n = len(evidence_horizons)
        return {h: 1.0 / n for h in evidence_horizons}

    return {h: w / total for h, w in raw.items()}


def precompute_weight_matrix(
    horizons: Sequence[int],
    alpha: float = DEFAULT_ALPHA,
) -> Dict[int, Dict[int, float]]:
    """Precompute the full weight matrix for all target×evidence pairs.

    Returns:
        ``{target_h: {evidence_h: weight}}``.
    """
    return {
        target_h: scale_matched_weights(target_h, horizons, alpha)
        for target_h in horizons
    }


def aggregate_weights(
    horizons: Sequence[int],
    T_char: float,
    alpha: float = DEFAULT_ALPHA,
) -> Dict[int, float]:
    """Compute belief-level aggregation weights based on T_char.

    Finds the horizon closest to T_char (in seconds) and uses that as the
    weighting anchor.  Horizons near T_char get highest weight.

    Args:
        horizons: Horizon indices to weight.
        T_char: Belief characteristic timescale in seconds.
        alpha: Decay rate.

    Returns:
        Normalized weight dict ``{horizon_idx: weight}``.
    """
    closest_h = min(horizons, key=lambda h: abs(HORIZON_SECONDS[h] - T_char))
    return scale_matched_weights(closest_h, horizons, alpha)
