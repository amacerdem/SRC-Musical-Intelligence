# VRIAP M-Layer — Temporal Integration (2D)

**Model**: VR-Integrated Analgesia Paradigm (IMU-β7)
**Unit**: IMU (Integrative Memory Unit)
**Layer**: Temporal Integration (M)
**Indices**: [3:5]
**Scope**: internal
**Activation**: sigmoid / product
**Output Dim (total)**: 10D

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 3 | M0:analgesia_index | [0, 1] | Composite analgesia estimate. Product of engagement, pain gate, and multi-modal binding: analgesia_index = f01 * f02 * f03, clamped to [0,1]. Multiplicative gating reflects the requirement that all three components (motor engagement, pain gating, multi-modal binding) must be active for full analgesia. Arican & Soyman 2025: active engagement required, not passive listening (p=0.001). |
| 4 | M1:active_passive | [0, 1] | Active-passive differential. Motor contribution to analgesia beyond passive distraction. active_passive = sigma(0.50*f01 + 0.50*(f01 - familiarity)). When engagement > familiarity: active mode dominates. When engagement ~ familiarity: passive-like distraction only. Arican & Soyman 2025: passive music alone not significant vs silence (p=0.101). |

---

## Design Rationale

1. **Analgesia Index (M0)**: The core analgesic output is a product of the three E-layer components. This multiplicative formulation ensures that all three pathways (motor engagement, pain gating, multi-modal binding) must co-activate for meaningful analgesia. If any single component is absent (e.g., no motor engagement), the analgesic effect collapses toward zero. This matches the clinical evidence that active VR + music > passive listening (Liang 2025; Arican & Soyman 2025).

2. **Active-Passive Differential (M1)**: Captures the advantage of active motor interaction over passive listening. The formula uses the difference between engagement (f01) and familiarity as a proxy for the motor contribution — when the listener is actively engaged beyond mere recognition, the active mode dominates. When engagement equals familiarity (passive distraction only), the differential is minimal.

---

## H3 Dependencies (M-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (11, 20, 1, 0) | onset_strength mean H20 L0 | Sustained motor drive over 5s — engagement trajectory |
| (10, 20, 1, 0) | loudness mean H20 L0 | Average engagement over 5s — sustained immersion |
| (7, 20, 4, 0) | amplitude max H20 L0 | Peak energy over 5s — engagement ceiling |
| (4, 20, 18, 0) | sensory_pleasantness trend H20 L0 | Comfort trajectory over 5s — analgesia build-up |
| (0, 20, 18, 0) | roughness trend H20 L0 | Dissonance trajectory over 5s |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0:7] | Consonance group | Comfort/safety context for analgesia index |
| [7:12] | Energy group | Engagement dynamics for active-passive differential |

---

## Brain Regions

| Region | Coordinates | Evidence | Function |
|--------|-------------|----------|----------|
| M1 | +/-38, -20, 52 | Direct (fNIRS, Liang 2025 N=50) | Motor execution — VRMS > VRMI activation (RM1 z=-2.196, p=0.028) |
| mPFC | 0, 52, 12 | Inferred (Bushnell 2013) | Pain appraisal, therapeutic context encoding |
| NAcc | +/-10, 12, -8 | Direct (PET, Putkinen 2025 N=15) | Opioid release during music pleasure (BPND x chills r=-0.52) |

---

## Scientific Foundation

- **Liang et al. (2025)**: VRMS > VRMI for bilateral M1 activation (RM1 z=-2.196, p=0.028; LM1 t=2.065, p=0.044; fNIRS, N=50)
- **Putkinen et al. (2025)**: NAcc opioid release correlates with chills (r=-0.52, p<0.05, PET, N=15)
- **Arican & Soyman (2025)**: Task engagement > silence (W=236.5, p=0.001, r_rb=0.491, N=123); passive music alone not significant (p=0.101)
- **Melzack & Wall (1965)**: Gate control theory — non-nociceptive input gates pain signal transmission

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/vriap/temporal_integration.py`
