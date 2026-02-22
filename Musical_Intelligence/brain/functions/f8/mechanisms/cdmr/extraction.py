"""CDMR E-Layer -- Extraction (4D).

Context-Dependent Mismatch Response extraction signals:
  f01: mismatch_amplitude    -- Deviance response magnitude [0, 1]
  f02: context_modulation    -- Context-dependent enhancement [0, 1]
  f03: subadditivity_index   -- Integration vs summation measure [0, 1]
  f04: expertise_effect      -- Expertise-context interaction [0, 1]

f01 captures the basic deviance detection signal -- how much the current frame
deviates from expectations. Driven by spectral flux and onset strength at 25ms
gamma timescale. Present in both musicians and non-musicians for simple contexts.
Maps to bilateral auditory cortex A1/STG (Rupp 2022: MEG; Wagner 2018: BESA
dipole source reconstruction).

f02 captures how melodic context richness modulates the mismatch response.
Driven by pitch change complexity at 100ms and 1s horizons. Complex melodic
contexts amplify mismatch detection selectively in experts. Maps to anterior
auditory cortex (Rupp 2022: pitch contour tracking gradient).

f03 captures cross-feature binding strength and variability at 100ms from
x_l5l6 interactions. Subadditivity (combined < sum of individual) indicates
integrated rather than additive processing. Higher values reflect more
expert-like integration. Maps to fronto-central cortex (Crespo-Bojorque 2018:
Fz electrode).

f04 captures the context-dependent expertise advantage. Zero in simple oddball
contexts, positive in complex melodic contexts for musicians. Computed from
f01 and f02 interaction scaled by expertise indicator. Maps to right IFG
(Koelsch: ERAN generators).

H3 demands consumed (8 tuples):
  (10, 0, 0, 2)   spectral_flux value H0 L2        -- instantaneous deviance 25ms
  (10, 3, 2, 2)   spectral_flux std H3 L2          -- deviance variability 100ms
  (11, 0, 0, 2)   onset_strength value H0 L2       -- onset deviance 25ms
  (11, 3, 8, 0)   onset_strength velocity H3 L0    -- onset velocity 100ms
  (23, 3, 0, 2)   pitch_change value H3 L2         -- pitch deviance 100ms
  (23, 16, 1, 2)  pitch_change mean H16 L2         -- mean pitch change 1s
  (41, 3, 0, 2)   x_l5l6 value H3 L2              -- binding strength 100ms
  (41, 3, 2, 2)   x_l5l6 std H3 L2                -- binding variability 100ms

R3 features:
  [10] spectral_flux (onset_strength), [11] onset_strength,
  [23] pitch_change, [41:49] x_l5l6

Upstream reads:
  EDNR relay (via relay_outputs)

Crespo-Bojorque 2018: consonance MMN in musicians and non-musicians.
Wagner 2018: MMN for major third deviant.
Rupp/Hansen 2022: musicians > non-musicians in subadditivity for combined
melodic deviants (MEG).

See Building/C3-Brain/F8-Learning-and-Plasticity/mechanisms/cdmr/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed (8 tuples) ----------------------------------------------
_FLUX_VAL_H0 = (10, 0, 0, 2)          # spectral_flux value H0 L2
_FLUX_STD_H3 = (10, 3, 2, 2)          # spectral_flux std H3 L2
_ONSET_VAL_H0 = (11, 0, 0, 2)         # onset_strength value H0 L2
_ONSET_VEL_H3 = (11, 3, 8, 0)         # onset_strength velocity H3 L0
_PITCH_VAL_H3 = (23, 3, 0, 2)         # pitch_change value H3 L2
_PITCH_MEAN_H16 = (23, 16, 1, 2)      # pitch_change mean H16 L2
_BINDING_VAL_H3 = (41, 3, 0, 2)       # x_l5l6 value H3 L2
_BINDING_STD_H3 = (41, 3, 2, 2)       # x_l5l6 std H3 L2


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    ednr: Tensor,
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """Compute E-layer: context-dependent mismatch response extraction signals.

    f01 (mismatch_amplitude): Basic mismatch detection signal from spectral
    flux and onset strength at 25ms gamma timescale.
    sigma(0.35 * flux_25ms + 0.35 * onset_25ms).
    Crespo-Bojorque 2018: consonance MMN (172-250ms), p=0.007 (non-mus),
    p=0.001 (mus). Wagner 2018: MMN for major third deviant -0.34uV,
    p=0.003.

    f02 (context_modulation): Melodic context complexity that modulates
    mismatch responses. sigma(0.35 * pitch_change_100ms + 0.35 *
    mean_pitch_change_1s). Crespo-Bojorque 2018: musicians show consonance
    MMN > dissonance MMN, right-lateralized F(1,15)=4.95, p<0.05.

    f03 (subadditivity_index): Response to combined deviants less than sum
    of individual responses. sigma(0.35 * binding_100ms + 0.35 *
    binding_variability_100ms). Rupp/Hansen 2022: musicians > non-musicians
    in subadditivity for combined melodic deviants (MEG).

    f04 (expertise_effect): Difference between complex and simple context
    mismatch responses scaled by expertise indicator.
    sigma(0.35 * f01 * f02 + 0.30 * onset_velocity_100ms).
    Rupp/Hansen 2022: no group difference in classic oddball, but
    musicians > non-musicians in complex melodic paradigm.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        ednr: ``(B, T, 10)`` upstream EDNR relay output.

    Returns:
        ``(f01, f02, f03, f04)`` each ``(B, T)``
    """
    # -- H3 features --
    flux_25ms = h3_features[_FLUX_VAL_H0]           # (B, T)
    onset_25ms = h3_features[_ONSET_VAL_H0]          # (B, T)
    pitch_100ms = h3_features[_PITCH_VAL_H3]         # (B, T)
    pitch_mean_1s = h3_features[_PITCH_MEAN_H16]     # (B, T)
    binding_100ms = h3_features[_BINDING_VAL_H3]     # (B, T)
    binding_std_100ms = h3_features[_BINDING_STD_H3] # (B, T)
    onset_vel_100ms = h3_features[_ONSET_VEL_H3]     # (B, T)

    # -- f01: Mismatch Amplitude --
    # Basic deviance detection from spectral flux and onset at 25ms gamma.
    # Crespo-Bojorque 2018: consonance MMN p=0.007 (non-mus), p=0.001 (mus).
    # Wagner 2018: MMN for major third deviant -0.34uV +/- 0.32, p=0.003.
    f01 = torch.sigmoid(
        0.35 * flux_25ms
        + 0.35 * onset_25ms
    )

    # -- f02: Context Modulation --
    # Melodic context complexity modulating mismatch sensitivity.
    # Crespo-Bojorque 2018: musicians consonance MMN > dissonance MMN,
    # right-lateralized F(1,15)=4.95, p<0.05.
    f02 = torch.sigmoid(
        0.35 * pitch_100ms
        + 0.35 * pitch_mean_1s
    )

    # -- f03: Subadditivity Index --
    # Integration vs summation from cross-feature binding.
    # Rupp/Hansen 2022: musicians > non-musicians in subadditivity for
    # combined melodic deviants (MEG).
    f03 = torch.sigmoid(
        0.35 * binding_100ms
        + 0.35 * binding_std_100ms
    )

    # -- f04: Expertise Effect --
    # Context-dependent expertise advantage: interaction of mismatch and
    # context, scaled by onset velocity (expertise indicator).
    # Rupp/Hansen 2022: no group difference in classic oddball, but
    # musicians > non-musicians in complex melodic paradigm.
    f04 = torch.sigmoid(
        0.35 * f01 * f02
        + 0.30 * onset_vel_100ms
    )

    return f01, f02, f03, f04
