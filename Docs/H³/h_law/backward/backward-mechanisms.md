# Backward Mode Mechanisms

**Mode**: Backward (L₁)
**Primary Use**: Anticipatory processing, offline analysis

---

## Mechanisms Using Backward Mode

Backward mode is **rarely used as a primary mode**. Most mechanisms prefer either Forward (causal) or Bidirectional (full context). However, backward mode is valuable for:

### Specific Use Cases

| Context | Purpose |
|---------|---------|
| **Offline analysis** | When entire piece is available |
| **Anticipation features** | Detecting buildup to events |
| **Reverse patterns** | Analyzing decay/release phases |
| **Comparison baseline** | Contrasting with forward mode |

---

## HC⁰ Mechanisms with Backward Components

| Mechanism | Use Case |
|-----------|----------|
| **HRM** | Forward + Backward replay (bidirectional hippocampal replay) |
| **CPD** | Anticipation tracking (what's about to resolve) |

---

## Why Backward Mode is Rare

### 1. Real-Time Constraint

Most musical applications require real-time or near-real-time processing:

```
Live performance: Cannot access future
Streaming: Minimal buffering preferred
Interactive: Immediate response needed
```

### 2. Cognitive Realism

Human cognition is primarily forward-looking:
- We hear the past
- We predict the future
- But we cannot "perceive" future sounds

### 3. Redundancy with Bidirectional

For offline analysis, bidirectional mode provides more information than backward alone.

---

## When to Use Backward Mode

1. **Analyzing anticipation**: How does the signal prepare for an event?
2. **Decay analysis**: What happens after a peak?
3. **Reverse engineering**: Understanding causal chains in reverse
4. **Academic research**: Testing directional hypotheses

---

## Implementation Pattern

```python
def extract_backward_features(
    h0_tensor: np.ndarray,
    mechanism: str
) -> np.ndarray:
    """Extract features using backward mode (l=1)."""
    features = []
    for h in mechanism_windows[mechanism]:
        for m in mechanism_morphs[mechanism]:
            # Backward mode = index 1
            features.append(h0_tensor[h, m, 1])
    return np.array(features)
```

---

## Comparison: Forward vs Backward

| Aspect | Forward (L₀) | Backward (L₁) |
|--------|--------------|---------------|
| Real-time | Yes | No |
| Temporal focus | History | Future |
| Primary use | Processing | Anticipation |
| Common | Very | Rare |

---

**See Also**: [../h-law.md](../h-law.md) — H-Law overview
