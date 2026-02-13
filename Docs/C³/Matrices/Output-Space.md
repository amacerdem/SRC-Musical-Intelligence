# Output-Space -- Output Dimensionality Across the Architecture

> **Scope**: 94 models across 9 units, 3 tiers
> **Grand Total**: 1006D brain output per frame (at 172.27 Hz)
> **Full MI-space**: 1183D + L3 (cochlea 128D + R3 49D + brain 1006D + L3 variable)
> **Data Source**: Unit docs (`Docs/C3/Units/*.md`), model `OUTPUT_DIM` class attributes, `C3-ARCHITECTURE.md`
> **Last Updated**: 2026-02-13

---

## Architecture Summary

Each frame of audio (5.805 ms at 172.27 Hz) is processed into a multi-layered output space:

```
MI-space = [ Cochlea(128D) | R3(49D) | Brain(1006D) | L3(variable) ]
             |               |          |               |
             mel spectrogram spectral   cognitive       semantic
             (fixed)         features   models          (planned)
                             (fixed)    (9 units)
```

| Section | Dimensions | Source | Status |
|---------|-----------|--------|--------|
| Cochlea | 128D | 128-band mel spectrogram | Fixed |
| R3 | 49D | 49 spectral features (5 groups) | Fixed |
| Brain | 1006D | 94 cognitive models in 9 units | Active |
| L3 | Variable | Semantic interpretation layer | Planned |
| **Total MI-space** | **1183D + L3** | | |

---

## Brain Output: Unit-Level Breakdown

| Unit | Full Name | Circuit | Models | Total Output | Avg/Model | Range |
|------|-----------|---------|:------:|:------------:|:---------:|:-----:|
| SPU | Spectral Processing Unit | Perceptual | 9 | 99D | 11.0 | 10--12 |
| STU | Sensorimotor Timing Unit | Sensorimotor | 14 | 148D* | 10.6 | 10--13 |
| IMU | Integrative Memory Unit | Mnemonic | 15 | 159D | 10.6 | 10--12 |
| ASU | Auditory Salience Unit | Salience | 9 | 94D | 10.4 | 10--12 |
| NDU | Novelty Detection Unit | Salience | 9 | 94D | 10.4 | 10--12 |
| MPU | Motor Planning Unit | Sensorimotor | 10 | 104D | 10.4 | 10--12 |
| PCU | Predictive Coding Unit | Mnemonic | 9 | 94D | 10.4 | 10--12 |
| ARU | Affective Resonance Unit | Mesolimbic | 10 | 120D | 12.0 | 10--19 |
| RPU | Reward Processing Unit | Mesolimbic | 9 | 94D | 10.4 | 10--12 |
| **Total** | | | **94** | **1006D** | **10.7** | **10--19** |

### Unit Output as Proportion of Brain Space

```
SPU  |===========                                    |  99D  (9.8%)
STU  |=================                              | 148D (14.7%)
IMU  |==================                             | 159D (15.8%)
ASU  |==========                                     |  94D  (9.3%)
NDU  |==========                                     |  94D  (9.3%)
MPU  |===========                                    | 104D (10.3%)
PCU  |==========                                     |  94D  (9.3%)
ARU  |=============                                  | 120D (11.9%)
RPU  |==========                                     |  94D  (9.3%)
     +-------+-------+-------+-------+-------+------+
     0      200     400     600     800    1000  1006
```

*Note: The STU unit doc and architecture doc declare STU total as 148D. Individual model OUTPUT_DIM values in code sum to 150D (a known 2D discrepancy). The canonical 1006D brain total from `C3-ARCHITECTURE.md` is used throughout this document.

**IMU has the largest output** (159D, 15.8%) due to its 15 models -- the most of any unit, reflecting the breadth of musical memory research. **STU is second** (148D, 14.7%) with 14 models.

---

## Tier-Level Breakdown

### Alpha Tier (>90% confidence, k >= 10)

| Unit | Alpha Models | Individual Dims | Subtotal |
|------|:---:|---|:---:|
| SPU | 3 | BCH(12), PSCL(12), PCCR(11) | 35D |
| STU | 3 | HMCE(13), AMSC(12), MDNS(12) | 37D |
| IMU | 3 | MEAMN(12), PNH(11), MMP(12) | 35D |
| ASU | 3 | SNEM(12), IACM(11), CSG(11) | 34D |
| NDU | 3 | MPG(12), SDD(11), EDNR(11) | 34D |
| MPU | 3 | PEOM(12), MSR(11), GSSM(11) | 34D |
| PCU | 3 | HTP(12), SPH(11), ICEM(11) | 34D |
| ARU | 3 | SRP(19), AAC(14), VMM(12) | 45D |
| RPU | 3 | DAED(12), MORMR(11), RPEM(11) | 34D |
| **Total** | **27** | | **322D** |

| Property | Value |
|----------|-------|
| Model count | 27 (3 per unit, uniform) |
| Total output | 322D |
| Average per model | 11.9D |
| Median per model | 12D |
| Range | 11D -- 19D |
| Outlier | SRP at 19D (the largest model in the system) |

### Beta Tier (70--90% confidence, 5 <= k < 10)

| Unit | Beta Models | Individual Dims | Subtotal |
|------|:---:|---|:---:|
| SPU | 3 | STAI(12), TSCP(10), MIAA(11) | 33D |
| STU | 6 | AMSS(11), TPIO(10), EDTA(10), ETAM(11), HGSIC(11), OMS(10) | 63D |
| IMU | 9 | RASN(11), PMIM(11), OII(10), HCMC(11), RIRI(10), MSPBA(11), VRIAP(10), TPRD(10), CMAPCC(10) | 94D |
| ASU | 3 | BARM(10), STANM(10), AACM(10) | 30D |
| NDU | 3 | DSP_(10), CDMR(10), SLEE(10) | 30D |
| MPU | 4 | ASAP(10), DDSMI(10), VRMSME(10), SPMC(10) | 40D |
| PCU | 3 | PWUP(10), WMED(10), UDP(10) | 30D |
| ARU | 4 | PUPF(12), CLAM(11), MAD(11), NEMAC(11) | 45D |
| RPU | 3 | IUCP(10), MCCN(10), MEAMR(10) | 30D |
| **Total** | **38** | | **395D** |

| Property | Value |
|----------|-------|
| Model count | 38 (variable: 3--9 per unit) |
| Total output | 395D |
| Average per model | 10.4D |
| Median per model | 10D |
| Range | 10D -- 12D |

### Gamma Tier (<70% confidence, k < 5)

| Unit | Gamma Models | Individual Dims | Subtotal |
|------|:---:|---|:---:|
| SPU | 3 | SDNPS(10), ESME(11), SDED(10) | 31D |
| STU | 5 | TMRM(10), NEWMD(10), MTNE(10), PTGMP(10), MPFS(10) | 50D |
| IMU | 3 | DMMS(10), CSSL(10), CDEM(10) | 30D |
| ASU | 3 | PWSM(10), DGTP(10), SDL(10) | 30D |
| NDU | 3 | SDDP(10), ONI(10), ECT(10) | 30D |
| MPU | 3 | NSCP(10), CTBB(10), STC(10) | 30D |
| PCU | 3 | IGFE(10), MAA(10), PSH(10) | 30D |
| ARU | 3 | DAP(10), CMAT(10), TAR(10) | 30D |
| RPU | 3 | LDAC(10), IOTMS(10), SSPS(10) | 30D |
| **Total** | **29** | | **291D** |

| Property | Value |
|----------|-------|
| Model count | 29 (3 per unit, except STU with 5) |
| Total output | 291D |
| Average per model | 10.0D |
| Median per model | 10D |
| Range | 10D -- 11D (ESME is the sole 11D gamma outlier) |

Note: Gamma models are **uniformly 10D** with the exception of ESME (SPU-gamma2, 11D). The 10D convention reflects conservative parameterization given limited evidence.

---

## Tier Comparison

| Tier | Models | Total D | Avg D | Median D | Min D | Max D | % of Brain* |
|------|:------:|:-------:|:-----:|:--------:|:-----:|:-----:|:-----------:|
| Alpha | 27 | 322D | 11.9 | 12 | 11 | 19 | 32.0% |
| Beta | 38 | 395D | 10.4 | 10 | 10 | 12 | 39.3% |
| Gamma | 29 | 291D | 10.0 | 10 | 10 | 11 | 28.9% |

*Percentages use the canonical 1006D brain total from `C3-ARCHITECTURE.md`. The per-model OUTPUT_DIM values in code sum to 1008D (a 2D discrepancy in the STU unit). The Alpha and Beta tier doc total numbers (327D and 419D respectively) include planned models CHPI and SSRI that have not yet been implemented in code. The numbers above reflect the 94 models currently in the codebase.

```
         Alpha (322D, 32.0%)       Beta (395D, 39.3%)       Gamma (291D, 28.9%)
     +-------------------------+----------------------------+------------------------+
     |                         |                            |                        |
     |  27 models              |  38 models                 |  29 models             |
     |  11.9D avg              |  10.4D avg                 |  10.0D avg             |
     |  >90% confidence        |  70-90% confidence         |  <70% confidence       |
     |                         |                            |                        |
     +-------------------------+----------------------------+------------------------+
     0                        322                          717                    1008
```

---

## Per-Model Output Layer Structure

Each model's output dimensions are organized into semantic layers. The most common pattern (from `LayerSpec` declarations) is:

| Layer | Label | Typical Size | Purpose |
|-------|-------|:---:|---------|
| E | Explicit Features | 3--5D | Directly extracted or computed features from the literature |
| M | Mathematical Model | 2--4D | Formal mathematical relationships (equations, functions) |
| P | Present Processing | 2--3D | Current-frame state variables |
| F | Future Predictions | 2--3D | Forward-looking predictions and expectations |

### Variant Layer Patterns

Some models use specialized layer structures:

| Model | Layers | Structure | Notes |
|-------|--------|-----------|-------|
| SRP (19D) | N+C+P+T+M+F | 3+3+3+4+3+3 | 6 layers: Neurochemical, Circuit, Psychological, Temporal, Musical, Forecast |
| AAC (14D) | E+M+P+F | 4+4+3+3 | Standard 4-layer with expanded E and M |
| HMCE (13D) | E+M+P+F | 5+2+3+3 | Standard 4-layer with large E |
| Gamma 10D | E+M+P+F | 3+2+2+3 | Minimal 4-layer (conservative) |

### Layer Distribution Across Tiers

| Tier | Typical E | Typical M | Typical P | Typical F | Extra Layers |
|------|:---------:|:---------:|:---------:|:---------:|:------------:|
| Alpha | 3--5D | 2--4D | 2--3D | 2--3D | Some (N, C, T) |
| Beta | 3D | 2--3D | 2--3D | 2--3D | Rare |
| Gamma | 3D | 2D | 2D | 3D | None |

---

## Circuit-Level Output Summary

| Circuit | Units | Total Models | Total Output | % of Brain |
|---------|-------|:---:|:---:|:---:|
| Perceptual | SPU | 9 | 99D | 9.8% |
| Sensorimotor | STU, MPU | 24 | 252D | 25.0% |
| Mnemonic | IMU, PCU | 24 | 253D | 25.1% |
| Salience | ASU, NDU | 18 | 188D | 18.7% |
| Mesolimbic | ARU, RPU | 19 | 214D | 21.3% |

```
Perceptual     |===                                | 99D   (9.8%)
Sensorimotor   |=========                          | 252D  (25.0%)
Mnemonic       |=========                          | 253D  (25.1%)
Salience       |=======                            | 188D  (18.7%)
Mesolimbic     |========                           | 214D  (21.3%)
               +--------+--------+--------+-------+
               0       250      500      750    1006
```

**Mnemonic and Sensorimotor circuits produce the most output** (~25% each), reflecting the prominence of memory and timing in musical cognition. The Perceptual circuit (SPU only) is the smallest, as spectral features are already well-represented in R3.

---

## Assembly Order and MI-Space Layout

The brain output is assembled in `UNIT_EXECUTION_ORDER` with contiguous ranges:

| Position | Unit | Range | Dimensions |
|----------|------|-------|-----------|
| 0 | SPU | [0, 99) | 99D |
| 1 | STU | [99, 247) | 148D |
| 2 | IMU | [247, 406) | 159D |
| 3 | ASU | [406, 500) | 94D |
| 4 | NDU | [500, 594) | 94D |
| 5 | MPU | [594, 698) | 104D |
| 6 | PCU | [698, 792) | 94D |
| 7 | ARU | [792, 912) | 120D |
| 8 | RPU | [912, 1006) | 94D |

### Full MI-Space Layout

| Section | Global Range | Dimensions |
|---------|-------------|-----------|
| Cochlea | [0, 128) | 128D |
| R3 | [128, 177) | 49D |
| Brain | [177, 1183) | 1006D |
| -- SPU | [177, 276) | 99D |
| -- STU | [276, 424) | 148D |
| -- IMU | [424, 583) | 159D |
| -- ASU | [583, 677) | 94D |
| -- NDU | [677, 771) | 94D |
| -- MPU | [771, 875) | 104D |
| -- PCU | [875, 969) | 94D |
| -- ARU | [969, 1089) | 120D |
| -- RPU | [1089, 1183) | 94D |
| L3 | [1183, 1183+L3) | Variable |

---

## Dependency and Phase Contribution

| Phase | Units | Output | % of Brain | Dependencies |
|-------|-------|--------|-----------|-------------|
| Phase 2 (Independent) | SPU, STU, IMU, ASU, NDU, MPU, PCU | 792D | 78.7% | H3/R3 only |
| Phase 4 (Dependent) | ARU, RPU | 214D | 21.3% | Cross-unit pathways |

The independent units produce nearly 4x more output than the dependent units. However, the dependent units (ARU, RPU) are the most functionally important for the system's primary purpose -- modeling musical pleasure and reward.

---

## Output Per Frame: Computational Budget

| Metric | Value |
|--------|-------|
| Frame rate | 172.27 Hz (5.805 ms per frame) |
| Brain output per frame | 1006 floats (4024 bytes at fp32) |
| MI-space per frame | 1183+ floats (4732+ bytes) |
| Brain output per second | ~173,300 floats/s |
| MI-space per second | ~203,800+ floats/s |
| Brain output for 3-min song | ~31.1M floats (~124 MB) |
| MI-space for 3-min song | ~36.7M+ floats (~147+ MB) |

---

## Complete Model Roster with OUTPUT_DIM

For reference, the complete list of all 94 models with their output dimensionality:

| # | Unit | Model | Tier | OUTPUT_DIM |
|---|------|-------|------|:---:|
| 1 | SPU | BCH | alpha | 12 |
| 2 | SPU | PSCL | alpha | 12 |
| 3 | SPU | PCCR | alpha | 11 |
| 4 | SPU | STAI | beta | 12 |
| 5 | SPU | TSCP | beta | 10 |
| 6 | SPU | MIAA | beta | 11 |
| 7 | SPU | SDNPS | gamma | 10 |
| 8 | SPU | ESME | gamma | 11 |
| 9 | SPU | SDED | gamma | 10 |
| 10 | STU | HMCE | alpha | 13 |
| 11 | STU | AMSC | alpha | 12 |
| 12 | STU | MDNS | alpha | 12 |
| 13 | STU | AMSS | beta | 11 |
| 14 | STU | TPIO | beta | 10 |
| 15 | STU | EDTA | beta | 10 |
| 16 | STU | ETAM | beta | 11 |
| 17 | STU | HGSIC | beta | 11 |
| 18 | STU | OMS | beta | 10 |
| 19 | STU | TMRM | gamma | 10 |
| 20 | STU | NEWMD | gamma | 10 |
| 21 | STU | MTNE | gamma | 10 |
| 22 | STU | PTGMP | gamma | 10 |
| 23 | STU | MPFS | gamma | 10 |
| 24 | IMU | MEAMN | alpha | 12 |
| 25 | IMU | PNH | alpha | 11 |
| 26 | IMU | MMP | alpha | 12 |
| 27 | IMU | RASN | beta | 11 |
| 28 | IMU | PMIM | beta | 11 |
| 29 | IMU | OII | beta | 10 |
| 30 | IMU | HCMC | beta | 11 |
| 31 | IMU | RIRI | beta | 10 |
| 32 | IMU | MSPBA | beta | 11 |
| 33 | IMU | VRIAP | beta | 10 |
| 34 | IMU | TPRD | beta | 10 |
| 35 | IMU | CMAPCC | beta | 10 |
| 36 | IMU | DMMS | gamma | 10 |
| 37 | IMU | CSSL | gamma | 10 |
| 38 | IMU | CDEM | gamma | 10 |
| 39 | ASU | SNEM | alpha | 12 |
| 40 | ASU | IACM | alpha | 11 |
| 41 | ASU | CSG | alpha | 11 |
| 42 | ASU | BARM | beta | 10 |
| 43 | ASU | STANM | beta | 10 |
| 44 | ASU | AACM | beta | 10 |
| 45 | ASU | PWSM | gamma | 10 |
| 46 | ASU | DGTP | gamma | 10 |
| 47 | ASU | SDL | gamma | 10 |
| 48 | NDU | MPG | alpha | 12 |
| 49 | NDU | SDD | alpha | 11 |
| 50 | NDU | EDNR | alpha | 11 |
| 51 | NDU | DSP_ | beta | 10 |
| 52 | NDU | CDMR | beta | 10 |
| 53 | NDU | SLEE | beta | 10 |
| 54 | NDU | SDDP | gamma | 10 |
| 55 | NDU | ONI | gamma | 10 |
| 56 | NDU | ECT | gamma | 10 |
| 57 | MPU | PEOM | alpha | 12 |
| 58 | MPU | MSR | alpha | 11 |
| 59 | MPU | GSSM | alpha | 11 |
| 60 | MPU | ASAP | beta | 10 |
| 61 | MPU | DDSMI | beta | 10 |
| 62 | MPU | VRMSME | beta | 10 |
| 63 | MPU | SPMC | beta | 10 |
| 64 | MPU | NSCP | gamma | 10 |
| 65 | MPU | CTBB | gamma | 10 |
| 66 | MPU | STC | gamma | 10 |
| 67 | PCU | HTP | alpha | 12 |
| 68 | PCU | SPH | alpha | 11 |
| 69 | PCU | ICEM | alpha | 11 |
| 70 | PCU | PWUP | beta | 10 |
| 71 | PCU | WMED | beta | 10 |
| 72 | PCU | UDP | beta | 10 |
| 73 | PCU | IGFE | gamma | 10 |
| 74 | PCU | MAA | gamma | 10 |
| 75 | PCU | PSH | gamma | 10 |
| 76 | ARU | SRP | alpha | 19 |
| 77 | ARU | AAC | alpha | 14 |
| 78 | ARU | VMM | alpha | 12 |
| 79 | ARU | PUPF | beta | 12 |
| 80 | ARU | CLAM | beta | 11 |
| 81 | ARU | MAD | beta | 11 |
| 82 | ARU | NEMAC | beta | 11 |
| 83 | ARU | DAP | gamma | 10 |
| 84 | ARU | CMAT | gamma | 10 |
| 85 | ARU | TAR | gamma | 10 |
| 86 | RPU | DAED | alpha | 12 |
| 87 | RPU | MORMR | alpha | 11 |
| 88 | RPU | RPEM | alpha | 11 |
| 89 | RPU | IUCP | beta | 10 |
| 90 | RPU | MCCN | beta | 10 |
| 91 | RPU | MEAMR | beta | 10 |
| 92 | RPU | LDAC | gamma | 10 |
| 93 | RPU | IOTMS | gamma | 10 |
| 94 | RPU | SSPS | gamma | 10 |

---

## Cross-References

- **Architecture Overview**: [C3-ARCHITECTURE.md](../C3-ARCHITECTURE.md) -- full pipeline and dimensionality summary
- **Tier Definitions**: [Tiers/Alpha.md](../Tiers/Alpha.md), [Beta.md](../Tiers/Beta.md), [Gamma.md](../Tiers/Gamma.md)
- **Unit Docs**: [Units/](../Units/) -- per-unit model rosters and output totals
- **Dimension Map**: `mi_beta.core.dimension_map.DimensionMap` -- runtime index tracking
- **Assembly**: `mi_beta.pipeline.brain_runner.BrainOrchestrator` -- Phase 5 concatenation
