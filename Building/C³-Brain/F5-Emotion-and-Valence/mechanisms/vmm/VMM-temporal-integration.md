# VMM Temporal Integration — Perceived Emotion (3D)

**Layer**: Temporal Integration (P-perceived)
**Indices**: [7:10]
**Scope**: exported (kernel relay)
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 7 | P0:perceived_happy | [0, 1] | Cognitive categorization "this sounds happy". f07 = sigma(0.50 * mode_signal + 0.30 * consonance_valence + 0.20 * brightness_section). Major + consonant + bright -> high. Fritz 2009: both Mafa and Germans use brightness + consonance for happy recognition. Brattico 2011: perceived happy -> R.insula, L.ACC. |
| 8 | P1:perceived_sad | [0, 1] | Cognitive categorization "this sounds sad". f08 = sigma(0.50 * (1 - mode_signal) + 0.30 * (1 - consonance_valence) + 0.20 * (1 - brightness_section)). Minor + less consonant + dark -> high. Khalfa 2005: sad recognition -> L.orbitofrontal. Brattico 2011: perceived sad -> bilateral AMY, PHG. |
| 9 | P2:emotion_certainty | [0, 1] | Categorization confidence. f09 = sigma(mode_stability_H22 + consonance_state_H19 - consonance_var_H19). High = clear major/minor (stable mode). Low = modulating, atonal, ambiguous. Drops during key changes and chromatic passages. |

---

## Design Rationale

1. **Perceived Happy (P0)**: The cognitive label "this sounds happy" — distinct from felt pleasure (SRP). This is Brattico's perceived emotion: the listener's classification of the music's emotional character. Dominated by mode signal (0.50) because mode is the strongest cue for happy categorization. Consonance valence and brightness are secondary cues. Fritz 2009 showed both Western-naive Mafa and German listeners use the same acoustic cues, confirming biological basis.

2. **Perceived Sad (P1)**: The cognitive label "this sounds sad." Computed as the inverse of the happy cues: minor mode (1 - mode_signal), dissonance (1 - consonance_valence), and darkness (1 - brightness). Khalfa 2005 found sad recognition engages left orbitofrontal and mid-dorsolateral frontal cortex. Brattico 2011 showed perceived sadness activates bilateral amygdala and PHG — partially overlapping with the sad_pathway but distinct from felt sadness.

3. **Emotion Certainty (P2)**: Confidence in the valence categorization. High when mode is stable (established key center at H22 15s), consonance is clear (strong tonal signal at H19 3s), and harmonic variance is low (consonance_var). Drops during modulation, atonal passages, and chromatic ambiguity. This is critical for the precision engine: low certainty means predictions about valence should carry low precision weighting.

---

## The Brattico Dissociation: Perceived vs Felt Emotion

```
PERCEIVED EMOTION (VMM P-layer):        FELT EMOTION (SRP P-layer):
"This music SOUNDS sad"                  "This music MAKES ME feel pleasure"

Bilateral amygdala                       NAcc, VTA (reward circuit)
Parahippocampal gyrus                    OFC (value computation)
R. claustrum, bilateral IFG              Overlapping but SEPARABLE

PARADOX OF SAD MUSIC:
  VMM.perceived_sad = HIGH               SRP.pleasure = HIGH
  The music sounds sad AND feels good.   This is expected, not contradictory.
  Separate neural circuits, separate computations.

  Sachs 2015: Liked -> Caudate z=6.27 (reward)
              Disliked -> Amygdala z=4.11 (aversion)
              But SAD music can be LIKED.
```

---

## Temporal Dynamics

```
MODE DETECTION REQUIRES PHRASE-LEVEL CONTEXT:

  Single frame (5.8ms): CANNOT determine mode
  1 chord (~0.5s):      Weak mode evidence
  2-3 chords (~2s):     Minimum for classification (Krumhansl & Kessler 1982)
  Full phrase (~5s):     Confident classification
  Section (~15s):        Stable tonal center

  VMM P-layer operates at PHRASE-TO-SECTION timescales (3s-15s)
  This is SLOWER than SRP (200ms-5s) or AAC (350ms-5s)

  Implication: perceived_happy/sad changes gradually (2-8s transitions)
  emotion_certainty dips during modulation then recovers over 8-15s
```

---

## Kernel Relay Export

P-layer perceived emotion feeds the C3 kernel:

| Export Field | P-Layer Idx | Kernel Usage |
|-------------|-------------|-------------|
| `perceived_happy` | P0 [7] | Reward formula: valence modulation |
| `perceived_sad` | P1 [8] | Reward formula: nostalgia/beauty pathway |
| `emotion_certainty` | P2 [9] | Precision engine: pi_pred for valence beliefs |

---

## H3 Dependencies (Temporal Integration)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (14, 22, 0, 2) | tonalness value H22 L2 | brightness_section — section brightness at 15s |
| (14, 22, 19, 2) | tonalness stability H22 L2 | mode_stability — tonal center stability at 15s |
| (4, 19, 0, 2) | sensory_pleasantness value H19 L2 | consonance_state — phrase-level consonance |
| (4, 19, 2, 2) | sensory_pleasantness std H19 L2 | consonance_var — harmonic ambiguity at 3s |

P-layer also reuses V+R layer outputs (mode_signal, consonance_valence, brightness_section) rather than making all H3 reads directly.

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [4] | sensory_pleasantness | P2: consonance state and variance for certainty |
| [14] | tonalness | P0+P1: brightness for happy/sad categorization |

---

## Scientific Foundation

- **Brattico 2011**: Perceived sad -> bilateral AMY + PHG (Z>=3.5). Perceived happy -> R.insula + L.ACC. Perceived != felt emotion (fMRI, N=15)
- **Fritz 2009**: Cross-cultural mode-valence — Mafa use brightness + consonance for happy recognition (behavioral, N=41+20, F(2,39)=15.48)
- **Khalfa 2005**: Sad recognition -> L.orbitofrontal / mid-dorsolateral frontal (fMRI)
- **Eerola & Vuoskoski 2011**: Valence categorization consistent across listeners. Factor 1 = valence (64% variance) (behavioral, N=116)
- **Krumhansl & Kessler 1982**: Probe-tone profiles require 2-3 chords for key classification
- **Carraturo 2025**: Major=positive, minor=negative across behavioral/EEG/fMRI modalities (meta-analysis, k=70)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/vmm/temporal_integration.py`
