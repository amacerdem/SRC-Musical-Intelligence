# Contract: R3Extractor

**Source**: `mi_beta/ear/r3/__init__.py`
**Type**: Orchestrator class
**Purpose**: Auto-discovers spectral groups from subdirectories, registers them into `R3FeatureRegistry`, and orchestrates the `mel -> R3Output` extraction pipeline.

---

## 1. Architecture Overview

```
mi_beta/ear/r3/
├── __init__.py          <-- R3Extractor lives here
├── _registry.py         <-- R3FeatureRegistry, R3FeatureMap, R3GroupInfo
├── psychoacoustic/      <-- Group A (Consonance)
│   └── __init__.py
├── dsp/                 <-- Groups B (Energy), C (Timbre), D (Change)
│   └── __init__.py
├── cross_domain/        <-- Group E (Interactions)
│   └── __init__.py
└── extensions/          <-- User-added groups
    ├── __init__.py
    └── _template.py
```

---

## 2. Auto-Discovery Mechanism

### 2.1 _SUBDIRECTORY_NAMES

```python
_SUBDIRECTORY_NAMES = ("psychoacoustic", "dsp", "cross_domain", "extensions")
```

These subdirectories are scanned in order. The scan order determines the concatenation order of groups in the R3 vector:

| Scan Position | Subdirectory | Groups Discovered | Index Range (v1) |
|:---:|--------------|-------------------|:---:|
| 1 | `psychoacoustic/` | A: Consonance (7D) | `[0:7]` |
| 2 | `dsp/` | B: Energy (5D), C: Timbre (9D), D: Change (4D) | `[7:25]` |
| 3 | `cross_domain/` | E: Interactions (24D) | `[25:49]` |
| 4 | `extensions/` | (user-defined groups) | `[49:...]` |

### 2.2 _discover_groups()

```python
def _discover_groups() -> List[BaseSpectralGroup]:
    """Import subdirectory __init__.py modules and collect exported groups.

    Each subdirectory's __init__.py is expected to define an __all__ list
    of BaseSpectralGroup subclasses. They are instantiated and returned
    in the order: psychoacoustic -> dsp -> cross_domain -> extensions.
    """
    groups: List[BaseSpectralGroup] = []

    for subdir in _SUBDIRECTORY_NAMES:
        try:
            mod = importlib.import_module(f".{subdir}", package=__name__)
        except ImportError:
            continue

        # Collect all BaseSpectralGroup subclasses exported by the module
        for attr_name in getattr(mod, "__all__", []):
            cls = getattr(mod, attr_name, None)
            if cls is None:
                continue
            if isinstance(cls, type) and issubclass(cls, BaseSpectralGroup) and cls is not BaseSpectralGroup:
                groups.append(cls())

    return groups
```

**Discovery protocol**:

1. For each subdirectory name in `_SUBDIRECTORY_NAMES`:
   - Attempt to import the subdirectory as a Python module (via `importlib.import_module`).
   - If the import fails (`ImportError`), skip silently. This allows optional subdirectories.

2. For each module that imports successfully:
   - Read its `__all__` list.
   - For each name in `__all__`, retrieve the attribute from the module.
   - If the attribute is a class, is a subclass of `BaseSpectralGroup`, and is not `BaseSpectralGroup` itself:
     - Instantiate it with no arguments: `cls()`.
     - Append the instance to the group list.

3. Return all discovered groups in order.

**Key points**:
- The `__all__` list controls which groups are exported. Groups not in `__all__` are ignored.
- Groups are instantiated at discovery time (in `R3Extractor.__init__`).
- `ImportError` on any subdirectory is silently swallowed, enabling graceful degradation.
- The `BaseSpectralGroup` ABC itself is filtered out, preventing accidental registration.

---

## 3. R3Extractor Class

### 3.1 Constructor

```python
class R3Extractor:
    """Orchestrates all R3 spectral groups.

    Groups are discovered from psychoacoustic/, dsp/, cross_domain/,
    and extensions/ subdirectories using the _registry.
    """

    def __init__(self, config: MIBetaConfig = MI_BETA_CONFIG) -> None:
        self.config = config

        # Discover and register groups
        self._registry = R3FeatureRegistry()
        for group in _discover_groups():
            self._registry.register(group)

        # Freeze to assign index ranges
        self._feature_map = self._registry.freeze()
        self.groups = self._registry.groups
```

**Initialization sequence**:

```
1. _discover_groups()          -- Import subdirectories, collect BaseSpectralGroup instances
2. registry.register(group)    -- Register each group (checks for duplicate names)
3. registry.freeze()           -- Assign contiguous INDEX_RANGE to each group
4. Store groups and feature_map
```

After initialization, `R3Extractor` holds:
- `self._registry`: The frozen registry.
- `self._feature_map`: The `R3FeatureMap` snapshot (total_dim, per-group info).
- `self.groups`: Ordered list of `BaseSpectralGroup` instances with assigned INDEX_RANGE.

### 3.2 feature_map Property

```python
@property
def feature_map(self) -> R3FeatureMap:
    """Frozen feature map with index ranges."""
    return self._feature_map
```

### 3.3 extract() Method

```python
def extract(self, mel: Tensor) -> R3Output:
    """Extract R3 features from mel spectrogram.

    Args:
        mel: (B, N_MELS, T) log-mel spectrogram

    Returns:
        R3Output with features (B, T, total_dim)
    """
    parts = []
    names: List[str] = []
    for group in self.groups:
        feat = group.compute(mel)  # (B, T, group_dim)
        parts.append(feat)
        names.extend(group.feature_names)

    features = torch.cat(parts, dim=-1)  # (B, T, total_dim)
    return R3Output(features=features, feature_names=tuple(names))
```

**Extraction pipeline (current)**:

```
Input: mel (B, 128, T)
           |
           v
    ┌──────────────┐
    │  For each     │
    │  group in     │──> group.compute(mel) -> (B, T, group_dim)
    │  order:       │
    └──────────────┘
           |
           v
    torch.cat(parts, dim=-1) -> (B, T, total_dim)
           |
           v
    R3Output(features=..., feature_names=(...))
```

**Current behavior**: Sequential iteration over groups. Each group receives the same `mel` input. There is no dependency injection -- groups that need other groups' outputs (like E needing A-D) use internal proxy computations.

### 3.4 feature_names Property

```python
@property
def feature_names(self) -> List[str]:
    names: List[str] = []
    for group in self.groups:
        names.extend(group.feature_names)
    return names
```

Returns all feature names in index order, concatenated across all groups.

### 3.5 total_dim Property

```python
@property
def total_dim(self) -> int:
    return self._feature_map.total_dim
```

Returns the total dimensionality of the R3 vector (currently 49).

---

## 4. R3Output Contract

The `extract()` method returns an `R3Output` (defined in `mi_beta/core/types.py`):

```python
R3Output(
    features=features,         # Tensor: (B, T, total_dim)
    feature_names=tuple(names) # Tuple[str, ...]: length == total_dim
)
```

**Output guarantees**:
- `features.shape[-1] == total_dim == sum(group.OUTPUT_DIM for group in groups)`.
- `len(feature_names) == total_dim`.
- Features at indices `[group.start_index : group.end_index]` correspond to `group.feature_names`.
- Values are in `[0, 1]` (per the BaseSpectralGroup compute() contract).

---

## 5. Phase 6 Planned Changes

### 5.1 Domain-Based Discovery

Phase 6 extends `_SUBDIRECTORY_NAMES` to include new subdirectories for groups F-K:

```python
# Current:
_SUBDIRECTORY_NAMES = ("psychoacoustic", "dsp", "cross_domain", "extensions")

# Phase 6 (proposed):
_SUBDIRECTORY_NAMES = (
    "psychoacoustic",    # A: Consonance
    "dsp",               # B: Energy, C: Timbre, D: Change
    "cross_domain",      # E: Interactions
    "pitch",             # F: Pitch & Chroma
    "rhythm",            # G: Rhythm & Groove
    "harmony",           # H: Harmony & Tonality
    "information",       # I: Information & Surprise
    "timbre_extended",   # J: Timbre Extended
    "modulation",        # K: Modulation & Psychoacoustic
    "extensions",        # User extensions (always last)
)
```

Alternatively, new groups F-K could be placed in `extensions/` without modifying `_SUBDIRECTORY_NAMES`.

### 5.2 Dependency-Aware Compute (Stage-Ordered Extraction)

The current `extract()` is sequential with no dependency awareness. Phase 6 introduces a 3-stage DAG:

```python
class R3Extractor:
    STAGE_ORDER = {
        1: ['consonance', 'energy', 'timbre', 'change',
            'pitch_chroma', 'timbre_extended', 'modulation_psychoacoustic'],
        2: ['interactions', 'rhythm_groove', 'harmony_tonality'],
        3: ['information_surprise'],
    }

    def extract(self, mel: Tensor) -> R3Output:
        outputs = {}
        for stage in sorted(self.STAGE_ORDER):
            stage_groups = [g for g in self.groups
                          if g.GROUP_NAME in self.STAGE_ORDER[stage]]
            for group in stage_groups:
                if hasattr(group, 'compute_with_deps'):
                    result = group.compute_with_deps(mel, outputs)
                else:
                    result = group.compute(mel)
                outputs[group.GROUP_NAME] = result

        # Concat in registration order
        ordered = [outputs[g.GROUP_NAME] for g in self.groups]
        features = torch.cat(ordered, dim=-1)  # (B, T, 128)
        names = []
        for g in self.groups:
            names.extend(g.feature_names)
        return R3Output(features=features, feature_names=tuple(names))
```

**Stage execution**:

```
Stage 1 (parallel, mel-only):    A, B, C, D, F, J, K
                                       |
Stage 2 (parallel, deps):        E(A,B,C,D), G(B[11]), H(F chroma)
                                       |
Stage 3:                          I(F chroma, G onset, H key)
                                       |
Concat:                           torch.cat([A..K]) -> (B, T, 128)
```

**Backward compatibility**: Groups that implement only `compute(mel)` continue to work. The `compute_with_deps()` method defaults to calling `compute(mel)` if not overridden.

### 5.3 GPU Parallelization

Within each stage, groups can execute in parallel on separate CUDA streams:

```python
# Phase 6 (proposed):
with torch.cuda.stream(stream_pool):
    for group in stage_groups:
        stream = next(stream_pool)
        with torch.cuda.stream(stream):
            outputs[group.GROUP_NAME] = group.compute(mel)
torch.cuda.synchronize()  # Wait for all streams in this stage
```

This is the mechanism that achieves the 3-stage parallel execution described in `R3-V2-DESIGN.md` Section 3.3.

---

## 6. Usage Example

```python
from mi_beta.ear.r3 import R3Extractor

# Initialize (auto-discovers groups)
extractor = R3Extractor()

# Check configuration
print(extractor.total_dim)          # 49 (v1) or 128 (v2)
print(extractor.feature_names[:7])  # ['roughness', 'sethares_dissonance', ...]
print(extractor.feature_map)        # R3FeatureMap(total_dim=49, groups=[...])

# Extract features
mel = torch.randn(2, 128, 1000)    # (batch=2, mel_bins=128, frames=1000)
output = extractor.extract(mel)

print(output.features.shape)        # torch.Size([2, 1000, 49])
print(len(output.feature_names))    # 49
```
