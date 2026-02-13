# ARU -- Affective Resonance Unit

| Property | Value |
|----------|-------|
| UNIT_NAME | ARU |
| FULL_NAME | Affective Resonance Unit |
| CIRCUIT | mesolimbic |
| POOLED_EFFECT | d = 0.83 |
| Evidence | Core-4 (k >= 10 studies) |
| Dependency | **Dependent** (Phase 4) |
| Total Output | 120D per frame |
| Model Count | 10 |

---

## Description

The ARU models how the human brain generates and processes musical emotion, pleasure, and affective responses. Its primary neural regions are NAcc, VTA, and Amygdala. As a dependent unit, it receives cross-unit inputs from SPU, STU, and IMU via pathways P1, P5, and P3 respectively.

---

## Model Roster

### Alpha (k >= 10, >90% confidence)

| # | Model ID | Full Name | OUTPUT_DIM | Mechanisms |
|---|----------|-----------|-----------|------------|
| 1 | SRP | Striatal Reward Pathway | 19D | AED, CPD, C0P |
| 2 | AAC | Autonomic-Affective Coupling | 14D | AED, CPD, ASA |
| 3 | VMM | Valence-Mode Mapping | 12D | AED, C0P |

### Beta (5 <= k < 10, 70--90% confidence)

| # | Model ID | Full Name | OUTPUT_DIM | Mechanisms |
|---|----------|-----------|-----------|------------|
| 4 | PUPF | Pleasure-Uncertainty-Prediction | 12D | AED, CPD |
| 5 | CLAM | Cognitive-Load-Arousal Modulation | 11D | AED |
| 6 | MAD | Musical Anhedonia Disconnection | 11D | AED, CPD |
| 7 | NEMAC | Nostalgia-Enhanced Memory-Affect | 11D | AED, MEM |

### Gamma (k < 5, <70% confidence)

| # | Model ID | Full Name | OUTPUT_DIM | Mechanisms |
|---|----------|-----------|-----------|------------|
| 8 | DAP | Developmental Affective Plasticity | 10D | AED |
| 9 | CMAT | Cross-Modal Affective Transfer | 10D | AED |
| 10 | TAR | Therapeutic Affective Resonance | 10D | AED |

**Total unit dimensionality: 19 + 14 + 12 + 12 + 11 + 11 + 11 + 10 + 10 + 10 = 120D**

---

## Mechanisms Used

| Mechanism | Circuit | Models Using It |
|-----------|---------|----------------|
| AED (Affective Entrainment Dynamics) | mesolimbic | SRP, AAC, VMM, PUPF, CLAM, MAD, NEMAC, DAP, CMAT, TAR |
| CPD (Chills & Peak Detection) | mesolimbic | SRP, AAC, PUPF, MAD |
| C0P (Cognitive Projection) | mesolimbic | SRP, VMM |
| ASA (Auditory Scene Analysis) | salience | AAC |
| MEM (Memory Encoding/Retrieval) | mnemonic | NEMAC |

All 10 ARU models use the AED mechanism. The alpha models (SRP, AAC, VMM) use the most mechanisms, consistent with their higher evidence confidence.

---

## Cross-Unit Pathways

| Pathway | Direction | Source | Description |
|---------|-----------|--------|-------------|
| P1 | SPU -> ARU | SPU | Consonance -> pleasure (Bidelman 2009, r=0.81) |
| P3 | IMU -> ARU | IMU | Memory -> affect (Janata 2009, r=0.55) |
| P5 | STU -> ARU | STU | Tempo -> emotion (Juslin & Vastfjall 2008, r=0.60) |

ARU is the primary target of cross-unit pathways, receiving inputs from 3 of the 7 independent units.

---

## Code Reference

- Unit class: `mi_beta.brain.units.aru._unit.ARUUnit`
- Models package: `mi_beta.brain.units.aru.models`
- Unit directory: `mi_beta/brain/units/aru/`

## Model Documentation

- [ARU-alpha1-SRP](../Models/ARU-α1-SRP/)
- [ARU-alpha2-AAC](../Models/ARU-α2-AAC/)
- [ARU-alpha3-VMM](../Models/ARU-α3-VMM/)
- [ARU-beta1-PUPF](../Models/ARU-β1-PUPF/)
- [ARU-beta2-CLAM](../Models/ARU-β2-CLAM/)
- [ARU-beta3-MAD](../Models/ARU-β3-MAD/)
- [ARU-beta4-NEMAC](../Models/ARU-β4-NEMAC/)
- [ARU-gamma1-DAP](../Models/ARU-γ1-DAP/)
- [ARU-gamma2-CMAT](../Models/ARU-γ2-CMAT/)
- [ARU-gamma3-TAR](../Models/ARU-γ3-TAR/)
