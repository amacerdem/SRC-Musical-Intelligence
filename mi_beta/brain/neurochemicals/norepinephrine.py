"""
Norepinephrine (NE) -- Arousal, attentional gating, and orienting response.

The noradrenergic system originates from the locus coeruleus (LC) in the
brainstem and projects to virtually every cortical and subcortical region.
In musical cognition, NE mediates:

    1. Arousal regulation:  NE sets the global arousal level that determines
       the intensity of musical experience.  LC firing rate tracks stimulus
       salience and surprise (Aston-Jones & Cohen 2005).

    2. Attentional gating:  NE modulates the signal-to-noise ratio in
       auditory cortex, enabling selective attention to musically relevant
       events (Menon & Levitin 2005).

    3. Orienting response:  Novel or unexpected musical events trigger NE
       release, producing the autonomic orienting response (pupil dilation,
       skin conductance increase, heart rate deceleration).

    4. Memory consolidation:  NE enhances encoding of emotionally salient
       musical events in hippocampus and amygdala (McGaugh 2004).

NE operates on two timescales:
    - Tonic mode:  Sustained baseline firing, sets alertness level.
    - Phasic mode:  Brief bursts to salient stimuli, drives orienting.

Key papers:
    - Aston-Jones & Cohen 2005: LC-NE function and adaptive gain theory
    - Menon & Levitin 2005: Distributed neural response to music
    - Chanda & Levitin 2013: Neurochemistry of music review
    - McGaugh 2004: NE and emotional memory consolidation
    - Sara 2009: LC-NE system and cognitive function
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


# =====================================================================
# NE REGION DEFINITIONS
# =====================================================================

@dataclass(frozen=True)
class NERegionSpec:
    """Specification of a norepinephrine-relevant brain region.

    Attributes:
        region_key:   Key used in NeurochemicalState.write/read.
        full_name:    Anatomical name.
        role:         Functional role of NE in this region.
        ne_mode:      Primary NE operating mode ("tonic", "phasic", or "both").
        receptor:     Primary adrenergic receptor subtype(s) involved.
        citation:     Primary supporting citation.
    """

    region_key: str
    full_name: str
    role: str
    ne_mode: str
    receptor: str
    citation: str


NE_REGIONS: Tuple[NERegionSpec, ...] = (
    NERegionSpec(
        region_key="locus_coeruleus",
        full_name="Locus Coeruleus",
        role=(
            "Primary NE source nucleus; contains ~50,000 neurons in humans "
            "that project to virtually the entire brain. Tonic firing rate "
            "sets global arousal level; phasic bursts signal salient events. "
            "The LC-NE system implements adaptive gain control, amplifying "
            "processing of task-relevant stimuli (Aston-Jones & Cohen 2005)"
        ),
        ne_mode="both",
        receptor="alpha-2 (autoreceptor), alpha-1/beta-1 (post-synaptic)",
        citation="Aston-Jones & Cohen 2005; Sara 2009",
    ),
    NERegionSpec(
        region_key="amygdala",
        full_name="Amygdala (Basolateral Complex)",
        role=(
            "NE amplifies emotional processing in basolateral amygdala, "
            "enhancing the encoding of emotionally arousing musical events. "
            "Beta-adrenergic activation increases synaptic plasticity for "
            "affectively salient stimuli (McGaugh 2004)"
        ),
        ne_mode="phasic",
        receptor="beta-1 (post-synaptic excitatory)",
        citation="McGaugh 2004; Menon & Levitin 2005",
    ),
    NERegionSpec(
        region_key="pfc",
        full_name="Prefrontal Cortex",
        role=(
            "NE optimises PFC function in an inverted-U dose-response "
            "curve: moderate NE enhances working memory and attentional "
            "control; excessive NE (high stress) impairs PFC function. "
            "Alpha-2A receptors strengthen PFC network connectivity for "
            "sustained attention to musical structure (Arnsten 2011)"
        ),
        ne_mode="tonic",
        receptor="alpha-2A (strengthens PFC), alpha-1 (weakens at high NE)",
        citation="Arnsten 2011; Menon & Levitin 2005",
    ),
)
"""All norepinephrine-relevant regions in the arousal/attention circuit."""


# =====================================================================
# AROUSAL / ATTENTION ROLE
# =====================================================================

AROUSAL_ATTENTION_DESCRIPTION: str = (
    "Norepinephrine is the brain's primary arousal and attentional gating "
    "system for musical cognition. The LC-NE system operates in two modes:\n"
    "\n"
    "  TONIC mode (sustained baseline):\n"
    "    - Sets global alertness and arousal level\n"
    "    - High tonic NE -> broad, exploratory attention\n"
    "    - Low tonic NE -> focused, exploitative attention\n"
    "    - Musical context: background arousal during listening\n"
    "\n"
    "  PHASIC mode (event-triggered bursts):\n"
    "    - Triggered by novel, unexpected, or salient musical events\n"
    "    - Produces autonomic orienting response (pupil dilation, SCR)\n"
    "    - Enhances signal-to-noise ratio in auditory cortex\n"
    "    - Musical context: sudden dynamic changes, unexpected harmonies,\n"
    "      timbral surprises, rhythmic violations\n"
    "\n"
    "Evidence: Aston-Jones & Cohen 2005 (adaptive gain theory); "
    "Menon & Levitin 2005 (distributed music response); "
    "Chanda & Levitin 2013 (NE in music neurochemistry review)."
)

# =====================================================================
# NE-DA INTERACTION
# =====================================================================
# NE and DA interact in the reward circuit:
#   - LC-NE phasic bursts can trigger VTA-DA phasic responses
#   - NE modulates DA release in NAcc via alpha-1 receptors
#   - Arousal (NE) gates reward sensitivity (DA)
#   - High arousal + positive prediction error = amplified reward

NE_DA_INTERACTION: str = (
    "NE and DA systems interact for musical reward processing: "
    "LC phasic bursts to salient events can trigger downstream VTA "
    "DA phasic responses (Devoto & Flore 2006). NE also modulates "
    "DA release in NAcc via alpha-1 receptors, meaning arousal state "
    "(NE) gates reward sensitivity (DA). During music: unexpected "
    "events -> NE phasic burst -> enhanced DA RPE signal -> amplified "
    "pleasure if the surprise resolves positively."
)


__all__ = [
    "NERegionSpec",
    "NE_REGIONS",
    "AROUSAL_ATTENTION_DESCRIPTION",
    "NE_DA_INTERACTION",
]
