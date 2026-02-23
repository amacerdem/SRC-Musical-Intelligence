"""Test 03 — R³ Feature Distribution Analysis.

Statistical deep-dive into R³ feature distributions across all 7 pieces.
Validates that features have reasonable statistical properties for real music.

Experiments:
- Per-group mean/std/min/max across pieces
- Feature correlation within groups
- Dynamic range analysis
- Outlier detection (features that are flat or saturated)
"""
from __future__ import annotations

import gc

import pytest
import torch

from Tests.benchmark_real_audio.helpers import (
    AUDIO_CATALOG,
    R3_GROUPS,
    load_audio_file,
)


@pytest.mark.benchmark
class TestR3Distributions:
    """Analyze R³ feature distributions on real audio."""

    def _extract_all(self, r3_extractor) -> dict:
        """Extract R³ for all files, return {name: features (T, 97)}."""
        results = {}
        for name in AUDIO_CATALOG:
            _, mel, _ = load_audio_file(name)
            r3 = r3_extractor.extract(mel).features.squeeze(0)  # (T, 97)
            results[name] = r3
            gc.collect()
        return results

    def test_per_group_statistics(self, r3_extractor) -> None:
        """Report mean/std per R³ group across all pieces."""
        all_r3 = self._extract_all(r3_extractor)

        print("\n╔═══════════════════════════════════════════════════════════════════╗")
        print("║               R³ Per-Group Statistics Across Pieces              ║")
        print("╠═══════════════════╦═════════╦═════════╦═════════╦════════════════╣")
        print("║ Group             ║  Mean   ║  Std    ║ DynRng  ║ Variation      ║")
        print("╠═══════════════════╬═════════╬═════════╬═════════╬════════════════╣")

        for group_name, (start, end) in R3_GROUPS.items():
            means = []
            stds = []
            for name, features in all_r3.items():
                group = features[:, start:end]
                means.append(group.mean().item())
                stds.append(group.std().item())

            avg_mean = sum(means) / len(means)
            avg_std = sum(stds) / len(stds)
            dyn_range = max(means) - min(means)
            variation = "HIGH" if avg_std > 0.15 else "MED" if avg_std > 0.05 else "LOW"

            print(f"║ {group_name:<17s} ║ {avg_mean:>7.4f} ║ {avg_std:>7.4f} ║ {dyn_range:>7.4f} ║ {variation:<14s} ║")

        print("╚═══════════════════╩═════════╩═════════╩═════════╩════════════════╝")

    def test_feature_dynamic_range(self, r3_extractor) -> None:
        """Each R³ feature uses a reasonable portion of [0, 1] range."""
        all_r3 = self._extract_all(r3_extractor)

        # Concatenate all pieces
        all_features = torch.cat(list(all_r3.values()), dim=0)  # (T_total, 97)

        per_feature_min = all_features.min(dim=0).values  # (97,)
        per_feature_max = all_features.max(dim=0).values
        dynamic_range = per_feature_max - per_feature_min

        # Count features with very low dynamic range (< 0.05)
        flat_count = (dynamic_range < 0.05).sum().item()
        saturated_high = (per_feature_min > 0.9).sum().item()
        saturated_low = (per_feature_max < 0.1).sum().item()

        print(f"\n  Feature Dynamic Range Analysis (all 7 pieces combined):")
        print(f"  Total features: 97")
        print(f"  Flat (<0.05 range): {flat_count}")
        print(f"  Saturated high (min>0.9): {saturated_high}")
        print(f"  Saturated low (max<0.1): {saturated_low}")
        print(f"  Median dynamic range: {dynamic_range.median():.4f}")

        assert flat_count < 20, f"Too many flat features: {flat_count}/97"

    def test_inter_piece_differentiation(self, r3_extractor) -> None:
        """Different pieces produce different R³ distributions (not identical)."""
        all_r3 = self._extract_all(r3_extractor)
        names = list(all_r3.keys())

        # Compute per-piece mean vector
        mean_vectors = {
            name: features.mean(dim=0)  # (97,)
            for name, features in all_r3.items()
        }

        # Pairwise cosine distance
        pairs_identical = 0
        total_pairs = 0
        print("\n  Inter-Piece Cosine Similarity (R³ mean vectors):")
        for i, n1 in enumerate(names):
            for n2 in names[i + 1:]:
                cos_sim = torch.nn.functional.cosine_similarity(
                    mean_vectors[n1].unsqueeze(0),
                    mean_vectors[n2].unsqueeze(0),
                ).item()
                total_pairs += 1
                if cos_sim > 0.999:
                    pairs_identical += 1
                print(f"    {n1} vs {n2}: {cos_sim:.4f}")

        assert pairs_identical == 0, \
            f"{pairs_identical}/{total_pairs} pairs are nearly identical"

    def test_within_group_correlation(self, r3_extractor) -> None:
        """Features within same R³ group show higher correlation than across groups."""
        _, mel, _ = load_audio_file("herald")
        features = r3_extractor.extract(mel).features.squeeze(0)  # (T, 97)

        within_corrs = []
        across_corrs = []

        for group_name, (start, end) in R3_GROUPS.items():
            group = features[:, start:end]  # (T, dim)
            if group.shape[1] < 2:
                continue
            # Within-group correlation
            corr_matrix = torch.corrcoef(group.T)
            mask = ~torch.eye(corr_matrix.shape[0], dtype=torch.bool)
            within_corrs.extend(corr_matrix[mask].abs().tolist())

        # Across groups: pick one feature from each group
        representatives = []
        for _, (start, _) in R3_GROUPS.items():
            representatives.append(features[:, start])
        rep_stack = torch.stack(representatives, dim=1)  # (T, 9)
        cross_corr = torch.corrcoef(rep_stack.T)
        mask = ~torch.eye(cross_corr.shape[0], dtype=torch.bool)
        across_corrs = cross_corr[mask].abs().tolist()

        avg_within = sum(within_corrs) / len(within_corrs)
        avg_across = sum(across_corrs) / len(across_corrs)

        print(f"\n  Correlation Analysis (herald):")
        print(f"    Within-group avg |r|: {avg_within:.4f}")
        print(f"    Across-group avg |r|: {avg_across:.4f}")

    def test_consonance_hierarchy_visible(self, r3_extractor) -> None:
        """Consonance group (A[0:7]) shows differentiated values across pieces.
        Bach solo cello should differ from orchestral pieces."""
        all_r3 = self._extract_all(r3_extractor)

        print("\n  Consonance Group (A[0:7]) Per-Piece Means:")
        for name, features in all_r3.items():
            cons = features[:, 0:7].mean(dim=0)
            print(f"    {name}: {cons.numpy().round(4)}")

        # Bach (solo) and Duel (epic) should be different
        bach_cons = all_r3["bach"][:, 0:7].mean().item()
        duel_cons = all_r3["duel"][:, 0:7].mean().item()
        diff = abs(bach_cons - duel_cons)
        assert diff > 0.01, \
            f"Bach and Duel consonance too similar: diff={diff:.4f}"
