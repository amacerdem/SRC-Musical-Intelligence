#!/usr/bin/env python3
"""Visualize training results — loss curves, per-dimension heatmaps, correlations.

Usage:
    python Training/visualize.py --run-dir Training/runs/v1
    python Training/visualize.py --run-dir Training/runs/v1 --epoch 25   # specific epoch detail
    python Training/visualize.py --run-dir Training/runs/v1 --compare Training/runs/v2
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Training.train import (
    R3_GROUPS, R3_NAMES, BELIEF_NAMES, BELIEF_FUNCTIONS, DIM_NAMES,
)

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    HAS_MPL = True
except ImportError:
    HAS_MPL = False
    print("WARNING: matplotlib not found. Install with: pip install matplotlib", flush=True)


# ======================================================================
# DATA LOADING
# ======================================================================

def load_summary(run_dir: Path) -> Dict[str, List]:
    """Load summary.csv into column-oriented dict."""
    path = run_dir / "logs" / "summary.csv"
    if not path.exists():
        raise FileNotFoundError(f"No summary.csv in {run_dir}")
    data = {}
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            for k, v in row.items():
                data.setdefault(k, []).append(v)
    # Convert numeric columns
    for k in data:
        try:
            data[k] = [float(x) for x in data[k]]
        except ValueError:
            pass
    return data


def load_epoch(run_dir: Path, epoch: int) -> Dict:
    """Load a single epoch's full JSON."""
    path = run_dir / "logs" / f"epoch_{epoch:03d}.json"
    with open(path) as f:
        return json.load(f)


def load_per_dim_csv(run_dir: Path, name: str) -> Dict[str, List[float]]:
    """Load per-dim CSV (r3.csv, beliefs.csv, dims.csv)."""
    path = run_dir / "logs" / "per_dim" / name
    data = {}
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            for k, v in row.items():
                data.setdefault(k, []).append(float(v))
    return data


# ======================================================================
# TEXT REPORTS (no matplotlib needed)
# ======================================================================

def print_summary(run_dir: Path):
    """Print text summary of training run."""
    summary = load_summary(run_dir)
    n_epochs = len(summary["epoch"])
    print(f"\n{'='*80}")
    print(f"Training Run: {run_dir}")
    print(f"{'='*80}")
    print(f"Epochs: {n_epochs}")
    print(f"Best val total: {min(summary['val_total']):.6f} (epoch {summary['val_total'].index(min(summary['val_total']))+1})")

    # Final epoch losses
    print(f"\nFinal epoch ({n_epochs}):")
    for head in ["r3", "h3", "beliefs", "dims"]:
        tr = summary[f"train_{head}"][-1]
        vl = summary[f"val_{head}"][-1]
        print(f"  {head:>8s}  train={tr:.6f}  val={vl:.6f}")

    # Correlation summary
    print(f"\nVal correlations (final):")
    for head in ["r3", "h3", "beliefs", "dims"]:
        key = f"val_{head}_corr"
        if key in summary:
            print(f"  {head:>8s}  r={summary[key][-1]:.4f}")

    # Per R³ group
    print(f"\nR³ Group Detail (final):")
    for g in R3_GROUPS:
        mse_key = f"val_r3_{g}_mse"
        corr_key = f"val_r3_{g}_corr"
        if mse_key in summary:
            print(f"  {g:25s}  MSE={summary[mse_key][-1]:.6f}  r={summary[corr_key][-1]:.4f}")

    # Per belief function
    print(f"\nBelief Function Detail (final):")
    for g in BELIEF_FUNCTIONS:
        mse_key = f"val_b_{g}_mse"
        corr_key = f"val_b_{g}_corr"
        if mse_key in summary:
            print(f"  {g:25s}  MSE={summary[mse_key][-1]:.6f}  r={summary[corr_key][-1]:.4f}")

    # 10 dims
    print(f"\n5+5 Dimensions (final):")
    print(f"  Musical:   ", end="")
    for i in range(5):
        mse_key = f"val_dim_{DIM_NAMES[i]}_mse"
        corr_key = f"val_dim_{DIM_NAMES[i]}_corr"
        if mse_key in summary:
            print(f" {DIM_NAMES[i]}={summary[mse_key][-1]:.5f}(r={summary[corr_key][-1]:+.3f})", end="")
    print()
    print(f"  Emotional: ", end="")
    for i in range(5, 10):
        mse_key = f"val_dim_{DIM_NAMES[i]}_mse"
        corr_key = f"val_dim_{DIM_NAMES[i]}_corr"
        if mse_key in summary:
            print(f" {DIM_NAMES[i]}={summary[mse_key][-1]:.5f}(r={summary[corr_key][-1]:+.3f})", end="")
    print(f"\n")


def print_epoch_detail(run_dir: Path, epoch: int):
    """Print full per-dimension detail for a specific epoch."""
    data = load_epoch(run_dir, epoch)
    pdm = data["per_dim"]

    print(f"\n{'='*80}")
    print(f"Epoch {epoch} — Full Per-Dimension Report")
    print(f"{'='*80}")

    # R³ per-feature
    print(f"\nR³ Features (97D) — sorted by MSE descending:")
    r3_mse = pdm["r3"]["mse"]
    r3_corr = pdm["r3"]["corr"]
    indices = np.argsort(r3_mse)[::-1]
    for idx in indices:
        group = ""
        for gname, (gs, ge) in R3_GROUPS.items():
            if gs <= idx < ge:
                group = gname
                break
        print(f"  [{idx:2d}] {R3_NAMES[idx]:30s} {group:25s}  MSE={r3_mse[idx]:.6f}  r={r3_corr[idx]:+.4f}")

    # Beliefs per-feature
    print(f"\nBeliefs (131D) — sorted by MSE descending:")
    b_mse = pdm["beliefs"]["mse"]
    b_corr = pdm["beliefs"]["corr"]
    indices = np.argsort(b_mse)[::-1]
    for idx in indices[:30]:  # top 30
        func = ""
        for fname, (fs, fe) in BELIEF_FUNCTIONS.items():
            if fs <= idx < fe:
                func = fname
                break
        print(f"  [b{idx:3d}] {BELIEF_NAMES[idx]:30s} {func:20s}  MSE={b_mse[idx]:.6f}  r={b_corr[idx]:+.4f}")
    if len(indices) > 30:
        print(f"  ... ({len(indices)-30} more beliefs not shown)")

    # Dims
    print(f"\nDimensions (10D):")
    d_mse = pdm["dims"]["mse"]
    d_corr = pdm["dims"]["corr"]
    for i, name in enumerate(DIM_NAMES):
        radar = "Musical" if i < 5 else "Emotional"
        bar = "█" * int(d_corr[i] * 20) if d_corr[i] > 0 else ""
        print(f"  [{i}] {name:15s} ({radar:9s})  MSE={d_mse[i]:.6f}  r={d_corr[i]:+.4f}  {bar}")


# ======================================================================
# MATPLOTLIB PLOTS
# ======================================================================

def plot_loss_curves(run_dir: Path, save_dir: Optional[Path] = None):
    """Plot train/val loss curves for all 4 heads."""
    if not HAS_MPL:
        print("Skipping plots (matplotlib not installed)")
        return

    summary = load_summary(run_dir)
    epochs = summary["epoch"]
    save_dir = save_dir or (run_dir / "plots")
    save_dir.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    heads = ["r3", "h3", "beliefs", "dims"]
    titles = ["R³ (97D)", "H³ (637D)", "Beliefs (131D)", "Dims (10D)"]

    for i, (head, title) in enumerate(zip(heads, titles)):
        ax = axes[i // 3][i % 3]
        ax.plot(epochs, summary[f"train_{head}"], label="train", alpha=0.8)
        ax.plot(epochs, summary[f"val_{head}"], label="val", alpha=0.8)
        ax.set_title(title)
        ax.set_xlabel("Epoch")
        ax.set_ylabel("MSE")
        ax.legend()
        ax.grid(True, alpha=0.3)

    # Total weighted loss
    ax = axes[1][1]
    ax.plot(epochs, summary["train_total"], label="train total", alpha=0.8)
    ax.plot(epochs, summary["val_total"], label="val total", alpha=0.8)
    ax.set_title("Total Weighted Loss")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Weighted MSE")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Correlations
    ax = axes[1][2]
    for head in heads:
        key = f"val_{head}_corr"
        if key in summary:
            ax.plot(epochs, summary[key], label=head, alpha=0.8)
    ax.set_title("Val Correlation (mean)")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Pearson r")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    path = save_dir / "loss_curves.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved: {path}")


def plot_r3_groups(run_dir: Path, save_dir: Optional[Path] = None):
    """Plot R³ group MSE and correlation over epochs."""
    if not HAS_MPL:
        return

    summary = load_summary(run_dir)
    epochs = summary["epoch"]
    save_dir = save_dir or (run_dir / "plots")
    save_dir.mkdir(parents=True, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    for g in R3_GROUPS:
        mse = summary.get(f"val_r3_{g}_mse", [])
        corr = summary.get(f"val_r3_{g}_corr", [])
        if mse:
            ax1.plot(epochs, mse, label=g, alpha=0.8)
        if corr:
            ax2.plot(epochs, corr, label=g, alpha=0.8)

    ax1.set_title("R³ Groups — Val MSE")
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("MSE")
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)

    ax2.set_title("R³ Groups — Val Correlation")
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("Pearson r")
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    path = save_dir / "r3_groups.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved: {path}")


def plot_belief_functions(run_dir: Path, save_dir: Optional[Path] = None):
    """Plot belief function group metrics over epochs."""
    if not HAS_MPL:
        return

    summary = load_summary(run_dir)
    epochs = summary["epoch"]
    save_dir = save_dir or (run_dir / "plots")
    save_dir.mkdir(parents=True, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    for g in BELIEF_FUNCTIONS:
        mse = summary.get(f"val_b_{g}_mse", [])
        corr = summary.get(f"val_b_{g}_corr", [])
        if mse:
            ax1.plot(epochs, mse, label=g, alpha=0.8)
        if corr:
            ax2.plot(epochs, corr, label=g, alpha=0.8)

    ax1.set_title("Belief Functions (F1-F9) — Val MSE")
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("MSE")
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.3)

    ax2.set_title("Belief Functions (F1-F9) — Val Correlation")
    ax2.set_xlabel("Epoch")
    ax2.set_ylabel("Pearson r")
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    path = save_dir / "belief_functions.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved: {path}")


def plot_dims_detail(run_dir: Path, save_dir: Optional[Path] = None):
    """Plot individual 5+5 dimension MSE and correlation."""
    if not HAS_MPL:
        return

    summary = load_summary(run_dir)
    epochs = summary["epoch"]
    save_dir = save_dir or (run_dir / "plots")
    save_dir.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(2, 2, figsize=(16, 10))

    # Musical dims MSE
    ax = axes[0][0]
    for i in range(5):
        key = f"val_dim_{DIM_NAMES[i]}_mse"
        if key in summary:
            ax.plot(epochs, summary[key], label=DIM_NAMES[i], alpha=0.8)
    ax.set_title("Musical Dimensions — Val MSE")
    ax.set_xlabel("Epoch")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Musical dims correlation
    ax = axes[0][1]
    for i in range(5):
        key = f"val_dim_{DIM_NAMES[i]}_corr"
        if key in summary:
            ax.plot(epochs, summary[key], label=DIM_NAMES[i], alpha=0.8)
    ax.set_title("Musical Dimensions — Val Correlation")
    ax.set_xlabel("Epoch")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Emotional dims MSE
    ax = axes[1][0]
    for i in range(5, 10):
        key = f"val_dim_{DIM_NAMES[i]}_mse"
        if key in summary:
            ax.plot(epochs, summary[key], label=DIM_NAMES[i], alpha=0.8)
    ax.set_title("Emotional Dimensions — Val MSE")
    ax.set_xlabel("Epoch")
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Emotional dims correlation
    ax = axes[1][1]
    for i in range(5, 10):
        key = f"val_dim_{DIM_NAMES[i]}_corr"
        if key in summary:
            ax.plot(epochs, summary[key], label=DIM_NAMES[i], alpha=0.8)
    ax.set_title("Emotional Dimensions — Val Correlation")
    ax.set_xlabel("Epoch")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    path = save_dir / "dims_5plus5.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved: {path}")


def plot_heatmap(run_dir: Path, epoch: int, save_dir: Optional[Path] = None):
    """Plot per-dimension MSE heatmap for a specific epoch."""
    if not HAS_MPL:
        return

    data = load_epoch(run_dir, epoch)
    pdm = data["per_dim"]
    save_dir = save_dir or (run_dir / "plots")
    save_dir.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(3, 1, figsize=(20, 12))

    # R³ heatmap
    r3_mse = np.array(pdm["r3"]["mse"]).reshape(1, -1)
    ax = axes[0]
    im = ax.imshow(r3_mse, aspect="auto", cmap="YlOrRd")
    ax.set_title(f"R³ Per-Feature MSE (Epoch {epoch})")
    ax.set_yticks([])
    ax.set_xticks(range(0, 97, 5))
    ax.set_xticklabels(range(0, 97, 5), fontsize=7)
    # Mark group boundaries
    for gname, (gs, ge) in R3_GROUPS.items():
        ax.axvline(gs - 0.5, color="blue", linewidth=0.5, alpha=0.5)
        ax.text((gs + ge) / 2, -0.5, gname.split("_")[0], ha="center", fontsize=7)
    plt.colorbar(im, ax=ax, shrink=0.5)

    # Beliefs heatmap
    b_mse = np.array(pdm["beliefs"]["mse"]).reshape(1, -1)
    ax = axes[1]
    im = ax.imshow(b_mse, aspect="auto", cmap="YlOrRd")
    ax.set_title(f"Belief Per-Feature MSE (Epoch {epoch})")
    ax.set_yticks([])
    ax.set_xticks(range(0, 131, 10))
    for fname, (fs, fe) in BELIEF_FUNCTIONS.items():
        ax.axvline(fs - 0.5, color="blue", linewidth=0.5, alpha=0.5)
        ax.text((fs + fe) / 2, -0.5, fname.split("_")[0], ha="center", fontsize=7)
    plt.colorbar(im, ax=ax, shrink=0.5)

    # Dims bar chart
    ax = axes[2]
    d_mse = pdm["dims"]["mse"]
    d_corr = pdm["dims"]["corr"]
    x = np.arange(10)
    bars = ax.bar(x, d_mse, color=["#2196F3"] * 5 + ["#FF5722"] * 5, alpha=0.8)
    ax.set_title(f"5+5 Dimension MSE (Epoch {epoch})")
    ax.set_xticks(x)
    ax.set_xticklabels([f"{n}\nr={d_corr[i]:+.3f}" for i, n in enumerate(DIM_NAMES)], fontsize=8)
    ax.set_ylabel("MSE")
    ax.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()
    path = save_dir / f"heatmap_epoch_{epoch:03d}.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved: {path}")


def plot_all(run_dir: Path, epoch: Optional[int] = None):
    """Generate all plots for a training run."""
    save_dir = run_dir / "plots"
    plot_loss_curves(run_dir, save_dir)
    plot_r3_groups(run_dir, save_dir)
    plot_belief_functions(run_dir, save_dir)
    plot_dims_detail(run_dir, save_dir)

    # Heatmap for last or specified epoch
    if epoch is None:
        summary = load_summary(run_dir)
        epoch = int(summary["epoch"][-1])
    plot_heatmap(run_dir, epoch, save_dir)
    print(f"\nAll plots saved to: {save_dir}")


# ======================================================================
# COMPARE RUNS
# ======================================================================

def compare_runs(dirs: List[Path]):
    """Print side-by-side comparison of multiple runs."""
    print(f"\n{'='*80}")
    print(f"Comparing {len(dirs)} runs")
    print(f"{'='*80}")

    summaries = {}
    for d in dirs:
        name = d.name
        summaries[name] = load_summary(d)

    # Header
    names = list(summaries.keys())
    header = f"{'Metric':>30s}"
    for n in names:
        header += f"  {n:>15s}"
    print(header)
    print("-" * len(header))

    # Best val total
    row = f"{'best_val_total':>30s}"
    for n in names:
        row += f"  {min(summaries[n]['val_total']):>15.6f}"
    print(row)

    # Final val per head
    for head in ["r3", "h3", "beliefs", "dims"]:
        row = f"{f'final_val_{head}':>30s}"
        for n in names:
            row += f"  {summaries[n][f'val_{head}'][-1]:>15.6f}"
        print(row)

    # Final correlation per head
    for head in ["r3", "h3", "beliefs", "dims"]:
        key = f"val_{head}_corr"
        row = f"{f'final_corr_{head}':>30s}"
        for n in names:
            if key in summaries[n]:
                row += f"  {summaries[n][key][-1]:>15.4f}"
            else:
                row += f"  {'N/A':>15s}"
        print(row)

    # Per dim
    print(f"\n5+5 Dimensions (final val MSE / correlation):")
    for i, dname in enumerate(DIM_NAMES):
        row = f"  {dname:>15s}"
        for n in names:
            mse_key = f"val_dim_{dname}_mse"
            corr_key = f"val_dim_{dname}_corr"
            if mse_key in summaries[n]:
                row += f"  {summaries[n][mse_key][-1]:.5f}(r={summaries[n][corr_key][-1]:+.3f})"
            else:
                row += f"  {'N/A':>18s}"
        print(row)


# ======================================================================
# MAIN
# ======================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize glass-box MI training")
    parser.add_argument("--run-dir", type=str, required=True, help="Training run directory")
    parser.add_argument("--epoch", type=int, default=None, help="Specific epoch for detail view")
    parser.add_argument("--compare", type=str, nargs="*", help="Additional run dirs to compare")
    parser.add_argument("--text-only", action="store_true", help="Skip matplotlib plots")
    args = parser.parse_args()

    run_dir = Path(args.run_dir)

    if args.compare:
        all_dirs = [run_dir] + [Path(d) for d in args.compare]
        compare_runs(all_dirs)
    elif args.epoch:
        print_epoch_detail(run_dir, args.epoch)
    else:
        print_summary(run_dir)
        if not args.text_only:
            plot_all(run_dir)
