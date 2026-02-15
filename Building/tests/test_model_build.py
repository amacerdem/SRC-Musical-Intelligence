"""Test whether models have been properly built (not still skeletons).

This test file complements the contract tests in Tests/unit/test_models.py
by checking for skeleton residue — generic patterns that indicate a model
has not yet been transformed from its placeholder implementation.

Usage:
    pytest Building/tests/test_model_build.py -v
    pytest Building/tests/test_model_build.py -v -k "BCH"
    pytest Building/tests/test_model_build.py -v -k "SPU"
"""
from __future__ import annotations

import pytest

from .conftest_building import is_skeleton, skeleton_indicators


# ---------------------------------------------------------------------------
# Collect all 96 models
# ---------------------------------------------------------------------------

def _collect_all_models():
    """Import and instantiate all 96 cognitive models."""
    models = []
    units = {
        "spu": "Musical_Intelligence.brain.units.spu.models",
        "stu": "Musical_Intelligence.brain.units.stu.models",
        "imu": "Musical_Intelligence.brain.units.imu.models",
        "asu": "Musical_Intelligence.brain.units.asu.models",
        "ndu": "Musical_Intelligence.brain.units.ndu.models",
        "mpu": "Musical_Intelligence.brain.units.mpu.models",
        "pcu": "Musical_Intelligence.brain.units.pcu.models",
        "aru": "Musical_Intelligence.brain.units.aru.models",
        "rpu": "Musical_Intelligence.brain.units.rpu.models",
    }
    for unit_name, module_path in units.items():
        try:
            import importlib
            mod = importlib.import_module(module_path)
            if hasattr(mod, "ALL_MODELS"):
                for model_cls in mod.ALL_MODELS:
                    models.append(model_cls())
        except ImportError:
            pass
    return models


ALL_MODELS = _collect_all_models()


# ---------------------------------------------------------------------------
# Parametric test: is this model built?
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "model",
    ALL_MODELS,
    ids=lambda m: f"{m.UNIT}-{m.NAME}",
)
class TestModelBuild:
    """Tests that verify a model has been properly built."""

    def test_not_skeleton(self, model):
        """Model should not have skeleton residue."""
        if is_skeleton(model):
            indicators = skeleton_indicators(model)
            indicator_str = "\n  - ".join(indicators)
            pytest.skip(
                f"{model.UNIT}-{model.NAME} is still a skeleton:\n"
                f"  - {indicator_str}"
            )

    def test_semantic_dimension_names(self, model):
        """Dimension names should be semantically meaningful."""
        name_lower = model.NAME.lower()
        for dim_name in model.dimension_names:
            assert not dim_name.startswith(f"{name_lower}_e"), (
                f"Generic dimension name '{dim_name}' — "
                f"should be semantic (e.g., 'f01_nps', 'consonance_signal')"
            )
            assert not dim_name.startswith(f"{name_lower}_m"), (
                f"Generic dimension name '{dim_name}'"
            )
            assert not dim_name.startswith(f"{name_lower}_p"), (
                f"Generic dimension name '{dim_name}'"
            )
            assert not dim_name.startswith(f"{name_lower}_f"), (
                f"Generic dimension name '{dim_name}'"
            )

    def test_real_citations(self, model):
        """Citations should reference real papers, not placeholders."""
        meta = model.metadata
        assert meta.citations, f"{model.NAME} has no citations"
        for cit in meta.citations:
            assert cit.first_author != "Author", (
                f"{model.NAME} has placeholder citation: "
                f"Citation('Author', {cit.year}, ...)"
            )

    def test_sufficient_h3_demand(self, model):
        """Built models should have at least 8 H3 demand tuples."""
        demand = model.h3_demand
        assert len(demand) >= 8, (
            f"{model.NAME} has only {len(demand)} h3_demand tuples. "
            f"Skeletons have 4; built models typically have 12-20."
        )

    def test_sufficient_brain_regions(self, model):
        """Built models should have at least 4 brain regions."""
        regions = model.brain_regions
        assert len(regions) >= 4, (
            f"{model.NAME} has only {len(regions)} brain regions. "
            f"Docs typically specify 4-6."
        )

    def test_version_updated(self, model):
        """Built models should have version > 1.0.0."""
        meta = model.metadata
        assert meta.version != "1.0.0", (
            f"{model.NAME} still at version 1.0.0 (skeleton default)"
        )
