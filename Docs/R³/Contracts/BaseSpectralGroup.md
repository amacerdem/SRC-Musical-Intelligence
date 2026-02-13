# Contract: BaseSpectralGroup

**Source**: `mi_beta/contracts/base_spectral_group.py`
**Type**: Abstract Base Class (ABC)
**Purpose**: Defines the interface that every R3 spectral feature group must implement.

---

## 1. Class Definition

```python
class BaseSpectralGroup(ABC):
    """Abstract base class for R3 spectral feature groups.

    Each subclass computes a contiguous slice of the 49-D R3 feature vector
    from the mel spectrogram.
    """

    # Class constants -- override in every subclass
    GROUP_NAME: str = ""
    DOMAIN: str = ""
    OUTPUT_DIM: int = 0
    INDEX_RANGE: Tuple[int, int] = (0, 0)

    # Abstract members
    @abstractmethod
    def compute(self, mel: Tensor) -> Tensor: ...

    @property
    @abstractmethod
    def feature_names(self) -> List[str]: ...

    # Computed helpers
    @property
    def start_index(self) -> int: ...
    @property
    def end_index(self) -> int: ...
    def validate(self) -> list[str]: ...
```

---

## 2. Class Constants

Every subclass **must** override these four class-level attributes:

### 2.1 GROUP_NAME

```python
GROUP_NAME: str = ""
"""Canonical group name (e.g. "consonance", "energy", "timbre")."""
```

- Must be non-empty.
- Must be unique across all registered groups (enforced by `R3FeatureRegistry.register()`).
- Convention: lowercase, underscore-separated (e.g. `"pitch_chroma"`, `"rhythm_groove"`).

### 2.2 DOMAIN

```python
DOMAIN: str = ""
"""Perceptual domain this group covers.  One of:
"psychoacoustic", "energetic", "timbral", "temporal", "cross_domain"."""
```

- Indicates the perceptual domain for organization and documentation.
- Current valid values: `"psychoacoustic"`, `"energetic"`, `"timbral"`, `"temporal"`, `"cross_domain"`.
- Phase 6 extends with: `"pitch"`, `"rhythm"`, `"harmony"`, `"information"`, `"modulation"`.

### 2.3 OUTPUT_DIM

```python
OUTPUT_DIM: int = 0
"""Number of features this group produces."""
```

- Must be strictly positive (`> 0`).
- Determines the last dimension of the output tensor.
- Must equal `len(feature_names)`.
- Must equal `INDEX_RANGE[1] - INDEX_RANGE[0]` (after freeze).

### 2.4 INDEX_RANGE

```python
INDEX_RANGE: Tuple[int, int] = (0, 0)
"""Half-open interval [start, end) in the 49-D R3 vector.
end - start MUST equal OUTPUT_DIM."""
```

- Defines the position of this group's features in the concatenated R3 vector.
- **Current behavior**: Hardcoded in each subclass (e.g. `(0, 7)` for consonance).
- **Registry behavior**: Automatically assigned by `R3FeatureRegistry.freeze()`. Groups can leave this as `(0, 0)` and it will be overwritten at freeze time.

---

## 3. Abstract Members

### 3.1 compute()

```python
@abstractmethod
def compute(self, mel: Tensor) -> Tensor:
    """Compute spectral features from the mel spectrogram.

    Args:
        mel: (B, N_MELS, T) log-mel spectrogram (log1p normalised).

    Returns:
        (B, T, OUTPUT_DIM) spectral features for this group.
        Values should be in [0, 1] unless the feature has a natural
        signed range (documented in feature_names).
    """
```

**Input contract**:
- Shape: `(B, N_MELS, T)` where `B` = batch size, `N_MELS` = 128, `T` = number of frames.
- Content: Log-mel spectrogram, log1p normalized.
- Frame rate: 172.27 Hz (sr=44100, hop_length=256).

**Output contract**:
- Shape: `(B, T, OUTPUT_DIM)` -- note the transposition from `(B, N, T)` input to `(B, T, D)` output.
- Range: `[0, 1]` for all dimensions unless explicitly documented.
- Dtype: Same as input (typically `torch.float32`).
- Device: Same as input tensor.

### 3.2 feature_names

```python
@property
@abstractmethod
def feature_names(self) -> List[str]:
    """Ordered names of each output dimension.

    len(feature_names) MUST equal OUTPUT_DIM.
    Names follow snake_case convention (e.g. "stumpf_fusion").
    """
```

**Naming contract**:
- Length must equal `OUTPUT_DIM` exactly.
- Names must be `snake_case` (lowercase with underscores).
- Names must be unique across all groups (enforced at registry freeze).
- Names should be descriptive and cite their psychoacoustic or signal-processing origin.

---

## 4. Computed Helpers

### 4.1 start_index / end_index

```python
@property
def start_index(self) -> int:
    """Start index in the R3 vector (inclusive)."""
    return self.INDEX_RANGE[0]

@property
def end_index(self) -> int:
    """End index in the R3 vector (exclusive)."""
    return self.INDEX_RANGE[1]
```

Convenience accessors for the half-open interval.

### 4.2 validate()

```python
def validate(self) -> list[str]:
    """Check internal consistency.

    Returns:
        List of error messages (empty if valid).
    """
    errors: list[str] = []

    if not self.GROUP_NAME:
        errors.append("GROUP_NAME must be non-empty")
    if self.OUTPUT_DIM <= 0:
        errors.append(f"OUTPUT_DIM must be > 0, got {self.OUTPUT_DIM}")

    start, end = self.INDEX_RANGE
    if end - start != self.OUTPUT_DIM:
        errors.append(
            f"INDEX_RANGE [{start}:{end}] span ({end - start}) "
            f"!= OUTPUT_DIM ({self.OUTPUT_DIM})"
        )

    try:
        names = self.feature_names
        if len(names) != self.OUTPUT_DIM:
            errors.append(
                f"feature_names has {len(names)} entries, "
                f"expected {self.OUTPUT_DIM}"
            )
    except NotImplementedError:
        pass

    return errors
```

Validation checks performed:
1. `GROUP_NAME` is non-empty.
2. `OUTPUT_DIM` is positive.
3. `INDEX_RANGE` span matches `OUTPUT_DIM`.
4. `feature_names` length matches `OUTPUT_DIM`.

### 4.3 __repr__()

```python
def __repr__(self) -> str:
    return (
        f"{self.__class__.__name__}("
        f"group={self.GROUP_NAME!r}, "
        f"domain={self.DOMAIN!r}, "
        f"dim={self.OUTPUT_DIM}, "
        f"range=[{self.INDEX_RANGE[0]}:{self.INDEX_RANGE[1]}])"
    )
```

---

## 5. Contract Obligations Summary

| Obligation | Requirement | Enforced By |
|------------|-------------|-------------|
| GROUP_NAME non-empty | `validate()` check | `validate()` |
| GROUP_NAME unique | No duplicates across registry | `R3FeatureRegistry.register()` |
| OUTPUT_DIM > 0 | Positive integer | `validate()` |
| INDEX_RANGE span = OUTPUT_DIM | After freeze | `validate()`, `R3FeatureRegistry.freeze()` |
| feature_names length = OUTPUT_DIM | Exact match | `validate()` |
| feature_names unique globally | No duplicates across all groups | Phase 6: `R3FeatureRegistry.freeze()` |
| compute() input shape | `(B, N_MELS, T)` | Caller contract |
| compute() output shape | `(B, T, OUTPUT_DIM)` | Runtime assertion recommended |
| compute() output range | `[0, 1]` | Group implementation responsibility |

---

## 6. Current Groups (v1)

| Group | GROUP_NAME | DOMAIN | OUTPUT_DIM | INDEX_RANGE | Subdirectory |
|-------|-----------|--------|:----------:|:-----------:|-------------|
| A | `"consonance"` | `"psychoacoustic"` | 7 | `[0:7]` | `psychoacoustic/` |
| B | `"energy"` | `"energetic"` | 5 | `[7:12]` | `dsp/` |
| C | `"timbre"` | `"timbral"` | 9 | `[12:21]` | `dsp/` |
| D | `"change"` | `"temporal"` | 4 | `[21:25]` | `dsp/` |
| E | `"interactions"` | `"cross_domain"` | 24 | `[25:49]` | `cross_domain/` |

---

## 7. Phase 6 Planned Changes

### 7.1 Docstring Update

Current docstring references "49-D R3 feature vector". Phase 6 changes this to a dynamic reference:

```python
# Current:
"""Each subclass computes a contiguous slice of the 49-D R3 feature vector"""
INDEX_RANGE: Tuple[int, int] = (0, 0)
"""Half-open interval [start, end) in the 49-D R3 vector."""

# Phase 6:
"""Each subclass computes a contiguous slice of the R3 feature vector."""
INDEX_RANGE: Tuple[int, int] = (0, 0)
"""Auto-assigned by R3FeatureRegistry.freeze()."""
```

### 7.2 compute_with_deps() Method

Phase 6 adds an optional method for groups that depend on other group outputs:

```python
def compute_with_deps(self, mel: Tensor, group_outputs: dict) -> Tensor:
    """Override this for groups that depend on other group outputs.

    Args:
        mel: (B, N_MELS, T) log-mel spectrogram.
        group_outputs: Dict mapping GROUP_NAME -> (B, T, dim) tensors
            from previously computed groups.

    Returns:
        (B, T, OUTPUT_DIM) spectral features.

    Default: falls back to compute(mel).
    """
    return self.compute(mel)
```

Groups using dependency injection (Phase 6):
- **E** (Interactions): Receives A, B, C, D outputs instead of computing proxies.
- **G** (Rhythm & Groove): Receives B[11] onset_strength.
- **H** (Harmony & Tonality): Receives F[49:61] chroma.
- **I** (Information & Surprise): Receives F chroma, G onset, H key.

### 7.3 New Groups (Phase 6)

| Group | GROUP_NAME | DOMAIN | OUTPUT_DIM | INDEX_RANGE |
|-------|-----------|--------|:----------:|:-----------:|
| F | `"pitch_chroma"` | `"pitch"` | 16 | `[49:65]` |
| G | `"rhythm_groove"` | `"rhythm"` | 10 | `[65:75]` |
| H | `"harmony_tonality"` | `"harmony"` | 12 | `[75:87]` |
| I | `"information_surprise"` | `"information"` | 7 | `[87:94]` |
| J | `"timbre_extended"` | `"timbre"` | 20 | `[94:114]` |
| K | `"modulation_psychoacoustic"` | `"modulation"` | 14 | `[114:128]` |

---

## 8. Example Implementation

Minimal example of a correctly implemented group:

```python
from typing import List
import torch
from torch import Tensor
from mi_beta.contracts import BaseSpectralGroup


class ExampleGroup(BaseSpectralGroup):
    """Example: computes 3 spectral features."""

    GROUP_NAME = "example"
    DOMAIN = "timbral"
    OUTPUT_DIM = 3
    INDEX_RANGE = (0, 0)  # Auto-assigned by registry.freeze()

    @property
    def feature_names(self) -> List[str]:
        return ["feature_mean", "feature_std", "feature_max"]

    def compute(self, mel: Tensor) -> Tensor:
        """mel: (B, 128, T) -> (B, T, 3)"""
        B, N, T = mel.shape
        mel_t = mel.transpose(1, 2)  # (B, T, N)

        f1 = mel_t.mean(dim=-1, keepdim=True)
        f2 = mel_t.std(dim=-1, keepdim=True)
        f3 = mel_t.max(dim=-1, keepdim=True).values

        features = torch.cat([f1, f2, f3], dim=-1)  # (B, T, 3)
        return features.clamp(0, 1)
```

Validation:

```python
group = ExampleGroup()
errors = group.validate()
assert errors == [], f"Validation failed: {errors}"
assert len(group.feature_names) == group.OUTPUT_DIM == 3
```
