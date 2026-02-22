# EDNR — Cognitive Present

**Model**: Expertise-Dependent Network Reorganization
**Unit**: NDU
**Function**: F8 Learning & Plasticity
**Tier**: α
**Layer**: P — Cognitive Present
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 6 | current_compartm | Real-time network state. Current compartmentalization level reflecting moment-by-moment expertise-dependent processing. σ(0.50 * f03.clamp(0,3)/3.0 + 0.50 * within_mean_1s). Paraskevopoulos 2022: PTE-based multilink analysis reveals real-time network interaction patterns in musicians. |
| 7 | network_isolation | Boundary maintenance. Degree to which functional network boundaries are maintained during auditory processing. Moller et al. 2021: musicians show only local CT correlations while NM show distributed V1-HG correlations; FA cluster p<0.001 (left IFOF) — BCG associated with FA in NM only (musicians p=0.64). |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 12 | 16 | 3 | M0 (value) | L2 (bidi) | Flatness at 100ms |
| 13 | 16 | 16 | M2 (std) | L2 (bidi) | Flatness variability 1s |

---

## Computation

The P-layer computes the real-time cognitive state of network organization:

1. **Current compartmentalization** (idx 6): Normalizes the compartmentalization ratio (f03) to [0,1] range via clamping to [0,3] and dividing by 3.0, then combines with within-network coupling mean at 1s. This produces a real-time readout of how compartmentalized the auditory processing network currently is. Values near 1.0 indicate highly specialized, expert-like processing; values near 0.5 indicate non-specialized, novice-like processing.

2. **Network isolation** (idx 7): Captures the degree of boundary maintenance between functional networks. Based on Moller et al. 2021's finding that musicians lack the distributed V1-HG cortical thickness correlations seen in non-musicians. The left IFOF white matter tract mediates audiovisual specialization — higher isolation reflects more specialized auditory processing independent of visual cortex.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f03_compartmentalization | Normalized for real-time compartmentalization readout |
| M-layer | network_architecture | Network state context for isolation computation |
| R³ [16] | spectral_flatness | Stimulus regularity proxy for processing complexity |
| H³ | 2 tuples (see above) | Flatness dynamics for distribution complexity assessment |
