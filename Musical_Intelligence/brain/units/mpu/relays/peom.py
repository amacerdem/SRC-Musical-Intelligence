"""PEOM — Period Entrainment Optimization Model.

Gold standard Relay nucleus for the Motor Planning Unit (MPU).

Neural Circuit:
    Audio → Cochlea → Auditory Cortex (STG, 60/-33/6)
                ↓
              Putamen (beat period locking, L: Z=5.67, R: Z=5.08)
                ↓
              SMA / pre-SMA (sequence planning, Z=5.03)
                ↓
              PMd (velocity profile optimization, Z=5.30)
                ↓
              Cerebellum (motor timing, error correction, Z=4.68)
                ↓
              M1 (motor execution)

Key Findings:
    - Period locking (not phase) defines entrainment; CTR optimizes
      velocity/acceleration (Thaut et al. 2015, review)
    - Motor period entrains to auditory period even during subliminal
      tempo changes (Thaut et al. 1998b, N=12)
    - Basal ganglia (putamen) and SMA respond to beat in rhythm
      (Grahn & Brett 2007, Z=5.67 putamen, Z=5.03 SMA)
    - SMA+M1 stimulation reduced stride time CV: d=-1.10
      (Yamashita 2025, RCT, η²p=0.309)
    - Beta oscillations in SMA/AC modulated by rhythmic frequency
      (Fujioka 2012, MEG, N=12)

Temporal Architecture:
    - H3 (100ms):  Alpha-band onset/beat detection
    - H4 (125ms):  Theta-band interval timing
    - H8 (500ms):  Delta-band phrase context
    - H16 (1s):    Beat-level period tracking

R³ Remapping (Ontology Freeze v1.0.0):
    - Doc [8] "loudness"      → Code [10] loudness
    - Doc [10] "spectral_flux" → Code [21] spectral_flux
    - Doc [21] "spectral_change" → Code [21] spectral_flux
    - Doc [25] "x_l0l5"       → Code [42] beat_strength (dissolved)
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

# Period integration window — convergence time constant
# Source: Thaut et al. 2015, review; ~4s for full entrainment
TAU_DECAY: float = 4.0  # seconds

# Motor attention weight — high for rhythmic cueing
# Source: Ross & Balasubramaniam 2022, covert motor entrainment
ALPHA_ATTENTION: float = 0.90

# CV reduction effect size
# Source: Yamashita et al. 2025, d=-1.10, η²p=0.309
CV_REDUCTION_D: float = 1.10


class PEOM(Relay):
    """Period Entrainment Optimization Model — MPU Relay (Depth 0, 11D).

    Models how motor systems lock to the period (not phase) of auditory
    rhythms, providing a continuous time reference (CTR) that optimizes
    movement velocity and acceleration profiles.

    Primary equation: dP/dt = α · (T - P(t))
        P(t) = motor period, T = auditory period, α = entrainment rate

    Output Structure (11D):
        E-layer (3D) [0:3]:  Period entrainment, velocity optimization,
                              variability reduction
        M-layer (4D) [3:7]:  Motor period, velocity, acceleration, CV
        P-layer (2D) [7:9]:  Period lock strength, kinematic smoothness
        F-layer (2D) [9:11]: Next beat prediction, velocity profile pred
    """

    NAME = "PEOM"
    FULL_NAME = "Period Entrainment Optimization Model"
    UNIT = "MPU"

    OUTPUT_DIM = 11

    LAYERS = (
        LayerSpec(
            code="E", name="Extraction", start=0, end=3,
            dim_names=(
                "period_entrainment",      # Motor period lock to auditory
                "velocity_optimization",   # Kinematic smoothness via fixed T
                "variability_reduction",   # CV reduction with rhythmic cueing
            ),
            scope="internal",
        ),
        LayerSpec(
            code="M", name="Model", start=3, end=7,
            dim_names=(
                "motor_period",            # Entrained motor period (norm)
                "velocity",                # Optimized velocity profile
                "acceleration",            # Optimized acceleration profile
                "cv_reduction",            # Coefficient of variation reduction
            ),
            scope="external",
        ),
        LayerSpec(
            code="P", name="Present", start=7, end=9,
            dim_names=(
                "period_lock_strength",    # Period-locked neural activity
                "kinematic_smoothness",    # Jerk-reduction metric
            ),
            scope="external",
        ),
        LayerSpec(
            code="F", name="Future", start=9, end=11,
            dim_names=(
                "next_beat_pred",          # Next beat onset prediction
                "velocity_profile_pred",   # Velocity profile 0.5T ahead
            ),
            scope="hybrid",
        ),
    )

    # R³ features (5)
    _R3_AMPLITUDE = 7
    _R3_LOUDNESS = 10
    _R3_ONSET_STRENGTH = 11
    _R3_SPECTRAL_FLUX = 21
    _R3_BEAT_STRENGTH = 42         # Replaces dissolved x_l0l5

    _EPS: float = 1e-8

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        """15 temporal demands for period/beat tracking and interval timing."""
        return (
            # --- Spectral flux: onset/beat detection ---
            H3DemandSpec(r3_idx=21, r3_name="spectral_flux",
                         horizon=3, horizon_label="100ms alpha",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Onset at 100ms alpha band",
                         citation="Nozaradan et al. 2011"),
            H3DemandSpec(r3_idx=21, r3_name="spectral_flux",
                         horizon=3, horizon_label="100ms alpha",
                         morph=14, morph_name="periodicity", law=2, law_name="integration",
                         purpose="Beat periodicity at alpha band",
                         citation="Fujioka et al. 2012"),
            H3DemandSpec(r3_idx=21, r3_name="spectral_flux",
                         horizon=16, horizon_label="1s beat",
                         morph=14, morph_name="periodicity", law=2, law_name="integration",
                         purpose="Beat periodicity at 1s — period tracking",
                         citation="Grahn & Brett 2007"),
            # --- Onset strength ---
            H3DemandSpec(r3_idx=11, r3_name="onset_strength",
                         horizon=3, horizon_label="100ms alpha",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Onset strength at alpha band",
                         citation="Thaut et al. 2015"),
            H3DemandSpec(r3_idx=11, r3_name="onset_strength",
                         horizon=16, horizon_label="1s beat",
                         morph=14, morph_name="periodicity", law=2, law_name="integration",
                         purpose="Onset periodicity at 1s",
                         citation="Thaut et al. 1998b"),
            # --- Amplitude: beat energy ---
            H3DemandSpec(r3_idx=7, r3_name="amplitude",
                         horizon=3, horizon_label="100ms alpha",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Beat amplitude at onset level",
                         citation="Grahn & Brett 2007"),
            H3DemandSpec(r3_idx=7, r3_name="amplitude",
                         horizon=3, horizon_label="100ms alpha",
                         morph=2, morph_name="std", law=2, law_name="integration",
                         purpose="Amplitude variability — motor consistency",
                         citation="Yamashita et al. 2025"),
            H3DemandSpec(r3_idx=7, r3_name="amplitude",
                         horizon=16, horizon_label="1s beat",
                         morph=1, morph_name="mean", law=2, law_name="integration",
                         purpose="Mean amplitude over beat cycle",
                         citation="Grahn & Brett 2007"),
            # --- Loudness: motor drive ---
            H3DemandSpec(r3_idx=10, r3_name="loudness",
                         horizon=8, horizon_label="500ms delta",
                         morph=1, morph_name="mean", law=0, law_name="memory",
                         purpose="Mean loudness — motor drive level",
                         citation="Thaut et al. 2015"),
            # --- Spectral flux: tempo dynamics ---
            H3DemandSpec(r3_idx=21, r3_name="spectral_flux",
                         horizon=4, horizon_label="125ms theta",
                         morph=8, morph_name="velocity", law=0, law_name="memory",
                         purpose="Tempo velocity at theta band",
                         citation="Repp 2005"),
            H3DemandSpec(r3_idx=21, r3_name="spectral_flux",
                         horizon=16, horizon_label="1s beat",
                         morph=1, morph_name="mean", law=0, law_name="memory",
                         purpose="Mean spectral change at beat level",
                         citation="Thaut et al. 2015"),
            # --- Beat strength: motor-auditory coupling ---
            H3DemandSpec(r3_idx=42, r3_name="beat_strength",
                         horizon=3, horizon_label="100ms alpha",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Motor-auditory coupling onset (replaces x_l0l5)",
                         citation="Nozaradan et al. 2011"),
            H3DemandSpec(r3_idx=42, r3_name="beat_strength",
                         horizon=3, horizon_label="100ms alpha",
                         morph=14, morph_name="periodicity", law=2, law_name="integration",
                         purpose="Coupling periodicity at alpha band",
                         citation="Fujioka et al. 2012"),
            H3DemandSpec(r3_idx=42, r3_name="beat_strength",
                         horizon=16, horizon_label="1s beat",
                         morph=14, morph_name="periodicity", law=2, law_name="integration",
                         purpose="Coupling periodicity at beat level — CTR basis",
                         citation="Thaut et al. 1998b"),
            H3DemandSpec(r3_idx=42, r3_name="beat_strength",
                         horizon=16, horizon_label="1s beat",
                         morph=21, morph_name="zero_crossings", law=2, law_name="integration",
                         purpose="Coupling phase resets — period correction",
                         citation="Repp 2005"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "period_entrainment", "velocity_optimization", "variability_reduction",
            "motor_period", "velocity", "acceleration", "cv_reduction",
            "period_lock_strength", "kinematic_smoothness",
            "next_beat_pred", "velocity_profile_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            RegionLink(dim_name="period_entrainment", region="Putamen",
                       weight=0.9, citation="Grahn & Brett 2007"),
            RegionLink(dim_name="velocity_optimization", region="PMd",
                       weight=0.85, citation="Grahn & Brett 2007"),
            RegionLink(dim_name="motor_period", region="SMA",
                       weight=0.9, citation="Grahn & Brett 2007"),
            RegionLink(dim_name="kinematic_smoothness", region="Cerebellum",
                       weight=0.8, citation="Thaut et al. 2009b"),
            RegionLink(dim_name="next_beat_pred", region="pre_SMA",
                       weight=0.7, citation="Grahn & Brett 2007"),
            RegionLink(dim_name="period_lock_strength", region="STG",
                       weight=0.6, citation="Nozaradan et al. 2011"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            NeuroLink(dim_name="period_entrainment", channel=0, effect="produce",
                      weight=0.3, citation="Fujioka et al. 2012"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Thaut", 2015,
                         "Period locking (not phase) defines entrainment; CTR "
                         "optimizes velocity and acceleration profiles",
                         "review, EEG/behavioral"),
                Citation("Thaut", 1998,
                         "Motor period entrains to auditory even during subliminal "
                         "2% tempo changes; phase fluctuates but period locks",
                         "behavioral, N=12"),
                Citation("Grahn", 2007,
                         "Putamen (Z=5.67) and SMA (Z=5.03) respond to beat; "
                         "musicians also cerebellum + PMC",
                         "fMRI, N=20, FDR p<.001"),
                Citation("Yamashita", 2025,
                         "SMA+M1 gait-synchronized stimulation reduced stride "
                         "time CV from 4.51 to 2.80; d=-1.10, η²p=0.309",
                         "RCT tDCS+tACS, N=16"),
                Citation("Fujioka", 2012,
                         "Beta oscillations in SMA and auditory cortex modulated "
                         "by rhythmic frequency; internalized timing",
                         "MEG, N=12"),
                Citation("Repp", 2005,
                         "Sensorimotor synchronization: period correction vs phase "
                         "correction as distinct mechanisms",
                         "review, tapping literature"),
                Citation("Nozaradan", 2011,
                         "Neural entrainment to beat and meter frequencies; "
                         "beat-related peaks in frequency spectrum",
                         "EEG SSVEP, N=14"),
                Citation("Ross", 2022,
                         "Sensorimotor simulation supports subsecond beat timing; "
                         "motor network engaged without movement",
                         "review"),
                Citation("Tierney", 2013,
                         "Beat synchronization linked to neural response "
                         "consistency in inferior colliculus; r=.37",
                         "EEG ABR, N=124"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.85, 0.92),
            falsification_criteria=(
                "Disrupting auditory rhythm should increase motor variability "
                "(testable)",
                "Non-isochronous rhythms should reduce entrainment benefits "
                "(testable)",
                "Phase disruption alone should NOT abolish entrainment "
                "(predicted by period-lock theory)",
                "Very fast/slow tempi should reduce optimization "
                "(testable)",
            ),
            version="3.0.0",
            paper_count=9,
        )

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Period entrainment optimization: lock → optimize → reduce CV.

        Args:
            h3_features: H³ dict {(r3_idx, h, m, l): (B, T)}.
            r3_features: (B, T, 97) R³ features.

        Returns:
            (B, T, 11) output.
        """
        B, T = r3_features.shape[:2]
        device = r3_features.device

        # R³ features (5)
        amplitude      = r3_features[:, :, self._R3_AMPLITUDE]
        loudness       = r3_features[:, :, self._R3_LOUDNESS]
        onset_str      = r3_features[:, :, self._R3_ONSET_STRENGTH]
        flux           = r3_features[:, :, self._R3_SPECTRAL_FLUX]
        beat_strength  = r3_features[:, :, self._R3_BEAT_STRENGTH]

        _zeros = torch.zeros(B, T, device=device)

        def _h3(key, fallback=None):
            v = h3_features.get(key)
            if v is not None:
                return v
            return fallback if fallback is not None else _zeros

        # H³ features (15 tuples)
        h3_flux_h3        = _h3((21, 3, 0, 2), flux)
        h3_flux_per_h3    = _h3((21, 3, 14, 2))
        h3_flux_per_h16   = _h3((21, 16, 14, 2))
        h3_onset_h3       = _h3((11, 3, 0, 2), onset_str)
        h3_onset_per_h16  = _h3((11, 16, 14, 2))
        h3_amp_h3         = _h3((7, 3, 0, 2), amplitude)
        h3_amp_std_h3     = _h3((7, 3, 2, 2))
        h3_amp_mean_h16   = _h3((7, 16, 1, 2))
        h3_loud_mean_h8   = _h3((10, 8, 1, 0))
        h3_flux_vel_h4    = _h3((21, 4, 8, 0))
        h3_flux_mean_h16  = _h3((21, 16, 1, 0))
        h3_beat_h3        = _h3((42, 3, 0, 2), beat_strength)
        h3_beat_per_h3    = _h3((42, 3, 14, 2))
        h3_beat_per_h16   = _h3((42, 16, 14, 2))
        h3_beat_zc_h16    = _h3((42, 16, 21, 2))

        # === E-LAYER (3D) — Explicit Features ===

        # Period entrainment: period locking strength
        period_entrainment = (
            0.30 * h3_flux_per_h16            # beat periodicity at 1s
            + 0.25 * h3_onset_per_h16         # onset periodicity
            + 0.25 * h3_beat_per_h16          # coupling periodicity 1s
            + 0.20 * h3_onset_h3              # current onset strength
        ).clamp(0.0, 1.0)

        # Velocity optimization: kinematic smoothness via fixed period
        velocity_optimization = (
            0.30 * h3_beat_per_h16            # coupling periodicity (CTR)
            + 0.25 * h3_flux_mean_h16         # spectral stability
            + 0.25 * (1.0 - h3_amp_std_h3)   # low amplitude variability
            + 0.20 * h3_loud_mean_h8          # motor drive level
        ).clamp(0.0, 1.0)

        # Variability reduction: CV reduction from rhythmic cueing
        variability_reduction = (
            0.30 * period_entrainment * velocity_optimization
            + 0.25 * h3_beat_per_h3           # short-term coupling
            + 0.25 * (1.0 - h3_beat_zc_h16)  # fewer phase resets = stable
            + 0.20 * h3_amp_mean_h16          # sustained energy
        ).clamp(0.0, 1.0)

        # === M-LAYER (4D) — Mathematical Model ===

        # Motor period: entrained period estimate (normalized)
        motor_period = (
            0.40 * period_entrainment
            + 0.30 * h3_flux_per_h16
            + 0.30 * h3_beat_per_h16
        ).clamp(0.0, 1.0)

        # Velocity: optimized velocity profile
        velocity = (
            0.40 * velocity_optimization
            + 0.30 * h3_flux_vel_h4.abs().clamp(0.0, 1.0)
            + 0.30 * h3_loud_mean_h8
        ).clamp(0.0, 1.0)

        # Acceleration: optimized acceleration
        acceleration = (
            0.50 * velocity
            + 0.50 * h3_amp_h3
        ).clamp(0.0, 1.0)

        # CV reduction: coefficient of variation improvement
        cv_reduction = variability_reduction

        # === P-LAYER (2D) — Present Processing ===

        period_lock_strength = (
            0.40 * h3_beat_per_h16
            + 0.30 * h3_onset_per_h16
            + 0.30 * h3_flux_per_h3
        ).clamp(0.0, 1.0)

        kinematic_smoothness = (
            0.40 * velocity_optimization
            + 0.30 * (1.0 - h3_amp_std_h3)
            + 0.30 * velocity
        ).clamp(0.0, 1.0)

        # === F-LAYER (2D) — Future Predictions ===

        next_beat_pred = (
            0.40 * period_entrainment
            + 0.30 * h3_flux_per_h16
            + 0.30 * h3_beat_per_h16
        ).clamp(0.0, 1.0)

        velocity_profile_pred = (
            0.40 * velocity_optimization
            + 0.30 * h3_beat_per_h16
            + 0.30 * h3_flux_vel_h4.abs().clamp(0.0, 1.0)
        ).clamp(0.0, 1.0)

        return torch.stack([
            period_entrainment, velocity_optimization, variability_reduction,
            motor_period, velocity, acceleration, cv_reduction,
            period_lock_strength, kinematic_smoothness,
            next_beat_pred, velocity_profile_pred,
        ], dim=-1)
