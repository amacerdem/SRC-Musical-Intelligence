# context_depth — Core Belief (HMCE)

**Category**: Core (full Bayesian PE)
**τ**: 0.70
**Owner**: HMCE (STU-α1)
**Multi-Scale**: 6 horizons, T_char = 2s

---

## Definition

"Integrating N layers of temporal hierarchy." Tracks how deeply the brain integrates temporal context across the cortical gradient from primary auditory cortex (pmHG) through STG, MTG, to temporal pole. High values indicate deep hierarchical encoding — the listener is tracking long-range musical structure across multiple timescales simultaneously.

---

## Multi-Scale Horizons

```
H10(400ms)  H13(600ms)  H16(1s)  H18(2s)
H21(8s)     H24(36s)
```

T_char = 2s reflects the characteristic timescale at which hierarchical context integration stabilizes. H10-H13 capture short/medium context encoding transitions; H16-H18 are the primary integration scales where phrase and section boundaries emerge; H21-H24 capture section-level and form-level depth persistence.

---

## Observation Formula

```
# HMCE Layer M context_depth computation:
f01 = sigma(0.90 * flux_mean * onset_val)         # short context (pmHG)
f02 = sigma(0.85 * energy_mean * loudness_mean)    # medium context (STG)
f03 = sigma(0.80 * x_coupling * autocorr)          # long context (MTG)

context_depth = (1 * f01 + 2 * f02 + 3 * f03) / 6

# Where:
# flux_mean    = H3[(10, 8, 1, 0)]    spectral_flux mean at H8
# onset_val    = H3[(11, 8, 0, 0)]    onset_strength value at H8
# energy_mean  = H3[(22, 14, 1, 0)]   energy_change mean at H14
# loudness_mean= H3[(8, 14, 1, 0)]    loudness mean at H14
# x_coupling   = H3[(25, 20, 1, 0)]   x_l0l5 mean at H20
# autocorr     = H3[(33, 20, 22, 0)]  x_l4l5 autocorrelation at H20

# Precision: gradient_coherence across 3 levels
# pi_obs = 1 / (std(f01, f02, f03) + 0.1)
# Coherent gradient (f01 > f02 > f03 or smooth ramp) → high precision
```

Relay components: HMCE.context_depth[M0] (index [5]).

---

## Prediction Formula

```
predict = Linear(τ × prev + w_trend × M18 + w_period × M14 + w_ctx × beliefs_{t-1})
```

Standard Bayesian PE cycle with gain = π_obs / (π_obs + π_pred).

Context depth has high inertia (τ = 0.70) reflecting the slow, stable nature of hierarchical encoding — the number of active context layers changes gradually as musical complexity evolves.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| HMCE M0 | context_depth [5] | Weighted integration depth |
| HMCE E0 | f01_short_context [0] | pmHG encoding (10-50 notes) |
| HMCE E1 | f02_medium_context [1] | STG encoding (50-100 notes) |
| HMCE E2 | f03_long_context [2] | MTG encoding (100-200 notes) |
| HMCE E3 | f04_gradient [3] | Anatomical gradient strength (r=0.99) |
| H³ | (10, 8, 1, 0) | Spectral flux mean at short context |
| H³ | (22, 14, 1, 0) | Energy change mean at medium context |
| H³ | (25, 20, 1, 0) | Cross-feature coupling at long context |
| H³ | (33, 20, 22, 0) | Autocorrelation at long context |

---

## Scientific Foundation

- **Mischler 2025**: Distance from pmHG correlates with context encoding depth (r=0.99 site-level, r=0.32 electrode-level, p=1.5e-05; LME p=0.004; ECoG+EEG, N=26)
- **Norman-Haignere 2022**: Integration windows increase with PAC distance: 74ms to 274ms (beta=0.064 oct/mm, F=20.56, p<0.001; iEEG, 18 patients)
- **Bonetti 2024**: Hierarchical feedforward AC to hippocampus to cingulate; expertise modulates contextual tones (BOR=2.91e-07; MEG, N=83)
- **Golesorkhi 2021**: Core-periphery temporal hierarchy in cortex; DMN/FPN longer ACW (d=-0.66 to -2.03; MEG, N=89)
- **Sabat 2025**: Integration windows invariant to stimulus context in ferret AC (15-150ms) — constrains: basic gradient may be hardwired

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/hmce_relay.py`
