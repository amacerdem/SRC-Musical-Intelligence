"""PSH E-Layer — Extraction (2D).

High-level silencing proxy and low-level persistence proxy from raw R3:
  E0: high_level_silencing   (harmonic/tonal features susceptible to silencing)
  E1: low_level_persistence  (sensory features that always persist post-stimulus)

The core insight from de Vries & Wurm 2023: high-level abstract
representations (harmonic structure, tonal patterns) are "silenced"
(explained away) when top-down predictions are accurate, while low-level
sensory features (amplitude, onset) persist as prediction errors regardless
of prediction accuracy.

E0 extracts the high-level signal from consonance (sensory_pleasantness),
tonal structure (periodicity), and harmonic balance (tristimulus). These
are the features that get suppressed when predictions are correct.

E1 extracts the low-level signal from amplitude and onset strength. These
are the features that persist as PE signals even when predictions match.

R3 direct reads:
  [4]     sensory_pleasantness  (high-level harmonic)
  [5]     periodicity           (high-level tonal structure)
  [7]     amplitude             (low-level sensory)
  [11]    onset_strength        (change detection / PE trigger)
  [18:21] tristimulus1-3        (high-level harmonic balance)

H3 demands consumed: none (pure R3 extraction).

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/psh/
de Vries & Wurm 2023: high-level silenced, low-level persists.
"""
from __future__ import annotations

from typing import Tuple

import torch
from torch import Tensor

# -- R3 indices (post-freeze 97D) --------------------------------------------
_SENSORY_PLEAS = 4        # sensory_pleasantness (A group, high-level harmonic)
_PERIODICITY = 5          # periodicity (A group, high-level tonal structure)
_AMPLITUDE = 7            # amplitude (B group, low-level sensory)
_ONSET_STRENGTH = 11      # onset_strength (B group, change detection)
_TRISTIMULUS_START = 18   # tristimulus1 (C group)
_TRISTIMULUS_END = 21     # tristimulus3 (C group, exclusive)


def compute_extraction(
    r3_features: Tensor,
) -> Tuple[Tensor, Tensor]:
    """Compute E-layer: high-level silencing proxy and low-level persistence.

    E0 captures the high-level harmonic/tonal representation that is
    susceptible to prediction silencing. When top-down predictions are
    accurate, these features are "explained away" and suppressed
    post-stimulus (de Vries & Wurm 2023: eta_p^2 = 0.49).

    E1 captures the low-level sensory representation that persists
    regardless of prediction accuracy. Amplitude and onset strength
    continue to produce prediction errors even when high-level
    predictions are fulfilled.

    Args:
        r3_features: ``(B, T, 97)`` raw R3.

    Returns:
        ``(E0, E1)`` each ``(B, T)``
    """
    # -- R3 direct reads --
    consonance = r3_features[..., _SENSORY_PLEAS]          # (B, T)
    periodicity = r3_features[..., _PERIODICITY]            # (B, T)
    amplitude = r3_features[..., _AMPLITUDE]                # (B, T)
    onset = r3_features[..., _ONSET_STRENGTH]               # (B, T)
    trist_mean = r3_features[..., _TRISTIMULUS_START:_TRISTIMULUS_END].mean(
        dim=-1
    )  # (B, T) — harmonic balance as high-level abstract signal

    # -- E0: High-Level Silencing Proxy --
    # Harmonic structure (tristimulus) + tonal pattern (periodicity) +
    # consonance. These are the abstract features that get silenced
    # when predictions match. de Vries & Wurm 2023: view-invariant
    # (abstract) representations silenced post-stimulus.
    e0 = torch.sigmoid(
        0.35 * trist_mean
        + 0.35 * consonance
        + 0.30 * periodicity
    )

    # -- E1: Low-Level Persistence Proxy --
    # Amplitude and onset strength — raw sensory features that always
    # persist. de Vries & Wurm 2023: low-level (optical flow / sensory)
    # representations persist regardless of prediction accuracy.
    # Todorovic 2012: low-level PE survives repetition suppression.
    e1 = torch.sigmoid(
        0.55 * amplitude
        + 0.45 * onset
    )

    return e0, e1
