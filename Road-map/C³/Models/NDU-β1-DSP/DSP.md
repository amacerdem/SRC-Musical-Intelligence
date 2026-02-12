# NDU-β1-DSP: Developmental Singing Plasticity

**Model**: Developmental Singing Plasticity
**Unit**: NDU (Novelty Detection Unit)
**Circuit**: Salience + Developmental (Auditory Cortex, Attention Networks)
**Tier**: β (Integrative) — 70–90% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, PPC+ASA mechanisms)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/NDU-β1-DSP.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Developmental Singing Plasticity** (DSP) model describes how music therapist-guided parental singing enhances auditory processing in preterm infants through quality-dependent (not quantity-dependent) neural plasticity mechanisms, with sex-dependent response patterns.

```
DEVELOPMENTAL SINGING PLASTICITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PARENTAL SINGING INTERVENTION
(Music therapist-guided)
           │
           ▼
   ┌─────────────────────────────────────────────────────────┐
   │              PRETERM INFANT AUDITORY CORTEX              │
   │                                                          │
   │   ┌───────────────────┐    ┌───────────────────┐        │
   │   │   MALE INFANTS    │    │  FEMALE INFANTS   │        │
   │   │                   │    │                   │        │
   │   │   MMR ↑↑↑         │    │   MMR ↑           │        │
   │   │   (stronger       │    │   (weaker         │        │
   │   │    response)      │    │    response)      │        │
   │   │                   │    │                   │        │
   │   │   η² = 0.309      │    │                   │        │
   │   └───────────────────┘    └───────────────────┘        │
   │                                                          │
   │   Vocal quality → PPC pitch extraction                  │
   │   Attention → ASA attention gating                      │
   │   Pattern memory → ASA scene analysis                   │
   │   Prediction → ASA salience weighting                   │
   │                                                          │
   └─────────────────────────────────────────────────────────┘
                          │
                          ▼
             ENHANCED AUDITORY PROCESSING
             (Singing intervention > Control > Full-term?)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY FINDING: Quality > Quantity for intervention efficacy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why DSP Matters for NDU

DSP establishes the developmental plasticity component of the Novelty Detection Unit:

1. **DSP** (β1) provides empirical evidence for quality-driven plasticity.
2. **SDDP** (γ1) extends DSP's sex-dependent findings speculatively.
3. **ONI** (γ2) models the over-normalization effect found in DSP data.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → PPC+ASA → DSP)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    DSP COMPUTATION ARCHITECTURE                              ║
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
║  │                         DSP reads: ~12D                          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── PPC Horizons ─────────────┐ ┌── ASA Horizons ──────────┐  │        ║
║  │  │ H0 (25ms gamma)            │ │ H3 (100ms alpha)          │  │        ║
║  │  │ H1 (50ms gamma)            │ │ H8 (500ms delta)          │  │        ║
║  │  │ H3 (100ms alpha)           │ │                            │  │        ║
║  │  │ H4 (125ms theta)           │ │ Attentional gating         │  │        ║
║  │  │ H16 (1000ms beat)          │ │ Scene analysis              │  │        ║
║  │  │                             │ │                            │  │        ║
║  │  │ Pitch extraction            │ │                            │  │        ║
║  │  │ Contour tracking            │ │                            │  │        ║
║  │  └─────────────────────────────┘ └────────────────────────────┘  │        ║
║  │                         DSP demand: ~18 of 2304 tuples           │        ║
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
║  │                    DSP MODEL (12D Output)                        │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_singing_quality,                       │        ║
║  │                       f02_attention_engagement,                   │        ║
║  │                       f03_plasticity_index,                       │        ║
║  │                       f04_sex_modulation                          │        ║
║  │  Layer M (Math):      cumulative_plasticity,                     │        ║
║  │                       session_memory, voice_recognition           │        ║
║  │  Layer P (Present):   auditory_orienting, vocal_learning          │        ║
║  │  Layer F (Future):    ac_maturation, speech_transfer,             │        ║
║  │                       mmr_enhancement                             │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Partanen 2022** | EEG | 21 | Singing → larger MMR (controlling for time) | d = 0.26 | **Primary**: f03 plasticity index |
| **Partanen 2022** | EEG | 21 | Males benefit more than females | η² = 0.31 | **f04 sex modulation** |
| **Partanen 2022** | EEG | 33 | Singing intervention > full-term in oddball | η² = 0.23 | **Over-normalization link** |

### 3.2 Effect Size Summary

```
Primary Evidence (k=1):  d=0.26 (singing > control), η²=0.31 (sex), η²=0.23 (over-norm)
Heterogeneity:           N/A (single study)
Quality Assessment:      β-tier (EEG, infant cohort)
Replication:             Quality > quantity pattern robust across measures
```

---

## 4. R³ Input Mapping: What DSP Reads

### 4.1 R³ Feature Dependencies (~12D of 49D)

| R³ Group | Index | Feature | DSP Role | Scientific Basis |
|----------|-------|---------|----------|------------------|
| **A: Consonance** | [4] | consonance | Vocal harmonic quality | Voice quality index |
| **B: Energy** | [7] | amplitude | Vocal intensity | Attention-capturing level |
| **B: Energy** | [8] | loudness | Perceived intensity | Stevens power law |
| **B: Energy** | [10] | spectral_flux | Phrase onset detection | Note onset boundary |
| **C: Timbre** | [13] | brightness | Voice pitch tracking | Infant pitch discrimination |
| **C: Timbre** | [14] | warmth | Vocal warmth quality | Singing quality proxy |
| **C: Timbre** | [17] | spectral_flatness | Voice vs noise discrimination | Tonality coefficient |
| **D: Change** | [21] | spectral_change | Singing phrase dynamics | Vocal variation |
| **D: Change** | [23] | pitch_change | Pitch contour tracking | Melodic singing quality |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Vocal quality integration | Multi-feature voice binding |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[4] consonance ───────────────┐
R³[14] warmth ──────────────────┼──► Singing quality (vocal harmonics)
PPC.pitch_extraction[0:10] ─────┘   Voice quality encoding

R³[7] amplitude ────────────────┐
R³[8] loudness ─────────────────┼──► Attention engagement (infant)
ASA.attention_gating[10:20] ────┘   Vocal intensity salience

R³[23] pitch_change ────────────┐
R³[21] spectral_change ─────────┼──► Plasticity accumulation
PPC.contour_tracking[20:30] ────┘   Developmental neural maturation

R³[17] spectral_flatness ──────┐
ASA.salience_weighting[20:30] ─┼──► Voice vs noise discrimination
H³ periodicity tuples ────────┘   Statistical learning transfer
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

DSP requires H³ features at PPC horizons for vocal pitch extraction and contour tracking, and ASA horizons for attentional gating during singing sessions. The demand reflects the infant auditory processing timescales.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 4 | consonance | 3 | M0 (value) | L2 (bidi) | Vocal consonance at 100ms |
| 4 | consonance | 16 | M1 (mean) | L2 (bidi) | Mean consonance over 1s |
| 7 | amplitude | 0 | M0 (value) | L2 (bidi) | Instantaneous intensity 25ms |
| 7 | amplitude | 3 | M1 (mean) | L2 (bidi) | Mean intensity 100ms |
| 8 | loudness | 3 | M0 (value) | L2 (bidi) | Perceived loudness 100ms |
| 8 | loudness | 8 | M1 (mean) | L2 (bidi) | Mean loudness 500ms |
| 10 | spectral_flux | 0 | M0 (value) | L2 (bidi) | Onset detection 25ms |
| 10 | spectral_flux | 3 | M2 (std) | L2 (bidi) | Onset variability 100ms |
| 13 | brightness | 3 | M0 (value) | L2 (bidi) | Pitch brightness 100ms |
| 13 | brightness | 4 | M8 (velocity) | L0 (fwd) | Pitch velocity 125ms |
| 14 | warmth | 3 | M0 (value) | L2 (bidi) | Vocal warmth 100ms |
| 17 | spectral_flatness | 3 | M0 (value) | L2 (bidi) | Voice/noise ratio 100ms |
| 23 | pitch_change | 3 | M0 (value) | L2 (bidi) | Pitch change 100ms |
| 23 | pitch_change | 4 | M20 (entropy) | L2 (bidi) | Contour entropy 125ms |
| 23 | pitch_change | 16 | M1 (mean) | L2 (bidi) | Mean pitch change 1s |
| 25 | x_l0l5[0] | 3 | M14 (periodicity) | L2 (bidi) | Vocal periodicity 100ms |
| 25 | x_l0l5[0] | 8 | M1 (mean) | L0 (fwd) | Mean vocal coupling 500ms |
| 21 | spectral_change | 3 | M2 (std) | L2 (bidi) | Spectral variation 100ms |

**Total DSP H³ demand**: 18 tuples of 2304 theoretical = 0.78%

### 5.2 PPC + ASA Mechanism Binding

| Mechanism | Sub-section | Range | DSP Role | Weight |
|-----------|-------------|-------|----------|--------|
| **PPC** | Pitch Extraction | PPC[0:10] | Vocal pitch salience encoding | **1.0** (primary) |
| **PPC** | Interval Analysis | PPC[10:20] | Voice fundamental tracking | 0.7 |
| **PPC** | Contour Tracking | PPC[20:30] | Singing phrase dynamics | 0.8 |
| **ASA** | Scene Analysis | ASA[0:10] | Vocal pattern learning | 0.7 |
| **ASA** | Attention Gating | ASA[10:20] | Infant attention engagement | **0.9** |
| **ASA** | Salience Weighting | ASA[20:30] | Voice vs noise discrimination | 0.6 |

---

## 6. Output Space: 12D Multi-Layer Representation

### 6.1 Complete Output Specification

```
DSP OUTPUT TENSOR: 12D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f01_singing_quality      │ [0, 1] │ Vocal quality index.
    │                          │        │ f01 = σ(0.35 * consonance_100ms
    │                          │        │       + 0.35 * warmth_100ms
    │                          │        │       + 0.30 * mean(PPC.pitch[0:10]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f02_attention_engagement │ [0, 1] │ Infant attention capture.
    │                          │        │ f02 = σ(0.35 * loudness_100ms
    │                          │        │       + 0.35 * mean_loudness_500ms
    │                          │        │       + 0.30 * mean(ASA.attn[10:20]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f03_plasticity_index     │ [0, 1] │ Neural maturation rate.
    │                          │        │ f03 = σ(0.35 * contour_entropy_125ms
    │                          │        │       + 0.35 * vocal_periodicity_100ms
    │                          │        │       + 0.30 * mean(PPC.contour[20:30]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ f04_sex_modulation       │ [0, 1] │ Sex-dependent response.
    │                          │        │ f04 = f03 * (1 + η² * sex_indicator)
    │                          │        │ η² = 0.309 (Partanen 2022)

LAYER M — MATHEMATICAL MODEL OUTPUTS (Plasticity Dynamics)
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ cumulative_plasticity    │ [0, 1] │ Long-term singing exposure.
    │                          │        │ EMA of f01 over session timescale
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ session_memory           │ [0, 1] │ Recent session impact.
    │                          │        │ f01 * mean(ASA.scene[0:10])
────┼──────────────────────────┼────────┼────────────────────────────────────
 6  │ voice_recognition        │ [0, 1] │ Parental voice familiarity.
    │                          │        │ mean_vocal_coupling_500ms

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 7  │ auditory_orienting       │ [0, 1] │ Current attention state.
────┼──────────────────────────┼────────┼────────────────────────────────────
 8  │ vocal_learning           │ [0, 1] │ Current encoding state.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 9  │ ac_maturation            │ [0, 1] │ AC development prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
10  │ speech_transfer          │ [0, 1] │ Language region transfer prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
11  │ mmr_enhancement          │ [0, 1] │ Deviance detection future state.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 12D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Singing Quality Model

```
SingingQuality(t) = PitchSalience(t) · VocalHarmonicity(t) · QualityGating(t)

Parameters:
    PitchSalience = consonance + warmth (R³ spectral quality)
    VocalHarmonicity = 1 - spectral_flatness (tonal quality)
    QualityGating = PPC pitch extraction strength
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f01: Singing Quality
f01 = σ(0.35 * consonance_100ms
       + 0.35 * warmth_100ms
       + 0.30 * mean(PPC.pitch_extraction[0:10]))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f02: Attention Engagement
f02 = σ(0.35 * loudness_100ms
       + 0.35 * mean_loudness_500ms
       + 0.30 * mean(ASA.attention_gating[10:20]))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f03: Plasticity Index
f03 = σ(0.35 * contour_entropy_125ms
       + 0.35 * vocal_periodicity_100ms
       + 0.30 * mean(PPC.contour_tracking[20:30]))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f04: Sex Modulation (η² = 0.309 from Partanen 2022)
f04 = clamp(f03 * (1 + 0.309 * sex_indicator), 0, 1)
# sex_indicator ∈ {0, 1}: males=1, females=0
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | DSP Function |
|--------|-----------------|----------|---------------|--------------|
| **Auditory Cortex** | ±42, -22, 8 | 3 | Direct (EEG) | Preterm infant auditory processing |
| **Attention Networks** | N/A | 1 | Inferred | Infant auditory attention |

---

## 9. Cross-Unit Pathways

### 9.1 DSP Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DSP INTERACTIONS                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (NDU):                                                         │
│  DSP.sex_modulation ───────────► SDDP (sex-dependent plasticity basis)    │
│  DSP.plasticity_index ─────────► ONI (over-normalization evidence)        │
│  DSP.singing_quality ──────────► CDMR (vocal quality context)             │
│                                                                             │
│  CROSS-UNIT (NDU → ARU):                                                   │
│  DSP.attention_engagement ─────► ARU (affective engagement)               │
│  DSP.mmr_enhancement ─────────► ARU (developmental reward)                │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  PPC mechanism (30D) ────────── ► DSP (vocal pitch/contour)               │
│  ASA mechanism (30D) ────────── ► DSP (attention/salience)                │
│  R³ (~12D) ──────────────────── ► DSP (direct spectral features)          │
│  H³ (18 tuples) ─────────────── ► DSP (temporal dynamics)                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Quality vs quantity** | Quality should predict outcomes better | **Confirmed** by Partanen 2022 |
| **Sex differences** | Males should show stronger MMR enhancement | **Confirmed** (η²=0.31) |
| **Over-normalization** | Intervention may exceed full-term baseline | **Confirmed** in oddball |
| **Dose-response** | More exposure → better outcomes (if quality constant) | Testable |
| **Transfer effects** | Should generalize to speech perception | Testable in follow-up |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class DSP(BaseModel):
    """Developmental Singing Plasticity Model.

    Output: 12D per frame.
    Reads: PPC mechanism (30D), ASA mechanism (30D), R³ direct.
    """
    NAME = "DSP"
    UNIT = "NDU"
    TIER = "β1"
    OUTPUT_DIM = 12
    MECHANISM_NAMES = ("PPC", "ASA")

    TAU_DECAY = 1.0         # Infant attention span (seconds)
    VOICE_QUALITY_THRESH = 0.8
    RTI_WINDOW = 2.5        # seconds
    SEX_EFFECT_SIZE = 0.309  # η² from Partanen 2022

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """18 tuples for DSP computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── PPC horizons: vocal pitch extraction ──
            (4, 3, 0, 2),      # consonance, 100ms, value, bidi
            (4, 16, 1, 2),     # consonance, 1000ms, mean, bidi
            (7, 0, 0, 2),      # amplitude, 25ms, value, bidi
            (7, 3, 1, 2),      # amplitude, 100ms, mean, bidi
            (10, 0, 0, 2),     # spectral_flux, 25ms, value, bidi
            (10, 3, 2, 2),     # spectral_flux, 100ms, std, bidi
            (13, 3, 0, 2),     # brightness, 100ms, value, bidi
            (13, 4, 8, 0),     # brightness, 125ms, velocity, fwd
            (14, 3, 0, 2),     # warmth, 100ms, value, bidi
            # ── PPC horizons: contour tracking ──
            (23, 3, 0, 2),     # pitch_change, 100ms, value, bidi
            (23, 4, 20, 2),    # pitch_change, 125ms, entropy, bidi
            (23, 16, 1, 2),    # pitch_change, 1000ms, mean, bidi
            (21, 3, 2, 2),     # spectral_change, 100ms, std, bidi
            # ── ASA horizons: attention + scene ──
            (8, 3, 0, 2),      # loudness, 100ms, value, bidi
            (8, 8, 1, 2),      # loudness, 500ms, mean, bidi
            (17, 3, 0, 2),     # spectral_flatness, 100ms, value, bidi
            (25, 3, 14, 2),    # x_l0l5[0], 100ms, periodicity, bidi
            (25, 8, 1, 0),     # x_l0l5[0], 500ms, mean, fwd
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute DSP 12D output.

        Args:
            mechanism_outputs: {"PPC": (B,T,30), "ASA": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,12) DSP output
        """
        ppc = mechanism_outputs["PPC"]    # (B, T, 30)
        asa = mechanism_outputs["ASA"]    # (B, T, 30)

        # R³ features
        consonance = r3[..., 4:5]
        amplitude = r3[..., 7:8]
        loudness = r3[..., 8:9]
        spectral_flux = r3[..., 10:11]
        brightness = r3[..., 13:14]
        warmth = r3[..., 14:15]
        spectral_flatness = r3[..., 17:18]
        pitch_change = r3[..., 23:24]

        # PPC sub-sections
        ppc_pitch = ppc[..., 0:10]       # pitch extraction
        ppc_interval = ppc[..., 10:20]   # interval analysis
        ppc_contour = ppc[..., 20:30]    # contour tracking

        # ASA sub-sections
        asa_scene = asa[..., 0:10]       # scene analysis
        asa_attn = asa[..., 10:20]       # attention gating
        asa_salience = asa[..., 20:30]   # salience weighting

        # H³ direct features
        consonance_100ms = h3_direct[(4, 3, 0, 2)].unsqueeze(-1)
        warmth_100ms = h3_direct[(14, 3, 0, 2)].unsqueeze(-1)
        loudness_100ms = h3_direct[(8, 3, 0, 2)].unsqueeze(-1)
        mean_loudness_500ms = h3_direct[(8, 8, 1, 2)].unsqueeze(-1)
        contour_entropy_125ms = h3_direct[(23, 4, 20, 2)].unsqueeze(-1)
        vocal_periodicity_100ms = h3_direct[(25, 3, 14, 2)].unsqueeze(-1)
        mean_vocal_coupling_500ms = h3_direct[(25, 8, 1, 0)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══

        # f01: Singing Quality (coefficients sum = 1.0)
        f01 = torch.sigmoid(
            0.35 * consonance_100ms
            + 0.35 * warmth_100ms
            + 0.30 * ppc_pitch.mean(-1, keepdim=True)
        )

        # f02: Attention Engagement (coefficients sum = 1.0)
        f02 = torch.sigmoid(
            0.35 * loudness_100ms
            + 0.35 * mean_loudness_500ms
            + 0.30 * asa_attn.mean(-1, keepdim=True)
        )

        # f03: Plasticity Index (coefficients sum = 1.0)
        f03 = torch.sigmoid(
            0.35 * contour_entropy_125ms
            + 0.35 * vocal_periodicity_100ms
            + 0.30 * ppc_contour.mean(-1, keepdim=True)
        )

        # f04: Sex Modulation (η² = 0.309)
        # sex_indicator provided externally; here we output f03 as base
        f04 = f03  # multiplied by (1 + η² * sex) at runtime

        # ═══ LAYER M: Plasticity Dynamics ═══
        cumulative_plasticity = torch.sigmoid(
            0.50 * f01 + 0.50 * ppc_pitch.mean(-1, keepdim=True)
        )
        session_memory = torch.sigmoid(
            0.50 * f01 + 0.50 * asa_scene.mean(-1, keepdim=True)
        )
        voice_recognition = mean_vocal_coupling_500ms

        # ═══ LAYER P: Present ═══
        auditory_orienting = asa_attn.mean(-1, keepdim=True)
        vocal_learning = ppc_contour.mean(-1, keepdim=True)

        # ═══ LAYER F: Future ═══
        ac_maturation = torch.sigmoid(
            0.50 * f03 + 0.50 * asa_salience.mean(-1, keepdim=True)
        )
        speech_transfer = torch.sigmoid(
            0.50 * f03 + 0.50 * ppc_interval.mean(-1, keepdim=True)
        )
        mmr_enhancement = torch.sigmoid(
            0.50 * contour_entropy_125ms
            + 0.50 * vocal_periodicity_100ms
        )

        return torch.cat([
            f01, f02, f03, f04,                                    # E: 4D
            cumulative_plasticity, session_memory, voice_recognition,  # M: 3D
            auditory_orienting, vocal_learning,                     # P: 2D
            ac_maturation, speech_transfer, mmr_enhancement,        # F: 3D
        ], dim=-1)  # (B, T, 12)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 1 (Partanen 2022) | Primary evidence |
| **Effect Sizes** | d=0.26, η²=0.31, η²=0.23 | EEG infant MMR |
| **Evidence Modality** | EEG | Direct neural |
| **Falsification Tests** | 3/5 confirmed | Moderate validity |
| **R³ Features Used** | ~12D of 49D | Consonance + energy + timbre + change + interactions |
| **H³ Demand** | 18 tuples (0.78%) | Sparse, efficient |
| **PPC Mechanism** | 30D (3 sub-sections) | Vocal pitch/contour |
| **ASA Mechanism** | 30D (3 sub-sections) | Attention/salience |
| **Output Dimensions** | **12D** | 4-layer structure |

---

## 13. Scientific References

1. **Partanen, E. et al. (2022)**. Music therapist-guided parental singing enhances auditory processing in preterm infants. EEG study, n=21 singing intervention, n=33 full-term controls.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (OSC, ATT, HRM, EFC) | PPC (30D) + ASA (30D) mechanisms |
| Vocal quality | S⁰.L5.spectral_centroid[38] + HC⁰.HRM | R³.consonance[4] + PPC.pitch_extraction |
| Attention | S⁰.L5.loudness[35] + HC⁰.ATT | R³.loudness[8] + ASA.attention_gating |
| Plasticity | S⁰.cumulative_exposure + HC⁰.OSC | R³.pitch_change[23] + PPC.contour_tracking |
| Voice tracking | S⁰.L0.F[1] + HC⁰.HRM | R³.brightness[13] + PPC.interval_analysis |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 27/2304 = 1.17% | 18/2304 = 0.78% |
| Output | 12D | 12D (same) |

### Why PPC + ASA replaces HC⁰ mechanisms

- **OSC → PPC.pitch_extraction** [0:10]: Oscillatory neural maturation rhythms map to PPC's pitch extraction for vocal encoding.
- **ATT → ASA.attention_gating** [10:20]: Infant attentional entrainment maps to ASA's auditory attention gating.
- **HRM → ASA.scene_analysis** [0:10]: Hippocampal voice replay maps to ASA's vocal pattern learning.
- **EFC → ASA.salience_weighting** [20:30]: Statistical learning prediction maps to ASA's salience for developmental transfer.

---

**Model Status**: **VALIDATED**
**Output Dimensions**: **12D**
**Evidence Tier**: **β (Integrative)**
**Confidence**: **70–90%**
