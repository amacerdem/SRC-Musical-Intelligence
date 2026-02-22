"""ECT E-Layer -- Extraction (4D).

Expertise compartmentalization trade-off extraction features:
  f01: within_efficiency        -- Intra-network coupling strength [0, 1]
  f02: between_reduction        -- Cross-network connectivity loss [0, 1]
  f03: trade_off_ratio          -- Cost-benefit balance [0, 10]
  f04: flexibility_index        -- Reconfiguration capacity [0, 1]

f01 captures the gains of within-network specialization from long-timescale
coupling and pattern binding means at 1s.
Paraskevopoulos et al. 2022: musicians show 106 within-network edges M > NM;
IFG area 47m is highest-degree node in 5/6 network states.
Papadaki et al. 2023: professionals show greater network strength and global
efficiency correlating with task performance.

f02 captures the costs of reduced between-network connectivity from
cross-network mean and entropy at 1s.
Paraskevopoulos et al. 2022: 192 between-network edges NM > M;
47 multilinks (NM) vs 15 (M), p < 0.001 FDR.
Moller et al. 2021: musicians show reduced cross-modal structural connectivity.

f03 is the direct ratio of within-efficiency to between-reduction,
clamped to [0, 10] with epsilon-guarded division.
Empirical baseline approximately 0.55 (106/192 edges).

f04 captures reconfiguration capacity from spectral change dynamics and
reconfiguration speed.
Wu-Chung et al. 2025: music creativity benefits depend on baseline network
flexibility; higher flexibility leads to more cognitive benefit from training.

H3 demands consumed (10):
  (25, 16, 1, 2)  x_l0l5 mean H16 L2          -- mean within-coupling 1s
  (33, 16, 1, 2)  x_l4l5 mean H16 L2          -- mean pattern binding 1s
  (41, 16, 1, 2)  x_l5l6 mean H16 L2          -- mean cross-network 1s
  (41, 16, 20, 2) x_l5l6 entropy H16 L2       -- cross-network entropy 1s
  (21, 3, 0, 2)   spectral_change value H3 L2  -- reconfiguration 100ms
  (21, 4, 8, 0)   spectral_change velocity H4 L0 -- reconfig speed 125ms
  (25, 3, 0, 2)   x_l0l5 value H3 L2          -- within coupling 100ms
  (25, 3, 2, 2)   x_l0l5 std H3 L2            -- coupling variability 100ms
  (41, 3, 0, 2)   x_l5l6 value H3 L2          -- cross-network binding 100ms
  (41, 3, 2, 2)   x_l5l6 std H3 L2            -- cross-network variability 100ms

R3 consumed:
    [25:33]  x_l0l5                  -- within-network coupling
    [33:41]  x_l4l5                  -- pattern-feature binding
    [41:49]  x_l5l6                  -- cross-network connectivity
    [21]     spectral_change         -- reconfiguration capacity proxy

See Building/C3-Brain/F8-Learning-and-Plasticity/mechanisms/ect/e_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed (10 tuples, E-layer) ------------------------------
# f01: within_efficiency
_WITHIN_MEAN_1S = (25, 16, 1, 2)          # mean within-coupling 1s
_BINDING_MEAN_1S = (33, 16, 1, 2)         # mean pattern binding 1s

# f02: between_reduction
_CROSS_MEAN_1S = (41, 16, 1, 2)           # mean cross-network 1s
_CROSS_ENT_1S = (41, 16, 20, 2)           # cross-network entropy 1s

# f04: flexibility_index
_RECONFIG_100MS = (21, 3, 0, 2)           # reconfiguration at 100ms
_RECONFIG_SPEED_125MS = (21, 4, 8, 0)     # reconfiguration speed 125ms

# P-layer also uses these, but E-layer registers them in the demand spec
_WITHIN_VAL_100MS = (25, 3, 0, 2)         # within coupling 100ms
_WITHIN_STD_100MS = (25, 3, 2, 2)         # coupling variability 100ms
_CROSS_VAL_100MS = (41, 3, 0, 2)          # cross-network binding 100ms
_CROSS_STD_100MS = (41, 3, 2, 2)          # cross-network variability 100ms

# -- Constants ----------------------------------------------------------------
_EPS = 1e-8
_RATIO_CLAMP_MAX = 10.0


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    ednr: Tensor,
    cdmr: Tensor,
    slee: Tensor,
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """Compute E-layer: 4D expertise compartmentalization trade-off features.

    f01 (within_efficiency): Intra-network coupling strength from mean
    within-coupling and pattern binding over 1s.
    sigma(0.35 * within_coupling_mean_1s + 0.35 * pattern_binding_mean_1s
          + 0.15 * ednr_mean + 0.15 * slee_mean).
    Paraskevopoulos 2022: 106 within-network edges M > NM.

    f02 (between_reduction): Cross-network connectivity loss from mean
    cross-network features and cross-network entropy over 1s.
    sigma(0.35 * cross_network_mean_1s + 0.35 * cross_entropy_1s
          + 0.15 * cdmr_mean + 0.15 * ednr_between).
    Paraskevopoulos 2022: 192 between-network edges NM > M.

    f03 (trade_off_ratio): Ratio of within-efficiency to between-reduction.
    clamp(f01 / (f02 + epsilon), 0, 10).
    Empirical baseline approximately 0.55 (106/192 edges).

    f04 (flexibility_index): Reconfiguration capacity from spectral change
    dynamics and reconfiguration speed.
    sigma(0.35 * reconfig_100ms + 0.35 * reconfig_speed_125ms
          + 0.15 * slee_mean + 0.15 * cdmr_mean).
    Wu-Chung et al. 2025: baseline network flexibility determines training
    benefit.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 spectral features.
        ednr: ``(B, T, 10)`` upstream EDNR output.
        cdmr: ``(B, T, 11)`` upstream CDMR output.
        slee: ``(B, T, 13)`` upstream SLEE output.

    Returns:
        ``(f01, f02, f03, f04)`` each ``(B, T)``.
    """
    # -- H3 features -----------------------------------------------------------
    within_mean_1s = h3_features[_WITHIN_MEAN_1S]       # (B, T)
    binding_mean_1s = h3_features[_BINDING_MEAN_1S]     # (B, T)
    cross_mean_1s = h3_features[_CROSS_MEAN_1S]         # (B, T)
    cross_ent_1s = h3_features[_CROSS_ENT_1S]           # (B, T)
    reconfig_100ms = h3_features[_RECONFIG_100MS]        # (B, T)
    reconfig_speed = h3_features[_RECONFIG_SPEED_125MS]  # (B, T)

    # -- Upstream summary signals (graceful degradation) -----------------------
    ednr_mean = ednr.mean(dim=-1)              # (B, T)
    cdmr_mean = cdmr.mean(dim=-1)              # (B, T)
    slee_mean = slee.mean(dim=-1)              # (B, T)

    # EDNR between_connectivity is dim 1 (f02 in EDNR E-layer)
    ednr_between = ednr[..., 1]                # (B, T)

    # -- f01: Within Efficiency ------------------------------------------------
    # sigma(0.35 * within_coupling_mean_1s + 0.35 * pattern_binding_mean_1s
    #       + 0.15 * ednr_mean + 0.15 * slee_mean)
    # Paraskevopoulos 2022: musicians show 106 within-network edges.
    # Papadaki 2023: network strength correlates with task performance.
    f01 = torch.sigmoid(
        0.35 * within_mean_1s
        + 0.35 * binding_mean_1s
        + 0.15 * ednr_mean
        + 0.15 * slee_mean
    )

    # -- f02: Between Reduction ------------------------------------------------
    # sigma(0.35 * cross_network_mean_1s + 0.35 * cross_entropy_1s
    #       + 0.15 * cdmr_mean + 0.15 * ednr_between)
    # Paraskevopoulos 2022: 192 between-network edges NM > M.
    # Moller 2021: reduced cross-modal structural connectivity (IFOF FA).
    f02 = torch.sigmoid(
        0.35 * cross_mean_1s
        + 0.35 * cross_ent_1s
        + 0.15 * cdmr_mean
        + 0.15 * ednr_between
    )

    # -- f03: Trade-off Ratio --------------------------------------------------
    # clamp(f01 / (f02 + epsilon), 0, 10)
    # NOT sigmoid -- raw ratio reflecting cost-benefit balance.
    # Empirical baseline ~0.55 (106/192 edges).
    f03 = (f01 / (f02 + _EPS)).clamp(0.0, _RATIO_CLAMP_MAX)

    # -- f04: Flexibility Index ------------------------------------------------
    # sigma(0.35 * reconfig_100ms + 0.35 * reconfig_speed_125ms
    #       + 0.15 * slee_mean + 0.15 * cdmr_mean)
    # Wu-Chung 2025: music creativity benefits depend on baseline flexibility.
    f04 = torch.sigmoid(
        0.35 * reconfig_100ms
        + 0.35 * reconfig_speed
        + 0.15 * slee_mean
        + 0.15 * cdmr_mean
    )

    return f01, f02, f03, f04
