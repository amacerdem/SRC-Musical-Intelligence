"""Micro band -- H0-H7 (5.8 ms to 250 ms).

Covers the shortest temporal horizons in H3, corresponding to
sensory-level auditory processing.  These horizons capture onset
transients, attack characteristics, and sub-beat temporal structure.

Source of truth
---------------
- Docs/H3/Bands/Micro/00-INDEX.md
- Docs/H3/Bands/Micro/H0-H5-SubBeat.md
- Docs/H3/Bands/Micro/H6-H7-BeatSubdivision.md
"""

from __future__ import annotations

from ..constants.horizons import HORIZON_FRAMES, HORIZON_MS


class MicroBand:
    """Metadata class for the Micro temporal band (H0-H7).

    The Micro band spans 5.8 ms to 250 ms (1-43 frames).  At these
    timescales the auditory system performs feature extraction before
    conscious beat perception begins.  Neural correlate: gamma
    oscillations (30-100 Hz).
    """

    NAME: str = "micro"
    HORIZON_RANGE: tuple[int, int] = (0, 8)  # half-open: H0 through H7
    DURATION_RANGE_MS: tuple[float, float] = (5.8, 250.0)
    FRAME_RANGE: tuple[int, int] = (1, 43)
    NEURAL_CORRELATE: str = "Gamma oscillations (30-100 Hz)"

    # ------------------------------------------------------------------
    # Horizons
    # ------------------------------------------------------------------

    @property
    def horizons(self) -> tuple[int, ...]:
        """Return horizon indices in this band."""
        return tuple(range(*self.HORIZON_RANGE))

    @property
    def horizon_ms(self) -> tuple[float, ...]:
        """Duration in milliseconds for each horizon in this band."""
        return tuple(HORIZON_MS[i] for i in self.horizons)

    @property
    def horizon_frames(self) -> tuple[int, ...]:
        """Frame count for each horizon in this band."""
        return tuple(HORIZON_FRAMES[i] for i in self.horizons)

    # ------------------------------------------------------------------
    # Musical character
    # ------------------------------------------------------------------

    @property
    def musical_character(self) -> dict[int, str]:
        """Per-horizon musical character descriptions from documentation."""
        return {
            0: "Single frame -- instantaneous snapshot, onset detection",
            1: "Double frame -- fine timing, sharpest onset transients",
            2: "Triple frame -- sub-onset grouping, minimum acceleration window",
            3: "Onset window -- earliest auditory scene analysis, attack beginning",
            4: "Attack phase -- percussive instrument attack transient",
            5: "Short transient -- attack-sustain transition, minimum timbre integration",
            6: "16th note @75 BPM / 32nd @150 BPM -- mechanism convergence point, "
               "architectural pivot between sensory and cognitive processing",
            7: "8th note @120 BPM / 16th @60 BPM -- beat subdivision, "
               "common subdivision level in popular music",
        }

    # ------------------------------------------------------------------
    # Neuroscience basis
    # ------------------------------------------------------------------

    @property
    def neuroscience_basis(self) -> dict[int, str]:
        """Per-horizon neuroscience basis from documentation."""
        return {
            0: "Auditory nerve phase-locking; frequency following response (FFR) "
               "at single-frame resolution",
            1: "FFR phase-locking; minimum window for first-difference velocity (M8)",
            2: "FFR phase-locking; minimum window for second-difference acceleration (M9)",
            3: "FFR to cortical onset transition; ASA onset-driven stream segregation "
               "begins; multiple units (SPU, ASU, NDU) first overlap",
            4: "Cortical onset response building; auditory brainstem relay",
            5: "Cortical onset response (N1/P2 complex peaks ~50-100 ms); "
               "minimum integration window for timbre perception",
            6: "Gamma-to-beta transition; pre-attentive grouping via mismatch "
               "negativity (MMN ~150-250 ms); earliest motor cortex response "
               "to rhythmic stimuli; five mechanisms converge (PPC, TPC, BEP, ASA, AED)",
            7: "Beta oscillation emergence; pre-attentive rhythmic grouping; "
               "motor system engagement at beat subdivision timescale",
        }

    # ------------------------------------------------------------------
    # Mechanisms
    # ------------------------------------------------------------------

    @property
    def primary_mechanisms(self) -> tuple[str, ...]:
        """Primary mechanisms active in this band."""
        return ("PPC", "ASA", "TPC", "BEP", "AED")

    @property
    def mechanism_map(self) -> dict[str, tuple[int, ...]]:
        """Mapping of mechanism name to horizon indices where it is active."""
        return {
            "PPC": (0, 3, 6),
            "ASA": (3, 6),
            "TPC": (6,),    # entry point -- extends into meso
            "BEP": (6,),    # entry point -- extends into meso
            "AED": (6,),    # entry point -- extends into macro
        }

    # ------------------------------------------------------------------
    # Demand
    # ------------------------------------------------------------------

    @property
    def demand_share(self) -> float:
        """Approximate percentage of total H3 demand in this band."""
        return 17.0

    # ------------------------------------------------------------------
    # Morph constraints
    # ------------------------------------------------------------------

    @property
    def reliable_morphs(self) -> dict[str, tuple[str, ...]]:
        """Morph reliability summary across the band.

        Keys are reliability categories; values are morph names.
        """
        return {
            "reliable": ("M0 (value)", "M1 (mean)", "M8 (velocity)"),
            "marginal_at_H5_H7": ("M2 (std)", "M4 (max)", "M5 (range)"),
            "unreliable": (
                "M14 (periodicity)",
                "M16 (curvature)",
                "M19 (stability)",
                "M20 (entropy)",
            ),
        }

    # ------------------------------------------------------------------
    # Repr
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"MicroBand(horizons=H{self.HORIZON_RANGE[0]}-H{self.HORIZON_RANGE[1] - 1}, "
            f"duration={self.DURATION_RANGE_MS[0]}-{self.DURATION_RANGE_MS[1]} ms, "
            f"frames={self.FRAME_RANGE[0]}-{self.FRAME_RANGE[1]})"
        )
