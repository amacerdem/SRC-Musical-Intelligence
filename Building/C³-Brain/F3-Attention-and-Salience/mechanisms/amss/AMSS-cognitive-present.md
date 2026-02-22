# AMSS P-Layer — Cognitive Present (2D)

**Layer**: Present Processing (P)
**Indices**: [7:9]
**Scope**: exported (kernel relay)
**Activation**: sigmoid
**Model**: AMSS (STU-B1, Attention-Modulated Stream Segregation, 11D, beta-tier 70-90%)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 7 | P0:attended_stream | [0, 1] | Current attended stream dominance. Attended > unattended tracking strength — the degree to which the attended stream dominates perceptual processing. Mesgarani & Chang 2012: cortical representation tracks attended stream selectively. |
| 8 | P1:competition_state | [0, 1] | Inter-stream competition level. Stream rivalry intensity — how much competing streams fight for attentional resources. Wikman 2025: fMRI shows competition-related activation in IFG and STG. |

---

## Design Rationale

1. **Attended Stream (P0)**: The present-moment summary of which stream dominates perception. Combines stream coherence (M0) with the attention gate (E4) to produce a real-time "how strongly am I tracking the attended stream" signal. High values indicate stable, dominant tracking of one stream. Low values indicate weak or ambiguous stream selection.

2. **Competition State (P1)**: Captures the rivalry between concurrent streams. When multiple streams are well-formed (high segregation depth M1) but attention is divided, competition is high. When one stream clearly dominates (high attended_stream P0, low segregation_depth M1), competition is low. This signal indicates processing load and potential for stream switching.

---

## Kernel Relay Export

P-layer outputs are the primary relay exports for AMSS:

| Export Field | P-Layer Idx | Kernel Usage |
|-------------|-------------|-------------|
| `attended_stream` | P0 [7] | Salience: stream-dependent attention weighting |
| `competition_state` | P1 [8] | Salience: competition-driven arousal signal |

---

## H3 Dependencies (P-Layer)

P-layer integrates M-layer and E-layer outputs. No new H3 tuples are introduced at this layer.

| Tuple | Feature | Purpose |
|-------|---------|---------|
| — | (inherited from M+E layers) | Attended stream combines M0 + E4 |
| — | (inherited from M+E layers) | Competition state combines M1 + P0 |

---

## Scientific Foundation

- **Mesgarani & Chang 2012**: Cortical representation selectively tracks attended speaker (ECoG, N=3)
- **Wikman et al. 2025**: fMRI shows IFG and STG activation during stream competition
- **Hausfeld et al. 2021**: Attention modulates stream tracking strength d=0.60 (fMRI, N=14)
- **Basinski et al. 2025**: ORN reflects segregation cost — competition increases ORN amplitude

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/amss/cognitive_present.py`
