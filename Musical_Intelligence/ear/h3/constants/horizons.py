"""H3 horizon constants -- 32 temporal scales from 5.8 ms to 981 s.

Defines the complete set of 32 horizons organized into 4 perceptual bands
(Micro, Meso, Macro, Ultra), along with frame-count derivations at the
canonical 172.27 Hz frame rate inherited from R3.

Source of truth
---------------
- Docs/H3/H3-TEMPORAL-ARCHITECTURE.md  Section 4
- Docs/H3/Registry/HorizonCatalog.md   authoritative 32-horizon catalog
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Frame rate (inherited from R3 / Cochlea)
# ---------------------------------------------------------------------------
FRAME_RATE: float = 172.27
"""Frame rate in Hz.  hop_length=256, sr=44100 -> 44100/256 = 172.27 Hz."""

FRAME_DURATION_MS: float = 5.804
"""Duration of a single frame in milliseconds.  1000 / 172.27 ~ 5.804 ms."""

# ---------------------------------------------------------------------------
# Number of horizons
# ---------------------------------------------------------------------------
N_HORIZONS: int = 32

# ---------------------------------------------------------------------------
# HORIZON_MS -- canonical durations in milliseconds
# ---------------------------------------------------------------------------
HORIZON_MS: tuple[float, ...] = (
    # Micro band  H0-H7  (sensory / sub-beat)
    5.8,        # H0   single frame, onset detection
    11.6,       # H1   double frame, fine timing
    17.4,       # H2   sub-onset grouping
    23.2,       # H3   consonant onset, attack
    34.8,       # H4   short attack transient
    46.4,       # H5   phoneme / short note boundary
    200,        # H6   short note, sixteenth note
    250,        # H7   beat subdivision, eighth note
    # Meso band  H8-H15  (beat / phrase)
    300,        # H8   fast beat (200 BPM)
    350,        # H9   quick beat (170 BPM)
    400,        # H10  moderate beat (150 BPM)
    450,        # H11  walking tempo (133 BPM)
    525,        # H12  common beat (114 BPM)
    600,        # H13  standard beat (100 BPM)
    700,        # H14  slow beat (86 BPM)
    800,        # H15  half-note, slow tempo
    # Macro band  H16-H23  (section / passage)
    1_000,      # H16  1 measure @ 240 BPM
    1_500,      # H17  1 measure @ 160 BPM
    2_000,      # H18  1 measure @ 120 BPM
    3_000,      # H19  2-measure phrase
    5_000,      # H20  short passage
    8_000,      # H21  extended passage / verse
    15_000,     # H22  musical section (A of ABA)
    25_000,     # H23  multi-section span
    # Ultra band  H24-H31  (movement / full work)
    36_000,     # H24  movement intro / extended section
    60_000,     # H25  short movement / song
    120_000,    # H26  standard movement
    200_000,    # H27  extended movement
    414_000,    # H28  multi-movement span
    600_000,    # H29  long movement / half work
    800_000,    # H30  near-complete work
    981_000,    # H31  full work (~16 min)
)

# ---------------------------------------------------------------------------
# HORIZON_FRAMES -- frame counts derived from HORIZON_MS
# ---------------------------------------------------------------------------
# Derivation formula: max(1, round(ms / 1000 * FRAME_RATE))
# Values below are the authoritative counts from HorizonCatalog.md, which
# resolve floating-point rounding ambiguities at large horizons.
HORIZON_FRAMES: tuple[int, ...] = (
    # Micro H0-H7
    1, 2, 3, 4, 6, 8, 34, 43,
    # Meso H8-H15
    52, 60, 69, 78, 90, 103, 121, 138,
    # Macro H16-H23
    172, 259, 345, 517, 861, 1_378, 2_584, 4_307,
    # Ultra H24-H31
    6_202, 10_336, 20_672, 34_453, 71_319, 103_359, 137_812, 168_999,
)

# ---------------------------------------------------------------------------
# Band assignments and ranges
# ---------------------------------------------------------------------------
_BAND_NAMES = ("micro", "meso", "macro", "ultra")

BAND_ASSIGNMENTS: tuple[str, ...] = tuple(
    _BAND_NAMES[i // 8] for i in range(N_HORIZONS)
)
"""Band label for each horizon index.  H0-H7='micro', H8-H15='meso',
H16-H23='macro', H24-H31='ultra'."""

BAND_RANGES: dict[str, tuple[int, int]] = {
    "micro": (0, 7),
    "meso":  (8, 15),
    "macro": (16, 23),
    "ultra": (24, 31),
}
"""Inclusive (start, end) horizon-index range for each perceptual band."""
