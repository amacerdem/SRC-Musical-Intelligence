# Temporal Weighting

## Scale-Matched Exponential Weights

Farklı horizon'lardan gelen evidence'ı target horizon'a göre ağırlıklandırma:

```
w(h, Δ) = exp(−α |h − Δ|)
weights = normalize(w)     # sum to 1.0
```

- `h` = evidence horizon index
- `Δ` = target horizon index
- `α` = decay rate (default 0.3)

### Decay Rate Etkileri (α = 0.3)

| Distance |h − Δ| | Raw weight | Normalized (~) |
|-----------------------|------------|-------------|
| 0 (exact match) | 1.00 | ~49% |
| ±3 indices | 0.41 | ~20% |
| ±8 indices | 0.09 | ~5% |

Denser horizon sets (16 veya 32) için α = 0.6–1.2 kullanılmalı.

## Horizon Activation — Data-Readiness Gating (v2.2)

Ultra horizon'lar yeterli veri olmadan spurious PE üretir.
Activation gating bunu önler:

```
activation(t, T_h) = σ(k × (t / T_h − 1))     # k = 5
```

| Elapsed / T_h | Activation |
|---------------|------------|
| 0.5× | 0.08 (barely) |
| 1.0× | 0.50 (half) |
| 2.0× | 0.99 (fully) |

### 30s Excerpt'lerde:

| Horizon | T_h | Activation at 30s |
|---------|-----|-------------------|
| H5–H21 | ≤8s | ~1.0 (fully active) |
| H24 | 36s | 0.30 (partially) |
| H28 | 414s | 0.01 (essentially silent) |

## Aggregation Weights (Belief-Level)

Belief'in characteristic timescale'ine (T_char) en yakın horizon anchor olur:

```
closest_h = argmin_h |HORIZON_SECONDS[h] − T_char|
weights = scale_matched_weights(closest_h, horizons, α)
aggregated = Σ weights[h] × prediction[h]
```

### Consonance: T_char = 525ms → anchor ≈ H10 (400ms)
### Tempo: T_char = 600ms → anchor ≈ H13 (600ms)

## Reward Weights

Reward'da per-horizon ağırlık = activation × (1/n veya custom):

```
# Consonance: activation-gated (ultra suppressed)
cons_weights = activated_reward_weights(elapsed_s, CONSONANCE_HORIZONS)

# Tempo: uniform (no ultra → no gating needed)
tempo_weights = {h: 1/n for h in TEMPO_HORIZONS}
```
