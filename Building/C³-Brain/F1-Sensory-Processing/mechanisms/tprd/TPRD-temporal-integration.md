# TPRD M-Layer — Temporal Integration (2D)

**Layer**: Mathematical (M)
**Indices**: [3:5]
**Scope**: internal
**Activation**: arithmetic (no sigmoid)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 3 | M0:dissociation_idx | [0, 1] | Normalized dissociation index. (T0-T1)/(T0+T1+eps) remapped to [0,1]. 0.0=pitch dominant, 0.5=balanced, 1.0=tonotopic dominant. Captures the relative strength of tonotopic vs pitch encoding. |
| 4 | M1:spectral_pitch_r | [0, 1] | Spectral-pitch coherence ratio. (1-T2)*min(T0,T1)/(max(T0,T1)+eps). High when T0 and T1 are aligned (low dissociation); low when dissociated. |

---

## Design Rationale

Two computed quantities from tonotopic-pitch encoding:

1. **Dissociation Index (M0)**: Normalized difference (T0-T1)/(T0+T1+eps) produces [-1,1], remapped to [0,1] via (x+1)/2. This is a balanced measure: 0.0 means pitch processing dominates, 0.5 means balanced encoding, 1.0 means tonotopic processing dominates. The eps=1e-7 prevents division by zero.

2. **Spectral-Pitch Ratio (M1)**: Coherence measure. When dissociation (T2) is low and T0/T1 are matched, M1 is high. The min/max ratio captures alignment (1.0 when equal, 0.0 when one is zero). The (1-T2) factor penalizes dissociated states. This quantifies how well the two encoding streams agree.

---

## H3 Dependencies

None. M-layer uses only T-layer outputs.

---

## Range Analysis

- M0 = ((sigmoid-sigmoid)/(sigmoid+sigmoid+eps) + 1) / 2 -> [0, 1]
- M1 = (1-sigmoid) * min/max -> [0, 1]
- Both naturally bounded, no clamping needed

---

## Scientific Foundation

- **Briley 2013**: Fundamental dissociation between tonotopic and pitch encoding in HG
- **Fishman 2001**: Phase-locked activity in A1/HG for dissonance; PT shows no phase-locking

## Implementation

File: `Musical_Intelligence/brain/functions/f1/mechanisms/tprd/temporal_integration.py`
