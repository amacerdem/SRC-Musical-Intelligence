"""
TemporalConstraintChecker — Validates neuroscience temporal predictions.

Scientific basis:
  - Wanting (caudate DA) should lead liking (NAcc DA) by ~200-500ms (Salimpoor 2011)
  - Appraisal (ITPRA-A) should lag pleasure by ~500-2000ms (Huron 2006)
  - Prediction error should peak before reward (Schultz 2016)
"""

from __future__ import annotations

import torch
from torch import Tensor

from ..core.types import ModelOutput


def wanting_leads_liking(output: ModelOutput, min_lag_frames: int = 34) -> bool:
    """Check that wanting (da_caudate) peaks before liking (da_nacc).

    Salimpoor 2011: caudate DA peaks during anticipation,
    NAcc DA peaks during consummation. The caudate signal should
    consistently lead the NAcc signal.

    Args:
        output: SRP ModelOutput with 19D tensor (B, T, 19)
        min_lag_frames: minimum expected lag in frames (~200ms at 172Hz)

    Returns:
        True if the temporal constraint holds
    """
    tensor = output.tensor.squeeze(0)  # (T, 19)

    da_caudate = tensor[:, 0]  # N0
    da_nacc = tensor[:, 1]     # N1

    caudate_peak = torch.argmax(da_caudate).item()
    nacc_peak = torch.argmax(da_nacc).item()

    return caudate_peak + min_lag_frames <= nacc_peak


def appraisal_lags_pleasure(output: ModelOutput, min_lag_frames: int = 86) -> bool:
    """Check that appraisal lags pleasure onset.

    Huron 2006 ITPRA: Appraisal (A) is the slowest component,
    occurring 0.5-2s after the event. Pleasure should precede
    conscious appraisal.

    Args:
        output: SRP ModelOutput with 19D tensor
        min_lag_frames: minimum expected lag (~500ms)

    Returns:
        True if appraisal onset lags pleasure onset
    """
    tensor = output.tensor.squeeze(0)  # (T, 19)

    pleasure = tensor[:, 8]      # P2
    appraisal = tensor[:, 12]    # T3 (appraisal)

    # Find onset: first frame exceeding 50% of peak
    pleasure_threshold = pleasure.max() * 0.5
    appraisal_threshold = appraisal.max() * 0.5

    pleasure_onset = (pleasure > pleasure_threshold).nonzero(as_tuple=True)[0]
    appraisal_onset = (appraisal > appraisal_threshold).nonzero(as_tuple=True)[0]

    if len(pleasure_onset) == 0 or len(appraisal_onset) == 0:
        return False

    return appraisal_onset[0].item() >= pleasure_onset[0].item() + min_lag_frames


def prediction_error_precedes_reward(output: ModelOutput) -> bool:
    """Check that prediction error peak precedes reward peak.

    Schultz 2016: RPE signals are computed before reward
    is fully experienced.

    Args:
        output: SRP ModelOutput with 19D tensor

    Returns:
        True if prediction_error peaks before pleasure
    """
    tensor = output.tensor.squeeze(0)  # (T, 19)

    prediction_error = tensor[:, 5].abs()  # C2 (prediction_error, signed)
    pleasure = tensor[:, 8]                # P2

    pe_peak = torch.argmax(prediction_error).item()
    pleasure_peak = torch.argmax(pleasure).item()

    return pe_peak <= pleasure_peak


def check_all(output: ModelOutput) -> dict[str, bool]:
    """Run all temporal constraint checks.

    Args:
        output: SRP ModelOutput

    Returns:
        Dict of constraint name → pass/fail
    """
    return {
        "wanting_leads_liking": wanting_leads_liking(output),
        "appraisal_lags_pleasure": appraisal_lags_pleasure(output),
        "prediction_error_precedes_reward": prediction_error_precedes_reward(output),
    }
