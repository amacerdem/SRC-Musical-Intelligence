# MCCN — Forecast

**Model**: Musical Chills Cortical Network
**Unit**: RPU
**Function**: F6 Reward & Motivation
**Tier**: β
**Layer**: F — Forecast
**Dimensions**: 1D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | chills_onset_pred | Predicted chills onset probability. Forecasts likelihood of a chill event in the upcoming 1-3s based on acoustic buildup patterns and current network activation. Salimpoor 2011: anticipatory dopamine release in caudate precedes chills, implying the brain actively predicts peak pleasure moments. High values indicate acoustic conditions (crescendo, tension buildup, harmonic trajectory) are converging toward a chills trigger. τ_decay = 3.0s (Chabin 2020). |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 7 | 8 | M8 (velocity) | L2 (bidi) | Amplitude buildup rate — crescendo detection |
| 1 | 7 | 16 | M2 (std) | L2 (bidi) | Amplitude variability 1s — dynamic range |
| 2 | 9 | 8 | M8 (velocity) | L2 (bidi) | Energy buildup trajectory |
| 3 | 22 | 8 | M8 (velocity) | L2 (bidi) | Energy change acceleration 500ms |
| 4 | 8 | 16 | M1 (mean) | L2 (bidi) | Background loudness for crescendo context |
| 5 | 21 | 8 | M0 (value) | L2 (bidi) | Spectral deviation for surprise buildup |

---

## Computation

The F-layer predicts the probability of an imminent chills event based on current acoustic dynamics and network pre-activation.

Salimpoor 2011 demonstrated anticipatory dopamine release in the caudate nucleus preceding chills by several seconds, establishing that the brain actively predicts and prepares for peak pleasure moments. The prediction integrates:

1. **Energy buildup**: Amplitude velocity and RMS energy velocity capture crescendo patterns that typically precede chills. Amplitude variability provides dynamic range context.

2. **Surprise trajectory**: Spectral deviation at 500ms and energy change acceleration capture the musical surprise buildup that triggers chills at resolution.

3. **Context**: Mean loudness over 1s provides the baseline against which crescendos are evaluated.

The τ_decay = 3.0s (Chabin 2020 chills sustain window) sets the relevant prediction horizon at 1-3 seconds ahead. This feeds DAED for anticipatory dopamine modulation and the kernel scheduler for salience computation.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R³ [7] | amplitude | Crescendo detection / buildup trajectory |
| R³ [8] | loudness | Background loudness context |
| R³ [9] | rms_energy | Energy buildup for chill prediction |
| R³ [21] | spectral_change | Spectral surprise buildup |
| R³ [22] | energy_change | Dynamic shift trajectory |
| E-layer [0-3] | f01-f04 | Current network state informs prediction baseline |
| Salimpoor 2011 | Anticipatory caudate DA before chills | r = 0.71 (PET, N = 8) |
| Chabin 2020 | Chills sustain ~3s, theta buildup | HD-EEG, N = 18 |
