# UDP E-Layer — Extraction (4D)

**Layer**: Extraction (E)
**Indices**: [0:4]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:uncertainty_level | [0, 1] | Contextual uncertainty from harmonic entropy. sigma(0.40*consonance_entropy_1s + 0.30*(1-tonalness_mean_1s) + 0.30*reward_entropy_1s). High entropy + low tonalness = atonal context. Mencke 2019: atonal contexts produce distinct PE-reward patterns. |
| 1 | E1:confirmation_reward | [0, 1] | Reward from correct predictions in uncertain contexts. sigma(0.40*uncertainty×(1-PE) + 0.30*periodicity_trend_1s + 0.30*consonance_mean). High when uncertain context + correct prediction (model improvement signal). Cheung 2019: high uncertainty, low surprise = pleasurable. |
| 2 | E2:error_reward | [0, 1] | Reward from prediction errors in certain contexts. sigma(0.40*(1-uncertainty)×PE + 0.30*PE_max + 0.30*flux_velocity). High when tonal context + surprising event (standard RPE). Gold 2019: IC × entropy interaction. |
| 3 | E3:pleasure_index | [0, 1] | Overall pleasure signal — context-dependent maximum. sigma(0.50*max(confirmation_reward, error_reward) + 0.50*coupling_skew). Selects the dominant reward pathway based on context. Salimpoor 2011: NAcc BOLD predicts 67% pleasure variance. |

---

## Design Rationale

1. **Uncertainty Level (E0)**: Measures how uncertain the current harmonic context is. Drives the reward inversion: high uncertainty → confirmation rewarding; low uncertainty → error rewarding.

2. **Confirmation Reward (E1)**: Reward from correct predictions in uncertain contexts. In atonal music, correctly predicting an event signals model improvement — intrinsically rewarding.

3. **Error Reward (E2)**: Standard RPE in certain contexts. In tonal music, surprising events trigger dopaminergic surprise-driven reward.

4. **Pleasure Index (E3)**: Context-dependent maximum of the two reward pathways. The brain selects whichever pathway provides stronger reward signal.

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 4 | 3 | M0 (value) | L2 | Current consonance |
| 1 | 4 | 16 | M1 (mean) | L0 | Mean consonance over bar |
| 2 | 4 | 16 | M20 (entropy) | L0 | Consonance entropy (uncertainty) |
| 3 | 14 | 8 | M1 (mean) | L0 | Tonalness at 500ms |
| 4 | 14 | 16 | M1 (mean) | L0 | Tonalness over bar |
| 5 | 5 | 8 | M1 (mean) | L0 | Periodicity at 500ms |
| 6 | 5 | 16 | M18 (trend) | L0 | Periodicity trend over bar |
| 7 | 21 | 1 | M0 (value) | L2 | Fast PE at 50ms |
| 8 | 21 | 3 | M0 (value) | L2 | PE at 100ms |
| 9 | 21 | 3 | M4 (max) | L2 | Max PE at 100ms |
| 10 | 10 | 3 | M0 (value) | L2 | Spectral flux at 100ms |
| 11 | 10 | 3 | M8 (velocity) | L2 | Flux velocity at 100ms |

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³ [4] | sensory_pleasantness | Consonance entropy for uncertainty |
| R³ [5] | periodicity | Periodicity trend for context |
| R³ [10] | spectral_flux | Flux velocity for error magnitude |
| R³ [14] | tonalness | Tonalness for context clarity |
| R³ [21] | spectral_change | Raw PE and PE max signals |
| H³ | 12 tuples (see above) | Multi-scale context and PE features |
