# C³ Architecture Evolution: From Flat Execution to Hierarchical Brain Model

**Version**: 1.0.0
**Date**: 2026-02-15
**Status**: PROPOSAL — Awaiting approval before implementation
**Based on**: Deep research into 7 brain modeling frameworks, auditory neuroscience literature, and complete 96-model dependency analysis

---

## 1. Executive Summary

The C³ cognitive architecture contains 96 models across 9 units that are documented with rich hierarchical dependencies, but executed as flat peers. This document proposes an **Evolution** — not a rewrite — that restructures the runtime to match the documented neuroscience while preserving every model, doc, and relationship.

**Core problem**: The code runs `for model in self.active_models: model.compute(h3, r3, cross_unit)` — all models get identical inputs. But the docs say BCH output feeds PSCL, which feeds PCCR. The docs are right. The code needs to catch up.

**Key proposal**: Add `PROCESSING_DEPTH` to each model, implement layered intra-unit execution, and expand the 5 unidirectional pathways to ~12 bidirectional pathways — all derived from what's already documented in the 96 model docs.

---

## 2. What the Research Found

### 2.1 Brain Modeling Frameworks (7 analyzed)

| Framework | Key Pattern | Relevance to MI |
|-----------|-------------|-----------------|
| **NENGO** | Nested graph hierarchy (Spaun: BG routes cortical signals) | Routing architecture for pathways |
| **TVB** | Connectome-based neural mass models | Connectome idea for inter-unit wiring |
| **NEST** | Point neurons, Potjans-Diesmann laminar columns (L1-L6) | Laminar depth concept |
| **Brian2** | Equation-based, flat execution | Anti-pattern — what we have now |
| **BluePyOpt/BBP** | Most detailed L1-L6 laminar reconstruction | Gold standard for processing depth |
| **HNN** | Proximal/distal = feedforward/feedback (cleanest hierarchy) | **Best match** — feedforward = bottom-up, feedback = top-down |
| **DCM/SPM** | Forward/backward/lateral connection typing | **Most applicable** — 3 connection types map directly |

### 2.2 Real Auditory Processing Hierarchy

The brain processes music in a clear hierarchy with known temporal integration windows:

```
Level 0: Brainstem (AN → CN → SOC → IC)     ← 1-10ms, tonotopy
Level 1: Primary Auditory (MGB → A1/HG)      ← 20-50ms, spectrotemporal
Level 2: Auditory Association (STG → STS)     ← 50-200ms, streams
Level 3: Frontal/Temporal (IFG, dlPFC, TP)    ← 200ms-2s, syntax/WM
Level 4: Limbic/Reward (amygdala → NAcc)      ← 2-15s, emotion/reward
Level 5: Integration (vmPFC, OFC, ACC)        ← 15-60s+, value/meaning
```

**Dual stream processing** confirmed:
- **Ventral (what)**: SPU → NDU → PCU → IMU → ARU
- **Dorsal (how)**: SPU → STU → MPU → ARU

**H³ temporal hierarchy** maps precisely:
- H0-H2 (5-20ms) = brainstem integration windows
- H3-H7 (20-200ms) = cortical spectrotemporal
- H8-H15 (200ms-2s) = phrase/syntax
- H16-H25 (2-60s) = long-term structure

### 2.3 Complete 96-Model Dependency Graph

Every model's Section 9 (Cross-Unit Pathways) was read. The findings:

**Intra-unit layers per unit:**

| Unit | Models | Layers | Foundation (Layer 0) | Max Depth |
|------|--------|--------|----------------------|-----------|
| SPU | 9 | 4 | BCH | Layer 3 |
| STU | 14 | 3 | HMCE | Layer 2 (+ circular) |
| IMU | 15 | 4 | MEAMN | Layer 3 |
| ASU | 9 | 3 | SNEM | Layer 2 |
| NDU | 9 | 4 | MPG | Layer 3 |
| MPU | 10 | 4 | PEOM | Layer 3 |
| PCU | 10 | 5 | HTP | Layer 4 |
| ARU | 10 | 4 | SRP | Layer 3 |
| RPU | 10 | 4 | DAED | Layer 3 |

**Two hub units identified:**
1. **STU** = Processing hub — receives from 7 units, distributes to ARU + IMU
2. **ARU** = Convergence hub — receives from ALL 8 units, final affective output

**Cross-unit pathway count:**
- Current code: 5 unidirectional (P1-P5)
- Documented in model docs: 17+ distinct cross-unit routes
- Missing feedback pathways: PCU→SPU, ASU→SPU, RPU→ASU, NDU→SPU, IMU→STU, RPU→STU, RPU→MPU

---

## 3. Gap Analysis: Docs vs Code

### 3.1 What's Correct (keep as-is)

| Feature | Assessment | Evidence |
|---------|------------|----------|
| **9 units** | Correct grouping | Maps to real neuroanatomical functional modules |
| **H³ temporal hierarchy** | **Excellent** | H0-H25 horizons match known neural integration windows precisely |
| **26 brain regions** | Good coverage | 12 cortical + 9 subcortical + 5 brainstem, MNI coords verified |
| **4 neurochemicals** | Correct set | DA, NE, opioid, 5-HT cover primary musical reward/emotion systems |
| **6 circuits** | Valid grouping | Mesolimbic, perceptual, sensorimotor, mnemonic, salience, imagery |
| **R³ spectral features** | Well-grounded | Maps to established psychoacoustic and DSP measures |
| **BEP+ASA mechanisms** | Solid concept | Binding-by-entrainment + adaptive salience alignment |
| **ARU/RPU dependency** | Correct | RPU (neurochemical) informs ARU (psychological) |

### 3.2 Critical Gaps (must fix)

#### Gap 1: Flat Intra-Unit Execution
**Current**: All models in a unit run in parallel with identical inputs.
**Required**: Layered execution where BCH output feeds PSCL, PSCL feeds PCCR, etc.
**Impact**: Without this, 90% of the documented model interactions are dead code.

#### Gap 2: No Processing Depth
**Current**: Models have `TIER` (alpha/beta/gamma) but no computational depth ordering.
**Required**: `PROCESSING_DEPTH` attribute (0-5) reflecting real neural hierarchy position.
**Framework precedent**: BluePyOpt (L1-L6 laminar), HNN (proximal/distal), DCM (forward/backward).

#### Gap 3: Only 5 Unidirectional Pathways
**Current**: P1(SPU→ARU), P2(SPU↔STU), P3(IMU→ARU), P4(STU internal), P5(STU→ARU).
**Documented**: 17+ cross-unit routes including feedback from PCU, RPU, ASU, NDU back to sensory units.
**Neuroscience**: Cortical processing is fundamentally bidirectional (DCM forward/backward/lateral).

#### Gap 4: No Feedback Pathways
**Current**: All pathways are feedforward (bottom-up sensory → top-down reward).
**Required**: Top-down feedback for predictive coding, attention modulation, reward-based learning.
**Key missing**: PCU→SPU (predictive silencing), ASU→SPU (attentional gain), RPU→ASU (reward salience).

#### Gap 5: PathwayRunner Routes Entire Unit Outputs
**Current**: `PathwayRunner.route()` passes entire unit tensors (e.g., all 99D of SPU to ARU).
**Required**: Model-specific dimension routing (e.g., BCH dims 0:12 → ARU.SRP, PSCL dims 12:24 → ARU.SRP).
**Impact**: Without this, receiving models can't distinguish which upstream model's signal they're getting.

#### Gap 6: ASU and NDU are Disconnected Islands
**Current**: ASU and NDU have no named pathways (P1-P5 don't include them).
**Documented**: ASU→STU (entrainment, timing), NDU→STU (onset timing), ASU→ARU, NDU→ARU, NDU→IMU.
**Impact**: Attention and development — two critical modulatory systems — have no influence on processing.

### 3.3 Secondary Gaps (should fix)

| Gap | Description | Priority |
|-----|-------------|----------|
| No conduction delays | Real brain signals take 1-20ms between regions | Medium |
| No thalamic gating | MGB gates ALL ascending auditory signals | Medium |
| No cerebellum region | Missing from region registry; critical for timing (CTBB model references it) | Medium |
| Neurochemicals decorative | 4 neurochemicals defined but unused at runtime | Low |
| No precision weighting | Predictive coding requires precision-weighted prediction errors | Low |
| STU circular deps | HGSIC↔OMS↔ETAM form a loop, needs iterative settling | Low |

---

## 4. Proposed Architecture: Hierarchical C³

### 4.1 New Model Attribute: PROCESSING_DEPTH

Every model gets a `PROCESSING_DEPTH` integer (0-5) reflecting its position in the neural processing hierarchy:

```python
class BaseModel:
    PROCESSING_DEPTH: int  # NEW — 0 = brainstem/foundation, 5 = integration

    # Depth assignment rules:
    # 0 = Foundation (alpha-1 models: BCH, HMCE, MEAMN, SNEM, MPG, PEOM, HTP, SRP, DAED)
    # 1 = Primary processing (depends only on foundation + R³/H³)
    # 2 = Secondary processing (depends on depth-1 models)
    # 3 = Tertiary (integration within unit)
    # 4 = Cross-modal integration (deep dependencies)
    # 5 = Global integration (TAR, PSH — highest-level convergence)
```

**Complete depth assignment (all 96 models):**

```
DEPTH 0 — Foundation (9 models, one per unit):
  SPU: BCH    STU: HMCE    IMU: MEAMN    ASU: SNEM    NDU: MPG
  MPU: PEOM   PCU: HTP     ARU: SRP      RPU: DAED

DEPTH 1 — Primary (23 models):
  SPU: PSCL, STAI
  STU: AMSC, MDNS, AMSS, ETAM, OMS, NEWMD, MTNE, MPFS
  IMU: PNH, MMP, PMIM, HCMC, CDEM, DMMS
  ASU: IACM, CSG, BARM, STANM
  NDU: SDD, EDNR, DSP
  MPU: MSR, GSSM, ASAP
  PCU: SPH, ICEM
  ARU: AAC, VMM
  RPU: MORMR, RPEM, IUCP, MCCN

DEPTH 2 — Secondary (30 models):
  SPU: PCCR, TSCP, SDNPS
  STU: TPIO, EDTA, HGSIC, TMRM, PTGMP
  IMU: RASN, OII, MSPBA, TPRD, CSSL
  ASU: AACM, PWSM, DGTP, SDL
  NDU: CDMR, SLEE, SDDP, ONI
  MPU: SPMC, DDSMI, NSCP, CTBB
  PCU: PWUP, CHPI
  ARU: PUPF, CLAM, MAD, NEMAC
  RPU: MEAMR, SSRI, LDAC, IOTMS

DEPTH 3 — Tertiary (22 models):
  SPU: MIAA, ESME, SDED
  IMU: RIRI, VRIAP, CMAPCC
  NDU: ECT
  MPU: VRMSME, STC
  PCU: WMED, UDP, IGFE
  ARU: DAP, CMAT
  RPU: SSPS

DEPTH 4 — Integration (5 models):
  PCU: MAA, PSH

DEPTH 5 — Global convergence (1 model):
  ARU: TAR
```

### 4.2 Layered Intra-Unit Execution

Replace the flat for-loop with depth-ordered execution:

```python
# CURRENT (flat — wrong):
class SPUUnit(BaseCognitiveUnit):
    def compute(self, h3, r3, cross_unit):
        outputs = []
        for model in self.active_models:
            out = model.compute(h3, r3, cross_unit)
            outputs.append(out)
        return torch.cat(outputs, dim=-1)

# PROPOSED (layered — correct):
class SPUUnit(BaseCognitiveUnit):
    def compute(self, h3, r3, cross_unit):
        model_outputs = {}
        outputs = []

        # Execute by processing depth
        for depth in sorted(self._depth_groups.keys()):
            for model in self._depth_groups[depth]:
                # Build intra-unit context from already-computed models
                intra_unit = {
                    name: tensor
                    for name, tensor in model_outputs.items()
                }
                out = model.compute(h3, r3, cross_unit, intra_unit)
                model_outputs[model.NAME] = out
                outputs.append(out)

        return torch.cat(outputs, dim=-1)
```

**Key change**: Models at depth N receive the outputs of all depth 0..N-1 models as `intra_unit` context. The model's `compute()` method selects which upstream outputs it needs (defined in its `INTRA_UNIT_READS` attribute).

### 4.3 Expanded Pathway System (5 → 12 pathways)

#### Current pathways (keep, refine):

| ID | Route | Type | Status |
|----|-------|------|--------|
| P1 | SPU → ARU | Feedforward | Keep — add model-specific routing |
| P2 | SPU ↔ STU | Bidirectional | Keep — add feedback direction |
| P3 | IMU → ARU | Feedforward | Keep — add model-specific routing |
| P4 | STU internal | Internal | Remove — replaced by intra-unit layering |
| P5 | STU → ARU | Feedforward | Keep — add model-specific routing |

#### New pathways (add):

| ID | Route | Type | Neuroscience basis |
|----|-------|------|-------------------|
| P6 | ASU → STU | Feedforward | Attentional gating of temporal processing (Lakatos 2008) |
| P7 | NDU → STU | Feedforward | Developmental influence on temporal processing |
| P8 | MPU → STU | Feedforward | Motor-to-sensory coupling (Chen 2008) |
| P9 | PCU → SPU | **Feedback** | Predictive silencing of expected stimuli (Rao & Ballard 1999) |
| P10 | PCU → STU | Feedforward | Prediction timing for entrainment |
| P11 | RPU → ARU | Feedforward | Neurochemical reward → psychological affect |
| P12 | RPU → IMU | Feedback | Reward-based memory consolidation (Shohamy & Adcock 2010) |

#### Connection type taxonomy (from DCM):

```python
class ConnectionType(Enum):
    FORWARD = "forward"      # Bottom-up: L2/3 → L4 (driving)
    BACKWARD = "backward"    # Top-down: L5/6 → L1 (modulatory)
    LATERAL = "lateral"      # Same level: L2/3 → L2/3 (contextual)
```

### 4.4 Model-Specific Pathway Routing

Replace unit-level routing with dimension-specific routing:

```python
# CURRENT (unit-level — coarse):
class PathwayRunner:
    def route(self, unit_outputs):
        cross = {}
        cross["P1_SPU_ARU"] = unit_outputs["SPU"]  # ALL 99D
        return cross

# PROPOSED (model-specific — precise):
class PathwayRunner:
    def route(self, unit_outputs, model_outputs):
        cross = {}
        # P1: BCH.consonance (dims 0:12) + PSCL.salience (dims 12:24) → ARU.SRP
        cross["P1_SPU_ARU"] = {
            "BCH": model_outputs["SPU"]["BCH"],       # 12D
            "PSCL": model_outputs["SPU"]["PSCL"],     # 12D
            "STAI": model_outputs["SPU"]["STAI"],     # 12D
            "SDED": model_outputs["SPU"]["SDED"],     # 10D
            "ESME": model_outputs["SPU"]["ESME"],     # 11D
            "SDNPS": model_outputs["SPU"]["SDNPS"],   # 10D
        }
        return cross
```

### 4.5 New BaseModel Interface

```python
class BaseModel:
    # Existing attributes (unchanged)
    NAME: str
    FULL_NAME: str
    TIER: str
    OUTPUT_DIM: int
    LAYERS: tuple
    MECHANISM_NAMES: tuple

    # NEW attributes
    PROCESSING_DEPTH: int                    # 0-5
    INTRA_UNIT_READS: tuple                  # ("BCH", "PSCL") — which same-unit models I read
    CROSS_UNIT_READS: dict                   # {"SPU": ("BCH",), "PCU": ("HTP",)} — specific models
    CONNECTION_TYPE: str                     # "forward" | "backward" | "lateral"
    CONDUCTION_DELAY_MS: float              # Estimated signal delay (1-20ms)

    def compute(
        self,
        h3_features,
        r3_features,
        cross_unit_inputs=None,
        intra_unit_inputs=None,   # NEW — outputs from same-unit models at lower depth
    ) -> Tensor:
        ...
```

---

## 5. Orchestrator Evolution

### 5.1 Current: 4-Phase Flat Execution

```
Phase 1: Independent units (7) — flat for-loop per unit
Phase 2: PathwayRunner routes unit-level outputs
Phase 3: Dependent units (ARU, RPU) — flat for-loop per unit
Phase 4: Assembly → (B, T, 1006)
```

### 5.2 Proposed: 6-Phase Hierarchical Execution

```
Phase 1: Foundation Layer (Depth 0)
  Run BCH, HMCE, MEAMN, SNEM, MPG, PEOM, HTP in parallel
  (These are the 7 independent alpha-1 models)

Phase 2: Forward Pathway Routing (feedforward)
  Route foundation outputs: SPU→STU, SPU→IMU, ASU→STU, etc.

Phase 3: Independent Processing (Depth 1-3)
  Each unit runs its depth 1→2→3 models in order
  Each model receives intra_unit_inputs from lower depths

Phase 4: Cross-Unit Routing (all pathways)
  Route all 12 pathways with model-specific dimensions
  Include feedback pathways: PCU→SPU, RPU→ASU, RPU→IMU

Phase 5: Dependent Processing
  ARU (Depth 0-3): SRP receives ALL pathway inputs, then AAC→VMM→...→TAR
  RPU (Depth 0-3): DAED receives pathway inputs, then MORMR→RPEM→...→SSPS

Phase 6: Assembly
  Concatenate all 96 model outputs → (B, T, 1006)
  Same output format, same total dimensions
```

**Key difference**: Phase 3 replaces the flat for-loop with layered execution. Each model at depth N waits for all depth 0..N-1 models in its unit to complete.

### 5.3 Backward Compatibility

The output format is **unchanged**:
- Still produces `(B, T, 1006)` tensor
- Same `unit_slices` mapping
- Same `BrainOutput` dataclass
- All existing tests continue to pass

What changes is the **internal routing** — models now receive richer, hierarchically-ordered inputs instead of identical flat inputs.

---

## 6. Implementation Plan

### Phase A: Contracts (non-breaking additions)

1. Add `PROCESSING_DEPTH`, `INTRA_UNIT_READS`, `CROSS_UNIT_READS`, `CONNECTION_TYPE` to `BaseModel`
2. Default values ensure all 96 skeleton models still work: `PROCESSING_DEPTH=0`, `INTRA_UNIT_READS=()`, etc.
3. Add `intra_unit_inputs` parameter to `compute()` with default `None`
4. Add `ConnectionType` enum to contracts

**Files changed**: `contracts/bases/base_model.py`

### Phase B: Unit Execution (layered)

1. Modify `BaseCognitiveUnit.compute()` to group models by `PROCESSING_DEPTH`
2. Execute depth-by-depth, passing `intra_unit_inputs` at each layer
3. Fall back to flat execution when all models have `PROCESSING_DEPTH=0` (backward compat)

**Files changed**: `contracts/bases/base_unit.py`, all 9 `units/*/unit.py`

### Phase C: Pathway Expansion

1. Add 7 new pathway definitions (P6-P12)
2. Refactor `PathwayRunner` to accept `model_outputs` dict (per-model, not per-unit)
3. Implement model-specific dimension routing
4. Add `ConnectionType` to each pathway definition

**Files changed**: `pathways/definitions.py`, `pathways/runner.py`

### Phase D: Orchestrator Upgrade

1. Implement 6-phase execution in `BrainOrchestrator.forward()`
2. Foundation models execute first, then layered, then dependent
3. Pathway routing uses model-specific outputs

**Files changed**: `brain/orchestrator.py`

### Phase E: Model-by-Model Build (96 models)

As each model is built (per the Building plan), populate:
- `PROCESSING_DEPTH` from the depth table in Section 4.1
- `INTRA_UNIT_READS` from the model's doc Section 9
- `CROSS_UNIT_READS` from the model's doc Section 9
- Real `compute()` logic that uses `intra_unit_inputs`

This is the existing Building workflow — the Evolution just gives it the right infrastructure.

---

## 7. Validation Strategy

### 7.1 Regression Tests

```python
# Every change must pass:
pytest Tests/integration/test_brain_pipeline.py  # (B, T, 1006) output
pytest Tests/unit/test_orchestrator.py           # Phase ordering
pytest Tests/unit/test_models.py                 # All 96 models

# New tests:
pytest Tests/unit/test_processing_depth.py       # Depth ordering correctness
pytest Tests/unit/test_pathway_routing.py        # Model-specific routing
pytest Tests/integration/test_layered_execution.py  # Intra-unit cascade
```

### 7.2 Neuroscience Validation

| Check | Expected | Test |
|-------|----------|------|
| BCH output influences PSCL | PSCL output changes when BCH values change | Sensitivity test |
| PCU→SPU feedback reduces SPU output | Predictive silencing attenuates expected signals | Direction test |
| ARU receives all pathways | TAR integrates signals from all 8 units | Completeness test |
| Depth ordering is acyclic | No model reads from a model at equal or higher depth | Graph validation |

### 7.3 Performance

- Foundation layer (9 models in parallel): ~same as current
- Layered execution per unit: Sequential within unit, but units still parallel
- Estimated overhead: <5% (depth groups are small, 2-5 models per layer)

---

## 8. What Stays the Same

| Component | Status | Reason |
|-----------|--------|--------|
| 96 model files | Unchanged | Skeleton code still works, built models get richer |
| 96 model docs | Unchanged | Already document the hierarchy — the code catches up |
| 9 unit boundaries | Unchanged | Valid neuroanatomical grouping |
| 10 mechanisms | Unchanged | BEP, ASA, PPC, TPC, TMH, MEM, AED, CPD, C0P + cross-circuit |
| 26 brain regions | Unchanged | Correct MNI coordinates and functional assignments |
| 4 neurochemicals | Unchanged | Correct set for musical reward/emotion |
| 6 circuits | Unchanged | Valid functional groupings |
| R³, H³, L³ layers | Unchanged | Ear and semantic layers are independent |
| Output format | Unchanged | Still (B, T, 1006) |
| HYBRID transformer | Unchanged | Reads from brain output, doesn't care about internal routing |

---

## 9. Complete Inter-Unit Pathway Map

```
         ┌──────────────────────────────────────────────────────────────────┐
         │                    INFORMATION FLOW                              │
         │                                                                  │
         │   ┌─────┐    P2(fwd)   ┌─────┐    P5(fwd)    ┌─────┐          │
         │   │ SPU │ ──────────→  │ STU │ ────────────→  │ ARU │          │
         │   │     │ ←────────── │     │                 │     │          │
         │   └──┬──┘   P9(back)  └──┬──┘                └──┬──┘          │
         │      │  P1(fwd)  ↑↑↑↑    │                      ↑              │
         │      │           ││││    │                      │              │
         │      └──────────────────────────────────────────┘              │
         │                  ││││    │                                      │
         │      ┌─────┐    ││││    │         ┌─────┐                     │
         │      │ ASU │ ───┘│││    │    ┌──→ │ RPU │ ──P11(fwd)──→ ARU  │
         │      └─────┘  P6 │││    │    │    └──┬──┘                     │
         │                  │││    │    │       │ P12(back)              │
         │      ┌─────┐    │││    │    │       ↓                        │
         │      │ NDU │ ───┘││    │    │    ┌─────┐                     │
         │      └─────┘  P7 ││    │    │    │ IMU │ ──P3(fwd)──→ ARU   │
         │                  ││    │    │    └─────┘                     │
         │      ┌─────┐    ││    │    │                                 │
         │      │ MPU │ ───┘│    │    │    ┌─────┐                     │
         │      └─────┘  P8 │    │    └──  │ PCU │ ──P9(back)──→ SPU   │
         │                  │    │         └──┬──┘                      │
         │                  │    │            │ P10(fwd)                │
         │                  │    └────────────┘                         │
         │                  │                                           │
         └──────────────────────────────────────────────────────────────┘

Pathway Legend:
  P1:  SPU → ARU     (consonance → reward)           FORWARD
  P2:  SPU ↔ STU     (spectral ↔ temporal)           BIDIRECTIONAL
  P3:  IMU → ARU     (memory → reward)               FORWARD
  P5:  STU → ARU     (temporal → reward)              FORWARD
  P6:  ASU → STU     (attention → temporal)           FORWARD
  P7:  NDU → STU     (development → temporal)         FORWARD
  P8:  MPU → STU     (motor → temporal)               FORWARD
  P9:  PCU → SPU     (prediction → spectral)          BACKWARD
  P10: PCU → STU     (prediction → temporal)           FORWARD
  P11: RPU → ARU     (neurochemical → affect)          FORWARD
  P12: RPU → IMU     (reward → memory)                 BACKWARD
```

---

## 10. Intra-Unit Dependency Maps (All 9 Units)

### SPU (Spectral Processing Unit) — 9 models, 4 layers

```
Layer 0: BCH ───────────────────────────────────────────────────
              │           │           │           │
Layer 1: PSCL ──────── STAI          │           │
              │     │     │           │           │
Layer 2: PCCR ── TSCP ── SDNPS       │           │
              │     │        │        │           │
Layer 3: MIAA ── ESME ──── SDED      │           │
```

### STU (Sensorimotor Temporal Unit) — 14 models, 3 layers

```
Layer 0: HMCE ──────────────────────────────────────────────────
              │      │      │      │      │      │      │     │
Layer 1: AMSC ── MDNS ── AMSS ── ETAM ── OMS ── NEWMD ── MTNE ── MPFS
              │            │      │             │
Layer 2: TPIO ── EDTA ── HGSIC ── TMRM ── PTGMP
         (circular deps: HGSIC↔OMS↔ETAM — needs iterative settling)
```

### IMU (Integrative Memory Unit) — 15 models, 4 layers

```
Layer 0: MEAMN ──────────────────────────────────────────────────
              │      │      │      │      │      │
Layer 1: PNH ── MMP ── PMIM ── HCMC ── CDEM ── DMMS
              │      │      │      │
Layer 2: RASN ── OII ── MSPBA ── TPRD ── CSSL
              │                   │
Layer 3: RIRI ── VRIAP ── CMAPCC
```

### ASU (Attention & Salience Unit) — 9 models, 3 layers

```
Layer 0: SNEM ──────────────────────────
              │      │      │      │
Layer 1: IACM ── CSG ── BARM ── STANM
              │      │      │      │
Layer 2: AACM ── PWSM ── DGTP ── SDL
```

### NDU (Neurodevelopmental Unit) — 9 models, 4 layers

```
Layer 0: MPG ──────────────────────
              │      │      │
Layer 1: SDD ── EDNR ── DSP
              │      │      │
Layer 2: CDMR ── SLEE ── SDDP ── ONI
                        │
Layer 3: ECT ───────────┘
```

### MPU (Motor Processing Unit) — 10 models, 4 layers

```
Layer 0: PEOM ──────────────────────────
              │      │      │
Layer 1: MSR ── GSSM ── ASAP
              │           │
Layer 2: SPMC ── DDSMI ── NSCP ── CTBB
              │      │
Layer 3: VRMSME ── STC
```

### PCU (Predictive Coding Unit) — 10 models, 5 layers

```
Layer 0: HTP ────────────────────────────────
              │      │
Layer 1: SPH ── ICEM
              │      │
Layer 2: PWUP ── CHPI
              │
Layer 3: WMED ── UDP ── IGFE
              │      │      │
Layer 4: MAA ── PSH ──────────
```

### ARU (Affective Response Unit) — 10 models, 4 layers

```
Layer 0: SRP ────────────────────────────────
              │      │
Layer 1: AAC ── VMM
              │      │
Layer 2: PUPF ── CLAM ── MAD ── NEMAC
              │      │
Layer 3: DAP ── CMAT ── TAR (receives ALL ARU models)
```

### RPU (Reward Processing Unit) — 10 models, 4 layers

```
Layer 0: DAED ──────────────────────────
              │      │      │      │
Layer 1: MORMR ── RPEM ── IUCP ── MCCN
              │      │      │      │
Layer 2: MEAMR ── SSRI ── LDAC ── IOTMS
                                │
Layer 3: SSPS ─────────────────┘
```

---

## 11. Framework Comparison Summary

| Feature | Current MI | DCM/SPM | HNN | BluePyOpt | **Proposed MI** |
|---------|-----------|---------|-----|-----------|----------------|
| Processing depth | None | Forward/backward | Proximal/distal | L1-L6 laminar | **0-5 depth** |
| Intra-module hierarchy | Flat | N/A | N/A | 6 layers | **Layer 0-4** |
| Connection types | None | Fwd/back/lateral | Proximal/distal | Excitatory/inhibitory | **Fwd/back/lateral** |
| Pathway count | 5 | Variable | 2 | Variable | **12** |
| Feedback | None | Yes | Yes | Yes | **Yes (P9, P12)** |
| Conduction delays | None | Yes (1-20ms) | Yes | Yes | **Planned** |
| Bidirectional | Partial (P2) | Yes | Yes | Yes | **Yes** |
| Hub identification | None | Analysis tool | N/A | N/A | **STU + ARU** |

---

## 12. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Output changes break downstream | Low | High | Phase A is purely additive, default values ensure backward compat |
| Performance regression | Low | Medium | Depth groups are small (2-5 models), units still parallel |
| Circular dependencies | Medium | Medium | STU has known cycles; implement 2-iteration settling for HGSIC↔OMS↔ETAM |
| Model build process changes | Low | Low | Building workflow adds 3 attributes per model, same doc-to-code process |
| Pathway routing complexity | Medium | Medium | Start with unit-level routing (current), add model-specific in Phase C |

---

## 13. Decision Points

Before implementation, the following decisions need user input:

1. **Implementation order**: Phase A→B→C→D (infrastructure first) or interleave with model building?
2. **Feedback pathways**: Implement in v1.0 or defer to v1.1?
3. **Conduction delays**: Real-time simulation or abstracted as weights?
4. **STU circular deps**: 2-iteration settling or break the cycle by designating a primary?
5. **Neurochemical activation**: Wire DA/NE/opioid/5-HT into runtime, or keep decorative for now?

---

## 14. References

### Brain Modeling Frameworks
- Bekolay et al. (2014). Nengo: A Python tool for building large-scale functional brain models. *Frontiers in Neuroinformatics*, 8, 48.
- Sanz Leon et al. (2013). The Virtual Brain: A simulator of primate brain network dynamics. *Frontiers in Neuroinformatics*, 7, 10.
- Gewaltig & Diesmann (2007). NEST (NEural Simulation Tool). *Scholarpedia*, 2(4), 1430.
- Stimberg et al. (2019). Brian 2: An intuitive and efficient neural simulator. *eLife*, 8, e47314.
- Van Geit et al. (2016). BluePyOpt: Leveraging open source software and cloud computing for neuroscience model optimization. *Frontiers in Neuroinformatics*, 10, 17.
- Neymotin et al. (2020). Human Neocortical Neurosolver (HNN). *eLife*, 9, e51214.
- Friston et al. (2003). Dynamic causal modelling. *NeuroImage*, 19(4), 1273-1302.

### Auditory Neuroscience
- Zatorre et al. (2002). Structure and function of auditory cortex. *Trends in Cognitive Sciences*, 6(1), 37-46.
- Hickok & Poeppel (2007). Cortical organization of speech processing: Dual-stream model. *Nature Reviews Neuroscience*, 8, 393-402.
- Rauschecker & Scott (2009). Maps and streams in the auditory cortex. *Current Opinion in Neurobiology*, 19(1), 43-48.
- Salimpoor et al. (2011). Anatomically distinct dopamine release during anticipation and experience of peak emotion to music. *Nature Neuroscience*, 14, 257-262.
- Koelsch (2014). Brain correlates of music-evoked emotions. *Nature Reviews Neuroscience*, 15, 170-180.
- Blood & Zatorre (2001). Intensely pleasurable responses to music correlate with activity in brain regions implicated in reward and emotion. *PNAS*, 98(20), 11818-11823.
- Lakatos et al. (2008). Entrainment of neuronal oscillations as a mechanism of attentional selection. *Science*, 320, 110-113.
- Rao & Ballard (1999). Predictive coding in the visual cortex. *Nature Neuroscience*, 2, 79-87.
