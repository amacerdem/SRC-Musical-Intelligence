# NDU -- Novelty Detection Unit

| Property | Value |
|----------|-------|
| UNIT_NAME | NDU |
| FULL_NAME | Novelty Detection Unit |
| CIRCUIT | salience |
| POOLED_EFFECT | d = 0.55 |
| Evidence | Experimental-5 (k < 10 studies) |
| Dependency | Independent (Phase 2) |
| Total Output | 94D per frame |
| Model Count | 9 |

---

## Description

The NDU models how the brain detects deviations from expected auditory patterns -- mismatch negativity (MMN), spectral deviance, statistical learning violations, and error correction. Its primary neural regions are the bilateral temporal cortex and IFG.

---

## Model Roster

### Alpha (k >= 10, >90% confidence)

| # | Model ID | Full Name | OUTPUT_DIM | Mechanisms |
|---|----------|-----------|-----------|------------|
| 1 | MPG | Mismatch Prediction Gate | 12D | ASA |
| 2 | SDD | Spectral Deviance Detection | 11D | ASA, PPC |
| 3 | EDNR | Expectation-Dependent Novelty Response | 11D | ASA |

### Beta (5 <= k < 10, 70--90% confidence)

| # | Model ID | Full Name | OUTPUT_DIM | Mechanisms |
|---|----------|-----------|-----------|------------|
| 4 | DSP_ | Deviance Salience Processing | 10D | ASA |
| 5 | CDMR | Context-Dependent Mismatch Response | 10D | ASA, TMH |
| 6 | SLEE | Statistical Learning Expectation Engine | 10D | ASA, MEM |

### Gamma (k < 5, <70% confidence)

| # | Model ID | Full Name | OUTPUT_DIM | Mechanisms |
|---|----------|-----------|-----------|------------|
| 7 | SDDP | Sensory-Driven Deviance Processing | 10D | ASA |
| 8 | ONI | Oddball Novelty Index | 10D | ASA |
| 9 | ECT | Error Correction Trace | 10D | ASA |

**Total unit dimensionality: 12 + 11 + 11 + 10 + 10 + 10 + 10 + 10 + 10 = 94D**

---

## Mechanisms Used

| Mechanism | Circuit | Models Using It |
|-----------|---------|----------------|
| ASA (Auditory Scene Analysis) | salience | MPG, SDD, EDNR, DSP_, CDMR, SLEE, SDDP, ONI, ECT |
| PPC (Pitch Processing Chain) | perceptual | SDD |
| TMH (Temporal Memory Hierarchy) | sensorimotor | CDMR |
| MEM (Memory Encoding/Retrieval) | mnemonic | SLEE |

---

## Cross-Unit Pathways

NDU does not currently participate in any declared cross-unit pathways. It is neither a source nor a target.

---

## Code Reference

- Unit class: `mi_beta.brain.units.ndu._unit.NDUUnit`
- Models package: `mi_beta.brain.units.ndu.models`
- Unit directory: `mi_beta/brain/units/ndu/`

## Model Documentation

- [NDU-alpha1-MPG](../Models/NDU-α1-MPG/)
- [NDU-alpha2-SDD](../Models/NDU-α2-SDD/)
- [NDU-alpha3-EDNR](../Models/NDU-α3-EDNR/)
- [NDU-beta1-DSP](../Models/NDU-β1-DSP/)
- [NDU-beta2-CDMR](../Models/NDU-β2-CDMR/)
- [NDU-beta3-SLEE](../Models/NDU-β3-SLEE/)
- [NDU-gamma1-SDDP](../Models/NDU-γ1-SDDP/)
- [NDU-gamma2-ONI](../Models/NDU-γ2-ONI/)
- [NDU-gamma3-ECT](../Models/NDU-γ3-ECT/)
