from ...contracts.brain_region import BrainRegion

SUBCORTICAL_REGIONS = (
    BrainRegion(
        name="Ventral Tegmental Area",
        abbreviation="VTA",
        hemisphere="bilateral",
        mni_coords=(0, -16, -8),
        function="Dopaminergic reward prediction and reinforcement learning",
    ),
    BrainRegion(
        name="Nucleus Accumbens",
        abbreviation="NAcc",
        hemisphere="bilateral",
        mni_coords=(9, 9, -8),
        function="Reward anticipation, pleasure, and motivational salience",
    ),
    BrainRegion(
        name="Caudate Nucleus",
        abbreviation="Caudate",
        hemisphere="bilateral",
        mni_coords=(13, 15, 9),
        function="Expectation and anticipation of musical reward",
    ),
    BrainRegion(
        name="Amygdala",
        abbreviation="Amygdala",
        hemisphere="bilateral",
        mni_coords=(24, -1, -17),
        function="Emotional valence detection and fear/tension processing",
    ),
    BrainRegion(
        name="Hippocampus",
        abbreviation="Hippocampus",
        hemisphere="bilateral",
        mni_coords=(25, -21, -11),
        function="Episodic memory encoding and musical context retrieval",
    ),
    BrainRegion(
        name="Putamen",
        abbreviation="Putamen",
        hemisphere="bilateral",
        mni_coords=(24, 3, 3),
        function="Beat perception, motor timing, and rhythm processing",
    ),
    BrainRegion(
        name="Thalamus (Medial Geniculate Body)",
        abbreviation="Thalamus_MGB",
        hemisphere="bilateral",
        mni_coords=(16, -24, -2),
        function="Auditory relay and spectrotemporal gating",
    ),
    BrainRegion(
        name="Hypothalamus",
        abbreviation="Hypothalamus",
        hemisphere="bilateral",
        mni_coords=(0, -3, -10),
        function="Autonomic arousal regulation and homeostatic response",
    ),
    BrainRegion(
        name="Insula",
        abbreviation="Insula",
        hemisphere="bilateral",
        mni_coords=(38, 6, 2),
        function="Interoceptive awareness, embodied feeling, and tension monitoring",
    ),
)
