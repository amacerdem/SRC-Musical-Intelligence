# L³ Extension Guide

**Scope**: Developer guide for extending the L³ semantic interpretation layer — adding groups, dimensions, polarity axes, vocabulary terms, and adapters.

---

## 1. Architecture Overview

L³ consists of 8 semantic groups (α→θ) managed by `L3Orchestrator`. Each group is a `BaseSemanticGroup` subclass that produces a `SemanticGroupOutput` tensor. Groups are executed in dependency order across two phases.

```
BaseSemanticGroup (ABC)
├── AlphaGroup     Level 1  (6D)   Phase 1   independent
├── BetaGroup      Level 2  (14D)  Phase 1   independent
├── GammaGroup     Level 3  (13D)  Phase 1   independent
├── DeltaGroup     Level 4  (12D)  Phase 1   independent
├── EpsilonGroup   Level 5  (19D)  Phase 1b  stateful
├── ZetaGroup      Level 6  (12D)  Phase 2a  reads ε
├── EtaGroup       Level 7  (12D)  Phase 2b  reads ζ
└── ThetaGroup     Level 8  (16D)  Phase 2c  reads ε + ζ
```

---

## 2. Adding a New Semantic Group

### Step 1: Create group file

Create `mi_beta/language/groups/{name}.py`:

```python
from ...contracts.base_semantic_group import BaseSemanticGroup, SemanticGroupOutput

class IotaGroup(BaseSemanticGroup):
    LEVEL = 9
    GROUP_NAME = "iota"
    DISPLAY_NAME = "iota"
    OUTPUT_DIM = 8  # your dimensionality

    @property
    def dimension_names(self):
        return ["dim_1", "dim_2", ...]  # must match OUTPUT_DIM

    def compute(self, brain_output, **kwargs):
        # Your computation here
        tensor = ...  # (B, T, OUTPUT_DIM)
        return SemanticGroupOutput(
            group_name=self.GROUP_NAME,
            level=self.LEVEL,
            tensor=tensor,
            dimension_names=tuple(self.dimension_names),
        )
```

### Step 2: Register in L3Orchestrator

Edit `mi_beta/language/groups/__init__.py`:

```python
from .iota import IotaGroup

class L3Orchestrator:
    def __init__(self, ...):
        self.groups = OrderedDict([
            ...existing groups...
            ("iota", IotaGroup()),
        ])
```

### Step 3: Add to execution phase

If the new group is independent (Phase 1), add to the Phase 1 loop. If it depends on other groups, add to the appropriate Phase 2 step.

### Step 4: Create documentation

1. Create `Docs/L³/Groups/{Independent or Dependent}/{Name}.md`
2. Create `Docs/L³/Epistemology/{Name}.md`
3. Update `Docs/L³/Registry/GroupMap.md` with new index range
4. Update `Docs/L³/Registry/DimensionCatalog.md` with new dimensions
5. Update `Docs/L³/00-INDEX.md` directory structure

---

## 3. Adding Dimensions to an Existing Group

### Step 1: Update the group code

In `mi_beta/language/groups/{group}.py`:
- Increment `OUTPUT_DIM`
- Add new name(s) to `dimension_names`
- Update `compute()` to produce the additional dimension(s)

### Step 2: Update documentation

1. Update `Docs/L³/Registry/DimensionCatalog.md` — add new rows
2. Update `Docs/L³/Registry/GroupMap.md` — adjust index ranges
3. Update the specific group doc in `Docs/L³/Groups/`

---

## 4. Adding a Polarity Axis (ζ)

### Step 1: Update ZetaGroup

In `mi_beta/language/groups/zeta.py`:
- Add new axis to `POLARITY_AXES` constant
- Increment `OUTPUT_DIM`
- Update `dimension_names`
- Add computation in `compute()`

### Step 2: Update EtaGroup

In `mi_beta/language/groups/eta.py`:
- Add corresponding vocabulary terms to `AXIS_TERMS`
- Add axis name to `AXIS_NAMES`
- Increment `OUTPUT_DIM`

### Step 3: Update documentation

1. `Docs/L³/Vocabulary/AxisDefinitions.md` — add axis definition
2. `Docs/L³/Vocabulary/TermCatalog.md` — add 8 band terms
3. `Docs/L³/Groups/Dependent/Zeta.md` — add axis spec
4. `Docs/L³/Groups/Dependent/Eta.md` — add vocabulary spec
5. Update DimensionCatalog and GroupMap

---

## 5. Adding Vocabulary Terms

The vocabulary system uses 8 intensity bands per axis. To change terms:

### In code

Edit `AXIS_TERMS` in `mi_beta/language/groups/eta.py`:

```python
AXIS_TERMS = {
    "new_axis": (
        "band_0", "band_1", "band_2", "band_3",   # negative pole
        "neutral",                                    # midpoint
        "band_5", "band_6", "band_7",               # positive pole
    ),
    ...
}
```

### Design principles

- Band 0 = extreme negative pole, Band 7 = extreme positive pole
- Band 4 = "neutral" for all axes
- Terms should be single words or very short phrases
- 64 gradations (8 bands × 8 sub-gradations) provide ~1.56% step size
- Step size is below human JND (~3%), ensuring perceptually smooth gradation

### In documentation

Update `Docs/L³/Vocabulary/TermCatalog.md` to match code exactly.

---

## 6. Adding a Per-Unit Adapter

### Step 1: Create adapter file

Create `mi_beta/language/adapters/{unit}_adapter.py`:

```python
from ._base_adapter import BaseModelSemanticAdapter

class SPUAdapter(BaseModelSemanticAdapter):
    UNIT_NAME = "SPU"

    def adapt(self, unit_output):
        return {"tensor": unit_output.tensor}
```

### Step 2: Create documentation

Create `Docs/L³/Adapters/{UNIT}-L3-ADAPTER.md` documenting:
- Which unit output dimensions map to which semantic inputs
- The semantic interpretation of each mapping
- Current status (stub / partial / full)

---

## 7. Making a Group Stateful

Only ε (Epsilon) is currently stateful. To make another group stateful:

1. Add internal state tensors as instance attributes
2. Implement lazy initialization in `compute()` (check `_state_initialized`)
3. Implement `reset()` method to clear all state
4. Register the group in `L3Orchestrator.reset()`
5. Document state layout in `Docs/L³/Contracts/EpsilonStateContract.md` (or create new contract)
6. Update `Docs/L³/Pipeline/StateManagement.md`

---

## 8. Checklist for Any L³ Extension

- [ ] Code change implemented and tested
- [ ] `DimensionCatalog.md` updated with all new dimensions
- [ ] `GroupMap.md` index ranges updated (all ranges must be contiguous and sum correctly)
- [ ] Relevant group doc updated
- [ ] `00-INDEX.md` updated if directory structure changed
- [ ] `CHANGELOG.md` entry added
- [ ] All dimension names follow snake_case convention
- [ ] Every new dimension has a formula and at least one primary citation
- [ ] Output range documented ([0,1] or [-1,+1])

---

**Parent**: [00-INDEX.md](00-INDEX.md)
