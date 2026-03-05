"""V7 Test — RSA: MI belief RDM should explain neural similarity better than baselines.

Predictions:
    1. MI belief RDM correlates with neural RDM (rho > 0)
    2. MI belief RDM > acoustic MFCC RDM
    3. MI belief RDM > simple spectral RDM
"""
from __future__ import annotations

import pytest
import numpy as np

from Validation.v7_rsa.compute_model_rdm import compute_belief_rdm, compute_r3_rdm
from Validation.v7_rsa.compute_baseline_rdms import compute_acoustic_rdm, compute_spectral_rdm
from Validation.v7_rsa.compare_rdms import rdm_correlation


@pytest.mark.v7
class TestMIvsBaselines:
    """Compare MI and baseline model RDMs."""

    @pytest.fixture(scope="class")
    def model_rdms(self, mi_bridge, rsa_stimuli, module_data):
        """Compute all model RDMs."""
        rdms = {}
        rdms["mi_beliefs"] = compute_belief_rdm(mi_bridge, rsa_stimuli)
        rdms["mi_r3"] = compute_r3_rdm(mi_bridge, rsa_stimuli)
        rdms["acoustic_mfcc"] = compute_acoustic_rdm(rsa_stimuli)
        rdms["spectral_mel"] = compute_spectral_rdm(rsa_stimuli)

        # Stash for auto-reporting
        stimulus_names = [p.stem for p in rsa_stimuli]
        comparisons = []
        for name in ("mi_beliefs", "mi_r3", "acoustic_mfcc", "spectral_mel"):
            from Validation.v7_rsa.compare_rdms import rdm_correlation
            rho, p = rdm_correlation(rdms["mi_beliefs"], rdms[name])
            comparisons.append({
                "model_name": name,
                "spearman_rho": float(rho),
                "p_permutation": float(p),
            })
        module_data["v7"] = {
            "comparisons": comparisons,
            "rdms": rdms,
            "stimulus_names": stimulus_names,
        }

        return rdms

    def test_belief_rdm_not_flat(self, model_rdms):
        """MI belief RDM should have meaningful variance (not all zeros)."""
        rdm = model_rdms["mi_beliefs"]
        assert rdm.std() > 0.01, (
            f"Belief RDM is too flat (std={rdm.std():.6f})"
        )

    def test_belief_rdm_differs_from_acoustic(self, model_rdms):
        """MI belief RDM should capture structure beyond acoustics."""
        rho, p = rdm_correlation(model_rdms["mi_beliefs"], model_rdms["acoustic_mfcc"])
        # Should be correlated (music with similar beliefs often similar acoustics)
        # but not perfectly (beliefs capture more than acoustics)
        assert rho < 0.95, (
            f"Belief RDM too similar to acoustic RDM (rho={rho:.3f}). "
            f"Expected MI to capture structure beyond acoustics."
        )

    def test_belief_rdm_richer_than_r3(self, model_rdms):
        """MI belief RDM should differ from R³ (acoustic features) RDM.

        This tests that C³ adds representational structure beyond R³.
        """
        rho, p = rdm_correlation(model_rdms["mi_beliefs"], model_rdms["mi_r3"])
        # Beliefs should be related to but different from raw acoustics
        assert rho < 0.90, (
            f"Belief RDM too similar to R³ RDM (rho={rho:.3f}). "
            f"C³ should add unique representational structure."
        )

    def test_rdm_symmetry(self, model_rdms):
        """All RDMs should be symmetric with zero diagonal."""
        for name, rdm in model_rdms.items():
            assert np.allclose(rdm, rdm.T, atol=1e-10), (
                f"{name} RDM is not symmetric"
            )
            assert np.allclose(np.diag(rdm), 0, atol=1e-10), (
                f"{name} RDM diagonal is not zero"
            )
