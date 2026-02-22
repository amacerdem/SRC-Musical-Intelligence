# VRIAP F-Layer — Forecast (3D)

**Model**: VR-Integrated Analgesia Paradigm (IMU-β7)
**Unit**: IMU (Integrative Memory Unit)
**Layer**: Forecast (F)
**Indices**: [7:10]
**Scope**: internal
**Activation**: sigmoid
**Output Dim (total)**: 10D

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 7 | F0:analgesia_fc | [0, 1] | Analgesia trajectory prediction (2-5s ahead). Based on engagement and pain gating trends using H20 (5s) horizon features. Predicts whether analgesic effect is building, stable, or declining. Uses retrieval dynamics trajectory from mnemonic circuit. Liang 2025: sustained VRMS FC effects over block durations support predictable analgesia trajectories. |
| 8 | F1:engagement_fc | [0, 1] | Motor engagement prediction (1-3s ahead). Premotor activation trajectory based on H16 (1s) horizon features. Predicts whether motor coupling will strengthen or weaken based on current onset patterns and amplitude dynamics. Uses encoding state trajectory from mnemonic circuit. |
| 9 | F2:reserved | [0, 1] | Reserved for future expansion. Currently outputs zeros. Potential use: therapeutic consolidation prediction using H24 (36s) horizon. |

---

## Design Rationale

1. **Analgesia Forecast (F0)**: Projects the analgesic state 2-5s into the future using H20 (5s window) trend features. This prediction enables the system to anticipate periods of stronger or weaker pain modulation based on the trajectory of engagement, pain gating, and multi-modal binding. Uses _predict_future() with retrieval dynamics from the mnemonic circuit and H20 window features (pleasantness trend, roughness trend, loudness mean).

2. **Engagement Forecast (F1)**: Projects motor engagement 1-3s ahead using H16 (1s window) features. This shorter-horizon prediction tracks the immediate trajectory of motor coupling with musical structure. Useful for anticipating periods where active engagement may lapse (e.g., during musical transitions) or strengthen (e.g., during groove sections). Uses _predict_future() with encoding state and H16 window features.

3. **Reserved (F2)**: Placeholder for future therapeutic consolidation prediction. When implemented, would use H24 (36s) horizon features to predict long-term analgesic memory formation, tracking hippocampus-mPFC encoding of pain-free states for repeated music-VR therapy applications.

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (4, 20, 18, 0) | sensory_pleasantness trend H20 L0 | Comfort trajectory for analgesia prediction |
| (0, 20, 18, 0) | roughness trend H20 L0 | Dissonance trajectory for analgesia prediction |
| (10, 20, 1, 0) | loudness mean H20 L0 | Average engagement over 5s — sustained trend |
| (10, 24, 3, 0) | loudness std H24 L0 | Engagement variability over 36s — stability |
| (22, 20, 1, 0) | entropy mean H20 L0 | Average complexity over 5s — predictability trend |
| (22, 24, 19, 0) | entropy stability H24 L0 | Pattern stability over 36s |
| (3, 20, 1, 0) | stumpf_fusion mean H20 L0 | Binding stability over 5s for consolidation |
| (21, 20, 1, 0) | spectral_flux mean H20 L0 | Sustained change rate for event prediction |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | F0: dissonance trajectory input |
| [4] | sensory_pleasantness | F0: comfort trajectory input |
| [10] | loudness | F0+F1: engagement trajectory |
| [22] | entropy | F0: complexity/predictability trajectory |

---

## Brain Regions

| Region | Coordinates | Evidence | Function |
|--------|-------------|----------|----------|
| mPFC | 0, 52, 12 | Inferred (Bushnell 2013) | Therapeutic context encoding, analgesic prediction |
| Hippocampus | +/-20, -24, -12 | Inferred | Analgesic memory consolidation, long-term prediction |
| ACC | 0, 30, 24 | Direct (fMRI, Putkinen 2025 N=30) | Pain-pleasure appraisal, trajectory evaluation |

---

## Scientific Foundation

- **Liang et al. (2025)**: VRMS block design shows sustained FC enhancement over experimental blocks, supporting temporally extended analgesic trajectories (fNIRS, N=50)
- **Putkinen et al. (2025)**: ACC shows pleasure-dependent BOLD and MOR-BOLD correlation — appraisal trajectory (fMRI, N=30; PET, N=15)
- **Bushnell et al. (2013)**: mPFC modulates pain processing through top-down cognitive and emotional mechanisms — predictive pain modulation
- **Garza-Villarreal et al. (2017)**: Moderate pooled analgesic effects across conditions support reliable, predictable analgesia trajectories

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/vriap/forecast.py`
