"""TSCP -- Temporal Synaptic Consolidation Processor.

Encoder nucleus (depth 1) in SPU, Function F8. Models timbre-specific cortical
plasticity -- the long-term reorganization of auditory cortex for trained
instrument timbres. The core finding is a double dissociation: violinists
show enhanced N1m responses to violin tones but not trumpet tones, and vice
versa (Pantev et al. 2001).

TSCP extracts harmonic envelope signatures (tristimulus balance), computes
spectral contrast (warmth/sharpness), and tracks plasticity magnitude through
timbre flux variability. The M-layer applies a multiplicative gate (f01 * f02)
ensuring that enhancement is high only when both trained response AND
timbre specificity are present simultaneously.

Reads: EDNR (intra-circuit via relay_outputs)

R3 Ontology Mapping (post-freeze 97D):
    inharmonicity:              [5]      (A, instrument character)
    warmth:                     [12]     (C, low-frequency spectral balance)
    sharpness:                  [13]     (C, high-frequency energy)
    tonalness:                  [14]     (C, harmonic-to-noise ratio)
    spectral_autocorrelation:   [17]     (C, harmonic periodicity)
    tristimulus1/2/3:           [18:21]  (C, harmonic envelope signature)
    timbre_change:              [24]     (D, temporal timbre flux)
    x_l5l7:                     [41:47]  (G, consonance-timbre coupling)

Output structure: E(3) + M(1) + P(3) + F(3) = 10D
  E-layer   [0:3]   Extraction           (sigmoid)  scope=internal
  M-layer   [3:4]   Temporal Integration (product)  scope=internal
  P-layer   [4:7]   Cognitive Present    (sigmoid)  scope=hybrid
  F-layer   [7:10]  Forecast             (sigmoid)  scope=external

See Building/C3-Brain/F8-Learning-and-Plasticity/mechanisms/tscp/
"""
from __future__ import annotations

from typing import Dict, Tuple

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
    2: "17ms (gamma)",
    5: "46ms (alpha-beta)",
    8: "300ms (delta)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 3: "std", 19: "stability",
}

# -- Law labels ----------------------------------------------------------------
_L_LABELS = {0: "memory", 1: "prediction", 2: "integration"}


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


# -- R3 feature name constants ------------------------------------------------
_INHARMONICITY = 5
_WARMTH = 12
_SHARPNESS = 13
_TONALNESS = 14
_TRISTIMULUS1 = 18
_TRISTIMULUS2 = 19
_TRISTIMULUS3 = 20
_TIMBRE_CHANGE = 24
_X_L5L7_0 = 41


# -- 12 H3 Demand Specifications -----------------------------------------------
# Timbre-specific cortical plasticity requires fast spectral envelope (17ms),
# mid-range harmonic structure (46ms), and long-range stability/variability
# (300ms) for template matching and plasticity tracking.
# E-layer: 6 tuples, M-layer: 0, P-layer: 2, F-layer: 4.

_TSCP_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-Layer: Timbre Extraction (6 tuples) ===
    # 0: Tristimulus1 (F0 energy) at 17ms -- fundamental energy
    _h3(18, "tristimulus1", 2, 0, 2,
        "F0 energy at 17ms -- fundamental harmonic energy",
        "Pantev 2001"),
    # 1: Tristimulus2 (mid-harmonic energy) at 17ms
    _h3(19, "tristimulus2", 2, 0, 2,
        "Mid-harmonic energy at 17ms -- partials 2-4",
        "Pantev 2001"),
    # 2: Tristimulus3 (high-harmonic energy) at 17ms
    _h3(20, "tristimulus3", 2, 0, 2,
        "High-harmonic energy at 17ms -- partials 5+",
        "Pantev 2001"),
    # 3: Inharmonicity at 46ms
    _h3(5, "inharmonicity", 5, 0, 2,
        "Inharmonicity at 46ms -- instrument character",
        "Pantev 2001"),
    # 4: Tonalness stability over 300ms
    _h3(14, "tonalness", 8, 19, 0,
        "Tonalness stability over 300ms -- harmonic purity tracking",
        "Bellmann 2024"),
    # 5: Timbre flux variability 300ms
    _h3(24, "timbre_change", 8, 3, 0,
        "Timbre flux variability 300ms -- plasticity trigger",
        "Santoyo 2023"),

    # === P-Layer: Real-Time State (2 unique tuples) ===
    # 6: Current warmth at 17ms
    _h3(12, "warmth", 2, 0, 2,
        "Current warmth at 17ms -- spectral template matching",
        "Bellmann 2024"),
    # 7: Current sharpness at 17ms
    _h3(13, "sharpness", 2, 0, 2,
        "Current sharpness at 17ms -- spectral template matching",
        "Bellmann 2024"),

    # === F-Layer: Predictions (4 unique tuples) ===
    # 8: Mean warmth over 46ms
    _h3(12, "warmth", 5, 1, 0,
        "Mean warmth over 46ms -- note-by-note timbre prediction",
        "Halpern 2004"),
    # 9: Mean tonalness over 46ms
    _h3(14, "tonalness", 5, 1, 0,
        "Mean tonalness over 46ms -- note-by-note timbre prediction",
        "Halpern 2004"),
    # 10: Mean timbre flux over 300ms
    _h3(24, "timbre_change", 8, 1, 0,
        "Mean timbre flux over 300ms -- enhancement trajectory",
        "Leipold 2021"),
    # 11: Consonance x Timbre coupling 300ms
    _h3(41, "x_l5l7[0]", 8, 0, 2,
        "Consonance x Timbre coupling 300ms -- generalization basis",
        "Pantev 2001"),
)

assert len(_TSCP_H3_DEMANDS) == 12


class TSCP(Encoder):
    """Temporal Synaptic Consolidation Processor -- SPU Encoder (depth 1, 10D).

    Models timbre-specific cortical plasticity -- the long-term reorganization
    of auditory cortex for trained instrument timbres. The core finding is a
    double dissociation: violinists show enhanced N1m responses to violin
    tones but not trumpet tones, and vice versa (Pantev et al. 2001).

    Three extraction features (trained_timbre_response, timbre_specificity,
    plasticity_magnitude) capture the timbre-specific cortical enhancement
    landscape. The temporal integration layer applies a multiplicative gate
    (enhancement_function = f01 * f02) to ensure selectivity. The cognitive
    present estimates template matching quality, enhanced response, and
    timbre identity binding. Forecasts predict timbre continuation,
    enhancement trajectory, and generalization to related timbres.

    Pantev et al. 2001: Timbre-specific N1m enhancement with double
    dissociation F(1,15)=28.55, p=.00008 (MEG, N=16).

    Bellmann & Asano 2024: ALE meta-analysis of timbre processing in
    auditory cortex. L-SMG/HG 4640 mm3, R-pSTG/PT 3128 mm3 (k=18, N=338).

    Santoyo et al. 2023: Enhanced theta phase-locking for timbre-based
    streams (EEG).

    Whiteford et al. 2025: Plasticity locus is cortical not subcortical
    (d=-0.064, BF=0.13, fMRI).

    Halpern et al. 2004: Timbre imagery activates posterior PT overlapping
    with perception (R STG t=4.66, perception t=6.89).

    Leipold et al. 2021: Robust musicianship effects on functional/structural
    networks replicable across AP/non-AP (n=153).

    Dependency chain:
        TSCP is an Encoder (Depth 1) -- reads EDNR relay output
        (F8 intra-circuit). Computed after EDNR in F8 pipeline.

    Downstream feeds:
        -> timbre_plasticity belief (Appraisal)
        -> instrument_identity belief (Appraisal)
        -> cortical_enhancement belief (Appraisal)
    """

    NAME = "TSCP"
    FULL_NAME = "Temporal Synaptic Consolidation Processor"
    UNIT = "SPU"
    FUNCTION = "F8"
    OUTPUT_DIM = 10
    UPSTREAM_READS = ("EDNR",)

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("f01:trained_timbre_response", "f02:timbre_specificity",
             "f03:plasticity_magnitude"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Temporal Integration", 3, 4,
            ("M0:enhancement_function",),
            scope="internal",
        ),
        LayerSpec(
            "P", "Cognitive Present", 4, 7,
            ("P0:recognition_quality", "P1:enhanced_response",
             "P2:timbre_identity"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 7, 10,
            ("F0:timbre_continuation", "F1:cortical_enhancement_pred",
             "F2:generalization_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _TSCP_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01:trained_timbre_response", "f02:timbre_specificity",
            "f03:plasticity_magnitude",
            "M0:enhancement_function",
            "P0:recognition_quality", "P1:enhanced_response",
            "P2:timbre_identity",
            "F0:timbre_continuation", "F1:cortical_enhancement_pred",
            "F2:generalization_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Secondary auditory cortex -- trained timbre response
            RegionLink("f01:trained_timbre_response", "A2", 0.85,
                       "Pantev 2001"),
            # Planum Temporale -- timbre specificity
            RegionLink("f02:timbre_specificity", "PT", 0.80,
                       "Bellmann 2024"),
            # Bilateral pSTG/HG -- plasticity magnitude
            RegionLink("f03:plasticity_magnitude", "pSTG", 0.75,
                       "Bellmann 2024"),
            # L-SMG/HG -- recognition quality (template storage)
            RegionLink("P0:recognition_quality", "SMG", 0.80,
                       "Bellmann 2024"),
            # Bilateral STG -- enhanced response
            RegionLink("P1:enhanced_response", "STG", 0.80,
                       "Alluri 2012"),
            # STG sub-regions -- timbre identity binding
            RegionLink("P2:timbre_identity", "STG", 0.75,
                       "Sturm 2014"),
            # Right posterior STG -- timbre continuation imagery
            RegionLink("F0:timbre_continuation", "rSTG", 0.70,
                       "Halpern 2004"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            # Acetylcholine -- plasticity gating for cortical reorganization
            NeuroLink("f03:plasticity_magnitude", "acetylcholine", 0.70,
                      "Whiteford 2025"),
            # BDNF -- long-term plasticity support for enhancement
            NeuroLink("F1:cortical_enhancement_pred", "BDNF", 0.65,
                      "Leipold 2021"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Pantev et al.", 2001,
                         "Timbre-specific N1m enhancement with double "
                         "dissociation F(1,15)=28.55, p=.00008. Violinists: "
                         "violin > trumpet > pure tone",
                         "MEG, N=16"),
                Citation("Bellmann & Asano", 2024,
                         "ALE meta-analysis of timbre processing in auditory "
                         "cortex. L-SMG/HG 4640 mm3 primary cluster, "
                         "R-pSTG/PT 3128 mm3",
                         "meta-analysis, k=18, N=338"),
                Citation("Santoyo et al.", 2023,
                         "Enhanced theta phase-locking for timbre-based "
                         "streams in musicians",
                         "EEG"),
                Citation("Whiteford et al.", 2025,
                         "Plasticity locus is cortical not subcortical. "
                         "Brainstem responses not enhanced (d=-0.064, BF=0.13)",
                         "fMRI"),
                Citation("Halpern et al.", 2004,
                         "Timbre imagery activates posterior PT overlapping "
                         "with perception. R STG imagery t=4.66, "
                         "perception t=6.89",
                         "fMRI"),
                Citation("Alluri et al.", 2012,
                         "Timbral brightness bilateral STG Z=8.13, "
                         "timbral fullness Z=7.35 during naturalistic music",
                         "fMRI"),
                Citation("Sturm et al.", 2014,
                         "Spectral centroid (timbre) has distinct activation "
                         "spots in STG separate from lyrics and harmony",
                         "ECoG high-gamma"),
                Citation("Leipold et al.", 2021,
                         "Robust musicianship effects on functional/structural "
                         "networks replicable across AP/non-AP",
                         "MRI, n=153"),
                Citation("Zatorre & Halpern", 2005,
                         "Auditory cortex supports veridical timbre "
                         "representation during imagery",
                         "review"),
            ),
            evidence_tier="beta",
            confidence_range=(0.65, 0.85),
            falsification_criteria=(
                "Trained timbre response (f01) must show enhanced N1m for "
                "trained instrument timbre relative to untrained timbres "
                "(Pantev 2001: F(1,15)=28.55, p=.00008)",
                "Timbre specificity (f02) must show age-of-inception effect "
                "(Pantev 2001: r=-0.634, p=.026); earlier training produces "
                "more selective cortical enhancement",
                "Enhancement function (M0) must implement double dissociation: "
                "high only when BOTH trained response AND specificity are "
                "present; if additive model fits better, multiplicative gate "
                "is invalid",
                "Plasticity magnitude (f03) must correlate with timbre change "
                "variability; if static timbres produce equal plasticity, "
                "the novelty trigger model is invalid (Santoyo 2023)",
                "Recognition quality (P0) must correlate with L-SMG/HG BOLD "
                "signal during instrument identification tasks (Bellmann & "
                "Asano 2024: ALE 4640 mm3 cluster)",
                "Timbre continuation (F0) must predict upcoming timbre in "
                "imagery paradigms; if imagery and perception do not share "
                "cortical substrate, model is invalid (Halpern 2004)",
                "Generalization prediction (F2) must show graded transfer: "
                "trained > similar > dissimilar > pure tone (Pantev 2001 "
                "hierarchy); if transfer is all-or-none, gradient model fails",
                "Plasticity effects must be cortical not subcortical "
                "(Whiteford 2025: d=-0.064, BF=0.13 for brainstem)",
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
        """Transform R3/H3 + EDNR relay output into 10D timbre plasticity.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{"EDNR": (B, T, D)}``

        Returns:
            ``(B, T, 10)`` -- E(3) + M(1) + P(3) + F(3)
        """
        relay_outputs = relay_outputs or {}
        ednr = relay_outputs.get(
            "EDNR",
            torch.zeros(r3_features.shape[0], r3_features.shape[1], 10,
                        device=r3_features.device),
        )

        e = compute_extraction(h3_features, r3_features, ednr)
        m = compute_temporal_integration(h3_features, r3_features, e, ednr)
        p = compute_cognitive_present(h3_features, r3_features, e, m, ednr)
        f = compute_forecast(h3_features, e, m, p, ednr)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
