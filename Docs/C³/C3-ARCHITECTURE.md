# C3 Cognitive Architecture -- Musical Intelligence

## Overview

The MI-Beta pipeline transforms raw audio into a high-dimensional Musical Intelligence space (MI-space) through a layered architecture:

```
audio -> Cochlea(128D) -> R3(49D*) -> H3(sparse†) -> Brain(1006D) -> L3(variable) -> MI-space
  * R3 v2 expands to 128D (see Docs/R³/)
  † H3 theoretical: 112,896D (v1) / 294,912D (v2); actual ~5,200 / ~8,600 tuples (see Docs/H³/)
```

MI-space is the concatenation of all pipeline stages:

```
MI-space = [cochlea(128D) | R3(49D) | brain(brain_dim) | L3(variable)]
```

The total MI-space dimensionality is dynamic, depending on which cognitive units and models are active. With all 9 units enabled, `brain_dim = 1006`.

**Entry point:** `mi_beta.pipeline.MIBetaPipeline`
**Brain orchestrator:** `mi_beta.pipeline.brain_runner.BrainOrchestrator`

---

## Pipeline Stages

| Stage | Code | Output | Description |
|-------|------|--------|-------------|
| Cochlea | `mi_beta.ear.cochlea` | (B, T, 128) | 128-band mel spectrogram at 172.27 Hz frame rate |
| R3 | `mi_beta.ear.r3` | (B, T, 49) | 49 spectral features: consonance(7), energy(5), timbre(9), change(4), interactions(24) |
| H3 | `mi_beta.ear.h3` | sparse dict | Temporal morphological analysis: 32 horizons x 24 morphs x 3 laws per R3 feature (v1: 112,896D; v2: 294,912D; sparse) |
| Brain | `mi_beta.brain` | (B, T, 1006) | 9 cognitive units, 94 models, 10 mechanisms, 5 pathways |
| L3 | (planned) | (B, T, variable) | Semantic interpretation layer |

---

## 5-Phase Execution Model

The `BrainOrchestrator` sequences brain computation through five phases:

```
Phase 1: Mechanisms     Shared sub-computations cached for reuse (10 mechanisms, 30D each)
Phase 2: Independent    SPU, STU, IMU, ASU, NDU, MPU, PCU compute from H3/R3 only
Phase 3: Pathways       PathwayRunner routes signals between units (5 pathways)
Phase 4: Dependent      ARU, RPU compute with cross-unit inputs
Phase 5: Assembly       Concatenate all unit outputs into BrainOutput (B, T, brain_dim)
```

### Phase 1 -- Mechanisms

10 shared mechanism implementations, each producing 30D output. Mechanisms are grouped by neural circuit:

| Circuit | Mechanisms |
|---------|-----------|
| Mesolimbic | AED (Affective Entrainment Dynamics), CPD (Chills & Peak Detection), C0P (Cognitive Projection) |
| Perceptual | PPC (Pitch Processing Chain), TPC (Timbre Processing Chain) |
| Sensorimotor | BEP (Beat Entrainment Processing), TMH (Temporal Memory Hierarchy) |
| Mnemonic | MEM (Memory Encoding/Retrieval), SYN (Syntactic Processing) |
| Salience | ASA (Auditory Scene Analysis) |

Code: `mi_beta.brain.mechanisms.MechanismRunner`

### Phase 2 -- Independent Units

7 units that compute from H3/R3 inputs only (no cross-unit dependencies):

```
SPU(99D)  STU(148D)  IMU(159D)  ASU(94D)  NDU(94D)  MPU(104D)  PCU(94D)
```

### Phase 3 -- Pathways

5 declared cross-unit pathways route signals from independent to dependent units:

| ID | Route | Description | Evidence |
|----|-------|-------------|----------|
| P1 | SPU -> ARU | Consonance -> pleasure | Bidelman 2009, r=0.81 |
| P2 | STU -> STU | Beat -> motor sync (internal) | Grahn & Brett 2007, r=0.70 |
| P3 | IMU -> ARU | Memory -> affect | Janata 2009, r=0.55 |
| P4 | STU -> STU | Context -> prediction (internal) | Mischler 2025, r=0.99 |
| P5 | STU -> ARU | Tempo -> emotion | Juslin & Vastfjall 2008, r=0.60 |

Code: `mi_beta.brain.pathways.PathwayRunner`

### Phase 4 -- Dependent Units

2 units that require cross-unit inputs:

```
ARU(120D)  receives P1 (SPU), P3 (IMU), P5 (STU)
RPU(94D)   receives routed signals from ARU and SPU
```

### Phase 5 -- Assembly

All unit tensors are concatenated in `UNIT_EXECUTION_ORDER` into a single `BrainOutput`:

```python
BrainOutput(
    tensor=(B, T, brain_dim),      # concatenated
    unit_ranges={"SPU": (0, 99), "STU": (99, 247), ...},
    dimension_names=("SPU_d0", "SPU_d1", ..., "RPU_d93"),
)
```

---

## Dependency Graph

```
                    +-----------+
                    |   H3/R3    |
                    |   inputs   |
                    +-----+-----+
                          |
          +---------------+---------------+
          |               |               |
    +-----v-----+   +-----v-----+   +-----v-----+
    | Mechanisms |   |           |   |           |
    |  (10x30D) |   |           |   |           |
    +-----+-----+   |           |   |           |
          |         |           |   |           |
    +-----v---+-----v---+-------v---+---+-------v---+---+-------+
    |   SPU   |   STU   |   IMU   | ASU | NDU | MPU | PCU |
    |  (99D)  | (148D)  | (159D)  |(94D)|(94D)|(104D)|(94D)|
    | percep. | sensori.| mnemonic|salience|sal.|senso.|mnem.|
    +----+----+----+----+----+----+--+--+--+--+--+--+--+--+
         |         |         |
         | P1      | P5      | P3
         v         v         v
    +----+----+----+----+----+----+
    |          ARU (120D)         |
    |        mesolimbic           |
    +-------------+---------------+
                  |
    +-------------v---------------+
    |          RPU (94D)          |
    |        mesolimbic           |
    +-----------+-----------------+
                |
         +------v------+
         |  BrainOutput |
         |  (1006D)     |
         +------+------+
                |
         +------v------+
         |   MI-space   |
         |  (1183D+)    |
         +--------------+
```

Independent units (Phase 2):
```
SPU ─┐
STU ─┤
IMU ─┤
ASU ─┼─── No cross-unit dependencies
NDU ─┤
MPU ─┤
PCU ─┘
```

Dependent units (Phase 4):
```
ARU ─── Reads from SPU (P1), IMU (P3), STU (P5)
RPU ─── Reads from ARU, SPU
```

---

## Unit Execution Order

Defined in `mi_beta.core.constants.UNIT_EXECUTION_ORDER`:

```python
UNIT_EXECUTION_ORDER = (
    # Phase 2: Independent
    "SPU",   # Spectral Processing Unit        (perceptual,    d=0.84, 99D)
    "STU",   # Sensorimotor Timing Unit        (sensorimotor,  d=0.67, 148D)
    "IMU",   # Integrative Memory Unit         (mnemonic,      d=0.53, 159D)
    "ASU",   # Auditory Salience Unit          (salience,      d=0.60, 94D)
    "NDU",   # Novelty Detection Unit          (salience,      d=0.55, 94D)
    "MPU",   # Motor Planning Unit             (sensorimotor,  d=0.62, 104D)
    "PCU",   # Predictive Coding Unit          (mnemonic,      d=0.58, 94D)
    # Phase 4: Dependent
    "ARU",   # Affective Resonance Unit        (mesolimbic,    d=0.83, 120D)
    "RPU",   # Reward Processing Unit          (mesolimbic,    d=0.70, 94D)
)
```

---

## Dimensionality Summary

| Component | Dimensions | Source |
|-----------|-----------|--------|
| Cochlea (mel) | 128 | `N_MELS = 128` |
| R3 spectral | 49 | `R3_DIM = 49` (consonance 7 + energy 5 + timbre 9 + change 4 + interactions 24) |
| H3 temporal | 112,896 sparse (v2: 294,912) | 49 R3 x 32 horizons x 24 morphs x 3 laws (v2: 128 R3) |
| Brain total | 1006 | Sum of all unit OUTPUT_DIMs |
| -- SPU | 99 | 9 models (3 alpha + 3 beta + 3 gamma) |
| -- STU | 148 | 14 models (3 alpha + 6 beta + 5 gamma) |
| -- IMU | 159 | 15 models (3 alpha + 9 beta + 3 gamma) |
| -- ASU | 94 | 9 models (3 alpha + 3 beta + 3 gamma) |
| -- NDU | 94 | 9 models (3 alpha + 3 beta + 3 gamma) |
| -- MPU | 104 | 10 models (3 alpha + 4 beta + 3 gamma) |
| -- PCU | 94 | 9 models (3 alpha + 3 beta + 3 gamma) |
| -- ARU | 120 | 10 models (3 alpha + 4 beta + 3 gamma) |
| -- RPU | 94 | 9 models (3 alpha + 3 beta + 3 gamma) |
| L3 semantic | variable | (planned) |
| **MI-space total** | **1183 + L3** | cochlea + R3 + brain |

---

## Core-4 vs Experimental-5

Units are classified by meta-analytic evidence strength:

**Core-4** (k >= 10 studies, validated pooled effect):
- SPU d=0.84 -- Spectral Processing (perceptual)
- ARU d=0.83 -- Affective Resonance (mesolimbic)
- STU d=0.67 -- Sensorimotor Timing (sensorimotor)
- IMU d=0.53 -- Integrative Memory (mnemonic)

**Experimental-5** (k < 10 studies):
- RPU d=0.70 -- Reward Processing (mesolimbic)
- MPU d=0.62 -- Motor Planning (sensorimotor)
- ASU d=0.60 -- Auditory Salience (salience)
- PCU d=0.58 -- Predictive Coding (mnemonic)
- NDU d=0.55 -- Novelty Detection (salience)

---

## Model Tiers

Each model within a unit is assigned an evidence tier (`mi_beta.core.constants.MODEL_TIERS`):

| Tier | Confidence | Studies | Typical OUTPUT_DIM |
|------|-----------|---------|-------------------|
| alpha | >90% | k >= 10 | 11--19D |
| beta | 70--90% | 5 <= k < 10 | 10--12D |
| gamma | <70% | k < 5 | 10D |

---

## Data Flow

```
  +-----------+     +---------+     +---------+     +----------+     +--------+
  |   Audio   | --> | Cochlea | --> |   R3    | --> |    H3    | --> | Brain  |
  | waveform  |     | 128 mel |     | 49 spec |     | sparse   |     | 1006D  |
  +-----------+     +----+----+     +----+----+     | 2304D    |     +---+----+
                         |               |          | v1:112,896|         |
                         |               |          | v2:294,912|         |
                         |               |          +----+-----+         |
                         |               |               |               |
                         v               v               v               v
                    +----+---------------+---------------+---------------+----+
                    |                    MI-space                              |
                    |  [cochlea(128) | R3(49) | brain(1006) | L3(var)]        |
                    |  Total: 1183 + L3                                       |
                    +---------------------------------------------------------+
```

---

## Neural Circuits

5 circuits span across multiple units (`mi_beta.core.constants.CIRCUITS`):

| Circuit | Description | Units |
|---------|-------------|-------|
| perceptual | Hearing & pattern recognition | SPU |
| sensorimotor | Rhythm & movement entrainment | STU, MPU |
| mnemonic | Memory consolidation & familiarity | IMU, PCU |
| mesolimbic | Reward & dopaminergic pleasure | ARU, RPU |
| salience | Attention, novelty, & arousal gating | ASU, NDU |

---

## Code-to-Documentation Reference

| Documentation Directory | Code Package | Description |
|------------------------|-------------|-------------|
| `Docs/C3/Units/` | `mi_beta.brain.units` | 9 cognitive unit definitions |
| `Docs/C3/Models/` | `mi_beta.brain.units.{unit}.models` | 94 individual model implementations |
| `Docs/C3/Mechanisms/` | `mi_beta.brain.mechanisms` | 10 shared mechanism implementations |
| `Docs/C3/Pathways/` | `mi_beta.brain.pathways` | 5 cross-unit pathway declarations |
| `Docs/C3/Contracts/` | `mi_beta.contracts` | Base classes: BaseModel, BaseMechanism, BaseCognitiveUnit |
| `Docs/C3/Regions/` | `mi_beta.brain.regions` | Anatomical brain region definitions (MNI152) |
| `Docs/C3/Neurochemicals/` | `mi_beta.brain.neurochemicals` | Neurochemical system definitions and state management |
| `Docs/C3/Circuits/` | `mi_beta.core.constants.CIRCUITS` | Neural circuit groupings |
| `Docs/C3/Tiers/` | `mi_beta.core.constants.MODEL_TIERS` | Evidence tier definitions |
| `Docs/C3/Matrices/` | -- | Cross-unit interaction matrices |

---

## Output Types

All pipeline outputs are defined in `mi_beta.core.types`:

| Type | Shape | Description |
|------|-------|-------------|
| `CochleaOutput` | (B, N_MELS, T) | Mel spectrogram |
| `R3Output` | (B, T, 49) | R3 spectral features |
| `H3Output` | dict{4-tuple: (B,T)} | Sparse temporal features |
| `ModelOutput` | (B, T, output_dim) | Single model result + metadata |
| `UnitOutput` | (B, T, unit_dim) | All models within one unit |
| `BrainOutput` | (B, T, brain_dim) | All units concatenated + ranges |
| `MIBetaOutput` | (B, T, total_dim) | Full MI-space + section ranges |

---

## Cross-References

- **R³ Spectral:** [Docs/R³/00-INDEX.md](../R³/00-INDEX.md) — 128D spectral feature architecture
- **H³ Temporal:** [Docs/H³/00-INDEX.md](../H³/00-INDEX.md) — temporal morphology architecture (294,912D sparse)
- **Units:** [Units/00-INDEX.md](Units/00-INDEX.md)
- **Models:** [Models/00-INDEX.md](Models/00-INDEX.md)
- **Mechanisms:** [Mechanisms/](Mechanisms/)
- **Pathways:** [Pathways/](Pathways/)
- **Contracts:** [Contracts/](Contracts/)
- **Regions:** [Regions/](Regions/)
- **Neurochemicals:** [Neurochemicals/](Neurochemicals/)
- **Circuits:** [Circuits/](Circuits/)
- **Tiers:** [Tiers/](Tiers/)
