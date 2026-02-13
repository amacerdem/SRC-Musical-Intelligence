# Mechanism-Map -- Mechanism Usage Across All Models

> **Scope**: 94 models across 9 units, 10 mechanisms
> **Mechanism Output**: Each mechanism produces 30D (3 x 10D sub-sections by horizon)
> **Data Source**: Unit docs (`Docs/C3/Units/*.md`), model `MECHANISM_NAMES` class attributes, `Docs/C3/Mechanisms/00-INDEX.md`
> **Last Updated**: 2026-02-13

---

## Mechanism Catalogue

| Abbr | Full Name | Circuit | Output | Horizons |
|------|-----------|---------|--------|----------|
| AED | Affective Entrainment Dynamics | Mesolimbic | 30D | H6, H16 |
| ASA | Auditory Scene Analysis | Salience | 30D | H3, H6, H9 |
| BEP | Beat Entrainment Processing | Sensorimotor | 30D | H6, H9, H11 |
| C0P | Cognitive Projection | Mesolimbic | 30D | H18, H19, H20 |
| CPD | Chills & Peak Detection | Mesolimbic | 30D | H9, H16, H18 |
| MEM | Memory Encoding / Retrieval | Mnemonic | 30D | H18, H20, H22, H25 |
| PPC | Pitch Processing Chain | Perceptual | 30D | H0, H3, H6 |
| SYN | Syntactic Processing | Mnemonic | 30D | H12, H16, H18 |
| TMH | Temporal Memory Hierarchy | Sensorimotor | 30D | H16, H18, H20, H22 |
| TPC | Timbre Processing Chain | Perceptual | 30D | H6, H12, H16 |

---

## Full 94-Model x 10-Mechanism Usage Matrix

### SPU -- Spectral Processing Unit (9 models)

| Model | Tier | AED | ASA | BEP | C0P | CPD | MEM | PPC | SYN | TMH | TPC |
|-------|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| BCH | alpha | . | . | . | . | . | . | **X** | . | . | . |
| PSCL | alpha | . | . | . | . | . | . | **X** | . | . | . |
| PCCR | alpha | . | . | . | . | . | . | **X** | . | . | . |
| STAI | beta | . | . | . | . | . | . | . | . | . | **X** |
| TSCP | beta | . | . | . | . | . | . | . | . | . | **X** |
| MIAA | beta | . | . | . | . | . | . | . | . | . | **X** |
| SDNPS | gamma | . | . | . | . | . | . | **X** | . | . | . |
| ESME | gamma | . | . | . | . | . | . | **X** | . | . | . |
| SDED | gamma | . | . | . | . | . | . | **X** | . | . | . |

**SPU mechanisms**: PPC (6 models), TPC (3 models). Clean split between pitch (alpha+gamma) and timbre (beta).

### STU -- Sensorimotor Timing Unit (14 models)

| Model | Tier | AED | ASA | BEP | C0P | CPD | MEM | PPC | SYN | TMH | TPC |
|-------|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| HMCE | alpha | . | . | **X** | . | . | . | . | . | **X** | . |
| AMSC | alpha | . | . | **X** | . | . | . | . | . | **X** | . |
| MDNS | alpha | . | . | **X** | . | . | . | . | . | . | . |
| AMSS | beta | . | . | **X** | . | . | . | . | . | . | . |
| TPIO | beta | . | . | . | . | . | . | . | . | . | **X** |
| EDTA | beta | . | . | **X** | . | . | . | . | . | . | . |
| ETAM | beta | . | . | **X** | . | . | . | . | . | . | . |
| HGSIC | beta | . | . | **X** | . | . | . | . | . | **X** | . |
| OMS | beta | . | . | **X** | . | . | . | . | . | . | . |
| TMRM | gamma | . | . | **X** | . | . | . | . | . | **X** | . |
| NEWMD | gamma | . | . | **X** | . | . | . | . | . | . | . |
| MTNE | gamma | . | . | **X** | . | . | . | . | . | . | . |
| PTGMP | gamma | . | . | **X** | . | . | . | . | . | . | . |
| MPFS | gamma | . | . | **X** | . | . | . | . | . | . | . |

**STU mechanisms**: BEP (13 models), TMH (4 models), TPC (1 model -- TPIO). BEP is the dominant mechanism.

### IMU -- Integrative Memory Unit (15 models)

| Model | Tier | AED | ASA | BEP | C0P | CPD | MEM | PPC | SYN | TMH | TPC |
|-------|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| MEAMN | alpha | . | . | . | . | . | **X** | . | . | **X** | . |
| PNH | alpha | . | . | . | . | . | **X** | . | . | . | . |
| MMP | alpha | . | . | . | . | . | **X** | . | . | . | . |
| RASN | beta | . | . | **X** | . | . | **X** | . | . | . | . |
| PMIM | beta | . | . | . | . | . | **X** | . | . | **X** | . |
| OII | beta | . | . | . | . | . | **X** | . | . | . | . |
| HCMC | beta | . | . | . | . | . | **X** | . | . | . | . |
| RIRI | beta | . | . | . | . | . | **X** | . | . | . | . |
| MSPBA | beta | . | . | . | . | . | . | . | **X** | . | . |
| VRIAP | beta | . | . | . | . | . | **X** | . | . | . | . |
| TPRD | beta | . | . | . | . | . | . | **X** | . | . | . |
| CMAPCC | beta | . | . | **X** | . | . | **X** | . | . | . | . |
| DMMS | gamma | . | . | . | . | . | **X** | . | . | . | . |
| CSSL | gamma | . | . | . | . | . | **X** | . | . | . | . |
| CDEM | gamma | . | . | . | . | . | **X** | . | . | . | . |

**IMU mechanisms**: MEM (13 models), TMH (2), BEP (2), SYN (1), PPC (1). MEM dominates, reflecting memory as the unit's core function.

### ASU -- Auditory Salience Unit (9 models)

| Model | Tier | AED | ASA | BEP | C0P | CPD | MEM | PPC | SYN | TMH | TPC |
|-------|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| SNEM | alpha | . | **X** | . | . | . | . | . | . | . | . |
| IACM | alpha | . | **X** | . | . | . | . | . | . | . | . |
| CSG | alpha | . | **X** | . | . | . | . | . | . | . | . |
| BARM | beta | . | **X** | . | . | . | . | . | . | . | . |
| STANM | beta | . | **X** | . | . | . | . | . | . | . | . |
| AACM | beta | . | **X** | . | . | . | . | . | . | . | . |
| PWSM | gamma | . | **X** | . | . | . | . | . | . | . | . |
| DGTP | gamma | . | **X** | . | . | . | . | . | . | . | . |
| SDL | gamma | . | **X** | . | . | . | . | . | . | . | . |

**ASU mechanisms**: ASA (9/9 models). All ASU models use ASA exclusively -- the most uniform unit.

### NDU -- Novelty Detection Unit (9 models)

| Model | Tier | AED | ASA | BEP | C0P | CPD | MEM | PPC | SYN | TMH | TPC |
|-------|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| MPG | alpha | . | **X** | . | . | . | . | . | . | . | . |
| SDD | alpha | . | **X** | . | . | . | . | **X** | . | . | . |
| EDNR | alpha | . | **X** | . | . | . | . | . | . | . | . |
| DSP_ | beta | . | **X** | . | . | . | . | . | . | . | . |
| CDMR | beta | . | **X** | . | . | . | . | . | . | **X** | . |
| SLEE | beta | . | **X** | . | . | . | **X** | . | . | . | . |
| SDDP | gamma | . | **X** | . | . | . | . | . | . | . | . |
| ONI | gamma | . | **X** | . | . | . | . | . | . | . | . |
| ECT | gamma | . | **X** | . | . | . | . | . | . | . | . |

**NDU mechanisms**: ASA (9/9), PPC (1), TMH (1), MEM (1). ASA is primary, with secondary mechanisms in specific models.

### MPU -- Motor Planning Unit (10 models)

| Model | Tier | AED | ASA | BEP | C0P | CPD | MEM | PPC | SYN | TMH | TPC |
|-------|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| PEOM | alpha | . | . | **X** | . | . | . | . | . | . | . |
| MSR | alpha | . | . | **X** | . | . | . | . | . | . | . |
| GSSM | alpha | . | . | **X** | . | . | . | . | . | . | . |
| ASAP | beta | . | . | **X** | . | . | . | . | . | . | . |
| DDSMI | beta | . | . | **X** | . | . | . | . | . | . | . |
| VRMSME | beta | . | . | **X** | . | . | . | . | . | . | . |
| SPMC | beta | . | . | **X** | . | . | . | . | . | . | . |
| NSCP | gamma | . | . | **X** | . | . | . | . | . | . | . |
| CTBB | gamma | . | . | **X** | . | . | . | . | . | . | . |
| STC | gamma | . | . | **X** | . | . | . | . | . | . | . |

**MPU mechanisms**: BEP (10/10 models). All MPU models use BEP exclusively -- tied with ASU for most uniform.

### PCU -- Predictive Coding Unit (9 models)

| Model | Tier | AED | ASA | BEP | C0P | CPD | MEM | PPC | SYN | TMH | TPC |
|-------|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| HTP | alpha | . | . | . | . | . | **X** | **X** | . | . | **X** |
| SPH | alpha | . | . | . | . | . | . | **X** | . | . | . |
| ICEM | alpha | **X** | . | . | **X** | . | . | . | . | . | . |
| PWUP | beta | . | . | . | . | . | . | **X** | . | . | . |
| WMED | beta | **X** | . | . | . | . | **X** | . | . | . | . |
| UDP | beta | . | . | . | **X** | . | . | . | . | . | . |
| IGFE | gamma | . | . | . | . | . | . | . | . | . | **X** |
| MAA | gamma | . | **X** | . | . | . | . | . | . | . | . |
| PSH | gamma | . | . | . | . | . | **X** | **X** | . | . | **X** |

**PCU mechanisms**: PPC (4), TPC (3), MEM (3), AED (2), C0P (2), ASA (1). PCU has the **broadest mechanism diversity** of any unit -- 6 of 10 mechanisms used.

### ARU -- Affective Resonance Unit (10 models)

| Model | Tier | AED | ASA | BEP | C0P | CPD | MEM | PPC | SYN | TMH | TPC |
|-------|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| SRP | alpha | **X** | . | . | **X** | **X** | . | . | . | . | . |
| AAC | alpha | **X** | **X** | . | . | **X** | . | . | . | . | . |
| VMM | alpha | **X** | . | . | **X** | . | . | . | . | . | . |
| PUPF | beta | **X** | . | . | . | **X** | . | . | . | . | . |
| CLAM | beta | **X** | . | . | . | . | . | . | . | . | . |
| MAD | beta | **X** | . | . | . | **X** | . | . | . | . | . |
| NEMAC | beta | **X** | . | . | . | . | **X** | . | . | . | . |
| DAP | gamma | **X** | . | . | . | . | . | . | . | . | . |
| CMAT | gamma | **X** | . | . | . | . | . | . | . | . | . |
| TAR | gamma | **X** | . | . | . | . | . | . | . | . | . |

**ARU mechanisms**: AED (10/10), CPD (4), C0P (2), ASA (1), MEM (1). **All 10 ARU models use AED** -- the defining mechanism of the affective system.

### RPU -- Reward Processing Unit (9 models)

| Model | Tier | AED | ASA | BEP | C0P | CPD | MEM | PPC | SYN | TMH | TPC |
|-------|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| DAED | alpha | **X** | . | . | . | **X** | . | . | . | . | . |
| MORMR | alpha | **X** | . | . | **X** | . | . | . | . | . | . |
| RPEM | alpha | **X** | . | . | . | **X** | . | . | . | . | . |
| IUCP | beta | . | . | . | **X** | . | . | . | . | . | . |
| MCCN | beta | **X** | . | . | . | . | . | . | . | **X** | . |
| MEAMR | beta | **X** | . | . | . | . | **X** | . | . | . | . |
| LDAC | gamma | **X** | . | . | . | . | . | . | . | . | . |
| IOTMS | gamma | . | . | **X** | . | . | . | . | . | . | . |
| SSPS | gamma | . | **X** | . | . | . | . | . | . | . | . |

**RPU mechanisms**: AED (6), CPD (2), C0P (2), TMH (1), MEM (1), BEP (1), ASA (1). RPU uses **7 of 10 mechanisms** -- broadest alongside PCU (6).

---

## Mechanism Usage Summary Statistics

### Models per Mechanism

| Mechanism | Models Using | % of 94 | Units Using | Primary Unit |
|-----------|:-----------:|:-------:|:-----------:|-------------|
| **BEP** | 26 | 28% | 4 (STU, MPU, IMU, RPU) | STU (13), MPU (10) |
| **ASA** | 21 | 22% | 5 (ASU, NDU, PCU, ARU, RPU) | ASU (9), NDU (9) |
| **AED** | 18 | 19% | 3 (ARU, RPU, PCU) | ARU (10), RPU (6) |
| **MEM** | 20 | 21% | 4 (IMU, PCU, ARU, RPU) | IMU (13) |
| **PPC** | 12 | 13% | 4 (SPU, NDU, PCU, IMU) | SPU (6) |
| **TPC** | 7 | 7% | 3 (SPU, STU, PCU) | SPU (3), PCU (3) |
| **CPD** | 6 | 6% | 2 (ARU, RPU) | ARU (4), RPU (2) |
| **TMH** | 8 | 9% | 4 (STU, IMU, NDU, RPU) | STU (4) |
| **C0P** | 6 | 6% | 3 (ARU, RPU, PCU) | ARU (2), RPU (2), PCU (2) |
| **SYN** | 1 | 1% | 1 (IMU) | IMU (1 -- MSPBA only) |

### Ranking

| Rank | Mechanism | Usage Count | Role |
|------|-----------|:-----------:|------|
| 1 | BEP | 26 | Beat entrainment -- the sensorimotor backbone |
| 2 | ASA | 21 | Scene analysis -- salience detection |
| 3 | MEM | 20 | Memory -- encoding and retrieval |
| 4 | AED | 18 | Affective dynamics -- emotional processing |
| 5 | PPC | 12 | Pitch processing -- spectral analysis |
| 6 | TMH | 8 | Temporal memory -- multi-scale integration |
| 7 | TPC | 7 | Timbre processing -- spectral quality |
| 8 | CPD | 6 | Chills detection -- peak emotional moments |
| 8 | C0P | 6 | Cognitive projection -- predictive valuation |
| 10 | SYN | 1 | Syntactic processing -- musical grammar |

**BEP is the most widely used mechanism** (26 models, 28%), reflecting the centrality of beat/rhythm processing in musical cognition.

**SYN is the least used** (1 model -- MSPBA), as musical syntax processing is narrowly specialized.

---

## Mechanism Diversity by Unit

| Unit | Mechanisms Used | Diversity (of 10) | Most Used Mechanism |
|------|:--------------:|:--:|-------------------|
| PCU | 6 | 60% | PPC (4 models) |
| RPU | 7 | 70% | AED (6 models) |
| IMU | 5 | 50% | MEM (13 models) |
| ARU | 5 | 50% | AED (10 models) |
| NDU | 4 | 40% | ASA (9 models) |
| STU | 3 | 30% | BEP (13 models) |
| SPU | 2 | 20% | PPC (6 models) |
| ASU | 1 | 10% | ASA (9 models) |
| MPU | 1 | 10% | BEP (10 models) |

**Observation**: Dependent units (ARU, RPU) and the predictive unit (PCU) use the most diverse mechanism sets, reflecting their integrative roles. Independent perceptual/motor units (SPU, ASU, MPU) are highly specialized.

---

## Mechanism Co-occurrence

Many models use multiple mechanisms. The most common pairings:

| Pair | Models Using Both | Example Models |
|------|:--:|----------------|
| AED + CPD | 6 | SRP, AAC, PUPF, MAD, DAED, RPEM |
| AED + C0P | 4 | SRP, VMM, MORMR, ICEM |
| BEP + TMH | 4 | HMCE, AMSC, HGSIC, TMRM |
| MEM + TMH | 2 | MEAMN, PMIM |
| PPC + TPC | 2 | HTP, PSH |
| PPC + MEM | 2 | HTP, PSH |
| AED + MEM | 2 | NEMAC, WMED |
| BEP + MEM | 2 | RASN, CMAPCC |

### Triple Mechanism Usage

| Triple | Models |
|--------|--------|
| AED + CPD + C0P | SRP |
| AED + CPD + ASA | AAC |
| PPC + TPC + MEM | HTP, PSH |

**SRP (ARU-alpha1) uses the most mechanisms of any single model**: AED + CPD + C0P (3 mechanisms, all mesolimbic).

**HTP (PCU-alpha1) uses the most diverse mechanisms**: PPC + TPC + MEM (3 mechanisms across 2 circuits).

---

## Circuit-Level Mechanism Clustering

| Circuit | Mechanisms | Total Model-Uses | % of All Uses |
|---------|-----------|:----:|:---:|
| Sensorimotor | BEP, TMH | 34 | 26% |
| Salience | ASA | 21 | 16% |
| Mnemonic | MEM, SYN | 21 | 16% |
| Mesolimbic | AED, CPD, C0P | 30 | 23% |
| Perceptual | PPC, TPC | 19 | 15% |

The Mesolimbic circuit (AED+CPD+C0P) accounts for the most total mechanism-model assignments (30), driven by ARU and RPU's high use of AED.

---

## Mechanism Sharing Architecture

Mechanisms are computed once by the `MechanismRunner` (Phase 1) and cached. Models reference cached outputs rather than recomputing:

```
Phase 1: MechanismRunner computes all needed mechanisms
  -> AED(30D), ASA(30D), BEP(30D), ... cached

Phase 2-4: Each model receives its MECHANISM_NAMES outputs
  -> SRP.compute({"AED": tensor, "CPD": tensor, "C0P": tensor}, ...)
  -> BCH.compute({"PPC": tensor}, ...)
```

This sharing means that a mechanism like BEP (used by 26 models) is computed exactly once per frame, not 26 times.

---

## Cross-References

- **Mechanism Definitions**: [Mechanisms/00-INDEX.md](../Mechanisms/00-INDEX.md) and individual files [AED.md](../Mechanisms/AED.md), etc.
- **Unit Docs**: [Units/](../Units/) -- mechanism assignments per unit
- **H3 Demand Patterns**: [H3-Demand.md](H3-Demand.md) -- mechanism horizon declarations
- **Code**: `mi_beta/brain/mechanisms/` -- BaseMechanism implementations
