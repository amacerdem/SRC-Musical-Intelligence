"""HCMC F-Layer -- Forecast (2D).

Forward predictions for hippocampal-cortical memory circuit:

  F0: consolidation_fc  -- Consolidation prediction (5-36s ahead) [0, 1]
  F1: retrieval_fc      -- Retrieval probability prediction (1-5s ahead) [0, 1]

H3 consumed:
    (3, 24, 19, 0)  stumpf_fusion stability H24 L0    -- long-term binding stability
    (22, 24, 19, 0) entropy stability H24 L0           -- pattern stability over 36s
    (5, 24, 22, 0)  harmonicity autocorrelation H24 L0 -- harmonic repetition
    (14, 20, 22, 0) tonalness autocorrelation H20 L0   -- tonal repetition
    (3, 16, 1, 2)   stumpf_fusion mean H16 L2          -- binding coherence

F-layer primarily reuses E+M+P outputs and long-horizon H3 tuples for
trajectory prediction.

See Building/C3-Brain/F4-Memory-Systems/mechanisms/hcmc/HCMC-forecast.md
Buzsaki 2015: Sharp-wave ripples forecast consolidation outcome.
Biau et al. 2025: Theta reinstatement during retrieval.
Rolls 2013: CA3 pattern completion from partial cues.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_STUMPF_STAB_36S = (3, 24, 19, 0)       # stumpf_fusion stability H24 L0
_ENTROPY_STAB_36S = (22, 24, 19, 0)     # entropy stability H24 L0
_HARM_AUTOCORR_36S = (5, 24, 22, 0)     # harmonicity autocorrelation H24 L0
_TONAL_AUTOCORR_5S = (14, 20, 22, 0)    # tonalness autocorrelation H20 L0
_STUMPF_MEAN_1S = (3, 16, 1, 2)         # stumpf_fusion mean H16 L2


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor, Tensor],
    p: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """F-layer: forward predictions for hippocampal-cortical memory.

    F0 (consolidation_fc): Predicts whether the hippocampal trace currently
    being formed will successfully transfer to cortical long-term storage.
    Uses long-horizon (H24, 36s) stability features. High consolidation
    forecast when patterns are stable and coherent over extended windows.
    Buzsaki 2015: sharp-wave ripples forecast consolidation outcome.

    F1 (retrieval_fc): Predicts the probability that a retrieval event
    will occur in the near future (1-5s). Based on autocorrelation features
    detecting repetition -- when musical patterns repeat, hippocampal
    pattern completion is triggered.
    Biau et al. 2025: theta reinstatement during retrieval.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e: ``(E0, E1, E2)`` from extraction layer.
        m: ``(M0, M1, M2)`` from temporal integration layer.
        p: ``(P0, P1, P2)`` from cognitive present layer.

    Returns:
        ``(F0, F1)`` each ``(B, T)``.
    """
    _e0, _e1, e2 = e
    m0, _m1, m2 = m
    p0, _p1, p2 = p

    # -- H3 features --
    stumpf_stab_36s = h3_features[_STUMPF_STAB_36S]       # (B, T)
    entropy_stab_36s = h3_features[_ENTROPY_STAB_36S]      # (B, T)
    harm_autocorr_36s = h3_features[_HARM_AUTOCORR_36S]    # (B, T)
    tonal_autocorr_5s = h3_features[_TONAL_AUTOCORR_5S]    # (B, T)
    stumpf_mean_1s = h3_features[_STUMPF_MEAN_1S]          # (B, T)

    # -- F0: Consolidation Forecast --
    # Will the current hippocampal trace consolidate to cortical storage?
    # Uses stumpf stability (binding coherence persists), entropy stability
    # (pattern regularity persists), M0 consolidation strength, and P2
    # storage state as trajectory inputs.
    # Buzsaki 2015: ripples drive transfer; stable patterns consolidate.
    f0 = torch.sigmoid(
        0.25 * stumpf_stab_36s
        + 0.25 * entropy_stab_36s
        + 0.25 * m0
        + 0.25 * p2
    )

    # -- F1: Retrieval Forecast --
    # Will a retrieval event occur in the next 1-5s?
    # Harmonic autocorrelation (H24) + tonal autocorrelation (H20) detect
    # repetition. Current binding state (P0) and stumpf binding coherence
    # indicate template readiness for pattern completion.
    # Biau et al. 2025: theta reinstatement during recall.
    # Rolls 2013: CA3 pattern completion from partial cues.
    f1 = torch.sigmoid(
        0.30 * harm_autocorr_36s
        + 0.25 * tonal_autocorr_5s
        + 0.25 * p0
        + 0.20 * stumpf_mean_1s
    )

    return f0, f1
