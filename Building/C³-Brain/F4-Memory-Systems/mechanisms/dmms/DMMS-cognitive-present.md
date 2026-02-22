# DMMS P-Layer — Cognitive Present (2D)

**Layer**: Present Processing (P)
**Indices**: [5:7]
**Scope**: internal
**Activation**: clamp [0, 1]

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 5 | P0:scaffold_activation | [0, 1] | Current scaffold activation level. retrieval * familiarity. High when current music activates early templates (familiar warmth + consonance). Nguyen et al. 2023: caregivers universally communicate with infants via song; infant-directed singing supports co-regulation. |
| 6 | P1:bonding_warmth | [0, 1] | Caregiver-bonding warmth signal. familiarity * warmth * consonance. The "comfort" dimension of early memory — high when current music evokes caregiver voice template. Scholkmann 2024: CMT induces hemodynamic changes in neonatal prefrontal and auditory regions (fNIRS, N=17). |

---

## Design Rationale

1. **Scaffold Activation (P0)**: The present-moment signal for developmental memory scaffold engagement. This is the product of retrieval state and familiarity — both must be active for the scaffold to be considered "activated." This captures the moment when current music successfully triggers pattern completion of early templates in the hippocampus.

2. **Bonding Warmth (P1)**: The affective dimension of scaffold activation. This specifically captures the caregiver-bonding quality of early musical memories. The triple product (familiarity x warmth x consonance) requires all three conditions: the music must be familiar, have warm timbre (voice-like), and be consonant (pleasant/safe). This is the "comfort" signal that makes childhood music evoke the deepest emotional responses.

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (12, 16, 0, 2) | warmth value H16 L2 | Current voice-warmth for bonding signal |
| (0, 16, 0, 2) | roughness value H16 L2 | Current consonance for comfort gating |
| (10, 16, 0, 2) | loudness value H16 L2 | Current arousal level for scaffold activation |

P-layer primarily aggregates E+M outputs rather than introducing many new H3 tuples.

---

## Brain Regions

| Region | MNI Coordinates | P-Layer Role |
|--------|-----------------|-------------|
| Hippocampus | +/-26, -18, -18 | P0: pattern completion for scaffold retrieval |
| Auditory Cortex (A1/STG) | +/-54, -22, 8 | P0+P1: template matching for familiar patterns |
| Right Prefrontal Cortex | 40, 50, 10 | P1: online processing of caregiver-directed music (Scholkmann 2024 fNIRS) |

---

## Scientific Foundation

- **Nguyen, Trainor et al. 2023**: Universal infant-directed singing provides ecological mechanism for scaffold formation (review)
- **Scholkmann et al. 2024**: CMT induces hemodynamic changes in neonatal prefrontal and auditory cortex (fNIRS, N=17)
- **Sena Moore et al. 2025**: Musical contour, repetition, and temporal structure scaffold emotion regulation during critical period (theoretical model)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/dmms/cognitive_present.py`
