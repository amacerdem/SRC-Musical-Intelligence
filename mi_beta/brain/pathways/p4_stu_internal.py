from ...contracts.pathway_spec import CrossUnitPathway

P4_STU_INTERNAL = CrossUnitPathway(
    pathway_id="P4_STU_INTERNAL",
    name="Hierarchical metric cycle to expressive timing and articulation within STU",
    source_unit="STU",
    source_model="HMCE",
    source_dims=(),
    target_unit="STU",
    target_model="ETAM",
    correlation="r=0.99",
    citation="Mischler 2025",
)
