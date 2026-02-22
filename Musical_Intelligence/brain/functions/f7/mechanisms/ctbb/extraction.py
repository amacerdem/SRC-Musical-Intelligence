"""CTBB E-Layer -- Extraction (3D).

Cerebellar Theta-Burst Balance extraction features:
  E0: f25_cerebellar_timing  -- Cerebellar timing enhancement from iTBS [0, 1]
  E1: f26_m1_modulation      -- Motor cortex excitability modulation [0, 1]
  E2: f27_postural_control   -- Balance improvement from cerebellar-M1 [0, 1]

Cerebellar timing (E0) captures how strongly the cerebellar timing circuit
is engaged, estimated from coupling stability at 1s. Sansare 2025: cerebellar
iTBS reduces postural sway (eta-sq=0.202, F=9.600, p=.004). Okada 2022:
cerebellar dentate contains 3 functional neuron types for rhythm prediction,
timing control, and error detection.

M1 modulation (E1) estimates motor cortex excitability change driven by
cerebellar output, combining coupling periodicity at 1s with fast cerebellar
signal at 100ms. Sansare 2025 CBI null (eta-sq=0.045 n.s.) suggests
alternative circuits may mediate the effect.

Postural control (E2) integrates f25 x f26 interaction with inverted balance
variability and mean motor amplitude. Sansare 2025: sway reduction sustained
>= 30 min post-iTBS; Bonferroni POST1-6 all p < .05.

H3 demands consumed (5):
  (25, 16, 19, 0) coupling stability 1s L0
  (25, 16, 14, 2) coupling periodicity 1s L2
  (25, 3,  0,  2) cerebellar coupling 100ms L2
  (33, 16, 2,  0) balance variability 1s L0
  (7,  16, 1,  2) mean motor output 1s L2

R3 inputs: amplitude[7], spectral_flux[10], x_l0l5[25:33], x_l4l5[33:41]

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/ctbb/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed ---------------------------------------------------
_COUPLING_STAB_H16 = (25, 16, 19, 0)   # coupling stability 1s L0
_COUPLING_PERIOD_H16 = (25, 16, 14, 2) # coupling periodicity 1s L2
_CEREBELLAR_100MS = (25, 3, 0, 2)      # cerebellar coupling 100ms L2
_BALANCE_VAR_H16 = (33, 16, 2, 0)      # balance variability 1s L0
_MEAN_MOTOR_H16 = (7, 16, 1, 2)        # mean motor output 1s L2

# -- R3 feature indices (post-freeze 97D) -------------------------------------
_AMPLITUDE = 7
_SPECTRAL_FLUX = 10
_X_L0L5_START = 25
_X_L0L5_END = 33
_X_L4L5_START = 33
_X_L4L5_END = 41


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute E-layer: 3D cerebellar extraction features.

    E0 (f25_cerebellar_timing): Cerebellar timing enhancement from coupling
    stability at 1s. Core iTBS effect on cerebellar timing function.
    Sansare 2025: causal TMS evidence. Okada 2022: 3 neuron types in dentate.

    E1 (f26_m1_modulation): Motor cortex excitability modulation from coupling
    periodicity at 1s and fast cerebellar signal at 100ms.
    Sansare 2025: CBI null (eta-sq=0.045 n.s.). Shi 2025: bilateral M1 iTBS.

    E2 (f27_postural_control): Balance improvement integrating f25 x f26
    interaction + inverted balance variability + mean motor amplitude.
    Sansare 2025: sway reduction POST1-6 Bonferroni all p < .05.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 spectral features.
        upstream_outputs: ``{"PEOM": (B, T, 11), "GSSM": ..., "SPMC": ...}``.

    Returns:
        ``(E0, E1, E2)`` each ``(B, T)``.
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device

    # -- H3 features --
    coupling_stab = h3_features.get(
        _COUPLING_STAB_H16, torch.zeros(B, T, device=device),
    )
    coupling_period = h3_features.get(
        _COUPLING_PERIOD_H16, torch.zeros(B, T, device=device),
    )
    cerebellar_fast = h3_features.get(
        _CEREBELLAR_100MS, torch.zeros(B, T, device=device),
    )
    balance_var = h3_features.get(
        _BALANCE_VAR_H16, torch.zeros(B, T, device=device),
    )
    mean_motor = h3_features.get(
        _MEAN_MOTOR_H16, torch.zeros(B, T, device=device),
    )

    # -- R3 features --
    amplitude = r3_features[..., _AMPLITUDE]                    # (B, T)

    # -- E0: Cerebellar Timing (f25) --
    # f25 = sigma(0.40 * coupling_stability_1s)
    # Doc: single coefficient, sum = 0.40 (not 1.0) -- maps to low pre-sigmoid
    # Sansare 2025: cerebellar iTBS causally modulates timing precision
    # Okada 2022: dentate neuron types for rhythm prediction
    e0 = torch.sigmoid(0.40 * coupling_stab)

    # -- E1: M1 Modulation (f26) --
    # f26 = sigma(0.30 * coupling_period_1s + 0.30 * cerebellar_100ms)
    # Sansare 2025: CBI null suggests alternative circuit mediation
    # Shi 2025: bilateral M1 iTBS enhances gait automaticity
    e1 = torch.sigmoid(
        0.30 * coupling_period
        + 0.30 * cerebellar_fast
    )

    # -- E2: Postural Control (f27) --
    # f27 = sigma(0.35 * f25 * f26 + 0.35 * (1 - balance_var_1s)
    #             + 0.30 * mean_amplitude_1s)
    # Sansare 2025: sway reduction from timing x modulation synergy
    e2 = torch.sigmoid(
        0.35 * e0 * e1
        + 0.35 * (1.0 - balance_var)
        + 0.30 * mean_motor
    )

    return e0, e1, e2
