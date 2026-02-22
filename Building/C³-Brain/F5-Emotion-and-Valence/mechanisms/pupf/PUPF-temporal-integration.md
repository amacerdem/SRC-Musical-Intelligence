# PUPF U+G-Layers — Temporal Integration (5D)

**Layer**: Temporal Integration (U: Uncertainty Components + G: Goldilocks Outputs)
**Indices**: [2:7]
**Scope**: internal (U) + exported (G: kernel relay)
**Activation**: sigmoid (U), tanh remapped (G)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 2 | U0:entropy_H | [0, 1] | Normalized Shannon entropy of harmonic context. High = unpredictable context. H = -sum(p(xi) log p(xi)) / log(n). Pearce 2005: IDyOM entropy tracks expectation. Integrated over H16 (1s) for beat-level uncertainty. |
| 3 | U1:surprise_S | [0, 1] | Prediction error magnitude. S = \|event - E[event]\| / sigma_distribution. Cheung 2019: surprise drives striatal reward (d=3.8-8.53). Combined spectral_flux[21] with H3 velocity morphs. |
| 4 | U2:HS_interaction | [0, 1] | H x S product term. Cheung 2019: this specific interaction drives amygdala + hippocampus activation (d=3.8-4.16). The non-linear coupling that produces the Goldilocks effect. |
| 5 | G0:pleasure_P | [-1, 1] | Goldilocks pleasure function. P(H,S) = alpha(1-H)S + beta*H(1-S) - gamma*H*S - delta(1-H)(1-S). alpha=0.6, beta=0.4, gamma=0.3, delta=0.2. Positive = in Goldilocks zone. Cheung 2019. |
| 6 | G1:goldilocks_zone | [0, 1] | Goldilocks zone indicator. sigma(P - theta), theta=0.3. Binary-ish sweet spot detection. Feeds SRP wanting/liking modulation. Gold 2019: intermediate complexity preferred. |

---

## Design Rationale

1. **Entropy H (U0)**: The temporally integrated uncertainty signal, computed over H16 (1s beat window). Reflects how uncertain the listener's internal model is about upcoming events. High entropy = many equally likely next events = unpredictable context. This forms the horizontal axis of the Goldilocks diagram. Pearce's IDyOM framework provides the computational basis.

2. **Surprise S (U1)**: The temporally contextualized prediction error. Unlike E0 which captures instantaneous surprise, U1 integrates surprise over the half-beat to beat window (H12-H15), providing a stable magnitude estimate. This forms the vertical axis of the Goldilocks diagram.

3. **H x S Interaction (U2)**: The critical non-linear coupling term. Cheung 2019 fMRI showed that neither H nor S alone explains amygdala activation — it is specifically their interaction. This product term captures the information-theoretic sweet spot where uncertainty and surprise combine to produce peak affective responses.

4. **Pleasure P (G0)**: The Goldilocks pleasure function, computed from H and S using Cheung 2019 coefficients. The four-term equation captures: surprising-in-predictable-context pleasure (alpha), expected-in-unpredictable-context pleasure (beta), overwhelming penalty (gamma), and boredom penalty (delta). Range [-1,1] allows negative (aversive) outcomes.

5. **Goldilocks Zone (G1)**: Sigmoid thresholding of P at theta=0.3, producing a soft binary indicator of whether the current H x S position is in the pleasure sweet spot. Exported to SRP for wanting/liking modulation. Gold 2019 behavioral data confirms this inverted-U preference for intermediate complexity.

---

## H3 Dependencies (U+G-Layers)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (22, 16, 20, 0) | distribution_entropy entropy H16 L0 | 1s integrated entropy for H |
| (22, 12, 18, 0) | distribution_entropy trend H12 L0 | Entropy trajectory over 525ms |
| (22, 15, 2, 0) | distribution_entropy std H15 L0 | Entropy variability at 800ms |
| (21, 12, 8, 0) | spectral_flux velocity H12 L0 | Surprise rate at half-beat |
| (21, 15, 8, 0) | spectral_flux velocity H15 L0 | Surprise rate at 800ms |
| (21, 16, 18, 0) | spectral_flux trend H16 L0 | Surprise trajectory over 1s |
| (6, 12, 8, 0) | harmonic_deviation velocity H12 L0 | Harmonic prediction error rate |
| (6, 16, 2, 0) | harmonic_deviation std H16 L0 | Harmonic uncertainty over 1s |
| (4, 16, 0, 0) | sensory_pleasantness value H16 L0 | Hedonic baseline for P computation |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [21] | spectral_flux | U1: surprise signal (S axis) |
| [22] | distribution_entropy | U0: Shannon entropy (H axis) |
| [4] | sensory_pleasantness | G0: hedonic signal for pleasure function |
| [6] | harmonic_deviation | U1: harmonic prediction accuracy |
| [25:33] | x_l0l5 (8D) | U2: energy x consonance surprise coupling |
| [33:41] | x_l4l5 (8D) | U2: dynamics x consonance interaction |

---

## Scientific Foundation

- **Cheung et al. 2019**: H x S interaction drives amygdala, hippocampus, auditory cortex (fMRI 3T, N=39, d=3.8-4.16); P(H,S) Goldilocks function with alpha=0.6, beta=0.4
- **Gold et al. 2019**: IC x entropy quadratic effects; intermediate complexity preferred (behavioral, N=43+27, significant)
- **Gold et al. 2023**: VS reflects musical surprise pleasure; STG-VS coupling increases with pleasure (fMRI, N=24, significant)
- **Pearce 2005**: IDyOM entropy correlates with expectation (computational model)
- **Singer et al. 2023**: Inverted-U for optimal tempo 80-160 BPM (behavioral, N=34, d=0.69)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/pupf/temporal_integration.py`
