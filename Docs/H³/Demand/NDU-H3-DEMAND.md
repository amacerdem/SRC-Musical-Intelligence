# NDU H3 Demand Specification

**Version**: 2.0.0
**Updated**: 2026-02-13
**Unit**: Novelty Detection Unit (NDU)
**Status**: Canonical demand specification for NDU models

---

## Table of Contents

1. [Unit Overview](#1-unit-overview)
2. [Mechanism Summary](#2-mechanism-summary)
3. [Per-Model Demand Table](#3-per-model-demand-table)
4. [Horizon Coverage](#4-horizon-coverage)
5. [R3 Feature Consumption](#5-r3-feature-consumption)
6. [R3 v2 Expansion Impact](#6-r3-v2-expansion-impact)
7. [Architectural Notes](#7-architectural-notes)
8. [Cross-References](#8-cross-references)

---

## 1. Unit Overview

The Novelty Detection Unit (NDU) identifies unexpected, deviant, or novel events in the auditory stream. Its 9 models span all three tiers (alpha, beta, gamma) and collectively consume an estimated **~400 H3 demand tuples** from the theoretical `(r3_idx, horizon, morph, law)` address space.

| Property | Value |
|----------|-------|
| Models | 9 (alpha: 3, beta: 3, gamma: 3) |
| Mechanisms | ASA (9), PPC (1), TMH (1), MEM (1) |
| Primary Band | All bands (Micro through Macro) |
| Primary R3 Domains | D (Change), E (Interactions) |
| Est. Total Tuples | ~400 |
| Primary Law | L1 (Prediction) |

NDU's primary law is **L1 (Prediction)** because novelty detection fundamentally requires forward prediction: a stimulus is novel only relative to what was expected. The prediction error signal drives the core computation of every NDU model.

---

## 2. Mechanism Summary

| Mechanism | Models Using | Horizons | Band Range | Role in NDU |
|-----------|:-----------:|----------|:----------:|-------------|
| ASA | 9 (all) | H3, H6, H9 | Micro-Meso | Core salience-driven attention for novelty gating |
| PPC | 1 (SDD) | H0, H3, H6 | Micro | Hierarchical predictive comparison for spectral deviance |
| TMH | 1 (SDD) | H16, H18, H20, H22 | Macro | Long-range temporal memory for structural novelty |
| MEM | 1 (EDNR) | H18, H20, H22, H25 | Macro-Ultra | Episodic memory integration for energy-domain novelty |

ASA is the universal mechanism across all 9 NDU models, reflecting the fundamental role of auditory salience in novelty gating. SDD and EDNR are outlier models that extend beyond the core ASA pattern, incorporating PPC/TMH and MEM respectively to capture structural and episodic novelty at longer timescales.

---

## 3. Per-Model Demand Table

| Model | Tier | Mechanisms | Horizons | Key R3 Features | Est. Tuples |
|-------|------|-----------|----------|-----------------|:-----------:|
| MPG | alpha1 | ASA | H3, H6, H9 | D, E (change, interactions) | ~40 |
| SDD | alpha2 | ASA, PPC, TMH | H0, H3, H6, H9, H16, H18, H20, H22 | A, C, D (spectral deviance) | ~120 |
| EDNR | alpha3 | ASA, MEM | H3, H6, H9, H18, H20, H22, H25 | B, D, E (energy novelty) | ~100 |
| DSP_ | beta1 | ASA | H3, H6, H9 | D, E (deviance statistics) | ~40 |
| CDMR | beta2 | ASA | H3, H6, H9 | D, E (change detection) | ~40 |
| SLEE | beta3 | ASA | H3, H6, H9 | A, D, E (surprise estimation) | ~40 |
| SDDP | gamma1 | ASA | H3, H6, H9 | C, D (spectral deviance) | ~30 |
| ONI | gamma2 | ASA | H3, H6, H9 | B, D, E (onset novelty) | ~30 |
| ECT | gamma3 | ASA | H3, H6, H9 | D, E (change tracking) | ~30 |

### Tier Distribution

- **Alpha tier** (MPG, SDD, EDNR): ~260 tuples -- alpha models carry 65% of NDU demand, with SDD and EDNR as the multi-mechanism outliers
- **Beta tier** (DSP_, CDMR, SLEE): ~120 tuples -- compact ASA-only demand at Micro-Meso horizons
- **Gamma tier** (SDDP, ONI, ECT): ~90 tuples -- minimal demand, each contributing output layer projections

---

## 4. Horizon Coverage

```
Micro   [H0-H7]:   H0(SDD), H3(all), H6(all)
Meso    [H8-H15]:  H9(all)
Macro   [H16-H23]: H16(SDD), H18(SDD,EDNR), H20(SDD,EDNR), H22(SDD,EDNR)
Ultra   [H24-H31]: H25(EDNR)
```

The majority of NDU models operate in the Micro-Meso range (H3, H6, H9) via ASA. Only SDD and EDNR extend into Macro and Ultra bands, requiring longer temporal windows for structural novelty detection and episodic memory comparison respectively.

### Horizon Heatmap

| Horizon | H0 | H3 | H6 | H9 | H16 | H18 | H20 | H22 | H25 |
|---------|:--:|:--:|:--:|:--:|:---:|:---:|:---:|:---:|:---:|
| Models  |  1 |  9 |  9 |  9 |  1  |  2  |  2  |  2  |  1  |

---

## 5. R3 Feature Consumption

NDU draws primarily from the Change (D) and Interactions (E) domains of R3:

| R3 Domain | Features Used | Primary Consumers |
|-----------|---------------|-------------------|
| A: Consonance | [0]-[6] | SDD (spectral deviance), SLEE (surprise) |
| B: Energy | [7]-[11] | EDNR (energy novelty), ONI (onset novelty) |
| C: Timbre | [12]-[20] | SDD (spectral deviance), SDDP (spectral deviance) |
| D: Change | [21]-[24] | All 9 models (core novelty features) |
| E: Interactions | [25]-[48] | All 9 models except SDD, SDDP |

Domain D (Change) is the universal consumption target -- every NDU model requires spectral change features as the basis for novelty computation. Domain E (Interactions) provides cross-domain coupling signals that contextualize novelty within the broader spectral landscape.

---

## 6. R3 v2 Expansion Impact

With the R3 v2 feature set (groups F through K), NDU demand expands substantially:

| R3 v2 Group | Impact Level | Rationale |
|-------------|:------------:|-----------|
| F: Pitch | LOW | Pitch novelty handled indirectly via D group |
| G: Rhythm | LOW-MEDIUM | Rhythmic deviations are a novelty source |
| H: Harmony | HIGH | `syntactic_irregularity` [86] is the single most important new feature for NDU -- harmonic syntax violations are a primary novelty signal in tonal music |
| I: Information | MEDIUM-HIGH | `prediction_error`, `surprise` map directly to NDU function |
| J: Dynamics | LOW | Dynamic novelty already captured via B group changes |
| K: Modulation | LOW | Slow modulation outside primary NDU timescales |

**Key feature**: R3 v2 index [86] `syntactic_irregularity` from the H:Harmony group is projected to become the highest-demand single feature across all NDU models, as harmonic syntax violation is one of the strongest known drivers of musical novelty perception.

### Projected v2 Demand

- v1 demand: ~400 tuples
- v2 additional: ~220 tuples (primarily H and I groups)
- Combined total: ~620 tuples

---

## 7. Architectural Notes

1. **SDD and EDNR are structural outliers.** While 7 of 9 NDU models use only ASA at H3/H6/H9, the two alpha-tier outliers (SDD, EDNR) consume 55% of the unit's total demand by incorporating PPC, TMH, and MEM mechanisms that span all four horizon bands. This bimodal demand structure -- compact core plus extended outliers -- is distinctive to NDU.

2. **ASA universality.** NDU is one of two units (alongside ASU) where ASA appears in every model. This reflects the tight coupling between auditory salience processing and novelty detection: a novel event must first be salient to be detected.

3. **L1 dominance.** Prediction (L1) is the primary law because novelty is defined as deviation from expectation. L0 (Memory) appears in EDNR's MEM mechanism for episodic comparison, and L2 (Integration) in SDD's TMH mechanism for structural context, but L1 carries the majority of tuple demand.

4. **Gamma compactness.** All three gamma models (SDDP, ONI, ECT) are strictly ASA-only with identical horizon profiles, producing compact output-layer summaries at ~30 tuples each.

---

## 8. Cross-References

### H3 Architecture
- [H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md) -- Definitive H3 specification
- [Bands/](../Bands/) -- Horizon band definitions (Micro, Meso, Macro, Ultra)
- [Laws/](../Laws/) -- Law specifications (L0, L1, L2)
- [Morphology/](../Morphology/) -- Morph definitions

### C3 Model Documentation
- [NDU Alpha Models](../../C3/Models/) -- MPG, SDD, EDNR model specifications
- [NDU Beta Models](../../C3/Models/) -- DSP_, CDMR, SLEE model specifications
- [NDU Gamma Models](../../C3/Models/) -- SDDP, ONI, ECT model specifications

### Related Demand Files
- [ASU-H3-DEMAND.md](ASU-H3-DEMAND.md) -- ASU demand (shares ASA-dominant pattern)
- [PCU-H3-DEMAND.md](PCU-H3-DEMAND.md) -- PCU demand (shares PPC mechanism with SDD)
- [00-INDEX.md](00-INDEX.md) -- Demand documentation index

### R3 Mappings
- [R3 Spectral Architecture](../../R3/) -- R3 feature definitions and domain groupings

---

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-02-13 | Initial NDU H3 demand specification |
