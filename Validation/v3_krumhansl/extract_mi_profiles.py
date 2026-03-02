"""Extract MI tonal profiles from probe-tone stimuli.

Runs MI on each context+probe stimulus, extracts the response to the
probe tone, and assembles a 12-element profile analogous to Krumhansl's
probe-tone ratings.
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
    gap_s: float = 0.5,
    probe_duration_s: float = 1.0,
) -> np.ndarray:
    """Run MI on a context+probe stimulus and extract probe-region features.

    Args:
        bridge: MI pipeline bridge.
        probe_path: Path to context+probe WAV.
        context_duration_s: Duration of tonal context.
        gap_s: Duration of silence gap.
        probe_duration_s: Duration of probe tone.

    Returns:
        Mean MI feature vector during the probe region (scalar or vector).
    """
    result = bridge.run(probe_path, excerpt_s=None)

    # Find the frame range corresponding to the probe tone
    probe_start_s = context_duration_s + gap_s
    probe_end_s = probe_start_s + probe_duration_s

    frame_start = int(probe_start_s * FRAME_RATE)
    frame_end = min(int(probe_end_s * FRAME_RATE), result.n_frames)

    if frame_start >= frame_end:
        return np.zeros(1)

    # Extract mean response during probe:
    # Use a combination of:
    # 1. R³ consonance features (Group A, indices 0:7) — captures tonal fit
    # 2. Beliefs — captures predictive processing response
    # 3. Reward — captures overall "goodness of fit"

    # Primary measure: consonance-weighted reward
    r3_probe = result.r3[frame_start:frame_end, 0:7]  # consonance features
    beliefs_probe = result.beliefs[frame_start:frame_end]
    reward_probe = result.reward[frame_start:frame_end]

    # Combine: mean consonance + mean reward as stability measure
    consonance_mean = r3_probe.mean()
    reward_mean = reward_probe.mean()
    belief_stability = beliefs_probe.mean()

    return np.array([consonance_mean, reward_mean, belief_stability])


def extract_tonal_profile(
    bridge: MIBridge,
    probes: List[Tuple[int, Path]],
    context_duration_s: float = 3.0,
) -> np.ndarray:
    """Extract a 12-element tonal profile from probe stimuli.

    Args:
        bridge: MI pipeline bridge.
        probes: List of (pitch_class, wav_path) from generate_contexts.

    Returns:
        (12,) profile array — MI's "rating" for each pitch class.
    """
    profile = np.zeros(12)

    for pc, path in probes:
        response = extract_probe_response(bridge, path, context_duration_s)
        # Use weighted combination as the profile "rating"
        # Consonance (0.4) + Reward (0.4) + Belief stability (0.2)
        profile[pc] = 0.4 * response[0] + 0.4 * response[1] + 0.2 * response[2]

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
