"""Pathway definitions -- 5 cross-unit data dependencies.

3 inter-unit pathways (P1, P3, P5) routed by PathwayRunner.
2 intra-unit pathways (P2, P4) handled within STU.compute().
"""
from __future__ import annotations

from ...contracts.dataclasses import CrossUnitPathway

# ================================================================
# Inter-unit pathways (routed by PathwayRunner)
# ================================================================

P1_SPU_ARU = CrossUnitPathway(
    pathway_id="P1_SPU_ARU",
    name="Consonance to Reward",
    source_unit="SPU",
    source_model="BCH",
    source_dims=("consonance_signal", "template_match", "neural_pitch"),
    target_unit="ARU",
    target_model="SRP",
    correlation="r=0.81",
    citation="Bidelman 2009",
)

P3_IMU_ARU = CrossUnitPathway(
    pathway_id="P3_IMU_ARU",
    name="Memory to Affect",
    source_unit="IMU",
    source_model="MEAMN",
    source_dims=("memory_state", "nostalgia_link"),
    target_unit="ARU",
    target_model="SRP",
    correlation="r=0.55",
    citation="Janata 2009",
)

P5_STU_ARU = CrossUnitPathway(
    pathway_id="P5_STU_ARU",
    name="Tempo to Emotion",
    source_unit="STU",
    source_model="HMCE",
    source_dims=("tempo_encoding",),
    target_unit="ARU",
    target_model="VMM",
    correlation="r=0.60",
    citation="Juslin & Vastfjall 2008",
)

# ================================================================
# Intra-unit pathways (handled within STU)
# ================================================================

P2_STU_INTERNAL = CrossUnitPathway(
    pathway_id="P2_STU_INTERNAL",
    name="Beat to Motor Sync",
    source_unit="STU",
    source_model="HMCE",
    source_dims=("beat_tracking", "context_depth"),
    target_unit="STU",
    target_model="AMSC",
    correlation="r=0.70",
    citation="Grahn & Brett 2007",
)

P4_STU_INTERNAL = CrossUnitPathway(
    pathway_id="P4_STU_INTERNAL",
    name="Context to Prediction",
    source_unit="STU",
    source_model="HMCE",
    source_dims=("context_prediction",),
    target_unit="STU",
    target_model="AMSC",
    correlation="r=0.99",
    citation="Mischler 2025",
)

# ================================================================
# Collections
# ================================================================

INTER_UNIT_PATHWAYS = (P1_SPU_ARU, P3_IMU_ARU, P5_STU_ARU)
INTRA_UNIT_PATHWAYS = (P2_STU_INTERNAL, P4_STU_INTERNAL)
ALL_PATHWAYS = INTER_UNIT_PATHWAYS + INTRA_UNIT_PATHWAYS
