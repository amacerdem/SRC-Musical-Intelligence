# ASU -- Auditory Salience Unit

| Property | Value |
|----------|-------|
| UNIT_NAME | ASU |
| FULL_NAME | Auditory Salience Unit |
| CIRCUIT | salience |
| POOLED_EFFECT | d = 0.60 |
| Evidence | Experimental-5 (k < 10 studies) |
| Dependency | Independent (Phase 2) |
| Total Output | 94D per frame |
| Model Count | 9 |

---

## Description

The ASU models how the brain detects and prioritises salient auditory events -- sudden onsets, spectral deviance, interaural differences, and bottom-up attention capture. Its primary neural regions are the anterior insula and ACC.

---

## Model Roster

### Alpha (k >= 10, >90% confidence)

| # | Model ID | Full Name | OUTPUT_DIM | Mechanisms |
|---|----------|-----------|-----------|------------|
| 1 | SNEM | Salience Network Engagement Model | 12D | ASA |
| 2 | IACM | Interaural Attention Capture Model | 11D | ASA |
| 3 | CSG | Cortical Salience Gating | 11D | ASA |

### Beta (5 <= k < 10, 70--90% confidence)

| # | Model ID | Full Name | OUTPUT_DIM | Mechanisms |
|---|----------|-----------|-----------|------------|
| 4 | BARM | Bottom-up Attention Reflex Model | 10D | ASA |
| 5 | STANM | Spectro-Temporal Attention Network Model | 10D | ASA |
| 6 | AACM | Auditory Attention Control Model | 10D | ASA |

### Gamma (k < 5, <70% confidence)

| # | Model ID | Full Name | OUTPUT_DIM | Mechanisms |
|---|----------|-----------|-----------|------------|
| 7 | PWSM | Pop-out Warning Salience Model | 10D | ASA |
| 8 | DGTP | Deviance-Gated Temporal Processing | 10D | ASA |
| 9 | SDL | Stimulus-Driven Listening | 10D | ASA |

**Total unit dimensionality: 12 + 11 + 11 + 10 + 10 + 10 + 10 + 10 + 10 = 94D**

---

## Mechanisms Used

| Mechanism | Circuit | Models Using It |
|-----------|---------|----------------|
| ASA (Auditory Scene Analysis) | salience | SNEM, IACM, CSG, BARM, STANM, AACM, PWSM, DGTP, SDL |

All 9 ASU models use the ASA mechanism exclusively.

---

## Cross-Unit Pathways

ASU does not currently participate in any declared cross-unit pathways. It is neither a source nor a target.

---

## Code Reference

- Unit class: `mi_beta.brain.units.asu._unit.ASUUnit`
- Models package: `mi_beta.brain.units.asu.models`
- Unit directory: `mi_beta/brain/units/asu/`

## Model Documentation

- [ASU-alpha1-SNEM](../Models/ASU-α1-SNEM/)
- [ASU-alpha2-IACM](../Models/ASU-α2-IACM/)
- [ASU-alpha3-CSG](../Models/ASU-α3-CSG/)
- [ASU-beta1-BARM](../Models/ASU-β1-BARM/)
- [ASU-beta2-STANM](../Models/ASU-β2-STANM/)
- [ASU-beta3-AACM](../Models/ASU-β3-AACM/)
- [ASU-gamma1-PWSM](../Models/ASU-γ1-PWSM/)
- [ASU-gamma2-DGTP](../Models/ASU-γ2-DGTP/)
- [ASU-gamma3-SDL](../Models/ASU-γ3-SDL/)
