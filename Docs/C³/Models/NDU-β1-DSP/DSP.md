# NDU-β1-DSP: Developmental Singing Plasticity

**Model**: Developmental Singing Plasticity
**Unit**: NDU (Novelty Detection Unit)
**Circuit**: Salience + Developmental (Auditory Cortex, Attention Networks)
**Tier**: β (Integrative) — 70–90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added I:Information feature dependencies)
**Date**: 2026-02-13

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
| **Partanen 2022** | MEG | 21 | Singing intervention group > full-term in oddball paradigm | F(2,27)=4.019, p=0.030, η²=0.229 | **Primary**: f03 plasticity index, over-normalization |
| **Partanen 2022** | MEG | 21 | Sex × Singing time interaction in tata paradigm | η²=0.309, p=0.017 | **f04 sex modulation** |
| **Partanen 2022** | MEG | 21 | Group × Singing time interaction: quality > quantity | η²=0.262, p=0.030 | **Quality-dependent plasticity** |
| **Partanen 2022** | MEG | 21 | Males in singing group > females for vowel duration | p=0.001 | **Sex-dependent MMR enhancement** |
| **Scholkmann 2024** | fNIRS | 17 | CMT → StO₂ increase 3.2±2.0% in auditory cortex (subgroup 1) | r_rb=1.00, p=0.002 | **f01 singing quality → cerebrovascular** |
| **Scholkmann 2024** | fNIRS | 17 | StO₂ increase 2.4±1.1% in prefrontal cortex (subgroup 1) | r_rb=1.00, p=0.008 | **f02 attention engagement** |
| **Scholkmann 2024** | fNIRS | 17 | Two response subgroups: sex-dependent (females > positive response) | χ²=4.496, p=0.034, τ_b=−0.514 | **f04 sex modulation (cerebrovascular)** |
| **Scholkmann 2024** | fNIRS | 17 | Hematocrit correlates with StO₂ change magnitude | r_s=0.394, p=0.034 | **Individual difference factor** |
| **Edalati 2023** | EEG | 19 | Premature neonates (32±2.59 wGA) show selective beat+meter enhancement | Selective duple meter enhancement | **Rhythmic processing at prematurity** |
| **Edalati 2023** | EEG | 19 | Phase alignment of neural oscillations to auditory rhythm envelope | Phase-coupling at beat/meter frequencies | **PPC periodicity input relevance** |
| **Kaminska 2025** | EEG | 30 | Voice-evoked DBs: stimulus-specific topography (mid-temporal + pre-central) | Click DBs 83% vs voice 50%, p<0.01 | **Voice vs noise discrimination** |
| **Kaminska 2025** | EEG | 30 | Gamma oscillations increase with age; voice lateralization shifts L with age | Age-dependent lateralization | **AC maturation trajectory** |

### 3.2 Effect Size Summary

```
Primary Evidence (k=4 empirical + 3 reviews):
  Partanen 2022:    η²=0.229 (group), η²=0.309 (sex×singing), η²=0.262 (group×singing)
  Scholkmann 2024:  r_rb=1.00 (AC StO₂), r_rb=1.00 (PFC StO₂), τ_b=−0.514 (sex)
  Edalati 2023:     Selective duple meter enhancement in premature neonates
  Kaminska 2025:    Stimulus-specific DB topography, age-dependent gamma increase
Heterogeneity:      Moderate — MEG (Partanen) vs fNIRS (Scholkmann) vs EEG (Edalati, Kaminska)
                    Sex effect direction: males > females in MMR (Partanen) vs females > positive
                    cerebrovascular response (Scholkmann) — may reflect different processing levels
Quality Assessment: β-tier (multi-modal infant cohorts, converging evidence)
Replication:        Quality > quantity pattern confirmed across MEG and fNIRS
                    Sex differences replicated but with nuanced modality-dependent patterns
Reviews:            Nguyen 2023 (ID singing universality), Papatzikis 2024 (56 NICU studies),
                    Yu 2015 (MMN plasticity mechanisms)
```

---

## 4. R³ Input Mapping: What DSP Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

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

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | DSP Role | Scientific Basis |
|----------|-------|---------|----------|------------------|
| **I: Information** | [91] | information_rate | Information flow rate | Weineck 2022: information rate quantifies the temporal density of novel auditory content; modulates plasticity accumulation rate — richer information flow during singing sessions accelerates neural maturation |

**Rationale**: DSP models how parental singing drives developmental auditory plasticity in preterm infants. The v1 representation uses pitch_change [23] and spectral_change [21] as proxies for vocal variation richness. information_rate [91] provides a direct, information-theoretically grounded measure of how much novel auditory content the infant receives per unit time — the core driver of quality-dependent (not quantity-dependent) plasticity. This aligns with Partanen 2022's finding that singing quality predicts outcomes better than quantity.

**Code impact**: None yet — R³ v2 features are doc-only until Phase 5 integration. Current code reads r3[..., 0:49]; v2 features will extend the slice to r3[..., 0:128] when the EAR pipeline emits the expanded vector.

### 4.3 Physical → Cognitive Transformation

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

**v1 demand**: 18 tuples

#### R³ v2 Projected Expansion

Minor v2 expansion for DSP from I:Information.

| R³ Idx | Feature | Group | H | Morph | Law | Purpose |
|:------:|---------|:-----:|:-:|-------|:---:|---------|
| 90 | spectral_surprise | I | 3 | M0 (value) | L2 | Acoustic surprise at singing transitions |

**v2 projected**: 1 tuple
**Total projected**: 19 tuples of 294,912 theoretical = 0.0064%

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

| Region | MNI Coordinates | Mentions | Evidence Type | DSP Function | Source |
|--------|-----------------|----------|---------------|--------------|--------|
| **Auditory Cortex (bilateral)** | ±42, −22, 8 | 5 | Direct (MEG, fNIRS) | Preterm infant auditory processing, MMR generation | Partanen 2022 (MEG); Scholkmann 2024 (fNIRS left AC) |
| **Right Prefrontal Cortex** | ~46, 45, 0 | 2 | Direct (fNIRS) | CMT-induced StO₂ increase 2.4±1.1% | Scholkmann 2024 (fNIRS optode placement) |
| **Mid-Temporal (T7-T8)** | ±65, −25, 5 | 3 | Direct (EEG) | Voice-evoked delta brush topography | Kaminska 2025 (32-electrode EEG) |
| **Pre-Central Inferior (FC5-FC6)** | ±55, 0, 20 | 2 | Direct (EEG) | Voice-specific DB response (higher amplitude than click) | Kaminska 2025 |
| **Temporal Posterior (CP5-CP6)** | ±55, −40, 10 | 2 | Direct (EEG) | Click-evoked DB topography (higher amplitude than voice) | Kaminska 2025 |
| **Attention Networks** | N/A | 1 | Inferred | Infant auditory attention | Partanen 2022 (behavioral) |

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
| **Papers** | 7 (4 empirical + 3 reviews) | Partanen 2022, Scholkmann 2024, Edalati 2023, Kaminska 2025, Nguyen 2023, Papatzikis 2024, Yu 2015 |
| **Effect Sizes** | η²=0.229–0.309, r_rb=1.00, τ_b=−0.514 | MEG + fNIRS + EEG |
| **Evidence Modality** | Multi-modal (MEG, fNIRS, EEG) | Direct neural + cerebrovascular |
| **Largest Sample** | n=30 (Kaminska 2025) | EEG, 30–38 PMW |
| **Falsification Tests** | 3/5 confirmed | Moderate validity |
| **R³ Features Used** | ~12D of 49D | Consonance + energy + timbre + change + interactions |
| **H³ Demand** | 18 tuples (0.78%) | Sparse, efficient |
| **PPC Mechanism** | 30D (3 sub-sections) | Vocal pitch/contour |
| **ASA Mechanism** | 30D (3 sub-sections) | Attention/salience |
| **Output Dimensions** | **12D** | 4-layer structure |

---

## 13. Scientific References

1. **Partanen, E., Mårtensson, G., Hugoson, P., Huotilainen, M., Fellman, V., & Ådén, U. (2022)**. Auditory Processing of the Brain Is Enhanced by Parental Singing for Preterm Infants. *Frontiers in Neuroscience*, 16, 772008. doi:10.3389/fnins.2022.772008. MEG, n=21 preterm (13 singing, 8 control) + 12 full-term.
2. **Scholkmann, F., Haslbeck, F., Oba, E., Restin, T., Ostojic, D., Kleiser, S., ... & Karen, T. (2024)**. Creative music therapy in preterm infants effects cerebrovascular oxygenation and perfusion. *Scientific Reports*, 14, 28249. doi:10.1038/s41598-024-75282-8. fNIRS, n=17 usable preterm.
3. **Edalati, M., Wallois, F., Safaie, J., Ghostine, G., Kongolo, G., Trainor, L. J., & Moghimi, S. (2023)**. Rhythm in the Premature Neonate Brain: Very Early Processing of Auditory Beat and Meter. *Journal of Neuroscience*, 43(15), 2794–2802. doi:10.1523/JNEUROSCI.1100-22.2023. EEG, n=19 premature (32±2.59 wGA).
4. **Kaminska, A., Arzounian, D., Delattre, V., Laschet, J., Magny, J.-F., ... & Khazipov, R. (2025)**. Auditory evoked delta brushes involve stimulus-specific cortical networks in preterm infants. *iScience*, 28, 112313. doi:10.1016/j.isci.2025.112313. EEG, n=30, 30–38 PMW.
5. **Nguyen, T., Flaten, E., Trainor, L. J., & Novembre, G. (2023)**. Early social communication through music: State of the art and future perspectives. *Developmental Cognitive Neuroscience*, 63, 101279. doi:10.1016/j.dcn.2023.101279. Review.
6. **Papatzikis, E. et al. (2024)**. Passive music listening in neonatal intensive care units: A scoping review. *BMC Pediatrics*, 24, 829. Scoping review, 56 studies.
7. **Yu, X., Liu, T., & Gao, D. (2015)**. The Mismatch Negativity: An Indicator of Perception of Regularities in Music. *Behavioural Neurology*, 2015, 469508. Review of MMN plasticity.

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

---

## 15. Doc-Code Mismatches (Phase 5 Reference)

| Aspect | Doc (DSP.md) | Code (dsp_.py) | Severity |
|--------|-------------|----------------|----------|
| **FULL_NAME** | "Developmental Singing Plasticity" | "Deviance Salience Processing" | HIGH — identity mismatch |
| **OUTPUT_DIM** | 12D (4E+3M+2P+3F) | 10D (4E+2M+2P+2F) | HIGH — Layer M missing voice_recognition, Layer F missing speech_transfer |
| **MECHANISM_NAMES** | ("PPC", "ASA") | ("ASA",) | HIGH — PPC mechanism missing |
| **h3_demand** | 18 tuples specified | () empty tuple | HIGH — no temporal demand in code |
| **Layer M dims** | cumulative_plasticity, session_memory, voice_recognition (3D) | cumulative_exposure, voice_familiarity (2D) | MEDIUM — name + count mismatch |
| **Layer F dims** | ac_maturation, speech_transfer, mmr_enhancement (3D) | auditory_development_pred, mmr_enhancement_pred (2D) | MEDIUM — name + count mismatch |
| **Brain regions** | 6 regions (with MNI from Partanen, Scholkmann, Kaminska) | 3 regions (STG, IFG, ACC with generic MNI) | MEDIUM |
| **Citations** | Partanen 2022 + 6 others | Virtala 2023, McMahon 2012 | MEDIUM — wrong primary citation |
| **Version** | 2.1.0 | 2.0.0 | LOW |

---

**Model Status**: **VALIDATED**
**Output Dimensions**: **12D**
**Evidence Tier**: **β (Integrative)**
**Confidence**: **70–90%**
