"""AAC -- Autonomic-Arousal Circuit.

Relay nucleus (depth 0) in ARU, Function F5. Models the autonomic nervous
system response to music. Five ANS markers (SCR, HR, RespR, BVP, Temp) are
integrated into a chills intensity composite and an ANS composite. The
co-activation paradox (SCR up + HR down at chills) places peak musical
emotion in Berntson's co-activation quadrant.

Dependency chain:
    AAC is a Relay (Depth 0) -- reads R3/H3 directly, no upstream dependencies.
    Runs in parallel with other depth-0 relays at Phase 0a.

R3 Ontology Mapping (v1 -> 97D freeze):
    amplitude:              [7]  -> [7]    (B, velocity_A)
    spectral_flux:          [10] -> [10]   (B, onset_strength)
    onset_strength:         [11] -> [11]   (B, onset_strength)
    spectral_flux:          [21] -> [21]   (D, spectral_flux)

Output structure: E+A(7) + I(2) + P(3) + F(2) = 14D
  E+A-layer [0:7]   Extraction    (sigmoid)    scope=internal
  I-layer   [7:9]   Integration   (sigmoid)    scope=internal
  P-layer   [9:12]  Present       (sigmoid)    scope=hybrid
  F-layer   [12:14] Forecast      (sigmoid)    scope=external

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/aac/
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
    7: "200ms (event)",
    9: "350ms (beat)",
    16: "1000ms (bar)",
    19: "3000ms (phrase)",
    20: "5000ms (section)",
    22: "15000ms (long)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    1: "mean", 4: "max", 8: "velocity", 11: "acceleration",
    14: "periodicity", 19: "stability", 22: "peaks",
}

# -- Law labels ----------------------------------------------------------------
_L_LABELS = {1: "forward", 2: "integration"}


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
_AMPLITUDE = 7               # B group (velocity_A)
_SPECTRAL_FLUX_B = 10        # B group (onset_strength)
_ONSET_STRENGTH = 11         # B group
_SPECTRAL_FLUX_D = 21        # D group


# -- 16 H3 Demand Specifications ----------------------------------------------
# Multi-scale: H9(350ms) -> H16(1s) -> H19(3s) -> H20(5s) -> H22(15s)

_AAC_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E+A-layer: Energy + ANS markers (10 tuples) ===
    # 1: Energy level 350ms — SCR correlate
    _h3(_AMPLITUDE, "amplitude", 9, 4, 2,
        "Energy level 350ms — SCR correlate",
        "Salimpoor 2009"),
    # 2: Energy change rate 350ms — ANS activation slope
    _h3(_AMPLITUDE, "amplitude", 9, 8, 2,
        "Energy change rate 350ms — ANS activation slope",
        "Craig 2002"),
    # 3: Onset acceleration 350ms — startle proxy
    _h3(_AMPLITUDE, "amplitude", 9, 11, 2,
        "Onset acceleration 350ms — startle proxy",
        "Grewe 2007"),
    # 4: Beat clarity 350ms — rhythmic entrainment
    _h3(_SPECTRAL_FLUX_B, "spectral_flux", 9, 14, 2,
        "Beat clarity 350ms — rhythmic entrainment",
        "Trost 2017"),
    # 5: Bar-level tempo 1s — sustained arousal
    _h3(_SPECTRAL_FLUX_B, "spectral_flux", 16, 14, 2,
        "Bar-level tempo 1s — sustained arousal",
        "Trost 2017"),
    # 6: Bar-level dynamics 1s — HR modulation
    _h3(_AMPLITUDE, "amplitude", 16, 8, 2,
        "Bar-level dynamics 1s — HR modulation",
        "Bernardi 2006"),
    # 7: Baseline ANS reference 3s — homeostatic anchor
    _h3(_AMPLITUDE, "amplitude", 19, 19, 2,
        "Baseline ANS reference 3s — homeostatic anchor",
        "Berntson 1991"),
    # 8: Homeostatic reference mean 3s — tonic level
    _h3(_AMPLITUDE, "amplitude", 19, 1, 2,
        "Homeostatic reference mean 3s — tonic level",
        "Berntson 1991"),
    # 9: Event density 350ms — SCR onset count
    _h3(_ONSET_STRENGTH, "onset_strength", 9, 22, 2,
        "Event density 350ms — SCR onset count",
        "Grewe 2007"),
    # 10: Timbral change density — BVP modulation
    _h3(_SPECTRAL_FLUX_D, "spectral_flux", 9, 8, 2,
        "Timbral change density — BVP modulation",
        "Trost 2017"),

    # === F-layer: Forward predictions (2 tuples) ===
    # 11: Future energy 5s — SCR prediction
    _h3(_AMPLITUDE, "amplitude", 20, 4, 1,
        "Future energy 5s — SCR prediction",
        "Salimpoor 2009"),
    # 12: Future energy 15s — HR prediction
    _h3(_AMPLITUDE, "amplitude", 22, 4, 1,
        "Future energy 15s — HR prediction",
        "Bernardi 2006"),

    # === P-layer reuses (4 tuples, same keys as E+A) ===
    # 13: Current energy 350ms (P-layer reuse of #1)
    _h3(_AMPLITUDE, "amplitude", 9, 4, 2,
        "Current energy 350ms — perceptual arousal",
        "Salimpoor 2009"),
    # 14: Periodicity H9 (P-layer reuse of #4)
    _h3(_SPECTRAL_FLUX_B, "spectral_flux", 9, 14, 2,
        "Periodicity H9 — driving rhythm signal",
        "Trost 2017"),
    # 15: Tempo signal H16 (P-layer reuse of #5)
    _h3(_SPECTRAL_FLUX_B, "spectral_flux", 16, 14, 2,
        "Tempo signal — bar-level arousal drive",
        "Trost 2017"),
    # 16: Energy accel (P-layer reuse of #3)
    _h3(_AMPLITUDE, "amplitude", 9, 11, 2,
        "Energy acceleration — intensity momentum",
        "Grewe 2007"),
)

assert len(_AAC_H3_DEMANDS) == 16


class AAC(Relay):
    """Autonomic-Arousal Circuit -- ARU Relay (depth 0, 14D).

    Models the autonomic nervous system response to music via five ANS
    markers (SCR, HR, RespR, BVP, Temp) integrated into chills intensity
    and ANS composite signals. Salimpoor 2009: chills coincide with DA
    release in caudate/NAcc (PET [11C]raclopride, N=8). Grewe 2007:
    77% of participants report chills during music (N=38). Trost 2017:
    arousal/valence map to distinct ANS profiles (SCR, HR, RespR).

    Dependency chain:
        AAC is a Relay (Depth 0) -- reads R3/H3 directly.
        No upstream mechanism dependencies.

    Downstream feeds:
        -> CLAM (closed-loop BCI modulation)
        -> CMAT (cross-modal affective transfer)
        -> MAD (musical anhedonia disconnection)
        -> F5 beliefs: chills_response (Appraisal)
    """

    NAME = "AAC"
    FULL_NAME = "Autonomic-Arousal Circuit"
    UNIT = "ARU"
    FUNCTION = "F5"
    OUTPUT_DIM = 14

    LAYERS = (
        LayerSpec(
            "E+A", "Extraction", 0, 7,
            ("E0:emotional_arousal", "E1:ans_response",
             "A0:scr", "A1:hr", "A2:respr", "A3:bvp", "A4:temp"),
            scope="internal",
        ),
        LayerSpec(
            "I", "Integration", 7, 9,
            ("I0:chills_intensity", "I1:ans_composite"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 9, 12,
            ("P0:current_intensity", "P1:driving_signal",
             "P2:perceptual_arousal"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 12, 14,
            ("F0:scr_pred_1s", "F1:hr_pred_2s"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _AAC_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:emotional_arousal", "E1:ans_response",
            "A0:scr", "A1:hr", "A2:respr", "A3:bvp", "A4:temp",
            "I0:chills_intensity", "I1:ans_composite",
            "P0:current_intensity", "P1:driving_signal",
            "P2:perceptual_arousal",
            "F0:scr_pred_1s", "F1:hr_pred_2s",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Amygdala -- arousal evaluation hub
            RegionLink("E0:emotional_arousal", "Amygdala", 0.85,
                       "Trost 2017"),
            # Anterior Insula -- interoceptive awareness
            RegionLink("I0:chills_intensity", "Anterior Insula", 0.80,
                       "Craig 2002"),
            # Hypothalamus -- autonomic efferent commands
            RegionLink("A0:scr", "Hypothalamus", 0.85,
                       "Bernardi 2006"),
            # LC / NE System -- sympathetic drive
            RegionLink("E1:ans_response", "LC/NE System", 0.75,
                       "Berntson 1991"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Salimpoor", 2009,
                         "Chills coincide with DA release in caudate/"
                         "NAcc during music listening",
                         "PET [11C]raclopride, N=8"),
                Citation("Grewe", 2007,
                         "77% of participants report chills; SCR peaks "
                         "at chill onset",
                         "behavioral + SCR, N=38"),
                Citation("Craig", 2002,
                         "Anterior insula maps interoceptive body "
                         "states to conscious feelings",
                         "review"),
                Citation("Trost", 2017,
                         "Arousal and valence map to distinct ANS "
                         "profiles (SCR, HR, RespR)",
                         "psychophysiology, N=40"),
                Citation("Bernardi", 2006,
                         "Tempo and loudness modulate HR and RespR; "
                         "crescendos increase HR, pauses activate PNS",
                         "cardiovascular, N=24"),
                Citation("Berntson", 1991,
                         "Autonomic space: SNS and PNS coactivation "
                         "during intense emotion",
                         "theoretical model"),
                Citation("Blood-Zatorre", 2001,
                         "Chills recruit paralimbic-brainstem-insular "
                         "circuitry; PET + HR + SCR",
                         "PET, N=10"),
                Citation("Koelsch", 2014,
                         "Neural correlates of music-evoked arousal: "
                         "amygdala and hypothalamus activation",
                         "fMRI, N=24"),
                Citation("Hodges", 2010,
                         "Psychophysiological measures of music affect: "
                         "SCR, HR, RespR, EMG converging",
                         "meta-review"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.90, 0.95),
            falsification_criteria=(
                "Musical chills require co-activation of SCR increase "
                "and HR deceleration (Berntson 1991 co-activation "
                "quadrant; Grewe 2007: SCR peak at chill onset)",
                "ANS response latency must be 1-5s post-acoustic "
                "trigger (Salimpoor 2009: DA release timing)",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Transform R3/H3 into 14D autonomic-arousal representation.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``

        Returns:
            ``(B, T, 14)`` -- E+A(7) + I(2) + P(3) + F(2)
        """
        ea = compute_extraction(h3_features, r3_features)
        i = compute_temporal_integration(h3_features, ea)
        p = compute_cognitive_present(h3_features, r3_features, ea, i)
        f = compute_forecast(h3_features, ea, i, p)

        output = torch.stack([*ea, *i, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
