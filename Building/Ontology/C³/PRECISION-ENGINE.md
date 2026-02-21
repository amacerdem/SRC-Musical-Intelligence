# Precision Engine

## Precision-Weighted Prediction

C³ iki tür precision kullanır:
- **π_obs** (observation): sensory confidence, observe() tarafından üretilir
- **π_pred** (prediction): PE history'den tahmin edilir

## π_pred Estimation

```
stability   = 1 / (mean(|PE|) + 0.1)     # low PE → high stability
consistency = 1 / (std(|PE|) + 0.1)       # steady PE → high consistency
tau_factor  = 0.5 + τ                      # slow beliefs more predictable
fill_factor = n_filled / window_size       # more history → more confident

π_raw = stability × consistency × tau_factor × fill_factor
π_pred = EMA(π_prev, π_raw, smooth_τ=0.6)
π_pred = clamp(π_pred, 0.01, 10.0)
```

## PE Ring Buffer

- Window size: 32 frames
- Stores: mean |PE| across batch and time per frame
- Per-belief key: `"belief_name"`
- Per-horizon key: `"belief_name:hN"` (v2.1 multi-scale)

## Tanh Compression (v2.3)

Reward formula'da precision normalization:
```
π_eff = tanh(π_raw / scale)     # scale = 12
```

| π_raw | Linear (÷10) | Tanh (÷12) |
|-------|-------------|------------|
| 1.0 | 0.10 | 0.08 |
| 5.0 | 0.50 | 0.40 |
| 10.0 | 1.00 | 0.68 |
| 20.0 | 2.00 | 0.93 |

Monotony = π_eff² — compression breaks saturation.

## HTP Hierarchical Boost (v4.0)

PCU engine: HTP prediction quality → per-belief precision boost.

| Belief | HTP Field A | HTP Field B | Scale |
|--------|-------------|-------------|-------|
| consonance | sensory_match | pitch_prediction | 0.15 |
| tempo | pitch_prediction | midlevel_future_200ms | 0.12 |
| salience | abstract_prediction | — | 0.10 |
| familiarity | abstract_prediction | abstract_future_500ms | 0.10 |

```
boost = scale × mean(field_a, field_b)
π_pred += boost
```

## Multi-Scale Precision (v2.1)

Her horizon kendi PE history'sine sahip:
- Compound key: `"perceived_consonance:h5"`, `"perceived_consonance:h7"`, ...
- Aynı ring buffer altyapısı, farklı key
- Short horizons: daha hızlı dolup yüksek π_pred üretir
- Long horizons: yavaş dolar, düşük π_pred → exploration ağırlıklı
