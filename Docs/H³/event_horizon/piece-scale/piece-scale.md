# Piece Scale — H₂₉-H₃₁ (500-981s)

**Windows**: H₂₉, H₃₀, H₃₁
**Duration Range**: 500-981s (8-16 minutes)
**Neural Basis**: Ventral Striatum (VS/NAcc), reward/narrative
**Cognitive Function**: Complete work perception, musical satisfaction

---

## Overview

The Piece Scale represents the longest temporal context in the Event Horizon, spanning complete musical works. This range is associated with the Ventral Striatum (NAcc) — the brain's reward center — explaining the deep satisfaction from hearing an entire symphony or album.

---

## Windows in This Scale

| Window | Duration | Status | Primary Use |
|--------|----------|--------|-------------|
| [H₂₉](piece-h29-500s.md) | 500s | Interpolated | Short piece integration |
| [H₃₀](piece-h30-700s.md) | 700s | Interpolated | Medium piece |
| [H₃₁](piece-h31-981s.md) | 981s | Validated | VS narrative reward |

---

## Neuroscience Foundation

| Paper | Year | Finding |
|-------|------|---------|
| Hamid et al. | 2024 | VS encodes long-term narrative reward |
| Salimpoor et al. | 2011 | NAcc activation during music pleasure |
| Berridge & Kringelbach | 2015 | VS for hedonic "liking" |

---

## HC⁰ Mechanisms Using This Scale

| Mechanism | Windows | Dimensions |
|-----------|---------|------------|
| **SGM** | H₃₁ | vs_value, vs_narrative, gradient_position, dopamine_level |

---

## HR⁰ Mechanisms Using This Scale

| Mechanism | Windows | Dimensions |
|-----------|---------|------------|
| **FTO** | H₂₉, H₃₀ | Extended form-temporal organization |

---

## Musical Relevance

- **Pop songs**: Complete 3-5 minute works at H₂₉
- **Symphony movements**: Extended classical forms at H₃₀
- **Complete symphonies**: Entire work satisfaction at H₃₁
- **Album coherence**: Multi-track narrative integration

---

## Memory Requirements

```python
# H₃₁ requires the largest history buffer
PIECE_SCALE = {
    'windows': [29, 30, 31],
    'range_ms': (500000, 981000),
    'range_minutes': (8.3, 16.35),
    'brain_regions': ['NAcc', 'VTA', 'vmPFC'],
    'striatal_gradient': 'VS (reward/narrative)',
    'validated': [False, False, True],  # Only H₃₁ validated

    # Memory: 981s × 172Hz × 256D × 4B = 173 MB buffer
    'max_buffer_mb': 173
}
```

---

## Striatal Gradient Theory

The three validated long-range windows (H₂₄, H₂₈, H₃₁) form the **Striatal Gradient Model** (SGM):

```
DLS (36s)  →  DMS (414s)  →  VS (981s)
 Habitual      Goal-directed   Narrative
 Procedural    Cognitive       Reward
```

This gradient explains how musical experience transitions from automatic processing to conscious appreciation to deep satisfaction.

---

**Implementation**: `Pipeline/D0/h0/event_horizon/piece_scale.py`
