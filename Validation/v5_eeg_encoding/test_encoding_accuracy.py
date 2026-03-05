"""V5 Test — EEG Encoding: MI features predict EEG better than baselines.

Predictions:
    1. MI full model R² > acoustic envelope baseline R²
    2. MI beliefs contribute unique variance beyond R³ features
    3. Mean encoding R² > 0 (above chance)
"""
from __future__ import annotations

import pytest

from Validation.v5_eeg_encoding.preprocess_eeg import load_eeg_subject
from Validation.v5_eeg_encoding.extract_mi_features import extract_features_for_eeg
from Validation.v5_eeg_encoding.baselines import get_all_baselines
from Validation.v5_eeg_encoding.fit_trf import compare_models


@pytest.mark.v5
@pytest.mark.requires_download
@pytest.mark.slow
class TestEncodingAccuracy:
    """MI features should predict EEG responses to music."""

    @pytest.fixture(scope="class")
    def encoding_results(self, mi_bridge, nmed_t_dir, module_data):
        """Run encoding models for first subject."""
        # Find first subject
        sub_dirs = sorted(d for d in nmed_t_dir.iterdir()
                          if d.is_dir() and d.name.startswith("sub"))
        if not sub_dirs:
            pytest.skip("No subjects found in NMED-T")

        sub_dir = sub_dirs[0]
        subject = load_eeg_subject(sub_dir, sub_dir.name)

        # Find stimulus audio
        stim_files = list(nmed_t_dir.rglob("*.wav"))
        if not stim_files:
            pytest.skip("No stimulus audio found in NMED-T")

        audio_path = stim_files[0]

        # Extract MI features
        mi_features = extract_features_for_eeg(
            mi_bridge, audio_path, eeg_sfreq=subject["sfreq"],
        )

        # Get baselines
        baselines = get_all_baselines(audio_path, eeg_sfreq=subject["sfreq"])

        # Combine
        all_features = {**baselines, **mi_features}

        # Fit models
        results = compare_models(all_features, subject["eeg"], subject["sfreq"])

        # Stash for auto-reporting
        module_data["v5"] = results

        return results

    def test_mi_full_beats_envelope(self, encoding_results):
        """MI full model should outperform acoustic envelope."""
        envelope_r2 = encoding_results["envelope"]["mean_r2"]
        full_r2 = encoding_results["full"]["mean_r2"]

        assert full_r2 > envelope_r2, (
            f"Expected MI full R² ({full_r2:.4f}) > envelope R² ({envelope_r2:.4f})"
        )

    def test_beliefs_add_unique_variance(self, encoding_results):
        """C³ beliefs should add unique variance beyond R³."""
        r3_r2 = encoding_results["r3"]["mean_r2"]
        full_r2 = encoding_results["full"]["mean_r2"]

        assert full_r2 > r3_r2, (
            f"Expected full R² ({full_r2:.4f}) > R³-only R² ({r3_r2:.4f})"
        )

    def test_above_chance(self, encoding_results):
        """Mean encoding R² should be above chance (> 0)."""
        full_r2 = encoding_results["full"]["mean_r2"]
        assert full_r2 > 0, (
            f"Expected positive R², got {full_r2:.4f}"
        )
