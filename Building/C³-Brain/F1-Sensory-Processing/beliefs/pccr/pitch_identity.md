# Belief: pitch_identity

**Category**: Core
**Owner**: PCCR (SPU-α3)
**Function**: F1 Sensory Processing
**Inertia (τ)**: 0.4 (moderate — chroma recognition takes more time than detection)
**Baseline**: 0.5

---

## 1. What This Belief Says

> "This pitch belongs to chroma class X."

When pitch_identity = 0.85, the listener's auditory cortex has a confident pitch-class assignment: "The current sound has a clear, stable pitch that belongs to a specific chroma class. The pitch-class encoding is strong and reliable."

When pitch_identity = 0.15, the inference is: "The current sound's pitch class is ambiguous — the chroma distribution is scattered, the pitch is weak, or the sound is too inharmonic for octave-invariant pitch-class encoding."

This is a **recognition** judgment, not a detection judgment. `pitch_prominence` (PSCL) answers "Is there a pitch?" — `pitch_identity` answers "WHICH pitch class is it, and how confident is that assignment?"

---

## 2. Observe Formula

```
observed = (
    0.55 × P0:chroma_identity_signal    # multi-source chroma identification
  + 0.25 × P2:chroma_salience           # perceptual salience of identified chroma
  + 0.20 × E1:chroma_clarity            # raw chroma dominance
)
```

### Source Breakdown

| Source | Weight | Layer | What It Captures |
|--------|--------|-------|------------------|
| P0:chroma_identity_signal | 55% | P-layer | Integrated chroma ID from E+M+PSCL+BCH |
| P2:chroma_salience | 25% | P-layer | Perceptual prominence of the chroma class |
| E1:chroma_clarity | 20% | E-layer | Raw dominance of one chroma class |

**Three complementary views of "pitch identity"**:
1. **Identification** (P0): Full integration — is the chroma class reliably identified?
2. **Salience** (P2): How perceptually prominent is this pitch class?
3. **Clarity** (E1): Raw spectral evidence — does one class clearly dominate?

---

## 3. Predict Formula

```
predicted = (
    τ × prev                              # 40% previous value (moderate inertia)
  + (1 − τ) × baseline                    # 60% regression to 0.5
  + w_trend × H3_M18_pce                  # PCE trend (chroma stability direction)
  + w_period × H3_M14_tonalness           # tonalness periodicity (tonal cycling)
  + w_ctx × beliefs_context               # context from related beliefs
)
```

### Prediction Context Signals

| Signal | Source | Role |
|--------|--------|------|
| H³ M18 (trend) | pitch_class_entropy at matched horizon | "Is chroma getting clearer or noisier?" |
| H³ M14 (periodicity) | tonalness at matched horizon | "Is tonal quality cycling predictably?" |
| `chroma_continuation` | PCCR F0 (own Anticipation proxy) | "Will the current chroma persist?" |
| `pitch_prominence` | PSCL (upstream Core) | "Prominent pitch supports chroma identity" |

### τ = 0.4 Rationale

Moderate inertia because:
- Chroma identity is more stable than pitch detection — once you recognize "this is a C", it takes evidence to change that assessment
- Pitch-class recognition involves cortical categorization (slower than brainstem detection)
- Musical notes typically last 100–500ms, so chroma identity should persist across a note's duration
- Compare: `pitch_prominence` (τ=0.35) is slightly faster — detecting pitch presence is faster than recognizing pitch class
- Compare: `timbral_character` (τ=0.5, future) is slower — timbre recognition involves more integration

---

## 4. Update (Bayesian)

```
PE = observed − predicted
gain = π_obs / (π_obs + π_pred + ε)
posterior = (1 − gain) × predicted + gain × observed
```

### Precision Sources

| Precision | Derivation |
|-----------|------------|
| π_obs | Confidence of chroma identification (high when chroma is clear and pitch is prominent, low in noise/ambiguity) |
| π_pred | From PE history ring buffer — stable chroma predictions → high π_pred |

### Prediction Error

`PE = observed − predicted`

- **Positive PE**: Chroma is CLEARER than expected → unexpected pitch emergence or resolution to a clear key center
- **Negative PE**: Chroma is LESS clear than expected → unexpected chromatic motion, modulation, or pitch loss

This PE feeds the **reward formula** (F6): `surprise = abs(PE)`, weighted by salience.

---

## 5. Multi-Scale Operation

pitch_identity operates at **6 horizons** with T_char = 500ms:

| Horizon | Duration | Musical Meaning | Weight Profile |
|---------|----------|-----------------|----------------|
| H5 | 46ms | Chroma onset detection | Low weight |
| H8 | 300ms | Eighth note evaluation | Moderate |
| H10 | 400ms | Quarter note / beat | **Peak weight** |
| H14 | 700ms | Half note evaluation | High |
| H18 | 2s | Phrase-level chroma | Moderate |
| H22 | 10s | Section-level key identity | Low |

**T_char = 500ms**: Slower than pitch_prominence (400ms) because recognizing WHICH pitch class takes longer than detecting WHETHER there is a pitch. Peak weight at H10 (400ms) matches typical note durations.

---

## 6. Downstream Consumers

| Consumer | Function | How It Uses PE/Value |
|----------|----------|---------------------|
| Reward formula | F6 | PE from pitch_identity → surprise component |
| HTP prediction | F2 | Chroma class identity as harmonic prediction context |
| HMCE encoding | F1/STU | Chroma identity feeds melodic/temporal encoding |
| IMU memory binding | F4 | Pitch class → melodic memory trace |
| STU temporal structure | F1/STU | Chroma sequence → melodic contour |
| Familiarity | F4 | Repeating chroma patterns → recurrence tracking |
| RAM | — | Contributes to alHG, STG, STS region activation |

---

## 7. What This Belief Is NOT

- **Not** pitch detection ("Is there a pitch?") → that's `pitch_prominence` (PSCL, F1)
- **Not** harmonic quality ("Is this harmonically stable?") → that's `harmonic_stability` (BCH, F1)
- **Not** interval identification ("This is a fifth") → that's `interval_quality` (BCH Appraisal, F1)
- **Not** octave equivalence ("These tones share a chroma class") → that's `octave_equivalence` (PCCR Appraisal, F1)
- **Not** melodic identity ("This is the theme from Beethoven's 5th") → that's F4 memory domain
- **Not** key identity ("We are in C major") → that's F2 prediction domain

pitch_identity is specifically: **"The currently sounding pitch belongs to chroma class X with confidence Y."**

---

## 8. Relationship to pitch_prominence

| Aspect | pitch_prominence (PSCL) | pitch_identity (PCCR) |
|--------|------------------------|----------------------|
| Question | "Is there a pitch?" | "Which pitch class?" |
| Level | Detection | Recognition |
| τ | 0.35 (faster) | 0.40 (slower) |
| Can be high when other is low? | Yes (ambiguous pitch but present) | No (requires prominence) |
| Neural correlate | alHG activation | Cortical chroma encoding |
| Dependency | Independent | Gates on pitch_prominence |

pitch_identity **requires** pitch_prominence — PSCL.P0 feeds PCCR.P0 with 15% weight, and zero pitch prominence naturally produces zero chroma identity. Detection must precede recognition.
