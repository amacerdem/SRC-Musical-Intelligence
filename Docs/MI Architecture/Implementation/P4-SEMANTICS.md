# Phase 4: Semantics — L³ Semantic Interpretation

**Phase**: P4
**Depends on**: P1 (contracts), P3 (brain — for BrainOutput type)
**Output**: 25 Python files in `Musical_Intelligence/semantics/`
**Gate**: G4 — L3Orchestrator produces (B, T, 104) tensor

---

## Overview

L³ maps 1,006D brain output to 104D semantic space through 8 epistemological groups,
9 unit adapters, and a 96-term vocabulary system. Groups execute in dependency order:

```
Phase 1 (parallel):   α(6D), β(14D), γ(13D), δ(12D)  ← BrainOutput only
Phase 1b (stateful):  ε(19D)                            ← BrainOutput (accumulates state)
Phase 2a:             ζ(12D)                             ← ε output
Phase 2b:             η(12D)                             ← ζ output
Phase 2c:             θ(16D)                             ← ε + ζ output
Assembly:             cat([α,β,γ,δ,ε,ζ,η,θ]) → (B,T,104)
```

---

## P4.1 — Semantic Groups (8 files)

### `semantics/groups/__init__.py`

**Purpose**: Re-export all 8 group classes.

---

### `semantics/groups/alpha.py`

**Purpose**: Computation semantics — HOW was this computed? [0:6] 6D

**Primary Docs**:
- `Docs/L³/Groups/Independent/Alpha.md` — formulas, dimension names, auto-configuration
- `Docs/L³/Contracts/BaseSemanticGroup.md` — ABC interface

**Related Docs**:
- `Docs/L³/Epistemology/Level-1-Computation.md` — epistemological basis
- `Docs/L³/Registry/DimensionCatalog.md` — dimension indices [0:6]

**Depends On**: `contracts/bases/base_semantic_group.py`, `contracts/dataclasses/semantic_output.py`

**Exports**: `AlphaGroup(BaseSemanticGroup)`

**Key Constraints**:
- LEVEL=1, GROUP_NAME="alpha", OUTPUT_DIM=6
- Per-unit attribution: `mean(unit_tensor, dim=-1)` for each active unit
- Computation certainty: `1 / (1 + Var(Brain))`
- Bipolar activation: `(mean(Brain) - 0.5) * 2 * 0.5 + 0.5`
- Auto-configurable dimensionality on first compute() call

**Verification Checklist**:
- [ ] OUTPUT_DIM matches doc (6D)
- [ ] Formulas match Alpha.md exactly
- [ ] Auto-configuration logic works with variable unit counts

---

### `semantics/groups/beta.py`

**Purpose**: Neuroscience semantics — WHERE in the brain? [6:20] 14D

**Primary Docs**:
- `Docs/L³/Groups/Independent/Beta.md` — region averaging, neurotransmitter proxies, circuit states

**Related Docs**:
- `Docs/L³/Epistemology/Level-2-Neuroscience.md`
- `Docs/C³/Regions/Cortical.md`, `Subcortical.md`, `Brainstem.md` — region definitions
- `Docs/C³/Neurochemicals/Dopamine.md`, `Opioid.md` — neurotransmitter models

**Depends On**: `contracts/bases/base_semantic_group.py`, `brain/regions/registry.py`

**Exports**: `BetaGroup(BaseSemanticGroup)`

**Key Constraints**:
- LEVEL=2, OUTPUT_DIM=14
- Brain regions (8D): NAcc, Caudate, VTA, SN, STG, IFG, Amygdala, Hippocampus
- Neurotransmitter dynamics (3D): dopamine proxy, opioid proxy, DA×Opioid interaction
- Circuit states (3D): anticipation, consummation, learning
- Formulas: region = mean(activations from models declaring that region)
- Default: 0.5 for absent regions

**Verification Checklist**:
- [ ] 14D total (8+3+3)
- [ ] Region averaging uses ModelRegistry brain_regions
- [ ] Dopamine proxy: `(NAcc + Caudate) / 2`
- [ ] All formulas from Beta.md reproduced

---

### `semantics/groups/gamma.py`

**Purpose**: Psychology semantics — WHAT subjectively? [20:33] 13D

**Primary Docs**:
- `Docs/L³/Groups/Independent/Gamma.md` — reward, ITPRA, aesthetics, emotion, chills

**Related Docs**:
- `Docs/L³/Epistemology/Level-3-Psychology.md`

**Depends On**: `contracts/bases/base_semantic_group.py`

**Exports**: `GammaGroup(BaseSemanticGroup)`

**Key Constraints**:
- LEVEL=3, OUTPUT_DIM=13
- Reward (3D): intensity, type (liking-wanting dissociation), phase
- ITPRA (2D): tension-resolution, surprise-evaluation (Huron's model)
- Aesthetics (3D): beauty, sublime (pleasure×arousal), groove (arousal×harmonic_context)
- Emotion (2D): valence, arousal (Russell's circumplex)
- Chills (3D): probability (SCR×(1-HR)), intensity, phase
- Uses `_safe_get_dim()` with 0.5 default for missing signals

**Verification Checklist**:
- [ ] 13D = 3+2+3+2+3
- [ ] All formulas from Gamma.md
- [ ] `_safe_get_dim()` graceful degradation

---

### `semantics/groups/delta.py`

**Purpose**: Validation semantics — HOW to test? [33:45] 12D

**Primary Docs**:
- `Docs/L³/Groups/Independent/Delta.md` — physiological, neural, behavioral, temporal

**Related Docs**:
- `Docs/L³/Epistemology/Level-4-Validation.md`

**Depends On**: `contracts/bases/base_semantic_group.py`

**Exports**: `DeltaGroup(BaseSemanticGroup)`

**Key Constraints**:
- LEVEL=4, OUTPUT_DIM=12
- Physiological (4D): SCR (d=0.85), HR, pupil, piloerection
- Neural (3D): fMRI NAcc BOLD (r=0.84), fMRI Caudate BOLD (r=0.71), EEG frontal alpha
- Behavioral (2D): willingness-to-pay, button-press rating
- Temporal (3D): wanting-leads-liking, RPE latency, refractory state
- Every dimension maps to a real-world measurement with known effect sizes

**Verification Checklist**:
- [ ] 12D = 4+3+2+3
- [ ] Effect sizes documented in docstring
- [ ] Formulas from Delta.md

---

### `semantics/groups/epsilon.py`

**Purpose**: Learning dynamics — HOW does listener learn? [45:64] 19D (STATEFUL)

**Primary Docs**:
- `Docs/L³/Groups/Independent/Epsilon.md` — CRITICAL: stateful accumulation, EMA, Markov, ring buffer

**Related Docs**:
- `Docs/L³/Epistemology/Level-5-Learning.md`
- `Docs/L³/Contracts/EpsilonStateContract.md` — state lifecycle, hyperparameters
- `Docs/L³/Pipeline/StateManagement.md` — reset protocol

**Depends On**: `contracts/bases/base_semantic_group.py`

**Exports**: `EpsilonGroup(BaseSemanticGroup)`

**Key Constraints**:
- LEVEL=5, OUTPUT_DIM=19, **STATEFUL** (must reset between audio files)
- Hyperparameters: ALPHA_SHORT=0.1, ALPHA_MEDIUM=0.01, ALPHA_LONG=0.001
- N_STATES=8, BUFFER_SIZE=50
- State components:
  - 3 EMA accumulators (short/medium/long) + 3 variance trackers
  - Welford online variance (count, mean, M2) for numerical stability
  - (B, 8, 8) Markov transition matrix (Laplace-smoothed)
  - (B, 50) ring buffer for compression progress
  - Previous frame pleasure cache
- 7 subcategories (19D total):
  - Surprise & Entropy (2D)
  - Prediction Errors (3D, 3 timescales)
  - Precision (2D, Bayesian confidence)
  - Information Dynamics (3D)
  - Interaction (1D): entropy × surprise (Cheung 2019)
  - ITPRA Mapping (5D, Huron's 5 stages)
  - Reward & Aesthetics (3D)
- Memory: ~588 bytes per batch element
- Compression progress: Schmidhuber's curiosity signal

**Verification Checklist**:
- [ ] 19D total
- [ ] State initialization on first compute()
- [ ] reset() clears all state
- [ ] EMA constants match doc exactly
- [ ] Markov transition matrix is Laplace-smoothed
- [ ] Ring buffer size = 50
- [ ] All 19 dimension formulas from Epsilon.md

---

### `semantics/groups/zeta.py`

**Purpose**: Polarity — WHICH direction? [64:76] 12D (BIPOLAR [-1,+1])

**Primary Docs**:
- `Docs/L³/Groups/Dependent/Zeta.md` — bipolar transform, 3 axis categories

**Related Docs**:
- `Docs/L³/Epistemology/Level-6-Polarity.md`

**Depends On**: `contracts/bases/base_semantic_group.py`, `epsilon.py` (reads ε output)

**Exports**: `ZetaGroup(BaseSemanticGroup)`

**Key Constraints**:
- LEVEL=6, OUTPUT_DIM=12
- ONLY group with [-1, +1] output range (all others [0, 1])
- Receives epsilon_output via **kwargs
- Reward axes (6D): valence, arousal, tension, power, wanting, liking — all `2*x - 1` transform
- Learning axes (3D): novelty, complexity, stability — from epsilon dims
- Aesthetic axes (3D): beauty, groove, engagement

**Verification Checklist**:
- [ ] 12D = 6+3+3
- [ ] Output range [-1, +1] (NOT [0, 1])
- [ ] Reads epsilon output correctly
- [ ] Transform: `2 * brain_value - 1`

---

### `semantics/groups/eta.py`

**Purpose**: Vocabulary — WHAT word? [76:88] 12D (96 terms, 64 gradations)

**Primary Docs**:
- `Docs/L³/Groups/Dependent/Eta.md` — 64-gradation quantization, 96-term vocabulary

**Related Docs**:
- `Docs/L³/Vocabulary/TermCatalog.md` — all 96 terms
- `Docs/L³/Vocabulary/AxisDefinitions.md` — 12 axes defined
- `Docs/L³/Epistemology/Level-7-Vocabulary.md`

**Depends On**: `contracts/bases/base_semantic_group.py`, `zeta.py` (reads ζ output)

**Exports**: `EtaGroup(BaseSemanticGroup)`

**Key Constraints**:
- LEVEL=7, OUTPUT_DIM=12
- Receives zeta_output via **kwargs
- Quantization: `ζ [-1,+1] → (x+1)/2 [0,1] → *63, round, clamp [0,63] → /63 [0,1]`
- 12 axes × 8 bands × 8 gradations = 64 levels per axis
- Step size: 1/64 = 1.5625% (below human JND of ~3%)
- `get_terms(tensor)` method returns list of vocabulary strings
- 96 vocabulary terms must be hardcoded (12 axes × 8 bands)

**Verification Checklist**:
- [ ] 12D output
- [ ] Quantization formula matches doc
- [ ] All 96 vocabulary terms present
- [ ] `get_terms()` method works
- [ ] Reads zeta output correctly

---

### `semantics/groups/theta.py`

**Purpose**: Narrative — LANGUAGE structure [88:104] 16D

**Primary Docs**:
- `Docs/L³/Groups/Dependent/Theta.md` — 4 narrative slots (subject, predicate, modifier, connector)

**Related Docs**:
- `Docs/L³/Epistemology/Level-8-Narrative.md`

**Depends On**: `contracts/bases/base_semantic_group.py`, `epsilon.py`, `zeta.py`

**Exports**: `ThetaGroup(BaseSemanticGroup)`

**Key Constraints**:
- LEVEL=8, OUTPUT_DIM=16
- Receives epsilon_output AND zeta_output via **kwargs
- Subject (4D): reward/tension/motion/beauty salience (softmax at temp=3.0)
- Predicate (4D): rising/peaking/falling/stable (temporal dynamics)
- Modifier (4D): intensity/certainty/novelty/speed
- Connector (4D): continuing/contrasting/resolving/transitioning
- Softmax temperature = 3.0 for subject competition

**Verification Checklist**:
- [ ] 16D = 4+4+4+4
- [ ] Softmax temperature = 3.0
- [ ] Reads both epsilon and zeta outputs
- [ ] All formulas from Theta.md

---

## P4.2 — Unit Adapters (9 files)

### Adapter Template

Each adapter maps unit-specific output dimensions to semantic labels. All are currently stubs awaiting real mapping.

**Primary Docs** (for each adapter):
- `Docs/L³/Adapters/{UNIT}-L3-ADAPTER.md` — per-unit semantic mapping
- `Docs/L³/Contracts/BaseModelSemanticAdapter.md` — ABC interface
- `Docs/C³/Units/{UNIT}.md` — unit output structure

**Depends On**: `contracts/bases/base_semantic_group.py` (for adapter base)

**Key Constraints**:
- Each adapter has `UNIT_NAME` constant
- Method: `adapt(unit_output) → Dict[str, Tensor]`
- Must extract specific dimension ranges and label them semantically

### Adapter Roster

| File | Unit | Semantic Focus | Primary Doc |
|------|------|---------------|-------------|
| `spu_adapter.py` | SPU | consonance→beauty, timbre→complexity | `Docs/L³/Adapters/SPU-L3-ADAPTER.md` |
| `stu_adapter.py` | STU | beat→groove, tempo→arousal | `Docs/L³/Adapters/STU-L3-ADAPTER.md` |
| `imu_adapter.py` | IMU | familiarity→stability | `Docs/L³/Adapters/IMU-L3-ADAPTER.md` |
| `asu_adapter.py` | ASU | novelty→surprise | `Docs/L³/Adapters/ASU-L3-ADAPTER.md` |
| `ndu_adapter.py` | NDU | deviation→surprise, PE→tension | `Docs/L³/Adapters/NDU-L3-ADAPTER.md` |
| `mpu_adapter.py` | MPU | groove→groove, movement→motion | `Docs/L³/Adapters/MPU-L3-ADAPTER.md` |
| `pcu_adapter.py` | PCU | PE→surprise, certainty→stability | `Docs/L³/Adapters/PCU-L3-ADAPTER.md` |
| `aru_adapter.py` | ARU | pleasure→valence, tension→tension | `Docs/L³/Adapters/ARU-L3-ADAPTER.md` |
| `rpu_adapter.py` | RPU | DA→wanting, opioid→liking | `Docs/L³/Adapters/RPU-L3-ADAPTER.md` |

**Verification Checklist** (per adapter):
- [ ] UNIT_NAME matches unit code
- [ ] adapt() returns Dict[str, Tensor] with correct keys
- [ ] Dimension extraction indices match unit output structure

---

## P4.3 — Vocabulary System (3 files)

### `semantics/vocabulary/terms.py`

**Purpose**: 96 vocabulary terms (12 axes × 8 bands).

**Primary Docs**:
- `Docs/L³/Vocabulary/TermCatalog.md` — complete 96-term list
- `Docs/L³/Groups/Dependent/Eta.md` — term-to-band mapping

**Exports**: `VOCABULARY: Dict[str, Tuple[str, ...]]` (axis_name → 8 terms)

**Key Constraints**:
- 12 axes: valence, arousal, tension, power, wanting, liking, novelty, complexity,
  beauty, groove, stability, engagement
- 8 bands per axis (e.g., valence: devastating→euphoric)
- All 96 terms must exactly match doc

---

### `semantics/vocabulary/axes.py`

**Purpose**: 12 semantic axis definitions.

**Primary Docs**:
- `Docs/L³/Vocabulary/AxisDefinitions.md` — axis names, polarities, ranges

**Exports**: `AXES: List[AxisDef]`

---

### `semantics/vocabulary/gradations.py`

**Purpose**: 64-gradation quantization system.

**Primary Docs**:
- `Docs/L³/Groups/Dependent/Eta.md` — quantization formula and JND rationale

**Exports**: `quantize()`, `N_GRADATIONS=64`, `N_BANDS=8`

---

## P4.4 — Orchestrator

### `semantics/orchestrator.py`

**Purpose**: L3Orchestrator — coordinates 8 groups in dependency order.

**Primary Docs**:
- `Docs/L³/Contracts/L3Orchestrator.md` — construction, execution phases, reset
- `Docs/L³/Pipeline/DependencyDAG.md` — phase ordering

**Related Docs**:
- `Docs/L³/L3-SEMANTIC-ARCHITECTURE.md` — overall architecture

**Depends On**: All 8 group files, `contracts/dataclasses/semantic_output.py`

**Exports**: `L3Orchestrator`

**Key Constraints**:
- Construction: OrderedDict of 8 groups in execution order
- Execution phases:
  - Phase 1: α, β, γ, δ (independent, potentially parallel)
  - Phase 1b: ε (stateful)
  - Phase 2a: ζ (needs ε output)
  - Phase 2b: η (needs ζ output)
  - Phase 2c: θ (needs ε + ζ output)
  - Assembly: `torch.cat(all_tensors, dim=-1)` → (B, T, 104)
- Method: `compute(brain_output) → L3Output`
- Method: `reset()` → delegates to epsilon group
- Property: `total_dim` = sum of all group OUTPUT_DIM = 104

**Verification Checklist**:
- [ ] Produces (B, T, 104) tensor
- [ ] Phase ordering respected (ε before ζ, ζ before η, etc.)
- [ ] reset() clears epsilon state
- [ ] total_dim == 104

---

## Verification Gate G4

```python
from Musical_Intelligence.semantics import L3Orchestrator
import torch

orchestrator = L3Orchestrator()
assert orchestrator.total_dim == 104

# Mock brain output (B=2, T=100, D=1006)
brain_output = torch.rand(2, 100, 1006)
l3_output = orchestrator.compute(brain_output)

assert l3_output.shape == (2, 100, 104), f"Expected (2,100,104), got {l3_output.shape}"
assert l3_output.min() >= -1.0  # zeta group can be [-1,+1]
assert l3_output.max() <= 1.0

# Test reset
orchestrator.reset()
l3_output_2 = orchestrator.compute(brain_output)
assert l3_output_2.shape == (2, 100, 104)

print("G4 PASSED: L3Orchestrator produces (B,T,104) with correct range")
```
