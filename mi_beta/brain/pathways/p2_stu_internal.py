"""
P2: STU internal -- Beat tracking feeds motor synchronization.

Scientific basis:
    Grahn & Brett (2007) showed that beat perception in auditory cortex
    (HMCE-like mechanisms) drives motor system entrainment (AMSC-like
    mechanisms) with correlation r=0.70.  This intra-unit pathway routes
    STU's beat tracking and context depth signals to its own motor
    synchronization component.

Source: STU / HMCE (Hierarchical Musical Context Encoding)
    - beat_tracking: Estimated beat positions and confidence
    - context_depth: Depth of hierarchical temporal context

Target: STU / AMSC (Auditory-Motor Synchronization Circuit)
    - Uses beat tracking to drive motor entrainment and synchronization
"""

from __future__ import annotations

from mi_beta.contracts import CrossUnitPathway

P2_STU_INTERNAL = CrossUnitPathway(
    pathway_id="P2_STU_INTERNAL",
    name="STU internal (beat -> motor sync)",
    source_unit="STU",
    source_model="HMCE",
    source_dims=("beat_tracking", "context_depth"),
    target_unit="STU",
    target_model="AMSC",
    correlation="r=0.70",
    citation="Grahn & Brett 2007",
)
