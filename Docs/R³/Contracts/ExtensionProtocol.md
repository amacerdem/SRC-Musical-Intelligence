# Contract: Extension Protocol

**Source**: `mi_beta/ear/r3/extensions/_template.py`
**Type**: Convention-based protocol
**Purpose**: Defines how to add new spectral feature groups to the R3 pipeline without modifying core files.

---

## 1. extensions/ Directory Purpose

The `extensions/` directory is the designated location for adding new `BaseSpectralGroup` implementations to the R3 feature vector. It is scanned last in the auto-discovery sequence, meaning extension groups are appended after all core groups.

```
mi_beta/ear/r3/
├── psychoacoustic/     # Scanned 1st: Group A
├── dsp/                # Scanned 2nd: Groups B, C, D
├── cross_domain/       # Scanned 3rd: Group E
└── extensions/         # Scanned 4th: User-defined groups
    ├── __init__.py     # Exports via __all__
    ├── _template.py    # Template file (not exported)
    └── my_new_group.py # Your new group
```

**Key property**: The `extensions/` directory is always scanned last in `_SUBDIRECTORY_NAMES`:

```python
_SUBDIRECTORY_NAMES = ("psychoacoustic", "dsp", "cross_domain", "extensions")
```

This means extension group features are always assigned index ranges after the core groups.

---

## 2. _template.py Pattern

The template file provides a complete, copy-ready skeleton for creating new groups:

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
        # Your computation here. Example:
        mel_t = mel.transpose(1, 2)  # (B, T, N)
        f1 = mel_t.mean(dim=-1, keepdim=True)
        f2 = mel_t.std(dim=-1, keepdim=True)
        f3 = mel_t.max(dim=-1, keepdim=True).values

        features = torch.cat([f1, f2, f3], dim=-1)  # (B, T, 3)
        return features.clamp(0, 1)
```

**Design notes on the template**:
- The class is named `_TemplateGroup` (leading underscore) to indicate it should not be used directly.
- `INDEX_RANGE = (0, 0)` is a placeholder -- the registry assigns the real range at freeze time.
- The `compute()` demonstrates the required shape transformation: `(B, N, T)` input to `(B, T, D)` output.
- The final `.clamp(0, 1)` demonstrates the normalization contract.

---

## 3. Step-by-Step: Adding a New Group

### Step 1: Create the Group File

Copy `_template.py` to a new file in `extensions/` (or any R3 subdirectory):

```bash
cp mi_beta/ear/r3/extensions/_template.py \
   mi_beta/ear/r3/extensions/spectral_balance.py
```

### Step 2: Implement the Group

Edit the new file:

```python
# mi_beta/ear/r3/extensions/spectral_balance.py

from __future__ import annotations
from typing import List
import torch
from torch import Tensor
from ....contracts import BaseSpectralGroup


class SpectralBalanceGroup(BaseSpectralGroup):
    """Custom group: spectral balance features (2D)."""

    GROUP_NAME = "spectral_balance"    # Must be unique
    DOMAIN = "timbral"
    OUTPUT_DIM = 2                     # Must match feature_names length
    INDEX_RANGE = (0, 0)               # Auto-assigned

    @property
    def feature_names(self) -> List[str]:
        return [
            "low_mid_ratio",
            "mid_high_ratio",
        ]

    def compute(self, mel: Tensor) -> Tensor:
        B, N, T = mel.shape

        low = mel[:, :42, :].sum(dim=1)    # 0-1kHz
        mid = mel[:, 42:85, :].sum(dim=1)  # 1-4kHz
        high = mel[:, 85:, :].sum(dim=1)   # 4kHz+

        total = (low + mid + high).clamp(min=1e-8)
        low_mid = low / (low + mid).clamp(min=1e-8)
        mid_high = mid / (mid + high).clamp(min=1e-8)

        features = torch.stack([low_mid, mid_high], dim=-1)  # (B, T, 2)
        return features.clamp(0, 1)
```

### Step 3: Export from __init__.py

Edit `mi_beta/ear/r3/extensions/__init__.py`:

```python
from .spectral_balance import SpectralBalanceGroup

__all__ = ["SpectralBalanceGroup"]
```

### Step 4: Verify

```python
from mi_beta.ear.r3 import R3Extractor

extractor = R3Extractor()
print(extractor.total_dim)        # 49 + 2 = 51
print(extractor.feature_names[-2:])  # ['low_mid_ratio', 'mid_high_ratio']
print(extractor.feature_map)
# R3FeatureMap(total_dim=51, groups=[
#   consonance: [0:7] (7D)
#   energy: [7:12] (5D)
#   timbre: [12:21] (9D)
#   change: [21:25] (4D)
#   interactions: [25:49] (24D)
#   spectral_balance: [49:51] (2D)
# ])
```

---

## 4. Auto-Discovery Integration

The connection between a new group file and the R3 pipeline is entirely convention-based:

```
[SpectralBalanceGroup]   defined in   extensions/spectral_balance.py
         |
         | exported via __all__ in
         v
extensions/__init__.py:  __all__ = ["SpectralBalanceGroup"]
         |
         | imported by importlib.import_module(".extensions", ...)
         v
_discover_groups()       filters for BaseSpectralGroup subclasses
         |
         | appends instance
         v
R3FeatureRegistry.register(SpectralBalanceGroup())
         |
         | at freeze()
         v
INDEX_RANGE auto-assigned: (49, 51)
```

**What makes auto-discovery work**:

1. The subdirectory `extensions` is listed in `_SUBDIRECTORY_NAMES`.
2. `importlib.import_module` imports `extensions/__init__.py`.
3. The `__all__` list in `__init__.py` declares which classes to export.
4. `_discover_groups()` checks each exported name:
   - Is it a class? (`isinstance(cls, type)`)
   - Is it a subclass of `BaseSpectralGroup`? (`issubclass(cls, BaseSpectralGroup)`)
   - Is it not `BaseSpectralGroup` itself? (`cls is not BaseSpectralGroup`)
5. If all checks pass, instantiate and add to the group list.

**What does NOT trigger auto-discovery**:
- Classes not in `__all__`.
- Classes with a leading underscore name (like `_TemplateGroup`) -- unless explicitly added to `__all__`.
- Non-class objects in `__all__`.
- Modules that fail to import (silently skipped).

---

## 5. Checklist for New Groups

Before adding a new group, verify:

- [ ] `GROUP_NAME` is unique (no other group uses this name).
- [ ] `OUTPUT_DIM` matches `len(feature_names)`.
- [ ] All feature names are `snake_case` and unique across all groups.
- [ ] `compute()` accepts `(B, N_MELS, T)` and returns `(B, T, OUTPUT_DIM)`.
- [ ] All output values are in `[0, 1]` (or documented exceptions).
- [ ] The class is exported in the subdirectory's `__init__.py` via `__all__`.
- [ ] `INDEX_RANGE = (0, 0)` (let the registry assign it).
- [ ] No circular imports (be careful with cross-group references).
- [ ] `validate()` returns no errors.

---

## 6. Phase 6: Domain-Based Extensions

### 6.1 New Subdirectory Layout

Phase 6 introduces dedicated subdirectories for new groups F-K, reducing reliance on `extensions/`:

```
mi_beta/ear/r3/
├── psychoacoustic/          # A: Consonance
├── dsp/                     # B, C, D: Energy, Timbre, Change
├── cross_domain/            # E: Interactions
├── pitch/                   # F: Pitch & Chroma (NEW)
├── rhythm/                  # G: Rhythm & Groove (NEW)
├── harmony/                 # H: Harmony & Tonality (NEW)
├── information/             # I: Information & Surprise (NEW)
├── timbre_extended/         # J: Timbre Extended (NEW)
├── modulation/              # K: Modulation & Psychoacoustic (NEW)
└── extensions/              # User extensions (always last)
```

### 6.2 Dependency-Aware Extensions

Phase 6 groups that depend on other groups implement `compute_with_deps()` instead of (or in addition to) `compute()`:

```python
class MyDependentGroup(BaseSpectralGroup):
    GROUP_NAME = "my_dependent"
    OUTPUT_DIM = 4
    INDEX_RANGE = (0, 0)

    @property
    def feature_names(self) -> List[str]:
        return ["feat_a", "feat_b", "feat_c", "feat_d"]

    def compute(self, mel: Tensor) -> Tensor:
        # Fallback: compute without dependencies
        raise NotImplementedError("This group requires compute_with_deps()")

    def compute_with_deps(self, mel: Tensor, group_outputs: dict) -> Tensor:
        chroma = group_outputs['pitch_chroma'][:, :, :12]  # F group output
        onset = group_outputs['energy'][:, :, 4]           # B[11]
        # ... compute features using dependencies
        return features
```

### 6.3 Stage Registration

Extensions that depend on other groups must declare their stage:

```python
class MyDependentGroup(BaseSpectralGroup):
    STAGE = 2  # Runs after Stage 1 groups
    # ... (Phase 6 proposed attribute)
```

The `R3Extractor.STAGE_ORDER` dict would then incorporate extension groups based on their `STAGE` attribute.
