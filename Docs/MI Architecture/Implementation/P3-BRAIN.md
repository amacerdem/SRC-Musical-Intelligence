# Phase 3: Brain -- C3 Cognitive Models

**Phase**: P3
**Depends on**: P1 (Contracts), P2 (Ear -- R3 + H3)
**Output**: 156 Python files in `Musical_Intelligence/brain/`
**Gate**: G3 -- all 96 models instantiate, `validate_constants()` passes for each

---

## Overview

Phase 3 implements the entire C3 cognitive brain layer: 10 shared mechanisms, 9 cognitive units containing 96 models, 5 cross-unit pathways, 6 circuit definitions, brain region registries, neurochemical systems, and the BrainOrchestrator that sequences the 5-phase execution.

Implementation follows the sub-phase order from MASTER-PLAN.md section 3:

| Sub-phase | Contents | File Count |
|-----------|----------|:----------:|
| P3.1 | 10 Mechanisms | 10 |
| P3.2 | MechanismRunner | 2 |
| P3.3 | Supporting infrastructure (circuits, regions, neurochemicals) | 10 |
| P3.4 | 9 Unit shells | 18 |
| P3.5 | 96 Models (3 batches) | 96 |
| P3.6 | 5 Pathways + PathwayRunner | 7 |
| P3.7 | BrainOrchestrator | 2 |
| | **Total** | **~145** |

---

## P3.1 -- Mechanisms (10 files)

Each mechanism is a `BaseMechanism` subclass producing `(B, T, 30)` output. Mechanisms are computed once and cached by the MechanismRunner.

### `brain/mechanisms/__init__.py`

**Purpose**: Re-export all 10 mechanism classes and MechanismRunner.
**Exports**: `PPC, TPC, BEP, ASA, TMH, MEM, SYN, AED, CPD, C0P, MechanismRunner`

---

### `brain/mechanisms/ppc.py`

**Purpose**: Pitch Processing Chain -- spectral pitch extraction across 3 horizons.

**Primary Docs**:
- `Docs/C³/Mechanisms/PPC.md` -- all fields, h3_demand, compute() formula, horizons

**Related Docs**:
- `Docs/C³/Contracts/BaseMechanism.md` -- ABC interface
- `Docs/C³/Circuits/Perceptual.md` -- circuit context
- `Docs/C³/Matrices/Mechanism-Map.md` -- which models use PPC

**Depends On**:
- `contracts/bases/base_mechanism.py`

**Exports**: `PPC`

**Key Constraints**:
- NAME = "PPC", FULL_NAME = "Pitch Processing Chain"
- OUTPUT_DIM = 30, HORIZONS = (0, 3, 6) -- H0 (5.8ms), H3 (23ms), H6 (200ms)
- 3 x 10D sub-sections: pitch extraction, interval analysis, contour tracking
- Used by: BCH, PSCL, PCCR, SDNPS, ESME, SDED, SPH, HTP, PSH, PWUP, TPRD, SDD

**Verification Checklist**:
- [ ] NAME, FULL_NAME, OUTPUT_DIM, HORIZONS match PPC.md
- [ ] h3_demand property returns correct set of 4-tuples
- [ ] compute() signature matches BaseMechanism
- [ ] Output shape is (B, T, 30)

---

### `brain/mechanisms/tpc.py`

**Purpose**: Timbre Processing Chain -- spectral shape and temporal envelope analysis.

**Primary Docs**:
- `Docs/C³/Mechanisms/TPC.md` -- all fields, h3_demand, compute() formula

**Related Docs**:
- `Docs/C³/Contracts/BaseMechanism.md` -- ABC interface
- `Docs/C³/Circuits/Perceptual.md` -- circuit context

**Depends On**:
- `contracts/bases/base_mechanism.py`

**Exports**: `TPC`

**Key Constraints**:
- NAME = "TPC", FULL_NAME = "Timbre Processing Chain"
- OUTPUT_DIM = 30, HORIZONS = (6, 12, 16) -- H6 (200ms), H12 (525ms), H16 (1s)
- 3 x 10D: spectral shape, temporal envelope, source identity
- Used by: STAI, TSCP, MIAA, TPIO, IGFE, HTP, PSH

**Verification Checklist**:
- [ ] Constants match TPC.md
- [ ] h3_demand covers all 3 horizons
- [ ] Output shape (B, T, 30)

---

### `brain/mechanisms/bep.py`

**Purpose**: Beat Entrainment Processing -- rhythmic synchronization and motor coupling.

**Primary Docs**:
- `Docs/C³/Mechanisms/BEP.md` -- all fields, h3_demand, compute() formula

**Related Docs**:
- `Docs/C³/Contracts/BaseMechanism.md` -- ABC interface
- `Docs/C³/Circuits/Sensorimotor.md` -- circuit context

**Depends On**:
- `contracts/bases/base_mechanism.py`

**Exports**: `BEP`

**Key Constraints**:
- NAME = "BEP", FULL_NAME = "Beat Entrainment Processing"
- OUTPUT_DIM = 30, HORIZONS = (6, 9, 11) -- H6 (200ms), H9 (350ms), H11 (525ms)
- 3 x 10D: beat entrainment, motor coupling, groove
- Most-used mechanism (26+ models across STU, ASU, MPU)

**Verification Checklist**:
- [ ] Constants match BEP.md
- [ ] h3_demand covers all 3 horizons
- [ ] Output shape (B, T, 30)

---

### `brain/mechanisms/asa.py`

**Purpose**: Auditory Scene Analysis -- attention gating and salience weighting.

**Primary Docs**:
- `Docs/C³/Mechanisms/ASA.md` -- all fields, h3_demand, compute() formula

**Related Docs**:
- `Docs/C³/Contracts/BaseMechanism.md` -- ABC interface
- `Docs/C³/Circuits/Salience.md` -- circuit context

**Depends On**:
- `contracts/bases/base_mechanism.py`

**Exports**: `ASA`

**Key Constraints**:
- NAME = "ASA", FULL_NAME = "Auditory Scene Analysis"
- OUTPUT_DIM = 30, HORIZONS = (3, 6, 9) -- H3 (23ms), H6 (200ms), H9 (350ms)
- 3 x 10D: scene analysis, attention gating, salience weighting
- Used by 21+ models across ASU, NDU, and others

**Verification Checklist**:
- [ ] Constants match ASA.md
- [ ] h3_demand covers all 3 horizons
- [ ] Output shape (B, T, 30)

---

### `brain/mechanisms/tmh.py`

**Purpose**: Temporal Memory Hierarchy -- sequence integration across multiple timescales.

**Primary Docs**:
- `Docs/C³/Mechanisms/TMH.md` -- all fields, h3_demand, compute() formula

**Related Docs**:
- `Docs/C³/Contracts/BaseMechanism.md` -- ABC interface
- `Docs/C³/Circuits/Sensorimotor.md` -- circuit context

**Depends On**:
- `contracts/bases/base_mechanism.py`

**Exports**: `TMH`

**Key Constraints**:
- NAME = "TMH", FULL_NAME = "Temporal Memory Hierarchy"
- OUTPUT_DIM = 30, HORIZONS = (16, 18, 20, 22) -- H16 (1s), H18 (2s), H20 (5s), H22 (15s)
- 4 horizons (exception to 3-horizon convention); 30D still holds
- Used by: HMCE, AMSC, HGSIC, TMRM, MEAMN, PMIM, MCCN, CDMR

**Verification Checklist**:
- [ ] Constants match TMH.md
- [ ] 4 horizons correctly declared
- [ ] Output shape (B, T, 30)

---

### `brain/mechanisms/mem.py`

**Purpose**: Memory Encoding/Retrieval -- working memory, long-term memory, prediction buffer.

**Primary Docs**:
- `Docs/C³/Mechanisms/MEM.md` -- all fields, h3_demand, compute() formula

**Related Docs**:
- `Docs/C³/Contracts/BaseMechanism.md` -- ABC interface
- `Docs/C³/Circuits/Mnemonic.md` -- circuit context

**Depends On**:
- `contracts/bases/base_mechanism.py`

**Exports**: `MEM`

**Key Constraints**:
- NAME = "MEM", FULL_NAME = "Memory Encoding / Retrieval"
- OUTPUT_DIM = 30, HORIZONS = (18, 20, 22, 25) -- H18 (2s), H20 (5s), H22 (15s), H25 (60s)
- 4 horizons; longest timescale mechanism (up to 60s)
- Used by: MEAMN, PNH, MMP, HCMC, OII, CDEM, CSSL, DMMS, RIRI, VRIAP, CMAPCC, RASN, PMIM, and others

**Verification Checklist**:
- [ ] Constants match MEM.md
- [ ] 4 horizons including H25
- [ ] Output shape (B, T, 30)

---

### `brain/mechanisms/syn.py`

**Purpose**: Syntactic Processing -- musical syntax in Broca's area analog.

**Primary Docs**:
- `Docs/C³/Mechanisms/SYN.md` -- all fields, h3_demand, compute() formula

**Related Docs**:
- `Docs/C³/Contracts/BaseMechanism.md` -- ABC interface
- `Docs/C³/Circuits/Mnemonic.md` -- circuit context

**Depends On**:
- `contracts/bases/base_mechanism.py`

**Exports**: `SYN`

**Key Constraints**:
- NAME = "SYN", FULL_NAME = "Syntactic Processing"
- OUTPUT_DIM = 30, HORIZONS = (12, 16, 18) -- H12 (525ms), H16 (1s), H18 (2s)
- Least-used mechanism (only MSPBA); still cached for consistency
- 3 x 10D sub-sections

**Verification Checklist**:
- [ ] Constants match SYN.md
- [ ] h3_demand covers all 3 horizons
- [ ] Output shape (B, T, 30)

---

### `brain/mechanisms/aed.py`

**Purpose**: Affective Entrainment Dynamics -- valence tracking and arousal dynamics.

**Primary Docs**:
- `Docs/C³/Mechanisms/AED.md` -- all fields, h3_demand, compute() formula

**Related Docs**:
- `Docs/C³/Contracts/BaseMechanism.md` -- ABC interface
- `Docs/C³/Circuits/Mesolimbic.md` -- circuit context

**Depends On**:
- `contracts/bases/base_mechanism.py`

**Exports**: `AED`

**Key Constraints**:
- NAME = "AED", FULL_NAME = "Affective Entrainment Dynamics"
- OUTPUT_DIM = 30, HORIZONS = (6, 16) -- H6 (200ms), H16 (1s)
- 2 horizons (fewest of any mechanism); 30D convention still holds
- Used by 18+ models in ARU and RPU

**Verification Checklist**:
- [ ] Constants match AED.md
- [ ] 2 horizons correctly declared
- [ ] Output shape (B, T, 30)

---

### `brain/mechanisms/cpd.py`

**Purpose**: Chills and Peak Detection -- anticipation, peak experience, resolution phases.

**Primary Docs**:
- `Docs/C³/Mechanisms/CPD.md` -- all fields, h3_demand, compute() formula

**Related Docs**:
- `Docs/C³/Contracts/BaseMechanism.md` -- ABC interface
- `Docs/C³/Circuits/Mesolimbic.md` -- circuit context

**Depends On**:
- `contracts/bases/base_mechanism.py`

**Exports**: `CPD`

**Key Constraints**:
- NAME = "CPD", FULL_NAME = "Chills & Peak Detection"
- OUTPUT_DIM = 30, HORIZONS = (9, 16, 18) -- H9 (350ms), H16 (1s), H18 (2s)
- 3 x 10D: anticipation, peak experience, resolution
- Used by: SRP, AAC, PUPF, MAD, DAED, RPEM

**Verification Checklist**:
- [ ] Constants match CPD.md
- [ ] h3_demand covers all 3 horizons
- [ ] Output shape (B, T, 30)

---

### `brain/mechanisms/c0p.py`

**Purpose**: Cognitive Projection -- tension-expectation-approach dynamics.

**Primary Docs**:
- `Docs/C³/Mechanisms/C0P.md` -- all fields, h3_demand, compute() formula

**Related Docs**:
- `Docs/C³/Contracts/BaseMechanism.md` -- ABC interface
- `Docs/C³/Circuits/Mesolimbic.md` -- circuit context

**Depends On**:
- `contracts/bases/base_mechanism.py`

**Exports**: `C0P`

**Key Constraints**:
- NAME = "C0P", FULL_NAME = "Cognitive Projection"
- OUTPUT_DIM = 30, HORIZONS = (18, 19, 20) -- H18 (2s), H19 (3s), H20 (5s)
- 3 x 10D sub-sections
- Used by: SRP, VMM, MORMR, IUCP, ICEM, UDP

**Verification Checklist**:
- [ ] Constants match C0P.md (note: zero not letter O in name)
- [ ] h3_demand covers all 3 horizons
- [ ] Output shape (B, T, 30)

---

## P3.2 -- MechanismRunner

### `brain/mechanisms/runner.py`

**Purpose**: Compute all required mechanisms once, cache outputs for model reuse.

**Primary Docs**:
- `Docs/C³/Mechanisms/00-INDEX.md` -- MechanismRunner architecture
- `Docs/C³/Contracts/BaseMechanism.md` -- interface consumed

**Related Docs**:
- `Docs/C³/C3-ARCHITECTURE.md` -- Phase 1 execution context

**Depends On**:
- `contracts/bases/base_mechanism.py`
- All 10 mechanism files (P3.1)

**Exports**: `MechanismRunner`

**Key Constraints**:
- Scans model registry for unique MECHANISM_NAMES across all active models
- Instantiates each needed mechanism exactly once
- `run(h3_features, r3_features)` computes all, stores in cache dict
- `get(name)` returns cached `(B, T, 30)` tensor; raises if not yet computed
- Thread-safe cache (deterministic, but guard against misuse)
- No re-computation: if already cached, return immediately

**Verification Checklist**:
- [ ] Each mechanism computed exactly once per run() call
- [ ] get() returns correct shape (B, T, 30) for all 10 mechanisms
- [ ] get() raises KeyError or ValueError if mechanism not cached
- [ ] Cache cleared between frames/batches as appropriate

---

## P3.3 -- Supporting Infrastructure

### `brain/circuits/__init__.py`

**Purpose**: Re-export circuit definitions and registry.
**Exports**: `CircuitDef, CircuitRegistry, CIRCUITS, CIRCUIT_NAMES`

---

### `brain/circuits/definitions.py`

**Purpose**: 6 CircuitDef instances defining neural circuit groupings.

**Primary Docs**:
- `Docs/C³/Circuits/00-INDEX.md` -- 6 circuit definitions with units and mechanisms
- `Docs/C³/Circuits/Mesolimbic.md` -- mesolimbic circuit detail
- `Docs/C³/Circuits/Perceptual.md` -- perceptual circuit detail
- `Docs/C³/Circuits/Sensorimotor.md` -- sensorimotor circuit detail
- `Docs/C³/Circuits/Mnemonic.md` -- mnemonic circuit detail
- `Docs/C³/Circuits/Salience.md` -- salience circuit detail
- `Docs/C³/Circuits/Imagery.md` -- imagery circuit detail

**Related Docs**:
- `Docs/C³/Contracts/BaseCognitiveUnit.md` -- CIRCUIT field used in units

**Depends On**: Nothing (pure data).

**Exports**: `CIRCUITS` (dict), `CIRCUIT_NAMES` (tuple of 6)

**Key Constraints**:
- 6 circuits: mesolimbic, perceptual, sensorimotor, mnemonic, salience, imagery
- CIRCUITS (operational set) = 5 circuits (excludes imagery)
- CIRCUIT_NAMES = all 6
- Each CircuitDef: name, description, mechanisms (tuple of str), units (tuple of str), key_regions

**Verification Checklist**:
- [ ] 6 CircuitDef instances match Circuits/00-INDEX.md
- [ ] CIRCUITS has 5 entries, CIRCUIT_NAMES has 6
- [ ] Mechanism and unit assignments match docs exactly

---

### `brain/circuits/registry.py`

**Purpose**: CircuitRegistry for lookup by name, mechanism, or unit.

**Primary Docs**:
- `Docs/C³/Circuits/00-INDEX.md` -- cross-circuit mechanism sharing table

**Depends On**:
- `brain/circuits/definitions.py`

**Exports**: `CircuitRegistry`

**Key Constraints**:
- `get_by_name(name)` -> CircuitDef
- `get_by_mechanism(mech_name)` -> CircuitDef
- `get_by_unit(unit_name)` -> CircuitDef
- Immutable after initialization

**Verification Checklist**:
- [ ] All lookup methods return correct results
- [ ] Unknown name raises KeyError

---

### `brain/regions/__init__.py`

**Purpose**: Re-export region registries.
**Exports**: `BrainRegionRegistry, CORTICAL_REGIONS, SUBCORTICAL_REGIONS, BRAINSTEM_REGIONS`

---

### `brain/regions/cortical.py`

**Purpose**: Cortical brain regions with Brodmann areas and MNI152 coordinates.

**Primary Docs**:
- `Docs/C³/Regions/Cortical.md` -- all cortical regions, Brodmann areas, MNI coords, functions

**Related Docs**:
- `Docs/C³/Contracts/BrainRegion.md` -- BrainRegion dataclass definition

**Depends On**:
- `contracts/dataclasses/brain_region.py`

**Exports**: `CORTICAL_REGIONS` (tuple of BrainRegion)

**Key Constraints**:
- Each entry: name, abbreviation, hemisphere, mni_coords, brodmann_area, function
- Includes: Heschl's Gyrus, Planum Temporale, SMA, PMC, IFG, STG, etc.
- All cortical regions MUST have brodmann_area set (non-None)
- MNI convention: x (L-/R+), y (P-/A+), z (I-/S+)

**Verification Checklist**:
- [ ] All regions from Cortical.md present
- [ ] All have brodmann_area (is_cortical == True)
- [ ] MNI coordinates match doc values exactly

---

### `brain/regions/subcortical.py`

**Purpose**: Subcortical nuclei without Brodmann areas.

**Primary Docs**:
- `Docs/C³/Regions/Subcortical.md` -- all subcortical regions, MNI coords, functions

**Depends On**:
- `contracts/dataclasses/brain_region.py`

**Exports**: `SUBCORTICAL_REGIONS` (tuple of BrainRegion)

**Key Constraints**:
- Includes: NAcc, VTA, Amygdala, Hippocampus, Caudate, Putamen, Thalamus, etc.
- brodmann_area = None for all (is_subcortical == True)

**Verification Checklist**:
- [ ] All regions from Subcortical.md present
- [ ] All have brodmann_area = None
- [ ] MNI coordinates match doc values

---

### `brain/regions/brainstem.py`

**Purpose**: Brainstem structures.

**Primary Docs**:
- `Docs/C³/Regions/Brainstem.md` -- brainstem regions, MNI coords, functions

**Depends On**:
- `contracts/dataclasses/brain_region.py`

**Exports**: `BRAINSTEM_REGIONS` (tuple of BrainRegion)

**Key Constraints**:
- Includes: Inferior Colliculus, Cochlear Nucleus, etc.
- brodmann_area = None for all

**Verification Checklist**:
- [ ] All regions from Brainstem.md present
- [ ] MNI coordinates match doc values

---

### `brain/regions/registry.py`

**Purpose**: BrainRegionRegistry combining all region categories with MNI lookup.

**Primary Docs**:
- `Docs/C³/Regions/00-INDEX.md` -- registry overview and lookup interface

**Depends On**:
- `brain/regions/cortical.py`, `subcortical.py`, `brainstem.py`

**Exports**: `BrainRegionRegistry`

**Key Constraints**:
- Aggregates CORTICAL + SUBCORTICAL + BRAINSTEM into unified registry
- `get_by_name(name)` -> BrainRegion
- `get_by_abbreviation(abbrev)` -> BrainRegion
- `get_nearest_mni(x, y, z)` -> BrainRegion (Euclidean nearest)

**Verification Checklist**:
- [ ] All 3 category sets merged correctly
- [ ] Lookup by name and abbreviation both work
- [ ] MNI nearest neighbor lookup returns correct region

---

### `brain/neurochemicals/__init__.py`

**Purpose**: Re-export neurochemical systems.
**Exports**: `Dopamine, Opioid, Serotonin, Norepinephrine, NeurochemicalRegistry`

---

### `brain/neurochemicals/dopamine.py`

**Purpose**: Dopamine system metadata and state model.

**Primary Docs**:
- `Docs/C³/Neurochemicals/Dopamine.md` -- receptor types, pathways, musical functions

**Depends On**: Nothing (pure data + simple state).

**Exports**: `Dopamine`

**Verification Checklist**:
- [ ] All fields match Dopamine.md

---

### `brain/neurochemicals/opioid.py`

**Purpose**: Endogenous opioid system metadata.

**Primary Docs**:
- `Docs/C³/Neurochemicals/Opioid.md` -- mu-opioid receptor role in musical pleasure

**Exports**: `Opioid`

---

### `brain/neurochemicals/serotonin.py`

**Purpose**: Serotonin system metadata.

**Primary Docs**:
- `Docs/C³/Neurochemicals/Serotonin.md` -- serotonergic modulation of musical mood

**Exports**: `Serotonin`

---

### `brain/neurochemicals/norepinephrine.py`

**Purpose**: Norepinephrine system metadata.

**Primary Docs**:
- `Docs/C³/Neurochemicals/Norepinephrine.md` -- arousal and attention modulation

**Exports**: `Norepinephrine`

---

### `brain/neurochemicals/registry.py`

**Purpose**: NeurochemicalRegistry for lookup by name.

**Primary Docs**:
- `Docs/C³/Neurochemicals/00-INDEX.md` -- registry overview

**Depends On**:
- `brain/neurochemicals/dopamine.py`, `opioid.py`, `serotonin.py`, `norepinephrine.py`

**Exports**: `NeurochemicalRegistry`

**Verification Checklist**:
- [ ] All 4 neurochemical systems registered
- [ ] Lookup by name returns correct system

---

## P3.4 -- Unit Shells (9 units)

Each unit is a `BaseCognitiveUnit` subclass in `brain/units/{code}/unit.py` with a models sub-package. All 9 units follow the same template.

### Unit Template

Every `unit.py` must:

1. Override class constants: `UNIT_NAME`, `FULL_NAME`, `CIRCUIT`, `POOLED_EFFECT`
2. Import and instantiate all models from `models/` sub-package
3. Implement `models` property returning List[BaseModel]
4. Implement `compute(mechanism_outputs, h3_features, r3_features, cross_unit_inputs)` that:
   - Calls each model's compute() in tier order (alpha, beta, gamma)
   - Concatenates outputs along last dimension
   - Returns `(B, T, unit_dim)` tensor
5. Pass `validate_constants()` from BaseCognitiveUnit

Each `models/__init__.py` re-exports all model classes for that unit.

### `brain/units/spu/unit.py` (example -- all 9 follow this pattern)

**Purpose**: Spectral Processing Unit shell -- 9 models, 99D output.

**Primary Docs**:
- `Docs/C³/Units/SPU.md` -- UNIT_NAME, FULL_NAME, CIRCUIT, POOLED_EFFECT, model roster

**Related Docs**:
- `Docs/C³/Contracts/BaseCognitiveUnit.md` -- ABC interface
- `Docs/C³/C3-ARCHITECTURE.md` -- Phase 2 independent execution

**Depends On**:
- `contracts/bases/base_unit.py`
- All SPU model files in `brain/units/spu/models/`

**Exports**: `SPUUnit`

**Key Constraints**:
- UNIT_NAME = "SPU", FULL_NAME = "Spectral Processing Unit"
- CIRCUIT = "perceptual", POOLED_EFFECT = 0.84
- 9 models: BCH(12D), PSCL(12D), PCCR(11D), STAI(12D), TSCP(10D), MIAA(11D), SDNPS(10D), ESME(11D), SDED(10D)
- Total: 99D
- Dependency: Independent (no cross_unit_inputs needed)
- Pathway source: P1_SPU_ARU

**Verification Checklist**:
- [ ] 4 constants match SPU.md
- [ ] models property returns 9 models in tier order
- [ ] total_dim == 99
- [ ] validate_constants() passes
- [ ] compute() returns (B, T, 99)

---

### Unit Roster (all 9 units)

| Code File | Unit | Full Name | Circuit | d | Models | Dim | Dependency | Primary Doc |
|-----------|------|-----------|---------|-----|:------:|:---:|------------|-------------|
| `brain/units/spu/unit.py` | SPU | Spectral Processing | perceptual | 0.84 | 9 | 99 | Independent | `Docs/C³/Units/SPU.md` |
| `brain/units/stu/unit.py` | STU | Sensorimotor Timing | sensorimotor | 0.67 | 14 | 148 | Independent | `Docs/C³/Units/STU.md` |
| `brain/units/imu/unit.py` | IMU | Integrative Memory | mnemonic | 0.53 | 15 | 159 | Independent | `Docs/C³/Units/IMU.md` |
| `brain/units/asu/unit.py` | ASU | Auditory Salience | salience | 0.60 | 9 | 94 | Independent | `Docs/C³/Units/ASU.md` |
| `brain/units/ndu/unit.py` | NDU | Novelty Detection | salience | 0.55 | 9 | 94 | Independent | `Docs/C³/Units/NDU.md` |
| `brain/units/mpu/unit.py` | MPU | Motor Planning | sensorimotor | 0.62 | 10 | 104 | Independent | `Docs/C³/Units/MPU.md` |
| `brain/units/pcu/unit.py` | PCU | Predictive Coding | mnemonic | 0.58 | 10 | 94 | Independent | `Docs/C³/Units/PCU.md` |
| `brain/units/aru/unit.py` | ARU | Affective Resonance | mesolimbic | 0.83 | 10 | 120 | Dependent | `Docs/C³/Units/ARU.md` |
| `brain/units/rpu/unit.py` | RPU | Reward Processing | mesolimbic | 0.70 | 10 | 94 | Dependent | `Docs/C³/Units/RPU.md` |

Each unit also has `brain/units/{code}/__init__.py` and `brain/units/{code}/models/__init__.py`.

---

## P3.5 -- 96 Models (3 batches)

### Model Template

Every model file `brain/units/{unit}/models/{acronym}.py` follows the same pattern:

**Primary Docs** (MUST read fully):
- `Docs/C³/Models/{UNIT}-{tier}{n}-{ACRONYM}/{ACRONYM}.md` -- the 14-section model document

**Related Docs** (read for context):
- `Docs/C³/Contracts/BaseModel.md` -- ABC interface
- `Docs/C³/Units/{UNIT}.md` -- unit context
- `Docs/C³/Mechanisms/{MECH}.md` -- for each mechanism the model uses
- `Docs/C³/Matrices/R3-Usage.md` -- R3 index mapping
- `Docs/C³/Matrices/H3-Demand.md` -- H3 demand mapping
- `Docs/Beta/DISCREPANCY-REGISTRY.md` -- known doc vs code gaps (use doc values)

**Depends On**:
- `contracts/bases/base_model.py`
- `contracts/dataclasses/layer_spec.py`
- `contracts/dataclasses/demand_spec.py`
- `contracts/dataclasses/brain_region.py`
- `contracts/dataclasses/model_metadata.py`
- `contracts/dataclasses/citation.py`

**Doc-to-code mapping** (14 model doc sections):

| Doc Section | Code Element |
|-------------|-------------|
| 1. Overview | Class docstring |
| 2. Context | Class docstring (continued) |
| 3. Scientific Foundation | `metadata` property -- citations, evidence_tier |
| 4. R3 Input Mapping | `R3_INDICES` class constant (tuple of ints) |
| 5. H3 Temporal Demand | `h3_demand` property returning tuple of H3DemandSpec |
| 6. Output Space | `LAYERS` class constant (tuple of LayerSpec) |
| 7. Mathematical Formulation | `compute()` method body |
| 8. Brain Regions | `brain_regions` property returning tuple of BrainRegion |
| 9. Integration Context | Class docstring or comments |
| 10. Falsification Criteria | `metadata.falsification_criteria` |
| 11. Implementation Pseudocode | `compute()` method reference |
| 12. Version History | Version constant or metadata |
| 13. References | `metadata.citations` |
| 14. Extension Points | Comments (future work) |

**Key Constraints** (apply to ALL 96 models):
- Class constants: NAME, FULL_NAME, UNIT, TIER, OUTPUT_DIM, MECHANISM_NAMES, CROSS_UNIT_READS, LAYERS
- Abstract properties: h3_demand, dimension_names, brain_regions, metadata
- Abstract method: compute(mechanism_outputs, h3_features, r3_features, cross_unit_inputs)
- `validate_constants()` MUST pass
- LAYERS must cover [0, OUTPUT_DIM) with no gaps or overlaps
- Use doc values (v2), NOT old code values (v1), per DISCREPANCY-REGISTRY.md
- All h3_demand populated (not empty tuples)
- MECHANISM_NAMES from doc (may differ from old code)
- FULL_NAME from doc Section 1 header

**Verification Checklist** (apply to each model):
- [ ] NAME, FULL_NAME match model doc Section 1
- [ ] UNIT, TIER match model ID pattern
- [ ] OUTPUT_DIM == sum of all LayerSpec dims
- [ ] LAYERS cover [0, OUTPUT_DIM) contiguously
- [ ] R3_INDICES match doc Section 4
- [ ] h3_demand tuples match doc Section 5
- [ ] compute() implements doc Section 7 formulas
- [ ] brain_regions match doc Section 8 with MNI coords
- [ ] metadata.citations match doc Section 13
- [ ] metadata.falsification_criteria match doc Section 10
- [ ] validate_constants() passes
- [ ] File under 1000 lines

---

### Batch 1: SPU (9), STU (14), IMU (15) -- Independent, Parallelizable

Within each unit, implement in tier order: alpha -> beta -> gamma.

#### SPU Models (9 models, 99D total)

| # | Model ID | Acronym | Tier | Dim | Mechanisms | Code Path | Doc Path |
|---|----------|---------|------|:---:|------------|-----------|----------|
| 1 | SPU-a1-BCH | BCH | alpha | 12 | PPC | `brain/units/spu/models/bch.py` | `Docs/C³/Models/SPU-α1-BCH/BCH.md` |
| 2 | SPU-a2-PSCL | PSCL | alpha | 12 | PPC | `brain/units/spu/models/pscl.py` | `Docs/C³/Models/SPU-α2-PSCL/PSCL.md` |
| 3 | SPU-a3-PCCR | PCCR | alpha | 11 | PPC | `brain/units/spu/models/pccr.py` | `Docs/C³/Models/SPU-α3-PCCR/PCCR.md` |
| 4 | SPU-b1-STAI | STAI | beta | 12 | TPC | `brain/units/spu/models/stai.py` | `Docs/C³/Models/SPU-β1-STAI/STAI.md` |
| 5 | SPU-b2-TSCP | TSCP | beta | 10 | TPC | `brain/units/spu/models/tscp.py` | `Docs/C³/Models/SPU-β2-TSCP/TSCP.md` |
| 6 | SPU-b3-MIAA | MIAA | beta | 11 | TPC | `brain/units/spu/models/miaa.py` | `Docs/C³/Models/SPU-β3-MIAA/MIAA.md` |
| 7 | SPU-g1-SDNPS | SDNPS | gamma | 10 | PPC | `brain/units/spu/models/sdnps.py` | `Docs/C³/Models/SPU-γ1-SDNPS/SDNPS.md` |
| 8 | SPU-g2-ESME | ESME | gamma | 11 | PPC | `brain/units/spu/models/esme.py` | `Docs/C³/Models/SPU-γ2-ESME/ESME.md` |
| 9 | SPU-g3-SDED | SDED | gamma | 10 | PPC | `brain/units/spu/models/sded.py` | `Docs/C³/Models/SPU-γ3-SDED/SDED.md` |

#### STU Models (14 models, 148D total)

| # | Model ID | Acronym | Tier | Dim | Mechanisms | Code Path | Doc Path |
|---|----------|---------|------|:---:|------------|-----------|----------|
| 10 | STU-a1-HMCE | HMCE | alpha | 14 | BEP, TMH | `brain/units/stu/models/hmce.py` | `Docs/C³/Models/STU-α1-HMCE/HMCE.md` |
| 11 | STU-a2-AMSC | AMSC | alpha | 12 | BEP, TMH | `brain/units/stu/models/amsc.py` | `Docs/C³/Models/STU-α2-AMSC/AMSC.md` |
| 12 | STU-a3-MDNS | MDNS | alpha | 11 | BEP | `brain/units/stu/models/mdns.py` | `Docs/C³/Models/STU-α3-MDNS/MDNS.md` |
| 13 | STU-b1-AMSS | AMSS | beta | 10 | BEP | `brain/units/stu/models/amss.py` | `Docs/C³/Models/STU-β1-AMSS/AMSS.md` |
| 14 | STU-b2-TPIO | TPIO | beta | 10 | TPC | `brain/units/stu/models/tpio.py` | `Docs/C³/Models/STU-β2-TPIO/TPIO.md` |
| 15 | STU-b3-EDTA | EDTA | beta | 11 | BEP | `brain/units/stu/models/edta.py` | `Docs/C³/Models/STU-β3-EDTA/EDTA.md` |
| 16 | STU-b4-ETAM | ETAM | beta | 10 | BEP | `brain/units/stu/models/etam.py` | `Docs/C³/Models/STU-β4-ETAM/ETAM.md` |
| 17 | STU-b5-HGSIC | HGSIC | beta | 12 | BEP, TMH | `brain/units/stu/models/hgsic.py` | `Docs/C³/Models/STU-β5-HGSIC/HGSIC.md` |
| 18 | STU-b6-OMS | OMS | beta | 10 | BEP | `brain/units/stu/models/oms.py` | `Docs/C³/Models/STU-β6-OMS/OMS.md` |
| 19 | STU-g1-TMRM | TMRM | gamma | 10 | BEP, TMH | `brain/units/stu/models/tmrm.py` | `Docs/C³/Models/STU-γ1-TMRM/TMRM.md` |
| 20 | STU-g2-NEWMD | NEWMD | gamma | 10 | BEP | `brain/units/stu/models/newmd.py` | `Docs/C³/Models/STU-γ2-NEWMD/NEWMD.md` |
| 21 | STU-g3-MTNE | MTNE | gamma | 10 | BEP | `brain/units/stu/models/mtne.py` | `Docs/C³/Models/STU-γ3-MTNE/MTNE.md` |
| 22 | STU-g4-PTGMP | PTGMP | gamma | 9 | BEP | `brain/units/stu/models/ptgmp.py` | `Docs/C³/Models/STU-γ4-PTGMP/PTGMP.md` |
| 23 | STU-g5-MPFS | MPFS | gamma | 9 | BEP | `brain/units/stu/models/mpfs.py` | `Docs/C³/Models/STU-γ5-MPFS/MPFS.md` |

#### IMU Models (15 models, 159D total)

| # | Model ID | Acronym | Tier | Dim | Mechanisms | Code Path | Doc Path |
|---|----------|---------|------|:---:|------------|-----------|----------|
| 24 | IMU-a1-MEAMN | MEAMN | alpha | 14 | MEM, TMH | `brain/units/imu/models/meamn.py` | `Docs/C³/Models/IMU-α1-MEAMN/MEAMN.md` |
| 25 | IMU-a2-PNH | PNH | alpha | 12 | MEM | `brain/units/imu/models/pnh.py` | `Docs/C³/Models/IMU-α2-PNH/PNH.md` |
| 26 | IMU-a3-MMP | MMP | alpha | 11 | MEM | `brain/units/imu/models/mmp.py` | `Docs/C³/Models/IMU-α3-MMP/MMP.md` |
| 27 | IMU-b1-RASN | RASN | beta | 10 | BEP, MEM | `brain/units/imu/models/rasn.py` | `Docs/C³/Models/IMU-β1-RASN/RASN.md` |
| 28 | IMU-b2-PMIM | PMIM | beta | 11 | MEM, TMH | `brain/units/imu/models/pmim.py` | `Docs/C³/Models/IMU-β2-PMIM/PMIM.md` |
| 29 | IMU-b3-OII | OII | beta | 10 | MEM | `brain/units/imu/models/oii.py` | `Docs/C³/Models/IMU-β3-OII/OII.md` |
| 30 | IMU-b4-HCMC | HCMC | beta | 10 | MEM | `brain/units/imu/models/hcmc.py` | `Docs/C³/Models/IMU-β4-HCMC/HCMC.md` |
| 31 | IMU-b5-RIRI | RIRI | beta | 10 | MEM | `brain/units/imu/models/riri.py` | `Docs/C³/Models/IMU-β5-RIRI/RIRI.md` |
| 32 | IMU-b6-MSPBA | MSPBA | beta | 11 | SYN, MEM | `brain/units/imu/models/mspba.py` | `Docs/C³/Models/IMU-β6-MSPBA/MSPBA.md` |
| 33 | IMU-b7-VRIAP | VRIAP | beta | 10 | MEM | `brain/units/imu/models/vriap.py` | `Docs/C³/Models/IMU-β7-VRIAP/VRIAP.md` |
| 34 | IMU-b8-TPRD | TPRD | beta | 11 | PPC | `brain/units/imu/models/tprd.py` | `Docs/C³/Models/IMU-β8-TPRD/TPRD.md` |
| 35 | IMU-b9-CMAPCC | CMAPCC | beta | 10 | BEP, MEM | `brain/units/imu/models/cmapcc.py` | `Docs/C³/Models/IMU-β9-CMAPCC/CMAPCC.md` |
| 36 | IMU-g1-DMMS | DMMS | gamma | 10 | MEM | `brain/units/imu/models/dmms.py` | `Docs/C³/Models/IMU-γ1-DMMS/DMMS.md` |
| 37 | IMU-g2-CSSL | CSSL | gamma | 10 | MEM | `brain/units/imu/models/cssl.py` | `Docs/C³/Models/IMU-γ2-CSSL/CSSL.md` |
| 38 | IMU-g3-CDEM | CDEM | gamma | 9 | MEM | `brain/units/imu/models/cdem.py` | `Docs/C³/Models/IMU-γ3-CDEM/CDEM.md` |

---

### Batch 2: ASU (9), NDU (9), MPU (10), PCU (10) -- Independent, Parallelizable

#### ASU Models (9 models, 94D total)

| # | Model ID | Acronym | Tier | Dim | Mechanisms | Code Path | Doc Path |
|---|----------|---------|------|:---:|------------|-----------|----------|
| 39 | ASU-a1-SNEM | SNEM | alpha | 12 | BEP, ASA | `brain/units/asu/models/snem.py` | `Docs/C³/Models/ASU-α1-SNEM/SNEM.md` |
| 40 | ASU-a2-IACM | IACM | alpha | 11 | ASA | `brain/units/asu/models/iacm.py` | `Docs/C³/Models/ASU-α2-IACM/IACM.md` |
| 41 | ASU-a3-CSG | CSG | alpha | 12 | ASA | `brain/units/asu/models/csg.py` | `Docs/C³/Models/ASU-α3-CSG/CSG.md` |
| 42 | ASU-b1-BARM | BARM | beta | 10 | BEP, ASA | `brain/units/asu/models/barm.py` | `Docs/C³/Models/ASU-β1-BARM/BARM.md` |
| 43 | ASU-b2-STANM | STANM | beta | 10 | ASA | `brain/units/asu/models/stanm.py` | `Docs/C³/Models/ASU-β2-STANM/STANM.md` |
| 44 | ASU-b3-AACM | AACM | beta | 10 | ASA | `brain/units/asu/models/aacm.py` | `Docs/C³/Models/ASU-β3-AACM/AACM.md` |
| 45 | ASU-g1-PWSM | PWSM | gamma | 10 | ASA | `brain/units/asu/models/pwsm.py` | `Docs/C³/Models/ASU-γ1-PWSM/PWSM.md` |
| 46 | ASU-g2-DGTP | DGTP | gamma | 10 | ASA | `brain/units/asu/models/dgtp.py` | `Docs/C³/Models/ASU-γ2-DGTP/DGTP.md` |
| 47 | ASU-g3-SDL | SDL | gamma | 9 | ASA | `brain/units/asu/models/sdl.py` | `Docs/C³/Models/ASU-γ3-SDL/SDL.md` |

#### NDU Models (9 models, 94D total)

| # | Model ID | Acronym | Tier | Dim | Mechanisms | Code Path | Doc Path |
|---|----------|---------|------|:---:|------------|-----------|----------|
| 48 | NDU-a1-MPG | MPG | alpha | 12 | PPC, ASA | `brain/units/ndu/models/mpg.py` | `Docs/C³/Models/NDU-α1-MPG/MPG.md` |
| 49 | NDU-a2-SDD | SDD | alpha | 11 | PPC, ASA | `brain/units/ndu/models/sdd.py` | `Docs/C³/Models/NDU-α2-SDD/SDD.md` |
| 50 | NDU-a3-EDNR | EDNR | alpha | 12 | ASA | `brain/units/ndu/models/ednr.py` | `Docs/C³/Models/NDU-α3-EDNR/EDNR.md` |
| 51 | NDU-b1-DSP | DSP | beta | 10 | ASA | `brain/units/ndu/models/dsp.py` | `Docs/C³/Models/NDU-β1-DSP/DSP.md` |
| 52 | NDU-b2-CDMR | CDMR | beta | 10 | TMH, ASA | `brain/units/ndu/models/cdmr.py` | `Docs/C³/Models/NDU-β2-CDMR/CDMR.md` |
| 53 | NDU-b3-SLEE | SLEE | beta | 10 | MEM, ASA | `brain/units/ndu/models/slee.py` | `Docs/C³/Models/NDU-β3-SLEE/SLEE.md` |
| 54 | NDU-g1-SDDP | SDDP | gamma | 10 | ASA | `brain/units/ndu/models/sddp.py` | `Docs/C³/Models/NDU-γ1-SDDP/SDDP.md` |
| 55 | NDU-g2-ONI | ONI | gamma | 10 | ASA | `brain/units/ndu/models/oni.py` | `Docs/C³/Models/NDU-γ2-ONI/ONI.md` |
| 56 | NDU-g3-ECT | ECT | gamma | 9 | ASA | `brain/units/ndu/models/ect.py` | `Docs/C³/Models/NDU-γ3-ECT/ECT.md` |

#### MPU Models (10 models, 104D total)

| # | Model ID | Acronym | Tier | Dim | Mechanisms | Code Path | Doc Path |
|---|----------|---------|------|:---:|------------|-----------|----------|
| 57 | MPU-a1-PEOM | PEOM | alpha | 12 | BEP | `brain/units/mpu/models/peom.py` | `Docs/C³/Models/MPU-α1-PEOM/PEOM.md` |
| 58 | MPU-a2-MSR | MSR | alpha | 12 | BEP | `brain/units/mpu/models/msr.py` | `Docs/C³/Models/MPU-α2-MSR/MSR.md` |
| 59 | MPU-a3-GSSM | GSSM | alpha | 11 | BEP | `brain/units/mpu/models/gssm.py` | `Docs/C³/Models/MPU-α3-GSSM/GSSM.md` |
| 60 | MPU-b1-ASAP | ASAP | beta | 10 | BEP | `brain/units/mpu/models/asap.py` | `Docs/C³/Models/MPU-β1-ASAP/ASAP.md` |
| 61 | MPU-b2-DDSMI | DDSMI | beta | 10 | BEP | `brain/units/mpu/models/ddsmi.py` | `Docs/C³/Models/MPU-β2-DDSMI/DDSMI.md` |
| 62 | MPU-b3-VRMSME | VRMSME | beta | 10 | BEP | `brain/units/mpu/models/vrmsme.py` | `Docs/C³/Models/MPU-β3-VRMSME/VRMSME.md` |
| 63 | MPU-b4-SPMC | SPMC | beta | 11 | BEP | `brain/units/mpu/models/spmc.py` | `Docs/C³/Models/MPU-β4-SPMC/SPMC.md` |
| 64 | MPU-g1-NSCP | NSCP | gamma | 10 | BEP | `brain/units/mpu/models/nscp.py` | `Docs/C³/Models/MPU-γ1-NSCP/NSCP.md` |
| 65 | MPU-g2-CTBB | CTBB | gamma | 9 | BEP | `brain/units/mpu/models/ctbb.py` | `Docs/C³/Models/MPU-γ2-CTBB/CTBB.md` |
| 66 | MPU-g3-STC | STC | gamma | 9 | BEP | `brain/units/mpu/models/stc.py` | `Docs/C³/Models/MPU-γ3-STC/STC.md` |

#### PCU Models (10 models, 94D total)

| # | Model ID | Acronym | Tier | Dim | Mechanisms | Code Path | Doc Path |
|---|----------|---------|------|:---:|------------|-----------|----------|
| 67 | PCU-a1-HTP | HTP | alpha | 12 | PPC, TPC, MEM | `brain/units/pcu/models/htp.py` | `Docs/C³/Models/PCU-α1-HTP/HTP.md` |
| 68 | PCU-a2-SPH | SPH | alpha | 11 | PPC | `brain/units/pcu/models/sph.py` | `Docs/C³/Models/PCU-α2-SPH/SPH.md` |
| 69 | PCU-a3-ICEM | ICEM | alpha | 11 | AED, C0P | `brain/units/pcu/models/icem.py` | `Docs/C³/Models/PCU-α3-ICEM/ICEM.md` |
| 70 | PCU-b1-PWUP | PWUP | beta | 10 | PPC | `brain/units/pcu/models/pwup.py` | `Docs/C³/Models/PCU-β1-PWUP/PWUP.md` |
| 71 | PCU-b2-WMED | WMED | beta | 10 | AED, MEM | `brain/units/pcu/models/wmed.py` | `Docs/C³/Models/PCU-β2-WMED/WMED.md` |
| 72 | PCU-b3-UDP | UDP | beta | 10 | C0P | `brain/units/pcu/models/udp.py` | `Docs/C³/Models/PCU-β3-UDP/UDP.md` |
| 73 | PCU-b4-CHPI | CHPI | beta | 11 | PPC, TPC | `brain/units/pcu/models/chpi.py` | `Docs/C³/Models/PCU-β4-CHPI/CHPI.md` |
| 74 | PCU-g1-IGFE | IGFE | gamma | 9 | TPC | `brain/units/pcu/models/igfe.py` | `Docs/C³/Models/PCU-γ1-IGFE/IGFE.md` |
| 75 | PCU-g2-MAA | MAA | gamma | 5 | ASA | `brain/units/pcu/models/maa.py` | `Docs/C³/Models/PCU-γ2-MAA/MAA.md` |
| 76 | PCU-g3-PSH | PSH | gamma | 5 | PPC, TPC, MEM | `brain/units/pcu/models/psh.py` | `Docs/C³/Models/PCU-γ3-PSH/PSH.md` |

---

### Batch 3: ARU (10), RPU (10) -- Dependent, AFTER Batch 1+2 and Pathways

#### ARU Models (10 models, 120D total)

| # | Model ID | Acronym | Tier | Dim | Mechanisms | Code Path | Doc Path |
|---|----------|---------|------|:---:|------------|-----------|----------|
| 77 | ARU-a1-SRP | SRP | alpha | 19 | AED, CPD, C0P | `brain/units/aru/models/srp.py` | `Docs/C³/Models/ARU-α1-SRP/SRP.md` |
| 78 | ARU-a2-AAC | AAC | alpha | 14 | AED, CPD, ASA | `brain/units/aru/models/aac.py` | `Docs/C³/Models/ARU-α2-AAC/AAC.md` |
| 79 | ARU-a3-VMM | VMM | alpha | 14 | AED, C0P | `brain/units/aru/models/vmm.py` | `Docs/C³/Models/ARU-α3-VMM/VMM.md` |
| 80 | ARU-b1-PUPF | PUPF | beta | 12 | AED, CPD | `brain/units/aru/models/pupf.py` | `Docs/C³/Models/ARU-β1-PUPF/PUPF.md` |
| 81 | ARU-b2-CLAM | CLAM | beta | 12 | AED | `brain/units/aru/models/clam.py` | `Docs/C³/Models/ARU-β2-CLAM/CLAM.md` |
| 82 | ARU-b3-MAD | MAD | beta | 10 | AED, CPD | `brain/units/aru/models/mad.py` | `Docs/C³/Models/ARU-β3-MAD/MAD.md` |
| 83 | ARU-b4-NEMAC | NEMAC | beta | 11 | AED, MEM | `brain/units/aru/models/nemac.py` | `Docs/C³/Models/ARU-β4-NEMAC/NEMAC.md` |
| 84 | ARU-g1-DAP | DAP | gamma | 10 | AED | `brain/units/aru/models/dap.py` | `Docs/C³/Models/ARU-γ1-DAP/DAP.md` |
| 85 | ARU-g2-CMAT | CMAT | gamma | 9 | AED | `brain/units/aru/models/cmat.py` | `Docs/C³/Models/ARU-γ2-CMAT/CMAT.md` |
| 86 | ARU-g3-TAR | TAR | gamma | 9 | AED | `brain/units/aru/models/tar.py` | `Docs/C³/Models/ARU-γ3-TAR/TAR.md` |

ARU receives cross-unit inputs from pathways P1 (SPU), P3 (IMU), P5 (STU).

#### RPU Models (10 models, 94D total)

| # | Model ID | Acronym | Tier | Dim | Mechanisms | Code Path | Doc Path |
|---|----------|---------|------|:---:|------------|-----------|----------|
| 87 | RPU-a1-DAED | DAED | alpha | 12 | AED, CPD | `brain/units/rpu/models/daed.py` | `Docs/C³/Models/RPU-α1-DAED/DAED.md` |
| 88 | RPU-a2-MORMR | MORMR | alpha | 11 | AED, C0P | `brain/units/rpu/models/mormr.py` | `Docs/C³/Models/RPU-α2-MORMR/MORMR.md` |
| 89 | RPU-a3-RPEM | RPEM | alpha | 11 | AED, CPD | `brain/units/rpu/models/rpem.py` | `Docs/C³/Models/RPU-α3-RPEM/RPEM.md` |
| 90 | RPU-b1-IUCP | IUCP | beta | 10 | C0P | `brain/units/rpu/models/iucp.py` | `Docs/C³/Models/RPU-β1-IUCP/IUCP.md` |
| 91 | RPU-b2-MCCN | MCCN | beta | 10 | AED, TMH | `brain/units/rpu/models/mccn.py` | `Docs/C³/Models/RPU-β2-MCCN/MCCN.md` |
| 92 | RPU-b3-MEAMR | MEAMR | beta | 10 | AED, MEM | `brain/units/rpu/models/meamr.py` | `Docs/C³/Models/RPU-β3-MEAMR/MEAMR.md` |
| 93 | RPU-b4-SSRI | SSRI | beta | 11 | AED | `brain/units/rpu/models/ssri.py` | `Docs/C³/Models/RPU-β4-SSRI/SSRI.md` |
| 94 | RPU-g1-LDAC | LDAC | gamma | 9 | AED | `brain/units/rpu/models/ldac.py` | `Docs/C³/Models/RPU-γ1-LDAC/LDAC.md` |
| 95 | RPU-g2-IOTMS | IOTMS | gamma | 5 | BEP, MEM | `brain/units/rpu/models/iotms.py` | `Docs/C³/Models/RPU-γ2-IOTMS/IOTMS.md` |
| 96 | RPU-g3-SSPS | SSPS | gamma | 5 | ASA | `brain/units/rpu/models/ssps.py` | `Docs/C³/Models/RPU-γ3-SSPS/SSPS.md` |

RPU receives routed signals from ARU via CROSS_UNIT_READS = ("ARU",).

---

## P3.6 -- Pathways and PathwayRunner

### `brain/pathways/__init__.py`

**Purpose**: Re-export all 5 pathway declarations and PathwayRunner.
**Exports**: `P1_SPU_ARU, P2_STU_INTERNAL, P3_IMU_ARU, P4_STU_INTERNAL, P5_STU_ARU, PathwayRunner`

---

### `brain/pathways/p1_spu_aru.py`

**Purpose**: Consonance-to-pleasure pathway (SPU -> ARU, r=0.81).

**Primary Docs**:
- `Docs/C³/Pathways/P1-SPU-ARU.md` -- source model, source dims, target model, correlation, citation

**Related Docs**:
- `Docs/C³/Contracts/CrossUnitPathway.md` -- dataclass interface

**Depends On**:
- `contracts/dataclasses/pathway_spec.py`

**Exports**: `P1_SPU_ARU` (CrossUnitPathway instance)

**Key Constraints**:
- pathway_id = "P1_SPU_ARU"
- source_unit = "SPU", target_unit = "ARU"
- correlation = "r=0.81", citation = "Bidelman 2009"
- Inter-unit pathway: creates Phase 2 -> Phase 4 dependency

**Verification Checklist**:
- [ ] All fields match P1-SPU-ARU.md
- [ ] is_inter_unit == True
- [ ] edge == ("SPU", "ARU")

---

### `brain/pathways/p2_stu_internal.py`

**Purpose**: Beat-to-motor-sync internal pathway (STU -> STU, r=0.70).

**Primary Docs**:
- `Docs/C³/Pathways/P2-STU-INTERNAL.md` -- pathway specification

**Depends On**:
- `contracts/dataclasses/pathway_spec.py`

**Exports**: `P2_STU_INTERNAL` (CrossUnitPathway instance)

**Key Constraints**:
- pathway_id = "P2_STU_INTERNAL"
- source_unit = "STU", target_unit = "STU"
- Intra-unit: is_intra_unit == True; does NOT affect unit execution order

**Verification Checklist**:
- [ ] Fields match P2-STU-INTERNAL.md
- [ ] is_intra_unit == True

---

### `brain/pathways/p3_imu_aru.py`

**Purpose**: Memory-to-affect pathway (IMU -> ARU, r=0.55).

**Primary Docs**:
- `Docs/C³/Pathways/P3-IMU-ARU.md` -- pathway specification

**Depends On**:
- `contracts/dataclasses/pathway_spec.py`

**Exports**: `P3_IMU_ARU` (CrossUnitPathway instance)

**Key Constraints**:
- pathway_id = "P3_IMU_ARU"
- source_unit = "IMU", target_unit = "ARU"
- Inter-unit pathway

**Verification Checklist**:
- [ ] Fields match P3-IMU-ARU.md
- [ ] is_inter_unit == True
- [ ] edge == ("IMU", "ARU")

---

### `brain/pathways/p4_stu_internal.py`

**Purpose**: Context-to-prediction internal pathway (STU -> STU, r=0.99).

**Primary Docs**:
- `Docs/C³/Pathways/P4-STU-INTERNAL.md` -- pathway specification

**Depends On**:
- `contracts/dataclasses/pathway_spec.py`

**Exports**: `P4_STU_INTERNAL` (CrossUnitPathway instance)

**Key Constraints**:
- pathway_id = "P4_STU_INTERNAL"
- source_unit = "STU", target_unit = "STU"
- Intra-unit; highest correlation (r=0.99)

**Verification Checklist**:
- [ ] Fields match P4-STU-INTERNAL.md
- [ ] is_intra_unit == True

---

### `brain/pathways/p5_stu_aru.py`

**Purpose**: Tempo-to-emotion pathway (STU -> ARU, r=0.60).

**Primary Docs**:
- `Docs/C³/Pathways/P5-STU-ARU.md` -- pathway specification

**Depends On**:
- `contracts/dataclasses/pathway_spec.py`

**Exports**: `P5_STU_ARU` (CrossUnitPathway instance)

**Key Constraints**:
- pathway_id = "P5_STU_ARU"
- source_unit = "STU", target_unit = "ARU"
- Inter-unit pathway

**Verification Checklist**:
- [ ] Fields match P5-STU-ARU.md
- [ ] is_inter_unit == True
- [ ] edge == ("STU", "ARU")

---

### `brain/pathways/runner.py`

**Purpose**: PathwayRunner routes signals from independent unit outputs to dependent units.

**Primary Docs**:
- `Docs/C³/Pathways/00-INDEX.md` -- routing flow, inter vs intra semantics

**Related Docs**:
- `Docs/C³/C3-ARCHITECTURE.md` -- Phase 3 pathway execution

**Depends On**:
- All 5 pathway files
- `contracts/dataclasses/pathway_spec.py`

**Exports**: `PathwayRunner`

**Key Constraints**:
- `route(unit_outputs: Dict[str, Tensor])` -> `Dict[str, Tensor]`
- Extracts source_dims from source unit output
- Returns dict keyed by pathway_id with extracted signal tensors
- Only inter-unit pathways produce cross_unit_inputs for dependent units
- Intra-unit pathways handled within the unit's own compute()

**Verification Checklist**:
- [ ] route() correctly extracts signals from 3 inter-unit pathways (P1, P3, P5)
- [ ] Returns dict with pathway_id keys
- [ ] Does not route intra-unit pathways (P2, P4) externally
- [ ] Unknown pathway_id raises error

---

## P3.7 -- BrainOrchestrator

### `brain/orchestrator.py`

**Purpose**: Orchestrate the 5-phase brain execution pipeline.

**Primary Docs**:
- `Docs/C³/C3-ARCHITECTURE.md` -- 5-phase execution model, dependency graph, assembly

**Related Docs**:
- `Docs/C³/Units/00-INDEX.md` -- UNIT_EXECUTION_ORDER
- `Docs/C³/Pathways/00-INDEX.md` -- pathway routing between phases
- `Docs/C³/Mechanisms/00-INDEX.md` -- mechanism caching

**Depends On**:
- `brain/mechanisms/runner.py` (MechanismRunner)
- All 9 unit files (P3.4)
- `brain/pathways/runner.py` (PathwayRunner)

**Exports**: `BrainOrchestrator`

**Key Constraints**:
- 5-phase execution sequence:

```
Phase 1: Mechanisms
  - MechanismRunner.run(h3_features, r3_features)
  - All 10 mechanisms compute, outputs cached

Phase 2: Independent Units
  - SPU, STU, IMU, ASU, NDU, MPU, PCU compute
  - Each receives: mechanism_outputs, h3_features, r3_features
  - cross_unit_inputs = {} (empty for independent units)
  - Parallelizable (no inter-dependencies)

Phase 3: Pathway Routing
  - PathwayRunner.route(unit_outputs)
  - Extracts cross-unit signals for P1, P3, P5

Phase 4: Dependent Units
  - ARU computes with cross_unit_inputs from P1, P3, P5
  - RPU computes with cross_unit_inputs from ARU
  - Sequential: ARU must complete before RPU

Phase 5: Assembly
  - Concatenate all 9 unit outputs in UNIT_EXECUTION_ORDER
  - Output: BrainOutput(tensor=(B,T,1006), unit_ranges={...}, dimension_names=(...))
```

- UNIT_EXECUTION_ORDER = ("SPU", "STU", "IMU", "ASU", "NDU", "MPU", "PCU", "ARU", "RPU")
- Total brain output: 99 + 148 + 159 + 94 + 94 + 104 + 94 + 120 + 94 = 1,006D
- All computations are deterministic (zero-parameter models)

**Verification Checklist**:
- [ ] 5 phases execute in correct order
- [ ] Phase 2 units receive empty cross_unit_inputs
- [ ] Phase 4 ARU receives P1, P3, P5 routed signals
- [ ] Phase 4 RPU receives ARU outputs
- [ ] Assembly concatenation produces (B, T, 1006)
- [ ] unit_ranges dict correctly maps each unit to its index range
- [ ] dimension_names has exactly 1006 entries

---

### `brain/__init__.py`

**Purpose**: Top-level brain package init.
**Exports**: `BrainOrchestrator`

---

## Dependency Graph Summary

```
P1 Contracts ──────────────────────────────────────────────────────┐
                                                                   │
P2 Ear (R3 + H3) ─────────────────────────────────────────────────┤
                                                                   │
P3.1 Mechanisms (10 files) ──────┐                                 │
                                 │                                 │
P3.2 MechanismRunner ────────────┤                                 │
                                 │                                 │
P3.3 Circuits, Regions, Neuroch. │ (independent of P3.1-2)         │
                                 │                                 │
P3.4 Unit Shells (9 units) ──────┤                                 │
                                 │                                 │
P3.5 Models Batch 1 ─────────────┤ SPU(9), STU(14), IMU(15)       │
                                 │                                 │
P3.5 Models Batch 2 ─────────────┤ ASU(9), NDU(9), MPU(10), PCU(10)
                                 │                                 │
P3.6 Pathways (5) + Runner ──────┤                                 │
                                 │                                 │
P3.5 Models Batch 3 ─────────────┤ ARU(10), RPU(10)               │
                                 │                                 │
P3.7 BrainOrchestrator ──────────┘                                 │
                                                                   │
P4 Semantics ◄─────────────────────────────────────────────────────┘
```

---

## Known Discrepancies

Agents MUST consult `Docs/Beta/DISCREPANCY-REGISTRY.md` before implementing. Key rules for P3:

| Issue | Old (v1) | New (v2) | Action |
|-------|----------|----------|--------|
| MECHANISM_NAMES | Some models list ("ASA",) only | Use doc value (e.g., ("BEP","ASA")) | Use v2 |
| h3_demand | Empty tuple () in old code | Populated tuples from doc Section 5 | Use v2 |
| Gamma OUTPUT_DIM | 10 in old code | 9 in some docs | Use doc value |
| FULL_NAME | Old code names | Doc Section 1 header | Use v2 |
| R3_DIM | 49 (v1) | 128 (v2) | Use 128 for r3_features shape |
| H3 theoretical | 112,896 (v1) | 294,912 (v2) | Use v2 |

---

## Verification Gate G3

After completing all P3 files:

```python
# G3 verification script
from Musical_Intelligence.brain import BrainOrchestrator
from Musical_Intelligence.brain.mechanisms import MechanismRunner
from Musical_Intelligence.brain.mechanisms import (
    PPC, TPC, BEP, ASA, TMH, MEM, SYN, AED, CPD, C0P
)

# 1. Verify all 10 mechanisms instantiate and have correct OUTPUT_DIM
for Mech in [PPC, TPC, BEP, ASA, TMH, MEM, SYN, AED, CPD, C0P]:
    m = Mech()
    assert m.OUTPUT_DIM == 30, f"{m.NAME} OUTPUT_DIM != 30"
    assert len(m.NAME) > 0

# 2. Verify all 96 models instantiate and pass validate_constants()
from Musical_Intelligence.brain.units import (
    spu, stu, imu, asu, ndu, mpu, pcu, aru, rpu
)

total_dim = 0
model_count = 0
for unit_mod in [spu, stu, imu, asu, ndu, mpu, pcu, aru, rpu]:
    unit = unit_mod.Unit()
    for model in unit.models:
        model.validate_constants()
        model_count += 1
    total_dim += unit.total_dim

assert model_count == 96, f"Expected 96 models, got {model_count}"
assert total_dim == 1006, f"Expected 1006D, got {total_dim}"

# 3. Verify BrainOrchestrator produces correct output shape
import torch
orchestrator = BrainOrchestrator()
h3_features = {}   # populated in real usage
r3_features = torch.zeros(1, 10, 128)  # (B=1, T=10, R3_DIM=128)
output = orchestrator.run(h3_features, r3_features)
assert output.tensor.shape == (1, 10, 1006)
assert len(output.dimension_names) == 1006
assert len(output.unit_ranges) == 9

print("G3 PASSED: All 96 models valid, BrainOrchestrator produces (B,T,1006)")
```
