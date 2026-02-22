"""OII M-Layer -- Temporal Integration (2D).

Two explicit features modeling oscillatory mode switching metrics:

  M0: gf_proxy             -- Fluid intelligence proxy (XOR-like) [0, 1]
  M1: switching_efficiency -- Mode switching efficiency metric [0, 1]

H3 consumed:
    (11, 14, 8, 0)  onset_strength velocity H14 L0  -- mode switching rate 700ms
    (22, 18, 19, 0) entropy stability H18 L0        -- pattern stability 2s phrase
    (5, 14, 14, 0)  periodicity periodicity H14 L0  -- meta-regularity
    (3, 14, 1, 0)   stumpf_fusion mean H14 L0       -- binding quality over progression

R3 consumed:
    [11] onset_strength  -- M1: mode switch trigger rate
    [22] entropy         -- M1: integration demand for stability
    [5]  periodicity     -- M0: oscillatory regularity for Gf
    [3]  stumpf_fusion   -- M0: binding quality as integration proxy

See Building/C3-Brain/F4-Memory-Systems/mechanisms/oii/OII-temporal-integration.md
Bruzzone et al. 2022: Gf group separation t(55)=11.08, p<1e-7 (DTI + MEG N=66/67).
Cabral et al. 2022: metastable oscillatory modes (computational model, MEG N=89).
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_ONSET_VEL_H14 = (11, 14, 8, 0)         # onset_strength velocity H14 L0
_ENTROPY_STAB_H18 = (22, 18, 19, 0)     # entropy stability H18 L0
_PERIOD_PERIOD_H14 = (5, 14, 14, 0)     # periodicity periodicity H14 L0
_FUSION_MEAN_H14 = (3, 14, 1, 0)        # stumpf_fusion mean H14 L0


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute M-layer: oscillatory mode-switching temporal integration.

    M0 (gf_proxy) implements the core insight that high fluid intelligence
    is efficient SWITCHING between integration and segregation, not simply
    high integration or segregation alone.  The XOR-like formula
    ``f16 * (1 - f17) + f17 * (1 - f16)`` peaks when one mode is dominant
    and the other suppressed -- exactly the complementary activation pattern
    in high-Gf individuals.

    M1 (switching_efficiency) quantifies how quickly and cleanly the brain
    transitions between oscillatory modes.  Uses onset velocity at H14
    (700ms) to capture gamma burst transition rate and entropy stability at
    H18 (2s) to capture coherent structure maintenance despite local
    transitions.

    Bruzzone et al. 2022: DTI + MEG N=66/67, Gf group separation
    t(55)=11.08, p<1e-7; high Gf = efficient complementary activation.
    Cabral et al. 2022: metastable oscillatory modes emerge from
    delay-coupled oscillators; coupling controls switching (MEG N=89).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e: ``(E0, E1, E2)`` from extraction layer.

    Returns:
        ``(M0, M1)`` each ``(B, T)``.
    """
    e0, e1, _e2 = e

    # -- H3 features --
    onset_vel_h14 = h3_features[_ONSET_VEL_H14]         # (B, T)
    entropy_stab_h18 = h3_features[_ENTROPY_STAB_H18]   # (B, T)
    _period_period_h14 = h3_features[_PERIOD_PERIOD_H14] # (B, T) -- context
    _fusion_mean_h14 = h3_features[_FUSION_MEAN_H14]     # (B, T) -- context

    # -- M0: Gf Proxy --
    # XOR-like: peaks when one mode is high and other low = efficient
    # complementary activation.  Both modes simultaneously active or
    # inactive indicates diffuse, inefficient processing.
    # Bruzzone et al. 2022: high Gf = stronger theta/alpha degree AND
    # higher gamma segregation -- complementary activation.
    m0 = (e0 * (1.0 - e1) + e1 * (1.0 - e0)).clamp(0.0, 1.0)

    # -- M1: Switching Efficiency --
    # Fast onset velocity + stable entropy = clean mode switching.
    # sigma(0.25 * onset_velocity_h14 + 0.25 * entropy_stability_h18).
    # Cabral et al. 2022: global coupling strength controls mode switching.
    m1 = torch.sigmoid(
        0.25 * onset_vel_h14
        + 0.25 * entropy_stab_h18
    )

    return m0, m1
