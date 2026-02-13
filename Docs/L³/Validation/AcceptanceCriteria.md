# Acceptance Criteria

Automated validation checks for L³ semantic output correctness.

## Per-Group Checks

### α — Computation (Variable D)

| Check | Expected | Severity |
|-------|----------|----------|
| Tensor shape | `(B, T, N_units×3+2)` — variable | FAIL |
| Range | `[0, 1]` all dimensions | FAIL |
| No NaN/Inf | `True` | FAIL |
| Attribution sum | `Σ(pathway means) > 0` | WARN |

### β — Neuroscience (Variable D)

| Check | Expected | Severity |
|-------|----------|----------|
| Tensor shape | `(B, T, N_regions+6)` — variable | FAIL |
| Range | `[0, 1]` all dimensions | FAIL |
| No NaN/Inf | `True` | FAIL |
| DA-opioid interaction | `β10 ≈ β8 × β9` | WARN |

### γ — Psychology (13D)

| Check | Expected | Severity |
|-------|----------|----------|
| Tensor shape | `(B, T, 13)` | FAIL |
| Range | `[0, 1]` all dimensions | FAIL |
| No NaN/Inf | `True` | FAIL |
| Chill phase coherence | chill_phase peaks follow chill_probability peaks | WARN |

### δ — Validation (12D)

| Check | Expected | Severity |
|-------|----------|----------|
| Tensor shape | `(B, T, 12)` | FAIL |
| Range | `[0, 1]` all dimensions | FAIL |
| No NaN/Inf | `True` | FAIL |
| Physiological plausibility | SCR > 0 when arousal > 0.7 | WARN |

### ε — Learning (19D)

| Check | Expected | Severity |
|-------|----------|----------|
| Tensor shape | `(B, T, 19)` | FAIL |
| Range | `[0, 1]` all dimensions | FAIL |
| No NaN/Inf | `True` | FAIL |
| State initialized | `_state_initialized == True` after first compute | FAIL |
| Familiarity monotone | Non-decreasing over long windows (>100 frames) | WARN |
| Surprise bounded | `surprise ≤ 1.0` after normalization | FAIL |
| Wundt curve | `wundt ≤ 1.0` and peaks at `surprise ≈ 0.5` | WARN |

### ζ — Polarity (12D)

| Check | Expected | Severity |
|-------|----------|----------|
| Tensor shape | `(B, T, 12)` | FAIL |
| Range | `[-1, +1]` all dimensions | FAIL |
| No NaN/Inf | `True` | FAIL |
| Zero-mean | `mean(ζ) ≈ 0` over long signals (>1000 frames) | WARN |

### η — Vocabulary (12D)

| Check | Expected | Severity |
|-------|----------|----------|
| Tensor shape | `(B, T, 12)` | FAIL |
| Range | `[0, 1]` all dimensions | FAIL |
| Quantization | Values are multiples of `1/63` | FAIL |
| No NaN/Inf | `True` | FAIL |

### θ — Narrative (16D)

| Check | Expected | Severity |
|-------|----------|----------|
| Tensor shape | `(B, T, 16)` | FAIL |
| Range | `[0, 1]` all dimensions | FAIL |
| Subject softmax | `Σ(θ0:4) ≈ 1.0` (±0.01) | FAIL |
| Connector coverage | At least one connector > 0.3 per frame | WARN |
| No NaN/Inf | `True` | FAIL |

## Orchestrator-Level Checks

| Check | Expected | Severity |
|-------|----------|----------|
| Total dimension | `sum(g.OUTPUT_DIM) == L3Output.tensor.shape[-1]` | FAIL |
| Group ordering | Groups appear in level order (1→8) | FAIL |
| Reset behavior | After `reset()`, epsilon state re-initializes on next compute | FAIL |
| Dimension names | Total names count == total_dim | FAIL |

## Severity Levels

- **FAIL**: Test fails, blocks deployment
- **WARN**: Logs warning, investigation recommended

---

**Parent**: [00-INDEX.md](00-INDEX.md)
