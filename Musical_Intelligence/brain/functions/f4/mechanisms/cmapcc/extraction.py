"""CMAPCC E-Layer -- Extraction (3D).

Three explicit features modeling cross-modal action-perception common code:

  E0: common_code             -- Unified perception-action representation [0, 1]
  E1: cross_modal_binding     -- Auditory-motor integration strength [0, 1]
  E2: sequence_generalization -- Pattern transfer across modalities [0, 1]

H3 consumed:
    (3, 16, 1, 2)   stumpf_fusion mean H16 L2           -- binding coherence at 1s
    (4, 16, 0, 2)   sensory_pleasantness value H16 L2   -- current sequence valence
    (5, 16, 1, 2)   periodicity mean H16 L2             -- pitch regularity at 1s
    (10, 6, 0, 2)   onset_strength value H6 L2          -- beat-level note onsets
    (8, 6, 0, 2)    loudness value H6 L2                -- beat-level intensity
    (0, 16, 0, 2)   roughness value H16 L2              -- current dissonance
    (1, 16, 1, 2)   sethares_dissonance mean H16 L2     -- interval quality at 1s

R3 consumed:
    [0]      roughness               -- E0: harmonic quality (inverse)
    [1]      sethares_dissonance     -- E0: interval identity
    [3]      stumpf_fusion           -- E0+E2: binding coherence
    [4]      sensory_pleasantness    -- E0: sequence valence
    [5]      periodicity             -- E0+E2: pitch regularity
    [8]      loudness                -- E1: arousal / motor engagement
    [10]     onset_strength          -- E1: event salience / note onset
    [25:33]  x_l0l5                  -- E1: perceptual sequence binding
    [33:41]  x_l4l5                  -- E0: common code basis (derivatives x consonance)
    [41:49]  x_l5l7                  -- E1: cross-modal binding (consonance x timbre)

See Building/C3-Brain/F4-Memory-Systems/mechanisms/cmapcc/CMAPCC-extraction.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_STUMPF_MEAN_1S = (3, 16, 1, 2)
_PLEAS_VAL_1S = (4, 16, 0, 2)
_PERIOD_MEAN_1S = (5, 16, 1, 2)
_ONSET_VAL_H6 = (10, 6, 0, 2)
_LOUD_VAL_H6 = (8, 6, 0, 2)
_ROUGH_VAL_1S = (0, 16, 0, 2)
_SETH_MEAN_1S = (1, 16, 1, 2)

# -- R3 indices ----------------------------------------------------------------
_ROUGHNESS = 0
_SETHARES = 1
_STUMPF_FUSION = 3
_SENSORY_PLEAS = 4
_PERIODICITY = 5
_LOUDNESS = 8
_ONSET_STRENGTH = 10
_X_L0L5_START = 25
_X_L0L5_END = 33
_X_L4L5_START = 33
_X_L4L5_END = 41
_X_L5L7_START = 41
_X_L5L7_END = 49


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
) -> Tuple[Tensor, Tensor, Tensor]:
    """E-layer: 3D extraction from H3/R3 features.

    Computes the three extraction dimensions for cross-modal common code:
    common_code (E0), cross_modal_binding (E1), and sequence
    generalization (E2).

    Bianco 2016: rIFG BA44 Z=4.29 (dorsal/action convergence),
    BA45 Z=5.12 (ventral/audio convergence), fMRI N=29 pianists.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.

    Returns:
        ``(E0, E1, E2)`` each ``(B, T)``.
    """
    # -- H3 features --
    stumpf_mean_1s = h3_features[_STUMPF_MEAN_1S]
    pleas_val_1s = h3_features[_PLEAS_VAL_1S]
    period_mean_1s = h3_features[_PERIOD_MEAN_1S]
    onset_val_h6 = h3_features[_ONSET_VAL_H6]
    loud_val_h6 = h3_features[_LOUD_VAL_H6]
    rough_val_1s = h3_features[_ROUGH_VAL_1S]
    seth_mean_1s = h3_features[_SETH_MEAN_1S]

    # -- R3 features --
    stumpf = r3_features[..., _STUMPF_FUSION]              # (B, T)
    periodicity = r3_features[..., _PERIODICITY]            # (B, T)
    loudness = r3_features[..., _LOUDNESS]                  # (B, T)
    onset = r3_features[..., _ONSET_STRENGTH]               # (B, T)
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END]  # (B, T, 8)
    x_l4l5 = r3_features[..., _X_L4L5_START:_X_L4L5_END]  # (B, T, 8)
    x_l5l7 = r3_features[..., _X_L5L7_START:_X_L5L7_END]  # (B, T, 8)

    # -- Derived signals --
    # Sequence coherence: binding x regularity (used for E2 retrieval)
    seq_coherence = stumpf * periodicity

    # E0: Common code -- unified perception-action representation
    # f01 = sigma(0.30*x_l4l5.mean + 0.35*stumpf + 0.35*periodicity)
    # x_l4l5 captures temporal dynamics coupled with pitch identity --
    # the perception-action bridge.
    # Bianco 2016: rIFG BA44 Z=4.29 dorsal convergence
    e0 = torch.sigmoid(
        0.30 * x_l4l5.mean(dim=-1)
        + 0.35 * stumpf
        + 0.35 * periodicity
    )

    # E1: Cross-modal binding -- auditory-motor integration strength
    # f02 = sigma(0.35*x_l5l7.mean + 0.35*x_l0l5.mean + 0.30*onset*loudness)
    # Moller 2021: left IFOF FA correlates with cross-modal gain
    # (t=3.38, p<0.001, DTI, N=45)
    e1 = torch.sigmoid(
        0.35 * x_l5l7.mean(dim=-1)
        + 0.35 * x_l0l5.mean(dim=-1)
        + 0.30 * onset * loudness
    )

    # Retrieval signal for E2 (from mnemonic context)
    retrieval = 0.50 * stumpf_mean_1s + 0.50 * period_mean_1s

    # E2: Sequence generalization -- pattern transfer across modalities
    # f03 = sigma(0.50*f01*f02 + 0.25*seq_coherence + 0.25*retrieval)
    # Product f01*f02 ensures both common code and cross-modal binding
    # must be active for generalization.
    # Di Liberto 2021: melody decoding from listening and imagery
    # (note-onset F(1,20)=80.6, p=1.9e-8, EEG, N=21)
    e2 = torch.sigmoid(
        0.50 * e0 * e1
        + 0.25 * seq_coherence
        + 0.25 * retrieval
    )

    return e0, e1, e2
