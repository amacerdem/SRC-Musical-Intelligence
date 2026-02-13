# V1 → V2 Migration Guide

Migration from per-model L³ semantic spaces (v1.x) to the unified Brain L³ (v2.x).

## Overview

| Aspect | v1.x (Per-Model) | v2.x (Unified Brain) |
|--------|-------------------|---------------------|
| Scope | One L³ per model (SRP, AAC, VMM) | Single L³ for all models |
| Groups | 4 levels (α, β, γ, δ) | 8 levels (α through θ) |
| Dimensions | ~30-50D per model | 104D unified |
| State | Stateless | ε is stateful |
| Output | Per-model tensors | Concatenated L3Output |
| Vocabulary | None | 12×8 = 96 terms |
| Narrative | None | 4-slot sentence structure |

## Key Changes

### 1. Unified Group System

v1.x had separate L³ definitions for each model (SRP: 40D, AAC: 37D, VMM: 30D).
v2.x defines 8 universal groups that interpret the Brain's unified output regardless of which models are active.

### 2. New Groups (v2.x only)

| Group | Level | Purpose | Why Added |
|-------|-------|---------|-----------|
| ε Epsilon | 5 | Learning dynamics | Captures temporal learning, absent in v1.x |
| ζ Zeta | 6 | Polarity axes | Standardizes bipolar interpretation |
| η Eta | 7 | Vocabulary | Human-readable term quantization |
| θ Theta | 8 | Narrative | Sentence-level description |

### 3. Variable Dimensionality

In mi_beta, α and β groups auto-configure their dimensionality based on active units and models. This means `total_dim` varies at runtime — a departure from v1.x's fixed dimensions.

### 4. Stateful Computation

v1.x groups were all stateless (pure functions of Brain output). v2.x introduces epsilon with:
- EMA accumulators (3 timescales)
- Markov transition model (8×8)
- Welford online variance
- Ring buffer (size 50)

**Implication**: Must call `orchestrator.reset()` between audio files.

### 5. Cross-Group Dependencies

v1.x groups were independent. v2.x introduces a dependency chain:

```
ε → ζ → η
ε → θ ← ζ
```

This requires strict execution ordering (Phase 1 → 1b → 2a → 2b → 2c).

## Dimension Mapping

### α (Computation) — Structural Change

| v1.x (SRP) | v2.x (Brain) | Notes |
|-------------|-------------|-------|
| SRP-specific pathways | Generic unit pathways | Auto-configured |
| Fixed 6D | Variable D | Depends on active units |

### β (Neuroscience) — Structural Change

| v1.x (SRP) | v2.x (Brain) | Notes |
|-------------|-------------|-------|
| SRP brain regions | All unit regions | Auto-configured |
| Fixed 7D | Variable D | Depends on registry |

### γ (Psychology) — Expanded

| v1.x (SRP) | v2.x (Brain) | Notes |
|-------------|-------------|-------|
| 6D (reward, affect) | 13D (reward, ITPRA, aesthetics, emotion, chills) | Expanded scope |

### δ (Validation) — Expanded

| v1.x (SRP) | v2.x (Brain) | Notes |
|-------------|-------------|-------|
| 5D (basic physiology) | 12D (physiology + neuroimaging + behavioral) | Expanded scope |

## Code Migration

### v1.x API
```python
# Per-model semantic interpretation
srp_l3 = SRPSemanticSpace()
result = srp_l3.interpret(srp_output)  # Fixed ~40D
```

### v2.x API
```python
# Unified Brain interpretation
orchestrator = L3Orchestrator(registry=brain.registry)
result = orchestrator.compute(brain_output)  # Variable ~104D
orchestrator.reset()  # Between audio files
```

## Checklist

- [ ] Replace per-model L³ instances with single L3Orchestrator
- [ ] Add `reset()` calls between audio files
- [ ] Update downstream code for variable dimensionality
- [ ] Handle new ε state lifecycle
- [ ] Update dimension name references (v1.x names → v2.x names)
- [ ] Update output shape expectations

---

**Parent**: [00-INDEX.md](00-INDEX.md)
