"""CSG P-Layer — Cognitive Present (3D).

Three present-processing dimensions for consonance-salience:

  P0: salience_network       — Attention-gated salience [0, 1]
  P1: affective_evaluation   — Salience-weighted valence [-1, 1] (tanh)
  P2: sensory_load           — Processing demand [0, 1]

H3 consumed:
    (17, 3, 0, 2)   spectral_auto H3 val L2      — cross-band salience coupling
    (10, 3, 0, 2)   loudness H3 val L2            — intensity for salience
    (22, 3, 8, 0)   energy_change H3 vel L0       — energy dynamics
    (4, 3, 0, 2)    sensory_pleas H3 val L2       — consonance (reused)
    (0, 3, 1, 2)    roughness H3 mean L2          — dissonance context
    (21, 4, 8, 0)   spectral_flux H4 vel L0       — spectral dynamics
    (1, 8, 8, 0)    sethares H8 vel L0            — dissonance velocity
    (17, 8, 0, 2)   spectral_auto H8 val L2       — medium-term coupling
    (10, 16, 1, 2)  loudness H16 mean L2          — sustained intensity

R3 consumed:
    [4] sensory_pleasantness — for ambiguity computation

See Building/C3-Brain/F1-Sensory-Processing/mechanisms/csg/CSG-cognitive-present.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_SPECTRAL_AUTO_H3 = (17, 3, 0, 2)
_LOUDNESS_H3 = (10, 3, 0, 2)
_ENERGY_VEL = (22, 3, 8, 0)
_PLEAS_H3 = (4, 3, 0, 2)
_ROUGHNESS_MEAN = (0, 3, 1, 2)
_SPECTRAL_FLUX_VEL = (21, 4, 8, 0)
_SETHARES_VEL = (1, 8, 8, 0)
_SPECTRAL_AUTO_H8 = (17, 8, 0, 2)
_LOUDNESS_MEAN_1S = (10, 16, 1, 2)

# -- R3 indices ----------------------------------------------------------------
_PLEAS = 4


def compute_cognitive_present(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """P-layer: 3D present processing from H3/R3 + E/M outputs.

    Args:
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(E0, E1, E2)`` each ``(B, T)``.
        m_outputs: ``(M0, M1, M2)`` each ``(B, T)``.

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``. P1 is tanh-valued ``[-1, 1]``.
    """
    _e0, _e1, e2 = e_outputs
    (m0, _m1, _m2) = m_outputs

    spectral_auto_h3 = h3_features[_SPECTRAL_AUTO_H3]
    loudness_h3 = h3_features[_LOUDNESS_H3]
    energy_vel = h3_features[_ENERGY_VEL]
    pleas_h3 = h3_features[_PLEAS_H3]
    roughness_mean = h3_features[_ROUGHNESS_MEAN]
    spectral_flux_vel = h3_features[_SPECTRAL_FLUX_VEL]
    sethares_vel = h3_features[_SETHARES_VEL]
    spectral_auto_h8 = h3_features[_SPECTRAL_AUTO_H8]
    loudness_mean_1s = h3_features[_LOUDNESS_MEAN_1S]

    consonance = r3_features[:, :, _PLEAS]
    ambiguity = 1.0 - torch.abs(consonance - 0.5) * 2

    # P0: Salience network — attention-gated consonance salience
    # Koelsch: dissonant -> amygdala/hippocampus; consonant -> AI/HG/NAc
    p0 = torch.sigmoid(
        0.30 * m0 + 0.25 * spectral_auto_h3
        + 0.25 * loudness_h3 + 0.20 * energy_vel
    )

    # P1: Affective evaluation — consonance-weighted valence [-1, 1]
    # Kim: vmPFC/NAc valence integration
    p1 = torch.tanh(
        0.50 * e2
        + 0.30 * (pleas_h3 - roughness_mean)
        + 0.20 * spectral_flux_vel
    )

    # P2: Sensory load — processing demand
    # Bravo 2017: intermediate dissonance -> increased HG load
    p2 = torch.sigmoid(
        0.30 * ambiguity + 0.25 * sethares_vel
        + 0.25 * spectral_auto_h8 + 0.20 * loudness_mean_1s
    )

    return p0, p1, p2
