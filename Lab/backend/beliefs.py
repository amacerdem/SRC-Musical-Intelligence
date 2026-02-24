"""Belief computation — derives 131 belief traces from mechanism outputs.

Each belief's value at time t is:
    belief[t] = Σ(source_dim_value[t] × weight)

Source dims reference mechanism output dimensions by name
(e.g., "P0:consonance_signal" → BCH dim index 8).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np

# ---------------------------------------------------------------------------
# Parse belief registry from frontend
# ---------------------------------------------------------------------------

_BELIEFS_TS = Path(__file__).resolve().parent.parent / "frontend" / "src" / "data" / "beliefs.ts"


def _parse_beliefs_registry() -> List[Dict[str, Any]]:
    """Parse the frontend beliefs.ts into a list of dicts.

    Each dict has: index, name, type, functionId, mechanism, sourceDims[{name, weight}]
    """
    text = _BELIEFS_TS.read_text(encoding="utf-8")

    # Extract the array literal between "export const BELIEFS: BeliefDef[] = [" and the closing "]"
    start = text.index("export const BELIEFS")
    # Skip past "BeliefDef[]" type annotation — find "= [" pattern
    eq_pos = text.index("= [", start)
    bracket_start = eq_pos + 2  # points to the "[" in "= ["

    # Find matching closing bracket
    depth = 0
    for i in range(bracket_start, len(text)):
        if text[i] == "[":
            depth += 1
        elif text[i] == "]":
            depth -= 1
            if depth == 0:
                bracket_end = i
                break

    array_str = text[bracket_start:bracket_end + 1]

    # Convert TS to valid JSON:
    import re
    # 1. Remove comments (// ...)
    array_str = re.sub(r"//[^\n]*", "", array_str)
    # 2. Remove trailing commas before } or ]
    array_str = re.sub(r",\s*([}\]])", r"\1", array_str)
    # 3. Replace single quotes with double BEFORE key quoting
    #    (so dim names like 'P0:salience_network' become "P0:..." first)
    array_str = array_str.replace("'", '"')
    # 4. Quote unquoted keys — negative lookbehind for " avoids
    #    matching colons inside strings like "P0:salience_network"
    array_str = re.sub(r'(?<!")(\b\w+)\s*:', r'"\1":', array_str)

    beliefs = json.loads(array_str)
    return beliefs


# Cache
_BELIEFS_CACHE: List[Dict[str, Any]] | None = None


def get_beliefs_registry() -> List[Dict[str, Any]]:
    global _BELIEFS_CACHE
    if _BELIEFS_CACHE is None:
        _BELIEFS_CACHE = _parse_beliefs_registry()
    return _BELIEFS_CACHE


# ---------------------------------------------------------------------------
# Build dim lookup from mechanism instances
# ---------------------------------------------------------------------------

def build_dim_lookup(nuclei) -> Dict[str, Tuple[str, int]]:
    """Build a lookup: "dim_name" → (mechanism_name, dim_index).

    Source dims in beliefs use the format "P0:consonance_signal",
    which matches the mechanism's dimension_names property.
    """
    lookup: Dict[str, Tuple[str, int]] = {}
    for n in nuclei:
        for i, name in enumerate(n.dimension_names):
            # Key by just the dim name (mechanism is known from belief.mechanism)
            lookup[(n.NAME, name)] = (n.NAME, i)
    return lookup


# ---------------------------------------------------------------------------
# Compute beliefs
# ---------------------------------------------------------------------------

def compute_beliefs(
    relays: Dict[str, np.ndarray],
    nuclei,
) -> np.ndarray:
    """Compute 131 belief traces from mechanism outputs.

    Args:
        relays: Dict mapping mechanism NAME → (T, D) numpy array.
        nuclei: List of mechanism instances (for dimension_names lookup).

    Returns:
        (T, 131) float32 array of belief values.
    """
    beliefs_reg = get_beliefs_registry()
    dim_lookup = build_dim_lookup(nuclei)
    n_beliefs = len(beliefs_reg)

    # Determine T from any relay
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

        mech_output = relays[mech_name]  # (T, D)

        value = np.zeros(T, dtype=np.float32)
        for sd in source_dims:
            dim_name = sd["name"]
            weight = sd["weight"]

            key = (mech_name, dim_name)
            if key not in dim_lookup:
                continue

            _, dim_idx = dim_lookup[key]
            if dim_idx < mech_output.shape[1]:
                value += mech_output[:, dim_idx] * weight

        result[:, idx] = np.clip(value, 0.0, 1.0)

    return result
