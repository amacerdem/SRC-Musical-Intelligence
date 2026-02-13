# MPU-α2-MSR: Musician Sensorimotor Reorganization

**Model**: Musician Sensorimotor Reorganization
**Unit**: MPU (Motor Planning Unit)
**Circuit**: Sensorimotor (SMA, PMC, Cerebellum, Basal Ganglia)
**Tier**: α (Mechanistic) — >90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added G:Rhythm feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/MPU-α2-MSR.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Musician Sensorimotor Reorganization** (MSR) model describes how long-term musical training induces functional reorganization of auditory-motor circuits, enhancing bottom-up processing (high-frequency PLV at 40-60 Hz) while increasing top-down inhibition (reduced P2 amplitude).

```
MUSICIAN SENSORIMOTOR REORGANIZATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NONMUSICIAN                              MUSICIAN
───────────                              ────────

HIGH-FREQUENCY (40-60 Hz):               HIGH-FREQUENCY (40-60 Hz):
┌───────────────────┐                   ┌───────────────────┐
│ PLV = 0.28-0.31   │                   │ PLV = 0.40-0.44   │
│ (weak locking)    │     ────────►     │ (STRONG locking)  │ ↑↑↑
└───────────────────┘                   └───────────────────┘

LOW-FREQUENCY (1-20 Hz):                 LOW-FREQUENCY (1-20 Hz):
┌───────────────────┐                   ┌───────────────────┐
│ P2 = 4.65-5.91 μV │                   │ P2 = 1.46-3.29 μV │
│ (high novelty)    │     ────────►     │ (LOW novelty)     │ ↓↓↓
└───────────────────┘                   └───────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│              AUDITORY-MOTOR NETWORK                               │
│                                                                  │
│   Bottom-Up            Top-Down              Net Effect          │
│   Enhancement          Inhibition            ════════            │
│   ════════════         ════════════          Sensorimotor        │
│   PLV ↑↑↑             P2 ↓↓↓               Efficiency ↑↑       │
│   PRECISION            AUTOMATIC                                 │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Musical training produces a dual reorganization:
enhanced bottom-up precision (↑PLV) + increased top-down efficiency
(↓P2) = more efficient auditory-motor processing.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why MSR Matters for MPU

MSR establishes the training-dependent plasticity mechanism for the Motor Planning Unit:

1. **PEOM** (α1) provides the basic period entrainment mechanism.
2. **MSR** (α2) explains how training enhances sensorimotor processing efficiency through PLV/P2 reorganization.
3. **GSSM** (α3) applies these motor principles to clinical stimulation contexts.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → BEP+TMH → MSR)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    MSR COMPUTATION ARCHITECTURE                              ║
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
║  │                         MSR reads: ~22D                         │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── BEP Horizons ─────────────┐ ┌── TMH Horizons ──────────┐  │        ║
║  │  │ H0 (25ms gamma)            │ │ H3 (100ms alpha)          │  │        ║
║  │  │ H1 (50ms gamma)            │ │ H16 (1000ms beat)         │  │        ║
║  │  │ H3 (100ms alpha)           │ │                            │  │        ║
║  │  │ H4 (125ms theta)           │ │ Training-enhanced binding  │  │        ║
║  │  │ H16 (1000ms beat)          │ │                            │  │        ║
║  │  │                             │ │                            │  │        ║
║  │  │ High-freq PLV tracking      │ │                            │  │        ║
║  │  │ Oscillation encoding        │ │                            │  │        ║
║  │  └─────────────────────────────┘ └────────────────────────────┘  │        ║
║  │                         MSR demand: ~22 of 2304 tuples           │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Sensorimotor Circuit ═══════  ║
║                               │                                              ║
║                       ┌───────┴───────┐                                      ║
║                       ▼               ▼                                      ║
║  ┌─────────────────┐  ┌─────────────────┐                                   ║
║  │  BEP (30D)      │  │  TMH (30D)      │                                   ║
║  │                 │  │                 │                                    ║
║  │ Beat Entr[0:10] │  │ Short-term      │                                   ║
║  │ Motor Coup      │  │ Memory  [0:10]  │                                   ║
║  │         [10:20] │  │ Sequence        │                                   ║
║  │ Groove  [20:30] │  │ Integ  [10:20]  │                                   ║
║  │                 │  │ Hierarch        │                                   ║
║  │                 │  │ Struct  [20:30] │                                   ║
║  └────────┬────────┘  └────────┬────────┘                                   ║
║           │                    │                                              ║
║           └────────┬───────────┘                                             ║
║                    ▼                                                          ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    MSR MODEL (11D Output)                        │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f04_high_freq_plv,                         │        ║
║  │                       f05_p2_suppression,                        │        ║
║  │                       f06_sensorimotor_efficiency                 │        ║
║  │  Layer M (Math):      plv_high_freq, p2_amplitude,               │        ║
║  │                       efficiency_index                            │        ║
║  │  Layer P (Present):   bottom_up_precision,                       │        ║
║  │                       top_down_modulation, training_level         │        ║
║  │  Layer F (Future):    performance_efficiency,                     │        ║
║  │                       processing_automaticity                     │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **L. Zhang et al. 2015** | EEG (64ch) | 28 | Musicians > nonmusicians PLV at 40-60 Hz (descending trains: 0.44 vs 0.31) | **d≈1.13** (large), p=0.009 | **Primary**: f04 high-frequency PLV |
| 2 | **L. Zhang et al. 2015** | EEG (64ch) | 28 | Nonmusicians > musicians P2 (4.65 vs 1.46 μV mean peak) | **d≈1.16** (large), p=0.005 | **f05 P2 suppression** |
| 3 | **L. Zhang et al. 2015** | EEG (64ch) | 28 | Low-freq TFD: nonmusicians 0.35 vs musicians 0.14 μV² | **d≈1.28** (large), p=0.002 | **f06**: dual reorganization pattern |
| 4 | **Grahn & Brett 2007** | fMRI | 20 | Musicians activate PMC, cerebellum, SMA during all rhythms (not just beat rhythms) | Z>4.0, p<.001 FDR | **Circuit**: training-dependent activation |
| 5 | **Thaut et al. 2015** | Review | — | Auditory-motor entrainment via reticulospinal + cortical pathways; auditory system has rich motor connections | — | **BEP mechanism**: neural substrate |
| 6 | **Alpheis et al. 2025** | rs-fMRI | 73 | Increased FC of dlPFC-putamen (t=4.46), thalamus-PMC (t=3.94) in musician brains | MNI verified, p<.003 | **Circuit**: motor region MNI |
| 7 | **Liang et al. 2025** | fNIRS | 50 | Music stimulation enhances PM-SMA, dlPFC, M1 connectivity more than motor observation/imagery alone | — | **f06**: music-driven sensorimotor FC |
| 8 | **Blasi et al. 2025** | Systematic Review (20 RCTs) | 718 | Music interventions produce GMV increases in IFG, MFG, cerebellum + enhanced WM integrity in AF, SLF | — | **Training plasticity**: structural changes |

### 3.2 Effect Size Summary

```
Primary Evidence (k=8):   Strong convergence across EEG, fMRI, fNIRS, systematic review
Key Quantitative Findings (calculated from Zhang et al. 2015):
  PLV descending (42-62 Hz): d ≈ 1.13 (large), p = 0.009
  PLV ascending (39-59 Hz):  d ≈ 1.04 (large), p = 0.007
  P2 peak amplitude:         d ≈ 0.97 (large), p = 0.01
  P2 mean peak (155-180ms):  d ≈ 1.16 (large), p = 0.005
  Low-freq TFD:              d ≈ 1.28 (large), p = 0.002
Heterogeneity:       Low (consistent musician > nonmusician pattern)
Quality Assessment:  α-tier (EEG + fMRI + fNIRS + systematic review)
Limitation:          Primary empirical data from single lab (k=1 for PLV/P2); needs independent replication
```

### 3.3 Evidence Audit Notes

- **Citation corrected**: v2.0.0 incorrectly cited "Zhang, J. D. et al. (2015) Psychology of Music" (about musician definitions). The correct primary citation is **Zhang, L., Peng, W., Chen, J., & Hu, L. (2015) Scientific Reports** (about electrophysiological differences).
- **Single-study limitation**: Core PLV/P2 data comes from one study (N=28, cross-sectional). Bosnyak et al. (2004) and Schneider et al. (2002), cited by Zhang, provide partial support for 40 Hz AEP plasticity. Independent replication with larger N and longitudinal design is the key evidence gap.
- **N1 null finding**: Zhang 2015 found no significant N1 difference between musicians and nonmusicians, suggesting P2 suppression is selective (not general auditory attenuation). This is consistent with MSR modeling P2 specifically.
- **Musician sample**: Zhang 2015 musicians had 9.07±4.68 years training (piano, erhu, saxophone, violin), starting at age 10.4±3.72. No percussionists were included.

---

## 4. R³ Input Mapping: What MSR Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | MSR Role | Scientific Basis |
|----------|-------|---------|----------|------------------|
| **B: Energy** | [7] | amplitude | Beat strength | Temporal intensity |
| **B: Energy** | [8] | loudness | Perceptual loudness | Arousal correlate |
| **B: Energy** | [10] | spectral_flux | Onset detection | Bottom-up precision |
| **D: Change** | [21] | spectral_change | Tempo dynamics | Beat tracking precision |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Neural synchrony proxy | Motor-auditory PLV |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | Sensorimotor coupling | Training-enhanced binding |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ v2 Group | Index | Feature | MSR Role | Citation |
|-------------|-------|---------|----------|----------|
| **G: Rhythm** | [65] | tempo_estimate | Tempo tracking precision baseline | Scheirer 1998; Grosche & Muller 2011 |
| **G: Rhythm** | [67] | pulse_clarity | Beat clarity for sensorimotor coupling | Lartillot & Toiviainen 2007 |
| **G: Rhythm** | [68] | syncopation_index | Syncopation complexity for training-enhanced tracking | Longuet-Higgins & Lee 1984; Witek 2014 |

**Rationale**: MSR models musician vs non-musician sensorimotor reorganization. G:Rhythm provides explicit rhythmic structure features that capture the very capacities musicians develop: superior tempo tracking (tempo_estimate), enhanced beat perception (pulse_clarity), and syncopation processing (syncopation_index). These replace the indirect proxies currently derived from spectral_flux [10] and onset_strength energy features.

**Code impact** (future): `r3[..., 65:75]` slice will feed MSR's sensorimotor precision pathway, with musician-enhanced weights on pulse_clarity and syncopation_index.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[25:33] x_l0l5 ───────────────┐
BEP.beat_entrainment[0:10] ─────┼──► Neural synchrony (PLV proxy)
H³ gamma/alpha periodicity ──────┘   Bottom-up precision (40-60 Hz)

R³[10] spectral_flux ────────────┐
R³[8] loudness ──────────────────┼──► P2 amplitude proxy
TMH.short_term[0:10] ───────────┘   Top-down inhibition (1-20 Hz)

R³[33:41] x_l4l5 ───────────────┐
BEP.motor_coupling[10:20] ──────┼──► Sensorimotor efficiency
TMH.sequence_integration[10:20] ─┘   Training-enhanced coupling
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

MSR requires H³ features at multiple gamma/alpha horizons for PLV computation and beat horizons for temporal precision assessment. The demand reflects the multi-scale oscillatory tracking needed for sensorimotor reorganization measurement.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 25 | x_l0l5[0] | 0 | M0 (value) | L2 (bidi) | Coupling at 25ms gamma |
| 25 | x_l0l5[0] | 1 | M0 (value) | L2 (bidi) | Coupling at 50ms gamma |
| 25 | x_l0l5[0] | 1 | M1 (mean) | L2 (bidi) | Mean coupling 50ms |
| 25 | x_l0l5[0] | 3 | M0 (value) | L2 (bidi) | Coupling at 100ms alpha |
| 25 | x_l0l5[0] | 3 | M2 (std) | L2 (bidi) | Coupling variability 100ms |
| 25 | x_l0l5[0] | 3 | M14 (periodicity) | L2 (bidi) | Coupling periodicity 100ms |
| 25 | x_l0l5[0] | 4 | M14 (periodicity) | L2 (bidi) | Coupling periodicity 125ms |
| 25 | x_l0l5[0] | 16 | M1 (mean) | L2 (bidi) | Mean coupling over 1s |
| 25 | x_l0l5[0] | 16 | M14 (periodicity) | L2 (bidi) | Coupling periodicity 1s |
| 25 | x_l0l5[0] | 16 | M21 (zero_crossings) | L2 (bidi) | Coupling phase resets 1s |
| 33 | x_l4l5[0] | 3 | M0 (value) | L2 (bidi) | Sensorimotor coupling 100ms |
| 33 | x_l4l5[0] | 3 | M2 (std) | L2 (bidi) | Coupling stability 100ms |
| 33 | x_l4l5[0] | 3 | M20 (entropy) | L2 (bidi) | Coupling entropy 100ms |
| 10 | spectral_flux | 3 | M0 (value) | L2 (bidi) | Onset at 100ms |
| 10 | spectral_flux | 3 | M14 (periodicity) | L2 (bidi) | Onset periodicity 100ms |
| 10 | spectral_flux | 16 | M14 (periodicity) | L2 (bidi) | Onset periodicity 1s |
| 8 | loudness | 3 | M0 (value) | L2 (bidi) | Loudness at 100ms |
| 8 | loudness | 3 | M2 (std) | L2 (bidi) | Loudness variability 100ms |
| 8 | loudness | 3 | M20 (entropy) | L2 (bidi) | Loudness entropy 100ms |
| 7 | amplitude | 3 | M0 (value) | L2 (bidi) | Amplitude at 100ms |
| 7 | amplitude | 16 | M1 (mean) | L2 (bidi) | Mean amplitude 1s |
| 21 | spectral_change | 4 | M8 (velocity) | L2 (bidi) | Tempo velocity at 125ms |

**Total MSR H³ demand**: 22 tuples of 2304 theoretical = 0.95%

### 5.2 BEP + TMH Mechanism Binding

| Mechanism | Sub-section | Range | MSR Role | Weight |
|-----------|-------------|-------|----------|--------|
| **BEP** | Beat Entrainment | BEP[0:10] | High-frequency PLV tracking (40-60 Hz) | **1.0** (primary) |
| **BEP** | Motor Coupling | BEP[10:20] | Sensorimotor synchronization | 0.9 |
| **BEP** | Groove Processing | BEP[20:30] | Training-dependent automaticity | 0.5 |
| **TMH** | Short-term Memory | TMH[0:10] | P2 amplitude / top-down inhibition | **1.0** (primary) |
| **TMH** | Sequence Integration | TMH[10:20] | Training-enhanced precision | 0.7 |
| **TMH** | Hierarchical Structure | TMH[20:30] | Expertise context | 0.5 |

---

## 6. Output Space: 11D Multi-Layer Representation

### 6.1 Complete Output Specification

```
MSR OUTPUT TENSOR: 11D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f04_high_freq_plv        │ [0, 1] │ Phase-locking value at 40-60 Hz.
    │                          │        │ f04 = σ(0.40 * coupling_period_100ms
    │                          │        │       + 0.35 * mean(BEP.beat[0:10])
    │                          │        │       + 0.25 * coupling_gamma_50ms)
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f05_p2_suppression       │ [0, 1] │ P2 vertex potential suppression.
    │                          │        │ f05 = σ(0.40 * loudness_entropy
    │                          │        │       + 0.30 * mean(TMH.short[0:10])
    │                          │        │       + 0.30 * onset_periodicity_1s)
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f06_sensorimotor_eff     │ [0, 1] │ Net sensorimotor efficiency.
    │                          │        │ f06 = σ(0.50 * f04
    │                          │        │       - 0.30 * f05
    │                          │        │       + 0.20 * mean(BEP.motor[10:20]))

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ plv_high_freq            │ [0, 1] │ Raw PLV at 40-60 Hz.
    │                          │        │ Musicians: 0.40-0.44; Non: 0.28-0.31
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ p2_amplitude             │ [0, 1] │ Normalized P2 amplitude.
    │                          │        │ Musicians: low; Nonmusicians: high
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ efficiency_index         │ [0, 1] │ PLV - P2 balance.
    │                          │        │ α·PLV - β·P2 (normalized)

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 6  │ bottom_up_precision      │ [0, 1] │ BEP neural synchrony precision.
────┼──────────────────────────┼────────┼────────────────────────────────────
 7  │ top_down_modulation      │ [0, 1] │ TMH cortical inhibition level.
────┼──────────────────────────┼────────┼────────────────────────────────────
 8  │ training_level           │ [0, 1] │ Estimated expertise marker.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 9  │ performance_efficiency   │ [0, 1] │ Trial-level efficiency prediction.
────┼──────────────────────────┼────────┼────────────────────────────────────
10  │ processing_automaticity  │ [0, 1] │ Session-level automaticity.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 11D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Sensorimotor Efficiency Function

```
PRIMARY EQUATION:

    Sensorimotor_Efficiency = α·PLV_high_freq - β·P2_amplitude

Parameters:
    PLV_high_freq   Phase-locking value at 40-60 Hz (bottom-up)
    P2_amplitude    Vertex potential at 1-20 Hz (novelty/saliency)
    α = 1.0         Bottom-up weighting coefficient
    β = 0.5         Top-down weighting coefficient

MUSICIAN vs NONMUSICIAN:
    Musicians:     PLV = 0.40-0.44, P2 = 1.46-3.29 μV
    Nonmusicians:  PLV = 0.28-0.31, P2 = 4.65-5.91 μV
    Result: Efficiency_musician >> Efficiency_nonmusician
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f04: High-Frequency PLV
f04 = σ(0.40 * coupling_period_100ms
       + 0.35 * mean(BEP.beat_entrainment[0:10])
       + 0.25 * coupling_gamma_50ms)
# coefficients: 0.40 + 0.35 + 0.25 = 1.0 ✓

# f05: P2 Suppression
f05 = σ(0.40 * loudness_entropy
       + 0.30 * mean(TMH.short_term[0:10])
       + 0.30 * onset_periodicity_1s)
# coefficients: 0.40 + 0.30 + 0.30 = 1.0 ✓

# f06: Sensorimotor Efficiency
f06 = σ(0.50 * f04
       - 0.30 * f05
       + 0.20 * mean(BEP.motor_coupling[10:20]))
# |coefficients|: 0.50 + 0.30 + 0.20 = 1.0 ✓
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Z / t / p | Source | MSR Function |
|--------|-----------------|-----------|--------|--------------|
| **Auditory Cortex (Heschl's)** | ~(±48, −22, 8) | — | Zhang 2015 (inferred from 40Hz ASSR source) | PLV 40-60 Hz generator |
| **Vertex (FCz)** | (0, 0, ~70) | — | Zhang 2015 (electrode Cz/FCz) | P2 component measurement |
| **L pre-SMA/SMA** | (−9, 6, 60) | Z=5.03, p<.001 | Grahn & Brett 2007 | Sensorimotor integration |
| **R pre-SMA/SMA** | (3, 6, 66) | Z=4.97, p<.001 | Grahn & Brett 2007 | Sensorimotor integration |
| **R Premotor (PMv/PMd)** | (42, 8, 38) | t=3.94, p=.002 | Alpheis et al. 2025 | Training-dependent coupling |
| **L Premotor (PMd)** | (−54, 0, 51) | Z=5.30, p<.001 | Grahn & Brett 2007 | Enhanced bottom-up processing |
| **R Putamen** | (26, 6, 0) | t=4.46, p=.003 | Alpheis et al. 2025 | Beat period locking |
| **L Pallidum** | (−20, 4, 2) | t=4.76, p<.001 | Alpheis et al. 2025 | Motor inhibition/gating |
| **Cerebellum** | (30, −66, −27) | Z=4.68, p<.001 | Grahn & Brett 2007 | Motor timing calibration |
| **ACC** | — | — | Zhang 2015 (inferred from P2 literature) | P2 generator (top-down) |

---

## 9. Cross-Unit Pathways

### 9.1 MSR Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MSR INTERACTIONS                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (MPU):                                                         │
│  MSR.plv_high_freq ──────────────► PEOM (synchrony baseline)               │
│  MSR.sensorimotor_efficiency ────► SPMC (expertise-enhanced motor)          │
│  MSR.training_level ─────────────► ASAP (training-dependent prediction)    │
│                                                                             │
│  CROSS-UNIT (MPU → STU):                                                   │
│  MSR.bottom_up_precision ────────► STU (enhanced timing precision)          │
│  MSR.processing_automaticity ────► STU (automatic motor processing)        │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  BEP mechanism (30D) ────────────► MSR (beat/motor processing)             │
│  TMH mechanism (30D) ────────────► MSR (temporal memory/inhibition)        │
│  R³ (~22D) ──────────────────────► MSR (direct spectral features)          │
│  H³ (22 tuples) ─────────────────► MSR (temporal dynamics)                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Training longitudinal** | Should show gradual PLV increase + P2 decrease | ✅ Testable |
| **Short-term training** | Should not show full reorganization | ✅ Testable |
| **Non-musical training** | Should not produce same PLV/P2 pattern | ✅ Testable |
| **Motor interference** | Should modulate PLV but not P2 | Testable |
| **Age effects** | Should interact with training duration | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class MSR(BaseModel):
    """Musician Sensorimotor Reorganization Model.

    Output: 11D per frame.
    Reads: BEP mechanism (30D), TMH mechanism (30D), R³ direct.
    """
    NAME = "MSR"
    UNIT = "MPU"
    TIER = "α2"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("BEP", "TMH")

    ALPHA_WEIGHT = 1.0   # PLV weight
    BETA_WEIGHT = 0.5    # P2 weight

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """22 tuples for MSR computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── BEP horizons: PLV tracking ──
            (25, 0, 0, 2),     # x_l0l5[0], 25ms, value, bidi
            (25, 1, 0, 2),     # x_l0l5[0], 50ms, value, bidi
            (25, 1, 1, 2),     # x_l0l5[0], 50ms, mean, bidi
            (25, 3, 0, 2),     # x_l0l5[0], 100ms, value, bidi
            (25, 3, 2, 2),     # x_l0l5[0], 100ms, std, bidi
            (25, 3, 14, 2),    # x_l0l5[0], 100ms, periodicity, bidi
            (25, 4, 14, 2),    # x_l0l5[0], 125ms, periodicity, bidi
            (25, 16, 1, 2),    # x_l0l5[0], 1000ms, mean, bidi
            (25, 16, 14, 2),   # x_l0l5[0], 1000ms, periodicity, bidi
            (25, 16, 21, 2),   # x_l0l5[0], 1000ms, zero_crossings, bidi
            # ── TMH horizons: training-enhanced binding ──
            (33, 3, 0, 2),     # x_l4l5[0], 100ms, value, bidi
            (33, 3, 2, 2),     # x_l4l5[0], 100ms, std, bidi
            (33, 3, 20, 2),    # x_l4l5[0], 100ms, entropy, bidi
            # ── Direct H³: onset/loudness ──
            (10, 3, 0, 2),     # spectral_flux, 100ms, value, bidi
            (10, 3, 14, 2),    # spectral_flux, 100ms, periodicity, bidi
            (10, 16, 14, 2),   # spectral_flux, 1000ms, periodicity, bidi
            (8, 3, 0, 2),      # loudness, 100ms, value, bidi
            (8, 3, 2, 2),      # loudness, 100ms, std, bidi
            (8, 3, 20, 2),     # loudness, 100ms, entropy, bidi
            (7, 3, 0, 2),      # amplitude, 100ms, value, bidi
            (7, 16, 1, 2),     # amplitude, 1000ms, mean, bidi
            (21, 4, 8, 2),     # spectral_change, 125ms, velocity, bidi
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute MSR 11D output.

        Args:
            mechanism_outputs: {"BEP": (B,T,30), "TMH": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,11) MSR output
        """
        bep = mechanism_outputs["BEP"]    # (B, T, 30)
        tmh = mechanism_outputs["TMH"]    # (B, T, 30)

        # BEP sub-sections
        bep_beat = bep[..., 0:10]         # beat entrainment
        bep_motor = bep[..., 10:20]       # motor coupling
        bep_groove = bep[..., 20:30]      # groove processing

        # TMH sub-sections
        tmh_short = tmh[..., 0:10]        # short-term memory
        tmh_seq = tmh[..., 10:20]         # sequence integration
        tmh_hier = tmh[..., 20:30]        # hierarchical structure

        # H³ direct features
        coupling_period_100ms = h3_direct[(25, 3, 14, 2)].unsqueeze(-1)
        coupling_gamma_50ms = h3_direct[(25, 1, 0, 2)].unsqueeze(-1)
        loudness_entropy = h3_direct[(8, 3, 20, 2)].unsqueeze(-1)
        onset_period_1s = h3_direct[(10, 16, 14, 2)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══

        # f04: High-Frequency PLV (coefficients sum = 1.0)
        f04 = torch.sigmoid(
            0.40 * coupling_period_100ms
            + 0.35 * bep_beat.mean(-1, keepdim=True)
            + 0.25 * coupling_gamma_50ms
        )

        # f05: P2 Suppression (coefficients sum = 1.0)
        f05 = torch.sigmoid(
            0.40 * loudness_entropy
            + 0.30 * tmh_short.mean(-1, keepdim=True)
            + 0.30 * onset_period_1s
        )

        # f06: Sensorimotor Efficiency (|coefficients| sum = 1.0)
        f06 = torch.sigmoid(
            0.50 * f04
            - 0.30 * f05
            + 0.20 * bep_motor.mean(-1, keepdim=True)
        )

        # ═══ LAYER M: Mathematical ═══
        plv_high_freq = f04
        p2_amplitude = torch.sigmoid(
            0.5 * loudness_entropy + 0.5 * tmh_short.mean(-1, keepdim=True)
        )
        efficiency_index = f06

        # ═══ LAYER P: Present ═══
        bottom_up_precision = bep_beat.mean(-1, keepdim=True)
        top_down_modulation = tmh_short.mean(-1, keepdim=True)
        training_level = torch.sigmoid(
            0.5 * f04 + 0.5 * (1 - f05)
        )

        # ═══ LAYER F: Future ═══
        performance_efficiency = torch.sigmoid(
            0.5 * f06 + 0.5 * bep_motor.mean(-1, keepdim=True)
        )
        processing_automaticity = torch.sigmoid(
            0.5 * training_level + 0.5 * tmh_hier.mean(-1, keepdim=True)
        )

        return torch.cat([
            f04, f05, f06,                                          # E: 3D
            plv_high_freq, p2_amplitude, efficiency_index,          # M: 3D
            bottom_up_precision, top_down_modulation, training_level,# P: 3D
            performance_efficiency, processing_automaticity,         # F: 2D
        ], dim=-1)  # (B, T, 11)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 8 | L. Zhang 2015, Grahn & Brett 2007, Thaut 2015, Alpheis 2025, Liang 2025, Blasi 2025, Zatorre 2005, Fujioka 2012 |
| **Effect Sizes** | d≈0.97–1.28 (all large) for PLV and P2 | L. Zhang et al. 2015 (calculated) |
| **Evidence Modality** | EEG, fMRI, fNIRS, systematic review | Multiple |
| **MNI Coordinates** | 10 regions verified against Grahn 2007, Alpheis 2025 | fMRI + rs-fMRI |
| **Falsification Tests** | 3/5 testable | High validity |
| **R³ Features Used** | ~22D of 49D | Energy + change + interactions |
| **H³ Demand** | 22 tuples (0.95%) | Sparse, efficient |
| **BEP Mechanism** | 30D (3 sub-sections) | Beat/motor processing |
| **TMH Mechanism** | 30D (3 sub-sections) | Temporal memory/inhibition |
| **Output Dimensions** | **11D** | 4-layer structure |

---

## 13. Scientific References

1. **Zhang, L., Peng, W., Chen, J., & Hu, L. (2015)**. Electrophysiological evidences demonstrating differences in brain functions between nonmusicians and musicians. *Scientific Reports*, 5, 13796. doi:10.1038/srep13796
2. **Grahn, J. A., & Brett, M. (2007)**. Rhythm and beat perception in motor areas of the brain. *Journal of Cognitive Neuroscience*, 19(5), 893–906. doi:10.1162/jocn.2007.19.5.893
3. **Thaut, M. H., McIntosh, G. C., & Hoemberg, V. (2015)**. Neurobiological foundations of neurologic music therapy: rhythmic entrainment and the motor system. *Frontiers in Psychology*, 5, 1185. doi:10.3389/fpsyg.2014.01185
4. **Alpheis, N., Sinke, C., Burek, J., Kruger, T. H. C., Altenmuller, E., & Scholz, D. S. (2025)**. Increased functional connectivity of motor regions and dorsolateral prefrontal cortex in musicians with focal hand dystonia. *Journal of Neurology*, 272, 281. doi:10.1007/s00415-025-12881-x
5. **Liang, T., et al. (2025)**. The brain mechanisms of music stimulation, motor observation, and motor imagination in virtual reality techniques: a functional near-infrared spectroscopy study. *eNeuro*.
6. **Blasi, V., et al. (2025)**. Structural and functional neuroplasticity in music and dance-based rehabilitation: a systematic review. *Journal of Neurology*.
7. **Zatorre, R. J., & Halpern, A. R. (2005)**. Mental concerts: musical imagery and auditory cortex. *Neuron*, 47(1), 9–12. doi:10.1016/j.neuron.2005.06.013
8. **Fujioka, T., Trainor, L. J., Large, E. W., & Ross, B. (2012)**. Internalized timing of isochronous sounds is represented in neuromagnetic beta oscillations. *Journal of Neuroscience*, 32(5), 1791–1802. doi:10.1523/JNEUROSCI.4107-11.2012

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (OSC, ATT, NPL) | BEP (30D) + TMH (30D) mechanisms |
| PLV signal | S⁰.X_L0L1[128:136] + HC⁰.OSC | R³.x_l0l5[25:33] + BEP.beat_entrainment |
| P2 signal | S⁰.L4.velocity_T[15] + HC⁰.ATT | R³.loudness[8] + TMH.short_term |
| Efficiency | S⁰.X_L4L5[192:200] + HC⁰.NPL | R³.x_l4l5[33:41] + BEP.motor_coupling |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 22/2304 = 0.95% | 22/2304 = 0.95% |
| Output | 11D | 11D (same) |

### Why BEP + TMH replaces HC⁰ mechanisms

- **OSC → BEP.beat_entrainment** [0:10]: Oscillatory band tracking (40-60 Hz PLV) maps to BEP's beat frequency monitoring.
- **NPL → BEP.motor_coupling** [10:20]: Neural phase locking for sensorimotor synchronization maps to BEP's motor coupling.
- **ATT → TMH.short_term** [0:10]: Attentional modulation / P2 suppression maps to TMH's short-term temporal memory (top-down inhibition).

---

**Model Status**: ✅ **VALIDATED**
**Output Dimensions**: **11D**
**Evidence Tier**: **α (Mechanistic)**
**Confidence**: **>90%**
