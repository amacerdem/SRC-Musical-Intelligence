"""HCMC P-Layer -- Cognitive Present (3D).

Present-time hippocampal-cortical memory state with MEAMN relay context:

  P0: binding_state       -- Current hippocampal binding activation [0, 1]
  P1: segmentation_state  -- Current episodic segmentation state [0, 1]
  P2: storage_state       -- Current cortical storage activation [0, 1]

H3 consumed:
    (7, 20, 5, 0)   amplitude range H20 L0             -- energy dynamic range
    (10, 24, 2, 0)  loudness std H24 L0                -- salience variability 36s
    (5, 24, 22, 0)  harmonicity autocorrelation H24 L0 -- harmonic repetition

Upstream reads:
    MEAMN.memory_state -- autobiographical memory context from relay_outputs

See Building/C3-Brain/F4-Memory-Systems/mechanisms/hcmc/HCMC-cognitive-present.md
Fernandez-Rubio et al. 2022: Hippocampus activated at memorized tonal sequences.
Zacks et al. 2007: Event segmentation theory -- boundaries trigger encoding.
Sikka et al. 2015: Age-related hippocampal-to-cortical shift for musical memory.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_AMP_RANGE_5S = (7, 20, 5, 0)           # amplitude range H20 L0
_LOUD_STD_36S = (10, 24, 2, 0)          # loudness std H24 L0
_HARM_AUTOCORR_36S = (5, 24, 22, 0)     # harmonicity autocorrelation H24 L0

# -- MEAMN relay index ---------------------------------------------------------
_MEAMN_MEMORY_STATE = 0   # MEAMN memory_state field


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor, Tensor],
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """P-layer: present-time hippocampal-cortical memory state.

    P0 (binding_state): Summary present-moment signal for hippocampal
    encoding. Aggregates E0 (fast binding) with M0 (consolidation strength)
    and MEAMN memory context. High binding state = novel or salient moments.
    Fernandez-Rubio et al. 2022: left hippocampus activated at 4th tone.

    P1 (segmentation_state): Whether the current frame is at or near an
    episodic boundary. Combines E1 (segmentation) with M1 (encoding rate)
    and amplitude dynamic range for boundary salience.
    Zacks et al. 2007: event boundaries close one segment, open another.

    P2 (storage_state): Degree to which cortical networks are receiving
    consolidated traces from hippocampus. Uses E2 (cortical storage),
    M2 (synthesis), harmonic repetition, and salience variability.
    Sikka et al. 2015: hippocampal-to-cortical shift for semantic memory.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e: ``(E0, E1, E2)`` from extraction layer.
        m: ``(M0, M1, M2)`` from temporal integration layer.
        relay_outputs: ``{"MEAMN": (B, T, 12)}``.

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``.
    """
    e0, e1, e2 = e
    m0, m1, m2 = m

    # -- Upstream relay features --
    B, T = e0.shape
    device = e0.device
    meamn = relay_outputs.get("MEAMN", torch.zeros(B, T, 12, device=device))
    meamn_memory = meamn[..., _MEAMN_MEMORY_STATE]       # (B, T)

    # -- H3 features --
    amp_range_5s = h3_features[_AMP_RANGE_5S]            # (B, T)
    loud_std_36s = h3_features[_LOUD_STD_36S]            # (B, T)
    harm_autocorr_36s = h3_features[_HARM_AUTOCORR_36S]  # (B, T)

    # -- P0: Binding State --
    # Current hippocampal binding = E0 binding + M0 consolidation + MEAMN.
    # MEAMN memory_state provides autobiographical context: strong existing
    # memories modulate current binding activation.
    # Fernandez-Rubio et al. 2022: hippocampus + cingulate at memorized tones.
    p0 = torch.sigmoid(
        0.35 * e0
        + 0.30 * m0
        + 0.35 * meamn_memory
    )

    # -- P1: Segmentation State --
    # Current episodic boundary detection = E1 segmentation + M1 encoding
    # rate + amplitude dynamic range (energy changes mark boundaries).
    # Zacks et al. 2007: event perception boundaries.
    p1 = torch.sigmoid(
        0.40 * e1
        + 0.30 * m1
        + 0.30 * amp_range_5s
    )

    # -- P2: Storage State --
    # Cortical storage activation = E2 storage + M2 synthesis + harmonic
    # repetition (autocorrelation indicates consolidable patterns) gated
    # by salience variability (varying salience means richer encoding).
    # Sikka et al. 2015: age-related hippocampal-to-cortical shift.
    p2 = torch.sigmoid(
        0.35 * e2
        + 0.25 * m2
        + 0.25 * harm_autocorr_36s
        + 0.15 * loud_std_36s
    )

    return p0, p1, p2
