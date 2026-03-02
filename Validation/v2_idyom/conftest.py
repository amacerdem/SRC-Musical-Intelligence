"""V2 IDyOM — fixtures for convergent validity tests."""
from __future__ import annotations

import pytest

from Validation.config.paths import IDYOM_DIR


@pytest.fixture(scope="session")
def idyom_corpus_dir():
    """Path to IDyOM corpus directory."""
    corpus_dir = IDYOM_DIR / "essen"
    if not corpus_dir.exists():
        pytest.skip("IDyOM corpus not downloaded. Run: python -m v2_idyom.corpora")
    return corpus_dir
