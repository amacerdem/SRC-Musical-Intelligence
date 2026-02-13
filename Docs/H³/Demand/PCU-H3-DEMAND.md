# PCU H3 Demand Specification

**Version**: 2.0.0
**Updated**: 2026-02-13
**Unit**: Predictive Coding Unit (PCU)
**Status**: Canonical demand specification for PCU models

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

The Predictive Coding Unit (PCU) implements hierarchical predictive processing across spectral, temporal, and cross-modal domains. Its 10 models span all three tiers (alpha, beta, gamma) and collectively consume an estimated **~500 H3 demand tuples** from the theoretical `(r3_idx, horizon, morph, law)` address space.

| Property | Value |
|----------|-------|
| Models | 10 (alpha: 3, beta: 4, gamma: 3) |
| Mechanisms | PPC (4), TPC (3), MEM (3), AED (2), C0P (2), ASA (1) |
| Primary Band | All bands (Micro through Ultra) |
| Primary R3 Domains | A (Consonance), C (Timbre), E (Interactions) |
| Est. Total Tuples | ~500 |
| Primary Law | All three (L0, L1, L2) |

PCU is unique in employing **all three laws as primary** -- predictive coding inherently requires memory (L0) to maintain priors, prediction (L1) to generate expectations, and integration (L2) to compute prediction errors. No single law dominates.

---

## 2. Mechanism Summary

| Mechanism | Models Using | Horizons | Band Range | Role in PCU |
|-----------|:-----------:|----------|:----------:|-------------|
| PPC | 4 (HTP, SPH, ICEM, PWUP) | H0, H3, H6 | Micro | Hierarchical predictive comparison at fine timescales |
| TPC | 3 (HTP, UDP, MAA) | H6, H12, H16 | Micro-Macro | Temporal prediction across beat-to-section scales |
| MEM | 3 (HTP, ICEM, PSH) | H18, H20, H22, H25 | Macro-Ultra | Episodic memory for long-range predictive context |
| AED | 2 (WMED, CHPI) | H6, H16 | Micro+Macro | Affective-evaluative prediction error |
| C0P | 2 (PWUP, WMED) | H18, H19, H20 | Macro | Cross-modal coherence prediction |
| ASA | 1 (IGFE) | H3, H6, H9 | Micro-Meso | Salience-driven gestalt feature extraction |

PCU deploys **6 different mechanisms** -- the most diverse mechanism usage of any C3 unit. This diversity reflects the multi-level nature of predictive coding: fine-grained spectral prediction (PPC), temporal sequence prediction (TPC), long-range memory-based prediction (MEM), affective prediction error (AED), cross-modal coherence (C0P), and salience gating (ASA).

---

## 3. Per-Model Demand Table

| Model | Tier | Mechanisms | Horizons | Key R3 Features | Est. Tuples |
|-------|------|-----------|----------|-----------------|:-----------:|
| HTP | alpha1 | PPC, TPC, MEM | H0, H3, H6, H8, H12, H16 | A, B, C, D, E (full predictive hierarchy) | ~120 |
| SPH | alpha2 | PPC | H0, H3, H6 | A, C (pitch hierarchy) | ~60 |
| ICEM | alpha3 | PPC, MEM | H0, H3, H6, H18, H20, H22, H25 | A, B, E (inference, coupling) | ~100 |
| PWUP | beta1 | PPC, C0P | H0, H3, H6, H18, H19, H20 | A, E (predictive uncertainty) | ~80 |
| WMED | beta2 | AED, C0P | H6, H16, H18, H19, H20 | B, D, E (working memory prediction) | ~60 |
| UDP | beta3 | TPC | H6, H12, H16 | A, D, E (uncertainty prediction) | ~45 |
| CHPI | beta4 | PPC, TPC, AED | H0, H3, H6, H12, H16 | A, B, C, D, E (cross-modal harmonic) | ~80 |
| IGFE | gamma1 | ASA | H3, H6, H9 | C (gestalt feature) | ~30 |
| MAA | gamma2 | TPC | H6, H12, H16 | A, B, C, E (multi-attribute) | ~40 |
| PSH | gamma3 | MEM | H18, H20, H22 | A, C, E (spectral hierarchy) | ~40 |

### Tier Distribution

- **Alpha tier** (HTP, SPH, ICEM): ~280 tuples -- 56% of total demand; HTP alone accounts for ~120 tuples with the richest multi-mechanism demand
- **Beta tier** (PWUP, WMED, UDP, CHPI): ~265 tuples -- diverse mechanism combinations including C0P and AED
- **Gamma tier** (IGFE, MAA, PSH): ~110 tuples -- each gamma model uses exactly one mechanism for focused output

### HTP Demand Detail

HTP (alpha1) has the **most detailed declared demand of any C3 model**, with 18 explicit tuples in its code-level `h3_demand` declaration. It is the only model in PCU that uses three mechanisms simultaneously (PPC + TPC + MEM), spanning Micro through Macro bands.

---

## 4. Horizon Coverage

```
Micro   [H0-H7]:   H0(HTP,SPH,ICEM,PWUP,CHPI), H3(HTP,SPH,ICEM,PWUP,IGFE,CHPI),
                    H6(all 10)
Meso    [H8-H15]:  H8(HTP), H9(IGFE), H12(HTP,UDP,MAA,CHPI)
Macro   [H16-H23]: H16(HTP,WMED,UDP,MAA,CHPI), H18(ICEM,PWUP,WMED,PSH),
                    H19(PWUP,WMED), H20(ICEM,PWUP,WMED,PSH), H22(ICEM,PSH)
Ultra   [H24-H31]: H25(ICEM)
```

PCU spans the **full horizon range** from H0 to H25, one of only three units (alongside IMU and STU) to reach Ultra band. H6 is the universal horizon used by all 10 models.

### Horizon Heatmap

| Horizon | H0 | H3 | H6 | H8 | H9 | H12 | H16 | H18 | H19 | H20 | H22 | H25 |
|---------|:--:|:--:|:--:|:--:|:--:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Models  |  5 |  6 | 10 |  1 |  1 |  4  |  5  |  4  |  2  |  4  |  2  |  1  |

The bimodal distribution is evident: a Micro cluster (H0-H6, heavily populated) and a Macro cluster (H16-H22, moderately populated), with sparse Meso coverage in between.

---

## 5. R3 Feature Consumption

PCU has broad R3 consumption spanning all five v1 domains:

| R3 Domain | Features Used | Primary Consumers |
|-----------|---------------|-------------------|
| A: Consonance | [0]-[6] (interval, roughness, tonalness) | HTP, SPH, ICEM, PWUP, UDP, CHPI, MAA, PSH (8 of 10) |
| B: Energy | [7]-[11] (velocity, onset, loudness) | HTP, ICEM, WMED, CHPI, MAA (5 of 10) |
| C: Timbre | [12]-[20] (spectral shape, brightness) | HTP, SPH, CHPI, IGFE, MAA, PSH (6 of 10) |
| D: Change | [21]-[24] (spectral_flux, temporal derivatives) | HTP, WMED, UDP, CHPI (4 of 10) |
| E: Interactions | [25]-[48] (cross-domain coupling) | HTP, ICEM, PWUP, WMED, UDP, CHPI, MAA, PSH (8 of 10) |

Domains A (Consonance) and E (Interactions) are the most broadly consumed, appearing in 8 of 10 models. This reflects PCU's role as a hierarchical prediction engine that must model both spectral structure (A) and cross-domain dependencies (E).

---

## 6. R3 v2 Expansion Impact

With the R3 v2 feature set (groups F through K), PCU demand expands significantly:

| R3 v2 Group | Impact Level | Rationale |
|-------------|:------------:|-----------|
| F: Pitch | MEDIUM | `pitch_salience`, `pitch_class_entropy` relevant for pitch prediction hierarchy |
| G: Rhythm | LOW-MEDIUM | Rhythmic prediction handled primarily by STU/MPU |
| H: Harmony | MEDIUM-HIGH | `key_clarity`, `tonnetz_distance`, `chord_complexity` -- harmonic prediction is core PCU function |
| I: Information | HIGH | `prediction_error`, `surprise`, `predictive_entropy` -- these features are definitionally central to predictive coding |
| J: Dynamics | LOW | Dynamic prediction handled by energy domain |
| K: Modulation | LOW | Slow modulation outside primary PCU focus |

**Key expansion**: The I:Information group maps almost exactly to PCU's computational function. Features like `prediction_error` and `predictive_entropy` provide explicit information-theoretic measures that PCU currently computes implicitly from R3 v1 features. The H:Harmony group adds structured harmonic features (`key_clarity`, `tonnetz_distance`) that enrich the pitch prediction hierarchy.

### Projected v2 Demand

- v1 demand: ~500 tuples
- v2 additional: ~300 tuples (primarily I and H groups)
- Combined total: ~800 tuples

---

## 7. Architectural Notes

1. **Most diverse mechanism usage.** PCU uses 6 of the 10 available mechanisms -- more than any other C3 unit. This diversity is not accidental; predictive coding operates at multiple levels of abstraction, each requiring a different temporal processing mechanism.

2. **HTP as anchor model.** HTP (alpha1) functions as PCU's anchor model, consuming ~24% of the unit's total demand with 3 mechanisms across 6 horizons. It is the only model in C3 with 18 explicitly declared H3 demand tuples in code.

3. **Bimodal horizon distribution.** PCU demand clusters in two bands: Micro (H0-H6) for fine-grained spectral prediction, and Macro (H16-H22) for structural prediction. The Meso band is sparsely populated, reflecting a gap between onset-level and section-level predictive processing.

4. **All three laws active.** Unlike most units where one law dominates, PCU distributes demand roughly evenly across L0 (maintaining predictive priors), L1 (generating predictions), and L2 (computing prediction errors). This three-law balance is unique to PCU.

5. **Gamma specialization.** Each gamma model uses exactly one mechanism: IGFE uses ASA, MAA uses TPC, PSH uses MEM. This clean separation produces focused output-layer projections for gestalt features, multi-attribute aggregation, and spectral hierarchy respectively.

---

## 8. Cross-References

### H3 Architecture
- [H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md) -- Definitive H3 specification
- [Bands/](../Bands/) -- Horizon band definitions (Micro, Meso, Macro, Ultra)
- [Laws/](../Laws/) -- Law specifications (L0, L1, L2)
- [Morphology/](../Morphology/) -- Morph definitions

### C3 Model Documentation
- [PCU Alpha Models](../../C3/Models/) -- HTP, SPH, ICEM model specifications
- [PCU Beta Models](../../C3/Models/) -- PWUP, WMED, UDP, CHPI model specifications
- [PCU Gamma Models](../../C3/Models/) -- IGFE, MAA, PSH model specifications

### Related Demand Files
- [NDU-H3-DEMAND.md](NDU-H3-DEMAND.md) -- NDU demand (SDD shares PPC mechanism)
- [SPU-H3-DEMAND.md](SPU-H3-DEMAND.md) -- SPU demand (shares PPC/TPC mechanisms)
- [IMU-H3-DEMAND.md](IMU-H3-DEMAND.md) -- IMU demand (shares MEM mechanism)
- [ARU-H3-DEMAND.md](ARU-H3-DEMAND.md) -- ARU demand (shares AED, C0P mechanisms)
- [00-INDEX.md](00-INDEX.md) -- Demand documentation index

### R3 Mappings
- [R3 Spectral Architecture](../../R3/) -- R3 feature definitions and domain groupings

---

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-02-13 | Initial PCU H3 demand specification |
