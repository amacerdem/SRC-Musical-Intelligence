# ECT — Extraction

**Model**: Expertise Compartmentalization Trade-off
**Unit**: NDU
**Function**: F8 Learning & Plasticity
**Tier**: γ
**Layer**: E — Extraction
**Dimensions**: 4D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f01_within_efficiency | Intra-network coupling strength. Measures within-network efficiency from long-timescale coupling and pattern binding means. f01 = σ(0.35 * within_coupling_mean_1s + 0.35 * pattern_binding_mean_1s). Paraskevopoulos et al. 2022: musicians show 106 within-network edges M > NM; IFG area 47m is highest-degree node in 5/6 network states. Papadaki et al. 2023: professionals show greater network strength and global efficiency correlating with task performance. |
| 1 | f02_between_reduction | Cross-network connectivity loss. Measures the reduction in between-network connectivity from cross-network mean and entropy at 1s. f02 = σ(0.35 * cross_network_mean_1s + 0.35 * cross_entropy_1s). Paraskevopoulos et al. 2022: 192 between-network edges NM > M; 47 multilinks (NM) vs 15 (M), p < 0.001 FDR. Moller et al. 2021: musicians show reduced cross-modal structural connectivity (IFOF FA correlates with visual reliance only in NM). |
| 2 | f03_trade_off_ratio | Cost-benefit balance of compartmentalization. Ratio of within-efficiency to between-reduction. f03 = clamp(f01 / (f02 + epsilon), 0, 10). Empirical baseline approximately 0.55 (106/192 edges). Values > 1.0 indicate gain exceeds cost; values < 1.0 indicate cost exceeds gain. |
| 3 | f04_flexibility_index | Reconfiguration capacity. Measures the system's ability to reconfigure its network architecture from spectral change dynamics and reconfiguration speed. f04 = σ(0.35 * reconfig_100ms + 0.35 * reconfig_speed_125ms). Wu-Chung et al. 2025: music creativity benefits depend on baseline network flexibility; higher flexibility leads to more cognitive benefit from training. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 25 | 16 | M1 (mean) | L2 (bidi) | Mean within-network coupling 1s |
| 1 | 33 | 16 | M1 (mean) | L2 (bidi) | Mean pattern binding 1s |
| 2 | 41 | 16 | M1 (mean) | L2 (bidi) | Mean cross-network connectivity 1s |
| 3 | 41 | 16 | M20 (entropy) | L2 (bidi) | Cross-network entropy 1s |
| 4 | 21 | 3 | M0 (value) | L2 (bidi) | Reconfiguration at 100ms |
| 5 | 21 | 4 | M8 (velocity) | L0 (fwd) | Reconfiguration speed 125ms |
| 6 | 25 | 3 | M0 (value) | L2 (bidi) | Within-network coupling 100ms |
| 7 | 25 | 3 | M2 (std) | L2 (bidi) | Coupling variability 100ms |
| 8 | 41 | 3 | M0 (value) | L2 (bidi) | Cross-network binding 100ms |
| 9 | 41 | 3 | M2 (std) | L2 (bidi) | Cross-network variability 100ms |

---

## Computation

The E-layer extracts four explicit features that characterize the expertise compartmentalization trade-off: the gains of within-network specialization, the costs of reduced cross-network integration, their ratio, and the system's capacity for reconfiguration. The key insight is that musical expertise involves a structural trade-off where increased within-network efficiency comes at the cost of reduced between-network connectivity (Paraskevopoulos et al. 2022).

All sigmoid features use coefficient sums equal to 1.0 (saturation rule). The trade-off ratio uses ratio computation with epsilon-guarded division.

1. **f01** (within efficiency): Estimates intra-network coupling strength from mean within-coupling and pattern binding over 1s. This captures the 106 within-network edges that musicians show relative to non-musicians (Paraskevopoulos 2022), reflecting the efficiency gained through specialization.

2. **f02** (between reduction): Estimates cross-network connectivity loss from mean cross-network features and cross-network entropy over 1s. This captures the 192 between-network edges that non-musicians show relative to musicians, and the entropy of cross-network connectivity reflects the diversity of lost connections.

3. **f03** (trade-off ratio): Direct ratio of gain (f01) to cost (f02), clamped to [0, 10]. This provides a single scalar summary of whether compartmentalization is net-beneficial. The empirical ratio of approximately 0.55 suggests the cost slightly exceeds the gain in terms of edge count.

4. **f04** (flexibility index): Estimates reconfiguration capacity from spectral change at 100ms and reconfiguration speed at 125ms. Wu-Chung et al. 2025 found that baseline network flexibility is a precondition for music training benefits, making flexibility a critical moderator of the trade-off.

H³ tuples span H3 (100ms) through H16 (1s), using primarily L2 (bidirectional) laws with L0 (forward) for velocity features. The within-network and cross-network features at 100ms provide instantaneous coupling snapshots; the 1s features provide stable baselines.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³[25:33] x_l0l5 | Intra-network coupling | Within-network efficiency measurement |
| R³[33:41] x_l4l5 | Pattern-feature binding | Within-network binding strength |
| R³[41:49] x_l5l6 | Cross-network connectivity | Between-network flexibility measurement |
| R³[21] spectral_change | Spectral dynamics | Reconfiguration capacity proxy |
| H³ (10 tuples) | Multi-scale temporal morphology | Coupling, binding, cross-network, and reconfiguration dynamics at 100ms-1s |
