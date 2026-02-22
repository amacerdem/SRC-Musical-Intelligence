"""RIRI E-Layer -- Extraction (3D).

Multi-modal rehabilitation entrainment signals from H3 + R3 features:
  E0: multimodal_entrainment  (multi-modal rhythmic phase-locking quality)
  E1: sensorimotor_integration (cross-modal sensorimotor coupling)
  E2: enhanced_recovery        (integration synergy -- multi > unimodal)

RAS (Rhythmic Auditory Stimulation) drives motor optimization via
reticulospinal pathways.  Multi-modal delivery (auditory + visual VR +
haptic robotics) converges on SMA / premotor cortex for period
entrainment.

H3 consumed (E-layer only):
  (10, 6, 0, 0)   spectral_flux value H6 L0         -- onset detection at beat level
  (10, 6, 17, 0)  spectral_flux peaks H6 L0         -- beat count per 200ms window
  (11, 6, 0, 0)   onset_strength value H6 L0        -- event onset precision
  (11, 6, 14, 2)  onset_strength periodicity H6 L2  -- rhythmic regularity
  (25, 6, 0, 2)   x_l0l5[0] value H6 L2            -- entrainment coupling
  (8, 11, 1, 0)   loudness mean H11 L0              -- motor drive intensity
  (33, 11, 0, 2)  x_l4l5[0] value H11 L2           -- sensorimotor coupling
  (33, 11, 17, 0) x_l4l5[0] peaks H11 L0           -- sensorimotor peak events
  (22, 11, 14, 2) energy_change periodicity H11 L2  -- intensity regularity
  (41, 16, 1, 0)  x_l5l7[0] mean H16 L0            -- mean connectivity coupling
  (4, 16, 1, 0)   sensory_pleasantness mean H16 L0  -- sustained pleasantness

R3 used:
  [10] spectral_flux       -- onset detection trigger
  [11] onset_strength      -- beat precision
  [25:33] x_l0l5           -- auditory-motor coupling (mean of 8D)

See Building/C3-Brain/F4-Memory-Systems/mechanisms/riri/RIRI-extraction.md
Thaut 2015: period entrainment via reticulospinal pathways.
Harrison 2025: SMA + putamen activation during musically-cued movement.
Blasi 2025: structural + functional neuroplasticity from music rehab (20 RCTs).
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed (E-layer) ------------------------------------------------
_FLUX_H6_VAL = (10, 6, 0, 0)          # spectral_flux value H6 L0
_FLUX_H6_PEAKS = (10, 6, 17, 0)       # spectral_flux peaks H6 L0
_ONSET_H6_VAL = (11, 6, 0, 0)         # onset_strength value H6 L0
_ONSET_H6_PERIOD = (11, 6, 14, 2)     # onset_strength periodicity H6 L2
_COUPLING_L0L5_H6_VAL = (25, 6, 0, 2) # x_l0l5 value H6 L2
_LOUD_H11_MEAN = (8, 11, 1, 0)        # loudness mean H11 L0
_COUPLING_L4L5_H11_VAL = (33, 11, 0, 2)  # x_l4l5 value H11 L2
_COUPLING_L4L5_H11_PEAKS = (33, 11, 17, 0)  # x_l4l5 peaks H11 L0
_ENERGY_H11_PERIOD = (22, 11, 14, 2)  # energy_change periodicity H11 L2
_CONN_H16_MEAN = (41, 16, 1, 0)       # x_l5l7 mean H16 L0
_PLEASANT_H16_MEAN = (4, 16, 1, 0)    # sensory_pleasantness mean H16 L0

# -- R3 indices (post-freeze 97D) -----------------------------------------------
_R3_SPECTRAL_FLUX = 10       # onset detection trigger
_R3_ONSET_STRENGTH = 11      # beat precision
_R3_X_L0L5_START = 25        # auditory-motor coupling (8D)
_R3_X_L0L5_END = 33


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute E-layer: multi-modal rehabilitation entrainment extraction.

    E0 (multimodal_entrainment) tracks how strongly all modality channels
    lock to a common rhythmic clock.  Spectral flux and onset strength at
    beat level (H6, 200ms) combine with auditory-motor coupling (x_l0l5)
    and onset periodicity.
    Thaut 2015: period entrainment drives motor optimization.

    E1 (sensorimotor_integration) measures cross-modal prediction coupling
    in cerebellum / IPL.  Loudness provides motor drive intensity, x_l4l5
    captures sensorimotor prediction, energy periodicity reflects rhythmic
    regularity.
    Harrison 2025: cerebellum activated during internal cueing.

    E2 (enhanced_recovery) captures multi-modal synergy exceeding unimodal
    RAS.  Connectivity coupling (x_l5l7) plus sensory pleasantness, gated
    by the product of E0 and E1.
    Blasi 2025: structural neuroplasticity from music-based rehabilitation.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``

    Returns:
        ``(E0, E1, E2)`` each ``(B, T)``
    """
    # -- H3 features -------------------------------------------------------
    flux_val = h3_features[_FLUX_H6_VAL]             # (B, T)
    onset_val = h3_features[_ONSET_H6_VAL]           # (B, T)
    onset_period = h3_features[_ONSET_H6_PERIOD]     # (B, T)
    coupling_l0l5_val = h3_features[_COUPLING_L0L5_H6_VAL]  # (B, T)

    loud_mean = h3_features[_LOUD_H11_MEAN]          # (B, T)
    coupling_l4l5_val = h3_features[_COUPLING_L4L5_H11_VAL]  # (B, T)
    energy_period = h3_features[_ENERGY_H11_PERIOD]  # (B, T)

    conn_mean = h3_features[_CONN_H16_MEAN]          # (B, T)
    pleasant_mean = h3_features[_PLEASANT_H16_MEAN]  # (B, T)

    # -- R3 features (used for gating / anchoring) -------------------------
    r3_flux = r3_features[..., _R3_SPECTRAL_FLUX]    # (B, T)
    r3_onset = r3_features[..., _R3_ONSET_STRENGTH]  # (B, T)
    # Mean auditory-motor coupling band (8D -> scalar)
    beat_induction = r3_features[..., _R3_X_L0L5_START:_R3_X_L0L5_END].mean(dim=-1)

    # -- E0: Multimodal Entrainment ----------------------------------------
    # Multi-modal rhythmic entrainment: SMA + premotor convergent temporal
    # input.  Thaut 2015: period entrainment via reticulospinal pathways.
    # f01 = sigma(0.35*flux*onset*mean(beat_induction) + 0.35*coupling + 0.30*onset_period)
    e0 = torch.sigmoid(
        0.35 * flux_val * onset_val * beat_induction
        + 0.35 * coupling_l0l5_val
        + 0.30 * onset_period
    )

    # -- E1: Sensorimotor Integration -------------------------------------
    # Cross-modal sensorimotor integration: cerebellum + IPL prediction.
    # Harrison 2025: SMA + putamen + sensorimotor cortex activation.
    # f02 = sigma(0.35*loudness*motor + 0.35*coupling_l4l5 + 0.30*energy_period)
    e1 = torch.sigmoid(
        0.35 * loud_mean * beat_induction
        + 0.35 * coupling_l4l5_val
        + 0.30 * energy_period
    )

    # -- E2: Enhanced Recovery ---------------------------------------------
    # Integration synergy (multi > uni): hippocampus + mPFC consolidation.
    # Blasi 2025: 20 RCTs (N=718) structural + functional neuroplasticity.
    # f03 = sigma(0.30*connectivity + 0.30*pleasantness + 0.20*f01 + 0.20*f02)
    e2 = torch.sigmoid(
        0.30 * conn_mean
        + 0.30 * pleasant_mean
        + 0.20 * e0
        + 0.20 * e1
    )

    return e0, e1, e2
