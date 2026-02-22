# meter_structure -- Appraisal Belief (HGSIC)

**Category**: Appraisal (observe-only)
**Owner**: HGSIC (STU-beta5)

---

## Definition

"Accent pattern groups beats in X metric." Observes the metric structure extracted from accent grouping at the meter level (H11=500ms). High values indicate clear metric organization -- beats are grouped into regular patterns (duple, triple, etc.) with syncopation and accent hierarchies. This is the second level of HGSIC's hierarchical cascade: meter extraction from beat-level signals.

---

## Observation Formula

```
# From HGSIC E-layer:
meter_structure = HGSIC.f02_meter_integration[E1]  # index [1]

# f02 = sigma(0.51 * f01_beat_gamma * energy_periodicity)
# energy_periodicity = H3 (22, 11, 14, 2)  -- energy change periodicity at 500ms
# 0.51 is the meter integration weight
```

No prediction -- observe-only appraisal. The value represents the current metric organization strength.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| HGSIC E1 | f02_meter_integration [1] | Metric structure from accent grouping |
| HGSIC E0 | f01_beat_gamma [0] | Beat-level input to meter extraction |
| H3 | (22, 11, 14, 2) | Energy change periodicity at H11 (500ms) |
| H3 | (22, 11, 1, 0) | Energy change mean at 500ms |
| H3 | (21, 11, 1, 0) | Spectral change mean at 500ms |

---

## Kernel Usage

The meter_structure appraisal feeds F2 prediction for metric hierarchy:

```python
# F2 prediction context:
# Metric structure informs hierarchical prediction depth
# Clear meter -> stronger metric-level predictions
```

---

## Scientific Foundation

- **Potes et al. 2012**: Auditory-to-motor propagation at 110ms delay enables metric grouping (ECoG, N=4 motor electrodes)
- **Grahn & Brett 2007**: Putamen and SMA respond specifically to metric simple > complex rhythms (fMRI, N=27)
- **Spiech et al. 2022**: Groove follows inverted-U with syncopation level, implicating metric complexity (Pupillometry+behavioral, N=30)
- **Noboa et al. 2025**: Syncopated vs unsyncopated rhythms show distinct SS-EP patterns, F(1,29)=9.094 (EEG, N=30)

## Implementation

File: `Musical_Intelligence/brain/functions/f7/mechanisms/hgsic/` (no dedicated relay -- H3-grounded)
