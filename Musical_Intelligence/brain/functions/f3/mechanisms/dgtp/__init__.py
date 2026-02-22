"""DGTP -- Domain-General Temporal Processing.

Associator nucleus (depth 2) in ASU, Function F3. Models the shared neural
infrastructure underlying temporal processing across auditory domains --
musical beat perception and speech timing rely on overlapping cortical and
subcortical circuits (SMA, putamen, cerebellum).

Reads: BARM (brainstem modulation), SNEM (entrainment/novelty)

R3 Ontology Mapping (post-freeze 97D):
    spectral_flux:      [10]     (B, onset_strength proxy)
    onset_strength:     [11]     (B, event salience)
    x_l0l5:             [25]     (F, sensorimotor coupling)

Output structure: E(3) + M(2) + P(2) + F(2) = 9D
  E-layer [0:3]  Extraction    (sigmoid)  scope=internal
  M-layer [3:5]  Memory        (sigmoid)  scope=internal
  P-layer [5:7]  Present       (sigmoid)  scope=hybrid
  F-layer [7:9]  Forecast      (sigmoid)  scope=external

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/dgtp/
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
    3: "100ms (alpha-beta)",
    13: "600ms",
    16: "1000ms (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 8: "velocity",
    11: "trend", 17: "peaks", 19: "stability",
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
_SPECTRAL_FLUX = 10       # spectral_flux / onset_strength proxy (B group)
_ONSET_STRENGTH = 11      # onset_strength (B group, event salience)
_X_L0L5 = 25             # sensorimotor coupling (F group)


# -- 9 H3 Demand Specifications -----------------------------------------------
# Domain-general timing: spectral flux (onset detection), onset strength
# (speech timing), and cross-band coupling (domain integration).

_DGTP_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    _h3(10, "spectral_flux", 3, 0, 2,
        "Flux value 100ms -- onset detection",
        "Grahn 2012"),
    _h3(10, "spectral_flux", 3, 17, 2,
        "Flux peaks 100ms -- event salience",
        "Grahn 2012"),
    _h3(10, "spectral_flux", 16, 17, 2,
        "Flux peaks 1s -- beat periodicity",
        "Tierney 2017"),
    _h3(11, "onset_strength", 13, 8, 0,
        "Onset velocity 600ms -- speech timing",
        "Tierney 2017"),
    _h3(11, "onset_strength", 13, 11, 0,
        "Onset trend 600ms -- speech trajectory",
        "Tierney 2017"),
    _h3(25, "x_l0l5", 16, 1, 0,
        "Coupling mean 1s L0 -- domain integration",
        "Patel 2011"),
    _h3(25, "x_l0l5", 16, 2, 0,
        "Coupling std 1s L0 -- integration variability",
        "Patel 2011"),
    _h3(25, "x_l0l5", 16, 19, 0,
        "Coupling stability 1s L0 -- timing stability",
        "Patel 2011"),
    _h3(25, "x_l0l5", 3, 17, 2,
        "Coupling peaks 100ms -- fast metric cue",
        "Grahn 2012"),
)

assert len(_DGTP_H3_DEMANDS) == 9


class DGTP(Associator):
    """Domain-General Temporal Processing -- ASU Associator (depth 2, 9D).

    Models shared neural mechanisms for temporal processing across music
    and speech domains. The OPERA hypothesis (Patel 2011) proposes that
    music training sharpens domain-general timing via shared subcortical
    circuits (SMA, putamen, cerebellum).

    Grahn & Rowe 2012: Beat perception recruits SMA and putamen (fMRI,
    N=20); rhythmic complexity modulates BG-cortical coupling.

    Tierney & Kraus 2017: Musicians show enhanced speech-in-noise
    perception linked to timing precision; beat synchronization ability
    predicts speech timing accuracy (behavioral+EEG, N=30).

    Patel 2011: OPERA hypothesis -- Overlap, Precision, Emotion,
    Repetition, Attention mediate music-to-language transfer through
    shared neural resources.

    Dependency chain:
        SNEM (Depth 0, Relay) + BARM (Depth 1, Encoder) --> DGTP (Depth 2)

    Upstream reads:
        BARM: P0:beat_alignment_accuracy [5]
        SNEM: P0:beat_locked_activity [6]

    Downstream feeds:
        -> domain_general_timing beliefs (Appraisal)
        -> cross-domain transfer assessments
    """

    NAME = "DGTP"
    FULL_NAME = "Domain-General Temporal Processing"
    UNIT = "ASU"
    FUNCTION = "F3"
    OUTPUT_DIM = 9
    UPSTREAM_READS = ("BARM", "SNEM")
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("E0:music_timing", "E1:speech_timing",
             "E2:shared_mechanism"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Memory", 3, 5,
            ("M0:domain_correlation", "M1:shared_variance"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 5, 7,
            ("P0:music_beat_perception", "P1:domain_general_timing"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 7, 9,
            ("F0:cross_domain_pred", "F1:training_transfer_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _DGTP_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:music_timing", "E1:speech_timing",
            "E2:shared_mechanism",
            "M0:domain_correlation", "M1:shared_variance",
            "P0:music_beat_perception", "P1:domain_general_timing",
            "F0:cross_domain_pred", "F1:training_transfer_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # SMA -- beat timing and motor preparation hub
            RegionLink("P0:music_beat_perception", "SMA", 0.85,
                       "Grahn 2012"),
            # Putamen -- beat-based timing in basal ganglia
            RegionLink("E0:music_timing", "putamen", 0.80,
                       "Grahn 2012"),
            # Cerebellum -- timing precision and error correction
            RegionLink("M0:domain_correlation", "CBLM", 0.75,
                       "Tierney 2017"),
            # AC -- auditory cortex temporal processing
            RegionLink("E1:speech_timing", "AC", 0.70,
                       "Tierney 2017"),
            # Premotor -- motor planning for timing
            RegionLink("P1:domain_general_timing", "premotor", 0.65,
                       "Grahn 2012"),
            # IFG -- domain-general sequencing and integration
            RegionLink("F0:cross_domain_pred", "IFG", 0.60,
                       "Patel 2011"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # DGTP is timing-structural, no direct neuromodulator

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Grahn & Rowe", 2012,
                         "Beat perception recruits SMA and putamen; rhythmic "
                         "complexity modulates BG-cortical coupling; beat-based "
                         "vs duration-based timing dissociation",
                         "fMRI, N=20"),
                Citation("Tierney & Kraus", 2017,
                         "Musicians show enhanced speech-in-noise perception "
                         "linked to timing precision; beat synchronization "
                         "ability predicts speech timing accuracy; domain-general "
                         "subcortical timing mechanism",
                         "behavioral+EEG, N=30"),
                Citation("Patel", 2011,
                         "OPERA hypothesis: Overlap, Precision, Emotion, "
                         "Repetition, Attention mediate music-to-language "
                         "transfer via shared neural resources; domain-general "
                         "timing framework",
                         "review"),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.70),
            falsification_criteria=(
                "Music timing (E0) and speech timing (E1) must share variance "
                "(E2 > 0.3 geometric mean) for the domain-general claim to "
                "hold (Patel 2011: OPERA overlap prediction)",
                "Beat synchronization accuracy must predict speech timing "
                "accuracy (Tierney 2017: r > 0.4, behavioral correlation)",
                "SMA/putamen lesion patients should show impaired timing in "
                "BOTH music and speech domains; if only one domain impaired, "
                "shared mechanism claim is invalid",
                "Training transfer (F1) must be bidirectional: music training "
                "improves speech timing AND speech training improves music "
                "timing (Patel 2011: OPERA predicts bidirectional transfer)",
                "Domain correlation (M0) should decrease when stimuli lack "
                "temporal structure (noise control); if M0 remains high for "
                "non-temporal stimuli, timing specificity is invalid",
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
        """Transform R3/H3 + BARM/SNEM upstream into 9D domain-general timing.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: ``{"BARM": (B, T, 10), "SNEM": (B, T, 12)}``

        Returns:
            ``(B, T, 9)`` -- E(3) + M(2) + P(2) + F(2)
        """
        e = compute_extraction(h3_features)
        m = compute_temporal_integration(h3_features, e)
        p = compute_cognitive_present(h3_features, e, m, upstream_outputs)
        f = compute_forecast(h3_features, e, m)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
