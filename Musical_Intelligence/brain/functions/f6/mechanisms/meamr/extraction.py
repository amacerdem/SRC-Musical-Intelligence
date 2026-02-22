"""MEAMR E-Layer -- Extraction (4D).

Music-Evoked Autobiographical Memory Reward extraction signals:
  E0: f01_familiarity_index   -- Musical familiarity level [0, 1]
  E1: f02_autobio_salience    -- Autobiographical salience from memories [0, 1]
  E2: f03_dmpfc_tracking      -- Dorsal medial PFC tonal space tracking [0, 1]
  E3: f04_positive_affect     -- Positive affect from familiar music [0, 1]

Hierarchical dependency: familiarity (E0) is prerequisite for autobiographical
salience (E1), which feeds positive affect (E3). E2 (dMPFC tracking) runs in
parallel from sensory signals.

Janata 2009: dMPFC tracks tonal space (P < 0.005, 40-voxel cluster).
Familiarity activates pre-SMA (Z = 5.37), IFG (Z = 4.81), STG (P < 0.001).
dMPFC correlates with autobiographical salience (FDR P < 0.025).
Salimpoor 2011: DA release during familiar music chills (PET, N = 8, r = 0.71).

H3 demands consumed (14 tuples):
  (4, 8, 1, 2)    sensory_pleasantness mean H8 L2    -- mean pleasantness 500ms
  (4, 16, 18, 2)  sensory_pleasantness trend H16 L2  -- pleasantness trend 1s
  (8, 8, 1, 2)    loudness mean H8 L2                -- mean loudness 500ms
  (8, 16, 1, 2)   loudness mean H16 L2               -- mean loudness 1s
  (12, 16, 1, 2)  warmth mean H16 L2                 -- mean warmth 1s
  (13, 16, 1, 2)  brightness mean H16 L2             -- mean brightness 1s
  (21, 8, 20, 2)  spectral_change entropy H8 L2      -- structural entropy 500ms
  (21, 16, 1, 2)  spectral_change mean H16 L2        -- mean structural change 1s
  (22, 8, 8, 0)   energy_change velocity H8 L0       -- energy velocity 500ms
  (22, 16, 18, 0) energy_change trend H16 L0         -- energy change trend 1s
  (41, 8, 1, 2)   x_l5l6[0] mean H8 L2              -- memory-structure 500ms
  (41, 16, 1, 2)  x_l5l6[0] mean H16 L2             -- mean memory-struct 1s
  (41, 16, 18, 2) x_l5l6[0] trend H16 L2            -- memory-struct trend 1s
  (41, 16, 5, 0)  x_l5l6[0] range H16 L0            -- memory-struct range 1s

R3 features:
  [4] sensory_pleasantness, [8] loudness, [12] warmth, [13] spectral_centroid,
  [21] spectral_change, [22] energy_change, [41:49] x_l5l6

Upstream reads:
  DAED relay (from relay_outputs), MEAMN (cross-function, from relay_outputs)

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/meamr/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed (14 tuples) --------------------------------------
_PLEAS_MEAN_H8 = (4, 8, 1, 2)          # mean pleasantness 500ms
_PLEAS_TREND_H16 = (4, 16, 18, 2)      # pleasantness trend 1s
_LOUD_MEAN_H8 = (8, 8, 1, 2)           # mean loudness 500ms
_LOUD_MEAN_H16 = (8, 16, 1, 2)         # mean loudness 1s
_WARMTH_MEAN_H16 = (12, 16, 1, 2)      # mean warmth 1s
_BRIGHT_MEAN_H16 = (13, 16, 1, 2)      # mean brightness 1s
_STRUCT_ENT_H8 = (21, 8, 20, 2)        # structural entropy 500ms
_STRUCT_MEAN_H16 = (21, 16, 1, 2)      # mean structural change 1s
_ENERGY_VEL_H8 = (22, 8, 8, 0)         # energy velocity 500ms
_ENERGY_TREND_H16 = (22, 16, 18, 0)    # energy change trend 1s
_MEM_MEAN_H8 = (41, 8, 1, 2)           # memory-structure coupling 500ms
_MEM_MEAN_H16 = (41, 16, 1, 2)         # mean memory-structure 1s
_MEM_TREND_H16 = (41, 16, 18, 2)       # memory-structure trend 1s
_MEM_RANGE_H16 = (41, 16, 5, 0)        # memory-structure range 1s

# -- R3 feature indices (post-freeze 97D) -------------------------------------
_SENSORY_PLEASANTNESS = 4
_LOUDNESS = 8
_WARMTH = 12
_SPECTRAL_CENTROID = 13
_SPECTRAL_CHANGE = 21
_ENERGY_CHANGE = 22
_X_L5L6_START = 41
_X_L5L6_END = 49

# -- Upstream relay indices ----------------------------------------------------
_DAED_WANTING_IDX = 0       # DAED wanting_index (idx 0)
_MEAMN_MEMORY_STATE_IDX = 5  # MEAMN P0:memory_state (idx 5)


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """Compute E-layer: 4D autobiographical memory reward extraction.

    Hierarchical computation:
      E0 (familiarity_index): Musical recognition from pleasantness trend
          and timbral warmth. Prerequisite for autobiographical salience.
      E1 (autobio_salience): Memory-structure coupling trend captures
          autobiographical buildup. Requires familiarity (E0).
      E2 (dmpfc_tracking): Continuous tonal space tracking by dMPFC.
          Brightness + pleasantness + structural complexity.
      E3 (positive_affect): Integrates familiarity and autobio salience
          into reward-related positive affect. Requires both E0 AND E1.

    Janata 2009: familiarity activates pre-SMA (Z = 5.37), IFG (Z = 4.81).
    dMPFC tracks tonal space (P < 0.005, 40-voxel cluster).
    Combined FAV in MPFC (FDR P < 0.025).
    Salimpoor 2011: DA release during familiar music (PET, r = 0.71).

    All formulas use sigmoid activation with coefficient sums <= 1.0
    (saturation rule). tau_decay = 10.0s for extended memory retrieval.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        relay_outputs: ``{"DAED": (B, T, D), "MEAMN": (B, T, D)}``

    Returns:
        ``(E0, E1, E2, E3)`` each ``(B, T)``
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device

    # -- H3 features --
    pleas_mean_500 = h3_features[_PLEAS_MEAN_H8]         # (B, T)
    pleas_trend_1s = h3_features[_PLEAS_TREND_H16]       # (B, T)
    loud_mean_500 = h3_features[_LOUD_MEAN_H8]           # (B, T)
    loud_mean_1s = h3_features[_LOUD_MEAN_H16]           # (B, T)
    warmth_mean_1s = h3_features[_WARMTH_MEAN_H16]       # (B, T)
    bright_mean_1s = h3_features[_BRIGHT_MEAN_H16]       # (B, T)
    struct_ent_500 = h3_features[_STRUCT_ENT_H8]         # (B, T)
    struct_mean_1s = h3_features[_STRUCT_MEAN_H16]       # (B, T)
    energy_vel_500 = h3_features[_ENERGY_VEL_H8]         # (B, T)
    energy_trend_1s = h3_features[_ENERGY_TREND_H16]     # (B, T)
    mem_mean_500 = h3_features[_MEM_MEAN_H8]             # (B, T)
    mem_mean_1s = h3_features[_MEM_MEAN_H16]             # (B, T)
    mem_trend_1s = h3_features[_MEM_TREND_H16]           # (B, T)
    mem_range_1s = h3_features[_MEM_RANGE_H16]           # (B, T)

    # -- R3 features --
    pleasantness = r3_features[..., _SENSORY_PLEASANTNESS]  # (B, T)
    loudness = r3_features[..., _LOUDNESS]                  # (B, T)
    warmth = r3_features[..., _WARMTH]                      # (B, T)
    centroid = r3_features[..., _SPECTRAL_CENTROID]         # (B, T)
    x_l5l6 = r3_features[..., _X_L5L6_START:_X_L5L6_END]  # (B, T, 8)
    x_l5l6_mean = x_l5l6.mean(dim=-1)                      # (B, T)

    # -- Upstream relay features (graceful fallback) --
    daed = relay_outputs.get("DAED", torch.zeros(B, T, 8, device=device))
    daed_wanting = daed[..., _DAED_WANTING_IDX]             # (B, T)

    meamn = relay_outputs.get("MEAMN", torch.zeros(B, T, 12, device=device))
    meamn_memory = meamn[..., _MEAMN_MEMORY_STATE_IDX]      # (B, T)

    # -- E0: Familiarity Index --
    # sigma(0.35 * pleasantness_trend_1s + 0.30 * mean_warmth_1s)
    # + upstream MEAMN memory as amplifier
    # Janata 2009: familiarity activates pre-SMA (Z = 5.37), IFG (Z = 4.81)
    e0 = torch.sigmoid(
        0.35 * pleas_trend_1s
        + 0.30 * warmth_mean_1s
        + 0.20 * pleas_mean_500
        + 0.15 * meamn_memory
    )

    # -- E1: Autobiographical Salience --
    # sigma(0.35 * memory_struct_trend_1s + 0.30 * f01)
    # Janata 2009: dMPFC (BA 8/9) correlates with autobio salience
    # (P < 0.001, FDR P < 0.025 in MPFC ROI)
    e1 = torch.sigmoid(
        0.35 * mem_trend_1s
        + 0.30 * e0
        + 0.20 * mem_mean_1s
        + 0.15 * x_l5l6_mean
    )

    # -- E2: dMPFC Tracking --
    # sigma(0.35 * mean_centroid_1s + 0.35 * mean_pleasantness_500ms
    #       + 0.30 * structural_entropy_500ms)
    # Janata 2009: dMPFC tracks tonal space (P < 0.005, 40-voxel cluster)
    e2 = torch.sigmoid(
        0.35 * bright_mean_1s
        + 0.35 * pleas_mean_500
        + 0.30 * struct_ent_500
    )

    # -- E3: Positive Affect --
    # sigma(... + 0.30 * f02 * f01)
    # Janata 2009: combined FAV in MPFC (FDR P < 0.025)
    # Maps onto vACC + SN/VTA positive affect integration
    e3 = torch.sigmoid(
        0.30 * e1 * e0
        + 0.25 * daed_wanting
        + 0.25 * energy_trend_1s
        + 0.20 * loud_mean_1s
    )

    return e0, e1, e2, e3
