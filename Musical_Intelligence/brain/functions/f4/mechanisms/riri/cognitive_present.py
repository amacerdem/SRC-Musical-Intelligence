"""RIRI P-Layer -- Cognitive Present (2D).

Present-time multi-modal rehabilitation state with intra-unit relay reads:
  P0: entrainment_state  (current multi-modal entrainment quality)
  P1: motor_adaptation   (current motor adaptation state)

P0 is the primary relay export: "are all rehabilitation channels locked to
the rhythm right now?"  P1 tracks real-time sensorimotor adaptation -- how
the motor system is responding to and adjusting with the rhythmic input.

Upstream reads (intra-unit, via relay_outputs):
  RASN  -- rhythmic auditory stimulation state
  MEAMN -- memory-emotional encoding state
  MMP   -- motor-memory prediction state
  HCMC  -- hippocampal-cortical memory consolidation

H3 consumed (P-layer):
  (25, 6, 0, 2)   x_l0l5[0] value H6 L2      -- entrainment coupling at beat
  (7, 11, 0, 2)   amplitude value H11 L2      -- current motor drive
  (7, 11, 8, 0)   amplitude velocity H11 L0   -- intensity change rate
  (33, 11, 0, 2)  x_l4l5[0] value H11 L2     -- sensorimotor coupling

See Building/C3-Brain/F4-Memory-Systems/mechanisms/riri/RIRI-cognitive-present.md
Thaut 2015: auditory rhythm primes motor system via reticulospinal pathways.
Harrison 2025: SMA + putamen during musically-cued movement.
Yamashita 2025: gait-synchronized M1+SMA tACS reduces step variability.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed (P-layer) ------------------------------------------------
_COUPLING_L0L5_H6_VAL = (25, 6, 0, 2)    # x_l0l5 value H6 L2
_AMP_H11_VAL = (7, 11, 0, 2)             # amplitude value H11 L2
_AMP_H11_VEL = (7, 11, 8, 0)             # amplitude velocity H11 L0
_COUPLING_L4L5_H11_VAL = (33, 11, 0, 2)  # x_l4l5 value H11 L2

# -- Upstream relay fallback dimension (safe default) --------------------------
_FALLBACK_DIM = 0.5


def _safe_relay_mean(
    relay_outputs: Dict[str, Tensor],
    name: str,
) -> Tensor:
    """Extract a relay mean or return scalar fallback.

    Graceful degradation: if the relay is missing from ``relay_outputs``
    we return 0.5 (neutral midpoint).  This allows RIRI to run even when
    upstream mechanisms are not yet computed.
    """
    if name in relay_outputs:
        return relay_outputs[name].mean(dim=-1)          # (B, T)
    # Return a broadcastable scalar fallback
    return torch.tensor(_FALLBACK_DIM)


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor],
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute P-layer: present-time rehabilitation state.

    P0 (entrainment_state) combines beat-level auditory-motor coupling
    (x_l0l5) with H3 onset features and upstream relay context.
    Thaut 2015: auditory rhythm primes motor system.

    P1 (motor_adaptation) tracks real-time sensorimotor adaptation using
    sensorimotor coupling (x_l4l5) and amplitude velocity.
    Yamashita 2025: gait-synchronized stimulation reduces step variability.

    Both dimensions are gated by upstream relay context via a geometric
    mean of the four intra-unit relay means.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2)`` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.
        relay_outputs: ``{"RASN": ..., "MEAMN": ..., "MMP": ..., "HCMC": ...}``

    Returns:
        ``(P0, P1)`` each ``(B, T)``
    """
    e0, e1, _e2 = e
    m0, m1 = m

    # -- H3 features -------------------------------------------------------
    coupling_l0l5_val = h3_features[_COUPLING_L0L5_H6_VAL]    # (B, T)
    amp_val = h3_features[_AMP_H11_VAL]                         # (B, T)
    amp_vel = h3_features[_AMP_H11_VEL]                         # (B, T)
    coupling_l4l5_val = h3_features[_COUPLING_L4L5_H11_VAL]    # (B, T)

    # -- Upstream relay context (graceful fallback) -------------------------
    rasn_ctx = _safe_relay_mean(relay_outputs, "RASN")
    meamn_ctx = _safe_relay_mean(relay_outputs, "MEAMN")
    mmp_ctx = _safe_relay_mean(relay_outputs, "MMP")
    hcmc_ctx = _safe_relay_mean(relay_outputs, "HCMC")

    # Geometric mean gate of 4 upstream relays -- all must contribute
    relay_gate = torch.pow(
        (rasn_ctx * meamn_ctx * mmp_ctx * hcmc_ctx).clamp(min=1e-8),
        0.25,
    )

    # -- P0: Entrainment State ---------------------------------------------
    # Current multi-modal entrainment quality.  Reflects "are all channels
    # locked to the rhythm right now?"
    # sigma(0.50 * x_l0l5_val + 0.50 * flux_val * onset_val)
    # Gated by relay context to ensure upstream contributions.
    p0 = torch.sigmoid(
        0.50 * coupling_l0l5_val
        + 0.50 * e0 * relay_gate
    )

    # -- P1: Motor Adaptation ----------------------------------------------
    # Current motor adaptation state.  Tracks how effectively the
    # sensorimotor system adjusts to rhythmic input.
    # sigma(0.50 * x_l4l5_val + 0.50 * amplitude_velocity)
    p1 = torch.sigmoid(
        0.50 * coupling_l4l5_val
        + 0.50 * amp_vel * relay_gate
    )

    return p0, p1
