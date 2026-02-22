# CLAM B+C-Layers — Temporal Integration (5D)

**Layer**: Temporal Integration (B: BCI State + C: Control Outputs)
**Indices**: [2:7]
**Scope**: internal (B) + exported (C: kernel relay)
**Activation**: tanh (idx 2-4), tanh (idx 5-6)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 2 | B0:decoded_affect | [-1, 1] | EEG-decoded current affective state. gamma_FC6 power mapped to valence-arousal composite via decoder. Ehrlich 2019: FC6 gamma encodes affect. Integrated over H16 (1s) matching total loop latency. |
| 3 | B1:target_affect | [-1, 1] | Desired target affective state. Set by therapeutic goal or user intent. Held constant or slowly varied over the modulation session. Drives the error computation. |
| 4 | B2:affect_error | [-1, 1] | Error signal e(t) = target - current. Drives the P-control law. Ehrlich 2019: error convergence observed in 3/5 participants. Temporally smoothed over H12 (525ms) for stability. |
| 5 | C0:control_output | [-1, 1] | P-control output. u(t) = Kp * e(t). Kp adapted by state confidence: Kp = Kp_base * (0.5 + 0.5 * confidence). High confidence = full gain, low confidence = half gain. |
| 6 | C1:music_param_delta | [-1, 1] | Generated music parameter change. control_output * sigma(loop_coherence * 3.0). Maps to tempo delta (20 BPM/unit) and mode delta (0.5 major-minor). Gated by loop coherence. |

---

## Design Rationale

1. **Decoded Affect (B0)**: The BCI's estimate of current affective state, decoded from frontal gamma power (FC6 electrode). Uses H16 (1s) integration to match the total loop latency: EEG acquisition (0ms) to feature extraction (100ms) to decode (200ms) to control (400ms) to audio generation (600ms) to brain response (1000ms). Ehrlich 2019 showed FC6 gamma as a reliable affective state proxy.

2. **Target Affect (B1)**: The reference signal for the feedback loop. In therapeutic applications, this is set by the clinician; in adaptive music systems, it could be user-specified or dynamically adjusted. Held as a slowly varying signal (not frame-rate) to allow the loop to converge. Without a target, no meaningful error can be computed.

3. **Affect Error (B2)**: The driving signal of the entire closed-loop system. Computed as target minus decoded state, temporally smoothed over H12 (525ms) to prevent oscillation from noisy EEG. When error converges to zero, modulation has succeeded. Ehrlich 2019 showed convergence in 60% of participants (3/5), indicating individual differences in loop responsiveness.

4. **Control Output (C0)**: The proportional control law output. Kp gain is adapted by decoded state confidence — when the decoder is uncertain (low confidence), gain is halved to prevent erratic control. This conservative strategy prevents the loop from amplifying noise during uncertain states. The tanh activation ensures bounded output.

5. **Music Parameter Delta (C1)**: The actual music generation adjustment, gated by loop coherence. Even if error is large, if the loop is not coherent (no bidirectional causality), adjustments are suppressed. The 20 BPM/unit tempo sensitivity and 0.5 mode sensitivity are from Ehrlich 2019's parameter mapping. This prevents meaningless adjustments when the BCI is not functioning.

---

## H3 Dependencies (B+C-Layers)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (10, 16, 0, 0) | loudness value H16 L0 | 1s integrated arousal for affect decode |
| (10, 12, 18, 0) | loudness trend H12 L0 | Arousal trajectory for error trend |
| (0, 16, 0, 0) | roughness value H16 L0 | 1s valence for affect decode |
| (0, 12, 18, 0) | roughness trend H12 L0 | Valence trajectory for control stability |
| (21, 7, 8, 0) | spectral_flux velocity H7 L0 | Instantaneous feedback signal rate |
| (12, 16, 20, 0) | spectral_centroid entropy H16 L0 | Brightness uncertainty for decoder confidence |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | B0: valence estimation (inverse pleasantness) |
| [8] | velocity_A | B0: arousal dynamics |
| [10] | loudness | B0: energy-level arousal proxy |
| [11] | onset_strength | C1: event density for tempo tracking |
| [12] | spectral_centroid | B0: brightness for cross-modal BCI mapping |
| [25:33] | x_l0l5 (8D) | B0: energy x consonance BCI affect mapping space |

---

## Scientific Foundation

- **Ehrlich et al. 2019**: P-control law u(t) = Kp * e(t); total loop latency ~1000ms; modulation success 3/5 participants (EEG-BCI + music gen, N=11)
- **Ehrlich et al. 2019**: Tempo sensitivity ~20 BPM/unit; mode sensitivity ~0.5 major-minor mapping (EEG-BCI, N=5)
- **Daly et al. 2016**: EEG + acoustic features predict emotion — decoder basis (EEG + music, significant)
- **Sayal et al. 2025**: Music-based neurofeedback systematic review — reward-system coupling critical for loop success (review, N=20+ studies)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/clam/temporal_integration.py`
