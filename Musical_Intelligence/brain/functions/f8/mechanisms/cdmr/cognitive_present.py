"""CDMR P-Layer -- Cognitive Present (3D).

Context-Dependent Mismatch Response present-state estimates:
  mismatch_signal  -- Current expectation violation [0, 1]
  context_state    -- Current context integration level [0, 1]
  binding_state    -- Multi-feature integration state [0, 1]

mismatch_signal is the core MMN-like signal combining instantaneous deviance
with context-modulated sensitivity. When melodic expectation is strong (rich
context), the mismatch signal is amplified for experts. When expectation is
weak (simple oddball), the signal reflects only basic deviance detection.
Rupp/Hansen 2022: context-dependent MMR in musicians at MEG.
Crespo-Bojorque 2018: consonance MMN at 172-250ms, dissonance late MMN at
232-314ms.

context_state is a real-time assessment of melodic context richness from
context modulation (f02), melodic expectation (M-layer), and tonal context.
Serves as the gate determining whether expertise effects are expressed.
Rupp/Hansen 2022: musicians = non-musicians in oddball (low context) but
musicians > non-musicians in melodic (high context).

binding_state reflects the current degree of multi-feature integration from
subadditivity index (f03) and pattern coupling (x_l4l5 at 100ms). High
binding indicates multiple deviant features are processed as an integrated
whole. Maps to fronto-central cortex (Crespo-Bojorque 2018: Fz).

H3 demands consumed (3 tuples):
  (13, 3, 0, 2)   brightness value H3 L2          -- tonal context 100ms
  (13, 3, 20, 2)  brightness entropy H3 L2        -- tonal entropy 100ms
  (33, 3, 0, 2)   x_l4l5 value H3 L2             -- pattern coupling 100ms

Dependencies:
  E-layer f01 (mismatch_amplitude)
  E-layer f02 (context_modulation)
  E-layer f03 (subadditivity_index)
  M-layer melodic_expectation
  R3 [13] brightness, R3 [33:41] x_l4l5
  EDNR relay (upstream)

See Building/C3-Brain/F8-Learning-and-Plasticity/mechanisms/cdmr/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_BRIGHTNESS_VAL_H3 = (13, 3, 0, 2)      # tonal context at 100ms
_BRIGHTNESS_ENT_H3 = (13, 3, 20, 2)     # tonal entropy at 100ms
_PATTERN_COUPLING_H3 = (33, 3, 0, 2)    # pattern coupling at 100ms


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor],
    ednr: Tensor,
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute P-layer: mismatch signal, context state, and binding state.

    mismatch_signal (idx 6) combines E-layer mismatch amplitude (f01) with
    M-layer melodic expectation to produce a context-sensitive violation
    signal. Brightness entropy at 100ms provides a tonal context quality
    measure that further gates the signal.
    Rupp/Hansen 2022: context-dependent MMR in musicians at MEG.
    Crespo-Bojorque 2018: consonance MMN at 172-250ms.

    context_state (idx 7) assesses melodic context richness from context
    modulation (f02), melodic expectation (M-layer), and tonal context
    (brightness at 100ms). This gate determines whether expertise effects
    are expressed.
    Rupp/Hansen 2022: musicians = non-musicians in oddball but
    musicians > non-musicians in melodic context.

    binding_state (idx 8) reflects current multi-feature integration from
    subadditivity index (f03) and pattern coupling (x_l4l5 at 100ms).
    Maps to IFG-auditory cortex interaction.
    Crespo-Bojorque 2018: fronto-central distribution (Fz).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        e_outputs: ``(f01, f02, f03, f04)`` from extraction layer.
        m_outputs: ``(melodic_expectation, deviance_history)`` from M-layer.
        ednr: ``(B, T, 10)`` upstream EDNR relay output.

    Returns:
        ``(mismatch_signal, context_state, binding_state)`` each ``(B, T)``
    """
    f01, f02, f03, _f04 = e_outputs
    melodic_expectation, _deviance_history = m_outputs

    # -- H3 features --
    brightness_100ms = h3_features[_BRIGHTNESS_VAL_H3]      # (B, T)
    brightness_ent_100ms = h3_features[_BRIGHTNESS_ENT_H3]  # (B, T)
    pattern_coupling = h3_features[_PATTERN_COUPLING_H3]     # (B, T)

    # -- mismatch_signal --
    # Combines mismatch amplitude (f01) with melodic expectation for
    # context-sensitive violation detection. Brightness entropy at 100ms
    # provides tonal context quality gating.
    # Rupp/Hansen 2022: context-dependent MMR in musicians at MEG.
    # Crespo-Bojorque 2018: consonance MMN at 172-250ms.
    mismatch_signal = torch.sigmoid(
        0.35 * f01
        + 0.30 * melodic_expectation
        + 0.25 * brightness_ent_100ms
    )

    # -- context_state --
    # Real-time assessment of melodic context richness from context
    # modulation (f02), melodic expectation, and tonal context (brightness).
    # Serves as the gate for expertise effects.
    # Rupp/Hansen 2022: musicians = non-musicians in oddball (low context)
    # but musicians > non-musicians in melodic (high context).
    context_state = torch.sigmoid(
        0.35 * f02
        + 0.30 * melodic_expectation
        + 0.25 * brightness_100ms
    )

    # -- binding_state --
    # Current multi-feature integration from subadditivity index (f03) and
    # pattern coupling (x_l4l5 at 100ms). High binding = integrated
    # processing of multiple deviant features.
    # Crespo-Bojorque 2018: fronto-central distribution (Fz).
    binding_state = torch.sigmoid(
        0.40 * f03
        + 0.30 * pattern_coupling
    )

    return mismatch_signal, context_state, binding_state
