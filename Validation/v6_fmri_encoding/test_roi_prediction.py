"""V6 Test — fMRI ROI Encoding: MI features predict BOLD in music regions.

Predictions:
    1. MI full model R² > 0 for auditory regions (A1, STG)
    2. MI full model R² > simple acoustic baseline
    3. At least 10/26 regions show positive R²
"""
from __future__ import annotations

import pytest

from Validation.config.constants import REGION_NAMES
from Validation.v6_fmri_encoding.preprocess_fmri import load_fmri_subject
from Validation.v6_fmri_encoding.extract_rois import extract_roi_signals
from Validation.v6_fmri_encoding.extract_mi_features import extract_features_for_fmri
from Validation.v6_fmri_encoding.fit_encoding import compare_feature_sets


@pytest.mark.v6
@pytest.mark.requires_download
@pytest.mark.slow
class TestROIPrediction:
    """MI features should predict fMRI BOLD in music-related brain regions."""

    @pytest.fixture(scope="class")
    def fmri_results(self, mi_bridge, fmri_dataset_dir):
        """Load fMRI, extract ROIs, run MI, fit models."""
        # Load first subject
        sub_dirs = sorted(d for d in fmri_dataset_dir.iterdir()
                          if d.is_dir() and d.name.startswith("sub"))
        if not sub_dirs:
            pytest.skip("No subjects in fMRI dataset")

        subject = load_fmri_subject(fmri_dataset_dir, sub_dirs[0].name)
        roi_signals = extract_roi_signals(subject)

        # Find stimulus audio
        stim_files = list(fmri_dataset_dir.rglob("stimuli/*.wav"))
        if not stim_files:
            pytest.skip("No stimulus audio in fMRI dataset")

        mi_features = extract_features_for_fmri(
            mi_bridge, stim_files[0], tr=subject["tr"],
        )

        results = compare_feature_sets(mi_features, roi_signals)
        return results

    def test_auditory_regions_predicted(self, fmri_results):
        """Auditory regions (A1_HG, STG) should have positive R²."""
        full = fmri_results["full"]
        a1_r2 = full["r2_per_roi"][0]   # A1_HG = index 0
        stg_r2 = full["r2_per_roi"][1]  # STG = index 1

        assert a1_r2 > 0 or stg_r2 > 0, (
            f"Expected positive R² for auditory regions. "
            f"A1_HG={a1_r2:.4f}, STG={stg_r2:.4f}"
        )

    def test_significant_roi_count(self, fmri_results):
        """At least 10 of 26 regions should show positive R²."""
        full = fmri_results["full"]
        assert full["significant_rois"] >= 10, (
            f"Expected ≥10 significant ROIs, got {full['significant_rois']}"
        )

    def test_beliefs_improve_prediction(self, fmri_results):
        """C³ beliefs should improve prediction over R³ alone."""
        r3_r2 = fmri_results["r3"]["mean_r2"]
        full_r2 = fmri_results["full"]["mean_r2"]

        assert full_r2 > r3_r2, (
            f"Expected full R² ({full_r2:.4f}) > R³ R² ({r3_r2:.4f})"
        )
