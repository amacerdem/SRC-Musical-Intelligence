"""DAP -- Developmental Affective Plasticity.

Associator nucleus (depth 2) in ARU, Function F5. Models how early musical
exposure (0-5 years) shapes lifelong affective processing capacity through
critical period plasticity, auditory-limbic connection formation, and
parental singing templates.

Core finding: Critical period plasticity gates formation of auditory-limbic
connections. Parental singing creates initial music-emotion binding
templates via hippocampus-amygdala pairing. Consonance preference emerges
by 2 months (Trainor 2005). Culture-specific rhythm processing by 12
months (Hannon & Trehub 2005).

Reads: NEMAC.nostalgia (E1, idx 1) — nostalgic warmth amplifies dev sensitivity
       MEAMN.memory_state (P0, idx 5) — memory retrieval for exposure history
MEAMN is cross-function (F4, IMU unit).

R3 Ontology Mapping (post-freeze 97D):
    roughness:              [0]      (A, consonance discrimination)
    sensory_pleasantness:   [4]      (A, hedonic response strength)
    loudness:               [10]     (B, arousal response baseline)
    tonalness:              [14]     (C, tonal template strength)
    distribution_entropy:   [22]     (D, pattern acquisition depth)
    x_l0l5:                 [25:33]  (F, affective learning pattern)

Output structure: E(1) + D(4) + P(3) + F(2) = 10D
  E-layer [0:1]   Extraction           (sigmoid)  scope=internal
  D-layer [1:5]   Temporal Integration (sigmoid)  scope=internal
  P-layer [5:8]   Cognitive Present    (sigmoid)  scope=hybrid
  F-layer [8:10]  Forecast             (sigmoid)  scope=external

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/dap/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.nucleus import Associator
from Musical_Intelligence.contracts.dataclasses import (
    Citation,
    CrossUnitPathway,
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
    16: "1000ms (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 2: "std", 8: "velocity", 20: "entropy",
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
_ROUGHNESS = 0
_PLEASANTNESS = 4
_LOUDNESS = 10
_TONALNESS = 14
_ENTROPY = 22


# -- 6 H3 Demand Specifications -----------------------------------------------
# Single horizon: H16 (1s) — critical period operates on immediate acoustic
# features, not long-horizon trends. All L2 (integration) except arousal
# dynamics (L0 memory) for maturation tracking.
#
# E-layer: 3 tuples (pleasantness, roughness, loudness — core hedonic input)
# D-layer: 3 tuples (pleasantness std, entropy, loudness velocity — plasticity)

_DAP_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-layer: Developmental Sensitivity (3 tuples) ===
    _h3(_PLEASANTNESS, "sensory_pleasantness", 16, 0, 2,
        "Hedonic response at 1s L2 — maturation marker for affective capacity",
        "Trainor 2005"),
    _h3(_ROUGHNESS, "roughness", 16, 0, 2,
        "Consonance discrimination at 1s L2 — critical period marker",
        "Trainor 2005"),
    _h3(_LOUDNESS, "loudness", 16, 0, 2,
        "Arousal baseline at 1s L2 — developmental arousal sensitivity",
        "Trehub 2015"),

    # === D-layer: Developmental Dynamics (3 tuples) ===
    _h3(_PLEASANTNESS, "sensory_pleasantness", 16, 2, 2,
        "Hedonic variability at 1s L2 — plasticity indicator (exploration)",
        "Hensch 2005"),
    _h3(_ENTROPY, "distribution_entropy", 16, 20, 2,
        "Predictability at 1s L2 — pattern acquisition depth",
        "Hannon & Trehub 2005"),
    _h3(_LOUDNESS, "loudness", 16, 8, 0,
        "Arousal dynamics at 1s L0 — neural maturation tracking",
        "Chang & Merzenich 2003"),
)

assert len(_DAP_H3_DEMANDS) == 6


class DAP(Associator):
    """Developmental Affective Plasticity -- ARU Associator (depth 2, 10D).

    Models how early musical exposure (0-5 years) shapes lifelong affective
    processing capacity through critical period plasticity in auditory cortex,
    hippocampus-amygdala scaffolding, and parental singing templates.

    Trainor et al. (2005): Infants show consonance preference by 2 months;
    critical period for auditory cortex (A1/STG) plasticity shapes lifelong
    tonal processing (EEG, N=20 infants).

    Hannon & Trehub (2005): Western infants detect mistuned intervals in
    non-native scales at 6 months but not 12 months -- culture-specific
    exposure narrows perceptual sensitivity (behavioral, N=36).

    Hensch (2005): Molecular brakes (PV interneurons, myelin) close
    critical periods; GABA maturation gates cortical plasticity
    (review, animal models + human analogy).

    Chang & Merzenich (2003): Continuous noise exposure during critical
    period delays tonotopic map refinement in A1 (rat, N=12/group).

    Dependency chain:
        DAP reads NEMAC (F5 intra-unit, depth 1) and MEAMN (F4 cross-unit).
        Computed after NEMAC and MEAMN in the C3 scheduler.

    Downstream feeds:
        -> developmental_sensitivity belief (Anticipation)
        -> F11 (Development) meta-layer
    """

    NAME = "DAP"
    FULL_NAME = "Developmental Affective Plasticity"
    UNIT = "ARU"
    FUNCTION = "F5"
    OUTPUT_DIM = 10
    UPSTREAM_READS = ("NEMAC", "MEAMN")
    CROSS_UNIT_READS = (
        CrossUnitPathway(
            pathway_id="IMU_MEAMN__ARU_DAP__memory_state",
            name="MEAMN memory state to DAP exposure history",
            source_unit="IMU",
            source_model="MEAMN",
            source_dims=("memory_state",),
            target_unit="ARU",
            target_model="DAP",
            correlation="r=0.55",
            citation="Janata 2009",
        ),
    )

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 1,
            ("E0:dev_sensitiv",),
            scope="internal",
        ),
        LayerSpec(
            "D", "Temporal Integration", 1, 5,
            ("D0:critical_period", "D1:plasticity_coeff",
             "D2:exposure_history", "D3:neural_maturation"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Cognitive Present", 5, 8,
            ("P0:current_affect", "P1:familiarity_warmth",
             "P2:learning_rate"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 8, 10,
            ("F0:adult_hedonic_pred", "F1:preference_stab"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _DAP_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:dev_sensitiv",
            "D0:critical_period", "D1:plasticity_coeff",
            "D2:exposure_history", "D3:neural_maturation",
            "P0:current_affect", "P1:familiarity_warmth",
            "P2:learning_rate",
            "F0:adult_hedonic_pred", "F1:preference_stab",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Auditory Cortex (A1/STG) — critical period plasticity hub
            RegionLink("E0:dev_sensitiv", "A1_STG", 0.85,
                       "Trainor 2005"),
            # Hippocampus — scaffold formation for music-memory binding
            RegionLink("D2:exposure_history", "hippocampus", 0.80,
                       "Hannon & Trehub 2005"),
            # Amygdala — emotional tagging of early scaffolds
            RegionLink("P0:current_affect", "amygdala", 0.80,
                       "Koelsch 2014"),
            # mPFC — synaptic plasticity hub, developmental integration
            RegionLink("D1:plasticity_coeff", "mPFC", 0.75,
                       "Hensch 2005"),
            # mPFC — familiarity-driven warmth and self-referential
            RegionLink("P1:familiarity_warmth", "mPFC", 0.70,
                       "Pereira 2011"),
            # A1/STG — neural maturation of tonotopic maps
            RegionLink("D3:neural_maturation", "A1_STG", 0.75,
                       "Chang & Merzenich 2003"),
            # Hippocampus — adult hedonic capacity from developmental scaffold
            RegionLink("F0:adult_hedonic_pred", "hippocampus", 0.65,
                       "Janata 2009"),
            # Amygdala — preference consolidation
            RegionLink("F1:preference_stab", "amygdala", 0.60,
                       "North & Hargreaves 2008"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # DAP modulates via plasticity, no direct neuromodulator

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Trainor et al.", 2005,
                         "Infants show consonance preference by 2 months; "
                         "critical period for auditory cortex (A1/STG) "
                         "plasticity shapes lifelong tonal processing",
                         "EEG, N=20 infants"),
                Citation("Hannon & Trehub", 2005,
                         "Western infants detect mistuned intervals in "
                         "non-native scales at 6 months but not 12 months; "
                         "culture-specific exposure narrows perceptual "
                         "sensitivity",
                         "behavioral, N=36"),
                Citation("Hensch", 2005,
                         "Molecular brakes (PV interneurons, myelin) close "
                         "critical periods; GABA maturation gates cortical "
                         "plasticity",
                         "review, animal models"),
                Citation("Chang & Merzenich", 2003,
                         "Continuous noise exposure during critical period "
                         "delays tonotopic map refinement in A1",
                         "rat, N=12/group"),
                Citation("Trehub et al.", 2015,
                         "Parental singing establishes music-emotion binding "
                         "templates; infant-directed singing modulates "
                         "arousal and attention",
                         "review + behavioral"),
                Citation("Koelsch", 2014,
                         "Music-evoked emotions via auditory cortex -> "
                         "amygdala -> hippocampus pathway; STAR model of "
                         "music-evoked affect",
                         "review"),
                Citation("Pereira et al.", 2011,
                         "Familiar music activates hippocampus and mPFC; "
                         "familiarity modulates reward network engagement",
                         "fMRI, N=21"),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.70),
            falsification_criteria=(
                "Developmental sensitivity (E0) must be higher for consonant "
                "vs dissonant stimuli; if roughness does not inversely predict "
                "E0, the consonance-discrimination marker is invalid "
                "(Trainor 2005: infants prefer consonance by 2 months)",
                "Critical period (D0) should activate most strongly for "
                "acoustic features matching infant sensitivity profiles; if "
                "D0 does not decrease with increased roughness/complexity, "
                "the critical period model is invalid (Knudsen 2004)",
                "Exposure history (D2) must correlate inversely with entropy; "
                "if high-entropy (novel) stimuli produce high D2, the "
                "familiarity-exposure link is invalid (Hannon & Trehub 2005)",
                "Plasticity coefficient (D1) must show inverted-U with "
                "hedonic variability; extreme low or high variability should "
                "both produce moderate plasticity (Hensch 2005)",
                "Learning rate (P2) must decrease as exposure history (D2) "
                "increases; if saturated exposure does not reduce learning "
                "rate, the critical period closure model is invalid",
                "NEMAC nostalgia (upstream) must amplify E0; removing "
                "nostalgia input should reduce developmental sensitivity "
                "(testable via ablation of NEMAC pathway)",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        upstream_outputs: Dict[str, Tensor],
    ) -> Tensor:
        """Transform R3/H3 + upstream into 10D developmental plasticity output.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: ``{"NEMAC": (B, T, 11), "MEAMN": (B, T, 12)}``

        Returns:
            ``(B, T, 10)`` -- E(1) + D(4) + P(3) + F(2)
        """
        e = compute_extraction(h3_features, r3_features, upstream_outputs)
        d = compute_temporal_integration(
            h3_features, r3_features, e, upstream_outputs,
        )
        p = compute_cognitive_present(h3_features, r3_features, e, d)
        f = compute_forecast(h3_features, e, d, p)

        output = torch.stack([*e, *d, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
