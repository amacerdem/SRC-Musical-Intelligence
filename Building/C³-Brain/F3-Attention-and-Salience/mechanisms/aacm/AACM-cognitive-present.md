# AACM P-Layer — Cognitive Present (2D)

**Layer**: Present Processing (P)
**Indices**: [5:7]
**Scope**: exported (kernel relay)
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 5 | P0:n1p2_engagement | [0, 1] | N1/P2 consonance-gated engagement. sigma(...+0.5*(1-roughness)). Consonance reduces roughness, allowing stronger N1/P2 engagement response. Sarasso 2019: N1/P2 amplitude proportional to preference (d=2.008). |
| 6 | P1:aesthetic_judgment | [0, 1] | Pleasantness-gated aesthetic judgment. sigma(...+0.5*pleasant). Ongoing real-time aesthetic evaluation gated by hedonic signal. Kim 2019: vmPFC activation during aesthetic judgments (T=6.852). |

---

## Design Rationale

1. **N1/P2 Engagement (P0)**: The present-moment consonance-gated engagement signal. This is the primary "right now" attention-capture output. Roughness is inverted: low roughness (high consonance) allows stronger engagement. This feeds the Appraisal belief `aesthetic_engagement` alongside M0.

2. **Aesthetic Judgment (P1)**: The present-moment pleasantness-gated evaluation. This captures the real-time aesthetic judgment — how pleasant the listener finds the current stimulus. Gated by the pleasant R3 feature to ensure the judgment is hedonic. Feeds the Appraisal belief `savoring_effect`.

---

## Kernel Relay Export

P-layer outputs are the primary relay exports:

| Export Field | P-Layer Idx | Kernel Usage |
|-------------|-------------|-------------|
| `n1p2_engagement` | P0 [5] | Feeds aesthetic_engagement Appraisal belief |
| `aesthetic_judgment` | P1 [6] | Feeds savoring_effect Appraisal belief |

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (0, 3, 0, 2) | roughness value H3 L2 | Consonance gating for N1/P2 engagement |
| (3, 6, 6, 2) | pleasant periodicity H6 L2 | Periodic hedonic fluctuation |
| (8, 16, 20, 2) | loudness entropy H16 L2 | Loudness entropy at 1s — attentional resource demand |

---

## Scientific Foundation

- **Sarasso 2019**: N1/P2 amplitude proportional to appreciation (EEG, d=2.008, eta2p=0.685)
- **Kim 2019**: vmPFC activation during aesthetic judgments (fMRI, T=6.852)
- **Salimpoor 2011**: Dopamine release in caudate/NAcc during pleasurable music (PET, r=0.71)

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/aacm/cognitive_present.py`
