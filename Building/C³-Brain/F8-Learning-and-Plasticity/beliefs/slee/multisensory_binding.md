# multisensory_binding -- Appraisal Belief (SLEE)

**Category**: Appraisal (observe-only)
**Owner**: SLEE (NDU-beta3)

---

## Definition

"Auditory and visual patterns synchronized." Observes the degree of cross-modal binding -- how well auditory and visual statistical patterns are integrated into a unified perceptual representation. High multisensory binding means the listener processes audiovisual regularities as a coherent stream, enabling better detection of cross-modal statistical irregularities. Musical training specifically enhances multisensory (not just unisensory) statistical learning.

---

## Observation Formula

```
# From SLEE E-layer + P-layer:
multisensory_binding = 0.60 * f03_multisensory_integ + 0.40 * cross_modal_binding

# f03 = sigma(0.35 * binding_100ms
#            + 0.35 * mean_binding_1s)
#   binding_100ms = H3[(41, 3, 0, 2)]  -- x_l5l6[0] value at 100ms bidi
#   mean_binding_1s = H3[(41, 16, 1, 2)]  -- x_l5l6[0] mean over 1s bidi
#   Cross-modal binding strength from multi-feature coherence

# cross_modal_binding = current multisensory integration state
#   Real-time assessment of audiovisual pattern coherence
```

No prediction -- observe-only appraisal. The value enhances salience computation by indicating cross-modal pattern coherence.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| SLEE E2 | f03_multisensory_integ [2] | Cross-modal binding strength |
| SLEE P1 | cross_modal_binding [8] | Current multisensory integration |
| H3 | (41, 3, 0, 2) | Cross-modal binding at 100ms |
| H3 | (41, 16, 1, 2) | Mean cross-modal binding over 1s |
| R3 [41:49] | x_l5l7 | Multi-feature coherence coupling |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| F3 Attention | Cross-modal binding enhances salience of coherent patterns |
| statistical_model (Core) | Multisensory integration enriches the statistical model |
| EDNR | Cross-modal binding evidence for network compartmentalization |

---

## Scientific Foundation

- **Paraskevopoulos et al. 2022**: IFG area 47m is primary supramodal hub across all network states -- highest node degree in 5/6 states (MEG/PTE, N=25)
- **Porfyri et al. 2025**: 4-week multisensory training improves audiovisual incongruency detection; unisensory training affects only auditory; F(1,28)=4.635, p=0.042, eta-sq=0.168 (EEG, N=30)
- **Porfyri et al. 2025**: Left MFG, IFS, and insula show greatest effective connectivity reorganization with top-down feedback mechanism after multisensory training

## Implementation

File: `Musical_Intelligence/brain/functions/f8/mechanisms/slee/slee.py` (Phase 5)
