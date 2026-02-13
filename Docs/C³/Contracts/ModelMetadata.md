# ModelMetadata -- Evidence Provenance

> **Code**: `mi_beta/contracts/model_metadata.py`
> **Kind**: Frozen Dataclasses (`Citation` + `ModelMetadata`)
> **Imports from**: (none -- leaf types)

## Purpose

Every `BaseModel` must declare its scientific grounding via `ModelMetadata`. This enables systematic evidence auditing: which papers support which dimensions, what is the overall confidence, and what would falsify the model.

---

## Citation

A single empirical finding supporting a model dimension or mechanism. This is NOT a bibliography entry -- it is a specific CLAIM from a specific study.

### Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `author` | `str` | (required) | First author last name (e.g. `"Salimpoor"`) |
| `year` | `int` | (required) | Publication year |
| `finding` | `str` | (required) | One-line summary of the relevant finding |
| `effect_size` | `str` | `""` | Reported effect size (e.g. `"r=0.84"`, `"d=0.67"`, `"F(2,39)=15.48"`). Empty if not applicable |

### Computed Properties

| Property | Return Type | Description |
|----------|-------------|-------------|
| `short_ref` | `str` | Short-form reference: `"Author YEAR"` |

---

## ModelMetadata

Evidence provenance and confidence metadata for a cognitive model.

### Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `citations` | `Tuple[Citation, ...]` | (required) | All supporting citations |
| `evidence_tier` | `str` | (required) | `"alpha"`, `"beta"`, or `"gamma"` (see tiers below) |
| `confidence_range` | `Tuple[float, float]` | (required) | `(low, high)` bounds as fractions in `[0, 1]` |
| `falsification_criteria` | `Tuple[str, ...]` | (required) | What empirical results would invalidate this model; at least one required (Popper 1959) |
| `version` | `str` | `"1.0.0"` | Semantic version string of the model spec |
| `paper_count` | `Optional[int]` | `None` | Number of unique papers. Auto-computed from citations if not set |

### Evidence Tiers

| Tier | Label | Confidence | Studies | Effect Size |
|------|-------|------------|---------|-------------|
| `alpha` | Mechanistic | >90% | k >= 10 | Pooled d or r |
| `beta` | Correlational | >70% | 5 <= k < 10 | Individual study effects |
| `gamma` | Exploratory | <70% | k < 5 | Theoretical or preliminary |

### Computed Properties

| Property | Return Type | Description |
|----------|-------------|-------------|
| `effective_paper_count` | `int` | Uses explicit `paper_count` if set; otherwise counts unique `(author, year)` pairs |
| `is_mechanistic` | `bool` | `True` if `evidence_tier == "alpha"` |

---

## Validation Rules (`__post_init__`)

Enforced at construction time:

1. `evidence_tier` must be one of `"alpha"`, `"beta"`, `"gamma"`; raises `ValueError` otherwise
2. `confidence_range` must satisfy `0 <= low <= high <= 1`; raises `ValueError` otherwise
3. `falsification_criteria` must be non-empty -- every scientific model must be falsifiable; raises `ValueError` if empty

---

## Usage Example

```python
metadata = ModelMetadata(
    citations=(
        Citation("Salimpoor", 2011, "DA release in NAcc correlates with pleasure", "r=0.84"),
        Citation("Ferreri", 2019, "Levodopa enhances musical pleasure causally", "p=0.017"),
        Citation("Berridge", 2003, "Wanting vs liking dissociation in reward", ""),
    ),
    evidence_tier="alpha",
    confidence_range=(0.90, 0.98),
    falsification_criteria=(
        "NAcc DA release fails to correlate with subjective pleasure (r < 0.3)",
        "Pharmacological DA blockade has no effect on musical reward ratings",
    ),
    version="4.0.0",
    paper_count=15,
)
```
