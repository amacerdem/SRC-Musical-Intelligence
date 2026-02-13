from ...contracts.brain_region import BrainRegion

BRAINSTEM_REGIONS = (
    BrainRegion(
        name="Inferior Colliculus",
        abbreviation="IC",
        hemisphere="bilateral",
        mni_coords=(0, -32, -8),
        function="Spectrotemporal integration and pitch periodicity encoding",
    ),
    BrainRegion(
        name="Auditory Nerve",
        abbreviation="AN",
        hemisphere="bilateral",
        mni_coords=(0, -40, -45),
        function="Peripheral transduction and frequency-place coding",
    ),
    BrainRegion(
        name="Cochlear Nucleus",
        abbreviation="CN",
        hemisphere="bilateral",
        mni_coords=(10, -38, -40),
        function="Onset detection, spectral notch filtering, and temporal pattern encoding",
    ),
    BrainRegion(
        name="Superior Olivary Complex",
        abbreviation="SOC",
        hemisphere="bilateral",
        mni_coords=(8, -36, -35),
        function="Binaural processing, interaural time and level difference computation",
    ),
    BrainRegion(
        name="Periaqueductal Gray",
        abbreviation="PAG",
        hemisphere="bilateral",
        mni_coords=(0, -30, -6),
        function="Emotional vocalization, chills response, and autonomic arousal",
    ),
)
