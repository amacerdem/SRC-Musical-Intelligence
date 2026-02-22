# melodic_recognition — Appraisal Belief (MMP)

**Category**: Appraisal (observe-only)
**Owner**: MMP (IMU-a3)

---

## Definition

"I can still recognize this melody." Measures the degree to which familiar melodies are recognized, even in the presence of neurodegenerative disease. MMP models how musical semantic memory is preserved in AD due to storage in SMA/ACC rather than hippocampus. High values indicate strong cortically-mediated melody recognition through the STG + angular gyrus pathway.

---

## Observation Formula

```
# Direct read from MMP P-layer:
melodic_recognition = MMP.melodic_id[P1]  # index [4]

# Kernel usage: feeds familiarity computation
# Indicates whether the listener has prior knowledge of the melody
# through preserved cortical pathways (STG + angular gyrus)
```

No prediction -- observe-only appraisal. The value is directly consumed by the familiarity computation as an indicator of melody-level recognition accuracy.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| MMP P1 | melodic_id [4] | Primary melody identification signal |
| MMP R1 | f08_melodic [1] | Melodic recognition accuracy (R-layer) |
| MMP P0 | preserved_rec [3] | Preserved recognition state (context) |
| R3 [14] | tonalness | Melody tracking quality |
| R3 [18:21] | tristimulus1-3 | Instrument/voice identity |

---

## Kernel Usage

The melodic_recognition appraisal feeds the familiarity computation:

```python
# Phase 2a in scheduler:
# familiarity += w_melody * mmp_relay['melodic_id']
```

This provides the melody-specific component of familiarity: whether the listener recognizes the melodic contour through preserved cortical pathways, independent of episodic memory.

---

## Scientific Foundation

- **Jacobsen et al. 2015**: Musical memory regions (SMA, pre-SMA, ACC) show least cortical atrophy in AD -- melodic recognition preserved (fMRI+VBM, N=32)
- **Baird & Samson 2015**: Musical memory spared in dementia -- semantic musical memory more resilient than episodic
- **Sikka et al. 2015**: Older adults shift to L-angular + L-superior-frontal gyrus for melody recognition (fMRI sparse-sampling, N=40)
- **Scarratt et al. 2025**: Familiar music activates auditory, motor, emotion, and memory areas (fMRI, N=57, 4 response clusters)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/mmp/` (pending)
