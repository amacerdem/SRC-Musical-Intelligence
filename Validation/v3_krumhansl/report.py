"""V3 Krumhansl — report generation and figure creation."""
from __future__ import annotations

from pathlib import Path

import numpy as np

from Validation.config.paths import V3_RESULTS
from Validation.infrastructure.figures import apply_nature_style, save_figure
from Validation.infrastructure.stats import pearson_with_ci, spearman_with_ci
from Validation.v3_krumhansl.profiles import (
    MAJOR_PROFILE,
    MINOR_PROFILE,
    PITCH_CLASS_NAMES,
)


def generate_profile_comparison_figure(
    mi_major: np.ndarray,
    mi_minor: np.ndarray,
    name: str = "v3_tonal_profiles",
) -> Path:
    """Generate dual panel comparing MI and K-K tonal profiles."""
    import matplotlib.pyplot as plt

    apply_nature_style()
    fig, axes = plt.subplots(1, 2, figsize=(7, 3))

    x = np.arange(12)
    width = 0.35

    # Major
    kk_norm = MAJOR_PROFILE / MAJOR_PROFILE.max()
    mi_norm = mi_major / mi_major.max() if mi_major.max() > 0 else mi_major

    r_maj, p_maj, ci_maj = pearson_with_ci(mi_major, MAJOR_PROFILE)

    axes[0].bar(x - width / 2, kk_norm, width, label="Krumhansl-Kessler",
                color="#2171b5", edgecolor="black", linewidth=0.3)
    axes[0].bar(x + width / 2, mi_norm, width, label="MI System",
                color="#cb181d", edgecolor="black", linewidth=0.3)
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(PITCH_CLASS_NAMES, fontsize=6)
    axes[0].set_ylabel("Normalized Rating")
    axes[0].set_title(f"Major Key (r = {r_maj:.3f}, p = {p_maj:.2e})")
    axes[0].legend(fontsize=5)

    # Minor
    kk_norm_m = MINOR_PROFILE / MINOR_PROFILE.max()
    mi_norm_m = mi_minor / mi_minor.max() if mi_minor.max() > 0 else mi_minor

    r_min, p_min, ci_min = pearson_with_ci(mi_minor, MINOR_PROFILE)

    axes[1].bar(x - width / 2, kk_norm_m, width, label="Krumhansl-Kessler",
                color="#2171b5", edgecolor="black", linewidth=0.3)
    axes[1].bar(x + width / 2, mi_norm_m, width, label="MI System",
                color="#cb181d", edgecolor="black", linewidth=0.3)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(PITCH_CLASS_NAMES, fontsize=6)
    axes[1].set_title(f"Minor Key (r = {r_min:.3f}, p = {p_min:.2e})")
    axes[1].legend(fontsize=5)

    fig.suptitle("Tonal Hierarchy: MI vs. Krumhansl-Kessler 1982", fontsize=9)
    fig.tight_layout()

    paths = save_figure(fig, name, subdir="v3_krumhansl")
    return paths[0]


def generate_summary_report(
    mi_major: np.ndarray,
    mi_minor: np.ndarray,
) -> str:
    """Generate V3 validation summary."""
    r_maj, p_maj, ci_maj = pearson_with_ci(mi_major, MAJOR_PROFILE)
    r_min, p_min, ci_min = pearson_with_ci(mi_minor, MINOR_PROFILE)
    rho_maj, _, _ = spearman_with_ci(mi_major, MAJOR_PROFILE)
    rho_min, _, _ = spearman_with_ci(mi_minor, MINOR_PROFILE)

    lines = [
        "=" * 60,
        "V3 TONAL HIERARCHY VALIDATION — SUMMARY",
        "=" * 60,
        "",
        "Major Key Profile:",
        f"  Pearson r  = {r_maj:.4f}  (p = {p_maj:.2e})",
        f"  95% CI     = [{ci_maj[0]:.4f}, {ci_maj[1]:.4f}]",
        f"  Spearman ρ = {rho_maj:.4f}",
        "",
        "Minor Key Profile:",
        f"  Pearson r  = {r_min:.4f}  (p = {p_min:.2e})",
        f"  95% CI     = [{ci_min[0]:.4f}, {ci_min[1]:.4f}]",
        f"  Spearman ρ = {rho_min:.4f}",
        "",
        "─── Profile Details (Normalized) ───",
        "",
        f"  {'PC':>4s}  {'K-K Maj':>8s}  {'MI Maj':>8s}  {'K-K Min':>8s}  {'MI Min':>8s}",
    ]

    kk_maj_n = MAJOR_PROFILE / MAJOR_PROFILE.max()
    mi_maj_n = mi_major / mi_major.max() if mi_major.max() > 0 else mi_major
    kk_min_n = MINOR_PROFILE / MINOR_PROFILE.max()
    mi_min_n = mi_minor / mi_minor.max() if mi_minor.max() > 0 else mi_minor

    for i, name in enumerate(PITCH_CLASS_NAMES):
        lines.append(
            f"  {name:>4s}  {kk_maj_n[i]:8.4f}  {mi_maj_n[i]:8.4f}  "
            f"{kk_min_n[i]:8.4f}  {mi_min_n[i]:8.4f}"
        )

    lines.extend(["", "=" * 60])

    report = "\n".join(lines)
    V3_RESULTS.mkdir(parents=True, exist_ok=True)
    (V3_RESULTS / "v3_summary.txt").write_text(report)
    return report
