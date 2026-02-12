"""Tests for the chill test validator itself."""

import torch
import pytest

from mi.validation.chill_test import ChillEvent, ChillTestResult, validate
from mi.core.types import MIOutput


def test_chill_event():
    e = ChillEvent(time_s=10.0, intensity=0.8, duration_s=2.0)
    assert e.time_s == 10.0
    assert e.intensity == 0.8


def test_chill_test_result_detection_rate():
    r = ChillTestResult(
        total_chills=10, detected=7, missed=3, false_positives=2,
        temporal_dissociation_ok=True, refractory_ok=True,
        peak_alignment_score=0.8,
    )
    assert r.detection_rate == 0.7
    assert r.passed is True


def test_chill_test_result_fails():
    r = ChillTestResult(
        total_chills=10, detected=3, missed=7, false_positives=5,
        temporal_dissociation_ok=False, refractory_ok=True,
        peak_alignment_score=0.3,
    )
    assert r.detection_rate == 0.3
    assert r.passed is False


def test_validate_no_brain():
    output = MIOutput(brain=None)
    events = [ChillEvent(time_s=10.0, intensity=0.8, duration_s=2.0)]
    result = validate(output, events)
    assert result.detected == 0
    assert result.missed == 1
