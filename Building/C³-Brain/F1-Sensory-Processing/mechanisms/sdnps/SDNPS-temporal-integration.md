# SDNPS M-Layer — Temporal Integration (1D)

**Layer**: Memory (M)
**Indices**: [3:4]
**Scope**: internal
**Activation**: none (raw product)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 3 | M0:nps_stimulus_function | [0, 1] | NPS validity as function of spectral complexity. E0 * E1 = NPS_value * stimulus_dependency. Maps the r=0.34 (synth) → 0.24 (sax) → -0.10 (voice) degradation curve. |

---

## Design Rationale

Single composite function — the product of NPS magnitude (E0) and stimulus dependency (E1):

1. **NPS Stimulus Function (M0)**: When the stimulus is simple (E1 high), NPS validity is preserved (M0 ≈ E0). When the stimulus is complex (E1 low), M0 collapses regardless of E0. This is the core finding of Cousineau 2015: brainstem pitch salience is a valid consonance predictor ONLY for spectrally simple stimuli.

No sigmoid — the raw product naturally stays in [0, 1] since both inputs are sigmoid outputs.

---

## H3 Dependencies

None. M-layer uses only E-layer outputs.

---

## Range Analysis

- M0 = sigmoid([0,1]) × sigmoid([0,1]) → [0, 1]
- In practice: ~[0.25, 0.50] (product of two sigmoids)

No clamping needed; output is naturally bounded.

---

## Scientific Foundation

- **Cousineau 2015**: NPS validity is stimulus-dependent (r=0.34 synth, 0.24 sax, -0.10 voice)
- **Bidelman & Heinz 2011**: AN pitch salience best predictor of consonance hierarchy

## Implementation

File: `Musical_Intelligence/brain/functions/f1/mechanisms/sdnps/temporal_integration.py`
