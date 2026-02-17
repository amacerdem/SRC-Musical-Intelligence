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

Temporal Architecture:
    BCH uses H³ demands across three temporal laws:
    - L0 (Memory):      Past — what consonance patterns have prevailed
    - L2 (Integration): Present — current consonance in bidirectional context
    - L1 (Prediction):  Future — predicted consonance trajectory

    Horizons span 5 scales: H0 (5.8ms), H3 (23ms), H6 (200ms),
    H12 (525ms), H16 (1s), H18 (2s).

Cross-Unit Dependencies:
    BCH is the FOUNDATION of SPU. Its outputs feed:
    - PSCL (Encoder): BCH.nps → cortical pitch salience processing
    - PCCR (Associator): BCH.harmonicity → chroma tuning
    - STAI (Encoder): BCH.consonance_signal → aesthetic evaluation input
    - SDED (Integrator): BCH.nps → roughness signal baseline
    - ARU.SRP (Pathway P1): BCH.consonance_signal → opioid_proxy
    - IMU.MEAMN (Pathway P2): BCH.consonance_signal → memory binding
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
    """Brainstem Consonance Hierarchy — SPU Relay (Depth 0, 16D).

    Transforms raw R³ spectral features and H³ temporal demands into the
    foundational consonance representation for the Spectral Processing Unit.

    The computation models the ascending auditory pathway from peripheral
    encoding (AN, 70-fiber population) through subcortical processing
    (IC, FFR generation) to the initial cortical representation (A1/HG).

    Temporal Architecture:
        Each H³ demand uses a specific law to define its temporal domain:
        - L0 (Memory):      looks backward — encodes the past
        - L2 (Integration): looks both ways — encodes the present
        - L1 (Prediction):  looks forward — encodes the future

    Output Structure (16D):
        E-layer  (4D) [0:4]:   Instantaneous features from R³ (no temporal)
        M-layer  (4D) [4:8]:   Memory — past consonance state (L0 demands)
        P-layer  (4D) [8:12]:  Present — context-aware now (L2 demands)
        F-layer  (4D) [12:16]: Future — predicted trajectory (L1 demands)
    """

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    NAME = "BCH"
    FULL_NAME = "Brainstem Consonance Hierarchy"
    UNIT = "SPU"
    # ROLE and PROCESSING_DEPTH inherited from Relay (relay, 0)

    # ------------------------------------------------------------------
    # Output structure — 16D: E(4) + Memory(4) + Present(4) + Future(4)
    # ------------------------------------------------------------------

    OUTPUT_DIM = 16

    LAYERS = (
        LayerSpec(
            code="E", name="Extraction", start=0, end=4,
            dim_names=(
                "nps",           # Neural Pitch Salience (FFR at fundamental)
                "harmonicity",   # Harmonicity Index (harmonic coincidence ratio)
                "hierarchy",     # Consonance Hierarchy ranking (P1>P5>P4>M3>m6>TT)
                "ffr_behavior",  # FFR-Behavior Correlation proxy (r=0.81)
            ),
            scope="internal",  # Extraction feeds downstream nuclei
        ),
        LayerSpec(
            code="M", name="Memory", start=4, end=8,
            dim_names=(
                "consonance_memory",  # Past consonance level (H6–H18 memory)
                "pitch_memory",       # Past pitch state (H3–H18 memory)
                "tonal_memory",       # Past tonal context (H6–H18 memory)
                "spectral_memory",    # Overall spectral history (multi-scale)
            ),
            scope="internal",  # Memory feeds Present + Future layers
        ),
        LayerSpec(
            code="P", name="Present", start=8, end=12,
            dim_names=(
                "consonance_signal",  # Current consonance in context
                "template_match",     # Current harmonic template match
                "neural_pitch",       # Current pitch clarity in context
                "tonal_context",      # Current tonal environment
            ),
            scope="external",  # Present layer = semantic meaning
        ),
        LayerSpec(
            code="F", name="Future", start=12, end=16,
            dim_names=(
                "consonance_forecast",  # Predicted consonance trajectory
                "pitch_forecast",       # Predicted pitch trajectory
                "tonal_forecast",       # Predicted tonal changes
                "interval_forecast",    # Predicted interval changes
            ),
            scope="hybrid",  # Predictions feed downstream + carry external meaning
        ),
    )

    # ------------------------------------------------------------------
    # R³ feature indices consumed (14 scalar, Groups E/I dissolved)
    # ------------------------------------------------------------------

    # Consonance group A [0:7]
    _R3_ROUGHNESS = 0
    _R3_SETHARES = 1
    _R3_HELMHOLTZ = 2
    _R3_STUMPF = 3
    _R3_SENSORY_PLEASANT = 4
    _R3_INHARMONICITY = 5
    _R3_HARMONIC_DEV = 6

    # Timbre group C [12:21]
    _R3_TONALNESS = 14        # Harmonic-to-noise ratio (pitch clarity)
    _R3_SPECTRAL_AUTOCORR = 17  # Harmonic periodicity

    # Tristimulus (spectral energy distribution)
    _R3_TRIST1 = 18  # Fundamental (F0) energy
    _R3_TRIST2 = 19  # 2nd-4th harmonic energy
    _R3_TRIST3 = 20  # 5th+ harmonic energy

    # Group E (Interactions) DISSOLVED — _R3_X_L5L7_START/END removed

    # Pitch & Chroma group F [25:41]
    _R3_PITCH_CLASS_ENTROPY = 38  # Chroma distribution entropy (low = tonal clarity)
    _R3_PITCH_SALIENCE = 39       # Harmonic peak prominence (direct NPS measure)

    # Harmony group H [51:63]
    _R3_KEY_CLARITY = 51          # Krumhansl-Kessler tonal center strength
    _R3_TONAL_STABILITY = 60      # Stability of tonal center over time

    # ------------------------------------------------------------------
    # H³ temporal demands — 48 tuples organized by temporal law
    #
    # L2 (Integration) = Present: 19 demands at H0/H3/H6
    # L0 (Memory)      = Past:    17 demands at H3/H6/H12/H16/H18
    # L1 (Prediction)  = Future:  12 demands at H6/H12/H16
    # ------------------------------------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        """48 temporal demands across three laws and six horizon scales.

        Present (L2): H0 (5.8ms), H3 (23ms), H6 (200ms) — bidirectional
        Past    (L0): H3 (23ms), H6 (200ms), H12 (525ms), H16 (1s), H18 (2s)
        Future  (L1): H6 (200ms), H12 (525ms), H16 (1s) — forward-looking
        """
        return (
            # ═══════════════════════════════════════════════════════════
            # PRESENT demands (L2 = Integration) — 19 tuples
            # Bidirectional context around current frame
            # ═══════════════════════════════════════════════════════════

            # --- Roughness (R³[0]) — 2 present scales ---
            H3DemandSpec(
                r3_idx=0, r3_name="roughness",
                horizon=0, horizon_label="5.8ms frame",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Current dissonance level",
                citation="Plomp & Levelt 1965",
            ),
            H3DemandSpec(
                r3_idx=0, r3_name="roughness",
                horizon=3, horizon_label="23ms note",
                morph=1, morph_name="mean",
                law=2, law_name="integration",
                purpose="Mean dissonance over note-level context",
                citation="Bidelman & Krishnan 2009",
            ),

            # --- Helmholtz consonance (R³[2]) — 2 present scales ---
            H3DemandSpec(
                r3_idx=2, r3_name="helmholtz_kang",
                horizon=0, horizon_label="5.8ms frame",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Current consonance measure",
                citation="Helmholtz 1863; Kang 2010",
            ),
            H3DemandSpec(
                r3_idx=2, r3_name="helmholtz_kang",
                horizon=3, horizon_label="23ms note",
                morph=1, morph_name="mean",
                law=2, law_name="integration",
                purpose="Mean consonance over note-level context",
                citation="Bidelman & Krishnan 2009",
            ),

            # --- Stumpf fusion (R³[3]) — 1 present scale ---
            H3DemandSpec(
                r3_idx=3, r3_name="stumpf_fusion",
                horizon=0, horizon_label="5.8ms frame",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Current tonal fusion strength",
                citation="Stumpf 1898; McDermott 2010",
            ),

            # --- Inharmonicity (R³[5]) — 1 present scale ---
            H3DemandSpec(
                r3_idx=5, r3_name="inharmonicity",
                horizon=0, horizon_label="5.8ms frame",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Current deviation from harmonic series",
                citation="Bidelman & Heinz 2011",
            ),

            # --- Harmonic deviation (R³[6]) — 1 present scale ---
            H3DemandSpec(
                r3_idx=6, r3_name="harmonic_deviation",
                horizon=0, horizon_label="5.8ms frame",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Current energy variance in partials",
                citation="Bidelman & Heinz 2011",
            ),

            # --- Tristimulus (R³[18-20]) — 3 present scales ---
            H3DemandSpec(
                r3_idx=18, r3_name="tristimulus1",
                horizon=0, horizon_label="5.8ms frame",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Fundamental (F0) energy for NPS weighting",
                citation="Pollack 1952; Bidelman 2009",
            ),
            H3DemandSpec(
                r3_idx=19, r3_name="tristimulus2",
                horizon=0, horizon_label="5.8ms frame",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Mid-harmonic energy (2nd-4th) for timbre context",
                citation="Pollack 1952",
            ),
            H3DemandSpec(
                r3_idx=20, r3_name="tristimulus3",
                horizon=0, horizon_label="5.8ms frame",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="High-harmonic energy (5th+) for brightness context",
                citation="Pollack 1952",
            ),

            # Group E (Interactions) dissolved — coupling demands removed

            # --- Pitch class entropy (R³[38]) — 2 present scales ---
            H3DemandSpec(
                r3_idx=38, r3_name="pitch_class_entropy",
                horizon=0, horizon_label="5.8ms frame",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Current chroma concentration (low = tonal clarity)",
                citation="Krumhansl 1990",
            ),
            H3DemandSpec(
                r3_idx=38, r3_name="pitch_class_entropy",
                horizon=3, horizon_label="23ms note",
                morph=1, morph_name="mean",
                law=2, law_name="integration",
                purpose="Mean tonal clarity over note-level context",
                citation="Krumhansl 1990",
            ),

            # --- Pitch salience (R³[39]) — 3 present scales ---
            H3DemandSpec(
                r3_idx=39, r3_name="pitch_salience",
                horizon=0, horizon_label="5.8ms frame",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Current pitch salience (direct NPS)",
                citation="Parncutt 1989",
            ),
            H3DemandSpec(
                r3_idx=39, r3_name="pitch_salience",
                horizon=3, horizon_label="23ms note",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Pitch salience at note-level",
                citation="Bidelman & Krishnan 2009",
            ),
            H3DemandSpec(
                r3_idx=39, r3_name="pitch_salience",
                horizon=6, horizon_label="200ms phrase",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Pitch salience at phrase-onset level",
                citation="Bidelman 2013",
            ),

            # --- Key clarity (R³[51]) — 3 present scales ---
            H3DemandSpec(
                r3_idx=51, r3_name="key_clarity",
                horizon=3, horizon_label="23ms note",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Key clarity at note-level for tonal context",
                citation="Krumhansl & Kessler 1982",
            ),
            H3DemandSpec(
                r3_idx=51, r3_name="key_clarity",
                horizon=3, horizon_label="23ms note",
                morph=1, morph_name="mean",
                law=2, law_name="integration",
                purpose="Sustained key clarity over note-level context",
                citation="Krumhansl & Kessler 1982",
            ),
            H3DemandSpec(
                r3_idx=51, r3_name="key_clarity",
                horizon=6, horizon_label="200ms phrase",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Key clarity at phrase-onset level",
                citation="Krumhansl 1990",
            ),

            # --- Tonal stability (R³[60]) — 1 present scale ---
            H3DemandSpec(
                r3_idx=60, r3_name="tonal_stability",
                horizon=3, horizon_label="23ms note",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Current tonal center stability",
                citation="Krumhansl 1990",
            ),

            # ═══════════════════════════════════════════════════════════
            # PAST demands (L0 = Memory) — 17 tuples
            # Causal lookback: what has happened
            # ═══════════════════════════════════════════════════════════

            # --- Roughness memory (R³[0]) — 3 past scales ---
            H3DemandSpec(
                r3_idx=0, r3_name="roughness",
                horizon=6, horizon_label="200ms phrase",
                morph=18, morph_name="trend",
                law=0, law_name="memory",
                purpose="Short-term roughness direction (200ms lookback)",
                citation="Bidelman 2013",
            ),
            H3DemandSpec(
                r3_idx=0, r3_name="roughness",
                horizon=12, horizon_label="525ms beat",
                morph=1, morph_name="mean",
                law=0, law_name="memory",
                purpose="Beat-level roughness history",
                citation="Plomp & Levelt 1965",
            ),
            H3DemandSpec(
                r3_idx=0, r3_name="roughness",
                horizon=16, horizon_label="1s measure",
                morph=1, morph_name="mean",
                law=0, law_name="memory",
                purpose="Measure-level roughness history",
                citation="Plomp & Levelt 1965",
            ),

            # --- Helmholtz memory (R³[2]) — 2 past scales ---
            H3DemandSpec(
                r3_idx=2, r3_name="helmholtz_kang",
                horizon=12, horizon_label="525ms beat",
                morph=1, morph_name="mean",
                law=0, law_name="memory",
                purpose="Beat-level consonance history",
                citation="Helmholtz 1863; Kang 2010",
            ),
            H3DemandSpec(
                r3_idx=2, r3_name="helmholtz_kang",
                horizon=18, horizon_label="2s phrase",
                morph=1, morph_name="mean",
                law=0, law_name="memory",
                purpose="Phrase-level consonance history",
                citation="Helmholtz 1863",
            ),

            # --- Stumpf memory (R³[3]) — 2 past scales ---
            H3DemandSpec(
                r3_idx=3, r3_name="stumpf_fusion",
                horizon=6, horizon_label="200ms phrase",
                morph=1, morph_name="mean",
                law=0, law_name="memory",
                purpose="Short-term fusion history",
                citation="McDermott et al. 2010",
            ),
            H3DemandSpec(
                r3_idx=3, r3_name="stumpf_fusion",
                horizon=16, horizon_label="1s measure",
                morph=1, morph_name="mean",
                law=0, law_name="memory",
                purpose="Measure-level fusion history",
                citation="Stumpf 1898",
            ),

            # --- Inharmonicity memory (R³[5]) — 2 past scales ---
            H3DemandSpec(
                r3_idx=5, r3_name="inharmonicity",
                horizon=3, horizon_label="23ms note",
                morph=18, morph_name="trend",
                law=0, law_name="memory",
                purpose="Short-term inharmonicity trend",
                citation="Bidelman 2013",
            ),
            H3DemandSpec(
                r3_idx=5, r3_name="inharmonicity",
                horizon=12, horizon_label="525ms beat",
                morph=1, morph_name="mean",
                law=0, law_name="memory",
                purpose="Beat-level inharmonicity history",
                citation="Bidelman & Heinz 2011",
            ),

            # --- Harmonic deviation memory (R³[6]) — 2 past scales ---
            H3DemandSpec(
                r3_idx=6, r3_name="harmonic_deviation",
                horizon=3, horizon_label="23ms note",
                morph=1, morph_name="mean",
                law=0, law_name="memory",
                purpose="Short-term harmonic deviation",
                citation="Bidelman 2013",
            ),
            H3DemandSpec(
                r3_idx=6, r3_name="harmonic_deviation",
                horizon=12, horizon_label="525ms beat",
                morph=1, morph_name="mean",
                law=0, law_name="memory",
                purpose="Beat-level harmonic deviation history",
                citation="Bidelman & Heinz 2011",
            ),

            # --- Pitch salience memory (R³[39]) — 2 past scales ---
            H3DemandSpec(
                r3_idx=39, r3_name="pitch_salience",
                horizon=12, horizon_label="525ms beat",
                morph=1, morph_name="mean",
                law=0, law_name="memory",
                purpose="Beat-level pitch salience history",
                citation="Parncutt 1989",
            ),
            H3DemandSpec(
                r3_idx=39, r3_name="pitch_salience",
                horizon=18, horizon_label="2s phrase",
                morph=1, morph_name="mean",
                law=0, law_name="memory",
                purpose="Phrase-level pitch salience history",
                citation="Bidelman & Krishnan 2009",
            ),

            # --- Key clarity memory (R³[51]) — 2 past scales ---
            H3DemandSpec(
                r3_idx=51, r3_name="key_clarity",
                horizon=12, horizon_label="525ms beat",
                morph=1, morph_name="mean",
                law=0, law_name="memory",
                purpose="Beat-level key clarity history",
                citation="Krumhansl & Kessler 1982",
            ),
            H3DemandSpec(
                r3_idx=51, r3_name="key_clarity",
                horizon=18, horizon_label="2s phrase",
                morph=1, morph_name="mean",
                law=0, law_name="memory",
                purpose="Phrase-level key establishment",
                citation="Krumhansl 1990",
            ),

            # --- Tonal stability memory (R³[60]) — 1 past scale ---
            H3DemandSpec(
                r3_idx=60, r3_name="tonal_stability",
                horizon=6, horizon_label="200ms phrase",
                morph=1, morph_name="mean",
                law=0, law_name="memory",
                purpose="Short-term tonal stability history",
                citation="Krumhansl & Kessler 1982",
            ),
            H3DemandSpec(
                r3_idx=60, r3_name="tonal_stability",
                horizon=18, horizon_label="2s phrase",
                morph=1, morph_name="mean",
                law=0, law_name="memory",
                purpose="Phrase-level tonal stability history",
                citation="Krumhansl 1990",
            ),

            # ═══════════════════════════════════════════════════════════
            # FUTURE demands (L1 = Prediction) — 12 tuples
            # Forward-looking: what will happen
            # ═══════════════════════════════════════════════════════════

            # --- Roughness prediction (R³[0]) — 2 future scales ---
            H3DemandSpec(
                r3_idx=0, r3_name="roughness",
                horizon=6, horizon_label="200ms phrase",
                morph=1, morph_name="mean",
                law=1, law_name="prediction",
                purpose="Near-future roughness prediction (200ms ahead)",
                citation="Plomp & Levelt 1965",
            ),
            H3DemandSpec(
                r3_idx=0, r3_name="roughness",
                horizon=12, horizon_label="525ms beat",
                morph=18, morph_name="trend",
                law=1, law_name="prediction",
                purpose="Beat-level roughness trend prediction",
                citation="Bidelman 2013",
            ),

            # --- Helmholtz prediction (R³[2]) — 2 future scales ---
            H3DemandSpec(
                r3_idx=2, r3_name="helmholtz_kang",
                horizon=6, horizon_label="200ms phrase",
                morph=1, morph_name="mean",
                law=1, law_name="prediction",
                purpose="Near-future consonance prediction",
                citation="Helmholtz 1863; Kang 2010",
            ),
            H3DemandSpec(
                r3_idx=2, r3_name="helmholtz_kang",
                horizon=12, horizon_label="525ms beat",
                morph=1, morph_name="mean",
                law=1, law_name="prediction",
                purpose="Beat-level consonance prediction",
                citation="Helmholtz 1863",
            ),

            # --- Stumpf prediction (R³[3]) — 1 future scale ---
            H3DemandSpec(
                r3_idx=3, r3_name="stumpf_fusion",
                horizon=6, horizon_label="200ms phrase",
                morph=1, morph_name="mean",
                law=1, law_name="prediction",
                purpose="Near-future fusion prediction",
                citation="Stumpf 1898",
            ),

            # --- Inharmonicity prediction (R³[5]) — 1 future scale ---
            H3DemandSpec(
                r3_idx=5, r3_name="inharmonicity",
                horizon=6, horizon_label="200ms phrase",
                morph=18, morph_name="trend",
                law=1, law_name="prediction",
                purpose="Near-future inharmonicity trajectory",
                citation="Bidelman 2013",
            ),

            # --- Pitch salience prediction (R³[39]) — 2 future scales ---
            H3DemandSpec(
                r3_idx=39, r3_name="pitch_salience",
                horizon=6, horizon_label="200ms phrase",
                morph=1, morph_name="mean",
                law=1, law_name="prediction",
                purpose="Near-future pitch salience prediction",
                citation="Parncutt 1989",
            ),
            H3DemandSpec(
                r3_idx=39, r3_name="pitch_salience",
                horizon=12, horizon_label="525ms beat",
                morph=1, morph_name="mean",
                law=1, law_name="prediction",
                purpose="Beat-level pitch salience prediction",
                citation="Bidelman & Krishnan 2009",
            ),

            # --- Key clarity prediction (R³[51]) — 2 future scales ---
            H3DemandSpec(
                r3_idx=51, r3_name="key_clarity",
                horizon=6, horizon_label="200ms phrase",
                morph=1, morph_name="mean",
                law=1, law_name="prediction",
                purpose="Near-future key clarity prediction",
                citation="Krumhansl & Kessler 1982",
            ),
            H3DemandSpec(
                r3_idx=51, r3_name="key_clarity",
                horizon=16, horizon_label="1s measure",
                morph=1, morph_name="mean",
                law=1, law_name="prediction",
                purpose="Measure-level key clarity prediction",
                citation="Krumhansl 1990",
            ),

            # --- Tonal stability prediction (R³[60]) — 2 future scales ---
            H3DemandSpec(
                r3_idx=60, r3_name="tonal_stability",
                horizon=6, horizon_label="200ms phrase",
                morph=1, morph_name="mean",
                law=1, law_name="prediction",
                purpose="Near-future tonal stability prediction",
                citation="Krumhansl 1990",
            ),
            H3DemandSpec(
                r3_idx=60, r3_name="tonal_stability",
                horizon=12, horizon_label="525ms beat",
                morph=1, morph_name="mean",
                law=1, law_name="prediction",
                purpose="Beat-level tonal stability prediction",
                citation="Krumhansl 1990",
            ),
        )

    # ------------------------------------------------------------------
    # Dimension names
    # ------------------------------------------------------------------

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # E-layer (4D): Extraction — instantaneous
            "nps", "harmonicity", "hierarchy", "ffr_behavior",
            # M-layer (4D): Memory — past
            "consonance_memory", "pitch_memory", "tonal_memory", "spectral_memory",
            # P-layer (4D): Present — context-aware now
            "consonance_signal", "template_match", "neural_pitch", "tonal_context",
            # F-layer (4D): Future — predictions
            "consonance_forecast", "pitch_forecast", "tonal_forecast", "interval_forecast",
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
            # AN: Peripheral encoding — NPS reflects AN population coding
            RegionLink(
                dim_name="nps",
                region="AN",
                weight=0.7,
                citation="Bidelman & Heinz 2011",
            ),
            # CN: Early spectral processing — harmonicity detection begins here
            RegionLink(
                dim_name="harmonicity",
                region="CN",
                weight=0.5,
                citation="Young & Oertel 2004",
            ),
            # IC: PRIMARY — FFR generation, consonance hierarchy encoding
            RegionLink(
                dim_name="nps",
                region="IC",
                weight=0.9,
                citation="Bidelman & Krishnan 2009",
            ),
            RegionLink(
                dim_name="hierarchy",
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
            # A1/HG: Cortical representation — pitch forecast target
            RegionLink(
                dim_name="pitch_forecast",
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
            # Pitch forecast → 5HT (temporal regularity → serotonin)
            NeuroLink(
                dim_name="pitch_forecast",
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
            version="3.0.0",
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

        Models the ascending auditory pathway with temporally separated
        layers: Memory (past, L0), Present (now, L2), Future (ahead, L1).

        All 14 R³ features and 48 H³ demands are consumed — no dead
        variables.  Each temporal layer uses a specific H³ law:
        - Memory  (Past):    L0 demands at H3–H18 (23ms–2s lookback)
        - Present (Now):     L2 demands at H0–H6 (5.8ms–200ms context)
        - Future  (Ahead):   L1 demands at H6–H16 (200ms–1s lookahead)

        Args:
            h3_features: Dict mapping (r3_idx, horizon, morph, law) 4-tuples
                         to (B, T) temporal feature scalars.
            r3_features: (B, T, 97) R³ spectral feature tensor.

        Returns:
            (B, T, 16) output: E(4) + Memory(4) + Present(4) + Future(4).
        """
        B, T = r3_features.shape[:2]
        device = r3_features.device

        # === Stage 1: Extract R³ features (14 scalar indices) ===

        # Consonance group A [0:7] — all 7 used
        roughness     = r3_features[:, :, self._R3_ROUGHNESS]          # (B, T)
        sethares      = r3_features[:, :, self._R3_SETHARES]           # (B, T)
        helmholtz     = r3_features[:, :, self._R3_HELMHOLTZ]          # (B, T)
        stumpf        = r3_features[:, :, self._R3_STUMPF]             # (B, T)
        sens_pleasant = r3_features[:, :, self._R3_SENSORY_PLEASANT]   # (B, T)
        inharmonicity = r3_features[:, :, self._R3_INHARMONICITY]      # (B, T)
        harmonic_dev  = r3_features[:, :, self._R3_HARMONIC_DEV]       # (B, T)

        # Timbre group C [12:21] — pitch clarity context
        tonalness = r3_features[:, :, self._R3_TONALNESS]              # (B, T)
        autocorr  = r3_features[:, :, self._R3_SPECTRAL_AUTOCORR]      # (B, T)

        # Tristimulus — spectral energy distribution
        trist1 = r3_features[:, :, self._R3_TRIST1]                    # (B, T)
        trist2 = r3_features[:, :, self._R3_TRIST2]                    # (B, T)
        trist3 = r3_features[:, :, self._R3_TRIST3]                    # (B, T)

        # Pitch & Chroma group F [25:41] — direct pitch measures
        pitch_class_entropy = r3_features[:, :, self._R3_PITCH_CLASS_ENTROPY]
        pitch_salience      = r3_features[:, :, self._R3_PITCH_SALIENCE]

        # Harmony group H [51:63] — tonal context
        key_clarity     = r3_features[:, :, self._R3_KEY_CLARITY]
        tonal_stability = r3_features[:, :, self._R3_TONAL_STABILITY]

        # === Stage 2: Extract H³ temporal features (48 demands) ===
        #
        # Organized by law: L2 (Present), L0 (Past), L1 (Future).
        # Signed morphs (trend = M18) are centered at 0.5:
        #   > 0.5 = increasing,  < 0.5 = decreasing,  0.5 = stable

        _neutral = torch.full((B, T), 0.5, device=device)

        def _h3(key, fallback=None):
            v = h3_features.get(key)
            if v is not None:
                return v
            return fallback if fallback is not None else torch.zeros(
                B, T, device=device,
            )

        # ── PRESENT demands (L2 = Integration, 19 tuples) ──

        # Roughness (R³[0])
        h3_rough_inst    = _h3((0, 0, 0, 2),  roughness)       # H0 present
        h3_rough_mean    = _h3((0, 3, 1, 2),  roughness)       # H3 present mean

        # Helmholtz (R³[2])
        h3_helm_inst     = _h3((2, 0, 0, 2),  helmholtz)       # H0 present
        h3_helm_mean     = _h3((2, 3, 1, 2),  helmholtz)       # H3 present mean

        # Stumpf (R³[3])
        h3_stumpf_inst   = _h3((3, 0, 0, 2),  stumpf)          # H0 present

        # Inharmonicity (R³[5])
        h3_inharm_inst   = _h3((5, 0, 0, 2),  inharmonicity)   # H0 present

        # Harmonic deviation (R³[6])
        h3_hdev_inst     = _h3((6, 0, 0, 2),  harmonic_dev)    # H0 present

        # Tristimulus (R³[18-20])
        h3_trist1        = _h3((18, 0, 0, 2), trist1)
        h3_trist2        = _h3((19, 0, 0, 2), trist2)
        h3_trist3        = _h3((20, 0, 0, 2), trist3)

        # Group E (Interactions) dissolved — coupling demands removed

        # Pitch class entropy (R³[38])
        h3_pce_inst      = _h3((38, 0, 0, 2), pitch_class_entropy)
        h3_pce_mean      = _h3((38, 3, 1, 2), pitch_class_entropy)

        # Pitch salience (R³[39])
        h3_pitchsal_inst = _h3((39, 0, 0, 2), pitch_salience)  # H0 present
        h3_pitchsal_h3   = _h3((39, 3, 0, 2), pitch_salience)  # H3 present
        h3_pitchsal_h6   = _h3((39, 6, 0, 2), pitch_salience)  # H6 present

        # Key clarity (R³[51])
        h3_keyclarity_h3   = _h3((51, 3, 0, 2), key_clarity)   # H3 present
        h3_keyclarity_mean = _h3((51, 3, 1, 2), key_clarity)   # H3 present mean
        h3_keyclarity_h6   = _h3((51, 6, 0, 2), key_clarity)   # H6 present

        # Tonal stability (R³[60])
        h3_tonalstab_h3  = _h3((60, 3, 0, 2), tonal_stability) # H3 present

        # ── PAST demands (L0 = Memory, 16 tuples) ──

        # Roughness memory
        h3_rough_trend_mem   = _h3((0, 6, 18, 0), _neutral)    # H6 200ms trend
        h3_rough_H12_mem     = _h3((0, 12, 1, 0))              # H12 525ms mean
        h3_rough_H16_mem     = _h3((0, 16, 1, 0))              # H16 1s mean

        # Helmholtz memory
        h3_helm_H12_mem      = _h3((2, 12, 1, 0))              # H12 525ms mean
        h3_helm_H18_mem      = _h3((2, 18, 1, 0))              # H18 2s mean

        # Stumpf memory
        h3_stumpf_H6_mem     = _h3((3, 6, 1, 0),  stumpf)      # H6 200ms mean
        h3_stumpf_H16_mem    = _h3((3, 16, 1, 0))              # H16 1s mean

        # Inharmonicity memory
        h3_inharm_trend_mem  = _h3((5, 3, 18, 0), _neutral)    # H3 trend
        h3_inharm_H12_mem    = _h3((5, 12, 1, 0))              # H12 525ms mean

        # Harmonic deviation memory
        h3_hdev_H3_mem       = _h3((6, 3, 1, 0),  harmonic_dev) # H3 mean
        h3_hdev_H12_mem      = _h3((6, 12, 1, 0))              # H12 525ms mean

        # Pitch salience memory
        h3_pitchsal_H12_mem  = _h3((39, 12, 1, 0))             # H12 525ms mean
        h3_pitchsal_H18_mem  = _h3((39, 18, 1, 0))             # H18 2s mean

        # Key clarity memory
        h3_keyclarity_H12_mem = _h3((51, 12, 1, 0))            # H12 525ms mean
        h3_keyclarity_H18_mem = _h3((51, 18, 1, 0))            # H18 2s mean

        # Tonal stability memory
        h3_tonalstab_H6_mem  = _h3((60, 6, 1, 0), tonal_stability)  # H6 200ms
        h3_tonalstab_H18_mem = _h3((60, 18, 1, 0))             # H18 2s mean

        # ── FUTURE demands (L1 = Prediction, 12 tuples) ──

        # Roughness prediction
        h3_rough_H6_pred     = _h3((0, 6, 1, 1))               # H6 200ms mean
        h3_rough_H12_pred    = _h3((0, 12, 18, 1), _neutral)   # H12 525ms trend

        # Helmholtz prediction
        h3_helm_H6_pred      = _h3((2, 6, 1, 1))               # H6 200ms mean
        h3_helm_H12_pred     = _h3((2, 12, 1, 1))              # H12 525ms mean

        # Stumpf prediction
        h3_stumpf_H6_pred    = _h3((3, 6, 1, 1))               # H6 200ms mean

        # Inharmonicity prediction
        h3_inharm_H6_pred    = _h3((5, 6, 18, 1), _neutral)    # H6 200ms trend

        # Pitch salience prediction
        h3_pitchsal_H6_pred  = _h3((39, 6, 1, 1))              # H6 200ms mean
        h3_pitchsal_H12_pred = _h3((39, 12, 1, 1))             # H12 525ms mean

        # Key clarity prediction
        h3_keyclarity_H6_pred  = _h3((51, 6, 1, 1))            # H6 200ms mean
        h3_keyclarity_H16_pred = _h3((51, 16, 1, 1))           # H16 1s mean

        # Tonal stability prediction
        h3_tonalstab_H6_pred   = _h3((60, 6, 1, 1))            # H6 200ms mean
        h3_tonalstab_H12_pred  = _h3((60, 12, 1, 1))           # H12 525ms mean

        # === Stage 3: Tristimulus balance (using present H³ values) ===
        trist_stack = torch.stack(
            [h3_trist1, h3_trist2, h3_trist3], dim=-1,
        )  # (B, T, 3)
        trist_balance = 1.0 - trist_stack.std(dim=-1)           # (B, T)

        # ═══════════════════════════════════════════════════════════════
        # E-LAYER (4D): Extraction — instantaneous R³ features
        # No H³ temporal processing. Direct products, no sigmoid.
        # ═══════════════════════════════════════════════════════════════

        # nps: Neural Pitch Salience — IC FFR at fundamental
        # Blends proxy (tonalness × autocorr) with direct pitch_salience
        nps = ALPHA * (
            0.5 * tonalness * autocorr                         # proxy via C[14]×C[17]
            + 0.5 * pitch_salience                             # direct via F[39]
        )                                                       # [0, 0.90]

        # harmonicity: Harmonicity Index — harmonic coincidence ratio
        harmonicity = BETA * (1.0 - inharmonicity) * (
            0.5 * trist_balance                                # spectral energy balance
            + 0.5 * (1.0 - pitch_class_entropy)                # tonal clarity
        )                                                       # [0, 0.85]

        # hierarchy: Consonance Hierarchy — P1 > P5 > P4 > M3 > m6 > TT
        hierarchy = GAMMA * helmholtz * stumpf                  # [0, 0.80]

        # ffr_behavior: FFR-Behavior Correlation — r = 0.81
        ffr_behavior = FFR_CORR * (nps + harmonicity) / 2.0    # [0, ~0.71]

        # ═══════════════════════════════════════════════════════════════
        # M-LAYER (4D): Memory — past consonance state
        # All inputs from L0 (memory) demands. Weights sum to 1.0.
        # ═══════════════════════════════════════════════════════════════

        # consonance_memory: Was the recent past consonant?
        # Short-term (H6) + beat-level (H12) + measure-level (H16/H18) memory
        consonance_memory = (
            0.15 * (1.0 - h3_rough_trend_mem)          # roughness not increasing (H6)
            + 0.10 * (1.0 - h3_rough_H16_mem)          # low roughness over measure (H16)
            + 0.15 * h3_helm_H12_mem                   # consonance at beat level (H12)
            + 0.15 * h3_helm_H18_mem                   # consonance at phrase level (H18)
            + 0.15 * h3_stumpf_H6_mem                  # fusion at short-term (H6)
            + 0.10 * h3_stumpf_H16_mem                 # fusion at measure level (H16)
            + 0.10 * (1.0 - h3_hdev_H3_mem)            # low harmonic deviation (H3)
            + 0.10 * (1.0 - h3_hdev_H12_mem)           # low deviation at beat (H12)
        )                                               # [0, 1]

        # pitch_memory: Was pitch clear and stable in the past?
        pitch_memory = (
            0.15 * (1.0 - h3_inharm_trend_mem)         # inharmonicity stable (H3)
            + 0.15 * (1.0 - h3_inharm_H12_mem)         # low inharmonicity at beat (H12)
            + 0.20 * h3_pitchsal_H12_mem               # pitch salience at beat (H12)
            + 0.20 * h3_pitchsal_H18_mem               # pitch salience at phrase (H18)
            + 0.15 * h3_tonalstab_H6_mem               # tonal stability short (H6)
            + 0.15 * h3_tonalstab_H18_mem              # tonal stability phrase (H18)
        )                                               # [0, 1]

        # tonal_memory: What tonal context was established?
        tonal_memory = (
            0.25 * h3_keyclarity_H12_mem               # key clarity at beat (H12)
            + 0.25 * h3_keyclarity_H18_mem             # key clarity at phrase (H18)
            + 0.25 * h3_tonalstab_H6_mem               # tonal stability short (H6)
            + 0.25 * h3_tonalstab_H18_mem              # tonal stability phrase (H18)
        )                                               # [0, 1]

        # spectral_memory: Overall spectral history summary
        spectral_memory = (
            0.15 * (1.0 - h3_rough_trend_mem)          # roughness direction (H6)
            + 0.10 * (1.0 - h3_rough_H12_mem)          # roughness level at beat (H12)
            + 0.15 * h3_stumpf_H6_mem                  # fusion history (H6)
            + 0.10 * h3_stumpf_H16_mem                 # fusion history at measure (H16)
            + 0.15 * h3_pitchsal_H12_mem               # pitch salience at beat (H12)
            + 0.10 * h3_pitchsal_H18_mem               # pitch salience at phrase (H18)
            + 0.15 * h3_keyclarity_H12_mem             # key clarity at beat (H12)
            + 0.10 * h3_tonalstab_H18_mem              # tonal stability at phrase (H18)
        )                                               # [0, 1]

        # ═══════════════════════════════════════════════════════════════
        # P-LAYER (4D): Present — context-aware current state
        # All temporal inputs from L2 (integration) demands + R³ direct.
        # ═══════════════════════════════════════════════════════════════

        # consonance_signal: Current consonance in bidirectional context
        # (Group E coupling terms removed — weights redistributed)
        consonance_signal = (
            0.20 * (1.0 - h3_rough_inst)               # low roughness (H0)
            + 0.20 * (1.0 - h3_rough_mean)             # sustained low roughness (H3)
            + 0.10 * (1.0 - sethares)                  # low Sethares dissonance
            + 0.10 * sens_pleasant                      # sensory pleasantness
            + 0.15 * (1.0 - harmonic_dev)              # harmonic regularity
            + 0.10 * h3_keyclarity_h6                  # tonal context (H6)
            + 0.15 * (1.0 - h3_pce_mean)               # tonal clarity (H3)
        )                                               # [0, 1]

        # template_match: Harmonic template matching in context
        template_match = (
            0.15 * h3_helm_inst                        # consonance (H0)
            + 0.15 * h3_helm_mean                      # sustained consonance (H3)
            + 0.15 * h3_stumpf_inst                    # fusion (H0)
            + 0.15 * (1.0 - h3_hdev_inst)              # low harmonic deviation (H0)
            + 0.10 * (1.0 - harmonic_dev)              # harmonic regularity
            + 0.10 * h3_keyclarity_h3                  # tonal context (H3)
            + 0.10 * h3_keyclarity_mean                # sustained key clarity (H3)
            + 0.10 * tonal_stability                   # R³ tonal stability
        )                                               # [0, 1]

        # neural_pitch: Pitch clarity in current context
        neural_pitch = (
            0.15 * h3_pitchsal_inst                    # pitch salience (H0)
            + 0.15 * h3_pitchsal_h3                    # pitch salience (H3)
            + 0.15 * h3_pitchsal_h6                    # pitch salience (H6)
            + 0.15 * (1.0 - h3_inharm_inst)            # low inharmonicity (H0)
            + 0.10 * tonalness                         # pitch clarity
            + 0.10 * autocorr                          # harmonic periodicity
            + 0.10 * (1.0 - pitch_class_entropy)       # tonal clarity
            + 0.10 * (1.0 - h3_pce_inst)               # H0 tonal clarity
        )                                               # [0, 1]

        # tonal_context: Current tonal environment (key + stability)
        tonal_context = (
            0.20 * h3_keyclarity_h3                    # key clarity (H3)
            + 0.15 * h3_keyclarity_mean                # sustained key clarity (H3)
            + 0.15 * h3_keyclarity_h6                  # key clarity (H6)
            + 0.15 * h3_tonalstab_h3                   # tonal stability (H3)
            + 0.10 * tonal_stability                   # R³ tonal stability
            + 0.15 * (1.0 - h3_pce_mean)               # sustained tonal clarity
            + 0.10 * (1.0 - h3_pce_inst)               # instantaneous clarity
        )                                               # [0, 1]

        # ═══════════════════════════════════════════════════════════════
        # F-LAYER (4D): Future — predicted trajectory
        # All temporal inputs from L1 (prediction) demands.
        # ═══════════════════════════════════════════════════════════════

        # consonance_forecast: Where is consonance heading?
        consonance_forecast = (
            0.20 * (1.0 - h3_rough_H6_pred)            # near-future roughness (H6)
            + 0.15 * (1.0 - h3_rough_H12_pred)         # roughness trend (H12)
            + 0.20 * h3_helm_H6_pred                   # consonance prediction (H6)
            + 0.15 * h3_helm_H12_pred                  # consonance prediction (H12)
            + 0.15 * h3_stumpf_H6_pred                 # fusion prediction (H6)
            + 0.15 * (1.0 - h3_inharm_H6_pred)         # inharmonicity prediction (H6)
        )                                               # [0, 1]

        # pitch_forecast: Where is pitch heading?
        pitch_forecast = (
            0.25 * h3_pitchsal_H6_pred                 # pitch salience prediction (H6)
            + 0.25 * h3_pitchsal_H12_pred              # pitch salience prediction (H12)
            + 0.25 * (1.0 - h3_inharm_H6_pred)         # inharmonicity prediction (H6)
            + 0.25 * h3_tonalstab_H6_pred              # tonal stability prediction (H6)
        )                                               # [0, 1]

        # tonal_forecast: Where is tonal context heading?
        tonal_forecast = (
            0.20 * h3_keyclarity_H6_pred               # key clarity prediction (H6)
            + 0.25 * h3_keyclarity_H16_pred            # key clarity prediction (H16)
            + 0.20 * h3_tonalstab_H6_pred              # stability prediction (H6)
            + 0.20 * h3_tonalstab_H12_pred             # stability prediction (H12)
            + 0.15 * h3_helm_H12_pred                  # consonance context (H12)
        )                                               # [0, 1]

        # interval_forecast: What interval changes are expected?
        interval_forecast = (
            0.20 * h3_helm_H6_pred                     # consonance prediction (H6)
            + 0.15 * h3_helm_H12_pred                  # consonance prediction (H12)
            + 0.15 * h3_stumpf_H6_pred                 # fusion prediction (H6)
            + 0.15 * (1.0 - h3_rough_H6_pred)          # roughness prediction (H6)
            + 0.15 * h3_keyclarity_H6_pred             # tonal context prediction (H6)
            + 0.10 * h3_pitchsal_H6_pred               # pitch context (H6)
            + 0.10 * h3_tonalstab_H12_pred             # stability context (H12)
        )                                               # [0, 1]

        # === Assemble 16D output ===
        return torch.stack([
            # E-layer (4D): Extraction
            nps, harmonicity, hierarchy, ffr_behavior,
            # M-layer (4D): Memory (Past)
            consonance_memory, pitch_memory, tonal_memory, spectral_memory,
            # P-layer (4D): Present
            consonance_signal, template_match, neural_pitch, tonal_context,
            # F-layer (4D): Future
            consonance_forecast, pitch_forecast, tonal_forecast, interval_forecast,
        ], dim=-1)  # (B, T, 16)
