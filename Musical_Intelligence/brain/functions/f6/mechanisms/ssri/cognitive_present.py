"""SSRI P-Layer -- Cognitive Present (2D).

Social Synchrony Reward Integration present-state estimates:
  prefrontal_coupling   -- Current rDLPFC/rTPJ synchronization state [0, 1]
  endorphin_proxy       -- Endorphin release estimate [0, 1]

prefrontal_coupling models the current level of inter-brain prefrontal
synchronization. Entrainment quality (f04, weight 0.40) is the primary
driver of neural alignment, with the current consonance-energy coupling
state at 500ms (weight 0.30). This reflects the fNIRS hyperscanning
finding that coordinated music-making produces measurable inter-brain
synchronization in rDLPFC and rTPJ (Ni et al. 2024, N=528, d=0.85).

endorphin_proxy models the slow-building beta-endorphin release from
sustained synchronized activity. Social bonding (f02, weight 0.40) is the
primary driver, group flow (f03, weight 0.30) is a flow-dependent
amplifier, and coupling mean at 5s (weight 0.30) provides long-range
sustained coordination signal. tau_endorphin = 30.0s, reflecting the slow
timescale of opioid release. Tarr, Launay & Dunbar 2014: synchronized
dancing elevates pain threshold (d ~ 0.62).

H3 demands consumed (2 tuples):
  (25, 8, 0, 2)    coupling at 500ms L2   -- current consonance-energy state
  (25, 20, 1, 0)   coupling mean 5s L0    -- sustained coordination

Dependencies:
  E-layer f02 (social_bonding_index)
  E-layer f03 (group_flow_state)
  E-layer f04 (entrainment_quality)

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/ssri/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_COUPLING_VAL_H8 = (25, 8, 0, 2)        # coupling at 500ms L2
_COUPLING_MEAN_H20 = (25, 20, 1, 0)     # coupling mean 5s LTI L0


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute P-layer: prefrontal coupling and endorphin proxy.

    prefrontal_coupling estimates the current rDLPFC/rTPJ synchronization
    from entrainment quality (f04) and consonance-energy coupling at 500ms.
    Ni et al. 2024: social bonding increases rDLPFC synchronization
    (fNIRS hyperscanning, N=528, d=0.85).

    endorphin_proxy estimates slow-building beta-endorphin release from
    sustained synchronized activity. Social bonding (f02), group flow (f03),
    and coupling mean at 5s drive the estimate with tau_endorphin = 30.0s.
    Dunbar 2012: synchronized music-making increases endorphin release
    (pain threshold proxy, d ~ 0.60-0.80). Tarr, Launay & Dunbar 2014:
    synchronized dancing elevates pain threshold (d ~ 0.62).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        e_outputs: ``(f01, f02, f03, f04, f05)`` from extraction layer.
        m_outputs: ``(spe, sa)`` from temporal integration layer.

    Returns:
        ``(prefrontal_coupling, endorphin_proxy)`` each ``(B, T)``
    """
    _f01, f02, f03, f04, _f05 = e_outputs

    # -- H3 features --
    coupling_500ms = h3_features[_COUPLING_VAL_H8]       # (B, T)
    coupling_mean_5s = h3_features[_COUPLING_MEAN_H20]   # (B, T)

    # -- prefrontal_coupling --
    # Current rDLPFC/rTPJ synchronization: entrainment quality (0.40) is the
    # primary driver of neural alignment, consonance-energy coupling at 500ms
    # (0.30) reflects current interaction state.
    # Ni et al. 2024: coordinated music-making produces inter-brain
    # synchronization in rDLPFC (fNIRS hyperscanning, d=0.85).
    prefrontal_coupling = torch.sigmoid(
        0.40 * f04
        + 0.30 * coupling_500ms
    )

    # -- endorphin_proxy --
    # Slow-building beta-endorphin release from sustained synchrony.
    # Social bonding (f02, 0.40) is the primary driver. Group flow (f03,
    # 0.30) amplifies through absorption. Coupling mean at 5s (0.30) provides
    # long-range sustained coordination signal. tau_endorphin = 30.0s.
    # Dunbar 2012: synchronized music increases endorphin (d~0.60-0.80).
    # Tarr, Launay & Dunbar 2014: synchronized dancing (d~0.62).
    endorphin_proxy = torch.sigmoid(
        0.40 * f02
        + 0.30 * f03
        + 0.30 * coupling_mean_5s
    )

    return prefrontal_coupling, endorphin_proxy
