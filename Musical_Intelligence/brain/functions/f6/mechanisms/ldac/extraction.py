"""LDAC E-Layer -- Extraction (4D).

Liking-dependent auditory cortex modulation features:
  E0: stg_liking_coupling    -- R STG tracks moment-to-moment liking [0, 1]
  E1: pleasure_gating        -- Pleasure gates sensory gain [0, 1]
  E2: ic_liking_interaction  -- IC x liking interaction (inversion) [0, 1]
  E3: moment_to_moment       -- Continuous tracking signal [0, 1]

E0 captures continuous coupling between R STG activity and hedonic
evaluation. Combines fast pleasantness (100ms) for immediate tracking
with smoothed pleasantness (500ms mean) for temporal stability.
Gold et al. 2023a: R STG BOLD covaries with joystick liking ratings
(t(23) = 2.56, p = 0.018).

E1 models top-down reward-to-perception pathway: pleasure state modulates
auditory cortex responsiveness. Liked music produces enhanced cortical
response; disliked music reduces sensory gain.
Martinez-Molina et al. 2016: R STG-NAcc connectivity modulated by
musical reward sensitivity (PPI group effect p = 0.05).

E2 captures the critical IC x liking interaction. High IC combined with
low liking (disliking) produces maximal sensory suppression (lowest STG
activity). The (1 - f01) term inverts liking so low liking amplifies IC.
Gold et al. 2023a: IC x liking in R STG (t(23) = 2.92, p = 0.008).
Cheung et al. 2019: replicated in harmonic domain.

E3 integrates all three preceding features with spectral flux for a
continuous frame-by-frame readout of reward-modulated processing.

H3 demands consumed (12):
  (4, 3, 0, 2)   sensory_pleasantness value H3 L2   -- fast hedonic
  (4, 8, 1, 2)   sensory_pleasantness mean H8 L2    -- smoothed liking
  (4, 16, 2, 2)  sensory_pleasantness std H16 L2    -- liking stability
  (8, 3, 0, 2)   loudness value H3 L2               -- sensory salience
  (8, 16, 1, 2)  loudness mean H16 L2               -- sustained arousal
  (21, 2, 0, 0)  spectral_change value H2 L0        -- IC surprise
  (21, 8, 8, 0)  spectral_change velocity H8 L0     -- IC change rate
  (21, 16, 20, 2) spectral_change entropy H16 L2    -- predictability
  (10, 3, 0, 2)  spectral_flux value H3 L2          -- deviation
  (10, 8, 2, 2)  spectral_flux std H8 L2            -- deviation consist.
  (25, 3, 0, 2)  x_l0l5 value H3 L2                 -- gating modulation
  (25, 16, 20, 2) x_l0l5 entropy H16 L2             -- gating complexity

R3 inputs: sensory_pleasantness[4], loudness[8], spectral_flux[10],
           spectral_change[21], x_l0l5[25]

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/ldac/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed (12 tuples, all E-layer) --------------------------
# f01: STG-liking coupling
_PLEAS_VAL_H3 = (4, 3, 0, 2)        # sensory_pleasantness value H3 L2
_PLEAS_MEAN_H8 = (4, 8, 1, 2)       # sensory_pleasantness mean H8 L2
_PLEAS_STD_H16 = (4, 16, 2, 2)      # sensory_pleasantness std H16 L2

# f02: Pleasure gating
_LOUD_VAL_H3 = (8, 3, 0, 2)         # loudness value H3 L2
_LOUD_MEAN_H16 = (8, 16, 1, 2)      # loudness mean H16 L2

# f03: IC x liking interaction
_IC_VAL_H2 = (21, 2, 0, 0)          # spectral_change value H2 L0
_IC_VEL_H8 = (21, 8, 8, 0)          # spectral_change velocity H8 L0
_IC_ENT_H16 = (21, 16, 20, 2)       # spectral_change entropy H16 L2

# f04: Moment-to-moment + cross-layer
_FLUX_VAL_H3 = (10, 3, 0, 2)        # spectral_flux value H3 L2
_FLUX_STD_H8 = (10, 8, 2, 2)        # spectral_flux std H8 L2
_GATE_VAL_H3 = (25, 3, 0, 2)        # x_l0l5 gating value H3 L2
_GATE_ENT_H16 = (25, 16, 20, 2)     # x_l0l5 gating entropy H16 L2

# -- Upstream dimension defaults -----------------------------------------------
_IUCP_DIM = 6
_RPEM_DIM = 8
_DAED_DIM = 8


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """Compute E-layer: 4D liking-dependent auditory cortex features.

    E0 (stg_liking_coupling): Continuous coupling between R STG and
    moment-to-moment liking. Fast pleasantness (100ms, w=0.35) +
    smoothed pleasantness (500ms mean, w=0.30).
    Gold et al. 2023a: R STG BOLD covaries with joystick liking.

    E1 (pleasure_gating): Top-down reward-to-perception pathway.
    f01 as pleasure signal (w=0.35) + loudness at 100ms (w=0.30)
    as sensory salience being gated.
    Martinez-Molina et al. 2016: STG-NAcc connectivity modulation.

    E2 (ic_liking_interaction): IC x liking interaction with inversion.
    ic_75ms * (1 - f01) so low liking amplifies IC contribution.
    Gold et al. 2023a: t=2.92, p=0.008. Cheung 2019: harmonic domain.

    E3 (moment_to_moment): Integrated tracking signal combining f01,
    f02, and spectral flux for frame-by-frame readout.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 spectral features.
        upstream_outputs: ``{"IUCP": (B, T, D), "RPEM": (B, T, D),
                              "DAED": (B, T, D)}``.

    Returns:
        ``(E0, E1, E2, E3)`` each ``(B, T)``.
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device

    # -- H3 features -----------------------------------------------------------
    pleas_val = h3_features[_PLEAS_VAL_H3]       # (B, T) -- 100ms hedonic
    pleas_mean = h3_features[_PLEAS_MEAN_H8]     # (B, T) -- 500ms smoothed
    # pleas_std used indirectly for stability context
    _pleas_std = h3_features[_PLEAS_STD_H16]     # (B, T) -- liking stability

    loud_val = h3_features[_LOUD_VAL_H3]         # (B, T) -- 100ms salience
    _loud_mean = h3_features[_LOUD_MEAN_H16]     # (B, T) -- 1s arousal context

    ic_val = h3_features[_IC_VAL_H2]             # (B, T) -- 75ms IC surprise
    _ic_vel = h3_features[_IC_VEL_H8]            # (B, T) -- IC change rate
    ic_ent = h3_features[_IC_ENT_H16]            # (B, T) -- 1s predictability

    flux_val = h3_features[_FLUX_VAL_H3]         # (B, T) -- 100ms deviation
    _flux_std = h3_features[_FLUX_STD_H8]        # (B, T) -- deviation consist.
    _gate_val = h3_features[_GATE_VAL_H3]        # (B, T) -- gating modulation
    _gate_ent = h3_features[_GATE_ENT_H16]       # (B, T) -- gating complexity

    # -- Upstream (graceful degradation with zeros) ----------------------------
    iucp = upstream_outputs.get(
        "IUCP", torch.zeros(B, T, _IUCP_DIM, device=device),
    )
    rpem = upstream_outputs.get(
        "RPEM", torch.zeros(B, T, _RPEM_DIM, device=device),
    )
    daed = upstream_outputs.get(
        "DAED", torch.zeros(B, T, _DAED_DIM, device=device),
    )

    # Upstream summary signals (mean across dims for modulation)
    iucp_mean = iucp.mean(dim=-1)              # (B, T)
    rpem_mean = rpem.mean(dim=-1)              # (B, T)
    daed_mean = daed.mean(dim=-1)              # (B, T)

    # -- E0: STG-Liking Coupling -----------------------------------------------
    # sigma(0.35 * pleasantness_100ms + 0.30 * mean_pleasantness_500ms
    #       + 0.20 * rpem_mean + 0.15 * daed_mean)
    # Gold et al. 2023a: R STG continuously covaries with moment-to-moment
    # liking (t(23) = 2.56, p = 0.018).
    f01 = torch.sigmoid(
        0.35 * pleas_val
        + 0.30 * pleas_mean
        + 0.20 * rpem_mean
        + 0.15 * daed_mean
    )

    # -- E1: Pleasure Gating ---------------------------------------------------
    # sigma(0.35 * f01 + 0.30 * loudness_100ms + 0.20 * iucp_mean
    #       + 0.15 * gate_val)
    # Martinez-Molina et al. 2016: R STG-NAcc functional connectivity
    # modulated by musical reward sensitivity (PPI group effect p = 0.05).
    f02 = torch.sigmoid(
        0.35 * f01
        + 0.30 * loud_val
        + 0.20 * iucp_mean
        + 0.15 * _gate_val
    )

    # -- E2: IC x Liking Interaction -------------------------------------------
    # sigma(0.35 * ic_75ms * (1 - f01) + 0.30 * ic_entropy_1s
    #       + 0.20 * ic_vel + 0.15 * pleas_std)
    # Gold et al. 2023a: IC x liking interaction in R STG
    # (t(23) = 2.92, p = 0.008). The (1 - f01) inversion means:
    # high IC + low liking -> highest activation (maximal suppression signal)
    # high IC + high liking -> reduced IC contribution (open gating)
    f03 = torch.sigmoid(
        0.35 * ic_val * (1.0 - f01)
        + 0.30 * ic_ent
        + 0.20 * _ic_vel
        + 0.15 * _pleas_std
    )

    # -- E3: Moment-to-Moment Tracking -----------------------------------------
    # sigma(0.40 * f01 + 0.30 * f02 + 0.30 * spectral_flux_100ms)
    # Integrated real-time summary combining liking coupling, pleasure
    # gating, and sensory deviation detection.
    f04 = torch.sigmoid(
        0.40 * f01
        + 0.30 * f02
        + 0.30 * flux_val
    )

    return f01, f02, f03, f04
