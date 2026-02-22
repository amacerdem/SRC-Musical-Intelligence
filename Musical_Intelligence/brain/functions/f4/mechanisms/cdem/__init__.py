"""CDEM -- Context-Dependent Emotional Memory.

Associator nucleus (depth 2) in IMU, Function F4. Models how emotional
context modulates memory encoding, consolidation, and retrieval. Music
heard in congruent emotional contexts produces stronger, more vivid
memories that are more easily reinstated.

Reads: MEAMN (autobiographical memory network, depth 0)

R3 Ontology Mapping (post-freeze 97D):
    roughness:              [0]      (A, roughness)
    stumpf_fusion:          [3]      (A, stumpf_fusion)
    sensory_pleasantness:   [4]      (A, sensory_pleasantness)
    amplitude:              [7]      (A, velocity_A)
    loudness:               [10]     (B, onset_strength)
    onset_strength:         [11]     (B, onset_strength)
    warmth:                 [12]     (C, warmth)
    tonalness:              [14]     (C, brightness_kuttruff)
    spectral_flux:          [21]     (D, spectral_flux)
    entropy:                [22]     (D, entropy)
    spectral_concentration: [24]     (D, spectral_concentration)
    x_l0l5:                 [25:33]  (F, coupling)
    x_l5l7:                 [41:49]  (H, coupling)

Output structure: C(2) + M(2) + P(3) + F(3) = 10D
  C-layer [0:2]  Context-Dependent (sigmoid)  scope=internal
  M-layer [2:4]  Memory            (sigmoid)  scope=internal
  P-layer [4:7]  Present           (clamp)    scope=hybrid
  F-layer [7:10] Forecast          (sigmoid)  scope=external

Affect cross-circuit: F-layer predictions feed downstream into F4-MEAMN
(encoding strength), F6-SRP (retrieval context -> hedonic), F5 Emotion
(mood congruency -> emotional momentum).

See Building/C3-Brain/F4-Memory-Systems/mechanisms/cdem/
"""
from __future__ import annotations

from typing import Dict, Tuple

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
    0: "value", 1: "mean", 2: "std", 4: "max", 8: "velocity",
    18: "trend", 19: "stability",
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


# -- R3 feature indices (post-freeze 97D) -------------------------------------
_ROUGHNESS = 0
_STUMPF_FUSION = 3
_SENSORY_PLEASANTNESS = 4
_AMPLITUDE = 7
_LOUDNESS = 10
_ONSET_STRENGTH = 11
_WARMTH = 12
_TONALNESS = 14
_SPECTRAL_FLUX = 21
_ENTROPY = 22
_SPECTRAL_CONCENTRATION = 24


# -- 18 H3 Demand Specifications ----------------------------------------------
# Multi-scale: H16(1s) -> H20(5s) -> H24(36s)
# Context-dependent emotional memory: binding, arousal, congruency, recall

_CDEM_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === C-layer: Context-dependent extraction (9 tuples) ===
    _h3(_STUMPF_FUSION, "stumpf_fusion", 16, 1, 2,
        "Binding stability at 1s -- context modulation",
        "Sachs 2025"),
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 16, 0, 2,
        "Current mood input -- congruency",
        "Cheung 2019"),
    _h3(_LOUDNESS, "loudness", 16, 0, 2,
        "Current arousal level -- suppression",
        "Mitterschiffthaler 2007"),
    _h3(_ROUGHNESS, "roughness", 16, 0, 2,
        "Current valence (inverse) -- context",
        "Sachs 2025"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 16, 0, 2,
        "Context change rate -- arousal suppression",
        "Mitterschiffthaler 2007"),
    _h3(_ENTROPY, "entropy", 16, 0, 2,
        "Current context complexity -- arousal gating",
        "Mitterschiffthaler 2007"),
    _h3(_WARMTH, "warmth", 16, 0, 2,
        "Current context warmth -- encoding quality",
        "Cheung 2019"),
    _h3(_ONSET_STRENGTH, "onset_strength", 16, 0, 2,
        "Event boundary detection -- context shifts",
        "Borderie 2024"),
    _h3(_AMPLITUDE, "amplitude", 16, 8, 0,
        "Energy change rate -- arousal dynamics",
        "Mitterschiffthaler 2007"),

    # === M-layer: Congruency + recall (5 tuples) ===
    _h3(_STUMPF_FUSION, "stumpf_fusion", 20, 1, 0,
        "Binding over 5s context window -- congruency",
        "Sachs 2025"),
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 20, 18, 0,
        "Pleasantness trajectory -- congruency trend",
        "Sakakibara 2025"),
    _h3(_ROUGHNESS, "roughness", 20, 18, 0,
        "Valence trajectory -- congruency forecast",
        "Sachs 2025"),
    _h3(_WARMTH, "warmth", 20, 1, 0,
        "Sustained context warmth stability",
        "Sakakibara 2025"),
    _h3(_ENTROPY, "entropy", 20, 1, 0,
        "Average complexity over 5s -- recall probability",
        "Godden & Baddeley 1975"),

    # === P-layer: Binding state + arousal gate (3 tuples) ===
    _h3(_LOUDNESS, "loudness", 20, 1, 0,
        "Average arousal over 5s context -- binding",
        "Borderie 2024"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 20, 4, 0,
        "Peak context change over 5s -- binding",
        "Borderie 2024"),
    _h3(_ONSET_STRENGTH, "onset_strength", 20, 4, 0,
        "Peak event onset over 5s -- context boundary",
        "Borderie 2024"),

    # === F-layer: Encoding + retrieval + congruency forecasts (1 new tuple) ===
    _h3(_ENTROPY, "entropy", 24, 19, 0,
        "Context stability over 36s -- retrieval prediction",
        "Sachs 2025"),
)

assert len(_CDEM_H3_DEMANDS) == 18


class CDEM(Associator):
    """Context-Dependent Emotional Memory -- IMU Associator (depth 2, 10D).

    Models how emotional context modulates memory encoding, consolidation,
    and retrieval. Music heard in congruent emotional contexts produces
    stronger memories that are more easily reinstated.

    Sachs et al. 2025: same-valence emotional context shifts brain-state
    transitions 6.26s earlier (fMRI, N=39, z=3.6-4.32); tempoparietal
    regions track contextual emotion dynamics.

    Mitterschiffthaler et al. 2007: happy music -> ventral striatum + ACC;
    sad music -> R hippocampus/amygdala (fMRI, N=16, Z=3.25-4.96).

    Cheung et al. 2019: uncertainty x surprise jointly predict musical
    pleasure and amygdala/hippocampus activity (fMRI, N=40).

    Godden & Baddeley 1975: ~40% better recall in same context (N=18);
    context-dependent memory framework.

    Dependency chain:
        MEAMN (Depth 0, Relay) --> CDEM (Depth 2)

    Upstream reads:
        MEAMN: P0:memory_state [5], P1:emotional_color [6]

    Downstream feeds:
        F0:encoding_strength_fc -> F4 MEAMN (encoding modulation)
        F1:retrieval_context_fc -> F6 SRP (hedonic response)
        F2:mood_congruency_fc   -> F5 Emotion (emotional momentum)
    """

    NAME = "CDEM"
    FULL_NAME = "Context-Dependent Emotional Memory"
    UNIT = "IMU"
    FUNCTION = "F4"
    OUTPUT_DIM = 10
    UPSTREAM_READS = ("MEAMN",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec(
            "C", "Context-Dependent", 0, 2,
            ("C0:context_modulation", "C1:arousal_suppression"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 2, 4,
            ("M0:congruency_index", "M1:context_recall_probability"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 4, 7,
            ("P0:binding_state", "P1:arousal_gate",
             "P2:from_synthesis"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 7, 10,
            ("F0:encoding_strength_fc", "F1:retrieval_context_fc",
             "F2:mood_congruency_fc"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _CDEM_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "C0:context_modulation", "C1:arousal_suppression",
            "M0:congruency_index", "M1:context_recall_probability",
            "P0:binding_state", "P1:arousal_gate",
            "P2:from_synthesis",
            "F0:encoding_strength_fc", "F1:retrieval_context_fc",
            "F2:mood_congruency_fc",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Hippocampus -- context-dependent episodic encoding + binding
            RegionLink("P0:binding_state", "Hippocampus", 0.90,
                       "Borderie 2024"),
            # Amygdala -- emotional tagging modulated by context
            RegionLink("C1:arousal_suppression", "Amygdala", 0.85,
                       "Mitterschiffthaler 2007"),
            # ACC (BA32) -- context-music conflict monitoring
            RegionLink("C0:context_modulation", "ACC", 0.80,
                       "Sachs 2025"),
            # STG/STS -- tempoparietal emotion tracking
            RegionLink("P2:from_synthesis", "STG", 0.75,
                       "Sachs 2025"),
            # Ventral Striatum -- reward for emotionally congruent contexts
            RegionLink("P1:arousal_gate", "VS", 0.70,
                       "Mori & Zatorre 2024"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # CDEM is context-structural, no direct neuromodulator

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Sachs et al.", 2025,
                         "Emotions in the brain are dynamic and contextually "
                         "dependent; tempoparietal brain-state transitions "
                         "track emotional changes to music; same-valence "
                         "context shifts transitions 6.26s earlier",
                         "fMRI, N=39, z=3.6-4.32"),
                Citation("Mitterschiffthaler et al.", 2007,
                         "Happy music -> ventral striatum + ACC; sad music -> "
                         "R hippocampus/amygdala; valence-specific activation "
                         "of hippocampal-amygdalar complex",
                         "fMRI, N=16, Z=3.25-4.96"),
                Citation("Cheung et al.", 2019,
                         "Uncertainty x surprise jointly predict musical "
                         "pleasure and amygdala/hippocampus activity; "
                         "prediction error drives encoding",
                         "fMRI, N=40"),
                Citation("Godden & Baddeley", 1975,
                         "Context-dependent memory: ~40% better recall in "
                         "same context; encoding specificity principle",
                         "behavioral, N=18"),
                Citation("Billig et al.", 2022,
                         "Hippocampus binds auditory information with "
                         "spatiotemporal context via trisynaptic loop",
                         "review"),
                Citation("Borderie et al.", 2024,
                         "Theta-gamma CFC in hippocampus + STS supports "
                         "auditory memory retention",
                         "iEEG, epilepsy patients"),
                Citation("Mori & Zatorre", 2024,
                         "Pre-listening auditory-reward FC predicts chills "
                         "duration; state-dependent connectivity",
                         "fMRI, N=49, r=0.53"),
                Citation("Sakakibara et al.", 2025,
                         "Nostalgia Brain-Music Interface enhances nostalgic "
                         "feelings and memory vividness",
                         "EEG, N=33, Cohen's r=0.71-0.88"),
            ),
            evidence_tier="gamma",
            confidence_range=(0.55, 0.75),
            falsification_criteria=(
                "Context-dependent encoding (C0) must be stronger when "
                "music-mood is congruent vs incongruent (Sachs 2025: "
                "same-valence r=0.303 > across-context r=0.265, p=0.04)",
                "Arousal suppression (C1) must be weaker with competing "
                "contextual stimuli (Mitterschiffthaler 2007: music alone "
                "activates amygdala more than music-with-video)",
                "Context recall probability (M1) must be higher when "
                "encoding and retrieval contexts match (Godden & Baddeley "
                "1975: ~40% improvement in same-context recall)",
                "Congruency index (M0) must predict subsequent memory "
                "strength (Cheung 2019: uncertainty x surprise -> "
                "amygdala/hippocampus encoding)",
                "Binding state (P0) should correlate with hippocampal "
                "theta-gamma CFC during encoding (Borderie 2024: iEEG); "
                "if no coupling, binding claim is invalid",
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
        """Transform R3/H3 + upstream MEAMN into 10D context-dependent memory.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: ``{"MEAMN": (B, T, 12)}``

        Returns:
            ``(B, T, 10)`` -- C(2) + M(2) + P(3) + F(3)
        """
        c = compute_extraction(h3_features, r3_features)
        m = compute_temporal_integration(h3_features, r3_features, c)
        p = compute_cognitive_present(h3_features, r3_features, c, m)
        f = compute_forecast(h3_features, c, m, p)

        output = torch.stack(
            [c.c0, c.c1, *m, *p, *f], dim=-1,
        )
        return output.clamp(0.0, 1.0)
