"""MPG — Melodic Processing Gradient.

Gold standard Relay nucleus for the Novelty Detection Unit (NDU).

Neural Circuit:
    Audio → Cochlea → pmHG / medial A1 (onset pitch detection, posterior)
                        ↓
                      Anterolateral HG (complex pitch/contour, anterior)
                        ↓
                      Posterior STG (non-selective onset processing)
                        ↓
                      Anterior STG (dissonance-sensitive, contour tracking)
                        ↓
                      Planum Temporale / Polare (pitch → melody gradient)

Key Findings:
    - Posterior-to-anterior gradient in auditory cortex for melodic
      complexity: onset → pitch → contour → melody (Rupp et al. 2022, MEG)
    - Complex pitch processing 7.2mm more lateral (L), 7.9mm more
      anterior (R) than simple pitch (Briley et al. 2013, EEG, F=29.865)
    - Anterior STG selectively responds to dissonant stimuli
      (Foo et al. 2016, ECoG, y p=0.003, z p=0.006)
    - Pitch-sensitive voxels extend anterolateral from HG
      (Patterson et al. 2002, fMRI; Norman-Haignere et al. 2013)
    - Delta-beta PAC for melodic structure (Samiee et al. 2022, F=49.7)

Temporal Architecture:
    - H0, H3: Instantaneous onset detection (posterior pathway)
    - H3, H4: Short-term pitch/contour tracking (anterior pathway)
    - H16: Measure-level periodicity and structure

R³ Remapping (Ontology Freeze v1.0.0):
    - Doc [8] "loudness"      → Code [10] loudness
    - Doc [10] "spectral_flux" → Code [21] spectral_flux
    - Doc [13] "brightness"   → Code [13] sharpness (same index, renamed)
    - Doc [23] "pitch_change" → Code [23] distribution_flatness (semantic shift)
    - Doc [25] "x_l0l5"      → Code [42] beat_strength (dissolved)
    - Doc [33] "x_l4l5"      → Code [60] tonal_stability (dissolved)
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

# Posterior weighting — onset detection dominance
# Source: Rupp et al. 2022, posterior STG for onset; Potes 2012
ALPHA_POSTERIOR: float = 0.7

# Anterior weighting — contour/melody processing
# Source: Patterson et al. 2002, anterolateral extension for melody
BETA_ANTERIOR: float = 0.3

# Onset-to-sequence transition time constant
# Source: Rupp et al. 2022, posterior → anterior processing shift
TAU_TRANSITION: float = 0.3  # seconds

# Complex pitch spatial offset
# Source: Briley et al. 2013, F(1,28) = 29.865
# Complex pitch 7.2mm lateral (L), 7.9mm anterior (R) from simple
SPATIAL_OFFSET_MM: float = 7.5  # average L/R


class MPG(Relay):
    """Melodic Processing Gradient — NDU Relay (Depth 0, 10D).

    Models the posterior-to-anterior processing gradient in auditory
    cortex: onset detection (posterior) → pitch extraction → contour
    tracking → melody representation (anterior).

    Output Structure (10D):
        E-layer (4D) [0:4]:  Onset posterior, sequence anterior,
                              contour complexity, gradient ratio
        M-layer (3D) [4:7]:  Activity function, posterior/anterior levels
        P-layer (2D) [7:9]:  Onset state, contour state
        F-layer (1D) [9:10]: Phrase boundary prediction
    """

    NAME = "MPG"
    FULL_NAME = "Melodic Processing Gradient"
    UNIT = "NDU"

    OUTPUT_DIM = 10

    LAYERS = (
        LayerSpec(
            code="E", name="Extraction", start=0, end=4,
            dim_names=(
                "onset_posterior",       # Posterior onset detection
                "sequence_anterior",     # Anterior contour/sequence
                "contour_complexity",    # Melodic contour complexity
                "gradient_ratio",        # Posterior / (Posterior + Anterior)
            ),
            scope="internal",
        ),
        LayerSpec(
            code="M", name="Model", start=4, end=7,
            dim_names=(
                "activity_gradient",     # Overall cortical activity gradient
                "posterior_activity",    # Posterior processing strength
                "anterior_activity",    # Anterior processing strength
            ),
            scope="external",
        ),
        LayerSpec(
            code="P", name="Present", start=7, end=9,
            dim_names=(
                "onset_state",           # Current onset-locked activity
                "contour_state",         # Current contour tracking
            ),
            scope="external",
        ),
        LayerSpec(
            code="F", name="Future", start=9, end=10,
            dim_names=(
                "phrase_boundary_pred",  # Phrase boundary prediction
            ),
            scope="hybrid",
        ),
    )

    # R³ features (8)
    _R3_AMPLITUDE = 7
    _R3_LOUDNESS = 10
    _R3_ONSET_STRENGTH = 11
    _R3_SHARPNESS = 13             # Doc "brightness" = code "sharpness"
    _R3_SPECTRAL_FLUX = 21
    _R3_DISTRIBUTION_FLATNESS = 23  # Proxy for pitch change context
    _R3_BEAT_STRENGTH = 42         # Replaces dissolved x_l0l5
    _R3_TONAL_STABILITY = 60       # Replaces dissolved x_l4l5

    _VELOCITY_GAIN: float = 5.0
    _ENTROPY_SCALE: float = 3.0
    _EPS: float = 1e-8

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        """16 temporal demands for posterior-anterior gradient."""
        return (
            # --- Spectral flux: onset detection (posterior) ---
            H3DemandSpec(r3_idx=21, r3_name="spectral_flux",
                         horizon=0, horizon_label="5.8ms frame",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Instantaneous onset — posterior pathway",
                         citation="Rupp et al. 2022"),
            H3DemandSpec(r3_idx=21, r3_name="spectral_flux",
                         horizon=3, horizon_label="23ms onset",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Onset at note level — posterior",
                         citation="Potes et al. 2012"),
            H3DemandSpec(r3_idx=21, r3_name="spectral_flux",
                         horizon=3, horizon_label="23ms onset",
                         morph=1, morph_name="mean", law=2, law_name="integration",
                         purpose="Mean onset strength — posterior baseline",
                         citation="Rupp et al. 2022"),
            # --- Onset strength ---
            H3DemandSpec(r3_idx=11, r3_name="onset_strength",
                         horizon=0, horizon_label="5.8ms frame",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Onset marker instantaneous",
                         citation="Rupp et al. 2022"),
            H3DemandSpec(r3_idx=11, r3_name="onset_strength",
                         horizon=3, horizon_label="23ms onset",
                         morph=1, morph_name="mean", law=2, law_name="integration",
                         purpose="Mean onset strength at note level",
                         citation="Patterson et al. 2002"),
            H3DemandSpec(r3_idx=11, r3_name="onset_strength",
                         horizon=16, horizon_label="1s measure",
                         morph=14, morph_name="periodicity", law=2, law_name="integration",
                         purpose="Onset periodicity — rhythmic structure",
                         citation="Samiee et al. 2022"),
            # --- Sharpness: pitch brightness (anterior pathway) ---
            H3DemandSpec(r3_idx=13, r3_name="sharpness",
                         horizon=3, horizon_label="23ms onset",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Pitch brightness at onset — anterior input",
                         citation="Briley et al. 2013"),
            H3DemandSpec(r3_idx=13, r3_name="sharpness",
                         horizon=3, horizon_label="23ms onset",
                         morph=2, morph_name="std", law=2, law_name="integration",
                         purpose="Brightness variability — contour complexity",
                         citation="Norman-Haignere et al. 2013"),
            H3DemandSpec(r3_idx=13, r3_name="sharpness",
                         horizon=4, horizon_label="35ms onset",
                         morph=8, morph_name="velocity", law=0, law_name="memory",
                         purpose="Pitch velocity — contour direction",
                         citation="Rupp et al. 2022"),
            # --- Distribution flatness: pitch change proxy ---
            H3DemandSpec(r3_idx=23, r3_name="distribution_flatness",
                         horizon=3, horizon_label="23ms onset",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Spectral flatness — pitch change context",
                         citation="Foo et al. 2016"),
            H3DemandSpec(r3_idx=23, r3_name="distribution_flatness",
                         horizon=4, horizon_label="35ms onset",
                         morph=20, morph_name="entropy", law=2, law_name="integration",
                         purpose="Contour entropy — melodic complexity",
                         citation="Cheung et al. 2019"),
            H3DemandSpec(r3_idx=23, r3_name="distribution_flatness",
                         horizon=16, horizon_label="1s measure",
                         morph=1, morph_name="mean", law=2, law_name="integration",
                         purpose="Mean pitch change at measure level",
                         citation="Patterson et al. 2002"),
            # --- Amplitude: event energy ---
            H3DemandSpec(r3_idx=7, r3_name="amplitude",
                         horizon=3, horizon_label="23ms onset",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Onset amplitude — event salience",
                         citation="Rupp et al. 2022"),
            # --- Beat strength: replaces dissolved x_l0l5 ---
            H3DemandSpec(r3_idx=42, r3_name="beat_strength",
                         horizon=3, horizon_label="23ms onset",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Onset-beat coupling (replaces x_l0l5)",
                         citation="Samiee et al. 2022"),
            H3DemandSpec(r3_idx=42, r3_name="beat_strength",
                         horizon=3, horizon_label="23ms onset",
                         morph=14, morph_name="periodicity", law=2, law_name="integration",
                         purpose="Beat periodicity at onset level",
                         citation="Samiee et al. 2022"),
            # --- Tonal stability: replaces dissolved x_l4l5 ---
            H3DemandSpec(r3_idx=60, r3_name="tonal_stability",
                         horizon=3, horizon_label="23ms onset",
                         morph=8, morph_name="velocity", law=0, law_name="memory",
                         purpose="Tonal velocity — harmonic contour (replaces x_l4l5)",
                         citation="Foo et al. 2016"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "onset_posterior", "sequence_anterior",
            "contour_complexity", "gradient_ratio",
            "activity_gradient", "posterior_activity", "anterior_activity",
            "onset_state", "contour_state",
            "phrase_boundary_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            RegionLink(dim_name="onset_posterior", region="Medial_HG",
                       weight=0.9, citation="Rupp et al. 2022"),
            RegionLink(dim_name="posterior_activity", region="STG_posterior",
                       weight=0.8, citation="Potes et al. 2012"),
            RegionLink(dim_name="sequence_anterior", region="Anterolateral_HG",
                       weight=0.85, citation="Patterson et al. 2002"),
            RegionLink(dim_name="anterior_activity", region="STG_anterior",
                       weight=0.8, citation="Foo et al. 2016"),
            RegionLink(dim_name="contour_complexity", region="Planum_Polare",
                       weight=0.7, citation="Norman-Haignere et al. 2013"),
            RegionLink(dim_name="onset_state", region="Planum_Temporale",
                       weight=0.6, citation="Briley et al. 2013"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            NeuroLink(dim_name="contour_complexity", channel=1, effect="amplify",
                      weight=0.3, citation="Cheung et al. 2019"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Rupp", 2022,
                         "MEG posterior-to-anterior gradient for melodic "
                         "complexity in auditory cortex",
                         "MEG, posterior→anterior gradient"),
                Citation("Patterson", 2002,
                         "fMRI pitch/melody processing extends anterolateral "
                         "from HG; melody > pitch > noise gradient",
                         "fMRI, anterolateral extension"),
                Citation("Norman-Haignere", 2013,
                         "fMRI pitch-sensitive voxels in anterior auditory "
                         "cortex; tonotopic vs pitch-sensitive dissociation",
                         "fMRI, pitch voxels"),
                Citation("Briley", 2013,
                         "EEG complex pitch processing: 7.2mm lateral (L), "
                         "7.9mm anterior (R); F(1,28)=29.865",
                         "F=29.865, EEG, 7-8mm shift"),
                Citation("Foo", 2016,
                         "ECoG anterior STG dissonance-selective; posterior "
                         "non-selective; y p=0.003, z p=0.006",
                         "ECoG, anterior p=0.003"),
                Citation("Samiee", 2022,
                         "Delta-beta phase-amplitude coupling for melodic "
                         "structure processing; F(1)=49.7",
                         "MEG/EEG, F=49.7, delta-beta PAC"),
                Citation("Zatorre", 2022,
                         "Review: right auditory cortex pitch specialization; "
                         "lateralization of spectral vs temporal processing",
                         "review, right AC pitch"),
                Citation("Cheung", 2019,
                         "Auditory cortex tracks surprise (β=-0.182, p=0.00012); "
                         "uncertainty × surprise interaction in amygdala/HPC",
                         "fMRI, N=39, AC surprise"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.85, 0.92),
            falsification_criteria=(
                "Single notes should activate posterior regions only — no "
                "anterior extension without contour",
                "Complex melodies should show stronger anterior activation "
                "(CONFIRMED: Rupp 2022)",
                "Fixed-pitch sequences should show reduced anterior activity "
                "(CONFIRMED: Rupp 2022, Patterson 2002)",
                "Posterior lesions should cause onset detection deficit",
                "Anterior lesions should impair contour processing while "
                "preserving onset detection",
            ),
            version="3.0.0",
            paper_count=8,
        )

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Posterior-anterior melodic processing gradient.

        Args:
            h3_features: H³ dict {(r3_idx, h, m, l): (B, T)}.
            r3_features: (B, T, 97) R³ features.

        Returns:
            (B, T, 10) output.
        """
        B, T = r3_features.shape[:2]
        device = r3_features.device

        # R³ (8)
        amplitude      = r3_features[:, :, self._R3_AMPLITUDE]
        loudness       = r3_features[:, :, self._R3_LOUDNESS]
        onset_strength = r3_features[:, :, self._R3_ONSET_STRENGTH]
        sharpness      = r3_features[:, :, self._R3_SHARPNESS]
        spectral_flux  = r3_features[:, :, self._R3_SPECTRAL_FLUX]
        dist_flat      = r3_features[:, :, self._R3_DISTRIBUTION_FLATNESS]
        beat_strength  = r3_features[:, :, self._R3_BEAT_STRENGTH]
        tonal_stab     = r3_features[:, :, self._R3_TONAL_STABILITY]

        _zeros = torch.zeros(B, T, device=device)

        def _h3(key, fallback=None):
            v = h3_features.get(key)
            if v is not None:
                return v
            return fallback if fallback is not None else _zeros

        # H³ (16 tuples)
        h3_flux_h0        = _h3((21, 0, 0, 2), spectral_flux)
        h3_flux_h3        = _h3((21, 3, 0, 2), spectral_flux)
        h3_flux_mean_h3   = _h3((21, 3, 1, 2))
        h3_onset_h0       = _h3((11, 0, 0, 2), onset_strength)
        h3_onset_mean_h3  = _h3((11, 3, 1, 2))
        h3_onset_per_h16  = _h3((11, 16, 14, 2))
        h3_sharp_h3       = _h3((13, 3, 0, 2), sharpness)
        h3_sharp_std_h3   = _h3((13, 3, 2, 2))
        h3_sharp_vel_h4   = _h3((13, 4, 8, 0))
        h3_flat_h3        = _h3((23, 3, 0, 2), dist_flat)
        h3_flat_ent_h4    = _h3((23, 4, 20, 2))
        h3_flat_mean_h16  = _h3((23, 16, 1, 2))
        h3_amp_h3         = _h3((7, 3, 0, 2), amplitude)
        h3_beat_h3        = _h3((42, 3, 0, 2), beat_strength)
        h3_beat_per_h3    = _h3((42, 3, 14, 2))
        h3_tonal_vel_h3   = _h3((60, 3, 8, 0))

        # Velocity/entropy normalization
        sharp_vel = (h3_sharp_vel_h4 * self._VELOCITY_GAIN).abs().clamp(0.0, 1.0)
        tonal_vel = (h3_tonal_vel_h3 * self._VELOCITY_GAIN).abs().clamp(0.0, 1.0)
        contour_ent = (h3_flat_ent_h4 / self._ENTROPY_SCALE).clamp(0.0, 1.0)

        # === E-LAYER (4D) ===

        # Onset posterior: onset detection strength (posterior pathway)
        onset_posterior = (
            0.25 * h3_onset_h0
            + 0.25 * h3_flux_h0
            + 0.20 * h3_flux_h3
            + 0.15 * h3_onset_mean_h3
            + 0.15 * h3_amp_h3
        ).clamp(0.0, 1.0)

        # Sequence anterior: contour/pitch tracking (anterior pathway)
        sequence_anterior = (
            0.25 * sharp_vel                    # pitch direction
            + 0.25 * contour_ent                # contour entropy
            + 0.20 * h3_sharp_std_h3            # brightness variability
            + 0.15 * tonal_vel                  # harmonic contour
            + 0.15 * h3_flat_h3                 # spectral flatness context
        ).clamp(0.0, 1.0)

        # Contour complexity: melodic richness
        contour_complexity = (
            0.30 * contour_ent
            + 0.25 * h3_sharp_std_h3
            + 0.20 * sharp_vel
            + 0.15 * h3_flat_mean_h16
            + 0.10 * loudness
        ).clamp(0.0, 1.0)

        # Gradient ratio: posterior / total (> 0.5 = onset-dominant)
        gradient_ratio = onset_posterior / (
            onset_posterior + sequence_anterior + self._EPS
        )

        # === M-LAYER (3D) ===
        activity_gradient = (
            ALPHA_POSTERIOR * onset_posterior
            + BETA_ANTERIOR * sequence_anterior
        ).clamp(0.0, 1.0)

        posterior_activity = (
            0.50 * onset_posterior
            + 0.25 * h3_beat_h3
            + 0.25 * h3_beat_per_h3
        ).clamp(0.0, 1.0)

        anterior_activity = (
            0.50 * sequence_anterior
            + 0.25 * h3_sharp_h3
            + 0.25 * h3_onset_per_h16
        ).clamp(0.0, 1.0)

        # === P-LAYER (2D) ===
        onset_state = (
            0.50 * h3_onset_h0
            + 0.30 * h3_flux_h0
            + 0.20 * onset_strength
        ).clamp(0.0, 1.0)

        contour_state = (
            0.40 * sequence_anterior
            + 0.30 * h3_sharp_h3
            + 0.30 * tonal_stab
        ).clamp(0.0, 1.0)

        # === F-LAYER (1D) ===
        phrase_boundary_pred = (
            0.35 * contour_ent
            + 0.30 * h3_flux_mean_h3
            + 0.20 * h3_flat_mean_h16
            + 0.15 * h3_onset_per_h16
        ).clamp(0.0, 1.0)

        return torch.stack([
            onset_posterior, sequence_anterior,
            contour_complexity, gradient_ratio,
            activity_gradient, posterior_activity, anterior_activity,
            onset_state, contour_state,
            phrase_boundary_pred,
        ], dim=-1)
