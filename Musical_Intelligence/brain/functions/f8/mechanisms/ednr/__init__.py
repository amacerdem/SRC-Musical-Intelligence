"""EDNR -- Expertise-Dependent Network Reorganization.

Relay nucleus (depth 0) in NDU, Function F8. Models the structural and
functional network changes that accompany long-term musical training.
Musicians show increased within-network connectivity and decreased
between-network connectivity compared to non-musicians, reflecting
functional compartmentalization — the brain's networks become more
specialised and internally coherent with expertise.

Paraskevopoulos et al. 2022: musicians show 106 within-network edges vs
192 between-network edges in non-musicians (MEG, FDR-corrected, Hedges'
g=-1.09 for area 47m). Leipold et al. 2021: robust musicianship effects
on intrahemispheric FC including bilateral PT-PT connectivity (pFWE<0.05,
n=153). Moller et al. 2021: NM show distributed CT correlations (V1-HG)
while musicians show only local correlations (FDR<10%).

Dependency chain:
    EDNR is a Relay (Depth 0) -- reads R3/H3 directly, no upstream dependencies.
    Runs in parallel with other depth-0 relays at Phase 0a.

R3 Ontology Mapping (v1 -> 97D freeze):
    sensory_pleasantness:       [4]      (A, sensory_pleasantness)
    loudness:                   [8]      (B, velocity_D)
    tonalness:                  [14]     (C, brightness_kuttruff)
    spectral_flatness:          [16]     (C, spectral_flatness)
    x_l0l5:                     [25:33]  (F, coupling)
    x_l4l5:                     [33:41]  (G, coupling)

Output structure: E(4) + M(2) + P(2) + F(2) = 10D
  E-layer [0:4]   Extraction           (mixed)    scope=internal
  M-layer [4:6]   Temporal Integration (mixed)    scope=internal
  P-layer [6:8]   Cognitive Present    (sigmoid)  scope=hybrid
  F-layer [8:10]  Forecast             (sigmoid)  scope=external

See Building/C3-Brain/F8-Learning-and-Plasticity/mechanisms/ednr/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.nucleus import Relay
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
    3: "100ms (instantaneous)",
    16: "1000ms (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 14: "periodicity", 20: "entropy",
}

# -- Law labels ----------------------------------------------------------------
_L_LABELS = {0: "memory", 1: "forward", 2: "integration"}


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


# -- 16 H3 Demand Specifications ----------------------------------------------
# E-layer: 8 tuples, M-layer: 4 tuples, P-layer: 2 tuples, F-layer: 2 tuples
# All 16 tuples are unique across layers.

_EDNR_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-layer: Network connectivity extraction (tuples 0-7) ===

    # #0: Within-network coupling 100ms -- intra-network binding
    _h3(25, "x_l0l5", 3, 0, 2,
        "Within-network coupling at 100ms -- intra-network binding",
        "Leipold 2021"),
    # #1: Coupling variability 100ms -- within-network dynamics
    _h3(25, "x_l0l5", 3, 2, 2,
        "Coupling variability at 100ms -- within-network dynamics",
        "Paraskevopoulos 2022"),
    # #2: Mean coupling over 1s -- sustained within-network coherence
    _h3(25, "x_l0l5", 16, 1, 2,
        "Mean coupling over 1s -- sustained within-network coherence",
        "Leipold 2021"),
    # #3: Coupling periodicity 1s -- within-network rhythmic structure
    _h3(25, "x_l0l5", 16, 14, 2,
        "Coupling periodicity at 1s -- within-network rhythmic structure",
        "Paraskevopoulos 2022"),
    # #4: Pleasantness at 100ms -- immediate hedonic quality
    _h3(4, "sensory_pleasantness", 3, 0, 2,
        "Pleasantness at 100ms -- immediate hedonic quality",
        "Papadaki 2023"),
    # #5: Mean pleasantness 1s -- sustained hedonic quality
    _h3(4, "sensory_pleasantness", 16, 1, 2,
        "Mean pleasantness over 1s -- sustained hedonic quality",
        "Papadaki 2023"),
    # #6: Tonalness at 100ms -- processing complexity indicator
    _h3(14, "tonalness", 3, 0, 2,
        "Tonalness at 100ms -- processing complexity indicator",
        "Papadaki 2023"),
    # #7: Mean tonalness over 1s -- sustained tonal processing
    _h3(14, "tonalness", 16, 1, 2,
        "Mean tonalness over 1s -- sustained tonal processing",
        "Porfyri 2025"),

    # === M-layer: Cross-network coupling (tuples 8-11) ===

    # #8: Cross-network coupling 100ms -- inter-network binding
    _h3(33, "x_l4l5", 3, 0, 2,
        "Cross-network coupling at 100ms -- inter-network binding",
        "Paraskevopoulos 2022"),
    # #9: Cross coupling variability 100ms -- inter-network dynamics
    _h3(33, "x_l4l5", 3, 2, 2,
        "Cross coupling variability at 100ms -- inter-network dynamics",
        "Paraskevopoulos 2022"),
    # #10: Mean cross coupling over 1s -- sustained inter-network state
    _h3(33, "x_l4l5", 16, 1, 2,
        "Mean cross coupling over 1s -- sustained inter-network state",
        "Paraskevopoulos 2022"),
    # #11: Cross coupling entropy 1s -- inter-network complexity
    _h3(33, "x_l4l5", 16, 20, 2,
        "Cross coupling entropy at 1s -- inter-network complexity",
        "Cui 2025"),

    # === P-layer: Flatness dynamics (tuples 12-13) ===

    # #12: Flatness at 100ms -- stimulus regularity
    _h3(16, "spectral_flatness", 3, 0, 2,
        "Flatness at 100ms -- stimulus regularity proxy",
        "Moller 2021"),
    # #13: Flatness variability 1s -- distribution complexity
    _h3(16, "spectral_flatness", 16, 2, 2,
        "Flatness variability at 1s -- distribution complexity",
        "Moller 2021"),

    # === F-layer: Loudness dynamics (tuples 14-15) ===

    # #14: Loudness at 100ms -- stimulus intensity
    _h3(8, "loudness", 3, 0, 2,
        "Loudness at 100ms -- stimulus intensity for efficiency prediction",
        "Papadaki 2023"),
    # #15: Loudness entropy 1s -- stimulus complexity
    _h3(8, "loudness", 16, 20, 2,
        "Loudness entropy at 1s -- stimulus complexity for efficiency prediction",
        "Papadaki 2023"),
)

assert len(_EDNR_H3_DEMANDS) == 16


class EDNR(Relay):
    """Expertise-Dependent Network Reorganization -- NDU Relay (depth 0, 10D).

    Models the structural and functional network changes accompanying
    long-term musical training. Musicians show increased within-network
    connectivity and decreased between-network connectivity (functional
    compartmentalization). The core metric is the within/between connectivity
    ratio, which increases with expertise.

    Paraskevopoulos et al. 2022: musicians 106 within-network vs 192
    between-network edges (MEG, FDR-corrected, Hedges' g=-1.09 for 47m).
    Leipold et al. 2021: bilateral PT-PT connectivity (pFWE<0.05, n=153).
    Moller et al. 2021: NM distributed CT correlations, M local only
    (FDR<10%). Papadaki et al. 2023: network strength correlates with
    interval recognition (rho=0.36) and BGS (r=0.35, Cohen's d=0.70).
    Cui et al. 2025: 1-year training does NOT change WM -- slow plasticity.
    Porfyri et al. 2025: Group x Time F(1,28)=4.635, eta^2=0.168.

    Dependency chain:
        EDNR is a Relay (Depth 0) -- reads R3/H3 directly.
        No upstream mechanism dependencies.

    Downstream feeds:
        -> within_connectivity, compartmentalization for F8 kernel beliefs
        -> network_architecture, expertise_signature for plasticity beliefs
        -> processing_efficiency for learning rate modulation
    """

    NAME = "EDNR"
    FULL_NAME = "Expertise-Dependent Network Reorganization"
    UNIT = "NDU"
    FUNCTION = "F8"
    OUTPUT_DIM = 10

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 4,
            ("f01:within_connectivity", "f02:between_connectivity",
             "f03:compartmentalization", "f04:expertise_signature"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Temporal Integration", 4, 6,
            ("network_architecture", "compartmentalization_idx"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Cognitive Present", 6, 8,
            ("current_compartm", "network_isolation"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 8, 10,
            ("optimal_config_pred", "processing_efficiency"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _EDNR_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01:within_connectivity", "f02:between_connectivity",
            "f03:compartmentalization", "f04:expertise_signature",
            "network_architecture", "compartmentalization_idx",
            "current_compartm", "network_isolation",
            "optimal_config_pred", "processing_efficiency",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # STG -- within-network connectivity (auditory cortex)
            RegionLink("f01:within_connectivity", "STG", 0.85,
                       "Leipold 2021"),
            # PT -- within-network coupling (planum temporale)
            RegionLink("f01:within_connectivity", "PT", 0.85,
                       "Leipold 2021"),
            # IFG -- between-network coupling (area 47m as hub)
            RegionLink("f02:between_connectivity", "IFG", 0.80,
                       "Paraskevopoulos 2022"),
            # HG -- compartmentalization (Heschl's Gyrus)
            RegionLink("f03:compartmentalization", "HG", 0.80,
                       "Moller 2021"),
            # SMG -- expertise signature
            RegionLink("f04:expertise_signature", "SMG", 0.75,
                       "Papadaki 2023"),
            # vmPFC -- expertise signature (valuation)
            RegionLink("f04:expertise_signature", "vmPFC", 0.70,
                       "Papadaki 2023"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            # BDNF -- within-connectivity plasticity
            NeuroLink("f01:within_connectivity", "BDNF", 0.70,
                      "Leipold 2021"),
            # Glutamate -- expertise-dependent processing efficiency
            NeuroLink("f04:expertise_signature", "Glutamate", 0.65,
                      "Papadaki 2023"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Paraskevopoulos", 2022,
                         "Musicians show 106 within-network vs 192 between-"
                         "network edges; area 47m as hub with Hedges' g=-1.09",
                         "MEG, multilayer network, FDR-corrected"),
                Citation("Leipold", 2021,
                         "Robust musicianship effects on intrahemispheric FC "
                         "including bilateral PT-PT connectivity",
                         "fMRI structural/functional, N=153, pFWE<0.05"),
                Citation("Moller", 2021,
                         "NM show distributed V1-HG CT correlations while "
                         "musicians show only local correlations; left IFOF "
                         "FA cluster p<0.001",
                         "structural MRI, cortical thickness, FDR<10%"),
                Citation("Papadaki", 2023,
                         "Aspiring professionals show greater auditory network "
                         "strength (d=0.70) and global efficiency (d=0.70) "
                         "correlating with performance (rho=0.36, r=0.35)",
                         "resting-state fMRI, N=48"),
                Citation("Cui", 2025,
                         "1-year musical training does NOT change white matter "
                         "structure -- slow structural plasticity constraint",
                         "longitudinal RCT, DTI, N=68"),
                Citation("Porfyri", 2025,
                         "Group x Time interaction for musical training: "
                         "F(1,28)=4.635, eta^2=0.168",
                         "longitudinal EEG, N=30"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.75, 0.88),
            falsification_criteria=(
                "Within-network connectivity (f01) must be higher in musicians "
                "than non-musicians during auditory processing "
                "(Paraskevopoulos 2022: 106 vs 192 edges, FDR-corrected)",
                "Between-network connectivity (f02) must be lower in musicians "
                "than non-musicians, reflecting compartmentalization "
                "(Paraskevopoulos 2022: Hedges' g=-1.09 for area 47m)",
                "Compartmentalization ratio (f03 = f01/f02) must exceed 1.0 "
                "for expert-like processing and approach 1.0 for novice-like "
                "(Moller 2021: local vs distributed CT correlations)",
                "1-year training should NOT produce significant WM changes, "
                "constraining the time-scale of structural plasticity "
                "(Cui 2025: longitudinal DTI, N=68)",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Transform R3/H3 into 10D expertise-dependent network representation.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``

        Returns:
            ``(B, T, 10)`` -- E(4) + M(2) + P(2) + F(2)
        """
        e = compute_extraction(h3_features, r3_features)
        m = compute_temporal_integration(h3_features, r3_features, e)
        p = compute_cognitive_present(h3_features, r3_features, e, m)
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
