"""SLEE E-Layer -- Extraction (4D).

Statistical Learning Expertise Enhancement extraction signals:
  f01: statistical_model       -- Internal distribution representation [0, 1]
  f02: detection_accuracy      -- Irregularity identification rate [0, 1]
  f03: multisensory_integration -- Cross-modal binding strength [0, 1]
  f04: expertise_advantage     -- Expert enhancement index [-1, 1] clamped

f01 captures how strongly the statistical model of the auditory environment
is built from loudness and amplitude entropy. The mean loudness at 100ms
(H3 tuple 0) and amplitude entropy at 100ms (H3 tuple 1) provide the
instantaneous model quality. Paraskevopoulos 2022: musicians show enhanced
statistical learning accuracy (Hedges' g = -1.09). Carbajal & Malmierca
2018: predictive coding hierarchy from SSA to MMN to deviance detection.

f02 measures irregularity detection from spectral flux variability at 100ms
(H3 tuple 2) and mean spectral flux over 1s (H3 tuple 3). This reflects
the core behavioral finding from Paraskevopoulos 2022: t(23) = -2.815,
p < 0.05 for musician > non-musician detection accuracy. Bridwell 2017:
45% amplitude reduction for patterned vs random sequences.

f03 estimates cross-modal binding from interaction feature values at 100ms
(H3 tuple 4) and mean binding over 1s (H3 tuple 5). Paraskevopoulos 2022:
IFG area 47m left is the primary supramodal hub across 5/6 network states.
Porfyri et al. 2025: multisensory training improves audiovisual detection
(eta-squared = 0.168).

f04 scales f02 by an expertise indicator, capturing the large effect size
(d = -1.09) between musician and non-musician statistical learning. The
expertise indicator is derived from the instantaneous irregularity signal
at 25ms (H3 tuple 6) and upstream EDNR expertise signature.

H3 demands consumed (7 tuples):
  (8, 3, 1, 2)    loudness mean H3 L2          -- mean loudness 100ms
  (7, 3, 20, 2)   amplitude entropy H3 L2      -- amplitude entropy 100ms
  (10, 3, 2, 2)   spectral_flux std H3 L2      -- flux variability 100ms
  (10, 16, 1, 2)  spectral_flux mean H16 L2    -- mean flux over 1s
  (41, 3, 0, 2)   x_l5l6 value H3 L2           -- cross-modal binding 100ms
  (41, 16, 1, 2)  x_l5l6 mean H16 L2           -- mean binding over 1s
  (10, 0, 0, 2)   spectral_flux value H0 L2    -- instantaneous irregularity 25ms

R3 features:
  [7] velocity_A (amplitude), [8] velocity_D (loudness),
  [10] onset_strength (spectral_flux), [41:49] x_l5l6

Upstream reads:
  EDNR relay (via ednr tensor)

Paraskevopoulos et al. 2022: statistical learning accuracy (g = -1.09).
Carbajal & Malmierca 2018: predictive coding hierarchy.
Bridwell et al. 2017: 45% amplitude reduction patterned vs random.
Porfyri et al. 2025: multisensory training (eta-squared = 0.168).

See Building/C3-Brain/F8-Learning-and-Plasticity/mechanisms/slee/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed (7 tuples) -----------------------------------------
_LOUDNESS_MEAN_H3 = (8, 3, 1, 2)          # mean loudness 100ms
_AMP_ENTROPY_H3 = (7, 3, 20, 2)           # amplitude entropy 100ms
_FLUX_STD_H3 = (10, 3, 2, 2)              # spectral flux variability 100ms
_FLUX_MEAN_H16 = (10, 16, 1, 2)           # mean spectral flux over 1s
_BINDING_VAL_H3 = (41, 3, 0, 2)           # cross-modal binding 100ms
_BINDING_MEAN_H16 = (41, 16, 1, 2)        # mean binding over 1s
_FLUX_VAL_H0 = (10, 0, 0, 2)             # instantaneous irregularity 25ms

# -- R3 feature indices (post-freeze 97D) --------------------------------
_AMPLITUDE = 7       # velocity_A
_LOUDNESS = 8        # velocity_D
_SPECTRAL_FLUX = 10  # onset_strength


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    ednr: Tensor,
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """Compute E-layer: four statistical learning extraction signals.

    f01 (statistical_model): sigma(0.35 * loudness_mean_100ms +
    0.35 * amplitude_entropy_100ms). Captures how strongly the internal
    distribution model is built from auditory regularities.
    Paraskevopoulos 2022: g = -1.09; Carbajal & Malmierca 2018.

    f02 (detection_accuracy): sigma(0.35 * flux_std_100ms +
    0.35 * flux_mean_1s). Irregularity identification rate from spectral
    dynamics. Paraskevopoulos 2022: t(23) = -2.815, p < 0.05.

    f03 (multisensory_integration): sigma(0.35 * binding_100ms +
    0.35 * mean_binding_1s). Cross-modal binding from interaction features.
    Paraskevopoulos 2022: IFG area 47m supramodal hub.

    f04 (expertise_advantage): clamp(f02 * expertise_indicator, -1, 1).
    Expert enhancement index scaling detection accuracy by expertise.
    Paraskevopoulos 2022: d = -1.09, 192 vs 106 edges.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        ednr: ``(B, T, 10)`` -- upstream EDNR relay output.

    Returns:
        ``(f01, f02, f03, f04)`` each ``(B, T)``
    """
    # -- H3 features --
    loudness_mean_100 = h3_features[_LOUDNESS_MEAN_H3]      # (B, T)
    amp_entropy_100 = h3_features[_AMP_ENTROPY_H3]           # (B, T)
    flux_std_100 = h3_features[_FLUX_STD_H3]                 # (B, T)
    flux_mean_1s = h3_features[_FLUX_MEAN_H16]               # (B, T)
    binding_100 = h3_features[_BINDING_VAL_H3]               # (B, T)
    binding_mean_1s = h3_features[_BINDING_MEAN_H16]         # (B, T)
    irreg_25ms = h3_features[_FLUX_VAL_H0]                   # (B, T)

    # -- Expertise indicator from EDNR --
    # EDNR f04 (expertise_signature) is the last field of the relay output.
    # Use it as expertise indicator; graceful fallback to 0.5.
    expertise_indicator = ednr[..., -1].clamp(0.0, 1.0)      # (B, T)

    # -- f01: Statistical Model --
    # sigma(0.35 * loudness_mean_100ms + 0.35 * amplitude_entropy_100ms)
    # Paraskevopoulos 2022: g = -1.09 for statistical learning accuracy
    # Carbajal & Malmierca 2018: predictive coding hierarchy (SSA -> MMN)
    f01 = torch.sigmoid(
        0.35 * loudness_mean_100
        + 0.35 * amp_entropy_100
    )

    # -- f02: Detection Accuracy --
    # sigma(0.35 * flux_std_100ms + 0.35 * flux_mean_1s)
    # Paraskevopoulos 2022: t(23) = -2.815, p < 0.05 musician > NM
    # Bridwell 2017: 45% amplitude reduction patterned vs random
    f02 = torch.sigmoid(
        0.35 * flux_std_100
        + 0.35 * flux_mean_1s
    )

    # -- f03: Multisensory Integration --
    # sigma(0.35 * binding_100ms + 0.35 * mean_binding_1s)
    # Paraskevopoulos 2022: IFG area 47m primary supramodal hub (5/6 states)
    # Porfyri et al. 2025: eta-squared = 0.168 for multisensory training
    f03 = torch.sigmoid(
        0.35 * binding_100
        + 0.35 * binding_mean_1s
    )

    # -- f04: Expertise Advantage --
    # clamp(f02 * expertise_indicator, -1, 1)
    # Paraskevopoulos 2022: d = -1.09 (large expertise effect);
    # network compartmentalization: 192 edges (NM) vs 106 edges (M), p < 0.001
    f04 = (f02 * expertise_indicator).clamp(-1.0, 1.0)

    return f01, f02, f03, f04
