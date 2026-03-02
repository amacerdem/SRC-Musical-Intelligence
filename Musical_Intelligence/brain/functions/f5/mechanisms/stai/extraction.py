"""STAI E-Layer -- Extraction (4D).

Spectral-Temporal Aesthetic Integration extraction signals:
  E0: spectral_integrity        -- Consonance quality of harmonic content [0, 1]
  E1: temporal_integrity        -- Forward flow / rhythmic coherence [0, 1]
  E2: aesthetic_integration     -- Supra-additive spectral x temporal [0, 1]
  E3: vmpfc_ifg_connectivity    -- vmPFC-IFG functional coupling [0, 1]

E0 captures spectral integrity -- the degree to which the harmonic content is
consonant and well-formed. Uses the A-group consonance features (roughness
inverted, helmholtz_kang, stumpf_fusion, sensory_pleasantness) combined with
short-horizon H3 consonance tracking. High E0 means the spectral content
supports aesthetic response.

E1 captures temporal integrity -- the quality of forward flow and temporal
coherence. Uses energy dynamics (amplitude, loudness, onset_strength) and
spectral/energy change rates at the 300ms phrase horizon. High E1 means the
temporal structure supports aesthetic engagement.

E2 captures the supra-additive interaction between spectral and temporal
dimensions. Kim 2019 showed that aesthetic response is NOT the sum of spectral
and temporal contributions -- it requires BOTH dimensions intact. E2 implements
this as a multiplicative interaction: spectral_integrity x temporal_integrity.
Disrupting either alone reduces to ~35%.

E3 captures vmPFC-IFG connectivity -- the functional coupling that mediates
the spectral-temporal interaction. Uses the aesthetic binding signal (x_l4l5)
as a proxy for inter-region connectivity. The binding signal at 300ms captures
the integration window where vmPFC and IFG coordinate aesthetic judgment.

H3 demands consumed (9 tuples):
  (0, 0, 0, 2)   roughness value H0 L2             -- dissonance 5.8ms
  (0, 3, 1, 2)   roughness mean H3 L2              -- mean dissonance 100ms
  (2, 0, 0, 2)   helmholtz_kang value H0 L2        -- consonance 5.8ms
  (2, 3, 1, 2)   helmholtz_kang mean H3 L2         -- mean consonance 100ms
  (4, 3, 0, 2)   sensory_pleasantness value H3 L2  -- pleasantness 100ms
  (21, 8, 1, 0)  spectral_change mean H8 L0        -- spectral flux 300ms
  (22, 8, 8, 0)  energy_change velocity H8 L0      -- energy change rate 300ms
  (33, 8, 0, 2)  x_l4l5[0] value H8 L2            -- aesthetic binding 300ms
  (33, 8, 14, 2) x_l4l5[0] periodicity H8 L2      -- binding periodicity 300ms

R3 features:
  [0] roughness, [1] sethares_dissonance, [2] helmholtz_kang,
  [3] stumpf_fusion, [4] sensory_pleasantness,
  [7] amplitude, [8] loudness, [11] onset_strength,
  [21] spectral_change, [22] energy_change, [33:41] x_l4l5

Kim et al. 2019: 2x2 factorial fMRI -- spectral x temporal interaction at
vmPFC-IFG (T=6.852). Disrupting either dimension reduces response to ~35%.
Blood & Zatorre 2001: vmPFC, NAcc activation from consonant music.
Koelsch 2014: STG/Heschl's for spectral quality, reward for temporal.

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/stai/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_ROUGH_VAL_H0 = (0, 0, 0, 2)          # roughness value H0 L2
_ROUGH_MEAN_H3 = (0, 3, 1, 2)         # roughness mean H3 L2
_HELM_VAL_H0 = (2, 0, 0, 2)           # helmholtz_kang value H0 L2
_HELM_MEAN_H3 = (2, 3, 1, 2)          # helmholtz_kang mean H3 L2
_PLEAS_VAL_H3 = (4, 3, 0, 2)          # sensory_pleasantness value H3 L2
_SPEC_CHANGE_MEAN_H8 = (21, 8, 1, 0)  # spectral_change mean H8 L0
_ENERGY_VEL_H8 = (22, 8, 8, 0)        # energy_change velocity H8 L0
_BINDING_VAL_H8 = (33, 8, 0, 2)       # x_l4l5[0] value H8 L2
_BINDING_PERIOD_H8 = (33, 8, 14, 2)   # x_l4l5[0] periodicity H8 L2

# -- R3 feature indices (post-freeze 97D) ------------------------------------
_ROUGHNESS = 0
_SETHARES = 1
_HELMHOLTZ = 2
_STUMPF_FUSION = 3
_SENSORY_PLEASANTNESS = 4
_AMPLITUDE = 7
_LOUDNESS = 8
_ONSET_STRENGTH = 11
_SPECTRAL_CHANGE = 21
_ENERGY_CHANGE = 22
_X_L4L5_START = 33
_X_L4L5_END = 41


def _wsig(x: Tensor) -> Tensor:
    """Wide sigmoid — full [0, 1] dynamic range (gain=5, center=0.35)."""
    return (1.0 + torch.exp(-5.0 * (x - 0.35))).reciprocal()


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """Compute E-layer: spectral-temporal aesthetic extraction signals.

    E0 (spectral_integrity) captures consonance quality. A-group features
    (roughness inverted, helmholtz, stumpf, pleasantness) combined with
    short-horizon H3 tracking. Heschl's gyrus + STG spectral encoding.

    E1 (temporal_integrity) captures forward flow quality. Energy dynamics
    (amplitude, loudness, onset) combined with spectral/energy change rates.
    Temporal coherence drives engagement via reward circuit.

    E2 (aesthetic_integration) captures the supra-additive spectral x temporal
    interaction. Multiplicative coupling -- disrupting either dimension alone
    collapses to ~35%, disrupting both to ~0%. Kim 2019: T=6.852.

    E3 (vmpfc_ifg_connectivity) captures the functional coupling between
    vmPFC and IFG that mediates the interaction. Aesthetic binding signal
    (x_l4l5) proxies inter-region connectivity at the 300ms integration
    window.

    Kim et al. 2019: vmPFC-IFG connectivity mediates spectral x temporal
    interaction (fMRI N=20, T=6.852, FWE p<.05).
    Blood & Zatorre 2001: vmPFC, NAcc activation correlates with consonance
    (PET N=10).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``

    Returns:
        ``(E0, E1, E2, E3)`` each ``(B, T)``
    """
    # -- H3 features --
    rough_val = h3_features[_ROUGH_VAL_H0]              # (B, T)
    rough_mean = h3_features[_ROUGH_MEAN_H3]            # (B, T)
    helm_val = h3_features[_HELM_VAL_H0]                # (B, T)
    helm_mean = h3_features[_HELM_MEAN_H3]              # (B, T)
    pleas_val = h3_features[_PLEAS_VAL_H3]              # (B, T)
    spec_change_mean = h3_features[_SPEC_CHANGE_MEAN_H8]  # (B, T)
    energy_vel = h3_features[_ENERGY_VEL_H8]            # (B, T)
    binding_val = h3_features[_BINDING_VAL_H8]          # (B, T)
    binding_period = h3_features[_BINDING_PERIOD_H8]    # (B, T)

    # -- R3 features --
    roughness = r3_features[..., _ROUGHNESS]              # (B, T)
    sethares = r3_features[..., _SETHARES]                # (B, T)
    helmholtz = r3_features[..., _HELMHOLTZ]              # (B, T)
    stumpf = r3_features[..., _STUMPF_FUSION]             # (B, T)
    pleasantness = r3_features[..., _SENSORY_PLEASANTNESS]  # (B, T)
    amplitude = r3_features[..., _AMPLITUDE]              # (B, T)
    loudness = r3_features[..., _LOUDNESS]                # (B, T)
    onset = r3_features[..., _ONSET_STRENGTH]             # (B, T)
    spectral_change = r3_features[..., _SPECTRAL_CHANGE]  # (B, T)
    energy_change = r3_features[..., _ENERGY_CHANGE]      # (B, T)
    x_l4l5 = r3_features[..., _X_L4L5_START:_X_L4L5_END]  # (B, T, 8)
    x_l4l5_mean = x_l4l5.mean(dim=-1)                    # (B, T)

    # -- Derived signals --
    # Consonance composite: higher = more consonant.
    # Includes Sethares 1993 (partial-pair beating) alongside Plomp-Levelt
    # roughness for robust noise vs harmonic differentiation — ratio-based
    # measures (helmholtz, stumpf) don't penalize broadband noise because
    # it lacks discrete partials.
    consonance = (
        0.25 * (1.0 - roughness)
        + 0.20 * (1.0 - sethares)
        + 0.15 * helmholtz
        + 0.15 * stumpf
        + 0.25 * pleasantness
    )

    # Temporal flow: energy dynamics + onset clarity + spectral stability.
    # ALL terms gated by consonance — temporal stationarity in broadband
    # noise is NOT forward flow.  Kim 2019: temporal integrity requires
    # musically structured content, not mere stationarity or loudness.
    temporal_flow = (
        0.35 * amplitude * onset
        + 0.35 * (1.0 - spectral_change.abs()) * consonance.clamp(min=0.1)
        + 0.30 * loudness * consonance.clamp(min=0.1)
    )

    # -- E0: Spectral Integrity --
    # Consonance quality of harmonic content. A-group features at micro and
    # integration horizons. Heschl's gyrus / STG spectral encoding.
    # Blood & Zatorre 2001: pleasure correlates with consonance quality.
    e0 = _wsig(
        0.30 * helm_val * (1.0 - rough_val).clamp(min=0.1)
        + 0.30 * helm_mean * pleas_val
        + 0.20 * consonance
        + 0.20 * (1.0 - sethares) * stumpf
    )

    # -- E1: Temporal Integrity --
    # Forward flow quality. Energy dynamics and change rates at phrase horizon.
    # Stability terms (energy_change, spectral_change) gated by consonance
    # to prevent broadband noise from scoring high on temporal integrity.
    # Koelsch 2014: temporal expectation resolution engages reward circuit
    # only for musically structured stimuli.
    e1 = _wsig(
        0.30 * spec_change_mean * energy_vel.clamp(min=0.1) * consonance.clamp(min=0.1)
        + 0.30 * temporal_flow
        + 0.20 * onset * amplitude
        + 0.20 * (1.0 - energy_change.abs()) * loudness * consonance.clamp(min=0.1)
    )

    # -- E2: Aesthetic Integration --
    # Supra-additive spectral x temporal interaction. The key finding from
    # Kim 2019: aesthetic response is NOT additive -- it requires BOTH
    # dimensions. Multiplicative coupling implements this property.
    # Disrupting either alone reduces to ~35% of full response.
    spectral_quality = 0.50 * e0 + 0.50 * consonance
    temporal_quality = 0.50 * e1 + 0.50 * temporal_flow
    interaction = spectral_quality * temporal_quality  # supra-additive

    e2 = _wsig(
        0.50 * interaction
        + 0.30 * pleas_val * spec_change_mean.clamp(min=0.1)
        + 0.20 * (1.0 - rough_mean) * energy_vel.clamp(min=0.1)
    )

    # -- E3: vmPFC-IFG Connectivity --
    # Functional coupling mediating the spectral-temporal interaction.
    # x_l4l5 aesthetic binding signal proxies inter-region connectivity.
    # Kim 2019: vmPFC-IFG connectivity is the interaction locus (T=6.852).
    e3 = _wsig(
        0.35 * binding_val * interaction.clamp(min=0.1)
        + 0.35 * binding_period * x_l4l5_mean
        + 0.30 * e2 * consonance.clamp(min=0.1)
    )

    return e0, e1, e2, e3
