# P4: STU Internal — Context to Prediction

| Field | Value |
|-------|-------|
| pathway_id | P4_STU_INTERNAL |
| name | STU internal (context -> prediction) |
| source_unit | STU |
| source_model | HMCE (Hierarchical Musical Context Encoding) |
| target_unit | STU |
| target_model | AMSC (Auditory-Motor Synchronisation Circuit) |
| correlation | r=0.99 |
| citation | Mischler 2025 |
| type | Intra-unit |

## Source Dimensions

| Dimension | Description |
|-----------|-------------|
| context_prediction | Predicted next temporal event from context model |

## Scientific Evidence

Mischler (2025) showed near-perfect correlation (r=0.99) between predictive context signals from hierarchical encoders and adaptive motor synchronisation models in auditory-motor coupling tasks. This represents the tight internal coupling within the sensorimotor timing circuit — the context model's predictions are almost perfectly reflected in the motor planning system's anticipatory activations.

## Routing Mechanism

1. STU computes in Phase 2 (independent pass).
2. HMCE model within STU produces context_prediction output.
3. As an intra-unit pathway, routing occurs within STU's internal computation graph.
4. AMSC receives prediction signals to pre-activate motor responses, enabling anticipatory synchronisation.

Note: Intra-unit pathways do not affect unit-level execution order. P4 represents a second, distinct signal from HMCE to AMSC (alongside P2), carrying prediction rather than beat-tracking information.

## Models Reading This Pathway

- **STU / AMSC** — Uses prediction signals to pre-activate motor responses.

## Code Reference

`mi_beta/brain/pathways/p4_stu_internal.py`
