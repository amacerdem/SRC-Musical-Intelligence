# MPU H3 Demand Specification

**Version**: 2.0.0
**Updated**: 2026-02-13
**Unit**: Motor Planning Unit (MPU)
**Status**: Canonical demand specification for MPU models

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

The Motor Planning Unit (MPU) models the sensorimotor planning and execution processes involved in musical entrainment. Its 10 models span all three tiers (alpha, beta, gamma) and collectively consume an estimated **~500 H3 demand tuples** from the theoretical `(r3_idx, horizon, morph, law)` address space.

| Property | Value |
|----------|-------|
| Models | 10 (alpha: 3, beta: 4, gamma: 3) |
| Mechanisms | BEP (all 10 models) |
| Primary Band | Micro-Meso |
| Primary R3 Domains | B (Energy), D (Change) |
| Est. Total Tuples | ~500 |
| Primary Law | L1 (Prediction) |

MPU's primary law is **L1 (Prediction)** because motor planning is inherently predictive: the motor system must anticipate upcoming events to prepare timed actions. Beat prediction, anticipatory sequencing, and motor timing all operate in predictive mode.

---

## 2. Mechanism Summary

| Mechanism | Models Using | Horizons | Band Range | Role in MPU |
|-----------|:-----------:|----------|:----------:|-------------|
| BEP | 10 (all) | H6, H9, H11 | Micro-Meso | Beat-entrained prediction for motor timing |

MPU is the **most mechanistically uniform unit** in the entire C3 architecture. All 10 models use exactly one mechanism (BEP) at exactly three horizons (H6, H9, H11). This uniformity reflects the tight functional coupling between beat-entrained prediction and motor planning -- there is no motor planning without beat entrainment.

### BEP Horizon Rationale

| Horizon | Temporal Scale | Motor Function |
|---------|---------------|----------------|
| H6 | ~93 ms | Onset-level motor preparation, keystroke/tap timing |
| H9 | ~372 ms | Beat-level motor coordination, rhythmic entrainment |
| H11 | ~744 ms | Bar/measure-level motor sequencing, phrase-scale planning |

---

## 3. Per-Model Demand Table

| Model | Tier | Mechanisms | Horizons | Key R3 Features | Est. Tuples |
|-------|------|-----------|----------|-----------------|:-----------:|
| PEOM | alpha1 | BEP | H6, H9, H11 | B, D (onset, spectral_flux) | ~60 |
| MSR | alpha2 | BEP | H6, H9, H11 | B, D (onset, spectral_flux) | ~60 |
| GSSM | alpha3 | BEP | H6, H9, H11 | B, D, E (gait-stride motor) | ~60 |
| ASAP | beta1 | BEP | H6, H9, H11 | B, D (anticipatory sequencing) | ~50 |
| DDSMI | beta2 | BEP | H6, H9, H11 | B, D (dynamic motor integration) | ~50 |
| VRMSME | beta3 | BEP | H6, H9, H11 | B (motor rhythm) | ~40 |
| SPMC | beta4 | BEP | H6, H9, H11 | B, D (sensorimotor coupling) | ~50 |
| NSCP | gamma1 | BEP | H6, H9, H11 | B, E (neural-motor coupling) | ~40 |
| CTBB | gamma2 | BEP | H6, H9, H11 | B, D (cortical timing) | ~40 |
| STC | gamma3 | BEP | H6, H9, H11 | B, D (sensorimotor timing) | ~40 |

### Tier Distribution

- **Alpha tier** (PEOM, MSR, GSSM): ~180 tuples -- richest R3 feature consumption, broadest domain coverage
- **Beta tier** (ASAP, DDSMI, VRMSME, SPMC): ~190 tuples -- 4 models with focused B/D domain demand
- **Gamma tier** (NSCP, CTBB, STC): ~120 tuples -- compact output summaries for motor timing

---

## 4. Horizon Coverage

```
Micro   [H0-H7]:   H6(all 10)
Meso    [H8-H15]:  H9(all 10), H11(all 10)
Macro   [H16-H23]: (none)
Ultra   [H24-H31]: (none)
```

MPU has the **most compact horizon footprint** of any C3 unit -- only 3 horizons across 10 models. No MPU model touches Macro or Ultra bands. This reflects the motor system's focus on immediate-to-near temporal scales: onset preparation (H6), beat entrainment (H9), and measure-level sequencing (H11).

### Horizon Heatmap

| Horizon | H6 | H9 | H11 |
|---------|:--:|:--:|:---:|
| Models  | 10 | 10 |  10 |

All horizons are uniformly saturated -- every model uses every horizon.

---

## 5. R3 Feature Consumption

MPU draws primarily from the Energy (B) and Change (D) domains of R3:

| R3 Domain | Features Used | Primary Consumers |
|-----------|---------------|-------------------|
| A: Consonance | -- | (not consumed by MPU) |
| B: Energy | [7]-[11] (velocity, onset, spectral_flux) | All 10 models (core motor features) |
| C: Timbre | -- | (not consumed by MPU) |
| D: Change | [21]-[24] (spectral_change, flux derivatives) | 9 of 10 models (VRMSME excluded) |
| E: Interactions | [25]-[48] (cross-domain coupling) | GSSM, NSCP (gait and neural coupling) |

Domain B (Energy) is the universal consumption target -- every MPU model requires energy envelope features as the basis for motor entrainment. Domain D (Change) provides temporal derivative information critical for anticipatory motor timing. Domains A, C are not consumed; MPU is functionally specialized to energy-temporal features.

---

## 6. R3 v2 Expansion Impact

With the R3 v2 feature set (groups F through K), MPU demand expands significantly:

| R3 v2 Group | Impact Level | Rationale |
|-------------|:------------:|-----------|
| F: Pitch | LOW | Pitch is not a primary motor planning input |
| G: Rhythm | VERY HIGH | `syncopation`, `metricality`, `beat_strength`, `groove` -- MPU is the second-largest G group consumer after STU; rhythm features map directly to motor entrainment |
| H: Harmony | LOW | Harmonic structure not directly relevant to motor planning |
| I: Information | LOW-MEDIUM | `prediction_error` useful for motor error correction |
| J: Dynamics | MEDIUM | Dynamic envelope features relevant to motor velocity scaling |
| K: Modulation | MEDIUM | Locomotion band (0.5-2 Hz) aligns with walking/entrainment rhythms |

**Key expansion**: The G:Rhythm group transforms MPU demand. Features like `beat_strength`, `syncopation`, and `groove` provide explicit rhythmic structure that the motor system currently infers from raw energy features. MPU is projected to be the second-largest consumer of G group features after STU.

### Projected v2 Demand

- v1 demand: ~500 tuples
- v2 additional: ~350 tuples (primarily G group, secondarily J and K)
- Combined total: ~850 tuples

---

## 7. Architectural Notes

1. **Maximum uniformity.** MPU is the most uniform unit in C3: 10 models, 1 mechanism (BEP), 3 horizons (H6, H9, H11). No other unit approaches this level of structural regularity. This uniformity is architecturally significant -- it means MPU demand is entirely predictable and can be optimized as a single computation block.

2. **BEP exclusivity.** MPU is the primary consumer of BEP (Beat-Entrained Prediction). While BEP also appears in STU and as a secondary mechanism in RPU (SSRI), MPU is the only unit where BEP is the sole mechanism. This tight BEP-MPU coupling is a defining architectural feature.

3. **No Macro/Ultra presence.** MPU operates entirely within Micro-Meso bands. Motor planning does not require long-range temporal context -- it operates on onset, beat, and measure timescales. Structural and episodic temporal processing is delegated to IMU and PCU.

4. **Compact domain footprint.** With only B and D as primary R3 domains (plus limited E usage), MPU has the narrowest spectral consumption of any unit. It does not need consonance, timbre, or harmonic features -- only energy dynamics and temporal change.

5. **L1 saturation.** While all three laws (L0, L1, L2) appear in BEP tuples, L1 (Prediction) dominates because motor preparation requires forward temporal models. L0 (Memory) and L2 (Integration) serve supporting roles for motor habit formation and sensorimotor integration respectively.

---

## 8. Cross-References

### H3 Architecture
- [H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md) -- Definitive H3 specification
- [Bands/Micro/](../Bands/Micro/) -- Micro band definition (H0-H7)
- [Bands/Meso/](../Bands/Meso/) -- Meso band definition (H8-H15)
- [Laws/](../Laws/) -- Law specifications (L0, L1, L2)
- [Morphology/](../Morphology/) -- Morph definitions

### C3 Model Documentation
- [MPU Alpha Models](../../C3/Models/) -- PEOM, MSR, GSSM model specifications
- [MPU Beta Models](../../C3/Models/) -- ASAP, DDSMI, VRMSME, SPMC model specifications
- [MPU Gamma Models](../../C3/Models/) -- NSCP, CTBB, STC model specifications

### Related Demand Files
- [STU-H3-DEMAND.md](STU-H3-DEMAND.md) -- STU demand (shares BEP mechanism, broader horizon range)
- [RPU-H3-DEMAND.md](RPU-H3-DEMAND.md) -- RPU demand (SSRI uses BEP as secondary mechanism)
- [00-INDEX.md](00-INDEX.md) -- Demand documentation index

### R3 Mappings
- [R3 Spectral Architecture](../../R3/) -- R3 feature definitions and domain groupings

---

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-02-13 | Initial MPU H3 demand specification |
