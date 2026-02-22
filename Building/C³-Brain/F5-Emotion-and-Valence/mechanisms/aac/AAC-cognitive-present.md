# AAC Cognitive Present — Real-Time Processing (3D)

**Layer**: Cognitive Present (P)
**Indices**: [9:12]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 9 | P0:current_intensity | [0, 1] | Real-time emotional arousal intensity. f09 = sigma(0.50 * f04_emotional_arousal + 0.30 * buildup_signal + 0.20 * peak_proximity). Immediate emotional state combining arousal level with anticipatory buildup. |
| 10 | P1:driving_signal | [0, 1] | Tempo-driven ANS component. f10 = sigma(0.50 * periodicity_H9 + 0.30 * periodicity_H16 + 0.20 * tempo_signal). Fast tempo drives higher ANS baseline independently of emotion. Beat clarity at 350ms (H9) and 1s (H16) captures rhythmic ANS entrainment. |
| 11 | P2:perceptual_arousal | [0, 1] | Onset-rate contribution to arousal. f11 = sigma(0.50 * onset_rate + 0.30 * energy_accel_H9 + 0.20 * spectral_flux_rate). Many onsets in a short window = high perceptual arousal. Distinct from emotional arousal — perceptual arousal from event density, not emotional significance. |

---

## Design Rationale

1. **Current Intensity (P0)**: The present-moment emotional intensity signal — "how intense is the emotional experience right now?" Integrates the top-level arousal (E0, amygdala-insula circuit) with anticipatory buildup (shared from SRP chills/peak detection). This is the summary output that best corresponds to continuous self-report ratings of emotional intensity. Peak proximity from SRP forecast enriches the signal with anticipatory information.

2. **Driving Signal (P1)**: The tempo-driven autonomic baseline — fast tempo directly elevates ANS regardless of emotional content. Beat clarity at two timescales: 350ms (individual beat onset detection) and 1s (bar-level periodicity). This captures why fast dance music elevates heart rate even when harmonic content is neutral. The rhythmic motor-autonomic coupling (Janata 2012) drives this independent of the reward pathway.

3. **Perceptual Arousal (P2)**: Event-density arousal — many acoustic events in rapid succession create high perceptual load that drives sympathetic activation. Distinct from emotional arousal (E0): a fast passage of scales has high perceptual arousal but may have low emotional significance. Uses onset rate (number of attacks per window), energy acceleration (onset sharpness), and spectral flux rate (timbral change density).

---

## Shared Mechanism Reading

P-layer reads from shared SRP mechanisms where applicable:

| Signal | Source | AAC Usage |
|--------|--------|-----------|
| buildup_signal | SRP chills/peak detection | P0: anticipatory buildup → current intensity |
| peak_proximity | SRP F-layer forecast | P0: how close to next peak → intensity boost |

---

## H3 Dependencies (Cognitive Present)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (10, 9, 14, 2) | spectral_flux periodicity H9 L2 | periodicity_h9 — beat clarity at 350ms |
| (10, 16, 14, 2) | spectral_flux periodicity H16 L2 | tempo_signal — bar-level periodicity at 1s |
| (7, 9, 11, 2) | amplitude acceleration H9 L2 | energy_accel — onset acceleration at 350ms |
| (11, 9, 22, 2) | onset_strength peaks H9 L2 | onset_rate — event density at 350ms |
| (21, 9, 8, 2) | spectral_flux velocity H9 L2 | spectral_flux_rate — timbral change density |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [7] | amplitude | P2: energy acceleration for perceptual arousal |
| [10] | spectral_flux | P1: beat periodicity, P2: timbral change rate |
| [11] | onset_strength | P2: onset density for perceptual arousal |
| [21] | spectral_flux | P2: spectral change velocity |

---

## Scientific Foundation

- **Gomez & Danuser 2007**: Factor structure confirms arousal dominance: RespR r=0.42 arousal, r=0.08 valence (multi-ANS, N=48)
- **Janata 2012**: Sensorimotor coupling — respiratory entrainment to beat (JEPG)
- **Craig 2009**: Anterior insula = interoceptive awareness hub for felt arousal (Nature Reviews Neuroscience)
- **Chabin 2020**: Theta up in OFC with pleasure, decreased theta in SMA + STG during chills (HD-EEG 256ch, N=18)
- **Sachs 2025**: Context modulates neural event boundaries — same music evokes different timing depending on preceding emotion (fMRI + HMM, N=39)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/aac/cognitive_present.py`
