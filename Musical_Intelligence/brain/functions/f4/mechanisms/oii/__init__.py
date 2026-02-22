"""OII -- Oscillatory Intelligence Integration.

Encoder nucleus (depth 1) in IMU, Function F4. Models how oscillatory
integration-segregation dynamics support fluid intelligence in music
cognition. Theta/alpha oscillations bind distributed features (integration)
while gamma oscillations extract local detail (segregation). Efficient
switching between these modes characterises high fluid intelligence.

Reads: PMIM, PNH, HCMC, MSPBA, MEAMN (5 intra-unit connections)
       via relay_outputs with graceful fallback.

R3 Ontology Mapping (post-freeze 97D):
    roughness:              [0]      (A, roughness_total)
    stumpf_fusion:          [3]      (A, tonal fusion)
    sensory_pleasantness:   [4]      (A, pleasantness)
    periodicity:            [5]      (A, roughness proxy)
    amplitude:              [7]      (A, velocity_A)
    loudness:               [10]     (B, velocity_D)
    onset_strength:         [11]     (B, event salience)
    tonalness:              [14]     (C, brightness_kuttruff)
    spectral_centroid:      [15]     (C, spectral centroid)
    spectral_flux:          [21]     (D, spectral_flux)
    entropy:                [22]     (D, dynamic change)

Output structure: E(3) + M(2) + P(3) + F(2) = 10D
  E-layer [0:3]  Extraction           (sigmoid)  scope=internal
  M-layer [3:5]  Temporal Integration (sigmoid)  scope=internal
  P-layer [5:8]  Cognitive Present    (sigmoid)  scope=hybrid
  F-layer [8:10] Forecast             (sigmoid)  scope=external

See Building/C3-Brain/F4-Memory-Systems/mechanisms/oii/
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
    10: "400ms (chord)",
    14: "700ms (progression)",
    16: "1s (beat/WM)",
    18: "2s (phrase)",
    20: "5s (consolidation)",
    24: "36s (episodic)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 3: "std", 4: "max",
    8: "velocity", 14: "periodicity", 18: "trend", 19: "stability",
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


# -- R3 feature indices (post-freeze 97D) ------------------------------------
_ROUGHNESS = 0
_STUMPF_FUSION = 3
_SENSORY_PLEASANTNESS = 4
_PERIODICITY = 5
_AMPLITUDE = 7
_LOUDNESS = 10
_ONSET_STRENGTH = 11
_TONALNESS = 14
_SPECTRAL_CENTROID = 15
_SPECTRAL_FLUX = 21
_ENTROPY = 22


# -- 24 H3 Demand Specifications (25 entries, 1 duplicate) --------------------
# Oscillatory integration-segregation dynamics require multi-timescale
# features spanning chord (400ms), progression (700ms), beat (1s),
# phrase (2s), consolidation (5s), and episodic (36s) windows.

_OII_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-Layer: Extraction (6 tuples) ===
    _h3(_STUMPF_FUSION, "stumpf_fusion", 10, 1, 2,
        "Harmonic binding state at chord level (400ms)",
        "Bruzzone 2022"),
    _h3(_ONSET_STRENGTH, "onset_strength", 10, 0, 2,
        "Current gamma burst trigger at chord level",
        "Sturm 2014"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 10, 0, 2,
        "Current transition signal at chord level",
        "Samiee 2022"),
    _h3(_PERIODICITY, "periodicity", 10, 0, 2,
        "Current oscillatory regularity",
        "Bruzzone 2022"),
    _h3(_ENTROPY, "entropy", 10, 0, 2,
        "Current integration demand",
        "Fries 2015"),
    _h3(_SPECTRAL_CENTROID, "spectral_centroid", 10, 0, 2,
        "Frequency balance at chord level",
        "Bruzzone 2022"),

    # === M-Layer: Temporal Integration (4 tuples, 1 shared with F) ===
    _h3(_ONSET_STRENGTH, "onset_strength", 14, 8, 0,
        "Mode switching rate over 700ms progression",
        "Cabral 2022"),
    _h3(_ENTROPY, "entropy", 18, 19, 0,
        "Pattern stability over 2s phrase",
        "Cabral 2022"),
    _h3(_PERIODICITY, "periodicity", 14, 14, 0,
        "Meta-regularity: regularity of regularity",
        "Bruzzone 2022"),
    _h3(_STUMPF_FUSION, "stumpf_fusion", 14, 1, 0,
        "Binding quality over progression",
        "Bruzzone 2022"),

    # === P-Layer: Cognitive Present (7 tuples) ===
    _h3(_TONALNESS, "tonalness", 16, 0, 2,
        "Current harmonic integration at 1s",
        "Biau 2025"),
    _h3(_TONALNESS, "tonalness", 20, 1, 0,
        "Tonal stability over 5s consolidation",
        "Biau 2025"),
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 16, 0, 2,
        "Current encoding reward at 1s",
        "Borderie 2024"),
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 20, 18, 0,
        "Pleasantness trajectory over 5s",
        "Borderie 2024"),
    _h3(_ROUGHNESS, "roughness", 16, 0, 2,
        "Current gamma-band demand at 1s",
        "Dobri 2023"),
    _h3(_LOUDNESS, "loudness", 16, 0, 2,
        "Current oscillatory drive at 1s",
        "Yuan 2025"),
    _h3(_LOUDNESS, "loudness", 20, 1, 0,
        "Average drive over 5s consolidation",
        "Yuan 2025"),

    # === F-Layer: Forecast (7 tuples; onset_vel_h14 shared with M) ===
    _h3(_STUMPF_FUSION, "stumpf_fusion", 18, 1, 0,
        "Phrase-level binding stability for integration forecast",
        "Bruzzone 2022"),
    _h3(_ENTROPY, "entropy", 14, 1, 0,
        "Average complexity trajectory for segregation forecast",
        "Samiee 2022"),
    # (11, 14, 8, 0) already in M-layer -- shared, listed once
    _h3(_SPECTRAL_FLUX, "spectral_flux", 18, 1, 0,
        "Average transition rate for integration forecast",
        "Cabral 2022"),
    _h3(_SPECTRAL_CENTROID, "spectral_centroid", 18, 3, 0,
        "Frequency balance variability for mode prediction",
        "Bruzzone 2022"),
    _h3(_ROUGHNESS, "roughness", 24, 1, 0,
        "Average dissonance over 36s episodic chunk",
        "Samiee 2022"),
    _h3(_AMPLITUDE, "amplitude", 16, 8, 0,
        "Energy change rate for switch prediction",
        "Cabral 2022"),
    _h3(_AMPLITUDE, "amplitude", 20, 4, 0,
        "Peak energy over 5s consolidation",
        "Bruzzone 2022"),
)

assert len(_OII_H3_DEMANDS) == 24


class OII(Encoder):
    """Oscillatory Intelligence Integration -- IMU Encoder (depth 1, 10D).

    Models how oscillatory integration-segregation dynamics support fluid
    intelligence in music cognition.  Theta/alpha oscillations bind
    distributed features across frontal-temporal networks (integration),
    while gamma oscillations in auditory cortex extract fine-grained
    spectral detail (segregation).  Efficient switching between these modes
    is the hallmark of high fluid intelligence.

    Bruzzone et al. 2022: DTI + MEG N=66/67, high Gf individuals show
    stronger theta/alpha degree (p<0.001) AND higher gamma segregation --
    complementary activation, not simple integration dominance.

    Cabral et al. 2022: Computational model validated with MEG N=89,
    metastable oscillatory modes emerge from delay-coupled oscillators;
    global coupling strength controls mode switching speed and frequency.

    Samiee et al. 2022: MEG N=16, delta-beta PAC in rIFG F(1)=43.95,
    p<0.0001 -- cross-frequency coupling as mechanism for pitch processing
    mode coordination.

    Dependency chain:
        OII is an Encoder (Depth 1) -- reads PMIM, PNH, HCMC, MSPBA,
        MEAMN relay outputs.  Computed after Depth-0 relays + other
        Depth-1 encoders complete in F4 pipeline.

    Downstream feeds:
        -> oscillatory_state beliefs (Core)
        -> encoding_quality beliefs (Appraisal)
        -> mode_prediction for F4 integrators
    """

    NAME = "OII"
    FULL_NAME = "Oscillatory Intelligence Integration"
    UNIT = "IMU"
    FUNCTION = "F4"
    OUTPUT_DIM = 10
    UPSTREAM_READS = ("PMIM", "PNH", "HCMC", "MSPBA", "MEAMN")
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 3,
            ("E0:slow_integration", "E1:fast_segregation",
             "E2:mode_switching"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Temporal Integration", 3, 5,
            ("M0:gf_proxy", "M1:switching_efficiency"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Cognitive Present", 5, 8,
            ("P0:integration_state", "P1:segregation_state",
             "P2:encoding_quality"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 8, 10,
            ("F0:integration_pred", "F1:segregation_pred"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _OII_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:slow_integration", "E1:fast_segregation",
            "E2:mode_switching",
            "M0:gf_proxy", "M1:switching_efficiency",
            "P0:integration_state", "P1:segregation_state",
            "P2:encoding_quality",
            "F0:integration_pred", "F1:segregation_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # Frontal cortex -- theta/alpha integration hub, Gf proxy
            RegionLink("E0:slow_integration", "frontal_cortex", 0.80,
                       "Bruzzone 2022"),
            # Temporal cortex -- gamma segregation for spectral detail
            RegionLink("E1:fast_segregation", "temporal_cortex", 0.80,
                       "Sturm 2014"),
            # DLPFC -- mode switching coordination
            RegionLink("E2:mode_switching", "DLPFC", 0.85,
                       "Samiee 2022"),
            # Hippocampus -- theta-gamma PAC for encoding quality
            RegionLink("P2:encoding_quality", "hippocampus", 0.75,
                       "Borderie 2024"),
            # Auditory cortex -- gamma oscillation segregation state
            RegionLink("P1:segregation_state", "auditory_cortex", 0.70,
                       "Dobri 2023"),
            # Thalamus -- oscillatory relay for integration state
            RegionLink("P0:integration_state", "thalamus", 0.65,
                       "Biau 2025"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return ()  # OII models oscillatory dynamics, not direct neuromodulation

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Bruzzone et al.", 2022,
                         "DTI + MEG N=66/67, high Gf individuals show "
                         "stronger theta/alpha degree (p<0.001), lower "
                         "theta/alpha segregation; reversed pattern in "
                         "gamma (p<0.001). Gf group separation "
                         "t(55)=11.08, p<1e-7",
                         "DTI+MEG, N=66"),
                Citation("Cabral et al.", 2022,
                         "Computational model validated with MEG N=89; "
                         "metastable oscillatory modes emerge from "
                         "delay-coupled oscillators; global coupling "
                         "strength controls mode switching",
                         "computational+MEG, N=89"),
                Citation("Samiee et al.", 2022,
                         "MEG N=16, delta-beta PAC in rAud "
                         "(F(1)=11.1, p<0.001) and rIFG "
                         "(F(1)=43.95, p<0.0001); cross-frequency "
                         "coupling for pitch processing",
                         "MEG, N=16"),
                Citation("Sturm et al.", 2014,
                         "ECoG N=10, high gamma (70-170 Hz) reveals "
                         "distinct cortical representations for lyrics, "
                         "harmonic, and timbre features",
                         "ECoG, N=10"),
                Citation("Biau et al.", 2025,
                         "MEG N=23, neocortical and hippocampal theta "
                         "oscillations track audiovisual integration "
                         "and replay of speech memories; theta phase "
                         "determines LTP/LTD",
                         "MEG, N=23"),
                Citation("Borderie et al.", 2024,
                         "iEEG, theta-gamma PAC in STS, IFG, ITG, "
                         "hippocampus supports auditory STM; PAC "
                         "strength decodes correct vs incorrect trials",
                         "iEEG"),
                Citation("Dobri et al.", 2023,
                         "MEG, 40-Hz gamma ASSR increases in older age; "
                         "correlates with hearing loss and left auditory "
                         "cortex GABA; excessive gamma = detrimental",
                         "MEG"),
            ),
            evidence_tier="beta",
            confidence_range=(0.65, 0.80),
            falsification_criteria=(
                "Gf proxy (M0) must separate high-Gf vs low-Gf groups "
                "(Bruzzone 2022: t(55)=11.08, p<1e-7)",
                "Integration state (P0) must be higher for tonal than "
                "atonal stimuli (Biau 2025: theta tracks integration)",
                "Segregation state (P1) must increase with spectral "
                "complexity (Sturm 2014: gamma resolves local detail)",
                "Mode switching (E2) must be faster for musically "
                "trained participants (Cabral 2022: coupling parameter)",
                "Encoding quality (P2) must predict subsequent recall "
                "(Borderie 2024: PAC decodes correct trials)",
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
        """Transform R3/H3 + upstream relay outputs into 10D oscillatory state.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{"PMIM": ..., "PNH": ..., "HCMC": ...,
                              "MSPBA": ..., "MEAMN": ...}``

        Returns:
            ``(B, T, 10)`` -- E(3) + M(2) + P(3) + F(2)
        """
        e = compute_extraction(h3_features, r3_features, relay_outputs)
        m = compute_temporal_integration(h3_features, e)
        p = compute_cognitive_present(
            h3_features, r3_features, e, m, relay_outputs,
        )
        f = compute_forecast(
            h3_features, r3_features, e, p, relay_outputs,
        )

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
