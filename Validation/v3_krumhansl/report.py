"""V3 Krumhansl — comprehensive report generation and figure creation."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats as sp_stats

from Validation.config.paths import V3_RESULTS
from Validation.infrastructure.figures import (
    apply_nature_style,
    bar_comparison,
    correlation_scatter,
    save_figure,
)
from Validation.infrastructure.stats import (
    pearson_with_ci,
    permutation_test,
    spearman_with_ci,
)
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
    """Generate comprehensive V3 tonal hierarchy report.

    Includes correlations with CI, permutation tests, Kendall's tau,
    residual analysis, effect size conversion, and hierarchy concordance.
    """
    r_maj, p_maj, ci_maj = pearson_with_ci(mi_major, MAJOR_PROFILE)
    r_min, p_min, ci_min = pearson_with_ci(mi_minor, MINOR_PROFILE)
    rho_maj, p_rho_maj, ci_rho_maj = spearman_with_ci(mi_major, MAJOR_PROFILE)
    rho_min, p_rho_min, ci_rho_min = spearman_with_ci(mi_minor, MINOR_PROFILE)

    # Permutation tests
    _, perm_p_maj = permutation_test(mi_major, MAJOR_PROFILE, stat_func="pearson")
    _, perm_p_min = permutation_test(mi_minor, MINOR_PROFILE, stat_func="pearson")

    # Kendall's tau
    tau_maj, p_tau_maj = sp_stats.kendalltau(mi_major, MAJOR_PROFILE)
    tau_min, p_tau_min = sp_stats.kendalltau(mi_minor, MINOR_PROFILE)

    # r-to-d conversion
    d_maj = 2 * r_maj / np.sqrt(1 - r_maj ** 2) if abs(r_maj) < 0.9999 else float("inf")
    d_min = 2 * r_min / np.sqrt(1 - r_min ** 2) if abs(r_min) < 0.9999 else float("inf")

    lines = [
        "=" * 78,
        "V3 TONAL HIERARCHY VALIDATION — COMPREHENSIVE REPORT",
        "=" * 78,
        "",
        "─── Major Key Profile ───",
        "",
        f"  Pearson r:       {r_maj:.4f}   p = {p_maj:.2e}   95% CI [{ci_maj[0]:.4f}, {ci_maj[1]:.4f}]",
        f"  Spearman ρ:      {rho_maj:.4f}   p = {p_rho_maj:.2e}   95% CI [{ci_rho_maj[0]:.4f}, {ci_rho_maj[1]:.4f}]",
        f"  Kendall τ:       {tau_maj:.4f}   p = {p_tau_maj:.2e}",
        f"  Permutation p:   {perm_p_maj:.4f}   (10,000 permutations)",
        f"  Cohen's d (r→d): {d_maj:+.3f}",
        "",
        "─── Minor Key Profile ───",
        "",
        f"  Pearson r:       {r_min:.4f}   p = {p_min:.2e}   95% CI [{ci_min[0]:.4f}, {ci_min[1]:.4f}]",
        f"  Spearman ρ:      {rho_min:.4f}   p = {p_rho_min:.2e}   95% CI [{ci_rho_min[0]:.4f}, {ci_rho_min[1]:.4f}]",
        f"  Kendall τ:       {tau_min:.4f}   p = {p_tau_min:.2e}",
        f"  Permutation p:   {perm_p_min:.4f}   (10,000 permutations)",
        f"  Cohen's d (r→d): {d_min:+.3f}",
        "",
    ]

    # Normalized profile table
    kk_maj_n = MAJOR_PROFILE / MAJOR_PROFILE.max()
    mi_maj_n = mi_major / mi_major.max() if mi_major.max() > 0 else mi_major
    kk_min_n = MINOR_PROFILE / MINOR_PROFILE.max()
    mi_min_n = mi_minor / mi_minor.max() if mi_minor.max() > 0 else mi_minor

    resid_maj = mi_maj_n - kk_maj_n
    resid_min = mi_min_n - kk_min_n

    lines.extend([
        "─── Profile Details (Normalized) ───",
        "",
        f"  {'PC':>4s}  {'K-K Maj':>8s}  {'MI Maj':>8s}  {'Resid':>8s}  "
        f"{'K-K Min':>8s}  {'MI Min':>8s}  {'Resid':>8s}",
        f"  {'─'*4}  {'─'*8}  {'─'*8}  {'─'*8}  "
        f"{'─'*8}  {'─'*8}  {'─'*8}",
    ])

    for i, pc_name in enumerate(PITCH_CLASS_NAMES):
        lines.append(
            f"  {pc_name:>4s}  {kk_maj_n[i]:8.4f}  {mi_maj_n[i]:8.4f}  {resid_maj[i]:+8.4f}  "
            f"{kk_min_n[i]:8.4f}  {mi_min_n[i]:8.4f}  {resid_min[i]:+8.4f}"
        )

    # Residual analysis
    lines.extend(["", "─── Residual Analysis ───", ""])

    # Largest deviations
    top3_maj = np.argsort(np.abs(resid_maj))[::-1][:3]
    top3_min = np.argsort(np.abs(resid_min))[::-1][:3]

    lines.append("  Largest major-key deviations:")
    for idx in top3_maj:
        lines.append(f"    {PITCH_CLASS_NAMES[idx]:>4s}: {resid_maj[idx]:+.4f}")
    lines.append("  Largest minor-key deviations:")
    for idx in top3_min:
        lines.append(f"    {PITCH_CLASS_NAMES[idx]:>4s}: {resid_min[idx]:+.4f}")

    lines.extend([
        "",
        f"  Major RMSE: {np.sqrt(np.mean(resid_maj**2)):.4f}",
        f"  Minor RMSE: {np.sqrt(np.mean(resid_min**2)):.4f}",
        f"  Major MAE:  {np.mean(np.abs(resid_maj)):.4f}",
        f"  Minor MAE:  {np.mean(np.abs(resid_min)):.4f}",
    ])

    # Hierarchy concordance
    lines.extend(_hierarchy_concordance(mi_major, mi_minor))

    lines.extend(["", "=" * 78])

    report = "\n".join(lines)
    V3_RESULTS.mkdir(parents=True, exist_ok=True)
    (V3_RESULTS / "v3_summary.txt").write_text(report)
    print(f"[V3] Report saved: {V3_RESULTS / 'v3_summary.txt'}")

    # Generate figures
    try:
        generate_profile_comparison_figure(mi_major, mi_minor)
        _generate_residual_figure(resid_maj, resid_min)
        _generate_scatter_figures(mi_major, mi_minor)
        print(f"[V3] 4 figures saved to: figures/v3_krumhansl/")
    except Exception as e:
        print(f"[V3] Figure generation failed: {e}")

    return report


def _hierarchy_concordance(mi_major: np.ndarray, mi_minor: np.ndarray) -> list[str]:
    """Check if MI preserves the expected tonal hierarchy."""
    lines = ["", "─── Hierarchy Concordance ───", ""]

    # Major: tonic(C=0) > dominant(G=7) > mediant(E=4) > subdominant(F=5)
    hierarchy_checks = [
        ("Major: C > G (tonic > dominant)", mi_major[0], mi_major[7]),
        ("Major: G > E (dominant > mediant)", mi_major[7], mi_major[4]),
        ("Major: E > F (mediant > subdominant)", mi_major[4], mi_major[5]),
        ("Major: C > F# (tonic > tritone)", mi_major[0], mi_major[6]),
        ("Minor: C > G (tonic > dominant)", mi_minor[0], mi_minor[7]),
        ("Minor: Eb > E (minor 3rd > major 3rd)", mi_minor[3], mi_minor[4]),
    ]

    n_pass = 0
    for label, higher, lower in hierarchy_checks:
        ok = higher > lower
        if ok:
            n_pass += 1
        lines.append(f"  {'✓' if ok else '✗'} {label}: {higher:.4f} vs {lower:.4f}")

    lines.append(f"\n  Hierarchy score: {n_pass}/{len(hierarchy_checks)}")
    return lines


def _generate_residual_figure(resid_maj: np.ndarray, resid_min: np.ndarray) -> None:
    """Bar chart of residuals per pitch class."""
    apply_nature_style()
    fig, axes = plt.subplots(1, 2, figsize=(7, 3))

    x = np.arange(12)
    colors_maj = ["#238b45" if r > 0 else "#cb181d" for r in resid_maj]
    colors_min = ["#238b45" if r > 0 else "#cb181d" for r in resid_min]

    axes[0].bar(x, resid_maj, color=colors_maj, edgecolor="black", linewidth=0.3)
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(PITCH_CLASS_NAMES, fontsize=6)
    axes[0].set_ylabel("Residual (MI − K-K)")
    axes[0].set_title("Major Key Residuals")
    axes[0].axhline(y=0, color="black", linewidth=0.5)

    axes[1].bar(x, resid_min, color=colors_min, edgecolor="black", linewidth=0.3)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(PITCH_CLASS_NAMES, fontsize=6)
    axes[1].set_title("Minor Key Residuals")
    axes[1].axhline(y=0, color="black", linewidth=0.5)

    fig.suptitle("MI − Krumhansl-Kessler Residuals", fontsize=8)
    fig.tight_layout()
    save_figure(fig, "v3_residual_plot", subdir="v3_krumhansl")


def _generate_scatter_figures(mi_major: np.ndarray, mi_minor: np.ndarray) -> None:
    """Scatter plots of MI vs K-K for major and minor."""
    r_maj, p_maj, ci_maj = pearson_with_ci(mi_major, MAJOR_PROFILE)
    correlation_scatter(
        MAJOR_PROFILE, mi_major,
        xlabel="K-K Major Profile", ylabel="MI Major Profile",
        title="Major Key: MI vs. K-K",
        r_value=r_maj, p_value=p_maj, ci=ci_maj,
        name=None,
    )
    save_figure(plt.gcf(), "v3_scatter_major", subdir="v3_krumhansl")

    r_min, p_min, ci_min = pearson_with_ci(mi_minor, MINOR_PROFILE)
    correlation_scatter(
        MINOR_PROFILE, mi_minor,
        xlabel="K-K Minor Profile", ylabel="MI Minor Profile",
        title="Minor Key: MI vs. K-K",
        r_value=r_min, p_value=p_min, ci=ci_min,
        name=None,
    )
    save_figure(plt.gcf(), "v3_scatter_minor", subdir="v3_krumhansl")
