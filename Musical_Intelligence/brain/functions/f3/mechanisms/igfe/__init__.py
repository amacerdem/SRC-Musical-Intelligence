"""IGFE -- Individual Gamma Frequency Enhancement.

Associator nucleus (depth 2) in PCU, Function F3. Models how individual
differences in gamma-band oscillation frequency modulate cognitive
enhancement from transcranial alternating current stimulation (tACS).
When tACS frequency matches individual gamma frequency (IGF), memory
and executive functions are selectively enhanced via gamma synchronization
and dose-dependent accumulation.

SPECIAL: IGFE has NO M-layer. Structure is E(4) + P(3) + F(2) = 9D.

Core finding (Baltus et al. 2018): tACS at individual gamma frequency
(IGF) enhances auditory temporal resolution; mismatch degrades performance.
EEG phase-locking at IGF predicts enhancement magnitude (tACS+EEG, N=18).

Rufener et al. 2016: Gamma-band tACS improves phoneme categorization
when frequency matches IGF; dose-dependent accumulation over 20-minute
sessions with sustained cognitive benefits (tACS+behavioral, N=24).

Dependency chain:
    IGFE is an Associator (Depth 2) -- cross-unit reads from WMED (F2, PCU).
    WMED provides working-memory-entrainment context for gamma integration.

R3 Ontology Mapping (97D freeze):
    periodicity:        [5]   (A, roughness_total)
    amplitude:          [7]   (A, velocity_A)
    spectral_flux:      [10]  (B, onset_strength)
    tonalness:          [14]  (B, brightness_kuttruff)
    x_l0l5:             [25]  (F, coupling)
    x_l5l7:             [41]  (G, cognitive coupling)

Output structure: E(4) + P(3) + F(2) = 9D  [NO M-layer]
  E-layer [0:4]  Extraction    (sigmoid)  scope=internal
  P-layer [4:7]  Present       (sigmoid)  scope=hybrid
  F-layer [7:9]  Forecast      (sigmoid)  scope=external

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/igfe/
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

# -- Horizon labels ------------------------------------------------------------
_H_LABELS = {
    0: "25ms (gamma)",
    1: "50ms (gamma)",
    3: "100ms (alpha-beta)",
    8: "500ms (delta)",
    16: "1000ms (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 14: "periodicity", 18: "trend",
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
_PERIODICITY = 5              # roughness_total (A group)
_AMPLITUDE = 7                # velocity_A (A group)
_SPECTRAL_FLUX = 10           # onset_strength (B group)
_TONALNESS = 14               # brightness_kuttruff (B group)
_X_L0L5 = 25                  # x_l0l5 coupling (F group)
_X_L5L7 = 41                  # x_l5l7 cognitive coupling (G group)


# -- 11 H3 Demand Specifications ----------------------------------------------
# Fast gamma-range horizons (H0=25ms, H1=50ms) with L2 integration,
# plus cognitive coupling at longer scales (H8=500ms, H16=1s) with L0 memory.

_IGFE_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    _h3(5, "periodicity", 0, 0, 2,
        "Periodicity 25ms L2 — gamma-range match",
        "Baltus 2018"),
    _h3(5, "periodicity", 1, 0, 2,
        "Periodicity 50ms L2 — gamma tracking",
        "Baltus 2018"),
    _h3(41, "x_l5l7", 16, 1, 0,
        "Cognitive coupling mean 1s L0 — dose accumulation",
        "Rufener 2016"),
    _h3(41, "x_l5l7", 8, 0, 0,
        "Cognitive coupling value 500ms L0 — integration",
        "Rufener 2016"),
    _h3(41, "x_l5l7", 16, 18, 0,
        "Cognitive coupling trend 1s L0 — trajectory",
        "Rufener 2016"),
    _h3(7, "amplitude", 16, 1, 2,
        "Amplitude mean 1s — intensity context",
        "Baltus 2018"),
    _h3(25, "x_l0l5", 0, 0, 2,
        "Coupling 25ms L2 — fast binding",
        "Baltus 2018"),
    _h3(25, "x_l0l5", 1, 0, 2,
        "Coupling 50ms L2 — fast binding",
        "Baltus 2018"),
    _h3(25, "x_l0l5", 3, 14, 2,
        "Coupling periodicity 100ms — binding rhythm",
        "Rufener 2016"),
    _h3(25, "x_l0l5", 16, 14, 2,
        "Coupling periodicity 1s — sustained binding",
        "Rufener 2016"),
    _h3(10, "spectral_flux", 0, 0, 2,
        "Flux 25ms — gamma-range onset",
        "Baltus 2018"),
)

assert len(_IGFE_H3_DEMANDS) == 11


class IGFE(Associator):
    """Individual Gamma Frequency Enhancement -- PCU Associator (depth 2, 9D).

    Models how individual gamma-band oscillation frequency (IGF) modulates
    cognitive enhancement from tACS. When stimulation frequency matches
    IGF, gamma synchronization drives selective memory and executive
    enhancement via dose-dependent accumulation.

    SPECIAL: No M-layer -- structure is E(4) + P(3) + F(2) = 9D.

    Baltus et al. 2018: tACS at IGF enhances auditory temporal resolution;
    mismatch degrades performance; EEG phase-locking at IGF predicts
    enhancement magnitude (tACS+EEG, N=18).

    Rufener et al. 2016: Gamma-band tACS improves phoneme categorization
    when frequency matches IGF; dose-dependent accumulation over 20-minute
    sessions with sustained cognitive benefits (tACS+behavioral, N=24).

    Dependency chain:
        IGFE is an Associator (Depth 2) -- cross-unit reads from WMED (F2).
        WMED provides WM-entrainment context for gamma integration.

    Downstream feeds:
        -> gamma enhancement beliefs (Appraisal)
        -> cognitive modulation predictions (Anticipation)
    """

    NAME = "IGFE"
    FULL_NAME = "Individual Gamma Frequency Enhancement"
    UNIT = "PCU"
    FUNCTION = "F3"
    OUTPUT_DIM = 9
    UPSTREAM_READS = ()
    CROSS_UNIT_READS = ("WMED",)

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 4,
            ("E0:igf_match", "E1:memory_enhancement",
             "E2:executive_enhancement", "E3:dose_response"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 4, 7,
            ("P0:gamma_synchronization", "P1:dose_accumulation",
             "P2:memory_access"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 7, 9,
            ("F0:memory_enhancement_post", "F1:executive_improve_post"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _IGFE_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:igf_match", "E1:memory_enhancement",
            "E2:executive_enhancement", "E3:dose_response",
            "P0:gamma_synchronization", "P1:dose_accumulation",
            "P2:memory_access",
            "F0:memory_enhancement_post", "F1:executive_improve_post",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # A1/STG -- gamma-band auditory cortex entrainment
            RegionLink("E0:igf_match", "A1_STG", 0.80,
                       "Baltus 2018"),
            # HG -- Heschl's gyrus, primary auditory gamma processing
            RegionLink("P0:gamma_synchronization", "HG", 0.75,
                       "Baltus 2018"),
            # Hippocampus -- gamma-mediated memory enhancement
            RegionLink("E1:memory_enhancement", "hippocampus", 0.70,
                       "Rufener 2016"),
            # DLPFC -- executive function enhancement via gamma
            RegionLink("E2:executive_enhancement", "DLPFC", 0.70,
                       "Rufener 2016"),
            # Thalamus -- thalamocortical gamma relay
            RegionLink("E3:dose_response", "thalamus", 0.60,
                       "Baltus 2018"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # IGFE is gamma-oscillatory, no direct neuromodulator output

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Baltus et al.", 2018,
                         "tACS at individual gamma frequency (IGF) enhances "
                         "auditory temporal resolution; mismatch degrades "
                         "performance; EEG phase-locking at IGF predicts "
                         "enhancement magnitude",
                         "tACS+EEG, N=18"),
                Citation("Rufener et al.", 2016,
                         "Gamma-band tACS improves phoneme categorization "
                         "when frequency matches IGF; dose-dependent "
                         "accumulation over 20-minute sessions with "
                         "sustained cognitive benefits",
                         "tACS+behavioral, N=24"),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.70),
            falsification_criteria=(
                "IGF match (E0) must produce larger enhancement than "
                "mismatched frequencies (Baltus 2018: frequency-specific "
                "effect); if non-specific enhancement observed, IGF "
                "specificity claim is invalid",
                "Dose accumulation (P1) must increase over stimulation "
                "duration (Rufener 2016: 20-min dose-response); if "
                "enhancement is immediate and constant, dose-dependent "
                "mechanism is invalid",
                "Memory enhancement (E1) and executive enhancement (E2) "
                "must dissociate under selective gamma disruption; if both "
                "degrade identically, separate pathways are not supported",
                "Gamma synchronization (P0) must correlate with EEG "
                "phase-locking value at IGF (Baltus 2018); absence of "
                "PLV-behavior correlation invalidates synchronization model",
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
        """Transform R3/H3 into 9D gamma-enhancement representation.

        SPECIAL: No M-layer -- delegates to 3 layer functions
        (extraction -> cognitive_present -> forecast) and stacks E+P+F.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: ``{"WMED": (B, T, 11)}`` cross-unit data.

        Returns:
            ``(B, T, 9)`` -- E(4) + P(3) + F(2)
        """
        e = compute_extraction(h3_features)
        p = compute_cognitive_present(h3_features, e)
        f = compute_forecast(e, p)

        output = torch.stack([*e, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
