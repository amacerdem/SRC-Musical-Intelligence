"""Meso band -- H8-H15 (300 ms to 800 ms).

Covers beat-period and phrase-level temporal horizons.  This is the core
timescale for musical rhythm perception, where beat entrainment, motor
synchronization, and short-range temporal pattern recognition occur.
All 24 morphs are reliable at meso timescales, making this the most
statistically complete band.

Source of truth
---------------
- Docs/H3/Bands/Meso/00-INDEX.md
- Docs/H3/Bands/Meso/H8-H11-BeatPeriod.md
- Docs/H3/Bands/Meso/H12-H15-Phrase.md
"""

from __future__ import annotations

from ..constants.horizons import HORIZON_FRAMES, HORIZON_MS


class MesoBand:
    """Metadata class for the Meso temporal band (H8-H15).

    The Meso band spans 300 ms to 800 ms (52-138 frames).  This is the
    core timescale for human beat perception and motor entrainment.
    Neural correlate: beta-theta oscillations (4-30 Hz).
    """

    NAME: str = "meso"
    HORIZON_RANGE: tuple[int, int] = (8, 16)  # half-open: H8 through H15
    DURATION_RANGE_MS: tuple[float, float] = (300.0, 800.0)
    FRAME_RANGE: tuple[int, int] = (52, 138)
    NEURAL_CORRELATE: str = "Beta-theta oscillations (4-30 Hz)"

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
            8: "Quarter note @200 BPM -- fast beat period, presto tempi, "
               "fast dance music and double-time passages",
            9: "Quarter note @171 BPM -- primary beat period, center of "
               "comfortable dance tempo range; most mechanism-dense meso horizon",
            10: "Quarter note @150 BPM -- moderate beat period, common tempo "
                "for pop, rock, and uptempo jazz",
            11: "Quarter note @133 BPM -- relaxed beat period, moderate walking "
                "tempo, ballads, and relaxed groove",
            12: "Half note @114 BPM -- phrase entry point, shortest phrase-level "
                "grouping; two-beat motifs, anacrusis-downbeat pairs",
            13: "Half note @100 BPM -- standard phrase, natural breathing/phrasing "
                "interval in vocal music",
            14: "Half note @86 BPM -- extended phrase, slow ballad phrasing "
                "and legato melodic lines",
            15: "Half note @75 BPM -- phrase boundary, bridge between meso and "
                "macro bands; complete two-beat phrases at moderate tempi",
        }

    # ------------------------------------------------------------------
    # Neuroscience basis
    # ------------------------------------------------------------------

    @property
    def neuroscience_basis(self) -> dict[int, str]:
        """Per-horizon neuroscience basis from documentation."""
        return {
            8: "Motor cortex beta desynchronization (ERD) ~200-500 ms before "
               "expected beats; basal ganglia-thalamo-cortical predictive timing; "
               "fastest standard beat period for spontaneous motor synchronization",
            9: "Sensorimotor synchronization at primary beat rate; beat perception "
               "resonance near peak (Large & Palmer 2002); ASA stream segregation "
               "influenced by temporal regularity at beat rate; CPD beat-level "
               "change detection",
            10: "Auditory-motor coupling strongest for tempi near 120-150 BPM; "
                "beat perception resonance peak (Large & Palmer 2002); passive "
                "listening activates motor cortex areas",
            11: "BEP upper meso-band anchor at 133 BPM; basal ganglia lesion "
                "studies show impaired beat perception at these timescales "
                "(Grahn & Brett 2007); robust morph estimates with 78 frames",
            12: "Phrase-level chunking (~0.5-2 s); SYN syntactic processing entry -- "
                "ERAN response to harmonic violations (Koelsch 2011); "
                "inferior frontal gyrus (Broca's area homolog) engagement; "
                "TPC meso-band anchor for sub-measure pattern detection",
            13: "Theta-band phrase tracking; cortical theta entrains to phrase "
                "rate even when not acoustically marked (Ding et al. 2016); "
                "natural breathing interval in vocal music",
            14: "Theta oscillation entrainment at phrase level; closure positive "
                "shift (CPS) at phrase boundaries indicates active segmentation; "
                "strong statistical reliability for all morphs with 121 frames",
            15: "Upper theta-band processing; bridge timescale between phrase "
                "chunking and measure-level temporal receptive fields; "
                "CPS phrase boundary detection at longest meso scale",
        }

    # ------------------------------------------------------------------
    # Mechanisms
    # ------------------------------------------------------------------

    @property
    def primary_mechanisms(self) -> tuple[str, ...]:
        """Primary mechanisms active in this band."""
        return ("BEP", "ASA", "CPD", "TPC", "SYN")

    @property
    def mechanism_map(self) -> dict[str, tuple[int, ...]]:
        """Mapping of mechanism name to horizon indices where it is active."""
        return {
            "BEP": (9, 11),     # H6 entry is in micro; meso anchors at H9, H11
            "ASA": (9,),        # extends from micro H3, H6 into meso H9
            "CPD": (9,),        # entry point -- extends into macro
            "TPC": (12,),       # meso anchor; spans from H6 (micro) to H16 (macro)
            "SYN": (12,),       # entry point -- extends into macro
        }

    # ------------------------------------------------------------------
    # Demand
    # ------------------------------------------------------------------

    @property
    def demand_share(self) -> float:
        """Approximate percentage of total H3 demand in this band."""
        return 27.0

    # ------------------------------------------------------------------
    # Morph applicability
    # ------------------------------------------------------------------

    @property
    def reliable_morphs(self) -> dict[str, tuple[str, ...]]:
        """Morph reliability summary across the band.

        All 24 morphs are valid at meso timescales (52-138 frames).
        """
        return {
            "all_valid": True,
            "particularly_relevant": (
                "M14 (periodicity) -- directly measures rhythmic regularity",
                "M18 (trend) -- detects accelerando/ritardando within phrase windows",
                "M8 (velocity) -- tracks dynamic changes at beat rate",
                "M1 (mean) -- stable average over beat-length windows",
                "M20 (entropy) -- information content of phrase",
            ),
        }

    # ------------------------------------------------------------------
    # Repr
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"MesoBand(horizons=H{self.HORIZON_RANGE[0]}-H{self.HORIZON_RANGE[1] - 1}, "
            f"duration={self.DURATION_RANGE_MS[0]}-{self.DURATION_RANGE_MS[1]} ms, "
            f"frames={self.FRAME_RANGE[0]}-{self.FRAME_RANGE[1]})"
        )
