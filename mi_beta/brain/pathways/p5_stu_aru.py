from ...contracts.pathway_spec import CrossUnitPathway

P5_STU_ARU = CrossUnitPathway(
    pathway_id="P5_STU_ARU",
    name="Hierarchical metric cycle to affective conditioned learned association",
    source_unit="STU",
    source_model="HMCE",
    source_dims=(),
    target_unit="ARU",
    target_model="CLAM",
    correlation="r=0.60",
    citation="Juslin & Vastfjall 2008",
)
