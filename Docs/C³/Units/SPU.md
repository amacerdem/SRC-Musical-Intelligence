# SPU -- Spectral Processing Unit

| Property | Value |
|----------|-------|
| UNIT_NAME | SPU |
| FULL_NAME | Spectral Processing Unit |
| CIRCUIT | perceptual |
| POOLED_EFFECT | d = 0.84 |
| Evidence | Core-4 (k >= 10 studies) |
| Dependency | Independent (Phase 2) |
| Total Output | 99D per frame |
| Model Count | 9 |

---

## Description

The SPU models how the auditory cortex processes spectral features of sound -- pitch, consonance, timbre, and spectral integration. Its primary neural regions are Heschl's gyrus and Planum Polare.

---

## Model Roster

### Alpha (k >= 10, >90% confidence)

| # | Model ID | Full Name | OUTPUT_DIM | Mechanisms |
|---|----------|-----------|-----------|------------|
| 1 | BCH | Brainstem Consonance Hierarchy | 12D | PPC |
| 2 | PSCL | Pitch Salience Cortical Localization | 12D | PPC |
| 3 | PCCR | Pitch Chroma Cortical Representation | 11D | PPC |

### Beta (5 <= k < 10, 70--90% confidence)

| # | Model ID | Full Name | OUTPUT_DIM | Mechanisms |
|---|----------|-----------|-----------|------------|
| 4 | STAI | Spectral-Temporal Aesthetic Interaction | 12D | TPC |
| 5 | TSCP | Timbre-Specific Cortical Plasticity | 10D | TPC |
| 6 | MIAA | Musical Imagery Auditory Activation | 11D | TPC |

### Gamma (k < 5, <70% confidence)

| # | Model ID | Full Name | OUTPUT_DIM | Mechanisms |
|---|----------|-----------|-----------|------------|
| 7 | SDNPS | Stimulus-Dependent Neural Pitch Scaling | 10D | PPC |
| 8 | ESME | Expertise-Specific MMN Enhancement | 11D | PPC |
| 9 | SDED | Sensory Dissonance Early Detection | 10D | PPC |

**Total unit dimensionality: 12 + 12 + 11 + 12 + 10 + 11 + 10 + 11 + 10 = 99D**

---

## Mechanisms Used

| Mechanism | Circuit | Models Using It |
|-----------|---------|----------------|
| PPC (Pitch Processing Chain) | perceptual | BCH, PSCL, PCCR, SDNPS, ESME, SDED |
| TPC (Timbre Processing Chain) | perceptual | STAI, TSCP, MIAA |

---

## Cross-Unit Pathways

| Pathway | Direction | Target | Description |
|---------|-----------|--------|-------------|
| P1 | SPU -> ARU | ARU | Consonance -> pleasure (Bidelman 2009, r=0.81) |

SPU is a source unit for pathway P1, feeding consonance signals to the Affective Resonance Unit.

---

## Code Reference

- Unit class: `mi_beta.brain.units.spu._unit.SPUUnit`
- Models package: `mi_beta.brain.units.spu.models`
- Unit directory: `mi_beta/brain/units/spu/`

## Model Documentation

- [SPU-alpha1-BCH](../Models/SPU-α1-BCH/)
- [SPU-alpha2-PSCL](../Models/SPU-α2-PSCL/)
- [SPU-alpha3-PCCR](../Models/SPU-α3-PCCR/)
- [SPU-beta1-STAI](../Models/SPU-β1-STAI/)
- [SPU-beta2-TSCP](../Models/SPU-β2-TSCP/)
- [SPU-beta3-MIAA](../Models/SPU-β3-MIAA/)
- [SPU-gamma1-SDNPS](../Models/SPU-γ1-SDNPS/)
- [SPU-gamma2-ESME](../Models/SPU-γ2-ESME/)
- [SPU-gamma3-SDED](../Models/SPU-γ3-SDED/)
