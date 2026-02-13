# H⁰ Tensor Indexing

**Formula**: `flat_idx = 256 + (h × 72) + (m × 3) + l`

---

## Index Components

### Event Horizon Index (h)

```
h ∈ [0, 31] — 32 temporal windows

h │ Window Duration │ Scale
──┼─────────────────┼─────────────
0 │ 25ms            │ Gamma
1 │ 50ms            │ Gamma
2 │ 75ms            │ Alpha-Beta
3 │ 100ms           │ Alpha-Beta
4 │ 125ms           │ Alpha-Beta
5 │ 150ms           │ Theta
6 │ 200ms           │ Theta
7 │ 250ms           │ Theta
8 │ 300ms           │ Syllable
9 │ 350ms           │ Syllable
10│ 400ms           │ Syllable
11│ 500ms           │ Syllable
12│ 525ms           │ Beat
13│ 600ms           │ Beat
14│ 730ms           │ Beat
15│ 800ms           │ Beat
16│ 1000ms          │ Beat
17│ 1250ms          │ Phrase
18│ 2000ms          │ Phrase
19│ 3000ms          │ Phrase
20│ 5000ms          │ Phrase
21│ 7500ms          │ Section
22│ 15s             │ Section
23│ 25s             │ Section
24│ 36s             │ Section
25│ 100s            │ Structural
26│ 200s            │ Structural
27│ 300s            │ Structural
28│ 414s            │ Structural
29│ 500s            │ Piece
30│ 700s            │ Piece
31│ 981s            │ Piece
```

### H-Morph Index (m)

```
m ∈ [0, 23] — 24 morphological parameters

m  │ Parameter         │ Domain
───┼───────────────────┼───────────
0  │ value             │ Value
1  │ mean              │ Value
2  │ std               │ Value
3  │ min               │ Value
4  │ max               │ Value
5  │ range             │ Value
6  │ skew              │ Value
7  │ kurtosis          │ Value
8  │ velocity          │ Derivative
9  │ velocity_mean     │ Derivative
10 │ velocity_std      │ Derivative
11 │ acceleration      │ Derivative
12 │ acceleration_mean │ Derivative
13 │ jerk              │ Derivative
14 │ jerk_mean         │ Derivative
15 │ smoothness        │ Derivative
16 │ curvature         │ Shape
17 │ periodicity       │ Shape
18 │ trend             │ Shape
19 │ stability         │ Shape
20 │ entropy           │ Shape
21 │ zero_crossings    │ Shape
22 │ peaks             │ Shape
23 │ troughs           │ Shape
```

### H-Law Index (l)

```
l ∈ [0, 2] — 3 causal attention modes

l │ Mode          │ Direction
──┼───────────────┼─────────────────
0 │ Forward       │ Past → Present
1 │ Backward      │ Present → Future
2 │ Bidirectional │ Past ↔ Future
```

---

## Flattening Formula

### 3D → 1D

```python
def h0_flat_index(h: int, m: int, l: int) -> int:
    """Convert (h, m, l) to flat manifold index."""
    assert 0 <= h < 32, f"h must be in [0, 31], got {h}"
    assert 0 <= m < 24, f"m must be in [0, 23], got {m}"
    assert 0 <= l < 3, f"l must be in [0, 2], got {l}"

    return 256 + (h * 72) + (m * 3) + l
```

### 1D → 3D

```python
def h0_unflat_index(flat_idx: int) -> tuple[int, int, int]:
    """Convert flat manifold index to (h, m, l)."""
    assert 256 <= flat_idx < 2560, f"Index must be in [256, 2559]"

    local_idx = flat_idx - 256  # Remove S⁰ offset

    h = local_idx // 72
    remainder = local_idx % 72
    m = remainder // 3
    l = remainder % 3

    return h, m, l
```

---

## Example Calculations

### Example 1: H₀, value, forward

```
h = 0, m = 0, l = 0
flat_idx = 256 + (0 × 72) + (0 × 3) + 0 = 256
```

### Example 2: H₁₅ (800ms), velocity (m=8), bidirectional

```
h = 15, m = 8, l = 2
flat_idx = 256 + (15 × 72) + (8 × 3) + 2
         = 256 + 1080 + 24 + 2
         = 1362
```

### Example 3: H₃₁ (981s), troughs (m=23), bidirectional

```
h = 31, m = 23, l = 2
flat_idx = 256 + (31 × 72) + (23 × 3) + 2
         = 256 + 2232 + 69 + 2
         = 2559  (last H⁰ index)
```

---

## Slice Patterns

### All modes for a single (h, m)

```python
def get_all_modes(h: int, m: int) -> list[int]:
    """Get indices for all 3 modes of a specific (h, m)."""
    base = 256 + (h * 72) + (m * 3)
    return [base, base + 1, base + 2]
```

### All parameters for a single window

```python
def get_window_slice(h: int) -> slice:
    """Get slice for all 72 dimensions of window h."""
    start = 256 + (h * 72)
    return slice(start, start + 72)
```

### All forward mode values

```python
def get_forward_indices() -> list[int]:
    """Get all indices where l = 0 (forward mode)."""
    indices = []
    for h in range(32):
        for m in range(24):
            indices.append(256 + (h * 72) + (m * 3) + 0)
    return indices  # 768 indices
```

---

## Index Ranges by Component

| Component | Index Range | Count |
|-----------|-------------|-------|
| Full H⁰ | [256:2560] | 2,304 |
| Window H₀ | [256:328] | 72 |
| Window H₃₁ | [2488:2560] | 72 |
| Forward mode | Every 3rd from 256 | 768 |
| Backward mode | Every 3rd from 257 | 768 |
| Bidirectional mode | Every 3rd from 258 | 768 |

---

**Implementation**: `Pipeline/D0/h0/h0_extractor.py`
