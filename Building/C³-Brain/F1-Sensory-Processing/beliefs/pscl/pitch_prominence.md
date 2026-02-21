# Belief: pitch_prominence

**Category**: Core
**Owner**: PSCL (SPU-α2)
**Function**: F1 Sensory Processing
**Inertia (τ)**: 0.35 (moderate-low — responds to pitch changes within ~300ms)
**Baseline**: 0.5

---

## 1. What This Belief Says

> "I perceive a prominent pitch."

When pitch_prominence = 0.85, the listener's cortical system infers: "There is a clear, salient pitch present in this sound — the anterolateral Heschl's Gyrus is strongly activated, and the sound has well-resolved harmonics."

When pitch_prominence = 0.15, the inference is: "The sound lacks a clear pitch — it is noise-like, has unresolved harmonics, or the pitch is too weak for cortical encoding."

This is a **sensory assessment**, not a recognition ("I know this note is C4") — that belongs to `pitch_identity` (PCCR). pitch_prominence answers: **"Is there a pitch at all, and how strong is it?"**

---

## 2. Observe Formula

```python
observed = (
    0.60 * P0_pitch_prominence_sig    # integrated pitch prominence
  + 0.25 * P1_hg_cortical_response    # HG region-specific activation
  + 0.15 * P3_salience_hierarchy      # hierarchical salience context
)
```

### Source Breakdown

| Source | Weight | Mechanism Layer | What It Captures |
|--------|--------|----------------|------------------|
| P0:pitch_prominence_sig | 60% | P-layer | Multi-source pitch salience (E0 + M0 + M3 + direct) |
| P1:hg_cortical_response | 25% | P-layer | Anterolateral HG activation (region-specific) |
| P3:salience_hierarchy | 15% | P-layer | Strong > Weak > Noise ranking with tonal context |

**Three complementary views of "pitch prominence"**:
1. **Salience** (P0): How prominent is the pitch overall? (quantity)
2. **Cortical** (P1): Is the pitch center in HG activated? (neural correlate)
3. **Hierarchical** (P3): Where in the salience ranking? (context)

---

## 3. Predict Formula

```python
predicted = (
    τ * prev                           # 35% previous value
  + (1 - τ) * baseline                 # 65% regression to 0.5
  + w_trend * H3_M18_pitch_salience    # pitch_salience trend (scale-matched)
  + w_period * H3_M14_concentration    # concentration periodicity
  + w_ctx * beliefs_context            # context from related beliefs
)
```

### Prediction Context Signals

| Signal | Source | Role |
|--------|--------|------|
| H³ M18 (trend) | pitch_salience at matched horizon | "Is pitch salience increasing or decreasing?" |
| H³ M14 (periodicity) | concentration at matched horizon | "Is pitch appearing periodically?" |
| `pitch_continuation` | PSCL F0 (Anticipation) | "PSCL's own trend extrapolation" |
| `harmonic_stability` | BCH (peer Core) | "Stable harmony supports pitch prominence" |

### τ = 0.35 Rationale

Moderate-low inertia because:
- Pitch changes in music can be rapid (melody, ornaments) but typically slower than harmonic shifts (chords)
- Cortical processing in alHG has ~30-100ms latency (slower than brainstem FFR)
- Pitch prominence should track note onsets/offsets with ~300ms response time
- Compare: `harmonic_stability` (τ=0.3) is slightly faster — brainstem vs cortical processing speed
- Compare: `pitch_identity` (τ=0.4) is slower — recognizing WHICH pitch takes more time

---

## 4. Update (Bayesian)

```python
PE = observed - predicted
gain = π_obs / (π_obs + π_pred + ε)
posterior = (1 - gain) * predicted + gain * observed
```

### Precision Sources

| Precision | Derivation |
|-----------|------------|
| π_obs | Confidence of pitch salience measurement (high when pitch is clear, low in noise/ambiguity) |
| π_pred | From PE history ring buffer — stable predictions → high π_pred |

### Prediction Error

`PE = observed − predicted`

- **Positive PE**: Pitch is MORE prominent than expected → surprising pitch onset or emergence
- **Negative PE**: Pitch is LESS prominent than expected → unexpected loss of pitch (noise intrusion, rest)

This PE feeds the **reward formula** (F6): `surprise = abs(PE)`, weighted by salience.

---

## 5. Multi-Scale Operation

pitch_prominence operates at **6 horizons** with T_char = 400ms:

| Horizon | Duration | Musical Meaning | Weight Profile |
|---------|----------|-----------------|----------------|
| H5 | 46ms | Pitch onset detection | Low weight |
| H7 | 250ms | Quarter note evaluation | Moderate |
| H10 | 400ms | Beat-level assessment | **Peak weight** |
| H13 | 600ms | Two-beat phrase | Moderate |
| H18 | 2s | Phrase-level | Low |
| H21 | 8s | Section-level | Low |

**Aggregation**: Scale-matched evidence weighting per BELIEF-CYCLE §Multi-Scale.

### Comparison with harmonic_stability

| Aspect | harmonic_stability (BCH) | pitch_prominence (PSCL) |
|--------|--------------------------|------------------------|
| Horizons | 8 (H0–H18) | 6 (H5–H21) |
| T_char | 200ms (brainstem) | 400ms (cortical) |
| Fastest | H0 = 5.8ms | H5 = 46ms |
| Slowest | H18 = 2s | H21 = 8s |

PSCL starts at H5 (not H0) because cortical pitch processing is inherently slower than brainstem. The extended reach to H21 (8s) captures phrase-level pitch tracking that brainstem cannot do.

---

## 6. Downstream Consumers

| Consumer | Function | How It Uses PE/Value |
|----------|----------|---------------------|
| Reward formula | F6 | PE from pitch_prominence → surprise component |
| Salience | F3 | Prominence value modulates salience (strong pitch = salient) |
| HTP prediction | F2 | Pitch presence as prediction context |
| PCCR (pitch_identity) | F1 | pitch_prominence gates chroma identification — no prominence = no identity |
| HMCE (temporal encoding) | F1 | Pitch stream informs temporal structure encoding |
| Familiarity | F4 | Prominent pitch patterns → recurrence tracking |
| RAM | — | Contributes to alHG, STG region activation |

---

## 7. What This Belief Is NOT

- **Not** pitch identity ("This is C4") → that's `pitch_identity` (PCCR, F1)
- **Not** harmonic stability ("This sound is consonant") → that's `harmonic_stability` (BCH, F1)
- **Not** melodic contour tracking ("The melody is going up") → that's `melodic_contour_tracking` (MPG, F1 Appraisal)
- **Not** aesthetic quality ("This sounds beautiful") → that's `aesthetic_quality` (STAI, F1)
- **Not** pitch continuation ("Pitch will persist") → that's `pitch_continuation` (PSCL, F1 Anticipation)

pitch_prominence is specifically: **"Is there a prominent pitch right now, and how strong is it?"**
