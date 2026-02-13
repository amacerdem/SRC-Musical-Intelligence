# MPU -- Motor Planning Unit

| Property | Value |
|----------|-------|
| UNIT_NAME | MPU |
| FULL_NAME | Motor Planning Unit |
| CIRCUIT | sensorimotor |
| POOLED_EFFECT | d = 0.62 |
| Evidence | Experimental-5 (k < 10 studies) |
| Dependency | Independent (Phase 2) |
| Total Output | 104D per frame |
| Model Count | 10 |

---

## Description

The MPU models how the brain plans and executes motor sequences during musical performance -- predictive error optimisation, groove states, dual-stream integration, and sensorimotor calibration. Its primary neural regions are premotor cortex, cerebellum, and basal ganglia.

---

## Model Roster

### Alpha (k >= 10, >90% confidence)

| # | Model ID | Full Name | OUTPUT_DIM | Mechanisms |
|---|----------|-----------|-----------|------------|
| 1 | PEOM | Predictive Error Optimization Model | 12D | BEP |
| 2 | MSR | Motor Sequence Representation | 11D | BEP |
| 3 | GSSM | Groove-State Sensorimotor Model | 11D | BEP |

### Beta (5 <= k < 10, 70--90% confidence)

| # | Model ID | Full Name | OUTPUT_DIM | Mechanisms |
|---|----------|-----------|-----------|------------|
| 4 | ASAP | Anticipatory Sequence Action Planning | 10D | BEP |
| 5 | DDSMI | Dynamic Dual-Stream Motor Integration | 10D | BEP |
| 6 | VRMSME | VR Motor Skill Music Enhancement | 10D | BEP |
| 7 | SPMC | Sensory-Predictive Motor Coupling | 10D | BEP |

### Gamma (k < 5, <70% confidence)

| # | Model ID | Full Name | OUTPUT_DIM | Mechanisms |
|---|----------|-----------|-----------|------------|
| 8 | NSCP | Neural Substrate Choreographic Planning | 10D | BEP |
| 9 | CTBB | Cerebello-Thalamic Beat Binding | 10D | BEP |
| 10 | STC | Sensorimotor Timing Calibration | 10D | BEP |

**Total unit dimensionality: 12 + 11 + 11 + 10 + 10 + 10 + 10 + 10 + 10 + 10 = 104D**

---

## Mechanisms Used

| Mechanism | Circuit | Models Using It |
|-----------|---------|----------------|
| BEP (Beat Entrainment Processing) | sensorimotor | PEOM, MSR, GSSM, ASAP, DDSMI, VRMSME, SPMC, NSCP, CTBB, STC |

All 10 MPU models use the BEP mechanism exclusively.

---

## Cross-Unit Pathways

MPU does not currently participate in any declared cross-unit pathways. It is neither a source nor a target.

---

## Code Reference

- Unit class: `mi_beta.brain.units.mpu._unit.MPUUnit`
- Models package: `mi_beta.brain.units.mpu.models`
- Unit directory: `mi_beta/brain/units/mpu/`

## Model Documentation

- [MPU-alpha1-PEOM](../Models/MPU-α1-PEOM/)
- [MPU-alpha2-MSR](../Models/MPU-α2-MSR/)
- [MPU-alpha3-GSSM](../Models/MPU-α3-GSSM/)
- [MPU-beta1-ASAP](../Models/MPU-β1-ASAP/)
- [MPU-beta2-DDSMI](../Models/MPU-β2-DDSMI/)
- [MPU-beta3-VRMSME](../Models/MPU-β3-VRMSME/)
- [MPU-beta4-SPMC](../Models/MPU-β4-SPMC/)
- [MPU-gamma1-NSCP](../Models/MPU-γ1-NSCP/)
- [MPU-gamma2-CTBB](../Models/MPU-γ2-CTBB/)
- [MPU-gamma3-STC](../Models/MPU-γ3-STC/)
