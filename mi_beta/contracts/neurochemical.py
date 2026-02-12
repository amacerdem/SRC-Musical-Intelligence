"""
NeurochemicalType / NeurochemicalState -- Neurochemical signalling contracts.

The mi_beta brain models neurochemical dynamics at the regional level.
Instead of a single scalar "dopamine", models write and read region-specific
neurochemical state (e.g. dopamine in NAcc vs dopamine in caudate).

NeurochemicalType enumerates the six transmitter systems relevant to musical
cognition.  NeurochemicalState is a lightweight registry that models use to
communicate via write/read semantics within a single compute pass:

    state = NeurochemicalState()
    # SRP model writes reward signals
    state.write(NeurochemicalType.DOPAMINE, "NAcc", da_nacc_tensor)
    state.write(NeurochemicalType.OPIOID, "NAcc_shell", opioid_tensor)
    # AAC model reads them for affect computation
    da = state.read(NeurochemicalType.DOPAMINE, "NAcc")

This avoids hard-wiring model-to-model tensor passing and makes cross-unit
dependencies explicit and auditable.
"""

from __future__ import annotations

from enum import Enum, unique
from typing import Dict, Optional, Tuple

from torch import Tensor


@unique
class NeurochemicalType(Enum):
    """Major neurotransmitter systems involved in musical cognition.

    Members:
        DOPAMINE:       Reward prediction error, incentive salience, anticipation.
                        Regions: VTA, NAcc, caudate (Salimpoor 2011, Ferreri 2019).
        OPIOID:         Hedonic "liking", consummatory pleasure.
                        Regions: NAcc shell, ventral pallidum (Nummenmaa 2025).
        SEROTONIN:      Mood regulation, emotional valence modulation.
                        Regions: Raphe nuclei, PFC (Koelsch 2014).
        NOREPINEPHRINE: Arousal, attentional gating, orienting response.
                        Regions: Locus coeruleus, amygdala (Menon & Levitin 2005).
        GABA:           Inhibitory modulation, timing precision.
                        Regions: Auditory cortex, motor cortex (Grahn & Rowe 2009).
        GLUTAMATE:      Excitatory drive, cortical-subcortical communication.
                        Regions: STG-NAcc pathway (Salimpoor 2013).
    """

    DOPAMINE = "dopamine"
    OPIOID = "opioid"
    SEROTONIN = "serotonin"
    NOREPINEPHRINE = "norepinephrine"
    GABA = "gaba"
    GLUTAMATE = "glutamate"


class NeurochemicalState:
    """Mutable registry for neurochemical signal tensors.

    Models write region-specific neurochemical values during their compute
    pass.  Downstream models (or cross-unit pathways) read those values.
    All tensors are expected to be (B, T) or (B, T, D).

    Thread safety: NOT thread-safe.  Intended for single-pass pipeline use.
    Call reset() between independent pipeline runs.
    """

    def __init__(self) -> None:
        self._store: Dict[Tuple[NeurochemicalType, str], Tensor] = {}

    def write(
        self,
        chemical: NeurochemicalType,
        region: str,
        value: Tensor,
    ) -> None:
        """Write a neurochemical signal for a specific region.

        Args:
            chemical: The neurotransmitter type.
            region:   Target brain region abbreviation (e.g. "NAcc", "caudate").
            value:    Tensor of shape (B, T) or (B, T, D).

        Raises:
            TypeError:  If chemical is not a NeurochemicalType.
            ValueError: If a value has already been written for this key
                        in the current pass (prevents silent overwrites).
        """
        if not isinstance(chemical, NeurochemicalType):
            raise TypeError(
                f"Expected NeurochemicalType, got {type(chemical).__name__}"
            )
        key = (chemical, region)
        if key in self._store:
            raise ValueError(
                f"NeurochemicalState: {chemical.value}@{region} already written. "
                f"Call reset() between pipeline passes."
            )
        self._store[key] = value

    def read(
        self,
        chemical: NeurochemicalType,
        region: str,
    ) -> Optional[Tensor]:
        """Read a neurochemical signal for a specific region.

        Args:
            chemical: The neurotransmitter type.
            region:   Brain region abbreviation.

        Returns:
            The tensor if it was written, or None if not available.
        """
        return self._store.get((chemical, region))

    def reset(self) -> None:
        """Clear all stored signals.  Call between independent pipeline runs."""
        self._store.clear()

    def keys(self) -> list[Tuple[NeurochemicalType, str]]:
        """Return all (chemical, region) keys currently stored."""
        return list(self._store.keys())

    def __len__(self) -> int:
        return len(self._store)

    def __contains__(self, key: Tuple[NeurochemicalType, str]) -> bool:
        return key in self._store

    def __repr__(self) -> str:
        entries = ", ".join(
            f"{c.value}@{r}" for c, r in sorted(self._store.keys(), key=str)
        )
        return f"NeurochemicalState({len(self._store)} signals: [{entries}])"
