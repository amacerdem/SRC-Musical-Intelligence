"""Macro band -- H16-H23 (1 s to 25 s).

The most functionally important band for higher musical cognition.
Covers measure-level through section-level timescales where musical
form, harmonic progressions, memory encoding, and predictive coding
operate.  Contains the highest mechanism density by count (7 distinct
mechanisms) and the largest share of estimated H3 tuples.

Source of truth
---------------
- Docs/H3/Bands/Macro/00-INDEX.md
- Docs/H3/Bands/Macro/H16-H17-Measure.md
- Docs/H3/Bands/Macro/H18-H23-Section.md
"""

from __future__ import annotations

from ..constants.horizons import HORIZON_FRAMES, HORIZON_MS


class MacroBand:
    """Metadata class for the Macro temporal band (H16-H23).

    The Macro band spans 1,000 ms to 25,000 ms (172-4,307 frames).
    This is the primary domain for higher musical cognition: harmonic
    progressions, memory encoding, predictive coding, and form-level
    processing.  Neural correlate: delta-theta oscillations (1-4 Hz).
    """

    NAME: str = "macro"
    HORIZON_RANGE: tuple[int, int] = (16, 24)  # half-open: H16 through H23
    DURATION_RANGE_MS: tuple[float, float] = (1_000.0, 25_000.0)
    FRAME_RANGE: tuple[int, int] = (172, 4_307)
    NEURAL_CORRELATE: str = "Delta-theta oscillations (1-4 Hz)"

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
            16: "1 bar @240 BPM (4/4), half bar @120 BPM -- macro convergence "
                "point; architectural pillar paired with H6; pivot between "
                "beat/phrase processing and section/form processing",
            17: "1 bar @160 BPM (4/4) -- extended measure; interpolation "
                "between H16 and H18; boundary of echoic memory duration",
            18: "1 bar @120 BPM (4/4) -- measure/section entry; most "
                "mechanism-dense section horizon (4 mechanisms); "
                "memory encoding begins; SYN completes its upward span",
            19: "2 bars @160 BPM -- two-bar grouping; antecedent-consequent "
                "phrase pairs; C0P middle horizon for predictive comparison",
            20: "4 bars @120 BPM -- four-bar section; complete musical period; "
                "verse-to-chorus or A-to-B section comparison; "
                "C0P completes its span",
            21: "~8 bars @120 BPM -- eight-bar block; fundamental structural "
                "unit of most Western tonal music; IMU interpolation",
            22: "~16 bars @120 BPM -- extended section (verse, chorus, bridge); "
                "TMH completes macro-band span; listeners form representations "
                "of musical form at this timescale",
            23: "~32 bars @120 BPM -- extended section boundary; "
                "interpolation endpoint before ultra band; captures transitions "
                "between major formal boundaries",
        }

    # ------------------------------------------------------------------
    # Neuroscience basis
    # ------------------------------------------------------------------

    @property
    def neuroscience_basis(self) -> dict[int, str]:
        """Per-horizon neuroscience basis from documentation."""
        return {
            16: "Delta oscillations (~1 Hz) -- measure-level temporal prediction; "
                "hierarchical metrical structure via delta-infra-slow nesting; "
                "attention modulation gating sensory processing; "
                "auditory cortex TRF lower boundary (Norman-Haignere 2022); "
                "hippocampal encoding initiation (Golesorkhi 2021)",
            17: "Echoic memory boundary (~1.5 s); processing increasingly relies "
                "on encoded representations rather than raw sensory traces; "
                "auditory cortex temporal receptive fields transition zone",
            18: "Lateral belt/parabelt TRFs 2-10 s (Norman-Haignere 2022); "
                "hippocampal encoding active at 2-10 s (Golesorkhi 2021); "
                "SYN syntactic processing completes at measure/section scale; "
                "CPD structural boundary detection at longest scale",
            19: "Hippocampal encoding at 2-10 s; predictive coding via "
                "frontal-temporal circuits; C0P comparative processing "
                "across phrase boundaries",
            20: "TMH section-level temporal memory; MEM section-level encoding; "
                "hippocampal encoding 2-10 s window (Golesorkhi 2021); "
                "C0P section comparison for verse-chorus structure",
            21: "Hippocampal encoding extending toward consolidation; "
                "superior temporal sulcus TRFs beginning to engage; "
                "eight-bar period as fundamental Western tonal unit",
            22: "Superior temporal sulcus TRFs 10-30 s (Norman-Haignere 2022); "
                "medial PFC consolidation at 10-25 s (Golesorkhi 2021); "
                "TMH longest macro-band temporal memory window; "
                "MEM hippocampus-to-PFC encoding hierarchy",
            23: "Medial PFC consolidation at 10-25 s; upper boundary of "
                "characterized auditory cortex TRFs; transition from "
                "empirically grounded to speculative temporal processing",
        }

    # ------------------------------------------------------------------
    # Mechanisms
    # ------------------------------------------------------------------

    @property
    def primary_mechanisms(self) -> tuple[str, ...]:
        """Primary mechanisms active in this band."""
        return ("TMH", "SYN", "AED", "CPD", "TPC", "MEM", "C0P")

    @property
    def mechanism_map(self) -> dict[str, tuple[int, ...]]:
        """Mapping of mechanism name to horizon indices where it is active."""
        return {
            "TMH": (16, 18, 20, 22),   # hierarchical temporal memory
            "TPC": (16,),               # longest TPC horizon (from H6, H12)
            "SYN": (16, 18),            # measure-to-section syntax
            "AED": (16,),               # macro-scale event detection (from H6)
            "CPD": (16, 18),            # structural boundary detection (from H9)
            "MEM": (18, 20, 22),        # memory encoding/retrieval
            "C0P": (18, 19, 20),        # comparative processing
        }

    # ------------------------------------------------------------------
    # Demand
    # ------------------------------------------------------------------

    @property
    def demand_share(self) -> float:
        """Approximate percentage of total H3 demand in this band.

        The 00-INDEX.md doc says ~49%, but user spec says ~46%.
        We follow the doc value from 00-INDEX.md.
        """
        return 46.0

    # ------------------------------------------------------------------
    # Morph applicability
    # ------------------------------------------------------------------

    @property
    def reliable_morphs(self) -> dict[str, tuple[str, ...]]:
        """Morph reliability summary across the band.

        All 24 morphs compute without issues at macro timescales
        (172-4,307 frames).  Statistical summary morphs dominate.
        """
        return {
            "preferred": (
                "M1 (mean)",
                "M2 (std)",
                "M18 (trend)",
                "M19 (stability)",
                "M20 (entropy)",
            ),
            "valid_but_less_informative": (
                "M8 (velocity) -- instantaneous dynamics less meaningful at section scale",
                "M9 (acceleration) -- high noise at section scale",
            ),
            "note": (
                "At H22-H23, M8/M9 approach noise floor; rely on M18 (trend) "
                "for directional information and M19 (stability) for consistency"
            ),
        }

    # ------------------------------------------------------------------
    # Repr
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"MacroBand(horizons=H{self.HORIZON_RANGE[0]}-H{self.HORIZON_RANGE[1] - 1}, "
            f"duration={self.DURATION_RANGE_MS[0]}-{self.DURATION_RANGE_MS[1]} ms, "
            f"frames={self.FRAME_RANGE[0]}-{self.FRAME_RANGE[1]})"
        )
