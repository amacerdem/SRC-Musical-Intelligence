"""ECT P-Layer -- Cognitive Present (2D).

Two present-moment features for expertise compartmentalization state:

  within_binding     -- Current within-network efficiency [0, 1]
  network_isolation  -- Current cross-network reduction [0, 1]

within_binding represents the instantaneous state of intra-network coupling,
reflecting how efficiently specialized modules are operating right now.
Derived from within-coupling at 100ms, coupling variability at 100ms, and
pattern binding at 100ms.
Papadaki et al. 2023: greater network strength and global efficiency in
professionals correlate with task performance.

network_isolation represents the instantaneous degree of between-network
isolation, reflecting how disconnected specialized modules are from each
other right now. Derived from cross-network binding at 100ms, cross-network
variability at 100ms, and inverted flexibility index (E-layer f04).
Moller et al. 2021: musicians show localized CT correlations only (not
distributed); structural evidence for network isolation.

The P-layer provides the real-time balance that the F-layer uses to predict
future transfer limitations and recovery capacity.

H3 demands consumed (4):
  (33, 3, 0, 2)   x_l4l5 value H3 L2          -- pattern binding 100ms
  (23, 3, 0, 2)   pitch_change value H3 L2     -- pitch specialization 100ms
  (23, 16, 1, 2)  pitch_change mean H16 L2     -- mean pitch specialization 1s
  (8, 3, 0, 2)    loudness value H3 L2         -- attention allocation 100ms

See Building/C3-Brain/F8-Learning-and-Plasticity/mechanisms/ect/p_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed (4 tuples, P-layer) -------------------------------
_BINDING_VAL_100MS = (33, 3, 0, 2)        # pattern binding at 100ms
_PITCH_VAL_100MS = (23, 3, 0, 2)          # pitch specialization at 100ms
_PITCH_MEAN_1S = (23, 16, 1, 2)           # mean pitch specialization 1s
_LOUD_VAL_100MS = (8, 3, 0, 2)            # attention allocation at 100ms

# -- E-layer H3 tuple keys reused for P-layer computation ---------------------
_WITHIN_VAL_100MS = (25, 3, 0, 2)         # within coupling 100ms (E-layer)
_WITHIN_STD_100MS = (25, 3, 2, 2)         # coupling variability 100ms (E-layer)
_CROSS_VAL_100MS = (41, 3, 0, 2)          # cross-network binding 100ms (E-layer)
_CROSS_STD_100MS = (41, 3, 2, 2)          # cross-network variability 100ms (E-layer)


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor],
    ednr: Tensor,
    cdmr: Tensor,
    slee: Tensor,
) -> Tuple[Tensor, Tensor]:
    """Compute P-layer: 2D present-moment compartmentalization features.

    within_binding: Current within-network efficiency from instantaneous
    coupling, variability, and binding at 100ms. Low variability with high
    coupling indicates efficient specialized processing.
    sigma(0.25 * within_val_100ms + 0.20 * (1 - within_std_100ms)
          + 0.25 * binding_val_100ms + 0.15 * pitch_val_100ms
          + 0.15 * pitch_mean_1s).
    Papadaki 2023: network strength correlates with task performance.

    network_isolation: Current between-network disconnection from
    cross-network binding, variability, and inverted flexibility.
    sigma(0.25 * cross_val_100ms + 0.20 * cross_std_100ms
          + 0.25 * (1 - f04) + 0.15 * loud_val_100ms
          + 0.15 * ednr_isolation).
    Moller 2021: localized CT correlations only in musicians.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        e_outputs: ``(f01, f02, f03, f04)`` each ``(B, T)``.
        m_outputs: ``(training_history, network_state, task_memory)``
            each ``(B, T)``.
        ednr: ``(B, T, 10)`` upstream EDNR output.
        cdmr: ``(B, T, 11)`` upstream CDMR output.
        slee: ``(B, T, 13)`` upstream SLEE output.

    Returns:
        ``(within_binding, network_isolation)`` each ``(B, T)``.
    """
    _f01, _f02, _f03, f04 = e_outputs

    # -- H3 features -----------------------------------------------------------
    within_val_100ms = h3_features[_WITHIN_VAL_100MS]     # (B, T)
    within_std_100ms = h3_features[_WITHIN_STD_100MS]     # (B, T)
    binding_val_100ms = h3_features[_BINDING_VAL_100MS]   # (B, T)
    cross_val_100ms = h3_features[_CROSS_VAL_100MS]       # (B, T)
    cross_std_100ms = h3_features[_CROSS_STD_100MS]       # (B, T)
    pitch_val_100ms = h3_features[_PITCH_VAL_100MS]       # (B, T)
    pitch_mean_1s = h3_features[_PITCH_MEAN_1S]           # (B, T)
    loud_val_100ms = h3_features[_LOUD_VAL_100MS]         # (B, T)

    # -- Upstream context signals ----------------------------------------------
    # EDNR network_isolation is P-layer dim 7 (index 7 in EDNR 10D output)
    ednr_isolation = ednr[..., 7]              # (B, T)

    # -- within_binding: Current within-network efficiency ---------------------
    # sigma(0.25 * within_val_100ms + 0.20 * (1 - within_std_100ms)
    #       + 0.25 * binding_val_100ms + 0.15 * pitch_val_100ms
    #       + 0.15 * pitch_mean_1s)
    # Papadaki 2023: greater network strength and global efficiency correlate
    # with task performance in aspiring professionals.
    within_binding = torch.sigmoid(
        0.25 * within_val_100ms
        + 0.20 * (1.0 - within_std_100ms)
        + 0.25 * binding_val_100ms
        + 0.15 * pitch_val_100ms
        + 0.15 * pitch_mean_1s
    )

    # -- network_isolation: Current cross-network reduction --------------------
    # sigma(0.25 * cross_val_100ms + 0.20 * cross_std_100ms
    #       + 0.25 * (1 - f04) + 0.15 * loud_val_100ms
    #       + 0.15 * ednr_isolation)
    # Moller 2021: musicians show localized CT correlations only (not
    # distributed); structural evidence for network isolation.
    network_isolation = torch.sigmoid(
        0.25 * cross_val_100ms
        + 0.20 * cross_std_100ms
        + 0.25 * (1.0 - f04)
        + 0.15 * loud_val_100ms
        + 0.15 * ednr_isolation
    )

    return within_binding, network_isolation
