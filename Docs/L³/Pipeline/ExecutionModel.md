# L³ Pipeline — Execution Model

**Version**: 2.1.0
**Scope**: Step-by-step orchestrator execution sequence
**Code**: `mi_beta/language/groups/__init__.py` (L3Orchestrator.compute)
**Updated**: 2026-02-13

---

## 1. Overview

The `L3Orchestrator.compute(brain_output)` method executes 8 semantic groups across 5 phases in strict dependency order. The method is deterministic, stateless (except for epsilon's internal state), and produces a single concatenated `L3Output` tensor.

**Input**: `BrainOutput` with tensor shape `(B, T, D_brain)`
**Output**: `L3Output` with tensor shape `(B, T, 104)` (reference spec)

---

## 2. Initialization

Before `compute()` is called, the orchestrator must be constructed:

```python
orchestrator = L3Orchestrator(registry=model_registry)
```

The constructor creates 8 group instances in an `OrderedDict`:

```python
self.groups = OrderedDict([
    ("alpha",   AlphaGroup()),
    ("beta",    BetaGroup(registry=registry)),
    ("gamma",   GammaGroup()),
    ("delta",   DeltaGroup()),
    ("epsilon", EpsilonGroup()),
    ("zeta",    ZetaGroup()),
    ("eta",     EtaGroup()),
    ("theta",   ThetaGroup()),
])
```

Only `BetaGroup` receives the `registry` parameter, which it uses to auto-discover brain region declarations from active models.

---

## 3. Execution Sequence

### Step 0: Prepare Accumulators

```python
group_outputs: Dict[str, SemanticGroupOutput] = {}
tensors = []
```

Two data structures are initialized:
- `group_outputs`: stores the full `SemanticGroupOutput` from each group (includes metadata)
- `tensors`: accumulates raw tensors for final concatenation

### Step 1: Phase 1 -- Independent Groups

```python
for name in ("alpha", "beta", "gamma", "delta"):
    out = self.groups[name].compute(brain_output)
    group_outputs[name] = out
    tensors.append(out.tensor)
```

Each group receives only `brain_output` (no kwargs). They execute sequentially in insertion order. Each returns a `SemanticGroupOutput` containing:
- `group_name`: str (e.g., `"alpha"`)
- `level`: int (e.g., `1`)
- `tensor`: Tensor of shape `(B, T, group_dim)`
- `dimension_names`: tuple of str

**Outputs accumulated**:
| Group | Tensor Shape | Appended to `tensors` |
|-------|:------------:|:---------------------:|
| alpha | (B, T, 6*) | Yes |
| beta | (B, T, 14*) | Yes |
| gamma | (B, T, 13) | Yes |
| delta | (B, T, 12) | Yes |

*Variable dimensionality in mi_beta.

### Step 2: Phase 1b -- Epsilon (Stateful)

```python
eps_out = self.groups["epsilon"].compute(brain_output)
group_outputs["epsilon"] = eps_out
tensors.append(eps_out.tensor)
```

Epsilon receives only `brain_output` but internally:
1. Checks if state is initialized; if not (first call or after reset), calls `_init_state(B, device, dtype)`
2. Extracts `pleasure` and `arousal` from BrainOutput (with fallback to mean/variance)
3. Iterates frame-by-frame (`for t in range(T)`), updating all internal state at each frame
4. Returns `SemanticGroupOutput` with tensor shape `(B, T, 19)`

The `eps_out` variable is retained for passing to downstream groups.

### Step 3: Phase 2a -- Zeta (Depends on Epsilon)

```python
zeta_out = self.groups["zeta"].compute(
    brain_output,
    epsilon_output=eps_out.tensor,
)
group_outputs["zeta"] = zeta_out
tensors.append(zeta_out.tensor)
```

Zeta receives `brain_output` plus `epsilon_output` as a keyword argument. The epsilon tensor `(B, T, 19)` provides learning dynamics (surprise, entropy, precision) that zeta uses to compute bipolar polarity axes.

**Output**: tensor shape `(B, T, 12)` with range `[-1, +1]`.

### Step 4: Phase 2b -- Eta (Depends on Zeta)

```python
eta_out = self.groups["eta"].compute(
    brain_output,
    zeta_output=zeta_out.tensor,
)
group_outputs["eta"] = eta_out
tensors.append(eta_out.tensor)
```

Eta receives `brain_output` plus `zeta_output` as a keyword argument. The zeta tensor `(B, T, 12)` provides bipolar polarity axes that eta quantizes into 64-gradation vocabulary indices.

**Output**: tensor shape `(B, T, 12)` with range `[0, 1]`.

### Step 5: Phase 2c -- Theta (Depends on Epsilon + Zeta)

```python
theta_out = self.groups["theta"].compute(
    brain_output,
    epsilon_output=eps_out.tensor,
    zeta_output=zeta_out.tensor,
)
group_outputs["theta"] = theta_out
tensors.append(theta_out.tensor)
```

Theta receives `brain_output` plus both `epsilon_output` and `zeta_output`. It uses:
- Epsilon's learning dynamics for Predicate (temporal change) and Modifier (confidence/magnitude)
- Zeta's polarity axes for Connector (valence/tension direction)
- Brain output for Subject (which aspect dominates, via softmax competition)

**Output**: tensor shape `(B, T, 16)` with range `[0, 1]`.

### Step 6: Assembly

```python
combined = torch.cat(tensors, dim=-1)  # (B, T, total_dim)

return L3Output(
    model_name="Brain",
    groups=group_outputs,
    tensor=combined,
)
```

All 8 tensors are concatenated along the last dimension in insertion order. The resulting `L3Output` contains:
- `model_name`: `"Brain"` (hardcoded)
- `groups`: dict of all 8 `SemanticGroupOutput` objects (keyed by group name)
- `tensor`: the concatenated tensor `(B, T, 104)`

---

## 4. Execution Timeline

```
Time ──>

Phase 1:   [alpha]──[beta]──[gamma]──[delta]
                                              \
Phase 1b:                                      [epsilon ──── T frames ────]
                                                                           \
Phase 2a:                                                                   [zeta]
                                                                                  \
Phase 2b:                                                                          [eta]
                                                                                        \
Phase 2c:                                                                                [theta]
                                                                                               \
Assembly:                                                                                       [cat]
```

The total wall-clock time is dominated by epsilon's frame loop. Phase 1 groups and Phase 2 groups are individually fast (vectorized tensor operations).

---

## 5. Error Handling

The current implementation has no explicit error handling within `compute()`. If any group raises an exception, it propagates to the caller. Potential failure modes:

| Failure | Cause | Effect |
|---------|-------|--------|
| Shape mismatch | BrainOutput has unexpected D | Group `compute()` raises at dimension extraction |
| Device mismatch | Epsilon state on CPU, input on GPU | Tensor operation error at EMA update |
| Batch size change | B differs from epsilon's initialized B | Epsilon re-initializes state (handled by `_batch_size` check) |
| Missing `get_dim` | Brain has no "pleasure" or "arousal" | `_safe_get_dim` returns fallback constant 0.5 |

---

## 6. Reset Protocol

Between audio files, the caller must invoke:

```python
orchestrator.reset()
```

This delegates to `self.groups["epsilon"].reset()`, which sets `_state_initialized = False`. The next `compute()` call triggers fresh state allocation. No other groups require reset because they are stateless.

**Failure to reset**: Epsilon's Markov model, EMA accumulators, and ring buffer carry state from the previous audio file into the next, corrupting all 19 epsilon dimensions and all downstream groups that depend on them (zeta, eta, theta).

---

## 7. L3Output Structure

The returned `L3Output` dataclass provides access at multiple granularities:

```python
l3 = orchestrator.compute(brain_output)

# Full tensor
l3.tensor                    # (B, T, 104)

# Per-group access
l3.groups["gamma"].tensor    # (B, T, 13)
l3.groups["gamma"].level     # 3
l3.groups["gamma"].dimension_names  # ("reward_intensity", "reward_type", ...)

# Total dimensionality
orchestrator.total_dim       # 104
```

---

## 8. Cross-References

| Related Document | Path |
|-----------------|------|
| Dependency DAG | [DependencyDAG.md](DependencyDAG.md) |
| State management | [StateManagement.md](StateManagement.md) |
| Performance analysis | [Performance.md](Performance.md) |
| L3Orchestrator contract | [../Contracts/L3Orchestrator.md](../Contracts/L3Orchestrator.md) |
| Epsilon group | [../Groups/Independent/Epsilon.md](../Groups/Independent/Epsilon.md) |
| Orchestrator code | `mi_beta/language/groups/__init__.py` |

---

**Parent**: [00-INDEX.md](00-INDEX.md)
