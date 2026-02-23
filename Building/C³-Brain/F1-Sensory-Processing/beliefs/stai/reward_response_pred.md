# Belief: reward_response_pred

**Category**: Anticipation
**Owner**: STAI (SPU-β1)
**Function**: F1 Sensory Processing

---

## 1. What This Belief Says

> "Reward circuit activation will be proportional to current aesthetic quality."

When reward_response_pred = 0.85: "Based on the current spectral-temporal aesthetic integration level, the reward system (NAc, caudate, vmPFC) will activate strongly in the next ~500ms."

When reward_response_pred = 0.15: "The current aesthetic state predicts minimal reward circuit engagement."

This is a **forward prediction** (Anticipation). It generates expectations about downstream reward processing based on the current sensory aesthetic state. No Bayesian update cycle — it observes and projects forward.

---

## 2. Observe Formula

```python
observed = (
    0.50 * STAI_F_reward_prediction        # forecast layer: reward trajectory
  + 0.30 * STAI_P_aesthetic_response        # present aesthetic level → reward proxy
  + 0.20 * STAI_E_aesthetic_integration     # interaction strength → reward driver
)
```

### Source Breakdown

| Source | Weight | What It Captures |
|--------|--------|------------------|
| F:reward_prediction | 50% | Forecast layer: extrapolated reward circuit activation |
| P:aesthetic_response | 30% | Current aesthetic state as reward predictor |
| E:aesthetic_integration | 20% | Spectral × temporal interaction driving reward |

---

## 3. Downstream Consumers

| Consumer | How It Uses This |
|----------|------------------|
| SRP (F6) | Prediction of upcoming reward level |
| DAED (F6) | Caudate anticipation from aesthetic prediction |
| Salience (F3) | Predicted reward modulates salience allocation |
| `aesthetic_quality` (F1 Core) | Reward prediction feeds back to aesthetic context |

---

## 4. What This Belief Is NOT

- **Not** actual reward → that's `wanting`/`liking`/`pleasure` (SRP, F6)
- **Not** aesthetic quality itself → that's `aesthetic_quality` (STAI Core)
- **Not** dopamine level → that's `da_caudate`/`da_nacc` (DAED, F6)

---

## 5. Evidence Foundation

| Study | Key Finding | Relevance |
|-------|-------------|-----------|
| Kim et al. 2019 | Spectral × Temporal → NAc, caudate, vmPFC activation | Aesthetic integration predicts reward regions |
| Salimpoor et al. 2011 | Caudate DA 15-30s before peak; NAc AT peak | Anticipatory reward from aesthetic features |
| Cheung et al. 2019 | Amygdala + hippocampus joint uncertainty × surprise | Aesthetic prediction → reward circuit |
