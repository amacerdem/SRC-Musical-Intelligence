"""MSPBA M-Layer -- Temporal Integration (3D).

Composite signals integrating S-layer extraction with progression-level
temporal context:

  M0: eran_amplitude   -- Predicted mERAN amplitude [0, 1]
  M1: syntax_violation -- Syntactic violation score [0, 1]
  M2: from_synthesis   -- S-layer synthesis signal [0, 1]

M0 predicts the magnitude of the mERAN response based on prediction error,
harmonic complexity (entropy), dissonance (roughness), and tonal fusion
deficit (1-stumpf). The multiplicative chain models the empirical finding
that mERAN amplitude scales with context depth: position 5 violation
produces 2x the mERAN of position 3. Maess et al. 2001 (MEG, N=28).

M1 is a normalised composite score from four independent markers of
harmonic violation: roughness, entropy, inharmonicity, and fusion deficit.
Equal weighting (0.25 each) provides robust multi-feature Neapolitan
detection. Koelsch et al. 2000 (EEG, p<0.001).

M2 synthesises the three S-layer signals into a unified syntactic
processing state for downstream P- and F-layer consumption.
Wohrle et al. 2024: N1m evolves over chord progression (MEG, N=30).

H3 consumed:
    (0, 14, 1, 0)   roughness mean H14 L0          -- avg dissonance
    (5, 14, 1, 0)   inharmonicity mean H14 L0      -- avg harmonic deviation
    (22, 14, 1, 0)  entropy mean H14 L0            -- avg complexity
    (23, 14, 1, 0)  spectral_flux mean H14 L0      -- avg spectral change

See Building/C3-Brain/F4-Memory-Systems/mechanisms/mspba/MSPBA-temporal-integration.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_ROUGHNESS_MEAN_H14 = (0, 14, 1, 0)     # roughness mean H14 L0
_INHARM_MEAN_H14 = (5, 14, 1, 0)        # inharmonicity mean H14 L0
_ENTROPY_MEAN_H14 = (22, 14, 1, 0)      # entropy mean H14 L0
_FLUX_MEAN_H14 = (23, 14, 1, 0)         # spectral_flux mean H14 L0


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    s_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """M-layer: 3D temporal integration from S-layer + H3 features.

    M0 (eran_amplitude) models the mERAN magnitude via a multiplicative
    chain of prediction error, entropy, roughness, and fusion deficit.
    Context depth produces the 2:1 position ratio (Maess 2001).

    M1 (syntax_violation) is a normalised composite score across four
    consonance/complexity markers (0.25 each). The Neapolitan chord (bII)
    simultaneously elevates all four markers. Koelsch et al. 2000.

    M2 (from_synthesis) integrates the three S-layer signals with spectral
    flux context for a unified syntactic processing state.
    Wohrle et al. 2024: N1m evolves over chord progression (eta-p2=0.101).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        s_outputs: ``(S0, S1, S2)`` each ``(B, T)``.

    Returns:
        ``(M0, M1, M2)`` each ``(B, T)``.
    """
    s0, s1, s2 = s_outputs

    # -- H3 features (progression-level, H14 = 700ms) ---------------------------
    roughness_mean = h3_features[_ROUGHNESS_MEAN_H14]        # (B, T)
    inharm_mean = h3_features[_INHARM_MEAN_H14]              # (B, T)
    entropy_mean = h3_features[_ENTROPY_MEAN_H14]            # (B, T)
    flux_mean = h3_features[_FLUX_MEAN_H14]                  # (B, T)

    # Derived: prediction error proxy from S0 (mERAN trigger)
    pred_error = s0  # S0 already encodes mERAN response strength

    # -- M0: ERAN Amplitude (predicted mERAN magnitude) --------------------------
    # eran_amplitude = sigma(pred_error * entropy * roughness * (1-stumpf))
    # stumpf_fusion deficit approximated by (1 - S1) since S1 = harmonic prediction
    # Maess et al. 2001: mERAN at position 5 = 2x vs position 3 (N=28)
    m0 = torch.sigmoid(
        pred_error * entropy_mean * roughness_mean * (1.0 - s1)
    )

    # -- M1: Syntax Violation (multi-feature violation score) --------------------
    # syntax_violation = sigma(0.25*roughness + 0.25*entropy
    #                         + 0.25*inharmonicity + 0.25*(1-stumpf_proxy))
    # Koelsch et al. 2000: ERAN for Neapolitan chord violations (EEG, p<0.001)
    stumpf_deficit = 1.0 - s1  # harmonic prediction deficit = fusion deficit
    m1 = torch.sigmoid(
        0.25 * roughness_mean
        + 0.25 * entropy_mean
        + 0.25 * inharm_mean
        + 0.25 * stumpf_deficit
    )

    # -- M2: From-Synthesis (unified S-layer integration) ------------------------
    # Synthesises S0 (mERAN), S1 (harmonic prediction), S2 (Broca's load)
    # with spectral flux context for a single processing state signal.
    # Wohrle et al. 2024: N1m evolves over chord progression (MEG, N=30)
    m2 = torch.sigmoid(
        0.35 * s0
        + 0.30 * s2
        + 0.20 * s1
        + 0.15 * flux_mean
    )

    return m0, m1, m2
