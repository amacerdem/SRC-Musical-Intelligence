"""BCH E-Layer — Extraction (4D).

Instantaneous sensory features from R³ — frame-local, no temporal integration.
Matches Building/C³-Brain/F1-Sensory-Processing/mechanisms/BCH-extraction.md

Outputs:
    E0: Neural Pitch Salience (nps)         [0, 0.90]
    E1: Harmonicity Index                   [0, 0.85]
    E2: Consonance Hierarchy                [0, 0.80]
    E3: FFR-Behavior Correlation            [0, ~0.71]
"""
from __future__ import annotations

from typing import Tuple

import torch
from torch import Tensor

# ── R³ feature indices (post-freeze 97D) ─────────────────────────────
_ROUGH = 0          # roughness
_SETH = 1           # sethares_dissonance
_HELM = 2           # helmholtz_kang
_STUMP = 3          # stumpf_fusion
_INHARM = 5         # inharmonicity
_TONAL = 14         # tonalness
_AUTOCORR = 17      # spectral_autocorrelation
_TRIST1 = 18        # tristimulus1
_TRIST2 = 19        # tristimulus2
_TRIST3 = 20        # tristimulus3
_PCE = 38           # pitch_class_entropy
_PITCHSAL = 39      # pitch_salience


def compute_extraction(
    r3_features: Tensor,
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """Compute E-layer: 4D instantaneous extraction from R³.

    Args:
        r3_features: ``(B, T, 97)`` R³ spectral features.

    Returns:
        Tuple of (E0, E1, E2, E3), each ``(B, T)``.
    """
    def r3(idx: int) -> Tensor:
        return r3_features[:, :, idx]

    # E0: Neural Pitch Salience
    e0 = 0.90 * (0.5 * r3(_TONAL) * r3(_AUTOCORR) + 0.5 * r3(_PITCHSAL))

    # E1: Harmonicity Index
    trist_std = torch.stack(
        [r3(_TRIST1), r3(_TRIST2), r3(_TRIST3)], dim=-1,
    ).std(dim=-1)
    trist_balance = (1.0 - trist_std).clamp(0, 1)
    e1 = 0.85 * (1.0 - r3(_INHARM)) * (
        0.5 * trist_balance + 0.5 * (1.0 - r3(_PCE))
    )

    # E2: Consonance Hierarchy
    e2 = 0.80 * r3(_HELM) * r3(_STUMP)

    # E3: FFR-Behavior Correlation
    e3 = 0.81 * (e0 + e1) / 2.0

    return e0, e1, e2, e3
