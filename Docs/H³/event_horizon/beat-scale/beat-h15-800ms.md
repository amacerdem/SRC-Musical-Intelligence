# H₁₅: 800ms — Groove Beat Period

**Window Index**: 15
**Duration**: 800ms (75 BPM)
**Scale**: Beat
**Neural Basis**: Motor-auditory entrainment
**Status**: Literature-validated

---

## Overview

H₁₅ captures the "groove sweet spot" — the ~800ms beat period at which humans experience maximum movement pleasure. This window represents optimal motor-auditory coupling for dance and embodied rhythm.

---

## Neural Basis

| Region | Function | Evidence |
|--------|----------|----------|
| Motor cortex | Movement generation | Janata et al. 2012 |
| Putamen | Groove pleasure | Madison et al. 2011 |
| Cerebellum | Timing precision | Witek et al. 2014 |

---

## HC⁰ Mechanisms Using This Window

| Mechanism | Dimensions | Function |
|-----------|------------|----------|
| **GRV** | movement_urge, body_specificity, groove_pleasure, pupf_zone | Groove mechanism |
| **CPD** | reaction_intensity, appraisal_valence, chills_probability, ans_prediction | ITPRA R-A stages |

**Groove Inverted-U:**
```
Groove Pleasure
     ▲
     │      ╭───╮
     │    ╭╯     ╰╮
     │  ╭╯         ╰╮
     │╭╯             ╰╮
     └──────────────────→
       Low  Medium  High
          Syncopation
```

---

## Scientific Evidence

| Paper | Year | Finding |
|-------|------|---------|
| Janata et al. | 2012 | 800ms optimal tempo for groove |
| Madison et al. | 2011 | Medium syncopation optimal |
| Witek et al. | 2014 | Groove pleasure inverted-U with complexity |

---

## Musical Relevance

- Dance music grooves
- Embodied rhythm experience
- Movement pleasure
- Optimal dance tempo

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | flat | No groove | < 0.125 |
| 1 | tepid | Minimal feel | < 0.25 |
| 2 | emerging | Building groove | < 0.375 |
| 3 | moderate | Some movement | < 0.5 |
| 4 | grooving | Normal groove | < 0.625 |
| 5 | infectious | Strong urge | < 0.75 |
| 6 | irresistible | High groove | < 0.875 |
| 7 | transcendent | Peak groove | ≥ 0.875 |

---

**Implementation**: `Pipeline/D0/h0/event_horizon/beat_scale/h15.py`
