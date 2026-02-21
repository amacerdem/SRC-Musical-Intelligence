"""PSCL E-Layer — Extraction (4D).

Instantaneous cortical pitch features from R³ — frame-local, no temporal integration.
Matches Building/C³-Brain/F1-Sensory-Processing/mechanisms/PSCL-extraction.md

Outputs:
    E0: Pitch Salience Raw          [0, 0.90]
    E1: HG Activation Proxy         [0, 0.85]
    E2: Salience Gradient            [0, 0.80]
    E3: Spectral Focus               [0, 1]
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

# ── R³ feature indices (post-freeze 97D) ─────────────────────────────
_PLEAS = 4          # sensory_pleasantness
_INHARM = 5         # inharmonicity
_TONAL = 14         # tonalness
_CLARITY = 15       # clarity
_SMOOTH = 16        # spectral_smoothness
_AUTOCORR = 17      # spectral_autocorrelation
_TRIST1 = 18        # tristimulus1
_ENTROPY = 22       # distribution_entropy
_FLATNESS = 23      # distribution_flatness
_CONC = 24          # distribution_concentration
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

    # E0: Pitch Salience Raw
    e0 = 0.90 * (
        0.40 * r3(_PITCHSAL)
        + 0.35 * r3(_TONAL) * r3(_AUTOCORR)
        + 0.25 * r3(_CONC)
    )

    # E1: HG Activation Proxy
    e1 = 0.85 * (1.0 - r3(_INHARM)) * (
        0.50 * r3(_TRIST1)
        + 0.30 * r3(_SMOOTH)
        + 0.20 * r3(_PITCHSAL)
    )

    # E2: Salience Gradient
    e2 = 0.80 * (1.0 - r3(_ENTROPY)) * (1.0 - r3(_FLATNESS)) * r3(_PLEAS)

    # E3: Spectral Focus
    e3 = r3(_CONC) * r3(_CLARITY) * (1.0 - r3(_FLATNESS))

    return e0, e1, e2, e3
