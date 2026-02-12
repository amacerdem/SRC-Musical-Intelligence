"""
P4: STU internal -- Context prediction feeds motor planning.

Scientific basis:
    Mischler (2025) showed near-perfect correlation (r=0.99) between
    predictive context signals from hierarchical encoders and adaptive
    motor synchronization models in auditory-motor coupling tasks.
    This represents the tight internal coupling within the sensorimotor
    timing circuit.

Source: STU / HMCE (Hierarchical Musical Context Encoding)
    - context_prediction: Predicted next temporal event from context model

Target: STU / AMSC (Auditory-Motor Synchronization Circuit)
    - Uses prediction signals to pre-activate motor responses
"""

from __future__ import annotations

from mi_beta.contracts import CrossUnitPathway

P4_STU_INTERNAL = CrossUnitPathway(
    pathway_id="P4_STU_INTERNAL",
    name="STU internal (context -> prediction)",
    source_unit="STU",
    source_model="HMCE",
    source_dims=("context_prediction",),
    target_unit="STU",
    target_model="AMSC",
    correlation="r=0.99",
    citation="Mischler 2025",
)
