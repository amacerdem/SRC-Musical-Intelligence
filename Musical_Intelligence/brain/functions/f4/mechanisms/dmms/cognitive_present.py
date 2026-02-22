"""DMMS P-Layer -- Cognitive Present (2D).

Two present-processing dimensions for developmental scaffold activation:

  P0: scaffold_activation  -- Current scaffold activation level [0, 1]
  P1: bonding_warmth       -- Caregiver-bonding warmth signal [0, 1]

H3 consumed:
    (12, 16, 0, 2)  warmth value H16 L2       -- current voice-warmth (shared E)
    (0, 16, 0, 2)   roughness value H16 L2    -- current consonance (shared E)
    (10, 16, 0, 2)  loudness value H16 L2     -- current arousal level

P-layer primarily aggregates E+M outputs rather than introducing many new
H3 tuples. Only (10, 16, 0, 2) is new to this layer.

See Building/C3-Brain/F4-Memory-Systems/mechanisms/dmms/DMMS-cognitive-present.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_WARMTH_VAL_1S = (12, 16, 0, 2)         # warmth value H16 L2 (shared with E)
_ROUGH_VAL_1S = (0, 16, 0, 2)           # roughness value H16 L2 (shared with E)
_LOUD_VAL_1S = (10, 16, 0, 2)           # loudness value H16 L2 (new)


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """P-layer: 2D present processing from H3 + E/M outputs.

    P0 (scaffold_activation) is the present-moment signal for developmental
    memory scaffold engagement. The product of retrieval state (E0) and
    familiarity (M1) -- both must be active for the scaffold to be
    considered "activated." This captures when current music successfully
    triggers pattern completion of early templates in the hippocampus.
    Nguyen et al. 2023: caregivers universally communicate with infants
    via song; infant-directed singing supports co-regulation.

    P1 (bonding_warmth) is the affective dimension of scaffold activation.
    The triple product (familiarity x warmth x consonance) requires all
    three conditions: the music must be familiar, have warm timbre
    (voice-like), and be consonant (pleasant/safe). This is the "comfort"
    signal that makes childhood music evoke the deepest emotional responses.
    Scholkmann 2024: CMT induces hemodynamic changes in neonatal prefrontal
    and auditory regions (fNIRS, N=17).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(E0, E1, E2)`` each ``(B, T)``.
        m_outputs: ``(M0, M1)`` each ``(B, T)``.

    Returns:
        ``(P0, P1)`` each ``(B, T)``.
    """
    e0, _e1, e2 = e_outputs
    m0, m1 = m_outputs

    # -- H3 features --
    warmth_val_1s = h3_features[_WARMTH_VAL_1S]          # (B, T)
    rough_val_1s = h3_features[_ROUGH_VAL_1S]            # (B, T)
    loud_val_1s = h3_features[_LOUD_VAL_1S]              # (B, T)

    # -- Derived signals --
    consonance = 1.0 - rough_val_1s                       # (B, T)

    # retrieval = E0 (early_binding) -- hippocampal scaffold signal
    retrieval = e0                                         # (B, T)
    # familiarity = M1 (imprinting_depth) -- deep template match
    familiarity = m1                                       # (B, T)

    # P0: Scaffold Activation -- retrieval * familiarity
    # Nguyen 2023: universal infant-directed singing scaffolds memory
    # High when current music activates early templates
    p0 = (retrieval * familiarity).clamp(0.0, 1.0)

    # P1: Bonding Warmth -- familiarity * warmth * consonance
    # Scholkmann 2024: CMT induces neonatal prefrontal hemodynamic changes
    # Triple product: must be familiar + warm + consonant for comfort
    p1 = (familiarity * warmth_val_1s * consonance).clamp(0.0, 1.0)

    return p0, p1
