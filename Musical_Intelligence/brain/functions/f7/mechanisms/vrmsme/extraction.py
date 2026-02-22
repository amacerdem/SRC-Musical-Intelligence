"""VRMSME E-Layer -- Extraction (3D).

VR Music Stimulation Motor Enhancement extraction signals:
  f16: music_enhancement       -- VRMS motor enhancement superiority [0, 1]
  f17: bilateral_activation    -- Bilateral sensorimotor activation [0, 1]
  f18: network_connectivity    -- PM-DLPFC-M1 interaction network [0, 1]

f16 captures the unique motor-enhancing effect of VR music stimulation
compared to VR action observation (VRAO) and VR motor imagery (VRMI).
Combines multi-modal coupling periodicity at 1s, music periodicity at 1s,
and music onset at 100ms.

f17 captures bilateral sensorimotor activation (S1/PM/SMA/M1) via
sensorimotor binding periodicity at three timescales: 1s (sustained), 500ms
(mid-range), and 100ms (fast action-perception binding).

f18 captures PM-DLPFC-M1 heterogeneous connectivity. The interaction term
(f16 * f17) is critical: both music enhancement AND bilateral activation
must be present for strong network connectivity. Loudness entropy and
binding variability modulate the signal.

H3 consumed (12 tuples, all L2):
    (10, 3, 0, 2)   onset value H3 L2               -- music onset at 100ms
    (10, 16, 14, 2)  onset periodicity H16 L2        -- music periodicity 1s
    (11, 3, 0, 2)   onset_strength value H3 L2       -- beat strength 100ms
    (11, 16, 14, 2)  onset_strength periodicity H16 L2 -- beat regularity 1s
    (25, 3, 0, 2)   coupling value H3 L2             -- VR-motor coupling 100ms
    (25, 3, 14, 2)  coupling periodicity H3 L2       -- coupling periodicity 100ms
    (25, 16, 14, 2) coupling periodicity H16 L2      -- coupling periodicity 1s
    (33, 3, 0, 2)   sensorimotor value H3 L2         -- sensorimotor binding 100ms
    (33, 3, 2, 2)   sensorimotor std H3 L2           -- binding variability 100ms
    (33, 8, 14, 2)  sensorimotor periodicity H8 L2   -- sensorimotor period 500ms
    (33, 16, 14, 2) sensorimotor periodicity H16 L2  -- sensorimotor period 1s
    (8, 3, 20, 2)   loudness entropy H3 L2           -- loudness entropy 100ms

R3 consumed:
    [8]      loudness               -- perceptual intensity
    [10]     spectral_flux          -- music onset detection
    [11]     onset_strength         -- beat marker strength
    [25:33]  x_l0l5                 -- VR-audio-motor coupling pathway
    [33:41]  x_l4l5                 -- sensorimotor binding

Liang et al. 2025: VRMS > VRAO in bilateral PM&SMA connectivity (p<.01 FDR);
VRMS > VRMI in bilateral M1 activation (p<.05 HBT).

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/vrmsme/e_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (12 tuples, all L2 integration) --------------------------------
_ONSET_VAL_100MS = (10, 3, 0, 2)              # #0: music onset at 100ms
_ONSET_PERIOD_1S = (10, 16, 14, 2)            # #1: music periodicity 1s
_BEAT_VAL_100MS = (11, 3, 0, 2)               # #2: beat strength 100ms
_BEAT_PERIOD_1S = (11, 16, 14, 2)             # #3: onset periodicity 1s
_COUPLING_VAL_100MS = (25, 3, 0, 2)           # #4: VR-motor coupling 100ms
_COUPLING_PERIOD_100MS = (25, 3, 14, 2)       # #5: coupling periodicity 100ms
_COUPLING_PERIOD_1S = (25, 16, 14, 2)         # #6: coupling periodicity 1s
_SENSORI_VAL_100MS = (33, 3, 0, 2)            # #7: sensorimotor binding 100ms
_SENSORI_STD_100MS = (33, 3, 2, 2)            # #8: binding variability 100ms
_SENSORI_PERIOD_500MS = (33, 8, 14, 2)        # #9: sensorimotor period 500ms
_SENSORI_PERIOD_1S = (33, 16, 14, 2)          # #10: sensorimotor period 1s
_LOUDNESS_ENTROPY_100MS = (8, 3, 20, 2)       # #11: loudness entropy 100ms

# -- R3 indices ----------------------------------------------------------------
_LOUDNESS = 8
_SPECTRAL_FLUX = 10
_ONSET_STRENGTH = 11
_X_L0L5_START = 25
_X_L0L5_END = 33
_X_L4L5_START = 33
_X_L4L5_END = 41


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """E-layer: 3D extraction from H3/R3 features.

    Implements Liang et al. (2025) VR music stimulation motor enhancement:
        f16: music enhancement from coupling + music periodicity
        f17: bilateral activation from sensorimotor binding multi-scale
        f18: network connectivity as f16*f17 interaction + loudness entropy

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        relay_outputs: ``{"PEOM": (B, T, D), "MSR": (B, T, D)}``

    Returns:
        ``(f16, f17, f18)`` each ``(B, T)``.
    """
    # -- H3 features --
    coupling_period_1s = h3_features[_COUPLING_PERIOD_1S]        # coupling period 1s
    onset_period_1s = h3_features[_ONSET_PERIOD_1S]              # music period 1s
    onset_val_100ms = h3_features[_ONSET_VAL_100MS]              # music onset 100ms
    sensori_period_1s = h3_features[_SENSORI_PERIOD_1S]          # sensorimotor 1s
    sensori_period_500ms = h3_features[_SENSORI_PERIOD_500MS]    # sensorimotor 500ms
    sensori_val_100ms = h3_features[_SENSORI_VAL_100MS]          # sensorimotor 100ms
    sensori_std_100ms = h3_features[_SENSORI_STD_100MS]          # binding variability
    loudness_entropy = h3_features[_LOUDNESS_ENTROPY_100MS]      # loudness entropy

    # -- R3 features --
    loudness = r3_features[..., _LOUDNESS]                       # (B, T)
    spectral_flux = r3_features[..., _SPECTRAL_FLUX]             # (B, T)

    # -- f16: Music Enhancement --
    # VRMS motor enhancement superiority over VRAO/VRMI.
    # Combines multi-modal coupling periodicity at 1s (sustained VR-music-motor
    # coupling), music periodicity at 1s (sustained auditory regularity), and
    # music onset at 100ms (immediate onset detection).
    # Liang 2025: VRMS > VRAO in bilateral PM&SMA (p<.01 FDR).
    # f16 = sigma(0.40 * coupling_period_1s + 0.30 * music_period_1s
    #              + 0.30 * music_onset_100ms)
    f16 = torch.sigmoid(
        0.40 * coupling_period_1s
        + 0.30 * onset_period_1s
        + 0.30 * onset_val_100ms * spectral_flux.clamp(min=0.1)
    )

    # -- f17: Bilateral Activation --
    # Bilateral sensorimotor activation (S1/PM/SMA/M1).
    # Combines sensorimotor binding periodicity at three timescales: 1s
    # (sustained bilateral activation), 500ms (mid-range), and 100ms (fast).
    # Liang 2025: VRMS > VRMI in bilateral M1 activation (p<.05 HBT).
    # f17 = sigma(0.40 * sensorimotor_period_1s + 0.30 * sensorimotor_period_500ms
    #              + 0.30 * sensorimotor_100ms)
    f17 = torch.sigmoid(
        0.40 * sensori_period_1s
        + 0.30 * sensori_period_500ms
        + 0.30 * sensori_val_100ms
    )

    # -- f18: Network Connectivity --
    # PM-DLPFC-M1 interaction network strength. The interaction term
    # (f16 * f17) requires both music enhancement AND bilateral activation
    # for strong network connectivity. Loudness entropy adds auditory
    # complexity and binding variability adds sensorimotor stability.
    # Liang 2025: VRMS shows strongest PM-DLPFC-M1 heterogeneous FC
    # (14 ROI pairs p<.05 FDR).
    # f18 = sigma(0.35 * f16 * f17 + 0.35 * loudness_entropy_100ms
    #              + 0.30 * binding_variability_100ms)
    f18 = torch.sigmoid(
        0.35 * f16 * f17
        + 0.35 * loudness_entropy * loudness.clamp(min=0.1)
        + 0.30 * sensori_std_100ms
    )

    return f16, f17, f18
