# DMMS E-Layer — Extraction (3D)

**Layer**: Extraction (E)
**Indices**: [0:3]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:early_binding | [0, 1] | Neonatal music-emotion scaffold strength. Hippocampus + Amygdala pairing. f37 = sigma(0.35 * (1 - roughness) * warmth + 0.35 * stumpf * encoding.mean + 0.30 * sensory_pleasantness). Partanen 2022: parental singing enhances auditory processing (MEG, N=33, eta2=0.229). |
| 1 | E1:dev_plasticity | [0, 1] | Critical period formation index. mPFC + Auditory cortex plasticity. f38 = sigma(0.40 * encoding.mean + 0.30 * x_l0l5.mean + 0.30 * (1 - entropy)). Qiu 2025: fetal-infant music exposure enhances mPFC/amygdala dendritic complexity (mouse, N=48, r=0.38). |
| 2 | E2:melodic_imprint | [0, 1] | Early melodic memory template strength. Auditory cortex + Hippocampus imprinting. f39 = sigma(0.40 * x_l5l7.mean * tonalness + 0.30 * familiarity.mean + 0.30 * warmth). Trehub 2003: infants prefer consonance, show enhanced processing of infant-directed singing. |

---

## Design Rationale

1. **Early Binding (E0)**: Tracks the neonatal music-emotion scaffold strength. Uses consonance (inverse roughness) and warmth as proxies for the caregiver voice "safety" signal. Stumpf fusion provides tonal binding coherence. Primary basis: Partanen 2022 MEG RCT showing parental singing enhances auditory processing in preterm infants.

2. **Developmental Plasticity (E1)**: Tracks the critical period formation index representing synaptic plasticity during the 0-5 year window. Encoding strength is weighted highest (0.40) as the primary plasticity driver. Energy-consonance interaction (x_l0l5) and low entropy (simple patterns scaffold first) contribute. Basis: Qiu 2025 showing dose-dependent mPFC/amygdala plasticity from music exposure.

3. **Melodic Imprinting (E2)**: Tracks how strongly melodic templates are formed during early exposure. The consonance-timbre interaction (x_l5l7) multiplied by tonalness captures the "familiar melodic pattern" signal. Warmth contributes as the caregiver voice proxy. Basis: Trehub 2003 on innate melodic contour sensitivity.

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (3, 16, 1, 2) | stumpf_fusion mean H16 L2 | Binding coherence at 1s for early binding |
| (4, 16, 0, 2) | sensory_pleasantness value H16 L2 | Current comfort signal for neonatal pairing |
| (12, 16, 0, 2) | warmth value H16 L2 | Current voice-warmth signal for caregiver proxy |
| (14, 16, 0, 2) | tonalness value H16 L2 | Melodic recognition state for imprinting |
| (0, 16, 0, 2) | roughness value H16 L2 | Current dissonance level (inverted for consonance) |
| (22, 16, 0, 2) | entropy value H16 L2 | Current pattern complexity for plasticity gating |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | E0: consonance proxy (1 - roughness) |
| [3] | stumpf_fusion | E0: tonal binding coherence |
| [4] | sensory_pleasantness | E0: comfort/safety association |
| [12] | warmth | E0+E2: caregiver voice proxy |
| [14] | tonalness | E2: melodic recognition template |
| [22] | entropy | E1: pattern complexity gating |
| [25:33] | x_l0l5 | E1: salience-binding scaffold |
| [41:49] | x_l5l7 | E2: familiarity template (consonance x timbre) |

---

## Brain Regions

| Region | MNI Coordinates | E-Layer Role |
|--------|-----------------|-------------|
| Hippocampus | +/-26, -18, -18 | E0: scaffold formation; E2: melodic template consolidation |
| Amygdala | +/-24, -4, -20 | E0: emotional tagging of early scaffolds |
| Auditory Cortex (A1/STG) | +/-54, -22, 8 | E1+E2: melodic template formation; enhanced by parental singing |
| mPFC | 0, 52, 12 | E1: critical period synaptic plasticity hub |

---

## Scientific Foundation

- **Partanen et al. 2022**: Parental singing enhances auditory processing in preterm infants (MEG RCT, N=33, eta2=0.229)
- **Qiu et al. 2025**: Fetal-infant music exposure enhances mPFC/amygdala dendritic complexity (mouse, N=48, r=0.38)
- **Trehub 2003**: Developmental origins of musicality; infants prefer consonance, show enhanced processing of infant-directed singing
- **DeCasper & Fifer 1980**: Neonates prefer mother's voice heard in utero (N=10)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/dmms/extraction.py`
