# Belief: pitch_continuation

**Category**: Anticipation
**Owner**: PSCL (SPU-α2)
**Function**: F1 Sensory Processing

---

## 1. What This Belief Says

> "Next event will contain a prominent pitch."

When pitch_continuation = 0.80, the cortical pitch system expects: "A clear pitch will persist or emerge in the next 200ms — the current trajectory of pitch salience indicates continuation."

When pitch_continuation = 0.20, the expectation is: "Pitch salience is fading — the next 200ms is likely to have weaker pitch or transition to noise."

This is a **forward prediction** about pitch presence, not a statement about pitch identity or pitch height. It answers: **"Will there be a pitch to perceive soon?"**

---

## 2. Source

```python
pitch_continuation = F0_pitch_continuation
```

### Mechanism Layer: F0

The source is PSCL F-layer output F0, which combines:

| Signal | Weight | What It Captures |
|--------|--------|------------------|
| H³ (14, H6, M18, L0) tonalness trend | 30% | "Is tonal quality increasing or decreasing?" |
| H³ (39, H6, M18, L0) pitch_salience trend | 25% | "Is pitch prominence increasing or decreasing?" |
| H³ (14, H6, M1, L1) expected tonalness | 20% | "What does the forward window show for tonal quality?" |
| H³ (39, H6, M1, L1) expected pitch_salience | 15% | "What does the forward window show for pitch salience?" |
| BCH.F1_pitch_forecast | 10% | "Does the brainstem agree about pitch trajectory?" |

---

## 3. Prediction Type: Trend Extrapolation

pitch_continuation uses **H³ M18 regression slopes** (trend) and **L1 forward means** to predict whether pitch salience will continue.

### What This IS
- **Trend extrapolation**: "Pitch salience has been stable/increasing → it will likely continue"
- **H³-grounded**: Uses stateless sliding-window temporal morphologies
- **Cortical timescale**: 200ms evaluation window (H6) — appropriate for pitch processing in alHG

### What This is NOT
- **NOT pattern prediction**: "After a V chord, the melody resolves to tonic" → that's F2/HTP domain
- **NOT identity prediction**: "The next note will be D5" → that's beyond PSCL's scope
- **NOT contour prediction**: "The melody will continue rising" → that's `contour_continuation` (MPG)

### Boundary with F2 (Prediction)

| Aspect | pitch_continuation (PSCL/F1) | HTP-based prediction (F2) |
|--------|-------------------------------|---------------------------|
| What | Will pitch be present? | Which pitch/pattern comes next? |
| Method | H³ trend extrapolation | Learned musical patterns |
| Timescale | ~200ms forward | Variable (100ms–5s) |
| Requires | R³/H³ only | Belief state + learned structure |

---

## 4. Role in the Bayesian Cycle

As an **Anticipation** belief, pitch_continuation does NOT undergo its own predict→observe→update cycle. Instead, it:

1. **Feeds** the `pitch_prominence` Core belief's predict() function as a context signal
2. **Informs** the precision engine — strong continuation predictions increase prediction precision (π_pred)
3. **Contributes** to salience computation — expected pitch continuation modulates attention

### How It Feeds pitch_prominence

```python
# Inside pitch_prominence.predict():
predicted = (
    τ * prev
  + (1 - τ) * baseline
  + w_trend * H3_M18_pitch_salience
  + w_period * H3_M14_concentration
  + w_ctx * pitch_continuation          # ← THIS
)
```

When pitch_continuation is high, it biases pitch_prominence prediction upward → if pitch then disappears, larger PE → larger surprise → stronger reward signal.

---

## 5. Downstream Consumers

| Consumer | Function | How It Uses This |
|----------|----------|-----------------|
| `pitch_prominence` predict() | F1 | Context signal in prediction formula |
| Precision engine | F1 | Modulates π_pred for pitch_prominence |
| Salience | F3 | Expected pitch continuation → attentional allocation |
| PCCR (pitch_identity) | F1 | If pitch expected → pre-activate chroma identification |
| HTP | F2 | Pitch persistence expectation as prediction context |

---

## 6. What This Belief Is NOT

- **Not** a Core belief — no predict/update cycle, no τ, no PE generation
- **Not** pitch identity prediction ("C4 will continue") → pitch-class-level prediction is F2/HTP territory
- **Not** consonance trajectory ("Harmony will stay stable") → that's `consonance_trajectory` (BCH)
- **Not** melodic contour continuation ("Melody will keep rising") → that's `contour_continuation` (MPG)

pitch_continuation is specifically: **"Will pitch be present and prominent in the near future?"**
