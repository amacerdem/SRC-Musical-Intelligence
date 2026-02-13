# EventHorizon -- Interface Contract

**Version**: 2.0.0
**Updated**: 2026-02-13
**Code**: `mi_beta/ear/h3/horizon.py`
**Class**: `EventHorizon`

---

## 1. Purpose

EventHorizon is a thin wrapper that maps a horizon index (0-31) to its physical attributes: frame count, duration in milliseconds, and duration in seconds. It provides the temporal scale information that H3Extractor needs to determine window sizes for each horizon.

---

## 2. Constructor

```python
def __init__(self, index: int) -> None
```

| Parameter | Type | Constraints | Description |
|-----------|------|-------------|-------------|
| `index` | `int` | `0 <= index < 32` | Horizon index into HORIZON_FRAMES and HORIZON_MS |

**Assertion**: Raises `AssertionError` if `index` is outside [0, 31].

---

## 3. Properties

| Property | Return Type | Source | Description |
|----------|-------------|--------|-------------|
| `frames` | `int` | `HORIZON_FRAMES[self.index]` | Number of audio frames in this horizon window |
| `ms` | `float` | `HORIZON_MS[self.index]` | Duration of this horizon in milliseconds |
| `seconds` | `float` | `self.ms / 1000.0` | Duration of this horizon in seconds |

All properties are read-only lookups into the constant arrays defined in `mi_beta/core/constants.py`.

---

## 4. Constants Source

The horizon system is defined by two parallel arrays of 32 values:

- **`HORIZON_MS`**: 32 durations in milliseconds, spanning from 5.8ms (sub-beat) to 981,000ms (~16.4 minutes)
- **`HORIZON_FRAMES`**: Computed as `max(1, round(ms / 1000 * 172.27))` for each horizon

The frame rate of 172.27 fps is the MI system's standard analysis rate.

### Horizon Table (Selected)

| Index | ms | Frames | Approx. Duration |
|:-----:|-------:|:------:|-------------------|
| 0 | 5.8 | 1 | ~6 ms |
| 4 | 23.2 | 4 | ~23 ms |
| 8 | 93.0 | 16 | ~93 ms |
| 12 | 371.0 | 64 | ~371 ms |
| 16 | 1,486.0 | 256 | ~1.5 s |
| 20 | 5,944.0 | 1,024 | ~5.9 s |
| 24 | 23,778.0 | 4,096 | ~23.8 s |
| 28 | 122,625.0 | 21,129 | ~2.0 min |
| 31 | 981,000.0 | 168,982 | ~16.4 min |

For the complete 32-horizon table, see [../Bands/HorizonCatalog.md](../Bands/HorizonCatalog.md).

---

## 5. Representation

```python
def __repr__(self) -> str
```

Returns a formatted string showing the horizon index, frame count, and duration. Example output:

```
EventHorizon(index=12, frames=64, ms=371.0)
```

---

## 6. Usage in H3Extractor

H3Extractor creates an EventHorizon instance for each unique horizon in the demand tree:

```python
for h_idx, rml_set in tree.items():
    horizon = EventHorizon(h_idx)
    n_frames = min(horizon.frames, T)
    weights = compute_attention_weights(n_frames, device=device)
```

The `min(horizon.frames, T)` clamp ensures that horizons longer than the available audio are truncated to the sequence length.

---

## 7. Design Notes

- EventHorizon carries no mutable state. It is constructed, queried, and discarded within the H3Extractor loop.
- The class exists primarily for clarity and encapsulation: it converts an opaque integer index into named, self-documenting properties.
- No validation is performed on the underlying constant arrays; they are trusted as system invariants.

---

## 8. Dependencies

| Component | Role |
|-----------|------|
| `mi_beta/core/constants.py` | `N_HORIZONS` (=32), `HORIZON_FRAMES`, `HORIZON_MS` |

---

## 9. Cross-References

| Document | Location |
|----------|----------|
| H3Extractor (consumer) | [H3Extractor.md](H3Extractor.md) |
| Horizon Catalog | [../Bands/HorizonCatalog.md](../Bands/HorizonCatalog.md) |
| Band Specifications | [../Bands/](../Bands/) |
| AttentionKernel (uses frames) | [AttentionKernel.md](AttentionKernel.md) |
| Contracts Index | [00-INDEX.md](00-INDEX.md) |
| Code | `mi_beta/ear/h3/horizon.py` |
