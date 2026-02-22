# EDNR — Temporal Integration

**Model**: Expertise-Dependent Network Reorganization
**Unit**: NDU
**Function**: F8 Learning & Plasticity
**Tier**: α
**Layer**: M — Temporal Integration
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 4 | network_architecture | Connectivity strength measure. Combines within and between connectivity into a unified network topology descriptor. σ(0.50 * f01 + 0.50 * f02). Leipold et al. 2021: structural subnetwork including bilateral auditory, frontal, and parietal regions (pFWE<0.05, n=153). |
| 5 | compartmentalization_idx | Musician vs non-musician compartmentalization index. Temporal integration of the E-layer ratio (f03) reflecting the slow plasticity dynamics of expertise-driven network reorganization. Directly inherits f03. Paraskevopoulos 2022: 192 vs 106 edges (NM vs M). Cui et al. 2025: 1-year training does NOT change WM — slow structural change constraint. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 8 | 33 | 3 | M0 (value) | L2 (bidi) | Cross-network coupling 100ms |
| 9 | 33 | 3 | M2 (std) | L2 (bidi) | Cross coupling variability 100ms |
| 10 | 33 | 16 | M1 (mean) | L2 (bidi) | Mean cross coupling over 1s |
| 11 | 33 | 16 | M20 (entropy) | L2 (bidi) | Cross coupling entropy 1s |

---

## Computation

The M-layer integrates E-layer outputs into temporally stable network architecture descriptors:

1. **Network architecture** (idx 4): Balanced combination of within-connectivity (f01) and between-connectivity (f02) through equal weighting. Provides a single scalar summarizing the current network topology. Higher values indicate stronger overall connectivity regardless of direction.

2. **Compartmentalization index** (idx 5): Carries forward the E-layer compartmentalization ratio (f03 = f01 / (f02 + epsilon)). This ratio captures the key expertise effect — musicians have higher within/between ratios (>1.0) indicating functional specialization, while non-musicians have lower ratios reflecting distributed processing. Constrained by the slow structural plasticity finding from Cui et al. 2025 (1-year training does not change white matter).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01_within_connectivity | Input to network_architecture computation |
| E-layer | f02_between_connectivity | Input to network_architecture computation |
| E-layer | f03_compartmentalization | Direct pass-through to compartmentalization_idx |
| R³ [33:41] | x_l4l5 | Cross-network coupling for temporal integration |
| H³ | 4 tuples (see above) | Cross-network coupling dynamics at 100ms and 1s |
