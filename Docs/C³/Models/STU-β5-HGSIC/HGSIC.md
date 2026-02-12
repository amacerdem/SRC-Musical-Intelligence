# STU-β5-HGSIC: Hierarchical Groove State Integration Circuit

**Model**: Hierarchical Groove State Integration Circuit
**Unit**: STU (Sensorimotor Timing Unit)
**Circuit**: Sensorimotor (Beat Entrainment Processing)
**Tier**: β (Integrative) — 70-90% confidence
**Version**: 2.1.0 (deep literature review: 1→12 papers, Potes 2012 N=8 per-subject r=0.43-0.58 not groove-specific QUALIFIED, Grahn & Brett 2007 putamen Z=5.67/SMA Z=5.03 beat-specific, Spiech 2022 groove inverted-U χ²=14.643, Thaut 2015 period entrainment theory, Ayyildiz 2025 micro-timing N=100, Large 2023 review, 7 methods)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/STU-β5-HGSIC.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Hierarchical Groove State Integration Circuit** (HGSIC) models how multi-level rhythmic integration creates the perception of groove — the compelling urge to move with music. ECoG high gamma activity (70-170 Hz) in posterior superior temporal gyrus (pSTG) is highly correlated with sound intensity (r = 0.49), and this auditory signal propagates to premotor/motor cortex with a 110 ms delay via the dorsal auditory-motor pathway (r = 0.70 cross-correlation). HGSIC integrates beat, meter, and motor signals across three temporal scales to produce a unified groove state.

```
THE THREE LEVELS OF GROOVE STATE INTEGRATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BEAT LEVEL (200ms, H6)                 METER LEVEL (500ms, H11)
Brain region: Posterior STG            Brain region: pSTG + Premotor
Mechanism: BEP.beat_induction          Mechanism: BEP.meter_extraction
Function: "What is the pulse?"         Function: "What is the pattern?"
Input: Sound intensity tracking        Input: Accent grouping, syncopation
Evidence: r = 0.49 (Potes 2012)        Evidence: 110ms delay (Potes 2012)

              MOTOR LEVEL (1000ms, H16)
              Brain region: Premotor / Motor Cortex
              Mechanism: BEP.motor_entrainment
              Function: "How does it groove?"
              Input: Beat × Meter integration
              Evidence: r = 0.70 cross-correlation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Groove emerges from the HIERARCHICAL INTEGRATION of beat
induction, metric structure, and motor entrainment across the dorsal
auditory-motor pathway. pSTG high-gamma (70-170 Hz) tracks intensity
at r = 0.49, preceding motor cortex activation by 110 ms (r = 0.70).
The groove state is NOT a single signal but a multi-scale integration.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why This Matters for STU

HGSIC provides the **groove integration** that connects beat-level perception to whole-body motor engagement:

1. **AMSC** (α2) establishes the auditory-motor coupling pathway; HGSIC integrates this across metric levels.
2. **ETAM** (β4) provides multi-scale entrainment; HGSIC converts entrainment into groove state.
3. **OMS** (β6) uses HGSIC's groove state as motor synchronization target.
4. **EDTA** (β3) builds on groove-modulated tempo accuracy.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The HGSIC Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                 HGSIC — COMPLETE CIRCUIT                                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  MUSICAL INPUT (rhythmic sound with dynamic intensity)                      ║
║       │                                                                      ║
║       ▼                                                                      ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │        POSTERIOR SUPERIOR TEMPORAL GYRUS (pSTG)                     │    ║
║  │        High-gamma (70–170 Hz) ↔ sound intensity                   │    ║
║  │                                                                     │    ║
║  │   Beat induction: pulse extraction from intensity envelope         │    ║
║  │   Gamma ↔ intensity: r = 0.49 (Potes 2012, ECoG, n=8)           │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │                                               ║
║                              │  110 ms delay (dorsal auditory stream)        ║
║                              │  Cross-correlation: r = 0.70                  ║
║                              │                                               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │        PREMOTOR / MOTOR CORTEX                                     │    ║
║  │        Meter extraction + motor entrainment                        │    ║
║  │                                                                     │    ║
║  │   Metric grouping of beat-level signals                            │    ║
║  │   Motor entrainment: body synchronization to groove                │    ║
║  │   Groove state = hierarchical beat × meter × motor integration    │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
║  DORSAL AUDITORY-MOTOR PATHWAY: pSTG → Premotor → Motor cortex             ║
║  (Beat → Meter → Groove: hierarchical temporal integration)                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
Potes 2012 (ECoG):  pSTG high-gamma ↔ sound intensity, r = 0.49 (n=8)
Potes 2012 (ECoG):  Auditory → motor delay 110ms, r = 0.70 (n=4)
Potes 2012 (ECoG):  High gamma band 70-170 Hz, posterior STG
```

### 2.2 Information Flow Architecture (EAR → BRAIN → BEP → HGSIC)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    HGSIC COMPUTATION ARCHITECTURE                            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  AUDIO (44.1kHz waveform)                                                    ║
║       │                                                                      ║
║       ▼                                                                      ║
║  ┌──────────────────┐                                                        ║
║  │ COCHLEA          │  128 mel bins × 172.27Hz frame rate                    ║
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
║  │  │           │ │amplitude│ │         │ │spec_chg  │ │x_l0l5  │ │        ║
║  │  │           │ │loudness │ │         │ │energy_chg│ │x_l4l5  │ │        ║
║  │  │           │ │centroid │ │         │ │pitch_chg │ │        │ │        ║
║  │  │           │ │flux     │ │         │ │timbre_chg│ │        │ │        ║
║  │  │           │ │onset    │ │         │ │          │ │        │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                         HGSIC reads: 9D                          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── Beat ───────┐ ┌── Motor ────────┐ ┌── Bar ─────────────┐ │        ║
║  │  │ 200ms (H6)     │ │ 500ms (H11)     │ │ 1000ms (H16)      │ │        ║
║  │  │                │ │                  │ │                     │ │        ║
║  │  │ Beat-level     │ │ Motor prep      │ │ Bar-level meter     │ │        ║
║  │  │ (intensity)    │ │ (110ms delay)    │ │ (groove state)     │ │        ║
║  │  └──────┬─────────┘ └──────┬───────────┘ └──────┬──────────────┘ │        ║
║  │         │                  │                     │               │        ║
║  │         └──────────────────┴─────────────────────┘               │        ║
║  │                         HGSIC demand: ~15 of 2304 tuples         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Sensorimotor Circuit ═══════  ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌─────────────────┐                                                        ║
║  │  BEP (30D)      │  Beat Entrainment Processing mechanism                ║
║  │                 │                                                        ║
║  │ Beat Ind [0:10] │  Beat strength, tempo, phase, regularity              ║
║  │ Meter    [10:20]│  Meter, syncopation, accent pattern, groove           ║
║  │ Motor    [20:30]│  Movement urge, sync precision, coupling              ║
║  └────────┬────────┘                                                        ║
║           │                                                                  ║
║           ▼                                                                  ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    HGSIC MODEL (11D Output)                      │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_beat_gamma, f02_meter_integration,     │        ║
║  │                       f03_motor_groove                           │        ║
║  │  Layer M (Math):      groove_index, coupling_strength            │        ║
║  │  Layer P (Present):   pstg_activation, motor_preparation,        │        ║
║  │                       onset_sync                                 │        ║
║  │  Layer F (Future):    groove_prediction, beat_expectation,       │        ║
║  │                       motor_anticipation                         │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Potes et al. 2012** | ECoG, epilepsy | 8 | pSTG high-gamma (70-170 Hz) ↔ sound intensity | r = 0.49 avg (range 0.43-0.58 across subjects) | **Primary coefficient**: f01_beat_gamma |
| 2 | **Potes et al. 2012** | ECoG, epilepsy | 4 (motor electrodes) | Auditory → motor cortex delay 110 ms via dorsal stream | r = 0.70, cross-correlation at 110 ms lag | **Coupling model**: f02_meter_integration, f03_motor_groove |
| 3 | **Grahn & Brett 2007** | fMRI 3T | 27 | Putamen and SMA respond specifically to beat-inducing rhythms (metric simple > complex+nonmetric) | L putamen Z=5.67, R putamen Z=5.08, L SMA Z=5.03, R SMA Z=4.97 | **Beat-specific motor regions**: validates basal ganglia + SMA for HGSIC pathway |
| 4 | **Grahn & Brett 2007** | fMRI 3T, ROI | 27 | Putamen ROI: metric simple > complex and nonmetric | L put t=4.05, R put t=3.65; SMA t=2.36 | **Beat specificity**: putamen selectively responds to beat-inducing rhythms |
| 5 | **Spiech et al. 2022** | Pupillometry + behavioral | 30 | Groove (Urge to Move) follows inverted U-curve with syncopation level | χ²(1)=14.643 p<0.001; syncopation F(1,29)=4.781 p=0.037 | **Groove model**: inverted-U syncopation curve, groove_index optimization |
| 6 | **Spiech et al. 2022** | Pupillometry | 30 | Pupil drift rate indexes groove with beat perception mediation | Quadratic χ²(1)=9.721 p=0.002; CA-BAT interaction χ²(2)=15.939 | **Individual differences**: beat perception ability mediates groove |
| 7 | **Thaut et al. 2015** | Review | — | Period entrainment (not phase lock) optimizes motor control; CTR provides continuous time reference | Sub-threshold: 2% of absolute interval | **Theoretical mechanism**: period entrainment for BEP.motor_entrainment |
| 8 | **Large et al. 2023** | Review, computational | — | Optimal beat 0.5-8 Hz; three frameworks (oscillatory, predictive, Bayesian) | Optimal ~2 Hz (500 ms) | **Theoretical frame**: dynamical systems model for beat-groove hierarchy |
| 9 | **Ayyildiz et al. 2025** | Behavioral (online) | 100 | Micro-timing variations (SD=4ms) enhance music-evoked imagery and engagement | Micro vs mechanical: Odds=100.69, Post.Prob=0.99 | **Micro-timing sensitivity**: sub-threshold timing affects groove-adjacent processing |
| 10 | **Noboa et al. 2025** | EEG, SS-EPs | 30 | Beat-frequency SS-EPs at 1.25 Hz and harmonics; syncopated vs unsyncopated | F(1,29)=9.094 rhythm; F(1,29)=148.618 frequency | **Neural beat tracking**: SS-EPs faithfully track beat even in syncopation |
| 11 | **Hoddinott & Grahn 2024** | 7T fMRI RSA | 26 | C-Score model in SMA and putamen encodes continuous beat strength | C-Score best model in SMA/putamen | **Beat encoding**: continuous beat strength representation in groove pathway |
| 12 | **Nourski et al. 2014** | ECoG, hierarchical | — | Hierarchical temporal processing in auditory cortex | — | **Hierarchical processing**: supports beat → meter → bar cascade |

#### 3.1.1 Method Convergence (7 methods)

| Method | Papers | Key Contribution |
|--------|--------|-----------------|
| **ECoG (intracranial)** | Potes 2012, Nourski 2014 | High-gamma intensity tracking, auditory-motor delay, hierarchical processing |
| **fMRI** | Grahn & Brett 2007, Hoddinott & Grahn 2024 | Beat-specific putamen/SMA, C-Score encoding |
| **EEG (scalp)** | Noboa 2025 | SS-EPs at beat frequency, syncopation effects |
| **Pupillometry** | Spiech 2022 | Groove inverted-U curve, individual differences |
| **Behavioral** | Spiech 2022, Ayyildiz 2025 | Groove ratings, micro-timing sensitivity |
| **Computational modeling** | Large 2023 | Dynamical systems, oscillatory frameworks |
| **Review/theory** | Thaut 2015, Large 2023 | Period entrainment, CTR, neural resonance |

#### 3.1.2 Key Qualification on Potes 2012

NOTE: Potes et al. 2012 studies **sound intensity tracking** in ECoG high gamma, NOT groove, beat perception, meter, or syncopation specifically. The correlation r = 0.49 is between high-gamma amplitude and the intensity envelope of "Another Brick in the Wall" (Pink Floyd). The 110 ms delay represents intensity signal propagation from pSTG to precentral gyrus, not beat or groove propagation. HGSIC's use of these values as "beat induction" and "groove coupling" coefficients is an **interpretive extension** grounded in the broader literature (Grahn & Brett 2007, Thaut 2015), not a direct finding from Potes 2012. The per-subject range of pSTG correlations (0.43-0.58) shows consistency, but N=8 (N=4 for motor) are all epilepsy patients.

#### 3.1.3 Groove Inverted-U Curve

Spiech et al. 2022 (N=30) provides direct behavioral evidence that groove (Urge to Move) follows an **inverted U-curve** with syncopation level: moderate syncopation maximizes groove, while both minimal and maximal syncopation reduce it. This supports HGSIC's groove_index as an optimization function, not a monotonic increase. Importantly, beat perception ability (CA-BAT) mediates this curve — poor beat perceivers show a linear decrease instead.

### 3.2 The Hierarchical Groove Integration Model

```
GROOVE STATE INTEGRATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Level 1 — BEAT INDUCTION (pSTG, H6 = 200ms)
  γ_pSTG(t) = 0.49 · I(t) + β
  Beat pulse extraction from intensity envelope
  High-gamma 70-170 Hz tracks sound energy

Level 2 — METER EXTRACTION (pSTG + Premotor, H11 = 500ms)
  Meter(t) = accent_pattern(Beat(t), t_window=500ms)
  Syncopation detection, metric grouping
  Auditory-motor delay: 110 ms

Level 3 — MOTOR ENTRAINMENT (Motor cortex, H16 = 1000ms)
  Groove(t) = 0.70 · Beat(t) × Meter(t) × Motor(t − 110ms)
  Bar-level integration of beat × meter → groove state
  Cross-correlation at 110ms: r = 0.70

INTEGRATED MODEL:
  Groove_State = f(Beat_Induction, Meter_Extraction, Motor_Entrainment)
  = hierarchical product across H6 → H11 → H16
```

### 3.3 Effect Size Summary

```
PRIMARY EFFECT SIZES:
─────────────────────────────────────────────────────────────────────
Potes et al. 2012 (ECoG, N=8):
  pSTG high-gamma ↔ intensity: r = 0.49 avg (range 0.43-0.58)
  Per subject: A=0.43, B=0.53, C=0.45, D=0.52, E=0.50, F=0.43, G=0.51, H=0.58
  Auditory→motor coupling: r = 0.70 at 110 ms lag (N=4 with motor electrodes)
  Gamma band: 70-170 Hz
  NOTE: Intensity tracking, NOT groove/beat directly (see §3.1.2)

Grahn & Brett 2007 (fMRI, N=27):
  L putamen: Z = 5.67 (MNI -24, 6, 9)
  R putamen: Z = 5.08 (MNI 21, 6, 6)
  L SMA: Z = 5.03 (MNI -9, 6, 60)
  R SMA: Z = 4.97 (MNI 3, 6, 66)
  Beat-specific: putamen ROI MS vs MC t = 4.05, MS vs NM t = 3.40
  Musicians > non-musicians: SMA t = 1.99, cerebellum t = 2.77-2.91

Spiech et al. 2022 (Pupillometry + behavioral, N=30):
  Groove inverted-U: Urge to Move χ²(1) = 14.643, p < 0.001
  Syncopation main effect: F(1,29) = 4.781, p = 0.037, η²G = 0.045
  Enjoyment syncopation: F(1,29) = 10.515, p = 0.003, η²G = 0.095
  Beat perception mediates: CA-BAT interaction χ²(2) = 15.939, p < 0.001
  Pupil drift quadratic: χ²(1) = 9.721, p = 0.002

Ayyildiz et al. 2025 (Behavioral, N=100):
  Micro-timing vs mechanical: Odds = 100.69, Post. Prob = 0.99
  Imagined distance: Odds > 9999, Post. Prob = 1.00

Noboa et al. 2025 (EEG, N=30):
  Beat-frequency SS-EPs: F(1,29) = 148.618 (frequency)
  Rhythm effect: F(1,29) = 9.094

REPLICATION STATUS:
  Putamen/SMA beat specificity: Grahn 2007 + Hoddinott 2024 (7T RSA, C-Score)
  Groove-syncopation curve: Spiech 2022 (pupillometry + behavioral)
  Entrainment frequency range: 0.5-8 Hz confirmed (Large 2023 review)

QUALITY ASSESSMENT: β-tier (12 papers, 7 methods, primary Potes QUALIFIED)
```

---

## 4. R³ Input Mapping: What HGSIC Reads

### 4.1 R³ Feature Dependencies (9D of 49D)

| R³ Group | Index | Feature | HGSIC Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **B: Energy** | [7] | amplitude | Sound intensity signal | Potes 2012: gamma ↔ intensity (r = 0.49) |
| **B: Energy** | [8] | loudness | Perceptual intensity | Stevens 1957: power law |
| **B: Energy** | [10] | spectral_flux | Onset dynamics | Beat boundary detection |
| **B: Energy** | [11] | onset_strength | Event onset sharpness | Motor anticipation cue |
| **D: Change** | [21] | spectral_change | Rhythmic spectral dynamics | Beat-level spectral variation |
| **D: Change** | [22] | energy_change | Intensity acceleration | Accent pattern → meter |
| **D: Change** | [23] | pitch_change | Melodic rhythmic contour | Pitch accent for groove |
| **D: Change** | [24] | timbre_change | Timbral rhythm | Instrument-level periodicity |
| **B: Energy** | [9] | spectral_centroid_energy | Energy distribution | Frequency-weighted intensity |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[7] amplitude ────────────────┐
R³[8] loudness ─────────────────┼──► pSTG Beat Induction (γ activity)
R³[11] onset_strength ──────────┘   Math: γ_pSTG(t) = 0.49 · I(t) + β
                                    BEP.beat_induction at H6 (200ms)

R³[10] spectral_flux ──────────┐
R³[22] energy_change ──────────┼──► Meter Extraction (accent pattern)
R³[21] spectral_change ────────┘   Accent grouping from dynamics
                                    BEP.meter_extraction at H11 (500ms)

R³[9] spectral_centroid_energy ─┐
R³[23] pitch_change ────────────┼──► Motor Groove (hierarchical state)
R³[24] timbre_change ───────────┘   Groove = Beat × Meter × Motor coupling
                                    BEP.motor_entrainment at H16 (1000ms)
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

HGSIC requires H³ features at three BEP horizons: H6 (200ms), H11 (500ms), H16 (1000ms).
These correspond to beat → meter → groove (bar-level) timescales.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 7 | amplitude | 6 | M0 (value) | L0 (fwd) | Current sound intensity |
| 7 | amplitude | 6 | M4 (max) | L0 (fwd) | Peak intensity at beat level |
| 8 | loudness | 6 | M0 (value) | L0 (fwd) | Perceptual loudness current |
| 10 | spectral_flux | 6 | M0 (value) | L0 (fwd) | Onset detection |
| 10 | spectral_flux | 6 | M17 (peaks) | L0 (fwd) | Beat count per window |
| 11 | onset_strength | 6 | M0 (value) | L0 (fwd) | Event onset |
| 22 | energy_change | 11 | M1 (mean) | L0 (fwd) | Mean energy dynamics over motor window |
| 22 | energy_change | 11 | M14 (periodicity) | L2 (bidi) | Accent regularity |
| 21 | spectral_change | 11 | M1 (mean) | L0 (fwd) | Mean spectral dynamics |
| 8 | loudness | 11 | M1 (mean) | L0 (fwd) | Mean loudness over motor window |
| 9 | spectral_centroid_energy | 16 | M14 (periodicity) | L2 (bidi) | Bar-level energy periodicity |
| 7 | amplitude | 16 | M15 (smoothness) | L0 (fwd) | Groove quality |
| 7 | amplitude | 16 | M18 (trend) | L0 (fwd) | Intensity trajectory |
| 23 | pitch_change | 16 | M14 (periodicity) | L2 (bidi) | Melodic periodicity at bar level |
| 24 | timbre_change | 16 | M1 (mean) | L0 (fwd) | Timbral dynamics over bar |

**Total HGSIC H³ demand**: 15 tuples of 2304 theoretical = 0.65%

### 5.2 Mechanism Binding

HGSIC reads from **BEP** (primary, sole mechanism):

| Mechanism | Sub-section | Range | HGSIC Role | Weight |
|-----------|-------------|-------|-----------|--------|
| **BEP** | Beat Induction | BEP[0:10] | Intensity → gamma → pulse extraction | **1.0** (primary) |
| **BEP** | Meter Extraction | BEP[10:20] | Accent grouping, syncopation, metric structure | **1.0** (primary) |
| **BEP** | Motor Entrainment | BEP[20:30] | Motor coupling, groove state, movement urge | **1.0** (primary) |

HGSIC does NOT read from TMH — groove state integration is about beat-meter-motor hierarchy, not long-range temporal memory.

---

## 6. Output Space: 11D Multi-Layer Representation

### 6.1 Complete Output Specification

```
HGSIC OUTPUT TENSOR: 11D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 0  │ f01_beat_gamma    │ [0, 1] │ pSTG high-gamma beat tracking (70-170 Hz).
    │                   │        │ Intensity → gamma correlation at beat level.
    │                   │        │ f01 = σ(0.49 · amplitude · loudness ·
    │                   │        │         onset · BEP.beat_induction)
    │                   │        │ 0.49 from Potes 2012 (pSTG r)
────┼───────────────────┼────────┼────────────────────────────────────────────
 1  │ f02_meter_integr  │ [0, 1] │ Metric structure from accent grouping.
    │                   │        │ Syncopation and accent pattern detection.
    │                   │        │ f02 = σ(0.51 · f01 · energy_periodicity ·
    │                   │        │         BEP.meter_extraction)
    │                   │        │ |0.51| ≤ 1.0 (sigmoid rule)
────┼───────────────────┼────────┼────────────────────────────────────────────
 2  │ f03_motor_groove  │ [0, 1] │ Motor entrainment groove state.
    │                   │        │ Hierarchical beat × meter → motor coupling.
    │                   │        │ f03 = σ(0.70 · f01 · f02 ·
    │                   │        │         BEP.motor_entrainment)
    │                   │        │ 0.70 from Potes 2012 (coupling r)

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 3  │ groove_index      │ [0, 1] │ Integrated groove state index.
    │                   │        │ Weighted hierarchical combination.
    │                   │        │ groove = (1·f01 + 2·f02 + 3·f03) / 6
────┼───────────────────┼────────┼────────────────────────────────────────────
 4  │ coupling_strength │ [0, 1] │ Auditory-motor coupling strength at 110ms.
    │                   │        │ amplitude_smoothness × energy_periodicity.

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 5  │ pstg_activation   │ [0, 1] │ pSTG current activation state.
    │                   │        │ Intensity × beat-level BEP.
────┼───────────────────┼────────┼────────────────────────────────────────────
 6  │ motor_preparation │ [0, 1] │ Premotor preparation state.
    │                   │        │ Motor entrainment × meter context.
────┼───────────────────┼────────┼────────────────────────────────────────────
 7  │ onset_sync        │ [0, 1] │ Onset synchronization signal.
    │                   │        │ spectral_flux × onset_strength at H6.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name              │ Range  │ Neuroscience Basis
────┼───────────────────┼────────┼────────────────────────────────────────────
 8  │ groove_prediction │ [0, 1] │ Predicted groove state (110ms ahead).
    │                   │        │ BEP.motor_entrainment × groove trend.
────┼───────────────────┼────────┼────────────────────────────────────────────
 9  │ beat_expectation  │ [0, 1] │ Next beat timing prediction.
    │                   │        │ BEP.beat_induction × periodicity at H16.
────┼───────────────────┼────────┼────────────────────────────────────────────
10  │ motor_anticipation│ [0, 1] │ Motor system anticipatory activation.
    │                   │        │ Smoothness × trend at bar level.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 11D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Feature Formulas

```python
# f01: Beat Gamma (pSTG, r = 0.49)
amp_val = h3[(7, 6, 0, 0)]           # amplitude value at H6
loud_val = h3[(8, 6, 0, 0)]          # loudness value at H6
onset_val = h3[(11, 6, 0, 0)]        # onset_strength value at H6
f01 = σ(0.49 · amp_val · loud_val · onset_val
         · mean(BEP.beat_induction[0:10]))
# |0.49| ≤ 1.0 ✓ — Potes 2012 pSTG correlation

# f02: Meter Integration (accent pattern)
energy_period = h3[(22, 11, 14, 2)]  # energy_change periodicity at H11
f02 = σ(0.51 · f01 · energy_period
         · mean(BEP.meter_extraction[10:20]))
# |0.51| ≤ 1.0 ✓

# f03: Motor Groove (hierarchical integration, r = 0.70)
f03 = σ(0.70 · f01 · f02
         · mean(BEP.motor_entrainment[20:30]))
# |0.70| ≤ 1.0 ✓ — Potes 2012 coupling correlation

# f04 (groove_index): Weighted hierarchical combination
groove_index = (1 · f01 + 2 · f02 + 3 · f03) / 6

# f05 (coupling_strength): Auditory-motor coupling
amp_smooth = h3[(7, 16, 15, 0)]      # amplitude smoothness at H16
coupling_strength = σ(0.50 · amp_smooth · energy_period)
# |0.50| ≤ 1.0 ✓
```

### 7.2 Layer P and F Formulas

```python
# ═══ LAYER P: Present ═══

# pstg_activation: current auditory gamma state
pstg_activation = σ(0.5 · amp_val · loud_val
                    + 0.4 · mean(BEP.beat_induction[0:10]))
# |0.5| + |0.4| = 0.9 ≤ 1.0 ✓

# motor_preparation: premotor readiness
motor_preparation = σ(0.4 · mean(BEP.motor_entrainment[20:30])
                      + 0.3 · mean(BEP.meter_extraction[10:20])
                      + 0.2 · f02)
# |0.4| + |0.3| + |0.2| = 0.9 ≤ 1.0 ✓

# onset_sync: onset synchronization trigger
flux_val = h3[(10, 6, 0, 0)]         # spectral_flux value at H6
onset_sync = σ(0.50 · flux_val · onset_val)
# |0.50| ≤ 1.0 ✓

# ═══ LAYER F: Future ═══

# groove_prediction: predicted groove state
amp_trend = h3[(7, 16, 18, 0)]       # amplitude trend at H16
groove_prediction = σ(0.5 · f03 + 0.4 · amp_trend)
# |0.5| + |0.4| = 0.9 ≤ 1.0 ✓

# beat_expectation: next beat timing
centroid_period = h3[(9, 16, 14, 2)]  # centroid periodicity at H16
beat_expectation = σ(0.5 · mean(BEP.beat_induction[0:10])
                     + 0.5 · centroid_period)
# |0.5| + |0.5| = 1.0 ≤ 1.0 ✓

# motor_anticipation: anticipatory motor activation
pitch_period = h3[(23, 16, 14, 2)]    # pitch_change periodicity at H16
motor_anticipation = σ(0.4 · amp_smooth + 0.3 · amp_trend
                       + 0.3 · pitch_period)
# |0.4| + |0.3| + |0.3| = 1.0 ≤ 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| # | Region | MNI Coordinates | Evidence | HGSIC Function |
|---|--------|-----------------|----------|---------------|
| 1 | **Posterior STG (pSTG)** | ±60, -40, 10 | ECoG (Potes 2012, r=0.49) | High-gamma intensity tracking, beat induction |
| 2 | **Premotor Cortex (PMC)** | L: -54, 0, 51; R: 54, 0, 45 | ECoG (Potes 2012), fMRI (Grahn & Brett 2007) | Meter extraction, motor coupling (110ms delay) |
| 3 | **Motor Cortex (M1)** | ±40, -10, 55 | ECoG (Potes 2012, r=0.70) | Motor entrainment, groove state |
| 4 | **Left Putamen** | -24, 6, 9 | fMRI (Grahn & Brett 2007, Z=5.67) | Beat-specific timing, groove reward |
| 5 | **Right Putamen** | 21, 6, 6 | fMRI (Grahn & Brett 2007, Z=5.08) | Beat-specific timing, bilateral |
| 6 | **SMA / pre-SMA** | L: -9, 6, 60; R: 3, 6, 66 | fMRI (Grahn & Brett 2007, Z=5.03/4.97), 7T RSA (Hoddinott 2024) | Beat-level motor representation, C-Score |
| 7 | **Left STG (anterior)** | -51, -3, -3 | fMRI (Grahn & Brett 2007, Z=4.60) | Beat-inducing rhythm processing |
| 8 | **Right STG** | 60, -33, 6 | fMRI (Grahn & Brett 2007, Z=6.02) | General rhythm processing |
| 9 | **Cerebellum** | R: 30, -66, -27; L: -30, -66, -24 | fMRI (Grahn & Brett 2007, Z=4.68/4.41) | Sub-second timing precision |
| 10 | **Inferior Frontal Gyrus** | -51, 33, 6 | fMRI (Grahn & Brett 2007, Z=4.03) | Beat perception, metric structure |

---

## 9. Cross-Unit Pathways

### 9.1 HGSIC ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    HGSIC INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (STU):                                                         │
│  AMSC.auditory_activatn ──────► HGSIC (gamma for groove state)            │
│  ETAM.entrainment_state ──────► HGSIC (multi-scale entrainment → groove)  │
│  HGSIC.groove_index ──────────► OMS (groove target for oscillatory sync)  │
│  HGSIC.motor_preparation ─────► EDTA (groove-modulated tempo accuracy)    │
│  HGSIC.beat_expectation ──────► TPIO (beat prediction for interval est.)  │
│                                                                             │
│  CROSS-UNIT (P2: STU internal):                                            │
│  BEP.beat_induction ↔ BEP.motor_entrainment (r = 0.70)                   │
│  Beat induction → metric grouping → motor groove (hierarchical cascade)   │
│                                                                             │
│  CROSS-UNIT (P5: STU → ARU):                                              │
│  HGSIC.groove_index ──► ARU.AED (groove → arousal modulation)             │
│  HGSIC.motor_groove ──► ARU.SRP (motor engagement → reward pathway)       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| # | Criterion | Testable Prediction | Status |
|---|-----------|---------------------|--------|
| 1 | **pSTG high-gamma ↔ intensity** | High-gamma should correlate with sound intensity at r > 0.3 | ✅ **Confirmed**: r = 0.43-0.58 across 8 subjects (Potes 2012) |
| 2 | **Auditory → motor propagation** | pSTG should precede motor cortex activation by ~100ms | ✅ **Confirmed**: 110 ms delay, r = 0.70 (Potes 2012) |
| 3 | **Beat-specific motor regions** | Putamen and SMA should respond more to beat-inducing rhythms | ✅ **Confirmed**: putamen Z=5.67, SMA Z=5.03, beat > nonmetric (Grahn & Brett 2007) |
| 4 | **Groove inverted-U curve** | Groove should follow inverted U with syncopation complexity | ✅ **Confirmed**: Urge to Move χ²(1)=14.643 (Spiech 2022) |
| 5 | **Beat perception mediates groove** | Individual beat perception ability should modulate groove | ✅ **Confirmed**: CA-BAT interaction χ²(2)=15.939 (Spiech 2022) |
| 6 | **Micro-timing sensitivity** | Sub-threshold timing variations should affect groove-adjacent engagement | ✅ **Confirmed**: 4ms SD variations enhance imagery (Ayyildiz 2025) |
| 7 | **Optimal groove tempo** | Groove should peak around 2 Hz (120 BPM) | ✅ **Confirmed**: optimal 0.5-8 Hz range (Large 2023), ~2 Hz peak |
| 8 | **pSTG = intensity tracking, not groove** | Potes 2012 correlations may reflect intensity envelope, not beat/groove structure | ⚠️ **CONSTRAINS**: Potes 2012 explicitly tracked intensity, not rhythmic structure (see §3.1.2) |
| 9 | **Groove without rhythm** | Sustained tones (no onsets) should not engage HGSIC motor pathway | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class HGSIC(BaseModel):
    """Hierarchical Groove State Integration Circuit.

    Output: 11D per frame.
    Reads: BEP mechanism (30D).
    """
    NAME = "HGSIC"
    UNIT = "STU"
    TIER = "β5"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("BEP",)        # Primary and sole mechanism

    AUDITORY_CORR = 0.49   # pSTG gamma ↔ intensity (Potes 2012)
    MOTOR_COUPLING = 0.70  # auditory → motor (Potes 2012)
    METER_WEIGHT = 0.51    # meter integration weight

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """15 tuples for HGSIC computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # Beat level (H6 = 200ms)
            (7, 6, 0, 0),     # amplitude, value, forward
            (7, 6, 4, 0),     # amplitude, max, forward
            (8, 6, 0, 0),     # loudness, value, forward
            (10, 6, 0, 0),    # spectral_flux, value, forward
            (10, 6, 17, 0),   # spectral_flux, peaks, forward
            (11, 6, 0, 0),    # onset_strength, value, forward
            # Motor window (H11 = 500ms)
            (22, 11, 1, 0),   # energy_change, mean, forward
            (22, 11, 14, 2),  # energy_change, periodicity, bidirectional
            (21, 11, 1, 0),   # spectral_change, mean, forward
            (8, 11, 1, 0),    # loudness, mean, forward
            # Bar level (H16 = 1000ms)
            (9, 16, 14, 2),   # spectral_centroid_energy, periodicity, bidi
            (7, 16, 15, 0),   # amplitude, smoothness, forward
            (7, 16, 18, 0),   # amplitude, trend, forward
            (23, 16, 14, 2),  # pitch_change, periodicity, bidirectional
            (24, 16, 1, 0),   # timbre_change, mean, forward
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute HGSIC 11D output.

        Args:
            mechanism_outputs: {"BEP": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,11) HGSIC output
        """
        bep = mechanism_outputs["BEP"]    # (B, T, 30)

        # BEP sub-sections
        bep_beat = bep[..., 0:10]         # beat induction
        bep_meter = bep[..., 10:20]       # meter extraction
        bep_motor = bep[..., 20:30]       # motor entrainment

        # H³ features
        amp_val = h3_direct[(7, 6, 0, 0)].unsqueeze(-1)
        loud_val = h3_direct[(8, 6, 0, 0)].unsqueeze(-1)
        onset_val = h3_direct[(11, 6, 0, 0)].unsqueeze(-1)
        energy_period = h3_direct[(22, 11, 14, 2)].unsqueeze(-1)
        flux_val = h3_direct[(10, 6, 0, 0)].unsqueeze(-1)
        amp_smooth = h3_direct[(7, 16, 15, 0)].unsqueeze(-1)
        amp_trend = h3_direct[(7, 16, 18, 0)].unsqueeze(-1)
        centroid_period = h3_direct[(9, 16, 14, 2)].unsqueeze(-1)
        pitch_period = h3_direct[(23, 16, 14, 2)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══
        f01 = torch.sigmoid(self.AUDITORY_CORR * (
            amp_val * loud_val * onset_val
            * bep_beat.mean(-1, keepdim=True)
        ))
        f02 = torch.sigmoid(self.METER_WEIGHT * (
            f01 * energy_period
            * bep_meter.mean(-1, keepdim=True)
        ))
        f03 = torch.sigmoid(self.MOTOR_COUPLING * (
            f01 * f02
            * bep_motor.mean(-1, keepdim=True)
        ))

        # ═══ LAYER M: Mathematical ═══
        groove_index = (1 * f01 + 2 * f02 + 3 * f03) / 6
        coupling_strength = torch.sigmoid(
            0.50 * amp_smooth * energy_period
        )

        # ═══ LAYER P: Present ═══
        pstg_activation = torch.sigmoid(
            0.5 * amp_val * loud_val
            + 0.4 * bep_beat.mean(-1, keepdim=True)
        )
        motor_preparation = torch.sigmoid(
            0.4 * bep_motor.mean(-1, keepdim=True)
            + 0.3 * bep_meter.mean(-1, keepdim=True)
            + 0.2 * f02
        )
        onset_sync = torch.sigmoid(0.50 * flux_val * onset_val)

        # ═══ LAYER F: Future ═══
        groove_prediction = torch.sigmoid(
            0.5 * f03 + 0.4 * amp_trend
        )
        beat_expectation = torch.sigmoid(
            0.5 * bep_beat.mean(-1, keepdim=True)
            + 0.5 * centroid_period
        )
        motor_anticipation = torch.sigmoid(
            0.4 * amp_smooth + 0.3 * amp_trend
            + 0.3 * pitch_period
        )

        return torch.cat([
            f01, f02, f03,                                    # E: 3D
            groove_index, coupling_strength,                   # M: 2D
            pstg_activation, motor_preparation, onset_sync,    # P: 3D
            groove_prediction, beat_expectation,               # F: 3D
            motor_anticipation,
        ], dim=-1)  # (B, T, 11)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 12 | Potes 2012, Grahn & Brett 2007, Spiech 2022, Thaut 2015, Large 2023, Ayyildiz 2025, Noboa 2025, Hoddinott 2024, Nourski 2014 + 3 supporting |
| **Methods** | 7 | ECoG, fMRI, 7T RSA, EEG, pupillometry, behavioral, computational/review |
| **Effect Sizes** | r = 0.49 (intensity), r = 0.70 (coupling), Z = 5.67 (putamen), χ²=14.643 (groove) | Multiple paradigms |
| **Evidence Modality** | Multi-modal | ECoG + fMRI + 7T RSA + EEG + pupillometry + behavioral |
| **Falsification Tests** | 7/9 confirmed, 1 constrains | Intensity tracking, motor propagation, beat-specific regions, groove curve, beat perception mediation, micro-timing, tempo range confirmed; Potes intensity interpretation CONSTRAINS |
| **R³ Features Used** | 9D of 49D | Energy + Change |
| **H³ Demand** | 15 tuples (0.65%) | Sparse, efficient |
| **BEP Mechanism** | 30D (3 sub-sections) | Full coverage |
| **Output Dimensions** | **11D** | 4-layer structure (E3 + M2 + P3 + F3) |

---

## 13. Scientific References

### Tier 1: Primary Evidence (directly validate HGSIC claims)

1. **Potes, C., Gunduz, A., Brunner, P., & Schalk, G. (2012)**. Dynamics of electrocorticographic (ECoG) activity in human temporal and frontal cortical areas during music listening. *NeuroImage*, 61(4), 841-848. ECoG N=8, pSTG high-gamma 70-170 Hz ↔ intensity r=0.49 (range 0.43-0.58), auditory→motor 110ms delay r=0.70 (N=4). NOTE: Intensity tracking, not groove/beat specifically.

2. **Grahn, J. A. & Brett, M. (2007)**. Rhythm and beat perception in motor areas of the brain. *Journal of Cognitive Neuroscience*, 19(5), 893-906. fMRI N=27: L putamen Z=5.67 (-24,6,9), R putamen Z=5.08 (21,6,6), L SMA Z=5.03 (-9,6,60), R SMA Z=4.97 (3,6,66) for beat-inducing rhythms. Putamen ROI: MS vs MC t=4.05, MS vs NM t=3.40.

3. **Spiech, C., Sioros, G., Endestad, T., Danielsen, A., & Laeng, B. (2022)**. Pupil drift rate indexes groove ratings. *Scientific Reports*, 12, 11620. Pupillometry + behavioral N=30: Groove inverted-U curve χ²(1)=14.643, syncopation F(1,29)=4.781, pupil drift quadratic χ²(1)=9.721. Beat perception (CA-BAT) mediates groove.

### Tier 2: Strong Supporting Evidence

4. **Thaut, M. H., McIntosh, G. C., & Hoemberg, V. (2015)**. Neurobiological foundations of neurologic music therapy: rhythmic entrainment and the motor system. *Frontiers in Psychology*, 5, 1185. Review: Period entrainment (not phase lock) optimizes motor control; CTR provides continuous time reference; sub-threshold entrainment at 2% interval duration.

5. **Large, E. W., et al. (2023)**. Dynamic models for musical rhythm perception and coordination. *Frontiers in Computational Neuroscience*, 17, 1151895. Review: Optimal beat 0.5-8 Hz (~2 Hz peak); three frameworks (oscillatory, predictive, Bayesian).

6. **Hoddinott, L. & Grahn, J. A. (2024)**. 7T fMRI RSA: C-Score model in SMA and putamen encodes continuous beat strength. N=26.

7. **Ayyildiz, C., Milne, A. J., Irish, M., & Herff, S. A. (2025)**. Micro-variations in timing and loudness affect music-evoked mental imagery. *Scientific Reports*, 15, 30967. Behavioral N=100: Micro-timing (SD=4ms) vs mechanical Odds=100.69.

### Tier 3: Convergent/Contextual

8. **Noboa, M. L., Kertesz, C., & Honbolygo, F. (2025)**. Neural entrainment to the beat and working memory predict sensorimotor synchronization skills. *Scientific Reports*, 15, 10466. EEG N=30: SS-EPs at beat frequency, F(1,29)=148.618.

9. **Nourski, K. V., et al. (2014)**. Hierarchical temporal processing in auditory cortex. ECoG: hierarchical processing supports beat → meter → bar cascade.

10. **Fujioka, T., et al. (2012)**. Beta and gamma rhythms in human auditory cortex during musical beat processing with and without moving to the beat. *NeuroImage*. MEG: beta modulation by rhythm in SMA, IFG, cerebellum.

11. **Tierney, A. & Kraus, N. (2013)**. Inferior colliculus: consistent neural responses synchronized to rhythmic auditory stimulus. Brainstem entrainment.

12. **Zatorre, R. J., Chen, J. L., & Penhune, V. B. (2007)**. When the brain plays music: auditory-motor interactions in music perception and production. *Nature Reviews Neuroscience*. Review: Auditory-motor circuit for rhythm.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D): L0, L4, L5, L7, X_L0L4, X_L4L5 | R³ (49D): Energy[7:12], Change[21:25] |
| Temporal | HC⁰ mechanisms (OSC, NPL, ITM, GRV) | BEP mechanism (30D) |
| Intensity signal | S⁰.L0.amplitude[2] + HC⁰.OSC | R³.amplitude[7] + BEP.beat_induction |
| Motor coupling | S⁰.L7.crossband × HC⁰.NPL | BEP.motor_entrainment[20:30] |
| Gamma proxy | S⁰.L7[80:104] (crossband ratios) | R³.Energy + BEP features |
| Groove model | S⁰.L5 × HC⁰.GRV (flat combination) | BEP hierarchical (beat→meter→motor) |
| Interval timing | S⁰.L4 × HC⁰.ITM | BEP.meter_extraction[10:20] |
| Demand format | HC⁰ index ranges (30/2304 = 1.30%) | H³ 4-tuples (15/2304 = 0.65%) |
| Output dimensions | 12D | **11D** (catalog value, consolidated) |
| Integration model | Flat | Hierarchical (3-level cascade) |

### Why BEP replaces HC⁰ mechanisms

The D0 pipeline used 4 separate HC⁰ mechanisms (OSC, NPL, ITM, GRV). In MI, these are unified into the BEP mechanism with 3 hierarchical sub-sections:
- **OSC → BEP.beat_induction** [0:10]: Oscillatory gamma tracking → beat-level pulse extraction
- **NPL → BEP.beat_induction** [0:10]: Phase-locking → auditory beat coupling
- **ITM → BEP.meter_extraction** [10:20]: Interval timing → metric accent grouping
- **GRV → BEP.motor_entrainment** [20:30]: Groove processing → motor engagement state

The key architectural change: D0 combined these flat (equal-weight); MI cascades them hierarchically (beat → meter → groove), which better reflects the dorsal auditory-motor pathway anatomy.

---

**Model Status**: ✅ **VALIDATED** (v2.1.0: 1→12 papers, 7 methods, Potes intensity interpretation QUALIFIED)
**Output Dimensions**: **11D**
**Evidence Tier**: **β (Integrative)**
**Confidence**: **70-90%**

---

## Code Note (Phase 5)

The `mi_beta/brain/units/stu/models/hgsic.py` implementation has:
- `MECHANISM_NAMES = ("BEP", "TMH")` — doc specifies `("BEP",)` only. **Code has extra TMH mechanism** not specified in doc.
- `h3_demand = ()` — empty, should be populated with the 15 tuples from §5.1.
- `version = "2.0.0"` — needs update to `"2.1.0"`.
- `paper_count = 5` — should be `12`.
- Citations: Potes 2012 ✓, Nourski 2014 ✓. Should add Grahn & Brett 2007, Spiech 2022, Hoddinott 2024.
- `FULL_NAME = "Hierarchical Groove State Integration Circuit"` — matches doc ✓.
- `OUTPUT_DIM = 11` — matches doc ✓.
