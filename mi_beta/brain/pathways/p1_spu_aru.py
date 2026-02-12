"""
P1: SPU -> ARU -- Consonance signals feed pleasure computation.

Scientific basis:
    Bidelman (2009) demonstrated that brainstem encoding of consonance
    (as measured by frequency-following response clarity) correlates with
    perceived pleasantness at r=0.81.  This pathway routes SPU's consonance
    and pitch processing outputs to ARU's reward/pleasure models.

Source: SPU / BCH (Brainstem Consonance Hierarchy)
    - consonance_signal: Overall consonance level from template matching
    - template_match: Harmonic template similarity
    - neural_pitch: Extracted fundamental frequency estimate

Target: ARU / SRP (Sensory Reward Prediction)
    - Uses consonance as a bottom-up hedonic signal for pleasure computation
"""

from __future__ import annotations

from mi_beta.contracts import CrossUnitPathway

P1_SPU_ARU = CrossUnitPathway(
    pathway_id="P1_SPU_ARU",
    name="SPU -> ARU (consonance -> pleasure)",
    source_unit="SPU",
    source_model="BCH",
    source_dims=("consonance_signal", "template_match", "neural_pitch"),
    target_unit="ARU",
    target_model="SRP",
    correlation="r=0.81",
    citation="Bidelman 2009",
)
