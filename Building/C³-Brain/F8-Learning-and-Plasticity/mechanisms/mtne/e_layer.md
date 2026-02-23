# MTNE — Extraction

**Model**: Music Training Neural Efficiency
**Unit**: STU
**Function**: F8 Learning & Plasticity
**Tier**: γ
**Layer**: E — Extraction
**Dimensions**: 4D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f01_inhibit_gain | Behavioral inhibition improvement (d=0.60). Music-trained executive function gain from spectral flux, onset strength, and spectral variability at short context (H8). σ(0.30 × flux_mean × onset_mean + 0.25 × spec_std). Moreno 2011: d=0.60 (fNIRS, N≈20). Kosokabe 2025: d=0.605 EXACT REPLICATION (fNIRS RCT, N=57). |
| 1 | f02_neural_effic | Neural efficiency: stable PFC activation despite improved behavioral output (d=0.04). Tracks energy dynamics and roughness at phrase level (H14). σ(0.25 × energy_mean × roughness_mean + 0.20 × loudness_trend). Moreno 2011: d=0.04 stable PFC. Kosokabe 2025: stable PFC / control group ↑ L-DLPFC p=.043. |
| 2 | f03_vlpfc_effic | VLPFC efficiency proxy (r=-0.57). Lower activation = higher performance. Inverted sigmoid of energy entropy and acceleration at phrase level. 1.0 − σ(0.30 × entropy_energy × loudness_mean + 0.25 × energy_accel). Moreno 2011 AND Kosokabe 2025: IDENTICAL r=-0.57 across two independent samples. |
| 3 | f04_effic_ratio | Efficiency ratio: behavioral × VLPFC efficiency. f01 × f03. High when both behavioral gain and neural efficiency are present. Multiplicative gating ensures both components are required. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 10 | 8 | M1 (mean) | L0 | Mean spectral flux at 300ms |
| 1 | 10 | 8 | M8 (velocity) | L0 | Flux change rate at 300ms |
| 2 | 11 | 8 | M1 (mean) | L0 | Mean onset strength at 300ms |
| 3 | 21 | 8 | M3 (std) | L0 | Spectral change variability |
| 4 | 7 | 14 | M1 (mean) | L0 | Mean amplitude at phrase |
| 5 | 8 | 14 | M1 (mean) | L0 | Mean loudness at phrase |
| 6 | 8 | 14 | M18 (trend) | L0 | Loudness trajectory |
| 7 | 16 | 14 | M1 (mean) | L0 | Mean roughness at phrase |
| 8 | 22 | 14 | M13 (entropy) | L0 | Energy change unpredictability |
| 9 | 22 | 14 | M11 (acceleration) | L0 | Energy change acceleration |

---

## Computation

The E-layer extracts four explicit features characterizing neural efficiency:

1. **Inhibition gain** (f01): Rapid executive function indexed by spectral flux × onset strength at H8. High information rate + strong onsets = high inhibition demand. The d=0.60 improvement (replicated: Kosokabe d=0.605) represents enhanced performance.

2. **Neural efficiency** (f02): Stable PFC activation (d=0.04) despite improved performance. Tracks energy dynamics × roughness at H14. In efficient processing, complex stimuli are handled without increased neural cost.

3. **VLPFC efficiency** (f03): Inverted — high complexity → high activation → LOW efficiency. The r=-0.57 DCCS-VLPFC correlation is identical across Moreno 2011 and Kosokabe 2025, suggesting a stable neural efficiency constant.

4. **Efficiency ratio** (f04): Multiplicative combination f01 × f03. Both behavioral improvement AND low neural cost must be present for high efficiency.

All sigmoid formulas satisfy coefficient saturation rule (|wᵢ| ≤ 1.0).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| H³ | 10 tuples (see above) | Short (H8) + phrase (H14) features |
| R³ [10] | spectral_flux | Information rate for inhibition demand |
| R³ [11] | onset_strength | Event boundaries for executive switching |
| R³ [21] | spectral_change | Spectral variability for exec. load |
| R³ [7,8] | amplitude, loudness | Intensity dynamics for sustained effort |
| R³ [16] | roughness | Sensory dissonance for conflict monitoring |
| R³ [22] | energy_change | Energy dynamics for PFC demand |
