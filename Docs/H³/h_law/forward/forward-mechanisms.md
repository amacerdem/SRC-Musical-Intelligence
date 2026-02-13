# Forward Mode Mechanisms

**Mode**: Forward (L₀)
**Primary Use**: Real-time causal processing

---

## HC⁰ Mechanisms Using Forward Mode

| Mechanism | Layer | Rationale |
|-----------|-------|-----------|
| **TIH** | L1 Oscillatory | Temporal integration is cumulative |
| **PTM** | L2 Timing | Beat prediction based on history |
| **HRM** | L3 Memory | Hippocampal replay uses past sequences |
| **SGM** | L3 Memory | Reward gradient tracks history |
| **EFC** | L3 Memory | Efference copy is strictly causal |
| **C0P** | L4 Affective | C⁰ projection from processed data |

---

## HR⁰ Mechanisms Using Forward Mode

| Mechanism | Rationale |
|-----------|-----------|
| **RTI** | Real-time integration requires causal processing |
| **GTI** | Global form tracking is cumulative |
| **FTO** | Form-temporal organization is history-dependent |

---

## Why Forward Mode?

### 1. Real-Time Compatibility

Forward mode is the only mode that works in real-time streaming applications:

```
Audio stream: ───────────────────────────────►
                                             ↑
                                          "Now"

Forward: Can compute immediately
Backward/Bidirectional: Requires buffering future
```

### 2. Causal Mechanisms

Some cognitive processes are inherently causal:

| Process | Why Causal |
|---------|------------|
| **Prediction** | Based on past patterns |
| **Memory** | Encodes past events |
| **Motor preparation** | Based on sensory history |
| **Reward learning** | Outcomes follow actions |

### 3. Temporal Order

Forward mode preserves temporal order in processing:

```
Event A → Event B → Event C → Now
   ↓         ↓         ↓
   More      ↓        Less
 weighted  weighted  weighted
```

---

## Implementation Pattern

```python
def extract_forward_features(
    h0_tensor: np.ndarray,
    mechanism: str
) -> np.ndarray:
    """Extract features using forward mode (l=0)."""
    features = []
    for h in mechanism_windows[mechanism]:
        for m in mechanism_morphs[mechanism]:
            # Forward mode = index 0
            features.append(h0_tensor[h, m, 0])
    return np.array(features)
```

---

**See Also**: [../h-law.md](../h-law.md) — H-Law overview
