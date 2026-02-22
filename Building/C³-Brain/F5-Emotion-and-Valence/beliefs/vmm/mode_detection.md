# mode_detection — Appraisal Belief (VMM)

**Category**: Appraisal (observe-only)
**Owner**: VMM (ARU-α3)

---

## Definition

"Major/minor mode (0.5 = ambiguous)." Continuous value from 0 (clearly minor) to 1 (clearly major). This is NOT the raw mode signal (VMM V1:mode_signal) but the confidence-weighted mode classification state computed by the C-layer. It reflects the real-time answer to "is this music in a clear key with identifiable mode?" High values mean confidently major, low values mean confidently minor, and values near 0.5 indicate tonal ambiguity -- modulation, chromaticism, or atonality.

---

## Observation Formula

```
# Direct read from VMM C-layer:
mode_detection = VMM.mode_detection_state[C0]  # index [10]

# C0 = sigma(0.40×mode_stability_H22 + 0.30×abs(mode_signal − 0.5)×2 + 0.30×emotion_certainty)
# High when mode is clearly established (strong major or minor)
# Low during modulation, chromaticism, or atonal passages
```

No prediction -- observe-only appraisal. The value is directly read from the VMM mechanism's C-layer mode detection state. It combines three signals: section-level tonal stability (H22 15s), the distance of the mode signal from ambiguity (rescaled to [0,1]), and the P-layer emotion certainty.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| VMM C0 | mode_detection_state [10] | Real-time mode classification confidence |
| VMM V1 | mode_signal [1] | Upstream: raw major/minor mode detection |
| VMM P2 | emotion_certainty [9] | Upstream: categorization confidence |
| H³ (14, 22, 19, 2) | tonalness stability H22 L2 | mode_stability -- tonal center stability at 15s |

---

## Kernel Usage

The mode_detection appraisal serves as a diagnostic and gating signal:

```python
# Available in BeliefStore for downstream consumers:
# - F2 Prediction: mode confidence modulates harmonic prediction precision
# - F3 Attention: mode ambiguity drives salience (novelty detection)
# - Precision engine: low mode_detection → lower pi_obs for valence beliefs
```

Unlike the perceived_happy/perceived_sad Core beliefs (which track emotional categorization with Bayesian PE), mode_detection is a pure mechanism read -- it reports the tonal mode state without kernel-level integration.

---

## Scientific Foundation

- **Krumhansl & Kessler 1982**: Probe-tone profiles -- tonal center requires 2-3 chords, stability over longer contexts
- **Fritz 2009**: Cross-cultural mode recognition -- both Mafa and Germans rely on brightness + consonance (behavioral, N=41+20, F(2,39)=15.48)
- **Eerola & Vuoskoski 2011**: Valence categorization consistent across listeners, mode is primary cue (behavioral, N=116)
- **Carraturo 2025**: Major=positive, minor=negative direction robust across k=70 studies (meta-analysis)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/vmm/cognitive_present.py`
