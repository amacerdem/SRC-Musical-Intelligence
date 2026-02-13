# R3 Extension Guide

**Version**: 2.0.0
**Audience**: Developers extending the R3 spectral feature vector
**Updated**: 2026-02-13

---

## Table of Contents

1. [Overview](#1-overview)
2. [Adding a New Feature to an Existing Group](#2-adding-a-new-feature-to-an-existing-group)
3. [Adding a New Group to an Existing Domain](#3-adding-a-new-group-to-an-existing-domain)
4. [Adding a New Domain](#4-adding-a-new-domain)
5. [BaseSpectralGroup Contract Checklist](#5-basespectralgroup-contract-checklist)
6. [Registration and Auto-Discovery](#6-registration-and-auto-discovery)
7. [Example: Adding an L-SpatialAudio Group](#7-example-adding-an-l-spatialaudio-group)
8. [Testing Requirements](#8-testing-requirements)
9. [Reference: _template.py Pattern](#9-reference-_templatepy-pattern)

---

## 1. Overview

The R3 spectral architecture is designed to be extensible without modifying core files. The primary extension mechanism is:

1. Create a Python class that subclasses `BaseSpectralGroup`
2. Implement the required interface (GROUP_NAME, OUTPUT_DIM, feature_names, compute)
3. Export it from the appropriate `__init__.py`
4. The `R3FeatureRegistry` auto-discovers and assigns index ranges

**Key principle**: Groups are self-describing. Each group declares its own name, dimension count, and feature names. The registry handles index assignment and validation.

---

## 2. Adding a New Feature to an Existing Group

To add a feature to an existing group (e.g., adding a new consonance measure to Group A):

### Step 1: Locate the Group Implementation

```
mi_beta/ear/r3/
  psychoacoustic/
    consonance.py          <-- Group A implementation
  dsp/
    energy.py              <-- Group B implementation
    timbre.py              <-- Group C implementation
    change.py              <-- Group D implementation
  cross_domain/
    interactions.py        <-- Group E implementation
  extensions/
    pitch_chroma.py        <-- Group F implementation
    ...
```

### Step 2: Update the Group Class

1. Increment `OUTPUT_DIM` by the number of new features
2. Add the new feature name(s) to the `feature_names` property
3. Compute the new feature(s) in the `compute()` method
4. Concatenate with existing features

```python
class ConsonanceGroup(BaseSpectralGroup):
    GROUP_NAME = "consonance"
    OUTPUT_DIM = 8  # was 7, now 8 with new feature

    @property
    def feature_names(self) -> List[str]:
        return [
            "roughness", "sethares_dissonance", "helmholtz_kang",
            "stumpf_fusion", "sensory_pleasantness", "inharmonicity",
            "harmonic_deviation",
            "new_consonance_feature",  # <-- added
        ]

    def compute(self, mel: Tensor) -> Tensor:
        # ... existing computation ...
        new_feat = self._compute_new_feature(mel)  # (B, T, 1)
        return torch.cat([existing_features, new_feat], dim=-1)
```

### Step 3: Update Documentation

- Update the group's entry in `Docs/R3/Registry/FeatureCatalog.md`
- Update the dimension map in `Docs/R3/Registry/DimensionMap.md`
- Note the change in `Docs/R3/CHANGELOG.md`

**Warning**: Adding features to existing groups A-E changes the total dimension and shifts downstream indices. This is a breaking change that requires updating all C3 model documentation. Prefer adding new groups instead.

---

## 3. Adding a New Group to an Existing Domain

This is the recommended way to extend R3. New groups are appended after existing groups, preserving all existing indices.

### Step 1: Copy the Template

```bash
cp mi_beta/ear/r3/extensions/_template.py mi_beta/ear/r3/extensions/my_new_group.py
```

### Step 2: Implement the Group

Edit `my_new_group.py`:

```python
from __future__ import annotations
from typing import List
import torch
from torch import Tensor
from ....contracts import BaseSpectralGroup


class MyNewGroup(BaseSpectralGroup):
    """Description of what this group computes."""

    GROUP_NAME = "my_new_group"       # Must be unique across all groups
    DOMAIN = "spectral"               # One of the 6 domains
    OUTPUT_DIM = 5                    # Number of features
    INDEX_RANGE = (0, 0)              # Auto-assigned by registry.freeze()

    @property
    def feature_names(self) -> List[str]:
        return [
            "feature_alpha",
            "feature_beta",
            "feature_gamma",
            "feature_delta",
            "feature_epsilon",
        ]

    def compute(self, mel: Tensor) -> Tensor:
        """Compute features from mel spectrogram.

        Args:
            mel: (B, N_MELS, T) log-mel spectrogram

        Returns:
            (B, T, OUTPUT_DIM) features in [0, 1]
        """
        B, N, T = mel.shape
        # ... your computation ...
        return features.clamp(0, 1)  # (B, T, 5)
```

### Step 3: Export from `__init__.py`

Edit `mi_beta/ear/r3/extensions/__init__.py`:

```python
from .my_new_group import MyNewGroup

__all__ = [
    # ... existing exports ...
    "MyNewGroup",
]
```

### Step 4: Verify Registration

```python
from mi_beta.ear.r3 import R3Extractor

extractor = R3Extractor()
print(extractor.feature_map)
# Should show your new group with auto-assigned index range
```

### Step 5: Update Documentation

- Add the group to `Docs/R3/Registry/FeatureCatalog.md`
- Add index ranges to `Docs/R3/Registry/DimensionMap.md`
- Update `Docs/R3/00-INDEX.md` architecture summary table
- Add entry to `Docs/R3/CHANGELOG.md`

---

## 4. Adding a New Domain

Domains are organizational categories. To add a new domain:

### Step 1: Create the Domain Directory

```bash
mkdir -p mi_beta/ear/r3/new_domain/
touch mi_beta/ear/r3/new_domain/__init__.py
```

### Step 2: Register the Subdirectory

Edit `mi_beta/ear/r3/__init__.py` to add the new subdirectory to the scan order:

```python
_SUBDIRECTORY_NAMES = (
    "psychoacoustic", "dsp", "cross_domain", "extensions",
    "new_domain",  # <-- added
)
```

### Step 3: Create Groups in the Domain

Place `BaseSpectralGroup` subclasses in the new directory and export them via `__all__` in the domain's `__init__.py`.

### Step 4: Create Documentation Directory

```bash
mkdir -p "Docs/R3/Domains/NewDomain/"
```

**Note**: Adding a new domain is a significant architectural decision. The current 6-domain taxonomy (Psychoacoustic, Spectral, Tonal, Temporal, Information, CrossDomain) is designed to be comprehensive. Consult the architecture team before adding new domains.

---

## 5. BaseSpectralGroup Contract Checklist

Every `BaseSpectralGroup` subclass must satisfy the following contract:

### Required Class Attributes

| Attribute | Type | Constraint | Example |
|-----------|------|------------|---------|
| `GROUP_NAME` | `str` | Non-empty, unique across all groups | `"pitch_chroma"` |
| `DOMAIN` | `str` | One of the recognized domain names | `"tonal"` |
| `OUTPUT_DIM` | `int` | > 0 | `16` |
| `INDEX_RANGE` | `Tuple[int, int]` | Set to `(0, 0)` -- auto-assigned by registry | `(0, 0)` |

### Required Methods

| Method | Signature | Contract |
|--------|-----------|----------|
| `compute` | `(self, mel: Tensor) -> Tensor` | Input: `(B, 128, T)`. Output: `(B, T, OUTPUT_DIM)`. Values in `[0, 1]`. |
| `feature_names` (property) | `-> List[str]` | Length must equal `OUTPUT_DIM`. Names in `snake_case`. |

### Validation Rules

The `validate()` method on `BaseSpectralGroup` checks:

1. `GROUP_NAME` is non-empty
2. `OUTPUT_DIM > 0`
3. `INDEX_RANGE[1] - INDEX_RANGE[0] == OUTPUT_DIM` (after freeze)
4. `len(feature_names) == OUTPUT_DIM`

### Compute Contract Details

```python
def compute(self, mel: Tensor) -> Tensor:
    """
    Input:
        mel: (B, N_MELS, T) log-mel spectrogram
        - B: batch size (variable)
        - N_MELS: 128 mel bins
        - T: time frames (variable)
        - Values: log1p-normalized mel spectrogram
        - Device: CPU or CUDA (must handle both)

    Output:
        features: (B, T, OUTPUT_DIM)
        - Values should be in [0, 1] range
        - Must be differentiable (use torch operations)
        - Must handle any T >= 1
        - Must be deterministic (same input -> same output)

    Performance:
        - Target: < 1 ms/frame on GPU for groups < 20D
        - Use register_buffer() for pre-computed constants
        - Avoid Python loops over frames; use vectorized operations
    """
```

### Pre-computed Constants

Use `register_buffer` for any pre-computed matrices or constants:

```python
class MyGroup(BaseSpectralGroup):
    def __init__(self):
        super().__init__()
        # Pre-compute and register as buffer
        matrix = self._build_transform_matrix()
        self.register_buffer("transform_matrix", matrix)
```

**Note**: `BaseSpectralGroup` does not inherit from `nn.Module`, so `register_buffer` must be implemented by the group if GPU transfer is needed. For simple groups, storing tensors as attributes is acceptable.

---

## 6. Registration and Auto-Discovery

### Discovery Flow

```
R3Extractor.__init__()
    |
    +-- _discover_groups()
    |     |
    |     +-- For subdir in ("psychoacoustic", "dsp", "cross_domain", "extensions"):
    |     |     import_module(f".{subdir}", package="mi_beta.ear.r3")
    |     |     for attr_name in module.__all__:
    |     |       if issubclass(cls, BaseSpectralGroup):
    |     |         groups.append(cls())
    |     |
    |     +-- Return ordered list of group instances
    |
    +-- R3FeatureRegistry()
    |     |
    |     +-- register(group) for each discovered group
    |     |     - Checks GROUP_NAME uniqueness
    |     |     - Appends to internal list
    |     |
    |     +-- freeze() -> R3FeatureMap
    |           - Assigns contiguous INDEX_RANGE to each group
    |           - Creates immutable R3FeatureMap(total_dim, groups)
    |           - Cannot register after freeze()
    |
    +-- extractor.groups = registry.groups
    +-- extractor.feature_map = registry.freeze()
```

### Registration Order

Groups are registered in the order they are discovered:

1. `psychoacoustic/__init__.py` exports (Group A)
2. `dsp/__init__.py` exports (Groups B, C, D)
3. `cross_domain/__init__.py` exports (Group E)
4. `extensions/__init__.py` exports (Groups F, G, H, I, J, K)

**Within each subdirectory**, the order is determined by the order of entries in `__all__`.

### Index Assignment

Indices are assigned sequentially at `freeze()` time:

```
Group A: offset=0,  range=[0:7]    (7D)
Group B: offset=7,  range=[7:12]   (5D)
Group C: offset=12, range=[12:21]  (9D)
Group D: offset=21, range=[21:25]  (4D)
Group E: offset=25, range=[25:49]  (24D)
Group F: offset=49, range=[49:65]  (16D)
Group G: offset=65, range=[65:75]  (10D)
Group H: offset=75, range=[75:87]  (12D)
Group I: offset=87, range=[87:94]  (7D)
Group J: offset=94, range=[94:114] (20D)
Group K: offset=114, range=[114:128] (14D)
Total: 128D
```

### Frozen State

After `freeze()`, the registry is immutable:

```python
registry.freeze()  # Returns R3FeatureMap
registry.register(new_group)  # Raises RuntimeError!
```

The `R3FeatureMap` is a frozen dataclass:

```python
@dataclass(frozen=True)
class R3FeatureMap:
    total_dim: int              # 128
    groups: Tuple[R3GroupInfo, ...]

@dataclass(frozen=True)
class R3GroupInfo:
    name: str                   # "consonance"
    dim: int                    # 7
    start: int                  # 0
    end: int                    # 7
    feature_names: Tuple[str, ...]
```

---

## 7. Example: Adding an L-SpatialAudio Group

This walkthrough demonstrates adding a hypothetical "L-SpatialAudio" group that computes spatial audio features from the mel spectrogram.

### Step 1: Create the Implementation File

File: `mi_beta/ear/r3/extensions/spatial_audio.py`

```python
"""
Group L: Spatial Audio [128:133] -- 5D (Hypothetical)

Computes spatial characteristics from mono mel spectrogram
by analyzing inter-channel correlation patterns and spatial cues.
"""

from __future__ import annotations

from typing import List

import torch
from torch import Tensor

from ....contracts import BaseSpectralGroup


class SpatialAudioGroup(BaseSpectralGroup):
    """Group L: Spatial Audio features.

    Extracts spatial perception cues from mono mel spectrogram
    by analyzing frequency-dependent energy distribution patterns
    that correlate with perceived spatial width and depth.
    """

    GROUP_NAME = "spatial_audio"
    DOMAIN = "psychoacoustic"
    OUTPUT_DIM = 5
    INDEX_RANGE = (0, 0)  # Auto-assigned by registry

    @property
    def feature_names(self) -> List[str]:
        return [
            "spatial_width",           # Perceived spatial extent
            "spectral_diffuseness",    # Diffuse vs. focused energy
            "low_high_decorrelation",  # Frequency-band independence
            "envelopment_proxy",       # Listener envelopment estimate
            "depth_cue",              # Near-far perception proxy
        ]

    def compute(self, mel: Tensor) -> Tensor:
        """Compute spatial audio features from mel spectrogram.

        Args:
            mel: (B, N_MELS, T) log-mel spectrogram

        Returns:
            (B, T, 5) spatial features in [0, 1]
        """
        B, N, T = mel.shape
        mel_t = mel.transpose(1, 2)  # (B, T, N)

        # Feature 1: Spatial width -- spectral entropy as proxy
        p = torch.softmax(mel_t, dim=-1)
        width = -(p * p.clamp(min=1e-8).log()).sum(dim=-1, keepdim=True)
        width = width / torch.log(torch.tensor(float(N)))  # [0, 1]

        # Feature 2: Spectral diffuseness -- flatness measure
        geo_mean = mel_t.clamp(min=1e-8).log().mean(dim=-1, keepdim=True).exp()
        ari_mean = mel_t.mean(dim=-1, keepdim=True).clamp(min=1e-8)
        diffuseness = (geo_mean / ari_mean).clamp(0, 1)

        # Feature 3: Low-high decorrelation
        low = mel_t[:, :, :N // 2].mean(dim=-1, keepdim=True)
        high = mel_t[:, :, N // 2:].mean(dim=-1, keepdim=True)
        decorr = 1 - torch.abs(low - high) / (low + high + 1e-8)

        # Feature 4: Envelopment proxy -- lateral energy fraction
        mid_energy = mel_t[:, :, N // 4 : 3 * N // 4].sum(dim=-1, keepdim=True)
        total = mel_t.sum(dim=-1, keepdim=True).clamp(min=1e-8)
        envelopment = 1 - mid_energy / total

        # Feature 5: Depth cue -- spectral centroid variance
        bins = torch.arange(N, dtype=mel_t.dtype, device=mel_t.device)
        centroid = (mel_t * bins).sum(dim=-1, keepdim=True) / total
        depth = (centroid / N).clamp(0, 1)

        features = torch.cat(
            [width, diffuseness, decorr, envelopment, depth], dim=-1
        )
        return features.clamp(0, 1)  # (B, T, 5)
```

### Step 2: Export from extensions/__init__.py

```python
# mi_beta/ear/r3/extensions/__init__.py
from .pitch_chroma import PitchChromaGroup
from .rhythm_groove import RhythmGrooveGroup
# ... existing groups ...
from .spatial_audio import SpatialAudioGroup

__all__ = [
    "PitchChromaGroup",
    "RhythmGrooveGroup",
    # ... existing exports ...
    "SpatialAudioGroup",
]
```

### Step 3: Verify

```python
from mi_beta.ear.r3 import R3Extractor

extractor = R3Extractor()
print(f"Total dim: {extractor.total_dim}")  # 133 (128 + 5)
print(extractor.feature_map)
# R3FeatureMap(total_dim=133, groups=[
#   consonance: [0:7] (7D)
#   ...
#   modulation_psychoacoustic: [114:128] (14D)
#   spatial_audio: [128:133] (5D)       <-- new!
# ])

# Test extraction
mel = torch.randn(2, 128, 100)  # (B=2, N=128, T=100)
output = extractor.extract(mel)
assert output.features.shape == (2, 100, 133)
```

### Step 4: Update Documentation

1. Add to `00-INDEX.md` architecture summary
2. Add 5 new entries to `Registry/FeatureCatalog.md`
3. Add index ranges to `Registry/DimensionMap.md`
4. Add changelog entry to `CHANGELOG.md`

### Step 5: Write Tests

```python
def test_spatial_audio_group():
    group = SpatialAudioGroup()

    # Contract checks
    assert group.GROUP_NAME == "spatial_audio"
    assert group.OUTPUT_DIM == 5
    assert len(group.feature_names) == 5
    assert all(isinstance(n, str) for n in group.feature_names)
    assert not group.validate()  # No errors

    # Compute check
    mel = torch.randn(2, 128, 50)
    out = group.compute(mel)
    assert out.shape == (2, 50, 5)
    assert out.min() >= 0.0
    assert out.max() <= 1.0

    # Determinism check
    out2 = group.compute(mel)
    assert torch.allclose(out, out2)
```

---

## 8. Testing Requirements

Every new group must pass the following test categories:

### 8.1 Contract Tests

```python
def test_contract(group: BaseSpectralGroup):
    """Verify BaseSpectralGroup contract compliance."""
    # 1. GROUP_NAME is non-empty and unique
    assert group.GROUP_NAME
    assert isinstance(group.GROUP_NAME, str)

    # 2. OUTPUT_DIM is positive
    assert group.OUTPUT_DIM > 0

    # 3. feature_names matches OUTPUT_DIM
    assert len(group.feature_names) == group.OUTPUT_DIM

    # 4. All feature names are snake_case strings
    import re
    for name in group.feature_names:
        assert isinstance(name, str)
        assert re.match(r'^[a-z][a-z0-9_]*$', name), f"Not snake_case: {name}"

    # 5. validate() returns no errors
    errors = group.validate()
    assert not errors, f"Validation errors: {errors}"
```

### 8.2 Shape Tests

```python
def test_shapes(group: BaseSpectralGroup):
    """Verify output tensor shapes."""
    for B in [1, 4]:
        for T in [1, 10, 100]:
            mel = torch.randn(B, 128, T)
            out = group.compute(mel)
            assert out.shape == (B, T, group.OUTPUT_DIM), \
                f"Expected ({B}, {T}, {group.OUTPUT_DIM}), got {out.shape}"
```

### 8.3 Range Tests

```python
def test_output_range(group: BaseSpectralGroup):
    """Verify output values are in [0, 1]."""
    mel = torch.randn(4, 128, 100)
    out = group.compute(mel)
    assert out.min() >= 0.0 - 1e-6, f"Min value {out.min()} < 0"
    assert out.max() <= 1.0 + 1e-6, f"Max value {out.max()} > 1"
```

### 8.4 Determinism Tests

```python
def test_determinism(group: BaseSpectralGroup):
    """Verify compute is deterministic."""
    mel = torch.randn(2, 128, 50)
    out1 = group.compute(mel)
    out2 = group.compute(mel)
    assert torch.allclose(out1, out2, atol=1e-6)
```

### 8.5 Registration Tests

```python
def test_registration():
    """Verify group is discoverable and registerable."""
    from mi_beta.ear.r3 import R3Extractor

    extractor = R3Extractor()
    group_names = [g.name for g in extractor.feature_map.groups]
    assert "my_new_group" in group_names
```

### 8.6 Integration Tests

```python
def test_integration():
    """Verify full pipeline produces correct total dim."""
    from mi_beta.ear.r3 import R3Extractor

    extractor = R3Extractor()
    mel = torch.randn(2, 128, 100)
    output = extractor.extract(mel)
    assert output.features.shape == (2, 100, extractor.total_dim)
```

---

## 9. Reference: _template.py Pattern

The canonical template file is located at:

**`mi_beta/ear/r3/extensions/_template.py`**

```python
"""
_template.py -- Template for creating a new R3 spectral group.

To add a new group to the R3 feature vector:

1. Copy this file to a new .py file in this directory (or any R3 subdirectory).
2. Rename the class and fill in GROUP_NAME, OUTPUT_DIM, feature_names, compute().
3. Export the class from the subdirectory's __init__.py via __all__.

The R3FeatureRegistry will auto-discover it and assign index ranges.
INDEX_RANGE is set automatically at freeze() time -- you can leave it as (0, 0).

Example:
    # In extensions/__init__.py:
    from .my_new_group import MyNewGroup
    __all__ = ["MyNewGroup"]
"""

from __future__ import annotations
from typing import List
import torch
from torch import Tensor
from ....contracts import BaseSpectralGroup


class _TemplateGroup(BaseSpectralGroup):
    """Template -- do NOT use directly. Copy and rename."""

    GROUP_NAME = "template"   # Unique name for this group
    OUTPUT_DIM = 3            # Number of features this group produces
    INDEX_RANGE = (0, 0)      # Auto-assigned by registry.freeze()

    @property
    def feature_names(self) -> List[str]:
        return [
            "feature_1",
            "feature_2",
            "feature_3",
        ]

    def compute(self, mel: Tensor) -> Tensor:
        """Compute features from mel spectrogram.

        Args:
            mel: (B, N_MELS, T) log-mel spectrogram

        Returns:
            (B, T, OUTPUT_DIM) features, ideally in [0, 1]
        """
        B, N, T = mel.shape
        mel_t = mel.transpose(1, 2)  # (B, T, N)
        f1 = mel_t.mean(dim=-1, keepdim=True)
        f2 = mel_t.std(dim=-1, keepdim=True)
        f3 = mel_t.max(dim=-1, keepdim=True).values

        features = torch.cat([f1, f2, f3], dim=-1)  # (B, T, 3)
        return features.clamp(0, 1)
```

**Important**: The `_TemplateGroup` class name starts with an underscore and is never exported in `__all__`, so the registry will not discover it. When you copy the template, rename the class to remove the underscore prefix.
