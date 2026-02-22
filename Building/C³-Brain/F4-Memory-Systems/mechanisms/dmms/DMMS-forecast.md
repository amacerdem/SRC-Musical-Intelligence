# DMMS F-Layer — Forecast (3D)

**Layer**: Future Predictions (F)
**Indices**: [7:10]
**Scope**: internal
**Activation**: sigmoid / clamp

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 7 | F0:scaffold_persistence | [0, 1] | Scaffold persistence prediction (36s ahead). Hippocampal consolidation trajectory based on H24 long-term stability signals. Qiu 2025: dose-dependent social behavior improvement from prenatal-infant music exposure (r=0.38, p<0.0001). |
| 8 | F1:preference_formation | [0, 1] | Preference formation prediction (5s ahead). How strongly current exposure is forming new scaffold layers. Based on H20 consolidation window. Trainor & Unrau 2012: training before age 7 enhances processing. |
| 9 | F2:therapeutic_potential | [0, 1] | Therapeutic potential prediction. scaffold_activation * consonance. High when music accesses deep scaffolds — clinical application for music therapy. Scholkmann 2024: CMT induces measurable hemodynamic changes in neonatal cortex (fNIRS, N=17). |

---

## Design Rationale

1. **Scaffold Persistence (F0)**: Predicts whether the current scaffold activation will be sustained over a 36-second window. Uses the H24 horizon to capture long-term consolidation dynamics. High persistence means the hippocampal-cortical dialogue is actively consolidating the scaffold trace. This is the "will this memory stick?" prediction.

2. **Preference Formation (F1)**: Predicts whether current musical exposure is forming new preference scaffolds over a 5-second consolidation window. Uses the H20 horizon with familiarity trend. During the critical period, high preference formation means the listener is actively building new musical preference templates.

3. **Therapeutic Potential (F2)**: Predicts the clinical utility of current music for therapy applications. This is the product of scaffold activation (how deeply current music accesses early scaffolds) and consonance (how pleasant/safe the music feels). High therapeutic potential indicates music that can access deep developmental memories — the basis for music therapy in dementia and trauma recovery.

---

## H3 Dependencies (F-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (3, 24, 1, 0) | stumpf_fusion mean H24 L0 | Long-term binding scaffold for persistence |
| (10, 24, 3, 0) | loudness std H24 L0 | Arousal variability over 36s for persistence |
| (22, 24, 19, 0) | entropy stability H24 L0 | Pattern stability over 36s for persistence |
| (7, 20, 4, 0) | amplitude max H20 L0 | Peak energy over 5s for preference formation |

F-layer also reuses M-layer scaffold_strength and P-layer scaffold_activation.

---

## Cross-Function Downstream

| F-Layer Output | Consumer | Purpose |
|---------------|----------|---------|
| F0:scaffold_persistence | F4 Memory (MEAMN) | Scaffold depth for autobiographical memory retrieval |
| F1:preference_formation | F6 Reward (DAP) | Hedonic capacity shaped by scaffold formation |
| F2:therapeutic_potential | F10 Clinical (meta-layer) | Music therapy intervention targeting |

---

## Scientific Foundation

- **Qiu et al. 2025**: Fetal-infant music exposure induces lasting synaptic plasticity; dose-dependent effects (mouse, N=48, r=0.38)
- **Trainor & Unrau 2012**: Early training shapes auditory cortex development during sensitive period (review)
- **Scholkmann et al. 2024**: CMT induces hemodynamic changes in neonatal prefrontal/auditory cortex (fNIRS, N=17)
- **Whiteford et al. 2025**: COUNTEREVIDENCE — no FFR-training association at population level (N>260); scaffold effects may be cortical/hippocampal rather than subcortical

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/dmms/forecast.py`
