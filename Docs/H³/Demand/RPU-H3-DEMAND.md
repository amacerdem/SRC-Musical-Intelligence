# RPU H3 Demand Specification

**Version**: 2.0.0
**Updated**: 2026-02-13
**Unit**: Reward Processing Unit (RPU)
**Status**: Canonical demand specification for RPU models

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

The Reward Processing Unit (RPU) models the dopaminergic reward circuitry underlying musical pleasure, anticipation, and consummation. Its 10 models span all three tiers (alpha, beta, gamma) and collectively consume an estimated **~400 H3 demand tuples** from the theoretical `(r3_idx, horizon, morph, law)` address space.

| Property | Value |
|----------|-------|
| Models | 10 (alpha: 3, beta: 4, gamma: 3) |
| Mechanisms | AED (6), CPD (2), C0P (2), TMH (1), MEM (1), BEP (1), ASA (1) |
| Primary Band | All bands (Micro through Ultra) |
| Primary R3 Domains | A (Consonance), B (Energy), E (Interactions) |
| Est. Total Tuples | ~400 |
| Primary Law | Mixed (all three) |

RPU's law distribution is **mixed across all three** because reward processing spans the full temporal arc of musical experience: anticipation (L1/Prediction), consummation (L0/Memory via comparison to stored reward templates), and the integration of anticipatory and consummatory signals (L2/Integration).

**Important**: RPU is a **dependent unit** receiving routed signals from ARU and SPU. Its R3 consumption is partially mediated through these upstream pathways.

---

## 2. Mechanism Summary

| Mechanism | Models Using | Horizons | Band Range | Role in RPU |
|-----------|:-----------:|----------|:----------:|-------------|
| AED | 6 (DAED, MORMR, RPEM, IUCP, MCCN, MEAMR) | H6, H16 | Micro+Macro | Affective-evaluative reward detection |
| CPD | 2 (MORMR, IUCP) | H9, H16, H18 | Meso-Macro | Cross-prediction for reward disambiguation |
| C0P | 2 (MCCN, SSPS) | H18, H19, H20 | Macro | Cross-modal coherence for reward integration |
| TMH | 1 (RPEM) | H16, H18, H20, H22 | Macro | Long-range temporal memory for reward history |
| MEM | 1 (LDAC) | H18, H20, H22 | Macro | Episodic memory for reward association |
| BEP | 1 (SSRI) | H6, H9, H11 | Micro-Meso | Beat-entrained reward prediction |
| ASA | 1 (SSPS) | H3, H6, H9 | Micro-Meso | Salience-driven reward attention |

RPU deploys **7 different mechanisms** -- the most diverse mechanism set of any C3 unit, exceeding even PCU's 6 mechanisms. This breadth reflects the multi-faceted nature of musical reward: it involves affective evaluation (AED), cross-prediction (CPD), coherence monitoring (C0P), temporal memory (TMH, MEM), motor entrainment (BEP), and salience gating (ASA).

---

## 3. Per-Model Demand Table

| Model | Tier | Mechanisms | Horizons | Key R3 Features | Est. Tuples |
|-------|------|-----------|----------|-----------------|:-----------:|
| DAED | alpha1 | AED | H6, H16 | A, B, D, E | ~30 |
| MORMR | alpha2 | AED, CPD | H6, H9, H16, H18 | A, B, C, E | ~60 |
| RPEM | alpha3 | AED, TMH | H6, H16, H18, H20, H22 | A, B, D, E | ~80 |
| IUCP | beta1 | AED, CPD | H6, H9, H16, H18 | A, D, E | ~60 |
| MCCN | beta2 | AED, C0P | H6, H16, H18, H19, H20 | A, B, C, E | ~60 |
| MEAMR | beta3 | AED | H6, H16 | A, B, C, E | ~30 |
| SSRI | beta4 | AED, BEP | H6, H9, H11, H16 | A, B, C, D, E | ~50 |
| LDAC | gamma1 | AED, MEM | H6, H16, H18, H20, H22 | A, B, C, E | ~50 |
| IOTMS | gamma2 | AED | H6, H16 | B, D | ~25 |
| SSPS | gamma3 | AED, ASA, C0P | H3, H6, H9, H16, H18, H19, H20 | A, B, C, E | ~60 |

### Tier Distribution

- **Alpha tier** (DAED, MORMR, RPEM): ~170 tuples -- RPEM dominates with TMH providing long-range reward temporal history
- **Beta tier** (IUCP, MCCN, MEAMR, SSRI): ~200 tuples -- most diverse mechanism combinations; SSRI uniquely includes BEP for beat-entrained reward
- **Gamma tier** (LDAC, IOTMS, SSPS): ~135 tuples -- SSPS is the most mechanism-rich gamma model in RPU (3 mechanisms)

### Notable Model: SSPS

SSPS (gamma3) is unusual for a gamma-tier model: it uses 3 mechanisms (AED + ASA + C0P) across 7 horizons, making it the most complex gamma model in RPU. Its combined Micro-Meso (ASA) and Macro (C0P) coverage enables salience-to-coherence reward integration.

---

## 4. Horizon Coverage

```
Micro   [H0-H7]:   H3(SSPS), H6(all 10)
Meso    [H8-H15]:  H9(MORMR,IUCP,SSRI,SSPS), H11(SSRI)
Macro   [H16-H23]: H16(all 10), H18(MORMR,RPEM,IUCP,MCCN,LDAC,SSPS),
                    H19(MCCN,SSPS), H20(RPEM,MCCN,LDAC,SSPS), H22(RPEM,LDAC)
Ultra   [H24-H31]: (none)
```

Like ARU, RPU has a **bimodal** horizon distribution anchored at H6 (Micro) and H16 (Macro), reflecting the dual-timescale nature of reward processing: immediate reward response and longer-term reward trajectory.

### Horizon Heatmap

| Horizon | H3 | H6 | H9 | H11 | H16 | H18 | H19 | H20 | H22 |
|---------|:--:|:--:|:--:|:---:|:---:|:---:|:---:|:---:|:---:|
| Models  |  1 | 10 |  4 |  1  |  10 |  6  |  2  |  4  |  2  |

H6 and H16 are fully saturated (all 10 models), confirming AED's universal bimodal presence. The Macro tail (H18-H22) is populated by models with TMH, MEM, and C0P mechanisms.

---

## 5. R3 Feature Consumption

RPU has broad R3 consumption, with Consonance (A), Energy (B), and Interactions (E) as primary domains:

| R3 Domain | Features Used | Primary Consumers |
|-----------|---------------|-------------------|
| A: Consonance | [0]-[6] (interval, roughness, tonalness) | DAED, MORMR, RPEM, IUCP, MCCN, MEAMR, LDAC, SSPS (8 of 10) |
| B: Energy | [7]-[11] (velocity, onset, loudness) | DAED, MORMR, RPEM, MCCN, MEAMR, SSRI, LDAC, IOTMS, SSPS (9 of 10) |
| C: Timbre | [12]-[20] (spectral shape, brightness) | MORMR, MCCN, MEAMR, SSRI, LDAC, SSPS (6 of 10) |
| D: Change | [21]-[24] (spectral_flux, temporal derivatives) | DAED, RPEM, IUCP, SSRI, IOTMS (5 of 10) |
| E: Interactions | [25]-[48] (cross-domain coupling) | DAED, MORMR, RPEM, IUCP, MCCN, MEAMR, SSRI, LDAC, SSPS (9 of 10) |

Domains B (Energy) and E (Interactions) are the most broadly consumed (9 of 10 models each). Domain A (Consonance) follows closely (8 of 10). This broad consumption reflects RPU's integrative role -- musical reward draws on nearly all spectral dimensions.

---

## 6. R3 v2 Expansion Impact

With the R3 v2 feature set (groups F through K), RPU demand expands substantially:

| R3 v2 Group | Impact Level | Rationale |
|-------------|:------------:|-----------|
| F: Pitch | LOW-MEDIUM | Pitch resolution contributes to consonance reward |
| G: Rhythm | MEDIUM | `groove`, `syncopation` are direct reward drivers via motor entrainment (SSRI) |
| H: Harmony | MEDIUM | Harmonic tension/resolution is a primary reward mechanism in tonal music |
| I: Information | VERY HIGH | RPU is the **largest I group consumer** -- 6 of 10 models have direct I:Information demand; `prediction_error`, `surprise`, `predictive_entropy` map directly to reward prediction error |
| J: Dynamics | LOW-MEDIUM | Dynamic contour contributes to reward trajectory |
| K: Modulation | LOW | Slow modulation outside primary reward timescales |

**Key expansion**: RPU is projected to be the **single largest consumer of I:Information group features** across all C3 units. Six of its 10 models (DAED, RPEM, IUCP, MCCN, SSRI, SSPS) have direct demand for information-theoretic features. This is architecturally significant -- musical reward is fundamentally an information-theoretic phenomenon (reward = resolved uncertainty), and the I group provides the explicit features to model this.

### Projected v2 Demand

- v1 demand: ~400 tuples
- v2 additional: ~280 tuples (primarily I group, secondarily G and H)
- Combined total: ~680 tuples

---

## 7. Architectural Notes

1. **Most diverse mechanism set.** RPU uses 7 of the 10 available mechanisms -- the broadest coverage of any C3 unit. This exceeds PCU (6 mechanisms) and reflects the multi-faceted nature of musical reward, which integrates affective, predictive, temporal, motor, and salience-based signals.

2. **AED as backbone, not sole mechanism.** While AED appears in all 10 models (as in ARU), RPU's secondary mechanisms are far more varied. This contrasts with ARU where CPD is the dominant secondary mechanism; RPU distributes secondary demand across CPD, C0P, TMH, MEM, BEP, and ASA.

3. **Dependent unit with partial direct access.** RPU receives routed signals from ARU and SPU, but also maintains direct R3 consumption for specific features. This hybrid dependency pattern distinguishes RPU from ARU (fully pathway-dependent) and PCU (fully direct).

4. **SSRI as BEP bridge.** SSRI (beta4) is the only RPU model using BEP, creating a unique bridge between motor entrainment and reward processing. Its horizon profile (H6, H9, H11, H16) combines BEP's Micro-Meso range with AED's Macro anchor, enabling beat-synchronized reward signals.

5. **I:Information as largest v2 consumer.** With 6 of 10 models demanding I group features, RPU will undergo the largest information-theoretic expansion of any unit. This positions RPU as the primary computational locus for the relationship between musical information content and reward.

6. **Mixed law distribution.** Unlike units with a dominant law, RPU distributes demand roughly evenly: L1 (Prediction) for anticipatory reward, L0 (Memory) for reward template comparison, L2 (Integration) for combining anticipation with consummation. This reflects the well-documented distinction between "wanting" (anticipatory/L1) and "liking" (consummatory/L0+L2) in reward neuroscience.

---

## 8. Cross-References

### H3 Architecture
- [H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md) -- Definitive H3 specification
- [Bands/](../Bands/) -- Horizon band definitions (Micro, Meso, Macro, Ultra)
- [Laws/](../Laws/) -- Law specifications (L0, L1, L2)
- [Morphology/](../Morphology/) -- Morph definitions

### C3 Model Documentation
- [RPU Alpha Models](../../C3/Models/) -- DAED, MORMR, RPEM model specifications
- [RPU Beta Models](../../C3/Models/) -- IUCP, MCCN, MEAMR, SSRI model specifications
- [RPU Gamma Models](../../C3/Models/) -- LDAC, IOTMS, SSPS model specifications

### Upstream Dependencies
- [ARU-H3-DEMAND.md](ARU-H3-DEMAND.md) -- ARU demand (upstream signal source for RPU)
- [SPU-H3-DEMAND.md](SPU-H3-DEMAND.md) -- SPU demand (upstream signal source for RPU)

### Related Demand Files
- [PCU-H3-DEMAND.md](PCU-H3-DEMAND.md) -- PCU demand (second-most mechanism-diverse unit)
- [MPU-H3-DEMAND.md](MPU-H3-DEMAND.md) -- MPU demand (BEP shared via SSRI)
- [NDU-H3-DEMAND.md](NDU-H3-DEMAND.md) -- NDU demand (ASA shared via SSPS)
- [00-INDEX.md](00-INDEX.md) -- Demand documentation index

### R3 Mappings
- [R3 Spectral Architecture](../../R3/) -- R3 feature definitions and domain groupings

---

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-02-13 | Initial RPU H3 demand specification |
