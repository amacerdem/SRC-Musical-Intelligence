"""VMM -- Valence-Mode Mapping.

Relay nucleus (depth 0) in ARU, Function F5. Models the double dissociation
between happy (striatal reward) and sad (limbic-emotional) neural pathways.
Major/consonant/bright music activates VS/DS/ACC; minor/dissonant/dark
music activates hippocampus/amygdala/PHG. Mode detection requires
phrase-level context (2-3 chords minimum).

Dependency chain:
    VMM is a Relay (Depth 0) -- reads R3/H3 directly, no upstream dependencies.
    Runs in parallel with other depth-0 relays at Phase 0a.

R3 Ontology Mapping (v1 -> 97D freeze):
    roughness:              [0]  -> [0]    (A, roughness)
    sensory_pleasantness:   [4]  -> [4]    (A, sensory_pleasantness)
    warmth:                 [12] -> [12]   (C, warmth)
    tonalness:              [14] -> [14]   (C, brightness_kuttruff)
    spectral_smoothness:    [16] -> [16]   (C, spectral_smoothness)

Output structure: V+R(7) + P(3) + C(2) = 12D
  V+R layer [0:7]   Extraction           (sigmoid)    scope=internal
  P   layer [7:10]  Temporal Integration  (sigmoid)    scope=hybrid
  C   layer [10:12] Cognitive Present     (sigmoid)    scope=external

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/vmm/
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
from .temporal_integration import compute_temporal_integration

# -- Horizon labels ------------------------------------------------------------
_H_LABELS = {
    19: "3000ms (phrase)",
    22: "15000ms (section)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 19: "stability",
}

# -- Law labels ----------------------------------------------------------------
_L_LABELS = {2: "integration"}


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
_SENSORY_PLEASANTNESS = 4    # A group
_WARMTH = 12                 # C group
_TONALNESS = 14              # C group (brightness_kuttruff)
_SPECTRAL_SMOOTHNESS = 16    # C group


# -- 7 H3 Demand Specifications -----------------------------------------------
# Two horizons: H19(3s phrase) -> H22(15s section), all L2 (bidirectional)

_VMM_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === V+R layer: Consonance + Brightness + Warmth + Smoothness (6 tuples) ===
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 19, 0, 2,
        "Consonance state 3s — valence anchor",
        "Pallesen 2005"),
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 19, 1, 2,
        "Consonance mean 3s — mode detection baseline",
        "Khalfa 2005"),
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 19, 2, 2,
        "Harmonic ambiguity 3s — mode uncertainty",
        "Koelsch 2006"),
    _h3(_TONALNESS, "tonalness", 22, 0, 2,
        "Section brightness 15s — major/minor proxy",
        "Khalfa 2005"),
    _h3(_WARMTH, "warmth", 19, 0, 2,
        "Affective warmth 3s — sad pathway comfort",
        "Mitterschiffthaler 2007"),
    _h3(_SPECTRAL_SMOOTHNESS, "spectral_smoothness", 19, 0, 2,
        "Smoothness 3s — spectral regularity for mode",
        "Blood & Zatorre 2001"),

    # === C layer: Mode stability (1 tuple) ===
    _h3(_TONALNESS, "tonalness", 22, 19, 2,
        "Mode stability 15s — categorization confidence",
        "Khalfa 2005"),
)

assert len(_VMM_H3_DEMANDS) == 7


class VMM(Relay):
    """Valence-Mode Mapping -- ARU Relay (depth 0, 12D).

    Models the double dissociation between happy (striatal reward) and
    sad (limbic-emotional) neural pathways. Khalfa 2005: mode (major vs
    minor) x tempo interaction for emotional categorization (behavioral,
    N=20, d=1.2). Pallesen 2005: fMRI shows bilateral temporal/frontal
    cortex differentiates consonance-based valence (fMRI 3T, N=20,
    p<0.001 corrected).

    Dependency chain:
        VMM is a Relay (Depth 0) -- reads R3/H3 directly.
        No upstream mechanism dependencies.

    Downstream feeds:
        -> belief: emotional_valence (Core, tau=0.4)
        -> belief: perceived_happiness (Appraisal)
        -> CMAT (cross-modal affective transfer)
        -> TAR (therapeutic affective resonance)
        -> MAA (musical appreciation of atonality)
    """

    NAME = "VMM"
    FULL_NAME = "Valence-Mode Mapping"
    UNIT = "ARU"
    FUNCTION = "F5"
    OUTPUT_DIM = 12

    LAYERS = (
        LayerSpec(
            "V+R", "Extraction", 0, 7,
            ("V0:valence", "V1:mode_signal", "V2:consonance_valence",
             "R0:happy_pathway", "R1:sad_pathway",
             "R2:parahippocampal", "R3:reward_evaluation"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Temporal Integration", 7, 10,
            ("P0:perceived_happy", "P1:perceived_sad",
             "P2:emotion_certainty"),
            scope="hybrid",
        ),
        LayerSpec(
            "C", "Cognitive Present", 10, 12,
            ("C0:mode_detection_state", "C1:valence_state"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _VMM_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "V0:valence", "V1:mode_signal", "V2:consonance_valence",
            "R0:happy_pathway", "R1:sad_pathway",
            "R2:parahippocampal", "R3:reward_evaluation",
            "P0:perceived_happy", "P1:perceived_sad",
            "P2:emotion_certainty",
            "C0:mode_detection_state", "C1:valence_state",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # NAcc (Ventral Striatum) -- happy pathway reward
            RegionLink("R0:happy_pathway", "NAcc", 0.85,
                       "Green 2008"),
            # Caudate (Dorsal Striatum) -- happy pathway anticipation
            RegionLink("V0:valence", "Caudate", 0.80,
                       "Pallesen 2005"),
            # ACC / sgACC -- reward evaluation, nostalgia
            RegionLink("R3:reward_evaluation", "ACC", 0.80,
                       "Pereira 2011"),
            # Hippocampus -- sad pathway episodic
            RegionLink("R1:sad_pathway", "Hippocampus", 0.85,
                       "Mitterschiffthaler 2007"),
            # Amygdala -- sad pathway emotional tagging
            RegionLink("P1:perceived_sad", "Amygdala", 0.80,
                       "Mitterschiffthaler 2007"),
            # Parahippocampal Gyrus -- context processing both pathways
            RegionLink("R2:parahippocampal", "Parahippocampal Gyrus", 0.75,
                       "Blood & Zatorre 2001"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Khalfa", 2005,
                         "Mode x tempo interaction for emotional "
                         "categorization of music",
                         "behavioral, N=20"),
                Citation("Pallesen", 2005,
                         "Bilateral temporal/frontal cortex differentiates "
                         "consonance-based valence",
                         "fMRI 3T, N=20"),
                Citation("Green", 2008,
                         "Happy music selectively activates ventral "
                         "striatum; sad music activates limbic regions",
                         "fMRI, N=15"),
                Citation("Mitterschiffthaler", 2007,
                         "Sad music activates hippocampus, amygdala, "
                         "parahippocampal gyrus",
                         "fMRI 1.5T, N=16"),
                Citation("Koelsch", 2006,
                         "Consonance-dissonance activates different "
                         "neural networks for valence processing",
                         "fMRI, N=18"),
                Citation("Blood & Zatorre", 2001,
                         "PHG activation correlates with dissonance; "
                         "NAcc with pleasant music",
                         "PET, N=10"),
                Citation("Pereira", 2011,
                         "ACC integrates reward evaluation across "
                         "valence categories in music",
                         "fMRI, N=21"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.90, 0.95),
            falsification_criteria=(
                "Happy and sad music activate dissociable neural pathways "
                "(Green 2008: VS for happy, hippocampus for sad)",
                "Mode detection requires phrase-level temporal context "
                "(Khalfa 2005: mode x tempo interaction, d=1.2)",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Transform R3/H3 into 12D valence-mode representation.

        Delegates to 3 layer functions (extraction -> temporal_integration
        -> cognitive_present) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``

        Returns:
            ``(B, T, 12)`` -- V+R(7) + P(3) + C(2)
        """
        vr = compute_extraction(h3_features, r3_features)
        p = compute_temporal_integration(h3_features, r3_features, vr)
        c = compute_cognitive_present(h3_features, r3_features, vr, p)

        output = torch.stack([*vr, *p, *c], dim=-1)
        return output.clamp(0.0, 1.0)
