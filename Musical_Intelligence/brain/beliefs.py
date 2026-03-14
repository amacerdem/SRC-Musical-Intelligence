"""Belief computation — derives 131 belief traces from mechanism outputs.

Each belief's value at time t is:
    belief[t] = Σ(source_dim_value[t] × weight)

Source dims reference mechanism output dimensions by name
(e.g., "P0:consonance_signal" → BCH dim index 8).

Variance recovery is applied at the mechanism level: each mechanism
dimension is percentile-stretched to [0, 1] before the weighted sum,
so that downstream beliefs and dimensions see full dynamic contrast.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np

_REGISTRY_PATH = Path(__file__).resolve().parent.parent / "data" / "beliefs_registry.json"

_BELIEFS_CACHE: List[Dict[str, Any]] | None = None


def get_beliefs_registry() -> List[Dict[str, Any]]:
    global _BELIEFS_CACHE
    if _BELIEFS_CACHE is None:
        with open(_REGISTRY_PATH, encoding="utf-8") as f:
            _BELIEFS_CACHE = json.load(f)
    return _BELIEFS_CACHE


def build_dim_lookup(nuclei) -> Dict[str, Tuple[str, int]]:
    """Build a lookup: (mechanism_name, dim_name) → (mechanism_name, dim_index)."""
    lookup: Dict[str, Tuple[str, int]] = {}
    for n in nuclei:
        dims = n.dimension_names
        if not dims:
            continue
        for i, name in enumerate(dims):
            lookup[(n.NAME, name)] = (n.NAME, i)
            if ":" in name:
                bare = name.split(":", 1)[1]
                key = (n.NAME, bare)
                if key not in lookup:
                    lookup[key] = (n.NAME, i)
    return lookup


def normalize_mechanism_outputs(
    relays: Dict[str, np.ndarray],
    *,
    pct_lo: float = 2.0,
    pct_hi: float = 98.0,
    min_range: float = 0.01,
) -> Dict[str, np.ndarray]:
    """Recover dynamic range at the mechanism output level.

    Stretches each mechanism dimension independently using robust
    percentile bounds so every dim contributes full observed contrast.
    """
    normalized: Dict[str, np.ndarray] = {}
    for name, data in relays.items():
        out = data.copy()
        for d in range(data.shape[1]):
            col = data[:, d]
            lo = np.percentile(col, pct_lo)
            hi = np.percentile(col, pct_hi)
            rng = hi - lo
            if rng < min_range:
                continue
            out[:, d] = np.clip((col - lo) / rng, 0.0, 1.0)
        normalized[name] = out
    return normalized


def compute_beliefs(
    relays: Dict[str, np.ndarray],
    nuclei,
    *,
    normalize: bool = True,
) -> np.ndarray:
    """Compute 131 belief traces from mechanism outputs.

    Args:
        relays: Dict mapping mechanism NAME → (T, D) numpy array.
        nuclei: List of mechanism instances (for dimension_names lookup).
        normalize: If True, apply per-mechanism-dim percentile normalization.

    Returns:
        (T, 131) float32 array of belief values.
    """
    if normalize:
        relays = normalize_mechanism_outputs(relays)

    beliefs_reg = get_beliefs_registry()
    dim_lookup = build_dim_lookup(nuclei)
    n_beliefs = len(beliefs_reg)

    T = 0
    for arr in relays.values():
        T = arr.shape[0]
        break

    result = np.zeros((T, n_beliefs), dtype=np.float32)

    for belief in beliefs_reg:
        idx = belief["index"]
        mech_name = belief["mechanism"]
        source_dims = belief.get("sourceDims", [])

        if mech_name not in relays:
            continue

        mech_output = relays[mech_name]

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

        result[:, idx] = np.clip(value, 0.0, 1.0)

    return result
