# NEWMD P-Layer — Cognitive Present (2D)

**Layer**: Present Processing (P)
**Indices**: [6:8]
**Scope**: exported (kernel relay)
**Activation**: sigmoid
**Model**: STU-γ2 (Neural Entrainment-Working Memory Dissociation, 10D, γ-tier <70%)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 6 | P0:current_entrain | [0, 1] | Instantaneous entrainment level. Beat-induction aggregation from E0 and M-layer paradox context. Represents the real-time "how entrained am I" signal. Nozaradan 2012: SS-EP magnitude tracks entrainment. |
| 7 | P1:current_wm_load | [0, 1] | Current working memory engagement. Temporal-context aggregation from E1 and M-layer balance. Represents the real-time "how much WM am I using" signal. Sares 2023: WM capacity independently predicts performance. |

---

## Design Rationale

1. **Current Entrainment (P0)**: The present-moment entrainment state. Aggregates the E-layer entrainment signal (E0) with temporal context from the M-layer paradox magnitude. This is the primary "entrainment status" output for the kernel — the real-time answer to whether the listener is locked to the beat.

2. **Current WM Load (P1)**: The present-moment working memory engagement. Aggregates E-layer WM capacity (E1) with temporal context from the dual-route balance. This tells the kernel how much cognitive (as opposed to automatic) processing the listener is applying to temporal structure.

---

## Kernel Relay Export

P-layer outputs are the primary relay exports:

| Export Field | P-Layer Idx | Kernel Usage |
|-------------|-------------|-------------|
| `current_entrain` | P0 [6] | Salience context: entrainment-based temporal attention |
| `current_wm_load` | P1 [7] | Precision engine: WM-based prediction confidence |

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (7, 6, 0, 0) | amplitude value H6 L0 | Beat amplitude at ~190ms — entrainment envelope |
| (8, 16, 1, 0) | loudness mean H16 L0 | Sustained loudness — WM tonic context |
| (9, 16, 15, 0) | spectral_centroid spectral_centroid H16 L0 | Spectral centroid stability — WM complexity |
| (21, 11, 8, 0) | spectral_change velocity H11 L0 | Spectral change rate — entrainment perturbation |
| (21, 11, 17, 0) | spectral_change skewness H11 L0 | Change asymmetry — entrainment disruption detection |
| (22, 14, 13, 0) | energy_change entropy H14 L0 | Energy unpredictability — WM demand |
| (23, 14, 1, 0) | pitch_change mean H14 L0 | Pitch trajectory — WM melodic tracking |

---

## Scientific Foundation

- **Nozaradan 2012**: SS-EP magnitude reflects real-time entrainment state (EEG, N=9)
- **Sares et al. 2023**: WM and entrainment independently track performance (N=48)
- **Grahn & Brett 2007**: Beat-locked activity in putamen/SMA (Z=5.67, fMRI, N=27)
- **Zanto et al. 2022**: Separable temporal attention mechanisms (RCT, d=0.52)

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/newmd/cognitive_present.py` (pending)
