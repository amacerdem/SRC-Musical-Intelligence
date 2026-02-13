# Phase 3: Brain -- C3 Cognitive Models

**Phase**: P3
**Depends on**: P1 (Contracts), P2 (Ear -- R3 + H3)
**Output**: ~145 Python files in `Musical_Intelligence/brain/`
**Gate**: G3 -- all 96 models instantiate, `validate_constants()` passes for each

---

## Overview

Phase 3 implements the C3 cognitive brain layer: 10 mechanisms, 9 units (96 models), 5 pathways, 6 circuits, brain regions, neurochemicals, and the BrainOrchestrator.

| Sub-phase | Contents | Files |
|-----------|----------|:-----:|
| P3.1 | 10 Mechanisms | 10 |
| P3.2 | MechanismRunner | 2 |
| P3.3 | Infrastructure (circuits, regions, neurochemicals) | 10 |
| P3.4 | 9 Unit shells | 18 |
| P3.5 | 96 Models (3 batches) | 96 |
| P3.6 | 5 Pathways + PathwayRunner | 7 |
| P3.7 | BrainOrchestrator | 2 |

---

## P3.1 -- Mechanisms (10 files)

Each mechanism is a `BaseMechanism` subclass producing `(B, T, 30)`. Computed once, cached by MechanismRunner.

### `brain/mechanisms/__init__.py`

**Purpose**: Re-export all 10 mechanisms and MechanismRunner.
**Exports**: `PPC, TPC, BEP, ASA, TMH, MEM, SYN, AED, CPD, C0P, MechanismRunner`

---

**Common structure for all 10 mechanism files below:**

- **Depends On**: `contracts/bases/base_mechanism.py`
- **Related Docs**: `Docs/C³/Contracts/BaseMechanism.md`, circuit doc for that mechanism
- **Verification**: NAME/FULL_NAME/OUTPUT_DIM/HORIZONS match doc; h3_demand correct; output (B,T,30)

### `brain/mechanisms/ppc.py`

**Purpose**: Pitch Processing Chain -- spectral pitch extraction.
**Primary Docs**: `Docs/C³/Mechanisms/PPC.md`
**Exports**: `PPC`
**Key Constraints**: NAME="PPC", HORIZONS=(0,3,6), 3x10D: pitch extraction / interval analysis / contour tracking. Used by 12 models (BCH, PSCL, PCCR, SDNPS, ESME, SDED, SPH, HTP, PSH, PWUP, TPRD, SDD).

### `brain/mechanisms/tpc.py`

**Purpose**: Timbre Processing Chain -- spectral shape and temporal envelope.
**Primary Docs**: `Docs/C³/Mechanisms/TPC.md`
**Exports**: `TPC`
**Key Constraints**: NAME="TPC", HORIZONS=(6,12,16), 3x10D: spectral shape / temporal envelope / source identity. Used by 7 models (STAI, TSCP, MIAA, TPIO, IGFE, HTP, PSH).

### `brain/mechanisms/bep.py`

**Purpose**: Beat Entrainment Processing -- rhythmic synchronization.
**Primary Docs**: `Docs/C³/Mechanisms/BEP.md`
**Exports**: `BEP`
**Key Constraints**: NAME="BEP", HORIZONS=(6,9,11), 3x10D: beat entrainment / motor coupling / groove. Most-used mechanism (26+ models across STU, ASU, MPU).

### `brain/mechanisms/asa.py`

**Purpose**: Auditory Scene Analysis -- attention gating and salience.
**Primary Docs**: `Docs/C³/Mechanisms/ASA.md`
**Exports**: `ASA`
**Key Constraints**: NAME="ASA", HORIZONS=(3,6,9), 3x10D: scene analysis / attention gating / salience weighting. Used by 21+ models.

### `brain/mechanisms/tmh.py`

**Purpose**: Temporal Memory Hierarchy -- multi-timescale sequence integration.
**Primary Docs**: `Docs/C³/Mechanisms/TMH.md`
**Exports**: `TMH`
**Key Constraints**: NAME="TMH", HORIZONS=(16,18,20,22), 4 horizons (exception); 30D. Used by 8 models.

### `brain/mechanisms/mem.py`

**Purpose**: Memory Encoding/Retrieval -- working memory and long-term memory.
**Primary Docs**: `Docs/C³/Mechanisms/MEM.md`
**Exports**: `MEM`
**Key Constraints**: NAME="MEM", HORIZONS=(18,20,22,25), 4 horizons; longest timescale (60s). Used by 20+ models.

### `brain/mechanisms/syn.py`

**Purpose**: Syntactic Processing -- musical syntax (Broca's area analog).
**Primary Docs**: `Docs/C³/Mechanisms/SYN.md`
**Exports**: `SYN`
**Key Constraints**: NAME="SYN", HORIZONS=(12,16,18), 3x10D. Least-used (only MSPBA).

### `brain/mechanisms/aed.py`

**Purpose**: Affective Entrainment Dynamics -- valence and arousal tracking.
**Primary Docs**: `Docs/C³/Mechanisms/AED.md`
**Exports**: `AED`
**Key Constraints**: NAME="AED", HORIZONS=(6,16), 2 horizons (fewest); 30D. Used by 18+ models (ARU/RPU).

### `brain/mechanisms/cpd.py`

**Purpose**: Chills and Peak Detection -- anticipation/peak/resolution.
**Primary Docs**: `Docs/C³/Mechanisms/CPD.md`
**Exports**: `CPD`
**Key Constraints**: NAME="CPD", HORIZONS=(9,16,18), 3x10D: anticipation / peak / resolution. Used by 6 models.

### `brain/mechanisms/c0p.py`

**Purpose**: Cognitive Projection -- tension-expectation-approach.
**Primary Docs**: `Docs/C³/Mechanisms/C0P.md`
**Exports**: `C0P`
**Key Constraints**: NAME="C0P" (zero, not O), HORIZONS=(18,19,20), 3x10D. Used by 6 models.

---

## P3.2 -- MechanismRunner

### `brain/mechanisms/runner.py`

**Purpose**: Compute all required mechanisms once, cache for model reuse.

**Primary Docs**:
- `Docs/C³/Mechanisms/00-INDEX.md` -- MechanismRunner architecture
- `Docs/C³/Contracts/BaseMechanism.md` -- interface

**Depends On**: `contracts/bases/base_mechanism.py`, all 10 mechanism files

**Exports**: `MechanismRunner`

**Key Constraints**:
- Scans model registry for unique MECHANISM_NAMES across active models
- `run(h3_features, r3_features)` computes all, stores in cache
- `get(name)` returns cached `(B, T, 30)` tensor; raises if not cached
- Each mechanism computed exactly once per run() call

**Verification Checklist**:
- [ ] Each mechanism computed exactly once
- [ ] get() returns (B, T, 30) for all 10
- [ ] get() raises if not cached
- [ ] Cache cleared between batches

---

## P3.3 -- Supporting Infrastructure

### Circuits

#### `brain/circuits/__init__.py`

**Purpose**: Re-export circuit definitions and registry.
**Exports**: `CircuitDef, CircuitRegistry, CIRCUITS, CIRCUIT_NAMES`

#### `brain/circuits/definitions.py`

**Purpose**: 6 CircuitDef instances for neural circuit groupings.

**Primary Docs**: `Docs/C³/Circuits/00-INDEX.md`, plus `Docs/C³/Circuits/{Mesolimbic,Perceptual,Sensorimotor,Mnemonic,Salience,Imagery}.md`

**Exports**: `CIRCUITS` (5 operational), `CIRCUIT_NAMES` (6 total, includes imagery)

**Key Constraints**:
- 6 circuits: mesolimbic (AED,CPD,C0P / ARU,RPU), perceptual (PPC,TPC / SPU), sensorimotor (BEP,TMH / STU,MPU), mnemonic (MEM,SYN / IMU,PCU), salience (ASA / ASU,NDU), imagery (PPC,TPC,MEM / PCU)
- CIRCUITS excludes imagery (emergent, not structural)

#### `brain/circuits/registry.py`

**Purpose**: CircuitRegistry with lookup by name, mechanism, or unit.
**Primary Docs**: `Docs/C³/Circuits/00-INDEX.md`
**Depends On**: `brain/circuits/definitions.py`
**Exports**: `CircuitRegistry`

---

### Regions

#### `brain/regions/__init__.py`

**Exports**: `BrainRegionRegistry, CORTICAL_REGIONS, SUBCORTICAL_REGIONS, BRAINSTEM_REGIONS`

#### `brain/regions/cortical.py`

**Purpose**: Cortical regions with Brodmann areas and MNI152 coordinates.
**Primary Docs**: `Docs/C³/Regions/Cortical.md`
**Depends On**: `contracts/dataclasses/brain_region.py`
**Exports**: `CORTICAL_REGIONS` (tuple of BrainRegion)
**Key Constraints**: All have brodmann_area (is_cortical==True). MNI: x(L-/R+), y(P-/A+), z(I-/S+).

#### `brain/regions/subcortical.py`

**Purpose**: Subcortical nuclei (NAcc, VTA, Amygdala, Hippocampus, etc.).
**Primary Docs**: `Docs/C³/Regions/Subcortical.md`
**Exports**: `SUBCORTICAL_REGIONS` -- brodmann_area=None for all.

#### `brain/regions/brainstem.py`

**Purpose**: Brainstem structures (Inferior Colliculus, Cochlear Nucleus, etc.).
**Primary Docs**: `Docs/C³/Regions/Brainstem.md`
**Exports**: `BRAINSTEM_REGIONS` -- brodmann_area=None for all.

#### `brain/regions/registry.py`

**Purpose**: Unified BrainRegionRegistry with MNI lookup.
**Primary Docs**: `Docs/C³/Regions/00-INDEX.md`
**Exports**: `BrainRegionRegistry` -- get_by_name(), get_by_abbreviation(), get_nearest_mni()

---

### Neurochemicals

#### `brain/neurochemicals/__init__.py`

**Exports**: `Dopamine, Opioid, Serotonin, Norepinephrine, NeurochemicalRegistry`

**4 neurochemical files** (each exports one class):

| File | Primary Doc | Exports |
|------|-------------|---------|
| `brain/neurochemicals/dopamine.py` | `Docs/C³/Neurochemicals/Dopamine.md` | `Dopamine` |
| `brain/neurochemicals/opioid.py` | `Docs/C³/Neurochemicals/Opioid.md` | `Opioid` |
| `brain/neurochemicals/serotonin.py` | `Docs/C³/Neurochemicals/Serotonin.md` | `Serotonin` |
| `brain/neurochemicals/norepinephrine.py` | `Docs/C³/Neurochemicals/Norepinephrine.md` | `Norepinephrine` |

#### `brain/neurochemicals/registry.py`

**Purpose**: NeurochemicalRegistry for lookup by name.
**Primary Docs**: `Docs/C³/Neurochemicals/00-INDEX.md`
**Exports**: `NeurochemicalRegistry`

---

## P3.4 -- Unit Shells (9 units)

Each unit is a `BaseCognitiveUnit` subclass in `brain/units/{code}/unit.py` with a `models/` sub-package.

### Unit Template

Every `unit.py` must:
1. Override: `UNIT_NAME`, `FULL_NAME`, `CIRCUIT`, `POOLED_EFFECT`
2. Import and instantiate all models from `models/`
3. Implement `models` property (List[BaseModel]), `compute()` method
4. compute() calls each model in tier order (alpha->beta->gamma), concatenates outputs
5. Pass `validate_constants()`

**Primary Doc pattern**: `Docs/C³/Units/{UNIT}.md`
**Related Docs**: `Docs/C³/Contracts/BaseCognitiveUnit.md`, `Docs/C³/C3-ARCHITECTURE.md`

### `brain/units/spu/unit.py` (example)

**Purpose**: SPU shell -- 9 models, 99D.
**Key Constraints**: UNIT_NAME="SPU", CIRCUIT="perceptual", POOLED_EFFECT=0.84, Independent.

### Unit Roster

| Unit File | Unit | Circuit | d | Models | Dim | Dep. | Doc |
|-----------|------|---------|-----|:------:|:---:|------|-----|
| `brain/units/spu/unit.py` | SPU | perceptual | 0.84 | 9 | 99 | Indep. | `Docs/C³/Units/SPU.md` |
| `brain/units/stu/unit.py` | STU | sensorimotor | 0.67 | 14 | 148 | Indep. | `Docs/C³/Units/STU.md` |
| `brain/units/imu/unit.py` | IMU | mnemonic | 0.53 | 15 | 159 | Indep. | `Docs/C³/Units/IMU.md` |
| `brain/units/asu/unit.py` | ASU | salience | 0.60 | 9 | 94 | Indep. | `Docs/C³/Units/ASU.md` |
| `brain/units/ndu/unit.py` | NDU | salience | 0.55 | 9 | 94 | Indep. | `Docs/C³/Units/NDU.md` |
| `brain/units/mpu/unit.py` | MPU | sensorimotor | 0.62 | 10 | 104 | Indep. | `Docs/C³/Units/MPU.md` |
| `brain/units/pcu/unit.py` | PCU | mnemonic | 0.58 | 10 | 94 | Indep. | `Docs/C³/Units/PCU.md` |
| `brain/units/aru/unit.py` | ARU | mesolimbic | 0.83 | 10 | 120 | Dep. | `Docs/C³/Units/ARU.md` |
| `brain/units/rpu/unit.py` | RPU | mesolimbic | 0.70 | 10 | 94 | Dep. | `Docs/C³/Units/RPU.md` |

Each unit also has `__init__.py` and `models/__init__.py`.

**Verification** (per unit): 4 constants match doc; models returns correct count in tier order; total_dim matches; validate_constants() passes.

---

## P3.5 -- 96 Models (3 batches)

### Model Template

Every model file `brain/units/{unit}/models/{acronym}.py`:

**Primary Docs**: `Docs/C³/Models/{UNIT}-{tier}{n}-{ACRONYM}/{ACRONYM}.md` (14-section doc)

**Related Docs**: `Docs/C³/Contracts/BaseModel.md`, `Docs/C³/Units/{UNIT}.md`, mechanism docs, `Docs/C³/Matrices/R3-Usage.md`, `Docs/C³/Matrices/H3-Demand.md`, `Docs/Beta/DISCREPANCY-REGISTRY.md`

**Depends On**: `contracts/bases/base_model.py`, `contracts/dataclasses/{layer_spec,demand_spec,brain_region,model_metadata,citation}.py`

**Doc-to-code mapping**:

| Doc Section | Code Element |
|-------------|-------------|
| 1. Overview | Class docstring |
| 3. Scientific Foundation | `metadata` property (citations, evidence_tier) |
| 4. R3 Input Mapping | `R3_INDICES` constant |
| 5. H3 Temporal Demand | `h3_demand` property |
| 6. Output Space | `LAYERS` constant (LayerSpec tuples) |
| 7. Mathematical Formulation | `compute()` method |
| 8. Brain Regions | `brain_regions` property |
| 10. Falsification Criteria | `metadata.falsification_criteria` |
| 13. References | `metadata.citations` |

**Key Constraints** (ALL 96 models):
- Constants: NAME, FULL_NAME, UNIT, TIER, OUTPUT_DIM, MECHANISM_NAMES, CROSS_UNIT_READS, LAYERS
- Properties: h3_demand, dimension_names, brain_regions, metadata
- Method: compute(mechanism_outputs, h3_features, r3_features, cross_unit_inputs)
- LAYERS must cover [0, OUTPUT_DIM) contiguously
- Use doc values (v2), not old code values (v1)
- All h3_demand populated, MECHANISM_NAMES from doc, FULL_NAME from doc Section 1

**Verification** (per model): NAME/FULL_NAME match doc; OUTPUT_DIM == sum(layer dims); LAYERS contiguous; R3_INDICES match Section 4; h3_demand match Section 5; compute() implements Section 7; brain_regions match Section 8; citations match Section 13; falsification match Section 10; validate_constants() passes; file under 1000 lines.

---

### Batch 1: SPU (9) + STU (14) + IMU (15) -- Independent, Parallelizable

Implement within each unit in tier order: alpha -> beta -> gamma.

#### SPU Models (9 models, 99D)

| # | Acronym | Tier | Dim | Mechs | Code | Doc |
|---|---------|------|:---:|-------|------|-----|
| 1 | BCH | a | 12 | PPC | `spu/models/bch.py` | `SPU-α1-BCH/BCH.md` |
| 2 | PSCL | a | 12 | PPC | `spu/models/pscl.py` | `SPU-α2-PSCL/PSCL.md` |
| 3 | PCCR | a | 11 | PPC | `spu/models/pccr.py` | `SPU-α3-PCCR/PCCR.md` |
| 4 | STAI | b | 12 | TPC | `spu/models/stai.py` | `SPU-β1-STAI/STAI.md` |
| 5 | TSCP | b | 10 | TPC | `spu/models/tscp.py` | `SPU-β2-TSCP/TSCP.md` |
| 6 | MIAA | b | 11 | TPC | `spu/models/miaa.py` | `SPU-β3-MIAA/MIAA.md` |
| 7 | SDNPS | g | 10 | PPC | `spu/models/sdnps.py` | `SPU-γ1-SDNPS/SDNPS.md` |
| 8 | ESME | g | 11 | PPC | `spu/models/esme.py` | `SPU-γ2-ESME/ESME.md` |
| 9 | SDED | g | 10 | PPC | `spu/models/sded.py` | `SPU-γ3-SDED/SDED.md` |

#### STU Models (14 models, 148D)

| # | Acronym | Tier | Dim | Mechs | Code | Doc |
|---|---------|------|:---:|-------|------|-----|
| 10 | HMCE | a | 14 | BEP,TMH | `stu/models/hmce.py` | `STU-α1-HMCE/HMCE.md` |
| 11 | AMSC | a | 12 | BEP,TMH | `stu/models/amsc.py` | `STU-α2-AMSC/AMSC.md` |
| 12 | MDNS | a | 11 | BEP | `stu/models/mdns.py` | `STU-α3-MDNS/MDNS.md` |
| 13 | AMSS | b | 10 | BEP | `stu/models/amss.py` | `STU-β1-AMSS/AMSS.md` |
| 14 | TPIO | b | 10 | TPC | `stu/models/tpio.py` | `STU-β2-TPIO/TPIO.md` |
| 15 | EDTA | b | 11 | BEP | `stu/models/edta.py` | `STU-β3-EDTA/EDTA.md` |
| 16 | ETAM | b | 10 | BEP | `stu/models/etam.py` | `STU-β4-ETAM/ETAM.md` |
| 17 | HGSIC | b | 12 | BEP,TMH | `stu/models/hgsic.py` | `STU-β5-HGSIC/HGSIC.md` |
| 18 | OMS | b | 10 | BEP | `stu/models/oms.py` | `STU-β6-OMS/OMS.md` |
| 19 | TMRM | g | 10 | BEP,TMH | `stu/models/tmrm.py` | `STU-γ1-TMRM/TMRM.md` |
| 20 | NEWMD | g | 10 | BEP | `stu/models/newmd.py` | `STU-γ2-NEWMD/NEWMD.md` |
| 21 | MTNE | g | 10 | BEP | `stu/models/mtne.py` | `STU-γ3-MTNE/MTNE.md` |
| 22 | PTGMP | g | 9 | BEP | `stu/models/ptgmp.py` | `STU-γ4-PTGMP/PTGMP.md` |
| 23 | MPFS | g | 9 | BEP | `stu/models/mpfs.py` | `STU-γ5-MPFS/MPFS.md` |

#### IMU Models (15 models, 159D)

| # | Acronym | Tier | Dim | Mechs | Code | Doc |
|---|---------|------|:---:|-------|------|-----|
| 24 | MEAMN | a | 14 | MEM,TMH | `imu/models/meamn.py` | `IMU-α1-MEAMN/MEAMN.md` |
| 25 | PNH | a | 12 | MEM | `imu/models/pnh.py` | `IMU-α2-PNH/PNH.md` |
| 26 | MMP | a | 11 | MEM | `imu/models/mmp.py` | `IMU-α3-MMP/MMP.md` |
| 27 | RASN | b | 10 | BEP,MEM | `imu/models/rasn.py` | `IMU-β1-RASN/RASN.md` |
| 28 | PMIM | b | 11 | MEM,TMH | `imu/models/pmim.py` | `IMU-β2-PMIM/PMIM.md` |
| 29 | OII | b | 10 | MEM | `imu/models/oii.py` | `IMU-β3-OII/OII.md` |
| 30 | HCMC | b | 10 | MEM | `imu/models/hcmc.py` | `IMU-β4-HCMC/HCMC.md` |
| 31 | RIRI | b | 10 | MEM | `imu/models/riri.py` | `IMU-β5-RIRI/RIRI.md` |
| 32 | MSPBA | b | 11 | SYN,MEM | `imu/models/mspba.py` | `IMU-β6-MSPBA/MSPBA.md` |
| 33 | VRIAP | b | 10 | MEM | `imu/models/vriap.py` | `IMU-β7-VRIAP/VRIAP.md` |
| 34 | TPRD | b | 11 | PPC | `imu/models/tprd.py` | `IMU-β8-TPRD/TPRD.md` |
| 35 | CMAPCC | b | 10 | BEP,MEM | `imu/models/cmapcc.py` | `IMU-β9-CMAPCC/CMAPCC.md` |
| 36 | DMMS | g | 10 | MEM | `imu/models/dmms.py` | `IMU-γ1-DMMS/DMMS.md` |
| 37 | CSSL | g | 10 | MEM | `imu/models/cssl.py` | `IMU-γ2-CSSL/CSSL.md` |
| 38 | CDEM | g | 9 | MEM | `imu/models/cdem.py` | `IMU-γ3-CDEM/CDEM.md` |

---

### Batch 2: ASU (9) + NDU (9) + MPU (10) + PCU (10) -- Independent, Parallelizable

#### ASU Models (9 models, 94D)

| # | Acronym | Tier | Dim | Mechs | Code | Doc |
|---|---------|------|:---:|-------|------|-----|
| 39 | SNEM | a | 12 | BEP,ASA | `asu/models/snem.py` | `ASU-α1-SNEM/SNEM.md` |
| 40 | IACM | a | 11 | ASA | `asu/models/iacm.py` | `ASU-α2-IACM/IACM.md` |
| 41 | CSG | a | 12 | ASA | `asu/models/csg.py` | `ASU-α3-CSG/CSG.md` |
| 42 | BARM | b | 10 | BEP,ASA | `asu/models/barm.py` | `ASU-β1-BARM/BARM.md` |
| 43 | STANM | b | 10 | ASA | `asu/models/stanm.py` | `ASU-β2-STANM/STANM.md` |
| 44 | AACM | b | 10 | ASA | `asu/models/aacm.py` | `ASU-β3-AACM/AACM.md` |
| 45 | PWSM | g | 10 | ASA | `asu/models/pwsm.py` | `ASU-γ1-PWSM/PWSM.md` |
| 46 | DGTP | g | 10 | ASA | `asu/models/dgtp.py` | `ASU-γ2-DGTP/DGTP.md` |
| 47 | SDL | g | 9 | ASA | `asu/models/sdl.py` | `ASU-γ3-SDL/SDL.md` |

#### NDU Models (9 models, 94D)

| # | Acronym | Tier | Dim | Mechs | Code | Doc |
|---|---------|------|:---:|-------|------|-----|
| 48 | MPG | a | 12 | PPC,ASA | `ndu/models/mpg.py` | `NDU-α1-MPG/MPG.md` |
| 49 | SDD | a | 11 | PPC,ASA | `ndu/models/sdd.py` | `NDU-α2-SDD/SDD.md` |
| 50 | EDNR | a | 12 | ASA | `ndu/models/ednr.py` | `NDU-α3-EDNR/EDNR.md` |
| 51 | DSP | b | 10 | ASA | `ndu/models/dsp.py` | `NDU-β1-DSP/DSP.md` |
| 52 | CDMR | b | 10 | TMH,ASA | `ndu/models/cdmr.py` | `NDU-β2-CDMR/CDMR.md` |
| 53 | SLEE | b | 10 | MEM,ASA | `ndu/models/slee.py` | `NDU-β3-SLEE/SLEE.md` |
| 54 | SDDP | g | 10 | ASA | `ndu/models/sddp.py` | `NDU-γ1-SDDP/SDDP.md` |
| 55 | ONI | g | 10 | ASA | `ndu/models/oni.py` | `NDU-γ2-ONI/ONI.md` |
| 56 | ECT | g | 9 | ASA | `ndu/models/ect.py` | `NDU-γ3-ECT/ECT.md` |

#### MPU Models (10 models, 104D)

| # | Acronym | Tier | Dim | Mechs | Code | Doc |
|---|---------|------|:---:|-------|------|-----|
| 57 | PEOM | a | 12 | BEP | `mpu/models/peom.py` | `MPU-α1-PEOM/PEOM.md` |
| 58 | MSR | a | 12 | BEP | `mpu/models/msr.py` | `MPU-α2-MSR/MSR.md` |
| 59 | GSSM | a | 11 | BEP | `mpu/models/gssm.py` | `MPU-α3-GSSM/GSSM.md` |
| 60 | ASAP | b | 10 | BEP | `mpu/models/asap.py` | `MPU-β1-ASAP/ASAP.md` |
| 61 | DDSMI | b | 10 | BEP | `mpu/models/ddsmi.py` | `MPU-β2-DDSMI/DDSMI.md` |
| 62 | VRMSME | b | 10 | BEP | `mpu/models/vrmsme.py` | `MPU-β3-VRMSME/VRMSME.md` |
| 63 | SPMC | b | 11 | BEP | `mpu/models/spmc.py` | `MPU-β4-SPMC/SPMC.md` |
| 64 | NSCP | g | 10 | BEP | `mpu/models/nscp.py` | `MPU-γ1-NSCP/NSCP.md` |
| 65 | CTBB | g | 9 | BEP | `mpu/models/ctbb.py` | `MPU-γ2-CTBB/CTBB.md` |
| 66 | STC | g | 9 | BEP | `mpu/models/stc.py` | `MPU-γ3-STC/STC.md` |

#### PCU Models (10 models, 94D)

| # | Acronym | Tier | Dim | Mechs | Code | Doc |
|---|---------|------|:---:|-------|------|-----|
| 67 | HTP | a | 12 | PPC,TPC,MEM | `pcu/models/htp.py` | `PCU-α1-HTP/HTP.md` |
| 68 | SPH | a | 11 | PPC | `pcu/models/sph.py` | `PCU-α2-SPH/SPH.md` |
| 69 | ICEM | a | 11 | AED,C0P | `pcu/models/icem.py` | `PCU-α3-ICEM/ICEM.md` |
| 70 | PWUP | b | 10 | PPC | `pcu/models/pwup.py` | `PCU-β1-PWUP/PWUP.md` |
| 71 | WMED | b | 10 | AED,MEM | `pcu/models/wmed.py` | `PCU-β2-WMED/WMED.md` |
| 72 | UDP | b | 10 | C0P | `pcu/models/udp.py` | `PCU-β3-UDP/UDP.md` |
| 73 | CHPI | b | 11 | PPC,TPC | `pcu/models/chpi.py` | `PCU-β4-CHPI/CHPI.md` |
| 74 | IGFE | g | 9 | TPC | `pcu/models/igfe.py` | `PCU-γ1-IGFE/IGFE.md` |
| 75 | MAA | g | 5 | ASA | `pcu/models/maa.py` | `PCU-γ2-MAA/MAA.md` |
| 76 | PSH | g | 5 | PPC,TPC,MEM | `pcu/models/psh.py` | `PCU-γ3-PSH/PSH.md` |

---

### Batch 3: ARU (10) + RPU (10) -- Dependent, AFTER Batch 1+2 and Pathways

#### ARU Models (10 models, 120D)

ARU receives cross-unit inputs from pathways P1 (SPU), P3 (IMU), P5 (STU).

| # | Acronym | Tier | Dim | Mechs | Code | Doc |
|---|---------|------|:---:|-------|------|-----|
| 77 | SRP | a | 19 | AED,CPD,C0P | `aru/models/srp.py` | `ARU-α1-SRP/SRP.md` |
| 78 | AAC | a | 14 | AED,CPD,ASA | `aru/models/aac.py` | `ARU-α2-AAC/AAC.md` |
| 79 | VMM | a | 14 | AED,C0P | `aru/models/vmm.py` | `ARU-α3-VMM/VMM.md` |
| 80 | PUPF | b | 12 | AED,CPD | `aru/models/pupf.py` | `ARU-β1-PUPF/PUPF.md` |
| 81 | CLAM | b | 12 | AED | `aru/models/clam.py` | `ARU-β2-CLAM/CLAM.md` |
| 82 | MAD | b | 10 | AED,CPD | `aru/models/mad.py` | `ARU-β3-MAD/MAD.md` |
| 83 | NEMAC | b | 11 | AED,MEM | `aru/models/nemac.py` | `ARU-β4-NEMAC/NEMAC.md` |
| 84 | DAP | g | 10 | AED | `aru/models/dap.py` | `ARU-γ1-DAP/DAP.md` |
| 85 | CMAT | g | 9 | AED | `aru/models/cmat.py` | `ARU-γ2-CMAT/CMAT.md` |
| 86 | TAR | g | 9 | AED | `aru/models/tar.py` | `ARU-γ3-TAR/TAR.md` |

#### RPU Models (10 models, 94D)

RPU receives routed signals from ARU via CROSS_UNIT_READS = ("ARU",).

| # | Acronym | Tier | Dim | Mechs | Code | Doc |
|---|---------|------|:---:|-------|------|-----|
| 87 | DAED | a | 12 | AED,CPD | `rpu/models/daed.py` | `RPU-α1-DAED/DAED.md` |
| 88 | MORMR | a | 11 | AED,C0P | `rpu/models/mormr.py` | `RPU-α2-MORMR/MORMR.md` |
| 89 | RPEM | a | 11 | AED,CPD | `rpu/models/rpem.py` | `RPU-α3-RPEM/RPEM.md` |
| 90 | IUCP | b | 10 | C0P | `rpu/models/iucp.py` | `RPU-β1-IUCP/IUCP.md` |
| 91 | MCCN | b | 10 | AED,TMH | `rpu/models/mccn.py` | `RPU-β2-MCCN/MCCN.md` |
| 92 | MEAMR | b | 10 | AED,MEM | `rpu/models/meamr.py` | `RPU-β3-MEAMR/MEAMR.md` |
| 93 | SSRI | b | 11 | AED | `rpu/models/ssri.py` | `RPU-β4-SSRI/SSRI.md` |
| 94 | LDAC | g | 9 | AED | `rpu/models/ldac.py` | `RPU-γ1-LDAC/LDAC.md` |
| 95 | IOTMS | g | 5 | BEP,MEM | `rpu/models/iotms.py` | `RPU-γ2-IOTMS/IOTMS.md` |
| 96 | SSPS | g | 5 | ASA | `rpu/models/ssps.py` | `RPU-γ3-SSPS/SSPS.md` |

**Note**: All Code paths are relative to `brain/units/`; all Doc paths are relative to `Docs/C³/Models/`.

---

## P3.6 -- Pathways and PathwayRunner

### `brain/pathways/__init__.py`

**Purpose**: Re-export all 5 pathway declarations and PathwayRunner.
**Exports**: `P1_SPU_ARU, P2_STU_INTERNAL, P3_IMU_ARU, P4_STU_INTERNAL, P5_STU_ARU, PathwayRunner`

---

**Common for all 5 pathway files**: Each exports one `CrossUnitPathway` instance.
**Depends On**: `contracts/dataclasses/pathway_spec.py`

### Pathway Files

| File | Exports | ID | Route | r | Type | Primary Doc |
|------|---------|----|-------|---|------|-------------|
| `brain/pathways/p1_spu_aru.py` | `P1_SPU_ARU` | P1_SPU_ARU | SPU->ARU | 0.81 | Inter | `Docs/C³/Pathways/P1-SPU-ARU.md` |
| `brain/pathways/p2_stu_internal.py` | `P2_STU_INTERNAL` | P2_STU_INTERNAL | STU->STU | 0.70 | Intra | `Docs/C³/Pathways/P2-STU-INTERNAL.md` |
| `brain/pathways/p3_imu_aru.py` | `P3_IMU_ARU` | P3_IMU_ARU | IMU->ARU | 0.55 | Inter | `Docs/C³/Pathways/P3-IMU-ARU.md` |
| `brain/pathways/p4_stu_internal.py` | `P4_STU_INTERNAL` | P4_STU_INTERNAL | STU->STU | 0.99 | Intra | `Docs/C³/Pathways/P4-STU-INTERNAL.md` |
| `brain/pathways/p5_stu_aru.py` | `P5_STU_ARU` | P5_STU_ARU | STU->ARU | 0.60 | Inter | `Docs/C³/Pathways/P5-STU-ARU.md` |

**Verification** (per pathway): All fields match doc; is_inter_unit/is_intra_unit correct; edge tuple correct.

### `brain/pathways/runner.py`

**Purpose**: Route signals from independent unit outputs to dependent units.

**Primary Docs**: `Docs/C³/Pathways/00-INDEX.md`
**Related Docs**: `Docs/C³/C3-ARCHITECTURE.md` -- Phase 3 execution
**Depends On**: All 5 pathway files, `contracts/dataclasses/pathway_spec.py`
**Exports**: `PathwayRunner`

**Key Constraints**:
- `route(unit_outputs: Dict[str, Tensor])` -> `Dict[str, Tensor]`
- Extracts source_dims from source unit output for inter-unit pathways only
- Intra-unit pathways (P2, P4) handled within the unit's compute()

**Verification Checklist**:
- [ ] route() extracts signals from P1, P3, P5
- [ ] Returns dict keyed by pathway_id
- [ ] Does not externally route P2, P4

---

## P3.7 -- BrainOrchestrator

### `brain/orchestrator.py`

**Purpose**: Orchestrate the 5-phase brain execution pipeline.

**Primary Docs**: `Docs/C³/C3-ARCHITECTURE.md` -- 5-phase execution, dependency graph, assembly
**Related Docs**: `Docs/C³/Units/00-INDEX.md`, `Docs/C³/Pathways/00-INDEX.md`, `Docs/C³/Mechanisms/00-INDEX.md`
**Depends On**: `brain/mechanisms/runner.py`, all 9 units, `brain/pathways/runner.py`
**Exports**: `BrainOrchestrator`

**5-phase execution**:

| Phase | Action | Details |
|:-----:|--------|---------|
| 1 | Mechanisms | MechanismRunner.run() -- all 10 compute, outputs cached |
| 2 | Independent units | SPU,STU,IMU,ASU,NDU,MPU,PCU compute (cross_unit_inputs={}) |
| 3 | Pathway routing | PathwayRunner.route() -- extracts P1,P3,P5 signals |
| 4 | Dependent units | ARU (receives P1,P3,P5), then RPU (receives ARU outputs) |
| 5 | Assembly | Concatenate all 9 units -> BrainOutput(B,T,1006) |

- UNIT_EXECUTION_ORDER = ("SPU","STU","IMU","ASU","NDU","MPU","PCU","ARU","RPU")
- Total: 99+148+159+94+94+104+94+120+94 = 1,006D
- All computations deterministic (zero-parameter)

**Verification Checklist**:
- [ ] 5 phases in correct order
- [ ] Phase 2 units get empty cross_unit_inputs
- [ ] Phase 4 ARU receives P1, P3, P5 routed signals
- [ ] Phase 4 RPU receives ARU outputs (sequential after ARU)
- [ ] Assembly produces (B, T, 1006)
- [ ] unit_ranges maps each unit to correct index range
- [ ] dimension_names has 1006 entries

### `brain/__init__.py`

**Purpose**: Top-level brain package init.
**Exports**: `BrainOrchestrator`

---

## Dependency Graph

```
P1 Contracts ──────────────────────────────────────────────────┐
P2 Ear (R3 + H3) ─────────────────────────────────────────────┤
                                                               │
P3.1 Mechanisms (10) ────────┐                                 │
P3.2 MechanismRunner ────────┤                                 │
P3.3 Circuits/Regions/Neuro  │ (independent of P3.1-2)         │
P3.4 Unit Shells (9) ────────┤                                 │
P3.5 Batch 1 ────────────────┤ SPU(9), STU(14), IMU(15)       │
P3.5 Batch 2 ────────────────┤ ASU(9), NDU(9), MPU(10), PCU(10)
P3.6 Pathways + Runner ──────┤                                 │
P3.5 Batch 3 ────────────────┤ ARU(10), RPU(10)               │
P3.7 BrainOrchestrator ──────┘                                 │
                                                               │
P4 Semantics ◄─────────────────────────────────────────────────┘
```

---

## Known Discrepancies

Agents MUST consult `Docs/Beta/DISCREPANCY-REGISTRY.md` before implementing.

| Issue | v1 (old) | v2 (doc) | Action |
|-------|----------|----------|--------|
| MECHANISM_NAMES | ("ASA",) only | ("BEP","ASA") | Use v2 |
| h3_demand | () empty | Populated from Section 5 | Use v2 |
| Gamma OUTPUT_DIM | 10 | 9 in some docs | Use doc |
| FULL_NAME | Old code names | Doc Section 1 header | Use v2 |
| R3_DIM | 49 | 128 | Use 128 |
| H3 theoretical | 112,896 | 294,912 | Use v2 |

---

## Verification Gate G3

```python
# G3 verification script
from Musical_Intelligence.brain import BrainOrchestrator
from Musical_Intelligence.brain.mechanisms import (
    PPC, TPC, BEP, ASA, TMH, MEM, SYN, AED, CPD, C0P
)

# 1. All 10 mechanisms instantiate with OUTPUT_DIM=30
for Mech in [PPC, TPC, BEP, ASA, TMH, MEM, SYN, AED, CPD, C0P]:
    m = Mech()
    assert m.OUTPUT_DIM == 30, f"{m.NAME} OUTPUT_DIM != 30"

# 2. All 96 models pass validate_constants()
from Musical_Intelligence.brain.units import (
    spu, stu, imu, asu, ndu, mpu, pcu, aru, rpu
)
total_dim, model_count = 0, 0
for unit_mod in [spu, stu, imu, asu, ndu, mpu, pcu, aru, rpu]:
    unit = unit_mod.Unit()
    for model in unit.models:
        model.validate_constants()
        model_count += 1
    total_dim += unit.total_dim

assert model_count == 96, f"Expected 96, got {model_count}"
assert total_dim == 1006, f"Expected 1006D, got {total_dim}"

# 3. BrainOrchestrator output shape
import torch
orchestrator = BrainOrchestrator()
output = orchestrator.run({}, torch.zeros(1, 10, 128))
assert output.tensor.shape == (1, 10, 1006)
assert len(output.dimension_names) == 1006
assert len(output.unit_ranges) == 9

print("G3 PASSED: 96 models valid, BrainOrchestrator -> (B,T,1006)")
```
