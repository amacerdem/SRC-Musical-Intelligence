"""Unit tests for all 96 cognitive model contracts.

Tests that every model across all 9 cognitive units is importable, passes
validate_constants(), has valid output dimensions, mechanism names, layers,
h3_demand_tuples, compute shapes, and that total output sums to 1006D.
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import List

sys.path.insert(0, str(Path(__file__).parents[2]))

import pytest
import torch

from Musical_Intelligence.contracts.bases.base_model import BaseModel


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ALL_UNITS = ["spu", "stu", "imu", "asu", "ndu", "mpu", "pcu", "aru", "rpu"]

# Valid mechanism names (the 10 mechanisms in the brain)
VALID_MECHANISM_NAMES = frozenset({
    "PPC", "TPC", "BEP", "ASA", "TMH", "MEM", "SYN", "AED", "CPD", "C0P",
})

B, T = 2, 40  # batch size, time steps


# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------

def get_all_model_classes() -> List[type]:
    """Import and return all model classes from all 9 units."""
    classes = []
    for unit_name in ALL_UNITS:
        mod = importlib.import_module(
            f"Musical_Intelligence.brain.units.{unit_name}.models"
        )
        classes.extend(mod.MODEL_CLASSES)
    return classes


def get_all_models() -> List[BaseModel]:
    """Instantiate all model classes from all 9 units."""
    return [cls() for cls in get_all_model_classes()]


# Cache for expensive operations
_ALL_MODELS = None


def all_models() -> List[BaseModel]:
    """Cached model instances."""
    global _ALL_MODELS
    if _ALL_MODELS is None:
        _ALL_MODELS = get_all_models()
    return _ALL_MODELS


def model_ids() -> List[str]:
    """Generate readable IDs for parametrized tests."""
    return [f"{m.UNIT}-{m.NAME}" for m in all_models()]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestAllModelsImportable:
    """Verify all 96 models can be imported and instantiated."""

    def test_all_96_models_importable(self):
        """Must find and instantiate exactly 96 model classes."""
        models = all_models()
        assert len(models) == 96, (
            f"Expected 96 models, got {len(models)}"
        )

    @pytest.mark.parametrize("unit_name", ALL_UNITS)
    def test_unit_has_model_classes(self, unit_name):
        """Each unit module must export a non-empty MODEL_CLASSES list."""
        mod = importlib.import_module(
            f"Musical_Intelligence.brain.units.{unit_name}.models"
        )
        assert hasattr(mod, "MODEL_CLASSES"), (
            f"Unit {unit_name} missing MODEL_CLASSES"
        )
        assert len(mod.MODEL_CLASSES) > 0, (
            f"Unit {unit_name} has empty MODEL_CLASSES"
        )

    def test_all_models_are_base_model_subclass(self):
        """Every model must be a subclass of BaseModel."""
        for model in all_models():
            assert isinstance(model, BaseModel), (
                f"{model.UNIT}-{model.NAME}: not a BaseModel subclass"
            )


class TestModelValidateConstants:
    """Verify all models pass validate_constants()."""

    @pytest.mark.parametrize("model", all_models(), ids=model_ids())
    def test_model_validate_constants(self, model):
        """validate_constants() must return an empty error list."""
        errors = model.validate_constants()
        assert errors == [], (
            f"{model.UNIT}-{model.NAME}: validate_constants() errors: {errors}"
        )


class TestModelOutputDim:
    """Verify all models have positive OUTPUT_DIM."""

    @pytest.mark.parametrize("model", all_models(), ids=model_ids())
    def test_model_output_dim_positive(self, model):
        """OUTPUT_DIM must be > 0."""
        assert model.OUTPUT_DIM > 0, (
            f"{model.UNIT}-{model.NAME}: OUTPUT_DIM = {model.OUTPUT_DIM}"
        )


class TestModelMechanismNames:
    """Verify all models reference only valid mechanism names."""

    @pytest.mark.parametrize("model", all_models(), ids=model_ids())
    def test_model_mechanism_names_valid(self, model):
        """Every name in MECHANISM_NAMES must be in the known mechanism set."""
        for name in model.MECHANISM_NAMES:
            assert name in VALID_MECHANISM_NAMES, (
                f"{model.UNIT}-{model.NAME}: unknown mechanism {name!r}. "
                f"Valid: {sorted(VALID_MECHANISM_NAMES)}"
            )


class TestModelLayersCoverOutput:
    """Verify LAYERS span [0, OUTPUT_DIM) without gaps or overlaps."""

    @pytest.mark.parametrize("model", all_models(), ids=model_ids())
    def test_model_layers_cover_output(self, model):
        """LAYERS must cover every index in [0, OUTPUT_DIM) exactly once."""
        if not model.LAYERS:
            pytest.skip(f"{model.UNIT}-{model.NAME}: no LAYERS defined")

        coverage = [0] * model.OUTPUT_DIM
        for layer in model.LAYERS:
            for i in range(layer.start, layer.end):
                assert 0 <= i < model.OUTPUT_DIM, (
                    f"{model.UNIT}-{model.NAME}: layer {layer.code!r} "
                    f"index {i} out of range [0, {model.OUTPUT_DIM})"
                )
                coverage[i] += 1

        uncovered = [i for i, c in enumerate(coverage) if c == 0]
        overlapped = [i for i, c in enumerate(coverage) if c > 1]

        assert not uncovered, (
            f"{model.UNIT}-{model.NAME}: uncovered indices: {uncovered}"
        )
        assert not overlapped, (
            f"{model.UNIT}-{model.NAME}: overlapped indices: {overlapped}"
        )

    @pytest.mark.parametrize("model", all_models(), ids=model_ids())
    def test_model_layers_have_empf_codes(self, model):
        """Every layer must have a code in {E, M, P, F}."""
        valid_codes = {"E", "M", "P", "F"}
        for layer in model.LAYERS:
            assert layer.code in valid_codes, (
                f"{model.UNIT}-{model.NAME}: layer code {layer.code!r} "
                f"not in {valid_codes}"
            )


class TestModelH3DemandTuples:
    """Verify h3_demand_tuples() returns valid tuples."""

    @pytest.mark.parametrize("model", all_models(), ids=model_ids())
    def test_model_h3_demand_tuples(self, model):
        """h3_demand_tuples() must return a set of valid 4-tuples."""
        tuples = model.h3_demand_tuples()
        assert isinstance(tuples, set), (
            f"{model.UNIT}-{model.NAME}: h3_demand_tuples() returned "
            f"{type(tuples)}, expected set"
        )
        for t in tuples:
            assert isinstance(t, tuple) and len(t) == 4, (
                f"{model.UNIT}-{model.NAME}: invalid tuple {t}"
            )
            r3_idx, horizon, morph, law = t
            assert 0 <= r3_idx <= 96
            assert 0 <= horizon <= 31
            assert 0 <= morph <= 23
            assert 0 <= law <= 2


class TestModelComputeShape:
    """Verify compute() returns (B, T, OUTPUT_DIM)."""

    @pytest.mark.parametrize("model", all_models(), ids=model_ids())
    def test_model_compute_shape(self, model):
        """compute() must return (B, T, OUTPUT_DIM) given synthetic inputs."""
        torch.manual_seed(42)
        r3_features = torch.rand(B, T, 97)

        # Build synthetic mechanism outputs
        mechanism_outputs = {}
        for name in model.MECHANISM_NAMES:
            mechanism_outputs[name] = torch.rand(B, T, 30)

        # Build synthetic H3 features for every demanded tuple
        h3_features = {}
        for tup in model.h3_demand_tuples():
            h3_features[tup] = torch.rand(B, T)

        out = model.compute(mechanism_outputs, h3_features, r3_features)
        assert out.shape == (B, T, model.OUTPUT_DIM), (
            f"{model.UNIT}-{model.NAME}: expected "
            f"({B}, {T}, {model.OUTPUT_DIM}), got {out.shape}"
        )


class TestTotalOutputDim:
    """Verify the sum of all model OUTPUT_DIMs equals 1006."""

    def test_total_output_dim_1006(self):
        """Sum of OUTPUT_DIM across all 96 models must be 1006."""
        models = all_models()
        total = sum(m.OUTPUT_DIM for m in models)
        assert total == 1006, (
            f"Expected total OUTPUT_DIM = 1006, got {total}"
        )

    def test_per_unit_output_dims(self):
        """Verify per-unit dimension totals match the architecture spec."""
        expected_per_unit = {
            "SPU": 99,
            "STU": 148,
            "IMU": 159,
            "ASU": 94,
            "NDU": 94,
            "MPU": 104,
            "PCU": 94,
            "ARU": 120,
            "RPU": 94,
        }
        models = all_models()
        per_unit: dict = {}
        for m in models:
            per_unit[m.UNIT] = per_unit.get(m.UNIT, 0) + m.OUTPUT_DIM

        for unit, expected_dim in expected_per_unit.items():
            actual = per_unit.get(unit, 0)
            assert actual == expected_dim, (
                f"Unit {unit}: expected {expected_dim}D, got {actual}D"
            )


class TestModelDimensionNames:
    """Verify dimension_names consistency with OUTPUT_DIM."""

    @pytest.mark.parametrize("model", all_models(), ids=model_ids())
    def test_model_dimension_names_count(self, model):
        """len(dimension_names) must equal OUTPUT_DIM."""
        names = model.dimension_names
        assert len(names) == model.OUTPUT_DIM, (
            f"{model.UNIT}-{model.NAME}: dimension_names has "
            f"{len(names)} entries, OUTPUT_DIM = {model.OUTPUT_DIM}"
        )

    @pytest.mark.parametrize("model", all_models(), ids=model_ids())
    def test_model_dimension_names_unique(self, model):
        """All dimension names within a model must be unique."""
        names = model.dimension_names
        assert len(set(names)) == len(names), (
            f"{model.UNIT}-{model.NAME}: duplicate dimension names found"
        )
