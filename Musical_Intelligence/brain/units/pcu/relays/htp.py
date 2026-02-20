"""HTP — Hierarchical Temporal Prediction.

Gold standard Relay nucleus for the Predictive Coding Unit (PCU).

Neural Circuit:
    Audio → Heschl's Gyrus (A1, low-level timing prediction, low-freq phase)
                ↓
              Planum Temporale (content prediction, high-gamma)
                ↓
              STG (mid-to-long integration, 200-500ms windows)
                ↓
              aIPL / LOTC (abstract, view-invariant prediction, ~500ms)
                ↓
              Hippocampus + ACC (sequence memory, prediction error)

Key Findings:
    - 500ms: abstract, 200ms: view-dependent, 110ms: low-level prediction
      (de Vries & Wurm 2023, MEG, N=22, ηp²=0.49, F(2)=19.9)
    - High-level predictions silence post-stimulus (explained away)
      (de Vries & Wurm 2023)
    - Auditory cortex integrates hierarchically 50-400ms
      (Norman-Haignere 2022, iEEG, N=7)
    - Feedforward auditory cortex→hippocampus; feedback in reverse
      (Bonetti 2024, MEG, N=83)
    - Intrinsic neural timescales follow core-periphery hierarchy
      (Golesorkhi 2021, MEG, N=89, d=-1.63, η²=0.86)
    - Two predictive mechanisms in A1: timing (low-freq phase) +
      content (high-gamma) (Forseth 2020, iEEG, N=37)

Temporal Architecture:
    - H0 (25ms):   Gamma — instantaneous sensory
    - H1 (50ms):   Gamma — short integration
    - H3 (100ms):  Alpha — low-level prediction (~110ms)
    - H4 (125ms):  Theta — mid-level prediction (~200ms)
    - H8 (500ms):  Delta — high-level prediction (~500ms)
    - H16 (1s):    Beat — long-term prediction context

R³ Remapping (Ontology Freeze v1.0.0):
    - Doc [9] "spectral_centroid" → Code [13] sharpness (proxy)
    - Doc [10] "spectral_flux"    → Code [21] spectral_flux
    - Doc [25] "x_l0l5"          → Code [42] beat_strength (dissolved)
    - Doc [33] "x_l4l5"          → Code [60] tonal_stability (dissolved)
    - Doc [41] "x_l5l7"          → Code [60] tonal_stability (dissolved)
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

# ======================================================================
# Scientific constants
# ======================================================================

# High-level prediction latency
# Source: de Vries & Wurm 2023, MEG, view-invariant prediction
LATENCY_HIGH: float = 500.0  # ms

# Mid-level prediction latency
# Source: de Vries & Wurm 2023, MEG, view-dependent prediction
LATENCY_MID: float = 200.0  # ms

# Low-level prediction latency
# Source: de Vries & Wurm 2023, MEG, optical flow/sensory
LATENCY_LOW: float = 110.0  # ms

# Hierarchy gradient (normalized)
HIERARCHY_GRADIENT: float = (LATENCY_HIGH - LATENCY_LOW) / LATENCY_HIGH  # 0.78


class HTP(Relay):
    """Hierarchical Temporal Prediction — PCU Relay (Depth 0, 12D).

    Models how predictive representations follow a hierarchical temporal
    pattern: high-level abstract features predicted ~500ms before input,
    mid-level ~200ms, low-level ~110ms. Post-stimulus, high-level
    representations are silenced (explained away) while low-level persist
    as prediction errors.

    Output Structure (12D):
        E-layer (4D) [0:4]:  High/mid/low level lead, hierarchy gradient
        M-layer (3D) [4:7]:  Latency high/mid/low (normalized)
        P-layer (3D) [7:10]: Sensory match, pitch prediction, abstract pred
        F-layer (2D) [10:12]: Abstract future, midlevel future
    """

    NAME = "HTP"
    FULL_NAME = "Hierarchical Temporal Prediction"
    UNIT = "PCU"

    OUTPUT_DIM = 12

    LAYERS = (
        LayerSpec(
            code="E", name="Extraction", start=0, end=4,
            dim_names=(
                "high_level_lead",       # Abstract prediction (~500ms)
                "mid_level_lead",        # Perceptual prediction (~200ms)
                "low_level_lead",        # Sensory prediction (~110ms)
                "hierarchy_gradient",    # Prediction gradient strength
            ),
            scope="internal",
        ),
        LayerSpec(
            code="M", name="Model", start=4, end=7,
            dim_names=(
                "latency_high",          # Normalized 500ms lead
                "latency_mid",           # Normalized 200ms lead
                "latency_low",           # Normalized 110ms lead
            ),
            scope="external",
        ),
        LayerSpec(
            code="P", name="Present", start=7, end=10,
            dim_names=(
                "sensory_match",         # Low-level prediction match
                "pitch_prediction",      # Mid-level pitch prediction
                "abstract_prediction",   # High-level abstract prediction
            ),
            scope="external",
        ),
        LayerSpec(
            code="F", name="Future", start=10, end=12,
            dim_names=(
                "abstract_future_500ms", # High cortical prediction
                "midlevel_future_200ms", # Intermediate area prediction
            ),
            scope="hybrid",
        ),
    )

    # R³ features (7)
    _R3_AMPLITUDE = 7
    _R3_SHARPNESS = 13             # Proxy for spectral_centroid
    _R3_SPECTRAL_FLUX = 21
    _R3_BEAT_STRENGTH = 42         # Replaces dissolved x_l0l5
    _R3_TONAL_STABILITY = 60       # Replaces dissolved x_l5l7 AND x_l4l5

    _VELOCITY_GAIN: float = 5.0
    _EPS: float = 1e-8

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        """18 temporal demands across hierarchical prediction timescales."""
        return (
            # --- Amplitude: low-level sensory ---
            H3DemandSpec(r3_idx=7, r3_name="amplitude",
                         horizon=0, horizon_label="25ms gamma",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Instantaneous amplitude — sensory level",
                         citation="Norman-Haignere et al. 2022"),
            H3DemandSpec(r3_idx=7, r3_name="amplitude",
                         horizon=3, horizon_label="100ms alpha",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Amplitude at alpha band — low-level prediction",
                         citation="Forseth et al. 2020"),
            H3DemandSpec(r3_idx=7, r3_name="amplitude",
                         horizon=3, horizon_label="100ms alpha",
                         morph=2, morph_name="std", law=2, law_name="integration",
                         purpose="Amplitude variability — prediction error proxy",
                         citation="de Vries & Wurm 2023"),
            # --- Spectral flux: onset/change detection ---
            H3DemandSpec(r3_idx=21, r3_name="spectral_flux",
                         horizon=0, horizon_label="25ms gamma",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Instantaneous onset — sensory detection",
                         citation="Forseth et al. 2020"),
            H3DemandSpec(r3_idx=21, r3_name="spectral_flux",
                         horizon=1, horizon_label="50ms gamma",
                         morph=1, morph_name="mean", law=2, law_name="integration",
                         purpose="Mean onset over 50ms — short integration",
                         citation="Norman-Haignere et al. 2022"),
            H3DemandSpec(r3_idx=21, r3_name="spectral_flux",
                         horizon=3, horizon_label="100ms alpha",
                         morph=14, morph_name="periodicity", law=2, law_name="integration",
                         purpose="Onset periodicity — low-level regularity",
                         citation="Sabat et al. 2025"),
            # --- Spectral flux: mid-level dynamics ---
            H3DemandSpec(r3_idx=21, r3_name="spectral_flux",
                         horizon=3, horizon_label="100ms alpha",
                         morph=8, morph_name="velocity", law=0, law_name="memory",
                         purpose="Spectral velocity — change rate prediction",
                         citation="de Vries & Wurm 2023"),
            H3DemandSpec(r3_idx=21, r3_name="spectral_flux",
                         horizon=4, horizon_label="125ms theta",
                         morph=0, morph_name="value", law=0, law_name="memory",
                         purpose="Change at theta band — mid-level boundary",
                         citation="Ye et al. 2025"),
            # --- Sharpness: mid-level pitch/brightness ---
            H3DemandSpec(r3_idx=13, r3_name="sharpness",
                         horizon=3, horizon_label="100ms alpha",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Pitch brightness — mid-level feature",
                         citation="Norman-Haignere et al. 2022"),
            H3DemandSpec(r3_idx=13, r3_name="sharpness",
                         horizon=4, horizon_label="125ms theta",
                         morph=8, morph_name="velocity", law=0, law_name="memory",
                         purpose="Pitch velocity — mid-level prediction",
                         citation="de Vries & Wurm 2023"),
            H3DemandSpec(r3_idx=13, r3_name="sharpness",
                         horizon=8, horizon_label="500ms delta",
                         morph=1, morph_name="mean", law=0, law_name="memory",
                         purpose="Mean pitch over 500ms — abstract context",
                         citation="Golesorkhi et al. 2021"),
            # --- Tonal stability: high-level abstraction ---
            H3DemandSpec(r3_idx=60, r3_name="tonal_stability",
                         horizon=8, horizon_label="500ms delta",
                         morph=0, morph_name="value", law=0, law_name="memory",
                         purpose="Tonal coupling — high-level (replaces x_l5l7)",
                         citation="Bonetti et al. 2024"),
            H3DemandSpec(r3_idx=60, r3_name="tonal_stability",
                         horizon=8, horizon_label="500ms delta",
                         morph=1, morph_name="mean", law=0, law_name="memory",
                         purpose="Mean tonal coupling — abstract template",
                         citation="Bonetti et al. 2024"),
            H3DemandSpec(r3_idx=60, r3_name="tonal_stability",
                         horizon=16, horizon_label="1s beat",
                         morph=1, morph_name="mean", law=0, law_name="memory",
                         purpose="Long-term tonal context — abstract prediction",
                         citation="Golesorkhi et al. 2021"),
            H3DemandSpec(r3_idx=60, r3_name="tonal_stability",
                         horizon=16, horizon_label="1s beat",
                         morph=20, morph_name="entropy", law=0, law_name="memory",
                         purpose="Tonal entropy — prediction uncertainty",
                         citation="Cheung 2019"),
            # --- Beat strength: low-level coupling ---
            H3DemandSpec(r3_idx=42, r3_name="beat_strength",
                         horizon=3, horizon_label="100ms alpha",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Low-level coupling (replaces x_l0l5)",
                         citation="Forseth et al. 2020"),
            H3DemandSpec(r3_idx=42, r3_name="beat_strength",
                         horizon=3, horizon_label="100ms alpha",
                         morph=2, morph_name="std", law=2, law_name="integration",
                         purpose="Coupling variability — prediction error",
                         citation="de Vries & Wurm 2023"),
            # --- Tonal stability: mid-level velocity ---
            H3DemandSpec(r3_idx=60, r3_name="tonal_stability",
                         horizon=4, horizon_label="125ms theta",
                         morph=8, morph_name="velocity", law=0, law_name="memory",
                         purpose="Tonal velocity — mid-level dynamics (replaces x_l4l5)",
                         citation="de Vries & Wurm 2023"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "high_level_lead", "mid_level_lead",
            "low_level_lead", "hierarchy_gradient",
            "latency_high", "latency_mid", "latency_low",
            "sensory_match", "pitch_prediction", "abstract_prediction",
            "abstract_future_500ms", "midlevel_future_200ms",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            RegionLink(dim_name="high_level_lead", region="aIPL",
                       weight=0.9, citation="de Vries & Wurm 2023"),
            RegionLink(dim_name="sensory_match", region="HG",
                       weight=0.9, citation="Forseth et al. 2020"),
            RegionLink(dim_name="pitch_prediction", region="PT",
                       weight=0.85, citation="Forseth et al. 2020"),
            RegionLink(dim_name="abstract_prediction", region="STG",
                       weight=0.8, citation="Norman-Haignere et al. 2022"),
            RegionLink(dim_name="hierarchy_gradient", region="Hippocampus",
                       weight=0.7, citation="Bonetti et al. 2024"),
            RegionLink(dim_name="abstract_future_500ms", region="ACC",
                       weight=0.6, citation="Bonetti et al. 2024"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            NeuroLink(dim_name="hierarchy_gradient", channel=1, effect="amplify",
                      weight=0.3, citation="de Vries & Wurm 2023"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("de Vries", 2023,
                         "Predictive representations follow hierarchical temporal "
                         "pattern: 500ms abstract, 200ms perceptual, 110ms sensory",
                         "MEG, N=22, ηp²=0.49, F(2)=19.9"),
                Citation("Norman-Haignere", 2022,
                         "Auditory cortex integrates hierarchically 50-400ms; "
                         "short = spectrotemporal, long = category-selective",
                         "iEEG, N=7 patients"),
                Citation("Bonetti", 2024,
                         "Feedforward auditory cortex→hippocampus/cingulate; "
                         "feedback in reverse; musical sequence recognition",
                         "MEG, N=83, p<0.001"),
                Citation("Golesorkhi", 2021,
                         "Intrinsic neural timescales follow core-periphery "
                         "hierarchy; core longer ACW than periphery",
                         "MEG, N=89, d=-1.63, η²=0.86"),
                Citation("Forseth", 2020,
                         "Two predictive mechanisms in A1: timing (low-freq phase) "
                         "and content (high-gamma)",
                         "iEEG, N=37, p<0.001"),
                Citation("Ye", 2025,
                         "3-level temporal hierarchy: clicks (10s ms), trains "
                         "(100s ms), higher-order (s); validated in primates",
                         "ECoG+EEG, primates+humans"),
                Citation("Sabat", 2025,
                         "Integration windows 15-150ms, fixed per neuron, increase "
                         "from primary to non-primary cortex",
                         "single-unit, ferrets"),
                Citation("Carbajal", 2018,
                         "SSA and MMN are micro/macro deviance detection; "
                         "hierarchical from subcortical to cortical",
                         "review, cellular"),
                Citation("Cheung", 2019,
                         "Uncertainty × surprise interaction in amygdala, "
                         "hippocampus, auditory cortex",
                         "ML+fMRI, N=39"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.88, 0.94),
            falsification_criteria=(
                "High-level predictions must precede low-level temporally "
                "(CONFIRMED: de Vries 2023)",
                "Post-stimulus high-level should be silenced "
                "(CONFIRMED: de Vries 2023)",
                "Novel stimuli should show delayed prediction timing "
                "(testable)",
                "Disrupting high-level areas should abolish 500ms predictions "
                "(testable via TMS)",
            ),
            version="3.0.0",
            paper_count=9,
        )

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Hierarchical temporal prediction: high→mid→low level.

        Args:
            h3_features: H³ dict {(r3_idx, h, m, l): (B, T)}.
            r3_features: (B, T, 97) R³ features.

        Returns:
            (B, T, 12) output.
        """
        B, T = r3_features.shape[:2]
        device = r3_features.device

        # R³ features (5)
        amplitude      = r3_features[:, :, self._R3_AMPLITUDE]
        sharpness      = r3_features[:, :, self._R3_SHARPNESS]
        flux           = r3_features[:, :, self._R3_SPECTRAL_FLUX]
        beat_strength  = r3_features[:, :, self._R3_BEAT_STRENGTH]
        tonal_stab     = r3_features[:, :, self._R3_TONAL_STABILITY]

        _zeros = torch.zeros(B, T, device=device)

        def _h3(key, fallback=None):
            v = h3_features.get(key)
            if v is not None:
                return v
            return fallback if fallback is not None else _zeros

        # H³ features (18 tuples)
        # Low-level (PPC)
        h3_amp_h0          = _h3((7, 0, 0, 2), amplitude)
        h3_amp_h3          = _h3((7, 3, 0, 2), amplitude)
        h3_amp_std_h3      = _h3((7, 3, 2, 2))
        h3_flux_h0         = _h3((21, 0, 0, 2), flux)
        h3_flux_mean_h1    = _h3((21, 1, 1, 2))
        h3_flux_per_h3     = _h3((21, 3, 14, 2))

        # Mid-level (TPC)
        h3_flux_vel_h3     = _h3((21, 3, 8, 0))
        h3_flux_h4         = _h3((21, 4, 0, 0))
        h3_sharp_h3        = _h3((13, 3, 0, 2), sharpness)
        h3_sharp_vel_h4    = _h3((13, 4, 8, 0))
        h3_sharp_mean_h8   = _h3((13, 8, 1, 0))

        # High-level (MEM)
        h3_tonal_h8        = _h3((60, 8, 0, 0), tonal_stab)
        h3_tonal_mean_h8   = _h3((60, 8, 1, 0))
        h3_tonal_mean_h16  = _h3((60, 16, 1, 0))
        h3_tonal_ent_h16   = _h3((60, 16, 20, 0))

        # Cross-level
        h3_beat_h3         = _h3((42, 3, 0, 2), beat_strength)
        h3_beat_std_h3     = _h3((42, 3, 2, 2))
        h3_tonal_vel_h4    = _h3((60, 4, 8, 0))

        # Velocity normalization
        sharp_vel = (h3_sharp_vel_h4 * self._VELOCITY_GAIN).abs().clamp(0.0, 1.0)
        tonal_vel = (h3_tonal_vel_h4 * self._VELOCITY_GAIN).abs().clamp(0.0, 1.0)

        # === E-LAYER (4D) — Hierarchical Prediction Leads ===

        # High-level: abstract prediction (~500ms lead)
        high_level_lead = (
            0.30 * h3_tonal_mean_h16          # long-term abstract template
            + 0.25 * h3_tonal_mean_h8         # abstract coupling 500ms
            + 0.25 * h3_tonal_h8              # current tonal coupling
            + 0.20 * (1.0 - h3_tonal_ent_h16) # low entropy = confident pred
        ).clamp(0.0, 1.0)

        # Mid-level: perceptual prediction (~200ms lead)
        mid_level_lead = (
            0.30 * h3_sharp_mean_h8           # mean pitch context
            + 0.25 * sharp_vel                # pitch velocity
            + 0.25 * tonal_vel                # tonal dynamics
            + 0.20 * h3_flux_h4              # spectral change at theta
        ).clamp(0.0, 1.0)

        # Low-level: sensory prediction (~110ms lead)
        low_level_lead = (
            0.30 * h3_flux_per_h3             # onset periodicity
            + 0.25 * h3_beat_h3              # coupling at alpha
            + 0.25 * h3_amp_h3              # amplitude context
            + 0.20 * h3_flux_mean_h1         # short-term onset mean
        ).clamp(0.0, 1.0)

        # Hierarchy gradient: how much high-level leads low-level
        hierarchy_gradient = (
            0.50 * (high_level_lead - low_level_lead + 0.5)
            + 0.25 * h3_tonal_mean_h16
            + 0.25 * (1.0 - h3_tonal_ent_h16)
        ).clamp(0.0, 1.0)

        # === M-LAYER (3D) — Normalized Latencies ===

        latency_high = (
            0.50 * high_level_lead
            + 0.50 * h3_tonal_mean_h8
        ).clamp(0.0, 1.0)

        latency_mid = (
            0.50 * mid_level_lead
            + 0.50 * h3_sharp_mean_h8
        ).clamp(0.0, 1.0)

        latency_low = (
            0.50 * low_level_lead
            + 0.50 * h3_amp_h3
        ).clamp(0.0, 1.0)

        # === P-LAYER (3D) — Present Processing ===

        # Sensory match: low-level prediction accuracy
        sensory_match = (
            0.40 * h3_amp_h3
            + 0.30 * (1.0 - h3_amp_std_h3)   # low variability = good match
            + 0.30 * h3_flux_per_h3
        ).clamp(0.0, 1.0)

        # Pitch prediction: mid-level pitch/brightness prediction
        pitch_prediction = (
            0.40 * h3_sharp_h3
            + 0.30 * h3_sharp_mean_h8
            + 0.30 * mid_level_lead
        ).clamp(0.0, 1.0)

        # Abstract prediction: high-level abstract template match
        abstract_prediction = (
            0.40 * h3_tonal_mean_h16
            + 0.30 * high_level_lead
            + 0.30 * (1.0 - h3_tonal_ent_h16)
        ).clamp(0.0, 1.0)

        # === F-LAYER (2D) — Future Predictions ===

        abstract_future = (
            0.50 * high_level_lead
            + 0.50 * h3_tonal_mean_h16
        ).clamp(0.0, 1.0)

        midlevel_future = (
            0.50 * mid_level_lead
            + 0.50 * sharp_vel
        ).clamp(0.0, 1.0)

        return torch.stack([
            high_level_lead, mid_level_lead,
            low_level_lead, hierarchy_gradient,
            latency_high, latency_mid, latency_low,
            sensory_match, pitch_prediction, abstract_prediction,
            abstract_future, midlevel_future,
        ], dim=-1)
