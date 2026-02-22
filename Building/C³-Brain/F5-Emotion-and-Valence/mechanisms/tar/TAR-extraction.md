# TAR E-Layer — Extraction (1D)

**Layer**: Extraction (E)
**Indices**: [0:1]
**Scope**: internal
**Activation**: clamp [0, 1]

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:f14_therapeutic | [0, 1] | Overall therapeutic efficacy estimate. f14 = 0.5 * anxiety_sig + 0.5 * depression_sig. Weighted combination of anxiolytic and antidepressant signal strengths. anxiety_sig = f(tempo_factor, consonance, arousal, warmth); depression_sig = f(valence, energy, c0p_mean). Kheirkhah 2025: music + ketamine + mindfulness for depression, d = 0.88. Bradt & Dileo 2014: music interventions for anxiety, d ~ 0.5-0.8. |

---

## Design Rationale

1. **Therapeutic Efficacy (E0)**: The single extraction feature provides an overall estimate of the therapeutic potential of the current music. It averages two condition-specific signals: anxiolytic potential (how well the music calms anxiety via low tempo, high consonance, soft dynamics) and antidepressant potential (how well the music elevates mood via positive valence, moderate energy, reward activation). The 0.5/0.5 equal weighting reflects the assumption that both therapeutic targets are equally important — downstream consumers can weight them differently based on the clinical context.

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (4, 6, 0, 2) | sensory_pleasantness value H6 L2 | Instant affect state for therapeutic assessment |
| (4, 16, 0, 2) | sensory_pleasantness value H16 L2 | Sustained affect for efficacy estimation |
| (0, 6, 0, 2) | roughness value H6 L2 | Consonance for anxiety reduction signal |
| (10, 6, 0, 2) | loudness value H6 L2 | Arousal for dynamics assessment |
| (8, 6, 8, 0) | velocity_A velocity H6 L0 | Tempo proxy for therapeutic tempo matching |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | E0: inverse consonance for anxiety/valence signal |
| [4] | sensory_pleasantness | E0: direct hedonic for reward activation |
| [5] | harmonicity | E0: harmonic purity for consonance prescription |
| [7] | amplitude | E0: energy level for dynamics assessment |
| [8] | velocity_A | E0: rate of change as tempo proxy |
| [10] | loudness | E0: overall arousal level |
| [11] | onset_strength | E0: rhythmic engagement events |
| [16] | warmth | E0: comfort/safety signal for anxiolytic pathway |

---

## Scientific Foundation

- **Kheirkhah et al. 2025**: Music + ketamine + mindfulness combination therapy for treatment-resistant depression (RCT, d=0.88, Journal of Affective Disorders)
- **Bradt & Dileo 2014**: Music interventions for anxiety — meta-analysis of 26 trials shows d ~ 0.5-0.8 range (Cochrane Database)
- **Bowling 2023**: 4 biological principles for music and mental health: tonality, rhythm, reward, sociality — unifying framework (review, Translational Psychiatry, 13, 374)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/tar/extraction.py`
