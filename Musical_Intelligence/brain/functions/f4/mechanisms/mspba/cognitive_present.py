"""MSPBA P-Layer -- Cognitive Present (2D).

Present-time harmonic context and violation state for kernel relay export:

  P0: harmonic_context -- Current harmonic context depth [0, 1]
  P1: violation_state  -- Current violation detection state [0, 1]

P0 summarises how much harmonic context has been accumulated. Deeper
context drives the position effect: later chords in a progression have
stronger expectations. The kernel reads this as harmonic prediction
confidence. Maess et al. 2001: position effect (2:1 ratio).

P1 indicates whether the current frame contains an active syntactic
violation being processed by IFG. High violation state means Broca's
area is actively processing a harmonic syntax error (e.g. Neapolitan
substitution). Kim et al. 2021: IFG connectivity enhanced for
syntactic irregularity (F=6.53, p=0.024).

H3 consumed:
    (3, 14, 1, 2)   stumpf_fusion mean H14 L2     -- fusion stability
    (22, 10, 0, 2)  entropy value H10 L2           -- harmonic unpredictability
    (0, 10, 0, 2)   roughness value H10 L2         -- current dissonance

Kernel relay export:
    harmonic_context  [P0, idx 6] -- harmonic stability belief: context depth
    violation_state   [P1, idx 7] -- prediction error: syntactic component

See Building/C3-Brain/F4-Memory-Systems/mechanisms/mspba/MSPBA-cognitive-present.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_STUMPF_MEAN_H14 = (3, 14, 1, 2)        # stumpf_fusion mean H14 L2
_ENTROPY_VAL_H10 = (22, 10, 0, 2)       # entropy value H10 L2
_ROUGHNESS_VAL_H10 = (0, 10, 0, 2)      # roughness value H10 L2


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    s_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """P-layer: 2D present processing from S/M outputs + H3 context.

    P0 (harmonic_context) aggregates harmonic prediction (S1) and
    stumpf fusion stability into a single context-depth indicator.
    Deeper context produces stronger expectations and larger mERAN
    on violation. Maess et al. 2001: position effect (2:1 ratio).

    P1 (violation_state) aggregates mERAN amplitude (M0) and syntax
    violation (M1) with current roughness into a real-time violation
    detection signal. Kim et al. 2021: IFG connectivity enhanced for
    syntactic irregularity (MEG, N=19, F=6.53, p=0.024).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        s_outputs: ``(S0, S1, S2)`` each ``(B, T)``.
        m_outputs: ``(M0, M1, M2)`` each ``(B, T)``.

    Returns:
        ``(P0, P1)`` each ``(B, T)``.
    """
    _s0, s1, _s2 = s_outputs
    m0, m1, _m2 = m_outputs

    # -- H3 features -------------------------------------------------------------
    stumpf_mean = h3_features[_STUMPF_MEAN_H14]              # (B, T)
    entropy_val = h3_features[_ENTROPY_VAL_H10]              # (B, T)
    roughness_val = h3_features[_ROUGHNESS_VAL_H10]          # (B, T)

    # -- P0: Harmonic Context (accumulated tonal context depth) ------------------
    # harmony.mean() -- accumulated tonal context from S1 + fusion stability
    # Maess et al. 2001: position effect (2:1 ratio at position 5 vs 3)
    harmony = 0.50 * s1 + 0.50 * stumpf_mean
    p0 = torch.sigmoid(harmony)

    # -- P1: Violation State (real-time syntactic violation processing) -----------
    # pred_error.mean() -- IFG activity reflecting syntactic violation
    # Kim et al. 2021: IFG connectivity enhanced for irregularity (F=6.53)
    pred_error = 0.40 * m0 + 0.30 * m1 + 0.30 * roughness_val
    p1 = torch.sigmoid(pred_error)

    return p0, p1
