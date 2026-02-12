"""
ChillTestValidator — The ultimate test: does the model detect chills?

Scientific basis:
  Sloboda (1991): Specific musical events (appoggiaturas, crescendos,
  melodic sequences) reliably induce chills in listeners.

  Salimpoor (2011): PET imaging shows caudate DA during anticipation
  (r=0.71) and NAcc DA during peak experience (r=0.84).

Test protocol:
  1. Process audio known to induce chills
  2. Provide ground-truth chill timestamps (from listener reports)
  3. Validate: chills_intensity peak aligns with chill times
  4. Validate: Temporal dissociation (da_caudate → da_nacc)
  5. Validate: Refractory period between consecutive chills
"""

from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import Tensor

from ..core.config import MIConfig, MI_CONFIG
from ..core.types import MIOutput


@dataclass
class ChillEvent:
    """A reported chill event."""
    time_s: float       # timestamp in seconds
    intensity: float    # 0-1 self-reported intensity
    duration_s: float   # duration of the chill


@dataclass
class ChillTestResult:
    """Result of chill test validation."""
    total_chills: int
    detected: int
    missed: int
    false_positives: int
    temporal_dissociation_ok: bool
    refractory_ok: bool
    peak_alignment_score: float  # 0-1, how well peaks align

    @property
    def detection_rate(self) -> float:
        return self.detected / max(self.total_chills, 1)

    @property
    def passed(self) -> bool:
        return (
            self.detection_rate >= 0.6
            and self.temporal_dissociation_ok
            and self.peak_alignment_score >= 0.5
        )


def validate(
    output: MIOutput,
    chill_events: list[ChillEvent],
    config: MIConfig = MI_CONFIG,
    tolerance_s: float = 2.0,
    refractory_s: float = 10.0,
) -> ChillTestResult:
    """Validate MI output against ground-truth chill events.

    Args:
        output: Full MIOutput from pipeline
        chill_events: Ground-truth chill timestamps
        config: MI configuration
        tolerance_s: temporal tolerance for peak alignment (seconds)
        refractory_s: minimum expected gap between chills

    Returns:
        ChillTestResult with detection metrics
    """
    brain = output.brain
    if brain is None:
        return ChillTestResult(
            total_chills=len(chill_events),
            detected=0, missed=len(chill_events),
            false_positives=0,
            temporal_dissociation_ok=False,
            refractory_ok=False,
            peak_alignment_score=0.0,
        )

    # Extract key signals from BrainOutput (26D)
    da_caudate = brain.get_dim("da_caudate").squeeze(0)    # (T,)
    da_nacc = brain.get_dim("da_nacc").squeeze(0)          # (T,)
    chills = brain.get_dim("chills_intensity").squeeze(0)   # (T,)
    pleasure = brain.get_dim("pleasure").squeeze(0)         # (T,)
    T = da_caudate.shape[0]

    # Chill signal: chills_intensity + pleasure (Sloboda 1991, Guhn 2007)
    chill_signal = (chills + pleasure) / 2

    tolerance_frames = int(tolerance_s * config.frame_rate)

    # Check each ground-truth chill
    detected = 0
    alignment_scores = []

    for event in chill_events:
        center_frame = int(event.time_s * config.frame_rate)
        start = max(0, center_frame - tolerance_frames)
        end = min(T, center_frame + tolerance_frames)

        if start >= T:
            continue

        window = chill_signal[start:end]
        peak_val = window.max().item()

        # Detection: chill signal exceeds threshold in window
        threshold = chill_signal.mean().item() + chill_signal.std().item()
        if peak_val > threshold:
            detected += 1
            # Alignment: how close is the peak to the ground truth?
            peak_offset = torch.argmax(window).item()
            peak_frame = start + peak_offset
            distance = abs(peak_frame - center_frame) / config.frame_rate
            alignment = max(0, 1.0 - distance / tolerance_s)
            alignment_scores.append(alignment)

    missed = len(chill_events) - detected

    # False positives: peaks above threshold not near any chill
    threshold = chill_signal.mean() + 1.5 * chill_signal.std()
    peak_frames = (chill_signal > threshold).nonzero(as_tuple=True)[0]
    false_positives = 0
    for pf in peak_frames:
        pf_time = pf.item() / config.frame_rate
        near_chill = any(
            abs(pf_time - e.time_s) < tolerance_s for e in chill_events
        )
        if not near_chill:
            false_positives += 1

    # Temporal dissociation: wanting should lead liking
    caudate_peak = torch.argmax(da_caudate).item()
    nacc_peak = torch.argmax(da_nacc).item()
    temporal_dissociation_ok = caudate_peak < nacc_peak

    # Refractory period: consecutive chills should be spaced
    refractory_ok = True
    sorted_events = sorted(chill_events, key=lambda e: e.time_s)
    for i in range(1, len(sorted_events)):
        gap = sorted_events[i].time_s - sorted_events[i - 1].time_s
        if gap < refractory_s:
            refractory_ok = False
            break

    return ChillTestResult(
        total_chills=len(chill_events),
        detected=detected,
        missed=missed,
        false_positives=false_positives,
        temporal_dissociation_ok=temporal_dissociation_ok,
        refractory_ok=refractory_ok,
        peak_alignment_score=(
            sum(alignment_scores) / len(alignment_scores)
            if alignment_scores else 0.0
        ),
    )
