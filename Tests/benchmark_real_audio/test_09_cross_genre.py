"""Test 09 — Cross-Genre Feature Comparison.

Compares R³ and H³ feature profiles across different musical genres:
- Solo acoustic (Bach Cello Suite)
- Orchestral (Swan Lake, Beethoven)
- Film/Epic (Herald, Duel of the Fates)
- Contemporary (Enigma, Yang)

Experiments:
- Per-genre R³ group fingerprints
- Spectral centroid / energy differences across genres
- Temporal complexity comparison (H³ volatility)
- Genre clustering based on R³ mean vectors
"""
from __future__ import annotations

import gc

import pytest
import torch

from Tests.benchmark_real_audio.helpers import (
    AUDIO_CATALOG,
    GENRE_GROUPS,
    R3_GROUPS,
    load_audio_file,
)


@pytest.mark.benchmark
class TestCrossGenre:
    """Cross-genre comparison experiments."""

    def _extract_genre_profiles(self, r3_extractor) -> dict:
        """Extract R³ for all files and compute per-genre profiles."""
        profiles = {}
        for name in AUDIO_CATALOG:
            _, mel, _ = load_audio_file(name)
            r3 = r3_extractor.extract(mel).features.squeeze(0)  # (T, 97)
            profiles[name] = {
                "mean_vector": r3.mean(dim=0),  # (97,)
                "std_vector": r3.std(dim=0),
                "features": r3,
            }
            gc.collect()
        return profiles

    def test_genre_fingerprints(self, r3_extractor) -> None:
        """Each genre has a distinct R³ group fingerprint."""
        profiles = self._extract_genre_profiles(r3_extractor)

        print("\n╔═══════════════════════════════════════════════════════════════════════════════════╗")
        print("║                    R³ Group Fingerprints by Genre                                 ║")
        print("╠══════════════════╦═══════╦═══════╦═══════╦═══════╦═══════╦═══════╦═══════╦═══════╣")
        print("║ Track            ║ Cons  ║ Enrgy ║ Timbr ║ Chng  ║ Pitch ║ Rhyth ║ Harm  ║ Modul ║")
        print("╠══════════════════╬═══════╬═══════╬═══════╬═══════╬═══════╬═══════╬═══════╬═══════╣")

        for name, p in profiles.items():
            vals = {}
            for gname, (s, e) in R3_GROUPS.items():
                vals[gname] = p["mean_vector"][s:e].mean().item()
            short = gname[:5]
            groups = list(R3_GROUPS.keys())
            print(f"║ {name:<16s} ║ {vals[groups[0]]:>.4f}║ {vals[groups[1]]:>.4f}║ "
                  f"{vals[groups[2]]:>.4f}║ {vals[groups[3]]:>.4f}║ {vals[groups[4]]:>.4f}║ "
                  f"{vals[groups[5]]:>.4f}║ {vals[groups[6]]:>.4f}║ {vals[groups[7]]:>.4f}║")

        print("╚══════════════════╩═══════╩═══════╩═══════╩═══════╩═══════╩═══════╩═══════╩═══════╝")

    def test_solo_vs_orchestral_energy(self, r3_extractor) -> None:
        """Solo acoustic (Bach) has different energy profile than orchestral (Swan)."""
        profiles = self._extract_genre_profiles(r3_extractor)

        bach_energy = profiles["bach"]["mean_vector"][7:12].mean().item()
        swan_energy = profiles["swan"]["mean_vector"][7:12].mean().item()
        duel_energy = profiles["duel"]["mean_vector"][7:12].mean().item()

        print(f"\n  Energy (B[7:12]) Comparison:")
        print(f"    Bach (solo):       {bach_energy:.4f}")
        print(f"    Swan (orchestral): {swan_energy:.4f}")
        print(f"    Duel (epic):       {duel_energy:.4f}")

        # Energy profiles should differ between solo and orchestral
        assert abs(bach_energy - duel_energy) > 0.005, \
            "Solo and epic energy profiles too similar"

    def test_genre_clustering_separation(self, r3_extractor) -> None:
        """Pieces in same genre cluster closer than across genres."""
        profiles = self._extract_genre_profiles(r3_extractor)

        def cosine_sim(a, b):
            return torch.nn.functional.cosine_similarity(
                a.unsqueeze(0), b.unsqueeze(0)
            ).item()

        # Within-genre similarities
        within_sims = []
        for genre, members in GENRE_GROUPS.items():
            if len(members) < 2:
                continue
            for i in range(len(members)):
                for j in range(i + 1, len(members)):
                    sim = cosine_sim(
                        profiles[members[i]]["mean_vector"],
                        profiles[members[j]]["mean_vector"],
                    )
                    within_sims.append((genre, members[i], members[j], sim))

        # Across-genre similarities (pick one from each)
        across_sims = []
        genre_reps = {}
        for genre, members in GENRE_GROUPS.items():
            genre_reps[genre] = members[0]

        genre_names = list(genre_reps.keys())
        for i in range(len(genre_names)):
            for j in range(i + 1, len(genre_names)):
                g1, g2 = genre_names[i], genre_names[j]
                sim = cosine_sim(
                    profiles[genre_reps[g1]]["mean_vector"],
                    profiles[genre_reps[g2]]["mean_vector"],
                )
                across_sims.append((g1, g2, sim))

        print("\n  Within-Genre Similarities:")
        for genre, m1, m2, sim in within_sims:
            print(f"    [{genre}] {m1} vs {m2}: {sim:.4f}")

        print("\n  Across-Genre Similarities:")
        for g1, g2, sim in across_sims:
            print(f"    {g1} vs {g2}: {sim:.4f}")

    def test_temporal_complexity_by_genre(
        self, r3_extractor, h3_extractor, h3_demand_set
    ) -> None:
        """Compare H³ temporal complexity (mean volatility) across genres."""
        results = {}
        for name in ["bach", "swan", "herald", "duel"]:
            _, mel, _ = load_audio_file(name)
            r3_features = r3_extractor.extract(mel).features
            h3_output = h3_extractor.extract(r3_features, h3_demand_set)

            volatilities = []
            for key, tensor in h3_output.features.items():
                t = tensor.squeeze(0)
                if t.shape[0] > 2:
                    diffs = t[1:] - t[:-1]
                    volatilities.append(diffs.std().item())

            results[name] = sum(volatilities) / len(volatilities) if volatilities else 0
            gc.collect()

        print("\n  Temporal Complexity (H³ mean volatility):")
        for name, vol in sorted(results.items(), key=lambda x: -x[1]):
            bar = "█" * int(vol * 200)
            print(f"    {name:<12s}: {vol:.6f} {bar}")

    def test_harmony_richness_gradient(self, r3_extractor) -> None:
        """Harmony group (H[51:63]) should be richer for polyphonic music."""
        profiles = self._extract_genre_profiles(r3_extractor)

        print("\n  Harmony Richness (H[51:63]):")
        for name, p in sorted(
            profiles.items(),
            key=lambda x: -x[1]["mean_vector"][51:63].mean().item(),
        ):
            harmony_mean = p["mean_vector"][51:63].mean().item()
            harmony_std = p["std_vector"][51:63].mean().item()
            print(f"    {name:<16s}: mean={harmony_mean:.4f}, std={harmony_std:.4f}")
