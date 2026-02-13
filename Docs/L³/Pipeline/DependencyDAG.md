# L³ Pipeline — Dependency DAG

**Version**: 2.1.0
**Scope**: Phase dependency graph, data flow edges, and parallelism opportunities
**Code**: `mi_beta/language/groups/__init__.py`
**Updated**: 2026-02-13

---

## 1. Dependency Graph

```
                            ┌─────────────────────────────────────────────┐
                            │             Phase 1 (Independent)           │
                            │                                             │
BrainOutput ──┬─────────────┼──> alpha  (6D)  ─────────────┐             │
              │             │                               │             │
              ├─────────────┼──> beta   (14D) ─────────────┤             │
              │             │                               │             │
              ├─────────────┼──> gamma  (13D) ─────────────┤             │
              │             │                               │             │
              ├─────────────┼──> delta  (12D) ─────────────┤             │
              │             └─────────────────────────────────────────────┘
              │                                             │
              │             ┌─────────────────────────────────────────────┐
              │             │            Phase 1b (Stateful)              │
              ├─────────────┼──> epsilon (19D) ────────────┤             │
              │             └─────────────────────────────────────────────┘
              │                        │                    │
              │                        │ epsilon_output     │
              │                        ▼                    │
              │             ┌─────────────────────┐         │
              ├─────────────┼──> zeta   (12D) ────┤ Phase 2a│
              │             └─────────────────────┘         │
              │                        │                    │
              │                        │ zeta_output        │
              │                        ▼                    │
              │             ┌─────────────────────┐         │
              ├─────────────┼──> eta    (12D) ────┤ Phase 2b│
              │             └─────────────────────┘         │
              │                        │                    │
              │    epsilon_output      │                    │
              │         │    zeta_output│                    │
              │         ▼              ▼                    │
              │             ┌─────────────────────┐         │
              └─────────────┼──> theta  (16D) ────┤ Phase 2c│
                            └─────────────────────┘         │
                                                            ▼
                                                    torch.cat(all, dim=-1)
                                                    ─────────────────────
                                                    L3Output (B, T, 104D)
```

---

## 2. Edge Descriptions

Each edge represents a data dependency. The orchestrator enforces these by executing phases sequentially.

| Source | Target | Keyword Argument | Tensor Shape | Description |
|--------|--------|-----------------|:------------:|-------------|
| BrainOutput | alpha | *(positional)* | (B, T, D_brain) | Full Brain tensor, per-unit attribution |
| BrainOutput | beta | *(positional)* | (B, T, D_brain) | Full Brain tensor, region activations |
| BrainOutput | gamma | *(positional)* | (B, T, D_brain) | Full Brain tensor, psychological dims |
| BrainOutput | delta | *(positional)* | (B, T, D_brain) | Full Brain tensor, validation dims |
| BrainOutput | epsilon | *(positional)* | (B, T, D_brain) | Full Brain tensor, pleasure + arousal |
| BrainOutput | zeta | *(positional)* | (B, T, D_brain) | Full Brain tensor |
| BrainOutput | eta | *(positional)* | (B, T, D_brain) | Full Brain tensor |
| BrainOutput | theta | *(positional)* | (B, T, D_brain) | Full Brain tensor |
| epsilon | zeta | `epsilon_output=` | (B, T, 19) | Learning dynamics for polarity |
| zeta | eta | `zeta_output=` | (B, T, 12) | Bipolar axes for vocabulary quantization |
| epsilon | theta | `epsilon_output=` | (B, T, 19) | Surprise, PE, precision for narrative |
| zeta | theta | `zeta_output=` | (B, T, 12) | Polarity axes for narrative connectors |

---

## 3. Data Flow Table

Summary of what each group receives:

| Group | Phase | `brain_output` | `epsilon_output` | `zeta_output` |
|-------|:-----:|:--------------:|:----------------:|:-------------:|
| alpha | 1 | Yes | -- | -- |
| beta | 1 | Yes | -- | -- |
| gamma | 1 | Yes | -- | -- |
| delta | 1 | Yes | -- | -- |
| epsilon | 1b | Yes | -- | -- |
| zeta | 2a | Yes | Yes | -- |
| eta | 2b | Yes | -- | Yes |
| theta | 2c | Yes | Yes | Yes |

---

## 4. Phase Ordering Constraints

The dependency DAG imposes a strict partial order on execution:

1. **Phase 1** groups {alpha, beta, gamma, delta} have no mutual dependencies and no upstream L³ dependencies. They depend only on BrainOutput.
2. **Phase 1b** (epsilon) also depends only on BrainOutput but is separated because it maintains state across frames and requires special lifecycle management (reset protocol).
3. **Phase 2a** (zeta) must wait for epsilon to complete, because it consumes `epsilon_output`.
4. **Phase 2b** (eta) must wait for zeta to complete, because it consumes `zeta_output`.
5. **Phase 2c** (theta) must wait for both epsilon and zeta to complete, because it consumes both `epsilon_output` and `zeta_output`. In practice, theta runs after eta (Phase 2b), but it does not depend on eta's output.

---

## 5. Parallelism Opportunities

The dependency structure reveals two parallelism opportunities:

### 5.1 Phase 1 Parallelism

Alpha, beta, gamma, and delta are fully independent. In the current implementation, they execute sequentially in a `for` loop:

```python
for name in ("alpha", "beta", "gamma", "delta"):
    out = self.groups[name].compute(brain_output)
```

These could theoretically be parallelized (e.g., via `torch.futures` or thread pool) since they read the same `brain_output` without mutation. The benefit would be modest because each group's computation is lightweight (no learned parameters, no iteration).

### 5.2 Theta Independence from Eta

Theta depends on epsilon and zeta but not on eta. In principle, eta and theta could execute in parallel once zeta completes. The current implementation runs them sequentially (eta then theta) for simplicity.

### 5.3 Sequential Bottleneck

Epsilon is the pipeline bottleneck. It iterates frame-by-frame (`for t in range(T)`) due to its stateful accumulation, while all other groups process the entire (B, T, D) tensor in a single vectorized pass. No parallelism can help here -- epsilon's frame loop is inherently sequential.

---

## 6. Concatenation Order

The final L3Output tensor concatenates group outputs in insertion order:

```
Index Range    Group     Dim    Phase
─────────────────────────────────────
[0:6]          alpha      6     1
[6:20]         beta      14     1
[20:33]        gamma     13     1
[33:45]        delta     12     1
[45:64]        epsilon   19     1b
[64:76]        zeta      12     2a
[76:88]        eta       12     2b
[88:104]       theta     16     2c
─────────────────────────────────────
Total                   104
```

This order matches the `OrderedDict` insertion order in the L3Orchestrator constructor. Downstream consumers should use the `groups` dict or `dimension_names` for safe indexing rather than hard-coded offsets.

---

## 7. Cross-References

| Related Document | Path |
|-----------------|------|
| Execution sequence detail | [ExecutionModel.md](ExecutionModel.md) |
| Epsilon state lifecycle | [StateManagement.md](StateManagement.md) |
| Performance analysis | [Performance.md](Performance.md) |
| L3Orchestrator contract | [../Contracts/L3Orchestrator.md](../Contracts/L3Orchestrator.md) |
| Group specifications | [../Groups/00-INDEX.md](../Groups/00-INDEX.md) |
| Orchestrator code | `mi_beta/language/groups/__init__.py` |

---

**Parent**: [00-INDEX.md](00-INDEX.md)
