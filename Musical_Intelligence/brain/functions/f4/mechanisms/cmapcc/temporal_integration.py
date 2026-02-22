"""CMAPCC M-Layer -- Temporal Integration (2D).

Two composite signals integrating E-layer with temporal context:

  M0: common_code_strength   -- Overall common code activation [0, 1]
  M1: transfer_probability   -- P(cross-modal transfer) [0, 1]

H3 consumed:
    (3, 20, 1, 0)   stumpf_fusion mean H20 L0           -- binding over 5s consolidation
    (5, 20, 19, 0)  periodicity stability H20 L0        -- sequence stability over 5s
    (10, 11, 14, 0) onset_strength periodicity H11 L0   -- onset regularity at 500ms
    (8, 11, 8, 0)   loudness velocity H11 L0            -- intensity dynamics at 500ms
    (10, 16, 1, 0)  onset_strength mean H16 L0          -- mean onset over 1s bar
    (8, 16, 1, 0)   loudness mean H16 L0                -- mean intensity over bar

R3 consumed:
    [3]  stumpf_fusion   -- M1: sequence coherence component (binding)
    [5]  periodicity     -- M1: sequence coherence component (regularity)
    [8]  loudness        -- M1: motor coupling intensity
    [10] onset_strength  -- M1: motor coupling event rate

See Building/C3-Brain/F4-Memory-Systems/mechanisms/cmapcc/CMAPCC-temporal-integration.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_STUMPF_MEAN_5S = (3, 20, 1, 0)
_PERIOD_STAB_5S = (5, 20, 19, 0)
_ONSET_PERIOD_500MS = (10, 11, 14, 0)
_LOUD_VEL_500MS = (8, 11, 8, 0)
_ONSET_MEAN_1S = (10, 16, 1, 0)
_LOUD_MEAN_1S = (8, 16, 1, 0)

# -- R3 indices ----------------------------------------------------------------
_STUMPF_FUSION = 3
_PERIODICITY = 5
_LOUDNESS = 8
_ONSET_STRENGTH = 10


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor]:
    """M-layer: 2D temporal integration from E-layer + H3/R3 + upstreams.

    M0 is the balanced average of E-layer dimensions, giving a single
    scalar summary of the perception-action common code state.

    M1 estimates the probability of cross-modal transfer using
    familiarity (from MEAMN upstream), motor coupling (from SNEM
    beat cross-circuit), and sequence coherence (stumpf x periodicity).

    Lahav 2007: motor training creates action representations of sound
    (fMRI, N=9). Cross-modal transfer requires stored representation.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        e_outputs: ``(E0, E1, E2)`` each ``(B, T)``.
        upstream_outputs: ``{"MEAMN": (B, T, D), "SNEM": (B, T, D)}``.

    Returns:
        ``(M0, M1)`` each ``(B, T)``.
    """
    e0, e1, e2 = e_outputs

    # -- H3 features --
    stumpf_mean_5s = h3_features[_STUMPF_MEAN_5S]
    period_stab_5s = h3_features[_PERIOD_STAB_5S]
    onset_period_500ms = h3_features[_ONSET_PERIOD_500MS]
    loud_vel_500ms = h3_features[_LOUD_VEL_500MS]
    onset_mean_1s = h3_features[_ONSET_MEAN_1S]
    loud_mean_1s = h3_features[_LOUD_MEAN_1S]

    # -- R3 features --
    stumpf = r3_features[..., _STUMPF_FUSION]    # (B, T)
    periodicity = r3_features[..., _PERIODICITY]  # (B, T)

    # -- Upstream reads (graceful degradation) --
    # MEAMN: M1:p_recall [4] as familiarity proxy
    meamn = upstream_outputs.get("MEAMN")
    if meamn is not None:
        familiarity = meamn[..., 4]  # M1:p_recall -- (B, T)
    else:
        familiarity = torch.zeros_like(e0)

    # SNEM: E0:beat_entrainment [0] as motor coupling proxy
    snem = upstream_outputs.get("SNEM")
    if snem is not None:
        motor_coupling = snem[..., 0]  # E0:beat_entrainment -- (B, T)
    else:
        motor_coupling = torch.zeros_like(e0)

    # -- Sequence coherence (stumpf x periodicity) --
    seq_coherence = stumpf * periodicity

    # M0: Common code strength -- balanced average of E-layer
    # Equal weighting: all three E-layer components contribute equally.
    # Bianco 2016: dual-stream convergence requires both dorsal and
    # ventral activations.
    m0 = (e0 + e1 + e2) / 3.0

    # M1: Transfer probability -- P(cross-modal transfer)
    # transfer_prob = sigma(0.40*familiarity + 0.30*motor_coupling
    #                       + 0.30*seq_coherence)
    # Familiarity strongest (0.40): transfer requires stored representation.
    # Lahav 2007: motor training creates action representations of sound.
    m1 = torch.sigmoid(
        0.40 * familiarity
        + 0.30 * motor_coupling
        + 0.30 * seq_coherence
    )

    return m0, m1
