"""Publication-quality figure generation — Nature Neuroscience style."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Tuple

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from Validation.config.paths import FIGURES

# Use non-interactive backend for server/CI environments
matplotlib.use("Agg")


def apply_nature_style() -> None:
    """Apply Nature-journal figure style."""
    style_path = FIGURES / "nature_style.mplstyle"
    if style_path.exists():
        plt.style.use(str(style_path))
    else:
        # Fallback inline style
        plt.rcParams.update({
            "font.family": "Arial",
            "font.size": 7,
            "axes.labelsize": 8,
            "axes.titlesize": 8,
            "xtick.labelsize": 7,
            "ytick.labelsize": 7,
            "legend.fontsize": 6,
            "figure.dpi": 300,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            "axes.linewidth": 0.5,
            "xtick.major.width": 0.5,
            "ytick.major.width": 0.5,
            "lines.linewidth": 0.75,
        })


def save_figure(
    fig: plt.Figure,
    name: str,
    formats: Tuple[str, ...] = ("pdf", "png"),
    subdir: Optional[str] = None,
) -> List[Path]:
    """Save figure in multiple formats.

    Args:
        fig: Matplotlib figure.
        name: Base filename (without extension).
        formats: Output formats.
        subdir: Optional subdirectory within figures/.

    Returns:
        List of saved file paths.
    """
    out_dir = FIGURES / subdir if subdir else FIGURES
    out_dir.mkdir(parents=True, exist_ok=True)

    paths = []
    for fmt in formats:
        path = out_dir / f"{name}.{fmt}"
        fig.savefig(path, format=fmt, bbox_inches="tight")
        paths.append(path)

    plt.close(fig)
    return paths


def correlation_scatter(
    x: np.ndarray,
    y: np.ndarray,
    xlabel: str,
    ylabel: str,
    title: str,
    r_value: float,
    p_value: float,
    ci: Optional[Tuple[float, float]] = None,
    name: Optional[str] = None,
) -> plt.Figure:
    """Create a publication-quality correlation scatter plot.

    Args:
        x, y: Data arrays.
        xlabel, ylabel: Axis labels.
        title: Figure title.
        r_value: Correlation coefficient.
        p_value: P-value.
        ci: Optional confidence interval (lower, upper).
        name: Optional filename to save.

    Returns:
        Matplotlib figure.
    """
    apply_nature_style()
    fig, ax = plt.subplots(figsize=(3.5, 3.5))

    ax.scatter(x, y, s=8, alpha=0.5, color="#2171b5", edgecolors="none")

    # Fit line
    z = np.polyfit(x, y, 1)
    p_line = np.poly1d(z)
    x_sorted = np.sort(x)
    ax.plot(x_sorted, p_line(x_sorted), color="#cb181d", linewidth=1)

    # Annotation
    stat_text = f"r = {r_value:.3f}"
    if ci is not None:
        stat_text += f" [{ci[0]:.3f}, {ci[1]:.3f}]"
    stat_text += f"\np = {p_value:.2e}"

    ax.text(0.05, 0.95, stat_text, transform=ax.transAxes,
            verticalalignment="top", fontsize=6,
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    if name:
        save_figure(fig, name)

    return fig


def bar_comparison(
    conditions: List[str],
    values: List[float],
    errors: Optional[List[float]] = None,
    ylabel: str = "Effect size",
    title: str = "",
    colors: Optional[List[str]] = None,
    name: Optional[str] = None,
) -> plt.Figure:
    """Bar chart for condition comparisons (e.g., pharmacological effects).

    Returns:
        Matplotlib figure.
    """
    apply_nature_style()
    fig, ax = plt.subplots(figsize=(3.5, 3.0))

    n = len(conditions)
    if colors is None:
        colors = ["#2171b5", "#6baed6", "#bdd7e7", "#eff3ff"][:n]

    x = np.arange(n)
    bars = ax.bar(x, values, yerr=errors, color=colors[:n],
                  edgecolor="black", linewidth=0.5, capsize=3,
                  error_kw={"linewidth": 0.5})

    ax.set_xticks(x)
    ax.set_xticklabels(conditions, rotation=45, ha="right")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.axhline(y=0, color="black", linewidth=0.5, linestyle="-")

    if name:
        save_figure(fig, name)

    return fig


def heatmap(
    data: np.ndarray,
    row_labels: List[str],
    col_labels: List[str],
    title: str = "",
    cmap: str = "RdBu_r",
    vmin: Optional[float] = None,
    vmax: Optional[float] = None,
    name: Optional[str] = None,
) -> plt.Figure:
    """Publication-quality heatmap (for RDMs, correlation matrices).

    Returns:
        Matplotlib figure.
    """
    import seaborn as sns

    apply_nature_style()
    fig, ax = plt.subplots(figsize=(5, 4))

    sns.heatmap(
        data, ax=ax,
        xticklabels=col_labels,
        yticklabels=row_labels,
        cmap=cmap, vmin=vmin, vmax=vmax,
        linewidths=0.3, linecolor="white",
        cbar_kws={"shrink": 0.8},
        annot=True if data.shape[0] <= 15 else False,
        fmt=".2f" if data.shape[0] <= 15 else "",
    )
    ax.set_title(title)

    if name:
        save_figure(fig, name)

    return fig


def forest_plot(
    labels: List[str],
    estimates: np.ndarray,
    ci_lower: np.ndarray,
    ci_upper: np.ndarray,
    xlabel: str = "Effect size",
    title: str = "",
    zero_line: bool = True,
    name: Optional[str] = None,
) -> plt.Figure:
    """Horizontal forest plot with confidence intervals.

    Args:
        labels: Per-item labels (y-axis).
        estimates: Point estimates.
        ci_lower, ci_upper: Lower/upper CI bounds.
        xlabel: X-axis label.
        title: Plot title.
        zero_line: Draw vertical line at x=0.
        name: Optional filename to save.

    Returns:
        Matplotlib figure.
    """
    apply_nature_style()
    n = len(labels)
    fig_height = max(3.0, n * 0.18 + 1.0)
    fig, ax = plt.subplots(figsize=(5, fig_height))

    y_pos = np.arange(n)
    xerr_lower = estimates - ci_lower
    xerr_upper = ci_upper - estimates

    ax.errorbar(
        estimates, y_pos,
        xerr=[xerr_lower, xerr_upper],
        fmt="o", markersize=3, color="#2171b5",
        ecolor="#6baed6", elinewidth=0.6, capsize=2, capthick=0.5,
    )

    if zero_line:
        ax.axvline(x=0, color="grey", linewidth=0.5, linestyle="--")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=5)
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    ax.invert_yaxis()

    if name:
        save_figure(fig, name)

    return fig


def volcano_plot(
    effects: np.ndarray,
    pvalues: np.ndarray,
    labels: Optional[List[str]] = None,
    alpha: float = 0.05,
    xlabel: str = "Effect size (r)",
    title: str = "",
    name: Optional[str] = None,
) -> plt.Figure:
    """Volcano plot: effect size vs. -log10(p-value).

    Args:
        effects: Effect size values (x-axis).
        pvalues: Raw p-values (transformed to -log10).
        labels: Optional per-point labels.
        alpha: Significance threshold line.
        xlabel: X-axis label.
        title: Plot title.
        name: Optional filename to save.

    Returns:
        Matplotlib figure.
    """
    apply_nature_style()
    fig, ax = plt.subplots(figsize=(4, 3.5))

    neg_log_p = -np.log10(np.clip(pvalues, 1e-300, 1.0))
    sig_mask = pvalues < alpha

    ax.scatter(effects[~sig_mask], neg_log_p[~sig_mask],
               s=8, alpha=0.5, color="#bdd7e7", edgecolors="none", label="n.s.")
    ax.scatter(effects[sig_mask], neg_log_p[sig_mask],
               s=12, alpha=0.7, color="#cb181d", edgecolors="none", label=f"p < {alpha}")

    ax.axhline(y=-np.log10(alpha), color="grey", linewidth=0.5, linestyle="--")

    if labels is not None:
        for i, lbl in enumerate(labels):
            if sig_mask[i]:
                ax.annotate(lbl, (effects[i], neg_log_p[i]),
                            fontsize=4, xytext=(3, 3),
                            textcoords="offset points")

    ax.set_xlabel(xlabel)
    ax.set_ylabel("-log₁₀(p)")
    ax.set_title(title)
    ax.legend(fontsize=5, loc="upper right")

    if name:
        save_figure(fig, name)

    return fig


def brain_regions_plot(
    activations: np.ndarray,
    region_names: List[str],
    title: str = "Region Activation",
    name: Optional[str] = None,
) -> plt.Figure:
    """Horizontal bar chart for brain region activations.

    Args:
        activations: (26,) mean activation per region.
        region_names: Region name labels.
        title: Plot title.
        name: Optional filename.

    Returns:
        Matplotlib figure.
    """
    apply_nature_style()
    fig, ax = plt.subplots(figsize=(4, 6))

    y_pos = np.arange(len(region_names))
    colors = []
    for i, _ in enumerate(region_names):
        if i < 12:
            colors.append("#2171b5")   # cortical
        elif i < 21:
            colors.append("#6baed6")   # subcortical
        else:
            colors.append("#bdd7e7")   # brainstem

    ax.barh(y_pos, activations, color=colors, edgecolor="black", linewidth=0.3)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(region_names)
    ax.set_xlabel("Mean Activation")
    ax.set_title(title)
    ax.invert_yaxis()

    if name:
        save_figure(fig, name)

    return fig
