# L3Orchestrator — Group Coordination Contract

**Scope**: The central coordinator for all 8 L³ semantic groups. Manages group registration, phase-ordered execution, dependency injection between groups, output assembly, and state reset delegation.

**Code file**: `mi_beta/language/groups/__init__.py`

---

## 1. Constructor

```python
class L3Orchestrator:
    def __init__(self, registry=None):
        self.groups = OrderedDict([
            ("alpha", AlphaGroup()),
            ("beta", BetaGroup(registry=registry)),
            ("gamma", GammaGroup()),
            ("delta", DeltaGroup()),
            ("epsilon", EpsilonGroup()),
            ("zeta", ZetaGroup()),
            ("eta", EtaGroup()),
            ("theta", ThetaGroup()),
        ])
```

**Parameters**:
- `registry` (optional) -- `ModelRegistry` instance, passed to `BetaGroup` for auto-configuring brain region dimensions from active model declarations

**Group registration**: Groups are stored in an `OrderedDict` that preserves insertion order. This order matches the phase execution sequence.

---

## 2. Group Registration

| Key | Group Class | Level | Dim | Phase |
|-----|-------------|:-----:|:---:|:-----:|
| `"alpha"` | `AlphaGroup` | 1 | 6* | 1 |
| `"beta"` | `BetaGroup` | 2 | 14* | 1 |
| `"gamma"` | `GammaGroup` | 3 | 13 | 1 |
| `"delta"` | `DeltaGroup` | 4 | 12 | 1 |
| `"epsilon"` | `EpsilonGroup` | 5 | 19 | 1b |
| `"zeta"` | `ZetaGroup` | 6 | 12 | 2a |
| `"eta"` | `EtaGroup` | 7 | 12 | 2b |
| `"theta"` | `ThetaGroup` | 8 | 16 | 2c |

*Variable dimensionality in mi_beta (alpha auto-configures per active units, beta per unique brain regions).

---

## 3. Phase Execution Sequence

The `compute()` method executes groups in strict dependency order across 5 phases:

### Phase 1 -- Independent (alpha, beta, gamma, delta)

```python
for name in ("alpha", "beta", "gamma", "delta"):
    outputs[name] = self.groups[name].compute(brain_output)
```

- Read only `brain_output` (BrainOutput from C³)
- No mutual dependencies between these 4 groups
- Could theoretically be parallelized (executed sequentially in mi_beta)

### Phase 1b -- Stateful (epsilon)

```python
eps_out = self.groups["epsilon"].compute(brain_output)
outputs["epsilon"] = eps_out
```

- Reads only `brain_output`
- Maintains internal state across frames (EMA, Markov, Welford, ring buffer)
- Must execute frame-by-frame (stateful accumulation)
- Separated from Phase 1 because it requires special lifecycle management

### Phase 2a -- Dependent on epsilon (zeta)

```python
zeta_out = self.groups["zeta"].compute(brain_output, epsilon_output=eps_out.tensor)
outputs["zeta"] = zeta_out
```

- Reads `brain_output` AND epsilon's output tensor
- Uses epsilon's learning dynamics (surprise, entropy, precision) for polarity axes
- Cannot execute until epsilon is complete

### Phase 2b -- Dependent on zeta (eta)

```python
eta_out = self.groups["eta"].compute(brain_output, zeta_output=zeta_out.tensor)
outputs["eta"] = eta_out
```

- Reads `brain_output` AND zeta's output tensor
- Quantizes zeta's bipolar polarity axes into 64-gradation vocabulary
- Cannot execute until zeta is complete

### Phase 2c -- Dependent on epsilon + zeta (theta)

```python
theta_out = self.groups["theta"].compute(
    brain_output,
    epsilon_output=eps_out.tensor,
    zeta_output=zeta_out.tensor,
)
outputs["theta"] = theta_out
```

- Reads `brain_output` AND epsilon's output tensor AND zeta's output tensor
- Uses epsilon for predicate (prediction errors) and modifier (precision, surprise)
- Uses zeta for connector (polarity of valence and tension)
- Cannot execute until both Phase 1b and Phase 2a are complete

---

## 4. Dependency DAG

```
BrainOutput
    |
    +---> alpha   (6D)  ---+
    |                       |
    +---> beta   (14D)  ---+
    |                       |
    +---> gamma  (13D)  ---+--> [Phase 1 complete]
    |                       |
    +---> delta  (12D)  ---+
    |
    +---> epsilon (19D) ---+--> [Phase 1b complete]
               |           |
               |           +---> zeta (12D) ---+--> [Phase 2a complete]
               |                   |           |
               |                   |           +---> eta (12D) -- [Phase 2b]
               |                   |
               +-------+-----------+
                       |
                       +---> theta (16D) ------- [Phase 2c complete]
```

---

## 5. Output Assembly

After all groups have been computed, the orchestrator concatenates their tensors along the last dimension:

```python
tensors = [outputs[name].tensor for name in self.groups]
combined = torch.cat(tensors, dim=-1)  # (B, T, total_dim)

return L3Output(
    model_name="Brain",
    groups=outputs,
    tensor=combined,
)
```

**Concatenation order**: alpha, beta, gamma, delta, epsilon, zeta, eta, theta (matching the `OrderedDict` insertion order).

**Index ranges** (reference specification):
```
[0:6]     alpha    6D
[6:20]    beta    14D
[20:33]   gamma   13D
[33:45]   delta   12D
[45:64]   epsilon 19D
[64:76]   zeta    12D
[76:88]   eta     12D
[88:104]  theta   16D
```

---

## 6. Properties

### `total_dim -> int`

Returns the sum of all group `OUTPUT_DIM` values:

```python
@property
def total_dim(self) -> int:
    return sum(g.OUTPUT_DIM for g in self.groups.values())
```

In the reference specification, `total_dim = 104`. In mi_beta, this value is dynamic because alpha and beta auto-configure their dimensionality.

---

## 7. Reset Protocol

```python
def reset(self):
    self.groups["epsilon"].reset()
```

**Purpose**: Clears epsilon's accumulated state between audio files. Epsilon is the only stateful group, so `reset()` only delegates to epsilon.

**When to call**: Between processing different audio files. Failure to reset will cause epsilon's state from one audio file to bleed into the next, corrupting learning dynamics (surprise, entropy, prediction errors).

**What it does**: Sets `epsilon._state_initialized = False`, so the next `compute()` call triggers a fresh `_init_state()` with clean accumulators.

See [EpsilonStateContract.md](EpsilonStateContract.md) for full state lifecycle details.

---

## 8. Typical Usage

```python
from mi_beta.language import L3Orchestrator

# Initialize
orchestrator = L3Orchestrator(registry=model_registry)

# Process audio file 1
l3_output = orchestrator.compute(brain_output_1)
# l3_output.tensor shape: (B, T, 104)
# l3_output.groups["gamma"].tensor shape: (B, T, 13)

# Reset before next file
orchestrator.reset()

# Process audio file 2
l3_output = orchestrator.compute(brain_output_2)
```

---

## 9. Relationship to Other Contracts

| Contract | Relationship |
|----------|-------------|
| [BaseSemanticGroup](BaseSemanticGroup.md) | Orchestrator calls `compute()` on all group instances |
| [SemanticGroupOutput](SemanticGroupOutput.md) | Orchestrator collects these from each group, concatenates tensors |
| [EpsilonStateContract](EpsilonStateContract.md) | Orchestrator delegates `reset()` to epsilon's state manager |
| [BaseModelSemanticAdapter](BaseModelSemanticAdapter.md) | Adapters operate upstream, preparing inputs before orchestration |

---

## 10. Cross-References

| Related Document | Path |
|-----------------|------|
| Pipeline execution model | [../Pipeline/ExecutionModel.md](../Pipeline/ExecutionModel.md) |
| Dependency DAG | [../Pipeline/DependencyDAG.md](../Pipeline/DependencyDAG.md) |
| State management | [../Pipeline/StateManagement.md](../Pipeline/StateManagement.md) |
| Group specifications | [../Groups/00-INDEX.md](../Groups/00-INDEX.md) |
| L³ architecture | [../L3-SEMANTIC-ARCHITECTURE.md](../L3-SEMANTIC-ARCHITECTURE.md) |

---

**Parent**: [00-INDEX.md](00-INDEX.md)
