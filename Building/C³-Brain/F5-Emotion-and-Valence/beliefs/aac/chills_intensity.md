# chills_intensity — Appraisal Belief (AAC)

**Category**: Appraisal (observe-only)
**Owner**: AAC (F5)

---

## Definition

"Experiencing chills/frisson, intensity X." Tracks the peak emotional response — musical chills/frisson. This is the most studied peak-emotion phenomenon in music cognition. Chills are brief (5-15s) involuntary piloerection episodes accompanied by sympathetic surge (SCR up) and parasympathetic co-activation (HR deceleration). The intensity value reflects the magnitude of the current chills experience from absent (0) to maximal (1).

---

## Observation Formula

```
# Direct read from AAC E-layer:
chills_intensity = AAC.f04_emotional_arousal[E0]  # when peak threshold exceeded

# Alternatively, from NEMAC E-layer:
# chills_intensity = NEMAC.f05_chills[E0]  # index [0]
# NEMAC chills = sigma(alpha * warmth * vividness * reward * 3.0)

# Composite: max(AAC peak detection, NEMAC nostalgia-chills)
# AAC captures arousal-driven chills; NEMAC captures nostalgia-driven chills
```

No prediction — observe-only appraisal. The value is a composite of arousal-driven chills (AAC: sudden arousal spike exceeding peak threshold) and nostalgia-driven chills (NEMAC: convergence of warmth, vividness, and reward). Both pathways can independently produce chills.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| AAC E0 | f04_emotional_arousal [0] | Arousal-driven chills detection |
| AAC E1 | f06_ans_response [1] | ANS co-activation pattern (SCR up + HR down = chills) |
| AAC A0 | scr [2] | Sympathetic surge — primary chills marker |
| AAC A1 | hr [3] | Parasympathetic co-activation — vagal brake |
| NEMAC E0 | f05_chills [0] | Nostalgia-driven chills (warmth * vividness * reward) |

---

## Kernel Usage

The chills_intensity appraisal serves as a peak-emotion diagnostic signal:

```python
# Available in BeliefStore for downstream consumers:
# - F6 Reward: chills → dopamine release → strong positive reward
# - Precision engine: chills → high pi_obs for arousal beliefs
# - F4 Memory: chills during music → enhanced memory encoding
# - Salience: chills boost salience signal (peak moment detection)
```

Unlike the emotional_arousal Core belief (which integrates implicit H3 and explicit AAC signals), chills_intensity is a peak-event appraisal — it reports the specific chills/frisson state rather than the general arousal level.

---

## Scientific Foundation

- **Salimpoor et al. 2011**: Dopamine release during anticipation (caudate) and experience (nucleus accumbens) of musical chills; SCR correlated r=0.84 with dopamine (PET, N=8)
- **Blood & Zatorre 2001**: Musical chills activate ventral striatum, midbrain, amygdala, OFC, and insula; deactivate vmPFC and hippocampus (PET, N=10)
- **Chabin 2020**: Theta increase in OFC with pleasure, decreased theta in SMA + STG during chills (HD-EEG 256ch, N=18)
- **Mori & Zatorre 2024**: Pre-listening auditory-reward connectivity predicts chills duration (fMRI + LASSO, N=49, r=0.53)

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/aac_relay.py`
