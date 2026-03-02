"""Pharmacological simulation engine — modify neurochemical gains and compare.

Runs the MI pipeline under different pharmacological conditions (levodopa,
risperidone, naltrexone, placebo) and extracts the relevant outcome measures.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np

from Validation.infrastructure.mi_bridge import MIBridge, ValidationResult
from Validation.v1_pharmacology.targets import PharmTarget


@dataclass
class PharmSimResult:
    """Result of a single pharmacological simulation."""
    target: PharmTarget
    mi_result: ValidationResult
    reward_mean: float
    emotion_mean: float
    arousal_mean: float
    valence_mean: float
    da_mean: float
    opi_mean: float
    ne_mean: float
    sht_mean: float


class PharmacologicalSimulator:
    """Simulate pharmacological manipulations on MI's neurochemical system.

    Modifies DA/NE/OPI/5HT gains in the accumulation step,
    then compares output measures against baseline (placebo).
    """

    def __init__(self, bridge: MIBridge):
        self.bridge = bridge

    def simulate(
        self,
        audio_path: str | Path,
        target: PharmTarget,
        excerpt_s: float = 30.0,
    ) -> PharmSimResult:
        """Run MI with pharmacological modification for a single target.

        Args:
            audio_path: Path to audio stimulus.
            target: Pharmacological target with gain specification.
            excerpt_s: Max audio duration.

        Returns:
            PharmSimResult with all outcome measures.
        """
        # Build gain dict
        gains = {"DA": 1.0, "NE": 1.0, "OPI": 1.0, "5HT": 1.0}
        gains[target.mi_channel] = target.mi_gain

        # Run pipeline with modified neurochemistry
        result = self.bridge.run_with_modified_neuro(
            audio_path, excerpt_s,
            da_gain=gains["DA"],
            ne_gain=gains["NE"],
            opi_gain=gains["OPI"],
            sht_gain=gains["5HT"],
        )

        # Extract outcome measures
        reward_mean = float(result.reward.mean())

        # Ψ³ emotion domain mean intensity
        emotion_mean = float(result.psi["emotion"].mean()) if "emotion" in result.psi else 0.0

        # Ψ³ affect: [0]=valence, [1]=arousal (first two dims of affect domain)
        affect = result.psi.get("affect", np.zeros((1, 4)))
        valence_mean = float(affect[:, 0].mean()) if affect.shape[-1] > 0 else 0.0
        arousal_mean = float(affect[:, 1].mean()) if affect.shape[-1] > 1 else 0.0

        # Neurochemical state means
        neuro = result.neuro  # (T, 4)
        da_mean = float(neuro[:, 0].mean())
        ne_mean = float(neuro[:, 1].mean())
        opi_mean = float(neuro[:, 2].mean())
        sht_mean = float(neuro[:, 3].mean())

        return PharmSimResult(
            target=target,
            mi_result=result,
            reward_mean=reward_mean,
            emotion_mean=emotion_mean,
            arousal_mean=arousal_mean,
            valence_mean=valence_mean,
            da_mean=da_mean,
            opi_mean=opi_mean,
            ne_mean=ne_mean,
            sht_mean=sht_mean,
        )

    def simulate_battery(
        self,
        audio_path: str | Path,
        targets: List[PharmTarget],
        excerpt_s: float = 30.0,
    ) -> List[PharmSimResult]:
        """Run a battery of pharmacological simulations.

        Args:
            audio_path: Audio stimulus path.
            targets: List of pharmacological targets.
            excerpt_s: Max duration.

        Returns:
            List of simulation results.
        """
        results = []
        for target in targets:
            print(f"[V1] Simulating {target.drug} ({target.mechanism})...")
            result = self.simulate(audio_path, target, excerpt_s)
            results.append(result)
        return results

    @staticmethod
    def compare_to_baseline(
        drug_result: PharmSimResult,
        baseline_result: PharmSimResult,
        measure: str = "reward",
    ) -> Dict[str, float]:
        """Compare a drug condition to baseline (placebo).

        Args:
            drug_result: Result under drug condition.
            baseline_result: Result under placebo/baseline.
            measure: Which measure to compare.

        Returns:
            Dict with delta, percent_change, and direction.
        """
        measure_map = {
            "reward": ("reward_mean", "reward_mean"),
            "emotion": ("emotion_mean", "emotion_mean"),
            "arousal": ("arousal_mean", "arousal_mean"),
            "valence": ("valence_mean", "valence_mean"),
        }

        drug_attr, base_attr = measure_map[measure]
        drug_val = getattr(drug_result, drug_attr)
        base_val = getattr(baseline_result, base_attr)

        delta = drug_val - base_val
        pct_change = (delta / abs(base_val) * 100) if base_val != 0 else 0.0
        direction = "increase" if delta > 0 else "decrease" if delta < 0 else "unchanged"

        return {
            "drug_value": drug_val,
            "baseline_value": base_val,
            "delta": delta,
            "percent_change": pct_change,
            "direction": direction,
        }

    @staticmethod
    def check_direction(
        comparison: Dict[str, float],
        expected: str,
    ) -> bool:
        """Check if the observed direction matches the expected direction.

        Args:
            comparison: Output from compare_to_baseline.
            expected: 'increase', 'decrease', 'preserved', or 'baseline'.

        Returns:
            True if direction matches expectation.
        """
        if expected == "baseline":
            return True  # baseline always matches itself
        if expected == "preserved":
            return abs(comparison["percent_change"]) < 15.0  # <15% change = preserved
        return comparison["direction"] == expected
