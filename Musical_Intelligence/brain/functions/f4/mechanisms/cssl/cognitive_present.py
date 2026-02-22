"""CSSL P-Layer -- Cognitive Present (2D).

Present-processing integration for cross-species song learning:
  P0: entrainment_state    (current motor-auditory entrainment level)
  P1: template_match       (current song template match quality)

P0 aggregates encoding state from E-layer to reflect real-time rhythmic
entrainment. When high, the listener's motor system is tightly locked
to the musical beat -- the same mechanism songbirds use for vocal practice.

P1 is the present-moment template recognition signal: familiarity times
the consonance-timbre interaction (x_l5l7). High template match means
the current spectrotemporal pattern is being compared against stored
song templates in auditory cortex.

H3 demands consumed:
    (11, 20, 17, 0) onset_strength periodicity H20 L0 -- beat regularity 5s
    (12, 16, 0, 2)  warmth value H16 L2               -- voice quality
    (7, 20, 3, 0)   amplitude std H20 L0              -- energy variability

R3 consumed:
    [41:49] x_l5l7  -- melody-timbre binding for template matching

See Building/C3-Brain/F4-Memory-Systems/mechanisms/cssl/CSSL-cognitive-present.md
Barchet et al. 2024: music-specific ~2 Hz beat entrainment timescale.
Eliades et al. 2024: dual vocal suppression timescales in marmoset auditory cortex.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_ONSET_PERIOD_H20_L0 = (11, 20, 17, 0)  # onset_strength periodicity H20 L0
_WARMTH_VAL_H16_L2 = (12, 16, 0, 2)     # warmth value H16 L2
_AMP_STD_H20_L0 = (7, 20, 3, 0)         # amplitude std H20 L0

# -- R3 feature indices -------------------------------------------------------
_X_L5L7_START = 41
_X_L5L7_END = 49


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e: Tuple[Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute P-layer: entrainment state and template match.

    P0 integrates encoding state (E0+E1 average) with beat regularity
    and dynamic range to assess real-time motor-auditory entrainment.
    When entrainment is strong, the basal ganglia motor loop is tightly
    coupled to the auditory template.

    P1 combines familiarity proxy (M1) with the melody-timbre interaction
    (x_l5l7) to assess present-moment template recognition. High P1 means
    the auditory cortex is actively matching against a stored song template.

    Barchet et al. 2024: music-specific ~2 Hz beat entrainment timescale;
    finger-tapping optimal at 2 Hz for music.
    Eliades et al. 2024: dual vocal suppression timescales (phasic + tonic)
    in marmoset auditory cortex (N=3285 units, r=0.46).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)`` R3 spectral features.
        e: ``(E0, E1, E2)`` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.

    Returns:
        ``(P0, P1)`` each ``(B, T)``
    """
    e0, e1, _e2 = e
    _m0, m1 = m

    # -- H3 reads --
    onset_period = h3_features[_ONSET_PERIOD_H20_L0]  # (B, T)
    amp_std = h3_features[_AMP_STD_H20_L0]            # (B, T)

    # -- R3 reads --
    x_l5l7 = r3_features[..., _X_L5L7_START:_X_L5L7_END]  # (B, T, 8)
    x_l5l7_mean = x_l5l7.mean(dim=-1)                       # (B, T)

    # -- Encoding state proxy --
    encoding_state = 0.5 * e0 + 0.5 * e1  # (B, T)

    # -- P0: Entrainment State --
    # Current motor-auditory entrainment level. Aggregation of encoding
    # state + beat regularity (H3 onset periodicity) + dynamic range.
    # Barchet et al. 2024: ~2 Hz beat entrainment timescale.
    p0 = (
        0.40 * encoding_state
        + 0.35 * onset_period
        + 0.25 * amp_std
    ).clamp(0.0, 1.0)

    # -- P1: Template Match --
    # Current song template match quality. Familiarity proxy (M1)
    # modulated by melody-timbre interaction (x_l5l7).
    # Eliades et al. 2024: dual vocal suppression timescales in marmoset AC.
    p1 = (
        m1 * x_l5l7_mean
    ).clamp(0.0, 1.0)

    return p0, p1
