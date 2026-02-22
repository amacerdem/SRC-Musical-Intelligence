"""VRMSME M-Layer -- Temporal Integration (3D).

VR Music Stimulation Motor Enhancement temporal integration signals:
  vrms_advantage        -- VRMS superiority over VRAO/VRMI [0, 1]
  bilateral_index       -- Bilateral activation balance [0, 1]
  connectivity_strength -- Network connectivity magnitude [0, 1]

vrms_advantage directly inherits from f16 (music_enhancement). The music
enhancement feature IS the VRMS advantage -- it directly quantifies how
much music adds to VR motor stimulation beyond observation or imagery.

bilateral_index directly inherits from f17 (bilateral_activation). The
bilateral activation feature IS the bilateral index -- it captures the
homotopic brain connectivity pattern distinguishing VRMS from VRMI.

connectivity_strength combines f16 and f18 through sigmoid with equal
weights. Both music-specific enhancement and the PM-DLPFC-M1 network
must be active for high connectivity.

H3 demands: This layer introduces 0 new H3 tuples. All computation
derives from E-layer features f16, f17, f18.

Liang et al. 2025: VRMS > VRAO bilateral PM&SMA (p<.01 FDR);
VRMS > VRMI bilateral M1 (p<.05 HBT); 14 ROI pairs with significant
heterogeneous FC in VRMS (p<.05 FDR).

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/vrmsme/m_layer.md
"""
from __future__ import annotations

from typing import Tuple

import torch
from torch import Tensor


def compute_temporal_integration(
    e: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """M-layer: 3D temporal integration from E-layer features.

    Transforms E-layer features into clinically interpretable measures
    of VR music stimulation effects.

    vrms_advantage = f16 (direct pass-through)
    bilateral_index = f17 (direct pass-through)
    connectivity_strength = sigma(0.5 * f16 + 0.5 * f18)

    Liang et al. 2025: VRMS superiority over VRAO/VRMI in bilateral
    PM&SMA connectivity and M1 activation.

    Args:
        e: ``(f16, f17, f18)`` from extraction layer, each ``(B, T)``.

    Returns:
        ``(vrms_advantage, bilateral_index, connectivity_strength)``
        each ``(B, T)``.
    """
    f16, f17, f18 = e

    # -- vrms_advantage: direct from f16 (music_enhancement) --
    # The music enhancement feature IS the VRMS advantage.
    # Liang 2025: VRMS > VRAO in bilateral PM&SMA (p<.01 FDR);
    # VRMS > VRMI in bilateral M1 (p<.05 HBT).
    vrms_advantage = f16

    # -- bilateral_index: direct from f17 (bilateral_activation) --
    # Homotopic brain connectivity (HBT) in M1 significantly greater
    # for VRMS vs VRMI.
    bilateral_index = f17

    # -- connectivity_strength: sigmoid(0.5*f16 + 0.5*f18) --
    # Integrates music enhancement (f16) with network connectivity (f18)
    # for overall connectivity measure. Both must be active.
    # Liang 2025: 14 ROI pairs with significant heterogeneous FC (p<.05 FDR).
    connectivity_strength = torch.sigmoid(
        0.50 * f16 + 0.50 * f18
    )

    return vrms_advantage, bilateral_index, connectivity_strength
