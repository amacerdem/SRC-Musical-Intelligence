# perceived_happy — Core Belief (VMM)

**Category**: Core (full Bayesian PE)
**τ**: 0.55
**Owner**: VMM (ARU-α3)
**Multi-Scale**: single-scale in v1.0, T_char = 2s

---

## Definition

"This music sounds happy (perceived, not felt)." Tracks the perceived emotional character -- how happy the music SOUNDS, independent of how the listener FEELS. This is Brattico's perceived emotion: the listener's cognitive categorization of the music's affective content based on mode, consonance, and brightness cues. A τ of 0.55 reflects that valence perception requires phrase-level harmonic context (2-3 chords minimum) but updates when mode or consonance shifts -- slower than arousal (τ=0.5) but faster than nostalgia (τ=0.65).

The perceived/felt distinction is critical: perceived_happy can be HIGH while SRP.pleasure is LOW (boring happy music) or perceived_sad can be HIGH while SRP.pleasure is also HIGH (the sad music paradox). These are separate neural circuits (Brattico 2011) and separate computations in the kernel.

---

## Multi-Scale Horizons

```
Single-scale in v1.0 kernel.
T_char = 2s (phrase-level emotional categorization)

When multi-scale extension is activated (deferred to wave 3+):
  Expected band: Macro
  Mode detection requires 2-3 chords (~2s at 120 BPM)
  Full phrase confirmation at ~5s
  Section-level stability at ~15s
```

---

## Observation Formula

```
# Implicit (60%): H³ mode + consonance signals
mode_signal = sigma(0.40×brightness_section_H22 + 0.30×consonance_state_H19 + 0.30×consonance_mean_H19)
consonance_valence = sigma(0.50×consonance_state + 0.30×spectral_smoothness + 0.20×warmth)
implicit = 0.50×mode_signal + 0.30×consonance_valence + 0.20×brightness_section

# Explicit (40%): VMM P-layer perceived emotion
explicit = VMM.perceived_happy[P0]
# P0 = sigma(0.50×mode_signal + 0.30×consonance_valence + 0.20×brightness_section)

# Combined: (0.60×implicit + 0.40×explicit) × energy_gate
# Energy gate: σ(10 × (energy − 0.1))

# Precision: mode_stability_H22 × consonance_state_H19 / (consonance_var_H19 + ε)
#            + VMM: 0.5×emotion_certainty
```

The implicit pathway captures the acoustic basis for happy categorization: major mode (bright, consonant) is the universal cue for positive valence (Fritz 2009: cross-cultural, Mafa N=41). The explicit pathway reads VMM's P-layer computed perceived emotion. The 60/40 split reflects that categorization is primarily driven by bottom-up acoustic features, with the mechanism model confirming and enriching.

Relay components: VMM.perceived_happy[P0] + VMM.mode_signal[V1] + VMM.consonance_valence[V2] + VMM.emotion_certainty[P2].

---

## Prediction Formula

```
predict = Linear(τ × prev + w_trend × M18 + w_period × M14 + w_ctx × beliefs_{t-1})
```

Standard Bayesian PE cycle with gain = π_obs / (π_obs + π_pred). With τ=0.55, predictions are moderately autocorrelated -- emotional character is somewhat persistent across phrases but not as sticky as memory (τ=0.85). M18 (consonance trend at H20) provides the primary forward correction. Context from beliefs_{t-1} includes perceived_sad (inversely related) and emotion_certainty.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| VMM P0 | perceived_happy [7] | P-layer happy categorization (40%) |
| VMM V1 | mode_signal [1] | Major/minor mode detection |
| VMM V2 | consonance_valence [2] | Consonance-derived pleasantness |
| VMM R0 | happy_pathway [3] | Striatal reward circuit composite |
| H³ (14, 22, 0, 2) | brightness_section | Section brightness at 15s |
| H³ (4, 19, 0, 2) | consonance_state | Phrase-level consonance at 3s |
| H³ (4, 19, 1, 2) | consonance_mean | Baseline consonance at 3s |
| R³ [4] | sensory_pleasantness | Consonance state and mean for mode |
| R³ [14] | tonalness | Brightness proxy for mode detection |

---

## Scientific Foundation

- **Brattico 2011**: Perceived happy -> R.insula + L.ACC. Perceived != felt emotion -- separable neural circuits (fMRI, N=15)
- **Fritz 2009**: Cross-cultural mode-valence -- Mafa (no Western exposure) and Germans use brightness + consonance for happy recognition (behavioral, N=41+20, F(2,39)=15.48)
- **Mitterschiffthaler 2007**: Happy music -> VS t=4.58, DS z=3.80, ACC z=3.39 (fMRI, N=16)
- **Eerola & Vuoskoski 2011**: Valence is the dominant emotion dimension (64% variance) (behavioral, N=116)
- **Carraturo 2025**: Major=positive direction robust across k=70 studies; cultural modulation of strength not direction (meta-analysis)
- **Krumhansl & Kessler 1982**: Probe-tone profiles -- tonal center requires 2-3 chords for reliable classification

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/vmm/temporal_integration.py`
