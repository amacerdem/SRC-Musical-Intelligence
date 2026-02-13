# H⁰ Memory Requirements

**History Buffer**: ~173 MB
**Per-Frame Output**: ~9 KB

---

## History Buffer

H⁰ requires a history buffer to compute temporal features across all 32 windows.

### Maximum Window Size

```
H₃₁ = 981 seconds = 16.35 minutes

This is the longest temporal context needed.
```

### Buffer Calculation

```
Sample Rate:    172 Hz (5.8ms per frame, from S⁰)
Max Window:     981 seconds
Buffer Frames:  981 × 172 = 168,732 frames

Per Frame:      256D × 4 bytes (float32) = 1,024 bytes = 1 KB
Total Buffer:   168,732 × 1,024 = 172,781,568 bytes ≈ 173 MB
```

### Buffer Implementation

```python
class H0HistoryBuffer:
    """Ring buffer for H⁰ temporal history."""

    def __init__(self, max_seconds: float = 981.0, sample_rate: float = 172.0):
        self.max_frames = int(max_seconds * sample_rate)  # 168,732
        self.feature_dim = 256  # S⁰ input dimension

        # Pre-allocate buffer
        self.buffer = np.zeros((self.max_frames, self.feature_dim), dtype=np.float32)
        self.timestamps = np.zeros(self.max_frames, dtype=np.float64)
        self.head = 0  # Current write position
        self.filled = 0  # Number of valid frames

    def add_frame(self, features: np.ndarray, timestamp: float):
        """Add a new frame to the buffer."""
        self.buffer[self.head] = features
        self.timestamps[self.head] = timestamp
        self.head = (self.head + 1) % self.max_frames
        self.filled = min(self.filled + 1, self.max_frames)

    def get_window(self, t_start: float, t_end: float) -> np.ndarray:
        """Extract frames within time window."""
        # Find indices within time range
        mask = (self.timestamps >= t_start) & (self.timestamps <= t_end)
        return self.buffer[mask]
```

---

## Output Tensor

### Per-Frame Output

```
H⁰ Tensor:      32 × 24 × 3 = 2,304 dimensions
Bytes per dim:  4 (float32)
Per Frame:      2,304 × 4 = 9,216 bytes ≈ 9 KB
```

### Storage in Manifold

```
Position:       SRC⁹[256:2560]
Dimension:      2,304D
Per Song:       (frames × 9,216) bytes

Example (5-minute song at 172 Hz):
  Frames:       300 × 172 = 51,600 frames
  H⁰ Size:      51,600 × 9,216 = 475,545,600 bytes ≈ 476 MB
```

---

## GPU Memory Considerations

### Batch Processing

```python
# Typical batch sizes for GPU
BATCH_SIZE = 32  # frames

# Memory per batch
batch_memory = BATCH_SIZE * (
    256 * 168_732 +   # Input buffer (S⁰ history)
    2_304             # Output tensor
) * 4  # float32

# ≈ 173 MB history + negligible output
# Total ≈ 173 MB per batch
```

### Sliding Window Optimization

```python
# Instead of storing full history, use sliding windows
# for each temporal scale independently

WINDOW_SIZES_MS = [25, 50, 75, 100, ...]  # 32 windows

def compute_h0_efficient(signal_buffer, window_sizes, sample_rate):
    """Compute H⁰ using minimal memory per window."""
    h0 = np.zeros((32, 24, 3))

    for h, window_ms in enumerate(window_sizes):
        # Only extract the window we need
        window_frames = int(window_ms / 1000 * sample_rate)
        window_signal = signal_buffer[-window_frames:]

        # Compute for this window
        for m, morph_fn in enumerate(MORPH_FUNCTIONS):
            for l, mode in enumerate(['forward', 'backward', 'bidirectional']):
                attention = compute_attention(window_signal, mode)
                h0[h, m, l] = morph_fn(window_signal * attention)

    return h0
```

---

## Memory by Temporal Scale

| Scale | Windows | Max Buffer | Memory |
|-------|---------|------------|--------|
| Gamma | H₀-H₁ | 50ms | 9 frames × 1KB = 9KB |
| Alpha-Beta | H₂-H₄ | 125ms | 22 frames × 1KB = 22KB |
| Theta | H₅-H₇ | 250ms | 43 frames × 1KB = 43KB |
| Syllable | H₈-H₁₁ | 500ms | 86 frames × 1KB = 86KB |
| Beat | H₁₂-H₁₆ | 1000ms | 172 frames × 1KB = 172KB |
| Phrase | H₁₇-H₂₀ | 5s | 860 frames × 1KB = 860KB |
| Section | H₂₁-H₂₄ | 36s | 6,192 frames × 1KB = 6.2MB |
| Structural | H₂₅-H₂₈ | 414s | 71,208 frames × 1KB = 71MB |
| Piece | H₂₉-H₃₁ | 981s | 168,732 frames × 1KB = 173MB |

**Total (all scales)**: Dominated by Piece scale ≈ **173 MB**

---

## Optimization Strategies

### 1. Lazy Loading

Only compute long windows (Structural, Piece) when needed:

```python
# Short windows: always available
# Long windows: compute on demand for structural analysis
```

### 2. Hierarchical Caching

```python
# Cache intermediate results
# Phrase-level features can derive Section-level
# Reduces redundant computation
```

### 3. Resolution Reduction

```python
# For very long windows, reduce temporal resolution
# H₃₁ (981s) doesn't need 172 Hz resolution
# 10 Hz is sufficient for piece-level analysis
```

---

**Implementation**: `Pipeline/D0/h0/h0_extractor.py`
