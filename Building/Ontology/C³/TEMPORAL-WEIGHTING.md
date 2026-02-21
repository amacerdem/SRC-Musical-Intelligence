# Temporal Weighting

**Version**: v3.0.0 (Mechanism-based beliefs)

## Scale-Matched Exponential Weights

Scale-matched weights apply to ALL 36 Core Beliefs, not just consonance+tempo.
Appraisal/Anticipation beliefs operate at single-scale (their mechanism's native rate).
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

### T_char Table (v3.0 — Core Beliefs Only)

Scale-matched temporal weighting applies only to **Core Beliefs** (36 total).
Appraisal/Anticipation beliefs operate at their mechanism's native rate (no multi-scale).

| Function | Core Belief | T_char | Anchor H | Band |
|----------|-------------|--------|----------|------|
| F1 | harmonic_stability | 525ms | H10 (400ms) | Meso |
| F1 | pitch_prominence | 400ms | H10 (400ms) | Meso |
| F1 | pitch_identity | 600ms | H13 (600ms) | Meso |
| F1 | timbral_character | 2s | H18 (2s) | Macro |
| F1 | aesthetic_quality | 1s | H16 (1s) | Macro |
| F7 | period_entrainment | 600ms | H13 (600ms) | Meso |
| F7 | kinematic_efficiency | 500ms | H12 (525ms) | Meso |
| F7 | groove_quality | 1s | H16 (1s) | Macro |
| F7 | context_depth | 2s | H18 (2s) | Macro |
| F2 | prediction_hierarchy | 1s | H16 (1s) | Macro |
| F2 | sequence_match | 600ms | H13 (600ms) | Meso |
| F2 | information_content | 400ms | H10 (400ms) | Meso |
| F2 | prediction_accuracy | 500ms | H12 (525ms) | Meso |
| F3 | beat_entrainment | 400ms | H10 (400ms) | Meso |
| F3 | meter_hierarchy | 1s | H16 (1s) | Macro |
| F3 | attention_capture | 250ms | H7 (250ms) | Meso |
| F3 | salience_network_activation | 400ms | H10 (400ms) | Meso |
| F4 | autobiographical_retrieval | 8s | H21 (8s) | Macro |
| F4 | nostalgia_intensity | 5s | H20 (5s) | Macro |
| F4 | emotional_coloring | 2s | H18 (2s) | Macro |
| F4 | episodic_encoding | 4s | H19 (4s) | Macro |
| F5 | perceived_happy | 2s | H18 (2s) | Macro |
| F5 | perceived_sad | 2s | H18 (2s) | Macro |
| F5 | emotional_arousal | 1s | H16 (1s) | Macro |
| F5 | nostalgia_affect | 5s | H20 (5s) | Macro |
| F6 | wanting | — | — | Single-scale |
| F6 | liking | — | — | Single-scale |
| F6 | pleasure | — | — | Single-scale |
| F6 | prediction_error | — | — | Single-scale |
| F6 | tension | — | — | Single-scale |
| F8 | trained_timbre_recognition | 60s | H25 (60s) | Ultra |
| F8 | expertise_enhancement | 120s | H26 (120s) | Ultra |
| F8 | network_specialization | 200s | H27 (200s) | Ultra |
| F8 | statistical_model | 30s | H24 (36s) | Macro |
| F9 | neural_synchrony | 5s | H20 (5s) | Macro |
| F9 | social_coordination | 8s | H21 (8s) | Macro |

> F6 Core Beliefs operate at single-scale (PE aggregation, no temporal horizon).
> F8/F9 Core Beliefs activate in implementation waves 4–5.
> v1.0 kernel: only harmonic_stability, period_entrainment, beat_entrainment, autobiographical_retrieval have active multi-scale.

## Reward Weights

Reward'da per-horizon ağırlık = activation × (1/n veya custom):

```
# Consonance: activation-gated (ultra suppressed)
cons_weights = activated_reward_weights(elapsed_s, CONSONANCE_HORIZONS)

# Tempo: uniform (no ultra → no gating needed)
tempo_weights = {h: 1/n for h in TEMPO_HORIZONS}
```
