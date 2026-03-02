"""SNEM E-Layer — Extraction (3D).

Three explicit features modeling beat entrainment and selective enhancement:

  E0: beat_entrainment         — Beat-frequency periodicity [0, 1]
  E1: meter_entrainment        — Metric coupling strength [0, 1]
  E2: selective_enhancement    — Enhancement from entrainment x coupling [0, 1]

H3 consumed:
    (8, 20, 14, 0)   loudness periodicity H20 L0    — beat periodicity at 5s
    (11, 20, 14, 0)  onset periodicity H20 L0       — onset periodicity at 5s
    (11, 16, 2, 0)   onset std H16 L0               — onset variability at 1s
    (10, 20, 20, 0)  flux entropy H20 L0            — meter entropy at 5s
    (10, 16, 20, 0)  flux entropy H16 L0            — meter entropy at 1s
    (21, 4, 8, 0)    spectral change velocity H4 L0 — enhancement cue
    (8, 3, 20, 2)    loudness entropy H3 L2         — salience context

Beat periodicity requires a multi-second integration window (H20 = 5s) to
accumulate enough cycles for reliable periodicity estimation. At H16 (1s),
even a single onset produces high periodicity values (0.87–0.95), collapsing
contrast between regular and irregular timing. At H20, isochronous sequences
build up true periodicity (delta = +0.52 loudness, +0.41 onset vs random).

Meter hierarchy uses flux entropy at H16/H20: accented metric patterns
(strong–weak alternation) produce higher spectral entropy than uniform beats,
reflecting the greater spectral diversity of metric accent patterns.

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/snem/SNEM-extraction.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
# Beat (E0): periodicity at 5s integration captures multi-cycle regularity
_LOUD_PERIOD_H20 = (8, 20, 14, 0)       # loudness periodicity at 5s
_ONSET_PERIOD_H20 = (11, 20, 14, 0)     # onset periodicity at 5s
_ONSET_STD_H16 = (11, 16, 2, 0)         # onset variability at 1s

# Meter (E1): entropy captures accent-pattern diversity
_FLUX_ENTROPY_H20 = (10, 20, 20, 0)     # flux entropy at 5s
_FLUX_ENTROPY_H16 = (10, 16, 20, 0)     # flux entropy at 1s

# Selective (E2): short-term enhancement cues
_SPECTRAL_CHANGE_VEL = (21, 4, 8, 0)    # spectral change velocity
_LOUD_ENTROPY = (8, 3, 20, 2)           # loudness entropy 100ms


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """E-layer: 3D extraction from H3 features.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.

    Returns:
        ``(E0, E1, E2)`` each ``(B, T)``.
    """
    loud_period_h20 = h3_features[_LOUD_PERIOD_H20]
    onset_period_h20 = h3_features[_ONSET_PERIOD_H20]
    onset_std_h16 = h3_features[_ONSET_STD_H16]
    flux_entropy_h20 = h3_features[_FLUX_ENTROPY_H20]
    flux_entropy_h16 = h3_features[_FLUX_ENTROPY_H16]
    spectral_change_vel = h3_features[_SPECTRAL_CHANGE_VEL]
    loud_entropy = h3_features[_LOUD_ENTROPY]

    # E0: Beat entrainment — SS-EP at beat frequency
    # Nozaradan 2011: frequency-tagging reveals beat-locked cortical response.
    # H20 periodicity captures multi-cycle regularity (5s window accumulates
    # 10 cycles at 120 BPM). Onset std provides variability context.
    e0 = torch.sigmoid(
        0.40 * loud_period_h20 + 0.35 * onset_period_h20
        + 0.25 * onset_std_h16
    )

    # E1: Meter entrainment — metric coupling strength
    # Grahn 2007: beat perception recruits SMA/BG via metric structure.
    # Flux entropy at multiple scales captures accent-pattern diversity:
    # accented metric patterns (strong-weak) produce higher spectral entropy
    # than uniform beats due to timbral/dynamic variation at accent positions.
    e1 = torch.sigmoid(
        0.50 * flux_entropy_h20 + 0.50 * flux_entropy_h16
    )

    # E2: Selective enhancement — entrainment x coupling driven
    # Nozaradan 2018: selective neural enhancement at beat frequency
    e2 = torch.sigmoid(
        0.35 * e0 * e1 + 0.35 * spectral_change_vel
        + 0.30 * loud_entropy
    )

    return e0, e1, e2
