"""Ultra band -- H24-H31 (36 s to 981 s).

Covers the longest temporal horizons in the H3 system, spanning from
36 seconds to over 16 minutes.  These horizons capture movement-level
and piece-level musical structure.  This is the sparsest band -- only
the MEM mechanism extends here (at H25), and only IMU actively consumes
ultra-band horizons.

Source of truth
---------------
- Docs/H3/Bands/Ultra/00-INDEX.md
- Docs/H3/Bands/Ultra/H24-H28-Movement.md
- Docs/H3/Bands/Ultra/H29-H31-Piece.md
"""

from __future__ import annotations

from ..constants.horizons import HORIZON_FRAMES, HORIZON_MS


class UltraBand:
    """Metadata class for the Ultra temporal band (H24-H31).

    The Ultra band spans 36,000 ms to 981,000 ms (6,202-168,999 frames).
    This band is the sparsest in the system; H29-H31 currently have no
    mechanism or unit assignments.  Neural correlate: infra-slow
    oscillations (<0.1 Hz).

    Known limitation: long-form musical structure processing
    (multi-movement symphonies, opera acts, album-length works)
    remains an area of active research with limited empirical grounding.
    """

    NAME: str = "ultra"
    HORIZON_RANGE: tuple[int, int] = (24, 32)  # half-open: H24 through H31
    DURATION_RANGE_MS: tuple[float, float] = (36_000.0, 981_000.0)
    FRAME_RANGE: tuple[int, int] = (6_202, 168_999)
    NEURAL_CORRELATE: str = "Infra-slow oscillations (<0.1 Hz)"

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
            24: "~36 s -- exposition; classical exposition, pop verse-chorus "
                "cycle, jazz head; IMU interpolation between H23 and H25",
            25: "1 minute -- MEM longest memory encoding window; complete "
                "musical sections (verse-chorus-verse, ABA form, rondo "
                "episodes); two verse-chorus cycles in pop",
            26: "2 minutes -- extended formal unit; pop song through bridge, "
                "classical development section, two jazz solo choruses",
            27: "~3.3 minutes -- typical pop single or classical aria length; "
                "median length of popular music tracks",
            28: "~7 minutes -- full movement of moderate-length classical "
                "works; complete jazz performance; extended pop/rock track; "
                "practical upper limit for single-movement processing",
            29: "10 minutes -- complete sonata-allegro movement; full jazz "
                "set piece; long pop/rock composition; no mechanism or "
                "unit assignments (reserved capacity)",
            30: "~13 minutes -- extended symphonic movement (Mahler adagios, "
                "Bruckner slow movements); no mechanism or unit assignments "
                "(reserved capacity)",
            31: "~16 minutes -- system maximum; accommodates extended "
                "symphonic movements, complete pop/rock album sides; "
                "no mechanism or unit assignments (reserved capacity)",
        }

    # ------------------------------------------------------------------
    # Neuroscience basis
    # ------------------------------------------------------------------

    @property
    def neuroscience_basis(self) -> dict[int, str]:
        """Per-horizon neuroscience basis from documentation."""
        return {
            24: "Infra-slow fluctuations (ISFs) modulating default mode network; "
                "sustained attention and mind-wandering cycles; "
                "autonomic responses (heart rate variability, skin conductance)",
            25: "MEM longest explicit encoding span; hippocampal replay for "
                "pattern completion of previously heard sections; "
                "prefrontal evaluation of form-level comparison; "
                "temporal tagging via hippocampal time-cells",
            26: "Infra-slow oscillations; hierarchical compression of "
                "section-level representations into form-level schemas; "
                "expectation generation from genre knowledge",
            27: "Long-term memory retrieval comparing current experience with "
                "expectations; hierarchical compression; surprise detection "
                "for deviations from expected form",
            28: "Form-level processing via hierarchical compression; "
                "expectation generation and surprise detection; "
                "primary computational bottleneck of the ultra band "
                "(71,319-frame buffer)",
            29: "Speculative -- very few empirical studies at 10+ minute "
                "timescales; limited evidence from behavioral form "
                "recognition and self-report emotional arc studies",
            30: "Speculative -- empirical research gap; evidence limited to "
                "behavioral studies and fMRI with <10 min stimuli",
            31: "Speculative -- system maximum; stationarity assumption "
                "strongly violated at 16-minute windows; "
                "reserved for future long-form cognition research",
        }

    # ------------------------------------------------------------------
    # Mechanisms
    # ------------------------------------------------------------------

    @property
    def primary_mechanisms(self) -> tuple[str, ...]:
        """Primary mechanisms active in this band.

        Only MEM extends into the ultra band, at a single horizon (H25).
        """
        return ("MEM",)

    @property
    def mechanism_map(self) -> dict[str, tuple[int, ...]]:
        """Mapping of mechanism name to horizon indices where it is active."""
        return {
            "MEM": (25,),  # H18, H20, H22 are in macro; H25 is the ultra anchor
        }

    # ------------------------------------------------------------------
    # Demand
    # ------------------------------------------------------------------

    @property
    def demand_share(self) -> float:
        """Approximate percentage of total H3 demand in this band.

        The ultra band is extremely sparse.  H24-H28 account for ~5.6%
        and H29-H31 account for ~0.4%, totaling roughly 6%.
        """
        return 10.0

    # ------------------------------------------------------------------
    # Morph applicability
    # ------------------------------------------------------------------

    @property
    def reliable_morphs(self) -> dict[str, tuple[str, ...]]:
        """Morph reliability summary across the band.

        Only simple aggregates are meaningful at ultra timescales.
        """
        return {
            "meaningful": (
                "M1 (mean)",
                "M18 (trend)",
                "M19 (stability)",
            ),
            "marginal": (
                "M2 (std)",
                "M5 (range)",
                "M20 (entropy)",
            ),
            "not_meaningful": (
                "M8 (velocity)",
                "M9 (acceleration)",
                "M14 (periodicity)",
                "M16 (curvature)",
                "M22 (peaks)",
            ),
        }

    # ------------------------------------------------------------------
    # Demand sparsity
    # ------------------------------------------------------------------

    @property
    def demand_sparsity(self) -> dict[int, dict[str, object]]:
        """Per-horizon demand estimates from documentation.

        Ultra band is the emptiest region of the H3 system.
        """
        return {
            24: {"estimated_models": 5, "estimated_tuples": 120, "pct_of_total": 1.4},
            25: {"estimated_models": 8, "estimated_tuples": 200, "pct_of_total": 2.3},
            26: {"estimated_models": 4, "estimated_tuples": 80, "pct_of_total": 0.9},
            27: {"estimated_models": 3, "estimated_tuples": 50, "pct_of_total": 0.6},
            28: {"estimated_models": 2, "estimated_tuples": 30, "pct_of_total": 0.3},
            29: {"estimated_models": 2, "estimated_tuples": 20, "pct_of_total": 0.2},
            30: {"estimated_models": 1, "estimated_tuples": 10, "pct_of_total": 0.1},
            31: {"estimated_models": 1, "estimated_tuples": 5, "pct_of_total": 0.06},
        }

    # ------------------------------------------------------------------
    # Repr
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"UltraBand(horizons=H{self.HORIZON_RANGE[0]}-H{self.HORIZON_RANGE[1] - 1}, "
            f"duration={self.DURATION_RANGE_MS[0]}-{self.DURATION_RANGE_MS[1]} ms, "
            f"frames={self.FRAME_RANGE[0]}-{self.FRAME_RANGE[1]})"
        )
