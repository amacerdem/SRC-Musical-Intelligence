# VMM Cognitive Present — Mode Detection + Valence State (2D)

**Layer**: Cognitive Present (C)
**Indices**: [10:12]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 10 | C0:mode_detection_state | [0, 1] | Current mode classification confidence. f10 = sigma(0.40 * mode_stability_H22 + 0.30 * abs(mode_signal - 0.5) * 2 + 0.30 * emotion_certainty). High when mode is clearly established (strong major or minor). Low during modulation, chromaticism, or atonal passages. Reflects real-time tonal center tracking (Krumhansl & Kessler 1982). |
| 11 | C1:valence_state | [-1, 1] | Current integrated valence with pathway context. f11 = tanh(0.50 * f03_valence + 0.30 * (perceived_happy - perceived_sad) + 0.20 * reward_evaluation). Combines bipolar valence with categorization confidence and reward evaluation. The present-moment answer to "what is the emotional character of this music right now?" |

---

## Design Rationale

1. **Mode Detection State (C0)**: The real-time confidence that the tonal center is established and mode is classifiable. This is NOT the mode itself (that is V1:mode_signal) but the certainty that mode detection is reliable. High values mean the music is in a clear key with stable mode; low values mean it is modulating, chromatic, or atonal. Uses mode stability at section level (H22 15s), the distance of mode_signal from ambiguity (abs(mode_signal - 0.5) rescaled to [0,1]), and the P-layer emotion certainty. Critical for downstream consumers: when mode_detection_state is low, valence predictions should carry lower precision.

2. **Valence State (C1)**: The integrated present-moment valence experience combining all VMM computations. Weights bipolar valence (V0, the pathway dissociation), perceived emotion difference (P0 - P1, the cognitive label), and reward evaluation (R3, the ACC affect monitoring). This is the "cognitive present" answer — the listener's current valence experience integrating both bottom-up (pathway) and top-down (categorization) processing. Bipolar [-1, 1] via tanh.

---

## Cross-Model Context

VMM cognitive present operates at slower timescales than SRP or AAC:

```
TIMESCALE COMPARISON:

SRP P-layer:  wanting/liking/pleasure at beat-to-phrase (200ms-5s)
              → "How rewarding is this moment?"

AAC P-layer:  current_intensity/driving/perceptual at 350ms-1s
              → "How aroused am I right now?"

VMM C-layer:  mode_detection/valence_state at phrase-to-section (3s-15s)
              → "What is the emotional character right now?"

VMM is the SLOWEST cognitive present — requires harmonic context
that only emerges over multiple chords. This is appropriate:
valence perception is a contextual judgment, not a reflex.
```

---

## H3 Dependencies (Cognitive Present)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (14, 22, 19, 2) | tonalness stability H22 L2 | mode_stability — tonal center stability at 15s |

C-layer primarily computes from V+R and P-layer outputs rather than making new H3 reads. The single direct read is mode_stability which feeds mode_detection_state.

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| — | — | C-layer reads from V+R and P-layer outputs |

---

## Scientific Foundation

- **Krumhansl & Kessler 1982**: Probe-tone profiles — tonal center requires 2-3 chords, stability over longer contexts
- **Mitterschiffthaler 2007**: Happy/sad pathway double dissociation — basis for bipolar valence (fMRI, N=16)
- **Sachs 2025**: Context modulates neural event boundaries — valence processing is dynamic and context-dependent (fMRI + HMM, N=39)
- **Guo 2021**: Cultural expertise modulates auditory-reward circuit strength for valence (fMRI, N=49)
- **Eerola & Vuoskoski 2011**: Valence is the dominant emotion dimension (64% variance) (behavioral, N=116)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/vmm/cognitive_present.py`
