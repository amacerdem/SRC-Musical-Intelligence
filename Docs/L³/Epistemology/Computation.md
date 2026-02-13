# L³ Epistemology — Computation

**Level**: 1 (α)
**Question**: HOW was this computed?
**Audience**: Engineers, system designers, auditors
**Version**: 2.1.0
**Updated**: 2026-02-13

---

## Overview

The Computation group answers the most fundamental epistemological question: given a Brain output, what produced it? This is the **white-box accountability** layer. Every L³ interpretation rests on computation that must be traceable and auditable.

Alpha produces 6 dimensions: 4 attribution scores (one per Brain output category), 1 certainty measure, and 1 signed activation summary.

---

## Core Concepts

### White-Box Attribution

Attribution traces the Brain's output back to its input pathways. Rather than treating the Brain as a black box, α decomposes the output into contributions from identifiable subsystems:

- **Shared attribution** (α0): contribution of shared early processing (Brain[0:4])
- **Reward attribution** (α1): contribution of reward-related models (Brain[4:13])
- **Affect attribution** (α2): contribution of affect-related models (Brain[13:19])
- **Autonomic attribution** (α3): contribution of autonomic/physiological models (Brain[19:24])

Each attribution is computed as the mean activation of its input slice — a transparent, differentiable operation.

### Bayesian Precision as Computation Certainty

How confident should we be in this frame's output? α4 (`computation_certainty`) answers this using **Bayesian precision** — the inverse of variance across the active Brain dimensions:

```
certainty = 1 / (1 + Var(Brain[0:26]))
```

When Brain outputs are consistent (low variance), certainty is high. When they diverge (high variance), certainty drops. This directly implements the **precision-weighting** principle from Friston's (2010) free energy framework: signals should be weighted by their reliability.

### Bipolar Activation

α5 (`bipolar_activation`) provides a single signed summary of the Brain's current state:

```
bipolar_activation = 0.5 * (prediction_error + f03_valence)
```

This collapses the high-dimensional Brain output into a [-1, +1] scalar that captures the net direction of processing — whether the current frame is positively or negatively valenced overall.

---

## Dimensions

| Local | Name | Range | Formula | Citation |
|:-----:|------|:-----:|---------|----------|
| α0 | `shared_attribution` | [0, 1] | mean(Brain[0:4]) | White-box attribution |
| α1 | `reward_attribution` | [0, 1] | mean(Brain[4:13]) | White-box attribution |
| α2 | `affect_attribution` | [0, 1] | mean(Brain[13:19]) | White-box attribution |
| α3 | `autonomic_attribution` | [0, 1] | mean(Brain[19:24]) | White-box attribution |
| α4 | `computation_certainty` | [0, 1] | 1 / (1 + Var(Brain[0:26])) | Bayesian precision |
| α5 | `bipolar_activation` | [-1, 1] | 0.5 * (PE + valence) | Signed summary |

---

## Key Theory

**Bayesian brain hypothesis** (Friston 2010): The brain operates as an inference engine that minimizes prediction error. Precision (inverse variance) determines how much weight a signal receives. α4 implements this principle at the system level — frames with inconsistent Brain outputs are flagged as uncertain.

**Attribution methods**: Tracing output to input is a standard practice in interpretable AI. α0-α3 provide per-category attribution that allows engineers to diagnose which Brain subsystem drives a given semantic interpretation.

---

## Relevance

Engineers and system designers need α to:

1. **Debug**: When L³ output seems wrong, α reveals which Brain subsystem is responsible.
2. **Trust**: α4 provides a built-in confidence measure — downstream consumers can threshold on certainty.
3. **Monitor**: Tracking attribution over time reveals whether the system's behavior is stable or drifting.

---

## Key Citations

- Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*, 11(2), 127-138.
- Bayesian brain hypothesis — precision-weighting as reliability signal.

---

**Parent**: [00-INDEX.md](00-INDEX.md)
**See also**: [Groups/Independent/Alpha.md](../Groups/Independent/Alpha.md) for implementation details | [Registry/DimensionCatalog.md](../Registry/DimensionCatalog.md) for dimension metadata
