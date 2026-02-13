# ARU H3 Demand Specification

**Version**: 2.0.0
**Updated**: 2026-02-13
**Unit**: Affective Resonance Unit (ARU)
**Status**: Canonical demand specification for ARU models

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

The Affective Resonance Unit (ARU) models the emotional and affective dimensions of music perception. Its 10 models span all three tiers (alpha, beta, gamma) and collectively consume an estimated **~500 H3 demand tuples** from the theoretical `(r3_idx, horizon, morph, law)` address space.

| Property | Value |
|----------|-------|
| Models | 10 (alpha: 3, beta: 4, gamma: 3) |
| Mechanisms | AED (10), CPD (4), C0P (2), ASA (1), MEM (1) |
| Primary Band | Micro-Macro |
| Primary R3 Domains | All groups via cross-unit pathways (P1, P3, P5) |
| Est. Total Tuples | ~500 |
| Primary Law | L2 (Integration) |

ARU's primary law is **L2 (Integration)** because affective resonance is fundamentally bidirectional: emotion arises from the integration of bottom-up sensory signals with top-down expectation and appraisal. The integration law captures this bidirectional coupling.

**Important**: ARU is a **dependent unit** -- it does not consume R3 features directly from the spectral pipeline. Instead, it receives pre-processed R3 signals through routed pathways from SPU (P1), IMU (P3), and STU (P5). This pathway dependency is a critical architectural distinction.

---

## 2. Mechanism Summary

| Mechanism | Models Using | Horizons | Band Range | Role in ARU |
|-----------|:-----------:|----------|:----------:|-------------|
| AED | 10 (all) | H6, H16 | Micro+Macro | Affective evaluation at dual timescales |
| CPD | 4 (SRP, AAC, VMM, -- see note) | H9, H16, H18 | Meso-Macro | Cross-prediction for affective disambiguation |
| C0P | 2 (PUPF, NEMAC) | H18, H19, H20 | Macro | Cross-modal coherence for predictive affect |
| ASA | 1 (CMAT) | H3, H6, H9 | Micro-Meso | Salience-driven attention for affective tagging |
| MEM | 1 (SRP) | H18, H20, H22 | Macro | Episodic memory for affective association |

AED (Affective-Evaluative Detection) is the **dominant mechanism**, appearing in all 10 models. Its bimodal horizon profile (H6 + H16) captures both immediate affective response (Micro) and structural emotional arc (Macro). CPD adds cross-prediction capacity to the alpha models, while C0P and ASA serve specialized roles in beta and gamma tiers.

---

## 3. Per-Model Demand Table

| Model | Tier | Mechanisms | Horizons | Key R3 Features | Est. Tuples |
|-------|------|-----------|----------|-----------------|:-----------:|
| SRP | alpha1 | AED, CPD, MEM | H6, H9, H16, H18, H20, H22 | A, B, C, D, E via pathways | ~80 |
| AAC | alpha2 | AED, CPD | H6, H9, H16, H18 | A, B, C, D, E via pathways | ~60 |
| VMM | alpha3 | AED, CPD | H6, H9, H16, H18 | A, B, C, E via pathways | ~60 |
| PUPF | beta1 | AED, C0P | H6, H16, H18, H19, H20 | A, B, D, E + I(predictive_entropy) | ~60 |
| CLAM | beta2 | AED | H6, H16 | B, D | ~30 |
| MAD | beta3 | AED | H6, H16 | A, B, C, E via pathways | ~30 |
| NEMAC | beta4 | AED, C0P | H6, H16, H18, H19, H20 | A, B, C, E via pathways | ~50 |
| DAP | gamma1 | AED | H6, H16 | A, B | ~25 |
| CMAT | gamma2 | AED, ASA | H3, H6, H9, H16 | B, C, E via pathways | ~40 |
| TAR | gamma3 | AED | H6, H16 | B, C | ~25 |

### Tier Distribution

- **Alpha tier** (SRP, AAC, VMM): ~200 tuples -- richest demand, all three use CPD for cross-prediction; SRP adds MEM for episodic affective memory
- **Beta tier** (PUPF, CLAM, MAD, NEMAC): ~170 tuples -- split between AED-only models (CLAM, MAD) and C0P-augmented models (PUPF, NEMAC)
- **Gamma tier** (DAP, CMAT, TAR): ~90 tuples -- compact output projections; CMAT is the only gamma model with a secondary mechanism (ASA)

---

## 4. Horizon Coverage

```
Micro   [H0-H7]:   H3(CMAT), H6(all 10)
Meso    [H8-H15]:  H9(SRP,AAC,VMM,CMAT)
Macro   [H16-H23]: H16(all 10), H18(SRP,AAC,VMM,PUPF,NEMAC),
                    H19(PUPF,NEMAC), H20(SRP,PUPF,NEMAC), H22(SRP)
Ultra   [H24-H31]: (none)
```

ARU has a characteristic **bimodal** horizon distribution anchored at H6 (Micro) and H16 (Macro), reflecting the dual-timescale nature of affective processing: immediate emotional response and longer-term emotional arc.

### Horizon Heatmap

| Horizon | H3 | H6 | H9 | H16 | H18 | H19 | H20 | H22 |
|---------|:--:|:--:|:--:|:---:|:---:|:---:|:---:|:---:|
| Models  |  1 | 10 |  4 |  10 |  5  |  2  |  3  |  1  |

The H6 and H16 columns are fully saturated (all 10 models), confirming AED's universal bimodal footprint as the structural backbone of ARU demand.

---

## 5. R3 Feature Consumption

ARU's R3 consumption is mediated through cross-unit pathways rather than direct spectral access:

| Pathway | Source Unit | R3 Domains Routed | Consuming Models |
|---------|------------|-------------------|------------------|
| P1 | SPU (Spectral Processing) | A (Consonance), C (Timbre) | SRP, AAC, VMM, MAD, NEMAC, DAP, TAR |
| P3 | IMU (Integrative Memory) | E (Interactions) | SRP, AAC, VMM, PUPF, NEMAC, CMAT |
| P5 | STU (Sensorimotor Timing) | B (Energy), D (Change) | All 10 models |

| R3 Domain | Via Pathway | Primary Consumers |
|-----------|:----------:|-------------------|
| A: Consonance | P1 (SPU) | SRP, AAC, VMM, PUPF, MAD, DAP (6 of 10) |
| B: Energy | P5 (STU) | All 10 models |
| C: Timbre | P1 (SPU) | SRP, AAC, VMM, MAD, NEMAC, CMAT, TAR (7 of 10) |
| D: Change | P5 (STU) | SRP, AAC, PUPF, CLAM (4 of 10) |
| E: Interactions | P3 (IMU) | SRP, AAC, VMM, PUPF, NEMAC, CMAT (6 of 10) |

**PUPF exception**: PUPF is the only ARU model with **direct I:Information demand** (specifically `predictive_entropy`), bypassing the standard pathway routing. This reflects its specialized role in predictive uncertainty processing for affect.

---

## 6. R3 v2 Expansion Impact

With the R3 v2 feature set (groups F through K), ARU demand expansion is largely **automatic** via pathway routing:

| R3 v2 Group | Impact Level | Rationale |
|-------------|:------------:|-----------|
| F: Pitch | LOW-MEDIUM | Routed via P1 (SPU); pitch features indirectly relevant to affect |
| G: Rhythm | MEDIUM | Routed via P5 (STU); groove and metricality influence affective response |
| H: Harmony | MEDIUM | Routed via P1 (SPU); harmonic tension/resolution drives emotional arc |
| I: Information | LOW (except PUPF) | Only PUPF has direct I demand; other models receive information features indirectly |
| J: Dynamics | MEDIUM | Routed via P5 (STU); dynamic contour shapes emotional trajectory |
| K: Modulation | LOW | Slow modulation outside primary affective timescales |

**Key architectural point**: Because ARU is a dependent unit receiving R3 through pathways, most v2 expansion happens automatically as source units (SPU, IMU, STU) expand their own R3 consumption. ARU itself does not need to declare new direct demands for most v2 features.

### Projected v2 Demand

- v1 demand: ~500 tuples
- v2 additional: ~150 tuples (primarily via automatic pathway expansion; ~30 direct from PUPF I:Information)
- Combined total: ~650 tuples

---

## 7. Architectural Notes

1. **AED universality with bimodal horizon.** All 10 ARU models use AED at H6 and H16, creating a structural bimodal pattern unique to this unit. The Micro horizon (H6) captures immediate affective valence, while the Macro horizon (H16) captures emotional arc over musical sections.

2. **Dependent unit architecture.** ARU does not access R3 directly. It receives routed signals through pathways P1 (from SPU), P3 (from IMU), and P5 (from STU). This dependency means ARU's effective R3 consumption is a function of upstream unit processing, not direct spectral features.

3. **PUPF as direct-demand exception.** Among ARU's 10 models, only PUPF declares direct demand for I:Information group features (`predictive_entropy`). This makes PUPF architecturally distinct -- it bridges the pathway-mediated pattern with direct R3 access.

4. **CPD concentration in alpha tier.** All three alpha models use CPD (Cross-Prediction Detection), but no beta or gamma model does. This tier-stratified mechanism usage reflects the alpha tier's role in detailed affective disambiguation through cross-prediction.

5. **L2 dominance reflects bidirectional processing.** Integration (L2) is the primary law because affective response requires combining sensory evidence with appraisal, expectation, and memory. L0 (Memory) supports SRP's episodic affective associations, while L1 (Prediction) supports PUPF/NEMAC's predictive affect.

---

## 8. Cross-References

### H3 Architecture
- [H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md) -- Definitive H3 specification
- [Bands/](../Bands/) -- Horizon band definitions (Micro, Meso, Macro, Ultra)
- [Laws/](../Laws/) -- Law specifications (L0, L1, L2)
- [Morphology/](../Morphology/) -- Morph definitions

### C3 Model Documentation
- [ARU Alpha Models](../../C3/Models/) -- SRP, AAC, VMM model specifications
- [ARU Beta Models](../../C3/Models/) -- PUPF, CLAM, MAD, NEMAC model specifications
- [ARU Gamma Models](../../C3/Models/) -- DAP, CMAT, TAR model specifications

### Pathway Dependencies
- [SPU-H3-DEMAND.md](SPU-H3-DEMAND.md) -- SPU demand (source for P1 pathway)
- [IMU-H3-DEMAND.md](IMU-H3-DEMAND.md) -- IMU demand (source for P3 pathway)
- [STU-H3-DEMAND.md](STU-H3-DEMAND.md) -- STU demand (source for P5 pathway)

### Related Demand Files
- [RPU-H3-DEMAND.md](RPU-H3-DEMAND.md) -- RPU demand (downstream consumer of ARU output)
- [00-INDEX.md](00-INDEX.md) -- Demand documentation index

### R3 Mappings
- [R3 Spectral Architecture](../../R3/) -- R3 feature definitions and domain groupings

---

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-02-13 | Initial ARU H3 demand specification |
