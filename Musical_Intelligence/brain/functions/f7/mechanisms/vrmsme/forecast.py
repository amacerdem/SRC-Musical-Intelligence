"""VRMSME F-Layer -- Forecast (3D).

Forward predictions for VR music stimulation motor enhancement:
  enhancement_pred    -- Motor enhancement prediction [0, 1]
  connectivity_pred   -- Network connectivity prediction [0, 1]
  bilateral_pred      -- Bilateral activation prediction [0, 1]

enhancement_pred predicts near-future motor enhancement strength.
Combines current music enhancement (f16) with sustained multi-modal
coupling periodicity at 1s. Periodic auditory-motor coupling with
strong current enhancement predicts continued VRMS advantage.

connectivity_pred predicts near-future PM-DLPFC-M1 network connectivity.
Combines current network connectivity (f18) with sustained sensorimotor
binding periodicity at 1s.

bilateral_pred predicts near-future bilateral sensorimotor activation
balance. Integrates f17 (bilateral_activation) with sensorimotor binding
stability to forecast whether bilateral M1 engagement will persist.

H3 demands: This layer introduces 0 new H3 tuples. It reuses from E-layer:
  coupling_period_1s:     (25, 16, 14, 2) from E-layer tuple #6
  sensorimotor_period_1s: (33, 16, 14, 2) from E-layer tuple #10

Blasi et al. 2025: music/dance interventions produce structural +
functional neuroplasticity (20 RCTs, N=718).

Sarasso et al. 2019: appreciated musical intervals enhance N1/P2 and
modulate bilateral motor cortex.

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/vrmsme/f_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples reused from E-layer -------------------------------------------
_COUPLING_PERIOD_1S = (25, 16, 14, 2)         # coupling periodicity 1s
_SENSORI_PERIOD_1S = (33, 16, 14, 2)          # sensorimotor period 1s
_SENSORI_STD_100MS = (33, 3, 2, 2)            # binding variability 100ms


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor, Tensor],
    p: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """F-layer: 3D forward predictions from E/M/P features + H3 reuse.

    Generates three forward-looking predictions about the state of the
    VR music stimulation system.

    enhancement_pred = sigma(0.5 * f16 + 0.5 * coupling_period_1s)
    connectivity_pred = sigma(0.5 * f18 + 0.5 * sensorimotor_period_1s)
    bilateral_pred = sigma(0.5 * f17 + 0.5 * binding_stability)

    Blasi et al. 2025: structural + functional neuroplasticity (20 RCTs).
    Sarasso et al. 2019: bilateral motor cortex modulation.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e: ``(f16, f17, f18)`` from extraction layer.
        m: ``(vrms_advantage, bilateral_index, connectivity_strength)``
            from temporal integration layer.
        p: ``(motor_drive, sensorimotor_sync)`` from cognitive present layer.

    Returns:
        ``(enhancement_pred, connectivity_pred, bilateral_pred)``
        each ``(B, T)``.
    """
    f16, f17, f18 = e
    _vrms_advantage, _bilateral_index, _connectivity_strength = m
    motor_drive, sensorimotor_sync = p

    # -- H3 features (reused from E-layer) --
    coupling_period_1s = h3_features[_COUPLING_PERIOD_1S]    # sustained coupling
    sensori_period_1s = h3_features[_SENSORI_PERIOD_1S]      # sustained binding
    sensori_std_100ms = h3_features[_SENSORI_STD_100MS]      # binding variability

    # Binding stability: inverse of binding variability (low variability
    # = high stability), bounded by sigmoid.
    binding_stability = 1.0 - sensori_std_100ms.abs().clamp(max=1.0)

    # -- enhancement_pred --
    # Predicts motor enhancement continuation. Current music enhancement
    # (f16) with sustained coupling periodicity.
    # Blasi 2025: neuroplasticity from music/dance interventions (20 RCTs).
    enhancement_pred = torch.sigmoid(
        0.50 * f16 + 0.50 * coupling_period_1s
    )

    # -- connectivity_pred --
    # Predicts network connectivity maintenance. Current network connectivity
    # (f18) with sustained sensorimotor binding periodicity.
    # Liang 2025: sustained network connectivity for rehabilitation.
    connectivity_pred = torch.sigmoid(
        0.50 * f18 + 0.50 * sensori_period_1s
    )

    # -- bilateral_pred --
    # Predicts bilateral activation persistence. Current bilateral
    # activation (f17) with sensorimotor binding stability.
    # Sarasso 2019: bilateral motor cortex modulation by music.
    bilateral_pred = torch.sigmoid(
        0.50 * f17 + 0.50 * binding_stability
    )

    return enhancement_pred, connectivity_pred, bilateral_pred
