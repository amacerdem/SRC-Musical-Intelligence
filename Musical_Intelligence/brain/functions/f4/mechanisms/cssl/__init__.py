"""CSSL -- Cross-Species Song Learning.

Associator nucleus (depth 2) in IMU, Function F4. Models the shared
neural mechanisms underlying vocal learning across species -- songbird
tutor-tutee copying, primate vocal learning, and human musical memory
rely on homologous auditory-motor circuits (HVC/Broca's, Area X/basal
ganglia, hippocampal binding).

Reads: upstream F4 depth-0/1 nuclei (MEAMN, PNH, MMP, RASN, etc.)

R3 Ontology Mapping (post-freeze 97D):
    roughness:              [0]      (A, consonance binding)
    sethares_dissonance:    [1]      (A, harmonic structure)
    stumpf_fusion:          [3]      (A, tonal fusion)
    harmonicity:            [5]      (A, harmonic purity)
    pitch_strength:         [6]      (A, pitch clarity)
    amplitude:              [7]      (B, vocal intensity)
    onset_strength:         [11]     (B, rhythm boundary)
    warmth:                 [12]     (C, voice quality)
    tonalness:              [14]     (C, tonal purity)
    entropy:                [22]     (D, pattern complexity)
    x_l0l5:                 [25:33]  (F, motor-auditory coupling)
    x_l5l7:                 [41:49]  (G, melody-timbre binding)

Output structure: E(3) + M(2) + P(2) + F(3) = 10D
  E-layer [0:3]   Extraction    (sigmoid)  scope=internal
  M-layer [3:5]   Memory        (sigmoid)  scope=internal
  P-layer [5:7]   Present       (clamp)    scope=hybrid
  F-layer [7:10]  Forecast      (sigmoid)  scope=external

See Building/C3-Brain/F4-Memory-Systems/mechanisms/cssl/
"""
from __future__ import annotations

from typing import Dict, Optional, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.nucleus import Associator
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
    16: "1000ms (beat)",
    20: "5000ms (phrase)",
    24: "36000ms (section)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 3: "std", 17: "periodicity", 19: "stability",
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


# -- 15 H3 Demand Specifications -----------------------------------------------
# Cross-species song learning: stumpf fusion, pitch, onset, tonalness, entropy,
# warmth, amplitude at beat/phrase/section horizons.

_CSSL_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # --- E-layer (6 tuples) ---
    _h3(3, "stumpf_fusion", 16, 1, 2,
        "Binding stability at beat level for melody copying",
        "Burchardt 2025"),
    _h3(6, "pitch_strength", 16, 0, 2,
        "Current pitch clarity for melody template",
        "Bolhuis 2015"),
    _h3(11, "onset_strength", 16, 0, 2,
        "Current rhythm boundary for beat segmentation",
        "Burchardt 2025"),
    _h3(14, "tonalness", 16, 0, 2,
        "Current tonal purity for melody matching",
        "Bolhuis 2010"),
    _h3(22, "entropy", 16, 0, 2,
        "Current pattern complexity for template novelty",
        "Burchardt 2025"),
    _h3(12, "warmth", 16, 0, 2,
        "Current voice quality for song recognition",
        "Eliades 2024"),
    # --- M-layer (5 tuples) ---
    _h3(3, "stumpf_fusion", 20, 1, 0,
        "Binding stability over phrase window for conservation",
        "Zhang 2024"),
    _h3(3, "stumpf_fusion", 24, 1, 0,
        "Long-term binding context for template fidelity",
        "Lipkind 2013"),
    _h3(6, "pitch_strength", 20, 1, 0,
        "Pitch stability over phrase for melody matching",
        "Bolhuis 2015"),
    _h3(14, "tonalness", 20, 1, 0,
        "Tonal stability over phrase for conservation",
        "Zhang 2024"),
    _h3(22, "entropy", 20, 1, 0,
        "Average complexity over 5s for fidelity",
        "Lipkind 2013"),
    # --- P-layer (2 new tuples; (12,16,0,2) shared with E-layer) ---
    _h3(11, "onset_strength", 20, 17, 0,
        "Beat regularity over 5s for entrainment",
        "Barchet 2024"),
    _h3(7, "amplitude", 20, 3, 0,
        "Energy variability = dynamic range for entrainment",
        "Barchet 2024"),
    # --- F-layer (2 tuples) ---
    _h3(22, "entropy", 24, 19, 0,
        "Pattern stability over 36s for binding prediction",
        "Burchardt 2025"),
    _h3(12, "warmth", 20, 1, 0,
        "Sustained voice warmth for learning trajectory",
        "Eliades 2024"),
)

assert len(_CSSL_H3_DEMANDS) == 15


class CSSL(Associator):
    """Cross-Species Song Learning -- IMU Associator (depth 2, 10D).

    Models the shared neural mechanisms underlying vocal learning across
    species. Songbird tutor-tutee copying (HVC-Area X pathway), primate
    vocal learning (auditory dorsal/ventral streams), and human musical
    memory all rely on homologous auditory-motor circuits.

    Burchardt, Varkevisser & Spierings 2025: Zebra finch tutees copy
    melody and rhythm from tutors; r=0.94 all-shared, r=0.88 overall
    (N=54).

    Bolhuis, Okanoya & Scharff 2010: FoxP2, basal ganglia, auditory
    cortex homologies across species (review).

    Bolhuis & Moorman 2015: HVC-Broca's area, Area X-basal ganglia
    neural circuit homologies (review).

    Zhang et al. 2024: Homologous auditory dorsal/ventral pathways
    across marmosets, macaques, and humans (dMRI, N=21, P<0.001).

    Dependency chain:
        MEAMN (Depth 0, Relay) + PNH/MMP (Depth 0) +
        RASN/PMIM/... (Depth 1, Encoder) --> CSSL (Depth 2)

    Upstream reads:
        All same-unit Relay and Encoder outputs (memory-only pathway)

    Downstream feeds:
        -> F4 Memory beliefs (Appraisal)
        -> DMMS: F0:learning_trajectory feeds developmental scaffold depth
        -> MEAMN: F1:binding_prediction feeds autobiographical memory
    """

    NAME = "CSSL"
    FULL_NAME = "Cross-Species Song Learning"
    UNIT = "IMU"
    FUNCTION = "F4"
    OUTPUT_DIM = 10
    UPSTREAM_READS = ("MEAMN", "PNH", "MMP",
                      "RASN", "PMIM", "OII", "HCMC", "RIRI", "MSPBA")
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("E0:rhythm_copying", "E1:melody_copying",
             "E2:all_shared_binding"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 3, 5,
            ("M0:conservation_index", "M1:template_fidelity"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 5, 7,
            ("P0:entrainment_state", "P1:template_match"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 7, 10,
            ("F0:learning_trajectory", "F1:binding_prediction",
             "F2:reserved"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _CSSL_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:rhythm_copying", "E1:melody_copying",
            "E2:all_shared_binding",
            "M0:conservation_index", "M1:template_fidelity",
            "P0:entrainment_state", "P1:template_match",
            "F0:learning_trajectory", "F1:binding_prediction",
            "F2:reserved",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Auditory cortex (STG/A1) -- spectrotemporal encoding, template
            RegionLink("E0:rhythm_copying", "STG", 0.85,
                       "Burchardt 2025"),
            RegionLink("E1:melody_copying", "A1", 0.85,
                       "Bolhuis 2015"),
            RegionLink("P1:template_match", "STG", 0.80,
                       "Eliades 2024"),
            # Basal ganglia -- motor sequencing, vocal refinement
            RegionLink("E0:rhythm_copying", "putamen", 0.80,
                       "Jarvis 2004"),
            RegionLink("P0:entrainment_state", "caudate", 0.80,
                       "Barchet 2024"),
            # Hippocampus -- sequential binding
            RegionLink("E2:all_shared_binding", "HPC", 0.85,
                       "Burchardt 2025"),
            RegionLink("F1:binding_prediction", "HPC", 0.75,
                       "Burchardt 2025"),
            # IFG / Broca's -- song timing and sequencing
            RegionLink("E1:melody_copying", "IFG", 0.75,
                       "Bolhuis 2015"),
            RegionLink("F0:learning_trajectory", "IFG", 0.70,
                       "Lipkind 2013"),
            # Premotor / SMA -- motor output for vocal production
            RegionLink("P0:entrainment_state", "SMA", 0.75,
                       "Barchet 2024"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # CSSL is structural-memory, no direct neuromodulator

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Burchardt, Varkevisser & Spierings", 2025,
                         "Zebra finch tutees copy melody and rhythm from "
                         "tutors; r=0.94 all-shared, r=0.88 overall IOI beat "
                         "correlation; cross-species vocal learning foundation",
                         "behavioral, N=54"),
                Citation("Bolhuis, Okanoya & Scharff", 2010,
                         "FoxP2, basal ganglia, auditory cortex homologies "
                         "across species; shared vocal learning neural "
                         "substrates across songbirds and humans",
                         "review"),
                Citation("Bolhuis & Moorman", 2015,
                         "HVC-Broca's area, Area X-basal ganglia neural "
                         "circuit homologies; song timing and sequencing "
                         "parallels between songbirds and humans",
                         "review"),
                Citation("Zhang et al.", 2024,
                         "Homologous auditory dorsal/ventral pathways across "
                         "marmosets, macaques, and humans; conservation of "
                         "auditory processing architecture",
                         "dMRI, N=21"),
                Citation("Lipkind et al.", 2013,
                         "Stepwise vocal combinatorial capacity parallels "
                         "between songbirds and human infants; babbling-to-"
                         "song developmental trajectory",
                         "cross-species behavioral"),
                Citation("Barchet et al.", 2024,
                         "Speech and music recruit partially distinct "
                         "rhythmic timing mechanisms; ~2 Hz music beat "
                         "entrainment timescale; motor-auditory coupling",
                         "behavioral"),
                Citation("Eliades et al.", 2024,
                         "Dual vocal suppression timescales (phasic + tonic) "
                         "in marmoset auditory cortex; template matching "
                         "during vocal production",
                         "single-neuron, N=3285"),
                Citation("Jarvis", 2004,
                         "7 homologous cerebral vocal nuclei for learned "
                         "birdsong and human language; cross-species vocal "
                         "learning circuit architecture",
                         "review"),
            ),
            evidence_tier="gamma",
            confidence_range=(0.45, 0.65),
            falsification_criteria=(
                "Rhythm copying (E0) and melody copying (E1) must both "
                "contribute to all-shared binding (E2 > 0.3 when both E0 "
                "and E1 > 0.5) per Burchardt 2025: r=0.94 all-shared "
                "correlation requires both rhythm and melody",
                "Conservation index (M0) should be high (> 0.5) for simple "
                "tonal patterns with clear harmonic structure and low for "
                "noise/atonal stimuli; if M0 remains high for non-tonal "
                "stimuli, cross-species universality claim is invalid",
                "Template fidelity (M1) must increase with repeated exposure "
                "to the same musical pattern; if M1 does not increase with "
                "repetition, template matching mechanism is invalid",
                "Learning trajectory (F0) should predict actual template "
                "fidelity improvement over the next 2-5s; if prediction "
                "accuracy < chance, the learning model is falsified",
                "Binding prediction (F1) should correlate with long-term "
                "memory consolidation; if F1 high but memory recall low "
                "after 36s, hippocampal binding model is invalid",
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
        """Transform R3/H3 + upstream into 10D cross-species song learning.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: ``{"MEAMN": (B, T, dim), ...}`` -- all
                same-unit Relay and Encoder routable outputs.

        Returns:
            ``(B, T, 10)`` -- E(3) + M(2) + P(2) + F(3)
        """
        e = compute_extraction(h3_features, r3_features, upstream_outputs)
        m = compute_temporal_integration(h3_features, r3_features, e)
        p = compute_cognitive_present(h3_features, r3_features, e, m)
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
