"""ICEM — Information Content Emotion Model.

Relay nucleus (depth 0) in PCU, Function F2. Models how computational
Information Content (IC = -log₂(P(event|context))) peaks predict
psychophysiological emotional responses: high IC leads to increased
arousal/SCR, decreased HR/valence, and defense cascade activation.

Dependency chain:
    ICEM is a Relay (Depth 0) -- reads R3/H3 directly, no upstream dependencies.
    Conceptually downstream of HTP and SPH (ICEM maps prediction error
    magnitude to emotional responses), but computes independently from
    R3/H3 features.

R3 Ontology Mapping (old 49D -> 97D freeze):
    sensory_pleasantness:  [4]  -> [4]    (A, unchanged)
    loudness:              [8]  -> [10]   (B, shifted)
    onset_strength:        [10] -> [11]   (B, was spectral_flux, shifted+renamed)
    spectral_flux:         [21] -> [21]   (D, was spectral_change, renamed)
    distribution_entropy:  [22] -> [22]   (D, was energy_change, remapped)
    pitch_class_entropy:   [87] -> [38]   (F, was I:melodic_entropy, dissolved)
    pitch_salience:        [33] -> [39]   (F, replaces dissolved x_l4l5 arousal)
    key_clarity:           [75] -> [51]   (H, relocated from old v2 spec)
    tonal_stability:       [41] -> [60]   (H, replaces dissolved x_l5l7 valence)

Output structure: E(4) + M(5) + P(2) + F(2) = 13D
  E-layer [0:4]   Extraction    (sigmoid)  scope=internal
  M-layer [4:9]   Memory        (sigmoid)  scope=internal
  P-layer [9:11]  Present       (sigmoid)  scope=hybrid
  F-layer [11:13] Forecast      (sigmoid)  scope=external

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/icem/
See Docs/C3/Models/PCU-a3-ICEM/ICEM.md (original model specification)
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
    3: "100ms (alpha-beta)",
    4: "125ms (theta)",
    8: "500ms (delta)",
    16: "1000ms (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 8: "velocity", 13: "entropy",
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
_SENSORY_PLEAS = 4        # sensory_pleasantness (A group)
_LOUDNESS = 10            # loudness (B, was at old [8])
_ONSET = 11               # onset_strength (B, was spectral_flux at old [10])
_SPECTRAL_FLUX = 21       # spectral_flux (D, was spectral_change)
_DIST_ENTROPY = 22        # distribution_entropy (D, was energy_change)
_PITCH_CLASS_ENT = 38     # pitch_class_entropy (F, replaces I:melodic_entropy)
_PITCH_SALIENCE = 39      # pitch_salience (F, replaces x_l4l5 arousal pathway)
_KEY_CLARITY = 51         # key_clarity (H, relocated from old v2 [75])
_TONAL_STABILITY = 60     # tonal_stability (H, replaces x_l5l7 valence pathway)


# -- 18 H3 Demand Specifications -----------------------------------------------
# IC computation at fast timescales, emotional response at slower timescales

_ICEM_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === Spectral Flux / IC computation (3 tuples) ===
    _h3(_SPECTRAL_FLUX, "spectral_flux", 3, 0, 2,
        "Spectral change at 100ms — IC surprise signal",
        "Egermann 2013"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 3, 2, 2,
        "Spectral change variability at 100ms — IC magnitude",
        "Egermann 2013"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 3, 13, 2,
        "Spectral change entropy at 100ms — distributional surprise",
        "Cheung 2019"),

    # === Distribution Entropy (1 tuple) ===
    _h3(_DIST_ENTROPY, "distribution_entropy", 3, 8, 0,
        "Entropy velocity at 100ms — rate of distributional change",
        "Egermann 2013"),

    # === Onset Strength (2 tuples) ===
    _h3(_ONSET, "onset_strength", 3, 0, 2,
        "Onset at 100ms — event detection for arousal",
        "Egermann 2013"),
    _h3(_ONSET, "onset_strength", 8, 1, 0,
        "Mean onset over 500ms — sustained event context",
        "Salimpoor 2011"),

    # === Loudness (2 tuples) ===
    _h3(_LOUDNESS, "loudness", 3, 0, 2,
        "Loudness at 100ms — perceptual intensity for surprise",
        "Egermann 2013"),
    _h3(_LOUDNESS, "loudness", 16, 8, 2,
        "Loudness velocity over 1s — defense cascade trigger",
        "Egermann 2013"),

    # === Sensory Pleasantness / Consonance (2 tuples) ===
    _h3(_SENSORY_PLEAS, "sensory_pleasantness", 3, 0, 2,
        "Consonance at 100ms — valence positive contributor",
        "Cheung 2019"),
    _h3(_SENSORY_PLEAS, "sensory_pleasantness", 8, 2, 0,
        "Consonance variability over 500ms — HR modulation",
        "Egermann 2013"),

    # === Pitch Salience / replaces x_l4l5 arousal (2 tuples) ===
    _h3(_PITCH_SALIENCE, "pitch_salience", 4, 8, 0,
        "Pitch salience velocity at 125ms — arousal pathway (replaces x_l4l5)",
        "Egermann 2013"),
    _h3(_PITCH_SALIENCE, "pitch_salience", 16, 1, 2,
        "Mean pitch salience over 1s — sustained arousal context",
        "Gold 2019"),

    # === Tonal Stability / replaces x_l5l7 valence (3 tuples) ===
    _h3(_TONAL_STABILITY, "tonal_stability", 8, 0, 0,
        "Tonal stability at 500ms — emotional evaluation (replaces x_l5l7)",
        "Cheung 2019"),
    _h3(_TONAL_STABILITY, "tonal_stability", 16, 1, 0,
        "Mean tonal stability over 1s — valence pathway context",
        "Gold 2019"),
    _h3(_TONAL_STABILITY, "tonal_stability", 16, 13, 0,
        "Tonal stability entropy over 1s — uncertainty for IC",
        "Cheung 2019"),

    # === Key Clarity / tonal context (2 tuples) ===
    _h3(_KEY_CLARITY, "key_clarity", 3, 0, 2,
        "Key clarity at 100ms — tonal grounding for evaluation",
        "Cheung 2019"),
    _h3(_KEY_CLARITY, "key_clarity", 8, 1, 0,
        "Mean key clarity over 500ms — sustained tonal context",
        "Gold 2019"),

    # === Pitch Class Entropy / melodic IC proxy (1 tuple) ===
    _h3(_PITCH_CLASS_ENT, "pitch_class_entropy", 3, 0, 2,
        "Pitch class entropy at 100ms — melodic unpredictability",
        "Cheung 2019"),
)

assert len(_ICEM_H3_DEMANDS) == 18


class ICEM(Relay):
    """Information Content Emotion Model — PCU Relay (depth 0, 13D).

    Maps computational Information Content (IC) to emotional and
    psychophysiological responses. High IC (unexpected events) produces
    increased arousal/SCR, decreased HR/valence, and defense cascade
    activation. IC × entropy interaction determines pleasure (inverted-U).

    Egermann et al. 2013: IC peaks → arousal↑, valence↓, SCR↑, HR↓
    (p<0.001, N=50, live concert psychophysiology).
    Cheung et al. 2019: uncertainty × surprise → pleasure; amygdala,
    hippocampus, auditory cortex (fMRI, N=79, R²=0.654).
    Gold et al. 2019: inverted-U for IC on liking (p<0.001).
    Salimpoor et al. 2011: dopamine release caudate (anticipation) and
    NAc (peak pleasure) to music (PET/fMRI, N=8).

    Dependency chain:
        ICEM is a Relay (Depth 0) — reads R3/H3 directly.
        Conceptually extends HTP/SPH prediction to emotional responses.

    Downstream feeds:
        -> PWUP (IC for precision weighting)
        -> UDP (arousal for reward computation)
        -> ARU (emotional arousal, valence, defense cascade)
        -> information_content belief (Core)
        -> defense_cascade, arousal_scaling, valence_inversion (Appraisal)
        -> arousal_change_pred, valence_shift_pred (Anticipation)
    """

    NAME = "ICEM"
    FULL_NAME = "Information Content Emotion Model"
    UNIT = "PCU"
    FUNCTION = "F2"
    OUTPUT_DIM = 13

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 4,
            ("E0:information_content", "E1:arousal_response",
             "E2:valence_response", "E3:defense_cascade"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 4, 9,
            ("M0:ic_value", "M1:arousal_pred", "M2:valence_pred",
             "M3:scr_pred", "M4:hr_pred"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 9, 11,
            ("P0:surprise_signal", "P1:emotional_evaluation"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 11, 13,
            ("F0:arousal_change_1_3s", "F1:valence_shift_2_5s"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _ICEM_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:information_content", "E1:arousal_response",
            "E2:valence_response", "E3:defense_cascade",
            "M0:ic_value", "M1:arousal_pred", "M2:valence_pred",
            "M3:scr_pred", "M4:hr_pred",
            "P0:surprise_signal", "P1:emotional_evaluation",
            "F0:arousal_change_1_3s", "F1:valence_shift_2_5s",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Left Auditory Cortex — strongest uncertainty × surprise
            RegionLink("E0:information_content", "STG", 0.85,
                       "Cheung 2019"),
            # Amygdala/Hippocampus — joint uncertainty × surprise
            RegionLink("P0:surprise_signal", "AMYG", 0.80,
                       "Cheung 2019"),
            # NAc — peak pleasure dopamine / uncertainty encoding
            RegionLink("P1:emotional_evaluation", "NAC", 0.75,
                       "Salimpoor 2011"),
            # Caudate — anticipatory dopamine
            RegionLink("F0:arousal_change_1_3s", "CAUD", 0.70,
                       "Salimpoor 2011"),
            # vmPFC — precision weighting of prediction errors
            RegionLink("E3:defense_cascade", "VMPFC", 0.65,
                       "Harding 2025"),
            # OFC — reward processing during chills
            RegionLink("M1:arousal_pred", "OFC", 0.60,
                       "Chabin 2020"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # ICEM maps to emotional responses, no direct neuromodulator

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Egermann et al.", 2013,
                         "IC peaks (IDyOM) → arousal↑, valence↓, SCR↑, HR↓, "
                         "RespR↑; p<0.001; N=50 live concert",
                         "Psychophysiology, N=50"),
                Citation("Cheung et al.", 2019,
                         "Uncertainty × surprise → pleasure (saddle-shaped); "
                         "amygdala β=-0.140, L-AC β=-0.182, R²=0.654; "
                         "NAc reflects uncertainty only",
                         "fMRI + behavioral, N=79"),
                Citation("Gold et al.", 2019,
                         "Inverted-U for IC and entropy on liking; "
                         "IC × entropy interaction: prefer surprise under "
                         "low uncertainty; p<0.001",
                         "Behavioral (IDyOM), N=70"),
                Citation("Gold et al.", 2023,
                         "IC × entropy interaction in VS and R-STG; "
                         "VS reflects liked surprises during naturalistic music",
                         "fMRI, N=24"),
                Citation("Salimpoor et al.", 2011,
                         "Dopamine release: caudate during anticipation, "
                         "NAc during peak pleasure to music; PET p<0.05",
                         "PET + fMRI, N=8"),
                Citation("Harding et al.", 2025,
                         "Musical surprise → vmPFC decreased post-psilocybin; "
                         "escitalopram blunts hedonic surprise; "
                         "F(1,39)=7.07, p=0.011",
                         "fMRI RCT, N=41"),
                Citation("Chabin et al.", 2020,
                         "Musical chills: theta increase OFC, decrease rSTG/SMA; "
                         "p<0.05 source-level",
                         "HD-EEG 256-ch, N=18"),
                Citation("Bravo et al.", 2017,
                         "Ambiguous intervals → R Heschl's gyrus activation; "
                         "sensory precision under uncertainty; p<0.001 FWE",
                         "fMRI, N=20"),
                Citation("Mencke et al.", 2019,
                         "Atonal music: high uncertainty context → correct "
                         "predictions more rewarding; personality modulates",
                         "Theoretical review"),
                Citation("Teixeira Borges et al.", 2019,
                         "1/f scaling of neuronal activity in temporal cortex "
                         "linked to music pleasure; z=-2.50, r=0.33, p<0.005",
                         "EEG + ECG, N=28"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.90, 0.95),
            falsification_criteria=(
                "Altering IC should change emotional responses "
                "(testable via stimulus design)",
                "Beta-blockers should reduce SCR/HR effects "
                "(testable via pharmacology)",
                "Changing context should shift IC calculations "
                "(testable via priming)",
                "High IC must correlate with increased arousal "
                "(confirmed: Egermann 2013)",
                "High IC must correlate with decreased valence "
                "(confirmed: Egermann 2013)",
                "Pleasure depends on joint uncertainty and surprise "
                "(confirmed: Cheung 2019, Gold 2019, Gold 2023)",
                "Musical anticipation/pleasure must engage striatal dopamine "
                "(confirmed: Salimpoor 2011)",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Transform R3/H3 into 13D information content emotion mapping.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``

        Returns:
            ``(B, T, 13)`` — E(4) + M(5) + P(2) + F(2)
        """
        e = compute_extraction(h3_features)
        m = compute_temporal_integration(h3_features, e)
        p = compute_cognitive_present(h3_features, e, m)
        f = compute_forecast(h3_features, e)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
