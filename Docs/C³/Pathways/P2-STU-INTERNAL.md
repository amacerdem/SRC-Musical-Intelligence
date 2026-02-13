# P2: STU Internal — Beat to Motor Sync

| Field | Value |
|-------|-------|
| pathway_id | P2_STU_INTERNAL |
| name | STU internal (beat -> motor sync) |
| source_unit | STU |
| source_model | HMCE (Hierarchical Musical Context Encoding) |
| target_unit | STU |
| target_model | AMSC (Auditory-Motor Synchronisation Circuit) |
| correlation | r=0.70 |
| citation | Grahn & Brett 2007 |
| type | Intra-unit |

## Source Dimensions

| Dimension | Description |
|-----------|-------------|
| beat_tracking | Estimated beat positions and confidence |
| context_depth | Depth of hierarchical temporal context |

## Scientific Evidence

Grahn & Brett (2007) showed that beat perception in auditory cortex (HMCE-like mechanisms) drives motor system entrainment (AMSC-like mechanisms) with correlation r=0.70. fMRI demonstrated SMA, premotor, and basal ganglia activation during beat perception, even without overt movement. This pathway models the auditory-to-motor coupling that underlies beat-synchronised behaviour.

## Routing Mechanism

1. STU computes in Phase 2 (independent pass).
2. HMCE model within STU produces beat_tracking and context_depth outputs.
3. As an intra-unit pathway, routing occurs within STU's internal computation graph.
4. AMSC receives beat tracking signals to drive motor entrainment and synchronisation.

Note: Intra-unit pathways do not affect unit-level execution order. Both HMCE and AMSC are within STU, so model-level ordering is handled internally by the unit.

## Models Reading This Pathway

- **STU / AMSC** — Uses beat tracking to drive motor entrainment and synchronisation.

## Code Reference

`mi_beta/brain/pathways/p2_stu_internal.py`
