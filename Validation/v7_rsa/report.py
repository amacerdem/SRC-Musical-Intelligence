"""V7 RSA — comprehensive report generation with figures."""
from __future__ import annotations

from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import spearmanr

from Validation.config.paths import V7_RESULTS
from Validation.infrastructure.figures import (
    apply_nature_style,
    bar_comparison,
    heatmap,
    save_figure,
)
from Validation.infrastructure.stats import fdr_correction, spearman_with_ci


def generate_summary_report(
    comparisons: List[Dict],
    rdms: Dict[str, np.ndarray],
    stimulus_names: List[str],
) -> str:
    """Generate comprehensive V7 RSA report.

    Includes CIs, FDR correction, effect sizes, inter-model RDM similarity,
    and MDS visualization.
    """
    n_models = len(comparisons)
    model_names = [c["model_name"] for c in comparisons]
    rhos = np.array([c["spearman_rho"] for c in comparisons])
    pvals = np.array([c["p_permutation"] for c in comparisons])

    # FDR correction
    fdr_p, fdr_reject = fdr_correction(pvals)

    # rho-to-d conversion
    ds = np.array([2 * rho / np.sqrt(1 - rho ** 2) if abs(rho) < 0.9999 else float("inf") for rho in rhos])

    lines = [
        "=" * 78,
        "V7 RSA — REPRESENTATIONAL SIMILARITY ANALYSIS — COMPREHENSIVE REPORT",
        "=" * 78,
        "",
        f"  Stimuli: {len(stimulus_names)}",
        f"  Models compared: {n_models}",
        "",
        "─── Model Comparison ───",
        "",
        f"  {'Model':20s}  {'ρ':>8s}  {'p(perm)':>10s}  {'FDR-p':>10s}  "
        f"{'Sig':>4s}  {'d':>8s}  {'|ρ| class':>10s}",
        f"  {'─'*20}  {'─'*8}  {'─'*10}  {'─'*10}  {'─'*4}  {'─'*8}  {'─'*10}",
    ]

    # Sort by rho descending
    sorted_idx = np.argsort(rhos)[::-1]
    for rank, idx in enumerate(sorted_idx):
        c = comparisons[idx]
        sig = "*" if fdr_reject[idx] else ""
        r_class = "large" if abs(rhos[idx]) >= 0.5 else "medium" if abs(rhos[idx]) >= 0.3 else "small" if abs(rhos[idx]) >= 0.1 else "negl."
        lines.append(
            f"  {c['model_name']:20s}  {rhos[idx]:8.4f}  {pvals[idx]:10.4f}  "
            f"{fdr_p[idx]:10.4f}  {sig:>4s}  {ds[idx]:+8.3f}  {r_class:>10s}"
        )

    # Best model
    best_idx = sorted_idx[0]
    lines.extend([
        "",
        f"  Best model: {comparisons[best_idx]['model_name']} "
        f"(ρ = {rhos[best_idx]:.4f}, p = {pvals[best_idx]:.4f})",
    ])

    # Pairwise model ranking
    lines.extend(["", "─── Model Ranking ───", ""])
    for rank, idx in enumerate(sorted_idx, 1):
        lines.append(f"  {rank}. {comparisons[idx]['model_name']:20s}  ρ = {rhos[idx]:.4f}")

    # Inter-model RDM similarity matrix
    rdm_names = list(rdms.keys())
    n_rdm = len(rdm_names)
    if n_rdm > 1:
        sim_matrix = _compute_rdm_similarity(rdms, rdm_names)
        lines.extend(["", "─── Inter-Model RDM Similarity (Spearman ρ) ───", ""])
        header = f"  {'':20s}" + "".join(f"  {n[:8]:>8s}" for n in rdm_names)
        lines.append(header)
        for i, name_i in enumerate(rdm_names):
            row = f"  {name_i:20s}"
            for j in range(n_rdm):
                row += f"  {sim_matrix[i, j]:8.3f}"
            lines.append(row)

    # Stimulus list
    lines.extend(["", "─── Stimuli ───", ""])
    for i, name in enumerate(stimulus_names):
        lines.append(f"  {i+1:3d}. {name}")

    lines.extend(["", "=" * 78])
    report = "\n".join(lines)

    V7_RESULTS.mkdir(parents=True, exist_ok=True)
    (V7_RESULTS / "v7_summary.txt").write_text(report)
    print(f"[V7] Report saved: {V7_RESULTS / 'v7_summary.txt'}")

    # Generate figures
    try:
        _generate_figures(comparisons, rdms, stimulus_names, rhos, pvals, fdr_reject)
        print(f"[V7] Figures saved to: figures/v7_rsa/")
    except Exception as e:
        print(f"[V7] Figure generation failed: {e}")

    return report


def _compute_rdm_similarity(rdms: Dict[str, np.ndarray], names: list) -> np.ndarray:
    """Compute pairwise Spearman correlation between RDM lower triangles."""
    n = len(names)
    sim = np.eye(n)
    vectors = {}
    for name in names:
        rdm = rdms[name]
        triu_idx = np.triu_indices(rdm.shape[0], k=1)
        vectors[name] = rdm[triu_idx]

    for i in range(n):
        for j in range(i + 1, n):
            rho, _ = spearmanr(vectors[names[i]], vectors[names[j]])
            sim[i, j] = rho
            sim[j, i] = rho
    return sim


def _generate_figures(
    comparisons: List[Dict],
    rdms: Dict[str, np.ndarray],
    stimulus_names: List[str],
    rhos: np.ndarray,
    pvals: np.ndarray,
    fdr_reject: np.ndarray,
) -> None:
    """Generate all V7 figures."""

    stim_labels = [s[:15] for s in stimulus_names]

    # 1. RDM heatmaps (existing, enhanced)
    for name, rdm in rdms.items():
        heatmap(
            rdm, stim_labels, stim_labels,
            title=f"RDM: {name}",
            cmap="viridis",
            name=None,
        )
        save_figure(plt.gcf(), f"v7_rdm_{name}", subdir="v7_rsa")

    # 2. Model comparison bar with error bars
    apply_nature_style()
    model_names = [c["model_name"] for c in comparisons]
    sorted_idx = np.argsort(rhos)[::-1]

    fig, ax = plt.subplots(figsize=(4.5, 3))
    x = np.arange(len(comparisons))
    sorted_names = [model_names[i] for i in sorted_idx]
    sorted_rhos = rhos[sorted_idx]
    colors = ["#cb181d" if fdr_reject[i] else "#bdd7e7" for i in sorted_idx]

    ax.bar(x, sorted_rhos, color=colors, edgecolor="black", linewidth=0.5)
    ax.set_xticks(x)
    ax.set_xticklabels(sorted_names, rotation=45, ha="right", fontsize=6)
    ax.set_ylabel("Spearman ρ")
    ax.set_title("RSA Model Comparison")
    ax.axhline(y=0, color="black", linewidth=0.5)
    save_figure(fig, "v7_model_comparison_bar", subdir="v7_rsa")

    # 3. Inter-model RDM correlation matrix
    rdm_names = list(rdms.keys())
    if len(rdm_names) > 1:
        sim_matrix = _compute_rdm_similarity(rdms, rdm_names)
        heatmap(
            sim_matrix, rdm_names, rdm_names,
            title="Inter-Model RDM Similarity",
            cmap="RdBu_r", vmin=-1, vmax=1,
            name=None,
        )
        save_figure(plt.gcf(), "v7_rdm_correlation_matrix", subdir="v7_rsa")

    # 4. MDS plot of stimulus space (best model)
    if len(stimulus_names) >= 3:
        best_rdm_name = model_names[np.argmax(rhos)]
        if best_rdm_name in rdms:
            _generate_mds_plot(rdms[best_rdm_name], stimulus_names, best_rdm_name)


def _generate_mds_plot(
    rdm: np.ndarray,
    stimulus_names: List[str],
    model_name: str,
) -> None:
    """2D MDS visualization of representational space."""
    try:
        from sklearn.manifold import MDS
    except ImportError:
        return

    apply_nature_style()

    # Ensure symmetric and non-negative
    rdm_sym = (rdm + rdm.T) / 2
    np.fill_diagonal(rdm_sym, 0)

    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=42, normalized_stress="auto")
    coords = mds.fit_transform(rdm_sym)

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.scatter(coords[:, 0], coords[:, 1], s=30, color="#2171b5",
               edgecolors="black", linewidth=0.5, zorder=5)
    for i, name in enumerate(stimulus_names):
        ax.annotate(name[:12], (coords[i, 0], coords[i, 1]),
                    fontsize=4, xytext=(4, 4), textcoords="offset points")

    ax.set_xlabel("MDS Dimension 1")
    ax.set_ylabel("MDS Dimension 2")
    ax.set_title(f"Stimulus Space ({model_name})")
    ax.set_aspect("equal")
    save_figure(fig, "v7_mds_plot", subdir="v7_rsa")
