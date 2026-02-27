"""Belief horizon decomposition — per-band and per-law belief traces.

For each belief, re-runs its mechanism with filtered H³ features to show
how different temporal scales (micro/meso/macro/ultra) and integration
laws (L0-memory/L1-prediction/L2-integration) contribute to the belief value.

Key insight: mechanism compute() functions use h3_features.get(key, zeros),
so missing H³ tuples gracefully fall back to zeros. We filter h3_features
and re-run the mechanism to get partial outputs.
"""
from __future__ import annotations

from typing import Any, Dict, List, Set, Tuple

import numpy as np
import torch
from torch import Tensor

from .beliefs import compute_beliefs, get_beliefs_registry, build_dim_lookup

# ---------------------------------------------------------------------------
# Horizon band definitions
# ---------------------------------------------------------------------------

HORIZON_BANDS = {
    "micro": set(range(0, 8)),    # H0-H7: <250ms
    "meso": set(range(8, 16)),    # H8-H15: 300ms-800ms
    "macro": set(range(16, 24)),  # H16-H23: 1s-25s
    "ultra": set(range(24, 32)),  # H24-H31: 36s-981s
}

BAND_ORDER = ("micro", "meso", "macro", "ultra")
LAW_ORDER = (0, 1, 2)
LAW_NAMES = {0: "memory", 1: "prediction", 2: "integration"}

# Variant keys for the output dict
VARIANT_KEYS = (
    "full",
    "band_micro", "band_meso", "band_macro", "band_ultra",
    "law_0", "law_1", "law_2",
)


# ---------------------------------------------------------------------------
# H³ filtering
# ---------------------------------------------------------------------------

def _filter_h3_by_band(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    band_horizons: Set[int],
) -> Dict[Tuple[int, int, int, int], Tensor]:
    """Keep only H³ tuples whose horizon index is in band_horizons."""
    return {k: v for k, v in h3_features.items() if k[1] in band_horizons}


def _filter_h3_by_law(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    law_idx: int,
) -> Dict[Tuple[int, int, int, int], Tensor]:
    """Keep only H³ tuples with a specific law index."""
    return {k: v for k, v in h3_features.items() if k[3] == law_idx}


# ---------------------------------------------------------------------------
# Mechanism-specific H³ filtering
# ---------------------------------------------------------------------------

def _get_mechanism_h3_keys(mechanism) -> Set[Tuple[int, int, int, int]]:
    """Get the set of H³ tuple keys that a mechanism demands."""
    keys = set()
    for spec in mechanism.h3_demand:
        keys.add(spec.as_tuple())
    return keys


def _filter_h3_for_mechanism(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    mech_keys: Set[Tuple[int, int, int, int]],
) -> Dict[Tuple[int, int, int, int], Tensor]:
    """Keep only H³ tuples that a mechanism actually demands."""
    return {k: v for k, v in h3_features.items() if k in mech_keys}


# ---------------------------------------------------------------------------
# Check which bands/laws a mechanism actually uses
# ---------------------------------------------------------------------------

def _mechanism_active_bands(mech_keys: Set[Tuple[int, int, int, int]]) -> Dict[str, bool]:
    """Return which bands have at least one H³ demand."""
    horizons_used = {k[1] for k in mech_keys}
    return {
        band: bool(horizons_used & band_set)
        for band, band_set in HORIZON_BANDS.items()
    }


def _mechanism_active_laws(mech_keys: Set[Tuple[int, int, int, int]]) -> Dict[int, bool]:
    """Return which laws have at least one H³ demand."""
    laws_used = {k[3] for k in mech_keys}
    return {law: law in laws_used for law in LAW_ORDER}


# ---------------------------------------------------------------------------
# Core decomposition computation
# ---------------------------------------------------------------------------

def compute_belief_decomposition(
    nuclei: List[Any],
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
) -> Dict[str, Dict[str, np.ndarray]]:
    """Compute per-band and per-law belief traces via H³ ablation.

    For each mechanism used by beliefs:
    1. Run with full H³ → full belief values
    2. Run with band-filtered H³ → per-band belief values
    3. Run with law-filtered H³ → per-law belief values

    Only processes Relay-type mechanisms (depth 0) that read R³+H³ directly.
    Non-relay mechanisms would need upstream relay outputs, which complicates
    the ablation approach.

    Args:
        nuclei: All mechanism instances.
        h3_features: Full H³ feature dict {(r3_idx, horizon, morph, law): (B, T)}.
        r3_features: (B, T, 97) R³ features.

    Returns:
        Dict mapping belief_name → {variant_key: (T,) numpy array}.
        Variant keys: full, band_micro, band_meso, band_macro, band_ultra,
                      law_0, law_1, law_2.
        Only non-empty variants are included (e.g., if mechanism has no L1
        tuples, law_1 is omitted).
    """
    from Musical_Intelligence.contracts.bases.nucleus import Relay

    beliefs_reg = get_beliefs_registry()
    dim_lookup = build_dim_lookup(nuclei)

    # Group beliefs by mechanism
    mech_beliefs: Dict[str, List[Dict]] = {}
    for belief in beliefs_reg:
        mech = belief["mechanism"]
        if mech not in mech_beliefs:
            mech_beliefs[mech] = []
        mech_beliefs[mech].append(belief)

    # Build mechanism name → instance lookup (only Relays)
    mech_instances: Dict[str, Any] = {}
    for n in nuclei:
        if isinstance(n, Relay):
            mech_instances[n.NAME] = n

    result: Dict[str, Dict[str, np.ndarray]] = {}

    for mech_name, beliefs in mech_beliefs.items():
        if mech_name not in mech_instances:
            continue

        mechanism = mech_instances[mech_name]
        mech_keys = _get_mechanism_h3_keys(mechanism)
        active_bands = _mechanism_active_bands(mech_keys)
        active_laws = _mechanism_active_laws(mech_keys)

        # Scope H³ to this mechanism's demands for efficiency
        mech_h3 = _filter_h3_for_mechanism(h3_features, mech_keys)

        # Full run (baseline)
        with torch.no_grad():
            full_output = mechanism.compute(mech_h3, r3_features)
        full_np = full_output[0].cpu().numpy()  # (T, D)

        # Band-ablated runs
        band_outputs: Dict[str, np.ndarray] = {}
        for band_name in BAND_ORDER:
            if not active_bands[band_name]:
                continue
            filtered = _filter_h3_by_band(mech_h3, HORIZON_BANDS[band_name])
            if not filtered:
                continue
            with torch.no_grad():
                out = mechanism.compute(filtered, r3_features)
            band_outputs[f"band_{band_name}"] = out[0].cpu().numpy()

        # Law-ablated runs
        law_outputs: Dict[str, np.ndarray] = {}
        for law_idx in LAW_ORDER:
            if not active_laws[law_idx]:
                continue
            filtered = _filter_h3_by_law(mech_h3, law_idx)
            if not filtered:
                continue
            with torch.no_grad():
                out = mechanism.compute(filtered, r3_features)
            law_outputs[f"law_{law_idx}"] = out[0].cpu().numpy()

        # Compute belief values from each variant's mechanism output
        T = full_np.shape[0]
        for belief in beliefs:
            belief_name = belief["name"]
            source_dims = belief.get("sourceDims", [])
            variants: Dict[str, np.ndarray] = {}

            # Compute belief value from a mechanism output array
            def _belief_from_output(mech_output: np.ndarray) -> np.ndarray:
                value = np.zeros(T, dtype=np.float32)
                for sd in source_dims:
                    dim_name = sd["name"]
                    weight = sd["weight"]
                    invert = False
                    if dim_name.startswith("1-"):
                        dim_name = dim_name[2:]
                        invert = True
                    key = (mech_name, dim_name)
                    if key not in dim_lookup:
                        continue
                    _, dim_idx = dim_lookup[key]
                    if dim_idx < mech_output.shape[1]:
                        dim_val = mech_output[:, dim_idx]
                        if invert:
                            dim_val = 1.0 - dim_val
                        value += dim_val * weight
                return np.clip(value, 0.0, 1.0)

            # Full
            variants["full"] = _belief_from_output(full_np)

            # Bands
            for key, arr in band_outputs.items():
                variants[key] = _belief_from_output(arr)

            # Laws
            for key, arr in law_outputs.items():
                variants[key] = _belief_from_output(arr)

            result[belief_name] = variants

    return result


# ---------------------------------------------------------------------------
# Atlas: per-mechanism H³ demand statistics
# ---------------------------------------------------------------------------

def build_mechanism_atlas(nuclei: List[Any]) -> Dict[str, Dict]:
    """Build H³ demand statistics per mechanism for the frontend atlas.

    Returns:
        Dict mapping mechanism_name → {
            totalDemands: int,
            bands: [{band, tupleCount, horizons, laws}],
            laws: [{law, lawName, tupleCount, horizons}],
        }
    """
    from Musical_Intelligence.contracts.bases.nucleus import Relay

    atlas: Dict[str, Dict] = {}

    for n in nuclei:
        if not isinstance(n, Relay):
            continue

        mech_keys = _get_mechanism_h3_keys(n)
        if not mech_keys:
            continue

        # Band breakdown
        bands = []
        for band_name in BAND_ORDER:
            band_tuples = {k for k in mech_keys if k[1] in HORIZON_BANDS[band_name]}
            if band_tuples:
                bands.append({
                    "band": band_name,
                    "tupleCount": len(band_tuples),
                    "horizons": sorted({k[1] for k in band_tuples}),
                    "laws": sorted({k[3] for k in band_tuples}),
                })

        # Law breakdown
        laws = []
        for law_idx in LAW_ORDER:
            law_tuples = {k for k in mech_keys if k[3] == law_idx}
            if law_tuples:
                laws.append({
                    "law": law_idx,
                    "lawName": LAW_NAMES[law_idx],
                    "tupleCount": len(law_tuples),
                    "horizons": sorted({k[1] for k in law_tuples}),
                })

        atlas[n.NAME] = {
            "totalDemands": len(mech_keys),
            "bands": bands,
            "laws": laws,
        }

    return atlas
