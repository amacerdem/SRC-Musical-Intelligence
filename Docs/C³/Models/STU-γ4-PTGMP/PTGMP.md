# STU-γ4-PTGMP: Piano Training Grey Matter Plasticity

**Model**: Piano Training Grey Matter Plasticity
**Unit**: STU (Sensorimotor Timing Unit)
**Circuit**: Sensorimotor (Temporal Memory Hierarchy)
**Tier**: γ (Speculative) — <70% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added G:Rhythm feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/General/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/STU-γ4-PTGMP.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Piano Training Grey Matter Plasticity** (PTGMP) model describes how piano training in older adults induces structural neuroplasticity — measurable grey matter volume (GMV) increases in DLPFC (bilateral) and cerebellum (right hemisphere), along with increased frontal theta power during improvisation. This model captures the acoustic correlates of motor-learning-driven plasticity, specifically the spectral and temporal features that track with training-induced structural brain changes.

```
PIANO TRAINING GREY MATTER PLASTICITY — THREE PATHWAYS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXECUTIVE PLANNING                     MOTOR COORDINATION
Brain region: DLPFC (bilateral)        Brain region: Cerebellum (right)
Effect: GMV increase d=0.34            Effect: GMV increase d=0.34
Function: Audio-motor planning         Function: Timing/coordination
R³ basis: Energy × Interactions        R³ basis: Change × Interactions

CREATIVE FLEXIBILITY
Brain region: Frontal cortex
Effect: Theta power increase d=0.27
Function: Improvisation / novel motor sequences
R³ basis: Energy dynamics + Change rate

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY INSIGHT: Late-life structural neuroplasticity is driven by
audio-motor integration demands. Older adults who train piano
show bilateral DLPFC and right cerebellar GMV increases comparable
to younger learners, suggesting age-resilient plasticity pathways.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why This Matters for STU

PTGMP provides evidence that sensorimotor timing circuits remain plastic in late life:

1. **HMCE** (α1) provides the hierarchical context that PTGMP's motor learning operates within.
2. **AMSC** (α2) describes the auditory-motor coupling that PTGMP's plasticity strengthens.
3. **TPIO** (β2) relates to timing precision that PTGMP's cerebellar plasticity improves.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The PTGMP Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                 PTGMP — COMPLETE CIRCUIT                                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  MUSICAL INPUT (piano performance — keystroke sequences)                     ║
║       │                                                                      ║
║       ▼                                                                      ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │        DORSOLATERAL PREFRONTAL CORTEX (DLPFC, bilateral)            │    ║
║  │        Executive planning for audio-motor sequences                  │    ║
║  │        GMV increase: d = 0.34                                        │    ║
║  │        Function: Sequence planning, working memory for music         │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │  Motor command relay                         ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │        CEREBELLUM (right hemisphere)                                │    ║
║  │        Motor coordination and timing precision                      │    ║
║  │        GMV increase: d = 0.34                                        │    ║
║  │        Function: Keystroke timing, error correction, smoothness     │    ║
║  └──────────────────────────┬──────────────────────────────────────────┘    ║
║                              │  Feedback loop                               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │        FRONTAL CORTEX                                               │    ║
║  │        Creative motor-perceptual integration                        │    ║
║  │        Theta power increase: d = 0.27                                │    ║
║  │        Function: Improvisation, novel sequence generation           │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
║  PLASTICITY: Late-life structural neuroplasticity — older adults show       ║
║  comparable GMV increases to younger learners after piano training.          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
DLPFC bilateral GMV increase:    d = 0.34 (VBM, piano training RCTs)
Cerebellum GMV increase:         d = 0.34 (VBM) | L cerebellum p<0.0001 (Espinosa 2025)
Frontal theta power increase:    d = 0.27 (EEG, improvisation)
Systematic review:               6 RCTs, N=555, confirms pattern BUT 4/6 high bias risk
ALE meta-analysis:               k=84, N=3005, musicians: higher sensorimotor (Criscuolo 2022)
CONSTRAINT: Espinosa 2025 VBM (N=61) found L cerebellum + auditory GM in active
  players but NO DLPFC — DLPFC finding may be training-specific, not expertise-related
Improvisation: Bilateral BA45 (Broca's) activation (Tachibana 2024, N=20)
  + ECN+NMR+limbic+memory systems (Liao 2024, N=25 percussionists)
```

### 2.2 Information Flow Architecture (EAR → BRAIN → TMH → PTGMP)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    PTGMP COMPUTATION ARCHITECTURE                            ║
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
║  │  │           │ │centroid │ │         │ │pitch_chg │ │x_l5l7  │ │        ║
║  │  │           │ │flux     │ │         │ │timbre_chg│ │        │ │        ║
║  │  │           │ │onset    │ │         │ │          │ │        │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                       PTGMP reads: 33D                          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── Syllable ────┐ ┌── Beat ──────────┐ ┌── Section ────────┐ │        ║
║  │  │ 300ms (H8)     │ │ 700ms (H14)      │ │ 5000ms (H20)     │ │        ║
║  │  │                │ │                   │ │                    │ │        ║
║  │  │ Short context  │ │ Medium context    │ │ Long context       │ │        ║
║  │  │ Keystroke-     │ │ Phrase-level      │ │ Practice session-  │ │        ║
║  │  │ level timing   │ │ motor planning    │ │ level adaptation   │ │        ║
║  │  └──────┬─────────┘ └──────┬────────────┘ └──────┬─────────────┘ │        ║
║  │         │                  │                     │               │        ║
║  │         └──────────────────┴─────────────────────┘               │        ║
║  │                       PTGMP demand: ~16 of 2304 tuples           │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN: Sensorimotor Circuit ═══════  ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌─────────────────┐                                                        ║
║  │  TMH (30D)      │  Temporal Memory Hierarchy mechanism                   ║
║  │                 │                                                        ║
║  │ Short   [0:10] │  Keystroke timing, onset patterns, local motor cue     ║
║  │ Medium  [10:20]│  Phrase-level planning, motor sequence coordination    ║
║  │ Long    [20:30]│  Practice adaptation, skill consolidation signal       ║
║  └────────┬────────┘                                                        ║
║           │                                                                  ║
║           ▼                                                                  ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    PTGMP MODEL (10D Output)                      │        ║
║  │                                                                  │        ║
║  │  Layer E (Explicit):  f01_dlpfc_plasticity, f02_cerebellar_plast,│        ║
║  │                       f03_frontal_theta                          │        ║
║  │  Layer M (Math):      plasticity_index, age_resilience           │        ║
║  │  Layer P (Present):   motor_coordination, audio_motor_binding    │        ║
║  │  Layer F (Future):    skill_trajectory, timing_improvement,      │        ║
║  │                       adaptation_rate                            │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Piano training RCTs** (via Espinosa 2025 SR) | VBM | 555 (6 RCTs) | DLPFC bilateral GMV increase after piano training | d = 0.34 | **f01_dlpfc_plasticity**: executive planning |
| 2 | **Piano training RCTs** (via Espinosa 2025 SR) | VBM | 555 (6 RCTs) | Cerebellum GMV increase | d = 0.34 | **f02_cerebellar_plast**: motor coordination |
| 3 | **Piano training RCTs** (via Espinosa 2025 SR) | EEG | 555 (6 RCTs) | Frontal theta power increase during improvisation | d = 0.27 | **f03_frontal_theta**: creative flexibility |
| 4 | **Espinosa et al. (2025)** VBM | VBM | 61 | Active players: ↑ GM in L planum temporale, L planum polare, R posterior insula, L cerebellum (all p < 0.0001 vs. naive) | p < 0.0001 | L cerebellum confirmed, NO DLPFC → CONSTRAINS |
| 5 | **Espinosa et al. (2025)** VBM | VBM | 61 | Former players vs. naive: NO GM differences; music NOT associated with neuropsych performance | NS | Former players lose benefit; no cognitive correlation |
| 6 | **Criscuolo et al. (2022)** | ALE meta-analysis | 3005 (k=84) | Musicians: higher auditory, sensorimotor, interoceptive, limbic; LOWER parietal volumes/activity | k = 84 studies | Population-level structural plasticity evidence |
| 7 | **Liu et al. (2025)** | VBM/morphometry | 33 | Musicians: greater cortical thickness in L superior frontal + R central parietal; non-musicians: greater gyrification bilateral insula | group differences | Cortical thickness supports frontal plasticity |
| 8 | **Liao et al. (2024)** | fMRI | 25 | Percussionists: SIMP → ECN+NMR ↑, DMN ↓; FIMP → ECN+NMR+limbic+memory ↑ | structural/free improv contrast | Improvisation engages executive+limbic+memory |
| 9 | **Tachibana et al. (2024)** | fNIRS | 20 | Guitar improvisation → bilateral BA45 (Broca's) activation, independent of skill level | all participants | Frontal motor-planning for creativity |
| 10 | **Leipold et al. (2021)** | rsfMRI + DWI | 153 | Robust musicianship effects on functional + structural brain networks | replicable across AP/non-AP | Network-level structural plasticity |
| 11 | **Yu et al. (2025)** | MIND morphometry | 89 | Musicians: higher structural similarity in DMN + somatomotor network | group-level MIND values | Structural connectivity reorganization |
| 12 | **Olszewska et al. (2021)** | Review | — | Renormalization model: expansion → retraction = efficiency; predispositions vs. neuroplasticity | conceptual | Framework for plasticity mechanisms |

#### §3.1.1 Evidence Convergence (7 methods)

Structural plasticity from music training converges across 7 methods: (1) RCT piano VBM (Espinosa 2025 SR), (2) cross-sectional VBM (Espinosa 2025), (3) ALE meta-analysis (Criscuolo 2022), (4) cortical thickness/morphometry (Liu 2025), (5) fMRI improvisation (Liao 2024), (6) fNIRS improvisation (Tachibana 2024), (7) rsfMRI/DWI connectivity (Leipold 2021).

#### §3.1.2 Espinosa 2025 Systematic Review Qualification

The Espinosa et al. (2025) systematic review of 6 piano training RCTs (N=555) confirms the DLPFC+cerebellum+theta findings BUT with critical caveats: (a) 4 of 6 studies had HIGH risk of bias; (b) 3 of 6 studies used overlapping cohorts from the same longitudinal project (Hannover/Geneva); (c) only 1 study reported a positive correlation between neurobiological changes and cognitive improvements; (d) no MCI participants were assessed. The model's d=0.34 and d=0.27 effect sizes should be considered preliminary.

#### §3.1.3 DLPFC Constraint from Cross-Sectional Evidence

Espinosa et al. (2025) VBM of active vs. former vs. naive older adults (N=61) found increased GM in L planum temporale, L planum polare, R posterior insula, and L cerebellum — but NOT in DLPFC. This suggests the DLPFC finding may be specific to the training intervention (piano learning) rather than a stable expertise-related structural difference. Additionally, former players showed NO GM differences from naive individuals, indicating that structural benefits may not persist after cessation of active playing.

### 3.2 The Plasticity Gradient

```
STRUCTURAL NEUROPLASTICITY FROM PIANO TRAINING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Region              Function            Effect Size   Evidence
────────────────────────────────────────────────────────────────
DLPFC (bilateral)   Executive planning  d = 0.34      VBM (GMV)
Cerebellum (right)  Motor coordination  d = 0.34      VBM (GMV)
Frontal cortex      Improvisation       d = 0.27      EEG (theta)

Key Finding: Older adults show grey matter volume increases
comparable to younger trainees. Late-life plasticity is driven
by the audio-motor integration demands of piano practice.

Note: d = 0.34 is a small-to-medium effect. γ-tier because
single-domain evidence (piano training only), limited
replication, and older-adult specificity.
```

### 3.3 Effect Size Summary

```
PIANO TRAINING RCT EFFECTS (from Espinosa 2025 systematic review):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Measure                  Effect      Source
─────────────────────────────────────────────────────────────────
DLPFC bilateral GMV      d = 0.34    VBM (piano training RCTs)
Cerebellum GMV           d = 0.34    VBM (piano training RCTs)
Frontal theta power      d = 0.27    EEG (improvisation)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CROSS-SECTIONAL EVIDENCE (Espinosa 2025 VBM, N=61):
  Active players vs naive: L cerebellum + auditory GM (p < 0.0001)
  BUT: NO DLPFC difference, NO neuropsych correlation
  Former players = naive (benefits do NOT persist)

META-ANALYTIC (Criscuolo 2022 ALE, k=84, N=3005):
  Musicians: ↑ auditory, sensorimotor, interoceptive, limbic
  Musicians: ↓ parietal regions

IMPROVISATION EVIDENCE:
  Bilateral BA45 activation (Tachibana 2024, N=20)
  ECN + NMR + limbic + memory activation (Liao 2024, N=25)

Quality Assessment: γ-tier (speculative)
  Strengths: Systematic review confirms GMV+theta pattern from
  6 RCTs (N=555); cross-sectional L cerebellum confirmed
  Weakness: 4/6 RCTs high risk of bias, 3 overlapping cohorts,
  DLPFC finding NOT replicated cross-sectionally, former players
  lose benefits, no cognitive-neural correlation robust
```

---

## 4. R³ Input Mapping: What PTGMP Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | PTGMP Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **B: Energy** | [7] | amplitude | Motor intensity dynamics | Keystroke force tracking |
| **B: Energy** | [8] | loudness | Perceptual intensity | Stevens 1957: power law |
| **B: Energy** | [9] | spectral_centroid | Pitch perception proxy | Melodic learning |
| **B: Energy** | [10] | spectral_flux | Note onset detection | Motor timing anchor |
| **B: Energy** | [11] | onset_strength | Event boundary marking | Keystroke precision |
| **D: Change** | [21] | spectral_change | Short-context motor dynamics | Rate of spectral change |
| **D: Change** | [22] | energy_change | Medium-context dynamics | Intensity rate of change |
| **D: Change** | [23] | pitch_change | Melodic contour dynamics | Pitch learning trajectory |
| **D: Change** | [24] | timbre_change | Timbral evolution | Instrument identity |
| **E: Interactions** | [25:33] | x_l0l5 (8D) | Foundation x Perceptual coupling | Motor-timing learning |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | Dynamics x Perceptual coupling | Audio-motor integration (DLPFC) |
| **E: Interactions** | [41:49] | x_l5l7 (8D) | Perceptual x Relations coupling | Structural coordination |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ v2 Group | Index | Feature | PTGMP Role | Scientific Basis |
|-------------|-------|---------|-----------|------------------|
| **G: Rhythm** | [73] | tempo_stability | Temporal prediction reliability for motor planning | Jones & Boltz 1989 |

**Rationale**: PTGMP models predictive timing and goal-directed motor planning. G[73] tempo_stability provides a direct measure of temporal prediction reliability, which is critical for the cerebellar timing coordination pathway -- stable tempo enables more precise motor planning and reduces the cognitive demand on DLPFC executive sequence planning.

**Code impact** (Phase 6): `r3_indices` will be extended to include `[73]`.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[10] spectral_flux ─────────┐
R³[11] onset_strength ────────┼──► Motor Timing Precision
R³[21:25] Change (4D) ────────┘   TMH.short_context at H8 (300ms)
                                    Cerebellar timing coordination

R³[7] amplitude ────────────────┐
R³[8] loudness ─────────────────┼──► Audio-Motor Planning
R³[22] energy_change ───────────┘   TMH.medium_context at H14 (700ms)
                                    DLPFC executive sequence planning

R³[25:33] x_l0l5 (8D) ────────┐
R³[33:41] x_l4l5 (8D) ────────┼──► Long-Range Skill Consolidation
R³[41:49] x_l5l7 (8D) ────────┘   TMH.long_context at H20 (5000ms)
                                    Practice-level adaptation signal

Plasticity Factor ─────────────── Age-Resilient Plasticity
                                    d = 0.34 DLPFC, d = 0.34 cerebellum
                                    Older adults maintain capacity

── R³ v2 (Phase 6) ──────────────────────────────────────────────
R³[73] tempo_stability ────────── Temporal prediction → motor planning
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

PTGMP requires H³ features at three TMH horizons: H8 (300ms), H14 (700ms), H20 (5000ms).
These correspond to keystroke → phrase → practice-session timescales.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 10 | spectral_flux | 8 | M0 (value) | L0 (fwd) | Current onset detection |
| 10 | spectral_flux | 8 | M1 (mean) | L0 (fwd) | Mean onset rate (short) |
| 11 | onset_strength | 8 | M0 (value) | L0 (fwd) | Keystroke boundary current |
| 21 | spectral_change | 8 | M1 (mean) | L0 (fwd) | Mean spectral dynamics |
| 22 | energy_change | 14 | M1 (mean) | L0 (fwd) | Mean energy dynamics |
| 22 | energy_change | 14 | M3 (std) | L0 (fwd) | Motor variability proxy |
| 23 | pitch_change | 14 | M1 (mean) | L0 (fwd) | Mean pitch dynamics |
| 7 | amplitude | 14 | M18 (trend) | L0 (fwd) | Intensity trajectory |
| 8 | loudness | 14 | M1 (mean) | L0 (fwd) | Mean loudness over phrase |
| 8 | loudness | 14 | M19 (stability) | L0 (fwd) | Performance consistency |
| 25 | x_l0l5[0] | 20 | M1 (mean) | L0 (fwd) | Long-term motor coupling |
| 25 | x_l0l5[0] | 20 | M19 (stability) | L0 (fwd) | Practice-level stability |
| 33 | x_l4l5[0] | 20 | M1 (mean) | L0 (fwd) | Audio-motor integration mean |
| 33 | x_l4l5[0] | 20 | M22 (autocorr) | L0 (fwd) | Repetition-based learning |
| 41 | x_l5l7[0] | 20 | M1 (mean) | L0 (fwd) | Structural coupling mean |
| 41 | x_l5l7[0] | 20 | M18 (trend) | L0 (fwd) | Skill improvement trend |

**Total PTGMP H³ demand**: 16 tuples of 2304 theoretical = 0.69%

### 5.2 TMH Mechanism Binding

PTGMP reads from the **TMH** (Temporal Memory Hierarchy) mechanism:

| TMH Sub-section | Range | PTGMP Role | Weight |
|-----------------|-------|-----------|--------|
| **Short Context** | TMH[0:10] | Keystroke-level motor timing (cerebellum, onset precision) | **1.0** (primary) |
| **Medium Context** | TMH[10:20] | Phrase-level motor planning (DLPFC, sequence coordination) | **1.0** (primary) |
| **Long Context** | TMH[20:30] | Practice-session adaptation (plasticity consolidation) | **1.0** (primary) |

PTGMP does NOT read from BEP — grey matter plasticity is about structural adaptation from motor-learning demands, not beat entrainment.

---

## 6. Output Space: 10D Multi-Layer Representation

### 6.1 Complete Output Specification

```
PTGMP OUTPUT TENSOR: 10D PER FRAME (172.27 Hz)
Manifold range: STU PTGMP [229:239]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                │ Range  │ Neuroscience Basis
────┼─────────────────────┼────────┼────────────────────────────────────────────
 0  │ f01_dlpfc_plasticity│ [0, 1] │ DLPFC bilateral GMV increase proxy (d=0.34).
    │                     │        │ Audio-motor planning complexity.
    │                     │        │ f01 = σ(0.35 · amp_trend ·
    │                     │        │         x_l4l5_mean · TMH.medium)
────┼─────────────────────┼────────┼────────────────────────────────────────────
 1  │ f02_cerebellar_plast│ [0, 1] │ Cerebellum right hemisphere GMV proxy (d=0.34).
    │                     │        │ Motor coordination and timing precision.
    │                     │        │ f02 = σ(0.30 · flux_mean · onset_val ·
    │                     │        │         TMH.short)
────┼─────────────────────┼────────┼────────────────────────────────────────────
 2  │ f03_frontal_theta   │ [0, 1] │ Frontal theta power increase proxy (d=0.27).
    │                     │        │ Creative motor-perceptual integration.
    │                     │        │ f03 = σ(0.30 · energy_change_std ·
    │                     │        │         pitch_change_mean · TMH.medium)

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                │ Range  │ Neuroscience Basis
────┼─────────────────────┼────────┼────────────────────────────────────────────
 3  │ plasticity_index    │ [0, 1] │ Overall structural plasticity signal.
    │                     │        │ Weighted sum of region-specific effects.
    │                     │        │ plast = (0.34·f01 + 0.34·f02 + 0.27·f03) /
    │                     │        │         (0.34 + 0.34 + 0.27)
────┼─────────────────────┼────────┼────────────────────────────────────────────
 4  │ age_resilience      │ [0, 1] │ Late-life plasticity preservation factor.
    │                     │        │ Stability of long-range motor coupling.
    │                     │        │ age_r = σ(0.50 · stability_loud ·
    │                     │        │           stability_coupling)

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                │ Range  │ Neuroscience Basis
────┼─────────────────────┼────────┼────────────────────────────────────────────
 5  │ motor_coordination  │ [0, 1] │ Current cerebellar motor state.
    │                     │        │ TMH.short_context aggregation.
────┼─────────────────────┼────────┼────────────────────────────────────────────
 6  │ audio_motor_binding │ [0, 1] │ Current DLPFC audio-motor integration state.
    │                     │        │ TMH.medium_context aggregation.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                │ Range  │ Neuroscience Basis
────┼─────────────────────┼────────┼────────────────────────────────────────────
 7  │ skill_trajectory    │ [0, 1] │ Predicted motor improvement direction.
    │                     │        │ Long-range coupling trend.
────┼─────────────────────┼────────┼────────────────────────────────────────────
 8  │ timing_improvement  │ [0, 1] │ Predicted timing precision improvement.
    │                     │        │ Autocorrelation-based repetition learning.
────┼─────────────────────┼────────┼────────────────────────────────────────────
 9  │ adaptation_rate     │ [0, 1] │ Rate of practice-level adaptation.
    │                     │        │ TMH.long_context trend-based estimate.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 10D per frame at 172.27 Hz
Manifold range: STU PTGMP [229:239]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Plasticity Encoding Function

```
Plasticity Encoding:

    GMV_Change(region) = f(Training_Intensity, Audio_Motor_Demand)

    For DLPFC (bilateral):
      Plasticity ∝ Audio-motor planning complexity
      d = 0.34 (grey matter volume increase)

    For Cerebellum (right):
      Plasticity ∝ Motor timing precision demand
      d = 0.34 (grey matter volume increase)

    For Frontal Cortex:
      Theta_Power ∝ Improvisation / creative flexibility
      d = 0.27 (theta band power increase)

    Age Resilience:
      Plasticity(older) ≈ Plasticity(younger)
      Late-life structural neuroplasticity maintained
```

### 7.2 Feature Formulas

```python
# ═══ IMPORTANT: Sigmoid coefficient rule ═══
# For σ(Σ wᵢ · gᵢ), |wᵢ| must sum ≤ 1.0
# All products below use multiplicative gating
# which keeps effective input in reasonable range.

# f01: DLPFC Plasticity (bilateral, d=0.34)
amp_trend = h3[(7, 14, 18, 0)]        # amplitude trend at H14
x_l4l5_mean = h3[(33, 20, 1, 0)]      # x_l4l5 mean at H20
f01 = σ(0.35 · amp_trend · x_l4l5_mean
         · mean(TMH.medium_context[10:20]))
# |0.35| ≤ 1.0 ✓  (multiplicative terms bounded [0,1])

# f02: Cerebellar Plasticity (right, d=0.34)
flux_mean = h3[(10, 8, 1, 0)]         # spectral_flux mean at H8
onset_val = h3[(11, 8, 0, 0)]         # onset_strength value at H8
f02 = σ(0.30 · flux_mean · onset_val
         · mean(TMH.short_context[0:10]))
# |0.30| ≤ 1.0 ✓

# f03: Frontal Theta (d=0.27)
energy_std = h3[(22, 14, 3, 0)]       # energy_change std at H14
pitch_mean = h3[(23, 14, 1, 0)]       # pitch_change mean at H14
f03 = σ(0.30 · energy_std · pitch_mean
         · mean(TMH.medium_context[10:20]))
# |0.30| ≤ 1.0 ✓

# f04: Plasticity Index (effect-size weighted average)
f04 = (0.34 · f01 + 0.34 · f02 + 0.27 · f03) / (0.34 + 0.34 + 0.27)
# Weighted by reported effect sizes → [0, 1]

# f05: Age Resilience
stability_loud = h3[(8, 14, 19, 0)]   # loudness stability at H14
stability_coupling = h3[(25, 20, 19, 0)] # x_l0l5 stability at H20
f05 = σ(0.50 · stability_loud · stability_coupling)
# |0.50| ≤ 1.0 ✓  (multiplicative → effective range compressed)
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Evidence Type | Effect | PTGMP Function |
|--------|-----------------|---------------|--------|---------------|
| **DLPFC (bilateral)** | ±44, 36, 28 | VBM RCT (piano training) | d = 0.34 | Executive audio-motor planning |
| **Cerebellum (L)** | -24, -60, -30 | VBM (Espinosa 2025 N=61, p<.0001) | d = 0.34 + cross-sectional | Motor coordination / timing |
| **Frontal cortex** | ±4, 28, 44 | EEG theta (improvisation) | d = 0.27 | Improvisation / creative flexibility |
| **Planum temporale (L)** | -50, -25, 10 | VBM (Espinosa 2025 p<.0001) | cross-sectional | Auditory processing plasticity |
| **Planum polare (L)** | -45, -5, -5 | VBM (Espinosa 2025 p<.0001) | cross-sectional | Anterior auditory cortex |
| **Posterior insula (R)** | 40, -15, 5 | VBM (Espinosa 2025 p<.0001) | cross-sectional | Interoceptive/auditory integration |
| **IFG / BA45 (bilateral)** | ±48, 20, 10 | fNIRS (Tachibana 2024 N=20) | improvisation | Broca's area motor planning for creativity |
| **SMA / Pre-SMA** | 0, -5, 55 | ALE (Criscuolo 2022 k=84) | meta-analytic | Sensorimotor coordination hub |
| **L Superior frontal** | -15, 35, 45 | VBM (Liu 2025 N=33) | cortical thickness | Prefrontal structural difference |
| **Auditory cortex** | ±55, -22, 10 | ALE (Criscuolo 2022 k=84) | meta-analytic | Enhanced auditory processing |

---

## 9. Cross-Unit Pathways

### 9.1 PTGMP ↔ Other Models

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PTGMP INTERACTIONS                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INTRA-UNIT (STU):                                                         │
│  PTGMP.motor_coordination ──► AMSC (cerebellar → auditory-motor coupling)  │
│  PTGMP.audio_motor_binding ──► TPIO (DLPFC → timing precision)            │
│  PTGMP.skill_trajectory ────► HMCE (plasticity → context depth growth)    │
│                                                                             │
│  CROSS-UNIT (P4: STU internal):                                            │
│  TMH.short_context ↔ PTGMP.cerebellar_plast (timing → plasticity)        │
│  TMH.medium_context ↔ PTGMP.dlpfc_plasticity (planning → plasticity)     │
│                                                                             │
│  CROSS-UNIT (P5: STU → IMU):                                              │
│  PTGMP.plasticity_index ──► IMU (structural plasticity → memory encoding) │
│                                                                             │
│  CROSS-UNIT (P5: STU → ARU):                                              │
│  PTGMP.frontal_theta ──► ARU (improvisation → affective engagement)       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| # | Criterion | Testable Prediction | Status |
|---|-----------|---------------------|--------|
| 1 | **DLPFC GMV increase** | Piano training should increase bilateral DLPFC GMV | **Partially confirmed**: d=0.34 from RCTs (Espinosa 2025 SR); NOT found cross-sectionally |
| 2 | **Cerebellum GMV increase** | Piano training should increase cerebellar GMV | **Confirmed**: d=0.34 from RCTs + L cerebellum p<.0001 cross-sectional (Espinosa 2025 VBM) |
| 3 | **Frontal theta increase** | Improvisation should increase frontal theta power | **Confirmed**: d=0.27 from piano RCTs (Espinosa 2025 SR) |
| 4 | **Population-level structural differences** | Musicians should show structural brain differences at meta-analytic level | **Confirmed**: ALE k=84, N=3005, higher sensorimotor+auditory (Criscuolo 2022) |
| 5 | **Improvisation frontal activation** | Musical improvisation should activate frontal motor-planning regions | **Confirmed**: bilateral BA45 (Tachibana 2024); ECN activation (Liao 2024) |
| 6 | **Persistence after cessation** | GMV benefits should persist in former players | **Disconfirmed**: Former players = naive (Espinosa 2025 VBM). Benefits require active playing |
| 7 | **Cognitive correlation** | Structural changes should correlate with cognitive improvement | **Weakly confirmed**: Only 1/6 RCTs showed correlation (Espinosa 2025 SR) |
| 8 | **Non-piano training** | Other motor training should show different GMV patterns | Testable |
| 9 | **Young adult comparison** | Effect sizes should be similar (age resilience) | Testable |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class PTGMP(BaseModel):
    """Piano Training Grey Matter Plasticity.

    Output: 10D per frame.
    Reads: TMH mechanism (30D), R³ direct.
    Zero learned parameters — all deterministic.
    """
    NAME = "PTGMP"
    UNIT = "STU"
    TIER = "γ4"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("TMH",)        # Primary mechanism

    # Effect sizes from literature
    DLPFC_D = 0.34     # DLPFC bilateral GMV increase
    CEREB_D = 0.34     # Cerebellum right GMV increase
    THETA_D = 0.27     # Frontal theta power increase

    # Sigmoid coefficients — |wᵢ| ≤ 1.0 rule enforced
    ALPHA = 0.35   # DLPFC plasticity weight
    BETA = 0.30    # Cerebellar plasticity weight
    GAMMA = 0.30   # Frontal theta weight
    DELTA = 0.50   # Age resilience weight

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """16 tuples for PTGMP computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # Short context (H8 = 300ms) — cerebellar timing
            (10, 8, 0, 0),    # spectral_flux, value, forward
            (10, 8, 1, 0),    # spectral_flux, mean, forward
            (11, 8, 0, 0),    # onset_strength, value, forward
            (21, 8, 1, 0),    # spectral_change, mean, forward
            # Medium context (H14 = 700ms) — DLPFC planning
            (22, 14, 1, 0),   # energy_change, mean, forward
            (22, 14, 3, 0),   # energy_change, std, forward
            (23, 14, 1, 0),   # pitch_change, mean, forward
            (7, 14, 18, 0),   # amplitude, trend, forward
            (8, 14, 1, 0),    # loudness, mean, forward
            (8, 14, 19, 0),   # loudness, stability, forward
            # Long context (H20 = 5000ms) — plasticity consolidation
            (25, 20, 1, 0),   # x_l0l5[0], mean, forward
            (25, 20, 19, 0),  # x_l0l5[0], stability, forward
            (33, 20, 1, 0),   # x_l4l5[0], mean, forward
            (33, 20, 22, 0),  # x_l4l5[0], autocorrelation, forward
            (41, 20, 1, 0),   # x_l5l7[0], mean, forward
            (41, 20, 18, 0),  # x_l5l7[0], trend, forward
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute PTGMP 10D output.

        Args:
            mechanism_outputs: {"TMH": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,10) PTGMP output
        """
        tmh = mechanism_outputs["TMH"]    # (B, T, 30)

        # TMH sub-sections
        tmh_short = tmh[..., 0:10]        # short context
        tmh_medium = tmh[..., 10:20]      # medium context
        tmh_long = tmh[..., 20:30]        # long context

        # ═══ LAYER E: Explicit features ═══

        # f01: DLPFC Plasticity (bilateral, d=0.34)
        amp_trend = h3_direct[(7, 14, 18, 0)].unsqueeze(-1)
        x_l4l5_mean = h3_direct[(33, 20, 1, 0)].unsqueeze(-1)
        f01 = torch.sigmoid(self.ALPHA * (
            amp_trend * x_l4l5_mean
            * tmh_medium.mean(-1, keepdim=True)
        ))

        # f02: Cerebellar Plasticity (right, d=0.34)
        flux_mean = h3_direct[(10, 8, 1, 0)].unsqueeze(-1)
        onset_val = h3_direct[(11, 8, 0, 0)].unsqueeze(-1)
        f02 = torch.sigmoid(self.BETA * (
            flux_mean * onset_val
            * tmh_short.mean(-1, keepdim=True)
        ))

        # f03: Frontal Theta (d=0.27)
        energy_std = h3_direct[(22, 14, 3, 0)].unsqueeze(-1)
        pitch_mean = h3_direct[(23, 14, 1, 0)].unsqueeze(-1)
        f03 = torch.sigmoid(self.GAMMA * (
            energy_std * pitch_mean
            * tmh_medium.mean(-1, keepdim=True)
        ))

        # ═══ LAYER M: Mathematical ═══

        # Plasticity index — effect-size weighted
        total_d = self.DLPFC_D + self.CEREB_D + self.THETA_D
        plasticity_index = (
            self.DLPFC_D * f01
            + self.CEREB_D * f02
            + self.THETA_D * f03
        ) / total_d

        # Age resilience — stability-based
        stability_loud = h3_direct[(8, 14, 19, 0)].unsqueeze(-1)
        stability_coupling = h3_direct[(25, 20, 19, 0)].unsqueeze(-1)
        age_resilience = torch.sigmoid(self.DELTA * (
            stability_loud * stability_coupling
        ))

        # ═══ LAYER P: Present ═══
        motor_coordination = tmh_short.mean(-1, keepdim=True)
        audio_motor_binding = tmh_medium.mean(-1, keepdim=True)

        # ═══ LAYER F: Future ═══

        # Skill trajectory — long-range trend
        x_l5l7_trend = h3_direct[(41, 20, 18, 0)].unsqueeze(-1)
        skill_trajectory = torch.sigmoid(
            0.6 * x_l5l7_trend + 0.4 * tmh_long.mean(-1, keepdim=True)
        )
        # |0.6| + |0.4| = 1.0 ≤ 1.0 ✓

        # Timing improvement — repetition learning
        x_l4l5_autocorr = h3_direct[(33, 20, 22, 0)].unsqueeze(-1)
        timing_improvement = torch.sigmoid(
            0.5 * x_l4l5_autocorr + 0.5 * tmh_short.mean(-1, keepdim=True)
        )
        # |0.5| + |0.5| = 1.0 ≤ 1.0 ✓

        # Adaptation rate — long context trend
        x_l0l5_mean = h3_direct[(25, 20, 1, 0)].unsqueeze(-1)
        adaptation_rate = torch.sigmoid(
            0.4 * x_l0l5_mean + 0.3 * tmh_long.mean(-1, keepdim=True)
            + 0.3 * plasticity_index
        )
        # |0.4| + |0.3| + |0.3| = 1.0 ≤ 1.0 ✓

        return torch.cat([
            f01, f02, f03,                                    # E: 3D
            plasticity_index, age_resilience,                  # M: 2D
            motor_coordination, audio_motor_binding,           # P: 2D
            skill_trajectory, timing_improvement, adaptation_rate,  # F: 3D
        ], dim=-1)  # (B, T, 10)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 12 (6 Tier 1 + 4 Tier 2 + 2 Tier 3) | 7 methods, >3600 cumulative N |
| **Effect Sizes** | d = 0.34 (DLPFC), d = 0.34 (cerebellum), d = 0.27 (theta) | Piano RCTs (Espinosa 2025 SR) |
| **Evidence Modality** | VBM, ALE meta-analysis, fMRI, fNIRS, EEG, rsfMRI, DWI | Multi-method convergence |
| **Falsification Tests** | 9 total: 5 confirmed, 1 disconfirmed, 1 weakly confirmed, 2 testable | Moderate validity |
| **R³ Features Used** | 33D of 49D | Energy + Change + Interactions |
| **H³ Demand** | 16 tuples (0.69%) | Sparse, efficient |
| **TMH Mechanism** | 30D (3 sub-sections) | Full coverage |
| **Output Dimensions** | **10D** | 4-layer structure (E3 + M2 + P2 + F3) |

---

## 13. Scientific References

### Tier 1 — Direct Quantitative Evidence (in collection)

1. **Espinosa, N., et al. (2025)**. Neurobiological effects of music-making interventions for older adults: a systematic review. *Aging Clinical and Experimental Research*, 37:113. (Systematic review, 6 RCTs, N=555. 5 piano + 1 choral singing. Confirms DLPFC d=0.34, cerebellum d=0.34, frontal theta d=0.27. HIGH risk of bias in 4/6 studies, 3 overlapping cohorts, only 1/6 showed cognitive-neural correlation)

2. **Espinosa, N., et al. (2025)**. The associations between playing a musical instrument and grey matter in older adults at risk for dementia: a whole-brain VBM analysis. *GeroScience*. (VBM, N=61, active/former/naive older adults. Active: ↑ GM in L planum temporale, L planum polare, R posterior insula, L cerebellum exterior, all p<.0001. Former = naive. NO DLPFC. Music NOT correlated with neuropsych. CONSTRAINS DLPFC and persistence claims)

3. **Criscuolo, A., et al. (2022)**. An ALE meta-analytic review of musical expertise. *Scientific Reports*, 12:11726. (ALE, k=84, N=3005. Musicians: higher auditory/sensorimotor/interoceptive/limbic; LOWER parietal. Population-level structural plasticity evidence)

4. **Liu, Z., et al. (2025)**. Differences in structural brain morphometry between musicians and non-musicians. *Frontiers in Human Neuroscience*. (N=33. Cortical thickness, fractal dimensionality, gyrification, sulcal depth. Musicians: greater thickness L superior frontal + R central parietal)

5. **Liao, Y.-C., et al. (2024)**. The rhythmic mind: brain functions of percussionists in improvisation. *Frontiers in Human Neuroscience*, 18:1418727. (fMRI, N=25 percussionists. SIMP: ECN+NMR ↑, DMN ↓. FIMP: ECN+NMR+limbic+memory ↑. Improvisation activates executive + limbic + memory systems)

6. **Tachibana, A., et al. (2024)**. Rock music improvisation shows increased activity in Broca's area and its right hemisphere homologue related to spontaneous creativity. *BMC Research Notes*, 17:61. (fNIRS, N=20 guitarists. Bilateral BA45 activation during improvisation. Independent of skill level. Motor planning for creativity)

### Tier 2 — Supporting Evidence (in collection)

7. **Leipold, S., et al. (2021)**. Musical expertise shapes functional and structural brain networks independent of absolute pitch ability. *Journal of Neuroscience*, 41(11):2496-2511. (rsfMRI + DWI, N=153. Robust musicianship effects on structural+functional connectivity)

8. **Yu, Y., et al. (2025)**. Shared and distinct patterns of cortical morphometric inverse divergence and their association with empathy in dancers and musicians. *Scientific Reports*, 15:28572. (MIND morphometry, N=89. Musicians: higher structural similarity in DMN + somatomotor network)

9. **Olszewska, A., et al. (2021)**. How musical training shapes the adult brain: predispositions and neuroplasticity. *Frontiers in Neuroscience*. (Review. Renormalization model: expansion → retraction. Framework for training-induced plasticity)

10. **Villanueva, S., et al. (2024)**. Long-term music instruction is partially associated with socioemotional skills. *PLoS ONE*. (N=83, 4-year longitudinal. Near-transfer only. CONSTRAINS broad transfer claims)

### Tier 3 — Founding / Historical (NOT in collection)

11. **Guo, Y., et al. (2021)**. Piano training increases grey matter in older adults. (Referenced in mi_beta code. Likely one of the piano RCTs reviewed by Espinosa 2025)

12. **Sluming, V., et al. (2002)**. Grey matter differences in orchestral musicians. (Referenced in mi_beta code. Cross-sectional VBM in professional orchestral musicians)

### Code Note (Phase 5)

The current `mi_beta` code (`ptgmp.py`) has several mismatches with this document:
- **MECHANISM_NAMES**: code has `("BEP",)` — doc specifies `("TMH",)` (TMH is correct)
- **Citations**: code has Guo 2021 + Sluming 2002 — doc adds Espinosa 2025 (×2), Criscuolo 2022, Liu 2025, Liao 2024, Tachibana 2024
- **Dimension names**: code uses `f01_gm_volume_change, f02_plasticity_index` etc. — doc uses `f01_dlpfc_plasticity, f02_cerebellar_plast, f03_frontal_theta`
- **Brain regions**: code has dlPFC (-44,30,28) + CB (20,-62,-26) — doc has 10 regions with corrected MNI
- **version**: code has `"2.0.0"` — should be `"2.1.0"`
- **paper_count**: code has `3` — should be `12`
These mismatches will be resolved in Phase 5 (code alignment).

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D): L0, L4, L5, L6, L9, X_L0L1, X_L4L5 | R³ (49D): Energy, Change, Interactions |
| Temporal | HC⁰ mechanisms (OSC, ITM, GRV, HRM) | TMH mechanism (30D) |
| Oscillation coupling | OSC[0:56] (gamma/alpha_beta/syllable) | TMH.short_context[0:10] + H³ tuples |
| Motor timing | ITM[216:244] (interval timing) | TMH.short_context + TMH.medium_context |
| Groove | GRV[244:272] (motor coordination) | TMH.medium_context + R³ Change features |
| Memory replay | HRM[272:302] (hippocampal) | TMH.long_context[20:30] |
| Statistics | S⁰.L9 (mean, std) | H³ morphs (M0, M1, M3, M18, M19, M22) |
| Cross-feature | X_L0L1[128:136], X_L4L5[192:200] | R³.x_l0l5[25:33], x_l4l5[33:41], x_l5l7[41:49] |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 32/2304 = 1.39% | 16/2304 = 0.69% |
| Output dimensions | 12D | **10D** (catalog spec, streamlined) |

### Why TMH replaces HC⁰ mechanisms

The D0 pipeline used 4 separate HC⁰ mechanisms (OSC, ITM, GRV, HRM). In MI, these are unified into the TMH mechanism with 3 sub-sections:
- **OSC + ITM → TMH.short_context** [0:10]: Neural oscillation coupling + interval timing → keystroke-level motor timing features
- **GRV → TMH.medium_context** [10:20]: Groove motor coordination → phrase-level planning and audio-motor integration
- **HRM → TMH.long_context** [20:30]: Hippocampal replay → practice-session adaptation and skill consolidation

### Output reduction: 12D → 10D

The legacy 12D output included redundant features that duplicated TMH sub-section means. The MI 10D output consolidates:
- Layer E: 4D → 3D (merged separate DLPFC left/right into bilateral)
- Layer M: 2D → 2D (unchanged)
- Layer P: 3D → 2D (merged motor sub-features)
- Layer F: 3D → 3D (unchanged)

---

**Model Status**: **SPECULATIVE** (systematic review confirms piano training GMV+theta effects from 6 RCTs but 4/6 high bias risk, DLPFC NOT found cross-sectionally, benefits do NOT persist in former players, 12 papers, 7 methods, >3600 cumulative N)
**Output Dimensions**: **10D**
**Evidence Tier**: **γ (Speculative)**
**Confidence**: **<70%** (cerebellar plasticity strongest; DLPFC finding limited to training RCTs; theta/improvisation well-supported across studies)
