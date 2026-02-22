# perceived_sad — Core Belief (VMM)

**Category**: Core (full Bayesian PE)
**τ**: 0.55
**Owner**: VMM (ARU-α3)
**Multi-Scale**: single-scale in v1.0, T_char = 2s

---

## Definition

"This music sounds sad (perceived, not felt)." Tracks the perceived emotional character -- how sad the music SOUNDS, independent of how the listener FEELS. This is the complement of perceived_happy: the listener's cognitive categorization of sad musical content based on minor mode, dissonance, and low brightness cues. Symmetric τ of 0.55 with perceived_happy because both valence poles require the same phrase-level harmonic context.

The paradox of sad music is central to this belief: perceived_sad can be HIGH while SRP.pleasure is also HIGH. Listeners enjoy sad music precisely because perceived and felt emotion are computed by separable neural circuits (Brattico 2011). The limbic circuit (AMY + HIP + PHG) processes perceived sadness while the reward circuit (NAcc + VTA) processes felt pleasure independently.

---

## Multi-Scale Horizons

```
Single-scale in v1.0 kernel.
T_char = 2s (phrase-level emotional categorization)

When multi-scale extension is activated (deferred to wave 3+):
  Expected band: Macro
  Symmetric with perceived_happy -- same temporal dynamics.
  Mode detection requires 2-3 chords (~2s at 120 BPM)
  Minor-mode recognition is slightly faster than major (Khalfa 2005)
```

---

## Observation Formula

```
# Implicit (60%): H³ inverted mode + dissonance signals
inv_mode = 1 − mode_signal
inv_consonance = 1 − consonance_valence
inv_brightness = 1 − brightness_section
implicit = 0.50×inv_mode + 0.30×inv_consonance + 0.20×inv_brightness

# Explicit (40%): VMM P-layer perceived emotion
explicit = VMM.perceived_sad[P1]
# P1 = sigma(0.50×(1−mode_signal) + 0.30×(1−consonance_valence) + 0.20×(1−brightness_section))

# Combined: (0.60×implicit + 0.40×explicit) × energy_gate
# Energy gate: σ(10 × (energy − 0.1))

# Precision: mode_stability_H22 × consonance_state_H19 / (consonance_var_H19 + ε)
#            + VMM: 0.5×emotion_certainty
```

The implicit pathway captures the acoustic basis for sad categorization: minor mode (dark, less consonant) is the universal cue for negative valence (Fritz 2009: cross-cultural). The formula is the symmetric inverse of perceived_happy. Precision is identical because certainty about happy/sad classification depends on the same mode stability signal.

Relay components: VMM.perceived_sad[P1] + VMM.mode_signal[V1] (inverted) + VMM.consonance_valence[V2] (inverted) + VMM.emotion_certainty[P2].

---

## Prediction Formula

```
predict = Linear(τ × prev + w_trend × M18 + w_period × M14 + w_ctx × beliefs_{t-1})
```

Standard Bayesian PE cycle with gain = π_obs / (π_obs + π_pred). Symmetric with perceived_happy. M18 (consonance trend at H20) provides forward correction: falling consonance predicts increasing sadness. Context from beliefs_{t-1} includes perceived_happy (inversely related) and emotion_certainty.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| VMM P1 | perceived_sad [8] | P-layer sad categorization (40%) |
| VMM V1 | mode_signal [1] | Major/minor mode detection (inverted) |
| VMM V2 | consonance_valence [2] | Consonance-derived pleasantness (inverted) |
| VMM R1 | sad_pathway [4] | Limbic emotional circuit composite |
| H³ (14, 22, 0, 2) | brightness_section | Section brightness at 15s (inverted) |
| H³ (4, 19, 0, 2) | consonance_state | Phrase-level consonance at 3s (inverted) |
| H³ (4, 19, 1, 2) | consonance_mean | Baseline consonance at 3s (inverted) |
| R³ [4] | sensory_pleasantness | Consonance state and mean (inverted) |
| R³ [14] | tonalness | Brightness proxy (inverted for darkness) |

---

## Scientific Foundation

- **Brattico 2011**: Perceived sad -> bilateral AMY + PHG (Z>=3.5). Perceived != felt emotion (fMRI, N=15)
- **Khalfa 2005**: Sad recognition -> L.orbitofrontal / mid-dorsolateral frontal (fMRI)
- **Mitterschiffthaler 2007**: Sad music -> HIP t=4.88. Double dissociation from happy pathway (fMRI, N=16)
- **Koelsch 2006**: Dissonant -> AMY (t=4.7), HIP (t=6.9), PHG (t=5.7) (fMRI, N=11)
- **Sachs 2015**: Liked sad music -> Caudate z=6.27 (reward). Disliked -> Amygdala z=4.11. Sad + liked = paradox resolved by separate circuits (fMRI)
- **Carraturo 2025**: Minor=negative direction robust across k=70 studies (meta-analysis)
- **Green 2008**: Minor -> limbic BEYOND dissonance alone -- PHG, ventral ACC, mPFC (fMRI)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/vmm/temporal_integration.py`
