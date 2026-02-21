# Precision Engine

**Version**: v3.0.0 (Mechanism-based beliefs)

## Precision-Weighted Prediction

Precision engine serves ALL 36 Core Beliefs across 9 Functions.
Appraisal/Anticipation beliefs do NOT have precision buffers (they are direct mechanism outputs).
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
- Per-belief key: `"function_belief"` (e.g. `"f1_harmonic_stability"`, `"f7_period_entrainment"`)
- Per-horizon key: `"function_belief:hN"` (v2.1 multi-scale)
- v3.0: keys for 36 Core Beliefs only (Appraisal/Anticipation have no PE buffer)
- Example keys: `"f1_harmonic_stability"`, `"f6_wanting"`, `"f4_autobiographical_retrieval"`

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

F2 Prediction (HTP): prediction quality → per-Core-Belief precision boost.
HTP is F2's primary relay but serves ALL Functions with precision evidence.

| Function | Core Belief | HTP Field A | HTP Field B | Scale |
|----------|-------------|-------------|-------------|-------|
| F1 | harmonic_stability | sensory_match | pitch_prediction | 0.15 |
| F1 | pitch_prominence | pitch_prediction | — | 0.10 |
| F7 | period_entrainment | pitch_prediction | midlevel_future_200ms | 0.12 |
| F7 | groove_quality | pitch_prediction | — | 0.08 |
| F3 | beat_entrainment | abstract_prediction | — | 0.10 |
| F3 | salience_network_activation | abstract_prediction | — | 0.08 |
| F4 | autobiographical_retrieval | abstract_prediction | abstract_future_500ms | 0.10 |
| F2 | prediction_hierarchy | sensory_match | abstract_prediction | 0.12 |
| F2 | information_content | abstract_prediction | — | 0.10 |
| F5 | perceived_happy | abstract_prediction | — | 0.08 |
| F5 | emotional_arousal | abstract_prediction | — | 0.06 |
| F8 | statistical_model | abstract_future_500ms | — | 0.05 |

```
boost = scale × mean(field_a, field_b)
π_pred += boost
```

> v1.0 kernel: only first 4 Core Beliefs active (harmonic_stability, period_entrainment, beat_entrainment, autobiographical_retrieval).
> v3.0 rows activate with their respective Function implementation waves.
> Appraisal/Anticipation beliefs never receive HTP boost (they have no PE/precision cycle).

## Multi-Scale Precision (v2.1)

Her horizon kendi PE history'sine sahip:
- Compound key: `"perceived_consonance:h5"`, `"perceived_consonance:h7"`, ...
- Aynı ring buffer altyapısı, farklı key
- Short horizons: daha hızlı dolup yüksek π_pred üretir
- Long horizons: yavaş dolar, düşük π_pred → exploration ağırlıklı
