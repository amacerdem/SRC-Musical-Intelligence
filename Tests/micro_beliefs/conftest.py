"""Shared fixtures for micro-belief tests.

The ``runner`` fixture is session-scoped — expensive pipeline init
happens once, then all test modules share the same extractors and
mechanism/belief instances.
"""
from __future__ import annotations

import pytest

from .pipeline_runner import MicroBeliefRunner


@pytest.fixture(scope="session")
def runner() -> MicroBeliefRunner:
    """Session-scoped full-pipeline runner."""
    return MicroBeliefRunner()
