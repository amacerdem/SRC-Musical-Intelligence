# C³ Neurochemical Systems -- Index

> **Module**: `mi_beta.brain.neurochemicals`
> **Manager**: `NeurochemicalStateManager` -- high-level typed wrapper
> **Contract**: `NeurochemicalType` (enum) + `NeurochemicalState` (registry)

## Overview

MI-Beta models neurochemical dynamics at the regional level. Instead of a single scalar "dopamine", models write and read region-specific neurochemical state (e.g. dopamine in NAcc vs dopamine in caudate).

Six neurotransmitter systems are defined in `NeurochemicalType`:

| # | System | Enum Value | Status | Primary Role in Music |
|---|--------|-----------|--------|----------------------|
| 1 | [Dopamine (DA)](Dopamine.md) | `DOPAMINE` | Implemented | Reward prediction error, anticipation, pleasure |
| 2 | [Endogenous Opioids](Opioid.md) | `OPIOID` | Implemented | Hedonic "liking", consummatory pleasure |
| 3 | [Serotonin (5-HT)](Serotonin.md) | `SEROTONIN` | Implemented | Mood regulation, emotional valence bias |
| 4 | [Norepinephrine (NE)](Norepinephrine.md) | `NOREPINEPHRINE` | Implemented | Arousal, attentional gating, orienting |
| 5 | GABA | `GABA` | Defined, no submodule | Inhibitory modulation, timing precision |
| 6 | Glutamate | `GLUTAMATE` | Defined, no submodule | Excitatory drive, cortical-subcortical communication |

GABA and Glutamate are defined in the enum but do not yet have dedicated submodules. They will be added as models require them.

---

## NeurochemicalState Write/Read Protocol

The `NeurochemicalState` class provides a mutable registry for neurochemical signal tensors within a single compute pass. This avoids hard-wiring model-to-model tensor passing and makes cross-unit dependencies explicit.

### Protocol

```python
state = NeurochemicalState()

# Model A writes reward signals
state.write(NeurochemicalType.DOPAMINE, "NAcc", da_nacc_tensor)
state.write(NeurochemicalType.OPIOID, "nacc_shell", opioid_tensor)

# Model B reads them for downstream computation
da = state.read(NeurochemicalType.DOPAMINE, "NAcc")  # Returns Optional[Tensor]

# Between pipeline passes
state.reset()
```

### Rules

1. **Write-once per pass**: Writing to the same `(chemical, region)` key twice in the same pass raises `ValueError`. Call `reset()` between passes.
2. **Read returns Optional**: If no model has written to a key, `read()` returns `None`.
3. **Not thread-safe**: Designed for single-pass pipeline use only.
4. **Tensors are (B, T) or (B, T, D)**: All signals follow standard batched temporal shape.

---

## NeurochemicalStateManager

The `NeurochemicalStateManager` wraps `NeurochemicalState` with typed convenience methods:

| Method | Shorthand for |
|--------|--------------|
| `write_da(region, tensor)` | `state.write(NeurochemicalType.DOPAMINE, region, tensor)` |
| `read_da(region)` | `state.read(NeurochemicalType.DOPAMINE, region)` |
| `write_opioid(region, tensor)` | `state.write(NeurochemicalType.OPIOID, region, tensor)` |
| `read_opioid(region)` | `state.read(NeurochemicalType.OPIOID, region)` |
| `write_serotonin(region, tensor)` | `state.write(NeurochemicalType.SEROTONIN, region, tensor)` |
| `read_serotonin(region)` | `state.read(NeurochemicalType.SEROTONIN, region)` |
| `write_ne(region, tensor)` | `state.write(NeurochemicalType.NOREPINEPHRINE, region, tensor)` |
| `read_ne(region)` | `state.read(NeurochemicalType.NOREPINEPHRINE, region)` |
| `write_gaba(region, tensor)` | `state.write(NeurochemicalType.GABA, region, tensor)` |
| `write_glutamate(region, tensor)` | `state.write(NeurochemicalType.GLUTAMATE, region, tensor)` |

### Query Helpers

| Property | Return Type | Description |
|----------|-------------|-------------|
| `da_keys` | `List[str]` | All region keys with DA signals |
| `opioid_keys` | `List[str]` | All region keys with opioid signals |
| `serotonin_keys` | `List[str]` | All region keys with 5-HT signals |
| `ne_keys` | `List[str]` | All region keys with NE signals |
| `all_signals` | `Dict[str, List[str]]` | Map from chemical name to list of region keys |
| `summary` | `str` | Human-readable summary for debugging |

---

## Code References

| File | Contents |
|------|----------|
| `mi_beta/contracts/neurochemical.py` | `NeurochemicalType` enum, `NeurochemicalState` registry |
| `mi_beta/brain/neurochemicals/__init__.py` | `NeurochemicalStateManager` wrapper |
| `mi_beta/brain/neurochemicals/dopamine.py` | DA regions, thresholds, reference values |
| `mi_beta/brain/neurochemicals/opioid.py` | Opioid regions, hedonic hotspots |
| `mi_beta/brain/neurochemicals/serotonin.py` | 5-HT regions, mood modulation, DA interaction |
| `mi_beta/brain/neurochemicals/norepinephrine.py` | NE regions, arousal/attention, DA interaction |
