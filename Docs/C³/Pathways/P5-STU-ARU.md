# P5: STU -> ARU — Tempo to Emotion

| Field | Value |
|-------|-------|
| pathway_id | P5_STU_ARU |
| name | STU -> ARU (tempo -> emotion) |
| source_unit | STU |
| source_model | HMCE (Hierarchical Musical Context Encoding) |
| target_unit | ARU |
| target_model | VMM (Valence Modulation Model) |
| correlation | r=0.60 |
| citation | Juslin & Vastfjall 2008 |
| type | Inter-unit |

## Source Dimensions

| Dimension | Description |
|-----------|-------------|
| tempo_encoding | Current tempo estimate and confidence |

## Scientific Evidence

Juslin & Vastfjall (2008) identified rhythmic entrainment as one of six mechanisms for musical emotion induction. Tempo and beat strength signals from the sensorimotor timing unit modulate arousal and emotional valence at r=0.60. Fast tempo tends to induce higher arousal and more positive valence; slow tempo induces lower arousal and more sombre affect. This pathway encodes the sensorimotor-to-affective link.

## Routing Mechanism

1. STU computes in Phase 2 (independent pass).
2. HMCE model within STU produces tempo_encoding as part of its output tensor.
3. PathwayRunner extracts STU's full unit output and keys it by `P5_STU_ARU`.
4. In Phase 4 (dependent pass), ARU's VMM model receives the routed signal as cross-unit input.
5. VMM uses tempo signals to modulate emotional arousal and valence.

## Models Reading This Pathway

- **ARU / VMM** — Uses tempo signals to modulate emotional arousal and valence.

## Code Reference

`mi_beta/brain/pathways/p5_stu_aru.py`
