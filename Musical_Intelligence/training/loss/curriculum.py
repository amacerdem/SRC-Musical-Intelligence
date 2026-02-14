"""CurriculumScheduler -- 5-phase training weight schedule.

Mirrors the MI Teacher pipeline computation order (Mel → R3 → H3 → C3)
to guide the backbone's learning progression:

    Phase 1 (ep 1-50):    Mel-heavy    — learn spectral decomposition
    Phase 2 (ep 50-150):  R3-heavy     — learn psychoacoustic features
    Phase 3 (ep 150-300): H3-heavy     — learn temporal context
    Phase 4 (ep 300-500): C3-heavy     — learn cognitive outputs
    Phase 5 (ep 500+):    Full balance — all objectives active

Reference: MI-VISION Section 12.4
"""
from __future__ import annotations

from typing import Dict


# Weight schedule: (epoch_start, weight_dict)
_PHASES = [
    (0, {
        "encode_mel": 1.0, "encode_r3": 0.5, "encode_h3": 0.1, "encode_c3": 0.0,
        "decode_h3": 0.0, "decode_r3": 0.0, "decode_mel": 0.0, "decode_wav": 0.0,
        "cycle_forward": 0.0, "cycle_inverse": 0.0,
        "fill_c3": 0.0, "fill_decode": 0.0,
        "temporal_smooth": 0.1, "expert_balance": 0.1,
    }),
    (50, {
        "encode_mel": 0.5, "encode_r3": 1.0, "encode_h3": 0.5, "encode_c3": 0.1,
        "decode_h3": 0.0, "decode_r3": 0.1, "decode_mel": 0.1, "decode_wav": 0.0,
        "cycle_forward": 0.0, "cycle_inverse": 0.0,
        "fill_c3": 0.0, "fill_decode": 0.0,
        "temporal_smooth": 0.1, "expert_balance": 0.1,
    }),
    (150, {
        "encode_mel": 0.2, "encode_r3": 0.5, "encode_h3": 1.0, "encode_c3": 0.5,
        "decode_h3": 0.5, "decode_r3": 0.3, "decode_mel": 0.2, "decode_wav": 0.0,
        "cycle_forward": 0.1, "cycle_inverse": 0.1,
        "fill_c3": 0.1, "fill_decode": 0.1,
        "temporal_smooth": 0.2, "expert_balance": 0.1,
    }),
    (300, {
        "encode_mel": 0.1, "encode_r3": 0.2, "encode_h3": 0.5, "encode_c3": 1.0,
        "decode_h3": 0.5, "decode_r3": 0.5, "decode_mel": 0.5, "decode_wav": 0.3,
        "cycle_forward": 0.5, "cycle_inverse": 0.5,
        "fill_c3": 0.5, "fill_decode": 0.5,
        "temporal_smooth": 0.2, "expert_balance": 0.1,
    }),
    (500, {
        "encode_mel": 0.2, "encode_r3": 0.3, "encode_h3": 0.3, "encode_c3": 1.0,
        "decode_h3": 0.5, "decode_r3": 0.5, "decode_mel": 0.5, "decode_wav": 0.5,
        "cycle_forward": 0.5, "cycle_inverse": 0.5,
        "fill_c3": 1.0, "fill_decode": 0.5,
        "temporal_smooth": 0.2, "expert_balance": 0.1,
    }),
]

# All 14 loss term names
LOSS_NAMES = (
    "encode_mel", "encode_r3", "encode_h3", "encode_c3",
    "decode_h3", "decode_r3", "decode_mel", "decode_wav",
    "cycle_forward", "cycle_inverse",
    "fill_c3", "fill_decode",
    "temporal_smooth", "expert_balance",
)


class CurriculumScheduler:
    """5-phase curriculum weight schedule.

    Returns the appropriate loss weights for a given epoch, with
    optional linear interpolation between phases.
    """

    def __init__(self, interpolate: bool = True) -> None:
        self._phases = _PHASES
        self._interpolate = interpolate

    def get_weights(self, epoch: int) -> Dict[str, float]:
        """Get loss weights for the given epoch.

        Parameters
        ----------
        epoch : int
            Current training epoch (0-indexed).

        Returns
        -------
        dict
            Maps each of 14 loss term names to its weight.
        """
        # Find the active phase
        phase_idx = 0
        for i, (start, _) in enumerate(self._phases):
            if epoch >= start:
                phase_idx = i

        if not self._interpolate or phase_idx == len(self._phases) - 1:
            return dict(self._phases[phase_idx][1])

        # Linear interpolation between current and next phase
        curr_start, curr_weights = self._phases[phase_idx]
        next_start, next_weights = self._phases[phase_idx + 1]

        alpha = (epoch - curr_start) / max(1, next_start - curr_start)
        alpha = min(max(alpha, 0.0), 1.0)

        result = {}
        for name in LOSS_NAMES:
            w_curr = curr_weights[name]
            w_next = next_weights[name]
            result[name] = w_curr + alpha * (w_next - w_curr)

        return result

    def get_phase(self, epoch: int) -> int:
        """Get the current phase number (1-5)."""
        phase = 1
        for i, (start, _) in enumerate(self._phases):
            if epoch >= start:
                phase = i + 1
        return phase
