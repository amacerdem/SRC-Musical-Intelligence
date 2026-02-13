# P3: IMU -> ARU — Memory to Affect

| Field | Value |
|-------|-------|
| pathway_id | P3_IMU_ARU |
| name | IMU -> ARU (memory -> affect) |
| source_unit | IMU |
| source_model | MEAMN (Music-Evoked Autobiographical Memory Network) |
| target_unit | ARU |
| target_model | SRP (Sensory Reward Prediction) |
| correlation | r=0.55 |
| citation | Janata 2009 |
| type | Inter-unit |

## Source Dimensions

| Dimension | Description |
|-----------|-------------|
| memory_state | Current memory retrieval activation level |
| nostalgia_link | Strength of nostalgic association |

## Scientific Evidence

Janata (2009) demonstrated that autobiographical memory activation during music listening correlates with emotional responses at r=0.55. Familiar melodies trigger mPFC-hippocampal memory retrieval that modulates mesolimbic reward processing. The "music and the self" phenomenon — where personally significant music activates medial prefrontal cortex and autobiographical memory networks — provides the basis for this memory-to-affect pathway.

## Routing Mechanism

1. IMU computes in Phase 2 (independent pass).
2. MEAMN model within IMU produces memory_state and nostalgia_link as part of its output tensor.
3. PathwayRunner extracts IMU's full unit output and keys it by `P3_IMU_ARU`.
4. In Phase 4 (dependent pass), ARU's SRP model receives the routed signal as cross-unit input.
5. SRP uses memory-evoked signals to modulate pleasure and reward prediction.

## Models Reading This Pathway

- **ARU / SRP** — Uses memory-evoked signals to modulate pleasure and reward prediction.

## Code Reference

`mi_beta/brain/pathways/p3_imu_aru.py`
