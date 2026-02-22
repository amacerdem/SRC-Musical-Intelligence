"""CMAPCC P-Layer -- Cognitive Present (2D).

Two present-processing dimensions for premotor cortex and mirror coupling:

  P0: pmc_activation   -- Right premotor cortex activation level [0, 1]
  P1: mirror_coupling  -- Mirror neuron system engagement [0, 1]

H3 consumed:
    (10, 6, 0, 2)  onset_strength value H6 L2             -- beat-level note onsets
    (8, 6, 0, 2)   loudness value H6 L2                   -- beat-level intensity
    (7, 6, 8, 0)   amplitude velocity H6 L0               -- action dynamics at beat
    (11, 6, 0, 2)  spectral_flux value H6 L2              -- spectral change at beat
    (0, 16, 0, 2)  roughness value H16 L2                 -- harmonic quality for encoding
    (4, 16, 0, 2)  sensory_pleasantness value H16 L2      -- valence for encoding

R3 consumed:
    [7]      amplitude      -- P0: action dynamics via velocity
    [8]      loudness       -- P0+P1: intensity for motor coupling
    [10]     onset_strength -- P0: event salience for action stream
    [11]     spectral_flux  -- P0: spectral change for event detection
    [33:41]  x_l4l5         -- P0: common code basis (derivatives x consonance)

See Building/C3-Brain/F4-Memory-Systems/mechanisms/cmapcc/CMAPCC-cognitive-present.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_ONSET_VAL_H6 = (10, 6, 0, 2)
_LOUD_VAL_H6 = (8, 6, 0, 2)
_AMP_VEL_H6 = (7, 6, 8, 0)
_FLUX_VAL_H6 = (11, 6, 0, 2)
_ROUGH_VAL_1S = (0, 16, 0, 2)
_PLEAS_VAL_1S = (4, 16, 0, 2)

# -- R3 indices ----------------------------------------------------------------
_X_L4L5_START = 33
_X_L4L5_END = 41


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor],
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor]:
    """P-layer: 2D present processing from H3/R3 + E/M + upstreams.

    P0 integrates encoding state (from MEAMN mnemonic circuit) and
    x_l4l5 interaction (action component) to provide a real-time readout
    of right premotor cortex activation.

    P1 tracks bidirectional perception-action mapping via the product
    of pmc_activation and familiarity, plus motor entrainment from SNEM.

    Bianco 2016: rIFG BA44 Z=4.29 (action-seed), fMRI N=29 pianists.
    Tanaka 2021: mu suppression d=0.72-0.86 during audiovisual opera
    (EEG, N=21).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        e_outputs: ``(E0, E1, E2)`` each ``(B, T)``.
        m_outputs: ``(M0, M1)`` each ``(B, T)``.
        upstream_outputs: ``{"MEAMN": (B, T, D), "SNEM": (B, T, D)}``.

    Returns:
        ``(P0, P1)`` each ``(B, T)``.
    """
    e0, _e1, _e2 = e_outputs
    m0, m1 = m_outputs

    # -- H3 features (contextual -- modulate encoding) --
    onset_val_h6 = h3_features[_ONSET_VAL_H6]
    loud_val_h6 = h3_features[_LOUD_VAL_H6]
    amp_vel_h6 = h3_features[_AMP_VEL_H6]
    flux_val_h6 = h3_features[_FLUX_VAL_H6]

    # -- R3 features --
    x_l4l5 = r3_features[..., _X_L4L5_START:_X_L4L5_END]  # (B, T, 8)

    # -- Upstream reads (graceful degradation) --
    # MEAMN: P0:memory_state [5] as encoding_state proxy
    meamn = upstream_outputs.get("MEAMN")
    if meamn is not None:
        encoding_state = meamn[..., 5]  # P0:memory_state -- (B, T)
        familiarity = meamn[..., 4]     # M1:p_recall -- (B, T)
    else:
        encoding_state = torch.zeros_like(e0)
        familiarity = torch.zeros_like(e0)

    # SNEM: P0:beat_locked_activity [6] as motor_entrainment
    snem = upstream_outputs.get("SNEM")
    if snem is not None:
        motor_entrainment = snem[..., 6]  # P0:beat_locked_activity -- (B, T)
    else:
        motor_entrainment = torch.zeros_like(e0)

    # P0: PMC activation -- right premotor cortex convergence zone
    # pmc_activation = sigma(0.50*encoding_state.mean + 0.50*x_l4l5.mean)
    # Encoding state (perception) + x_l4l5 (action dynamics).
    # Bianco 2016: dual-stream architecture, both dorsal (fronto-parietal)
    # and ventral (fronto-temporal) must contribute.
    # Ross & Balasubramaniam 2022: motor networks causally involved
    # in beat perception via covert entrainment.
    p0 = torch.sigmoid(
        0.50 * encoding_state
        + 0.50 * x_l4l5.mean(dim=-1)
    )

    # P1: Mirror coupling -- bidirectional perception-action mapping
    # mirror_coupling = sigma(0.50*pmc_activation*familiarity
    #                         + 0.50*motor_entrainment)
    # Multiplicative p0*familiarity ensures mirror coupling requires both
    # active PMC and stored representations.
    # Tanaka 2021: mu suppression d=0.72-0.86 during audiovisual
    # perception (EEG, N=21).
    p1 = torch.sigmoid(
        0.50 * p0 * familiarity
        + 0.50 * motor_entrainment
    )

    return p0, p1
