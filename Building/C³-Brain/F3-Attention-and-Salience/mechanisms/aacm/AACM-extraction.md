# AACM E-Layer — Extraction (3D)

**Layer**: Extraction (E)
**Indices**: [0:3]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:attentional_engage | [0, 1] | Attentional engagement from pleasantness. f16 = sigma(0.35*pleasant_value_100ms + 0.30*(1-roughness_mean_1s)). N1/P2 amplitude proportional to aesthetic appreciation. Sarasso 2019: d=2.008, eta2p=0.685. |
| 1 | E1:motor_inhibition | [0, 1] | Motor inhibition from pleasantness. f17 = sigma(0.35*pleasant_value_100ms). N2/P3 amplitude proportional to appreciation — motor system pauses during liked stimuli. Sarasso 2019: motor inhibition linked to aesthetic response. |
| 2 | E2:savoring_effect | [0, 1] | RT slowing from aesthetic engagement. f18 = sigma(0.35*f16*f17 + 0.35*pleasant_velocity_1s + 0.30*integration_mean_1s). Reaction time slows when liking is high — attention is captured. Foo 2016: RT proportional to preference. |

---

## Design Rationale

1. **Attentional Engage (E0)**: Tracks how strongly attention is captured by aesthetically pleasant stimuli. Uses pleasantness at 100ms (immediate hedonic response) and inverted roughness at 1s (sustained consonance). N1/P2 ERP amplitudes increase when listeners prefer the interval. Primary basis: Sarasso 2019 showing large effect sizes for preference-modulated ERPs.

2. **Motor Inhibition (E1)**: Tracks the motor pause response — when listeners encounter preferred intervals, motor activity is inhibited (N2/P3 complex). Uses pleasantness at 100ms as the primary driver. This reflects an automatic "stop and listen" response to liked stimuli.

3. **Savoring Effect (E2)**: The interaction of attention capture and motor inhibition creates a measurable RT slowing: listeners take longer to respond during preferred stimuli because cognitive resources are absorbed. This is multiplicative (f16*f17), requiring both attention engagement and motor inhibition. Pleasant velocity captures hedonic change; integration captures sustained context.

---

## H3 Dependencies (E-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (3, 3, 0, 2) | pleasant value H3 L2 | Pleasantness at 100ms — immediate hedonic response |
| (0, 16, 1, 2) | roughness mean H16 L2 | Roughness mean at 1s — sustained dissonance level |
| (3, 16, 8, 2) | pleasant velocity H16 L2 | Pleasantness velocity at 1s — hedonic change rate |
| (25, 16, 1, 0) | integration mean H16 L0 | Motor-auditory integration mean at 1s — sustained context |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | E0: consonance-gated attention (inverted) |
| [3] | pleasant | E0, E1, E2: hedonic value for engagement and inhibition |
| [8] | loudness | E2: amplitude context for integration |

---

## Scientific Foundation

- **Sarasso 2019**: N1/P2 proportional to appreciation (EEG, eta2p=0.685, d=2.008)
- **Foo 2016**: RT slowing proportional to aesthetic preference
- **Salimpoor 2011**: Dopamine release correlates with pleasantness (PET, r=0.71)

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/aacm/extraction.py`
