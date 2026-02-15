"""Neurochemical: Endogenous Opioids (OPI)

Hedonic evaluation system responsible for the subjective "liking" of music.
Mu-opioid receptors in nucleus accumbens (NAcc) produce consummatory pleasure,
distinct from the dopaminergic "wanting" signal. Peak opioid release coincides
with chills, frisson, and moments of intense musical beauty. Naltrexone
(mu-opioid antagonist) selectively reduces musical pleasure without affecting
motivation to listen, confirming the wanting-liking dissociation.

Channel Index: 2
Key References: Berridge 2003, Blood & Zatorre 2001, Mallik 2017
"""

CHANNEL: int = 2
NAME: str = "OPI"
BASELINE: float = 0.5

# Reference values from literature
REFERENCE_VALUES = {
    "peak_pleasure_chills": (0.85, "Blood & Zatorre 2001, peak during musical chills"),
    "naltrexone_blockade": (0.30, "Mallik 2017, opioid antagonist reduces pleasure"),
    "neutral_listening": (0.40, "baseline during non-preferred music"),
}

# Interactions
INTERACTIONS = {
    "DA": "DA encodes wanting, OPI encodes liking; they converge in NAcc but are dissociable",
    "NE": "Arousal amplifies hedonic response: NE burst potentiates OPI-mediated pleasure",
    "5HT": "Mood baseline modulates hedonic capacity: low 5HT blunts OPI response",
}
