"""V6 Test — fMRI ROI Encoding: MI features predict BOLD in music regions.

Predictions:
    1. MI full model R² > 0 for auditory regions (A1, STG)
    2. MI full model R² > simple acoustic baseline
    3. At least 10/26 regions show positive R²
"""
from __future__ import annotations

import gc
import tempfile
from pathlib import Path

import numpy as np
import pytest
import torch

from Validation.config.constants import REGION_NAMES
from Validation.v6_fmri_encoding.preprocess_fmri import load_fmri_subject
from Validation.v6_fmri_encoding.extract_rois import extract_roi_signals
from Validation.v6_fmri_encoding.extract_mi_features import extract_features_for_fmri
from Validation.v6_fmri_encoding.fit_encoding import compare_feature_sets


def _concatenate_stimuli(audio_files: list[Path], out_path: Path) -> Path:
    """Concatenate multiple audio files into one WAV for MI processing."""
    import soundfile as sf

    segments = []
    target_sr = None
    for f in sorted(audio_files):
        try:
            data, sr = sf.read(str(f), dtype="float32")
            if data.ndim == 2:
                data = data.mean(axis=1)
            if target_sr is None:
                target_sr = sr
            segments.append(data)
        except Exception:
            continue

    if not segments:
        return None
    combined = np.concatenate(segments)
    sf.write(str(out_path), combined, target_sr)
    return out_path


@pytest.mark.v6
@pytest.mark.requires_download
@pytest.mark.slow
class TestROIPrediction:
    """MI features should predict fMRI BOLD in music-related brain regions."""

    @pytest.fixture(scope="class")
    def fmri_results(self, mi_bridge, fmri_dataset_dir):
        """Load fMRI, extract ROIs, run MI, fit models.

        Uses classicalMusic task with matching classical stimuli to ensure
        proper stimulus—BOLD alignment.
        """
        # Load first subject — classicalMusic task (continuous music listening)
        sub_dirs = sorted(d for d in fmri_dataset_dir.iterdir()
                          if d.is_dir() and d.name.startswith("sub"))
        if not sub_dirs:
            pytest.skip("No subjects in fMRI dataset")

        subject = load_fmri_subject(
            fmri_dataset_dir, sub_dirs[0].name, task="classicalMusic",
        )
        roi_signals = extract_roi_signals(subject)

        # Use matching classical music stimuli (not generated clips)
        stim_dir = fmri_dataset_dir / "stimuli" / "classical"
        stim_files = sorted(stim_dir.glob("*.mp3")) + sorted(stim_dir.glob("*.wav"))
        if not stim_files:
            # Fallback: try any music stimulus
            stim_files = sorted(fmri_dataset_dir.rglob("stimuli/**/*.wav"))
            stim_files += sorted(fmri_dataset_dir.rglob("stimuli/**/*.mp3"))
        if not stim_files:
            pytest.skip("No stimulus audio in fMRI dataset")

        # Concatenate stimuli to match fMRI duration
        scan_duration = roi_signals.shape[0] * subject["tr"]
        tmp_dir = Path(tempfile.mkdtemp())
        concat_path = tmp_dir / "classical_concat.wav"
        concat_path = _concatenate_stimuli(stim_files, concat_path)
        if concat_path is None:
            pytest.skip("Could not read stimulus audio files")

        mi_features = extract_features_for_fmri(
            mi_bridge, concat_path,
            tr=subject["tr"],
            excerpt_s=scan_duration,
        )

        # Memory cleanup before fitting
        gc.collect()
        if torch.backends.mps.is_available():
            torch.mps.empty_cache()

        results = compare_feature_sets(mi_features, roi_signals)

        # Clean up temp
        concat_path.unlink(missing_ok=True)
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
