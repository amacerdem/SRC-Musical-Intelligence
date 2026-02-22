# DMMS M-Layer — Temporal Integration (2D)

**Layer**: Mathematical Model (M)
**Indices**: [3:5]
**Scope**: internal
**Activation**: sigmoid / clamp

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 3 | M0:scaffold_strength | [0, 1] | Overall scaffold formation/activation strength. Combines encoding and familiarity signals through binding coherence. scaffold_strength = clamp(encoding * binding_coherence + familiarity * imprint_depth_raw, 0, 1). Strait 2012: early training enhances subcortical encoding (ABR, N=31, r=0.562-0.629). |
| 4 | M1:imprinting_depth | [0, 1] | Depth of melodic imprinting into long-term scaffold. sigma(0.35 * familiarity + 0.35 * tonalness + 0.30 * warmth). High when music matches early templates. Trainor & Unrau 2012: auditory cortex development is experience-dependent during sensitive period. |

---

## Design Rationale

1. **Scaffold Strength (M0)**: The core mathematical model for developmental scaffold formation. This is a multiplicative combination: encoding strength times binding coherence (stumpf x consonance) plus familiarity times imprinting depth (x_l5l7 x tonalness). Both encoding AND coherent tonal binding must be present for scaffold formation. The multiplicative structure ensures that weak encoding or weak binding produces weak scaffolds.

2. **Imprinting Depth (M1)**: Quantifies how deeply a melodic pattern has been imprinted into the scaffold. Uses familiarity (0.35), tonalness (0.35), and warmth (0.30). All three weighted roughly equally because deep imprinting requires familiar patterns that are tonal (melodic) and warm (voice-like). High imprinting depth indicates the current music closely matches templates laid down during the critical period.

---

## Mathematical Formulation

```
Scaffold Strength:
  binding_coherence = stumpf[3] * consonance
  imprint_depth_raw = x_l5l7.mean() * tonalness[14]
  scaffold_strength = clamp(encoding * binding_coherence + familiarity * imprint_depth_raw, 0, 1)

Imprinting Depth:
  imprinting_depth = sigma(0.35 * familiarity + 0.35 * tonalness + 0.30 * warmth)
  |0.35| + |0.35| + |0.30| = 1.0
```

---

## H3 Dependencies (M-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (3, 24, 1, 0) | stumpf_fusion mean H24 L0 | Long-term binding scaffold at 36s |
| (4, 20, 1, 0) | sensory_pleasantness mean H20 L0 | Sustained pleasantness over 5s consolidation |
| (14, 20, 1, 0) | tonalness mean H20 L0 | Tonal template stability over 5s |
| (12, 20, 1, 0) | warmth mean H20 L0 | Sustained warmth for caregiver signal |
| (0, 20, 1, 0) | roughness mean H20 L0 | Consonance scaffold stability over 5s |

---

## Scientific Foundation

- **Strait et al. 2012**: Early musical training enhances subcortical speech encoding (ABR, N=31, r=0.562-0.629)
- **Trainor & Unrau 2012**: Musical training before age 7 enhances auditory processing; experience-dependent development
- **Qiu et al. 2025**: Dose-dependent synaptic plasticity in mPFC/amygdala from music exposure (mouse, N=48)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/dmms/temporal_integration.py`
