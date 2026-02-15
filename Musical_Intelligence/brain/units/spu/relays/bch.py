"""BCH — Brainstem Consonance Hierarchy.

Gold standard Relay nucleus for the Spectral Processing Unit (SPU).

Neural Circuit:
    Audio → Cochlea → AN (70-fiber population model)
                        ↓
                      CN (spectral/temporal extraction)
                        ↓
                      SOC (binaural processing)
                        ↓
                      IC (FFR generator — rostral brainstem)
                        ↓  NPS ↔ Behavioral consonance: r = 0.81
                      MGB (thalamic relay)
                        ↓
                      A1/HG (cortical consonance representation)

Key Findings:
    - NPS (Neural Pitch Salience) in IC encodes the full consonance hierarchy:
      P1 > P5 > P4 > M3 > m6 > TT (Bidelman & Krishnan 2009)
    - FFR pitch salience ↔ behavioral consonance: r = 0.81 (synthetic, N=10)
    - AN population (70 fibers) predicts full hierarchy from peripheral
      encoding alone (Bidelman & Heinz 2011)
    - Harmonicity > roughness as consonance predictor (Bidelman 2013)

Critical Qualifier:
    NPS ↔ behavior correlation is NOT universal for natural sounds:
    - Synthetic tones: r = 0.81 (Bidelman 2009), r = 0.34 (Cousineau 2015)
    - Saxophone: r = 0.24 (NS) — Cousineau 2015
    - Voice: r = -0.10 (NS) — Cousineau 2015
    This stimulus-dependence is captured by SDNPS (SPU-γ1), which directly
    challenges BCH's universality assumption.

Cross-Unit Dependencies:
    BCH is the FOUNDATION of SPU. Its outputs feed:
    - PSCL (Encoder): BCH.f01_nps → cortical pitch salience processing
    - PCCR (Associator): BCH.f02_harmonicity → chroma tuning
    - STAI (Encoder): BCH.consonance_signal → aesthetic evaluation input
    - SDED (Integrator): BCH.f01_nps → roughness signal baseline
    - ARU.SRP (Pathway P1): BCH.consonance_signal → opioid_proxy
    - IMU.MEAMN (Pathway P2): BCH.consonance_signal → memory binding
"""
from __future__ import annotations

from typing import Dict, Set, Tuple

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

# NPS weight — Neural Pitch Salience dominance in consonance encoding
# Source: Bidelman & Krishnan 2009, r = 0.81, N = 10 (synthetic intervals)
ALPHA: float = 0.90

# Harmonicity weight — harmonic coincidence ratio
# Source: Bidelman 2013, review: harmonicity > roughness as predictor
BETA: float = 0.85

# Hierarchy weight — consonance ranking fidelity
# Source: Bidelman & Heinz 2011, AN population model (70 fibers)
GAMMA: float = 0.80

# FFR-behavior correlation — THE primary effect size
# Source: Bidelman & Krishnan 2009, r = 0.81, p < 0.01, N = 10
FFR_CORR: float = 0.81

# NPS-roughness coupling — secondary effect
# Source: Cousineau et al. 2015, r = -0.57 to -0.64
NPS_ROUGHNESS_CORR: float = -0.57

# Cortical roughness correlation — STG high gamma (70-150 Hz)
# Source: Foo et al. 2016, RH r = 0.43, LH r = 0.41
CORTICAL_ROUGHNESS_RH: float = 0.43
CORTICAL_ROUGHNESS_LH: float = 0.41

# POR latency gap — consonant vs dissonant processing in A1
# Source: Tabas et al. 2019, up to 36 ms difference
POR_LATENCY_GAP_MS: float = 36.0


class BCH(Relay):
    """Brainstem Consonance Hierarchy — SPU Relay (Depth 0, 12D).

    Transforms raw R³ spectral features and H³ temporal demands into the
    foundational consonance representation for the Spectral Processing Unit.

    The computation models the ascending auditory pathway from peripheral
    encoding (AN, 70-fiber population) through subcortical processing
    (IC, FFR generation) to the initial cortical representation (A1/HG).

    Output Structure (12D):
        E-layer (4D): f01_nps, f02_harmonicity, f03_hierarchy, f04_ffr_behavior
        M-layer (2D): nps_t, harm_interval
        P-layer (3D): consonance_signal, template_match, neural_pitch
        F-layer (3D): consonance_pred, pitch_propagation, interval_expect
    """

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    NAME = "BCH"
    FULL_NAME = "Brainstem Consonance Hierarchy"
    UNIT = "SPU"
    # ROLE and PROCESSING_DEPTH inherited from Relay (relay, 0)

    # ------------------------------------------------------------------
    # Output structure — 12D with scope labels
    # ------------------------------------------------------------------

    OUTPUT_DIM = 12

    LAYERS = (
        LayerSpec(
            code="E", name="Extraction", start=0, end=4,
            dim_names=(
                "f01_nps",           # Neural Pitch Salience (FFR at fundamental)
                "f02_harmonicity",   # Harmonicity Index (harmonic coincidence ratio)
                "f03_hierarchy",     # Consonance Hierarchy ranking (P1>P5>P4>M3>m6>TT)
                "f04_ffr_behavior",  # FFR-Behavior Correlation proxy (r=0.81)
            ),
            scope="internal",  # Extraction feeds downstream nuclei
        ),
        LayerSpec(
            code="M", name="Mechanism", start=4, end=6,
            dim_names=(
                "nps_t",          # NPS at time t (FFR magnitude at fundamental)
                "harm_interval",  # Harmonicity of current interval
            ),
            scope="internal",  # Mechanism layer = processing artifacts
        ),
        LayerSpec(
            code="P", name="Cognitive", start=6, end=9,
            dim_names=(
                "consonance_signal",  # Phase-locked consonance signal
                "template_match",     # Harmonic template match strength
                "neural_pitch",       # Neural pitch strength
            ),
            scope="external",  # Cognitive layer = semantic meaning
        ),
        LayerSpec(
            code="F", name="Forecast", start=9, end=12,
            dim_names=(
                "consonance_pred",     # Behavioral consonance prediction
                "pitch_propagation",   # FFR → cortical pitch processing
                "interval_expect",     # Next interval prediction (H³ trend)
            ),
            scope="hybrid",  # Predictions feed downstream + carry external meaning
        ),
    )

    # ------------------------------------------------------------------
    # R³ feature indices consumed
    # ------------------------------------------------------------------

    # Consonance group [0:7]
    _R3_ROUGHNESS = 0
    _R3_SETHARES = 1
    _R3_HELMHOLTZ = 2
    _R3_STUMPF = 3
    _R3_SENSORY_PLEASANT = 4
    _R3_INHARMONICITY = 5
    _R3_HARMONIC_DEV = 6

    # Timbre features
    _R3_TONALNESS = 14        # Harmonic-to-noise ratio (pitch clarity)
    _R3_SPECTRAL_AUTOCORR = 17  # Harmonic periodicity

    # Tristimulus (spectral energy distribution)
    _R3_TRIST1 = 18  # Fundamental (F0) energy
    _R3_TRIST2 = 19  # 2nd-4th harmonic energy
    _R3_TRIST3 = 20  # 5th+ harmonic energy

    # Interaction features
    _R3_X_L5L7_START = 41  # Consonance × Timbre coupling (8D: [41:49])
    _R3_X_L5L7_END = 49

    # ------------------------------------------------------------------
    # H³ temporal demands — 16 tuples
    # ------------------------------------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        """16 temporal demands spanning consonance, fusion, and spectral dynamics.

        Horizons: H0=25ms (frame-level), H3=100ms (note-level), H6=200ms (phrase-onset)
        """
        return (
            # --- Roughness dynamics (R³[0]) ---
            H3DemandSpec(
                r3_idx=0, r3_name="roughness",
                horizon=0, horizon_label="25ms frame",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Current dissonance level",
                citation="Plomp & Levelt 1965",
            ),
            H3DemandSpec(
                r3_idx=0, r3_name="roughness",
                horizon=3, horizon_label="100ms note",
                morph=1, morph_name="mean",
                law=2, law_name="integration",
                purpose="Mean dissonance over note-level window",
                citation="Bidelman & Krishnan 2009",
            ),
            H3DemandSpec(
                r3_idx=0, r3_name="roughness",
                horizon=6, horizon_label="200ms phrase",
                morph=18, morph_name="trend",
                law=0, law_name="memory",
                purpose="Dissonance trajectory for prediction",
                citation="Bidelman 2013",
            ),

            # --- Helmholtz-Kang consonance (R³[2]) ---
            H3DemandSpec(
                r3_idx=2, r3_name="helmholtz_kang",
                horizon=0, horizon_label="25ms frame",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Current consonance measure",
                citation="Helmholtz 1863; Kang 2010",
            ),
            H3DemandSpec(
                r3_idx=2, r3_name="helmholtz_kang",
                horizon=3, horizon_label="100ms note",
                morph=1, morph_name="mean",
                law=2, law_name="integration",
                purpose="Mean consonance over note-level window",
                citation="Bidelman & Krishnan 2009",
            ),

            # --- Stumpf tonal fusion (R³[3]) ---
            H3DemandSpec(
                r3_idx=3, r3_name="stumpf_fusion",
                horizon=0, horizon_label="25ms frame",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Current tonal fusion strength",
                citation="Stumpf 1898; McDermott 2010",
            ),
            H3DemandSpec(
                r3_idx=3, r3_name="stumpf_fusion",
                horizon=6, horizon_label="200ms phrase",
                morph=1, morph_name="mean",
                law=0, law_name="memory",
                purpose="Fusion stability over phrase-onset window",
                citation="McDermott et al. 2010",
            ),

            # --- Inharmonicity (R³[5]) ---
            H3DemandSpec(
                r3_idx=5, r3_name="inharmonicity",
                horizon=0, horizon_label="25ms frame",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Current deviation from harmonic series",
                citation="Bidelman & Heinz 2011",
            ),
            H3DemandSpec(
                r3_idx=5, r3_name="inharmonicity",
                horizon=3, horizon_label="100ms note",
                morph=18, morph_name="trend",
                law=0, law_name="memory",
                purpose="Inharmonicity trajectory for spectral change",
                citation="Bidelman 2013",
            ),

            # --- Harmonic deviation (R³[6]) ---
            H3DemandSpec(
                r3_idx=6, r3_name="harmonic_deviation",
                horizon=0, horizon_label="25ms frame",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Current energy variance in partials",
                citation="Bidelman & Heinz 2011",
            ),
            H3DemandSpec(
                r3_idx=6, r3_name="harmonic_deviation",
                horizon=3, horizon_label="100ms note",
                morph=1, morph_name="mean",
                law=0, law_name="memory",
                purpose="Mean partial deviation over note window",
                citation="Bidelman 2013",
            ),

            # --- Tristimulus (spectral energy balance: R³[18-20]) ---
            H3DemandSpec(
                r3_idx=18, r3_name="tristimulus1",
                horizon=0, horizon_label="25ms frame",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Fundamental (F0) energy for NPS weighting",
                citation="Pollack 1952; Bidelman 2009",
            ),
            H3DemandSpec(
                r3_idx=19, r3_name="tristimulus2",
                horizon=0, horizon_label="25ms frame",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Mid-harmonic energy (2nd-4th) for timbre context",
                citation="Pollack 1952",
            ),
            H3DemandSpec(
                r3_idx=20, r3_name="tristimulus3",
                horizon=0, horizon_label="25ms frame",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="High-harmonic energy (5th+) for brightness context",
                citation="Pollack 1952",
            ),

            # --- Consonance × Timbre interaction (R³[41]) ---
            H3DemandSpec(
                r3_idx=41, r3_name="x_l5l7_0",
                horizon=3, horizon_label="100ms note",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Consonance-timbre coupling strength",
                citation="Cousineau et al. 2015",
            ),
            H3DemandSpec(
                r3_idx=41, r3_name="x_l5l7_0",
                horizon=6, horizon_label="200ms phrase",
                morph=14, morph_name="periodicity",
                law=2, law_name="integration",
                purpose="Harmonic periodicity in coupling signal",
                citation="Trulla et al. 2018",
            ),
        )

    # ------------------------------------------------------------------
    # Dimension names
    # ------------------------------------------------------------------

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # E-layer (4D)
            "f01_nps", "f02_harmonicity", "f03_hierarchy", "f04_ffr_behavior",
            # M-layer (2D)
            "nps_t", "harm_interval",
            # P-layer (3D)
            "consonance_signal", "template_match", "neural_pitch",
            # F-layer (3D)
            "consonance_pred", "pitch_propagation", "interval_expect",
        )

    # ------------------------------------------------------------------
    # Region links — 6 brain regions in the ascending auditory pathway
    # ------------------------------------------------------------------

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        """BCH activates the ascending auditory pathway: AN → CN → SOC → IC → MGB → A1.

        Primary site: IC (Inferior Colliculus) — FFR generator.
        """
        return (
            # AN: Peripheral encoding — f01_nps reflects AN population coding
            RegionLink(
                dim_name="f01_nps",
                region="AN",
                weight=0.7,
                citation="Bidelman & Heinz 2011",
            ),
            # CN: Early spectral processing — harmonicity detection begins here
            RegionLink(
                dim_name="f02_harmonicity",
                region="CN",
                weight=0.5,
                citation="Young & Oertel 2004",
            ),
            # IC: PRIMARY — FFR generation, consonance hierarchy encoding
            RegionLink(
                dim_name="f01_nps",
                region="IC",
                weight=0.9,
                citation="Bidelman & Krishnan 2009",
            ),
            RegionLink(
                dim_name="f03_hierarchy",
                region="IC",
                weight=0.85,
                citation="Bidelman & Heinz 2011",
            ),
            # MGB: Thalamic relay — consonance signal en route to cortex
            RegionLink(
                dim_name="consonance_signal",
                region="MGB",
                weight=0.6,
                citation="Suga 2008",
            ),
            # A1/HG: Cortical representation — pitch propagation target
            RegionLink(
                dim_name="pitch_propagation",
                region="A1_HG",
                weight=0.7,
                citation="Fishman et al. 2001",
            ),
            # STG: Cortical roughness encoding — high gamma
            RegionLink(
                dim_name="consonance_signal",
                region="STG",
                weight=0.4,
                citation="Foo et al. 2016",
            ),
        )

    # ------------------------------------------------------------------
    # Neuro links — BCH produces DA signal via consonance → reward
    # ------------------------------------------------------------------

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        """Consonance drives dopaminergic reward via brainstem → VTA pathway.

        High consonance → positive reward prediction → DA release.
        This is the subcortical foundation of the consonance-pleasure link
        (Blood & Zatorre 2001, Salimpoor et al. 2011).
        """
        return (
            # Consonance signal → DA (reward prediction via brainstem)
            NeuroLink(
                dim_name="consonance_signal",
                channel=0,  # DA
                effect="produce",
                weight=0.3,
                citation="Blood & Zatorre 2001",
            ),
            # Neural pitch clarity → 5HT (temporal regularity → serotonin)
            NeuroLink(
                dim_name="neural_pitch",
                channel=3,  # 5HT
                effect="amplify",
                weight=0.2,
                citation="Doya 2002",
            ),
        )

    # ------------------------------------------------------------------
    # Evidence metadata — 13 papers, alpha tier
    # ------------------------------------------------------------------

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                # PRIMARY — BCH core (brainstem consonance)
                Citation(
                    "Bidelman", 2009,
                    "FFR pitch salience correlates with behavioral consonance ratings",
                    "r=0.81, p<0.01, N=10",
                ),
                Citation(
                    "Bidelman", 2013,
                    "Harmonicity > roughness as consonance predictor; subcortical "
                    "hierarchy mirrors Western music theory",
                    "strong (review)",
                ),
                Citation(
                    "Bidelman", 2011,
                    "AN population (70 fibers) predicts full consonance hierarchy; "
                    "neural harmonicity is best predictor",
                    "computational validation",
                ),
                Citation(
                    "Cousineau", 2015,
                    "NPS-behavior correlation is stimulus-dependent: synthetic r=0.34, "
                    "sax r=0.24 (NS), voice r=-0.10 (NS). NPS ↔ roughness r=-0.57",
                    "eta2=0.27 (sound type), eta2=0.13 (interval)",
                ),
                Citation(
                    "Lee", 2009,
                    "Enhanced brainstem phase-locking for consonant intervals in musicians",
                    "enhanced FFR",
                ),
                # SUPPORTING — cortical consonance
                Citation(
                    "Fishman", 2001,
                    "Phase-locked oscillatory activity in A1 correlates with dissonance; "
                    "Heschl's gyrus shows roughness encoding",
                    "dissonant > consonant phase-locking",
                ),
                Citation(
                    "Foo", 2016,
                    "High gamma (70-150Hz) increase for dissonant chords in STG; "
                    "bilateral organization",
                    "RH r=0.43, LH r=0.41",
                ),
                Citation(
                    "Tabas", 2019,
                    "POR latency for dissonant dyads up to 36ms longer than consonant; "
                    "consonance processing advantage in early auditory cortex",
                    "36ms latency difference",
                ),
                Citation(
                    "Crespo-Bojorque", 2018,
                    "Consonant→dissonant change: MMN in all; dissonant→consonant: "
                    "late MMN only in musicians",
                    "MMN amplitude p<0.05, N=40",
                ),
                Citation(
                    "Schon", 2005,
                    "N1-P2 modulated by consonance in musicians; N2 in non-musicians",
                    "N2 modulation",
                ),
                # BEHAVIORAL & COMPUTATIONAL
                Citation(
                    "McDermott", 2010,
                    "Consonance preference correlates with harmonicity (not roughness); "
                    "individual differences in preference",
                    "strong correlation",
                ),
                Citation(
                    "Trulla", 2018,
                    "Recurrence peaks match just intonation ratios; Devil's staircase "
                    "pattern; mode-locking links to consonance hierarchy",
                    "recurrence profile match",
                ),
                Citation(
                    "Terhardt", 1974,
                    "Virtual pitch computation in peripheral auditory system; "
                    "foundational NPS computation basis",
                    "foundational theory",
                ),
            ),
            evidence_tier="alpha",
            confidence_range=(0.90, 0.95),
            falsification_criteria=(
                "Pure tones should NOT show consonance effects — only complex "
                "tones with harmonics trigger NPS differentiation",
                "Non-Western listeners should show same NEURAL hierarchy (NPS ranking) "
                "even if BEHAVIORAL preferences differ (cultural modulation)",
                "Hearing impairment (especially cochlear) should alter consonance "
                "hierarchy due to degraded phase-locking",
                "Removing harmonics from stimuli should reduce NPS and flatten "
                "the consonance hierarchy toward uniform",
                "Brainstem lesions affecting IC should abolish FFR consonance "
                "effects while leaving cortical processing partially intact",
            ),
            version="2.0.0",
            paper_count=13,
        )

    # ------------------------------------------------------------------
    # compute() — the neural circuit
    # ------------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Brainstem consonance computation: AN → IC → A1 pathway.

        Models the ascending auditory pathway for consonance encoding:
        1. Extract R³ consonance, timbre, and interaction features
        2. Compute internal pitch/harmonicity representations (E-layer)
        3. Derive mechanism outputs (M-layer)
        4. Produce cognitive consonance signals (P-layer)
        5. Generate predictions for downstream processing (F-layer)

        Args:
            h3_features: Dict mapping (r3_idx, horizon, morph, law) 4-tuples
                         to (B, T) temporal feature scalars.
            r3_features: (B, T, 49) R³ spectral feature tensor.

        Returns:
            (B, T, 12) output tensor structured as E(4) + M(2) + P(3) + F(3).
        """
        B, T = r3_features.shape[:2]

        # === Stage 1: Extract R³ features ===

        # Consonance group [0:7] — the sensory basis
        roughness = r3_features[:, :, self._R3_ROUGHNESS]           # (B, T)
        sethares = r3_features[:, :, self._R3_SETHARES]             # (B, T)
        helmholtz = r3_features[:, :, self._R3_HELMHOLTZ]           # (B, T)
        stumpf = r3_features[:, :, self._R3_STUMPF]                 # (B, T)
        inharmonicity = r3_features[:, :, self._R3_INHARMONICITY]   # (B, T)
        harmonic_dev = r3_features[:, :, self._R3_HARMONIC_DEV]     # (B, T)

        # Timbre features — pitch clarity context
        tonalness = r3_features[:, :, self._R3_TONALNESS]           # (B, T)
        autocorr = r3_features[:, :, self._R3_SPECTRAL_AUTOCORR]    # (B, T)

        # Tristimulus — spectral energy distribution
        trist1 = r3_features[:, :, self._R3_TRIST1]                 # (B, T)
        trist2 = r3_features[:, :, self._R3_TRIST2]                 # (B, T)
        trist3 = r3_features[:, :, self._R3_TRIST3]                 # (B, T)

        # === Stage 2: Compute tristimulus balance ===
        # Balanced spectral energy → higher harmonicity confidence
        # std across tristimulus channels: low std = balanced = harmonic
        trist_stack = torch.stack([trist1, trist2, trist3], dim=-1)  # (B, T, 3)
        trist_balance = 1.0 - trist_stack.std(dim=-1)                # (B, T)

        # === Stage 3: E-LAYER — Explicit features (4D) ===

        # f01: Neural Pitch Salience — IC FFR at fundamental
        # NPS ∝ tonalness × autocorrelation (pitch clarity × periodicity)
        # Bidelman & Krishnan 2009: FFR pitch salience encodes consonance hierarchy
        f01_nps = torch.sigmoid(ALPHA * tonalness * autocorr)        # (B, T)

        # f02: Harmonicity Index — harmonic coincidence ratio
        # Harmonicity > roughness as predictor (Bidelman 2013)
        # (1 - inharmonicity) = harmonic regularity
        # trist_balance = spectral energy distribution quality
        f02_harmonicity = torch.sigmoid(
            BETA * (1.0 - inharmonicity) * trist_balance
        )  # (B, T)

        # f03: Consonance Hierarchy — P1 > P5 > P4 > M3 > m6 > TT
        # Combines Helmholtz integer-ratio detection with Stumpf fusion
        # and pitch salience (Bidelman & Heinz 2011: AN population model)
        f03_hierarchy = torch.sigmoid(
            GAMMA * helmholtz * stumpf
        )  # (B, T)

        # f04: FFR-Behavior Correlation — the primary effect size
        # Bidelman & Krishnan 2009: r = 0.81 between FFR pitch salience
        # and behavioral consonance ratings (synthetic, N=10)
        f04_ffr_behavior = FFR_CORR * (f01_nps + f02_harmonicity) / 2.0  # (B, T)

        # === Stage 4: M-LAYER — Mechanism outputs (2D) ===

        # nps_t: NPS at current time step (FFR magnitude)
        nps_t = f01_nps  # (B, T)

        # harm_interval: Harmonicity of current interval
        harm_interval = f02_harmonicity  # (B, T)

        # === Stage 5: P-LAYER — Cognitive consonance signals (3D) ===

        # consonance_signal: Inverse of combined roughness and Sethares dissonance
        # 1 - (roughness + sethares)/2 = perceptual consonance
        # Plomp & Levelt 1965, Sethares 1993
        consonance_signal = 1.0 - (roughness + sethares) / 2.0  # (B, T)

        # template_match: How well the current spectrum matches a harmonic template
        # Combines Helmholtz consonance with Stumpf fusion
        template_match = (helmholtz + stumpf) / 2.0  # (B, T)

        # neural_pitch: Overall neural pitch strength
        # Aggregates NPS with tonal clarity
        neural_pitch = (f01_nps + tonalness) / 2.0  # (B, T)

        # === Stage 6: F-LAYER — Predictions (3D) ===

        # consonance_pred: Predicted behavioral consonance rating
        # Weighted combination of harmonicity and FFR correlation
        consonance_pred = torch.sigmoid(
            0.6 * f02_harmonicity + 0.4 * f04_ffr_behavior
        )  # (B, T)

        # pitch_propagation: Brainstem → A1 pitch processing strength
        # How strongly the brainstem FFR signal propagates to cortex
        # Fishman et al. 2001, Tabas et al. 2019
        pitch_propagation = torch.sigmoid(
            0.7 * f01_nps + 0.3 * neural_pitch
        )  # (B, T)

        # interval_expect: Next interval expectation from H³ trends
        # Uses roughness trend and Helmholtz mean to predict upcoming consonance
        roughness_trend = h3_features.get((0, 6, 18, 0))    # (B, T) or None
        helmholtz_mean = h3_features.get((2, 3, 1, 2))      # (B, T) or None

        if roughness_trend is not None and helmholtz_mean is not None:
            interval_expect = torch.sigmoid(
                0.5 * helmholtz_mean + 0.5 * (1.0 - roughness_trend)
            )  # (B, T) — high consonance expected when roughness trending down
        else:
            # Fallback: neutral expectation
            interval_expect = torch.full((B, T), 0.5, device=r3_features.device)

        # === Assemble 12D output ===
        return torch.stack([
            # E-layer (4D)
            f01_nps, f02_harmonicity, f03_hierarchy, f04_ffr_behavior,
            # M-layer (2D)
            nps_t, harm_interval,
            # P-layer (3D)
            consonance_signal, template_match, neural_pitch,
            # F-layer (3D)
            consonance_pred, pitch_propagation, interval_expect,
        ], dim=-1)  # (B, T, 12)
