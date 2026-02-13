"""DependencyDAG -- 3-stage execution DAG for R3 spectral groups.

Hardcodes the dependency structure between the 11 R3 spectral groups (A-K).
Groups are assigned to one of three stages based on their inter-group
dependencies:

    Stage 1 (7 groups, no deps):
        A(consonance), B(energy), C(timbre), D(change),
        F(pitch_chroma), J(timbre_extended), K(modulation)

    Stage 2 (3 groups):
        E(interactions)   <- {consonance, energy, timbre, change}
        G(rhythm_groove)  <- {energy}
        H(harmony)        <- {pitch_chroma}

    Stage 3 (1 group):
        I(information)    <- {pitch_chroma, rhythm_groove, harmony}

Groups within the same stage can theoretically execute in parallel (e.g., on
separate CUDA streams). Synchronisation barriers are inserted between stages.

See Also:
    Docs/R3/Pipeline/DependencyDAG.md
    Docs/R3/R3-SPECTRAL-ARCHITECTURE.md  Section 9
"""
from __future__ import annotations

from typing import Dict, FrozenSet, Tuple

from ..constants.group_boundaries import R3_GROUP_BOUNDARIES

# ---------------------------------------------------------------------------
# Internal type aliases
# ---------------------------------------------------------------------------
_DepsMap = Dict[str, FrozenSet[str]]

# ---------------------------------------------------------------------------
# Canonical group names (derived from R3_GROUP_BOUNDARIES)
# ---------------------------------------------------------------------------
# The DAG uses the lowercase canonical names that match the
# BaseSpectralGroup.GROUP_NAME convention used throughout the codebase.
_GROUP_CANONICAL_NAMES: Tuple[str, ...] = (
    "consonance",         # A
    "energy",             # B
    "timbre",             # C
    "change",             # D
    "interactions",       # E
    "pitch_chroma",       # F
    "rhythm_groove",      # G
    "harmony",            # H
    "information",        # I
    "timbre_extended",    # J
    "modulation",         # K
)

# ---------------------------------------------------------------------------
# Mapping: letter -> canonical name (and reverse)
# ---------------------------------------------------------------------------
_LETTER_TO_NAME: Dict[str, str] = {
    boundary.letter: name
    for boundary, name in zip(R3_GROUP_BOUNDARIES, _GROUP_CANONICAL_NAMES)
}
_NAME_TO_LETTER: Dict[str, str] = {v: k for k, v in _LETTER_TO_NAME.items()}


class DependencyDAG:
    """Immutable 3-stage dependency DAG for R3 spectral feature groups.

    The DAG encodes which groups depend on which other groups' outputs.
    Stage 1 groups depend only on the mel spectrogram.  Stage 2 and 3 groups
    depend on outputs from earlier-stage groups.

    Attributes:
        STAGE_GROUPS: Mapping from stage number (1, 2, 3) to a tuple of
            canonical group names computed in that stage.
        DEPENDENCIES: Mapping from canonical group name to a frozenset of
            canonical names of groups it depends on.  Stage 1 groups map to
            an empty frozenset.
    """

    # ------------------------------------------------------------------
    # Stage -> groups (hardcoded from docs)
    # ------------------------------------------------------------------
    STAGE_GROUPS: Dict[int, Tuple[str, ...]] = {
        1: (
            "consonance",
            "energy",
            "timbre",
            "change",
            "pitch_chroma",
            "timbre_extended",
            "modulation",
        ),
        2: (
            "interactions",
            "rhythm_groove",
            "harmony",
        ),
        3: (
            "information",
        ),
    }

    # ------------------------------------------------------------------
    # Group -> dependencies (hardcoded from docs)
    # ------------------------------------------------------------------
    DEPENDENCIES: _DepsMap = {
        # Stage 1 -- no dependencies (mel only)
        "consonance":      frozenset(),
        "energy":          frozenset(),
        "timbre":          frozenset(),
        "change":          frozenset(),
        "pitch_chroma":    frozenset(),
        "timbre_extended": frozenset(),
        "modulation":      frozenset(),
        # Stage 2
        "interactions":    frozenset({"consonance", "energy", "timbre", "change"}),
        "rhythm_groove":   frozenset({"energy"}),
        "harmony":         frozenset({"pitch_chroma"}),
        # Stage 3
        "information":     frozenset({"pitch_chroma", "rhythm_groove", "harmony"}),
    }

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def stages(self) -> Tuple[int, ...]:
        """Return the ordered stage numbers ``(1, 2, 3)``."""
        return (1, 2, 3)

    def get_stage(self, n: int) -> Tuple[str, ...]:
        """Return the canonical group names assigned to stage *n*.

        Args:
            n: Stage number (1, 2, or 3).

        Returns:
            Tuple of canonical group names for that stage.

        Raises:
            ValueError: If *n* is not a valid stage number.
        """
        if n not in self.STAGE_GROUPS:
            raise ValueError(
                f"Invalid stage number {n!r}; must be one of {sorted(self.STAGE_GROUPS)}"
            )
        return self.STAGE_GROUPS[n]

    def get_dependencies(self, group_name: str) -> Tuple[str, ...]:
        """Return the dependency group names for *group_name*.

        Args:
            group_name: Canonical group name (e.g. ``"interactions"``).

        Returns:
            Tuple of canonical group names that *group_name* depends on.
            Empty tuple for Stage 1 groups.

        Raises:
            KeyError: If *group_name* is not a known group.
        """
        if group_name not in self.DEPENDENCIES:
            raise KeyError(
                f"Unknown group name {group_name!r}; "
                f"known groups: {sorted(self.DEPENDENCIES)}"
            )
        return tuple(sorted(self.DEPENDENCIES[group_name]))

    def get_stage_for_group(self, group_name: str) -> int:
        """Return the stage number for *group_name*.

        Args:
            group_name: Canonical group name.

        Returns:
            Stage number (1, 2, or 3).

        Raises:
            KeyError: If *group_name* is not in any stage.
        """
        for stage_num, groups in self.STAGE_GROUPS.items():
            if group_name in groups:
                return stage_num
        raise KeyError(
            f"Unknown group name {group_name!r}; "
            f"not found in any stage"
        )

    def validate(self) -> None:
        """Validate the DAG for consistency.

        Checks:
            1. All 11 groups are covered across the three stages.
            2. All dependency targets exist as known groups.
            3. No group depends on a group in the same or later stage
               (acyclicity by construction).

        Raises:
            ValueError: If any validation check fails.
        """
        errors: list[str] = []

        # 1. All 11 groups covered
        all_groups_in_stages: set[str] = set()
        for groups in self.STAGE_GROUPS.values():
            all_groups_in_stages.update(groups)

        expected = set(_GROUP_CANONICAL_NAMES)
        if all_groups_in_stages != expected:
            missing = expected - all_groups_in_stages
            extra = all_groups_in_stages - expected
            if missing:
                errors.append(f"Groups missing from stages: {sorted(missing)}")
            if extra:
                errors.append(f"Unexpected groups in stages: {sorted(extra)}")

        # Also check that DEPENDENCIES covers all groups
        dep_groups = set(self.DEPENDENCIES.keys())
        if dep_groups != expected:
            missing_dep = expected - dep_groups
            extra_dep = dep_groups - expected
            if missing_dep:
                errors.append(
                    f"Groups missing from DEPENDENCIES: {sorted(missing_dep)}"
                )
            if extra_dep:
                errors.append(
                    f"Unexpected groups in DEPENDENCIES: {sorted(extra_dep)}"
                )

        # 2. All dependency targets exist
        for group_name, deps in self.DEPENDENCIES.items():
            for dep in deps:
                if dep not in expected:
                    errors.append(
                        f"Group {group_name!r} depends on unknown group {dep!r}"
                    )

        # 3. No group depends on a group in the same or later stage
        #    (ensures acyclicity)
        for group_name, deps in self.DEPENDENCIES.items():
            if group_name not in all_groups_in_stages:
                continue  # Already flagged above
            group_stage = self.get_stage_for_group(group_name)
            for dep in deps:
                if dep not in all_groups_in_stages:
                    continue  # Already flagged above
                dep_stage = self.get_stage_for_group(dep)
                if dep_stage >= group_stage:
                    errors.append(
                        f"Cycle risk: {group_name!r} (stage {group_stage}) "
                        f"depends on {dep!r} (stage {dep_stage})"
                    )

        if errors:
            raise ValueError(
                "DependencyDAG validation failed:\n  "
                + "\n  ".join(errors)
            )

    # ------------------------------------------------------------------
    # Repr
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        stage_summary = ", ".join(
            f"S{s}={len(g)}" for s, g in sorted(self.STAGE_GROUPS.items())
        )
        return f"DependencyDAG({stage_summary}, groups=11)"
