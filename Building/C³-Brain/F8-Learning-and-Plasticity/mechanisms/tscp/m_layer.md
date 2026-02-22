# TSCP — Temporal Integration

**Model**: Timbre-Specific Cortical Plasticity
**Unit**: SPU
**Function**: F8 Learning & Plasticity
**Tier**: β
**Layer**: M — Temporal Integration
**Dimensions**: 1D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 3 | enhancement_function | Enhancement selectivity function. Ratio of trained to untrained instrument response computed as the product of trained timbre response and specificity. E(t) = f01 * f02. Captures the core timbre-specific enhancement: high only when both strong trained response AND high specificity are present simultaneously. Pantev 2001: trained instrument >> other instrument >> pure tone hierarchy. |

---

## H³ Demands

This layer has no additional H³ demands beyond those consumed by the E-layer. The enhancement function is computed purely from E-layer outputs.

---

## Computation

The M-layer computes a single mathematical model output that integrates extraction features:

1. **Enhancement function** (idx 3): Multiplicative combination of f01 (trained timbre response) and f02 (timbre specificity). This product ensures that enhancement is high only when both conditions are met: (a) the stimulus strongly activates the trained instrument template, AND (b) the response is selective for that specific timbre. This mirrors the double dissociation found by Pantev et al. 2001 — violinists show enhanced responses to violin tones but not trumpet tones, and vice versa. The multiplicative gating prevents general auditory enhancement from registering as timbre-specific plasticity.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01_trained_timbre_response | Trained instrument activation strength |
| E-layer | f02_timbre_specificity | Selectivity of response to trained timbre |
