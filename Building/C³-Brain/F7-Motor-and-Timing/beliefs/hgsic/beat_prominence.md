# beat_prominence -- Appraisal Belief (HGSIC)

**Category**: Appraisal (observe-only)
**Owner**: HGSIC (STU-beta5)

---

## Definition

"Sound intensity high; beat is prominent." Observes the current prominence of the beat as tracked by pSTG high-gamma activity. High values indicate that the sound intensity envelope has strong, clear beat-aligned peaks -- the beat is acoustically salient and readily available for motor entrainment. This is the first level of HGSIC's hierarchical cascade: beat induction from intensity tracking.

---

## Observation Formula

```
# From HGSIC E-layer + P-layer:
beat_prominence = 0.50*f01_beat_gamma + 0.50*pstg_activation

# f01 = sigma(0.49 * amp_val * loud_val * onset_val)
# pstg_activation = sigma(0.5 * amp_val * loud_val)
# 0.49 from Potes 2012 (pSTG high-gamma <-> intensity, r=0.49)
```

No prediction -- observe-only appraisal. The value represents current beat-level acoustic salience.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| HGSIC E0 | f01_beat_gamma [0] | Beat-level gamma tracking |
| HGSIC P0 | pstg_activation [5] | pSTG current activation state |
| H3 | (7, 6, 0, 0) | Amplitude value at H6 (200ms beat level) |
| H3 | (8, 6, 0, 0) | Loudness value at H6 |
| H3 | (11, 6, 0, 0) | Onset strength value at H6 |

---

## Kernel Usage

The beat_prominence appraisal feeds F3 attention for salience allocation:

```python
# F3 salience mixer context:
# Beat prominence modulates how much attention is allocated to rhythmic events
# Higher beat_prominence -> stronger beat-aligned salience peaks
```

---

## Scientific Foundation

- **Potes et al. 2012**: pSTG high-gamma (70-170 Hz) correlates with sound intensity r=0.49, per-subject range 0.43-0.58 (ECoG, N=8). NOTE: intensity tracking, not groove/beat directly (see HGSIC doc S3.1.2)
- **Nourski et al. 2014**: Hierarchical temporal processing in auditory cortex -- beat-level is foundational (ECoG)
- **Noboa et al. 2025**: SS-EPs at beat frequency F(1,29)=148.618 faithfully track beat even in syncopation (EEG, N=30)

## Implementation

File: `Musical_Intelligence/brain/functions/f7/mechanisms/hgsic/` (no dedicated relay -- H3-grounded)
