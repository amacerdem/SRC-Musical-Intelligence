# emotion_certainty — Appraisal Belief (VMM)

**Category**: Appraisal (observe-only)
**Owner**: VMM (ARU-α3)

---

## Definition

"Certain/uncertain about emotional character." Confidence in the happy/sad classification. High when the music is in a clear key with stable mode -- the listener can confidently say "this sounds happy" or "this sounds sad." Low during modulation, atonal passages, chromaticism, and harmonic ambiguity -- moments when valence perception is unreliable. This signal is critical for the precision engine: when emotion_certainty is low, predictions about valence carry lower precision weighting.

---

## Observation Formula

```
# Direct read from VMM P-layer:
emotion_certainty = VMM.emotion_certainty[P2]  # index [9]

# P2 = sigma(mode_stability_H22 + consonance_state_H19 − consonance_var_H19)
# High = clear major/minor (stable mode, consistent consonance)
# Low = modulating, atonal, ambiguous (unstable mode, variable consonance)
```

No prediction -- observe-only appraisal. The value is directly read from the VMM mechanism's P-layer emotion certainty output. It combines three H3 signals: mode stability at section level (H22 15s, positive contribution), consonance clarity at phrase level (H19 3s, positive contribution), and harmonic variance (H19 3s, negative contribution -- ambiguity reduces certainty).

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| VMM P2 | emotion_certainty [9] | Categorization confidence signal |
| H³ (14, 22, 19, 2) | tonalness stability H22 L2 | mode_stability -- tonal center stability at 15s |
| H³ (4, 19, 0, 2) | sensory_pleasantness value H19 L2 | consonance_state -- phrase-level consonance |
| H³ (4, 19, 2, 2) | sensory_pleasantness std H19 L2 | consonance_var -- harmonic ambiguity at 3s |

---

## Kernel Usage

The emotion_certainty appraisal serves as a precision modulator:

```python
# Available in BeliefStore for downstream consumers:
# - Precision engine: pi_pred for perceived_happy and perceived_sad Core beliefs
#   When emotion_certainty is LOW:
#     → pi_obs for valence beliefs DECREASES
#     → Bayesian gain shifts toward prediction (prior dominates)
#     → Valence beliefs become less responsive to noisy observations
# - F2 Prediction: harmonic prediction confidence adjustment
# - F3 Attention: uncertain valence → heightened salience (novelty)
```

Emotion certainty drops during key changes and chromatic passages, then recovers over 8-15s as the new tonal center stabilizes. This temporal profile matches the typical modulation resolution time in tonal music.

---

## Scientific Foundation

- **Krumhansl & Kessler 1982**: Probe-tone profiles require 2-3 chords for key classification; stability over longer contexts
- **Sachs 2025**: Context modulates neural event boundaries -- valence processing is dynamic and context-dependent (fMRI + HMM, N=39)
- **Eerola & Vuoskoski 2011**: Valence categorization consistent across listeners when mode is clear (behavioral, N=116)
- **Lerdahl 2001**: Tonal pitch space -- section-level context required for modulation detection

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/vmm/temporal_integration.py`
