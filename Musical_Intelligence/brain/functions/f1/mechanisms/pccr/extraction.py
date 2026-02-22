"""PCCR E-Layer — Extraction (4D).

Instantaneous pitch-class (chroma) features from R³ — frame-local, no temporal
integration, no upstream dependency.
Matches Building/C³-Brain/F1-Sensory-Processing/mechanisms/pccr/PCCR-extraction.md

Outputs:
    E0: Chroma Energy           [0, 0.95]
    E1: Chroma Clarity          [0, 0.90]
    E2: Octave Coherence        [0, 0.85]
    E3: Pitch Class Confidence  [0, 0.90]
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

# ── R³ feature indices (post-freeze 97D) ─────────────────────────────
_INHARM = 5          # inharmonicity
_TONAL = 14          # tonalness
_AUTOCORR = 17       # spectral_autocorrelation
_CHROMA_START = 25   # chroma bin C
_CHROMA_END = 37     # chroma bin B (exclusive)
_PCE = 38            # pitch_class_entropy
_PITCHSAL = 39       # pitch_salience


def compute_extraction(
    r3_features: Tensor,
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """Compute E-layer: 4D instantaneous chroma extraction from R³.

    Args:
        r3_features: ``(B, T, 97)`` R³ spectral features.

    Returns:
        Tuple of (E0, E1, E2, E3), each ``(B, T)``.
    """
    def r3(idx: int) -> Tensor:
        return r3_features[:, :, idx]

    chroma = r3_features[:, :, _CHROMA_START:_CHROMA_END]  # (B, T, 12)
    chroma_peak = chroma.max(dim=-1).values  # (B, T)

    # E0: Chroma Energy — peak chroma bin × pitch salience gate
    e0 = 0.95 * chroma_peak * r3(_PITCHSAL)

    # E1: Chroma Clarity — low PCE × tonalness
    e1 = 0.90 * (1.0 - r3(_PCE)) * r3(_TONAL)

    # E2: Octave Coherence — low inharmonicity × spectral autocorrelation
    e2 = 0.85 * (1.0 - r3(_INHARM)) * r3(_AUTOCORR)

    # E3: Pitch Class Confidence — multi-indicator quality check
    e3 = 0.90 * (
        0.40 * r3(_PITCHSAL)
        + 0.30 * (1.0 - r3(_PCE))
        + 0.30 * r3(_TONAL)
    )

    return e0, e1, e2, e3
