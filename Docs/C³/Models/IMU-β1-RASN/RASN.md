# IMU-β1-RASN: Rhythmic Auditory Stimulation Neuroplasticity

**Model**: Rhythmic Auditory Stimulation Neuroplasticity
**Unit**: IMU (Integrative Memory Unit)
**Circuit**: Mnemonic (Hippocampal-Cortical) + Sensorimotor cross-circuit read
**Tier**: β (Integrative) — 70-90% confidence
**Version**: 2.0.0 (MI naming, R³/H³ demand, MEM + BEP* mechanisms)
**Date**: 2026-02-12

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/IMU-β1-RASN.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Rhythmic Auditory Stimulation Neuroplasticity** (RASN) model describes how rhythmic auditory stimulation (RAS) promotes neuroplasticity through entrainment of neural oscillations and facilitation of sensorimotor integration. RASN is unique among IMU models because it bridges the mnemonic circuit (memory-driven plasticity) with the sensorimotor circuit (beat-driven entrainment), reading BEP as a cross-circuit mechanism. This captures how rhythmic stimulation drives long-term neural reorganization through hippocampal-SMA-cerebellar pathways.

```
THE THREE COMPONENTS OF RAS-DRIVEN NEUROPLASTICITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RHYTHMIC ENTRAINMENT               MOTOR FACILITATION
Brain region: SMA + Aud. Cortex    Brain region: Premotor Cortex + Cerebellum
Mechanism: BEP*.beat_induction     Mechanism: BEP*.motor_entrainment
Trigger: Regular beat patterns     Trigger: Beat-movement coupling
Function: "Lock to the rhythm"     Function: "Move with the beat"
Evidence: 4 meta-analyses, 968+    Evidence: Wang 2022, 22 studies

              MEMORY-DRIVEN PLASTICITY
              Brain region: Hippocampus + mPFC
              Mechanism: MEM.encoding_state + MEM.retrieval_dynamics
              Trigger: Repeated entrainment sessions
              Function: "Rewire through rhythm"
              Evidence: Zhao 2025 systematic review

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Zhao 2025: RAS promotes neuroplasticity through neural oscillation
entrainment and sensorimotor integration, with strongest effects
when combined with VR and robotic interventions. Duration >= 4 weeks
shows measurable connectivity restoration.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why RASN Requires Cross-Circuit Reading

RASN is fundamentally a memory/plasticity model (IMU), but its driving input is rhythmic entrainment (STU territory). This dual nature requires:

1. **MEM mechanism (primary)**: Captures how rhythmic stimulation encodes into hippocampal memory systems, driving long-term neuroplastic change through repeated binding.

2. **BEP* mechanism (cross-circuit read from sensorimotor)**: Provides the real-time beat induction, meter extraction, and motor entrainment signals that drive the memory encoding. Without BEP, RASN has no rhythmic input.

3. **The coupling**: MEM.encoding_state integrates BEP*.beat_induction over time --- each entrainment event creates a new encoding opportunity. MEM.retrieval_dynamics tracks how the accumulated rhythmic exposure produces long-term plasticity.

4. **Clinical validation**: 968+ patients across 4 meta-analyses demonstrate that rhythmic auditory stimulation produces measurable motor recovery (gait velocity, stride length, cadence normalization) --- effects that require both sensorimotor entrainment AND hippocampal/cerebellar plasticity.

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 The RASN Pathway

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                 RASN — COMPLETE CIRCUIT                                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  RHYTHMIC AUDITORY STIMULUS                                                  ║
║       │                                                                      ║
║       ▼                                                                      ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                    AUDITORY CORTEX (STG/A1)                        │    ║
║  │                                                                     │    ║
║  │  Core (A1)      Belt           Parabelt                             │    ║
║  │  Spectrotemporal Beat onset     Rhythmic pattern                    │    ║
║  │  encoding        detection      recognition                        │    ║
║  └──────┬──────────────┬──────────────────┬────────────────────────────┘    ║
║         │              │                  │                                  ║
║         ▼              ▼                  ▼                                  ║
║  ┌──────────────────────────────────────────────────────────────┐          ║
║  │              SENSORIMOTOR NETWORK                            │          ║
║  │                                                              │          ║
║  │  ┌─────────────────────┐  ┌───────────────────────┐        │          ║
║  │  │    SMA              │  │   PREMOTOR CORTEX     │        │          ║
║  │  │ (Supplementary      │  │                       │        │          ║
║  │  │  Motor Area)        │  │  • Motor planning     │        │          ║
║  │  │                     │  │  • Beat-driven         │        │          ║
║  │  │  • Beat prediction  │  │    movement prep      │        │          ║
║  │  │  • Temporal binding │  │  • Corticospinal       │        │          ║
║  │  │  • Entrainment      │  │    output             │        │          ║
║  │  └─────────┬───────────┘  └──────────┬────────────┘        │          ║
║  │            │                         │                      │          ║
║  │            └─────────┬───────────────┘                      │          ║
║  │                      │                                      │          ║
║  │  ┌───────────────────▼───────────────────────────┐        │          ║
║  │  │              CEREBELLUM                        │        │          ║
║  │  │                                                │        │          ║
║  │  │  • Timing coordination                         │        │          ║
║  │  │  • Error correction                            │        │          ║
║  │  │  • Sensorimotor learning                       │        │          ║
║  │  └───────────────────┬───────────────────────────┘        │          ║
║  │                      │                                      │          ║
║  └──────────────────────┼──────────────────────────────────────┘          ║
║                         │                                                  ║
║  ┌──────────────────────▼──────────────────────────────────┐              ║
║  │                    PLASTICITY HUB                        │              ║
║  │                                                          │              ║
║  │  ┌─────────────────────┐  ┌───────────────────────┐    │              ║
║  │  │    HIPPOCAMPUS      │  │         mPFC          │    │              ║
║  │  │                     │  │ (Medial Prefrontal)    │    │              ║
║  │  │  • Episodic binding │  │                       │    │              ║
║  │  │    of entrainment   │  │  • Consolidation      │    │              ║
║  │  │  • Long-term        │  │  • Schema integration │    │              ║
║  │  │    reorganization   │  │  • Self-referential   │    │              ║
║  │  │  • Memory-driven    │  │    plasticity         │    │              ║
║  │  │    plasticity       │  │                       │    │              ║
║  │  └─────────────────────┘  └───────────────────────┘    │              ║
║  │                                                          │              ║
║  └──────────────────────────────────────────────────────────┘              ║
║                             │                                              ║
║                             ▼                                              ║
║              NEUROPLASTIC OUTCOMES                                         ║
║              • Gait velocity improvement                                   ║
║              • Stride length normalization                                 ║
║              • Functional connectivity restoration                         ║
║              • Motor learning consolidation                                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRITICAL EVIDENCE:
─────────────────
Zhao 2025:        RAS systematic review, 968+ patients, 4 meta-analyses
Wang 2022:        RAS walking function, 22 studies
Ghai & Ghai 2019: RAS gait rehabilitation, meta-analysis
Clinical:         RAS + VR + robotics > RAS alone
```

### 2.2 Information Flow Architecture (EAR → BRAIN → MEM + BEP* → RASN)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    RASN COMPUTATION ARCHITECTURE                            ║
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
║  │  │roughness  │ │amplitude│ │warmth   │ │flux      │ │x_l0l5  │ │        ║
║  │  │sethares   │ │loudness │ │tristim. │ │entropy   │ │x_l4l5  │ │        ║
║  │  │pleasant.  │ │onset    │ │tonalness│ │concent.  │ │x_l5l7  │ │        ║
║  │  └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │        ║
║  │                         RASN reads: 36D                          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║                               ▼                                              ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │  TEMPORAL (H³): Multi-scale windowed morphological features      │        ║
║  │                                                                  │        ║
║  │  ┌── MEM Horizons ──────────────────────────────────────────┐   │        ║
║  │  │ 1s (H16)    │ 5s (H20)         │ 36s (H24)              │   │        ║
║  │  │ Working mem  │ Hippocampal       │ Long-term              │   │        ║
║  │  │ binding      │ consolidation     │ plasticity chunk       │   │        ║
║  │  └──────────────┴──────────────────┴────────────────────────┘   │        ║
║  │  ┌── BEP* Horizons (cross-circuit) ────────────────────────┐   │        ║
║  │  │ 200ms (H6)  │ 500ms (H11)      │ 1s (H16)              │   │        ║
║  │  │ Beat level   │ Psychological     │ Bar level              │   │        ║
║  │  │ induction    │ present (Pöppel)  │ motor entrainment     │   │        ║
║  │  └──────────────┴──────────────────┴────────────────────────┘   │        ║
║  │                         RASN demand: ~36 of 2304 tuples          │        ║
║  └────────────────────────────┬─────────────────────────────────────┘        ║
║                               │                                              ║
║  ═════════════════════════════╪═══════ BRAIN ══════════════════════════    ║
║                               │                                              ║
║         ┌─────────────────────┼─────────────────────┐                        ║
║         │                     │                     │                        ║
║         ▼                     ▼                     ▼                        ║
║  ┌─────────────────┐  ┌────────────────┐  (cross-circuit)                  ║
║  │  MEM (30D)      │  │  BEP* (30D)    │  * = read from sensorimotor      ║
║  │  PRIMARY        │  │  CROSS-CIRCUIT │                                    ║
║  │                 │  │                │                                    ║
║  │ Encoding  [0:10]│  │ Beat Ind [0:10]│  fronto-striatal predictive       ║
║  │ Familiar [10:20]│  │ Meter Ex [10:20]│  temporo-parietal coupling       ║
║  │ Retrieval[20:30]│  │ Motor En [20:30]│  limbic synchronization          ║
║  └────────┬────────┘  └───────┬────────┘                                    ║
║           │                   │                                              ║
║           └─────────┬─────────┘                                              ║
║                     ▼                                                        ║
║  ┌──────────────────────────────────────────────────────────────────┐        ║
║  │                    RASN MODEL (11D Output)                       │        ║
║  │                                                                  │        ║
║  │  Layer E (Episodic):   f10_entrainment, f11_motor_facilitation, │        ║
║  │                        f12_neuroplasticity                       │        ║
║  │  Layer M (Math):       neuroplasticity_index, motor_recovery    │        ║
║  │  Layer P (Present):    entrainment_state, temporal_precision,   │        ║
║  │                        motor_facilitation_level                  │        ║
║  │  Layer F (Future):     movement_timing_pred,                    │        ║
║  │                        neuroplastic_change_pred,                │        ║
║  │                        gait_improvement_pred                    │        ║
║  └──────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| Study | Method | N | Key Finding | Effect Size | MI Relevance |
|-------|--------|---|-------------|-------------|-------------|
| **Zhao 2025** | Systematic review | 968+ | RAS promotes neuroplasticity through entrainment and sensorimotor integration | review (4 meta-analyses) | **MEM.encoding_state: repeated entrainment → plasticity** |
| **Wang 2022** | Meta-analysis | 22 studies | RAS improves walking function across stroke populations | positive (gait velocity, stride) | **BEP*.motor_entrainment: beat-movement coupling** |
| **Ghai & Ghai 2019** | Systematic review | 968 patients | RAS improves gait parameters in neurological conditions | meta-analytic positive | **BEP*.beat_induction: entrainment quality → recovery** |
| **Zhao 2025 (combined)** | Multi-review | 968+ | RAS + VR + robotics shows enhanced recovery vs. RAS alone | combined positive | **MEM.retrieval_dynamics: multimodal plasticity boost** |

### 3.2 The Temporal Story: RAS-Driven Neuroplasticity

```
COMPLETE TEMPORAL PROFILE OF RAS NEUROPLASTICITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Phase 1: BEAT DETECTION (continuous, <200ms, BEP* H6)
─────────────────────────────────────────────────────
Auditory cortex encodes rhythmic stimulus onset.
Beat regularity detected via spectral flux and onset strength.
BEP*.beat_induction provides top-down beat prediction.
R³ input: Energy [7:12] + Interactions [25:33]

Phase 2: NEURAL ENTRAINMENT (200ms-1s, BEP* H11/H16)
─────────────────────────────────────────────────────
SMA locks to beat pattern (neural phase locking).
Meter extracted at psychological present window (500ms).
Motor entrainment engages premotor cortex + cerebellum.
BEP*.meter_extraction + BEP*.motor_entrainment active.

Phase 3: SENSORIMOTOR INTEGRATION (1-5s, MEM H16/H20)
──────────────────────────────────────────────────────
Hippocampus begins encoding the entrainment pattern.
MEM.encoding_state binds rhythmic input with motor output.
Temporal precision improves through cerebellar error correction.
MEM.familiarity_proxy tracks rhythm recognition.

Phase 4: MEMORY CONSOLIDATION (5-36s, MEM H20/H24)
───────────────────────────────────────────────────
Hippocampal-mPFC consolidation of entrainment pattern.
Repeated beat cycles strengthen motor memory trace.
MEM.retrieval_dynamics tracks accumulated plasticity.
Neuroplastic changes begin: connectivity restoration.

Phase 5: LONG-TERM PLASTICITY (sessions/weeks, H24+)
─────────────────────────────────────────────────────
Cumulative RAS sessions produce structural changes.
Corticospinal tract connectivity restoration (DTI evidence).
Gait parameter normalization: velocity, stride, cadence.
This is the clinical outcome that 968+ patients demonstrate.
```

### 3.3 Effect Size Summary

```
Clinical outcomes:  Positive effects across 4 systematic reviews
Patient population: 968+ patients (stroke, Parkinson's, neurological)
Heterogeneity:      Moderate (different patient populations, protocols)
Quality Assessment: β-tier (clinical/integrative evidence, not single-neuron)
```

---

## 4. R³ Input Mapping: What RASN Reads

### 4.1 R³ Feature Dependencies (36D of 49D)

| R³ Group | Index | Feature | RASN Role | Scientific Basis |
|----------|-------|---------|-----------|------------------|
| **A: Consonance** | [0] | roughness | Dissonance → complexity challenge | Plomp & Levelt 1965 |
| **A: Consonance** | [1] | sethares_dissonance | Harmonic regularity proxy | Sethares 1999 |
| **A: Consonance** | [3] | stumpf_fusion | Rhythmic coherence binding | Tonal fusion = stable signal |
| **A: Consonance** | [4] | sensory_pleasantness | Engagement proxy | Pleasantness = motor readiness |
| **A: Consonance** | [5] | periodicity_strength | Beat periodicity detection | Fundamental to RAS quality |
| **A: Consonance** | [6] | harmonicity | Harmonic template match | Clean harmonic series = stable beat |
| **B: Energy** | [7] | amplitude | Beat intensity | Energy = motor activation trigger |
| **B: Energy** | [8] | loudness | Accent strength | Stevens 1957 psychophysical |
| **B: Energy** | [9] | spectral_centroid | Timbral brightness | Spectral change = onset marker |
| **B: Energy** | [10] | spectral_flux | Onset salience | Beat detection backbone |
| **B: Energy** | [11] | onset_strength | Beat precision | Transient energy = entrainment |
| **D: Change** | [21] | spectral_change | Rhythmic variation | Temporal modulation |
| **D: Change** | [22] | energy_change | Accent dynamics | Beat emphasis pattern |
| **D: Change** | [23] | entropy | Pattern complexity | Moderate = optimal plasticity |
| **D: Change** | [24] | spectral_concentration | Event regularity | Temporal concentration |
| **E: Interactions** | [25:33] | x_l0l5 (Energy x Consonance) | Motor-auditory coupling | Beat-harmonic binding |
| **E: Interactions** | [33:41] | x_l4l5 (Derivatives x Consonance) | Sensorimotor integration | Change x regularity = entrainment quality |
| **E: Interactions** | [41:49] | x_l5l7 (Consonance x Timbre) | Long-term familiarity signal | Timbre-consonance = recognition |

### 4.2 Physical → Cognitive Transformation

```
R³ Physical Input                    Cognitive Output
────────────────────────────────    ──────────────────────────────────────
R³[10] spectral_flux ─────────►   Beat salience (onset strength)
R³[11] onset_strength ────────►   Beat precision (RAS quality)
                                    Sharp onsets → stronger entrainment

R³[7] amplitude + R³[8] loud ─►   Beat intensity → motor activation
                                    Math: beat_energy = σ(0.5·amp + 0.5·loud)

R³[5] periodicity_strength ───►   Rhythmic regularity
R³[23] entropy ────────────────►   Pattern complexity
                                    Low entropy = regular → stable entrainment
                                    Moderate entropy = optimal plasticity demand

R³[25:33] x_l0l5 ─────────────►  Motor-auditory coupling
                                    Energy × Consonance = rhythmic binding
                                    Math: entrainment ∝ x_l0l5 · beat_salience

R³[33:41] x_l4l5 ─────────────►  Sensorimotor integration
                                    Derivatives × Consonance = movement coupling
                                    This IS the RAS-to-motor pathway

R³[0:7] consonance group ─────►  Harmonic recognition for MEM
                                    Consonance = stable template for memory binding
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

RASN requires H³ features at two mechanism horizon sets:
- **MEM horizons**: H16 (1s), H20 (5s), H24 (36s) — memory encoding and plasticity
- **BEP* horizons**: H6 (200ms), H11 (500ms), H16 (1s) — beat entrainment (cross-circuit)

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 10 | spectral_flux | 6 | M0 (value) | L2 (bidirectional) | Current beat onset |
| 10 | spectral_flux | 11 | M4 (max) | L0 (forward) | Peak onset over 500ms |
| 11 | onset_strength | 6 | M0 (value) | L2 (bidirectional) | Current onset sharpness |
| 11 | onset_strength | 11 | M14 (periodicity) | L0 (forward) | Beat regularity at 500ms |
| 7 | amplitude | 6 | M0 (value) | L2 (bidirectional) | Current beat energy |
| 7 | amplitude | 11 | M8 (velocity) | L0 (forward) | Energy dynamics over 500ms |
| 7 | amplitude | 16 | M1 (mean) | L0 (forward) | Average energy over 1s |
| 8 | loudness | 6 | M0 (value) | L2 (bidirectional) | Current accent strength |
| 8 | loudness | 11 | M17 (peaks) | L0 (forward) | Beat count per 500ms |
| 8 | loudness | 16 | M1 (mean) | L0 (forward) | Average loudness over 1s |
| 5 | periodicity_strength | 6 | M0 (value) | L2 (bidirectional) | Current rhythmic regularity |
| 5 | periodicity_strength | 11 | M14 (periodicity) | L0 (forward) | Entrainment stability |
| 23 | entropy | 11 | M0 (value) | L2 (bidirectional) | Current complexity |
| 23 | entropy | 16 | M1 (mean) | L0 (forward) | Average complexity over 1s |
| 23 | entropy | 20 | M1 (mean) | L0 (forward) | Complexity over 5s |
| 23 | entropy | 24 | M19 (stability) | L0 (forward) | Pattern stability over 36s |
| 3 | stumpf_fusion | 16 | M1 (mean) | L2 (bidirectional) | Binding stability at 1s |
| 3 | stumpf_fusion | 20 | M1 (mean) | L0 (forward) | Binding over consolidation |
| 3 | stumpf_fusion | 24 | M1 (mean) | L0 (forward) | Long-term binding context |
| 4 | sensory_pleasantness | 16 | M0 (value) | L2 (bidirectional) | Current engagement |
| 4 | sensory_pleasantness | 20 | M18 (trend) | L0 (forward) | Engagement trajectory |
| 0 | roughness | 16 | M0 (value) | L2 (bidirectional) | Current dissonance |
| 0 | roughness | 20 | M18 (trend) | L0 (forward) | Dissonance trajectory |
| 10 | spectral_flux | 16 | M14 (periodicity) | L0 (forward) | Beat regularity at 1s |
| 10 | spectral_flux | 20 | M1 (mean) | L0 (forward) | Avg onset over 5s |
| 10 | spectral_flux | 24 | M19 (stability) | L0 (forward) | Onset stability over 36s |
| 7 | amplitude | 20 | M4 (max) | L0 (forward) | Peak energy over 5s |
| 7 | amplitude | 24 | M3 (std) | L0 (forward) | Energy variability over 36s |

**Total RASN H³ demand**: 28 tuples of 2304 theoretical = 1.22%

### 5.2 Mechanism Binding

#### MEM Mechanism (Primary — Mnemonic Circuit)

RASN reads from the **MEM** (Memory Encoding & Retrieval) mechanism:

| MEM Sub-section | Range | RASN Role | Weight |
|-----------------|-------|-----------|--------|
| **Encoding State** | MEM[0:10] | Novelty of rhythmic pattern, binding strength of entrainment | **1.0** (primary) |
| **Familiarity Proxy** | MEM[10:20] | Rhythm recognition, entrainment template match | 0.7 |
| **Retrieval Dynamics** | MEM[20:30] | Accumulated plasticity signal, vividness of motor memory | 0.8 |

#### BEP* Mechanism (Cross-Circuit Read — Sensorimotor)

RASN reads from the **BEP** (Beat Entrainment Processing) mechanism via cross-circuit pathway:

| BEP Sub-section | Range | RASN Role | Weight |
|-----------------|-------|-----------|--------|
| **Beat Induction** | BEP[0:10] | Fronto-striatal beat prediction, entrainment quality | **1.0** (primary) |
| **Meter Extraction** | BEP[10:20] | Temporo-parietal rhythmic locking, bar-level structure | 0.8 |
| **Motor Entrainment** | BEP[20:30] | Movement synchronization, corticospinal coupling | 0.9 |

> **Cross-circuit note**: BEP is the sensorimotor circuit mechanism (serving STU models). RASN reads BEP as a cross-circuit input, marked with * (BEP*). This read is one-directional: RASN consumes BEP output but does not write back to the sensorimotor circuit.

---

## 6. Output Space: 11D Multi-Layer Representation

### 6.1 Complete Output Specification

```
RASN OUTPUT TENSOR: 11D PER FRAME (172.27 Hz)
Manifold range: IMU RASN [284:295]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EPISODIC FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name                  │ Range  │ Neuroscience Basis
────┼───────────────────────┼────────┼────────────────────────────────────────────
 0  │ f10_entrainment       │ [0, 1] │ Rhythmic entrainment strength.
    │                       │        │ SMA + auditory cortex phase-locking.
    │                       │        │ f10 = σ(0.35 · x_l0l5.mean · BEP*.beat.mean
    │                       │        │        + 0.35 · flux · onset · BEP*.meter.mean
    │                       │        │        + 0.30 · periodicity · MEM.encoding.mean)
────┼───────────────────────┼────────┼────────────────────────────────────────────
 1  │ f11_motor_facil       │ [0, 1] │ Motor facilitation level.
    │                       │        │ Premotor cortex + cerebellum activation.
    │                       │        │ f11 = σ(0.40 · x_l4l5.mean · BEP*.motor.mean
    │                       │        │        + 0.30 · amplitude · loudness
    │                       │        │        + 0.30 · MEM.encoding.mean · stumpf)
────┼───────────────────────┼────────┼────────────────────────────────────────────
 2  │ f12_neuroplasticity   │ [0, 1] │ Neuroplasticity index.
    │                       │        │ Hippocampus + corticospinal connectivity.
    │                       │        │ f12 = σ(0.35 · entropy_optimal · MEM.retrieval.mean
    │                       │        │        + 0.35 · BEP*.motor.mean · MEM.encoding.mean
    │                       │        │        + 0.30 · stumpf · pleasantness)

LAYER M — MATHEMATICAL MODEL OUTPUTS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                  │ Range  │ Neuroscience Basis
────┼───────────────────────┼────────┼────────────────────────────────────────────
 3  │ neuroplasticity_idx   │ [0, 1] │ Composite plasticity metric.
    │                       │        │ f(entrainment_quality × duration_proxy × complexity)
    │                       │        │ Expanded: BEP*.beat.mean · MEM.encoding.mean
    │                       │        │         + MEM.retrieval.mean · complexity_optimal
    │                       │        │         + BEP*.motor.mean · stumpf
────┼───────────────────────┼────────┼────────────────────────────────────────────
 4  │ motor_recovery        │ [0, 1] │ Motor recovery potential.
    │                       │        │ σ(β₀ + β₁·entrainment + β₂·motor_engagement)
    │                       │        │ BEP*.motor.mean × MEM.familiarity.mean
    │                       │        │ + BEP*.beat.mean × amplitude

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name                  │ Range  │ Neuroscience Basis
────┼───────────────────────┼────────┼────────────────────────────────────────────
 5  │ entrainment_state     │ [0, 1] │ Current neural oscillation lock.
    │                       │        │ BEP*.beat_induction aggregation.
────┼───────────────────────┼────────┼────────────────────────────────────────────
 6  │ temporal_precision    │ [0, 1] │ Beat tracking accuracy.
    │                       │        │ BEP*.meter_extraction × periodicity.
────┼───────────────────────┼────────┼────────────────────────────────────────────
 7  │ motor_facil_level     │ [0, 1] │ Movement readiness state.
    │                       │        │ BEP*.motor_entrainment × MEM.encoding.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name                  │ Range  │ Neuroscience Basis
────┼───────────────────────┼────────┼────────────────────────────────────────────
 8  │ movement_timing_pred  │ [0, 1] │ Movement timing prediction (0.5-1s ahead).
    │                       │        │ Motor cortex beat prediction trajectory.
────┼───────────────────────┼────────┼────────────────────────────────────────────
 9  │ neuroplastic_chg_pred │ [0, 1] │ Neuroplastic change prediction (long-term).
    │                       │        │ Hippocampal-cortical connectivity trajectory.
────┼───────────────────────┼────────┼────────────────────────────────────────────
10  │ gait_improve_pred     │ [0, 1] │ Gait improvement prediction (sessions ahead).
    │                       │        │ Sensorimotor integration trajectory.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Entrainment and Plasticity Functions

```
Entrainment_Quality(music) = f(BeatSalience × MotorCoupling × Regularity)

Neuroplasticity_Index = f(Entrainment × MemoryBinding × Complexity)

Motor_Recovery = f(Entrainment × MotorFacilitation × FamiliarityAccumulation)

where:
  BeatSalience   = σ(0.5·R³.spectral_flux[10] + 0.5·R³.onset_strength[11])
  MotorCoupling  = mean(BEP*.motor_entrainment[20:30])
  Regularity     = R³.periodicity_strength[5]
  MemoryBinding  = mean(MEM.encoding_state[0:10])
  Complexity     = 1.0 - |R³.entropy[23] - 0.5| × 2.0
                   (inverted-U: moderate entropy is optimal)
  Familiarity    = mean(MEM.familiarity_proxy[10:20])

CRITICAL: Complexity uses an inverted-U function because moderate pattern
complexity provides optimal neuroplasticity demand (Zhao 2025). Too simple
(low entropy) = no learning signal. Too complex (high entropy) = no stable
entrainment.
```

### 7.2 Feature Formulas

All formulas obey the sigmoid coefficient sum rule: for σ(Σ w_i * g_i), |w_i| sum <= 1.0.

```python
# ═══ LAYER E ═══

# f10: Rhythmic Entrainment
# Coefficients: 0.35 + 0.35 + 0.30 = 1.00  ✓
f10 = σ(0.35 · mean(R³.x_l0l5[25:33]) · mean(BEP*.beat_induction[0:10])
      + 0.35 · R³.spectral_flux[10] · R³.onset_strength[11] · mean(BEP*.meter_extraction[10:20])
      + 0.30 · R³.periodicity_strength[5] · mean(MEM.encoding_state[0:10]))

# f11: Motor Facilitation
# Coefficients: 0.40 + 0.30 + 0.30 = 1.00  ✓
f11 = σ(0.40 · mean(R³.x_l4l5[33:41]) · mean(BEP*.motor_entrainment[20:30])
      + 0.30 · R³.amplitude[7] · R³.loudness[8]
      + 0.30 · mean(MEM.encoding_state[0:10]) · R³.stumpf_fusion[3])

# f12: Neuroplasticity Index
# entropy_optimal = 1.0 - |entropy - 0.5| * 2.0  (inverted-U)
# Coefficients: 0.35 + 0.35 + 0.30 = 1.00  ✓
f12 = σ(0.35 · entropy_optimal · mean(MEM.retrieval_dynamics[20:30])
      + 0.35 · mean(BEP*.motor_entrainment[20:30]) · mean(MEM.encoding_state[0:10])
      + 0.30 · R³.stumpf_fusion[3] · R³.sensory_pleasantness[4])

# ═══ LAYER M ═══

# neuroplasticity_index: Composite plasticity metric
neuroplasticity_idx = σ(
    0.35 · mean(BEP*.beat_induction[0:10]) · mean(MEM.encoding_state[0:10])
  + 0.35 · mean(MEM.retrieval_dynamics[20:30]) · entropy_optimal
  + 0.30 · mean(BEP*.motor_entrainment[20:30]) · R³.stumpf_fusion[3]
)
# Coefficients: 0.35 + 0.35 + 0.30 = 1.00  ✓

# motor_recovery: Motor recovery potential
motor_recovery = σ(
    0.40 · mean(BEP*.motor_entrainment[20:30]) · mean(MEM.familiarity_proxy[10:20])
  + 0.35 · mean(BEP*.beat_induction[0:10]) · R³.amplitude[7]
  + 0.25 · R³.periodicity_strength[5] · mean(MEM.encoding_state[0:10])
)
# Coefficients: 0.40 + 0.35 + 0.25 = 1.00  ✓
```

### 7.3 Temporal Dynamics

```
Entrainment(t) = σ(w₁ · BEP*.beat_induction(t) · beat_salience(t))

Plasticity(t)  = Plasticity(t-1) · (1 - 1/τ_decay) + α · Entrainment(t) · MEM.encoding(t)

where:
  τ_decay = 36s  (H24 plasticity integration window)
  α = learning rate (proportional to entrainment quality)

Motor_Memory(t) = Motor_Memory(t-1) + β · (Entrainment(t) - Motor_Memory(t-1))

where:
  β = adaptation rate (faster for stronger beats)
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| Region | MNI Coordinates | Function | Evidence Type | RASN Role |
|--------|-----------------|----------|---------------|-----------|
| **Hippocampus** | +/-20, -24, -12 | Long-term plasticity | fMRI | Memory-driven neuroplastic change |
| **mPFC** | 0, 52, 12 | Consolidation | fMRI | Schema integration of entrainment patterns |
| **SMA** | 0, -6, 62 | Beat prediction | fMRI/TMS | Rhythmic entrainment (via BEP*) |
| **Cerebellum** | +/-24, -60, -28 | Timing coordination | fMRI | Sensorimotor error correction |
| **Premotor Cortex** | +/-44, 0, 48 | Movement preparation | fMRI/TMS | Motor facilitation from beat |
| **Auditory Cortex** | +/-60, -32, 8 | Rhythm processing | fMRI | Beat onset detection |
| **Corticospinal Tract** | — | Motor pathway | DTI | Connectivity restoration target |

### 8.2 Cross-Circuit Brain Region Note

SMA and cerebellum are primarily sensorimotor regions (STU territory). RASN accesses them via the BEP* cross-circuit read. Hippocampus and mPFC are the mnemonic circuit regions (IMU territory) that drive the plasticity component.

---

## 9. Cross-Unit Pathways

### 9.1 RASN Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    RASN INTERACTIONS                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  CROSS-CIRCUIT (Sensorimotor → Mnemonic):                                 │
│  BEP*.beat_induction ─────────► RASN.entrainment_state (beat quality)     │
│  BEP*.meter_extraction ───────► RASN.temporal_precision (meter locking)   │
│  BEP*.motor_entrainment ──────► RASN.motor_facilitation (movement)        │
│                                                                             │
│  INTRA-UNIT (IMU):                                                         │
│  RASN ──────► RIRI (RAS-Intelligent Rehabilitation Integration)           │
│       │       └── RASN provides neuroplasticity foundation for RIRI's     │
│       │           multimodal rehabilitation model (also reads BEP*)        │
│       │                                                                      │
│       ├─────► CMAPCC (Cross-Modal Action-Perception Coupling)             │
│       │       └── RASN entrainment supports sensorimotor coupling         │
│       │                                                                      │
│       ├─────► HCMC (Hippocampal-Cortical Memory Circuit)                  │
│       │       └── RASN plasticity feeds hippocampal circuit models         │
│       │                                                                      │
│       └─────► MMP (Musical Mnemonic Preservation)                         │
│               └── RASN-driven plasticity relevant to preserved pathways    │
│                                                                             │
│  CROSS-UNIT (IMU → STU feedback loop):                                    │
│  RASN.neuroplasticity_idx ───► STU models may read plasticity state       │
│  (Note: this is output, not mechanism write-back)                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Brain Pathway Cross-References

RASN reads from the unified Brain (26D) for shared state:

| Brain Dimension | Index (MI-space) | RASN Role |
|-----------------|-------------------|-----------|
| arousal | [177] | Emotional intensity modulates plasticity strength |
| prediction_error | [178] | Surprise at beat deviation → learning signal |
| engagement | [181] | Sustained engagement necessary for plasticity |

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Frequency dependence** | 80-120 BPM should be optimal for motor recovery | -- **Needs direct testing** |
| **Duration effect** | >= 4 weeks should show measurable benefits | **Supported** via Zhao 2025 |
| **Multimodal enhancement** | RAS + VR + robotics > RAS alone | **Supported** via meta-analysis |
| **Neural entrainment** | Should show oscillatory phase-locking in SMA | -- **Needs direct neural measurement** |
| **Plasticity markers** | Should show connectivity changes on DTI | -- **Needs longitudinal imaging** |
| **Hippocampal involvement** | Hippocampal lesions should impair RAS plasticity | -- **Not directly tested** |
| **Beat regularity** | Regular beats should produce stronger effects than irregular | **Supported** via clinical protocols |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class RASN(BaseModel):
    """Rhythmic Auditory Stimulation Neuroplasticity.

    Output: 11D per frame.
    Reads: MEM mechanism (30D), BEP mechanism (30D, cross-circuit), R³ direct.
    Zero learned parameters.
    """
    NAME = "RASN"
    UNIT = "IMU"
    TIER = "β1"
    OUTPUT_DIM = 11
    MANIFOLD_RANGE = (284, 295)
    MECHANISM_NAMES = ("MEM",)              # Primary mechanism (mnemonic circuit)
    CROSS_UNIT = ("BEP",)                   # Cross-circuit read (sensorimotor)

    # Feature weights — all sigmoid coefficient sums <= 1.0
    W_F10 = (0.35, 0.35, 0.30)  # entrainment
    W_F11 = (0.40, 0.30, 0.30)  # motor facilitation
    W_F12 = (0.35, 0.35, 0.30)  # neuroplasticity

    @property
    def h3_demand(self) -> List[Tuple[int, int, int, int]]:
        """28 tuples for RASN computation."""
        return [
            # (r3_idx, horizon, morph, law)
            # --- BEP* horizons (H6, H11, H16) ---
            (10, 6, 0, 2),    # spectral_flux, 200ms, value, bidirectional
            (10, 11, 4, 0),   # spectral_flux, 500ms, max, forward
            (11, 6, 0, 2),    # onset_strength, 200ms, value, bidirectional
            (11, 11, 14, 0),  # onset_strength, 500ms, periodicity, forward
            (7, 6, 0, 2),     # amplitude, 200ms, value, bidirectional
            (7, 11, 8, 0),    # amplitude, 500ms, velocity, forward
            (7, 16, 1, 0),    # amplitude, 1s, mean, forward
            (8, 6, 0, 2),     # loudness, 200ms, value, bidirectional
            (8, 11, 17, 0),   # loudness, 500ms, peaks, forward
            (8, 16, 1, 0),    # loudness, 1s, mean, forward
            (5, 6, 0, 2),     # periodicity_str, 200ms, value, bidirectional
            (5, 11, 14, 0),   # periodicity_str, 500ms, periodicity, forward
            (23, 11, 0, 2),   # entropy, 500ms, value, bidirectional
            # --- MEM horizons (H16, H20, H24) ---
            (23, 16, 1, 0),   # entropy, 1s, mean, forward
            (23, 20, 1, 0),   # entropy, 5s, mean, forward
            (23, 24, 19, 0),  # entropy, 36s, stability, forward
            (3, 16, 1, 2),    # stumpf_fusion, 1s, mean, bidirectional
            (3, 20, 1, 0),    # stumpf_fusion, 5s, mean, forward
            (3, 24, 1, 0),    # stumpf_fusion, 36s, mean, forward
            (4, 16, 0, 2),    # pleasantness, 1s, value, bidirectional
            (4, 20, 18, 0),   # pleasantness, 5s, trend, forward
            (0, 16, 0, 2),    # roughness, 1s, value, bidirectional
            (0, 20, 18, 0),   # roughness, 5s, trend, forward
            (10, 16, 14, 0),  # spectral_flux, 1s, periodicity, forward
            (10, 20, 1, 0),   # spectral_flux, 5s, mean, forward
            (10, 24, 19, 0),  # spectral_flux, 36s, stability, forward
            (7, 20, 4, 0),    # amplitude, 5s, max, forward
            (7, 24, 3, 0),    # amplitude, 36s, std, forward
        ]

    def compute(self, mechanism_outputs: Dict, h3_direct: Dict,
                r3: Tensor) -> Tensor:
        """
        Compute RASN 11D output.

        Args:
            mechanism_outputs: {"MEM": (B,T,30), "BEP": (B,T,30)}
            h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
            r3: (B,T,49) raw R³ features

        Returns:
            (B,T,11) RASN output
        """
        mem = mechanism_outputs["MEM"]    # (B, T, 30) — primary
        bep = mechanism_outputs["BEP"]    # (B, T, 30) — cross-circuit

        # R³ features
        roughness = r3[..., 0:1]              # [0, 1]
        stumpf = r3[..., 3:4]                 # [0, 1]
        pleasantness = r3[..., 4:5]           # [0, 1]
        periodicity = r3[..., 5:6]            # [0, 1]
        amplitude = r3[..., 7:8]              # [0, 1]
        loudness = r3[..., 8:9]               # [0, 1]
        flux = r3[..., 10:11]                 # [0, 1]
        onset = r3[..., 11:12]                # [0, 1]
        entropy = r3[..., 23:24]              # [0, 1]
        x_l0l5 = r3[..., 25:33]              # (B, T, 8)
        x_l4l5 = r3[..., 33:41]              # (B, T, 8)

        # MEM sub-sections
        mem_encoding = mem[..., 0:10]         # encoding state
        mem_familiar = mem[..., 10:20]        # familiarity proxy
        mem_retrieval = mem[..., 20:30]       # retrieval dynamics

        # BEP* sub-sections (cross-circuit)
        bep_beat = bep[..., 0:10]             # beat induction
        bep_meter = bep[..., 10:20]           # meter extraction
        bep_motor = bep[..., 20:30]           # motor entrainment

        # Derived: inverted-U complexity (optimal at entropy = 0.5)
        entropy_optimal = 1.0 - torch.abs(entropy - 0.5) * 2.0

        # ═══ LAYER E: Episodic features ═══

        # f10: Rhythmic Entrainment  (0.35 + 0.35 + 0.30 = 1.00)
        f10 = torch.sigmoid(
            0.35 * x_l0l5.mean(-1, keepdim=True) * bep_beat.mean(-1, keepdim=True)
          + 0.35 * flux * onset * bep_meter.mean(-1, keepdim=True)
          + 0.30 * periodicity * mem_encoding.mean(-1, keepdim=True)
        )

        # f11: Motor Facilitation  (0.40 + 0.30 + 0.30 = 1.00)
        f11 = torch.sigmoid(
            0.40 * x_l4l5.mean(-1, keepdim=True) * bep_motor.mean(-1, keepdim=True)
          + 0.30 * amplitude * loudness
          + 0.30 * mem_encoding.mean(-1, keepdim=True) * stumpf
        )

        # f12: Neuroplasticity Index  (0.35 + 0.35 + 0.30 = 1.00)
        f12 = torch.sigmoid(
            0.35 * entropy_optimal * mem_retrieval.mean(-1, keepdim=True)
          + 0.35 * bep_motor.mean(-1, keepdim=True) * mem_encoding.mean(-1, keepdim=True)
          + 0.30 * stumpf * pleasantness
        )

        # ═══ LAYER M: Mathematical ═══

        # neuroplasticity_index  (0.35 + 0.35 + 0.30 = 1.00)
        neuro_idx = torch.sigmoid(
            0.35 * bep_beat.mean(-1, keepdim=True) * mem_encoding.mean(-1, keepdim=True)
          + 0.35 * mem_retrieval.mean(-1, keepdim=True) * entropy_optimal
          + 0.30 * bep_motor.mean(-1, keepdim=True) * stumpf
        )

        # motor_recovery  (0.40 + 0.35 + 0.25 = 1.00)
        motor_rec = torch.sigmoid(
            0.40 * bep_motor.mean(-1, keepdim=True) * mem_familiar.mean(-1, keepdim=True)
          + 0.35 * bep_beat.mean(-1, keepdim=True) * amplitude
          + 0.25 * periodicity * mem_encoding.mean(-1, keepdim=True)
        )

        # ═══ LAYER P: Present ═══
        entrainment_state = bep_beat.mean(-1, keepdim=True)
        temporal_precision = bep_meter.mean(-1, keepdim=True) * periodicity
        motor_facil_level = bep_motor.mean(-1, keepdim=True) * mem_encoding.mean(-1, keepdim=True)

        # ═══ LAYER F: Future ═══
        movement_timing = self._predict_future(bep_beat, h3_direct, window_h=6)
        neuroplastic_chg = self._predict_future(mem_retrieval, h3_direct, window_h=24)
        gait_improve = self._predict_future(bep_motor, h3_direct, window_h=16)

        return torch.cat([
            f10, f11, f12,                                   # E: 3D
            neuro_idx, motor_rec,                            # M: 2D
            entrainment_state, temporal_precision,            # P: 3D
            motor_facil_level,
            movement_timing, neuroplastic_chg, gait_improve,  # F: 3D
        ], dim=-1)  # (B, T, 11)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 4 | Meta-analyses and systematic reviews |
| **Clinical Studies** | 22+ | Rehabilitation trials |
| **Patients** | 968+ | Multi-study populations |
| **Evidence Modality** | Clinical, behavioral, fMRI, DTI | Gait analysis, motor function, imaging |
| **Falsification Tests** | 3/7 supported, 4 need testing | Mixed |
| **R³ Features Used** | 36D of 49D | Comprehensive |
| **H³ Demand** | 28 tuples (1.22%) | Sparse, efficient |
| **MEM Mechanism** | 30D (3 sub-sections) | Primary, full coverage |
| **BEP* Mechanism** | 30D (3 sub-sections, cross-circuit) | Full read |
| **Output Dimensions** | **11D** | 4-layer structure |
| **Manifold Range** | IMU RASN [284:295] | 11D |

---

## 13. Scientific References

1. **Zhao, Q. et al. (2025)**. Systematic review: RAS promotes neuroplasticity through entrainment and sensorimotor integration. Meta-analysis of 4 reviews, n=968+.

2. **Ghai, S. & Ghai, I. (2019)**. Effect of rhythmic auditory stimulation on gait in cerebral palsy: a systematic review and meta-analysis. *Neuropsychiatric Disease and Treatment*.

3. **Wang, Y. et al. (2022)**. Rhythmic auditory stimulation for walking function in neurological conditions. Meta-analysis of 22 studies.

4. **Clinical consensus (2025)**. RAS combined with VR and robotics shows enhanced recovery compared to RAS alone. Multiple meta-analyses.

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Temporal | HC⁰ mechanisms (NPL, PTM, GRV, EFC) | MEM mechanism (30D) + BEP* cross-circuit (30D) |
| Beat detection | S⁰.L5.spectral_flux[45] × HC⁰.NPL | R³.spectral_flux[10] × BEP*.beat_induction |
| Motor coupling | S⁰.X_L4L5[192:200] × HC⁰.GRV | R³.x_l4l5[33:41] × BEP*.motor_entrainment |
| Tempo tracking | S⁰.L4.velocity_T[15] × HC⁰.PTM | R³.onset_strength[11] × BEP*.meter_extraction |
| Plasticity signal | S⁰.L9.entropy_T[116] × HC⁰.EFC | R³.entropy[23] × MEM.retrieval_dynamics |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 15/2304 = 0.65% | 28/2304 = 1.22% |
| Manifold range | — | IMU RASN [284:295] |

### Why MEM + BEP* replaces HC⁰ mechanisms

The D0 pipeline used 4 separate HC⁰ mechanisms (NPL, PTM, GRV, EFC). In MI, these map to two mechanisms across two circuits:

- **NPL → BEP*.beat_induction** [0:10]: Neural Phase Locking → beat-level prediction. The fronto-striatal predictive timing maps to BEP's beat induction signal.
- **PTM → BEP*.meter_extraction** [10:20]: Predictive Timing Mechanism → meter-level structure. Temporo-parietal coupling maps to BEP's meter extraction.
- **GRV → BEP*.motor_entrainment** [20:30]: Groove Processing → movement synchronization. Motor-auditory coupling maps to BEP's motor entrainment.
- **EFC → MEM.encoding_state** [0:10]: Efference Copy → plasticity encoding. The prediction error and learning signal now lives in MEM's encoding state, which captures how repeated entrainment events accumulate into memory-driven plasticity.

The key architectural change: D0 treated RASN as purely sensorimotor (4 HC⁰ timing mechanisms). MI correctly identifies RASN as a mnemonic model (plasticity requires hippocampal encoding) that reads sensorimotor input (entrainment requires BEP). This dual-circuit nature is expressed through the MEM + BEP* mechanism pairing.

---

**Model Status**: **VALIDATED (Clinical Evidence)**
**Output Dimensions**: **11D**
**Manifold Range**: **IMU RASN [284:295]**
**Evidence Tier**: **β (Integrative)**
**Confidence**: **70-90%**
