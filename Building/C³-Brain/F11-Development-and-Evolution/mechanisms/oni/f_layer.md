# ONI — Forecast

**Model**: Over-Normalization in Intervention
**Unit**: NDU
**Function**: F11 Development & Evolution
**Tier**: gamma
**Layer**: F — Forecast
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 9 | longterm_outcomes | Developmental trajectory prediction. Estimates long-term developmental outcomes based on the degree of over-normalization and compensatory response. sigma(0.50 * f01_over_normalization + 0.50 * f02_compensatory_response). Whether over-normalization is beneficial or detrimental remains mechanistically unclear. Nayak et al. 2025: rhythm processing links to language outcomes (OR=1.33, p<0.0001); enhanced MMR may predict better speech-language development. Range [0, 1]. |
| 10 | intervention_optimization | Protocol ceiling detection. Predicts the point of diminishing returns for continued intervention, combining ceiling saturation with accumulated dosage. sigma(0.50 * f04_intervention_ceiling + 0.50 * dosage_accumulation). Relevant for clinical optimization of music therapy protocols in NICU settings. Range [0, 1]. |

---

## H3 Demands

| # | R3 idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 33 | 16 | M18 (trend) | L0 (fwd) | Dynamic coupling trend over 1s for trajectory direction |

---

## Computation

The F-layer generates two forward-looking predictions about the consequences and management of over-normalization:

1. **Long-term outcomes** (idx 9): Predicts the developmental trajectory that follows from the observed over-normalization pattern. This is the most clinically significant prediction in the ONI model. If over-normalization reflects genuinely enhanced auditory processing (the compensatory hypothesis), then higher values predict better developmental outcomes. If it reflects delayed inhibitory maturation (Kushnerenko et al. 2013 interpretation), higher values may predict transient enhancement that normalizes later. The model explicitly does not resolve this ambiguity -- it captures the current state and projects forward, leaving interpretation to clinical assessment.

   The coupling trend at 1s (H3 tuple) provides the trajectory direction: positive trends suggest increasing enhancement; negative trends suggest normalization toward full-term baseline.

2. **Intervention optimization** (idx 10): Predicts when continued intervention reaches diminishing returns. Combines the E-layer's ceiling function with the M-layer's dosage accumulation. As both approach saturation, intervention_optimization approaches 1.0, signaling that the protocol has extracted maximal benefit. This prediction is clinically actionable: it could inform decisions about intervention duration and intensity in NICU music therapy protocols.

Both F-layer dimensions are speculative (gamma-tier). The over-normalization finding itself requires independent replication, and the direction of its long-term implications remains debated in the literature. Blasi et al. 2025 provide framework support that music interventions can produce structural and functional neuroplasticity exceeding baseline.

All sigmoid formulas use coefficient sums <= 1.0 (saturation rule).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R3 [33] | x_l4l5[0] | Dynamic coupling for trend direction via H3 |
| H3 | 1 tuple (see above) | Coupling trend over 1s for trajectory estimation |
| E-layer | f01_over_normalization, f02_compensatory_response, f04_intervention_ceiling | Over-normalization magnitude, compensatory response, and ceiling for predictions |
| M-layer | dosage_accumulation | Cumulative exposure for optimization prediction |
