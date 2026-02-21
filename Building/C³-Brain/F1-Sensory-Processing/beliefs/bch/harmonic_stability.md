# Belief: harmonic_stability

**Category**: Core
**Owner**: BCH (SPU-α1)
**Function**: F1 Sensory Processing
**Inertia (τ)**: 0.3 (low — responds quickly to harmonic changes)
**Baseline**: 0.5

---

## 1. What This Belief Says

> "This sound is harmonically resolved/stable."

When harmonic_stability = 0.85, the listener's auditory system infers: "The current sound has clear harmonic structure, low roughness, and the partials align well with a harmonic template. The sound is consonant."

When harmonic_stability = 0.15, the inference is: "The current sound is harmonically unresolved — high roughness, misaligned partials, dissonant."

This is **not** a preference judgment ("I like this"). It is a **sensory assessment** of the sound's harmonic coherence at the brainstem level.

---

## 2. Observe Formula

```python
observed = (
    0.50 * P0_consonance_signal       # perceptual consonance with tonal context
  + 0.30 * P1_template_match          # harmonic template structural fit
  + 0.20 * E2_hierarchy               # P1>P5>P4>M3>m6>TT position
)
```

### Source Breakdown

| Source | Weight | Mechanism Layer | What It Captures |
|--------|--------|----------------|------------------|
| P0:consonance_signal | 50% | P-layer | Roughness-based perceptual consonance + tonal context |
| P1:template_match | 30% | P-layer | Structural fit to harmonic series |
| E2:hierarchy | 20% | E-layer | Categorical consonance rank |

**Three complementary views of "harmonic stability"**:
1. **Perceptual** (P0): How smooth/pleasant does it sound? (roughness, pleasantness)
2. **Structural** (P1): Do the partials fit a harmonic template? (helmholtz, stumpf)
3. **Categorical** (E2): Where in the universal consonance hierarchy? (discrete ranking)

---

## 3. Predict Formula

```python
predicted = (
    τ * prev                           # 30% previous value (low inertia)
  + (1 - τ) * baseline                 # 70% regression to 0.5
  + w_trend * H3_M18_roughness         # roughness trend (scale-matched)
  + w_period * H3_M14_roughness        # roughness periodicity
  + w_ctx * beliefs_context            # context from related beliefs
)
```

### Prediction Context Signals

| Signal | Source | Role |
|--------|--------|------|
| H³ M18 (trend) | roughness at matched horizon | "Is roughness increasing or decreasing?" |
| H³ M14 (periodicity) | roughness at matched horizon | "Is roughness cycling predictably?" |
| `consonance_trajectory` | BCH F0 (Anticipation) | "BCH's own trend extrapolation" |
| `pitch_prominence` | PSCL (peer Core) | "Clear pitch supports harmonic stability" |

### τ = 0.3 Rationale

Low inertia because:
- Harmonic changes in music are often rapid (chord changes, ornaments)
- Brainstem processing is fast (5–25ms latency)
- The listener should respond quickly to consonance/dissonance shifts
- Compare: `autobiographical_retrieval` (τ=0.85) is slow because memories emerge gradually

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
| π_obs | Confidence of consonance measurement (high when roughness is clear, low in noise) |
| π_pred | From PE history ring buffer — stable predictions → high π_pred |

### Prediction Error

`PE = observed − predicted`

- **Positive PE**: Sound is MORE consonant than expected → pleasant surprise
- **Negative PE**: Sound is LESS consonant than expected → dissonant surprise

This PE feeds the **reward formula** (F6): `surprise = abs(PE)`, weighted by salience.

---

## 5. Multi-Scale Operation

harmonic_stability operates at **8 consonance horizons** with activated (non-uniform) weights:

| Horizon | Duration | Musical Meaning | Weight Profile |
|---------|----------|-----------------|----------------|
| H0 | 5.8ms | Phase-lock instant | Low weight |
| H3 | 23ms | Consonant onset | Moderate |
| H6 | 200ms | 16th note evaluation | **Peak weight** |
| H8 | 300ms | Beat-level | High |
| H10 | 400ms | Moderate beat | Moderate |
| H12 | 525ms | Two-beat motif | Moderate |
| H16 | 1s | Measure | Low |
| H18 | 2s | Phrase | Low |

**Aggregation**: Scale-matched evidence weighting per BELIEF-CYCLE §Multi-Scale.

---

## 6. Downstream Consumers

| Consumer | Function | How It Uses PE/Value |
|----------|----------|---------------------|
| Reward formula | F6 | PE from harmonic_stability → surprise component |
| Salience | F3 | Stability value modulates salience |
| HTP prediction | F2 | Consonance state as prediction context |
| Familiarity | F4 | Stable harmony → higher recurrence-based familiarity |
| RAM | — | Contributes to IC, AN, MGB region activation |

---

## 7. What This Belief Is NOT

- **Not** aesthetic preference ("I like consonance") → that's `aesthetic_quality` (STAI, F1)
- **Not** reward ("This consonance feels good") → that's F6 `wanting`/`liking` (SRP)
- **Not** pitch clarity ("I hear a clear pitch") → that's `pitch_prominence` (PSCL, F1)
- **Not** interval identification ("This is a perfect fifth") → that's `interval_quality` (BCH Appraisal, F1)

harmonic_stability is specifically: **"How resolved/stable is the harmonic structure right now?"**
