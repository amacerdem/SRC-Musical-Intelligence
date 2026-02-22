"""ESME P-Layer -- Cognitive Present (3D).

Present-moment deviance detection signals:
  P0: pitch_deviance_detection   -- Current pitch deviance signal [0, 1]
  P1: rhythm_deviance_detection  -- Current rhythm deviance signal [0, 1]
  P2: timbre_deviance_detection  -- Current timbre deviance signal [0, 1]

The P-layer decomposes the unified expertise-MMN function into three
domain-specific present-moment detection signals. These represent the
raw deviance detection happening right now in the auditory system,
before expertise modulation.

P0 (pitch_deviance_detection): Absolute pitch change velocity from
E-layer's pitch_change_vel H3 feature, with tonalness template context.
Wagner et al. 2018: pre-attentive harmonic interval MMN = -0.34 uV
at 173ms (p = 0.003).

P1 (rhythm_deviance_detection): Absolute onset timing deviation from
E-layer's onset_val H3 feature.
Vuust et al. 2012: jazz musicians show strongest MMN for complex
rhythmic deviants.

P2 (timbre_deviance_detection): Timbre envelope change from E-layer's
timbre_change_std, with warmth instantaneous context.
Tervaniemi 2022: trained parameter evokes the largest MMN.

H3 demands consumed (2 tuples):
  (12, 2, 0, 2)  warmth value H2 L2          -- warmth instantaneous 17ms
  (14, 5, 1, 0)  tonalness mean H5 L0        -- tonalness template 46ms

Dependencies:
  E-layer f01 (pitch_mmn) -- pitch deviance context
  E-layer f02 (rhythm_mmn) -- rhythm deviance context
  E-layer f03 (timbre_mmn) -- timbre deviance context
  M-layer mmn_expertise_function -- unified metric
  H3 pitch_change_vel, onset_val, timbre_change_std (reused from E-layer)
  R3[12] warmth -- timbre baseline
  R3[14] tonalness -- pitch clarity

See Building/C3-Brain/F8-Learning-and-Plasticity/mechanisms/esme/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed (2 P-layer tuples) --------------------------------
_WARMTH_VAL_H2 = (12, 2, 0, 2)          # #10: warmth instantaneous 17ms
_TONAL_MEAN_H5 = (14, 5, 1, 0)          # #11: tonalness template 46ms

# -- E-layer H3 tuple keys (reused for raw deviance) --------------------------
_PITCH_VEL_H3 = (23, 3, 8, 0)           # E#2: pitch deviant velocity 100ms
_ONSET_VAL_H3 = (11, 3, 0, 0)           # E#3: onset strength 100ms
_TIMBRE_STD_H8 = (24, 8, 2, 0)          # E#9: timbre change std 300ms

# -- R3 indices ----------------------------------------------------------------
_WARMTH = 12
_TONALNESS = 14


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor],
    ednr: Tensor,
    tscp: Tensor,
    cdmr: Tensor,
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute P-layer: 3D present-moment deviance detection.

    P0 (pitch_deviance_detection): Absolute pitch change velocity with
    tonalness context. Captures the pre-attentive pitch deviance signal
    that generates the pitch MMN component at ~150-250ms post-deviant.
    Wagner et al. 2018: harmonic interval MMN = -0.34 uV at 173ms.
    Koelsch et al. 1999: violinists detect 0.75% deviants.

    P1 (rhythm_deviance_detection): Absolute onset timing deviation.
    Captures temporal deviance generating the rhythm MMN component.
    Vuust et al. 2012: jazz musicians show strongest response.
    Liao et al. 2024: percussionists NMR network.

    P2 (timbre_deviance_detection): Timbre envelope change with warmth
    context at gamma-band. Captures spectral deviance generating the
    timbre MMN component.
    Tervaniemi 2022: trained parameter evokes largest MMN.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 spectral features.
        e_outputs: ``(f01, f02, f03, f04)`` each ``(B, T)``
            from extraction layer.
        m_outputs: ``(mmn_expertise_function,)`` each ``(B, T)``
            from temporal integration layer.
        ednr: ``(B, T, 10)`` upstream EDNR output.
        tscp: ``(B, T, 10)`` upstream TSCP output.
        cdmr: ``(B, T, 11)`` upstream CDMR output.

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``.
    """
    _f01, _f02, _f03, _f04 = e_outputs
    (_mmn_expertise,) = m_outputs

    # -- H3 features (P-layer own) ---------------------------------------------
    warmth_val = h3_features[_WARMTH_VAL_H2]             # (B, T) -- 17ms warmth
    tonal_mean = h3_features[_TONAL_MEAN_H5]             # (B, T) -- 46ms tonalness

    # -- H3 features (reused from E-layer for raw deviance) --------------------
    pitch_vel = h3_features[_PITCH_VEL_H3]               # (B, T) -- pitch velocity
    onset_val = h3_features[_ONSET_VAL_H3]               # (B, T) -- onset strength
    timbre_std = h3_features[_TIMBRE_STD_H8]             # (B, T) -- timbre change

    # -- P0: Pitch Deviance Detection ------------------------------------------
    # sigma(0.50 * abs(pitch_change_vel) + 0.30 * tonalness_template
    #       + 0.20 * r3_tonalness)
    # Wagner et al. 2018: pre-attentive harmonic interval MMN
    # Fong et al. 2020: 150-250ms post-deviant
    p0 = torch.sigmoid(
        0.50 * pitch_vel.abs()
        + 0.30 * tonal_mean
        + 0.20 * r3_features[..., _TONALNESS]
    )

    # -- P1: Rhythm Deviance Detection -----------------------------------------
    # sigma(0.50 * abs(onset_val) + 0.30 * onset_val
    #       + 0.20 * r3_warmth)
    # Vuust et al. 2012: jazz > rock > pop > non-musicians
    # Liao et al. 2024: percussionists NMR network
    p1 = torch.sigmoid(
        0.50 * onset_val.abs()
        + 0.30 * onset_val
        + 0.20 * r3_features[..., _WARMTH]
    )

    # -- P2: Timbre Deviance Detection -----------------------------------------
    # sigma(0.50 * timbre_change_std + 0.30 * warmth_instantaneous
    #       + 0.20 * r3_warmth)
    # Tervaniemi 2022: trained parameter evokes largest MMN
    p2 = torch.sigmoid(
        0.50 * timbre_std
        + 0.30 * warmth_val
        + 0.20 * r3_features[..., _WARMTH]
    )

    return p0, p1, p2
