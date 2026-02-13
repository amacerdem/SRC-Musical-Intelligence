# STU -- Sensorimotor Timing Unit

| Property | Value |
|----------|-------|
| UNIT_NAME | STU |
| FULL_NAME | Sensorimotor Timing Unit |
| CIRCUIT | sensorimotor |
| POOLED_EFFECT | d = 0.67 |
| Evidence | Core-4 (k >= 10 studies) |
| Dependency | Independent (Phase 2) |
| Total Output | 148D per frame |
| Model Count | 14 |

---

## Description

The STU models how the brain encodes temporal structure in music -- beat, metre, tempo, groove, and auditory-motor coupling. Its primary neural regions are SMA and Heschl's gyrus. Some internal routing occurs via pathways P2 and P4.

---

## Model Roster

### Alpha (k >= 10, >90% confidence)

| # | Model ID | Full Name | OUTPUT_DIM | Mechanisms |
|---|----------|-----------|-----------|------------|
| 1 | HMCE | Hierarchical Musical Context Encoding | 13D | BEP, TMH |
| 2 | AMSC | Auditory-Motor Stream Coupling | 12D | BEP, TMH |
| 3 | MDNS | Melody Decoding Neural Signals | 12D | BEP |

### Beta (5 <= k < 10, 70--90% confidence)

| # | Model ID | Full Name | OUTPUT_DIM | Mechanisms |
|---|----------|-----------|-----------|------------|
| 4 | AMSS | Attention-Modulated Stream Segregation | 11D | BEP |
| 5 | TPIO | Timbre Perception-Imagery Overlap | 10D | TPC |
| 6 | EDTA | Expertise-Dependent Tempo Adaptation | 10D | BEP |
| 7 | ETAM | Entrainment Tempo Attention Modulation | 11D | BEP |
| 8 | HGSIC | Hierarchical Groove State Integration | 11D | BEP, TMH |
| 9 | OMS | Oscillatory Motor Synchronization | 10D | BEP |

### Gamma (k < 5, <70% confidence)

| # | Model ID | Full Name | OUTPUT_DIM | Mechanisms |
|---|----------|-----------|-----------|------------|
| 10 | TMRM | Tempo Memory Reproduction Matrix | 10D | BEP, TMH |
| 11 | NEWMD | Neural Entrainment-Working Memory Dissociation | 10D | BEP |
| 12 | MTNE | Music Training Neural Efficiency | 10D | BEP |
| 13 | PTGMP | Piano Training Grey Matter Plasticity | 10D | BEP |
| 14 | MPFS | Musical Prodigy Flow State | 10D | BEP |

**Total unit dimensionality: 13 + 12 + 12 + 11 + 10 + 10 + 11 + 11 + 10 + 10 + 10 + 10 + 10 + 10 = 148D**

---

## Mechanisms Used

| Mechanism | Circuit | Models Using It |
|-----------|---------|----------------|
| BEP (Beat Entrainment Processing) | sensorimotor | HMCE, AMSC, MDNS, AMSS, EDTA, ETAM, HGSIC, OMS, TMRM, NEWMD, MTNE, PTGMP, MPFS |
| TMH (Temporal Memory Hierarchy) | sensorimotor | HMCE, AMSC, HGSIC, TMRM |
| TPC (Timbre Processing Chain) | perceptual | TPIO |

---

## Cross-Unit Pathways

| Pathway | Direction | Target | Description |
|---------|-----------|--------|-------------|
| P2 | STU -> STU | STU (internal) | Beat -> motor sync (Grahn & Brett 2007, r=0.70) |
| P4 | STU -> STU | STU (internal) | Context -> prediction (Mischler 2025, r=0.99) |
| P5 | STU -> ARU | ARU | Tempo -> emotion (Juslin & Vastfjall 2008, r=0.60) |

STU is a source unit for pathways P2 (internal), P4 (internal), and P5 (to ARU).

---

## Code Reference

- Unit class: `mi_beta.brain.units.stu._unit.STUUnit`
- Models package: `mi_beta.brain.units.stu.models`
- Unit directory: `mi_beta/brain/units/stu/`

## Model Documentation

- [STU-alpha1-HMCE](../Models/STU-α1-HMCE/)
- [STU-alpha2-AMSC](../Models/STU-α2-AMSC/)
- [STU-alpha3-MDNS](../Models/STU-α3-MDNS/)
- [STU-beta1-AMSS](../Models/STU-β1-AMSS/)
- [STU-beta2-TPIO](../Models/STU-β2-TPIO/)
- [STU-beta3-EDTA](../Models/STU-β3-EDTA/)
- [STU-beta4-ETAM](../Models/STU-β4-ETAM/)
- [STU-beta5-HGSIC](../Models/STU-β5-HGSIC/)
- [STU-beta6-OMS](../Models/STU-β6-OMS/)
- [STU-gamma1-TMRM](../Models/STU-γ1-TMRM/)
- [STU-gamma2-NEWMD](../Models/STU-γ2-NEWMD/)
- [STU-gamma3-MTNE](../Models/STU-γ3-MTNE/)
- [STU-gamma4-PTGMP](../Models/STU-γ4-PTGMP/)
- [STU-gamma5-MPFS](../Models/STU-γ5-MPFS/)
