# ETAM P-Layer — Cognitive Present (2D)

**Layer**: Present Processing (P)
**Indices**: [6:8]
**Scope**: exported (kernel relay)
**Activation**: sigmoid
**Model**: ETAM (STU-B4, Entrainment Tempo & Attention Modulation, 11D, beta-tier 70-90%)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 6 | P0:envelope_tracking | [0, 1] | Real-time envelope-neural coupling. Attended stream tracking quality — how faithfully the neural response follows the acoustic envelope of the attended stream. Combines attention gain (M0) with early window onset tracking (E0). Pesnot Lerousseau 2021: high-gamma persistent activity reflects envelope tracking quality. |
| 7 | P1:stream_separation | [0, 1] | sigma(0.4*f03 + 0.3*f04 + 0.3*x_dyn_bar). Polyphonic stream separation quality. Integrates late window (E2), instrument asymmetry (E3), and dynamic coupling at bar level. Higher values indicate successful separation of concurrent melodic lines. Mesgarani & Chang 2012: cortical stream separation in polyphonic contexts. |

---

## Design Rationale

1. **Envelope Tracking (P0)**: The present-moment measure of how well the brain is following the attended acoustic stream. This combines the overall attention gain (M0) with onset-driven tracking (E0) — attention must be deployed AND onsets must be detectable for successful envelope tracking. This is the primary output for cortical tracking paradigms.

2. **Stream Separation (P1)**: Measures the quality of polyphonic stream separation in real time. The late window (E2, weight 0.4) provides the structural context, instrument asymmetry (E3, weight 0.3) captures timbre-dependent segregation, and dynamic coupling at bar level (weight 0.3) reflects the temporal coherence of separated streams. This is critical for music with multiple concurrent voices.

---

## Kernel Relay Export

P-layer outputs are the primary relay exports for ETAM:

| Export Field | P-Layer Idx | Kernel Usage |
|-------------|-------------|-------------|
| `envelope_tracking` | P0 [6] | Salience: envelope coupling quality feeds attention state |
| `stream_separation` | P1 [7] | Salience: polyphonic separation quality |

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (33, 16, 0, 2) | x_l4l5 value H16 L2 | P1: dynamic coupling at bar level for stream separation |

P0 integrates M0 + E0 outputs (no new H3 tuples). P1 introduces one new H3 tuple for the bar-level dynamic coupling.

---

## Scientific Foundation

- **Pesnot Lerousseau et al. 2021**: High-gamma persistent activity in auditory cortex reflects envelope tracking quality (iEEG)
- **Mesgarani & Chang 2012**: Cortical representation selectively tracks attended stream in polyphonic scenes (ECoG)
- **Hausfeld et al. 2021**: Attention modulates stream tracking fidelity d=0.60 (fMRI, N=14)
- **Doelling & Poeppel 2015**: Musicians show enhanced envelope tracking during rhythmic entrainment (MEG)

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/etam/cognitive_present.py`
