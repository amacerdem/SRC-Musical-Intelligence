"""SRP — Striatal Reward Pathway.

Gold standard Relay nucleus for the Affective Resonance Unit (ARU).

Neural Circuit:
    Audio → STG/STS (spectrotemporal pattern recognition)
                ↓
              IFG / dlPFC (musical syntax, expectation, prediction)
                ↓
              Amygdala (salience, uncertainty × surprise)
                ↓
              Caudate (dorsal striatum, anticipatory DA ramp)
                ↓
              NAcc (ventral striatum, consummatory DA + μ-opioid)
                ↓
              VTA → Hippocampus (memory encoding, contextual association)

Key Findings:
    - NAcc DA ↑ at consummation, Caudate DA ↑ at anticipation
      (Salimpoor 2011, PET, r=0.84 NAcc, r=0.71 Caudate)
    - NAcc-STG connectivity predicts reward value
      (Salimpoor 2013, fMRI+auction, N=19)
    - Pleasure = f(uncertainty, surprise) nonlinear
      (Cheung 2019, ML+fMRI, N=39, d=3.8-8.53)
    - DA causally modulates wanting AND liking
      (Ferreri 2019, pharmacology, Z=1.97 pleasure)
    - dlPFC TMS modulates NAcc reward
      (Mas-Herrero 2021, d=0.81 pleasure)
    - Musical anhedonia = NAcc-STG disconnection
      (Martinez-Molina 2016, d=3.6-7.0)
    - μ-opioid in ventral striatum during pleasure
      (Nummenmaa 2025, PET)

Temporal Architecture:
    - H3, H4:  Beat-level prediction error (50-125ms)
    - H16:     Beat-level peak detection (1s)
    - H20:     Phrase-level tension/anticipation (5s)
    - H24:     Section-level caudate ramp (36s)

R³ Remapping (Ontology Freeze v1.0.0):
    - Doc [8] "loudness"      → Code [10] loudness
    - Doc [10] "spectral_flux" → Code [21] spectral_flux
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

# NAcc-pleasure correlation coefficient
# Source: Salimpoor 2011, PET [¹¹C]raclopride, r=0.84
BETA_NACC: float = 0.84

# Caudate-anticipation correlation coefficient
# Source: Salimpoor 2011, PET [¹¹C]raclopride, r=0.71
BETA_CAUDATE: float = 0.71

# Anticipatory ramp half-life (quasi-hyperbolic profile)
# Source: Howe et al. 2013, in vivo rodent DA recordings
TAU_ANTICIPATION: float = 15.0  # seconds

# Opioid-consonance weight
# Source: Nummenmaa 2025, PET [¹¹C]carfentanil, ventral striatum
OPIOID_CONSONANCE_WEIGHT: float = 0.4


class SRP(Relay):
    """Striatal Reward Pathway — ARU Relay (Depth 0, 14D).

    Models how the brain generates musical pleasure through dopamine
    release in the striatum, decomposed into wanting (caudate,
    anticipatory), liking (NAcc, consummatory), and prediction error
    (VTA phasic burst).

    Three dissociable reward systems (Berridge & Robinson 1993):
        1. WANTING: Incentive salience, caudate DA ramp
        2. LIKING: Hedonic impact, NAcc DA + μ-opioid
        3. LEARNING: Prediction error, VTA phasic burst

    Output Structure (14D):
        E-layer (4D) [0:4]:   Caudate DA, NAcc DA, opioid proxy, pred error
        M-layer (3D) [4:7]:   Harmonic tension, dynamic intensity, peak
        P-layer (3D) [7:10]:  Wanting, liking, pleasure
        F-layer (4D) [10:14]: Tension, reward forecast, chills prox, resolution
    """

    NAME = "SRP"
    FULL_NAME = "Striatal Reward Pathway"
    UNIT = "ARU"

    OUTPUT_DIM = 14

    LAYERS = (
        LayerSpec(
            code="E", name="Extraction", start=0, end=4,
            dim_names=(
                "caudate_da",          # Dorsal striatal DA — anticipatory ramp
                "nacc_da",             # Ventral striatal DA — consummatory burst
                "opioid_proxy",        # μ-opioid hedonic component
                "prediction_error",    # Signed RPE (positive=better than expected)
            ),
            scope="internal",
        ),
        LayerSpec(
            code="M", name="Model", start=4, end=7,
            dim_names=(
                "harmonic_tension",    # Tonal distance from tonic
                "dynamic_intensity",   # Energy trajectory (crescendo/decrescendo)
                "peak_detection",      # Chill trigger detection
            ),
            scope="external",
        ),
        LayerSpec(
            code="P", name="Present", start=7, end=10,
            dim_names=(
                "wanting",             # Berridge incentive salience
                "liking",              # Berridge hedonic impact
                "pleasure",            # Composite subjective pleasure
            ),
            scope="external",
        ),
        LayerSpec(
            code="F", name="Future", start=10, end=14,
            dim_names=(
                "tension",             # Huron T: preparatory arousal
                "reward_forecast",     # Expected reward 2-8s ahead
                "chills_proximity",    # Proximity to chills event
                "resolution_expect",   # Expected harmonic resolution
            ),
            scope="hybrid",
        ),
    )

    # R³ features (13)
    _R3_ROUGHNESS = 0
    _R3_SENSORY_PLEASANT = 4
    _R3_AMPLITUDE = 7
    _R3_LOUDNESS = 10
    _R3_ONSET_STRENGTH = 11
    _R3_WARMTH = 12
    _R3_SHARPNESS = 13
    _R3_TONALNESS = 14
    _R3_SPECTRAL_SMOOTHNESS = 16
    _R3_SPECTRAL_FLUX = 21
    _R3_DISTRIBUTION_ENTROPY = 22
    _R3_BEAT_STRENGTH = 42         # Replaces dissolved x_l0l5
    _R3_TONAL_STABILITY = 60       # Replaces dissolved x_l4l5

    _VELOCITY_GAIN: float = 5.0
    _EPS: float = 1e-8

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        """18 temporal demands across reward-relevant timescales."""
        return (
            # --- Spectral flux: prediction error trigger ---
            H3DemandSpec(r3_idx=21, r3_name="spectral_flux",
                         horizon=3, horizon_label="23ms onset",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Onset detection — RPE trigger",
                         citation="Schultz 2016"),
            H3DemandSpec(r3_idx=21, r3_name="spectral_flux",
                         horizon=3, horizon_label="23ms onset",
                         morph=8, morph_name="velocity", law=2, law_name="integration",
                         purpose="Spectral velocity — surprise magnitude",
                         citation="Cheung 2019"),
            H3DemandSpec(r3_idx=21, r3_name="spectral_flux",
                         horizon=16, horizon_label="1s beat",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Beat-level spectral context",
                         citation="Gold 2019"),
            # --- Onset strength: peak detection ---
            H3DemandSpec(r3_idx=11, r3_name="onset_strength",
                         horizon=3, horizon_label="23ms onset",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Onset marker — chill trigger",
                         citation="Sloboda 1991"),
            H3DemandSpec(r3_idx=11, r3_name="onset_strength",
                         horizon=16, horizon_label="1s beat",
                         morph=14, morph_name="periodicity", law=2, law_name="integration",
                         purpose="Rhythmic regularity — groove reward",
                         citation="Salimpoor 2011"),
            # --- Roughness: tension/resolution ---
            H3DemandSpec(r3_idx=0, r3_name="roughness",
                         horizon=16, horizon_label="1s beat",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Current dissonance — harmonic tension",
                         citation="Cheung 2019"),
            H3DemandSpec(r3_idx=0, r3_name="roughness",
                         horizon=20, horizon_label="5s phrase",
                         morph=18, morph_name="trend", law=0, law_name="memory",
                         purpose="Roughness trajectory — resolution direction",
                         citation="Huron 2006"),
            # --- Sensory pleasantness: opioid proxy ---
            H3DemandSpec(r3_idx=4, r3_name="sensory_pleasantness",
                         horizon=16, horizon_label="1s beat",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Current pleasantness — opioid drive",
                         citation="Nummenmaa 2025"),
            H3DemandSpec(r3_idx=4, r3_name="sensory_pleasantness",
                         horizon=20, horizon_label="5s phrase",
                         morph=1, morph_name="mean", law=0, law_name="memory",
                         purpose="Mean pleasantness over phrase",
                         citation="Blood & Zatorre 2001"),
            # --- Amplitude: dynamic intensity ---
            H3DemandSpec(r3_idx=7, r3_name="amplitude",
                         horizon=3, horizon_label="23ms onset",
                         morph=8, morph_name="velocity", law=2, law_name="integration",
                         purpose="Energy velocity — crescendo detection",
                         citation="Panksepp 1995"),
            H3DemandSpec(r3_idx=7, r3_name="amplitude",
                         horizon=16, horizon_label="1s beat",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Beat-level energy — arousal",
                         citation="Salimpoor 2011"),
            H3DemandSpec(r3_idx=7, r3_name="amplitude",
                         horizon=20, horizon_label="5s phrase",
                         morph=8, morph_name="velocity", law=0, law_name="memory",
                         purpose="Phrase-level energy trajectory — buildup",
                         citation="Howe et al. 2013"),
            # --- Tonalness: consonance resolution ---
            H3DemandSpec(r3_idx=14, r3_name="tonalness",
                         horizon=16, horizon_label="1s beat",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Current consonance — resolution signal",
                         citation="Cheung 2019"),
            H3DemandSpec(r3_idx=14, r3_name="tonalness",
                         horizon=16, horizon_label="1s beat",
                         morph=2, morph_name="std", law=0, law_name="memory",
                         purpose="Consonance variability — harmonic surprise",
                         citation="Cheung 2019"),
            # --- Loudness: arousal ---
            H3DemandSpec(r3_idx=10, r3_name="loudness",
                         horizon=16, horizon_label="1s beat",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Perceptual loudness — arousal proxy",
                         citation="Salimpoor 2011"),
            # --- Beat strength: anticipatory DA ---
            H3DemandSpec(r3_idx=42, r3_name="beat_strength",
                         horizon=16, horizon_label="1s beat",
                         morph=14, morph_name="periodicity", law=2, law_name="integration",
                         purpose="Beat regularity — anticipation basis",
                         citation="Salimpoor 2011"),
            H3DemandSpec(r3_idx=42, r3_name="beat_strength",
                         horizon=20, horizon_label="5s phrase",
                         morph=18, morph_name="trend", law=0, law_name="memory",
                         purpose="Beat trend — wanting ramp",
                         citation="Howe et al. 2013"),
            # --- Tonal stability: resolution expectation ---
            H3DemandSpec(r3_idx=60, r3_name="tonal_stability",
                         horizon=16, horizon_label="1s beat",
                         morph=0, morph_name="value", law=2, law_name="integration",
                         purpose="Tonal resolution — expected reward",
                         citation="Cheung 2019"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "caudate_da", "nacc_da", "opioid_proxy", "prediction_error",
            "harmonic_tension", "dynamic_intensity", "peak_detection",
            "wanting", "liking", "pleasure",
            "tension", "reward_forecast", "chills_proximity", "resolution_expect",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            RegionLink(dim_name="caudate_da", region="Caudate",
                       weight=0.9, citation="Salimpoor 2011"),
            RegionLink(dim_name="nacc_da", region="NAcc",
                       weight=0.9, citation="Salimpoor 2011"),
            RegionLink(dim_name="opioid_proxy", region="NAcc_shell",
                       weight=0.8, citation="Nummenmaa 2025"),
            RegionLink(dim_name="prediction_error", region="VTA",
                       weight=0.85, citation="Schultz 2016"),
            RegionLink(dim_name="wanting", region="Caudate",
                       weight=0.7, citation="Berridge 2007"),
            RegionLink(dim_name="liking", region="NAcc",
                       weight=0.8, citation="Berridge 2007"),
            RegionLink(dim_name="tension", region="IFG",
                       weight=0.6, citation="Huron 2006"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            NeuroLink(dim_name="caudate_da", channel=0, effect="produce",
                      weight=0.7, citation="Salimpoor 2011"),
            NeuroLink(dim_name="nacc_da", channel=0, effect="produce",
                      weight=0.8, citation="Salimpoor 2011"),
            NeuroLink(dim_name="prediction_error", channel=0, effect="amplify",
                      weight=0.5, citation="Schultz 2016"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Salimpoor", 2011,
                         "PET: NAcc DA at consummation (r=0.84), Caudate DA "
                         "at anticipation (r=0.71); ~3.7 chills per excerpt",
                         "PET, N=8, [¹¹C]raclopride"),
                Citation("Salimpoor", 2013,
                         "NAcc-STG connectivity predicts how much listeners "
                         "would PAY for novel music",
                         "fMRI+auction, N=19"),
                Citation("Cheung", 2019,
                         "Pleasure = nonlinear f(uncertainty, surprise); "
                         "80,000 chords; amygdala, hippocampus, AC interact",
                         "ML+fMRI, N=39, d=3.8-8.53"),
                Citation("Ferreri", 2019,
                         "Levodopa ↑ pleasure (Z=1.97), chills (Z=2.34), "
                         "willingness to pay (Z=2.44). Risperidone blocks all",
                         "pharmacology, N=27, causal"),
                Citation("Mas-Herrero", 2021,
                         "dlPFC TMS modulates NAcc reward; pre-experience → "
                         "motivation (R²=0.47), experience → pleasure (R²=0.44)",
                         "TMS+fMRI, N=17, d=0.81"),
                Citation("Martinez-Molina", 2016,
                         "Musical anhedonia (~5%) = NAcc-STG disconnection; "
                         "music-specific, NOT monetary",
                         "fMRI+DTI, N=30, d=3.6-7.0"),
                Citation("Nummenmaa", 2025,
                         "Pleasurable music activates μ-opioid receptors in "
                         "ventral striatum and OFC",
                         "PET, [¹¹C]carfentanil"),
                Citation("Schultz", 2016,
                         "Two-component phasic DA: unselective (40-120ms) + "
                         "value-coding RPE; baseline ~5Hz, burst 14-30Hz",
                         "review"),
                Citation("Howe", 2013,
                         "DA ramps quasi-hyperbolically toward distant rewards; "
                         "scales with distance × magnitude",
                         "in vivo rodent"),
                Citation("Blood", 2001,
                         "Chills correlate with ↑ ventral striatum, midbrain "
                         "(VTA), OFC; ↓ amygdala, hippocampus",
                         "PET rCBF, N=10"),
                Citation("Huron", 2006,
                         "ITPRA: 5 temporal response systems — Imagination, "
                         "Tension, Prediction, Reaction, Appraisal",
                         "theoretical"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.88, 0.95),
            falsification_criteria=(
                "Wanting should ramp BEFORE liking peaks — not simultaneous "
                "(CONFIRMED: Salimpoor 2011)",
                "NAcc-STG connectivity should predict reward value "
                "(CONFIRMED: Salimpoor 2013)",
                "DA antagonists should reduce musical pleasure "
                "(CONFIRMED: Ferreri 2019, risperidone)",
                "Musical anhedonia should show NAcc-STG disconnection "
                "(CONFIRMED: Martinez-Molina 2016)",
                "Deceptive cadence should produce negative then positive RPE",
            ),
            version="3.0.0",
            paper_count=11,
        )

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Striatal reward pathway: wanting + liking + prediction error.

        Args:
            h3_features: H³ dict {(r3_idx, h, m, l): (B, T)}.
            r3_features: (B, T, 97) R³ features.

        Returns:
            (B, T, 14) output.
        """
        B, T = r3_features.shape[:2]
        device = r3_features.device

        # R³ features (13)
        roughness      = r3_features[:, :, self._R3_ROUGHNESS]
        pleasant       = r3_features[:, :, self._R3_SENSORY_PLEASANT]
        amplitude      = r3_features[:, :, self._R3_AMPLITUDE]
        loudness       = r3_features[:, :, self._R3_LOUDNESS]
        onset_str      = r3_features[:, :, self._R3_ONSET_STRENGTH]
        warmth         = r3_features[:, :, self._R3_WARMTH]
        tonalness      = r3_features[:, :, self._R3_TONALNESS]
        smoothness     = r3_features[:, :, self._R3_SPECTRAL_SMOOTHNESS]
        flux           = r3_features[:, :, self._R3_SPECTRAL_FLUX]
        dist_ent       = r3_features[:, :, self._R3_DISTRIBUTION_ENTROPY]
        beat_strength  = r3_features[:, :, self._R3_BEAT_STRENGTH]
        tonal_stab     = r3_features[:, :, self._R3_TONAL_STABILITY]

        _zeros = torch.zeros(B, T, device=device)

        def _h3(key, fallback=None):
            v = h3_features.get(key)
            if v is not None:
                return v
            return fallback if fallback is not None else _zeros

        # H³ features (18 tuples)
        h3_flux_h3        = _h3((21, 3, 0, 2), flux)
        h3_flux_vel_h3    = _h3((21, 3, 8, 2))
        h3_flux_h16       = _h3((21, 16, 0, 2), flux)
        h3_onset_h3       = _h3((11, 3, 0, 2), onset_str)
        h3_onset_per_h16  = _h3((11, 16, 14, 2))
        h3_rough_h16      = _h3((0, 16, 0, 2), roughness)
        h3_rough_trend_h20 = _h3((0, 20, 18, 0))
        h3_pleas_h16      = _h3((4, 16, 0, 2), pleasant)
        h3_pleas_mean_h20 = _h3((4, 20, 1, 0))
        h3_amp_vel_h3     = _h3((7, 3, 8, 2))
        h3_amp_h16        = _h3((7, 16, 0, 2), amplitude)
        h3_amp_vel_h20    = _h3((7, 20, 8, 0))
        h3_tonal_h16      = _h3((14, 16, 0, 2), tonalness)
        h3_tonal_std_h16  = _h3((14, 16, 2, 0))
        h3_loud_h16       = _h3((10, 16, 0, 2), loudness)
        h3_beat_per_h16   = _h3((42, 16, 14, 2))
        h3_beat_trend_h20 = _h3((42, 20, 18, 0))
        h3_tonal_stab_h16 = _h3((60, 16, 0, 2), tonal_stab)

        # Velocity normalization
        flux_vel = (h3_flux_vel_h3 * self._VELOCITY_GAIN).clamp(-1.0, 1.0)
        amp_vel_onset = (h3_amp_vel_h3 * self._VELOCITY_GAIN).abs().clamp(0.0, 1.0)

        # Derived: consonance (inverse roughness)
        consonance = (1.0 - h3_rough_h16).clamp(0.0, 1.0)

        # Derived: resolution signal (decreasing roughness + high tonalness)
        resolution = (
            0.50 * consonance
            + 0.50 * h3_tonal_stab_h16
        ).clamp(0.0, 1.0)

        # === E-LAYER (4D) — Neurochemical Signals ===

        # Caudate DA: anticipatory ramp (quasi-hyperbolic buildup)
        caudate_da = (
            0.30 * h3_beat_trend_h20           # beat trend → wanting ramp
            + 0.25 * h3_beat_per_h16           # rhythmic regularity
            + 0.20 * h3_amp_vel_h20.abs().clamp(0.0, 1.0)  # energy buildup
            + 0.15 * h3_tonal_std_h16          # harmonic surprise context
            + 0.10 * beat_strength
        ).clamp(0.0, 1.0)

        # NAcc DA: consummatory burst (at peak moment)
        nacc_da = (
            0.25 * h3_pleas_h16               # current pleasantness
            + 0.25 * resolution                # harmonic resolution
            + 0.20 * h3_flux_h3               # onset at event
            + 0.15 * h3_onset_h3              # onset strength
            + 0.15 * h3_loud_h16              # arousal
        ).clamp(0.0, 1.0)

        # Opioid proxy: μ-opioid hedonic (consonance + smoothness)
        opioid_proxy = (
            OPIOID_CONSONANCE_WEIGHT * consonance
            + 0.30 * h3_pleas_mean_h20
            + 0.30 * smoothness
        ).clamp(0.0, 1.0)

        # Prediction error: signed RPE (positive = better than expected)
        prediction_error = (
            0.40 * flux_vel                    # spectral velocity direction
            + 0.30 * (h3_flux_h3 - h3_flux_h16)  # local vs context
            + 0.30 * h3_tonal_std_h16          # harmonic surprise
        ).clamp(-1.0, 1.0)

        # === M-LAYER (3D) — Musical Meaning ===

        # Harmonic tension: tonal distance from resolution
        harmonic_tension = (
            0.35 * h3_rough_h16               # current dissonance
            + 0.30 * (1.0 - h3_tonal_h16)    # tonal instability
            + 0.20 * dist_ent                  # entropy → uncertainty
            + 0.15 * h3_rough_trend_h20.abs().clamp(0.0, 1.0)
        ).clamp(0.0, 1.0)

        # Dynamic intensity: energy trajectory
        dynamic_intensity = (
            0.40 * amp_vel_onset               # onset energy velocity
            + 0.30 * h3_amp_h16               # beat-level energy
            + 0.30 * h3_amp_vel_h20.abs().clamp(0.0, 1.0)
        ).clamp(0.0, 1.0)

        # Peak detection: chill trigger features
        peak_detection = (
            0.30 * h3_onset_h3                # onset strength
            + 0.25 * amp_vel_onset            # crescendo
            + 0.25 * flux_vel.abs()           # surprise magnitude
            + 0.20 * h3_onset_per_h16         # rhythmic regularity
        ).clamp(0.0, 1.0)

        # === P-LAYER (3D) — Psychological States ===

        # Wanting: Berridge incentive salience (DA-dependent)
        wanting = (BETA_CAUDATE * caudate_da).clamp(0.0, 1.0)

        # Liking: Berridge hedonic impact (opioid + DA)
        liking = (
            0.50 * (BETA_NACC * nacc_da)
            + 0.50 * opioid_proxy
        ).clamp(0.0, 1.0)

        # Pleasure: composite (Salimpoor 2011 coefficients)
        pleasure = (
            BETA_NACC * nacc_da * 0.55
            + BETA_CAUDATE * caudate_da * 0.45
        ).clamp(0.0, 1.0)

        # === F-LAYER (4D) — Forecast ===

        # Tension: Huron T preparatory arousal
        tension = (
            0.40 * harmonic_tension
            + 0.30 * dynamic_intensity
            + 0.30 * caudate_da
        ).clamp(0.0, 1.0)

        # Reward forecast: expected reward 2-8s
        reward_forecast = (
            0.50 * caudate_da
            + 0.30 * h3_beat_trend_h20.clamp(0.0, 1.0)
            + 0.20 * h3_amp_vel_h20.clamp(0.0, 1.0)
        ).clamp(0.0, 1.0)

        # Chills proximity: estimated distance to chill event
        chills_proximity = (
            0.35 * nacc_da
            + 0.35 * peak_detection
            + 0.30 * caudate_da
        ).clamp(0.0, 1.0)

        # Resolution expectation: expected harmonic resolution
        resolution_expect = (
            0.40 * resolution
            + 0.30 * h3_tonal_stab_h16
            + 0.30 * (1.0 - harmonic_tension)
        ).clamp(0.0, 1.0)

        return torch.stack([
            caudate_da, nacc_da, opioid_proxy, prediction_error,
            harmonic_tension, dynamic_intensity, peak_detection,
            wanting, liking, pleasure,
            tension, reward_forecast, chills_proximity, resolution_expect,
        ], dim=-1)
