# MTNE — Cognitive Present

**Model**: Music Training Neural Efficiency
**Unit**: STU
**Function**: F8 Learning & Plasticity
**Tier**: γ
**Layer**: P — Cognitive Present
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 6 | exec_load | Current executive function load. Aggregation of short-context features: σ(0.30 × flux_mean + 0.30 × onset_mean + 0.20 × spec_std + 0.20 × flux_velocity). Reflects the momentary cognitive demand placed on prefrontal circuits. High load = more PFC engagement needed. In efficiently trained brains, load is handled with less activation. |
| 7 | conflict_monitor | Current conflict monitoring level (ACC). σ(0.50 × roughness_mean + 0.50 × entropy_energy). Tracks sensory dissonance (roughness) and energy unpredictability (entropy) as indices of conflict detection. ACC monitors and resolves these conflicts more efficiently in trained individuals. Sarasso 2019: consonance effect η²=0.685 on N2/P3 motor inhibition. |

---

## H³ Demands

No unique H³ tuples — P-layer reuses E-layer tuples:

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| — | 10 | 8 | M1 (mean) | L0 | Flux mean (from E-layer) |
| — | 10 | 8 | M8 (velocity) | L0 | Flux velocity (from E-layer) |
| — | 11 | 8 | M1 (mean) | L0 | Onset mean (from E-layer) |
| — | 21 | 8 | M3 (std) | L0 | Spectral change std (from E-layer) |
| — | 16 | 14 | M1 (mean) | L0 | Roughness mean (from E-layer) |
| — | 22 | 14 | M13 (entropy) | L0 | Energy entropy (from E-layer) |

---

## Computation

The P-layer represents the present-tense cognitive state:

1. **Executive load** (idx 6): Real-time PFC demand from information rate (flux), event boundaries (onsets), spectral variability, and flux acceleration. All at H8 (300ms) for rapid executive function assessment. Coefficient sum: 0.30 + 0.30 + 0.20 + 0.20 = 1.0.

2. **Conflict monitor** (idx 7): Real-time ACC conflict detection from roughness and energy entropy at H14 (700ms). Roughness = sensory dissonance creating processing conflict. Entropy = unpredictable energy dynamics requiring monitoring. Equal weighting (0.50 + 0.50 = 1.0) reflects joint contribution.

Both outputs are sigmoid-bounded to [0, 1].

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| H³ (reused) | Short-context tuples at H8 | Rapid executive function features |
| H³ (reused) | Phrase-context tuples at H14 | Sustained conflict monitoring features |
