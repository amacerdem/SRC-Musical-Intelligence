# Contract: R3FeatureSpec

**Source**: `mi_beta/contracts/feature_spec.py`
**Type**: Frozen dataclass
**Purpose**: Registration record for a single R3 spectral feature. Names the feature, places it in a group, assigns its index, and records the scientific basis.

---

## 1. Class Definition

```python
@dataclass(frozen=True)
class R3FeatureSpec:
    """Registration of a single R3 spectral feature.

    Attributes:
        name:        Canonical name (e.g. "stumpf_fusion", "loudness").
        group:       Parent spectral group (e.g. "consonance", "energy").
        index:       Position in the 49-D R3 vector (0-48).
        description: One-line description of what this feature measures.
        citation:    Primary citation (e.g. "Stumpf 1898", "Plomp & Levelt 1965").
        unit:        Physical unit if applicable (e.g. "dB", "Hz", "").
                     Empty string for dimensionless quantities.
    """

    name: str
    group: str
    index: int
    description: str
    citation: str
    unit: str = ""
```

---

## 2. Fields

### 2.1 name

```python
name: str
```

- Canonical feature name in `snake_case`.
- Must be unique across all R3 features.
- Examples: `"roughness"`, `"stumpf_fusion"`, `"onset_strength"`, `"chroma_C"`.

### 2.2 group

```python
group: str
```

- Parent spectral group name, matching the `GROUP_NAME` of the corresponding `BaseSpectralGroup` subclass.
- Current values: `"consonance"`, `"energy"`, `"timbre"`, `"change"`, `"interactions"`.
- Phase 6 adds: `"pitch_chroma"`, `"rhythm_groove"`, `"harmony_tonality"`, `"information_surprise"`, `"timbre_extended"`, `"modulation_psychoacoustic"`.

### 2.3 index

```python
index: int
```

- Zero-based position in the R3 feature vector.
- Current valid range: `[0, 48]` (49 features).
- Phase 6 valid range: `[0, 127]` (128 features).

### 2.4 description

```python
description: str
```

- One-line human-readable description of what the feature measures.
- Example: `"Spectral variance-based roughness proxy"`.

### 2.5 citation

```python
citation: str
```

- Primary scientific citation for the feature.
- Examples: `"Plomp & Levelt 1965"`, `"Stumpf 1898"`, `"Stevens' power law"`.
- Use `"DERIVED"` for features computed from other features without independent psychoacoustic basis.
- Use `"PROXY"` suffix to indicate approximation: `"Plomp & Levelt 1965 (PROXY)"`.

### 2.6 unit

```python
unit: str = ""
```

- Physical unit if applicable.
- Examples: `"dB"`, `"Hz"`, `"BPM"`, `"acum"` (for Zwicker sharpness).
- Empty string for dimensionless quantities (ratios, normalized values).

---

## 3. Validation

### 3.1 Current __post_init__ Validation

```python
def __post_init__(self) -> None:
    if not (0 <= self.index < 49):
        raise ValueError(
            f"R3FeatureSpec {self.name!r}: index must be in [0, 48], "
            f"got {self.index}"
        )
```

The current validation enforces the hardcoded 49-dimension limit. Any index outside `[0, 48]` raises a `ValueError` at construction time.

### 3.2 Implications

Because `R3FeatureSpec` is a frozen dataclass, all validation occurs at construction time via `__post_init__`. The spec is immutable after creation -- fields cannot be modified.

This means:
- Specs for features in groups F-K (indices 49-127) **cannot** be created with the current code.
- The 49-dimension constraint is the primary blocker for R3 v2 feature registration.

---

## 4. __repr__()

```python
def __repr__(self) -> str:
    u = f" ({self.unit})" if self.unit else ""
    return (
        f"R3FeatureSpec(idx={self.index}, "
        f"{self.name!r}{u}, "
        f"group={self.group!r}, "
        f"cite={self.citation!r})"
    )
```

Example output:

```
R3FeatureSpec(idx=3, 'stumpf_fusion', group='consonance', cite='Stumpf 1898')
R3FeatureSpec(idx=10, 'loudness' (dB), group='energy', cite="Stevens' power law")
```

---

## 5. Usage Patterns

### 5.1 Feature Registration

```python
from mi_beta.contracts.feature_spec import R3FeatureSpec

roughness = R3FeatureSpec(
    name="roughness",
    group="consonance",
    index=0,
    description="Spectral variance-based roughness proxy",
    citation="Plomp & Levelt 1965 (PROXY)",
)

loudness = R3FeatureSpec(
    name="loudness",
    group="energy",
    index=10,
    description="Stevens' power law loudness estimate",
    citation="Stevens' power law",
    unit="dB",
)
```

### 5.2 Model Documentation Reference

C3 models that read specific R3 features can reference the spec:

```python
# In a model doc: "da_nacc reads r3[3] stumpf_fusion"
spec = R3FeatureSpec(
    name="stumpf_fusion",
    group="consonance",
    index=3,
    description="Low-frequency energy ratio (tonal fusion proxy)",
    citation="Stumpf 1898",
)
```

### 5.3 Invalid Constructions (Current)

```python
# Current code rejects indices >= 49:
try:
    R3FeatureSpec(name="chroma_C", group="pitch_chroma", index=49,
                  description="C pitch class energy", citation="Shepard 1964")
except ValueError as e:
    print(e)  # "R3FeatureSpec 'chroma_C': index must be in [0, 48], got 49"
```

---

## 6. Phase 6 Planned Changes

### 6.1 Dynamic Index Validation

The hardcoded `49` is replaced with a dynamic reference to `R3_DIM`:

```python
# Current:
def __post_init__(self) -> None:
    if not (0 <= self.index < 49):
        raise ValueError(
            f"R3FeatureSpec {self.name!r}: index must be in [0, 48], "
            f"got {self.index}"
        )

# Phase 6:
def __post_init__(self) -> None:
    from mi_beta.core.constants import R3_DIM
    if not (0 <= self.index < R3_DIM):
        raise ValueError(
            f"R3FeatureSpec {self.name!r}: index must be in [0, {R3_DIM - 1}], "
            f"got {self.index}"
        )
```

With `R3_DIM = 128` in Phase 6, this allows indices `[0, 127]`.

### 6.2 Alternative: Registry-Based Validation

A more robust Phase 6 approach validates against the actual registry total_dim:

```python
def __post_init__(self) -> None:
    # Validate against registry if available, else use R3_DIM constant
    try:
        from mi_beta.ear.r3._registry import get_default_registry
        max_dim = get_default_registry().freeze().total_dim
    except (ImportError, RuntimeError):
        from mi_beta.core.constants import R3_DIM
        max_dim = R3_DIM

    if not (0 <= self.index < max_dim):
        raise ValueError(
            f"R3FeatureSpec {self.name!r}: index must be in [0, {max_dim - 1}], "
            f"got {self.index}"
        )
```

### 6.3 Test Strategy

```python
# Valid indices:
R3FeatureSpec(name="test", group="g", index=0, description="", citation="")   # OK
R3FeatureSpec(name="test", group="g", index=127, description="", citation="")  # OK (v2)

# Invalid indices:
R3FeatureSpec(name="test", group="g", index=128, description="", citation="")  # ValueError
R3FeatureSpec(name="test", group="g", index=-1, description="", citation="")   # ValueError
```

---

## 7. Relationship to Other Contracts

```
R3FeatureSpec (per-feature metadata)
      |
      | references group by name
      v
BaseSpectralGroup.GROUP_NAME
      |
      | groups registered into
      v
R3FeatureRegistry
      |
      | freeze() produces
      v
R3FeatureMap (contains R3GroupInfo with feature_names)
```

`R3FeatureSpec` provides the finest-grained metadata -- individual feature level. `R3GroupInfo` (from the registry) provides group-level metadata. The two are complementary:

- `R3FeatureSpec` is used for documentation and model-level feature references.
- `R3GroupInfo` is used for runtime index assignment and extraction orchestration.
