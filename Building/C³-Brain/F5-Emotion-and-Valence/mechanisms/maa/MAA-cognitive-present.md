# MAA P-Layer — Cognitive Present (3D)

**Layer**: Present Processing (P)
**Indices**: [4:7]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 4 | P0:pattern_search | [0, 1] | Real-time pattern recognition attempt in atonal structure. Pitch-processing search for regularity within high-entropy harmonic sequences. Bravo 2017: right Heschl's gyrus shows heightened response under uncertainty (p<0.05 cluster-corrected); Gold 2023: R STG reflects liking via pattern detection. |
| 5 | P1:context_assessment | [0, 1] | Timbre-processing framing application. Cognitive evaluation of current spectral context for meaning extraction. Huang 2016: mPFC + ToM areas active for artistic framing (p<0.05 FWE); Sarasso 2019: aesthetic appreciation enhances N1/P2 attentional engagement (eta2_p=0.685). |
| 6 | P2:aesthetic_evaluation | [0, 1] | Memory-encoding appreciation response. Integrated aesthetic judgment incorporating complexity tolerance, familiarity, and framing. Derived from f04 (appreciation composite). Cheung 2019: NAc reflects uncertainty (beta=0.242, p=0.002); Teixeira Borges 2019: cortical scaling mediates pleasure (r=0.37-0.42). |

---

## Design Rationale

1. **Pattern Search (P0)**: The real-time cognitive effort to find structure in atonal music. When listeners encounter high-entropy sequences, auditory cortex (particularly right Heschl's gyrus) increases its gain to search for patterns. This reflects the active listening strategy where appreciation depends on finding regularity within complexity. High pattern_search indicates the listener is actively engaged in structural parsing.

2. **Context Assessment (P1)**: The cognitive framing evaluation happening in the present moment. Captures the listener's ongoing assessment of "what kind of music is this?" and "how should I interpret this complexity?" When framing is effective (aesthetic context provided), this signal is high, facilitating meaning extraction from spectral complexity. Maps to mPFC and ToM network activation during artistic music evaluation.

3. **Aesthetic Evaluation (P2)**: The moment-to-moment aesthetic judgment. This is the primary P-layer output summarizing the current appreciation state. Derived from the appreciation composite (f04), it represents the integrated aesthetic response after accounting for complexity tolerance, familiarity, and framing. Maps to NAc uncertainty encoding and cortical pleasure mediation.

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (4, 3, 0, 2) | sensory_pleasantness value H3 L2 | Current consonance at 100ms |
| (0, 3, 0, 2) | roughness value H3 L2 | Current dissonance at 100ms |
| (14, 8, 1, 0) | tonalness mean H8 L0 | Mean tonalness at 500ms |
| (41, 8, 0, 0) | x_l5l7[0] value H8 L0 | Coupling value at 500ms |
| (41, 16, 1, 0) | x_l5l7[0] mean H16 L0 | Mean coupling over 1s |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | P0: dissonance level for pattern search difficulty |
| [4] | sensory_pleasantness | P2: consonance for aesthetic baseline |
| [14] | tonalness | P1: tonal context quality for framing assessment |
| [18:21] | tristimulus1-3 | P1: harmonic structure cues for context |
| [41:49] | x_l5l7 (8D) | P0/P2: coupling signal for pattern detection |

---

## Scientific Foundation

- **Bravo et al. 2017**: Right Heschl's gyrus heightened response under uncertainty; sensory cortex gain increase for uncertain stimuli (fMRI, N=12+75, p<0.05 cluster-corrected)
- **Gold et al. 2023**: R STG + ventral striatum reflect liking; VS integrates uncertainty x surprise x liking (fMRI, N=24)
- **Huang et al. 2016**: Artistic music activates mPFC + PCC/PC + arMFC + TPJ; popular music activates putamen (fMRI, N=18, p<0.05 FWE)
- **Sarasso et al. 2019**: Aesthetic appreciation enhances N1/P2 (attention) and N2/P3 (motor inhibition); appreciated intervals produce slower RTs (EEG, N=22+22, eta2_p=0.685)
- **Cheung et al. 2019**: NAc beta=0.242 (p=0.002) reflects uncertainty; amygdala/hippocampus reflect interaction (fMRI, N=39+40)
- **Teixeira Borges et al. 2019**: 1/f scaling in temporal cortex predicts pleasure; music-induced gamma scaling correlates with pleasure (EEG+ECG, N=28, r=0.37-0.42)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/maa/cognitive_present.py`
