"""STANM -- Spectrotemporal Attention Network Model.

Encoder nucleus (depth 1, reads R3/H3 directly + context) in ASU, Function F3.
Models how spectrotemporal attention networks in auditory cortex allocate
processing resources across temporal and spectral dimensions. Neural populations
in STG/HG form distributed networks that dynamically weight temporal vs spectral
features, with lateralization reflecting the asymmetric hemispheric specialization
for temporal (left) vs spectral (right) processing.

Dependency chain:
    STANM is an Encoder (Depth 1) -- reads R3/H3 directly + context.
    No upstream mechanism dependencies (UPSTREAM_READS = ()).

R3 Ontology Mapping (97D freeze):
    spectral_flux:      [10]  (B, onset_strength -- temporal periodicity proxy)
    spectral_change:    [21]  (D, spectral_flux -- tempo velocity)
    tonalness:          [14]  (C, tonal structure / spectral clarity)
    energy_change:      [22]  (D, energy variability)
    loudness:           [8]   (A, velocity_D -- loudness envelope)
    x_l0l5:             [25]  (F, coupling -- cross-band interaction)

Output structure: E(3) + M(3) + P(2) + F(3) = 11D
  E-layer [0:3]   Extraction    (sigmoid)  scope=internal
  M-layer [3:6]   Memory        (sigmoid/tanh)  scope=internal   NOTE: M2 uses TANH [-1,1]
  P-layer [6:8]   Present       (sigmoid)  scope=hybrid
  F-layer [8:11]  Forecast      (sigmoid/tanh)  scope=external   NOTE: F1 uses TANH [-1,1]

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/stanm/
"""
from __future__ import annotations

from typing import Dict, Optional, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.nucleus import Encoder
from Musical_Intelligence.contracts.dataclasses import (
    Citation,
    H3DemandSpec,
    LayerSpec,
    ModelMetadata,
    NeuroLink,
    RegionLink,
)

from .cognitive_present import compute_cognitive_present
from .extraction import compute_extraction
from .forecast import compute_forecast
from .temporal_integration import compute_temporal_integration

# -- Horizon labels ------------------------------------------------------------
_H_LABELS = {
    0: "25ms (gamma)",
    1: "50ms (gamma)",
    3: "100ms (alpha-beta)",
    4: "125ms (theta)",
    8: "500ms (delta)",
    16: "1000ms (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 8: "velocity",
    14: "periodicity", 18: "trend", 20: "entropy",
}

# -- Law labels ----------------------------------------------------------------
_L_LABELS = {0: "memory", 2: "integration"}


def _h3(
    r3_idx: int, r3_name: str, horizon: int, morph: int, law: int,
    purpose: str, citation: str,
) -> H3DemandSpec:
    """Shorthand factory for H3DemandSpec."""
    return H3DemandSpec(
        r3_idx=r3_idx,
        r3_name=r3_name,
        horizon=horizon,
        horizon_label=_H_LABELS.get(horizon, f"H{horizon}"),
        morph=morph,
        morph_name=_M_LABELS.get(morph, f"M{morph}"),
        law=law,
        law_name=_L_LABELS[law],
        purpose=purpose,
        citation=citation,
    )


# -- R3 feature indices (post-freeze 97D) ------------------------------------
_LOUDNESS = 8             # velocity_D (A group)
_SPECTRAL_FLUX = 10       # onset_strength (B group)
_TONALNESS = 14           # tonalness (C group)
_SPECTRAL_CHANGE = 21     # spectral_flux (D group)
_ENERGY_CHANGE = 22       # energy_change (D group)
_COUPLING = 25            # x_l0l5 (F group)


# -- 16 H3 Demand Specifications -----------------------------------------------
# Spectrotemporal attention at multiple timescales

_STANM_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    _h3(10, "spectral_flux", 16, 14, 2,
        "Temporal periodicity 1s", "Fritz 2007"),
    _h3(21, "spectral_change", 8, 8, 0,
        "Tempo velocity 500ms", "Fritz 2007"),
    _h3(14, "tonalness", 3, 0, 2,
        "Tonalness value 100ms", "Bidet-Caulet 2007"),
    _h3(14, "tonalness", 16, 1, 2,
        "Tonalness mean 1s", "Bidet-Caulet 2007"),
    _h3(22, "energy_change", 8, 2, 0,
        "Energy variability 500ms", "Fritz 2007"),
    _h3(25, "x_l0l5", 3, 20, 2,
        "Coupling entropy 100ms", "Mesgarani 2012"),
    _h3(10, "spectral_flux", 0, 0, 2,
        "Flux instant", "Fritz 2007"),
    _h3(10, "spectral_flux", 3, 1, 2,
        "Flux mean 100ms", "Fritz 2007"),
    _h3(21, "spectral_change", 1, 8, 0,
        "Spectral velocity 50ms", "Fritz 2007"),
    _h3(10, "spectral_flux", 4, 14, 2,
        "Flux periodicity 125ms", "Fritz 2007"),
    _h3(8, "loudness", 3, 0, 2,
        "Loudness value 100ms", "Bidet-Caulet 2007"),
    _h3(25, "x_l0l5", 16, 1, 2,
        "Coupling mean 1s", "Mesgarani 2012"),
    _h3(25, "x_l0l5", 16, 14, 2,
        "Coupling periodicity 1s", "Mesgarani 2012"),
    _h3(25, "x_l0l5", 3, 0, 2,
        "Coupling value 100ms", "Mesgarani 2012"),
    _h3(8, "loudness", 3, 20, 2,
        "Loudness entropy 100ms", "Bidet-Caulet 2007"),
    _h3(8, "loudness", 16, 1, 2,
        "Loudness mean 1s", "Bidet-Caulet 2007"),
)

assert len(_STANM_H3_DEMANDS) == 16


class STANM(Encoder):
    """Spectrotemporal Attention Network Model -- ASU Encoder (depth 1, 11D).

    Models how spectrotemporal attention networks in auditory cortex allocate
    processing resources across temporal and spectral dimensions. Neural
    populations in STG/HG form distributed networks that dynamically weight
    temporal vs spectral features, with lateralization reflecting hemispheric
    asymmetry for temporal (left) vs spectral (right) processing.

    Fritz et al. 2007: Rapid task-related plasticity of spectrotemporal
    receptive fields in primary auditory cortex (monkey single-unit, N=6).
    Bidet-Caulet et al. 2007: Dynamics of auditory cortex activation during
    selective attention (MEG, N=15).
    Mesgarani et al. 2012: Selective cortical representation of attended
    speaker in multi-talker scenes (ECoG, N=3).

    Dependency chain:
        STANM is an Encoder (Depth 1) -- reads R3/H3 directly + context.
        No upstream mechanism dependencies.

    Downstream feeds:
        -> Beliefs: spectrotemporal_allocation, network_state (Appraisal)
        -> Beliefs: lateral_asymmetry, compensation (Anticipation)
    """

    NAME = "STANM"
    FULL_NAME = "Spectrotemporal Attention Network Model"
    UNIT = "ASU"
    FUNCTION = "F3"
    OUTPUT_DIM = 11
    UPSTREAM_READS = ()

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("E0:temporal_attention", "E1:spectral_attention",
             "E2:network_topology"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 3, 6,
            ("M0:network_topology_m", "M1:local_clustering",
             "M2:lateralization"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 6, 8,
            ("P0:temporal_alloc", "P1:spectral_alloc"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 8, 11,
            ("F0:network_state_pred", "F1:lateral_pred",
             "F2:compensation_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _STANM_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:temporal_attention", "E1:spectral_attention",
            "E2:network_topology",
            "M0:network_topology_m", "M1:local_clustering",
            "M2:lateralization",
            "P0:temporal_alloc", "P1:spectral_alloc",
            "F0:network_state_pred", "F1:lateral_pred",
            "F2:compensation_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # STG -- spectrotemporal attention hub
            RegionLink("E0:temporal_attention", "STG", 0.85,
                       "Fritz 2007"),
            # HG -- primary auditory cortex spectral processing
            RegionLink("E1:spectral_attention", "A1_HG", 0.80,
                       "Fritz 2007"),
            # IFG -- top-down attention control
            RegionLink("M0:network_topology_m", "IFG", 0.75,
                       "Bidet-Caulet 2007"),
            # FEF -- attentional orienting
            RegionLink("P0:temporal_alloc", "FEF", 0.65,
                       "Fritz 2007"),
            # Parietal -- spatial/spectral attention
            RegionLink("P1:spectral_alloc", "IPS", 0.60,
                       "Bidet-Caulet 2007"),
            # TPJ -- lateralization / hemispheric asymmetry
            RegionLink("M2:lateralization", "TPJ", 0.60,
                       "Mesgarani 2012"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # STANM models attention allocation, no direct neuromodulator

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Fritz et al.", 2007,
                         "Rapid task-related plasticity of spectrotemporal "
                         "receptive fields in primary auditory cortex; "
                         "attention reshapes STRF within seconds; single-unit "
                         "recordings during active listening tasks",
                         "Monkey single-unit, N=6"),
                Citation("Bidet-Caulet et al.", 2007,
                         "Dynamics of auditory cortex activation during "
                         "selective attention; MEG reveals lateralized "
                         "spectrotemporal attention with sustained gamma "
                         "enhancement for attended features",
                         "MEG, N=15"),
                Citation("Mesgarani et al.", 2012,
                         "Selective cortical representation of attended "
                         "speaker in multi-talker scenes; ECoG shows STG "
                         "neural populations track attended spectrotemporal "
                         "features with high fidelity",
                         "ECoG, N=3"),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.85),
            falsification_criteria=(
                "Spectrotemporal receptive fields should reshape during "
                "active attention tasks (confirmed: Fritz 2007)",
                "Lateralized attention effects should be measurable via "
                "MEG/EEG hemispheric asymmetry (confirmed: Bidet-Caulet 2007)",
                "STG neural populations should selectively represent "
                "attended spectrotemporal features (confirmed: Mesgarani 2012)",
                "Disrupting STG should impair spectrotemporal attention "
                "(testable via TMS/lesion)",
                "Network topology should predict allocation efficiency "
                "(testable via graph-theoretic EEG analysis)",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        relay_outputs: Dict[str, Tensor],
    ) -> Tensor:
        """Transform R3/H3 into 11D spectrotemporal attention representation.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        NOTE: M2 (lateralization) and F1 (lateral_pred) use tanh activation
        with range [-1, 1]. The final clamp is (-1, 1) not (0, 1).

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{}`` (empty -- no upstream reads).

        Returns:
            ``(B, T, 11)`` -- E(3) + M(3) + P(2) + F(3)
        """
        e = compute_extraction(h3_features)
        m = compute_temporal_integration(h3_features, e)
        p = compute_cognitive_present(h3_features, e, m)
        f = compute_forecast(h3_features, m)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(-1.0, 1.0)
