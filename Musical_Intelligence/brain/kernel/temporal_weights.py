"""Scale-matched exponential temporal weighting for multi-horizon prediction.

Implements two core weighting functions for C³ multi-scale prediction:

v2.0 — Scale-matched evidence weighting:
    w(h, Δ) = exp(-α |h - Δ|)
    Evidence from H³ at horizon h peaks when h matches prediction target Δ.

v2.2 — Horizon activation (data-readiness gating):
    a(t, T_h) = σ(k · (t / T_h − 1))
    A horizon contributes to reward only after enough elapsed time relative
    to its window length.  Prevents ultra horizons (H24, H28) from producing
    spurious negative reward in early phases when insufficient data exists.

Usage:
    weights = scale_matched_weights(target_h=18, evidence_horizons=CONSONANCE_HORIZONS)
    trend_sum = sum(w * h3_trend[h] for h, w in weights.items())

    rw = activated_reward_weights(elapsed_s=15.0, horizons=CONSONANCE_HORIZONS)
    reward = sum(rw[h] * reward_h for h, reward_h in per_horizon_reward.items())
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


# ---------------------------------------------------------------------------
# Horizon activation — data-readiness gating (v2.2)
# ---------------------------------------------------------------------------

DEFAULT_ACTIVATION_K: float = 5.0
"""Sigmoid steepness for horizon activation.

k=5 gives:
  t = 0.5 × T_h  →  activation ≈ 0.08  (barely active)
  t = 1.0 × T_h  →  activation = 0.50   (half active)
  t = 2.0 × T_h  →  activation ≈ 0.99  (fully active)

For 30s excerpts:
  H5-H21 (≤8s)   →  fully active after first seconds
  H24   (36s)     →  0.30 at 30s, gradually activating
  H28   (414s)    →  0.01 at 30s, essentially silent
"""


def horizon_activation(
    elapsed_s: float,
    horizon_s: float,
    k: float = DEFAULT_ACTIVATION_K,
) -> float:
    """Compute activation level for a single horizon.

    A horizon should contribute to reward in proportion to how much data
    it has seen relative to its window length.  Before ``t = T_h``, the
    horizon has not accumulated a full window of evidence and its
    prediction/PE values are unreliable.

    Args:
        elapsed_s: Elapsed time in seconds since piece start.
        horizon_s: Horizon window duration in seconds.
        k: Sigmoid steepness.

    Returns:
        Activation in (0, 1).  Near 0 when ``t << T_h``,
        0.5 when ``t = T_h``, near 1.0 when ``t >> T_h``.
    """
    x = k * (elapsed_s / (horizon_s + 1e-12) - 1.0)
    # Clamp to avoid overflow in exp
    x = max(-20.0, min(20.0, x))
    return 1.0 / (1.0 + math.exp(-x))


def activated_reward_weights(
    elapsed_s: float,
    horizons: Sequence[int],
    k: float = DEFAULT_ACTIVATION_K,
) -> Dict[int, float]:
    """Compute activation-weighted horizon weights for reward.

    Each horizon's weight is proportional to its activation level (how much
    data it has seen).  Weights are normalized to sum to 1.0.

    This replaces uniform ``1/n_h`` weighting in the reward formula,
    preventing ultra horizons from dominating reward with unreliable PEs.

    Args:
        elapsed_s: Elapsed time in seconds since piece start.
        horizons: Horizon indices.
        k: Sigmoid steepness.

    Returns:
        Normalized weight dict ``{horizon_idx: weight}``.
    """
    raw: Dict[int, float] = {}
    for h in horizons:
        h_seconds = HORIZON_SECONDS[h]
        raw[h] = horizon_activation(elapsed_s, h_seconds, k)

    total = sum(raw.values())
    if total < 1e-12:
        # All horizons inactive (very early frames) — uniform fallback
        n = len(horizons)
        return {h: 1.0 / n for h in horizons}

    return {h: w / total for h, w in raw.items()}
