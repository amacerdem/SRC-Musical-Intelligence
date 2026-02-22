# resource_allocation — Appraisal Belief (DDSMI)

**Category**: Appraisal (observe-only)
**Owner**: DDSMI (MPU-beta2)

---

## Definition

"Brain prioritizing social over music." Observes the balance of neural processing resources between social coordination and music tracking during dyadic interaction. High resource allocation toward social processing indicates that visual contact and partner coordination demands are drawing neural resources away from auditory music tracking -- the brain is prioritizing the social partner over the musical stimulus. This reflects the resource competition documented by Bigand et al. 2025.

---

## Observation Formula

```
# Direct read from DDSMI E-layer + M-layer:
resource_allocation = 0.60 * DDSMI.f15_visual_modulation[E2]  # index [2]
                    + 0.40 * DDSMI.mTRF_balance[M2]           # index [5]

# f15 = sigma(0.35 * loudness_entropy + 0.35 * social_variability_100ms + 0.30 * (f13 - f14))
# mTRF_balance = sigma(0.5 * f13 + 0.5 * (1 - f14))
# mTRF_balance > 0.5: social dominates; < 0.5: music dominates
```

No prediction -- observe-only appraisal. The value tracks resource competition in real-time, reflecting visual contact modulation effects.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| DDSMI E2 | f15_visual_modulation [2] | Visual contact resource shift |
| DDSMI M2 | mTRF_balance [5] | Social/auditory resource ratio |
| DDSMI E0 | f13_social_coordination [0] | Social coordination level |
| DDSMI E1 | f14_music_tracking [1] | Music tracking level |
| H3 | (8, 3, 20, 2) | Loudness entropy at 100ms |
| H3 | (33, 3, 2, 2) | Social coupling variability at 100ms |

---

## Kernel Usage

Resource allocation modulates attentional salience:

```python
# Phase 3 in scheduler:
# Resource allocation signals social vs. music priority
# High value -> attention directed to social partner
# Low value -> attention directed to music
salience_modulation = ddsmi_relay['resource_allocation']
```

---

## Scientific Foundation

- **Bigand et al. 2025**: Visual contact reduces music tracking F(1,57)=7.48, p=.033 but increases social coordination F(1,57)=249.75, p<.001; resource competition between auditory and social processing (dual-EEG, N=70)
- **Bigand et al. 2025**: Self-movement tracking unaffected by visual contact or music presence (all ps>.224) -- motor control is autonomous, but social and auditory streams compete
- **Leahy et al. 2025**: Environmental factors (music, visual contact) modulate inter-brain coupling in social interaction (systematic review, 7 studies)
- **Sabharwal et al. 2024**: Leadership dynamics in dyadic music; directional coupling from EEG hyperscanning (N=60)

## Implementation

File: `Musical_Intelligence/brain/functions/f9/mechanisms/ddsmi.py`
