# L3Orchestrator — Group Coordination

Manages the dependency-ordered execution of all 8 semantic groups.

**Code**: `mi_beta/language/groups/__init__.py`

## Construction

```python
class L3Orchestrator:
    def __init__(self, registry=None):
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

Groups are stored in an `OrderedDict` that preserves insertion (and execution) order. The optional `registry` parameter configures `BetaGroup` with the brain region registry.

## Phase Execution

### `compute(brain_output: BrainOutput) → L3Output`

Executes groups in strict dependency order:

| Step | Phase | Groups | Input | Output |
|------|-------|--------|-------|--------|
| 1 | Phase 1 | alpha, beta, gamma, delta | `brain_output` only | Independent |
| 2 | Phase 1b | epsilon | `brain_output` only | Stateful accumulation |
| 3 | Phase 2a | zeta | `brain_output` + `epsilon_output` | Bipolar polarity |
| 4 | Phase 2b | eta | `brain_output` + `zeta_output` | Vocabulary quantization |
| 5 | Phase 2c | theta | `brain_output` + `epsilon_output` + `zeta_output` | Narrative structure |
| 6 | Assembly | — | All 8 `SemanticGroupOutput` tensors | `torch.cat(dim=-1)` |

### Phase 1 (Independent Loop)

```python
for name in ("alpha", "beta", "gamma", "delta"):
    out = self.groups[name].compute(brain_output)
    group_outputs[name] = out
    tensors.append(out.tensor)
```

These 4 groups are independent — they read only `brain_output` and produce no cross-group dependencies. They could theoretically run in parallel.

### Phase 1b (Stateful)

```python
eps_out = self.groups["epsilon"].compute(brain_output)
```

Epsilon reads only `brain_output` but maintains internal state (EMA accumulators, Markov transitions, ring buffer). Must run before Phase 2.

### Phase 2 (Dependent Chain)

```python
zeta_out  = self.groups["zeta"].compute(brain_output, epsilon_output=eps_out.tensor)
eta_out   = self.groups["eta"].compute(brain_output, zeta_output=zeta_out.tensor)
theta_out = self.groups["theta"].compute(brain_output, epsilon_output=eps_out.tensor,
                                                        zeta_output=zeta_out.tensor)
```

Each Phase 2 group receives specific kwargs from earlier groups. This chain MUST execute sequentially.

## Reset

```python
def reset(self):
    self.groups["epsilon"].reset()
```

Delegates to epsilon's `reset()`. Must be called between audio files.

## Properties

### `total_dim → int`

```python
@property
def total_dim(self) -> int:
    return sum(g.OUTPUT_DIM for g in self.groups.values())
```

Variable in mi_beta (depends on active units/models for α and β).

---

**Parent**: [00-INDEX.md](00-INDEX.md)
**See also**: [../Pipeline/ExecutionModel.md](../Pipeline/ExecutionModel.md)
