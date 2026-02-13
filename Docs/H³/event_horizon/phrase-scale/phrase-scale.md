# Phrase Scale — H₁₇-H₂₀ (1.25-5s)

**Windows**: H₁₇, H₁₈, H₁₉, H₂₀
**Duration Range**: 1.25-5s
**Neural Basis**: Association cortex, prefrontal integration
**Cognitive Function**: Phrase structure, melodic arcs

---

## Overview

The Phrase Scale captures musical phrases — the "sentences" of music. This range spans from two-bar phrases through complete melodic arcs, integrating multiple beats into coherent musical ideas. This is where music transitions from rhythmic patterns to meaningful structure.

---

## Windows in This Scale

| Window | Duration | Status | Primary Use |
|--------|----------|--------|-------------|
| [H₁₇](phrase-h17-1250ms.md) | 1250ms | Validated | Phrase boundary detection |
| [H₁₈](phrase-h18-2s.md) | 2s | Interpolated | Short phrase integration |
| [H₁₉](phrase-h19-3s.md) | 3s | Interpolated | Standard phrase |
| [H₂₀](phrase-h20-5s.md) | 5s | Validated | Section boundary preview |

---

## Neuroscience Foundation

| Paper | Year | Finding |
|-------|------|---------|
| Hickok & Poeppel | 2007 | Dual-stream model for auditory processing |
| Rauschecker & Scott | 2009 | Ventral stream integration |
| Pöppel | 1997 | 2-3s psychological present |
| Working memory | Various | 7±2 items in auditory buffer |

---

## HC⁰ Mechanisms Using This Scale

| Mechanism | Windows | Dimensions |
|-----------|---------|------------|
| **TIH** | H₁₇, H₂₀ | macro scale, global scale |

---

## HR⁰ Mechanisms Using This Scale

| Mechanism | Windows | Dimensions |
|-----------|---------|------------|
| **RTI** | H₁₈, H₁₉ | temporal_average, recency_weight |

---

## Musical Relevance

- **Two-bar phrases**: Antecedent phrases at H₁₇
- **Four-beat phrases**: Question phrases at H₁₈
- **Standard phrases**: Complete melodic ideas at H₁₉
- **Extended phrases**: 8-bar structures at H₂₀

---

## Implementation

```python
PHRASE_SCALE = {
    'windows': [17, 18, 19, 20],
    'range_ms': (1250, 5000),
    'brain_regions': ['dlPFC', 'mPFC', 'ACC', 'Parietal', 'Temporal association'],
    'validated': [True, False, False, True]  # H₁₈, H₁₉ interpolated
}
```

---

**Implementation**: `Pipeline/D0/h0/event_horizon/phrase_scale.py`
