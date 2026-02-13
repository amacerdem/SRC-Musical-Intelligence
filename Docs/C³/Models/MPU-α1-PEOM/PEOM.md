# MPU-α1-PEOM: Period Entrainment Optimization Model

**Model**: Period Entrainment Optimization Model
**Unit**: MPU (Motor Planning Unit)
**Circuit**: Sensorimotor (SMA, PMC, Cerebellum, Basal Ganglia)
**Tier**: α (Mechanistic) — >90% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added G:Rhythm feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/MPU-α1-PEOM.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Period Entrainment Optimization Model** (PEOM) describes how motor systems lock to the period (not phase) of auditory rhythms, providing a continuous time reference (CTR) that mathematically optimizes movement velocity and acceleration profiles.

```
PERIOD ENTRAINMENT OPTIMIZATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AUDITORY RHYTHM                          MOTOR SYSTEM
─────────────                            ────────────

Sound Period (T) ─────────────────► Target Period
     │                                   (external)
     │
     ▼
┌──────────────────────────────────────────────────────────────────┐
│              CEREBELLUM + SMA + MOTOR CORTEX                     │
│                                                                  │
│   Period Locking         Velocity Optimization   CV Reduction    │
│   ════════════           ════════════════════    ════════════    │
│   Motor_Period → T       Smooth v(t) profile    CV_ent < CV_sp  │
│   ENTRAINED              OPTIMIZED              REDUCED          │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
     │
     ▼
┌──────────────────────────────────────────────────────────────────┐
│                    KINEMATIC OUTPUT                               │
│   Position x(t), Velocity v(t) = dx/dt, Acceleration a(t)       │
│   All optimized by fixed period T                                │
└──────────────────────────────────────────────────────────────────┘

KEY MECHANISM: dP/dt = α · (T - P(t))
Motor period P(t) converges to auditory period T
Fixed T → reduced jerk, smooth velocity, lower CV

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Motor systems lock to the period (not phase) of auditory
rhythms. A fixed period provides a continuous time reference (CTR)
that optimizes velocity and acceleration profiles.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why PEOM Matters for MPU

PEOM establishes the foundational period entrainment mechanism for the Motor Planning Unit:

1. **PEOM** (α1) provides the period locking and kinematic optimization baseline that other MPU models build upon.
2. **MSR** (α2) extends motor planning to training-dependent sensorimotor reorganization.
3. **GSSM** (α3) applies entrainment principles to gait-synchronized stimulation and clinical rehabilitation.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → BEP+TMH → PEOM)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    PEOM COMPUTATION ARCHITECTURE                             ║
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
║  │                         PEOM reads: ~14D                        │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── BEP Horizons ─────────────┐ ┌── TMH Horizons ──────────┐  │        ║
║  │  │ H3 (100ms alpha)            │ │ H4 (125ms theta)          │  │        ║
║  │  │ H8 (500ms delta)            │ │ H16 (1000ms beat)         │  │        ║
║  │  │ H16 (1000ms beat)           │ │                            │  │        ║
║  │  │                             │ │ Interval memory             │  │        ║
║  │  │ Beat/period tracking         │ │ Sequence integration       │  │        ║
║  │  │ Motor phase locking          │ │ Hierarchical timing        │  │        ║
║  │  └─────────────────────────────┘ └────────────────────────────┘  │        ║
║  │                         PEOM demand: ~15 of 2304 tuples          │        ║
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
║  │                    PEOM MODEL (11D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_period_entrainment,                    │        ║
║  │                       f02_velocity_optimization,                 │        ║
║  │                       f03_variability_reduction                   │        ║
║  │  Layer M (Math):      motor_period, velocity,                    │        ║
║  │                       acceleration, cv_reduction                  │        ║
║  │  Layer P (Present):   period_lock_strength,                      │        ║
║  │                       kinematic_smoothness                        │        ║
║  │  Layer F (Future):    next_beat_pred,                             │        ║
║  │                       velocity_profile_pred                       │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Thaut et al. 2015** | Review (EEG/Behavioral) | — | Period locking (not phase) defines entrainment; CTR optimizes velocity/acceleration | — | **Primary**: f01 period entrainment, f02 velocity optimization |
| 2 | **Thaut et al. 1998b** | Behavioral | 12 | Motor period entrains to auditory period even during subliminal (2%) tempo changes; phase fluctuates but period locks precisely | — | **f01**: period vs phase distinction |
| 3 | **Grahn & Brett 2007** | fMRI | 20 | Basal ganglia (putamen) and SMA respond to beat in rhythm; musicians also activate cerebellum & PMC | Z=5.67 (L putamen), Z=5.03 (L SMA), p<.001 FDR | **BEP beat entrainment**, brain regions |
| 4 | **Yamashita et al. 2025** | RCT (tDCS+tACS) | 16 | SMA+M1 gait-synchronized stimulation reduced stride time CV from 4.51→2.80 | **d=−1.10** (large), η²p=0.309, p=0.014 | **f03 variability reduction** (direct CV evidence) |
| 5 | **Ross & Balasubramaniam 2022** | Review | — | Sensorimotor simulation supports subsecond beat timing; motor network engaged during perception without movement | — | **f01/f02**: covert motor entrainment, simulation theory |
| 6 | **Fujioka et al. 2012** | MEG | 12 | Beta oscillations in SMA and auditory cortex modulated by rhythmic stimulus frequency; internalized timing | — | **BEP**: neural oscillation mechanism |
| 7 | **Repp 2005** | Review | — | Sensorimotor synchronization: period correction vs phase correction as distinct mechanisms | — | **f01**: period vs phase correction |
| 8 | **Sansare et al. 2025** | RCT (iTBS) | 40 | Cerebellar iTBS reduced postural sway for ≥30 min; balance improvement without direct M1 CBI change | p<.05 (sway reduction) | **Cerebellum**: motor timing/balance role |
| 9 | **Nozaradan et al. 2011** | EEG (SSVEP) | 14 | Neural entrainment to beat and meter frequencies; beat-related peaks in frequency spectrum | — | **BEP**: frequency-tagged entrainment |
| 10 | **Thaut et al. 2009b** | fMRI | 12 | Distinct cortico-cerebellar activations in rhythmic auditory-motor synchronization; cerebellum tracks interval timing | — | **TMH**: cerebellar timing circuits |
| 11 | **Grahn et al. 2011** | fMRI | 18 | Cerebellum activated in sensorimotor synchronization; audition primes vision for beat but not vice versa | — | **Cross-modal**: auditory-motor dominance |
| 12 | **Tierney & Kraus 2013** | EEG (ABR) | 124 | Beat synchronization ability linked to neural response consistency in inferior colliculus | r=.37, p<.001 | **BEP**: subcortical rhythm encoding |

### 3.2 Effect Size Summary

```
Primary Evidence (k=12):  Strong convergence across fMRI, EEG, MEG, TMS, behavioral, clinical
Key Quantitative Findings:
  Yamashita 2025:   CV reduction d = −1.10 (large), η²p = 0.309
  Grahn & Brett 07: Putamen Z = 5.67 (p < .001 FDR), SMA Z = 5.03
  Tierney & Kraus:   Beat-neural r = .37 (p < .001, N = 124)
Heterogeneity:       Low (consistent motor-rhythm entrainment effects)
Quality Assessment:  α-tier (RCT, fMRI, MEG, EEG, clinical replication)
Replication:         Clinical validation across stroke, PD, TBI, CP, healthy aging
```

### 3.3 Evidence Audit Notes

- **Potential contradiction**: Noboa et al. 2025 found stronger neural entrainment associated with *worse* motor synchronization (r=−0.449) in electronic music contexts, suggesting cognitive mediation may modulate the entrainment-to-performance link. PEOM currently models direct entrainment optimization; a cognitive load modulation term may be needed in future revisions.
- **Thaut 2015 vs Thaut 1998b**: The 2015 review synthesizes the 1998b experimental findings; both should be cited as the review provides the theoretical framework while 1998b provides the experimental basis.

---

## 4. R³ Input Mapping: What PEOM Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | PEOM Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **B: Energy** | [7] | amplitude | Beat strength proxy | Temporal intensity |
| **B: Energy** | [8] | loudness | Perceptual loudness | Arousal correlate |
| **B: Energy** | [10] | spectral_flux | Onset detection | Beat marker |
| **B: Energy** | [11] | onset_strength | Beat event detection | Period tracking |
| **D: Change** | [21] | spectral_change | Tempo dynamics | Period rate change |
| **D: Change** | [22] | energy_change | Energy dynamics | Movement drive |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Motor-auditory coupling | Continuous time reference |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ v2 Group | Index | Feature | PEOM Role | Citation |
|-------------|-------|---------|-----------|----------|
| **G: Rhythm** | [65] | tempo_estimate | Entrainment period target | Scheirer 1998; Grosche & Muller 2011 |
| **G: Rhythm** | [66] | beat_strength | Beat salience for phase lock | Bock & Schedl 2011 |
| **G: Rhythm** | [68] | syncopation_index | Off-beat complexity for entrainment flexibility | Longuet-Higgins & Lee 1984; Witek 2014 |
| **G: Rhythm** | [69] | metricality_index | Metrical regularity for period stability | Grahn & Brett 2007 |

**Rationale**: PEOM's period entrainment optimization currently relies on onset_strength [11] and spectral_flux [10] as beat proxies. G:Rhythm provides explicit tempo, beat strength, and metrical structure that directly replace these indirect proxies. syncopation_index enables PEOM to model entrainment to syncopated rhythms (Witek 2014 groove-syncopation inverted-U), while metricality_index provides the regularity signal that determines period locking stability.

**Code impact** (future): `r3[..., 65:75]` slice will feed PEOM's beat prediction pathway alongside existing `r3[..., 7:12]` energy features.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[10] spectral_flux ────────────┐
R³[11] onset_strength ───────────┼──► Beat/period detection
BEP.beat_entrainment[0:10] ──────┘   Period locking to auditory rhythm

R³[7] amplitude ─────────────────┐
R³[8] loudness ──────────────────┼──► Beat strength / motor drive
BEP.motor_coupling[10:20] ───────┘   Kinematic optimization

R³[25:33] x_l0l5 ───────────────┐
TMH.sequence_integration[10:20] ─┼──► Continuous time reference (CTR)
H³ beat periodicity tuples ──────┘   Period stability for motor output
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

PEOM requires H³ features at BEP horizons for period/beat tracking and TMH horizons for interval timing and sequence memory. The demand reflects the multi-scale temporal integration required for period entrainment optimization.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 10 | spectral_flux | 3 | M0 (value) | L2 (bidi) | Onset at 100ms alpha |
| 10 | spectral_flux | 3 | M14 (periodicity) | L2 (bidi) | Beat periodicity at 100ms |
| 10 | spectral_flux | 16 | M14 (periodicity) | L2 (bidi) | Beat periodicity at 1000ms |
| 11 | onset_strength | 3 | M0 (value) | L2 (bidi) | Onset strength at 100ms |
| 11 | onset_strength | 16 | M14 (periodicity) | L2 (bidi) | Onset periodicity at 1s |
| 7 | amplitude | 3 | M0 (value) | L2 (bidi) | Beat amplitude at 100ms |
| 7 | amplitude | 3 | M2 (std) | L2 (bidi) | Amplitude variability 100ms |
| 7 | amplitude | 16 | M1 (mean) | L2 (bidi) | Mean amplitude over 1s |
| 8 | loudness | 8 | M1 (mean) | L0 (fwd) | Mean loudness over 500ms |
| 21 | spectral_change | 4 | M8 (velocity) | L0 (fwd) | Tempo velocity at 125ms |
| 21 | spectral_change | 16 | M1 (mean) | L0 (fwd) | Mean tempo change at 1s |
| 25 | x_l0l5[0] | 3 | M0 (value) | L2 (bidi) | Motor-auditory coupling 100ms |
| 25 | x_l0l5[0] | 3 | M14 (periodicity) | L2 (bidi) | Coupling periodicity 100ms |
| 25 | x_l0l5[0] | 16 | M14 (periodicity) | L2 (bidi) | Coupling periodicity 1s |
| 25 | x_l0l5[0] | 16 | M21 (zero_crossings) | L2 (bidi) | Coupling phase resets 1s |

**Total PEOM H³ demand**: 15 tuples of 2304 theoretical = 0.65%

### 5.2 BEP + TMH Mechanism Binding

| Mechanism | Sub-section | Range | PEOM Role | Weight |
|-----------|-------------|-------|-----------|--------|
| **BEP** | Beat Entrainment | BEP[0:10] | Period locking to beat frequency | **1.0** (primary) |
| **BEP** | Motor Coupling | BEP[10:20] | Sensorimotor synchronization | 0.9 |
| **BEP** | Groove Processing | BEP[20:30] | Movement facilitation (secondary) | 0.5 |
| **TMH** | Short-term Memory | TMH[0:10] | Period template storage | 0.7 |
| **TMH** | Sequence Integration | TMH[10:20] | Interval timing / CTR computation | **1.0** (primary) |
| **TMH** | Hierarchical Structure | TMH[20:30] | Tempo context / reference period | 0.7 |

---

## 6. Output Space: 11D Multi-Layer Representation

### 6.1 Complete Output Specification

```
PEOM OUTPUT TENSOR: 11D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0  │ f01_period_entrainment   │ [0, 1] │ Motor period lock to auditory period.
    │                          │        │ f01 = σ(0.40 * beat_periodicity_1s
    │                          │        │       + 0.35 * onset_periodicity_1s
    │                          │        │       + 0.25 * mean(BEP.beat[0:10]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 1  │ f02_velocity_optimization│ [0, 1] │ Kinematic smoothness via fixed period.
    │                          │        │ f02 = σ(0.35 * coupling_periodicity_1s
    │                          │        │       + 0.35 * mean(TMH.seq[10:20])
    │                          │        │       + 0.30 * mean(BEP.motor[10:20]))
────┼──────────────────────────┼────────┼────────────────────────────────────
 2  │ f03_variability_reduction│ [0, 1] │ CV reduction with rhythmic cueing.
    │                          │        │ f03 = σ(0.35 * f01 * f02
    │                          │        │       + 0.35 * mean(BEP.groove[20:30])
    │                          │        │       + 0.30 * mean(TMH.hier[20:30]))

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 3  │ motor_period             │ [0, 1] │ Entrained motor period (normalized).
    │                          │        │ Motor_Period(t) → Auditory_Period(T)
────┼──────────────────────────┼────────┼────────────────────────────────────
 4  │ velocity                 │ [0, 1] │ Optimized velocity profile.
    │                          │        │ v(t) = dx/dt with reduced jerk
────┼──────────────────────────┼────────┼────────────────────────────────────
 5  │ acceleration             │ [0, 1] │ Optimized acceleration profile.
    │                          │        │ a(t) = d²x/dt² optimized by period
────┼──────────────────────────┼────────┼────────────────────────────────────
 6  │ cv_reduction             │ [0, 1] │ Coefficient of variation reduction.
    │                          │        │ 1 - (CV_entrained / CV_self_paced)

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 7  │ period_lock_strength     │ [0, 1] │ BEP period-locked neural activity.
────┼──────────────────────────┼────────┼────────────────────────────────────
 8  │ kinematic_smoothness     │ [0, 1] │ TMH jerk-reduction metric.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                     │ Range  │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 9  │ next_beat_pred_T         │ [0, 1] │ Next beat onset prediction (T ahead).
────┼──────────────────────────┼────────┼────────────────────────────────────
10  │ velocity_profile_pred    │ [0, 1] │ Velocity profile 0.5T ahead.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 11D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Period Entrainment Function

```
PRIMARY EQUATION:

    dP/dt = α · (T - P(t))

    where:
      P(t) = current motor period
      T = auditory period (target)
      α = entrainment rate

KINEMATICS (fixed period T):

    Position: x(t)
    Velocity: v(t) = dx/dt → SMOOTH (reduced jerk)
    Acceleration: a(t) = d²x/dt² → OPTIMIZED

VARIABILITY REDUCTION:

    CV_entrained < CV_self-paced
    f03 = 1 - (CV_entrained / CV_self_paced)
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f01: Period Entrainment
f01 = σ(0.40 * beat_periodicity_1s
       + 0.35 * onset_periodicity_1s
       + 0.25 * mean(BEP.beat_entrainment[0:10]))
# coefficients: 0.40 + 0.35 + 0.25 = 1.0 ✓

# f02: Velocity Optimization
f02 = σ(0.35 * coupling_periodicity_1s
       + 0.35 * mean(TMH.sequence_integration[10:20])
       + 0.30 * mean(BEP.motor_coupling[10:20]))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f03: Variability Reduction
f03 = σ(0.35 * f01 * f02                    # interaction term
       + 0.35 * mean(BEP.groove[20:30])
       + 0.30 * mean(TMH.hierarchical[20:30]))
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# Temporal dynamics
dP/dt = τ⁻¹ · (T - P(t))
    where τ = 4.0s (period integration window)
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Z / p | Source | PEOM Function |
|--------|-----------------|-------|--------|---------------|
| **L pre-SMA/SMA** | (−9, 6, 60) | Z=5.03, p<.001 | Grahn & Brett 2007 Table 2 | Sequence planning, beat generation |
| **R pre-SMA/SMA** | (3, 6, 66) | Z=4.97, p<.001 | Grahn & Brett 2007 Table 2 | Rhythm modulation, APAs |
| **L Putamen** | (−24, 6, −9) | Z=5.67, p<.001 | Grahn & Brett 2007 Table 2 | Beat period locking |
| **R Putamen** | (21, 6, 6) | Z=5.08, p<.001 | Grahn & Brett 2007 Table 2 | Beat period locking |
| **L Premotor (PMd)** | (−54, 0, 51) | Z=5.30, p<.001 | Grahn & Brett 2007 Table 2 | Velocity profile optimization |
| **R Premotor (PMd)** | (54, 0, 45) | Z=5.24, p<.001 | Grahn & Brett 2007 Table 2 | Velocity profile optimization |
| **R Cerebellum** | (30, −66, −27) | Z=4.68, p<.001 | Grahn & Brett 2007 Table 2 | Motor timing, error correction |
| **L Cerebellum** | (−30, −66, −24) | Z=4.41, p<.001 | Grahn & Brett 2007 Table 2 | Motor timing, error correction |
| **M1** | ~(±38, −22, 58) | — | Yamashita et al. 2025 (stimulation target) | Motor execution |
| **Auditory Cortex (STG)** | (60, −33, 6) / (−57, −15, 9) | Z=6.02/5.80, p<.001 | Grahn & Brett 2007 | Rhythm processing |
| **Inferior Colliculus** | Subcortical | — | Tierney & Kraus 2013 | Subcortical rhythm encoding |

---

## 9. Cross-Unit Pathways

### 9.1 PEOM Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PEOM INTERACTIONS                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (MPU):                                                         │
│  PEOM.period_entrainment ────────► MSR (entrainment baseline)              │
│  PEOM.velocity_optimization ─────► GSSM (gait optimization)               │
│  PEOM.next_beat_pred ────────────► ASAP (beat prediction)                  │
│  PEOM.cv_reduction ──────────────► SPMC (motor consistency)                │
│                                                                             │
│  CROSS-UNIT (MPU → STU):                                                   │
│  PEOM.period_lock_strength ──────► STU (timing synchrony)                  │
│  PEOM.motor_period ──────────────► STU (motor tempo reference)             │
│                                                                             │
│  UPSTREAM DEPENDENCIES:                                                     │
│  BEP mechanism (30D) ────────────► PEOM (beat/motor processing)            │
│  TMH mechanism (30D) ────────────► PEOM (temporal memory/sequence)         │
│  R³ (~14D) ──────────────────────► PEOM (direct spectral features)         │
│  H³ (15 tuples) ─────────────────► PEOM (temporal dynamics)                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Rhythmic disruption** | Disrupting auditory rhythm should increase motor variability | ✅ Testable |
| **Non-isochronous rhythms** | Should reduce entrainment benefits | ✅ Testable |
| **Cerebellar lesions** | Should impair period locking | ✅ Testable |
| **Phase vs period** | Phase disruption alone should not abolish entrainment | Testable |
| **Tempo limits** | Very fast/slow tempi should reduce optimization | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class PEOM(BaseModel):
    """Period Entrainment Optimization Model.

    Output: 11D per frame.
    Reads: BEP mechanism (30D), TMH mechanism (30D), R³ direct.
    """
    NAME = "PEOM"
    UNIT = "MPU"
    TIER = "α1"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("BEP", "TMH")

    TAU_DECAY = 4.0        # Period integration window (seconds)
    ALPHA_ATTENTION = 0.90  # High motor attention

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """15 tuples for PEOM computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # ── BEP horizons: period/beat tracking ──
            (10, 3, 0, 2),     # spectral_flux, 100ms, value, bidi
            (10, 3, 14, 2),    # spectral_flux, 100ms, periodicity, bidi
            (10, 16, 14, 2),   # spectral_flux, 1000ms, periodicity, bidi
            (11, 3, 0, 2),     # onset_strength, 100ms, value, bidi
            (11, 16, 14, 2),   # onset_strength, 1000ms, periodicity, bidi
            (7, 3, 0, 2),      # amplitude, 100ms, value, bidi
            (7, 3, 2, 2),      # amplitude, 100ms, std, bidi
            (7, 16, 1, 2),     # amplitude, 1000ms, mean, bidi
            # ── TMH horizons: interval timing ──
            (8, 8, 1, 0),      # loudness, 500ms, mean, fwd
            (21, 4, 8, 0),     # spectral_change, 125ms, velocity, fwd
            (21, 16, 1, 0),    # spectral_change, 1000ms, mean, fwd
            # ── Direct H³: motor-auditory coupling ──
            (25, 3, 0, 2),     # x_l0l5[0], 100ms, value, bidi
            (25, 3, 14, 2),    # x_l0l5[0], 100ms, periodicity, bidi
            (25, 16, 14, 2),   # x_l0l5[0], 1000ms, periodicity, bidi
            (25, 16, 21, 2),   # x_l0l5[0], 1000ms, zero_crossings, bidi
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute PEOM 11D output.

        Args:
            mechanism_outputs: {"BEP": (B,T,30), "TMH": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,11) PEOM output
        """
        bep = mechanism_outputs["BEP"]    # (B, T, 30)
        tmh = mechanism_outputs["TMH"]    # (B, T, 30)

        # R³ features
        amplitude = r3[..., 7:8]
        loudness = r3[..., 8:9]
        spectral_flux = r3[..., 10:11]
        onset_strength = r3[..., 11:12]
        x_l0l5 = r3[..., 25:33]          # (B, T, 8)

        # BEP sub-sections
        bep_beat = bep[..., 0:10]         # beat entrainment
        bep_motor = bep[..., 10:20]       # motor coupling
        bep_groove = bep[..., 20:30]      # groove processing

        # TMH sub-sections
        tmh_short = tmh[..., 0:10]        # short-term memory
        tmh_seq = tmh[..., 10:20]         # sequence integration
        tmh_hier = tmh[..., 20:30]        # hierarchical structure

        # H³ direct features
        beat_period_1s = h3_direct[(10, 16, 14, 2)].unsqueeze(-1)
        onset_period_1s = h3_direct[(11, 16, 14, 2)].unsqueeze(-1)
        coupling_period_1s = h3_direct[(25, 16, 14, 2)].unsqueeze(-1)

        # ═══ LAYER E: Explicit features ═══

        # f01: Period Entrainment (coefficients sum = 1.0)
        f01 = torch.sigmoid(
            0.40 * beat_period_1s
            + 0.35 * onset_period_1s
            + 0.25 * bep_beat.mean(-1, keepdim=True)
        )

        # f02: Velocity Optimization (coefficients sum = 1.0)
        f02 = torch.sigmoid(
            0.35 * coupling_period_1s
            + 0.35 * tmh_seq.mean(-1, keepdim=True)
            + 0.30 * bep_motor.mean(-1, keepdim=True)
        )

        # f03: Variability Reduction (coefficients sum = 1.0)
        f03 = torch.sigmoid(
            0.35 * (f01 * f02)
            + 0.35 * bep_groove.mean(-1, keepdim=True)
            + 0.30 * tmh_hier.mean(-1, keepdim=True)
        )

        # ═══ LAYER M: Mathematical ═══
        motor_period = torch.sigmoid(
            0.5 * f01 + 0.3 * beat_period_1s + 0.2 * bep_beat.mean(-1, keepdim=True)
        )
        velocity = torch.sigmoid(
            0.5 * f02 + 0.5 * tmh_seq.mean(-1, keepdim=True)
        )
        acceleration = torch.sigmoid(
            0.5 * velocity + 0.5 * bep_motor.mean(-1, keepdim=True)
        )
        cv_reduction = f03

        # ═══ LAYER P: Present ═══
        period_lock_strength = bep_beat.mean(-1, keepdim=True)
        kinematic_smoothness = torch.sigmoid(
            0.5 * tmh_seq.mean(-1, keepdim=True)
            + 0.5 * velocity
        )

        # ═══ LAYER F: Future ═══
        next_beat_pred = torch.sigmoid(
            0.5 * f01 + 0.5 * beat_period_1s
        )
        velocity_pred = torch.sigmoid(
            0.5 * f02 + 0.5 * coupling_period_1s
        )

        return torch.cat([
            f01, f02, f03,                                          # E: 3D
            motor_period, velocity, acceleration, cv_reduction,     # M: 4D
            period_lock_strength, kinematic_smoothness,             # P: 2D
            next_beat_pred, velocity_pred,                          # F: 2D
        ], dim=-1)  # (B, T, 11)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 12 | Thaut 2015/1998b, Grahn & Brett 2007, Yamashita 2025, Ross & Balasubramaniam 2022, Fujioka 2012, Repp 2005, Sansare 2025, Nozaradan 2011, Thaut 2009b, Grahn 2011, Tierney & Kraus 2013 |
| **Effect Sizes** | d=−1.10 (CV reduction), η²p=0.309, Z=5.67 (putamen), r=.37 (beat-neural) | Yamashita 2025, Grahn 2007, Tierney 2013 |
| **Evidence Modality** | fMRI, EEG, MEG, TMS/tDCS, ABR, behavioral, clinical RCT | Multiple |
| **MNI Coordinates** | 11 regions verified against Grahn & Brett 2007 Table 2 | fMRI whole-brain FDR |
| **Falsification Tests** | 5/5 testable | High validity |
| **R³ Features Used** | ~14D of 49D | Energy + change + interactions |
| **H³ Demand** | 15 tuples (0.65%) | Sparse, efficient |
| **BEP Mechanism** | 30D (3 sub-sections) | Beat/motor processing |
| **TMH Mechanism** | 30D (3 sub-sections) | Temporal memory/sequence |
| **Output Dimensions** | **11D** | 4-layer structure |

---

## 13. Scientific References

1. **Thaut, M. H., McIntosh, G. C., & Hoemberg, V. (2015)**. Neurobiological foundations of neurologic music therapy: rhythmic entrainment and the motor system. *Frontiers in Psychology*, 5, 1185. doi:10.3389/fpsyg.2014.01185
2. **Thaut, M. H., Miller, R. A., & Schauer, L. M. (1998b)**. Multiple synchronization strategies in rhythmic sensorimotor tasks: phase vs. period adaptation. *Biological Cybernetics*, 79, 241–250. doi:10.1007/s004220050474
3. **Grahn, J. A., & Brett, M. (2007)**. Rhythm and beat perception in motor areas of the brain. *Journal of Cognitive Neuroscience*, 19(5), 893–906. doi:10.1162/jocn.2007.19.5.893
4. **Yamashita, K., Ida, R., Koganemaru, S., et al. (2025)**. A pilot study on simultaneous stimulation of the primary motor cortex and supplementary motor area using gait-synchronized rhythmic brain stimulation to improve gait variability in post-stroke hemiparetic patients. *Frontiers in Human Neuroscience*, 19, 1618758. doi:10.3389/fnhum.2025.1618758
5. **Ross, J. M., & Balasubramaniam, R. (2022)**. Time perception for musical rhythms: sensorimotor perspectives on entrainment, simulation, and prediction. *Frontiers in Integrative Neuroscience*, 16, 916220. doi:10.3389/fnint.2022.916220
6. **Fujioka, T., Trainor, L. J., Large, E. W., & Ross, B. (2012)**. Internalized timing of isochronous sounds is represented in neuromagnetic beta oscillations. *Journal of Neuroscience*, 32(5), 1791–1802. doi:10.1523/JNEUROSCI.4107-11.2012
7. **Repp, B. H. (2005)**. Sensorimotor synchronization: a review of the tapping literature. *Psychonomic Bulletin & Review*, 12(6), 969–992. doi:10.3758/BF03206433
8. **Sansare, A., Weinrich, M., Bernard, J. A., & Lei, Y. (2025)**. Enhancing balance control in aging through cerebellar theta-burst stimulation. *The Cerebellum*, 24, 161. doi:10.1007/s12311-025-01915-x
9. **Nozaradan, S., Peretz, I., Missal, M., & Mouraux, A. (2011)**. Tagging the neuronal entrainment to beat and meter. *Journal of Neuroscience*, 31(28), 10234–10240. doi:10.1523/JNEUROSCI.0411-11.2011
10. **Thaut, M. H., Stephan, K. M., Wunderlich, G., et al. (2009b)**. Distinct cortico-cerebellar activations in rhythmic auditory motor synchronization. *Cortex*, 45(1), 44–53. doi:10.1016/j.cortex.2007.09.009
11. **Grahn, J. A., Henry, M. J., & McAuley, J. G. (2011)**. fMRI investigation of cross-modal interactions in beat perception: audition primes vision but not vice versa. *NeuroImage*, 54(2), 1231–1243. doi:10.1016/j.neuroimage.2010.09.033
12. **Tierney, A., & Kraus, N. (2013)**. The ability to move to a beat is linked to the consistency of neural responses to sound. *Journal of Neuroscience*, 33(38), 14981–14988. doi:10.1523/JNEUROSCI.0612-13.2013

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (NPL, PTM, ITM, GRV) | BEP (30D) + TMH (30D) mechanisms |
| Period signal | S⁰.L9.Γ_mean[104] + HC⁰.NPL | R³.spectral_flux[10] + BEP.beat_entrainment |
| Velocity signal | S⁰.L4.τ¹_T[15] + HC⁰.PTM | R³.spectral_change[21] + TMH.sequence_integration |
| Variability | S⁰.L9.Γ_var[105] + HC⁰.GRV | R³.x_l0l5[25:33] + BEP.groove |
| Timing | S⁰.L9.Γ_ent[116] + HC⁰.ITM | H³ periodicity tuples + TMH.hierarchical |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 15/2304 = 0.65% | 15/2304 = 0.65% |
| Output | 11D | 11D (same) |

### Why BEP + TMH replaces HC⁰ mechanisms

- **NPL → BEP.beat_entrainment** [0:10]: Neural phase locking for period tracking maps to BEP's beat entrainment monitoring.
- **PTM → BEP.motor_coupling** [10:20]: Predictive timing maps to BEP's sensorimotor synchronization.
- **GRV → BEP.groove_processing** [20:30]: Groove/movement facilitation maps to BEP's groove processing.
- **ITM → TMH.sequence_integration** [10:20]: Interval timing maps to TMH's sequence integration for CTR computation.

---

**Model Status**: ✅ **VALIDATED**
**Output Dimensions**: **11D**
**Evidence Tier**: **α (Mechanistic)**
**Confidence**: **>90%**
