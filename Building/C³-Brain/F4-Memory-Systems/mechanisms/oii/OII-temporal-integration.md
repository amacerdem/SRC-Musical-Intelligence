# OII M-Layer — Temporal Integration (2D)

**Layer**: Mathematical / Temporal Integration (M)
**Indices**: [3:5]
**Scope**: internal
**Activation**: clamp / sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 3 | M0:gf_proxy | [0, 1] | Fluid intelligence proxy. gf_proxy = f16 * (1.0 - f17) + f17 * (1.0 - f16). XOR-like: peaks when one mode is high and the other low = efficient complementary activation. Bruzzone et al. 2022: Gf group separation t(55)=11.08, p<1e-7; high Gf = efficient switching between integration/segregation (DTI + MEG N=66/67). |
| 4 | M1:switching_efficiency | [0, 1] | Mode switching efficiency metric. sigma(0.25 * onset_velocity_h14 + 0.25 * entropy_stability_h18). |w| sum = 0.50. Fast complementary transitions = high Gf. Cabral et al. 2022: metastable oscillatory modes, global coupling strength controls mode switching (computational model validated with MEG N=89). |

---

## Design Rationale

1. **Gf Proxy (M0)**: Implements the core insight that high fluid intelligence is NOT high integration OR high segregation alone, but efficient SWITCHING between them. The XOR-like formula (f16 * (1 - f17) + f17 * (1 - f16)) peaks when one mode is dominant and the other suppressed — exactly the complementary activation pattern seen in high-Gf individuals. Both modes simultaneously active or inactive indicates diffuse, inefficient processing.

2. **Switching Efficiency (M1)**: Quantifies how quickly and cleanly the brain transitions between oscillatory modes. Uses onset velocity at H14 (700ms) to capture the rate of gamma burst transitions (mode switch triggers) and entropy stability at H18 (2s) to capture whether the overall pattern maintains coherent structure despite local transitions. Fast onset velocity + stable entropy = clean mode switching. This maps to DLPFC executive control over oscillatory dynamics.

---

## H3 Dependencies (M-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (11, 14, 8, 0) | onset_strength velocity H14 L0 | Mode switching rate over 700ms progression |
| (22, 18, 19, 0) | entropy stability H18 L0 | Pattern stability over 2s phrase |
| (5, 14, 14, 0) | periodicity periodicity H14 L0 | Meta-regularity: regularity of regularity |
| (3, 14, 1, 0) | stumpf_fusion mean H14 L0 | Binding quality over progression |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [11] | onset_strength | M1: mode switch trigger rate |
| [22] | entropy | M1: integration demand for stability assessment |
| [5] | periodicity | M0: oscillatory regularity for Gf computation |
| [3] | stumpf_fusion | M0: binding quality as integration proxy |

---

## Scientific Foundation

- **Bruzzone et al. 2022**: DTI + MEG N=66/67, Gf group separation t(55)=11.08, p<1e-7; high Gf = stronger theta/alpha degree AND higher gamma segregation — complementary activation
- **Cabral et al. 2022**: Computational model validated with MEG N=89, metastable oscillatory modes emerge from delay-coupled oscillators; global coupling controls switching
- **Fries 2015**: Review, CTC framework — phase coherence gates information flow; gamma=local, theta=long-range, alpha=gating
- **Hovsepyan et al. 2020**: Computational model, theta-gamma coupling + predictive coding; oscillatory parsing + prediction synergize

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/oii/temporal_integration.py`
