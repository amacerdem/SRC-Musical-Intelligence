"""HCMC -- Hippocampal-Cortical Memory Circuit.

Encoder nucleus (depth 1) in IMU, Function F4. Models hippocampal-cortical
interactions underlying episodic memory formation, consolidation, and
retrieval during music listening.

Reads: MEAMN.memory_state (intra-F4 dependency via relay_outputs)

R3 Ontology Mapping (post-freeze 97D):
    stumpf_fusion:     [3]      (A, tonal fusion)
    harmonicity:       [5]      (A, roughness_total)
    amplitude:         [7]      (A, velocity_A)
    loudness:          [10]     (B, velocity_D)
    onset_strength:    [11]     (B, event salience)
    tonalness:         [14]     (B, brightness_kuttruff)
    spectral_flux:     [21]     (D, spectral_flux)
    entropy:           [22]     (D, dynamic entropy)
    x_l0l5:            [25:33]  (F, energy x consonance)
    x_l5l7:            [41:49]  (H, consonance x timbre)

Output structure: E(3) + M(3) + P(3) + F(2) = 11D
  E-layer [0:3]  Extraction          (sigmoid)  scope=internal
  M-layer [3:6]  Temporal Integration (sigmoid/clamp)  scope=internal
  P-layer [6:9]  Cognitive Present   (sigmoid)  scope=hybrid
  F-layer [9:11] Forecast            (sigmoid)  scope=external

See Building/C3-Brain/F4-Memory-Systems/mechanisms/hcmc/
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
    16: "1000ms (beat)",
    20: "5000ms (phrase)",
    24: "36000ms (section)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    1: "mean", 2: "std", 5: "range", 13: "entropy",
    19: "stability", 22: "autocorrelation",
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


# -- R3 feature names (post-freeze 97D) ----------------------------------------
_STUMPF_FUSION = "stumpf_fusion"
_HARMONICITY = "harmonicity"
_AMPLITUDE = "amplitude"
_LOUDNESS = "loudness"
_ONSET_STRENGTH = "onset_strength"
_TONALNESS = "tonalness"
_SPECTRAL_FLUX = "spectral_flux"
_ENTROPY = "entropy"


# -- 22 H3 Demand Specifications -----------------------------------------------
# Hippocampal-cortical memory circuit requires binding stability (stumpf),
# event boundaries (flux, onset), harmonic templates (harmonicity, tonalness),
# pattern complexity (entropy), and energy dynamics (amplitude, loudness).

_HCMC_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-Layer: Extraction (12 tuples) ===
    _h3(3, _STUMPF_FUSION, 16, 1, 2,
        "Binding coherence at 1s -- CA3 autoassociative binding",
        "Rolls 2013"),
    _h3(3, _STUMPF_FUSION, 16, 2, 2,
        "Binding variability at 1s -- encoding uncertainty",
        "Cheung 2019"),
    _h3(21, _SPECTRAL_FLUX, 16, 1, 2,
        "Current segmentation rate -- event boundary detection",
        "Zacks 2007"),
    _h3(21, _SPECTRAL_FLUX, 16, 2, 2,
        "Flux variability at 1s -- boundary salience",
        "Zacks 2007"),
    _h3(11, _ONSET_STRENGTH, 16, 1, 2,
        "Event density at 1s -- encoding trigger rate",
        "Zacks 2007"),
    _h3(10, _LOUDNESS, 16, 1, 2,
        "Encoding salience at 1s -- arousal correlate",
        "Cheung 2019"),
    _h3(7, _AMPLITUDE, 16, 1, 2,
        "Energy level at 1s -- binding strength modulator",
        "Borderie 2024"),
    _h3(5, _HARMONICITY, 16, 1, 2,
        "Harmonic template at 1s -- pattern recognition cue",
        "Fernandez-Rubio 2022"),
    _h3(5, _HARMONICITY, 20, 1, 0,
        "Harmonic stability over 5s -- consolidation template",
        "Liu 2024"),
    _h3(14, _TONALNESS, 16, 1, 2,
        "Melodic content at 1s -- tonal encoding quality",
        "Fernandez-Rubio 2022"),
    _h3(14, _TONALNESS, 20, 22, 0,
        "Tonal repetition over 5s -- retrieval cue",
        "Biau 2025"),
    _h3(22, _ENTROPY, 16, 1, 2,
        "Current pattern complexity -- encoding difficulty",
        "Cheung 2019"),

    # === M-Layer: Temporal Integration (7 tuples) ===
    _h3(3, _STUMPF_FUSION, 20, 1, 0,
        "Binding stability over 5s -- consolidation window",
        "McClelland 1995"),
    _h3(3, _STUMPF_FUSION, 24, 19, 0,
        "Long-term binding stability 36s -- cortical transfer",
        "Buzsaki 2015"),
    _h3(22, _ENTROPY, 20, 13, 0,
        "Entropy of entropy over 5s -- pattern regularity",
        "McClelland 1995"),
    _h3(22, _ENTROPY, 24, 19, 0,
        "Pattern stability over 36s -- consolidation quality",
        "Squire 1995"),
    _h3(21, _SPECTRAL_FLUX, 20, 5, 0,
        "Flux dynamic range over 5s -- event rate context",
        "Squire 1995"),
    _h3(11, _ONSET_STRENGTH, 20, 5, 0,
        "Onset dynamic range over 5s -- encoding rate context",
        "Squire 1995"),
    _h3(10, _LOUDNESS, 20, 1, 0,
        "Average salience over 5s -- sustained encoding",
        "Liu 2024"),

    # === P-Layer: Cognitive Present (3 tuples) ===
    _h3(7, _AMPLITUDE, 20, 5, 0,
        "Energy dynamic range -- binding activation salience",
        "Fernandez-Rubio 2022"),
    _h3(10, _LOUDNESS, 24, 2, 0,
        "Salience variability over 36s -- storage quality",
        "Sikka 2015"),
    _h3(5, _HARMONICITY, 24, 22, 0,
        "Harmonic repetition detection -- storage template",
        "Billig 2022"),
)

assert len(_HCMC_H3_DEMANDS) == 22


class HCMC(Encoder):
    """Hippocampal-Cortical Memory Circuit -- IMU Encoder (depth 1, 11D).

    Models how the hippocampus and cortical networks (mPFC, PCC, entorhinal
    cortex) interact to support episodic memory formation, consolidation,
    and retrieval during music listening. The hippocampus rapidly binds
    incoming auditory features into episodic traces (CA3 autoassociation),
    segments experience at event boundaries, and consolidates stable patterns
    into cortical long-term storage via replay mechanisms.

    Rolls 2013: CA3 autoassociative network for fast pattern binding -- the
    hippocampus rapidly forms conjunctive representations of co-occurring
    features, enabling single-trial episodic encoding (computational model).

    Zacks et al. 2007: Event segmentation theory -- the hippocampus
    detects boundaries where musical structure changes, closing one episodic
    segment and opening another (behavioral + fMRI, N=multiple studies).

    Liu et al. 2024: Replay-triggered hippocampal-cortical transfer -- sharp
    wave ripple events during consolidation windows drive transfer of
    hippocampal traces to mPFC cortical networks (EEG-fMRI, N=33).

    Dependency chain:
        HCMC is an Encoder (Depth 1) -- reads MEAMN relay output.
        Computed after MEAMN relay in F4 pipeline.

    Downstream feeds:
        -> familiarity beliefs (binding_state, storage_state)
        -> salience mixer (segmentation_state)
        -> F8 Learning (consolidation_fc)
        -> F6 Reward / F5 Emotion (retrieval_fc)
    """

    NAME = "HCMC"
    FULL_NAME = "Hippocampal-Cortical Memory Circuit"
    UNIT = "IMU"
    FUNCTION = "F4"
    OUTPUT_DIM = 11
    UPSTREAM_READS = ("MEAMN",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("E0:fast_binding", "E1:episodic_segmentation",
             "E2:cortical_storage"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Temporal Integration", 3, 6,
            ("M0:consolidation_strength", "M1:encoding_rate",
             "M2:from_synthesis"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Cognitive Present", 6, 9,
            ("P0:binding_state", "P1:segmentation_state",
             "P2:storage_state"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 9, 11,
            ("F0:consolidation_fc", "F1:retrieval_fc"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _HCMC_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:fast_binding", "E1:episodic_segmentation",
            "E2:cortical_storage",
            "M0:consolidation_strength", "M1:encoding_rate",
            "M2:from_synthesis",
            "P0:binding_state", "P1:segmentation_state",
            "P2:storage_state",
            "F0:consolidation_fc", "F1:retrieval_fc",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Hippocampus (CA3) -- fast binding and episodic encoding hub
            RegionLink("E0:fast_binding", "Hippocampus", 0.85,
                       "Rolls 2013"),
            # Entorhinal Cortex -- sensory input gateway to hippocampus
            RegionLink("E1:episodic_segmentation", "Entorhinal Cortex", 0.75,
                       "Billig 2022"),
            # mPFC -- cortical storage target for consolidated memories
            RegionLink("P2:storage_state", "mPFC", 0.80,
                       "Liu 2024"),
            # PCC / Cingulate -- episodic recollection and binding state
            RegionLink("P0:binding_state", "PCC", 0.75,
                       "Fernandez-Rubio 2022"),
            # Hippocampus -- consolidation forecast source
            RegionLink("F0:consolidation_fc", "Hippocampus", 0.70,
                       "Buzsaki 2015"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # HCMC modulates memory via structural connectivity, no direct neuromodulator

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Rolls", 2013,
                         "CA3 autoassociative network for fast pattern "
                         "binding -- hippocampus rapidly forms conjunctive "
                         "representations enabling single-trial episodic "
                         "encoding",
                         "computational"),
                Citation("Zacks et al.", 2007,
                         "Event segmentation theory -- boundaries at "
                         "structural changes trigger hippocampal encoding "
                         "of new episodic segments",
                         "behavioral+fMRI"),
                Citation("Liu et al.", 2024,
                         "Replay-triggered hippocampal-cortical transfer -- "
                         "sharp wave ripple events drive transfer of "
                         "hippocampal traces to mPFC (N=33)",
                         "EEG-fMRI, N=33"),
                Citation("Cheung et al.", 2019,
                         "Hippocampal encoding of musical expectation "
                         "uncertainty (beta=-0.140, p=0.002, N=79)",
                         "fMRI, N=79"),
                Citation("Fernandez-Rubio et al.", 2022,
                         "Left hippocampus activated at 4th tone of "
                         "memorized tonal sequences (MCS p<0.001, N=71)",
                         "MEG, N=71"),
                Citation("Borderie et al.", 2024,
                         "Theta-gamma PAC for hippocampal auditory binding "
                         "-- intracranial evidence for binding mechanism",
                         "SEEG, intracranial"),
                Citation("Sikka et al.", 2015,
                         "Age-related hippocampal-to-cortical shift for "
                         "musical semantic memory (N=40)",
                         "fMRI, N=40"),
                Citation("Biau et al.", 2025,
                         "Theta reinstatement during memory recall "
                         "(N=23)",
                         "MEG, N=23"),
            ),
            evidence_tier="beta",
            confidence_range=(0.65, 0.85),
            falsification_criteria=(
                "Fast binding (E0) must increase for novel salient events "
                "vs repeated familiar passages (Cheung 2019: beta=-0.140)",
                "Episodic segmentation (E1) must peak at structural "
                "boundaries in music (Zacks 2007: event segmentation)",
                "Cortical storage (E2) must correlate with long-term "
                "retention in delayed recall tasks (Liu 2024: N=33)",
                "Consolidation strength (M0) must predict subsequent "
                "recognition memory accuracy (McClelland 1995)",
                "Retrieval forecast (F1) must predict actual recognition "
                "events above chance (Biau 2025: theta reinstatement)",
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
        """Transform R3/H3 + MEAMN relay output into 11D memory circuit.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{"MEAMN": (B, T, 12)}``

        Returns:
            ``(B, T, 11)`` -- E(3) + M(3) + P(3) + F(2)
        """
        e = compute_extraction(h3_features, r3_features)
        m = compute_temporal_integration(h3_features, r3_features, e)
        p = compute_cognitive_present(h3_features, e, m, relay_outputs)
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
