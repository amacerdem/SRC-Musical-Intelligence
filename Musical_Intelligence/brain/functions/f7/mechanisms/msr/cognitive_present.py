"""MSR P-Layer -- Cognitive Present (3D).

Three present-state assessments of sensorimotor reorganization:

  bottom_up_precision   -- Current neural synchrony precision [0, 1]
  top_down_modulation   -- Current cortical inhibition level [0, 1]
  training_level        -- Estimated expertise marker [0, 1]

H3 consumed (tuples 16-18 from demand spec):
    (25, 16, 21, 2)  x_l0l5 zero_crossings H16 L2 -- coupling phase resets 1s
    (10, 3, 0, 2)    onset_strength value H3 L2     -- onset at 100ms (bottom-up)
    (10, 3, 14, 2)   onset_strength period H3 L2    -- onset periodicity 100ms

E-layer consumed:
    f04 (high_freq_plv)    -- PLV feeds precision and training estimation
    f05 (p2_suppression)   -- P2 feeds modulation and training estimation

M-layer consumed:
    plv_high_freq          -- Continuous PLV for precision assessment
    p2_amplitude           -- P2 level for modulation strength

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/msr/p_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (tuples 16-18 from demand spec) --------------------------------
_COUPLING_ZC_1S = (25, 16, 21, 2)    # #16: coupling phase resets 1s (stability)
_ONSET_VAL_100MS = (10, 3, 0, 2)     # #17: onset at 100ms (bottom-up input)
_ONSET_PERIOD_100MS = (10, 3, 14, 2) # #18: onset periodicity 100ms (regularity)


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """P-layer: 3D present-state assessment from H3/R3 + E/M outputs.

    Evaluates the real-time state of sensorimotor reorganization:
        bottom_up_precision: Instantaneous bottom-up processing quality from
            gamma coupling and onset features. Grahn & Brett 2007.
        top_down_modulation: Instantaneous top-down inhibition from P2
            suppression and coupling phase resets. L. Zhang 2015.
        training_level: Expertise marker from PLV/P2 dissociation pattern:
            sigma(0.5 * f04 + 0.5 * (1 - f05)). L. Zhang 2015.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        e_outputs: ``(f04, f05, f06)`` each ``(B, T)``.
        m_outputs: ``(plv_high_freq, p2_amplitude, efficiency_index)`` each ``(B, T)``.

    Returns:
        ``(bottom_up_precision, top_down_modulation, training_level)`` each ``(B, T)``.
    """
    f04, f05, _f06 = e_outputs
    plv_high_freq, p2_amplitude, _efficiency_index = m_outputs

    # -- H3 features --
    coupling_zc_1s = h3_features[_COUPLING_ZC_1S]
    onset_val_100ms = h3_features[_ONSET_VAL_100MS]
    onset_period_100ms = h3_features[_ONSET_PERIOD_100MS]

    # bottom_up_precision (idx 6): Instantaneous bottom-up processing quality
    # Grahn & Brett 2007: musicians activate PMC, cerebellum, SMA during all rhythms
    # Alpheis 2025: increased FC of dlPFC-putamen (t=4.46) in musician brains
    # Precision from gamma coupling (PLV) + onset value and periodicity at 100ms
    bottom_up_precision = torch.sigmoid(
        0.35 * plv_high_freq
        + 0.25 * onset_val_100ms
        + 0.25 * onset_period_100ms
        + 0.15 * f04
    )

    # top_down_modulation (idx 7): Instantaneous top-down inhibition level
    # L. Zhang 2015: P2 suppression reflects efficient cortical gating
    # Liang 2025: music stimulation enhances PM-SMA, dlPFC, M1 connectivity
    # Zero-crossings at 1s track disruptions -- fewer resets = more stable modulation
    # Inverted zero-crossings: (1 - zc) means high zc -> less stable modulation
    top_down_modulation = torch.sigmoid(
        0.35 * f05
        + 0.30 * (1.0 - coupling_zc_1s)
        + 0.20 * (1.0 - p2_amplitude)
        + 0.15 * onset_period_100ms
    )

    # training_level (idx 8): Inferred expertise marker
    # L. Zhang 2015: musicians had 9.07 +/- 4.68 years training
    # sigma(0.5 * f04 + 0.5 * (1 - f05))
    # High PLV (f04 high) + strong P2 suppression (f05 high -> inverted) = expertise
    training_level = torch.sigmoid(
        0.50 * f04
        + 0.50 * (1.0 - f05)
    )

    return bottom_up_precision, top_down_modulation, training_level
