"""CDEM P-Layer -- Cognitive Present (3D).

Present-processing integration for context-dependent emotional memory:

  P0: binding_state    -- Current cross-modal binding activation [0, 1]
  P1: arousal_gate     -- Context-modulated arousal gate [0, 1]
  P2: from_synthesis   -- Encoding-congruency synthesis [0, 1]

H3 consumed:
    (10, 20, 1, 0)  loudness mean H20 L0         -- average arousal over 5s
    (21, 20, 4, 0)  spectral_flux max H20 L0     -- peak context change 5s
    (11, 20, 4, 0)  onset_strength max H20 L0    -- peak event onset 5s

P-layer primarily aggregates C+M outputs rather than introducing many new
H3 tuples. P2 synthesises encoding_strength (from C-layer) with
congruency_index (M0) to give a hybrid context-encoding signal.

See Building/C3-Brain/F4-Memory-Systems/mechanisms/cdem/CDEM-cognitive-present.md
Borderie 2024: theta-gamma CFC in hippocampus + STS (iEEG).
Mori & Zatorre 2024: state-dependent auditory-reward FC (fMRI, N=49, r=0.53).
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from .extraction import ExtractionResult

# -- H3 tuples ----------------------------------------------------------------
_LOUD_MEAN_5S = (10, 20, 1, 0)
_FLUX_MAX_5S = (21, 20, 4, 0)
_ONSET_MAX_5S = (11, 20, 4, 0)

# -- R3 indices ----------------------------------------------------------------
_STUMPF_FUSION = 3
_ENTROPY = 22


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    c: ExtractionResult,
    m: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """P-layer: 3D present processing from H3/R3 + C/M outputs.

    P0 (binding_state): present-moment cross-modal binding. Product of
    encoding state and stumpf fusion -- both must be active for binding.
    Borderie 2024: theta-gamma CFC in hippocampus + STS during auditory
    memory tasks (iEEG, epilepsy patients).

    P1 (arousal_gate): context-modulated arousal gate. Product of arousal
    and inverse entropy -- high arousal in simple contexts produces strong
    gating, complex contexts suppress the gate.
    Mitterschiffthaler 2007: music alone activates amygdala more strongly.

    P2 (from_synthesis): encoding-congruency synthesis. Combines the
    C-layer encoding_strength with the M-layer congruency_index and
    onset peak salience to assess real-time context-encoding quality.
    Mori & Zatorre 2024: auditory-reward FC predicts chills (r=0.53).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        c: :class:`ExtractionResult` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``.
    """
    m0, m1 = m

    # -- H3 features --
    loud_mean_5s = h3_features[_LOUD_MEAN_5S]    # (B, T)
    flux_max_5s = h3_features[_FLUX_MAX_5S]       # (B, T)
    onset_max_5s = h3_features[_ONSET_MAX_5S]     # (B, T)

    # -- R3 features --
    stumpf = r3_features[..., _STUMPF_FUSION]     # (B, T)
    entropy = r3_features[..., _ENTROPY]           # (B, T)

    # -- Derived signals from C-layer --
    encoding = c.encoding_strength
    arousal = c.arousal

    # -- P0: Binding State --
    # Current cross-modal binding activation
    # encoding_strength.mean * stumpf -- both must be active for binding
    # Borderie 2024: hippocampus + STS theta-gamma coupling
    # Billig 2022: hippocampal trisynaptic loop for auditory binding
    p0 = (encoding * stumpf).clamp(0.0, 1.0)

    # -- P1: Arousal Gate --
    # Context-modulated arousal gate
    # arousal.mean * (1 - entropy) -- high arousal + low entropy = strong gate
    # Mori & Zatorre 2024: state-dependent auditory-reward FC (r=0.53)
    # Calabria 2023: arousal x mood regulation interaction
    p1 = (arousal * (1.0 - entropy)).clamp(0.0, 1.0)

    # -- P2: Synthesis (encoding-congruency) --
    # Hybrid present signal combining encoding trajectory with congruency
    # and onset salience. Captures real-time context-encoding quality.
    # When encoding is strong AND music-mood is congruent, memory binding
    # is at its peak. Onset peaks mark context shift boundaries.
    p2 = torch.sigmoid(
        0.35 * encoding * m0
        + 0.35 * m1 * stumpf
        + 0.30 * onset_max_5s
    )

    return p0, p1, p2
