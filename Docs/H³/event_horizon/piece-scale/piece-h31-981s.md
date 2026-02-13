# H₃₁: 981s — SGM VS (Ventral Striatum)

**Window Index**: 31
**Duration**: 981000ms (981s / 16.35 min)
**Scale**: Piece
**Neural Basis**: Ventral Striatum (VS/NAcc)
**Status**: Literature-validated

---

## Overview

H₃₁ captures the Ventral Striatum (NAcc) component of the Striatal Gradient Model — the peak of the striatal reward gradient. This enables piece-level narrative reward and the deep satisfaction from hearing complete musical works.

---

## Neural Basis

| Region | Function | Evidence |
|--------|----------|----------|
| NAcc | Reward/pleasure | Salimpoor et al. 2011 |
| VTA | Dopamine release | Berridge & Kringelbach 2015 |
| vmPFC | Valuation | Hamid et al. 2024 |

---

## HC⁰ Mechanisms Using This Window

| Mechanism | Dimensions | Function |
|-----------|------------|----------|
| **SGM** | vs_value, vs_narrative, gradient_position, dopamine_level | Striatal Gradient - VS |

**Striatal Gradient Position:**
```
DLS (36s)  →  DMS (414s)  →  VS (981s)
                              ↑
                      H₃₁ = Reward/Narrative
```

---

## Scientific Evidence

| Paper | Year | Finding |
|-------|------|---------|
| Hamid et al. | 2024 | VS encodes long-term narrative reward |
| Salimpoor et al. | 2011 | NAcc activation during peak music pleasure |
| Berridge & Kringelbach | 2015 | VS for hedonic "liking" |

---

## Musical Relevance

- Entire symphony satisfaction
- Album-level coherence
- Concert experience integration
- Musical journey completion

---

## Memory Requirements

```python
# H₃₁ defines maximum history buffer
MAX_WINDOW_SECONDS = 981
SAMPLE_RATE_HZ = 172
FEATURE_DIM = 256
BYTES_PER_FLOAT = 4

buffer_frames = MAX_WINDOW_SECONDS * SAMPLE_RATE_HZ  # 168,732
buffer_bytes = buffer_frames * FEATURE_DIM * BYTES_PER_FLOAT
# = 173 MB
```

---

## Vocabulary Gradient (8 levels)

| Index | Term | Description | Threshold |
|-------|------|-------------|-----------|
| 0 | unmoved | No reward | < 0.125 |
| 1 | touched | Minimal pleasure | < 0.25 |
| 2 | pleased | Light satisfaction | < 0.375 |
| 3 | satisfied | Moderate reward | < 0.5 |
| 4 | fulfilled | Normal pleasure | < 0.625 |
| 5 | elated | Strong satisfaction | < 0.75 |
| 6 | transported | High reward | < 0.875 |
| 7 | transcendent | Peak pleasure | ≥ 0.875 |

---

## Striatal Gradient Summary

| Window | Region | Duration | Memory Type | Function |
|--------|--------|----------|-------------|----------|
| H₂₄ | DLS | 36s | Habitual | Automatic response |
| H₂₈ | DMS | 414s | Goal-directed | Cognitive tracking |
| H₃₁ | VS | 981s | Reward/Narrative | Deep satisfaction |

---

**Implementation**: `Pipeline/D0/h0/event_horizon/piece_scale/h31.py`
