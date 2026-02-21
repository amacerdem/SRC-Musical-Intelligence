# Perception-Imagery Overlap

**Source**: STU-β2-TPIO (Timbre Perception-Imagery Overlap)
**Unit**: STU (Structural Temporal Unit)
**Tier**: β (Integrative)
**Score**: 9/10 — Directly implementable with replicated behavioral correlation

---

## Scientific Basis

- **Halpern et al. (2004)**: r=0.84 behavioral correlation, N=10, p<0.001
- pSTG conjunction confirmed via fMRI
- Replicated across 7 methods

## Mechanism

Perception and imagery share a common pSTG substrate. The overlap strength
is the product of perception quality and imagery quality, weighted by the
replicated behavioral correlation coefficient.

### Formula

```
Overlap = 0.84 · Perception · Imagery

Where:
  Perception = timbre encoding quality (from spectral features)
  Imagery = temporal context retrieval (from long-range H³)
  0.84 = replicated behavioral correlation (Halpern 2004)
```

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| Perception | H³ timbre features (H2, H5 horizons) | Spectral encoding substrate |
| Imagery | H³ temporal context (H14, H20 horizons) | Long-range retrieval substrate |

## Outputs

| Name | Range | Description |
|------|-------|-------------|
| overlap | [0, 1] | Shared pSTG substrate strength |

## Why 9/10

- r=0.84 replicated behavioral correlation
- Multiplicative gate: both perception AND imagery must be active
- Direct pSTG conjunction in fMRI
- Immediately codable, no state needed
- Clear falsification: conjunction should activate pSTG
