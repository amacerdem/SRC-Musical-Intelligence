# wellbeing_enhancement — Appraisal Belief (NEMAC)

**Category**: Appraisal (observe-only)
**Owner**: NEMAC (F5)

---

## Definition

"Nostalgic music increasing my well-being." Tracks whether the nostalgia experience is enhancing subjective well-being, counteracting loneliness, or increasing social connectedness. This appraisal captures the therapeutic dimension of music-evoked nostalgia — the N-BMI (Nostalgia-Brain-Music Interface) loop where nostalgic engagement produces measurable mood improvement. The dose-response relationship (beta ~ 0.7) means strong nostalgia reliably predicts well-being enhancement.

---

## Observation Formula

```
# Direct read from NEMAC F-layer:
wellbeing_enhancement = NEMAC.wellbeing_pred[F0]  # index [9]

# wellbeing_pred = sigma(nostalgia_intensity * 0.7)
# nostalgia_intensity: current nostalgia state from E-layer + P-layer integration
# 0.7 coefficient: dose-response transfer rate (nostalgia → wellbeing)

# Wellbeing computation chain:
# 1. NEMAC E1: f11_nostalgia (current nostalgia strength)
# 2. NEMAC P0: nostalgia_correl (acoustic match to nostalgia profile)
# 3. NEMAC F0: wellbeing_pred (predicted mood improvement 5-30s ahead)
```

No prediction — observe-only appraisal. The value is read from the NEMAC forecast layer's wellbeing prediction, which applies the nostalgia-to-wellbeing transfer function. It represents the estimated mood improvement from the current nostalgic engagement.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| NEMAC F0 | wellbeing_pred [9] | Well-being improvement prediction |
| NEMAC E1 | f11_nostalgia [1] | Current nostalgia intensity (upstream input) |
| NEMAC P0 | nostalgia_correl [7] | Acoustic nostalgia correlate (upstream input) |
| H3 | (10, 20, 1, 0) loudness mean H20 L0 | Arousal trajectory for wellbeing prediction |
| H3 | (22, 20, 19, 0) entropy stability H20 L0 | Pattern stability for familiarity trajectory |

---

## Kernel Usage

The wellbeing_enhancement appraisal serves as a therapeutic benefit diagnostic:

```python
# Available in BeliefStore for downstream consumers:
# - F6 Reward: well-being enhancement modulates sustained positive reward
# - F5 Emotion: well-being trajectory modulates emotional valence
# - F3 Attention: high well-being → sustained attention to nostalgic passages
# - Clinical (F10): primary signal for music therapy outcome prediction
```

Unlike the nostalgia_affect Core belief (which tracks the felt nostalgic state), wellbeing_enhancement captures the downstream consequence — whether nostalgia is producing its therapeutic benefit. Strong nostalgia without well-being improvement (low transfer) may indicate complicated nostalgia (more bitter than sweet).

---

## Scientific Foundation

- **Sakakibara et al. 2025**: N-BMI loop: nostalgia engagement enhances well-being; dose-response relationship validated experimentally (EEG + behavioral, N=33, eta_p^2=0.541)
- **Barrett et al. 2010**: Nostalgia-wellbeing link modulated by personality traits; nostalgia counteracts loneliness and increases social connectedness (behavioral, N=226)
- **Wildschut et al. 2006**: Nostalgia is predominantly positive — increases self-esteem, social connectedness, and meaning in life; music is the most common trigger (behavioral, N=172)

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/nemac_relay.py`
