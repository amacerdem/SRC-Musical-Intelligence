# MTNE — Temporal Integration

**Model**: Music Training Neural Efficiency
**Unit**: STU
**Function**: F8 Learning & Plasticity
**Tier**: γ
**Layer**: M — Temporal Integration
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 4 | efficiency_index | Weighted efficiency across timescales. Longer timescales → stronger efficiency weighting. (1×f01 + 2×f02 + 3×f03) / 6. This reflects the principle that sustained efficiency (f02, f03) contributes more to the overall efficiency profile than rapid inhibition (f01). Range [0, 1]. |
| 5 | dissociation_score | Behavior-neural dissociation strength. High behavioral gain + low neural activation = high dissociation. f01 × f03 (identical to f04_effic_ratio). The key neural efficiency signature: d=0.60 behavioral improvement with d=0.04 neural change. Moreno 2011 + Kosokabe 2025 replicate this dissociation. |

---

## H³ Demands

No unique H³ tuples — M-layer operates entirely on E-layer outputs.

---

## Computation

The M-layer integrates E-layer features into two temporally consolidated metrics:

1. **Efficiency index** (idx 4): Weighted average favoring sustained efficiency measures. The 1:2:3 weighting reflects that VLPFC efficiency (long-term, weight 3) and neural stability (medium-term, weight 2) are more diagnostic of training-induced efficiency than rapid inhibition alone (weight 1).

2. **Dissociation score** (idx 5): Product of behavioral gain × neural efficiency. This directly operationalizes the core finding: music training produces MORE behavioral improvement per unit of neural activation. The identical r=-0.57 across two studies suggests this dissociation is a stable property of trained neural circuits.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01_inhibit_gain | Behavioral improvement component |
| E-layer | f02_neural_effic | Neural stability component |
| E-layer | f03_vlpfc_effic | Prefrontal efficiency component |
