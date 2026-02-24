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
    # 3. Quote unquoted keys — only at property positions (after { or ,)
    #    Done BEFORE single→double swap so string values are still in
    #    single quotes and can't confuse the regex
    array_str = re.sub(r"([{,])\s*(\w+)\s*:", r'\1 "\2":', array_str)
    # 4. Replace single quotes with double
    array_str = array_str.replace("'", '"')

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
    """Build a lookup: (mechanism_name, dim_name) → (mechanism_name, dim_index).

    Source dims in beliefs use formats like "P0:consonance_signal" or
    sometimes just "consonance_signal" (without scope prefix).
    We index both forms for robust matching.
    """
    lookup: Dict[str, Tuple[str, int]] = {}
    for n in nuclei:
        dims = n.dimension_names
        if not dims:
            continue
        for i, name in enumerate(dims):
            lookup[(n.NAME, name)] = (n.NAME, i)
            # Also index without scope prefix (e.g. "groove_index" for "M0:groove_index")
            if ":" in name:
                bare = name.split(":", 1)[1]
                key = (n.NAME, bare)
                if key not in lookup:  # prefixed form takes priority
                    lookup[key] = (n.NAME, i)
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

            # Handle inversion syntax: "1-V1:mode_signal" → (1 - dim_value)
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
