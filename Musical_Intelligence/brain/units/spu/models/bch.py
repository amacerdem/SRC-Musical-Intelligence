"""BCH -- Brainstem Consonance Hierarchy.

Unit: SPU | Tier: alpha-1 | Output: 12D

==========================================================================
NEURAL CIRCUIT
==========================================================================

The Brainstem Consonance Hierarchy models how frequency-following responses
(FFR) in the brainstem preferentially encode consonant musical intervals
over dissonant ones. This is one of the most direct neural correlates of
consonance perception, emerging at the earliest stage of auditory hierarchy
— before cortical processing.

Pathway:
    Musical interval (stimulus)
        → Auditory Nerve (70-fiber AN population, phase-locked to harmonics)
        → Inferior Colliculus (FFR generator, rostral brainstem)
        → Primary Auditory Cortex (Heschl's Gyrus, phase-locked dissonance)
        → Superior Temporal Gyrus (high gamma 70-150 Hz dissonance tracking)

Three computational components:

    1. HARMONICITY (Spectral)
       Region: Auditory Nerve
       Mechanism: Harmonic template matching
       Evidence: r = 0.81 (Bidelman & Krishnan 2009)
       Function: "How harmonic is this signal?"

    2. NEURAL PITCH SALIENCE (Temporal)
       Region: Inferior Colliculus
       Mechanism: Frequency-following response magnitude
       Evidence: 70-fiber AN model (Bidelman & Heinz 2011)
       Function: "How clear is this pitch?"

    3. FFR-BEHAVIOR CORRELATION (Bridge)
       Region: IC → Cortex → Perception
       Mechanism: Bottom-up neural encoding predicts behavioral ratings
       Evidence: r = 0.81, p < 0.01 (Bidelman & Krishnan 2009)
       Function: "NPS predicts consonance ratings"

==========================================================================
KEY INSIGHT
==========================================================================

Harmonicity is the PRIMARY predictor of perceived consonance (McDermott
et al. 2010), though roughness contributes independently. Bidelman &
Heinz (2011) showed AN population responses predict the full consonance
hierarchy from peripheral encoding alone.

==========================================================================
CRITICAL QUALIFICATION (Cousineau et al. 2015)
==========================================================================

The NPS-behavior correlation (r = 0.81, Bidelman 2009) was obtained with
SYNTHETIC complex tones (6 equal-amplitude harmonics). Cousineau et al.
(2015) showed this correlation drops to non-significant for natural sounds
(sax: r = 0.24 NS; voice: r = -0.10 NS). NPS also correlates with
roughness (r = -0.57), complicating its interpretation as a pure
harmonicity measure.

The model retains alpha-tier because:
  (1) The neural hierarchy IS universal (confirmed in infants, animals)
  (2) AN modeling confirms peripheral encoding suffices (Bidelman & Heinz 2011)
  (3) The limitation is about the NPS MEASURE, not the underlying mechanism

==========================================================================
CONSONANCE HIERARCHY (Neural Evidence)
==========================================================================

    Interval       Ratio    NPS (norm)   Rank   Harmonicity
    P1 (unison)    1:1      1.00         1      1.00
    P5 (fifth)     3:2      0.95         2      ~0.90
    P4 (fourth)    4:3      0.90         3      ~0.85
    M3 (third)     5:4      0.85         4      ~0.80
    m6 (minor 6th) 8:5      0.75         5      ~0.65
    TT (tritone)   45:32    0.50         6      ~0.20

Cross-cultural: Neural (FFR) hierarchy is UNIVERSAL — same across cultures.
Behavioral ratings VARY by culture. BCH models the neural level.

==========================================================================
INTRA-UNIT AND CROSS-UNIT PATHWAYS
==========================================================================

    Intra-SPU:
        BCH.f01_nps           → PSCL (cortical pitch salience input)
        BCH.f02_harmonicity   → PCCR (chroma tuning from harmonicity)
        BCH.consonance_signal → STAI (aesthetic evaluation input)
        BCH.f01_nps           → SDED (early roughness baseline)

    Cross-unit P1 (SPU → ARU):
        BCH.consonance_signal → ARU.SRP (consonance → opioid proxy)
        BCH.f02_harmonicity   → ARU.SRP (harmonicity → pleasure)

    Cross-unit P2 (SPU → IMU):
        BCH.consonance_signal → IMU.MEAMN (consonance → memory binding)

Version: 3.0.0 (Building Phase: gold standard implementation from BCH.md)
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional, Tuple

import torch

from .....contracts.bases.base_model import BaseModel
from .....contracts.dataclasses import (
    BrainRegion,
    Citation,
    H3DemandSpec,
    LayerSpec,
    ModelMetadata,
)

if TYPE_CHECKING:
    from torch import Tensor


class BCH(BaseModel):
    """Brainstem Consonance Hierarchy.

    SPU-alpha1 | 12D | No mechanisms — direct R³ + H³ computation

    Models brainstem frequency-following responses (FFR) that preferentially
    encode consonant musical intervals. The neural consonance hierarchy
    (P1 > P5 > P4 > M3 > m6 > TT) emerges from peripheral auditory encoding
    and predicts behavioral consonance ratings with r = 0.81 for synthetic
    stimuli (Bidelman & Krishnan 2009).

    Architecture (mechanism-free):
        R³ reads (spectral features, per frame):
            A: Consonance [0:7]     — roughness, sethares, helmholtz, stumpf,
                                      pleasantness, inharmonicity, harmonic_dev
            C: Timbre [14,17,18:21] — tonalness, autocorr, tristimulus 1/2/3
            E: Interactions [41:49] — x_l5l7 consonance × timbre coupling

        H³ reads (temporal features, multi-scale):
            17 tuples at H0 (25ms, gamma), H3 (100ms, alpha-beta),
            H6 (200ms, syllable) — brainstem processing timescales

        Derived intermediate signals (replace former PPC mechanism):
            brainstem_pitch_encoding — from H³ consonance features at H0
            harmonic_template_match  — from H³ consonance features at H3

        Every computation traces directly to R³/H³ features. No opaque
        mechanism aggregation. Every variable has a citation.

    Evidence: alpha-tier (direct neural measurement via FFR)
    Confidence: 90-95%
    """

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    NAME = "BCH"
    FULL_NAME = "Brainstem Consonance Hierarchy"
    UNIT = "SPU"
    TIER = "alpha"
    OUTPUT_DIM = 12
    CROSS_UNIT_READS: Tuple = ()

    # ------------------------------------------------------------------
    # Scientific constants — each cites its source
    # ------------------------------------------------------------------

    # NPS weight for f01 computation
    # Bidelman & Krishnan 2009: r = 0.81 correlation in 10 non-musicians
    ALPHA = 0.90

    # Harmonicity weight for f02 computation
    # Bidelman 2013: harmonicity > roughness as consonance predictor
    BETA = 0.85

    # Hierarchy weight for f03 computation
    # Bidelman & Heinz 2011: AN population predicts full hierarchy
    GAMMA = 0.80

    # FFR-behavior correlation coefficient
    # Bidelman & Krishnan 2009: r = 0.81, p < 0.01, N=10, synthetic tones
    # Cousineau et al. 2015: r = 0.34 replication (synthetic), NS for natural
    FFR_BEHAVIOR_CORR = 0.81

    # Cortical roughness encoding (STG high gamma)
    # Foo et al. 2016: RH r = 0.43, LH r = 0.41
    CORTICAL_ROUGHNESS_R = 0.43

    # POR latency advantage for consonant stimuli
    # Tabas et al. 2019: up to 36ms faster for consonant dyads
    POR_LATENCY_ADVANTAGE_MS = 36

    # NPS-roughness correlation (potential confound)
    # Cousineau et al. 2015: r = -0.57 to -0.64
    NPS_ROUGHNESS_CORR = -0.57

    # Brainstem pitch encoding weights (replaces former PPC mechanism)
    # These weights combine H³ consonance features at gamma rate (H0=25ms)
    # to compute "pitch salience" — how strongly the brainstem encodes pitch.
    # Helmholtz (integer ratio) + Stumpf (tonal fusion) are the primary
    # brainstem consonance correlates (Bidelman 2013).
    PITCH_ENCODING_W_HELMHOLTZ = 0.4   # Integer ratio detection weight
    PITCH_ENCODING_W_STUMPF = 0.3      # Tonal fusion weight
    PITCH_ENCODING_W_INV_ROUGH = 0.3   # Inverse roughness weight

    # ------------------------------------------------------------------
    # Output layers — from BCH.md Section 6
    # ------------------------------------------------------------------

    LAYERS: Tuple[LayerSpec, ...] = (
        # Layer E: Explicit Features (4D)
        # Direct neural encoding measures
        LayerSpec("E", "Extraction", 0, 4, (
            "f01_nps",            # Neural Pitch Salience (FFR magnitude)
            "f02_harmonicity",    # Harmonicity Index (coincidence ratio)
            "f03_hierarchy",      # Consonance Hierarchy ranking
            "f04_ffr_behavior",   # FFR-Behavior Correlation proxy (r=0.81)
        )),
        # Layer M: Mathematical Model Outputs (2D)
        # Computed mathematical quantities
        LayerSpec("M", "Mechanism", 4, 6, (
            "nps_t",              # NPS at time t: FFR magnitude at fundamental
            "harm_interval",      # Harmonicity of current interval
        )),
        # Layer P: Present Processing (3D)
        # Current consonance state
        LayerSpec("P", "Psychological", 6, 9, (
            "consonance_signal",  # Phase-locked consonance: 1-(roughness+sethares)/2
            "template_match",     # Harmonic template match strength (PPC aggregation)
            "neural_pitch",       # Neural pitch strength (PPC aggregation)
        )),
        # Layer F: Future Predictions (3D)
        # Forward-looking consonance expectations
        LayerSpec("F", "Forecast", 9, 12, (
            "consonance_pred",    # Behavioral consonance prediction from f02+f04
            "pitch_propagation",  # FFR → cortical pitch propagation signal
            "interval_expect",    # Next interval prediction from H3 trends
        )),
    )

    # ------------------------------------------------------------------
    # H³ Temporal Demand — 16 tuples from BCH.md Section 5.1
    # ------------------------------------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        """17 H³ tuples across three brainstem horizons.

        Horizons:
            H0 = 25ms  (gamma rate, phase-locking instantaneous)
            H3 = 100ms (alpha-beta, FFR integration window)
            H6 = 200ms (syllable rate, consonance interval evaluation)

        These correspond to brainstem processing timescales:
            - H0 captures instantaneous phase-locking (AN → IC)
            - H3 captures FFR integration (Bidelman 2009 recording window)
            - H6 captures harmonic evaluation period (~200ms consonance window)

        Morph indices follow canonical MORPH_NAMES in morphs.py:
            M0  = value (instantaneous)
            M1  = mean (windowed average)
            M14 = periodicity (harmonic recurrence)
            M18 = trend (directional change)

        Law indices:
            L0 = forward (causal memory)
            L2 = bidirectional (integration)
        """
        return (
            # --- Consonance group A: roughness tracking ---
            # Roughness is the inverse of consonance; dissonant intervals
            # produce more beating = higher roughness (Plomp & Levelt 1965)
            H3DemandSpec(
                0, "roughness_sethares", 0, "25ms", 0, "value", 2, "bidi",
                "Instantaneous dissonance (roughness at gamma rate)",
                "Plomp & Levelt 1965"),
            H3DemandSpec(
                0, "roughness_sethares", 3, "100ms", 1, "mean", 2, "bidi",
                "Mean dissonance over FFR window (100ms integration)",
                "Bidelman & Krishnan 2009"),
            H3DemandSpec(
                0, "roughness_sethares", 6, "200ms", 18, "trend", 0, "fwd",
                "Dissonance trajectory over syllable window",
                "Tabas et al. 2019"),

            # --- Consonance group A: harmonic template matching ---
            # Helmholtz-Kang measures integer ratio detection;
            # higher = more consonant interval (Helmholtz 1863, Kang 2009)
            H3DemandSpec(
                2, "helmholtz_kang", 0, "25ms", 0, "value", 2, "bidi",
                "Instantaneous consonance (integer ratio detection)",
                "Helmholtz 1863; Kang 2009"),
            H3DemandSpec(
                2, "helmholtz_kang", 3, "100ms", 1, "mean", 2, "bidi",
                "Mean consonance over FFR window",
                "Bidelman & Heinz 2011"),

            # --- Consonance group A: tonal fusion ---
            # Stumpf fusion = perceptual blending of simultaneous tones
            # High fusion → consonant (Stumpf 1890)
            H3DemandSpec(
                3, "stumpf_fusion", 0, "25ms", 0, "value", 2, "bidi",
                "Instantaneous tonal fusion strength",
                "Stumpf 1890"),
            H3DemandSpec(
                3, "stumpf_fusion", 3, "100ms", 1, "mean", 2, "bidi",
                "Mean tonal fusion over FFR integration window — "
                "used in harmonic_template_match computation",
                "Stumpf 1890; Bidelman 2013"),
            H3DemandSpec(
                3, "stumpf_fusion", 6, "200ms", 1, "mean", 0, "fwd",
                "Sustained fusion over harmonic evaluation window",
                "Stumpf 1890"),

            # --- Consonance group A: inharmonicity ---
            # Deviation from harmonic series; inverse relates to consonance
            # (Fletcher 1934)
            H3DemandSpec(
                5, "inharmonicity", 0, "25ms", 0, "value", 2, "bidi",
                "Instantaneous inharmonicity (harmonic series deviation)",
                "Fletcher 1934"),
            H3DemandSpec(
                5, "inharmonicity", 3, "100ms", 18, "trend", 0, "fwd",
                "Inharmonicity trajectory over FFR window",
                "Bidelman 2013"),

            # --- Consonance group A: harmonic deviation ---
            # Energy variance in partials (Jensen 1999)
            H3DemandSpec(
                6, "harmonic_deviation", 0, "25ms", 0, "value", 2, "bidi",
                "Instantaneous harmonic deviation (partial energy variance)",
                "Jensen 1999"),
            H3DemandSpec(
                6, "harmonic_deviation", 3, "100ms", 1, "mean", 0, "fwd",
                "Mean harmonic deviation over FFR window",
                "Jensen 1999"),

            # --- Timbre group C: fundamental strength ---
            # Tristimulus1 = F0 energy / total energy
            # Higher F0 energy → clearer pitch → more harmonic → more consonant
            # (Pollard & Jansson 1982)
            H3DemandSpec(
                18, "tristimulus1", 0, "25ms", 0, "value", 2, "bidi",
                "Fundamental (F0) energy ratio — pitch clarity proxy",
                "Pollard & Jansson 1982"),
            H3DemandSpec(
                19, "tristimulus2", 0, "25ms", 0, "value", 2, "bidi",
                "Mid-harmonic (H2-H4) energy — spectral balance",
                "Pollard & Jansson 1982"),
            H3DemandSpec(
                20, "tristimulus3", 0, "25ms", 0, "value", 2, "bidi",
                "High-harmonic (H5+) energy — brightness component",
                "Pollard & Jansson 1982"),

            # --- Interaction group E: cross-band coherence ---
            # x_l5l7 = consonance × timbre coupling
            # Consonant intervals show higher cross-frequency coupling
            H3DemandSpec(
                41, "x_l5l7_0", 3, "100ms", 0, "value", 2, "bidi",
                "Consonance-timbre coupling at FFR window",
                "Trulla, Di Stefano & Giuliani 2018"),
            H3DemandSpec(
                41, "x_l5l7_0", 6, "200ms", 14, "periodicity", 2, "bidi",
                "Harmonic periodicity in consonance-timbre interaction",
                "Trulla, Di Stefano & Giuliani 2018"),
        )

    # ------------------------------------------------------------------
    # Dimension names — semantic, from BCH.md Section 6
    # ------------------------------------------------------------------

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # Layer E: Explicit Features (4D)
            "f01_nps",            # [0] Neural Pitch Salience
            "f02_harmonicity",    # [1] Harmonicity Index
            "f03_hierarchy",      # [2] Consonance Hierarchy ranking
            "f04_ffr_behavior",   # [3] FFR-Behavior Correlation
            # Layer M: Mathematical (2D)
            "nps_t",              # [4] NPS at time t
            "harm_interval",      # [5] Harmonicity of current interval
            # Layer P: Present (3D)
            "consonance_signal",  # [6] Phase-locked consonance signal
            "template_match",     # [7] Harmonic template match strength
            "neural_pitch",       # [8] Neural pitch strength
            # Layer F: Future (3D)
            "consonance_pred",    # [9]  Behavioral consonance prediction
            "pitch_propagation",  # [10] FFR → cortical propagation
            "interval_expect",    # [11] Next interval prediction
        )

    # ------------------------------------------------------------------
    # Brain regions — from BCH.md Section 8
    # ------------------------------------------------------------------

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        """Six brain regions involved in the BCH pathway.

        The pathway flows bottom-up from peripheral auditory nerve through
        brainstem (IC) to cortical regions (HG, STG). BCH primarily models
        brainstem processing; cortical regions are the downstream targets.
        """
        return (
            BrainRegion(
                "Auditory Nerve", "AN", "bilateral",
                (0, 0, 0), 0,  # Peripheral — no MNI coordinates
                "Phase-locked encoding, 70-fiber AN population model. "
                "Consonant > dissonant pitch salience ranking. "
                "Source: Bidelman & Heinz 2011"),
            BrainRegion(
                "Inferior Colliculus", "IC", "bilateral",
                (0, -32, -8), 0,
                "FFR generator (rostral brainstem). NPS computed here: "
                "P1 > P5 > P4 > M3 > m6 > TT hierarchy. "
                "r = 0.81 with behavioral consonance ratings. "
                "Source: Bidelman & Krishnan 2009"),
            BrainRegion(
                "Cochlear Nucleus", "CN", "bilateral",
                (10, -38, -40), 0,
                "Early spectral processing, tonotopic organization. "
                "Source: Cousineau et al. 2015"),
            BrainRegion(
                "Auditory Brainstem", "AB", "bilateral",
                (0, -30, -10), 0,
                "Harmonic encoding site. 8 direct mentions in evidence. "
                "Source: Bidelman & Krishnan 2009"),
            BrainRegion(
                "Heschl's Gyrus", "HG", "bilateral",
                (44, -18, 8), 41,
                "Primary auditory cortex (A1). Phase-locked dissonance "
                "representation. POR latency up to 36ms faster for consonant "
                "dyads. Sources: Fishman et al. 2001; Tabas et al. 2019"),
            BrainRegion(
                "Superior Temporal Gyrus", "STG", "bilateral",
                (58, -22, 4), 22,
                "High gamma (70-150 Hz) increase for dissonant chords at "
                "75-200ms. Roughness correlation: RH r=0.43, LH r=0.41. "
                "Spatial organization: p=0.003 (y), p=0.006 (z). "
                "Source: Foo et al. 2016"),
        )

    # ------------------------------------------------------------------
    # Metadata — all 13 papers from BCH.md Section 13
    # ------------------------------------------------------------------

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                # --- Primary evidence: brainstem consonance ---
                Citation(
                    "Bidelman", 2009,
                    "Neural correlates of consonance, dissonance, and the "
                    "hierarchy of musical pitch in the human brainstem",
                    "FFR recording, dichotic, N=10 non-musicians. "
                    "NPS-behavior: r=0.81, p<0.01. Primary coefficient "
                    "for f04_ffr_behavior."),
                Citation(
                    "Bidelman", 2013,
                    "The role of the auditory brainstem in processing "
                    "musically relevant pitch",
                    "Review. Harmonicity > roughness as consonance predictor. "
                    "Subcortical hierarchy mirrors Western music theory."),
                Citation(
                    "Bidelman", 2011,
                    "Auditory-nerve responses predict pitch attributes "
                    "related to musical consonance-dissonance for normal "
                    "and impaired hearing",
                    "AN computational model, 70 fibers (simulated). "
                    "AN population predicts full consonance hierarchy. "
                    "f03_hierarchy: peripheral encoding suffices."),
                Citation(
                    "Cousineau", 2015,
                    "On the relevance of natural stimuli for the study of "
                    "brainstem correlates: The example of consonance perception",
                    "FFR, dichotic, N=14. NPS-behavior: r=0.34 (synthetic), "
                    "NS for natural sounds (sax r=0.24, voice r=-0.10). "
                    "NPS-roughness: r=-0.57. CRITICAL QUALIFIER: NPS is "
                    "stimulus-dependent, not a universal correlate."),
                Citation(
                    "Lee", 2009,
                    "Selective subcortical enhancement of musical intervals "
                    "in musicians",
                    "FFR, musicians vs non-musicians. Enhanced brainstem "
                    "phase-locking for consonant intervals in musicians. "
                    "PLASTICITY: training refines subcortical encoding."),

                # --- Supporting evidence: cortical consonance ---
                Citation(
                    "Fishman", 2001,
                    "Consonance and dissonance of musical chords: Neural "
                    "correlates in auditory cortex of monkeys and humans",
                    "Intracranial AEP/MUA/CSD, 3 monkeys + 2 humans. "
                    "Phase-locked oscillatory activity in A1 correlates "
                    "with perceived dissonance."),
                Citation(
                    "Foo", 2016,
                    "Differential processing of consonance and dissonance "
                    "within the human superior temporal gyrus",
                    "ECoG bilateral STG, N=8. High gamma (70-150 Hz) for "
                    "dissonant chords 75-200ms. RH roughness r=0.43, "
                    "LH r=0.41. Spatial: p=0.003(y), p=0.006(z)."),
                Citation(
                    "Tabas", 2019,
                    "Modeling and MEG evidence of early consonance processing "
                    "in auditory cortex",
                    "MEG + computational model, N=14. POR latency for "
                    "dissonant dyads up to 36ms longer than consonant."),
                Citation(
                    "Crespo-Bojorque", 2018,
                    "Early neural responses underlie advantages for "
                    "consonance over dissonance",
                    "ERP (MMN) oddball, N=40 (20 musicians + 20 non). "
                    "Consonant→dissonant: MMN in all. Dissonant→consonant: "
                    "late MMN only in musicians. Pre-attentive advantage."),
                Citation(
                    "Schon", 2005,
                    "Sensory consonance: An ERP study",
                    "N1-P2-N2 modulated by consonance in musicians. "
                    "N2 modulation in non-musicians. Harmonic > melodic. "
                    "Expertise modulation of cortical consonance processing."),

                # --- Behavioral & computational ---
                Citation(
                    "McDermott", 2010,
                    "Individual differences reveal the basis of consonance",
                    "Behavioral (psychoacoustic), large sample. Consonance "
                    "preference correlates with harmonicity preference "
                    "(not roughness). BEHAVIORAL FOUNDATION."),
                Citation(
                    "Trulla", 2018,
                    "Computational approach to musical consonance "
                    "and dissonance",
                    "Computational (RQA). Recurrence peaks match just "
                    "intonation ratios. Devil's staircase pattern. "
                    "Mode-locking links to consonance hierarchy."),
                Citation(
                    "Terhardt", 1974,
                    "Pitch, consonance, and harmony",
                    "Psychoacoustic theory. Virtual pitch computation. "
                    "Roughness from periodic sound fluctuations. "
                    "NPS computation basis."),
            ),
            evidence_tier="alpha",
            confidence_range=(0.90, 0.95),
            falsification_criteria=(
                # From BCH.md Section 10
                "Pure tones: FFR should NOT show consonance effects "
                "(CONFIRMED — only complex tones)",
                "Non-Western listeners: neural hierarchy should be same, "
                "behavioral may differ (CONFIRMED — universal neural basis)",
                "Hearing impairment: should show altered consonance hierarchy "
                "(TESTABLE)",
                "Harmonic removal: removing harmonics should reduce NPS "
                "(TESTABLE)",
                "Brainstem lesions: should abolish FFR consonance effects "
                "(TESTABLE)",
            ),
            version="3.0.0",
        )

    # ------------------------------------------------------------------
    # H³ helper
    # ------------------------------------------------------------------

    def _h3_get(
        self,
        h3_features: Dict[Tuple[int, int, int, int], "Tensor"],
        key: Tuple[int, int, int, int],
        B: int, T: int, device: "torch.device",
    ) -> "Tensor":
        """Fetch a single H³ feature, fallback to 0.5 if unavailable.

        H³ features are sparse — not all 4-tuples may be computed by
        the H³ pipeline for a given audio input. Fallback to 0.5 (neutral)
        ensures graceful degradation.

        Args:
            h3_features: Dict mapping (r3_idx, horizon, morph, law) → (B, T).
            key: The 4-tuple to look up.
            B: Batch size.
            T: Time frames.
            device: Tensor device.

        Returns:
            (B, T) scalar tensor.
        """
        if key in h3_features:
            return h3_features[key]
        return torch.full((B, T), 0.5, device=device)

    # ------------------------------------------------------------------
    # Computation — from BCH.md Sections 7 + 11
    # ------------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], "Tensor"],
        r3_features: "Tensor",
        cross_unit_inputs: Optional[Dict[str, "Tensor"]] = None,
    ) -> "Tensor":
        """Compute BCH 12D output per the brainstem consonance hierarchy.

        Architecture (mechanism-free, direct R³ + H³):

            INPUT:
                R³ features (per-frame spectral):
                    A: Consonance [0:7]    — roughness, sethares, helmholtz,
                                             stumpf, pleasantness, inharmonicity,
                                             harmonic_deviation
                    C: Timbre [14,17:21]   — tonalness, autocorr, tristimulus
                    E: Interactions [41:49] — x_l5l7 cross-band coupling
                H³ features (17 tuples, multi-scale temporal):
                    H0 (25ms, gamma)       — instantaneous brainstem encoding
                    H3 (100ms, alpha-beta) — FFR integration window
                    H6 (200ms, syllable)   — harmonic evaluation period

            DERIVED INTERMEDIATE SIGNALS:
                brainstem_pitch_encoding — weighted combination of H³
                    consonance features at gamma rate (H0=25ms), replacing
                    the former PPC.pitch_salience[0:10] mechanism section.
                    Components: helmholtz_instant × 0.4 + stumpf_instant × 0.3
                    + (1-roughness_instant) × 0.3
                    (Bidelman 2013: harmonicity > roughness)

                harmonic_template_match — weighted combination of H³
                    consonance features at FFR window (H3=100ms), replacing
                    the former PPC.consonance_encoding[10:20] mechanism section.
                    Components: helmholtz_mean_100ms × 0.5 + stumpf_mean_100ms
                    × 0.3 + (1-roughness_mean_100ms) × 0.2
                    (Bidelman & Heinz 2011: AN template matching)

            COMPUTATION:
                Layer E: f01_nps, f02_harmonicity, f03_hierarchy, f04_ffr
                Layer M: nps_t, harm_interval
                Layer P: consonance_signal, template_match, neural_pitch
                Layer F: consonance_pred, pitch_propagation, interval_expect

            OUTPUT:
                (B, T, 12) tensor in [0, 1]

        Scientific basis for each computation is documented inline.
        Every variable traces to a specific R³ index or H³ tuple with citation.
        """
        B, T, _ = r3_features.shape
        device = r3_features.device

        # ================================================================
        # R³ SPECTRAL FEATURES — from BCH.md Section 4.1
        # ================================================================

        # --- Group A: Consonance [0:7] ---
        # These 7 features capture different facets of sensory consonance.
        # BCH reads ALL 7 — this is the consonance foundation model.
        roughness = r3_features[..., 0:1]        # Plomp & Levelt 1965
        sethares = r3_features[..., 1:2]         # Sethares 1999
        helmholtz = r3_features[..., 2:3]        # Helmholtz 1863, Kang 2009
        stumpf = r3_features[..., 3:4]           # Stumpf 1890 tonal fusion
        # r3[4] = sensory_pleasantness            (available but not primary)
        inharmonicity = r3_features[..., 5:6]    # Fletcher 1934
        # r3[6] = harmonic_deviation              (used via H³ tuples, not directly)

        # --- Group C: Timbre [12:21] ---
        # Tonalness and tristimulus inform harmonic structure.
        # High tonalness = strong harmonic series → more consonant.
        # Balanced tristimulus = harmonic energy distributed normally.
        tonalness = r3_features[..., 14:15]      # Harmonic-to-noise ratio
        autocorr = r3_features[..., 17:18]       # Harmonic periodicity
        trist1 = r3_features[..., 18:19]         # F0 energy (Pollard 1982)
        trist2 = r3_features[..., 19:20]         # H2-H4 energy (mid harmonics)
        trist3 = r3_features[..., 20:21]         # H5+ energy (high harmonics)

        # Group E: Interactions [41:49] — x_l5l7 consonance × timbre coupling
        # Accessed via H³ tuples (41, 3, 0, 2) and (41, 6, 14, 2) below,
        # not as a raw R³ tensor.

        # ================================================================
        # H³ TEMPORAL FEATURES — fetch with neutral fallback
        # Keys: (r3_idx, horizon, morph, law)
        # ================================================================

        # Helper: fetch H³ scalar → (B, T, 1) for concatenation
        def h3(key: Tuple[int, int, int, int]) -> "Tensor":
            return self._h3_get(h3_features, key, B, T, device).unsqueeze(-1)

        # ================================================================
        # DERIVED INTERMEDIATE SIGNALS
        # These replace the former PPC mechanism sub-sections.
        # Instead of an opaque 30D mechanism output, we compute
        # transparent, citable intermediate signals from H³ features.
        # ================================================================

        # --- brainstem_pitch_encoding ---
        # Replaces: PPC.pitch_salience[0:10].mean()
        # What it represents: How strongly the brainstem encodes pitch
        # at the gamma rate (25ms). This is the FFR strength signal.
        #
        # Components at H0 (25ms, gamma):
        #   helmholtz_instant: integer ratio detection (Helmholtz 1863)
        #   stumpf_instant: tonal fusion (Stumpf 1890)
        #   inv_roughness_instant: inverse dissonance (Plomp & Levelt 1965)
        #
        # Weighting: Bidelman 2013 showed harmonicity (helmholtz) is the
        # primary brainstem consonance predictor, so it gets highest weight.
        helmholtz_instant = h3((2, 0, 0, 2))    # Consonance at gamma rate
        stumpf_instant = h3((3, 0, 0, 2))       # Fusion at gamma rate
        roughness_instant = h3((0, 0, 0, 2))    # Dissonance at gamma rate

        brainstem_pitch_encoding = (
            self.PITCH_ENCODING_W_HELMHOLTZ * helmholtz_instant
            + self.PITCH_ENCODING_W_STUMPF * stumpf_instant
            + self.PITCH_ENCODING_W_INV_ROUGH * (1.0 - roughness_instant)
        )

        # --- harmonic_template_match ---
        # Replaces: PPC.consonance_encoding[10:20].mean()
        # What it represents: How well the current spectrum matches a
        # harmonic template over the FFR integration window (100ms).
        #
        # Components at H3 (100ms, alpha-beta):
        #   helmholtz_mean_100ms: sustained integer ratio detection
        #   stumpf_mean_100ms: sustained tonal fusion
        #   inv_roughness_mean_100ms: sustained low dissonance
        #
        # Evidence: Bidelman & Heinz 2011 — AN population harmonic
        # template matching over ~100ms integration window predicts
        # the full consonance hierarchy.
        helmholtz_mean_100ms = h3((2, 3, 1, 2))   # Consonance mean at FFR
        stumpf_mean_100ms = h3((3, 3, 1, 2))      # Fusion mean at FFR
        roughness_mean_100ms = h3((0, 3, 1, 2))   # Dissonance mean at FFR

        harmonic_template_match = (
            0.5 * helmholtz_mean_100ms
            + 0.3 * stumpf_mean_100ms
            + 0.2 * (1.0 - roughness_mean_100ms)
        )

        # ================================================================
        # LAYER E: EXPLICIT FEATURES (4D)
        # Direct neural encoding measures from brainstem
        # ================================================================

        # --- f01: Neural Pitch Salience ---
        # NPS = FFR magnitude at fundamental frequency.
        # Brainstem encoding strength of periodic (pitched) signals.
        # High tonalness × high autocorrelation × strong brainstem encoding
        # → strong NPS → consonant interval.
        #
        # Formula:
        #   f01 = sigma(alpha * tonalness * autocorr * brainstem_pitch_enc)
        # where alpha = 0.90
        #
        # Evidence: Bidelman & Krishnan 2009 — FFR pitch salience correlates
        # with perceived consonance hierarchy (P1 > P5 > P4 > M3 > m6 > TT)
        f01 = torch.sigmoid(self.ALPHA * (
            tonalness * autocorr * brainstem_pitch_encoding
        ))

        # --- f02: Harmonicity Index ---
        # How well the spectrum matches a harmonic template.
        # Consonant intervals produce harmonic spectra (more coincidence).
        # Low inharmonicity + balanced tristimulus + strong template match
        # → high harmonicity.
        #
        # Formula:
        #   trist_balance = 1 - std(tristimulus[1,2,3])
        #   f02 = sigma(beta * (1 - inharmonicity) * trist_balance
        #               * harmonic_template_match)
        # where beta = 0.85
        #
        # Evidence: McDermott et al. 2010 — individual differences show
        # consonance preference = harmonicity preference (not roughness).
        # Bidelman 2013 — harmonicity > roughness as consonance predictor.
        trist_balance = 1.0 - torch.std(
            torch.cat([trist1, trist2, trist3], dim=-1),
            dim=-1, keepdim=True,
        )
        f02 = torch.sigmoid(self.BETA * (
            (1.0 - inharmonicity) * trist_balance
            * harmonic_template_match
        ))

        # --- f03: Consonance Hierarchy ---
        # The rank-ordered consonance hierarchy: P1 > P5 > P4 > M3 > m6 > TT.
        # Computed from Helmholtz consonance × Stumpf fusion × brainstem pitch.
        #
        # Formula:
        #   f03 = sigma(gamma * helmholtz * stumpf * brainstem_pitch_enc)
        # where gamma = 0.80
        #
        # Evidence: Bidelman & Heinz 2011 — AN population (70 fibers)
        # predicts full consonance hierarchy from peripheral encoding alone.
        # Neural hierarchy is UNIVERSAL (confirmed in infants, animals).
        f03 = torch.sigmoid(self.GAMMA * (
            helmholtz * stumpf * brainstem_pitch_encoding
        ))

        # --- f04: FFR-Behavior Correlation ---
        # Models the r = 0.81 correlation between brainstem FFR and
        # behavioral consonance ratings (Bidelman & Krishnan 2009).
        #
        # Formula:
        #   f04 = FFR_CORR * (f01 + f02) / 2
        #
        # QUALIFICATION (Cousineau et al. 2015):
        # This correlation holds for SYNTHETIC tones (r = 0.81 Bidelman 2009,
        # r = 0.34 Cousineau replication) but NOT for natural sounds
        # (sax r = 0.24 NS, voice r = -0.10 NS). The measure is
        # stimulus-dependent; the underlying neural mechanism is valid.
        f04 = self.FFR_BEHAVIOR_CORR * (f01 + f02) / 2.0

        # ================================================================
        # LAYER M: MATHEMATICAL MODEL OUTPUTS (2D)
        # Computed mathematical quantities
        # ================================================================

        # --- nps_t: NPS at time t ---
        # The instantaneous Neural Pitch Salience, equivalent to f01
        # but semantically represents the mathematical NPS function:
        #   NPS(t) = FFR_magnitude(fundamental_at_time_t)
        nps_t = f01

        # --- harm_interval: Harmonicity of current interval ---
        # Mathematical harmonicity = sum of harmonic coincidence / total:
        #   Harm(f1, f2) = sum_i coincidence(harmonic_i(f1), harmonics(f2))
        #                  / total_harmonics
        # Equivalent to f02 but represents the mathematical formula.
        harm_interval = f02

        # ================================================================
        # LAYER P: PRESENT PROCESSING (3D)
        # Current consonance state in auditory cortex
        # ================================================================

        # --- consonance_signal: Phase-locked consonance ---
        # Inverse of roughness: consonant intervals have low roughness.
        #   C = 1 - (roughness + sethares_dissonance) / 2
        #
        # This is the PRIMARY output for cross-unit pathways:
        #   → ARU.SRP via P1 (consonance → opioid proxy)
        #   → IMU.MEAMN via P2 (consonance → memory binding)
        #   → STAI (aesthetic evaluation input)
        #
        # Evidence: Fishman et al. 2001 — phase-locked oscillatory activity
        # in A1 correlates with perceived dissonance.
        consonance_signal = 1.0 - (roughness + sethares) / 2.0

        # --- template_match: Harmonic template match strength ---
        # Directly from H³: how well the spectrum matches harmonic template
        # over the FFR integration window (100ms).
        #
        # Evidence: Bidelman & Heinz 2011 — AN population harmonic
        # template matching predicts consonance hierarchy.
        template_match = harmonic_template_match

        # --- neural_pitch: Neural pitch strength ---
        # Directly from H³: how strongly the brainstem encodes pitch
        # at the gamma rate (25ms instantaneous encoding).
        #
        # This feeds into PSCL (cortical pitch salience processing)
        # and SDED (early roughness signal baseline) via intra-SPU paths.
        neural_pitch = brainstem_pitch_encoding

        # ================================================================
        # LAYER F: FUTURE PREDICTIONS (3D)
        # Forward-looking consonance expectations
        # ================================================================

        # --- consonance_pred: Behavioral consonance prediction ---
        # Immediate consonance rating prediction combining harmonicity
        # (f02) and FFR-behavior correlation (f04).
        #
        # Weights: harmonicity (0.6) > FFR-behavior (0.4)
        # because McDermott 2010 showed harmonicity is the perceptual basis.
        consonance_pred = torch.sigmoid(0.6 * f02 + 0.4 * f04)

        # --- pitch_propagation: FFR → cortical pitch signal ---
        # Models the brainstem-to-cortex propagation of pitch information.
        # The FFR in IC feeds forward to A1 (Heschl's Gyrus) where it
        # becomes the cortical pitch representation.
        #
        # Evidence: Tabas et al. 2019 — POR latency advantage (up to 36ms)
        # for consonant stimuli suggests faster brainstem→cortical propagation.
        pitch_propagation = torch.sigmoid(
            0.7 * f01 + 0.3 * neural_pitch
        )

        # --- interval_expect: Next interval prediction ---
        # Temporal prediction of upcoming consonance based on H³ trends.
        # Uses roughness trajectory (trend) and helmholtz mean to predict
        # whether the next interval will be consonant or dissonant.
        #
        # H³ keys:
        #   (0, 6, 18, 0) = roughness at 200ms, trend morph, fwd law
        #   (2, 3, 1, 2)  = helmholtz at 100ms, mean morph, bidi law
        #
        # Inverts roughness trend: high roughness trend → low consonance
        # expectation, combined with mean consonance level.
        roughness_trend = h3((0, 6, 18, 0))   # Dissonance trajectory
        helmholtz_mean = h3((2, 3, 1, 2))     # Mean consonance at 100ms
        interval_expect = torch.sigmoid(
            0.5 * (1.0 - roughness_trend)
            + 0.5 * helmholtz_mean
        )

        # ================================================================
        # TEMPORAL MODULATION — cross-band coherence
        # ================================================================
        # Apply x_l5l7 coherence as a temporal modulation factor.
        # Consonant intervals show higher cross-frequency coupling
        # (Trulla et al. 2018 — recurrence peaks match just intonation).
        #
        # H³ keys:
        #   (41, 3, 0, 2)  = x_l5l7 value at 100ms (coupling strength)
        #   (41, 6, 14, 2) = x_l5l7 periodicity at 200ms (recurrence)
        xband_coherence = h3((41, 3, 0, 2))
        xband_periodic = h3((41, 6, 14, 2))

        # Modulation centered at 1.0 (neutral when features = 0.5)
        xband_mod = (0.5 + 0.25 * xband_coherence + 0.25 * xband_periodic)

        # Apply to Layer E (brainstem encoding modulated by cross-frequency)
        f01 = f01 * xband_mod
        f02 = f02 * xband_mod
        f03 = f03 * xband_mod
        f04 = self.FFR_BEHAVIOR_CORR * (f01 + f02) / 2.0  # Recompute

        # ================================================================
        # CONCATENATE AND CLAMP — output (B, T, 12)
        # ================================================================
        # Order follows LAYERS: E[0:4], M[4:6], P[6:9], F[9:12]

        return torch.cat([
            # Layer E: Explicit Features (4D)
            f01,                  # [0] f01_nps
            f02,                  # [1] f02_harmonicity
            f03,                  # [2] f03_hierarchy
            f04,                  # [3] f04_ffr_behavior
            # Layer M: Mathematical (2D)
            nps_t,                # [4] nps_t
            harm_interval,        # [5] harm_interval
            # Layer P: Present Processing (3D)
            consonance_signal,    # [6] consonance_signal
            template_match,       # [7] template_match
            neural_pitch,         # [8] neural_pitch
            # Layer F: Future Predictions (3D)
            consonance_pred,      # [9]  consonance_pred
            pitch_propagation,    # [10] pitch_propagation
            interval_expect,      # [11] interval_expect
        ], dim=-1).clamp(0.0, 1.0)
