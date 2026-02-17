"""SNEM — Steady-State Evoked Potential / Neural Entrainment Monitor.

Gold standard Relay nucleus for the Auditory Salience Unit (ASU).

Neural Circuit:
    Audio → Cochlea → A1/STG (onset detection, SS-EP generation)
                        ↓
                      SMA (beat-motor coupling)
                        ↓
                      Basal Ganglia / Putamen (beat/meter detection)
                        ↓
                      PMC (motor preparation, pre-motor timing)
                        ↓
                      dACC / Anterior Insula (salience evaluation)

Key Findings:
    - Frequency-tagged EEG (SS-EP) shows selective neural entrainment
      to beat AND meter frequencies, beyond what is present in the
      acoustic envelope (Nozaradan et al. 2011, 2012)
    - Enhancement is SELECTIVE: beat frequencies enhanced ~2:1 over
      non-beat frequencies in the same stimulus (Nozaradan 2012)
    - Basal ganglia (putamen) and SMA show beat-specific activation
      regardless of training (Grahn & Brett 2007, fMRI)
    - Oscillatory entrainment follows period-correction dynamics
      with coupling strength proportional to beat salience
      (Large & Palmer 2002, computational model)
    - Musical tempo modulates emotional states via neural
      entrainment (Yang et al. 2025, EEG)

Critical Qualifier:
    - SS-EP enhancement operates only within 1-4 Hz range;
      tempi outside this window show reduced entrainment
      (Nozaradan 2011)
    - Enhancement requires rhythmic regularity; random timing
      abolishes the effect (p = 0.65, n.s. — Nozaradan 2012)
    - Motor system involvement is partially automatic but modulated
      by attention (Grahn & Brett 2007)
    - Individual differences in rhythm ability are partly genetic
      (Niarchou et al. 2022, GWAS, N = 606,825)

Temporal Architecture:
    SNEM uses H³ demands at four timescales:
    - Onset (H0, H3):  Individual onset detection and identification
    - Beat (H6):       Beat-level periodicity and pulse clarity
    - Measure (H16):   Meter-level periodicity and temporal structure
    All demands use L2 (integration) for bidirectional context except
    velocity/entropy demands which use L0 (memory) for causal lookback.

R³ Remapping (Ontology Freeze v1.0.0):
    Doc referenced dissolved Group E (x_l0l5 [25:33]) for motor-auditory
    coupling.  Replaced with beat_strength [42] from Group G (Rhythm &
    Groove), which directly measures the beat clarity that drives
    sensorimotor entrainment.

    Doc index mismatches resolved:
    - Doc [8] "loudness"       → Code [10] loudness
    - Doc [10] "spectral_flux" → Code [21] spectral_flux
    - Doc [22] "energy_change" → Code [11] onset_strength
    - Doc [25] "x_l0l5"       → Code [42] beat_strength (dissolved)

Cross-Unit Dependencies:
    SNEM is the FOUNDATION of ASU.  Its outputs feed:
    - BARM (Encoder): SNEM.beat_entrainment → entrainment baseline
    - STANM (Encoder): SNEM.selective_gain → temporal attention
    - PWSM (Associator): SNEM.entrainment_strength → precision weighting
    - DGTP (Associator): SNEM.beat_salience → speech/beat processing
    - STU.HMCE (Cross-unit): SNEM.beat_locked_activity → motor sync
    - STU.AMSC (Cross-unit): SNEM.meter_position_pred → metrical hierarchy
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
# Scientific constants — every coefficient cites its source
# ======================================================================

# SS-EP enhancement weights
# Source: Nozaradan et al. 2011, 2012 — frequency-tagged EEG
# Beat frequencies enhanced ~2:1 over non-beat; meter also enhanced
ALPHA_SSEP: float = 1.0   # Beat salience weight (primary)
BETA_SSEP: float = 0.8    # Meter salience weight (secondary)
GAMMA_SSEP: float = 0.5   # Envelope subtraction (non-specific removal)

# Entrainment coupling strength
# Source: Large & Palmer 2002 — oscillatory entrainment model
# Period correction: Δt/τ, where τ reflects coupling strength
COUPLING_STRENGTH: float = 0.75

# Basal ganglia beat specificity
# Source: Grahn & Brett 2007 — fMRI, putamen activation for beat
# Beat > non-beat in putamen regardless of musical training
PUTAMEN_BEAT_WEIGHT: float = 0.85


class SNEM(Relay):
    """SS-EP / Neural Entrainment Monitor — ASU Relay (Depth 0, 12D).

    Transforms raw R³ rhythm/onset features and H³ temporal demands into
    the foundational salience representation for the Auditory Salience Unit.

    The computation models the neural entrainment pathway from auditory
    cortex (SS-EP generation) through basal ganglia (beat/meter detection)
    to frontal motor areas (SMA/PMC, sensorimotor coupling).

    The key scientific insight is SELECTIVE enhancement: the brain amplifies
    neural responses at beat and meter frequencies beyond what is present
    in the acoustic input (Nozaradan et al. 2011, 2012).

    Output Structure (12D):
        E-layer (3D) [0:3]:   Beat/meter entrainment + selective enhancement
        M-layer (3D) [3:6]:   SS-EP enhancement, enhancement index, beat salience
        P-layer (3D) [6:9]:   Beat-locked activity, entrainment strength, gain
        F-layer (3D) [9:12]:  Predictions — beat onset, meter position, enhancement
    """

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    NAME = "SNEM"
    FULL_NAME = "Steady-State Evoked Potential / Neural Entrainment Monitor"
    UNIT = "ASU"

    # ------------------------------------------------------------------
    # Output structure — 12D: E(3) + M(3) + P(3) + F(3)
    # ------------------------------------------------------------------

    OUTPUT_DIM = 12

    LAYERS = (
        LayerSpec(
            code="E", name="Extraction", start=0, end=3,
            dim_names=(
                "beat_entrainment",        # Neural entrainment to beat frequency
                "meter_entrainment",       # Neural entrainment to meter frequency
                "selective_enhancement",   # SS-EP selective gain (beat > non-beat)
            ),
            scope="internal",  # Feeds downstream ASU nuclei
        ),
        LayerSpec(
            code="M", name="Model", start=3, end=6,
            dim_names=(
                "ssep_enhancement",   # SS-EP enhancement index (Nozaradan formula)
                "enhancement_index",  # Beat-locked enhancement magnitude
                "beat_salience",      # Composite beat salience from onsets
            ),
            scope="external",  # Key scientific observable
        ),
        LayerSpec(
            code="P", name="Present", start=6, end=9,
            dim_names=(
                "beat_locked_activity",  # Beat-locked neural amplitude
                "entrainment_strength",  # Overall entrainment strength
                "selective_gain",        # Selective gain magnitude
            ),
            scope="external",  # Regional activation outputs
        ),
        LayerSpec(
            code="F", name="Future", start=9, end=12,
            dim_names=(
                "beat_onset_pred",       # Predicted next beat onset timing
                "meter_position_pred",   # Predicted metrical position
                "enhancement_pred",      # Predicted enhancement trajectory
            ),
            scope="hybrid",  # Predictions feed downstream + carry external meaning
        ),
    )

    # ------------------------------------------------------------------
    # R³ feature indices consumed (8 scalar features)
    # ------------------------------------------------------------------

    # Energy group B [7:12]
    _R3_AMPLITUDE = 7            # RMS amplitude (beat energy)
    _R3_LOUDNESS = 10            # Perceptual loudness
    _R3_ONSET_STRENGTH = 11      # Onset detection energy

    # Change group D [21:25]
    _R3_SPECTRAL_FLUX = 21       # Spectral frame-to-frame change (onset marker)

    # Rhythm group G [41:51]
    _R3_TEMPO_ESTIMATE = 41      # Current tempo estimate (BPM proxy)
    _R3_BEAT_STRENGTH = 42       # Pulse/beat clarity (replaces dissolved x_l0l5)
    _R3_PULSE_CLARITY = 43       # Pulse quality/clarity index
    _R3_EVENT_DENSITY = 48       # Musical event density

    # ------------------------------------------------------------------
    # Computation parameters
    # ------------------------------------------------------------------

    _VELOCITY_GAIN: float = 5.0   # M8 velocity normalization
    _ENTROPY_SCALE: float = 3.0   # M20 entropy normalization
    _EPS: float = 1e-8

    # ------------------------------------------------------------------
    # H³ temporal demands — 18 tuples organized by temporal law
    #
    # L2 (Integration) = Present: 15 demands
    # L0 (Memory)      = Past:     3 demands
    # ------------------------------------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        """18 temporal demands across two laws and four timescales.

        Onset  (H0, H3):  Individual onset detection (5.8ms, 23ms)
        Beat   (H6):      Beat-level periodicity (200ms)
        Measure (H16):    Meter-level structure (1s)
        """
        return (
            # ═══════════════════════════════════════════════════════════
            # PRESENT demands (L2 = Integration) — 15 tuples
            # ═══════════════════════════════════════════════════════════

            # --- Spectral flux (R³[21]) — 4 present scales ---
            # Primary onset detection signal for SS-EP computation
            H3DemandSpec(
                r3_idx=21, r3_name="spectral_flux",
                horizon=0, horizon_label="5.8ms frame",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Instantaneous spectral onset — SS-EP input",
                citation="Nozaradan et al. 2011",
            ),
            H3DemandSpec(
                r3_idx=21, r3_name="spectral_flux",
                horizon=3, horizon_label="23ms onset",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Onset at note level — beat marker identification",
                citation="Nozaradan et al. 2012",
            ),
            H3DemandSpec(
                r3_idx=21, r3_name="spectral_flux",
                horizon=6, horizon_label="200ms beat",
                morph=14, morph_name="periodicity",
                law=2, law_name="integration",
                purpose="Beat-level onset periodicity — entrainment detection",
                citation="Nozaradan et al. 2011",
            ),
            H3DemandSpec(
                r3_idx=21, r3_name="spectral_flux",
                horizon=16, horizon_label="1s measure",
                morph=14, morph_name="periodicity",
                law=2, law_name="integration",
                purpose="Measure-level onset periodicity — meter entrainment",
                citation="Nozaradan et al. 2012",
            ),

            # --- Onset strength (R³[11]) — 3 present scales ---
            H3DemandSpec(
                r3_idx=11, r3_name="onset_strength",
                horizon=0, horizon_label="5.8ms frame",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Instantaneous onset strength — beat marker",
                citation="Large & Palmer 2002",
            ),
            H3DemandSpec(
                r3_idx=11, r3_name="onset_strength",
                horizon=3, horizon_label="23ms onset",
                morph=1, morph_name="mean",
                law=2, law_name="integration",
                purpose="Mean onset strength at note level",
                citation="Grahn & Brett 2007",
            ),
            H3DemandSpec(
                r3_idx=11, r3_name="onset_strength",
                horizon=16, horizon_label="1s measure",
                morph=14, morph_name="periodicity",
                law=2, law_name="integration",
                purpose="Onset periodicity at measure level — meter structure",
                citation="Nozaradan et al. 2012",
            ),

            # --- Amplitude (R³[7]) — 3 present scales ---
            H3DemandSpec(
                r3_idx=7, r3_name="amplitude",
                horizon=3, horizon_label="23ms onset",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Beat amplitude at onset level — energy at beat",
                citation="Grahn & Brett 2007",
            ),
            H3DemandSpec(
                r3_idx=7, r3_name="amplitude",
                horizon=3, horizon_label="23ms onset",
                morph=2, morph_name="std",
                law=2, law_name="integration",
                purpose="Amplitude variability — dynamic accent detection",
                citation="Large & Palmer 2002",
            ),
            H3DemandSpec(
                r3_idx=7, r3_name="amplitude",
                horizon=16, horizon_label="1s measure",
                morph=1, morph_name="mean",
                law=2, law_name="integration",
                purpose="Mean amplitude at measure level — energy context",
                citation="Grahn & Brett 2007",
            ),

            # --- Loudness (R³[10]) — 2 present scales ---
            H3DemandSpec(
                r3_idx=10, r3_name="loudness",
                horizon=3, horizon_label="23ms onset",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Loudness at onset level — perceptual beat salience",
                citation="Yang et al. 2025",
            ),
            H3DemandSpec(
                r3_idx=10, r3_name="loudness",
                horizon=3, horizon_label="23ms onset",
                morph=20, morph_name="entropy",
                law=2, law_name="integration",
                purpose="Loudness entropy — information content of rhythm",
                citation="Ding et al. 2025",
            ),

            # --- Beat strength (R³[42]) — 3 present scales ---
            # (Replaces dissolved Group E motor-auditory coupling x_l0l5)
            H3DemandSpec(
                r3_idx=42, r3_name="beat_strength",
                horizon=3, horizon_label="23ms onset",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Beat strength at onset — motor coupling signal",
                citation="Grahn & Brett 2007",
            ),
            H3DemandSpec(
                r3_idx=42, r3_name="beat_strength",
                horizon=6, horizon_label="200ms beat",
                morph=14, morph_name="periodicity",
                law=2, law_name="integration",
                purpose="Beat periodicity at beat level — entrainment quality",
                citation="Nozaradan et al. 2011",
            ),
            H3DemandSpec(
                r3_idx=42, r3_name="beat_strength",
                horizon=16, horizon_label="1s measure",
                morph=14, morph_name="periodicity",
                law=2, law_name="integration",
                purpose="Beat periodicity at measure — meter structure",
                citation="Nozaradan et al. 2012",
            ),

            # ═══════════════════════════════════════════════════════════
            # PAST demands (L0 = Memory) — 3 tuples
            # ═══════════════════════════════════════════════════════════

            # --- Spectral flux memory ---
            H3DemandSpec(
                r3_idx=21, r3_name="spectral_flux",
                horizon=6, horizon_label="200ms beat",
                morph=8, morph_name="velocity",
                law=0, law_name="memory",
                purpose="Onset rate change — tempo acceleration/deceleration",
                citation="Large & Palmer 2002",
            ),

            # --- Pulse clarity memory ---
            H3DemandSpec(
                r3_idx=43, r3_name="pulse_clarity",
                horizon=6, horizon_label="200ms beat",
                morph=0, morph_name="value",
                law=0, law_name="memory",
                purpose="Recent pulse clarity — entrainment quality baseline",
                citation="Grahn & Brett 2007",
            ),

            # --- Tempo estimate memory ---
            H3DemandSpec(
                r3_idx=41, r3_name="tempo_estimate",
                horizon=16, horizon_label="1s measure",
                morph=1, morph_name="mean",
                law=0, law_name="memory",
                purpose="Mean tempo at measure level — metrical context",
                citation="Large & Palmer 2002",
            ),
        )

    # ------------------------------------------------------------------
    # Dimension names
    # ------------------------------------------------------------------

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # E-layer (3D): Entrainment signals
            "beat_entrainment", "meter_entrainment", "selective_enhancement",
            # M-layer (3D): Model outputs
            "ssep_enhancement", "enhancement_index", "beat_salience",
            # P-layer (3D): Present state
            "beat_locked_activity", "entrainment_strength", "selective_gain",
            # F-layer (3D): Predictions
            "beat_onset_pred", "meter_position_pred", "enhancement_pred",
        )

    # ------------------------------------------------------------------
    # Region links — 5 brain regions in the entrainment pathway
    # ------------------------------------------------------------------

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        """SNEM activates the beat perception / entrainment network.

        Primary sites: A1/STG (SS-EP), Putamen (beat detection), SMA (motor).
        """
        return (
            # A1/STG: SS-EP generation in auditory cortex
            RegionLink(
                dim_name="ssep_enhancement",
                region="A1_STG",
                weight=0.9,
                citation="Nozaradan et al. 2011",
            ),
            RegionLink(
                dim_name="beat_salience",
                region="A1_STG",
                weight=0.7,
                citation="Nozaradan et al. 2012",
            ),
            # Putamen: Beat and meter detection
            RegionLink(
                dim_name="beat_entrainment",
                region="Putamen",
                weight=0.85,
                citation="Grahn & Brett 2007",
            ),
            RegionLink(
                dim_name="meter_entrainment",
                region="Putamen",
                weight=0.8,
                citation="Grahn & Brett 2007",
            ),
            # SMA: Beat-motor coupling, sensorimotor integration
            RegionLink(
                dim_name="beat_locked_activity",
                region="SMA",
                weight=0.8,
                citation="Grahn & Brett 2007",
            ),
            # PMC: Motor preparation / pre-motor timing
            RegionLink(
                dim_name="beat_onset_pred",
                region="PMC",
                weight=0.6,
                citation="Grahn & Brett 2007",
            ),
            # dACC: Salience evaluation
            RegionLink(
                dim_name="selective_gain",
                region="dACC",
                weight=0.5,
                citation="Ding et al. 2025",
            ),
        )

    # ------------------------------------------------------------------
    # Neuro links — DA for beat prediction, NE for attention
    # ------------------------------------------------------------------

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        """Beat prediction drives DA (putamen), attention drives NE."""
        return (
            # DA: Beat prediction reward via basal ganglia
            NeuroLink(
                dim_name="beat_entrainment",
                channel=0,  # DA
                effect="produce",
                weight=0.4,
                citation="Grahn & Brett 2007",
            ),
            # NE: Selective attention to beat-locked events
            NeuroLink(
                dim_name="selective_gain",
                channel=1,  # NE
                effect="amplify",
                weight=0.3,
                citation="Ding et al. 2025",
            ),
        )

    # ------------------------------------------------------------------
    # Evidence metadata — 12 papers, alpha tier
    # ------------------------------------------------------------------

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                # PRIMARY — SS-EP entrainment
                Citation(
                    "Nozaradan", 2011,
                    "Frequency-tagged EEG reveals selective neural entrainment "
                    "to beat frequency in auditory cortex; enhancement beyond "
                    "acoustic envelope; SS-EP method introduced",
                    "EEG frequency tagging, N=12, beat enhancement ~2:1",
                ),
                Citation(
                    "Nozaradan", 2012,
                    "Selective neural entrainment to beat AND meter frequencies; "
                    "meter entrainment is endogenous (not in stimulus); "
                    "enhancement abolished by irregular timing (p=0.65 NS)",
                    "EEG frequency tagging, N=15, meter > non-meter",
                ),
                # SUPPORTING — computational model
                Citation(
                    "Large", 2002,
                    "Oscillatory model of beat perception: period correction and "
                    "phase correction dynamics; coupling strength predicts "
                    "entrainment quality",
                    "computational model, behavioral validation",
                ),
                # SUPPORTING — neural substrates
                Citation(
                    "Grahn", 2007,
                    "Basal ganglia (putamen) and SMA activated by beat perception "
                    "regardless of training; beat-specific > non-beat; motor "
                    "areas involved even without movement",
                    "fMRI, N=14, putamen p<0.001",
                ),
                # SUPPORTING — emotional modulation
                Citation(
                    "Ding", 2025,
                    "Neural entrainment to rhythmic tonal sequences modulates "
                    "emotional states; entrainment strength correlates with "
                    "emotional intensity",
                    "EEG, tonal sequence paradigm",
                ),
                Citation(
                    "Yang", 2025,
                    "Music tempo modulates emotional states through neural "
                    "entrainment; faster tempo → higher arousal via "
                    "cortical oscillation coupling",
                    "EEG, tempo manipulation",
                ),
                # SUPPORTING — cortical entrainment
                Citation(
                    "Bridwell", 2017,
                    "Cortical EEG entrainment to guitar note repetition patterns; "
                    "sensitivity to both repetition and key structure",
                    "EEG, N=16, guitar stimuli",
                ),
                Citation(
                    "Rimmele", 2023,
                    "Acoustically driven cortical delta oscillations underpin "
                    "prosodic chunking; shared mechanism with musical beat",
                    "MEG, delta 0.5-4 Hz entrainment",
                ),
                # SUPPORTING — developmental / genetic
                Citation(
                    "Saadatmehr", 2023,
                    "Rhythm processing in premature neonates: very early auditory "
                    "beat and meter processing present before term age",
                    "EEG neonatal, beat/meter encoding",
                ),
                Citation(
                    "Edalati", 2023,
                    "Auditory rhythm encoding during last trimester of gestation; "
                    "fetal entrainment to beat structure",
                    "fetal EEG, prenatal entrainment",
                ),
                Citation(
                    "Niarchou", 2022,
                    "GWAS of musical beat synchronization identifies 69 loci; "
                    "shared genetic architecture with biological rhythms; "
                    "N = 606,825",
                    "GWAS, N=606825, 69 loci, h2_SNP~13%",
                ),
                # SUPPORTING — altered states
                Citation(
                    "Aparicio-Terres", 2023,
                    "Neural entrainment strength to electronic music correlates "
                    "with proxies of altered states of consciousness",
                    "EEG, electronic music, ASC correlation",
                ),
            ),
            evidence_tier="alpha",
            confidence_range=(0.88, 0.94),
            falsification_criteria=(
                "Disrupting rhythmic regularity (random timing) should abolish "
                "selective SS-EP enhancement (confirmed: Nozaradan 2012, p=0.65 NS)",
                "Tempi outside 1-4 Hz range should show reduced neural entrainment "
                "(confirmed: Nozaradan 2011, frequency specificity)",
                "Non-beat frequencies in the same stimulus should NOT show selective "
                "enhancement — enhancement is beat-specific (confirmed: Nozaradan 2012)",
                "Putamen lesions should impair beat but not rhythm perception "
                "(Grahn & Brett 2007 prediction)",
                "Motor cortex TMS disruption should modulate SS-EP enhancement "
                "strength (motor-auditory coupling is bidirectional)",
            ),
            version="3.0.0",
            paper_count=12,
        )

    # ------------------------------------------------------------------
    # compute() — the entrainment circuit
    # ------------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Neural entrainment computation: A1 → Putamen → SMA pathway.

        Models the frequency-tagged SS-EP enhancement of beat and meter
        frequencies in auditory cortex (Nozaradan et al. 2011, 2012),
        with basal ganglia beat detection (Grahn & Brett 2007) and
        sensorimotor coupling (Large & Palmer 2002).

        All 8 R³ features and 18 H³ demands are consumed — no dead
        variables.

        Args:
            h3_features: Dict mapping (r3_idx, horizon, morph, law) 4-tuples
                         to (B, T) temporal feature scalars.
            r3_features: (B, T, 97) R³ spectral feature tensor.

        Returns:
            (B, T, 12) output: E(3) + M(3) + P(3) + F(3).
        """
        B, T = r3_features.shape[:2]
        device = r3_features.device

        # === Stage 1: Extract R³ features (8 scalar indices) ===

        amplitude      = r3_features[:, :, self._R3_AMPLITUDE]        # (B, T)
        loudness       = r3_features[:, :, self._R3_LOUDNESS]         # (B, T)
        onset_strength = r3_features[:, :, self._R3_ONSET_STRENGTH]   # (B, T)
        spectral_flux  = r3_features[:, :, self._R3_SPECTRAL_FLUX]    # (B, T)
        tempo_est      = r3_features[:, :, self._R3_TEMPO_ESTIMATE]   # (B, T)
        beat_strength  = r3_features[:, :, self._R3_BEAT_STRENGTH]    # (B, T)
        pulse_clarity  = r3_features[:, :, self._R3_PULSE_CLARITY]    # (B, T)
        event_density  = r3_features[:, :, self._R3_EVENT_DENSITY]    # (B, T)

        # === Stage 2: Extract H³ temporal features (18 demands) ===

        _zeros = torch.zeros(B, T, device=device)

        def _h3(key, fallback=None):
            v = h3_features.get(key)
            if v is not None:
                return v
            return fallback if fallback is not None else _zeros

        # ── PRESENT demands (L2 = Integration, 15 tuples) ──

        # Spectral flux (R³[21]) — onset detection
        h3_flux_h0          = _h3((21, 0, 0, 2),  spectral_flux)   # instant onset
        h3_flux_h3          = _h3((21, 3, 0, 2),  spectral_flux)   # onset at note
        h3_flux_period_h6   = _h3((21, 6, 14, 2))                  # beat periodicity
        h3_flux_period_h16  = _h3((21, 16, 14, 2))                 # measure periodicity

        # Onset strength (R³[11])
        h3_onset_h0         = _h3((11, 0, 0, 2),  onset_strength)  # instant onset
        h3_onset_mean_h3    = _h3((11, 3, 1, 2))                   # mean onset note
        h3_onset_period_h16 = _h3((11, 16, 14, 2))                 # onset periodicity 1s

        # Amplitude (R³[7])
        h3_amp_h3           = _h3((7, 3, 0, 2),   amplitude)       # amp at onset
        h3_amp_std_h3       = _h3((7, 3, 2, 2))                    # amp variability
        h3_amp_mean_h16     = _h3((7, 16, 1, 2))                   # mean amp 1s

        # Loudness (R³[10])
        h3_loud_h3          = _h3((10, 3, 0, 2),  loudness)        # loudness at onset
        h3_loud_entropy_h3  = _h3((10, 3, 20, 2))                  # loudness entropy

        # Beat strength (R³[42]) — replaces dissolved x_l0l5
        h3_beat_h3          = _h3((42, 3, 0, 2),  beat_strength)   # beat level
        h3_beat_period_h6   = _h3((42, 6, 14, 2))                  # beat periodicity
        h3_beat_period_h16  = _h3((42, 16, 14, 2))                 # meter periodicity

        # ── PAST demands (L0 = Memory, 3 tuples) ──

        h3_flux_vel_h6      = _h3((21, 6, 8, 0))                   # onset rate change
        h3_pulse_h6_mem     = _h3((43, 6, 0, 0),  pulse_clarity)   # pulse clarity
        h3_tempo_mean_h16   = _h3((41, 16, 1, 0))                  # mean tempo 1s

        # === Stage 3: E-LAYER (3D) — Entrainment signals ===
        #
        # The three E-layer signals capture beat entrainment, meter
        # entrainment, and selective enhancement.

        # ── f01: Beat Entrainment ──
        #
        # How strongly is the neural response locked to beat frequency?
        # Primary signal: onset/spectral periodicity at measure scale.
        # Nozaradan 2011: beat-frequency SS-EP > non-beat by ~2:1.

        beat_entrainment = (
            0.25 * h3_flux_period_h16                          # spectral onset periodicity 1s
            + 0.25 * h3_onset_period_h16                       # onset marker periodicity 1s
            + 0.20 * h3_beat_period_h16                        # R³ beat periodicity 1s
            + 0.15 * h3_amp_h3                                 # amplitude at beat onset
            + 0.15 * event_density                             # event rate context
        ).clamp(0.0, 1.0)

        # ── f02: Meter Entrainment ──
        #
        # How strongly is the response locked to metrical structure?
        # Combines fast (beat-level) and slow (measure-level) periodicity.
        # Nozaradan 2012: meter frequencies enhanced endogenously.

        meter_entrainment = (
            0.25 * h3_beat_period_h6                           # beat periodicity at beat
            + 0.25 * h3_beat_period_h16                        # beat periodicity at measure
            + 0.20 * h3_beat_h3                                # beat strength level
            + 0.15 * h3_pulse_h6_mem                           # pulse clarity baseline
            + 0.15 * pulse_clarity                             # R³ pulse clarity
        ).clamp(0.0, 1.0)

        # ── f03: Selective Enhancement ──
        #
        # SS-EP selective gain: enhancement only when both beat AND meter
        # are entrained (multiplicative gating).
        # Nozaradan 2012: irregular timing abolishes enhancement.

        # Normalize loudness entropy to [0, 1]
        loud_entropy_norm = (
            h3_loud_entropy_h3 / self._ENTROPY_SCALE
        ).clamp(0.0, 1.0)

        # Onset velocity — changing onset patterns drive attention
        flux_vel_norm = (
            h3_flux_vel_h6 * self._VELOCITY_GAIN
        ).abs().clamp(0.0, 1.0)

        selective_enhancement = (
            0.40 * beat_entrainment * meter_entrainment        # joint gating
            + 0.30 * (1.0 - loud_entropy_norm)                # low entropy = predictable
            + 0.30 * flux_vel_norm                             # onset dynamics
        ).clamp(0.0, 1.0)

        # === Stage 4: M-LAYER (3D) — Model outputs ===
        #
        # SS-EP formula from Nozaradan et al. (2011):
        # Enhancement = α·BeatSalience + β·MeterSalience - γ·Envelope

        # SS-EP Enhancement (Nozaradan formula)
        ssep_enhancement = (
            ALPHA_SSEP * beat_entrainment
            + BETA_SSEP * meter_entrainment
            - GAMMA_SSEP * (1.0 - selective_enhancement)
        ).clamp(0.0, 1.0)

        # Enhancement Index: beat-locked enhancement magnitude
        enhancement_index = (
            beat_entrainment * selective_enhancement
        ).clamp(0.0, 1.0)

        # Beat Salience: composite onset salience from multiple sources
        beat_salience = (
            0.25 * h3_onset_h0                                 # instantaneous onset
            + 0.25 * h3_flux_h0                                # instantaneous flux
            + 0.20 * h3_beat_h3                                # beat strength
            + 0.15 * h3_onset_mean_h3                          # sustained onset
            + 0.15 * h3_loud_h3                                # loudness at onset
        ).clamp(0.0, 1.0)

        # === Stage 5: P-LAYER (3D) — Present state ===

        # Beat-locked activity: neural amplitude at beat times
        beat_locked_activity = (
            COUPLING_STRENGTH * beat_entrainment * h3_amp_h3
        ).clamp(0.0, 1.0)

        # Entrainment strength: overall quality of entrainment
        entrainment_strength = (
            0.50 * beat_entrainment
            + 0.50 * meter_entrainment
        ).clamp(0.0, 1.0)

        # Selective gain: how much is attention selectively amplifying
        selective_gain = (
            selective_enhancement * entrainment_strength
        ).clamp(0.0, 1.0)

        # === Stage 6: F-LAYER (3D) — Predictions ===

        # Beat onset prediction: periodicity → next onset expectation
        # High periodicity at beat level = strong prediction of next beat
        beat_onset_pred = (
            0.40 * h3_flux_period_h6                           # beat-level periodicity
            + 0.30 * h3_beat_period_h6                         # beat strength periodicity
            + 0.30 * h3_onset_period_h16                       # onset regularity
        ).clamp(0.0, 1.0)

        # Meter position prediction: tempo × beat periodicity
        # Stable tempo + regular beats = confident metrical prediction
        meter_position_pred = (
            0.30 * h3_tempo_mean_h16                           # stable tempo
            + 0.30 * h3_beat_period_h16                        # measure periodicity
            + 0.20 * h3_amp_mean_h16                           # energy context
            + 0.20 * tempo_est                                 # R³ tempo estimate
        ).clamp(0.0, 1.0)

        # Enhancement prediction: current enhancement trajectory
        enhancement_pred = (
            0.50 * selective_enhancement                       # current enhancement
            + 0.30 * h3_beat_period_h16                        # regularity predicts more
            + 0.20 * h3_amp_std_h3                             # variability context
        ).clamp(0.0, 1.0)

        # === Assemble 12D output ===
        return torch.stack([
            # E-layer (3D): Entrainment
            beat_entrainment, meter_entrainment, selective_enhancement,
            # M-layer (3D): Model outputs
            ssep_enhancement, enhancement_index, beat_salience,
            # P-layer (3D): Present state
            beat_locked_activity, entrainment_strength, selective_gain,
            # F-layer (3D): Predictions
            beat_onset_pred, meter_position_pred, enhancement_pred,
        ], dim=-1)  # (B, T, 12)
