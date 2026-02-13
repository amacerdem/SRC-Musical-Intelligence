# Contract: R3FeatureRegistry

**Source**: `mi_beta/ear/r3/_registry.py`
**Type**: Mutable registry with freeze semantics
**Purpose**: Collects `BaseSpectralGroup` instances, assigns contiguous index ranges, and produces a frozen `R3FeatureMap` for downstream consumers.

---

## 1. Lifecycle: register() -> freeze()

The registry follows a two-phase lifecycle:

```
Phase 1: MUTABLE                    Phase 2: FROZEN
┌─────────────────┐                 ┌─────────────────┐
│  R3FeatureRegistry                │  R3FeatureMap    │
│                  │   freeze()     │  (frozen=True)   │
│  register(A)     │ ───────────>  │  total_dim: 49   │
│  register(B)     │                │  groups: (...)   │
│  register(C)     │                │                  │
│  ...             │                │  [IMMUTABLE]     │
│                  │                │                  │
│  [MUTABLE]       │                └─────────────────┘
└─────────────────┘
```

**Rules**:
1. `register()` can only be called before `freeze()`.
2. `freeze()` can only be called once (idempotent -- returns cached result on subsequent calls).
3. After `freeze()`, `register()` raises `RuntimeError`.

---

## 2. R3FeatureRegistry Class

### 2.1 Constructor

```python
class R3FeatureRegistry:
    def __init__(self) -> None:
        self._groups: List[BaseSpectralGroup] = []
        self._frozen: Optional[R3FeatureMap] = None
```

Initializes an empty registry with no groups and no frozen state.

### 2.2 register()

```python
def register(self, group: BaseSpectralGroup) -> None:
    """Add a spectral group to the registry.

    Groups are appended in order; index ranges are assigned at freeze().
    Cannot register after freeze().
    """
    if self._frozen is not None:
        raise RuntimeError(
            "Cannot register groups after freeze(). "
            "Create a new R3FeatureRegistry if you need to modify."
        )
    # Check for duplicate group names
    for existing in self._groups:
        if existing.GROUP_NAME == group.GROUP_NAME:
            raise ValueError(
                f"Duplicate group name: {group.GROUP_NAME!r}. "
                f"Each group must have a unique GROUP_NAME."
            )
    self._groups.append(group)
```

**Preconditions**:
- Registry must not be frozen.
- `group.GROUP_NAME` must not duplicate any previously registered group.

**Postconditions**:
- Group is appended to the internal list (order preserved).
- Index ranges are NOT assigned yet (deferred to `freeze()`).

**Error cases**:
- `RuntimeError`: Attempting to register after `freeze()`.
- `ValueError`: Duplicate `GROUP_NAME`.

### 2.3 groups Property

```python
@property
def groups(self) -> List[BaseSpectralGroup]:
    """Registered groups (mutable list)."""
    return list(self._groups)
```

Returns a copy of the internal group list. Modifications to the returned list do not affect the registry.

### 2.4 freeze()

```python
def freeze(self) -> R3FeatureMap:
    """Finalize registry and assign contiguous index ranges.

    Returns:
        R3FeatureMap with total_dim and per-group metadata.
    """
    if self._frozen is not None:
        return self._frozen

    offset = 0
    group_infos: List[R3GroupInfo] = []

    for group in self._groups:
        dim = group.OUTPUT_DIM
        info = R3GroupInfo(
            name=group.GROUP_NAME,
            dim=dim,
            start=offset,
            end=offset + dim,
            feature_names=tuple(group.feature_names),
        )
        # Update the group's INDEX_RANGE to reflect its assigned position
        group.INDEX_RANGE = (offset, offset + dim)
        group_infos.append(info)
        offset += dim

    self._frozen = R3FeatureMap(
        total_dim=offset,
        groups=tuple(group_infos),
    )
    return self._frozen
```

**What freeze() does**:
1. Iterates over registered groups in registration order.
2. Assigns contiguous `INDEX_RANGE` to each group: `[offset, offset + dim)`.
3. Mutates each group's `INDEX_RANGE` attribute in-place.
4. Creates and caches a frozen `R3FeatureMap`.
5. Returns the frozen map.

**Key behavior: automatic index assignment**:

```
Register order:    A(7D)  B(5D)  C(9D)  D(4D)  E(24D)
                   ─────  ─────  ─────  ─────  ──────
After freeze():    [0:7]  [7:12] [12:21] [21:25] [25:49]
                   ═════════════════════════════════════
                              total_dim = 49
```

The offset accumulates: each group starts where the previous one ended. This guarantees contiguous, gap-free, non-overlapping index ranges.

**Idempotency**: Calling `freeze()` multiple times returns the same cached `R3FeatureMap`.

---

## 3. Dataclasses

### 3.1 R3GroupInfo

```python
@dataclass(frozen=True)
class R3GroupInfo:
    """Metadata for a registered R3 group."""
    name: str
    dim: int
    start: int
    end: int
    feature_names: Tuple[str, ...]
```

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | GROUP_NAME of the group |
| `dim` | `int` | OUTPUT_DIM (number of features) |
| `start` | `int` | Start index in R3 vector (inclusive) |
| `end` | `int` | End index in R3 vector (exclusive) |
| `feature_names` | `Tuple[str, ...]` | Ordered feature names for this group |

Invariant: `end - start == dim == len(feature_names)`.

### 3.2 R3FeatureMap

```python
@dataclass(frozen=True)
class R3FeatureMap:
    """Frozen registry snapshot -- total dim + group metadata."""
    total_dim: int
    groups: Tuple[R3GroupInfo, ...]

    def __repr__(self) -> str:
        lines = [f"R3FeatureMap(total_dim={self.total_dim}, groups=["]
        for g in self.groups:
            lines.append(f"  {g.name}: [{g.start}:{g.end}] ({g.dim}D)")
        lines.append("])")
        return "\n".join(lines)
```

| Field | Type | Description |
|-------|------|-------------|
| `total_dim` | `int` | Sum of all group dimensions |
| `groups` | `Tuple[R3GroupInfo, ...]` | Per-group metadata in registration order |

**Example repr output** (v1, 49D):

```
R3FeatureMap(total_dim=49, groups=[
  consonance: [0:7] (7D)
  energy: [7:12] (5D)
  timbre: [12:21] (9D)
  change: [21:25] (4D)
  interactions: [25:49] (24D)
])
```

---

## 4. Duplicate Name Prevention

The registry enforces unique GROUP_NAME across all registered groups:

```python
for existing in self._groups:
    if existing.GROUP_NAME == group.GROUP_NAME:
        raise ValueError(
            f"Duplicate group name: {group.GROUP_NAME!r}. "
            f"Each group must have a unique GROUP_NAME."
        )
```

This check occurs at `register()` time, providing an immediate error rather than a deferred one at `freeze()`.

Note: Feature name uniqueness (across groups) is NOT currently enforced. It is planned for Phase 6.

---

## 5. Usage Pattern

### 5.1 Standard Usage (via R3Extractor)

```python
# R3Extractor.__init__ handles the full lifecycle:
registry = R3FeatureRegistry()
for group in _discover_groups():       # auto-discovery
    registry.register(group)
feature_map = registry.freeze()        # assigns INDEX_RANGE
groups = registry.groups               # ordered list
```

### 5.2 Manual Usage

```python
from mi_beta.ear.r3._registry import R3FeatureRegistry

registry = R3FeatureRegistry()
registry.register(ConsonanceGroup())
registry.register(EnergyGroup())
registry.register(TimbreGroup())
registry.register(ChangeGroup())
registry.register(InteractionsGroup())

feature_map = registry.freeze()

assert feature_map.total_dim == 49
assert feature_map.groups[0].name == "consonance"
assert feature_map.groups[0].start == 0
assert feature_map.groups[0].end == 7

# After freeze, registration is blocked:
try:
    registry.register(SomeOtherGroup())
except RuntimeError as e:
    print(e)  # "Cannot register groups after freeze()."
```

---

## 6. Phase 6 Planned Changes

### 6.1 Validation at Freeze

Phase 6 adds validation assertions at the end of `freeze()`:

```python
def freeze(self) -> R3FeatureMap:
    # ... existing index assignment logic ...

    # Phase 6: validation
    feature_map = R3FeatureMap(total_dim=offset, groups=tuple(group_infos))
    assert offset == R3_DIM, f"Registry total_dim={offset} != R3_DIM={R3_DIM}"

    # Feature name uniqueness check
    all_names = []
    for info in group_infos:
        all_names.extend(info.feature_names)
    assert len(all_names) == len(set(all_names)), "Duplicate feature names"

    self._frozen = feature_map
    return self._frozen
```

This ensures:
- The total dimensionality matches the expected `R3_DIM` constant (128 in v2).
- All feature names across all groups are unique.

### 6.2 R3FeatureMap.feature_names Property

Phase 6 adds a convenience property to get all feature names in order:

```python
@property
def feature_names(self) -> Tuple[str, ...]:
    """All feature names in index order."""
    names = []
    for g in self.groups:
        names.extend(g.feature_names)
    return tuple(names)
```

### 6.3 Expected v2 FeatureMap

```
R3FeatureMap(total_dim=128, groups=[
  consonance: [0:7] (7D)
  energy: [7:12] (5D)
  timbre: [12:21] (9D)
  change: [21:25] (4D)
  interactions: [25:49] (24D)
  pitch_chroma: [49:65] (16D)
  rhythm_groove: [65:75] (10D)
  harmony_tonality: [75:87] (12D)
  information_surprise: [87:94] (7D)
  timbre_extended: [94:114] (20D)
  modulation_psychoacoustic: [114:128] (14D)
])
```
