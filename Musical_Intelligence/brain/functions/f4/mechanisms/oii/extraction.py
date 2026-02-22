"""OII E-Layer -- Extraction (3D).

Three explicit features modeling oscillatory integration-segregation dynamics:

  E0: slow_integration    -- Theta/alpha integration strength [0, 1]
  E1: fast_segregation    -- Gamma-band local processing efficiency [0, 1]
  E2: mode_switching      -- Integration-segregation switch efficiency [0, 1]

H3 consumed:
    (3, 10, 1, 2)   stumpf_fusion mean H10 L2      -- harmonic binding at chord level
    (11, 10, 0, 2)  onset_strength value H10 L2     -- gamma burst trigger at chord level
    (21, 10, 0, 2)  spectral_flux value H10 L2      -- transition signal at chord level
    (5, 10, 0, 2)   periodicity value H10 L2        -- oscillatory regularity
    (22, 10, 0, 2)  entropy value H10 L2            -- integration demand
    (15, 10, 0, 2)  spectral_centroid value H10 L2  -- frequency balance at chord level

R3 consumed:
    [0]  roughness          -- E1: gamma-band complexity proxy
    [3]  stumpf_fusion      -- E0: tonal fusion = theta-mediated binding
    [5]  periodicity        -- E0: oscillatory regularity proxy
    [11] onset_strength     -- E1+E2: mode switch trigger
    [21] spectral_flux      -- E2: integration-segregation transition signal
    [22] entropy            -- E2: integration demand

Reads: PMIM, PNH, HCMC, MSPBA, MEAMN via relay_outputs (graceful fallback).

See Building/C3-Brain/F4-Memory-Systems/mechanisms/oii/OII-extraction.md
Bruzzone et al. 2022: high Gf = stronger theta/alpha degree (p<0.001, MEG N=66).
Sturm et al. 2014: ECoG high gamma reveals distinct cortical representations.
Samiee et al. 2022: delta-beta PAC in rIFG (F(1)=43.95, p<0.0001).
"""
from __future__ import annotations

from typing import Dict, Optional, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_FUSION_MEAN_H10 = (3, 10, 1, 2)        # stumpf_fusion mean H10 L2
_ONSET_VAL_H10 = (11, 10, 0, 2)         # onset_strength value H10 L2
_FLUX_VAL_H10 = (21, 10, 0, 2)          # spectral_flux value H10 L2
_PERIOD_VAL_H10 = (5, 10, 0, 2)         # periodicity value H10 L2
_ENTROPY_VAL_H10 = (22, 10, 0, 2)       # entropy value H10 L2
_CENTROID_VAL_H10 = (15, 10, 0, 2)      # spectral_centroid value H10 L2

# -- R3 indices ----------------------------------------------------------------
_ROUGHNESS = 0
_STUMPF_FUSION = 3
_PERIODICITY = 5
_ONSET_STRENGTH = 11
_SPECTRAL_FLUX = 21
_ENTROPY = 22


def _relay_field(
    relay_outputs: Dict[str, Tensor],
    name: str,
    idx: int,
    shape_ref: Tensor,
) -> Tensor:
    """Gracefully extract a single field from an upstream relay.

    Returns zeros matching *shape_ref* ``(B, T)`` when *name* is absent.
    """
    relay = relay_outputs.get(name)
    if relay is None:
        return torch.zeros_like(shape_ref)
    return relay[..., idx]


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute E-layer: oscillatory integration-segregation extraction.

    E0 (slow_integration) tracks theta/alpha long-range binding strength.
    Frontal theta binds distributed features across temporal and parietal
    regions into unified percepts.  Uses harmonic syntax from upstream
    synthesis (PMIM encoding quality) and stumpf fusion at H10 (400ms
    chord-level timescale).

    E1 (fast_segregation) tracks gamma-band local processing efficiency.
    Gamma oscillations in auditory cortex support fine-grained spectral
    and temporal feature extraction.  Uses roughness (gamma demand) and
    onset strength at H10 (transient events trigger gamma bursts).

    E2 (mode_switching) tracks integration-to-segregation switch efficiency.
    DLPFC coordinates when to switch from binding (theta) to detail
    extraction (gamma).  Uses prediction error proxy from upstream HCMC,
    spectral flux at H10, and encoding quality from PNH.

    Bruzzone et al. 2022: DTI + MEG N=66/67, high Gf = stronger
    theta/alpha degree (p<0.001), lower theta/alpha segregation.
    Sturm et al. 2014: ECoG N=10, high gamma reveals distinct cortical
    representations for musical features.
    Samiee et al. 2022: MEG N=16, delta-beta PAC in rIFG
    F(1)=43.95, p<0.0001.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        relay_outputs: Upstream mechanism outputs (PMIM, PNH, HCMC, etc.).

    Returns:
        ``(E0, E1, E2)`` each ``(B, T)``.
    """
    # -- H3 features --
    fusion_h10 = h3_features[_FUSION_MEAN_H10]       # (B, T)
    onset_h10 = h3_features[_ONSET_VAL_H10]           # (B, T)
    flux_h10 = h3_features[_FLUX_VAL_H10]             # (B, T)
    period_h10 = h3_features[_PERIOD_VAL_H10]         # (B, T)
    entropy_h10 = h3_features[_ENTROPY_VAL_H10]       # (B, T)
    _centroid_h10 = h3_features[_CENTROID_VAL_H10]    # (B, T) -- reserved

    # -- R3 features --
    roughness = r3_features[..., _ROUGHNESS]           # (B, T)
    stumpf = r3_features[..., _STUMPF_FUSION]          # (B, T)
    periodicity = r3_features[..., _PERIODICITY]       # (B, T)
    onset = r3_features[..., _ONSET_STRENGTH]          # (B, T)
    flux = r3_features[..., _SPECTRAL_FLUX]            # (B, T)
    entropy = r3_features[..., _ENTROPY]               # (B, T)

    # -- Upstream relay signals (graceful fallback) --
    # PMIM synthesis quality → proxy for harmonic syntax aggregation
    syntax_proxy = _relay_field(relay_outputs, "PMIM", 0, roughness)
    # PNH encoding quality → proxy for encoding context
    encoding_proxy = _relay_field(relay_outputs, "PNH", 0, roughness)
    # HCMC prediction error → proxy for mode switching demand
    predict_err_proxy = _relay_field(relay_outputs, "HCMC", 0, roughness)

    # -- E0: Slow Integration --
    # Theta/alpha integration strength.  Frontal theta to temporal alpha
    # coherence.  f16 = sigma(0.30 * syntax.mean + 0.20 * fusion_h10).
    # Bruzzone et al. 2022: high Gf = stronger theta/alpha degree.
    e0 = torch.sigmoid(
        0.30 * (syntax_proxy + stumpf + periodicity) / 3.0
        + 0.20 * fusion_h10
    )

    # -- E1: Fast Segregation --
    # Gamma-band local processing efficiency.  Temporal cortex gamma
    # segregation.  f17 = sigma(0.25 * roughness + 0.25 * onset_h10).
    # Sturm et al. 2014: high gamma reveals distinct representations.
    e1 = torch.sigmoid(
        0.25 * roughness
        + 0.25 * onset_h10
    )

    # -- E2: Mode Switching --
    # DLPFC-mediated mode coordination.
    # f18 = sigma(0.20 * predict_err.mean + 0.15 * flux_h10
    #             + 0.15 * encoding.mean).
    # Samiee et al. 2022: delta-beta PAC as mode switching mechanism.
    e2 = torch.sigmoid(
        0.20 * predict_err_proxy
        + 0.15 * flux_h10
        + 0.15 * encoding_proxy
    )

    return e0, e1, e2
