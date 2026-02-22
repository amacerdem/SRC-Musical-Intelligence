# SDL P-Layer — Cognitive Present (2D)

**Layer**: Present Processing (P)
**Indices**: [5:7]
**Scope**: exported (kernel relay)
**Activation**: mixed (tanh for dynamic lateral, sigmoid for hemispheric engagement)
**Model**: ASU-gamma3, Salience-Dependent Lateralization (9D, gamma-tier 50-70%)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 5 | P0:dynamic_lateral | [-1, 1] | Connectivity-gated lateralization. tanh(0.5*ts_mean_1s). Present-moment hemispheric balance gated by cross-stream connectivity mean. Positive = right hemisphere lead (spectral dominance), negative = left hemisphere lead (temporal dominance). Leipold 2021: N=153 shows stable individual differences in lateralization patterns. |
| 6 | P1:hemispheric_engage | [0, 1] | Hemispheric engagement strength. sigma(0.5*ts_periodicity_1s). How strongly the lateralized network is engaged, irrespective of direction. Beat-connectivity interaction — rhythmic stimuli sustain stronger engagement. Alluri 2012: naturalistic music drives lateralized networks continuously. |

---

## Design Rationale

1. **Dynamic Lateral (P0)**: The present-moment lateralization readout — "which hemisphere is leading processing right now?" Uses cross-stream connectivity mean (x_l4l5) at 1s as the gating signal. The tanh activation preserves signed output: positive values indicate spectral (right-hemisphere) dominance, negative values indicate temporal (left-hemisphere) dominance. Leipold 2021 with N=153 demonstrates stable individual differences in these patterns.

2. **Hemispheric Engagement (P1)**: The magnitude of lateralized processing — "how strongly is the lateralized network active?" Uses cross-stream periodicity at 1s to capture sustained rhythmic engagement. This is independent of direction — both strong rightward and strong leftward lateralization produce high engagement. Alluri 2012 showed naturalistic music continuously drives lateralized networks.

---

## Kernel Relay Export

P-layer outputs are the primary relay exports:

| Export Field | P-Layer Idx | Kernel Usage |
|-------------|-------------|-------------|
| `dynamic_lateral` | P0 [5] | Lateralization direction for processing routing |
| `hemispheric_engage` | P1 [6] | Engagement strength for attention allocation |

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (37, 16, 1, 2) | x_l4l5 mean H16 L2 | Cross-stream connectivity mean at 1s — lateralization gate |
| (37, 16, 17, 2) | x_l4l5 periodicity H16 L2 | Cross-stream periodicity at 1s — engagement (shared with E-layer) |

---

## Scientific Foundation

- **Leipold 2021**: N=153 shows stable individual differences in auditory lateralization patterns
- **Alluri 2012**: Naturalistic music drives lateralized cortical networks continuously (fMRI)
- **Zatorre 2022**: AST model predicts moment-to-moment lateralization shifts

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/sdl/cognitive_present.py` (pending)
