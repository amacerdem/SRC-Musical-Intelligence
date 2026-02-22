"""DAED -- Dopamine Anticipation-Experience Dissociation.

Relay nucleus (depth 0) in RPU, Function F6. Models the temporal-anatomical
dissociation between anticipatory (caudate) and consummatory (NAcc) dopamine
release during music listening. Salimpoor (2011) demonstrated with PET
[11C]raclopride that caudate DA peaks 15-30s before emotional climax while
NAcc DA peaks at the moment of peak pleasure. DAED is the F6 relay: it
directly bridges R3/H3 features to C3 cognitive-level reward representations.

Dependency chain:
    DAED is a Relay (Depth 0) -- reads R3/H3 directly, no upstream dependencies.
    Runs in parallel with other depth-0 relays at Phase 0a.

R3 Ontology Mapping (v1 -> 97D freeze):
    roughness:              [0]  -> [0]    (A, roughness)
    sensory_pleasantness:   [4]  -> [4]    (A, sensory_pleasantness)
    amplitude:              [7]  -> [7]    (B, velocity_A)
    loudness:               [8]  -> [8]    (B, velocity_D)
    onset_strength:         [10] -> [10]   (B, onset_strength)
    spectral_change:        [21] -> [21]   (D, spectral_flux)
    energy_change:          [22] -> [22]   (D, distribution_entropy)
    x_l0l5:                 [25:33]        (F, coupling)

Output structure: E(4) + M(2) + P(2) = 8D
  E-layer [0:4]  Extraction          (sigmoid)    scope=internal
  M-layer [4:6]  Temporal Integration (mixed)     scope=internal
  P-layer [6:8]  Present             (sigmoid)    scope=hybrid

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/daed/
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
    3: "100ms (instantaneous)",
    4: "125ms (sub-beat)",
    8: "500ms (beat-fraction)",
    16: "1000ms (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 8: "velocity", 14: "periodicity", 20: "entropy",
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
# E-layer: 7 tuples, M-layer: 7 tuples, P-layer: 2 tuples

_DAED_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-layer: Dopaminergic extraction (tuples 0-6) ===

    # #0: Loudness velocity 1s -- anticipatory DA ramp
    _h3(8, "loudness", 16, 8, 0,
        "Loudness velocity over 1s -- anticipatory DA ramp",
        "Salimpoor 2011"),
    # #1: Spectral uncertainty 125ms -- prediction uncertainty
    _h3(21, "spectral_change", 4, 20, 0,
        "Spectral uncertainty at 125ms -- prediction uncertainty",
        "Salimpoor 2011"),
    # #2: Roughness velocity 500ms -- tension dynamics
    _h3(0, "roughness", 8, 8, 0,
        "Roughness velocity at 500ms -- tension dynamics",
        "Huron 2006"),
    # #3: Mean pleasantness 1s -- consummatory pleasure
    _h3(4, "sensory_pleasantness", 16, 1, 2,
        "Mean pleasantness over 1s -- consummatory pleasure",
        "Salimpoor 2011"),
    # #4: Mean loudness 1s -- intensity baseline
    _h3(8, "loudness", 16, 1, 2,
        "Mean loudness over 1s -- intensity baseline",
        "Salimpoor 2011"),
    # #5: Coupling entropy 1s -- wanting uncertainty
    _h3(25, "x_l0l5", 16, 20, 2,
        "Coupling entropy at 1s -- wanting uncertainty",
        "Berridge 2007"),
    # #6: Pleasantness 100ms -- immediate hedonic signal
    _h3(4, "sensory_pleasantness", 3, 0, 2,
        "Pleasantness at 100ms -- immediate hedonic signal",
        "Berridge 2007"),

    # === M-layer: Temporal context (tuples 7-13) ===

    # #7: Loudness at 100ms -- current intensity state
    _h3(8, "loudness", 3, 0, 2,
        "Loudness at 100ms -- current intensity state",
        "Salimpoor 2011"),
    # #8: Mean loudness 500ms -- medium-term context
    _h3(8, "loudness", 8, 1, 0,
        "Mean loudness over 500ms -- medium-term context",
        "Salimpoor 2011"),
    # #9: Amplitude at 500ms -- energy envelope
    _h3(7, "amplitude", 8, 0, 2,
        "Amplitude at 500ms -- energy envelope",
        "Salimpoor 2011"),
    # #10: Mean amplitude 1s -- sustained energy
    _h3(7, "amplitude", 16, 1, 2,
        "Mean amplitude over 1s -- sustained energy",
        "Salimpoor 2011"),
    # #11: Roughness at 100ms -- instantaneous tension
    _h3(0, "roughness", 3, 0, 2,
        "Roughness at 100ms -- instantaneous tension",
        "Huron 2006"),
    # #12: Onset at 125ms -- event detection
    _h3(10, "onset_strength", 4, 0, 2,
        "Onset at 125ms -- event detection",
        "Salimpoor 2011"),
    # #13: Peak periodicity 500ms -- rhythmic regularity
    _h3(10, "onset_strength", 8, 14, 2,
        "Peak periodicity at 500ms -- rhythmic regularity",
        "Mohebi 2024"),

    # === P-layer: Present state (tuples 14-15) ===

    # #14: Energy velocity 500ms -- dynamic build-up rate
    _h3(22, "energy_change", 8, 8, 0,
        "Energy velocity at 500ms -- dynamic build-up rate",
        "Salimpoor 2011"),
    # #15: Coupling at 500ms -- present cross-domain state
    _h3(25, "x_l0l5", 8, 0, 2,
        "Coupling at 500ms -- present cross-domain state",
        "Salimpoor 2013"),
)

assert len(_DAED_H3_DEMANDS) == 16


class DAED(Relay):
    """Dopamine Anticipation-Experience Dissociation -- RPU Relay (depth 0, 8D).

    Models the temporal-anatomical dissociation between anticipatory (caudate)
    and consummatory (NAcc) dopamine release during music listening.
    Salimpoor 2011: caudate DA increases 15-30s before peak (PET [11C]raclopride,
    N=8, r=0.71 caudate, r=0.84 NAcc). Berridge 2007: wanting (incentive
    salience, DA-dependent) vs liking (hedonic impact, opioid-dependent) are
    dissociable. Mohebi 2024: DA transients follow a ventral-to-dorsal striatal
    gradient corresponding to reward time horizons.

    Dependency chain:
        DAED is a Relay (Depth 0) -- reads R3/H3 directly.
        No upstream mechanism dependencies.

    Downstream feeds:
        -> wanting_index, liking_index for SRP (ARU) and kernel scheduler
        -> caudate_activation, nacc_activation for reward and salience computations
    """

    NAME = "DAED"
    FULL_NAME = "Dopamine Anticipation-Experience Dissociation"
    UNIT = "RPU"
    FUNCTION = "F6"
    OUTPUT_DIM = 8

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 4,
            ("f01:anticipatory_da", "f02:consummatory_da",
             "f03:wanting_index", "f04:liking_index"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Temporal Integration", 4, 6,
            ("dissociation_index", "temporal_phase"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 6, 8,
            ("caudate_activation", "nacc_activation"),
            scope="hybrid",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _DAED_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01:anticipatory_da", "f02:consummatory_da",
            "f03:wanting_index", "f04:liking_index",
            "dissociation_index", "temporal_phase",
            "caudate_activation", "nacc_activation",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Caudate (dorsal striatum) -- anticipatory DA ramp
            RegionLink("f01:anticipatory_da", "Caudate", 0.90,
                       "Salimpoor 2011"),
            # NAcc (ventral striatum) -- consummatory DA burst
            RegionLink("f02:consummatory_da", "NAcc", 0.90,
                       "Salimpoor 2011"),
            # Caudate -- wanting (incentive salience)
            RegionLink("f03:wanting_index", "Caudate", 0.85,
                       "Berridge 2007"),
            # NAcc -- liking (hedonic impact)
            RegionLink("f04:liking_index", "NAcc", 0.85,
                       "Berridge 2007"),
            # Caudate present-moment activation
            RegionLink("caudate_activation", "Caudate", 0.90,
                       "Salimpoor 2011"),
            # NAcc present-moment activation
            RegionLink("nacc_activation", "NAcc", 0.90,
                       "Salimpoor 2011"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            # Dopamine -- anticipatory DA ramp (caudate pathway)
            NeuroLink("f01:anticipatory_da", "Dopamine", 0.90,
                      "Salimpoor 2011"),
            # Dopamine -- consummatory DA burst (NAcc pathway)
            NeuroLink("f02:consummatory_da", "Dopamine", 0.90,
                      "Salimpoor 2011"),
            # Dopamine -- wanting (mesolimbic DA)
            NeuroLink("f03:wanting_index", "Dopamine", 0.85,
                      "Berridge 2007"),
            # Mu-opioid -- liking (hedonic impact)
            NeuroLink("f04:liking_index", "Mu-opioid", 0.80,
                      "Mallik 2017"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Salimpoor", 2011,
                         "Caudate DA ramps 15-30s before musical peak; "
                         "NAcc DA bursts at peak pleasure moment",
                         "PET [11C]raclopride, N=8, r=0.71/0.84"),
                Citation("Berridge", 2007,
                         "Wanting (incentive salience, DA-dependent) vs "
                         "liking (hedonic impact, opioid-dependent) are "
                         "dissociable components of reward",
                         "theoretical framework + rodent pharmacology"),
                Citation("Mohebi", 2024,
                         "DA transients follow a ventral-to-dorsal striatal "
                         "gradient corresponding to reward time horizons",
                         "fiber photometry, rodent striatum"),
                Citation("Salimpoor", 2013,
                         "STG-to-NAcc structural connectivity predicts "
                         "individual reward sensitivity to music",
                         "DTI + fMRI, N=19"),
                Citation("Mallik", 2017,
                         "Naltrexone blocks music-evoked pleasure; mu-opioid "
                         "system mediates hedonic impact",
                         "double-blind crossover, N=15"),
                Citation("Ferreri", 2019,
                         "Levodopa enhances and risperidone diminishes "
                         "music-evoked reward; pharmacological DA causal",
                         "double-blind RCT, N=27"),
                Citation("Huron", 2006,
                         "ITPRA theory: tension-prediction-reaction-appraisal "
                         "stages of musical expectation and reward",
                         "theoretical framework"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.85, 0.92),
            falsification_criteria=(
                "Music-evoked DA release shows temporal dissociation between "
                "caudate (anticipatory) and NAcc (consummatory) "
                "(Salimpoor 2011: PET DA binding r=0.71/0.84)",
                "Pharmacological blockade of DA (risperidone) eliminates "
                "anticipatory reward; opioid blockade (naltrexone) "
                "eliminates hedonic pleasure "
                "(Ferreri 2019, Mallik 2017)",
                "Wanting-liking dissociation requires intact mesolimbic "
                "DA for wanting and mu-opioid for liking "
                "(Berridge 2007)",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Transform R3/H3 into 8D dopaminergic dissociation representation.

        Delegates to 3 layer functions (extraction -> temporal_integration
        -> cognitive_present) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``

        Returns:
            ``(B, T, 8)`` -- E(4) + M(2) + P(2)
        """
        e = compute_extraction(h3_features, r3_features)
        m = compute_temporal_integration(h3_features, r3_features, e)
        p = compute_cognitive_present(h3_features, r3_features, e, m)

        output = torch.stack([*e, *m, *p], dim=-1)
        return output.clamp(0.0, 1.0)
