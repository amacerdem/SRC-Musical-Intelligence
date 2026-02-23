# PSH E-Layer — Extraction (4D)

**Layer**: Extraction (E)
**Indices**: [0:4]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:high_level_silencing | [0, 1] | High-level representation silencing. sigma(0.40*(1-high_coupling_500ms) + 0.30*consonance_mean_1s + 0.30*periodicity_mean_1s). When high-level coupling drops post-stimulus (explained away), silencing is active. de Vries 2023: LOTC/aIPL silenced by accurate predictions. |
| 1 | E1:low_level_persistence | [0, 1] | Low-level sensory persistence. sigma(0.35*low_coupling_100ms + 0.35*low_coupling_25ms + 0.30*amp_100ms). Low-level (A1/V1) representations persist regardless of prediction accuracy. de Vries 2023: V1/A1 ~110ms pixelwise persistence. |
| 2 | E2:silencing_efficiency | [0, 1] | Prediction-dependent silencing quality. sigma(0.40*high_silencing*(1-PE) + 0.30*periodicity_mean_1s + 0.30*consonance_mean). Maximal when predictions are accurate (PE low) and high-level representations are silenced. |
| 3 | E3:hierarchy_dissociation | [0, 1] | Level-dependent silencing difference. sigma(0.50*|high_silencing-low_persistence| + 0.50*high_entropy_1s). Maximal when high-level is silenced but low-level persists — the core PSH prediction. de Vries 2023: ηp²=0.49 for prediction × hierarchy interaction. |

---

## Design Rationale

1. **High-Level Silencing (E0)**: Detects when high-level (LOTC/aIPL equivalent) representations are suppressed post-stimulus. Inverted coupling at 500ms — accurate predictions reduce coupling because the representation has been "explained away."

2. **Low-Level Persistence (E1)**: Tracks low-level (A1 equivalent) sensory representation persistence. These persist regardless of prediction accuracy, supporting ongoing error monitoring.

3. **Silencing Efficiency (E2)**: Combines silencing with prediction accuracy. Maximal silencing occurs when predictions match outcomes (low PE). This is the prediction-silencing mechanism.

4. **Hierarchy Dissociation (E3)**: The core PSH finding — high and low levels show opposite post-stimulus patterns. Maximal when the hierarchy dissociation is strongest.

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 7 | 0 | M0 (value) | L2 | Amplitude at 25ms |
| 1 | 7 | 1 | M0 (value) | L2 | Amplitude at 50ms |
| 2 | 7 | 3 | M0 (value) | L2 | Amplitude at 100ms |
| 3 | 7 | 3 | M2 (std) | L2 | Amplitude variability 100ms |
| 4 | 10 | 0 | M0 (value) | L2 | Spectral flux at 25ms |
| 5 | 10 | 3 | M0 (value) | L2 | Spectral flux at 100ms |
| 6 | 21 | 1 | M0 (value) | L2 | Spectral change at 50ms |
| 7 | 21 | 3 | M0 (value) | L2 | PE at 100ms |
| 8 | 21 | 3 | M2 (std) | L2 | PE variability at 100ms |
| 9 | 25 | 0 | M0 (value) | L2 | Low-level coupling at 25ms |
| 10 | 25 | 3 | M0 (value) | L2 | Low-level coupling at 100ms |
| 11 | 25 | 3 | M16 (curvature) | L2 | Coupling curvature at 100ms |

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³ [7] | amplitude | Low-level sensory persistence |
| R³ [10] | spectral_flux | Low-level sensory persistence |
| R³ [21] | spectral_change | PE signal for silencing decision |
| R³ [25] | x_l0l5 | Low-level coupling persistence |
| H³ | 12 tuples (see above) | Fast timescale features at H0/H1/H3 |
