"""Neurochemical: Dopamine (DA)

Reward prediction error signal with two temporally dissociable subsystems.
Anticipatory DA release in caudate nucleus peaks 10-15 seconds before the
moment of peak pleasure, encoding expectation. Consummatory DA release in
nucleus accumbens (NAcc) peaks at the pleasure moment itself. The ventral
tegmental area (VTA) is the primary source nucleus. Phasic bursts encode
positive prediction errors; dips encode negative prediction errors.

Channel Index: 0
Key References: Schultz 1997, Salimpoor 2011, Ferreri 2019, Berridge 2003
"""

CHANNEL: int = 0
NAME: str = "DA"
BASELINE: float = 0.5

# Phasic threshold: below = tonic/sustained, above = phasic/burst
PHASIC_THRESHOLD: float = 0.6

# Reference values from literature
REFERENCE_VALUES = {
    "peak_anticipatory_caudate": (0.78, "Salimpoor 2011, BP_ND decrease 5.7%"),
    "peak_consummatory_nacc": (0.88, "Salimpoor 2011, BP_ND decrease 8.4%"),
    "neutral_music_nacc": (0.35, "Salimpoor 2011, baseline"),
    "levodopa_enhancement": (0.92, "Ferreri 2019, pleasure +14.7%"),
    "risperidone_blockade": (0.28, "Ferreri 2019, pleasure -10.2%"),
}

# Interactions
INTERACTIONS = {
    "OPI": "Wanting vs liking dissociation: DA encodes wanting, OPI encodes liking; they converge in NAcc",
    "5HT": "Mood gates reward: 5HT2C on VTA inhibits DA release; 5HT1B on NAcc facilitates DA",
    "NE": "Arousal gates reward: NE phasic burst enhances DA reward prediction error signal",
}
