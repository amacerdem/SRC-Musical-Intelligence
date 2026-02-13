from ...contracts.pathway_spec import CrossUnitPathway

P2_STU_INTERNAL = CrossUnitPathway(
    pathway_id="P2_STU_INTERNAL",
    name="Hierarchical metric cycle to onset metric salience within STU",
    source_unit="STU",
    source_model="HMCE",
    source_dims=(),
    target_unit="STU",
    target_model="OMS",
    correlation="r=0.70",
    citation="Grahn & Brett 2007",
)
