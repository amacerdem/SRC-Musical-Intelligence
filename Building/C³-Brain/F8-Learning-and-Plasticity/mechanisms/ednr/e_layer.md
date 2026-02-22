# EDNR — Extraction

**Model**: Expertise-Dependent Network Reorganization
**Unit**: NDU
**Function**: F8 Learning & Plasticity
**Tier**: α
**Layer**: E — Extraction
**Dimensions**: 4D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f01_within_connectivity | Intra-network coupling strength. Measures within-network connectivity that increases with musical expertise. σ(0.35 * within_mean_1s + 0.30 * within_periodicity_1s). Paraskevopoulos 2022: musicians show 106 within-network edges vs 192 between-network edges in non-musicians. Leipold et al. 2021: robust musicianship effects on intrahemispheric FC (pFWE<0.05, n=153). |
| 1 | f02_between_connectivity | Inter-network coupling (inverse). Measures between-network connectivity that decreases with expertise. σ(0.35 * cross_mean_1s + 0.30 * cross_entropy_1s). Paraskevopoulos 2022: NM > M between-network multilinks (192 vs 106 edges, p<0.001 FDR). |
| 2 | f03_compartmentalization | Within/between ratio. Compartmentalization index computed as f01 / (f02 + epsilon). Higher values indicate greater functional specialization. Møller et al. 2021: NM show distributed CT correlations while musicians show only local correlations (FDR<10%). |
| 3 | f04_expertise_signature | Expertise-specific pattern. Captures the processing refinement signature that emerges from long-term training. σ(0.35 * tonalness_mean_1s + 0.35 * pleasantness_mean_1s). Papadaki et al. 2023: network strength correlates with interval recognition (rho=0.36, p=0.02). Porfyri et al. 2025: Group x Time interaction F(1,28)=4.635, eta²=0.168. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 25 | 3 | M0 (value) | L2 (bidi) | Within-network coupling 100ms |
| 1 | 25 | 3 | M2 (std) | L2 (bidi) | Coupling variability 100ms |
| 2 | 25 | 16 | M1 (mean) | L2 (bidi) | Mean coupling over 1s |
| 3 | 25 | 16 | M14 (periodicity) | L2 (bidi) | Coupling periodicity 1s |
| 4 | 4 | 3 | M0 (value) | L2 (bidi) | Pleasantness at 100ms |
| 5 | 4 | 16 | M1 (mean) | L2 (bidi) | Mean pleasantness 1s |
| 6 | 14 | 3 | M0 (value) | L2 (bidi) | Tonalness at 100ms |
| 7 | 14 | 16 | M1 (mean) | L2 (bidi) | Mean tonalness over 1s |

---

## Computation

The E-layer extracts four explicit features that characterize expertise-dependent network reorganization:

1. **Within connectivity** (f01): Driven by within-network coupling mean and periodicity at 1s horizon from R³ x_l0l5[25]. Tracks intra-network binding strength that increases with musical training. Maps to bilateral STG and Planum Temporale (Leipold et al. 2021: PT-PT connectivity pFWE<0.05).

2. **Between connectivity** (f02): Driven by cross-network coupling mean and entropy at 1s from R³ x_l4l5[33]. Captures inter-network coupling that decreases with expertise as networks compartmentalize. Maps to IFG (Paraskevopoulos 2022: area 47m as hub, Hedges' g=-1.09).

3. **Compartmentalization** (f03): Ratio of f01 to f02. The core metric of EDNR — musicians show higher within/between connectivity ratios reflecting functional specialization. Maps to Heschl's Gyrus (Moller et al. 2021: CT correlations FDR<10%).

4. **Expertise signature** (f04): Driven by tonalness and pleasantness means at 1s horizon. Captures the processing refinement pattern unique to trained musicians. Maps to SMG and vmPFC (Papadaki et al. 2023: Cohen's d=0.70).

All formulas use sigmoid activation with coefficient sums <= 1.0 (saturation rule).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³ [25:33] | x_l0l5 | Within-network coupling proxy for intra-network binding |
| R³ [33:41] | x_l4l5 | Cross-network coupling proxy for inter-network binding |
| R³ [14] | tonalness | Processing complexity indicator for expertise signature |
| R³ [4] | sensory_pleasantness | Processing quality proxy for expertise refinement |
| H³ | 8 tuples (see above) | Multi-scale coupling dynamics and expertise signal features |
