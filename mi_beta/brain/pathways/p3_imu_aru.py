"""
P3: IMU -> ARU -- Memory signals modulate affective processing.

Scientific basis:
    Janata (2009) demonstrated that autobiographical memory activation
    during music listening correlates with emotional responses at r=0.55.
    Familiar melodies trigger mPFC-hippocampal memory retrieval that
    modulates mesolimbic reward processing.

Source: IMU / MEAMN (Music-Evoked Autobiographical Memory Network)
    - memory_state: Current memory retrieval activation level
    - nostalgia_link: Strength of nostalgic association

Target: ARU / SRP (Sensory Reward Prediction)
    - Uses memory-evoked signals to modulate pleasure and reward prediction
"""

from __future__ import annotations

from mi_beta.contracts import CrossUnitPathway

P3_IMU_ARU = CrossUnitPathway(
    pathway_id="P3_IMU_ARU",
    name="IMU -> ARU (memory -> affect)",
    source_unit="IMU",
    source_model="MEAMN",
    source_dims=("memory_state", "nostalgia_link"),
    target_unit="ARU",
    target_model="SRP",
    correlation="r=0.55",
    citation="Janata 2009",
)
