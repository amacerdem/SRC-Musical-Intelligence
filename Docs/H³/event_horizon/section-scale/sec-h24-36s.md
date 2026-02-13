# H₂₄: 36s — SGM DLS (Dorsolateral Striatum)

**Window Index**: 24
**Duration**: 36000ms (36s)
**Scale**: Section
**Neural Basis**: Dorsolateral Striatum (DLS)
**Status**: Literature-validated

---

## Overview

H₂₄ captures the Dorsolateral Striatum component of the Striatal Gradient Model — encoding habitual/procedural memory at the section scale. This explains why repeated musical patterns become "automatic."

---

## Neural Basis

| Region | Function | Evidence |
|--------|----------|----------|
| DLS | Habitual behavior | Yin & Knowlton 2006 |
| Putamen (lateral) | Procedural memory | Mello et al. 2015 |
| Motor circuits | Automatic response | Hamid et al. 2024 |

---

## HC⁰ Mechanisms Using This Window

| Mechanism | Dimensions | Function |
|-----------|------------|----------|
| **SGM** | dls_value, dls_habit | Striatal Gradient - DLS |

**Striatal Gradient Position:**
```
DLS (36s)  →  DMS (414s)  →  VS (981s)
  ↑
H₂₄ = Habitual/Procedural
```

---

## Scientific Evidence

| Paper | Year | Finding |
|-------|------|---------|
| Hamid et al. | 2024 | DLS encodes short-term reward integration |
| Mello et al. | 2015 | Striatal time gradient discovery |
| Yin & Knowlton | 2006 | DLS for habitual behavior |

---

## Musical Relevance

- Learning repeated patterns
- Automatic rhythm response
- Groove habituation
- Procedural memory for familiar songs

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | novel | No habit formation | < 0.125 |
| 1 | learning | Beginning habituation | < 0.25 |
| 2 | practicing | Developing habit | < 0.375 |
| 3 | familiar | Emerging automaticity | < 0.5 |
| 4 | habitual | Normal automaticity | < 0.625 |
| 5 | automatic | Strong habit | < 0.75 |
| 6 | ingrained | Deep procedural | < 0.875 |
| 7 | reflexive | Perfect automaticity | ≥ 0.875 |

---

**Implementation**: `Pipeline/D0/h0/event_horizon/section_scale/h24.py`
