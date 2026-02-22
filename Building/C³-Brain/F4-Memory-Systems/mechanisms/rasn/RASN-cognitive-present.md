# RASN P-Layer — Cognitive Present (3D)

**Layer**: Present Processing (P)
**Indices**: [5:8]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 5 | P0:entrainment_state | [0, 1] | Current neural oscillation lock. Beat induction aggregation reflecting real-time SMA phase-locking to rhythmic stimulus. Noboa et al. 2025: SS-EPs at beat-related frequencies (1.25 Hz, harmonics 2.5/5 Hz, EEG N=30). |
| 6 | P1:temporal_precision | [0, 1] | Beat tracking accuracy. Meter extraction x periodicity. Reflects cerebellar error correction producing precise temporal alignment. Ding et al. 2025: all 12 rates (1-12 Hz) entrain neural oscillations (ITPC eta-sq=0.14, EPS eta-sq=0.32, N=37). |
| 7 | P2:motor_facilitation_level | [0, 1] | Movement readiness state. Current motor pathway activation from rhythmic stimulation. Reflects premotor cortex + cerebellum engagement for beat-driven movement preparation. Harrison et al. 2025: external/internal cues activate sensorimotor cortex (N=55 fMRI). |

---

## Design Rationale

1. **Entrainment State (P0)**: Captures the real-time phase-locking state between neural oscillations and the auditory beat. This is the instantaneous reading of how well the brain has locked onto the rhythmic stimulus. Derived from beat_induction aggregation — the present-moment neural entrainment level that drives all downstream plasticity.

2. **Temporal Precision (P1)**: Measures how accurately the brain tracks the beat. Derived from meter_extraction crossed with periodicity. High temporal precision indicates clean cerebellar-SMA coordination where beat predictions closely match actual onsets. This is distinct from entrainment (which measures lock strength) — precision measures lock quality.

3. **Motor Facilitation Level (P2)**: The current state of motor pathway readiness driven by rhythmic stimulation. Captures the moment-by-moment activation of premotor cortex and cerebellum. This reflects the clinical observation that rhythmic auditory stimulation facilitates movement even without explicit motor tasks (covert motor simulation; Ross & Balasubramaniam 2022).

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (5, 6, 0, 2) | periodicity_strength value H6 L2 | Current rhythmic regularity at beat level |
| (5, 11, 14, 0) | periodicity_strength periodicity H11 L0 | Entrainment stability over 500ms |
| (10, 16, 14, 0) | spectral_flux periodicity H16 L0 | Beat regularity at 1s bar level |
| (7, 16, 1, 0) | amplitude mean H16 L0 | Average energy over 1s for motor state |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [5] | periodicity_strength | P1: rhythmic regularity for temporal precision |
| [10] | spectral_flux | P0+P1: beat onset for entrainment state |
| [11] | onset_strength | P1: beat precision measurement |
| [25:33] | x_l0l5 | P0: motor-auditory coupling for entrainment |

---

## Scientific Foundation

- **Noboa et al. 2025**: EEG N=30, SS-EPs at beat-related frequencies (1.25 Hz); working memory predicts tapping consistency
- **Ding et al. 2025**: EEG N=37, all 12 rates (1-12 Hz) entrain neural oscillations; ITPC eta-sq=0.14, EPS eta-sq=0.32
- **Ross & Balasubramaniam 2022**: Review, covert motor simulation for beat perception; motor networks active during passive listening
- **Harrison et al. 2025**: fMRI N=55, external/internal cues activate sensorimotor cortex, SMA, putamen (FWE-corrected)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/rasn/cognitive_present.py`
