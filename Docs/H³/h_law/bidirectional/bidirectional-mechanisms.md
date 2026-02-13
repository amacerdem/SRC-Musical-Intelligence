# Bidirectional Mode Mechanisms

**Mode**: Bidirectional (L₂)
**Primary Use**: Full context processing, pattern detection

---

## HC⁰ Mechanisms Using Bidirectional Mode

| Mechanism | Layer | Rationale |
|-----------|-------|-----------|
| **OSC** | L1 Oscillatory | Phase requires symmetric context |
| **TGC** | L1 Oscillatory | Coupling measured across time |
| **ATT** | L1 Oscillatory | Attention to surrounding context |
| **NPL** | L2 Timing | Phase-locking bilateral |
| **GRV** | L2 Timing | Groove from surrounding beats |
| **BND** | L3 Memory | Binding features across time |
| **AED** | L4 Affective | Emotion from full context |
| **ASA** | L4 Affective | Stream segregation needs context |
| **CPD** | L4 Affective | Peak detection uses surrounding |

---

## HR⁰ Mechanisms Using Bidirectional Mode

| Mechanism | Rationale |
|-----------|-----------|
| **LTI** | Long-term integration needs full context |
| **XTI** | Cross-layer integration both directions |
| **HRT** | Harmonic rhythm analyzed bilaterally |
| **PST** | Phrase boundaries need surrounding context |
| **TKT** | Key stability measured from context |

---

## Why Bidirectional Mode?

### 1. Maximum Information

Bidirectional mode captures all available temporal information:

```
Information content:
  Forward:       ~50% (past only)
  Backward:      ~50% (future only)
  Bidirectional: 100% (both)
```

### 2. Phase Analysis

Accurate phase estimation requires symmetric context:

```
For oscillation with period T:
  Forward: Phase biased toward recent values
  Bidirectional: True phase at center of window
```

### 3. Pattern Detection

Musical patterns often span both past and future:

```
Example: Phrase boundary

    ───────╲╱───────
            ↑
          Center

Needs context from both sides to identify
```

### 4. Structural Analysis

Understanding musical structure requires seeing both:
- What came before (antecedent)
- What comes after (consequent)

---

## Use Cases

| Analysis Type | Why Bidirectional |
|--------------|-------------------|
| **Beat tracking** | Phase coherent |
| **Phrase segmentation** | Boundary detection |
| **Harmonic analysis** | Full chord context |
| **Timbre analysis** | Attack + sustain + decay |
| **Emotion tracking** | Context-dependent |

---

## Implementation Pattern

```python
def extract_bidirectional_features(
    h0_tensor: np.ndarray,
    mechanism: str
) -> np.ndarray:
    """Extract features using bidirectional mode (l=2)."""
    features = []
    for h in mechanism_windows[mechanism]:
        for m in mechanism_morphs[mechanism]:
            # Bidirectional mode = index 2
            features.append(h0_tensor[h, m, 2])
    return np.array(features)
```

---

## Mode Selection Guide

| Requirement | Recommended Mode |
|-------------|-----------------|
| Real-time processing | Forward (L₀) |
| Anticipation features | Backward (L₁) |
| Maximum accuracy | **Bidirectional (L₂)** |
| Structural analysis | **Bidirectional (L₂)** |
| Phase-sensitive | **Bidirectional (L₂)** |

---

**See Also**: [../h-law.md](../h-law.md) — H-Law overview
