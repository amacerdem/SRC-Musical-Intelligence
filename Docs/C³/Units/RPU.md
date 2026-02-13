# RPU -- Reward Processing Unit

| Property | Value |
|----------|-------|
| UNIT_NAME | RPU |
| FULL_NAME | Reward Processing Unit |
| CIRCUIT | mesolimbic |
| POOLED_EFFECT | d = 0.70 |
| Evidence | Experimental-5 (k < 10 studies) |
| Dependency | **Dependent** (Phase 4) |
| Total Output | 94D per frame |
| Model Count | 9 |

---

## Description

The RPU models how the brain computes reward signals from musical stimuli -- dopamine dynamics, reward prediction error, information-uncertainty coupling, and aesthetic computation. Its primary neural regions are the ventral striatum, OFC, and vmPFC. As a dependent unit, it receives cross-unit inputs from ARU and SPU after the first-pass independent units have been computed.

---

## Model Roster

### Alpha (k >= 10, >90% confidence)

| # | Model ID | Full Name | OUTPUT_DIM | Mechanisms |
|---|----------|-----------|-----------|------------|
| 1 | DAED | DA-Expectation Dynamics | 12D | AED, CPD |
| 2 | MORMR | Model-Optimal Reward Modulation Relay | 11D | AED, C0P |
| 3 | RPEM | Reward Prediction Error Model | 11D | AED, CPD |

### Beta (5 <= k < 10, 70--90% confidence)

| # | Model ID | Full Name | OUTPUT_DIM | Mechanisms |
|---|----------|-----------|-----------|------------|
| 4 | IUCP | Information-Uncertainty Coupling Process | 10D | C0P |
| 5 | MCCN | Musical Context Coupling Network | 10D | TMH, AED |
| 6 | MEAMR | Memory-Affect Modulated Reward | 10D | MEM, AED |

### Gamma (k < 5, <70% confidence)

| # | Model ID | Full Name | OUTPUT_DIM | Mechanisms |
|---|----------|-----------|-----------|------------|
| 7 | LDAC | Listener-Dependent Aesthetic Computation | 10D | AED |
| 8 | IOTMS | Individual Optimal Tempo Matching System | 10D | BEP |
| 9 | SSPS | Social Signal Processing System | 10D | ASA |

**Total unit dimensionality: 12 + 11 + 11 + 10 + 10 + 10 + 10 + 10 + 10 = 94D**

---

## Mechanisms Used

| Mechanism | Circuit | Models Using It |
|-----------|---------|----------------|
| AED (Affective Entrainment Dynamics) | mesolimbic | DAED, MORMR, RPEM, MCCN, MEAMR, LDAC |
| CPD (Chills & Peak Detection) | mesolimbic | DAED, RPEM |
| C0P (Cognitive Projection) | mesolimbic | MORMR, IUCP |
| TMH (Temporal Memory Hierarchy) | sensorimotor | MCCN |
| MEM (Memory Encoding/Retrieval) | mnemonic | MEAMR |
| BEP (Beat Entrainment Processing) | sensorimotor | IOTMS |
| ASA (Auditory Scene Analysis) | salience | SSPS |

RPU uses 7 of the 10 available mechanisms -- the broadest spread alongside PCU -- reflecting its integrative role in computing reward from multiple sensory and cognitive inputs.

---

## Cross-Unit Pathways

RPU is a target of cross-unit signals routed from ARU and SPU. The specific pathway declarations currently route through the general PathwayRunner mechanism rather than named RPU-specific pathways.

---

## Code Reference

- Unit class: `mi_beta.brain.units.rpu._unit.RPUUnit`
- Models package: `mi_beta.brain.units.rpu.models`
- Unit directory: `mi_beta/brain/units/rpu/`

## Model Documentation

- [RPU-alpha1-DAED](../Models/RPU-α1-DAED/)
- [RPU-alpha2-MORMR](../Models/RPU-α2-MORMR/)
- [RPU-alpha3-RPEM](../Models/RPU-α3-RPEM/)
- [RPU-beta1-IUCP](../Models/RPU-β1-IUCP/)
- [RPU-beta2-MCCN](../Models/RPU-β2-MCCN/)
- [RPU-beta3-MEAMR](../Models/RPU-β3-MEAMR/)
- [RPU-gamma1-LDAC](../Models/RPU-γ1-LDAC/)
- [RPU-gamma2-IOTMS](../Models/RPU-γ2-IOTMS/)
- [RPU-gamma3-SSPS](../Models/RPU-γ3-SSPS/)
