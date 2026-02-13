# IMU -- Integrative Memory Unit

| Property | Value |
|----------|-------|
| UNIT_NAME | IMU |
| FULL_NAME | Integrative Memory Unit |
| CIRCUIT | mnemonic |
| POOLED_EFFECT | d = 0.53 |
| Evidence | Core-4 (k >= 10 studies) |
| Dependency | Independent (Phase 2) |
| Total Output | 159D per frame |
| Model Count | 15 |

---

## Description

The IMU models how the brain stores, retrieves, and integrates musical memories -- autobiographical associations, tonal schema, recognition, and consolidation. Its primary neural regions are the hippocampus and mPFC. Its memory_state output feeds into ARU via pathway P3.

---

## Model Roster

### Alpha (k >= 10, >90% confidence)

| # | Model ID | Full Name | OUTPUT_DIM | Mechanisms |
|---|----------|-----------|-----------|------------|
| 1 | MEAMN | Music-Evoked Autobiographical Memory | 12D | MEM, TMH |
| 2 | PNH | Pythagorean Neural Hierarchy | 11D | MEM |
| 3 | MMP | Musical Mnemonic Preservation | 12D | MEM |

### Beta (5 <= k < 10, 70--90% confidence)

| # | Model ID | Full Name | OUTPUT_DIM | Mechanisms |
|---|----------|-----------|-----------|------------|
| 4 | RASN | Rhythmic Auditory Stimulation Network | 11D | BEP, MEM |
| 5 | PMIM | Predictive Memory Integration Matrix | 11D | MEM, TMH |
| 6 | OII | Oscillatory Intelligence Integration | 10D | MEM |
| 7 | HCMC | Hippocampal-Cortical Memory Consolidation | 11D | MEM |
| 8 | RIRI | Recognition-Recall Integration Recency | 10D | MEM |
| 9 | MSPBA | Musical Syntax Processing Broca's Area | 11D | SYN |
| 10 | VRIAP | VR-Induced Analgesia Paradigm | 10D | MEM |
| 11 | TPRD | Tonotopy-Pitch Representation Density | 10D | PPC |
| 12 | CMAPCC | Cross-Modal Action-Perception Coupling | 10D | BEP, MEM |

### Gamma (k < 5, <70% confidence)

| # | Model ID | Full Name | OUTPUT_DIM | Mechanisms |
|---|----------|-----------|-----------|------------|
| 13 | DMMS | Developmental Music Memory Schema | 10D | MEM |
| 14 | CSSL | Cross-Species Song Learning | 10D | MEM |
| 15 | CDEM | Context-Dependent Emotional Memory | 10D | MEM |

**Total unit dimensionality: 12 + 11 + 12 + 11 + 11 + 10 + 11 + 10 + 11 + 10 + 10 + 10 + 10 + 10 + 10 = 159D**

---

## Mechanisms Used

| Mechanism | Circuit | Models Using It |
|-----------|---------|----------------|
| MEM (Memory Encoding/Retrieval) | mnemonic | MEAMN, PNH, MMP, RASN, PMIM, OII, HCMC, RIRI, VRIAP, CMAPCC, DMMS, CSSL, CDEM |
| TMH (Temporal Memory Hierarchy) | sensorimotor | MEAMN, PMIM |
| BEP (Beat Entrainment Processing) | sensorimotor | RASN, CMAPCC |
| SYN (Syntactic Processing) | mnemonic | MSPBA |
| PPC (Pitch Processing Chain) | perceptual | TPRD |

---

## Cross-Unit Pathways

| Pathway | Direction | Target | Description |
|---------|-----------|--------|-------------|
| P3 | IMU -> ARU | ARU | Memory -> affect (Janata 2009, r=0.55) |

IMU is a source unit for pathway P3, feeding memory state signals to the Affective Resonance Unit.

---

## Code Reference

- Unit class: `mi_beta.brain.units.imu._unit.IMUUnit`
- Models package: `mi_beta.brain.units.imu.models`
- Unit directory: `mi_beta/brain/units/imu/`

## Model Documentation

- [IMU-alpha1-MEAMN](../Models/IMU-α1-MEAMN/)
- [IMU-alpha2-PNH](../Models/IMU-α2-PNH/)
- [IMU-alpha3-MMP](../Models/IMU-α3-MMP/)
- [IMU-beta1-RASN](../Models/IMU-β1-RASN/)
- [IMU-beta2-PMIM](../Models/IMU-β2-PMIM/)
- [IMU-beta3-OII](../Models/IMU-β3-OII/)
- [IMU-beta4-HCMC](../Models/IMU-β4-HCMC/)
- [IMU-beta5-RIRI](../Models/IMU-β5-RIRI/)
- [IMU-beta6-MSPBA](../Models/IMU-β6-MSPBA/)
- [IMU-beta7-VRIAP](../Models/IMU-β7-VRIAP/)
- [IMU-beta8-TPRD](../Models/IMU-β8-TPRD/)
- [IMU-beta9-CMAPCC](../Models/IMU-β9-CMAPCC/)
- [IMU-gamma1-DMMS](../Models/IMU-γ1-DMMS/)
- [IMU-gamma2-CSSL](../Models/IMU-γ2-CSSL/)
- [IMU-gamma3-CDEM](../Models/IMU-γ3-CDEM/)
