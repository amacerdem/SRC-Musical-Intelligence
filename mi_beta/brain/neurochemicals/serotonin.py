"""
Serotonin (5-HT) -- Mood regulation and emotional valence modulation.

The serotonergic system originates from the raphe nuclei in the brainstem
and projects widely to cortical and subcortical targets.  In musical
cognition, 5-HT modulates:

    1. Emotional valence:  Background mood state that colours the
       emotional interpretation of musical stimuli.  Low 5-HT biases
       toward negative valence (sadness), high 5-HT toward positive
       (Koelsch 2014).

    2. Social bonding:  Serotonin mediates pro-social effects of group
       music-making, contributing to feelings of connection and trust
       (Tarr et al. 2014).

    3. Anxiety modulation:  5-HT1A receptor activation in amygdala
       and PFC reduces anxiety, enabling relaxation responses to
       calming music (Chanda & Levitin 2013).

Unlike dopamine, serotonin operates primarily as a slow neuromodulator
(seconds to minutes) rather than encoding discrete events.

Key papers:
    - Koelsch 2014: Serotonin in music-evoked emotion model
    - Chanda & Levitin 2013: Neurochemistry of music review
    - Tarr et al. 2014: Social bonding through music
    - Kreutz et al. 2012: 5-HT changes during choral singing
    - Ferreri et al. 2019: DA/5-HT interaction in musical pleasure
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


# =====================================================================
# 5-HT REGION DEFINITIONS
# =====================================================================

@dataclass(frozen=True)
class SerotoninRegionSpec:
    """Specification of a serotonin-relevant brain region.

    Attributes:
        region_key:  Key used in NeurochemicalState.write/read.
        full_name:   Anatomical name.
        role:        Functional role of 5-HT in this region.
        receptor:    Primary receptor subtype(s) involved.
        timescale:   Temporal dynamics ("slow" = seconds-minutes, "fast" = ms).
        citation:    Primary supporting citation.
    """

    region_key: str
    full_name: str
    role: str
    receptor: str
    timescale: str
    citation: str


SEROTONIN_REGIONS: Tuple[SerotoninRegionSpec, ...] = (
    SerotoninRegionSpec(
        region_key="raphe",
        full_name="Dorsal Raphe Nucleus",
        role=(
            "Primary 5-HT source; provides tonic serotonergic drive "
            "that sets overall emotional valence bias and mood state. "
            "Firing rate modulates sensitivity to musical affect"
        ),
        receptor="5-HT1A (autoreceptor), 5-HT2A (post-synaptic)",
        timescale="slow (tonic modulation, seconds to minutes)",
        citation="Koelsch 2014; Chanda & Levitin 2013",
    ),
    SerotoninRegionSpec(
        region_key="amygdala",
        full_name="Amygdala",
        role=(
            "5-HT modulates amygdala reactivity to emotionally salient "
            "musical stimuli. High 5-HT reduces threat/anxiety response, "
            "enabling nuanced emotional processing of minor mode, "
            "dissonance, and tension"
        ),
        receptor="5-HT1A (inhibitory), 5-HT2A (excitatory)",
        timescale="slow (seconds)",
        citation="Koelsch 2014; Trost 2012",
    ),
    SerotoninRegionSpec(
        region_key="pfc",
        full_name="Prefrontal Cortex",
        role=(
            "5-HT in PFC supports cognitive reappraisal of musical "
            "emotions and top-down regulation of affective state. "
            "Mediates the transition from raw affect to conscious "
            "aesthetic judgement"
        ),
        receptor="5-HT2A (cortical layer V pyramidal cells)",
        timescale="slow (seconds to minutes)",
        citation="Koelsch 2014; Ferreri 2019",
    ),
)
"""All serotonin-relevant regions in the mood modulation circuit."""


# =====================================================================
# MOOD MODULATION ROLE
# =====================================================================
# Serotonin's primary role in musical cognition is as a background
# modulator of emotional processing.  It does NOT encode discrete
# musical events (that is DA's role), but rather sets the tonic
# "emotional colour" through which music is interpreted.

MOOD_MODULATION_DESCRIPTION: str = (
    "Serotonin acts as a slow neuromodulator (seconds to minutes) that "
    "sets the background emotional valence bias during music listening. "
    "Unlike dopamine, which encodes discrete reward prediction errors, "
    "5-HT provides the tonic mood state that determines whether musical "
    "stimuli are interpreted with positive or negative emotional colouring. "
    "Three primary mechanisms:\n"
    "  1. Valence bias: High 5-HT -> positive interpretation (raphe -> PFC)\n"
    "  2. Anxiety reduction: 5-HT1A activation -> reduced amygdala reactivity\n"
    "  3. Social bonding: Group music -> oxytocin/5-HT interaction -> trust\n"
    "\n"
    "Evidence: Koelsch 2014 model; Chanda & Levitin 2013 review; "
    "Kreutz et al. 2012 choral singing increases 5-HT metabolites."
)

# =====================================================================
# INTERACTION WITH DOPAMINE
# =====================================================================
# 5-HT and DA interact bidirectionally in the reward circuit:
#   - 5-HT2C receptors on VTA DA neurons INHIBIT DA release
#   - 5-HT1B receptors on NAcc terminals FACILITATE DA release
#   - Net effect depends on receptor balance and tonic 5-HT level
# This means mood state (5-HT) gates reward sensitivity (DA).

SEROTONIN_DA_INTERACTION: str = (
    "5-HT modulates DA release bidirectionally via receptor subtypes: "
    "5-HT2C on VTA neurons inhibits DA (negative gate), while "
    "5-HT1B on NAcc terminals facilitates DA (positive gate). "
    "Net effect: positive mood (high 5-HT) can either amplify or "
    "dampen musical reward depending on receptor balance. "
    "Ferreri 2019 showed levodopa (DA+) and 5-HT interact for "
    "musical pleasure."
)


__all__ = [
    "SerotoninRegionSpec",
    "SEROTONIN_REGIONS",
    "MOOD_MODULATION_DESCRIPTION",
    "SEROTONIN_DA_INTERACTION",
]
