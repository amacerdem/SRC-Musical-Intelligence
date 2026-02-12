"""
Neurochemical State Management -- Convenience wrapper around NeurochemicalState.

NeurochemicalStateManager extends the low-level NeurochemicalState contract
with convenience methods for the four primary neurochemical systems
modelled in MI-Beta:

    1. Dopamine (DA):       Reward prediction error, anticipation, pleasure.
    2. Endogenous Opioids:  Hedonic "liking", consummatory pleasure.
    3. Serotonin (5-HT):    Mood regulation, emotional valence bias.
    4. Norepinephrine (NE): Arousal, attentional gating, orienting.

Two additional systems (GABA, Glutamate) are defined in NeurochemicalType
but do not yet have dedicated submodules.  They will be added as models
require them.

Usage:
    manager = NeurochemicalStateManager()

    # Write DA signals from reward model
    manager.write_da("caudate", caudate_tensor)
    manager.write_da("nacc", nacc_tensor)

    # Read from downstream model
    da_nacc = manager.read_da("nacc")  # Returns Optional[Tensor]

    # Query what has been written
    print(manager.da_keys)   # ["caudate", "nacc"]
    print(manager.summary)   # Human-readable summary

    # Reset between pipeline passes
    manager.reset()
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from torch import Tensor

from mi_beta.contracts import NeurochemicalState, NeurochemicalType

from .dopamine import (  # noqa: F401
    DA_PHASIC_THRESHOLD,
    DA_REFERENCE_VALUES,
    DA_REGIONS,
    DAReferenceValue,
    DARegionSpec,
    is_phasic,
    is_tonic,
)
from .norepinephrine import (  # noqa: F401
    AROUSAL_ATTENTION_DESCRIPTION,
    NE_DA_INTERACTION,
    NE_REGIONS,
    NERegionSpec,
)
from .opioid import (  # noqa: F401
    HEDONIC_HOTSPOTS,
    OPIOID_REGIONS,
    HedonicHotspot,
    OpioidRegionSpec,
)
from .serotonin import (  # noqa: F401
    MOOD_MODULATION_DESCRIPTION,
    SEROTONIN_DA_INTERACTION,
    SEROTONIN_REGIONS,
    SerotoninRegionSpec,
)


class NeurochemicalStateManager:
    """High-level manager wrapping NeurochemicalState with typed helpers.

    Provides shorthand methods for the four primary neurochemical systems
    so that model code reads naturally:

        manager.write_da("nacc", tensor)    instead of
        state.write(NeurochemicalType.DOPAMINE, "nacc", tensor)

    Also provides query helpers (da_keys, opioid_keys, etc.) and a
    human-readable summary property for debugging.

    Thread safety: NOT thread-safe (same as underlying NeurochemicalState).
    """

    def __init__(self) -> None:
        self._state = NeurochemicalState()

    # ─── Raw state access ────────────────────────────────────────────

    @property
    def state(self) -> NeurochemicalState:
        """Access the underlying NeurochemicalState for advanced usage."""
        return self._state

    # ─── Dopamine (DA) ───────────────────────────────────────────────

    def write_da(self, region: str, value: Tensor) -> None:
        """Write a dopamine signal for a specific region.

        Args:
            region: Brain region key (e.g. "caudate", "nacc", "vta").
            value:  Tensor of shape (B, T) or (B, T, D).
        """
        self._state.write(NeurochemicalType.DOPAMINE, region, value)

    def read_da(self, region: str) -> Optional[Tensor]:
        """Read a dopamine signal for a specific region.

        Returns:
            The tensor if written, or None.
        """
        return self._state.read(NeurochemicalType.DOPAMINE, region)

    @property
    def da_keys(self) -> List[str]:
        """All region keys that have DA signals written."""
        return self._keys_for(NeurochemicalType.DOPAMINE)

    # ─── Opioid ──────────────────────────────────────────────────────

    def write_opioid(self, region: str, value: Tensor) -> None:
        """Write an opioid signal for a specific region.

        Args:
            region: Brain region key (e.g. "nacc_shell", "vp", "parabrachial").
            value:  Tensor of shape (B, T) or (B, T, D).
        """
        self._state.write(NeurochemicalType.OPIOID, region, value)

    def read_opioid(self, region: str) -> Optional[Tensor]:
        """Read an opioid signal for a specific region.

        Returns:
            The tensor if written, or None.
        """
        return self._state.read(NeurochemicalType.OPIOID, region)

    @property
    def opioid_keys(self) -> List[str]:
        """All region keys that have opioid signals written."""
        return self._keys_for(NeurochemicalType.OPIOID)

    # ─── Serotonin (5-HT) ───────────────────────────────────────────

    def write_serotonin(self, region: str, value: Tensor) -> None:
        """Write a serotonin signal for a specific region.

        Args:
            region: Brain region key (e.g. "raphe", "amygdala", "pfc").
            value:  Tensor of shape (B, T) or (B, T, D).
        """
        self._state.write(NeurochemicalType.SEROTONIN, region, value)

    def read_serotonin(self, region: str) -> Optional[Tensor]:
        """Read a serotonin signal for a specific region.

        Returns:
            The tensor if written, or None.
        """
        return self._state.read(NeurochemicalType.SEROTONIN, region)

    @property
    def serotonin_keys(self) -> List[str]:
        """All region keys that have serotonin signals written."""
        return self._keys_for(NeurochemicalType.SEROTONIN)

    # ─── Norepinephrine (NE) ─────────────────────────────────────────

    def write_ne(self, region: str, value: Tensor) -> None:
        """Write a norepinephrine signal for a specific region.

        Args:
            region: Brain region key (e.g. "locus_coeruleus", "amygdala", "pfc").
            value:  Tensor of shape (B, T) or (B, T, D).
        """
        self._state.write(NeurochemicalType.NOREPINEPHRINE, region, value)

    def read_ne(self, region: str) -> Optional[Tensor]:
        """Read a norepinephrine signal for a specific region.

        Returns:
            The tensor if written, or None.
        """
        return self._state.read(NeurochemicalType.NOREPINEPHRINE, region)

    @property
    def ne_keys(self) -> List[str]:
        """All region keys that have NE signals written."""
        return self._keys_for(NeurochemicalType.NOREPINEPHRINE)

    # ─── GABA / Glutamate (pass-through) ─────────────────────────────

    def write_gaba(self, region: str, value: Tensor) -> None:
        """Write a GABA signal for a specific region."""
        self._state.write(NeurochemicalType.GABA, region, value)

    def read_gaba(self, region: str) -> Optional[Tensor]:
        """Read a GABA signal for a specific region."""
        return self._state.read(NeurochemicalType.GABA, region)

    def write_glutamate(self, region: str, value: Tensor) -> None:
        """Write a glutamate signal for a specific region."""
        self._state.write(NeurochemicalType.GLUTAMATE, region, value)

    def read_glutamate(self, region: str) -> Optional[Tensor]:
        """Read a glutamate signal for a specific region."""
        return self._state.read(NeurochemicalType.GLUTAMATE, region)

    # ─── Lifecycle ───────────────────────────────────────────────────

    def reset(self) -> None:
        """Clear all neurochemical signals.  Call between pipeline passes."""
        self._state.reset()

    # ─── Query helpers ───────────────────────────────────────────────

    def _keys_for(self, chemical: NeurochemicalType) -> List[str]:
        """Return all region keys written for a given neurochemical type."""
        return [
            region
            for chem, region in self._state.keys()
            if chem == chemical
        ]

    @property
    def all_signals(self) -> Dict[str, List[str]]:
        """Map from neurochemical name to list of region keys with data.

        Returns:
            Dict like {"dopamine": ["caudate", "nacc"], "opioid": ["nacc_shell"]}.
        """
        result: Dict[str, List[str]] = {}
        for chemical, region in self._state.keys():
            name = chemical.value
            if name not in result:
                result[name] = []
            result[name].append(region)
        return result

    @property
    def summary(self) -> str:
        """Human-readable summary of all stored neurochemical signals."""
        if len(self._state) == 0:
            return "NeurochemicalStateManager(empty)"
        lines = [f"NeurochemicalStateManager({len(self._state)} signals):"]
        for chem_name, regions in sorted(self.all_signals.items()):
            regions_str = ", ".join(sorted(regions))
            lines.append(f"  {chem_name}: [{regions_str}]")
        return "\n".join(lines)

    # ─── Dunder ──────────────────────────────────────────────────────

    def __len__(self) -> int:
        return len(self._state)

    def __repr__(self) -> str:
        return (
            f"NeurochemicalStateManager("
            f"{len(self._state)} signals, "
            f"chemicals={list(self.all_signals.keys())})"
        )


__all__ = [
    # Manager
    "NeurochemicalStateManager",
    # Dopamine
    "DARegionSpec",
    "DA_REGIONS",
    "DA_PHASIC_THRESHOLD",
    "is_tonic",
    "is_phasic",
    "DAReferenceValue",
    "DA_REFERENCE_VALUES",
    # Opioid
    "OpioidRegionSpec",
    "OPIOID_REGIONS",
    "HedonicHotspot",
    "HEDONIC_HOTSPOTS",
    # Serotonin
    "SerotoninRegionSpec",
    "SEROTONIN_REGIONS",
    "MOOD_MODULATION_DESCRIPTION",
    "SEROTONIN_DA_INTERACTION",
    # Norepinephrine
    "NERegionSpec",
    "NE_REGIONS",
    "AROUSAL_ATTENTION_DESCRIPTION",
    "NE_DA_INTERACTION",
]
