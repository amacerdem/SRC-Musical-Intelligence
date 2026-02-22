"""TSCP P-Layer -- Cognitive Present (3D).

Timbre-Specific Cortical Plasticity real-time cognitive state:
  recognition_quality (idx 4)  -- Template matching quality [0, 1]
  enhanced_response   (idx 5)  -- Training-dependent cortical enhancement [0, 1]
  timbre_identity     (idx 6)  -- Feature binding coherence [0, 1]

recognition_quality evaluates how well the incoming spectral envelope
matches stored instrument template representations. Based on warmth and
sharpness features at 17ms (H3 short-horizon). Maps to L-SMG/HG (Bellmann
& Asano 2024: ALE peak, 4640 mm3 -- primary timbre processing cluster).

enhanced_response combines the M-layer enhancement function with current
tonalness to produce a real-time measure of training-dependent cortical
enhancement. Captures the ATT-like boost that trained timbres receive
during auditory processing. Alluri et al. 2012: timbral brightness
bilateral STG Z=8.13, timbral fullness Z=7.35.

timbre_identity binds multiple spectral features (tristimulus balance,
inharmonicity inverse, spectral autocorrelation) into a unified instrument
identity representation. Maps to distinct STG sub-regions (Sturm et al.
2014: ECoG high-gamma).

H3 demands consumed (2 tuples):
  (12, 2, 0, 2)  warmth value H2 L2       -- current warmth at 17ms
  (13, 2, 0, 2)  sharpness value H2 L2    -- current sharpness at 17ms

R3 features:
  [14] tonalness (harmonic-to-noise ratio)
  [5]  inharmonicity (instrument character)
  [17] spectral_autocorrelation (harmonic periodicity)
  [12] warmth (spectral warmth for template matching)
  [13] sharpness (spectral sharpness for template matching)

See Building/C3-Brain/F8-Learning-and-Plasticity/mechanisms/tscp/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed (2 tuples) ----------------------------------------------
_WARMTH_VALUE_H2 = (12, 2, 0, 2)       # warmth value H2 L2
_SHARPNESS_VALUE_H2 = (13, 2, 0, 2)    # sharpness value H2 L2

# -- R3 feature indices (post-freeze 97D) ------------------------------------
_INHARMONICITY = 5
_TONALNESS = 14
_SPECTRAL_AUTOCORRELATION = 17


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor],
    ednr: Tensor,
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute P-layer: real-time timbre perception and plasticity state.

    recognition_quality (idx 4): Template matching quality. Aggregation of
    warmth and sharpness at 17ms for real-time instrument identity matching.
    Maps to L-SMG/HG (Bellmann & Asano 2024: ALE peak, 4640 mm3).

    enhanced_response (idx 5): Training-dependent cortical response
    enhancement. sigma(0.60 * enhancement_function + 0.40 * tonalness).
    Captures ATT-like boost for trained timbres. Alluri et al. 2012:
    bilateral STG Z=8.13 for timbral brightness.

    timbre_identity (idx 6): Feature binding coherence. sigma(0.40 *
    trist_balance + 0.30 * (1-inharmonicity) + 0.30 * spectral_autocorrelation).
    Binds spectral features into a unified instrument identity. Sturm et al.
    2014: ECoG high-gamma shows distinct STG sub-regions for timbre.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        e_outputs: ``(f01, f02, f03)`` from extraction layer.
        m_outputs: ``(enhancement_function,)`` from temporal integration layer.
        ednr: ``(B, T, 10)`` from upstream EDNR relay.

    Returns:
        ``(recognition_quality, enhanced_response, timbre_identity)`` each ``(B, T)``
    """
    f01, _f02, _f03 = e_outputs
    (enhancement_function,) = m_outputs

    # -- H3 features --
    warmth_h2 = h3_features[_WARMTH_VALUE_H2]                # (B, T)
    sharpness_h2 = h3_features[_SHARPNESS_VALUE_H2]          # (B, T)

    # -- R3 features --
    tonalness = r3_features[..., _TONALNESS]                 # (B, T)
    inharmonicity = r3_features[..., _INHARMONICITY]         # (B, T)
    spectral_autocorr = r3_features[..., _SPECTRAL_AUTOCORRELATION]  # (B, T)

    # -- Recompute tristimulus balance from E-layer's f01 context --
    # Use warmth and sharpness H3 features as template matching quality.
    # recognition_quality maps to L-SMG/HG instrument template storage.
    # Bellmann & Asano 2024: ALE peak, 4640 mm3
    recognition_quality = torch.sigmoid(
        0.50 * warmth_h2.clamp(0.0, 1.0)
        + 0.50 * sharpness_h2.clamp(0.0, 1.0)
    )

    # -- enhanced_response --
    # sigma(0.60 * enhancement_function + 0.40 * tonalness)
    # Combines M-layer gate with current tonalness for real-time enhancement.
    # Alluri et al. 2012: bilateral STG Z=8.13 timbral brightness, Z=7.35 fullness
    enhanced_response = torch.sigmoid(
        0.60 * enhancement_function
        + 0.40 * tonalness.clamp(0.0, 1.0)
    )

    # -- Tristimulus balance from f01 -- reuse the E-layer concept --
    # f01 already encodes trist_balance + harmonic_purity. We use f01 as
    # a proxy for the tristimulus-balance component of timbre identity.
    # (Cannot recompute trist_balance here without H3 tuples already consumed
    # by E-layer -- reusing f01 avoids duplicate H3 demand.)

    # -- timbre_identity --
    # sigma(0.40 * trist_balance_proxy + 0.30 * (1-inharmonicity)
    #        + 0.30 * spectral_autocorrelation)
    # Sturm et al. 2014: distinct STG sub-regions for timbre via ECoG high-gamma
    timbre_identity = torch.sigmoid(
        0.40 * f01
        + 0.30 * (1.0 - inharmonicity.clamp(0.0, 1.0))
        + 0.30 * spectral_autocorr.clamp(0.0, 1.0)
    )

    return recognition_quality, enhanced_response, timbre_identity
