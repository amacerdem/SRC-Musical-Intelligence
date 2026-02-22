"""VRMSME P-Layer -- Cognitive Present (2D).

Present-time VR music stimulation motor signals:
  motor_drive          -- Music-driven motor activation level [0, 1]
  sensorimotor_sync    -- Sensorimotor synchronization state [0, 1]

motor_drive captures the instantaneous motor activation driven by the
music in the VR environment. Derived from the interaction of VRMS advantage
(M-layer) with fast-scale onset and coupling signals. When music enhancement
is strong and beat-level signals are active, motor_drive is high.

sensorimotor_sync captures the instantaneous quality of multi-modal
binding. Derived from bilateral index (M-layer) interacting with
connectivity strength (M-layer) and fast sensorimotor binding signals.
Represents current synchronization across the VR music stimulation's
three processing streams: auditory, visual (VR), and motor.

H3 demands: This layer introduces 0 new H3 tuples. All computation
derives from E-layer and M-layer features.

Li et al. 2025: high-groove music increases hip-ankle coordination 28.7%
and muscle synergy complexity (median synergies HG=7 vs LG=6, p=.039).

Liang et al. 2025: VRMS produces the strongest sensorimotor integration,
PM-DLPFC-M1 connectivity exceeding VRAO and VRMI conditions.

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/vrmsme/p_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples reused from E-layer (for fast-scale inputs) --------------------
_ONSET_VAL_100MS = (10, 3, 0, 2)              # music onset 100ms
_COUPLING_VAL_100MS = (25, 3, 0, 2)           # VR-motor coupling 100ms
_SENSORI_VAL_100MS = (33, 3, 0, 2)            # sensorimotor binding 100ms

# -- R3 indices ----------------------------------------------------------------
_SPECTRAL_FLUX = 10
_ONSET_STRENGTH = 11


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e: Tuple[Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """P-layer: 2D present-state from E/M-layer features + fast H3 signals.

    motor_drive represents the current motor cortex engagement driven
    by VR music stimulation. High when VRMS advantage is strong and
    beat-level signals are active.

    sensorimotor_sync represents current multi-modal synchronization
    quality across auditory, visual (VR), and motor streams.

    Li et al. 2025: high-groove music increases coordination 28.7%.
    Liang et al. 2025: VRMS strongest sensorimotor integration.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        e: ``(f16, f17, f18)`` from extraction layer.
        m: ``(vrms_advantage, bilateral_index, connectivity_strength)``
            from temporal integration layer.

    Returns:
        ``(motor_drive, sensorimotor_sync)`` each ``(B, T)``.
    """
    f16, f17, f18 = e
    vrms_advantage, bilateral_index, connectivity_strength = m

    # -- H3 features (reused from E-layer) --
    onset_val = h3_features[_ONSET_VAL_100MS]         # fast onset
    coupling_val = h3_features[_COUPLING_VAL_100MS]   # fast coupling
    sensori_val = h3_features[_SENSORI_VAL_100MS]     # fast sensorimotor

    # -- R3 features --
    spectral_flux = r3_features[..., _SPECTRAL_FLUX]     # (B, T)
    onset_str = r3_features[..., _ONSET_STRENGTH]         # (B, T)

    # -- motor_drive --
    # Instantaneous motor activation from VRMS advantage interacting with
    # fast onset and coupling signals. High when music enhancement is
    # strong AND beat-level cues are present.
    # Li 2025: high-groove increases coordination 28.7%.
    motor_drive = torch.sigmoid(
        0.35 * vrms_advantage * onset_val.clamp(min=0.1)
        + 0.35 * coupling_val * onset_str.clamp(min=0.1)
        + 0.30 * f16 * spectral_flux.clamp(min=0.1)
    )

    # -- sensorimotor_sync --
    # Instantaneous multi-modal binding quality. Bilateral index interacting
    # with connectivity strength and fast sensorimotor binding signals.
    # High when all three streams (auditory, visual, motor) are synchronized.
    # Liang 2025: PM-DLPFC-M1 connectivity exceeding VRAO and VRMI.
    sensorimotor_sync = torch.sigmoid(
        0.35 * bilateral_index * connectivity_strength.clamp(min=0.1)
        + 0.35 * sensori_val * f18.clamp(min=0.1)
        + 0.30 * f17 * coupling_val.clamp(min=0.1)
    )

    return motor_drive, sensorimotor_sync
