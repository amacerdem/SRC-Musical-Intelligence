# PCU -- Predictive Coding Unit

| Property | Value |
|----------|-------|
| UNIT_NAME | PCU |
| FULL_NAME | Predictive Coding Unit |
| CIRCUIT | mnemonic |
| POOLED_EFFECT | d = 0.58 |
| Evidence | Experimental-5 (k < 10 studies) |
| Dependency | Independent (Phase 2) |
| Total Output | 94D per frame |
| Model Count | 9 |

---

## Description

The PCU models how the brain generates predictions about upcoming musical events -- harmonic tension, pitch uncertainty, imagery-cognition coupling, and working-memory-emotion dynamics. Its primary neural regions are the dorsolateral prefrontal cortex and inferior parietal lobule.

---

## Model Roster

### Alpha (k >= 10, >90% confidence)

| # | Model ID | Full Name | OUTPUT_DIM | Mechanisms |
|---|----------|-----------|-----------|------------|
| 1 | HTP | Harmonic Tension Prediction | 12D | PPC, TPC, MEM |
| 2 | SPH | Spectral Pitch Height | 11D | PPC |
| 3 | ICEM | Imagery-Cognition Emotion Mapping | 11D | AED, C0P |

### Beta (5 <= k < 10, 70--90% confidence)

| # | Model ID | Full Name | OUTPUT_DIM | Mechanisms |
|---|----------|-----------|-----------|------------|
| 4 | PWUP | Pitch-Weight Uncertainty Processing | 10D | PPC |
| 5 | WMED | Working Memory Emotion Dynamics | 10D | MEM, AED |
| 6 | UDP | Uncertainty-Driven Prediction | 10D | C0P |

### Gamma (k < 5, <70% confidence)

| # | Model ID | Full Name | OUTPUT_DIM | Mechanisms |
|---|----------|-----------|-----------|------------|
| 7 | IGFE | Imagery-Guided Feature Enhancement | 10D | TPC |
| 8 | MAA | Musical Agentic Attention | 10D | ASA |
| 9 | PSH | Perceptual Salience Hierarchy | 10D | PPC, TPC, MEM |

**Total unit dimensionality: 12 + 11 + 11 + 10 + 10 + 10 + 10 + 10 + 10 = 94D**

---

## Mechanisms Used

| Mechanism | Circuit | Models Using It |
|-----------|---------|----------------|
| PPC (Pitch Processing Chain) | perceptual | HTP, SPH, PWUP, PSH |
| TPC (Timbre Processing Chain) | perceptual | HTP, IGFE, PSH |
| MEM (Memory Encoding/Retrieval) | mnemonic | HTP, WMED, PSH |
| AED (Affective Entrainment Dynamics) | mesolimbic | ICEM, WMED |
| C0P (Cognitive Projection) | mesolimbic | ICEM, UDP |
| ASA (Auditory Scene Analysis) | salience | MAA |

PCU has the broadest mechanism usage of any unit, drawing from 6 of the 10 available mechanisms across 4 circuits.

---

## Cross-Unit Pathways

PCU does not currently participate in any declared cross-unit pathways. It is neither a source nor a target.

---

## Code Reference

- Unit class: `mi_beta.brain.units.pcu._unit.PCUUnit`
- Models package: `mi_beta.brain.units.pcu.models`
- Unit directory: `mi_beta/brain/units/pcu/`

## Model Documentation

- [PCU-alpha1-HTP](../Models/PCU-α1-HTP/)
- [PCU-alpha2-SPH](../Models/PCU-α2-SPH/)
- [PCU-alpha3-ICEM](../Models/PCU-α3-ICEM/)
- [PCU-beta1-PWUP](../Models/PCU-β1-PWUP/)
- [PCU-beta2-WMED](../Models/PCU-β2-WMED/)
- [PCU-beta3-UDP](../Models/PCU-β3-UDP/)
- [PCU-gamma1-IGFE](../Models/PCU-γ1-IGFE/)
- [PCU-gamma2-MAA](../Models/PCU-γ2-MAA/)
- [PCU-gamma3-PSH](../Models/PCU-γ3-PSH/)
