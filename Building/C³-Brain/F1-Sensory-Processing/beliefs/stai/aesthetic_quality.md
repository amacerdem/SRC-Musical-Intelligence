# Belief: aesthetic_quality

**Category**: Core
**Owner**: STAI (SPU-β1)
**Function**: F1 Sensory Processing
**Inertia (τ)**: 0.4 (moderate — aesthetic judgments integrate over ~400ms)
**Baseline**: 0.5

---

## 1. What This Belief Says

> "This sound is aesthetically pleasant."

When aesthetic_quality = 0.85, the listener's auditory system infers: "The current sound has both spectral integrity (consonance, harmonic clarity) and temporal integrity (forward-flowing, predictable structure), producing a strong aesthetic response."

When aesthetic_quality = 0.15, the inference is: "The current sound lacks aesthetic appeal — either spectrally disrupted (dissonant, noisy) or temporally disrupted (reversed, unpredictable), or both."

This is **not** a simple consonance judgment ("this is harmonically stable") — that's `harmonic_stability` (BCH). It is a **higher-order integrative judgment** that combines spectral and temporal dimensions into an aesthetic evaluation, reflecting vmPFC-IFG integration.

---

## 2. Observe Formula

```python
observed = (
    0.40 * STAI_E_aesthetic_integration    # spectral x temporal interaction
  + 0.30 * STAI_P_aesthetic_response       # integrated present-state aesthetic signal
  + 0.20 * STAI_M_aesthetic_value          # weighted spectral+temporal+interaction model
  + 0.10 * STAI_E_vmpfc_connectivity       # vmPFC-IFG coupling strength
)
```

### Source Breakdown

| Source | Weight | Mechanism Layer | What It Captures |
|--------|--------|----------------|------------------|
| E:aesthetic_integration | 40% | E-layer | Spectral x temporal interaction — core aesthetic signal |
| P:aesthetic_response | 30% | P-layer | Real-time integrated aesthetic evaluation |
| M:aesthetic_value | 20% | M-layer | Mathematical model: α×Spectral + β×Temporal + γ×Interaction |
| E:vmpfc_connectivity | 10% | E-layer | vmPFC-IFG coupling — integration network engagement marker |

---

## 3. Predict Formula

```python
predicted = (
    τ * prev                           # 40% previous value (moderate inertia)
  + (1 - τ) * baseline                 # 60% regression to 0.5
  + w_trend * H3_M18_binding           # aesthetic trend
  + w_period * H3_M14_binding          # binding periodicity
  + w_ctx * beliefs_context            # context from harmonic_stability, spectral_temporal_synergy
)
```

### τ = 0.4 Rationale

Moderate inertia: aesthetic judgments integrate over longer windows than pure sensory assessments (~400ms vs ~300ms for harmonic_stability). The spectral × temporal interaction requires accumulation of both dimensions. Kim et al. (2019) factorial design reflects integration that is slower than brainstem processing.

---

## 4. Update (Bayesian)

```python
PE = observed - predicted
gain = π_obs / (π_obs + π_pred + ε)
posterior = (1 - gain) * predicted + gain * observed
```

- **Positive PE**: Sound is MORE aesthetically pleasant than expected → aesthetic surprise (reward)
- **Negative PE**: Sound is LESS aesthetically pleasant than expected → aesthetic disappointment

PE feeds the **reward formula** (F6): `surprise = abs(PE)`, weighted by salience.

---

## 5. What This Belief Is NOT

- **Not** harmonic consonance → that's `harmonic_stability` (BCH)
- **Not** reward feeling → that's `wanting`/`liking` (SRP, F6)
- **Not** spectral-temporal coherence observation → that's `spectral_temporal_synergy` (STAI Appraisal)

---

## 6. Evidence Foundation

| Study | Key Finding | Relevance |
|-------|-------------|-----------|
| Kim et al. 2019 | Spectral × Temporal interaction in vmPFC, NAc, caudate (d=0.709-0.735) | Core mechanism: interaction drives aesthetic response |
| Alluri et al. 2012 | Parallel streams (timbral→STG, rhythmic→motor, tonal→prefrontal) integrate downstream | Multi-stream integration architecture |
| Cheung et al. 2019 | Uncertainty × surprise → pleasure in amygdala, hippocampus, auditory cortex | Prediction-aesthetic link |
| Sarasso et al. 2019 | Consonance → aesthetic judgment (ηp²=0.685) | Spectral integrity as aesthetic dimension |
