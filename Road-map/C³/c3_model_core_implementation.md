> **HISTORICAL** — This plan described the multi-model C³ integration approach (v1.x).
> In v2.0, the separate-model architecture was replaced by a unified MusicalBrain (26D).
> See [04-BRAIN-DATA-FLOW.md](General/04-BRAIN-DATA-FLOW.md) for the current architecture.
> Retained for historical reference.

# C³ Core-4 Model Implementation Plan

> Musical Intelligence (MI) v2.0.0 — 2026-02-11
> How to integrate all 48 Core-4 C³ models into the MI pipeline.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Current State](#2-current-state)
3. [Complete 48-Model Catalog](#3-complete-48-model-catalog)
4. [Target Architecture](#4-target-architecture)
5. [Circuit-to-Unit Mapping](#5-circuit-to-unit-mapping)
6. [New Mechanisms Design](#6-new-mechanisms-design)
7. [Phased Implementation](#7-phased-implementation)
8. [Dimension Budget](#8-dimension-budget)
9. [H³ Demand Expansion](#9-h3-demand-expansion)
10. [R³ Feature Coverage](#10-r3-feature-coverage)
11. [Cross-Unit Pathways](#11-cross-unit-pathways)
12. [Testing & Validation](#12-testing--validation)
13. [File Layout](#13-file-layout)

---

## 1. Overview

### 1.1 What Are the 48 Models?

The C³ Meta-Theory (448 peer-reviewed papers, 1,116 empirical claims) identifies **4 core
cognitive units** with sufficient evidence for quantitative meta-analysis (k ≥ 10 studies each):

| Unit | Full Name | Pooled Effect | Papers | Models |
|------|-----------|--------------|--------|--------|
| **SPU** | Spectral Processing Unit | d = 0.84 (large) | 46 | 9 |
| **STU** | Sensorimotor Timing Unit | d = 0.67 (medium) | 104 | 14 |
| **IMU** | Integrative Memory Unit | d = 0.53 (medium) | 213 | 15 |
| **ARU** | Affective Resonance Unit | d = 0.83 (large) | 42 | 10 |
| | | | **405** | **48** |

These 48 models account for **90% of the empirical literature** and are organized into
three tiers based on evidence strength:

| Tier | Label | Confidence | Criteria |
|------|-------|-----------|----------|
| **α** | Mechanistic | >90% | Multi-study converging evidence, replicated effects |
| **β** | Integrative | 70–90% | Moderate evidence, integrative mechanisms |
| **γ** | Speculative | <70% | Preliminary evidence, theoretical extensions |

### 1.2 Design Philosophy

Every model follows the MI white-box contract:

1. **Zero learned parameters** — 100% deterministic, same input → same output
2. **Demand-driven computation** — models declare H³ demand; pipeline computes only what's needed
3. **Mechanism sharing** — multiple models read from the same mechanism (computed once)
4. **4-level epistemology** — computation, neuroscience, psychology, validation
5. **Traceable** — every output dimension traces back to R³ features through H³ morphs
6. **Literature-grounded** — every weight and formula cites its source paper

### 1.3 Core Abstractions

```python
# BaseMechanism: H³ context → intermediate features (30D each)
class BaseMechanism(ABC):
    NAME: str                           # "AED"
    HORIZONS: Tuple[int, ...]           # (6, 16)
    OUTPUT_DIM: int = 30
    def compute(self, h3_avg: Tensor) -> Tensor  # (B,T,72) → (B,T,30)

# BaseModel: mechanisms + H³ direct → output
class BaseModel(ABC):
    NAME: str                           # "SRP"
    UNIT: str                           # "ARU"
    TIER: str                           # "α1"
    OUTPUT_DIM: int                     # 19
    MECHANISM_NAMES: Tuple[str, ...]    # ("AED", "CPD", "C0P")
    LAYERS: Tuple[LayerSpec, ...]       # output structure
    def compute(self, mechanism_outputs, h3_direct) -> ModelOutput
```

---

## 2. Current State

### 2.1 What's Built

| Component | Status | Location |
|-----------|--------|----------|
| **EAR: Cochlea** | Done | `mi/ear/cochlea.py` |
| **EAR: R³ (49D)** | Done | `mi/ear/r3/` (6 files) |
| **EAR: H³ (sparse)** | Done | `mi/ear/h3/` (5 files) |
| **Mechanism: AED (30D)** | Done | `mi/brain/mesolimbic/mechanisms/aed.py` |
| **Mechanism: CPD (30D)** | Done | `mi/brain/mesolimbic/mechanisms/cpd.py` |
| **Mechanism: C0P (30D)** | Done | `mi/brain/mesolimbic/mechanisms/c0p.py` |
| **Mechanism: ASA (30D)** | Done | `mi/brain/salience/mechanisms/asa.py` |
| **Model: SRP (19D)** | Done | `mi/brain/mesolimbic/models/srp.py` |
| **Model: AAC (14D)** | Spec done, code pending | `Road-map/C³/Models/ARU-α2-AAC/` |
| **Semantics: SRP (45D)** | Done | `mi/language/srp/` |
| **Pipeline orchestrator** | Done | `mi/pipeline/mi.py` |
| **Tests** | 79 passing | `tests/` |
| **Brain scaffolding** | 6 circuits × 3 subdirs | `mi/brain/*/` |

### 2.2 What's Missing

- **46 models** not yet implemented (8 ARU + 9 SPU + 14 STU + 15 IMU)
- **~8 new mechanisms** for SPU, STU, IMU circuits
- **Semantic layers** for all new models
- **Cross-unit pathway** computation
- **~200+ new tests**

---

## 3. Complete 48-Model Catalog

### 3.1 SPU — Spectral Processing Unit (9 models)

> Brain regions: Heschl's gyrus, STG, inferior colliculus, planum polare
> Function: Pitch, timbre, consonance extraction from acoustic input

#### Tier α — Mechanistic (3 models)

| ID | Code | Full Name | Output | Core Claim |
|----|------|-----------|--------|------------|
| α1 | **BCH** | Brainstem Consonance Hierarchy | 12D | FFR encodes consonance via harmonicity (r=0.81) |
| α2 | **PSCL** | Pitch Salience Cortical Localization | 12D | Pitch salience in anterolateral Heschl's, parametric with periodicity |
| α3 | **PCCR** | Pitch Chroma Cortical Representation | 11D | Chroma (pitch class) in non-primary auditory cortex, octave-independent |

#### Tier β — Integrative (3 models)

| ID | Code | Full Name | Output | Core Claim |
|----|------|-----------|--------|------------|
| β1 | **STAI** | Spectral-Temporal Aesthetic Integration | 12D | Aesthetic preference peaks at intermediate spectral complexity × temporal predictability |
| β2 | **TSCP** | Timbre-Specific Cortical Plasticity | 10D | Musical training induces timbre-specific auditory cortex reorganization |
| β3 | **MIAA** | Musical Imagery Auditory Activation | 11D | Musical imagery activates auditory cortex without physical sound |

#### Tier γ — Speculative (3 models)

| ID | Code | Full Name | Output | Core Claim |
|----|------|-----------|--------|------------|
| γ1 | **SDNPS** | Stimulus-Dependent Neural Pitch Salience | 10D | NPS from brainstem FFR predicts behavior for synthetic tones but not natural sounds |
| γ2 | **ESME** | Expertise-Specific MMN Enhancement | 11D | MMN amplitude reflects trained instrument expertise (d=−1.09) |
| γ3 | **SDED** | Sensory Dissonance Early Detection | 10D | Roughness detected at early sensory stages regardless of expertise |

**SPU Total: 99D**

---

### 3.2 STU — Sensorimotor Timing Unit (14 models)

> Brain regions: STG, SMA, cerebellum, primary motor cortex, premotor, basal ganglia
> Function: Temporal structure encoding, beat induction, auditory-motor coupling

#### Tier α — Mechanistic (3 models)

| ID | Code | Full Name | Output | Core Claim |
|----|------|-----------|--------|------------|
| α1 | **HMCE** | Hierarchical Musical Context Encoding | 13D | Context encoding follows anatomical gradient from A1 outward (r=0.99) |
| α2 | **AMSC** | Auditory-Motor Stream Coupling | 12D | Dual-stream auditory processing: ventral (what) + dorsal (how) (r=0.70) |
| α3 | **MDNS** | Melody Decoding from Neural Signals | 12D | Melodic features decodable from EEG with gradient mapping |

#### Tier β — Integrative (6 models)

| ID | Code | Full Name | Output | Core Claim |
|----|------|-----------|--------|------------|
| β1 | **AMSS** | Attention-Modulated Stream Segregation | 11D | Top-down attention modulates polyphonic stream segregation |
| β2 | **TPIO** | Timbre Perception-Imagery Overlap | 10D | Perceived and imagined timbre overlap in auditory association areas |
| β3 | **EDTA** | Expertise-Dependent Tempo Accuracy | 10D | Musicians show greater temporal precision in beat entrainment |
| β4 | **ETAM** | Entrainment, Tempo & Attention Modulation | 11D | Multi-scale neural oscillation synchronization modulates attention |
| β5 | **HGSIC** | Hierarchical Groove State Integration Circuit | 11D | Multi-level rhythmic integration creates groove perception |
| β6 | **OMS** | Oscillatory Motor Synchronization | 10D | Beta/gamma motor-auditory coupling enables temporal synchronization |

#### Tier γ — Speculative (5 models)

| ID | Code | Full Name | Output | Core Claim |
|----|------|-----------|--------|------------|
| γ1 | **TMRM** | Tempo Memory Reproduction Method | 10D | Sensory feedback enhances tempo memory accuracy (d=2.76) |
| γ2 | **NEWMD** | Neural Entrainment-Working Memory Dissociation | 10D | Stronger SS-EP correlates with worse tapping (β=−0.060) |
| γ3 | **MTNE** | Music Training Neural Efficiency | 10D | Music training improves executive function with decreased activation (d=0.60) |
| γ4 | **PTGMP** | Piano Training Grey Matter Plasticity | 10D | Piano training increases DLPFC + cerebellum grey matter (d=0.34) |
| γ5 | **MPFS** | Musical Prodigy Flow State | 10D | Prodigies distinguished by flow propensity, not IQ (r=0.47) |

**STU Total: 150D**

---

### 3.3 IMU — Integrative Memory Unit (15 models)

> Brain regions: Hippocampus, mPFC, entorhinal cortex, posterior cingulate, precuneus, ACC
> Function: Encoding, consolidation, retrieval of musical memories in autobiographical context

#### Tier α — Mechanistic (3 models)

| ID | Code | Full Name | Output | Core Claim |
|----|------|-----------|--------|------------|
| α1 | **MEAMN** | Music-Evoked Autobiographical Memory Network | 12D | Music uniquely activates hippocampus-mPFC for autobiographical retrieval |
| α2 | **PNH** | Pythagorean Neural Hierarchy | 11D | Neural encoding preserves harmonic hierarchy (octave > fifth > fourth) |
| α3 | **MMP** | Musical Mnemonic Preservation | 12D | Musical memory survives AD even when verbal memory fails |

#### Tier β — Integrative (9 models)

| ID | Code | Full Name | Output | Core Claim |
|----|------|-----------|--------|------------|
| β1 | **RASN** | Rhythmic Auditory Stimulation Neuroplasticity | 11D | RAS induces neuroplastic changes in motor/sensory circuits |
| β2 | **PMIM** | Predictive Memory Integration Model | 11D | ERAN/MMN reflect hierarchical prediction error signals |
| β3 | **OII** | Oscillatory Intelligence Integration | 10D | Musical aptitude correlates with neural oscillatory patterns + Gf |
| β4 | **HCMC** | Hippocampal-Cortical Memory Circuit | 11D | Musical memory requires hippocampal-cortical dialogue |
| β5 | **RIRI** | RAS-Intelligent Rehabilitation Integration | 10D | RAS + VR + robotics > RAS alone for motor recovery |
| β6 | **MSPBA** | Musical Syntax Processing in Broca's Area | 11D | Harmonic violations elicit mERAN in BA 44 (domain-general syntax) |
| β7 | **VRIAP** | VR-Induced Analgesia Active-Passive | 10D | Active VR + music shows better analgesic effect than passive |
| β8 | **TPRD** | Tonotopy-Pitch Representation Dissociation | 10D | Primary HGs = spectral content; nonprimary = pitch (perceptual) |
| β9 | **CMAPCC** | Cross-Modal Action-Perception Common Code | 10D | Unified perception-action code in right premotor cortex |

#### Tier γ — Speculative (3 models)

| ID | Code | Full Name | Output | Core Claim |
|----|------|-----------|--------|------------|
| γ1 | **DMMS** | Developmental Music Memory Scaffold | 10D | Early musical exposure establishes lifelong memory scaffolds |
| γ2 | **CSSL** | Cross-Species Song Learning | 10D | Bird song learning shares mechanisms with human musical memory (r=0.94) |
| γ3 | **CDEM** | Context-Dependent Emotional Memory | 10D | Musical emotional memories modulated by cross-modal context |

**IMU Total: 159D**

---

### 3.4 ARU — Affective Resonance Unit (10 models)

> Brain regions: NAcc, VTA, caudate, amygdala, insula, vmPFC, SMA, STG
> Function: Emotional and reward processing for music

#### Tier α — Mechanistic (3 models)

| ID | Code | Full Name | Output | Status | Core Claim |
|----|------|-----------|--------|--------|------------|
| α1 | **SRP** | Striatal Reward Pathway | 19D | **DONE** | Dopaminergic pleasure: anticipation (caudate) → consummation (NAcc) |
| α2 | **AAC** | Autonomic-Affective Coupling | 14D | **Spec done** | ANS physiology: SCR, HR, respiration, chills intensity |
| α3 | **VMM** | Valence-Mode Mapping | 12D | **Spec done** | Major/minor → valence via mode-dependent neural pathways |

#### Tier β — Integrative (4 models)

| ID | Code | Full Name | Output | Core Claim |
|----|------|-----------|--------|------------|
| β1 | **PUPF** | Predictive Uncertainty-Pleasure Function | 12D | P(H,S) = Goldilocks principle: optimal pleasure at intermediate surprise × uncertainty |
| β2 | **CLAM** | Closed-Loop Affective Modulation | 11D | Bidirectional brain-music affective loop (arousal r=0.74, valence r=0.52) |
| β3 | **MAD** | Musical Anhedonia Disconnection | 11D | Specific anhedonia from NAcc-STG structural disconnection (d=−5.89) |
| β4 | **NEMAC** | Nostalgia-Enhanced Memory-Affect Circuit | 11D | Self-selected nostalgic music activates mPFC-hippocampus (d=0.88) |

#### Tier γ — Speculative (3 models)

| ID | Code | Full Name | Output | Core Claim |
|----|------|-----------|--------|------------|
| γ1 | **DAP** | Developmental Affective Plasticity | 10D | Early music exposure shapes affective circuit development |
| γ2 | **CMAT** | Cross-Modal Affective Transfer | 10D | Affect learned in one modality transfers to music via mPFC/OFC/Insula |
| γ3 | **TAR** | Therapeutic Affective Resonance | 10D | Targeted acoustic-neural pathways for pathological affective states |

**ARU Total: 120D**

---

### 3.5 Summary Table

| Unit | α | β | γ | Total Models | Total Dims |
|------|---|---|---|-------------|-----------|
| SPU | 3 (35D) | 3 (33D) | 3 (31D) | **9** | **99D** |
| STU | 3 (37D) | 6 (63D) | 5 (50D) | **14** | **150D** |
| IMU | 3 (35D) | 9 (94D) | 3 (30D) | **15** | **159D** |
| ARU | 3 (45D) | 4 (45D) | 3 (30D) | **10** | **120D** |
| **Total** | **12** | **22** | **14** | **48** | **528D** |

---

## 4. Target Architecture

### 4.1 Full Pipeline

```
Audio (44.1kHz waveform)
    │
    ▼
┌─────────────────────────── EAR ──────────────────────────────┐
│                                                               │
│  Cochlea ─────► R³ Spectral ─────► H³ Temporal               │
│  audio→mel      mel→49D/frame      R³×time→sparse scalars    │
│  (128 bins)     (172.27 Hz)        (demand-driven)           │
│                                                               │
└───────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────── BRAIN ─────────────────────────────┐
│                                                               │
│  ┌─ PERCEPTUAL CIRCUIT (SPU) ──────────────────────────────┐ │
│  │  Mechanisms: PPC (30D), TPC (30D)                       │ │
│  │  Models: BCH, PSCL, PCCR, STAI, TSCP, MIAA,           │ │
│  │          SDNPS, ESME, SDED                              │ │
│  │  Total: 9 models → 99D                                  │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  ┌─ SENSORIMOTOR CIRCUIT (STU) ────────────────────────────┐ │
│  │  Mechanisms: BEP (30D), TMH (30D)                       │ │
│  │  Models: HMCE, AMSC, MDNS, AMSS, TPIO, EDTA,          │ │
│  │          ETAM, HGSIC, OMS, TMRM, NEWMD, MTNE,         │ │
│  │          PTGMP, MPFS                                    │ │
│  │  Total: 14 models → 150D                                │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  ┌─ MNEMONIC CIRCUIT (IMU) ────────────────────────────────┐ │
│  │  Mechanisms: MEM (30D), SYN (30D)                       │ │
│  │  Models: MEAMN, PNH, MMP, RASN, PMIM, OII,            │ │
│  │          HCMC, RIRI, MSPBA, VRIAP, TPRD, CMAPCC,      │ │
│  │          DMMS, CSSL, CDEM                               │ │
│  │  Total: 15 models → 159D                                │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  ┌─ MESOLIMBIC CIRCUIT (ARU) ──────────────────────────────┐ │
│  │  Mechanisms: AED (30D), CPD (30D), C0P (30D)  ✓ DONE   │ │
│  │  Models: SRP ✓, AAC, VMM, PUPF, CLAM, MAD,            │ │
│  │          NEMAC, DAP, CMAT, TAR                          │ │
│  │  Total: 10 models → 120D                                │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  ┌─ SALIENCE CIRCUIT (shared) ─────────────────────────────┐ │
│  │  Mechanisms: ASA (30D)  ✓ DONE                          │ │
│  │  Available to: AAC, and any model needing scene analysis │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
│  ┌─ CROSS-UNIT PATHWAYS ───────────────────────────────────┐ │
│  │  P1: SPU → ARU (Consonance → Pleasure)     r=0.81-0.84 │ │
│  │  P2: STU internal (Beat → Motor)            r=0.70      │ │
│  │  P3: IMU → ARU (Music → Autobiographical Memory)        │ │
│  │  P4: STU internal (Temporal Hierarchy → Prediction) 0.99│ │
│  │  P5: STU → ARU (Tempo → Emotion)            moderate    │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                               │
└───────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────── LANGUAGE ──────────────────────────┐
│                                                               │
│  L³ Semantic Spaces — one per model                          │
│  Each model output → human-readable interpretation            │
│                                                               │
└───────────────────────────────────────────────────────────────┘
    │
    ▼
  528D total output per frame (172.27 Hz)
    SPU:  99D (spectral cognition)
    STU: 150D (timing & motor)
    IMU: 159D (memory & syntax)
    ARU: 120D (affect & reward)
```

### 4.2 Key Architectural Principles

**Mechanism isolation**: Each circuit has its own mechanisms. No mechanism is shared across
circuits except ASA (salience), which serves as a cross-circuit utility.

**Intra-circuit sharing**: Within a circuit, mechanisms are shared across models:
- Mesolimbic: AED, CPD, C0P shared by SRP, AAC, VMM, PUPF, etc.
- Perceptual: PPC, TPC shared by BCH, PSCL, PCCR, etc.

**DemandAggregator**: The pipeline automatically unions all active model demands:
```python
self._demand = DemandAggregator.from_models(self.models)
# Only computes H³ tuples that at least one model actually reads
```

**Mechanism-first, model-second**: Mechanisms compute once; models read from them multiple times.

---

## 5. Circuit-to-Unit Mapping

### 5.1 Six Brain Circuits

The MI pipeline organizes computation into six neural circuits, each with a physical
directory under `mi/brain/`:

```
mi/brain/
├── perceptual/          ← SPU (Spectral Processing)
│   ├── mechanisms/      PPC, TPC
│   ├── models/          BCH, PSCL, PCCR, STAI, TSCP, MIAA, SDNPS, ESME, SDED
│   └── units/           SPU aggregator
│
├── sensorimotor/        ← STU (Sensorimotor Timing)
│   ├── mechanisms/      BEP, TMH
│   ├── models/          HMCE, AMSC, MDNS, AMSS, TPIO, EDTA, ETAM, HGSIC, OMS,
│   │                    TMRM, NEWMD, MTNE, PTGMP, MPFS
│   └── units/           STU aggregator
│
├── mnemonic/            ← IMU (Integrative Memory)
│   ├── mechanisms/      MEM, SYN
│   ├── models/          MEAMN, PNH, MMP, RASN, PMIM, OII, HCMC, RIRI, MSPBA,
│   │                    VRIAP, TPRD, CMAPCC, DMMS, CSSL, CDEM
│   └── units/           IMU aggregator
│
├── mesolimbic/          ← ARU (Affective Resonance)  ✓ EXISTS
│   ├── mechanisms/      AED ✓, CPD ✓, C0P ✓
│   ├── models/          SRP ✓, AAC, VMM, PUPF, CLAM, MAD, NEMAC, DAP, CMAT, TAR
│   └── units/           ARU ✓
│
├── salience/            ← Shared utility circuit  ✓ EXISTS
│   ├── mechanisms/      ASA ✓
│   ├── models/          (none — ASA serves other models)
│   └── units/           (none)
│
└── imagery/             ← Reserved for future (PCU, etc.)
    ├── mechanisms/
    ├── models/
    └── units/
```

### 5.2 Circuit Rationale

| Circuit | Unit(s) | Neural Basis | Why Separate |
|---------|---------|-------------|-------------|
| **Perceptual** | SPU | A1, Heschl's, IC | Subcortical → cortical pitch pathway, distinct from timing/affect |
| **Sensorimotor** | STU | SMA, cerebellum, M1, BG | Motor network, entrainment, temporal prediction |
| **Mnemonic** | IMU | Hippocampus, mPFC, EC | Memory systems, syntactic processing, consolidation |
| **Mesolimbic** | ARU | NAcc, VTA, caudate, amygdala | Reward/dopamine circuitry, emotional processing |
| **Salience** | (shared) | Anterior insula, dACC, TPJ | Scene analysis, attention capture — utility for all circuits |
| **Imagery** | (future) | Secondary auditory, DLPFC | Mental simulation, future expansion |

---

## 6. New Mechanisms Design

### 6.1 Overview

Currently: 4 mechanisms (AED, CPD, C0P, ASA) = 120D
Target: 10 mechanisms total = 300D

| # | Mechanism | Circuit | Output | Horizons | Function |
|---|-----------|---------|--------|----------|----------|
| 1 | **AED** | Mesolimbic | 30D | H6, H16 | Affective entrainment, ITPRA | ✓ |
| 2 | **CPD** | Mesolimbic | 30D | H7, H12, H15 | Chills & peak detection | ✓ |
| 3 | **C0P** | Mesolimbic | 30D | H11 | Cognitive projection, reward | ✓ |
| 4 | **ASA** | Salience | 30D | H9 | Auditory scene analysis | ✓ |
| 5 | **PPC** | Perceptual | 30D | H0, H3, H6 | Pitch processing chain | NEW |
| 6 | **TPC** | Perceptual | 30D | H2, H5, H8 | Timbre processing chain | NEW |
| 7 | **BEP** | Sensorimotor | 30D | H6, H11, H16 | Beat entrainment processing | NEW |
| 8 | **TMH** | Sensorimotor | 30D | H8, H14, H20 | Temporal memory hierarchy | NEW |
| 9 | **MEM** | Mnemonic | 30D | H16, H20, H24 | Memory encoding / retrieval | NEW |
| 10 | **SYN** | Mnemonic | 30D | H10, H14, H18 | Syntactic processing | NEW |

### 6.2 PPC — Pitch Processing Chain (Perceptual Circuit)

**Function**: Brainstem → cortical pitch pathway. Extracts pitch salience,
harmonicity, consonance hierarchy at the fastest timescales.

**Horizons**: H0 (5.8ms cochlear), H3 (23.2ms brainstem), H6 (200ms beat-level)
- H0: Immediate cochlear response (FFR timescale)
- H3: Brainstem processing window (IC response)
- H6: Beat-level pitch integration

**Sub-sections** (30D):
```
Pitch Salience      [0:10]   — NPS, harmonicity, fundamental tracking
Consonance Encoding [10:20]  — interval hierarchy, roughness, fusion
Chroma Processing   [20:30]  — pitch class, octave equivalence, tonal center
```

**H³ Demand** (~15 unique morph-law pairs × 3 horizons = ~45 scalars):
- M0 (value): raw pitch/consonance values
- M1 (mean): averaged consonance over window
- M4 (max): peak consonance
- M5 (range): pitch range
- M8 (velocity): pitch change rate
- M14 (periodicity): harmonic regularity
- M15 (smoothness): spectral continuity

**Key R³ inputs**: Consonance group (R3[0:7]) — Plomp-Levelt, Helmholtz-Kang, Stumpf fusion,
periodicity, tristimulus ratios.

**Models served**: BCH, PSCL, PCCR, STAI, SDNPS, ESME, SDED (7 of 9 SPU models)

```python
class PPC(BaseMechanism):
    NAME = "PPC"
    FULL_NAME = "Pitch Processing Chain"
    OUTPUT_DIM = 30
    HORIZONS = (0, 3, 6)
    SUB_SECTIONS = (
        SubSection("pitch_salience", 0, 10),
        SubSection("consonance_encoding", 10, 20),
        SubSection("chroma_processing", 20, 30),
    )
```

---

### 6.3 TPC — Timbre Processing Chain (Perceptual Circuit)

**Function**: Spectral envelope → instrument identity → timbre space.
Captures the "what" of sound beyond pitch.

**Horizons**: H2 (17.4ms onset), H5 (46.4ms attack), H8 (300ms timbre integration)
- H2: Sub-onset transient (attack detection)
- H5: Attack integration window
- H8: Full timbre perception window (~300ms for instrument ID)

**Sub-sections** (30D):
```
Spectral Envelope   [0:10]   — brightness, warmth, sharpness, spectral shape
Instrument Identity [10:20]  — timbre space coordinates, formant tracking
Plasticity Markers  [20:30]  — training effects, imagery overlap, adaptation
```

**H³ Demand** (~14 unique morph-law pairs × 3 horizons = ~42 scalars):
- M0 (value): raw timbre values
- M1 (mean): timbre stability
- M3 (std): timbre variation
- M5 (range): dynamic range
- M6 (velocity): timbre change
- M12 (zero crossings): spectral transitions
- M16 (centroid): spectral center of mass

**Key R³ inputs**: Timbre group (R3[12:21]) — brightness, warmth, sharpness, roughness,
spectral centroid, spectral flatness, spectral rolloff.

**Models served**: TSCP, MIAA, STAI, PCCR, SDNPS, ESME, SDED (7 of 9 SPU models)

```python
class TPC(BaseMechanism):
    NAME = "TPC"
    FULL_NAME = "Timbre Processing Chain"
    OUTPUT_DIM = 30
    HORIZONS = (2, 5, 8)
    SUB_SECTIONS = (
        SubSection("spectral_envelope", 0, 10),
        SubSection("instrument_identity", 10, 20),
        SubSection("plasticity_markers", 20, 30),
    )
```

---

### 6.4 BEP — Beat Entrainment Processing (Sensorimotor Circuit)

**Function**: Beat induction, meter extraction, groove detection.
The "when" of music — temporal regularity and motor synchronization.

**Horizons**: H6 (200ms beat), H11 (500ms psychological present), H16 (1000ms bar)
- H6: Single beat level (120-300 BPM range)
- H11: Pöppel's psychological present (Pöppel 1997)
- H16: Bar-level meter integration

**Sub-sections** (30D):
```
Beat Induction      [0:10]   — beat strength, tempo, phase, regularity
Meter Extraction    [10:20]  — meter, syncopation, accent pattern, groove
Motor Entrainment   [20:30]  — movement urge, synchronization precision, coupling
```

**H³ Demand** (~18 unique morph-law pairs × 3 horizons = ~54 scalars):
- M4 (max): beat peak detection
- M8 (velocity): tempo dynamics
- M9 (acceleration): tempo change
- M14 (periodicity): beat regularity
- M15 (smoothness): groove quality
- M17 (peaks): beat count per window
- M18 (trend): tempo trend

**Key R³ inputs**: Energy group (R3[7:12]) — loudness, spectral centroid, spectral flux;
Change group (R3[21:25]) — spectral change, energy change.

**Models served**: All 14 STU models (HMCE, AMSC, MDNS, AMSS, TPIO, EDTA, ETAM, HGSIC,
OMS, TMRM, NEWMD, MTNE, PTGMP, MPFS)

```python
class BEP(BaseMechanism):
    NAME = "BEP"
    FULL_NAME = "Beat Entrainment Processing"
    OUTPUT_DIM = 30
    HORIZONS = (6, 11, 16)
    SUB_SECTIONS = (
        SubSection("beat_induction", 0, 10),
        SubSection("meter_extraction", 10, 20),
        SubSection("motor_entrainment", 20, 30),
    )
```

---

### 6.5 TMH — Temporal Memory Hierarchy (Sensorimotor Circuit)

**Function**: Multi-scale context encoding at phrase, section, and form levels.
Captures the "where in the piece" sense that enables prediction.

**Horizons**: H8 (300ms motif), H14 (700ms phrase), H20 (5s section)
- H8: Motif-level context (2-5 notes)
- H14: Phrase-level context (Lerdahl's GTTM grouping)
- H20: Section-level context (verse/chorus structure)

**Sub-sections** (30D):
```
Short Context       [0:10]   — motif features, onset patterns, local prediction
Medium Context      [10:20]  — phrase boundaries, cadence detection, progression
Long Context        [20:30]  — formal structure, return detection, global prediction
```

**H³ Demand** (~16 unique morph-law pairs × 3 horizons = ~48 scalars):
- M1 (mean): context average
- M3 (std): context variability
- M8 (velocity): dynamics within context
- M11 (acceleration): rate of change
- M13 (entropy): context unpredictability
- M18 (trend): directional tendency
- M22 (autocorrelation): self-similarity

**Key R³ inputs**: All groups — context requires spectral + energy + change features.

**Models served**: HMCE, AMSC, AMSS, ETAM, HGSIC, TMRM, NEWMD (7 of 14 STU models)

```python
class TMH(BaseMechanism):
    NAME = "TMH"
    FULL_NAME = "Temporal Memory Hierarchy"
    OUTPUT_DIM = 30
    HORIZONS = (8, 14, 20)
    SUB_SECTIONS = (
        SubSection("short_context", 0, 10),
        SubSection("medium_context", 10, 20),
        SubSection("long_context", 20, 30),
    )
```

---

### 6.6 MEM — Memory Encoding & Retrieval (Mnemonic Circuit)

**Function**: Hippocampal binding, familiarity detection, episodic encoding.
Bridges musical features to autobiographical memory systems.

**Horizons**: H16 (1s encoding window), H20 (5s consolidation), H24 (36s retrieval)
- H16: Immediate encoding (working memory timescale)
- H20: Short-term consolidation (hippocampal binding window)
- H24: Long-term retrieval context (36s episodic chunk)

**Sub-sections** (30D):
```
Encoding State      [0:10]   — novelty, binding strength, schema match
Familiarity Proxy   [10:20]  — recognition signal, nostalgia, déjà-vu
Retrieval Dynamics  [20:30]  — recall probability, vividness, emotional coloring
```

**H³ Demand** (~14 unique morph-law pairs × 3 horizons = ~42 scalars):
- M1 (mean): stability (familiarity proxy)
- M3 (std): variability (novelty proxy)
- M5 (range): dynamic range over memory window
- M13 (entropy): unpredictability (surprise)
- M19 (stability): temporal stability
- M22 (autocorrelation): repetition detection

**Key R³ inputs**: Consonance (R3[0:7]) for harmonic recognition, Interactions (R3[25:49])
for cross-feature binding.

**Models served**: MEAMN, MMP, HCMC, RASN, RIRI, VRIAP, DMMS, CSSL, CDEM (9 of 15 IMU models)

```python
class MEM(BaseMechanism):
    NAME = "MEM"
    FULL_NAME = "Memory Encoding and Retrieval"
    OUTPUT_DIM = 30
    HORIZONS = (16, 20, 24)
    SUB_SECTIONS = (
        SubSection("encoding_state", 0, 10),
        SubSection("familiarity_proxy", 10, 20),
        SubSection("retrieval_dynamics", 20, 30),
    )
```

---

### 6.7 SYN — Syntactic Processing (Mnemonic Circuit)

**Function**: Harmonic syntax, prediction error (ERAN/MMN), structural expectation.
Captures rule-based musical processing (Koelsch 2014, Lerdahl's GTTM).

**Horizons**: H10 (400ms chord), H14 (700ms progression), H18 (2s phrase)
- H10: Single chord processing window
- H14: Chord progression (2-4 chords)
- H18: Phrase-level harmonic arc (I-IV-V-I)

**Sub-sections** (30D):
```
Harmonic Syntax     [0:10]   — chord function, progression regularity, key stability
Prediction Error    [10:20]  — ERAN amplitude, MMN proxy, surprise magnitude
Structural Expect   [20:30]  — cadence expectation, resolution probability, closure
```

**H³ Demand** (~15 unique morph-law pairs × 3 horizons = ~45 scalars):
- M0 (value): current harmonic state
- M1 (mean): tonal center proxy
- M8 (velocity): harmonic rhythm
- M13 (entropy): harmonic unpredictability
- M14 (periodicity): cadential regularity
- M18 (trend): harmonic direction

**Key R³ inputs**: Consonance (R3[0:7]) — the backbone of harmonic analysis.

**Models served**: PNH, PMIM, OII, MSPBA, TPRD, CMAPCC (6 of 15 IMU models)

```python
class SYN(BaseMechanism):
    NAME = "SYN"
    FULL_NAME = "Syntactic Processing"
    OUTPUT_DIM = 30
    HORIZONS = (10, 14, 18)
    SUB_SECTIONS = (
        SubSection("harmonic_syntax", 0, 10),
        SubSection("prediction_error", 10, 20),
        SubSection("structural_expect", 20, 30),
    )
```

---

### 6.8 Mechanism Summary

```
MECHANISM TOPOLOGY — 10 mechanisms, 300D total

PERCEPTUAL CIRCUIT          SENSORIMOTOR CIRCUIT
┌─────────────────┐         ┌─────────────────┐
│ PPC (30D)       │         │ BEP (30D)       │
│ H0, H3, H6     │         │ H6, H11, H16    │
│ Pitch/consonance│         │ Beat/meter/groove│
├─────────────────┤         ├─────────────────┤
│ TPC (30D)       │         │ TMH (30D)       │
│ H2, H5, H8     │         │ H8, H14, H20    │
│ Timbre/identity │         │ Context/structure│
└─────────────────┘         └─────────────────┘

MNEMONIC CIRCUIT            MESOLIMBIC CIRCUIT         SALIENCE
┌─────────────────┐         ┌─────────────────┐       ┌──────────────┐
│ MEM (30D)       │         │ AED (30D) ✓     │       │ ASA (30D) ✓  │
│ H16, H20, H24  │         │ H6, H16         │       │ H9           │
│ Memory/encoding │         │ Affect/ITPRA    │       │ Scene/salience│
├─────────────────┤         ├─────────────────┤       └──────────────┘
│ SYN (30D)       │         │ CPD (30D) ✓     │
│ H10, H14, H18  │         │ H7, H12, H15   │
│ Syntax/predict  │         │ Chills/peaks    │
└─────────────────┘         ├─────────────────┤
                            │ C0P (30D) ✓     │
                            │ H11             │
                            │ Cognitive/reward │
                            └─────────────────┘
```

**Horizon Usage Map** (which mechanisms share horizons):

| Horizon | ms | PPC | TPC | BEP | TMH | MEM | SYN | AED | CPD | C0P | ASA |
|---------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| H0 | 5.8 | ● | | | | | | | | | |
| H2 | 17.4 | | ● | | | | | | | | |
| H3 | 23.2 | ● | | | | | | | | | |
| H5 | 46.4 | | ● | | | | | | | | |
| H6 | 200 | ● | | ● | | | | ● | | | |
| H7 | 250 | | | | | | | | ● | | |
| H8 | 300 | | ● | | ● | | | | | | |
| H9 | 350 | | | | | | | | | | ● |
| H10 | 400 | | | | | | ● | | | | |
| H11 | 450 | | | ● | | | | | | ● | |
| H12 | 525 | | | | | | | | ● | | |
| H14 | 700 | | | | ● | | ● | | | | |
| H15 | 800 | | | | | | | | ● | | |
| H16 | 1000 | | | ● | | ● | | ● | | | |
| H18 | 2000 | | | | | | ● | | | | |
| H20 | 5000 | | | | ● | ● | | | | | |
| H24 | 36000 | | | | | ● | | | | | |

**Total unique horizons used**: 17 of 32

---

## 7. Phased Implementation

### Phase 0: Foundation (current — DONE)

**What's built**: EAR (R³+H³) + 4 mechanisms + SRP (19D) + SRP Semantics

| Deliverable | Status |
|------------|--------|
| Cochlea, R³, H³ | ✓ Done |
| AED, CPD, C0P, ASA mechanisms | ✓ Done |
| SRP model (19D) | ✓ Done |
| SRP semantics (45D) | ✓ Done |
| 79 tests | ✓ Passing |

---

### Phase 1: Complete ARU — Mesolimbic Circuit

**Goal**: Implement remaining 9 ARU models (AAC already spec'd)
**New mechanisms**: None (AED, CPD, C0P, ASA already exist)
**Priority**: Highest — all mechanisms exist, lowest friction

#### Phase 1a: AAC (α2) — Autonomic-Affective Coupling

| Task | Files | Output |
|------|-------|--------|
| AAC model code | `mi/brain/mesolimbic/models/aac.py` | 14D |
| AAC semantics | `mi/language/aac/` | ~26D |
| Pipeline integration | Update `mi/pipeline/mi.py` | SRP+AAC |
| Tests | `tests/brain/mesolimbic/test_aac.py` | ~15 tests |

**Mechanisms used**: AED + CPD + ASA (already done)
**Config update**: `active_models = ("SRP", "AAC")`

#### Phase 1b: VMM (α3) — Valence-Mode Mapping

| Task | Files | Output |
|------|-------|--------|
| VMM model code | `mi/brain/mesolimbic/models/vmm.py` | 12D |
| VMM semantics | `mi/language/vmm/` | ~18D |
| Tests | `tests/brain/mesolimbic/test_vmm.py` | ~10 tests |

**Mechanisms used**: AED + C0P (mode → valence via affective state)
**Key formula**: Major-mode index from R³ consonance + H³ pitch stability

#### Phase 1c: β-tier ARU Models (PUPF, CLAM, MAD, NEMAC)

| Model | Mechanisms | Output | Unique Feature |
|-------|-----------|--------|----------------|
| PUPF | AED + CPD + C0P | 12D | P(H,S) Goldilocks function |
| CLAM | AED + CPD | 11D | Bidirectional affect loop |
| MAD | AED + C0P | 11D | Disconnection indicator (NAcc-STG) |
| NEMAC | AED + CPD + C0P | 11D | Nostalgia-memory coupling |

#### Phase 1d: γ-tier ARU Models (DAP, CMAT, TAR)

| Model | Mechanisms | Output | Unique Feature |
|-------|-----------|--------|----------------|
| DAP | AED | 10D | Developmental trajectory proxy |
| CMAT | AED + C0P | 10D | Cross-modal transfer indicator |
| TAR | AED + CPD + C0P | 10D | Therapeutic potential score |

**Phase 1 Total**: 10 models, 120D output, ~60 tests
**Phase 1 Timeline**: All mechanisms exist → models are pure compute formulas

---

### Phase 2: SPU — Perceptual Circuit

**Goal**: Implement 9 SPU models + 2 new mechanisms (PPC, TPC)
**New mechanisms**: PPC (Pitch Processing Chain), TPC (Timbre Processing Chain)
**Priority**: High — spectral features are the foundation all other units build upon

#### Phase 2a: PPC + TPC Mechanisms

| Task | Files | Output |
|------|-------|--------|
| PPC mechanism | `mi/brain/perceptual/mechanisms/ppc.py` | 30D |
| TPC mechanism | `mi/brain/perceptual/mechanisms/tpc.py` | 30D |
| Mechanism tests | `tests/brain/perceptual/test_ppc.py`, `test_tpc.py` | ~10 tests |
| Circuit __init__ | `mi/brain/perceptual/__init__.py` | exports |

#### Phase 2b: α-tier SPU Models (BCH, PSCL, PCCR)

| Model | Mechanisms | Output | Key Science |
|-------|-----------|--------|-------------|
| BCH | PPC | 12D | FFR consonance hierarchy (r=0.81) |
| PSCL | PPC + TPC | 12D | Anterolateral Heschl's pitch salience |
| PCCR | PPC + TPC | 11D | Octave-independent chroma in non-primary AC |

#### Phase 2c: β-tier SPU Models (STAI, TSCP, MIAA)

| Model | Mechanisms | Output | Key Science |
|-------|-----------|--------|-------------|
| STAI | PPC + TPC | 12D | Inverted-U complexity preference |
| TSCP | TPC | 10D | Training-induced timbre plasticity (MEG) |
| MIAA | TPC | 11D | Imagery activates auditory cortex |

#### Phase 2d: γ-tier SPU Models (SDNPS, ESME, SDED)

| Model | Mechanisms | Output | Key Science |
|-------|-----------|--------|-------------|
| SDNPS | PPC | 10D | NPS fails for natural sounds |
| ESME | PPC + TPC | 11D | MMN expertise modulation (d=−1.09) |
| SDED | PPC | 10D | Early roughness detection |

**Phase 2 Total**: 9 models + 2 mechanisms, 99D output, ~40 tests

---

### Phase 3: STU — Sensorimotor Circuit

**Goal**: Implement 14 STU models + 2 new mechanisms (BEP, TMH)
**New mechanisms**: BEP (Beat Entrainment Processing), TMH (Temporal Memory Hierarchy)
**Priority**: Medium — largest model count, requires new timing mechanisms

#### Phase 3a: BEP + TMH Mechanisms

| Task | Files | Output |
|------|-------|--------|
| BEP mechanism | `mi/brain/sensorimotor/mechanisms/bep.py` | 30D |
| TMH mechanism | `mi/brain/sensorimotor/mechanisms/tmh.py` | 30D |
| Mechanism tests | `tests/brain/sensorimotor/test_bep.py`, `test_tmh.py` | ~10 tests |

#### Phase 3b: α-tier STU Models (HMCE, AMSC, MDNS)

| Model | Mechanisms | Output | Key Science |
|-------|-----------|--------|-------------|
| HMCE | TMH | 13D | Anatomical context gradient (r=0.99) |
| AMSC | BEP + TMH | 12D | Dual-stream auditory processing (r=0.70) |
| MDNS | BEP + TMH | 12D | Melody decodable from EEG |

#### Phase 3c: β-tier STU Models (6 models)

| Model | Mechanisms | Output | Key Science |
|-------|-----------|--------|-------------|
| AMSS | TMH | 11D | Attention modulates stream segregation |
| TPIO | TPC* + TMH | 10D | Timbre perception-imagery overlap |
| EDTA | BEP | 10D | Musicians > non-musicians in timing |
| ETAM | BEP + TMH | 11D | Multi-scale oscillatory entrainment |
| HGSIC | BEP | 11D | Groove from optimal complexity |
| OMS | BEP | 10D | Beta/gamma motor-auditory coupling |

*TPIO cross-references TPC from perceptual circuit (cross-circuit read)

#### Phase 3d: γ-tier STU Models (5 models)

| Model | Mechanisms | Output | Key Science |
|-------|-----------|--------|-------------|
| TMRM | BEP | 10D | Sensory feedback > motor-only (d=2.76) |
| NEWMD | BEP + TMH | 10D | Entrainment-WM paradox (β=−0.060) |
| MTNE | TMH | 10D | Training = neural efficiency (d=0.60) |
| PTGMP | TMH | 10D | Grey matter plasticity (d=0.34) |
| MPFS | BEP + TMH | 10D | Flow propensity, not IQ (r=0.47) |

**Phase 3 Total**: 14 models + 2 mechanisms, 150D output, ~60 tests

---

### Phase 4: IMU — Mnemonic Circuit

**Goal**: Implement 15 IMU models + 2 new mechanisms (MEM, SYN)
**New mechanisms**: MEM (Memory Encoding & Retrieval), SYN (Syntactic Processing)
**Priority**: Medium — largest dimension count, most β models

#### Phase 4a: MEM + SYN Mechanisms

| Task | Files | Output |
|------|-------|--------|
| MEM mechanism | `mi/brain/mnemonic/mechanisms/mem.py` | 30D |
| SYN mechanism | `mi/brain/mnemonic/mechanisms/syn.py` | 30D |
| Mechanism tests | `tests/brain/mnemonic/test_mem.py`, `test_syn.py` | ~10 tests |

#### Phase 4b: α-tier IMU Models (MEAMN, PNH, MMP)

| Model | Mechanisms | Output | Key Science |
|-------|-----------|--------|-------------|
| MEAMN | MEM | 12D | Hippocampus-mPFC autobiographical retrieval |
| PNH | SYN | 11D | Neural harmonic hierarchy preservation |
| MMP | MEM | 12D | Musical memory survives Alzheimer's |

#### Phase 4c: β-tier IMU Models (9 models)

| Model | Mechanisms | Output | Key Science |
|-------|-----------|--------|-------------|
| RASN | MEM + BEP* | 11D | Rhythmic stimulation neuroplasticity |
| PMIM | SYN | 11D | ERAN/MMN = hierarchical prediction error |
| OII | SYN + MEM | 10D | Aptitude ↔ oscillatory patterns + Gf |
| HCMC | MEM | 11D | Hippocampal-cortical dialogue for music memory |
| RIRI | MEM + BEP* | 10D | RAS + VR + robotics synergy |
| MSPBA | SYN | 11D | mERAN in Broca's area (domain-general syntax) |
| VRIAP | MEM | 10D | Active VR > passive for analgesia |
| TPRD | SYN + PPC* | 10D | Tonotopy ≠ pitch representation |
| CMAPCC | MEM + BEP* | 10D | Common perception-action code |

*Cross-circuit reads: BEP from sensorimotor, PPC from perceptual

#### Phase 4d: γ-tier IMU Models (DMMS, CSSL, CDEM)

| Model | Mechanisms | Output | Key Science |
|-------|-----------|--------|-------------|
| DMMS | MEM | 10D | Early exposure → lifelong scaffolds |
| CSSL | MEM | 10D | Cross-species song learning (r=0.94) |
| CDEM | MEM + AED* | 10D | Context-dependent emotional memory |

*Cross-circuit read: AED from mesolimbic

**Phase 4 Total**: 15 models + 2 mechanisms, 159D output, ~65 tests

---

### Phase 5: Cross-Unit Integration

**Goal**: Implement the 5 high-confidence pathways identified in the C³ meta-analysis,
enabling inter-circuit communication.

#### 5.1 Cross-Unit Pathway Module

```
mi/brain/pathways/
├── __init__.py
├── base.py               # BasePathway class
├── p1_consonance_pleasure.py   # SPU → ARU (r=0.81-0.84)
├── p2_beat_motor.py            # STU internal (r=0.70)
├── p3_music_memory.py          # IMU → ARU (preserved in AD)
├── p4_temporal_prediction.py   # STU internal (r=0.99)
└── p5_tempo_emotion.py         # STU → ARU (moderate-high)
```

#### 5.2 Pathway Specifications

| ID | Path | Correlation | Mechanism |
|----|------|-------------|-----------|
| **P1** | SPU → ARU | r=0.81–0.84 | BCH consonance → SRP pleasure via opioid_proxy |
| **P2** | STU internal | r=0.70 | BEP beat → motor entrainment coupling |
| **P3** | IMU → ARU | Preserved in AD | MEM retrieval → NEMAC nostalgia → SRP reward |
| **P4** | STU internal | r=0.99 | TMH context depth ↔ HMCE anatomical gradient |
| **P5** | STU → ARU | Moderate–high | BEP tempo → AED arousal → SRP valence |

#### 5.3 Implementation Pattern

```python
class BasePathway(ABC):
    NAME: str                    # "P1"
    SOURCE_UNIT: str             # "SPU"
    TARGET_UNIT: str             # "ARU"
    SOURCE_MODELS: Tuple[str]    # ("BCH",)
    TARGET_MODELS: Tuple[str]    # ("SRP",)
    CORRELATION: float           # 0.84

    @abstractmethod
    def compute(
        self,
        source_outputs: Dict[str, ModelOutput],
        target_outputs: Dict[str, ModelOutput],
    ) -> Tensor:
        """Compute pathway modulation signal."""
```

**Phase 5 Total**: 5 pathways, integration layer
**Phase 5 Depends on**: Phases 1-4 complete

---

### Phase Summary

| Phase | Content | Models | Mechanisms | Output | Tests | Dependencies |
|-------|---------|--------|------------|--------|-------|-------------|
| **0** | Foundation | 1 (SRP) | 4 | 19D | 79 | — | ✓ DONE |
| **1** | ARU complete | +9 | 0 new | +101D | +60 | Phase 0 |
| **2** | SPU | +9 | +2 (PPC,TPC) | +99D | +40 | Phase 0 |
| **3** | STU | +14 | +2 (BEP,TMH) | +150D | +60 | Phase 0 |
| **4** | IMU | +15 | +2 (MEM,SYN) | +159D | +65 | Phases 2,3 |
| **5** | Pathways | — | — | Pathway modulation | +25 | Phases 1-4 |
| **Total** | | **48** | **10** | **528D** | **~330** | |

**Recommended order**: Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5
(Phases 2 and 3 can run in parallel since they don't depend on each other)

---

## 8. Dimension Budget

### 8.1 Per-Unit Breakdown

```
528D TOTAL OUTPUT MANIFOLD
═══════════════════════════════════════════════════════════════

SPU [0:99]           99D   Spectral Processing
├── BCH  [0:12]      12D   α1 — Brainstem Consonance
├── PSCL [12:24]     12D   α2 — Pitch Salience Cortical
├── PCCR [24:35]     11D   α3 — Pitch Chroma
├── STAI [35:47]     12D   β1 — Spectral-Temporal Aesthetic
├── TSCP [47:57]     10D   β2 — Timbre Cortical Plasticity
├── MIAA [57:68]     11D   β3 — Musical Imagery Activation
├── SDNPS[68:78]     10D   γ1 — Stimulus-Dependent NPS
├── ESME [78:89]     11D   γ2 — Expertise MMN
└── SDED [89:99]     10D   γ3 — Sensory Dissonance

STU [99:249]        150D   Sensorimotor Timing
├── HMCE [99:112]    13D   α1 — Hierarchical Context
├── AMSC [112:124]   12D   α2 — Auditory-Motor Coupling
├── MDNS [124:136]   12D   α3 — Melody Decoding
├── AMSS [136:147]   11D   β1 — Attention-Modulated Stream
├── TPIO [147:157]   10D   β2 — Timbre Perception-Imagery
├── EDTA [157:167]   10D   β3 — Expertise Tempo Accuracy
├── ETAM [167:178]   11D   β4 — Entrainment-Tempo-Attention
├── HGSIC[178:189]   11D   β5 — Groove State Integration
├── OMS  [189:199]   10D   β6 — Oscillatory Motor Sync
├── TMRM [199:209]   10D   γ1 — Tempo Memory Reproduction
├── NEWMD[209:219]   10D   γ2 — Entrainment-WM Dissociation
├── MTNE [219:229]   10D   γ3 — Training Neural Efficiency
├── PTGMP[229:239]   10D   γ4 — Piano Training Plasticity
└── MPFS [239:249]   10D   γ5 — Musical Prodigy Flow

IMU [249:408]       159D   Integrative Memory
├── MEAMN[249:261]   12D   α1 — Autobiographical Memory
├── PNH  [261:272]   11D   α2 — Pythagorean Neural Hierarchy
├── MMP  [272:284]   12D   α3 — Musical Mnemonic Preservation
├── RASN [284:295]   11D   β1 — Rhythmic Stimulation
├── PMIM [295:306]   11D   β2 — Predictive Memory Integration
├── OII  [306:316]   10D   β3 — Oscillatory Intelligence
├── HCMC [316:327]   11D   β4 — Hippocampal-Cortical Circuit
├── RIRI [327:337]   10D   β5 — Rehab Integration
├── MSPBA[337:348]   11D   β6 — Broca's Syntax Processing
├── VRIAP[348:358]   10D   β7 — VR Analgesia
├── TPRD [358:368]   10D   β8 — Tonotopy-Pitch Dissociation
├── CMAPCC[368:378]  10D   β9 — Cross-Modal Action-Perception
├── DMMS [378:388]   10D   γ1 — Developmental Memory Scaffold
├── CSSL [388:398]   10D   γ2 — Cross-Species Song Learning
└── CDEM [398:408]   10D   γ3 — Context-Dependent Memory

ARU [408:528]       120D   Affective Resonance
├── SRP  [408:427]   19D   α1 — Striatal Reward  ✓ DONE
├── AAC  [427:441]   14D   α2 — Autonomic-Affective
├── VMM  [441:453]   12D   α3 — Valence-Mode Mapping
├── PUPF [453:465]   12D   β1 — Uncertainty-Pleasure
├── CLAM [465:476]   11D   β2 — Closed-Loop Affect
├── MAD  [476:487]   11D   β3 — Musical Anhedonia
├── NEMAC[487:498]   11D   β4 — Nostalgia-Memory-Affect
├── DAP  [498:508]   10D   γ1 — Developmental Plasticity
├── CMAT [508:518]   10D   γ2 — Cross-Modal Transfer
└── TAR  [518:528]   10D   γ3 — Therapeutic Resonance
```

### 8.2 Dimension Budget Summary

| Category | Current | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Total |
|----------|---------|---------|---------|---------|---------|-------|
| **Mechanisms** | 120D | 120D | 180D | 240D | 300D | 300D |
| **Model output** | 19D | 120D | 219D | 369D | 528D | 528D |
| **Semantic** | 45D | ~180D | ~330D | ~550D | ~790D | ~790D |

### 8.3 Output Dimension Per Tier

| Tier | Models | Total Dims | Avg Dims | % of Total |
|------|--------|-----------|----------|-----------|
| α | 12 | 154D | 12.8D | 29.2% |
| β | 22 | 234D | 10.6D | 44.3% |
| γ | 14 | 140D | 10.0D | 26.5% |
| **All** | **48** | **528D** | **11.0D** | **100%** |

---

## 9. H³ Demand Expansion

### 9.1 Current Demand

SRP + ASA (for AAC) use 11 horizons out of 32:
```
Active: H6, H7, H9, H11, H12, H15, H16, H18, H20, H22
Total scalars: ~140 (sparse demand, 2.3% of theoretical 2304D)
```

### 9.2 Full 48-Model Demand

With all 10 mechanisms, the demand expands to 17 horizons:
```
NEW:     H0, H2, H3, H5, H8, H10, H14, H24
SHARED:  H6, H7, H9, H11, H12, H15, H16, H18, H20, H22
Total:   17 horizons

Estimated scalars:
  Existing:  ~140 (AED+CPD+C0P+ASA + SRP direct)
  PPC:       ~45 (15 pairs × 3 horizons)
  TPC:       ~42 (14 pairs × 3 horizons)
  BEP:       ~54 (18 pairs × 3 horizons)
  TMH:       ~48 (16 pairs × 3 horizons)
  MEM:       ~42 (14 pairs × 3 horizons)
  SYN:       ~45 (15 pairs × 3 horizons)
  Model direct reads: ~80 (est. across 48 models)
  ────────────────────────────
  Total: ~500 unique (h, m, l) tuples
  Coverage: 500/2304 = 21.7% of theoretical H³ space
```

### 9.3 Demand Aggregation

The DemandAggregator automatically handles deduplication:

```python
# Before (Phase 0): ~140 tuples, 11 horizons
demand = DemandAggregator.from_models({"SRP": srp})

# After (Phase 5): ~500 tuples, 17 horizons
demand = DemandAggregator.from_models({
    "SRP": srp, "AAC": aac, "VMM": vmm, ...,   # ARU
    "BCH": bch, "PSCL": pscl, ...,              # SPU
    "HMCE": hmce, "AMSC": amsc, ...,            # STU
    "MEAMN": meamn, "PNH": pnh, ...,            # IMU
})
```

**Performance impact**: H³ computation scales with unique tuple count, not model count.
Going from 140 → 500 tuples is ~3.6× more H³ work, but H³ is already fast
(windowed morph computation, no learned parameters).

---

## 10. R³ Feature Coverage

### 10.1 R³ Groups (49D)

| Group | Range | Dim | Features |
|-------|-------|-----|----------|
| **A: Consonance** | R3[0:7] | 7D | Plomp-Levelt, Sethares, Helmholtz-Kang, Stumpf, periodicity, tristimulus |
| **B: Energy** | R3[7:12] | 5D | Loudness, spectral centroid, spectral flux, RMS, spectral bandwidth |
| **C: Timbre** | R3[12:21] | 9D | Brightness, warmth, sharpness, roughness, spectral flatness, rolloff, ... |
| **D: Change** | R3[21:25] | 4D | Spectral change, energy change, pitch change, timbre change |
| **E: Interactions** | R3[25:49] | 24D | Cross-feature correlations (A×B, A×C, B×C, ...) |

### 10.2 Unit → R³ Group Mapping

| Unit | Primary R³ Groups | Key Features |
|------|-------------------|-------------|
| **SPU** | **A (Consonance)**, C (Timbre) | Harmonicity, pitch salience, roughness, spectral shape |
| **STU** | **B (Energy)**, D (Change) | Loudness dynamics, spectral flux, onset detection |
| **IMU** | A (Consonance), **E (Interactions)** | Harmonic syntax, cross-feature binding, familiarity |
| **ARU** | A, B, C, D, E (all) | Full spectral context for affect computation |

### 10.3 R³ Feature Utilization Matrix

```
Feature             │ SPU │ STU │ IMU │ ARU │ Total
────────────────────┼─────┼─────┼─────┼─────┼──────
Consonance [0:7]    │ ●●● │  ●  │ ●●  │ ●●  │  9
Energy [7:12]       │  ●  │ ●●● │  ●  │ ●●  │  8
Timbre [12:21]      │ ●●● │  ●  │  ●  │  ●  │  6
Change [21:25]      │  ●  │ ●●● │  ●  │ ●●  │  7
Interactions [25:49]│  ●  │  ●  │ ●●● │ ●●  │  7
────────────────────┼─────┼─────┼─────┼─────┼──────
Total features used │ ~30 │ ~25 │ ~28 │ ~40 │ ~49

● = light use   ●● = moderate   ●●● = primary
```

All 49 R³ features are utilized across the 48-model system. No features are wasted.

---

## 11. Cross-Unit Pathways

### 11.1 Five High-Confidence Pathways

The C³ meta-analysis identifies five pathways with correlational evidence
(all require future experimental validation for causal claims):

#### P1: Consonance → Pleasure (SPU → ARU)

```
BCH.consonance_hierarchy ──── r=0.81-0.84 ────► SRP.opioid_proxy
    (pitch salience)                              (pleasure from consonance)

Mechanism: FFR magnitude → NAcc-mediated pleasure
Evidence: Bidelman 2013 (r=0.81, n=40), Blood & Zatorre 2001
MI formula: SRP.opioid_proxy += w_p1 · BCH.harmonicity_index
```

#### P2: Beat → Motor Synchronization (STU internal)

```
BEP.beat_induction ──── r=0.70 ────► BEP.motor_entrainment
    (beat strength)                    (movement urge)

Mechanism: Auditory beat → automatic motor cortex activation
Evidence: Grahn & Brett 2007 (r=0.70)
MI formula: BEP.motor_entrainment += w_p2 · BEP.beat_strength · groove
```

#### P3: Music → Autobiographical Memory (IMU → ARU)

```
MEM.retrieval_dynamics ────────────► NEMAC.nostalgia_intensity
    (memory vividness)                (nostalgia → reward)

Mechanism: Hippocampal retrieval → mPFC → striatal reward
Evidence: Janata 2009 (music-evoked autobiographical memory)
Clinical: Preserved in Alzheimer's disease (MMP model)
MI formula: NEMAC.nostalgia += w_p3 · MEM.familiarity · MEM.emotional_coloring
```

#### P4: Temporal Hierarchy → Prediction (STU internal)

```
TMH.context_depth ──── r=0.99 ────► HMCE.encoding_complexity
    (phrase → section)                (anatomical gradient)

Mechanism: Longer temporal context → higher cortical encoding
Evidence: Mischler 2025 (r=0.99, context depth vs cortical distance)
MI formula: HMCE.encoding[layer_k] = TMH[scale_k] · w_gradient[k]
```

#### P5: Tempo → Emotion (STU → ARU)

```
BEP.tempo_dynamics ──── moderate–high ────► AED.arousal_level
    (tempo, rhythm)                          (emotional arousal)

Mechanism: Fast tempo → sympathetic activation → arousal
Evidence: Gomez & Danuser 2007, Dalla Bella 2001
MI formula: AED.arousal_level += w_p5 · BEP.tempo · BEP.regularity
```

### 11.2 Pathway Architecture

Pathways are **modulation signals**, not data flows. They adjust existing model outputs
rather than creating new computations:

```python
class CrossUnitPathways:
    """Modulates model outputs based on inter-circuit relationships."""

    def modulate(
        self,
        all_model_outputs: Dict[str, ModelOutput],
    ) -> Dict[str, ModelOutput]:
        """Apply pathway modulations after all models compute."""

        # P1: SPU consonance → ARU pleasure
        if "BCH" in outputs and "SRP" in outputs:
            bch_harmonicity = outputs["BCH"].tensor[..., 1]  # harmonicity_index
            srp = outputs["SRP"].tensor
            srp[..., 2] += P1_WEIGHT * bch_harmonicity  # opioid_proxy

        # P5: STU tempo → ARU arousal
        if "BEP" in mechanisms and "AED" in mechanisms:
            bep_tempo = mechanisms["BEP"][..., 0:10].mean(dim=-1)
            mechanisms["AED"][..., 0] += P5_WEIGHT * bep_tempo

        return outputs
```

---

## 12. Testing & Validation

### 12.1 Test Categories

| Category | Tests | Purpose |
|----------|-------|---------|
| **Unit tests** | ~120 | Each mechanism/model in isolation |
| **Integration tests** | ~80 | Circuit-level (mechanism → model → semantics) |
| **Demand tests** | ~20 | H³ demand aggregation correctness |
| **Shape tests** | ~40 | Input/output dimensions match specs |
| **Range tests** | ~30 | Outputs bounded [0,1] or [-1,1] as specified |
| **Pathway tests** | ~25 | Cross-unit modulation effects |
| **Validation tests** | ~15 | Known pieces produce expected patterns |
| **Total** | **~330** | |

### 12.2 Validation Criteria

#### Per-Model Validation

Each model must pass:

1. **Shape**: `output.shape == (B, T, OUTPUT_DIM)` for any B, T
2. **Range**: All sigmoid outputs in [0, 1], tanh outputs in [-1, 1]
3. **Determinism**: Same input → identical output (no stochasticity)
4. **Zero input**: Silent audio produces neutral (≈0.5 sigmoid, ≈0 tanh) output
5. **Gradient sensitivity**: Output varies with relevant R³ feature changes
6. **Mechanism independence**: Model produces different output than raw mechanism passthrough

#### Per-Circuit Validation

Each circuit must pass:

1. **Mechanism sharing**: Multiple models reading same mechanism produce different outputs
2. **DemandAggregator**: Union of model demands matches sum of individual demands
3. **Independence**: Circuit outputs don't depend on other circuits (before pathway modulation)

#### System Validation (on known pieces)

Test on validated pieces (Swan Lake, Duel of the Fates, Yang, etc.):

| Criterion | Source | Test |
|-----------|--------|------|
| Wanting → liking lag 2-30s | Salimpoor 2011 | SRP wanting peaks before liking |
| Consonance → pleasure | Blood & Zatorre 2001 | BCH high → SRP pleasure high |
| Groove at moderate complexity | Witek 2014 | BEP groove peaks at medium syncopation |
| Familiar music → nostalgia | Janata 2009 | MEM familiarity → NEMAC activation |
| Deceptive cadence → surprise | Huron 2006 | SYN prediction_error spikes |

### 12.3 Regression Testing

As new models are added:
- All existing tests must continue passing
- New models must not alter existing model outputs (isolated computation)
- DemandAggregator may grow but never shrink (only adds tuples)
- Pipeline latency must remain < 2× baseline per additional circuit

---

## 13. File Layout

### 13.1 New Files (estimated)

```
mi/
├── brain/
│   ├── perceptual/                    ← Phase 2 (NEW)
│   │   ├── __init__.py
│   │   ├── mechanisms/
│   │   │   ├── __init__.py
│   │   │   ├── ppc.py                # ~100 lines
│   │   │   └── tpc.py                # ~100 lines
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── bch.py                # ~150 lines
│   │   │   ├── pscl.py               # ~150 lines
│   │   │   ├── pccr.py               # ~130 lines
│   │   │   ├── stai.py               # ~130 lines
│   │   │   ├── tscp.py               # ~120 lines
│   │   │   ├── miaa.py               # ~120 lines
│   │   │   ├── sdnps.py              # ~110 lines
│   │   │   ├── esme.py               # ~120 lines
│   │   │   └── sded.py               # ~110 lines
│   │   └── units/
│   │       ├── __init__.py
│   │       └── spu.py                # SPU unit aggregator
│   │
│   ├── sensorimotor/                  ← Phase 3 (NEW)
│   │   ├── __init__.py
│   │   ├── mechanisms/
│   │   │   ├── __init__.py
│   │   │   ├── bep.py                # ~100 lines
│   │   │   └── tmh.py                # ~100 lines
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── hmce.py               # ~150 lines
│   │   │   ├── amsc.py               # ~140 lines
│   │   │   ├── mdns.py               # ~140 lines
│   │   │   ├── amss.py               # ~120 lines
│   │   │   ├── tpio.py               # ~120 lines
│   │   │   ├── edta.py               # ~110 lines
│   │   │   ├── etam.py               # ~120 lines
│   │   │   ├── hgsic.py              # ~120 lines
│   │   │   ├── oms.py                # ~110 lines
│   │   │   ├── tmrm.py               # ~110 lines
│   │   │   ├── newmd.py              # ~110 lines
│   │   │   ├── mtne.py               # ~110 lines
│   │   │   ├── ptgmp.py              # ~110 lines
│   │   │   └── mpfs.py               # ~110 lines
│   │   └── units/
│   │       ├── __init__.py
│   │       └── stu.py                # STU unit aggregator
│   │
│   ├── mnemonic/                      ← Phase 4 (NEW)
│   │   ├── __init__.py
│   │   ├── mechanisms/
│   │   │   ├── __init__.py
│   │   │   ├── mem.py                # ~100 lines
│   │   │   └── syn.py                # ~100 lines
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── meamn.py              # ~150 lines
│   │   │   ├── pnh.py                # ~130 lines
│   │   │   ├── mmp.py                # ~140 lines
│   │   │   ├── rasn.py               # ~120 lines
│   │   │   ├── pmim.py               # ~120 lines
│   │   │   ├── oii.py                # ~110 lines
│   │   │   ├── hcmc.py               # ~120 lines
│   │   │   ├── riri.py               # ~110 lines
│   │   │   ├── mspba.py              # ~120 lines
│   │   │   ├── vriap.py              # ~110 lines
│   │   │   ├── tprd.py               # ~110 lines
│   │   │   ├── cmapcc.py             # ~110 lines
│   │   │   ├── dmms.py               # ~100 lines
│   │   │   ├── cssl.py               # ~100 lines
│   │   │   └── cdem.py               # ~100 lines
│   │   └── units/
│   │       ├── __init__.py
│   │       └── imu.py                # IMU unit aggregator
│   │
│   ├── mesolimbic/                    ← Phase 1 (EXTEND)
│   │   └── models/
│   │       ├── aac.py                # ~200 lines (Phase 1a)
│   │       ├── vmm.py                # ~150 lines (Phase 1b)
│   │       ├── pupf.py               # ~140 lines (Phase 1c)
│   │       ├── clam.py               # ~130 lines (Phase 1c)
│   │       ├── mad.py                # ~130 lines (Phase 1c)
│   │       ├── nemac.py              # ~130 lines (Phase 1c)
│   │       ├── dap.py                # ~110 lines (Phase 1d)
│   │       ├── cmat.py               # ~110 lines (Phase 1d)
│   │       └── tar.py                # ~110 lines (Phase 1d)
│   │
│   └── pathways/                      ← Phase 5 (NEW)
│       ├── __init__.py
│       ├── base.py
│       ├── p1_consonance_pleasure.py
│       ├── p2_beat_motor.py
│       ├── p3_music_memory.py
│       ├── p4_temporal_prediction.py
│       └── p5_tempo_emotion.py
│
├── language/                          ← Expand per model
│   ├── aac/                           # Phase 1a
│   ├── vmm/                           # Phase 1b
│   ├── bch/                           # Phase 2
│   ├── hmce/                          # Phase 3
│   ├── meamn/                         # Phase 4
│   └── ...                            # ~48 semantic modules total
│
└── pipeline/
    └── mi.py                          # Updated each phase (circuit registration)
```

### 13.2 Estimated Code Volume

| Phase | New Files | New Lines | Cumulative |
|-------|-----------|-----------|------------|
| Phase 0 (done) | 73 | ~4,100 | 4,100 |
| Phase 1 (ARU) | ~25 | ~2,500 | 6,600 |
| Phase 2 (SPU) | ~25 | ~2,700 | 9,300 |
| Phase 3 (STU) | ~35 | ~3,500 | 12,800 |
| Phase 4 (IMU) | ~40 | ~3,800 | 16,600 |
| Phase 5 (Pathways) | ~8 | ~600 | 17,200 |
| **Total** | **~206** | **~17,200** | |

---

## Appendix A: Model → Mechanism Matrix

Which mechanisms does each model read from?

```
                AED  CPD  C0P  ASA  PPC  TPC  BEP  TMH  MEM  SYN
─── ARU ───────────────────────────────────────────────────────────
SRP   α1        ●    ●    ●
AAC   α2        ●    ●         ●
VMM   α3        ●         ●
PUPF  β1        ●    ●    ●
CLAM  β2        ●    ●
MAD   β3        ●         ●
NEMAC β4        ●    ●    ●
DAP   γ1        ●
CMAT  γ2        ●         ●
TAR   γ3        ●    ●    ●
─── SPU ───────────────────────────────────────────────────────────
BCH   α1                            ●
PSCL  α2                            ●    ●
PCCR  α3                            ●    ●
STAI  β1                            ●    ●
TSCP  β2                                 ●
MIAA  β3                                 ●
SDNPS γ1                            ●
ESME  γ2                            ●    ●
SDED  γ3                            ●
─── STU ───────────────────────────────────────────────────────────
HMCE  α1                                      ●    ●
AMSC  α2                                      ●    ●
MDNS  α3                                      ●    ●
AMSS  β1                                           ●
TPIO  β2                                 ●         ●
EDTA  β3                                      ●
ETAM  β4                                      ●    ●
HGSIC β5                                      ●
OMS   β6                                      ●
TMRM  γ1                                      ●
NEWMD γ2                                      ●    ●
MTNE  γ3                                           ●
PTGMP γ4                                           ●
MPFS  γ5                                      ●    ●
─── IMU ───────────────────────────────────────────────────────────
MEAMN α1                                                ●
PNH   α2                                                     ●
MMP   α3                                                ●
RASN  β1                                      ●*        ●
PMIM  β2                                                     ●
OII   β3                                                ●    ●
HCMC  β4                                                ●
RIRI  β5                                      ●*        ●
MSPBA β6                                                     ●
VRIAP β7                                                ●
TPRD  β8                            ●*                        ●
CMAPCC β9                                     ●*        ●
DMMS  γ1                                                ●
CSSL  γ2                                                ●
CDEM  γ3        ●*                                      ●

* = cross-circuit read (mechanism from another circuit)
```

---

## Appendix B: Scientific Evidence Summary

| Tier | Total Effect Sizes | Mean d | Studies | Papers |
|------|-------------------|--------|---------|--------|
| **α (Core-4)** | 574 | 0.72 | 405 | 405 |
| **β (Integrative)** | ~150 est. | ~0.55 | ~100 | ~80 |
| **γ (Speculative)** | ~50 est. | ~0.40 | ~30 | ~25 |

**Power analysis**: All Core-4 units demonstrate >80% power for detecting observed effects
(SPU: 91%, STU: 99%, IMU: 98%, ARU: 93%).

**Publication bias**: Egger's regression non-significant for 3 of 4 units
(STU p=0.003, small-study effect detected → trim-fill adjusted d=0.58).

---

## Appendix C: Glossary

| Term | Meaning |
|------|---------|
| **Mechanism** | Shared 30D intermediate computation reading H³ at specific horizons |
| **Model** | Final output computation reading mechanisms + direct H³ |
| **Circuit** | Group of related mechanisms + models (maps to brain network) |
| **Unit** | Cognitive function category (SPU, STU, IMU, ARU) |
| **Tier** | Evidence confidence level (α > β > γ) |
| **H³ Demand** | Set of (horizon, morph, law) tuples a model/mechanism needs |
| **Direct H³ read** | Model reads H³ values bypassing mechanisms |
| **Cross-circuit read** | Model reads mechanism from a different circuit |
| **Pathway** | Modulation signal between units (P1-P5) |
| **DemandAggregator** | Unions all active model demands for efficient H³ computation |
| **L³** | Language / semantic interpretation layer per model |

---

*Last updated: 2026-02-11*
*Source: C³-Meta-Theory-F01.tex (448 papers, 1,116 claims, 634 effect sizes)*
*Reference models: Library/Auditory/C⁰/Models/ (93 files)*
