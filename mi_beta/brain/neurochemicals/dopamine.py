"""
Dopamine (DA) -- Mesolimbic reward and anticipatory signalling.

Dopamine is THE central neurochemical for musical reward.  Two distinct
DA subsystems operate in parallel during music listening:

    1. Anticipatory DA (caudate/dorsal striatum):
       Released 10-15 seconds BEFORE peak pleasure.  Encodes expected
       future reward based on learned musical expectations.  Correlates
       with "wanting" / motivation (Salimpoor 2011, r=0.71).

    2. Consummatory DA (NAcc/ventral striatum):
       Released AT the moment of peak pleasure.  Encodes experienced
       hedonic value of the musical stimulus.  Correlates with "liking"
       (Salimpoor 2011, r=0.84).

    3. VTA drive:
       Dopaminergic cell bodies in VTA fire in response to
       reward prediction error: DA bursts for better-than-expected
       outcomes, pauses for worse-than-expected (Schultz 1997).

Key papers:
    - Salimpoor et al. 2011: PET [11C]raclopride, DA release during music
    - Ferreri et al. 2019: Causal link via levodopa/risperidone
    - Zatorre & Salimpoor 2013: Review of reward, prediction, DA
    - Berridge 2003: Wanting vs liking dissociation
    - Schultz 1997: Reward prediction error theory
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


# =====================================================================
# DA REGION DEFINITIONS
# =====================================================================

@dataclass(frozen=True)
class DARegionSpec:
    """Specification of a dopamine-relevant brain region.

    Attributes:
        region_key: Key used in NeurochemicalState.write/read (e.g. "caudate").
        full_name:  Anatomical name.
        role:       Functional role of DA in this region.
        pathway:    Mesolimbic / mesocortical / nigrostriatal pathway.
        citation:   Primary supporting citation.
    """

    region_key: str
    full_name: str
    role: str
    pathway: str
    citation: str


DA_REGIONS: Tuple[DARegionSpec, ...] = (
    DARegionSpec(
        region_key="caudate",
        full_name="Caudate Nucleus",
        role=(
            "Anticipatory reward; DA release peaks 10-15s before "
            "consummatory pleasure, encoding expected future reward value"
        ),
        pathway="nigrostriatal / mesolimbic overlap",
        citation="Salimpoor 2011, r=0.71 (caudate BP vs anticipation)",
    ),
    DARegionSpec(
        region_key="nacc",
        full_name="Nucleus Accumbens",
        role=(
            "Consummatory pleasure; DA release at peak hedonic moments "
            "encodes experienced reward magnitude"
        ),
        pathway="mesolimbic",
        citation="Salimpoor 2011, r=0.84 (NAcc BP vs pleasure rating)",
    ),
    DARegionSpec(
        region_key="vta",
        full_name="Ventral Tegmental Area",
        role=(
            "DA cell body source; phasic firing encodes reward prediction "
            "error (RPE) -- bursts for positive surprise, pauses for "
            "negative surprise"
        ),
        pathway="mesolimbic (origin)",
        citation="Schultz 1997; Ferreri 2019 (causal DA manipulation)",
    ),
)
"""All dopamine-relevant regions in the musical reward circuit."""


# =====================================================================
# DA STATE CLASSIFICATION
# =====================================================================

# Threshold for tonic vs phasic DA classification.
# Tonic DA: slow, sustained background level (< threshold).
# Phasic DA: fast, transient bursts (>= threshold).
# Derived from Schultz 1997 RPE framework: phasic DA encodes the
# "surprise" component, tonic DA the "baseline expectation".

DA_PHASIC_THRESHOLD: float = 0.6
"""Value above which DA is classified as phasic (burst).
Below this threshold, DA is considered tonic (background).
Based on normalised [0,1] scale where 0.5 = expected reward level."""


def is_tonic(value: float) -> bool:
    """Classify a DA signal value as tonic (sustained baseline).

    Tonic DA represents the slow, background dopaminergic tone that
    encodes average expected reward in the current musical context.
    It modulates sensitivity to phasic bursts (Niv 2007).

    Args:
        value: Normalised DA signal in [0, 1].

    Returns:
        True if the value is below the phasic threshold.
    """
    return value < DA_PHASIC_THRESHOLD


def is_phasic(value: float) -> bool:
    """Classify a DA signal value as phasic (transient burst).

    Phasic DA represents fast, event-locked dopaminergic bursts
    that encode reward prediction error -- the difference between
    received and expected reward (Schultz 1997).

    Args:
        value: Normalised DA signal in [0, 1].

    Returns:
        True if the value is at or above the phasic threshold.
    """
    return value >= DA_PHASIC_THRESHOLD


# =====================================================================
# DA REFERENCE VALUES FROM LITERATURE
# =====================================================================

@dataclass(frozen=True)
class DAReferenceValue:
    """A reference DA measurement from published research.

    These anchors allow calibration of the deterministic DA model:
    computed DA values should reproduce the relative ordering and
    approximate magnitude of empirical observations.

    Attributes:
        description:  What was measured and when.
        region:       Brain region (matches DA_REGIONS region_key).
        value:        Normalised reference value [0, 1].
        original:     Original metric from the paper.
        citation:     Source paper.
    """

    description: str
    region: str
    value: float
    original: str
    citation: str


DA_REFERENCE_VALUES: Tuple[DAReferenceValue, ...] = (
    # --- Salimpoor et al. 2011 (PET [11C]raclopride) ---
    DAReferenceValue(
        description="Peak anticipatory DA during chill-inducing music",
        region="caudate",
        value=0.78,
        original="BP_ND decrease 5.7% vs neutral (p<0.003)",
        citation="Salimpoor 2011",
    ),
    DAReferenceValue(
        description="Peak consummatory DA at chill moment",
        region="nacc",
        value=0.88,
        original="BP_ND decrease 8.4% vs neutral (p<0.001)",
        citation="Salimpoor 2011",
    ),
    DAReferenceValue(
        description="DA during neutral (non-preferred) music",
        region="nacc",
        value=0.35,
        original="Baseline BP_ND (no significant change)",
        citation="Salimpoor 2011",
    ),
    # --- Ferreri et al. 2019 (pharmacological manipulation) ---
    DAReferenceValue(
        description="DA enhancement (levodopa) increases pleasure rating",
        region="nacc",
        value=0.92,
        original="Pleasure rating +14.7% vs placebo (p=0.017)",
        citation="Ferreri 2019",
    ),
    DAReferenceValue(
        description="DA blockade (risperidone) decreases pleasure",
        region="nacc",
        value=0.28,
        original="Pleasure rating -10.2% vs placebo (p=0.033)",
        citation="Ferreri 2019",
    ),
    # --- Zatorre & Salimpoor 2013 (review) ---
    DAReferenceValue(
        description="Anticipatory caudate response during familiar excerpt",
        region="caudate",
        value=0.70,
        original="Temporal dissociation: caudate peaks before NAcc",
        citation="Zatorre & Salimpoor 2013",
    ),
)
"""Reference DA values from empirical studies for model calibration."""


__all__ = [
    "DARegionSpec",
    "DA_REGIONS",
    "DA_PHASIC_THRESHOLD",
    "is_tonic",
    "is_phasic",
    "DAReferenceValue",
    "DA_REFERENCE_VALUES",
]
