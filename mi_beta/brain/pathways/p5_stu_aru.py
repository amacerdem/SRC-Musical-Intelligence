"""
P5: STU -> ARU -- Tempo encoding feeds emotional valence.

Scientific basis:
    Juslin & Vastfjall (2008) identified rhythmic entrainment as one of
    six mechanisms for musical emotion induction.  Tempo and beat strength
    signals from the sensorimotor timing unit modulate arousal and
    emotional valence in the affective resonance unit at r=0.60.

Source: STU / HMCE (Hierarchical Musical Context Encoding)
    - tempo_encoding: Current tempo estimate and confidence

Target: ARU / VMM (Valence Modulation Model)
    - Uses tempo signals to modulate emotional arousal and valence
"""

from __future__ import annotations

from mi_beta.contracts import CrossUnitPathway

P5_STU_ARU = CrossUnitPathway(
    pathway_id="P5_STU_ARU",
    name="STU -> ARU (tempo -> emotion)",
    source_unit="STU",
    source_model="HMCE",
    source_dims=("tempo_encoding",),
    target_unit="ARU",
    target_model="VMM",
    correlation="r=0.60",
    citation="Juslin & Vastfjall 2008",
)
