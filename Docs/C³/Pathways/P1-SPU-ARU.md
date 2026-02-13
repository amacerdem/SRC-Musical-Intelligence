# P1: SPU -> ARU — Consonance to Pleasure

| Field | Value |
|-------|-------|
| pathway_id | P1_SPU_ARU |
| name | SPU -> ARU (consonance -> pleasure) |
| source_unit | SPU |
| source_model | BCH (Brainstem Consonance Hierarchy) |
| target_unit | ARU |
| target_model | SRP (Sensory Reward Prediction) |
| correlation | r=0.81 |
| citation | Bidelman 2009 |
| type | Inter-unit |

## Source Dimensions

| Dimension | Description |
|-----------|-------------|
| consonance_signal | Overall consonance level from template matching |
| template_match | Harmonic template similarity |
| neural_pitch | Extracted fundamental frequency estimate |

## Scientific Evidence

Bidelman (2009) demonstrated that brainstem encoding of consonance — as measured by frequency-following response clarity — correlates with perceived pleasantness at r=0.81. This establishes a direct bottom-up pathway from subcortical spectral processing to hedonic evaluation.

## Routing Mechanism

1. SPU computes in Phase 2 (independent pass).
2. BCH model within SPU produces consonance_signal, template_match, and neural_pitch as part of its output tensor.
3. PathwayRunner extracts SPU's full unit output and keys it by `P1_SPU_ARU`.
4. In Phase 4 (dependent pass), ARU's SRP model receives the routed signal as cross-unit input.
5. SRP uses consonance as a bottom-up hedonic signal for pleasure computation.

## Models Reading This Pathway

- **ARU / SRP** — Uses consonance as a bottom-up hedonic signal for pleasure computation.

## Code Reference

`mi_beta/brain/pathways/p1_spu_aru.py`
