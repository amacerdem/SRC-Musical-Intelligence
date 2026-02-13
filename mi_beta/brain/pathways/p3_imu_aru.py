from ...contracts.pathway_spec import CrossUnitPathway

P3_IMU_ARU = CrossUnitPathway(
    pathway_id="P3_IMU_ARU",
    name="Imagery mental auditory map to affective neural emotional appraisal",
    source_unit="IMU",
    source_model="MEAMN",
    source_dims=(),
    target_unit="ARU",
    target_model="NEMAC",
    correlation="r=0.55",
    citation="Janata 2009",
)
