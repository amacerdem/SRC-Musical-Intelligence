"""Krumhansl & Kessler 1982 tonal hierarchy profiles.

Published probe-tone ratings for major and minor keys.
These are the gold standard for tonal expectation in music cognition.

Source: Krumhansl, C.L. & Kessler, E.J. (1982). Tracing the dynamic changes
        in perceived tonal organization in a spatial representation of musical
        keys. Psychological Review, 89(4), 334-368.
"""
from __future__ import annotations

import numpy as np

# Pitch classes: C, C#, D, D#, E, F, F#, G, G#, A, A#, B
PITCH_CLASS_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# ── Krumhansl-Kessler major key profile (C major) ──
# Probe-tone ratings normalized to sum to 1 for correlation
MAJOR_PROFILE = np.array([
    6.35,  # C  (tonic)
    2.23,  # C#
    3.48,  # D
    2.33,  # D#
    4.38,  # E  (mediant)
    4.09,  # F  (subdominant)
    2.52,  # F#
    5.19,  # G  (dominant)
    2.39,  # G#
    3.66,  # A
    2.29,  # A#
    2.88,  # B
], dtype=np.float64)

# ── Krumhansl-Kessler minor key profile (C minor) ──
MINOR_PROFILE = np.array([
    6.33,  # C  (tonic)
    2.68,  # C#
    3.52,  # D
    5.38,  # D#/Eb (mediant)
    2.60,  # E
    3.53,  # F  (subdominant)
    2.54,  # F#
    4.75,  # G  (dominant)
    3.98,  # G#/Ab
    2.69,  # A
    3.34,  # A#/Bb
    3.17,  # B
], dtype=np.float64)


def get_profile(key: str = "C", mode: str = "major") -> np.ndarray:
    """Get the Krumhansl-Kessler profile for any key.

    Rotates the canonical C major/minor profile to the specified key.

    Args:
        key: Root pitch class (e.g. 'C', 'F#', 'Bb').
        mode: 'major' or 'minor'.

    Returns:
        12-element profile array.
    """
    # Map key name to semitone offset from C
    key_map = {
        "C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
        "E": 4, "Fb": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7,
        "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11, "Cb": 11,
    }

    offset = key_map.get(key, 0)
    profile = MAJOR_PROFILE if mode == "major" else MINOR_PROFILE

    # Rotate: shift profile so the tonic is at the correct position
    return np.roll(profile, offset)


def get_all_profiles() -> dict[str, np.ndarray]:
    """Get profiles for all 24 major/minor keys.

    Returns:
        Dict mapping 'C_major', 'C#_major', ..., 'B_minor' to profiles.
    """
    profiles = {}
    for key in PITCH_CLASS_NAMES:
        for mode in ("major", "minor"):
            label = f"{key}_{mode}"
            profiles[label] = get_profile(key, mode)
    return profiles


# ── Tonal hierarchy expectations ──
# Expected ordering of probe-tone ratings within a key

MAJOR_HIERARCHY = {
    "tonic": 0,       # C — highest
    "dominant": 7,    # G — second highest
    "mediant": 4,     # E — third
    "subdominant": 5, # F — fourth
    "diatonic": [2, 9, 11],  # D, A, B — mid-range
    "chromatic": [1, 3, 6, 8, 10],  # non-diatonic — lowest
}

MINOR_HIERARCHY = {
    "tonic": 0,       # C — highest
    "mediant": 3,     # Eb — high
    "dominant": 7,    # G — high
    "subdominant": 5, # F — mid
    "diatonic": [2, 8, 10],  # D, Ab, Bb — mid-range
    "chromatic": [1, 4, 6, 9, 11],  # non-diatonic — lowest
}
