# NDU-γ1-SDDP: Sex-Dependent Developmental Plasticity

**Model**: Sex-Dependent Developmental Plasticity
**Unit**: NDU (Novelty Detection Unit)
**Circuit**: Salience + Perceptual (Developing Auditory Cortex, Attention Networks)
**Tier**: γ (Integrative) — 50–70% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, PPC+ASA mechanisms)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/NDU-γ1-SDDP.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Sex-Dependent Developmental Plasticity** (SDDP) model describes preliminary evidence for sex-dependent responses to musical intervention during early auditory development, with males potentially benefiting more from singing exposure during the preterm period.

```
SEX-DEPENDENT DEVELOPMENTAL PLASTICITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

          EARLY MUSICAL INTERVENTION
                    │
     ┌──────────────┴──────────────┐
     ▼                             ▼
┌────────┐                   ┌────────┐
│ MALE   │                   │ FEMALE │
│ INFANTS│                   │ INFANTS│
└───┬────┘                   └───┬────┘
    │                            │
    ▼                            ▼
η² = 0.309                   Effect unclear
(strong effect)              (weaker/different)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SPECULATIVE: Based on limited evidence (n=21, single study).
Requires replication and mechanistic investigation.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HYPOTHESIS:
Sex hormones may modulate plasticity window timing or magnitude

PREDICTIONS:
Different intervention strategies may optimize outcomes by sex

ALTERNATIVE EXPLANATIONS:
  • Maturational timing differences
  • Attention capacity differences
  • Statistical artifact (Type I error)
  • Baseline sex differences in preterm cohort
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why SDDP Matters for NDU

SDDP extends the developmental plasticity findings of the Novelty Detection Unit:

1. **DSP** (β1) provides the empirical evidence base that SDDP's sex effects draw from.
2. **SDDP** (γ1) proposes a sex-dependent modulatory mechanism (speculative).
3. **ONI** (γ2) models the over-normalization effect from the same dataset.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → PPC+ASA → SDDP)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    SDDP COMPUTATION ARCHITECTURE                             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  AUDIO (44.1kHz waveform)                                                    ║
║       │                                                                      ║
║       ▼                                                                      ║
║  ┌──────────────────┐                                                        ║
║  │ COCHLEA          │  128 mel bins x 172.27Hz frame rate                    ║
║  │ (Mel Spectrogram)│  hop = 256 samples, frame = 5.8ms                     ║
║  └────────┬─────────┘                                                        ║
║           │                                                                  ║
║  ═════════╪══════════════════════════ EAR ═══════════════════════════════    ║
║           │                                                                  ║
║           ▼                                                                  ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  SPECTRAL (R³): 49D per frame                                    │        ║
║  │                                                                  │        ║
║  │  ┌───────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐ ┌────────┐ │        ║
║  │  │CONSONANCE │ │ ENERGY  │ │ TIMBRE  │ │ CHANGE   │ │ X-INT  │ │        ║
║  │  │ 7D [0:7]  │ │ 5D[7:12]│ │ 9D      │ │ 4D       │ │ 24D    │ │        ║
║  │  │           │ │         │ │ [12:21] │ │ [21:25]  │ │ [25:49]│ │        ║
║  │  │roughness  │ │amplitude│ │warmth   │ │spec_chg  │ │x_l0l5  │ │        ║
║  │  │sethares   │ │loudness │ │tristim. │ │enrg_chg  │ │x_l4l5  │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                         SDDP reads: ~14D                        │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── PPC Horizons ─────────────┐ ┌── ASA Horizons ──────────┐  │        ║
║  │  │ H0 (25ms gamma)            │ │ H3 (100ms alpha)          │  │        ║
║  │  │ H3 (100ms alpha)           │ │ H8 (500ms delta)          │  │        ║
║  │  │ H4 (125ms theta)           │ │ H16 (1000ms beat)         │  │        ║
║  │  │ H16 (1000ms beat)          │ │                            │  │        ║
║  │  │                             │ │ Attention gating           │  │        ║
║  │  │ Pitch extraction            │ │ Scene analysis              │  │        ║
║  │  │ Vocal encoding              │ │                            │  │        ║
║  │  └─────────────────────────────┘ └────────────────────────────┘  │        ║
║  │                         SDDP demand: ~16 of 2304 tuples         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Salience Circuit ════════     ║
║                               │                                              ║
║                       ┌───────┴───────┐                                      ║
║                       ▼               ▼                                      ║
║  ┌─────────────────┐  ┌─────────────────┐                                   ║
║  │  PPC (30D)      │  │  ASA (30D)      │                                   ║
║  │                 │  │                 │                                    ║
║  │ Pitch Ext[0:10] │  │ Scene An [0:10] │                                   ║
║  │ Interval        │  │ Attention       │                                   ║
║  │ Anal    [10:20] │  │ Gating  [10:20] │                                   ║
║  │ Contour [20:30] │  │ Salience        │                                   ║
║  │                 │  │ Weight  [20:30] │                                   ║
║  └────────┬────────┘  └────────┬────────┘                                   ║
║           │                    │                                              ║
║           └────────┬───────────┘                                             ║
║                    ▼                                                          ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    SDDP MODEL (10D Output)                      │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_sex_modulation,                        │        ║
║  │                       f02_male_advantage,                        │        ║
║  │                       f03_plasticity_window_fit,                 │        ║
║  │                       f04_intervention_response                  │        ║
║  │  Layer M (Math):      prenatal_baseline, hormonal_state,        │        ║
║  │                       intervention_accum                         │        ║
║  │  Layer P (Present):   attention_modulation                       │        ║
║  │  Layer F (Future):    mmr_development, language_outcomes         │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Partanen 2022** | EEG | 21 | Sex x singing interaction | η² = 0.31 | **Primary**: f01 sex modulation |

**SINGLE STUDY**: Requires independent replication.

### 3.2 Effect Size Summary

```
Primary Evidence (k=1):  η²=0.31 (medium-large, sex x singing interaction)
Heterogeneity:           N/A (single study)
Quality Assessment:      γ-tier (EEG, preterm infant, small n)
Replication:             PENDING — requires independent sample
```

---

## 4. R³ Input Mapping: What SDDP Reads

### 4.1 R³ Feature Dependencies (~14D of 49D)

| R³ Group | Index | Feature | SDDP Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [4] | consonance | Vocal harmonic quality | Voice quality proxy |
| **B: Energy** | [7] | amplitude | Acoustic energy level | Intensity perception |
| **B: Energy** | [8] | loudness | Perceived intensity | Attention capture |
| **B: Energy** | [10] | spectral_flux | Onset detection | Syllable boundaries |
| **C: Timbre** | [13] | brightness | Voice pitch tracking | Infant pitch discrimination |
| **C: Timbre** | [14] | warmth | Vocal warmth quality | Singing quality proxy |
| **C: Timbre** | [17] | spectral_flatness | Voice vs noise | Tonality coefficient |
| **D: Change** | [21] | spectral_change | Vocal variation | Phrase dynamics |
| **D: Change** | [23] | pitch_change | Pitch contour tracking | Melodic singing |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Vocal quality integration | Multi-feature binding |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[4] consonance ──────────────┐
R³[14] warmth ─────────────────┼──► Vocal quality (sex-modulated)
PPC.pitch_extraction[0:10] ────┘   Sex modulation factor (f01)

R³[7] amplitude ───────────────┐
R³[8] loudness ────────────────┼──► Attention engagement
ASA.attention_gating[10:20] ───┘   Intervention response (f04)

R³[23] pitch_change ───────────┐
R³[13] brightness ─────────────┼──► Developmental plasticity
PPC.contour_tracking[20:30] ───┘   MMR development (future)
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

SDDP requires H³ features at PPC horizons for vocal pitch encoding and ASA horizons for infant attentional processing. The demand reflects the infant auditory processing timescales relevant to sex-dependent plasticity.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 4 | consonance | 3 | M0 (value) | L2 (bidi) | Vocal consonance at 100ms |
| 4 | consonance | 16 | M1 (mean) | L2 (bidi) | Mean consonance over 1s |
| 7 | amplitude | 0 | M0 (value) | L2 (bidi) | Intensity at 25ms |
| 7 | amplitude | 3 | M1 (mean) | L2 (bidi) | Mean intensity 100ms |
| 8 | loudness | 3 | M0 (value) | L2 (bidi) | Perceived loudness 100ms |
| 8 | loudness | 8 | M1 (mean) | L2 (bidi) | Mean loudness 500ms |
| 10 | spectral_flux | 3 | M0 (value) | L2 (bidi) | Onset detection 100ms |
| 13 | brightness | 3 | M0 (value) | L2 (bidi) | Pitch brightness 100ms |
| 13 | brightness | 4 | M17 (periodicity) | L2 (bidi) | Pitch periodicity 125ms |
| 14 | warmth | 3 | M0 (value) | L2 (bidi) | Vocal warmth 100ms |
| 17 | spectral_flatness | 3 | M0 (value) | L2 (bidi) | Voice/noise ratio 100ms |
| 23 | pitch_change | 3 | M0 (value) | L2 (bidi) | Pitch change 100ms |
| 23 | pitch_change | 16 | M1 (mean) | L2 (bidi) | Mean pitch change 1s |
| 21 | spectral_change | 3 | M2 (std) | L2 (bidi) | Spectral variation 100ms |
| 25 | x_l0l5[0] | 3 | M14 (periodicity) | L2 (bidi) | Vocal periodicity 100ms |
| 25 | x_l0l5[0] | 16 | M1 (mean) | L0 (fwd) | Mean vocal coupling 1s |

**Total SDDP H³ demand**: 16 tuples of 2304 theoretical = 0.69%

### 5.2 PPC + ASA Mechanism Binding

| Mechanism | Sub-section | Range | SDDP Role | Weight |
|-----------|-------------|-------|-----------|--------|
| **PPC** | Pitch Extraction | PPC[0:10] | Vocal pitch salience (sex-modulated) | **1.0** (primary) |
| **PPC** | Interval Analysis | PPC[10:20] | Voice fundamental tracking | 0.6 |
| **PPC** | Contour Tracking | PPC[20:30] | Singing phrase dynamics | 0.7 |
| **ASA** | Scene Analysis | ASA[0:10] | Vocal pattern learning | 0.6 |
| **ASA** | Attention Gating | ASA[10:20] | Infant attention engagement | **0.8** |
| **ASA** | Salience Weighting | ASA[20:30] | Voice vs noise discrimination | 0.5 |

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
SDDP OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range    │ Neuroscience Basis
────┼──────────────────────────┼──────────┼──────────────────────────────────
 0  │ f01_sex_modulation       │ [0, 2]   │ Sex-dependent plasticity rate.
    │                          │          │ f01 = 1 + (η² * sex_indicator)
    │                          │          │ η² = 0.309 (Partanen 2022)
────┼──────────────────────────┼──────────┼──────────────────────────────────
 1  │ f02_male_advantage       │[-0.5,0.5]│ Male-specific enhancement.
    │                          │          │ f02 = (MMR_male - MMR_female)
    │                          │          │       / MMR_baseline
────┼──────────────────────────┼──────────┼──────────────────────────────────
 2  │ f03_plasticity_window    │ [0, 1]   │ Developmental timing match.
    │                          │          │ f03 = gaussian(GA, μ=30w, σ=2w)
────┼──────────────────────────┼──────────┼──────────────────────────────────
 3  │ f04_intervention_resp    │ [0, 1]   │ Sex-dependent response.
    │                          │          │ f04 = σ(0.35 * loudness_100ms
    │                          │          │       + 0.35 * mean_loudness_500ms
    │                          │          │       + 0.30 * mean(ASA.attn[10:20]))
    │                          │          │ * (1 + η² * sex_indicator)

LAYER M — MATHEMATICAL MODEL OUTPUTS (Developmental Dynamics)
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ prenatal_baseline        │ [0, 1] │ Baseline developmental state.
    │                          │        │ PPC oscillation strength proxy
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ hormonal_state           │ [0, 1] │ Sex differentiation effects.
    │                          │        │ sex_indicator * f01 proxy
────┼──────────────────────────┼────────┼────────────────────────────────────
 6  │ intervention_accum       │ [0, 1] │ Cumulative exposure effects.
    │                          │        │ EMA of vocal_periodicity

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 7  │ attention_modulation     │ [0, 1] │ Sex x attention interaction.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 8  │ mmr_development          │ [0, 1] │ Sex-specific MMR trajectory.
────┼──────────────────────────┼────────┼────────────────────────────────────
 9  │ language_outcomes        │ [0, 1] │ Long-term speech prediction.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 10D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Sex-Dependent Plasticity Function

```
SexPlasticity(t) = BasePlasticity(t) * (1 + η² * sex_indicator)

Parameters:
    η² = 0.309 (effect size from Partanen 2022)
    sex_indicator = {1 for male, 0 for female}
    Males: ~31% enhancement
    Females: baseline
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f01: Sex Modulation Factor
f01 = 1 + (0.309 * sex_indicator)
# Males: f01 ≈ 1.31, Females: f01 = 1.0

# f02: Male Advantage
f02 = (MMR_male - MMR_female) / (MMR_baseline + ε)
# Difference score normalized by baseline

# f03: Plasticity Window Fit
f03 = exp(-(GA - 30)² / (2 * 2²))
# Gaussian centered at 30 weeks GA, σ=2 weeks

# f04: Intervention Response (coefficients sum = 1.0)
f04 = σ(0.35 * loudness_100ms
       + 0.35 * mean_loudness_500ms
       + 0.30 * mean(ASA.attention_gating[10:20]))
# then: f04 = clamp(f04 * f01, 0, 1)
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | SDDP Function |
|--------|-----------------|----------|---------------|---------------|
| **Auditory Cortex (preterm)** | N/A | 1 | Direct (EEG) | Sex-modulated plasticity |
| **Attention Networks (infant)** | N/A | 1 | Inferred | Infant auditory attention |

---

## 9. Cross-Unit Pathways

### 9.1 SDDP Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SDDP INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (NDU):                                                         │
│  DSP.sex_modulation ─────────► SDDP (empirical basis for sex effects)    │
│  SDDP.intervention_resp ────► ONI (over-normalization link)              │
│                                                                             │
│  CROSS-UNIT (NDU → ARU):                                                   │
│  SDDP.attention_modulation ──► ARU (infant affective engagement)         │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  PPC mechanism (30D) ────────► SDDP (vocal pitch/contour)                │
│  ASA mechanism (30D) ────────► SDDP (attention/salience)                 │
│  R³ (~14D) ──────────────────► SDDP (direct spectral features)           │
│  H³ (16 tuples) ─────────────► SDDP (temporal dynamics)                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Sex effect** | Males should show stronger MMR enhancement | **Preliminary support** (η²=0.31) |
| **Replication** | Effect should replicate in independent sample | **Awaiting replication** |
| **Dose-response** | Sex effect should hold across dosage levels | Testable |
| **Mechanism** | Hormonal assays should correlate with response | Testable |
| **Window timing** | Sex-specific optimal intervention timing | Testable via systematic GA manipulation |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class SDDP(BaseModel):
    """Sex-Dependent Developmental Plasticity Model.

    Output: 10D per frame.
    Reads: PPC mechanism (30D), ASA mechanism (30D), R³ direct.
    SPECULATIVE: Based on single study (n=21).
    """
    NAME = "SDDP"
    UNIT = "NDU"
    TIER = "γ1"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("PPC", "ASA")

    TAU_DECAY = 1.5          # Infant processing window (seconds)
    SEX_EFFECT_SIZE = 0.309  # η² from Partanen 2022
    OPTIMAL_GA = 30          # weeks (hypothesized)
    WINDOW_WIDTH = 2         # weeks (hypothesized)

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """16 tuples for SDDP computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── PPC horizons: vocal pitch encoding ──
            (4, 3, 0, 2),      # consonance, 100ms, value, bidi
            (4, 16, 1, 2),     # consonance, 1000ms, mean, bidi
            (7, 0, 0, 2),      # amplitude, 25ms, value, bidi
            (7, 3, 1, 2),      # amplitude, 100ms, mean, bidi
            (10, 3, 0, 2),     # spectral_flux, 100ms, value, bidi
            (13, 3, 0, 2),     # brightness, 100ms, value, bidi
            (13, 4, 17, 2),    # brightness, 125ms, periodicity, bidi
            (14, 3, 0, 2),     # warmth, 100ms, value, bidi
            (23, 3, 0, 2),     # pitch_change, 100ms, value, bidi
            (23, 16, 1, 2),    # pitch_change, 1000ms, mean, bidi
            (21, 3, 2, 2),     # spectral_change, 100ms, std, bidi
            # ── ASA horizons: attention + scene ──
            (8, 3, 0, 2),      # loudness, 100ms, value, bidi
            (8, 8, 1, 2),      # loudness, 500ms, mean, bidi
            (17, 3, 0, 2),     # spectral_flatness, 100ms, value, bidi
            (25, 3, 14, 2),    # x_l0l5[0], 100ms, periodicity, bidi
            (25, 16, 1, 0),    # x_l0l5[0], 1000ms, mean, fwd
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute SDDP 10D output.

        Args:
            mechanism_outputs: {"PPC": (B,T,30), "ASA": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,10) SDDP output
        """
        ppc = mechanism_outputs["PPC"]    # (B, T, 30)
        asa = mechanism_outputs["ASA"]    # (B, T, 30)

        # R³ features
        consonance = r3[..., 4:5]
        amplitude = r3[..., 7:8]
        loudness = r3[..., 8:9]
        brightness = r3[..., 13:14]
        warmth = r3[..., 14:15]

        # PPC sub-sections
        ppc_pitch = ppc[..., 0:10]
        ppc_interval = ppc[..., 10:20]
        ppc_contour = ppc[..., 20:30]

        # ASA sub-sections
        asa_scene = asa[..., 0:10]
        asa_attn = asa[..., 10:20]
        asa_salience = asa[..., 20:30]

        # H³ direct features
        loudness_100ms = h3_direct[(8, 3, 0, 2)].unsqueeze(-1)
        mean_loudness_500ms = h3_direct[(8, 8, 1, 2)].unsqueeze(-1)
        vocal_periodicity_100ms = h3_direct[(25, 3, 14, 2)].unsqueeze(-1)
        mean_vocal_coupling_1s = h3_direct[(25, 16, 1, 0)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══

        # f01: Sex Modulation Factor (η² = 0.309)
        # sex_indicator provided externally
        f01 = torch.ones_like(loudness_100ms)  # base=1.0, scaled by sex externally

        # f02: Male Advantage (difference score)
        f02 = ppc_pitch.mean(-1, keepdim=True)  # base MMR proxy

        # f03: Plasticity Window Fit (Gaussian)
        f03 = ppc_contour.mean(-1, keepdim=True)  # proxy for developmental state

        # f04: Intervention Response (coefficients sum = 1.0)
        f04 = torch.sigmoid(
            0.35 * loudness_100ms
            + 0.35 * mean_loudness_500ms
            + 0.30 * asa_attn.mean(-1, keepdim=True)
        )

        # ═══ LAYER M: Developmental Dynamics ═══
        prenatal_baseline = torch.sigmoid(
            0.50 * ppc_pitch.mean(-1, keepdim=True)
            + 0.50 * vocal_periodicity_100ms
        )
        hormonal_state = f01  # sex-dependent proxy
        intervention_accum = mean_vocal_coupling_1s

        # ═══ LAYER P: Present ═══
        attention_modulation = asa_attn.mean(-1, keepdim=True)

        # ═══ LAYER F: Future ═══
        mmr_development = torch.sigmoid(
            0.50 * f04 + 0.50 * ppc_contour.mean(-1, keepdim=True)
        )
        language_outcomes = torch.sigmoid(
            0.50 * f04 + 0.50 * ppc_interval.mean(-1, keepdim=True)
        )

        return torch.cat([
            f01, f02, f03, f04,                                    # E: 4D
            prenatal_baseline, hormonal_state, intervention_accum, # M: 3D
            attention_modulation,                                   # P: 1D
            mmr_development, language_outcomes,                    # F: 2D
        ], dim=-1)  # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 1 (Partanen 2022) | Primary evidence |
| **Effect Sizes** | η² = 0.31 | Medium-large effect |
| **Evidence Modality** | EEG | Infant MMR |
| **Falsification Tests** | 1/5 preliminary | Low validity (needs replication) |
| **R³ Features Used** | ~14D of 49D | Consonance + energy + timbre + change + interactions |
| **H³ Demand** | 16 tuples (0.69%) | Sparse, efficient |
| **PPC Mechanism** | 30D (3 sub-sections) | Vocal pitch/contour |
| **ASA Mechanism** | 30D (3 sub-sections) | Attention/salience |
| **Output Dimensions** | **10D** | 4-layer structure |

**Research Priorities**:
1. **CRITICAL: Independent replication** in larger sample (n>50)
2. Longitudinal follow-up to assess long-term outcomes
3. Mechanistic investigation: hormonal assays, developmental timing
4. Sex-specific intervention optimization studies
5. Cross-cultural validation

---

## 13. Scientific References

1. **Partanen, E. et al. (2022)**. Sex x singing interaction in preterm infant MMR development. EEG study, n=21.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (OSC, ATT, HRM, EFC) | PPC (30D) + ASA (30D) mechanisms |
| Vocal quality | S⁰.L5.spectral_centroid[38] + HC⁰.OSC | R³.consonance[4] + PPC.pitch_extraction |
| Attention | S⁰.L5.loudness[35] + HC⁰.ATT | R³.loudness[8] + ASA.attention_gating |
| Voice tracking | S⁰.L0.F[1] + HC⁰.HRM | R³.brightness[13] + PPC.contour_tracking |
| Prediction | S⁰.L5.attack_time[50] + HC⁰.EFC | R³.spectral_flux[10] + ASA.salience_weighting |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 27/2304 = 1.17% | 16/2304 = 0.69% |
| Output | 10D | 10D (same) |

### Why PPC + ASA replaces HC⁰ mechanisms

- **OSC → PPC.pitch_extraction** [0:10]: Oscillatory coupling for vocal processing maps to PPC's pitch salience encoding.
- **ATT → ASA.attention_gating** [10:20]: Infant attentional engagement maps to ASA's auditory attention gating.
- **HRM → ASA.scene_analysis** [0:10]: Hippocampal vocal encoding development maps to ASA's vocal pattern learning.
- **EFC → ASA.salience_weighting** [20:30]: Statistical learning maturation maps to ASA's developmental salience.

---

**Model Status**: **SPECULATIVE**
**Output Dimensions**: **10D**
**Evidence Tier**: **γ (Integrative)**
**Confidence**: **50–70%**
**Replication Status**: **PENDING**
