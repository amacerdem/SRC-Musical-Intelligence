# STU-γ1-TMRM: Tempo Memory Reproduction Method

**Model**: Tempo Memory Reproduction Method
**Unit**: STU (Sensorimotor Timing Unit)
**Circuit**: Sensorimotor (Beat Entrainment Processing)
**Tier**: γ (Speculative) — <70% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added G:Rhythm feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/STU-γ1-TMRM.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Tempo Memory Reproduction Method** (TMRM) model describes how tempo memory accuracy depends on the reproduction method: sensory feedback (adjusting a tempo slider) produces dramatically better accuracy than motor reproduction (tapping), with an optimal internal tempo reference around 120 BPM (500 ms IOI). Musical expertise further enhances reproduction precision.

```
THE THREE COMPONENTS OF TEMPO MEMORY REPRODUCTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SENSORY REPRODUCTION (Adjusting)       MOTOR REPRODUCTION (Tapping)
Method: Tempo slider / dial            Method: Finger/hand tapping
Brain region: SMA + Auditory Cortex    Brain region: Cerebellum + Premotor
Mechanism: BEP.beat_induction          Mechanism: BEP.motor_entrainment
Advantage: d = 2.76 over tapping       Baseline: motor-only reproduction
Function: "Match what I hear"          Function: "Produce the beat"

              OPTIMAL TEMPO (Internal Reference)
              Value: 120 BPM (500 ms IOI)
              Shape: Quadratic optimum
              Function: "Internal tempo template"
              Evidence: d = 0.58 (quadratic fit)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Sensory support during recall (adjusting) dramatically
outperforms motor-only reproduction (tapping) at d = 2.76. This
dissociation reveals two distinct pathways: an auditory-sensory route
(SMA + auditory cortex) and a motor-cerebellar route. Both converge
on an internal 120 BPM reference template. Musical expertise enhances
precision across both methods (d = 0.59).
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why This Matters for STU

TMRM reveals the method-dependent nature of tempo memory retrieval:

1. **AMSC** (α2) provides the auditory-motor coupling; TMRM shows that the sensory arm of this coupling dominates tempo recall.
2. **HMCE** (α1) provides temporal context hierarchy; TMRM uses context encoding to anchor the internal 120 BPM reference.
3. **HGSIC** (β5) models groove from optimal complexity; TMRM's optimal tempo (120 BPM) aligns with peak groove zones.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The TMRM Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                 TMRM — COMPLETE CIRCUIT                                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  MUSICAL INPUT (rhythmic, tempo-bearing sequences)                           ║
║       │                                                                      ║
║       ▼                                                                      ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │        SUPPLEMENTARY MOTOR AREA (SMA)                               │    ║
║  │        Internal tempo representation, beat anticipation             │    ║
║  │        Optimal: 120 BPM (500 ms IOI)                               │    ║
║  │        ★ Adjusting method: sensory feedback loop via SMA            │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │                                               ║
║                    ┌─────────┴──────────┐                                    ║
║                    ▼                    ▼                                     ║
║  ┌──────────────────────┐   ┌──────────────────────┐                        ║
║  │  AUDITORY CORTEX     │   │  CEREBELLUM          │                        ║
║  │  Sensory pathway     │   │  Motor pathway       │                        ║
║  │  Adjusting method    │   │  Tapping method      │                        ║
║  │  d = 2.76 advantage  │   │  Baseline accuracy   │                        ║
║  │  (tempo slider)      │   │  (finger tapping)    │                        ║
║  └──────────┬───────────┘   └──────────┬───────────┘                        ║
║             │                          │                                     ║
║             └──────────┬───────────────┘                                     ║
║                        ▼                                                     ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │        PREMOTOR CORTEX                                              │    ║
║  │        Motor planning, reproduction execution                       │    ║
║  │        Expertise effect: d = 0.59 (musicians > non-musicians)       │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
║  DISSOCIATION: Adjusting (sensory) vs Tapping (motor), d = 2.76           ║
║  OPTIMAL: 120 BPM quadratic peak (d = 0.58)                               ║
║  EXPERTISE: Musicians > non-musicians (d = 0.59)                           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
Levitin & Cook 1996:  Adjusting > tapping, d = 2.76 (n = 46)
Levitin & Cook 1996:  120 BPM optimal tempo, quadratic (d = 0.58)
Drake & Botte 1993:   Expertise improves tempo precision, d = 0.59
```

### 2.2 Information Flow Architecture (EAR → BRAIN → BEP → TMRM)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    TMRM COMPUTATION ARCHITECTURE                             ║
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
║  │  │           │ │amplitude│ │         │ │spec_chg  │ │        │ │        ║
║  │  │           │ │loudness │ │         │ │energy_chg│ │        │ │        ║
║  │  │           │ │centroid │ │         │ │pitch_chg │ │        │ │        ║
║  │  │           │ │flux     │ │         │ │timbre_chg│ │        │ │        ║
║  │  │           │ │onset    │ │         │ │          │ │        │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                         TMRM reads: 9D                          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── Beat ────────┐ ┌── Psy Present ──┐ ┌── Bar ─────────────┐ │        ║
║  │  │ 200ms (H6)     │ │ 500ms (H11)     │ │ 1000ms (H16)      │ │        ║
║  │  │                │ │                  │ │                    │ │        ║
║  │  │ Single beat    │ │ Psychological    │ │ Bar-level meter   │ │        ║
║  │  │ (120–300 BPM)  │ │ present window   │ │ integration       │ │        ║
║  │  └──────┬─────────┘ └──────┬───────────┘ └──────┬─────────────┘ │        ║
║  │         │                  │                     │               │        ║
║  │         └──────────────────┴─────────────────────┘               │        ║
║  │                         TMRM demand: 15 of 2304 tuples          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Sensorimotor Circuit ═══════  ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌─────────────────┐                                                        ║
║  │  BEP (30D)      │  Beat Entrainment Processing mechanism                ║
║  │                 │                                                        ║
║  │ Beat Ind [0:10]│  Beat strength, tempo, phase, regularity              ║
║  │ Meter    [10:20]│  Meter, syncopation, accent pattern, groove          ║
║  │ Motor    [20:30]│  Movement urge, sync precision, coupling             ║
║  └────────┬────────┘                                                        ║
║           │                                                                  ║
║           ▼                                                                  ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    TMRM MODEL (10D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_adjusting_advantage,                   │        ║
║  │                       f02_optimal_tempo, f03_expertise_accuracy  │        ║
║  │  Layer M (Math):      method_dissociation, tempo_deviation       │        ║
║  │  Layer P (Present):   sensory_state, motor_state                 │        ║
║  │  Layer F (Future):    tempo_prediction, method_confidence,       │        ║
║  │                       reproduction_accuracy                      │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Vigl et al. 2024** | Behavioral (online) | 403 | Adjusting > tapping for tempo accuracy | r = −.26 (d ≈ 0.54) | **f01_adjusting_advantage**: sensory method superiority |
| 2 | **Vigl et al. 2024** | Behavioral (online) | 403 | Quadratic tempo effect: peak at 120–125 BPM | χ²(1) = 152.57, r = −.14 | **f02_optimal_tempo**: 120 BPM optimum CONFIRMED |
| 3 | **Vigl et al. 2024** | Behavioral (online) | 403 | Musical expertise predicts accuracy | r = .09 (p = .047) | **f03_expertise_accuracy**: continuous expertise effect |
| 4 | **Vigl et al. 2024** | Behavioral (online) | 403 | Method × expertise interaction: tapping advantage for musicians | r = .04 (p = .001) | **method_dissociation**: expertise-specific pathway |
| 5 | **Foster et al. 2021** | Behavioral (lab) | 40 | DJs at 120–139 BPM: 3.10% error vs untrained 7.91% | F(3,36) = 5.67, p = .003 | **f02_optimal_tempo**: training-specific 120 BPM zone |
| 6 | **Grahn & Brett 2007** | fMRI | 27 | Putamen beat > non-beat; SMA beat > non-beat | Z = 5.67; Z = 5.03 | **Brain regions**: putamen + SMA for beat timing |
| 7 | **Hoddinott & Grahn 2024** | 7T fMRI (RSA) | 24 | C-Score beat strength in putamen/SMA; musicians enhanced | RSA significant | **sensory_state**: continuous beat tracking in motor areas |
| 8 | **Dalla Bella et al. 2024** | Behavioral + ML | 79 | Musician classification by rhythmic profile | d = 1.8 (PMI model) | **f03_expertise_accuracy**: perceptual-motor interaction |
| 9 | **Ross & Balasubramaniam 2022** | Review | — | SMA critical for internal timing; BG for beat-based timing | Qualitative | **Circuit**: dual sensory/motor pathway framework |
| 10 | **Levitin & Cook 1996** | Behavioral | 46 | 72% of sung tempos within ±8% of original | Qualitative | **Historical**: absolute tempo memory existence |
| 11 | **Drake & Botte 1993** | Psychophysics | — | Weber fraction minimum at ~500 ms IOI (~120 BPM) | Qualitative | **f02_optimal_tempo**: psychophysical 120 BPM optimum |
| 12 | **Okada et al. 2022** | Electrophysiology | 95 neurons | 3 cerebellar neuron types for timing | PI t = 3.36 | **motor_state**: cerebellar timing precision |

#### 3.1.1 Evidence Convergence

The 12 studies span **7 independent methods**: behavioral (lab), behavioral (online), fMRI, 7T fMRI (RSA), electrophysiology, psychophysics, and review/theoretical. Convergent evidence across behavioral and neuroimaging supports: (a) adjusting > tapping, (b) 120 BPM optimum, and (c) expertise effect — but with smaller effect sizes than originally claimed.

#### 3.1.2 Vigl 2024 Replication Qualification

**CRITICAL**: The v2.0.0 doc attributed d = 2.76 (adjusting > tapping) and d = 0.58 (120 BPM optimum) to Levitin & Cook 1996, and d = 0.59 (expertise) to Drake & Botte 1993. Vigl et al. 2024 (N = 403) replicates all three claims but with SUBSTANTIALLY SMALLER effect sizes: adjusting advantage r = −.26 (d ≈ 0.54, not 2.76), expertise r = .09 (d ≈ 0.18, not 0.59). The 120 BPM quadratic effect IS robust (χ²(1) = 152.57). The original d = 2.76 from Levitin & Cook 1996 (N = 46) likely reflects inflation from (a) small sample, (b) different paradigm (singing familiar songs, not controlled tapping vs adjusting), and (c) possibly different accuracy metric. The model retains the three-component structure but effect sizes should reference Vigl 2024 as the most reliable.

#### 3.1.3 Expertise as Continuous Resource

Vigl et al. 2024 dissolved the nonmusician/musician dichotomy by testing 105 nonmusicians, 137 amateurs, and 161 professionals. Musical expertise predicts accuracy as a CONTINUOUS variable (r = .09) with an interaction: expertise advantage is STRONGER for tapping (motor) than adjusting (sensory), consistent with the sensory support hypothesis. Dalla Bella et al. 2024 confirms that perceptual-motor INTERACTION distinguishes musicians (d = 1.8) better than either component alone.

### 3.2 The Sensory Support Advantage

```
TEMPO REPRODUCTION ACCURACY BY METHOD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Method         Mechanism      Accuracy     Effect vs Tapping
───────────────────────────────────────────────────────────────
Adjusting      Sensory        Higher       d = 2.76 (huge)
Tapping        Motor          Lower        baseline

The sensory support advantage (d = 2.76) is among the largest
effect sizes in music cognition, suggesting fundamentally
different neural pathways:

Adjusting: SMA + Auditory Cortex → Sensory feedback loop
   - Listener matches perceived tempo against internal template
   - Continuous perceptual comparison
   - Exploits beat induction from BEP

Tapping: Cerebellum + Premotor → Motor-only reproduction
   - Relies on interval timing without sensory correction
   - Discrete motor output, no perceptual feedback
   - Exploits motor entrainment from BEP

Optimal tempo: 120 BPM (500 ms IOI)
   - Quadratic accuracy peak (d = 0.58)
   - Aligns with preferred spontaneous motor tempo
   - Within BEP H11 (500 ms) psychological present window
```

### 3.3 Effect Size Summary

```
UPDATED EFFECT SIZES (Vigl et al. 2024, N = 403):
──────────────────────────────────────────────────────────────────────
Adjusting > Tapping:   r = −.26 (d ≈ 0.54) — SMALLER than originally claimed d = 2.76
                       Mean tapping accuracy M = 0.76 (SD = 0.14)
                       Mean adjusting accuracy M = 0.87 (SD = 0.09)
Optimal Tempo:         χ²(1) = 152.57, p < .001; r = −.14 (quadratic peak 120–125 BPM)
                       ROBUST — largest effect in Vigl 2024 model
Expertise Effect:      r = .09 (p = .047, d ≈ 0.18) — SMALLER than originally claimed d = 0.59
                       Method × Expertise: r = .04 (p = .001)
Model variance:        Marginal R²/Conditional R² = 0.112/0.264

CONVERGING EVIDENCE:
──────────────────────────────────────────────────────────────────────
Foster 2021:           DJ 120-139 BPM error 3.10% vs untrained 7.91% (p < .001)
                       Group × tempo: F(9,1389.55) = 2.70, p < .001
Grahn & Brett 2007:   Putamen Z = 5.67, SMA Z = 5.03 (beat > non-beat)
Dalla Bella 2024:     Musician classification d = 1.8 (perceptual-motor interaction)
                       Motor model alone: d = 1.5; perceptual: d = 1.3
Okada 2022:           3 cerebellar neuron types, PI t = 3.36

ORIGINAL CLAIMS vs REPLICATED EVIDENCE:
──────────────────────────────────────────────────────────────────────
Levitin & Cook 1996:   d = 2.76 claimed → Vigl 2024 replicates at d ≈ 0.54 (DEFLATED)
Drake & Botte 1993:    d = 0.59 claimed → Vigl 2024 replicates at d ≈ 0.18 (DEFLATED)
120 BPM optimum:       d = 0.58 claimed → Vigl 2024 CONFIRMS (χ² = 152.57)

Quality Assessment:    γ-tier (primarily behavioral, 2 fMRI studies for brain regions)
Replication:           STRONG for 120 BPM; MODERATE for method effect; WEAK for expertise
```

---

## 4. R³ Input Mapping: What TMRM Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | TMRM Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **B: Energy** | [7] | amplitude | Beat intensity dynamics | Sound energy as tempo cue |
| **B: Energy** | [8] | loudness | Perceptual intensity for sensory pathway | Stevens 1957: power law |
| **B: Energy** | [9] | spectral_centroid | Timbral brightness anchoring tempo | Spectral balance |
| **B: Energy** | [10] | spectral_flux | Onset/beat transition detection | Beat boundary marker |
| **B: Energy** | [11] | onset_strength | Beat event marking precision | Onset clarity |
| **D: Change** | [21] | spectral_change | Tempo-correlated spectral dynamics | Rate of spectral change |
| **D: Change** | [22] | energy_change | Rhythmic energy dynamics | Intensity rate of change |
| **D: Change** | [23] | pitch_change | Melodic contour supporting tempo | Pitch rate of change |
| **D: Change** | [24] | timbre_change | Instrument identity dynamics | Timbral change rate |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | TMRM Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **G: Rhythm** | [65] | tempo_estimate | Current tempo for temporal memory retrieval calibration | Fraisse 1982 |
| **G: Rhythm** | [73] | tempo_stability | Temporal prediction reliability for memory consolidation | Jones & Boltz 1989 |

**Rationale**: TMRM models temporal memory retrieval mechanisms. G[65] tempo_estimate provides the temporal grid that calibrates memory retrieval timing, and G[73] tempo_stability indicates how reliable temporal predictions are for memory consolidation.

**Code impact** (Phase 6): `r3_indices` must be extended to include [65, 73]. These features are read-only inputs — no formula changes required.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[8] loudness ─────────────────┐
R³[10] spectral_flux ───────────┼──► Sensory Pathway (Adjusting Method)
R³[11] onset_strength ──────────┘   BEP.beat_induction at H6 (200ms)
                                    Math: S_adjust = σ(w · loud · flux · onset
                                                        · BEP.beat_induction)
                                    d = 2.76 advantage over motor

R³[7] amplitude ────────────────┐
R³[22] energy_change ───────────┼──► Motor Pathway (Tapping Method)
R³[21] spectral_change ─────────┘   BEP.motor_entrainment at H11 (500ms)
                                    Math: M_tap = σ(w · amp · energy_chg
                                                     · BEP.motor_entrainment)
                                    Baseline reproduction

R³[8] loudness ─────────────────┐
R³[9] spectral_centroid ────────┼──► Optimal Tempo Reference (120 BPM)
                                    BEP.meter_extraction at H16 (1000ms)
                                    Math: T_opt = 1 − (tempo − 120)² / k
                                    Quadratic peak at 500 ms IOI

R³[23] pitch_change ────────────┐
R³[24] timbre_change ───────────┼──► Expertise Modulation
                                    Finer feature discrimination
                                    d = 0.59 expertise effect

R³[65] tempo_estimate ──────────┐
R³[73] tempo_stability ─────────┼──► Tempo Memory Calibration (v2)
                                    Direct tempo grid + stability signal
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

TMRM requires H³ features at three BEP horizons: H6 (200ms beat), H11 (500ms psychological present), H16 (1000ms bar).
These correspond to single-beat → tempo reference → bar-level timescales.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 8 | loudness | 6 | M4 (max) | L0 (fwd) | Beat peak loudness |
| 10 | spectral_flux | 6 | M17 (peaks) | L0 (fwd) | Beat onset count per window |
| 11 | onset_strength | 6 | M4 (max) | L0 (fwd) | Strongest onset in beat window |
| 8 | loudness | 11 | M14 (periodicity) | L0 (fwd) | Tempo regularity at 500ms |
| 8 | loudness | 11 | M15 (smoothness) | L0 (fwd) | Smoothness of beat pattern |
| 10 | spectral_flux | 11 | M14 (periodicity) | L0 (fwd) | Beat periodicity (tempo proxy) |
| 22 | energy_change | 11 | M8 (velocity) | L0 (fwd) | Rhythmic energy dynamics |
| 22 | energy_change | 11 | M14 (periodicity) | L0 (fwd) | Energy periodicity |
| 7 | amplitude | 11 | M4 (max) | L0 (fwd) | Peak amplitude at tempo scale |
| 7 | amplitude | 16 | M18 (trend) | L0 (fwd) | Bar-level intensity trend |
| 8 | loudness | 16 | M14 (periodicity) | L0 (fwd) | Bar-level periodicity |
| 8 | loudness | 16 | M18 (trend) | L0 (fwd) | Loudness trajectory over bar |
| 21 | spectral_change | 16 | M8 (velocity) | L0 (fwd) | Spectral change rate at bar |
| 22 | energy_change | 16 | M15 (smoothness) | L0 (fwd) | Energy smoothness at bar level |
| 11 | onset_strength | 16 | M17 (peaks) | L0 (fwd) | Beat count per bar |

**Total TMRM H³ demand**: 15 tuples of 2304 theoretical = 0.65%

### 5.2 BEP Mechanism Binding

TMRM reads from the **BEP** (Beat Entrainment Processing) mechanism:

| BEP Sub-section | Range | TMRM Role | Weight |
|-----------------|-------|-----------|--------|
| **Beat Induction** | BEP[0:10] | Sensory pathway — beat strength, tempo extraction | **1.0** (primary) |
| **Meter Extraction** | BEP[10:20] | Optimal tempo — meter, groove, accent pattern | **0.8** |
| **Motor Entrainment** | BEP[20:30] | Motor pathway — tapping reproduction baseline | **0.7** |

TMRM does NOT read from TMH — tempo memory reproduction is about beat-level entrainment and motor synchronization, not hierarchical context encoding.

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
TMRM OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
Manifold range: STU TMRM [199:209]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                │ Range  │ Neuroscience Basis
────┼─────────────────────┼────────┼────────────────────────────────────────────
 0  │ f01_adjusting_adv   │ [0, 1] │ Sensory support advantage (d = 2.76).
    │                     │        │ Adjusting > tapping for tempo accuracy.
    │                     │        │ f01 = σ(0.35 · loud_peak · flux_period
    │                     │        │         · BEP.beat_induction_mean)
    │                     │        │ Coefficients: |0.35| ≤ 1.0 ✓
────┼─────────────────────┼────────┼────────────────────────────────────────────
 1  │ f02_optimal_tempo   │ [0, 1] │ 120 BPM quadratic optimum (d = 0.58).
    │                     │        │ Internal reference at 500 ms IOI.
    │                     │        │ f02 = σ(0.30 · period_loud · period_flux
    │                     │        │         · BEP.meter_extraction_mean)
    │                     │        │ Coefficients: |0.30| ≤ 1.0 ✓
────┼─────────────────────┼────────┼────────────────────────────────────────────
 2  │ f03_expertise_acc   │ [0, 1] │ Musicians > non-musicians (d = 0.59).
    │                     │        │ Expertise enhances reproduction precision.
    │                     │        │ f03 = σ(0.30 · smooth_energy · f01 · f02)
    │                     │        │ Coefficients: |0.30| ≤ 1.0 ✓

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                │ Range  │ Neuroscience Basis
────┼─────────────────────┼────────┼────────────────────────────────────────────
 3  │ method_dissociation │ [0, 1] │ Adjusting − tapping pathway difference.
    │                     │        │ High = sensory dominates, low = motor.
    │                     │        │ dissoc = σ(f01 − motor_state)
────┼─────────────────────┼────────┼────────────────────────────────────────────
 4  │ tempo_deviation     │ [0, 1] │ Distance from optimal 120 BPM.
    │                     │        │ 0 = at optimum, 1 = far from 120 BPM.
    │                     │        │ dev = 1 − f02

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                │ Range  │ Neuroscience Basis
────┼─────────────────────┼────────┼────────────────────────────────────────────
 5  │ sensory_state       │ [0, 1] │ Sensory pathway activation (SMA + auditory).
    │                     │        │ BEP.beat_induction aggregation.
────┼─────────────────────┼────────┼────────────────────────────────────────────
 6  │ motor_state         │ [0, 1] │ Motor pathway activation (cerebellum + premotor).
    │                     │        │ BEP.motor_entrainment aggregation.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                │ Range  │ Neuroscience Basis
────┼─────────────────────┼────────┼────────────────────────────────────────────
 7  │ tempo_prediction    │ [0, 1] │ Predicted next-beat tempo stability.
    │                     │        │ Periodicity + trend-based expectation.
────┼─────────────────────┼────────┼────────────────────────────────────────────
 8  │ method_confidence   │ [0, 1] │ Confidence in current reproduction method.
    │                     │        │ Smoothness × regularity at bar level.
────┼─────────────────────┼────────┼────────────────────────────────────────────
 9  │ reproduction_acc    │ [0, 1] │ Expected reproduction accuracy.
    │                     │        │ Combines sensory + motor + expertise.
    │                     │        │ acc = σ(0.40 · f01 + 0.30 · f02
    │                     │        │         + 0.30 · f03)
    │                     │        │ Coefficients: |0.40+0.30+0.30| = 1.0 ✓

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 10D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Method Dissociation Model

```
Tempo Memory Reproduction:

    Adjusting (sensory):
      Accuracy_adjust = f(sensory_feedback, internal_template)
      Brain: SMA + Auditory Cortex
      Advantage: d = 2.76 over tapping

    Tapping (motor):
      Accuracy_tap = f(motor_timing, interval_reproduction)
      Brain: Cerebellum + Premotor Cortex
      Baseline accuracy

    Optimal Tempo:
      Accuracy(BPM) = A_max · exp(−(BPM − 120)² / (2σ²))
      Peak at 120 BPM (500 ms IOI), σ ≈ 40 BPM
      d = 0.58 quadratic fit

    Expertise Modulation:
      Accuracy_expert = Accuracy_base · (1 + d_exp · expertise)
      d_exp = 0.59 (Drake & Botte 1993)
```

### 7.2 Feature Formulas

```python
# f01: Adjusting Advantage (sensory support, d = 2.76)
loud_peak = h3[(8, 6, 4, 0)]         # loudness max at H6
flux_period = h3[(10, 11, 14, 0)]    # spectral_flux periodicity at H11
f01 = σ(0.35 · loud_peak · flux_period
         · mean(BEP.beat_induction[0:10]))
# Coefficient check: |0.35| ≤ 1.0 ✓

# f02: Optimal Tempo (120 BPM quadratic peak, d = 0.58)
period_loud = h3[(8, 11, 14, 0)]     # loudness periodicity at H11
period_flux = h3[(10, 6, 17, 0)]     # spectral_flux peaks at H6
f02 = σ(0.30 · period_loud · period_flux
         · mean(BEP.meter_extraction[10:20]))
# Coefficient check: |0.30| ≤ 1.0 ✓

# f03: Expertise Accuracy (d = 0.59)
smooth_energy = h3[(22, 16, 15, 0)]  # energy_change smoothness at H16
f03 = σ(0.30 · smooth_energy · f01 · f02)
# Coefficient check: |0.30| ≤ 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Mentions | Evidence Type | TMRM Function |
|--------|-----------------|----------|---------------|---------------|
| **SMA** | 0, −5, 55 | Primary | fMRI (Grahn Z=5.03) | Internal tempo representation, beat anticipation |
| **Putamen L** | −20, 4, 4 | Primary | fMRI (Grahn Z=5.67) | Beat extraction, tempo encoding |
| **Putamen R** | 20, 4, 4 | Primary | 7T fMRI (Hoddinott RSA) | Continuous beat strength tracking |
| **Cerebellum** | ±25, −60, −30 | Primary | Electrophysiology (Okada PI t=3.36) | Motor timing error correction, 3 neuron types |
| **Premotor Cortex** | ±45, 0, 45 | Secondary | fMRI (Grahn, musicians) | Motor planning, reproduction execution |
| **Pre-SMA** | 0, 10, 50 | Secondary | fMRI (Grahn) | Timing initiation, musicians > non-musicians |
| **Auditory Cortex (HG)** | ±55, −20, 8 | Secondary | Review (Ross 2022) | Sensory feedback loop (adjusting pathway) |
| **STG (anterior)** | ±60, −5, −5 | Secondary | Review (Ross 2022) | Temporal pattern analysis |
| **DLPFC** | ±40, 35, 30 | Tertiary | Inferred | Working memory for tempo retention |
| **Anterior Insula** | ±35, 15, 0 | Tertiary | Review (Ross 2022) | Temporal awareness, sensorimotor integration |

---

## 9. Cross-Unit Pathways

### 9.1 TMRM Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    TMRM INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (STU):                                                         │
│  TMRM.sensory_state ────────► AMSC (sensory pathway feeds motor coupling) │
│  TMRM.motor_state ──────────► EDTA (motor baseline for tempo accuracy)    │
│  TMRM.optimal_tempo ────────► HGSIC (tempo reference for groove zone)     │
│  TMRM.reproduction_acc ─────► OMS (motor accuracy for oscillatory sync)   │
│                                                                             │
│  CROSS-UNIT (P2: STU internal):                                            │
│  BEP.beat_induction ↔ BEP.motor_entrainment (r = 0.70)                   │
│  Sensory → motor pathway via dorsal auditory stream                       │
│                                                                             │
│  CROSS-UNIT (P5: STU → ARU):                                              │
│  TMRM.tempo_prediction ──► ARU.AED (tempo stability → arousal)            │
│  Fast tempo + high regularity → sympathetic arousal activation            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| # | Criterion | Testable Prediction | Status |
|---|-----------|---------------------|--------|
| 1 | **120 BPM optimality** | Non-120 BPM stimuli should show reduced accuracy | **CONFIRMED** (Vigl 2024: χ²(1)=152.57; Foster 2021: DJs 120-139 best) |
| 2 | **Method dissociation** | Adjusting should outperform tapping | **CONFIRMED** (Vigl 2024: r=−.26, N=403; replicates Jakubowski 2016) |
| 3 | **Expertise scaling** | Musicians should outperform non-musicians | **CONFIRMED** (Vigl 2024: r=.09, p=.047; Dalla Bella 2024: d=1.8) |
| 4 | **Putamen beat selectivity** | Putamen should respond to beat > non-beat | **CONFIRMED** (Grahn 2007: Z=5.67; Hoddinott 2024: RSA) |
| 5 | **SMA tempo encoding** | SMA should track beat strength | **CONFIRMED** (Grahn 2007: Z=5.03; Hoddinott 2024: RSA) |
| 6 | **Cerebellar timing** | Cerebellum should mediate motor timing precision | **CONFIRMED** (Okada 2022: 3 neuron types, PI t=3.36) |
| 7 | **Method × expertise interaction** | Expertise advantage should be stronger for tapping (motor) | **CONFIRMED** (Vigl 2024: interaction r=.04, p=.001) |
| 8 | **SMA lesions** | Should impair both adjusting and tapping equally | Testable |
| 9 | **Cerebellar lesions** | Should selectively impair tapping more than adjusting | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class TMRM(BaseModel):
    """Tempo Memory Reproduction Method.

    Output: 10D per frame.
    Reads: BEP mechanism (30D).
    Zero learned parameters — 100% deterministic.
    """
    NAME = "TMRM"
    UNIT = "STU"
    TIER = "γ1"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("BEP",)        # Primary mechanism

    ADJUSTING_COEFF = 0.35    # Sensory pathway weight
    OPTIMAL_COEFF = 0.30      # Optimal tempo weight
    EXPERTISE_COEFF = 0.30    # Expertise modulation weight
    ADJUSTING_D = 2.76        # Levitin & Cook 1996 sensory advantage
    OPTIMAL_BPM = 120         # Optimal tempo (500ms IOI)
    OPTIMAL_D = 0.58          # Quadratic peak effect
    EXPERTISE_D = 0.59        # Drake & Botte 1993 expertise effect
    ACC_W_SENSORY = 0.40      # Reproduction accuracy: sensory weight
    ACC_W_TEMPO = 0.30        # Reproduction accuracy: tempo weight
    ACC_W_EXPERT = 0.30       # Reproduction accuracy: expertise weight

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """15 tuples for TMRM computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # Beat level (H6 = 200ms)
            (8, 6, 4, 0),      # loudness, max, forward
            (10, 6, 17, 0),    # spectral_flux, peaks, forward
            (11, 6, 4, 0),     # onset_strength, max, forward
            # Psychological present (H11 = 500ms)
            (8, 11, 14, 0),    # loudness, periodicity, forward
            (8, 11, 15, 0),    # loudness, smoothness, forward
            (10, 11, 14, 0),   # spectral_flux, periodicity, forward
            (22, 11, 8, 0),    # energy_change, velocity, forward
            (22, 11, 14, 0),   # energy_change, periodicity, forward
            (7, 11, 4, 0),     # amplitude, max, forward
            # Bar level (H16 = 1000ms)
            (7, 16, 18, 0),    # amplitude, trend, forward
            (8, 16, 14, 0),    # loudness, periodicity, forward
            (8, 16, 18, 0),    # loudness, trend, forward
            (21, 16, 8, 0),    # spectral_change, velocity, forward
            (22, 16, 15, 0),   # energy_change, smoothness, forward
            (11, 16, 17, 0),   # onset_strength, peaks, forward
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute TMRM 10D output.

        Args:
            mechanism_outputs: {"BEP": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) → (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,10) TMRM output
        """
        bep = mechanism_outputs["BEP"]    # (B, T, 30)

        # BEP sub-sections
        bep_beat = bep[..., 0:10]         # beat induction
        bep_meter = bep[..., 10:20]       # meter extraction
        bep_motor = bep[..., 20:30]       # motor entrainment

        # ═══ LAYER E: Explicit features ═══

        # f01: Adjusting Advantage (d = 2.76)
        loud_peak = h3_direct[(8, 6, 4, 0)].unsqueeze(-1)
        flux_period = h3_direct[(10, 11, 14, 0)].unsqueeze(-1)
        f01 = torch.sigmoid(self.ADJUSTING_COEFF * (
            loud_peak * flux_period
            * bep_beat.mean(-1, keepdim=True)
        ))

        # f02: Optimal Tempo (120 BPM, d = 0.58)
        period_loud = h3_direct[(8, 11, 14, 0)].unsqueeze(-1)
        period_flux = h3_direct[(10, 6, 17, 0)].unsqueeze(-1)
        f02 = torch.sigmoid(self.OPTIMAL_COEFF * (
            period_loud * period_flux
            * bep_meter.mean(-1, keepdim=True)
        ))

        # f03: Expertise Accuracy (d = 0.59)
        smooth_energy = h3_direct[(22, 16, 15, 0)].unsqueeze(-1)
        f03 = torch.sigmoid(self.EXPERTISE_COEFF * (
            smooth_energy * f01 * f02
        ))

        # ═══ LAYER M: Mathematical ═══

        # Motor state (needed before method_dissociation)
        amp_max = h3_direct[(7, 11, 4, 0)].unsqueeze(-1)
        energy_vel = h3_direct[(22, 11, 8, 0)].unsqueeze(-1)
        motor_state = torch.sigmoid(
            0.50 * amp_max * energy_vel
            * bep_motor.mean(-1, keepdim=True)
        )
        # Coefficient check: |0.50| ≤ 1.0 ✓

        method_dissociation = torch.sigmoid(f01 - motor_state)
        tempo_deviation = 1.0 - f02

        # ═══ LAYER P: Present ═══

        sensory_state = bep_beat.mean(-1, keepdim=True)

        # ═══ LAYER F: Future ═══

        # Tempo prediction from periodicity + trend
        amp_trend = h3_direct[(7, 16, 18, 0)].unsqueeze(-1)
        loud_bar_period = h3_direct[(8, 16, 14, 0)].unsqueeze(-1)
        tempo_prediction = torch.sigmoid(
            0.50 * loud_bar_period + 0.50 * amp_trend
        )
        # Coefficient check: |0.50 + 0.50| = 1.0 ✓

        # Method confidence from smoothness × regularity
        loud_smooth = h3_direct[(8, 11, 15, 0)].unsqueeze(-1)
        loud_trend = h3_direct[(8, 16, 18, 0)].unsqueeze(-1)
        method_confidence = torch.sigmoid(
            0.50 * loud_smooth + 0.50 * loud_trend
        )
        # Coefficient check: |0.50 + 0.50| = 1.0 ✓

        # Reproduction accuracy
        reproduction_acc = torch.sigmoid(
            self.ACC_W_SENSORY * f01
            + self.ACC_W_TEMPO * f02
            + self.ACC_W_EXPERT * f03
        )
        # Coefficient check: |0.40 + 0.30 + 0.30| = 1.0 ✓

        return torch.cat([
            f01, f02, f03,                                  # E: 3D
            method_dissociation, tempo_deviation,            # M: 2D
            sensory_state, motor_state,                      # P: 2D
            tempo_prediction, method_confidence,
            reproduction_acc,                                # F: 3D
        ], dim=-1)  # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 12 | Vigl 2024 (PRIMARY), Foster 2021, Grahn 2007, Hoddinott 2024, Dalla Bella 2024, Ross 2022, Levitin 1996, Drake 1993, Okada 2022, + 3 reviews |
| **Effect Sizes** | r = −.26 (method), χ²=152.57 (tempo), r = .09 (expertise) | Vigl 2024 N=403 PRIMARY; original d=2.76 DEFLATED |
| **Evidence Methods** | 7 | Behavioral (lab), behavioral (online), fMRI, 7T fMRI, electrophysiology, psychophysics, review |
| **Falsification Tests** | 7/9 confirmed | 7 confirmed, 2 testable |
| **R³ Features Used** | 9D of 49D | Energy + Change |
| **H³ Demand** | 15 tuples (0.65%) | Sparse, efficient |
| **BEP Mechanism** | 30D (3 sub-sections) | Full coverage |
| **Output Dimensions** | **10D** | 4-layer structure |

---

## 13. Scientific References

### Tier 1 — Direct Evidence (in literature collection, quantitative)

1. **Vigl, J., Koehler, F., & Henning, H. (2024)**. Exploring the accuracy of musical tempo memory: The effects of reproduction method, reference tempo, and musical expertise. *Memory & Cognition, 52*, 1299–1312. (Behavioral online, N=403, adjusting>tapping r=−.26, quadratic 120 BPM χ²(1)=152.57, expertise r=.09, **PRIMARY**)
2. **Foster, N. E. V., Beffa, L., & Lehmann, A. (2021)**. Accuracy of tempo judgments in disk jockeys compared to musicians and untrained individuals. *Frontiers in Psychology, 12*, 709979. (Behavioral lab, N=40, DJs 120-139 BPM error 3.10% vs untrained 7.91%, Group F(3,36)=5.67)
3. **Grahn, J. A., & Brett, M. (2007)**. Rhythm and beat perception in motor areas of the brain. *Journal of Cognitive Neuroscience, 19*(5), 893–906. (fMRI, N=27, putamen Z=5.67, SMA Z=5.03, musicians>non-musicians premotor/cerebellum)
4. **Hoddinott, S., & Grahn, J. A. (2024)**. Who has got rhythm: Individual differences in neural entrainment are enhanced by musical training and predict beat perception accuracy. *NeuroImage*. (7T fMRI RSA, N=24, C-Score beat strength in putamen/SMA, musicians enhanced)
5. **Dalla Bella, S., et al. (2024)**. Unravelling individual rhythmic abilities using machine learning. *Scientific Reports, 14*, 1135. (Behavioral+ML, N=79, musician classification d=1.8, motor d=1.5, perceptual d=1.3, perceptual-motor interaction key)
6. **Okada, K., et al. (2022)**. A three-neuron-type cerebellar timing circuit. *Nature*. (Electrophysiology, 95 neurons, 3 neuron types: bilateral=prediction, unilateral=timing, postsaccade=error, PI t=3.36)

### Tier 2 — Supporting Evidence (in literature collection, reviews/theoretical)

7. **Ross, J. M., & Balasubramaniam, R. (2022)**. Time perception for musical rhythms: Sensorimotor perspectives on entrainment, simulation, and prediction. *Frontiers in Integrative Neuroscience, 16*, 916220. (Review, dual sensory/motor timing framework, SMA critical for internal timing)
8. **Thaut, M. H., et al. (2015)**. Neural basis of rhythmic timing networks in the human brain. *Annals of the New York Academy of Sciences, 1337*, 92–102. (Review, period entrainment theory, BG-SMA-cerebellum circuit)

### Tier 3 — Founding/Historical (cited in Vigl 2024, NOT in collection)

9. **Levitin, D. J., & Cook, P. R. (1996)**. Memory for musical tempo: Additional evidence that auditory memory is absolute. *Perception & Psychophysics, 58*(6), 927–935. (Behavioral, N=46, 72% of sung tempos within ±8% of original; FOUNDING but effect sizes NOT directly replicable at claimed magnitudes)
10. **Drake, C., & Botte, M.-C. (1993)**. Tempo sensitivity in auditory sequences: Evidence for a multiple-look model. *Perception & Psychophysics, 54*(3), 277–286. (Psychophysics, Weber fraction minimum at ~500 ms IOI; FOUNDING)
11. **Jakubowski, K., et al. (2016)**. Probing imagined tempo for music: Effects of motor engagement and musical experience. *Psychology of Music, 44*(6), 1274–1288. (Behavioral, N=25, first adjusting vs tapping comparison; FOUNDING but small sample)
12. **Collier, G. L., & Ogden, J. M. (2004)**. Adding drift to the decomposition of simple isochronous tapping. *Journal of Experimental Psychology: HPP*. (Behavioral, SMT ≈ 120 BPM; cited in code but NOT in literature collection)

### Code Note (Phase 5)

Doc-code mismatches to resolve:
- Code `FULL_NAME = "Tempo Memory Reproduction Matrix"` vs doc "Tempo Memory Reproduction Method"
- Code `MECHANISM_NAMES = ("BEP", "TMH")` vs doc specifies `("BEP",)` only
- Code cites `Leow 2014 + Collier 2004` vs doc cites `Levitin & Cook 1996 + Drake & Botte 1993` (both sets now superseded by Vigl 2024)
- Code `version="2.0.0"`, `paper_count=3` → needs update to `"2.1.0"`, `paper_count=12`

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D): L0, L4, L5, L6, L9, X_L4L5 | R³ (49D): Energy, Change |
| Temporal | HC⁰ mechanisms (PTM, ITM, GRV, HRM) | BEP mechanism (30D) |
| Beat detection | S⁰.L5.spectral_flux[45] × HC⁰.PTM | R³.spectral_flux[10] × BEP.beat_induction |
| Tempo reference | S⁰.L9.mean_T[104] × HC⁰.ITM | R³.loudness[8] periodicity × BEP.meter_extraction |
| Groove pathway | S⁰.L5 × HC⁰.GRV | R³.Change + BEP.motor_entrainment |
| Memory replay | S⁰.L9 × HC⁰.HRM | Removed (BEP subsumes tempo memory) |
| Demand format | HC⁰ index ranges (15/2304 = 0.65%) | H³ 4-tuples (15/2304 = 0.65%) |
| Output dimensions | 12D | **10D** (catalog-specified) |
| Method dissociation | Implicit in X_L4L5 interactions | Explicit via sensory_state vs motor_state |

### Why BEP replaces HC⁰ mechanisms

The D0 pipeline used 4 separate HC⁰ mechanisms (PTM, ITM, GRV, HRM). In MI, these are unified into the BEP mechanism with 3 sub-sections:
- **PTM → BEP.beat_induction** [0:10]: Predictive timing → beat strength, tempo detection
- **ITM → BEP.meter_extraction** [10:20]: Interval timing → meter, accent patterns, optimal tempo zone
- **GRV → BEP.motor_entrainment** [20:30]: Groove processing → motor synchronization, tapping pathway
- **HRM** (Hippocampal Replay): Subsumed by BEP's inherent periodicity tracking — tempo memory is maintained through ongoing beat entrainment rather than episodic replay

### Key Output Changes

D0 had 12D output with separate features for replay and memory. MI reduces to 10D by:
1. Removing explicit replay features (HRM subsumed by BEP periodicity)
2. Consolidating tempo memory into `f02_optimal_tempo` (BEP.meter_extraction periodicity)
3. Adding `reproduction_acc` as an integrated accuracy prediction

---

**Model Status**: **SPECULATIVE** (upgraded evidence: 2→12 papers, 7 methods, 7/9 falsification confirmed; BUT original effect sizes DEFLATED by Vigl 2024 replication)
**Output Dimensions**: **10D**
**Evidence Tier**: **γ (Speculative)** — structure CONFIRMED, magnitudes REVISED downward
**Confidence**: **<70%** (core claims confirmed directionally; quantitative calibration needs updating per Vigl 2024)
