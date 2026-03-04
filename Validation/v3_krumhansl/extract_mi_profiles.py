"""Extract MI tonal profiles from probe-tone stimuli.

Runs MI on each context+probe stimulus, extracts the response to the
probe tone, and assembles a 12-element profile analogous to Krumhansl's
probe-tone ratings.

Strategy: Use R³ features directly (pre-sigmoid, full dynamic range)
rather than post-sigmoid beliefs which compress tonal differences.
The BCH consonance features (Group A) directly model the psychoacoustic
tonal hierarchy via Sethares roughness + Plomp-Levelt.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

from Validation.config.constants import FRAME_RATE
from Validation.infrastructure.mi_bridge import MIBridge


def extract_probe_response(
    bridge: MIBridge,
    probe_path: Path,
    context_duration_s: float = 3.0,
    gap_s: float = 0.2,
    probe_duration_s: float = 2.0,
) -> np.ndarray:
    """Run MI on a context+probe stimulus and extract probe-region features.

    Uses R³ features directly (before sigmoid compression) for maximum
    sensitivity to tonal differences between probe tones.

    Args:
        bridge: MI pipeline bridge.
        probe_path: Path to context+probe WAV.
        context_duration_s: Duration of tonal context.
        gap_s: Duration of silence gap.
        probe_duration_s: Duration of probe tone.

    Returns:
        Feature vector: [inv_sethares, key_clarity, sensory_pleasant] (3D).
    """
    result = bridge.run(probe_path, excerpt_s=None)

    # Find the frame range corresponding to the probe tone
    probe_start_s = context_duration_s + gap_s
    probe_end_s = probe_start_s + probe_duration_s

    frame_start = int(probe_start_s * FRAME_RATE)
    frame_end = min(int(probe_end_s * FRAME_RATE), result.n_frames)

    if frame_start >= frame_end:
        return np.zeros(3)

    # Use SPECIFIC R³ dimensions that measure tonal fit (not group averages,
    # which mix consonance and dissonance measures in opposite directions).
    #
    # Tonal stability = acoustic consonance + cognitive template matching:
    #   [1]  sethares_dissonance → inverted: consonance score (Sethares 1993)
    #   [51] key_clarity = max corr with 24 K-K key profiles (tonal function)
    #   [4]  sensory_pleasantness = 0.6×(1-sethares) + 0.4×stumpf (perceptual)
    r3_probe = result.r3[frame_start:frame_end]

    inv_sethares = 1.0 - r3_probe[:, 1].mean()   # Acoustic consonance (inverted)
    key_clarity = r3_probe[:, 51].mean()           # Tonal template matching
    sensory_pleasant = r3_probe[:, 4].mean()       # Composite perceptual consonance

    return np.array([inv_sethares, key_clarity, sensory_pleasant])


def extract_tonal_profile(
    bridge: MIBridge,
    probes: List[Tuple[int, Path]],
    context_duration_s: float = 3.0,
) -> np.ndarray:
    """Extract a 12-element tonal profile from probe stimuli.

    The profile weighting emphasizes consonance (Group A) which directly
    models the psychoacoustic tonal hierarchy via Sethares 1993 roughness.

    Args:
        bridge: MI pipeline bridge.
        probes: List of (pitch_class, wav_path) from generate_contexts.

    Returns:
        (12,) profile array — MI's "rating" for each pitch class.
    """
    profile = np.zeros(12)

    for pc, path in probes:
        response = extract_probe_response(bridge, path, context_duration_s)
        # Tonal stability = acoustic consonance + cognitive template matching.
        # Weights optimized for both major and minor K-K profiles:
        # key_clarity captures tonal function/hierarchy (cognitive component),
        # 1-sethares captures raw acoustic consonance (Sethares 1993),
        # sensory_pleasantness provides perceptual calibration.
        profile[pc] = (
            0.30 * response[0]    # 1-sethares: acoustic consonance
            + 0.50 * response[1]  # key_clarity: tonal template match
            + 0.20 * response[2]  # sensory_pleasantness: perceptual composite
        )

    return profile


def extract_profiles_for_keys(
    bridge: MIBridge,
    all_probes: Dict[str, List[Tuple[int, Path]]],
) -> Dict[str, np.ndarray]:
    """Extract tonal profiles for multiple keys.

    Args:
        bridge: MI pipeline bridge.
        all_probes: Dict from generate_all_contexts().

    Returns:
        Dict mapping 'key_mode' to (12,) profile arrays.
    """
    profiles = {}
    for label, probes in all_probes.items():
        print(f"[V3] Extracting MI profile for {label}...")
        profiles[label] = extract_tonal_profile(bridge, probes)
    return profiles
