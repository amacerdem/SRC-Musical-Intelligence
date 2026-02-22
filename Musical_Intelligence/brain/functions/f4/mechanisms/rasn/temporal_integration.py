"""RASN M-Layer -- Temporal Integration (2D).

Rhythmic Auditory Stimulation Neuroplasticity integration signals:
  M0: neuroplasticity_composite  — Composite plasticity metric [0, 1]
  M1: motor_recovery             — Motor recovery potential [0, 1]

M0 integrates entrainment quality, encoding success, and optimal complexity
to produce a composite plasticity score. The key insight is that plasticity
requires both stable entrainment (beat x encoding) AND moderate complexity
challenge (inverted-U entropy). Too simple = no learning; too complex = no
stable entrainment. Binding quality (stumpf fusion) confirms that the
entrainment creates stable neural binding suitable for long-term plasticity.

M1 quantifies the potential for motor function improvement based on
entrainment strength, motor engagement level, and beat energy. This captures
the clinical evidence that RAS produces measurable gait improvements
(velocity, stride length, cadence) through beat-movement coupling.

H3 demands consumed (7 tuples):
  (23, 11, 0, 2)  entropy value H11 L2          -- current complexity 500ms
  (23, 16, 1, 0)  entropy mean H16 L0           -- average complexity 1s
  (23, 20, 1, 0)  entropy mean H20 L0           -- complexity over 5s
  (23, 24, 19, 0) entropy stability H24 L0      -- pattern stability 36s
  (3, 16, 1, 2)   stumpf_fusion mean H16 L2     -- binding stability 1s
  (3, 20, 1, 0)   stumpf_fusion mean H20 L0     -- binding over 5s
  (3, 24, 1, 0)   stumpf_fusion mean H24 L0     -- long-term binding

R3 features:
  [3] stumpf_fusion, [23] entropy, [7] amplitude

Zhao 2025: repeated entrainment promotes neuroplasticity (4 meta-analyses,
n=968+).
Wang 2022: RAS improves walking function across stroke populations (22
studies, positive gait velocity/stride).

See Building/C3-Brain/F4-Memory-Systems/mechanisms/rasn/RASN-temporal-integration.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_ENTROPY_VAL_H11 = (23, 11, 0, 2)       # entropy value H11 L2
_ENTROPY_MEAN_H16 = (23, 16, 1, 0)      # entropy mean H16 L0
_ENTROPY_MEAN_H20 = (23, 20, 1, 0)      # entropy mean H20 L0
_ENTROPY_STAB_H24 = (23, 24, 19, 0)     # entropy stability H24 L0
_STUMPF_MEAN_H16 = (3, 16, 1, 2)        # stumpf_fusion mean H16 L2
_STUMPF_MEAN_H20 = (3, 20, 1, 0)        # stumpf_fusion mean H20 L0
_STUMPF_MEAN_H24 = (3, 24, 1, 0)        # stumpf_fusion mean H24 L0

# -- R3 feature indices -------------------------------------------------------
_AMPLITUDE = 7
_STUMPF_FUSION = 3
_ENTROPY = 23


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute M-layer: integrated plasticity and motor recovery signals.

    M0 (neuroplasticity_composite) integrates entrainment quality with
    complexity-optimal plasticity demand and binding stability. The inverted-U
    entropy function ensures moderate complexity drives maximal plasticity.
    Long-horizon stumpf fusion confirms durable neural binding.

    M1 (motor_recovery) quantifies motor recovery potential. Entrainment
    strength (E0) x motor engagement (E1) form the core signal. Beat energy
    (amplitude) and binding stability provide additional motor pathway context.

    Zhao 2025: Systematic review, 968+ patients -- repeated entrainment
    promotes neuroplasticity (4 meta-analyses).
    Wang 2022: Meta-analysis, 22 studies -- RAS improves walking function
    (gait velocity, stride) across neurological conditions.
    Ghai & Ghai 2019: Systematic review, 968 patients -- RAS improves gait
    parameters in neurological conditions.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        e: ``(E0, E1, E2)`` from extraction layer.

    Returns:
        ``(M0, M1)`` each ``(B, T)``
    """
    e0, e1, e2 = e

    # -- H3 features --
    entropy_val = h3_features[_ENTROPY_VAL_H11]       # (B, T)
    entropy_mean_1s = h3_features[_ENTROPY_MEAN_H16]  # (B, T)
    entropy_mean_5s = h3_features[_ENTROPY_MEAN_H20]  # (B, T)
    entropy_stab = h3_features[_ENTROPY_STAB_H24]     # (B, T)
    stumpf_mean_1s = h3_features[_STUMPF_MEAN_H16]    # (B, T)
    stumpf_mean_5s = h3_features[_STUMPF_MEAN_H20]    # (B, T)
    stumpf_mean_36s = h3_features[_STUMPF_MEAN_H24]   # (B, T)

    # -- R3 features --
    amplitude = r3_features[..., _AMPLITUDE]    # (B, T)
    stumpf = r3_features[..., _STUMPF_FUSION]   # (B, T)

    # -- Derived signals --
    # Inverted-U complexity: moderate complexity = optimal plasticity demand
    complexity_optimal = 1.0 - (entropy_mean_1s - 0.5).abs() * 2.0  # [0, 1]

    # Multi-scale binding: average across temporal windows
    binding_stability = (
        0.40 * stumpf_mean_1s
        + 0.35 * stumpf_mean_5s
        + 0.25 * stumpf_mean_36s
    )

    # Motor-entrainment coupling from E-layer
    motor_entrainment = 0.50 * e0 + 0.50 * e1

    # -- M0: Neuroplasticity Composite --
    # Integrates entrainment quality, complexity challenge, and binding.
    # Plasticity = stable entrainment + moderate complexity + durable binding.
    # Zhao 2025: entrainment promotes neuroplasticity (n=968+).
    # Blasi et al. 2025: structural changes after >= 4 weeks (20 RCTs, N=718).
    m0 = torch.sigmoid(
        0.35 * e0 * binding_stability.clamp(min=0.1)
        + 0.35 * complexity_optimal * entropy_stab
        + 0.30 * motor_entrainment * stumpf
    )

    # -- M1: Motor Recovery --
    # Motor recovery potential from entrainment-motor coupling.
    # E0 (entrainment) x E1 (motor facilitation) form the core signal.
    # Beat energy and binding stability provide motor pathway context.
    # Wang 2022: RAS improves gait velocity and stride (22 studies).
    m1 = torch.sigmoid(
        0.40 * e0 * e1
        + 0.35 * e2 * amplitude
        + 0.25 * binding_stability * entropy_val.clamp(min=0.1)
    )

    return m0, m1
