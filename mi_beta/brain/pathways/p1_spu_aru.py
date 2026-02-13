from ...contracts.pathway_spec import CrossUnitPathway

P1_SPU_ARU = CrossUnitPathway(
    pathway_id="P1_SPU_ARU",
    name="Spectral pitch to affective reward via brainstem-cortical relay",
    source_unit="SPU",
    source_model="BCH",
    source_dims=(),
    target_unit="ARU",
    target_model="SRP",
    correlation="r=0.81",
    citation="Bidelman 2009",
)
