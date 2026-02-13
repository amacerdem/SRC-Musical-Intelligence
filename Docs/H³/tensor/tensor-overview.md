# H⁰ Tensor Overview

**Dimension**: 2,304D
**Formula**: H⁰ = H ⊗ M ⊗ L
**Position**: SRC⁹[256:2560] in 8,192D Manifold

---

## Tensor Product Definition

H⁰ is defined as the **tensor product** of three independent components:

```
H⁰ = H ⊗ M ⊗ L

where:
    H = Event Horizon    (32 temporal windows)
    M = H-Morph          (24 morphological parameters)
    L = H-Law            (3 causal attention modes)

Dimension:
    dim(H⁰) = dim(H) × dim(M) × dim(L)
             = 32 × 24 × 3
             = 2,304D
```

---

## Tensor Shape

```
H⁰ Tensor: (32, 24, 3)

Axis 0: Event Horizon (h) — WHAT temporal scale
        h ∈ [0, 31] — 32 windows from 25ms to 981s

Axis 1: H-Morph (m) — WHAT features to extract
        m ∈ [0, 23] — 24 morphological parameters

Axis 2: H-Law (l) — HOW attention flows
        l ∈ [0, 2] — 3 causal modes
```

---

## Tensor Indexing

### 3D Indexing

```python
H0[h, m, l] = scalar value for:
    h ∈ [0, 31]   Event Horizon window index
    m ∈ [0, 23]   H-Morph parameter index
    l ∈ [0, 2]    H-Law causal mode index
```

### Flat Indexing

For storage in the 8,192D manifold:

```python
flat_idx = 256 + (h × 72) + (m × 3) + l

where:
    256 = S⁰ offset (H⁰ starts after S⁰)
    72 = 24 × 3 (M × L stride)
    3 = L stride
```

---

## Computational Formula

```python
def compute_h0(signal: np.ndarray, t_current: float) -> np.ndarray:
    """
    Compute H⁰ tensor for current time.

    Args:
        signal: Historical signal values (time, 256) from S⁰
        t_current: Current timestamp in seconds

    Returns:
        H⁰ tensor of shape (32, 24, 3)
    """
    h0 = np.zeros((32, 24, 3))

    for h, window_ms in enumerate(EVENT_HORIZONS):  # 32 windows
        window_sec = window_ms / 1000.0

        for l, mode in enumerate(['forward', 'backward', 'bidirectional']):
            # Extract time range based on mode
            if mode == 'forward':
                t_start, t_end = t_current - window_sec, t_current
            elif mode == 'backward':
                t_start, t_end = t_current, t_current + window_sec
            else:  # bidirectional
                t_start, t_end = t_current - window_sec/2, t_current + window_sec/2

            # Get signal in window
            windowed_signal = extract_window(signal, t_start, t_end)

            # Apply H-Law attention
            attention = compute_hlaw_attention(windowed_signal, mode, window_sec)
            weighted_signal = windowed_signal * attention

            for m, morph_func in enumerate(MORPH_FUNCTIONS):  # 24 parameters
                h0[h, m, l] = morph_func(weighted_signal)

    return h0
```

---

## Tensor Properties

| Property | Value |
|----------|-------|
| Total dimensions | 2,304 |
| Per window | 72 (24 × 3) |
| Per morph parameter | 96 (32 × 3) |
| Per H-Law mode | 768 (32 × 24) |

---

## Memory Layout

```
H⁰ in SRC⁹ manifold [256:2560]:

Index    │ H  │ M  │ L  │ Description
─────────┼────┼────┼────┼────────────────────────────────
256      │ 0  │ 0  │ 0  │ H₀, value, forward
257      │ 0  │ 0  │ 1  │ H₀, value, backward
258      │ 0  │ 0  │ 2  │ H₀, value, bidirectional
259      │ 0  │ 1  │ 0  │ H₀, mean, forward
...      │    │    │    │
327      │ 0  │ 23 │ 2  │ H₀, troughs, bidirectional
328      │ 1  │ 0  │ 0  │ H₁, value, forward
...      │    │    │    │
2559     │ 31 │ 23 │ 2  │ H₃₁, troughs, bidirectional
```

---

## Downstream Consumption

H⁰'s 2,304D tensor is consumed by two branches:

| Branch | Mechanism | Extraction | Output |
|--------|-----------|------------|--------|
| **C⁰** | HC⁰ | Selects specific (h, m, l) combinations | 512D |
| **R⁰** | HR⁰ | Selects specific (h, m, l) combinations | 256D |

See:
- [downstream-hc0.md](downstream-hc0.md) — C⁰ extraction
- [downstream-hr0.md](downstream-hr0.md) — R⁰ extraction

---

**Implementation**: `Pipeline/D0/h0/h0_extractor.py`
