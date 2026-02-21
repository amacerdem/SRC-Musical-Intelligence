# Belief: consonance_trajectory

**Category**: Anticipation
**Owner**: BCH (SPU-α1)
**Function**: F1 Sensory Processing
**τ**: — (Anticipation beliefs have no inertia)

---

## 1. What This Belief Says

> "Harmonic stability will continue at this level / is trending toward more/less consonance."

When consonance_trajectory = 0.80, the auditory system extrapolates: "The current consonant state is likely to persist or increase."

When consonance_trajectory = 0.30, the extrapolation is: "The current state is trending toward dissonance or instability."

This is a **trend extrapolation**, not a pattern-based prediction. BCH does not "know" that a V chord resolves to I — it only knows that roughness is decreasing and consonance measures are increasing.

---

## 2. Observe Formula

```python
consonance_trajectory = F0_consonance_forecast
```

### Source

| Source | Layer | Mechanism |
|--------|-------|-----------|
| F0:consonance_forecast | F-layer | E+M+P integration + H³ trend slopes |

### F0 Internals (from mechanism/BCH-forecast.md)

```python
F0_consonance_forecast = (
    0.15 * E1_harmonicity
  + 0.15 * M0_consonance_memory
  + 0.20 * P0_consonance_signal
  + 0.10 * coupling
  + 0.10 * E3_ffr_behavior
  + 0.10 * R3[4]                         # sensory_pleasantness
  + 0.10 * H3[51, H12, M1, L0]          # key clarity memory 525ms
  + 0.10 * H3[60, H6, M1, L0]           # tonal stability memory 200ms
)
```

This combines:
- **Current state summary** (60%): E, M, P layer values
- **Extended memory** (20%): Key clarity at 525ms, tonal stability at 200ms
- **Signal features** (20%): Coupling, pleasantness

When available (offline), L1 forward-window H³ features also contribute.

---

## 3. No Predict/Update Cycle

As an Anticipation belief:
- No prediction of this prediction — it IS the prediction
- No PE generated from this belief
- Value set directly from F0:consonance_forecast each frame
- Stored in BeliefStore as a forward signal

---

## 4. Role in the Bayesian Cycle

consonance_trajectory feeds into `harmonic_stability`'s **predict()** formula:

```python
# In harmonic_stability.predict():
predicted = (
    τ * prev + (1-τ) * baseline
  + w_trend * H3_M18(matched_horizon)
  + w_period * H3_M14(matched_horizon)
  + w_ctx * consonance_trajectory            # ← THIS BELIEF
)
```

The anticipation belief provides **context-aware trend information** to the Core belief's prediction. This creates a feedback loop:

```
BCH mechanism → F0 → consonance_trajectory → harmonic_stability.predict()
                                                         ↓
                                                    predicted value
                                                         ↓
                                              PE = observed - predicted
                                                         ↓
                                                   reward formula
```

**Higher consonance_trajectory** → higher predicted harmonic_stability → smaller PE when consonance arrives → less surprise → less reward from expected consonance.

**Lower consonance_trajectory** → lower predicted harmonic_stability → if consonance actually arrives → positive PE → pleasant surprise → reward.

---

## 5. Extrapolation vs Prediction Boundary

| Property | consonance_trajectory (F1) | F2 Consonance Prediction (HTP) |
|----------|---------------------------|-------------------------------|
| **Type** | Trend extrapolation | Pattern-based prediction |
| **Method** | H³ M18 slopes + current state | Learned harmonic sequences |
| **Knowledge** | Zero — signal continuation | Musical grammar |
| **Example** | "Roughness ↓ → consonance ↑" | "V chord → expect I resolution" |
| **Horizon** | 200ms–525ms | 500ms–25s |
| **Phase** | 0a (relay output) | 1 (F2 prediction) |
| **Owner** | BCH | HTP |

BCH's consonance_trajectory and HTP's consonance prediction are **complementary**, not redundant:
- BCH provides the **brainstem-level sensory extrapolation** (fast, local)
- HTP provides the **cortical pattern-based prediction** (slower, structural)

Both feed harmonic_stability's predict() — the Bayesian gain determines which is trusted more based on precision.

---

## 6. Downstream Consumers

| Consumer | How It Uses This |
|----------|-----------------|
| `harmonic_stability` predict() | Context signal for prediction (w_ctx weight) |
| Precision engine | consonance_trajectory stability → π_pred estimation |
| HTP (F2) | Brainstem trend as input to hierarchical prediction model |

---

## 7. What This Belief Is NOT

- **Not** a prediction based on musical knowledge → that's F2/HTP's domain
- **Not** a reward prediction → that's F6 `reward_forecast` (SRP)
- **Not** the consonance value itself → that's `harmonic_stability` (Core)
- **Not** interval identification → that's `interval_quality` (Appraisal)

consonance_trajectory is specifically: **"Based on signal trends, where is consonance heading?"**
