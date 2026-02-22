"""VRIAP E-Layer -- Extraction (3D).

Episodic engagement features for VR-integrated analgesia:
  E0: motor_engagement       -- Active motor engagement level [0, 1]
  E1: pain_gate              -- Pain gating signal (S1 connectivity reduction) [0, 1]
  E2: multimodal_binding     -- Multi-modal binding strength [0, 1]

Motor engagement (E0) tracks auditory-motor coupling via onset strength
weighted by energy-consonance coupling (x_l0l5) and loudness modulated
by amplitude velocity. Liang 2025: VRMS enhances bilateral PM&SMA FC
vs VRAO (t=3.574, p=0.004 FDR, N=50).

Pain gate (E1) models S1 connectivity reduction driven by motor
engagement * memory retrieval, weighted by pleasantness and low
roughness (safety signal). Liang 2025: RS1 FC t=4.023, p=0.002 FDR.

Multi-modal binding (E2) captures hippocampal integration of auditory,
visual, and motor streams via stumpf fusion x timbre-consonance
coupling (x_l5l7). Bushnell 2013: cognitive-emotional pain control.

H3 demands consumed (7):
  (11, 16, 0, 2) onset_strength value H16 L2   -- motor cueing 1s
  (10, 16, 0, 2) loudness value H16 L2         -- engagement intensity
  (7, 16, 8, 0)  amplitude velocity H16 L0     -- energy change rate
  (4, 16, 0, 2)  sensory_pleasantness value H16 L2 -- comfort level
  (0, 16, 0, 2)  roughness value H16 L2        -- dissonance (inverted)
  (22, 16, 0, 2) entropy value H16 L2          -- unpredictability
  (3, 16, 1, 2)  stumpf_fusion mean H16 L2     -- binding stability

R3 inputs: roughness[0], stumpf_fusion[3], sensory_pleasantness[4],
           amplitude[7], loudness[10], onset_strength[11], entropy[22],
           x_l0l5[25:33], x_l5l7[41:49]

See Building/C3-Brain/F4-Memory-Systems/mechanisms/vriap/VRIAP-extraction.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed ---------------------------------------------------
_ONSET_VAL_H16 = (11, 16, 0, 2)       # onset_strength value H16 L2
_LOUD_VAL_H16 = (10, 16, 0, 2)        # loudness value H16 L2
_AMP_VEL_H16 = (7, 16, 8, 0)          # amplitude velocity H16 L0
_PLEASANT_VAL_H16 = (4, 16, 0, 2)     # sensory_pleasantness value H16 L2
_ROUGH_VAL_H16 = (0, 16, 0, 2)        # roughness value H16 L2
_ENTROPY_VAL_H16 = (22, 16, 0, 2)     # entropy value H16 L2
_STUMPF_MEAN_H16 = (3, 16, 1, 2)      # stumpf_fusion mean H16 L2

# -- R3 feature indices (post-freeze 97D) -------------------------------------
_ROUGHNESS = 0
_STUMPF = 3
_PLEASANTNESS = 4
_AMPLITUDE = 7
_LOUDNESS = 10
_ONSET = 11
_ENTROPY = 22
_X_L0L5_START = 25
_X_L0L5_END = 33
_X_L5L7_START = 41
_X_L5L7_END = 49


def _mnemonic_encoding(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tensor:
    """Memory encoding state -- engagement weighted by H3 onset cueing.

    Returns (B, T) encoding strength in [0, 1].
    """
    onset_val = h3_features[_ONSET_VAL_H16]           # (B, T)
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END]  # (B, T, 8)
    return torch.sigmoid(0.50 * onset_val + 0.50 * x_l0l5.mean(dim=-1))


def _mnemonic_retrieval(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tensor:
    """Memory retrieval state -- pleasantness weighted by low entropy.

    Returns (B, T) retrieval strength in [0, 1].
    """
    pleasant = h3_features[_PLEASANT_VAL_H16]         # (B, T)
    entropy = h3_features[_ENTROPY_VAL_H16]            # (B, T)
    return torch.sigmoid(0.50 * pleasant + 0.50 * (1.0 - entropy))


def compute_extraction(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute E-layer: 3D episodic engagement features.

    E0 (motor_engagement): Active motor engagement from onset strength
    weighted by energy-consonance coupling and loudness * amplitude
    velocity. Liang 2025: PM&SMA FC enhancement in VRMS.

    E1 (pain_gate): S1 connectivity reduction driven by E0 * retrieval
    interaction, weighted by pleasantness and safety (1-roughness).
    Liang 2025: RS1 FC t=4.023, p=0.002 FDR.

    E2 (multimodal_binding): Hippocampal multi-modal binding from
    stumpf fusion * timbre-consonance coupling, memory encoding, and
    low entropy (predictable context). Bushnell 2013: mPFC pathways.

    Args:
        r3_features: ``(B, T, 97)`` R3 spectral features.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.

    Returns:
        ``(E0, E1, E2)`` each ``(B, T)``.
    """
    # -- H3 features --
    onset_val = h3_features[_ONSET_VAL_H16]            # (B, T)
    loud_val = h3_features[_LOUD_VAL_H16]              # (B, T)
    amp_vel = h3_features[_AMP_VEL_H16]                # (B, T)
    pleasant_val = h3_features[_PLEASANT_VAL_H16]      # (B, T)
    rough_val = h3_features[_ROUGH_VAL_H16]            # (B, T)
    entropy_val = h3_features[_ENTROPY_VAL_H16]        # (B, T)
    stumpf_mean = h3_features[_STUMPF_MEAN_H16]        # (B, T)

    # -- R3 features --
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END]  # (B, T, 8)
    x_l5l7 = r3_features[..., _X_L5L7_START:_X_L5L7_END]  # (B, T, 8)

    # -- Mnemonic circuit signals --
    mem_enc = _mnemonic_encoding(r3_features, h3_features)   # (B, T)
    mem_ret = _mnemonic_retrieval(r3_features, h3_features)  # (B, T)

    # -- E0: Motor Engagement --
    # f01 = sigma(0.35*onset*x_l0l5.mean + 0.35*loudness*amp_vel + 0.30*mem_enc)
    # Liang 2025: VRMS enhances bilateral PM&SMA FC (t=3.574, p=0.004 FDR)
    e0 = torch.sigmoid(
        0.35 * onset_val * x_l0l5.mean(dim=-1)
        + 0.35 * loud_val * amp_vel
        + 0.30 * mem_enc
    )

    # -- E1: Pain Gate --
    # f02 = sigma(0.40*f01*mem_ret + 0.30*pleasantness + 0.30*(1-roughness))
    # Liang 2025: RS1 FC t=4.023, p=0.002 FDR (N=50)
    e1 = torch.sigmoid(
        0.40 * e0 * mem_ret
        + 0.30 * pleasant_val
        + 0.30 * (1.0 - rough_val)
    )

    # -- E2: Multi-modal Binding --
    # f03 = sigma(0.35*stumpf*x_l5l7.mean + 0.35*mem_enc + 0.30*(1-entropy))
    # Bushnell 2013: mPFC/insula modulate pain through multi-modal control
    e2 = torch.sigmoid(
        0.35 * stumpf_mean * x_l5l7.mean(dim=-1)
        + 0.35 * mem_enc
        + 0.30 * (1.0 - entropy_val)
    )

    return e0, e1, e2
