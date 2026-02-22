# MMP P-Layer — Temporal Integration (3D)

**Layer**: Present Processing (P)
**Indices**: [3:6]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 3 | P0:preserved_rec | [0, 1] | Current preserved recognition state. familiarity * preservation_factor. Measures how strongly the AD-resistant cortical pathway is recognizing the current music. High values = strong cortically-mediated recognition without hippocampal dependency. Scarratt et al. 2025: familiar music activates auditory, motor, emotion, and memory areas (fMRI, N=57). |
| 4 | P1:melodic_id | [0, 1] | Melody identification signal. familiarity * tonalness. Current accuracy of familiar melody matching through STG + angular gyrus. This signal persists even when hippocampal pattern completion fails. Sikka et al. 2015: age-related shift to angular gyrus for recognition (fMRI, N=40). |
| 5 | P2:familiarity | [0, 1] | Familiarity response (warmth). familiarity * x_l5l7.mean. The consonance-timbre interaction weighted by familiarity proxy. This is the primary signal indicating whether the listener recognizes the music through preserved cortical pathways. El Haj et al. 2012: music-evoked memories more specific and vivid than verbal-evoked in AD. |

---

## Design Rationale

1. **Preserved Recognition (P0)**: The present-moment state of cortically-mediated music recognition. This is the key clinical signal — it tells us how well the patient's preserved music-memory pathways are functioning right now. High preserved_rec even with impaired general memory indicates intact cortical music networks, making the patient a good candidate for music therapy.

2. **Melodic Identification (P1)**: The current accuracy of melody matching. Uses familiarity and tonalness (harmonic-to-noise ratio) to assess whether the melodic template stored in angular gyrus is being successfully retrieved. This signal is specifically about melody recognition, not emotional response.

3. **Familiarity (P2)**: The warmth-familiarity response. Uses consonance-timbre interaction (x_l5l7) as the acoustic signature of familiar music. This signal drives the "I know this music" experience that is preserved in AD and serves as the entry point for therapeutic music selection.

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (14, 20, 1, 0) | tonalness mean H20 L0 | Tonal stability over 5s |
| (12, 24, 19, 0) | warmth stability H24 L0 | Long-term warmth stability (36s) |
| (14, 24, 19, 0) | tonalness stability H24 L0 | Long-term tonal stability (36s) |
| (10, 16, 0, 2) | loudness value H16 L2 | Current arousal (1s) |
| (11, 16, 14, 2) | onset_strength periodicity H16 L2 | Rhythmic regularity (1s) |

---

## Scientific Foundation

- **Scarratt et al. 2025**: Familiar music activates auditory, motor, emotion, and memory areas; calm+familiar = max relaxation (fMRI, N=57, 4 response clusters)
- **Sikka et al. 2015**: Age-related shift to L-angular + L-superior-frontal for melody recognition (fMRI sparse-sampling, N=40)
- **El Haj et al. 2012**: Music-evoked autobiographical memories more specific and vivid than verbal-evoked in AD (behavioral, AD patients)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/mmp/temporal_integration.py`
