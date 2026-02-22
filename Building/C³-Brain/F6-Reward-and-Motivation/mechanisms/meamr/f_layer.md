# MEAMR — Forecast

**Model**: Music-Evoked Autobiographical Memory Reward
**Unit**: RPU
**Function**: F6 Reward & Motivation
**Tier**: β
**Layer**: F — Forecast
**Dimensions**: 1D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | nostalgia_response_pred | Predicted nostalgia response. σ(0.5 * f04 + 0.5 * f02). Projects likelihood of a sustained nostalgia experience based on current positive affect and autobiographical salience. High positive affect combined with strong autobiographical salience predicts an emerging nostalgia response — the bittersweet pleasure of music-evoked personal memories. τ_decay = 10.0s reflects the slow, sustained nature of nostalgic responses. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 41 | 16 | M18 (trend) | L2 (bidi) | Memory-structure trend 1s — via f02 autobio trajectory |
| 1 | 41 | 16 | M1 (mean) | L2 (bidi) | Mean memory-structure 1s — via f02 sustained salience |
| 2 | 4 | 16 | M18 (trend) | L2 (bidi) | Pleasantness trend 1s — via f01 -> f04 hedonic trajectory |
| 3 | 12 | 16 | M1 (mean) | L2 (bidi) | Mean warmth 1s — via f01 -> f04 timbral trajectory |

---

## Computation

The F-layer forecasts the probability and intensity of an emerging nostalgia response. Nostalgia is the sustained emotional reward following music-evoked autobiographical memory retrieval.

The prediction combines:

1. **f04 (positive affect)**: Integrates familiarity and autobiographical salience into a reward signal. Positive affect from familiar music engages vACC + SN/VTA.

2. **f02 (autobiographical salience)**: Direct memory salience signal from dMPFC tracking. Ensures the prediction is anchored in the memory pathway, not just hedonic response.

The f04 + f02 combination ensures nostalgia prediction requires both emotional reward (the positive affect of remembering) and autobiographical specificity (the personal significance of the memory). The τ_decay = 10.0s reflects the slow unfolding and persistence of nostalgic responses.

This signal feeds:
- DAED for affect-driven dopamine consummation
- IMU for memory retrieval cue
- The kernel for familiarity-modulated reward

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer [1] | f02_autobio_salience | Autobiographical salience trajectory |
| E-layer [3] | f04_positive_affect | Reward signal from familiar music |
| R³ [41:49] | x_l5l6 | Memory-structure trajectory (via f02, f04) |
| R³ [4] | sensory_pleasantness | Hedonic trajectory (via f01 -> f04) |
| R³ [12] | warmth | Timbral familiarity trajectory (via f01 -> f04) |
| Janata 2009 | Sustained dMPFC during autobio music | P < 0.001, FDR P < 0.025 (fMRI, N = 13) |
| Salimpoor 2011 | Anticipatory caudate DA for familiar music | r = 0.71 (PET, N = 8) |
