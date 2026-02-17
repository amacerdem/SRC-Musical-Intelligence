"""FeatureNormalizer -- per-group normalization to [0, 1].

Each R3 spectral group produces features with different raw ranges.  This
module applies the documented normalization method per group so that every
feature in the final 97-D vector is in [0, 1].

Since each group's ``compute()`` method already applies its own
normalization internally (sigmoid, ratio, max-norm, etc.), this normalizer
serves as a **safety clamp** and an optional post-processing step for
groups that defer normalization to the pipeline level.

Source of truth
---------------
- Docs/R3/Pipeline/Normalization.md
- Docs/R3/R3-SPECTRAL-ARCHITECTURE.md  Section 6
"""

from __future__ import annotations

from typing import Dict

import torch
from torch import Tensor


# ======================================================================
# Normalization strategies
# ======================================================================

def _clamp_01(x: Tensor) -> Tensor:
    """Safety clamp to [0, 1]."""
    return x.clamp(0.0, 1.0)


def _sigmoid(x: Tensor, gain: float = 1.0) -> Tensor:
    """Sigmoid normalization: maps (-inf, inf) → (0, 1)."""
    return torch.sigmoid(x * gain)


def _max_norm(x: Tensor) -> Tensor:
    """Batch max normalization: x / max(x)."""
    x_max = x.amax(dim=-2, keepdim=True).clamp(min=1e-8)
    return x / x_max


def _affine_neg1_pos1(x: Tensor) -> Tensor:
    """Affine map [-1, 1] → [0, 1]: (x + 1) / 2."""
    return (x + 1.0) / 2.0


# ======================================================================
# Per-group normalization config
# ======================================================================
# Each group's compute() already applies normalization, so the pipeline
# normalizer acts as a safety net.  The primary method is "clamp" for
# most groups, with group-specific overrides for edge cases.

_GROUP_METHODS: Dict[str, str] = {
    "consonance":      "clamp",       # mixed sigmoid/ratio/composite
    "energy":          "clamp",       # mixed max-norm/sigmoid
    "timbre":          "clamp",       # ratio/complement/clamp
    "change":          "clamp",       # max-norm/ratio/clamp
    "pitch_chroma":    "clamp",       # L1-norm/min-max/ratio
    "rhythm_groove":   "clamp",       # min-max/sigmoid/ratio
    "harmony":         "clamp",       # min-max/affine/ratio
    "timbre_extended": "clamp",       # per-coeff/clamp
    "modulation":      "clamp",       # per-rate max-norm/sigmoid
}


class FeatureNormalizer:
    """Per-group normalization ensuring all R3 features are in [0, 1].

    Since each group's ``compute()`` already normalizes internally, this
    normalizer primarily applies a safety clamp.  It can be extended with
    group-specific post-processing if needed.

    Usage
    -----
    ::

        normalizer = FeatureNormalizer()
        clamped = normalizer.normalize(features, "consonance")
        all_clamped = normalizer.normalize_all(features_dict)
    """

    def normalize(self, features: Tensor, group_name: str) -> Tensor:
        """Apply normalization for a single group.

        Parameters
        ----------
        features : Tensor
            ``(B, T, group_dim)`` output from a spectral group.
        group_name : str
            Canonical group name (e.g. ``"consonance"``).

        Returns
        -------
        Tensor
            ``(B, T, group_dim)`` with all values in ``[0, 1]``.
        """
        method = _GROUP_METHODS.get(group_name, "clamp")

        if method == "clamp":
            return _clamp_01(features)
        elif method == "sigmoid":
            return _clamp_01(_sigmoid(features))
        elif method == "max_norm":
            return _clamp_01(_max_norm(features))
        elif method == "affine":
            return _clamp_01(_affine_neg1_pos1(features))
        else:
            return _clamp_01(features)

    def normalize_all(
        self, features_dict: Dict[str, Tensor]
    ) -> Dict[str, Tensor]:
        """Apply normalization to all groups.

        Parameters
        ----------
        features_dict : dict
            Mapping from group name to ``(B, T, group_dim)`` tensors.

        Returns
        -------
        dict
            Same mapping with normalized tensors, all in ``[0, 1]``.
        """
        return {
            name: self.normalize(tensor, name)
            for name, tensor in features_dict.items()
        }

    def __repr__(self) -> str:
        return f"FeatureNormalizer(groups={len(_GROUP_METHODS)})"
