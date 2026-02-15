"""IMU Visualization Suite — Comprehensive figures for R³, H³, C³ data flows.

Generates 20 publication-quality figures probing every stage of the IMU pipeline.
Each test method produces one or more PNG files in Tests/scientific/outputs/.

Run:
    pytest Tests/scientific/test_imu_visualize.py -v
"""
from __future__ import annotations

import math
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pytest
import torch
from torch import Tensor

import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.gridspec import GridSpec
import matplotlib.ticker as ticker

from .conftest import (
    SCI_B,
    SCI_T,
    SCI_D,
    FRAME_RATE,
    R3_GROUPS,
    R3_GROUP_FREQS,
    run_model,
    run_imu_unit,
)

# ---------------------------------------------------------------------------
# Output directory
# ---------------------------------------------------------------------------
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Style
# ---------------------------------------------------------------------------
plt.rcParams.update({
    "figure.dpi": 150,
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9,
    "figure.facecolor": "white",
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.15,
})

# Color palettes
TIER_COLORS = {"alpha": "#2196F3", "beta": "#FF9800", "gamma": "#4CAF50"}
MODEL_CMAP = plt.cm.tab20


def _save(fig, name: str):
    """Save figure and close."""
    path = OUTPUT_DIR / f"{name}.png"
    fig.savefig(path)
    plt.close(fig)
    return path


def _compute_model_output(model, mechanism_outputs, h3_features, r3) -> np.ndarray:
    with torch.no_grad():
        out = run_model(model, mechanism_outputs, h3_features, r3)
    return out[0].numpy()


# ======================================================================
# Visualization 1: R³ Input Heatmap
# ======================================================================


class TestVisualize:
    """All 20 visualizations as test methods."""

    def test_viz_01_r3_input_heatmap(self, structured_r3):
        """R³ input heatmap (T × 49) with group annotations."""
        r3_np = structured_r3[0].numpy()  # (T, 49)

        fig, ax = plt.subplots(figsize=(14, 5))
        im = ax.imshow(r3_np.T, aspect="auto", cmap="viridis",
                       origin="lower", extent=[0, SCI_T / FRAME_RATE, 0, SCI_D])
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("R³ Dimension")
        ax.set_title("R³ Spectral Input — Structured Sinusoidal (T×49)")

        # Group annotations
        for name, (start, end) in R3_GROUPS.items():
            freq = R3_GROUP_FREQS[name]
            mid = (start + end) / 2
            ax.axhline(start, color="white", linewidth=0.5, alpha=0.7)
            ax.text(SCI_T / FRAME_RATE + 0.1, mid, f"{name}\n({freq}Hz)",
                    fontsize=7, va="center", ha="left")

        fig.colorbar(im, ax=ax, label="Value [0, 1]", shrink=0.8)
        path = _save(fig, "01_r3_input_heatmap")
        assert path.exists()

    def test_viz_02_h3_demand_coverage(self, imu_models, all_imu_h3_demand):
        """H³ demand coverage: which (r3_idx, horizon) pairs demanded by which model."""
        fig, ax = plt.subplots(figsize=(12, 6))

        for i, model in enumerate(imu_models):
            color = TIER_COLORS[model.TIER]
            for spec in model.h3_demand:
                t = spec.as_tuple()
                ax.scatter(t[0], t[1], c=color, s=60, alpha=0.7,
                          edgecolors="black", linewidths=0.5, zorder=3)
                ax.annotate(model.NAME, (t[0], t[1]), fontsize=5,
                           ha="center", va="bottom", alpha=0.6)

        # Group boundaries on x-axis
        for name, (start, end) in R3_GROUPS.items():
            ax.axvspan(start, end, alpha=0.08, color="gray")
            ax.text((start + end) / 2, 19, name, fontsize=7, ha="center", va="bottom")

        ax.set_xlabel("R³ Index")
        ax.set_ylabel("Horizon Index")
        ax.set_title("H³ Demand Coverage — IMU 15 Models (blue=α, orange=β, green=γ)")
        ax.set_xlim(-1, 50)
        ax.set_ylim(14, 20)
        ax.grid(True, alpha=0.3)

        # Legend
        for tier, color in TIER_COLORS.items():
            ax.scatter([], [], c=color, s=60, label=tier, edgecolors="black", linewidths=0.5)
        ax.legend(loc="upper right")

        path = _save(fig, "02_h3_demand_coverage")
        assert path.exists()

    def test_viz_03_h3_modulation_timeseries(
        self, imu_models, mechanism_outputs, h3_random, random_r3
    ):
        """H³ modulation signal per model over time."""
        fig, ax = plt.subplots(figsize=(14, 6))
        t_axis = np.arange(SCI_T) / FRAME_RATE

        for i, model in enumerate(imu_models):
            # Compute h3_mod for this model
            h3_mod = np.ones(SCI_T)
            for spec in model.h3_demand:
                key = spec.as_tuple()
                if key in h3_random:
                    h3_val = h3_random[key][0].numpy()
                    h3_mod *= (0.5 + 0.5 * h3_val)

            color = TIER_COLORS[model.TIER]
            alpha = 0.8 if model.TIER == "alpha" else 0.5
            ax.plot(t_axis, h3_mod, color=color, alpha=alpha,
                   linewidth=0.8, label=model.NAME if model.TIER == "alpha" else None)

        ax.set_xlabel("Time (s)")
        ax.set_ylabel("H³ Modulation Gate")
        ax.set_title("H³ Temporal Gate Signal — All 15 IMU Models")
        ax.axhline(0.0625, color="red", linestyle="--", linewidth=0.5, label="Min gate (0.5⁴)")
        ax.axhline(1.0, color="green", linestyle="--", linewidth=0.5, label="Max gate (1.0)")
        ax.set_ylim(-0.05, 1.1)
        ax.legend(fontsize=7, loc="upper right", ncol=2)
        ax.grid(True, alpha=0.3)

        path = _save(fig, "03_h3_modulation_timeseries")
        assert path.exists()

    def test_viz_04_imu_output_heatmap(
        self, imu_unit, mechanism_outputs, h3_random, structured_r3
    ):
        """Full 159D IMU output heatmap with model boundaries."""
        out = run_imu_unit(imu_unit, mechanism_outputs, h3_random, structured_r3)
        out_np = out[0].numpy()  # (T, 159)

        fig, ax = plt.subplots(figsize=(16, 6))
        im = ax.imshow(out_np.T, aspect="auto", cmap="magma",
                       origin="lower", extent=[0, SCI_T / FRAME_RATE, 0, 159])
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("IMU Output Dimension")
        ax.set_title("IMU C³ Output — 159D Temporal Heatmap")

        # Model boundaries
        from Musical_Intelligence.brain.units.imu.models import MODEL_CLASSES
        offset = 0
        models = [cls() for cls in MODEL_CLASSES]
        for model in models:
            ax.axhline(offset, color="white", linewidth=0.3, alpha=0.5)
            ax.text(SCI_T / FRAME_RATE + 0.05, offset + model.OUTPUT_DIM / 2,
                    model.NAME, fontsize=6, va="center", ha="left",
                    color=TIER_COLORS[model.TIER])
            offset += model.OUTPUT_DIM

        fig.colorbar(im, ax=ax, label="Value [0, 1]", shrink=0.8)
        path = _save(fig, "04_imu_output_heatmap")
        assert path.exists()

    def test_viz_05_correlation_matrix_159d(
        self, imu_unit, mechanism_outputs, h3_random, random_r3
    ):
        """Inter-dimension correlation matrix (159 × 159)."""
        out = run_imu_unit(imu_unit, mechanism_outputs, h3_random, random_r3)
        out_np = out[0].numpy()  # (T, 159)
        corr = np.corrcoef(out_np.T)

        fig, ax = plt.subplots(figsize=(10, 10))
        im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1, origin="lower")
        ax.set_xlabel("Dimension")
        ax.set_ylabel("Dimension")
        ax.set_title("IMU Output Correlation Matrix (159×159)")

        # Model boundary lines
        from Musical_Intelligence.brain.units.imu.models import MODEL_CLASSES
        offset = 0
        models = [cls() for cls in MODEL_CLASSES]
        for model in models:
            ax.axhline(offset, color="black", linewidth=0.3, alpha=0.3)
            ax.axvline(offset, color="black", linewidth=0.3, alpha=0.3)
            offset += model.OUTPUT_DIM

        fig.colorbar(im, ax=ax, label="Pearson r", shrink=0.8)
        path = _save(fig, "05_correlation_matrix_159d")
        assert path.exists()

    def test_viz_06_correlation_matrix_inter_model(
        self, imu_models, mechanism_outputs, h3_random, random_r3
    ):
        """15×15 model-level correlation matrix."""
        model_means = []
        names = []
        for model in imu_models:
            out = _compute_model_output(model, mechanism_outputs, h3_random, random_r3)
            model_means.append(out.mean(axis=-1))  # (T,)
            names.append(model.NAME)

        model_means = np.array(model_means)  # (15, T)
        corr = np.corrcoef(model_means)  # (15, 15)

        fig, ax = plt.subplots(figsize=(9, 8))
        im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
        ax.set_xticks(range(15))
        ax.set_yticks(range(15))
        ax.set_xticklabels(names, rotation=45, ha="right", fontsize=7)
        ax.set_yticklabels(names, fontsize=7)
        ax.set_title("Inter-Model Correlation (15×15)")

        # Annotate values
        for i in range(15):
            for j in range(15):
                val = corr[i, j]
                color = "white" if abs(val) > 0.5 else "black"
                ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                       fontsize=5, color=color)

        # Tier boundaries
        ax.axhline(2.5, color="black", linewidth=1.5)
        ax.axhline(11.5, color="black", linewidth=1.5)
        ax.axvline(2.5, color="black", linewidth=1.5)
        ax.axvline(11.5, color="black", linewidth=1.5)

        fig.colorbar(im, ax=ax, label="Pearson r", shrink=0.8)
        path = _save(fig, "06_correlation_inter_model")
        assert path.exists()

    def test_viz_07_pca_2d_projection(
        self, imu_unit, mechanism_outputs, h3_random, structured_r3
    ):
        """First 2 PCs of IMU output, colored by time."""
        out = run_imu_unit(imu_unit, mechanism_outputs, h3_random, structured_r3)
        out_np = out[0].numpy()  # (T, 159)

        centered = out_np - out_np.mean(axis=0)
        cov = np.cov(centered.T)
        eigenvalues, eigenvectors = np.linalg.eigh(cov)
        idx = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]

        pc = centered @ eigenvectors[:, :2]  # (T, 2)
        explained = eigenvalues[:2] / eigenvalues.sum() * 100

        fig, ax = plt.subplots(figsize=(8, 7))
        sc = ax.scatter(pc[:, 0], pc[:, 1], c=np.arange(SCI_T) / FRAME_RATE,
                       cmap="plasma", s=3, alpha=0.7)
        ax.set_xlabel(f"PC1 ({explained[0]:.1f}% var)")
        ax.set_ylabel(f"PC2 ({explained[1]:.1f}% var)")
        ax.set_title("IMU Output — PCA 2D Projection (colored by time)")
        fig.colorbar(sc, ax=ax, label="Time (s)")
        ax.grid(True, alpha=0.3)

        path = _save(fig, "07_pca_2d_projection")
        assert path.exists()

    def test_viz_08_pca_3d_projection(
        self, imu_unit, mechanism_outputs, h3_random, structured_r3
    ):
        """First 3 PCs of IMU output in 3D."""
        out = run_imu_unit(imu_unit, mechanism_outputs, h3_random, structured_r3)
        out_np = out[0].numpy()

        centered = out_np - out_np.mean(axis=0)
        cov = np.cov(centered.T)
        eigenvalues, eigenvectors = np.linalg.eigh(cov)
        idx = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]

        pc = centered @ eigenvectors[:, :3]
        explained = eigenvalues[:3] / eigenvalues.sum() * 100

        fig = plt.figure(figsize=(9, 8))
        ax = fig.add_subplot(111, projection="3d")
        sc = ax.scatter(pc[:, 0], pc[:, 1], pc[:, 2],
                       c=np.arange(SCI_T) / FRAME_RATE, cmap="plasma", s=2, alpha=0.6)
        ax.set_xlabel(f"PC1 ({explained[0]:.1f}%)")
        ax.set_ylabel(f"PC2 ({explained[1]:.1f}%)")
        ax.set_zlabel(f"PC3 ({explained[2]:.1f}%)")
        ax.set_title("IMU Output — PCA 3D Trajectory")
        fig.colorbar(sc, ax=ax, label="Time (s)", shrink=0.6)

        path = _save(fig, "08_pca_3d_projection")
        assert path.exists()

    def test_viz_09_eigenvalue_spectrum(
        self, imu_unit, mechanism_outputs, h3_random, random_r3
    ):
        """Eigenvalue spectrum of covariance with participation ratio."""
        out = run_imu_unit(imu_unit, mechanism_outputs, h3_random, random_r3)
        out_np = out[0].numpy()

        cov = np.cov(out_np.T)
        eigenvalues = np.linalg.eigvalsh(cov)[::-1]

        # Participation ratio
        lam = eigenvalues[eigenvalues > 0]
        pr = (lam.sum() ** 2) / (lam ** 2).sum() if len(lam) > 0 else 0

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        # Linear scale
        ax1.bar(range(len(eigenvalues)), eigenvalues, color="#2196F3", alpha=0.7)
        ax1.set_xlabel("Component")
        ax1.set_ylabel("Eigenvalue")
        ax1.set_title(f"Eigenvalue Spectrum (PR = {pr:.1f})")
        ax1.axhline(0, color="black", linewidth=0.5)

        # Cumulative explained variance
        total = eigenvalues.sum()
        if total > 0:
            cumulative = np.cumsum(eigenvalues) / total * 100
            ax2.plot(cumulative, color="#FF5722", linewidth=2)
            ax2.axhline(90, color="gray", linestyle="--", linewidth=0.5, label="90%")
            ax2.axhline(95, color="gray", linestyle=":", linewidth=0.5, label="95%")
            # Find 90% threshold
            n90 = np.searchsorted(cumulative, 90) + 1
            ax2.axvline(n90, color="#2196F3", linestyle="--", linewidth=0.5,
                       label=f"90% @ PC{n90}")
        ax2.set_xlabel("Component")
        ax2.set_ylabel("Cumulative Variance (%)")
        ax2.set_title("Cumulative Explained Variance")
        ax2.legend(fontsize=8)
        ax2.grid(True, alpha=0.3)

        fig.suptitle(f"IMU Covariance Analysis — Effective Dim = {pr:.1f} / 159",
                    fontsize=12)

        path = _save(fig, "09_eigenvalue_spectrum")
        assert path.exists()

    def test_viz_10_psd_per_model(
        self, imu_models, mechanism_outputs, h3_random, structured_r3
    ):
        """Power spectral density of each model's mean output."""
        from scipy.signal import welch

        fig, axes = plt.subplots(3, 5, figsize=(20, 10), sharex=True, sharey=True)
        axes_flat = axes.flatten()

        for i, model in enumerate(imu_models):
            out = _compute_model_output(model, mechanism_outputs, h3_random, structured_r3)
            out_mean = out.mean(axis=-1)

            freqs, psd = welch(out_mean, fs=FRAME_RATE, nperseg=min(256, SCI_T))

            ax = axes_flat[i]
            ax.semilogy(freqs, psd, color=TIER_COLORS[model.TIER], linewidth=1)
            ax.set_title(f"{model.NAME} ({model.TIER[0]})", fontsize=8)
            ax.grid(True, alpha=0.3)

            # Mark input frequencies
            for freq in R3_GROUP_FREQS.values():
                ax.axvline(freq, color="red", linewidth=0.3, alpha=0.5)

        fig.supxlabel("Frequency (Hz)")
        fig.supylabel("PSD")
        fig.suptitle("Power Spectral Density — All 15 IMU Models (red lines = R³ input freqs)",
                    fontsize=12)
        plt.tight_layout()

        path = _save(fig, "10_psd_per_model")
        assert path.exists()

    def test_viz_11_phase_portraits(
        self, imu_models, mechanism_outputs, h3_random, structured_r3
    ):
        """Phase portraits (Y, dY/dt) for α, β, γ representatives."""
        representatives = [
            imu_models[0],   # MEAMN (alpha)
            imu_models[3],   # RASN (beta)
            imu_models[12],  # DMMS (gamma)
        ]

        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        for i, model in enumerate(representatives):
            out = _compute_model_output(model, mechanism_outputs, h3_random, structured_r3)
            # Use first output dimension
            y = out[:, 0]
            v = np.diff(y)

            ax = axes[i]
            sc = ax.scatter(y[:-1], v, c=np.arange(len(v)) / FRAME_RATE,
                          cmap="plasma", s=2, alpha=0.5)
            ax.set_xlabel("Y (position)")
            ax.set_ylabel("dY/dt (velocity)")
            ax.set_title(f"{model.NAME} ({model.TIER})")
            ax.grid(True, alpha=0.3)
            ax.axhline(0, color="gray", linewidth=0.5)

        fig.suptitle("Phase Portraits — IMU Representative Models", fontsize=12)
        fig.colorbar(sc, ax=axes[-1], label="Time (s)", shrink=0.8)
        plt.tight_layout()

        path = _save(fig, "11_phase_portraits")
        assert path.exists()

    def test_viz_12_sensitivity_heatmap(
        self, imu_models, mechanism_outputs, h3_ones, random_r3
    ):
        """Jacobian ∂output/∂r3 heatmap per model."""
        eps = 0.001
        n_models = len(imu_models)

        fig, axes = plt.subplots(3, 5, figsize=(22, 12))
        axes_flat = axes.flatten()

        for idx, model in enumerate(imu_models):
            with torch.no_grad():
                out_base = model.compute(mechanism_outputs, h3_ones, random_r3)

            jacobian = np.zeros((model.OUTPUT_DIM, SCI_D))

            for d in range(SCI_D):
                r3_plus = random_r3.clone()
                r3_plus[:, :, d] = (r3_plus[:, :, d] + eps).clamp(0, 1)
                r3_minus = random_r3.clone()
                r3_minus[:, :, d] = (r3_minus[:, :, d] - eps).clamp(0, 1)

                with torch.no_grad():
                    out_plus = model.compute(mechanism_outputs, h3_ones, r3_plus)
                    out_minus = model.compute(mechanism_outputs, h3_ones, r3_minus)

                jac = ((out_plus - out_minus) / (2 * eps))[0].mean(dim=0).numpy()
                jacobian[:, d] = jac

            ax = axes_flat[idx]
            im = ax.imshow(jacobian, aspect="auto", cmap="RdBu_r",
                          vmin=-0.15, vmax=0.15, origin="lower")
            ax.set_title(f"{model.NAME} ({model.TIER[0]})", fontsize=8)
            ax.set_xlabel("R³ dim", fontsize=7)
            ax.set_ylabel("Output dim", fontsize=7)

        fig.suptitle("Sensitivity ∂output/∂R³ — All 15 IMU Models", fontsize=12)
        fig.colorbar(im, ax=axes_flat[-1], label="Jacobian", shrink=0.8)
        plt.tight_layout()

        path = _save(fig, "12_sensitivity_heatmap")
        assert path.exists()

    def test_viz_13_tier_comparison_violin(
        self, imu_models, mechanism_outputs, h3_random, random_r3
    ):
        """Output distribution violin plots by tier."""
        tier_data = {"alpha": [], "beta": [], "gamma": []}

        for model in imu_models:
            out = _compute_model_output(model, mechanism_outputs, h3_random, random_r3)
            tier_data[model.TIER].extend(out.ravel().tolist())

        fig, ax = plt.subplots(figsize=(8, 6))

        positions = [1, 2, 3]
        tier_names = ["alpha", "beta", "gamma"]
        data_list = [tier_data[t] for t in tier_names]

        parts = ax.violinplot(data_list, positions=positions, showmeans=True,
                             showmedians=True, showextrema=False)

        for i, body in enumerate(parts["bodies"]):
            body.set_facecolor(TIER_COLORS[tier_names[i]])
            body.set_alpha(0.6)

        ax.set_xticks(positions)
        ax.set_xticklabels([f"{t}\n(n={len(tier_data[t])//1000}K)" for t in tier_names])
        ax.set_ylabel("Output Value")
        ax.set_title("IMU Output Distribution by Tier")
        ax.set_ylim(-0.05, 1.05)
        ax.grid(True, alpha=0.3, axis="y")

        path = _save(fig, "13_tier_comparison_violin")
        assert path.exists()

    def test_viz_14_h3_gate_range_diagram(self):
        """Visualization of h3_mod mapping: [0,1] → gate value."""
        h3_vals = np.linspace(0, 1, 200)

        # Single gate: 0.5 + 0.5 * h3
        single_gate = 0.5 + 0.5 * h3_vals

        # Cumulative with 4 identical tuples
        gate_4 = single_gate ** 4

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        # Single gate function
        ax1.plot(h3_vals, single_gate, color="#2196F3", linewidth=2, label="Single gate")
        ax1.fill_between(h3_vals, 0, single_gate, alpha=0.1, color="#2196F3")
        ax1.set_xlabel("H³ Feature Value")
        ax1.set_ylabel("Gate Multiplier")
        ax1.set_title("Single H³ Gate: 0.5 + 0.5 × h3")
        ax1.axhline(0.5, color="red", linestyle="--", linewidth=0.5, label="Min (h3=0)")
        ax1.axhline(1.0, color="green", linestyle="--", linewidth=0.5, label="Max (h3=1)")
        ax1.legend(fontsize=8)
        ax1.grid(True, alpha=0.3)

        # Cumulative 4-gate product
        for n_gates in [1, 2, 3, 4]:
            gate_n = single_gate ** n_gates
            ax2.plot(h3_vals, gate_n, linewidth=1.5, label=f"{n_gates} gate{'s' if n_gates > 1 else ''}")

        ax2.set_xlabel("H³ Feature Value (all tuples equal)")
        ax2.set_ylabel("Combined Gate")
        ax2.set_title("Cumulative Gate: (0.5 + 0.5 × h3)ⁿ")
        ax2.axhline(0.0625, color="red", linestyle=":", linewidth=0.5, label="Min (0.5⁴)")
        ax2.legend(fontsize=8)
        ax2.grid(True, alpha=0.3)

        fig.suptitle("H³ Temporal Gating Mechanism", fontsize=12)
        plt.tight_layout()

        path = _save(fig, "14_h3_gate_range_diagram")
        assert path.exists()

    def test_viz_15_recurrence_plot(
        self, imu_models, mechanism_outputs, h3_random, random_r3
    ):
        """Recurrence matrix for MEAMN output."""
        model = imu_models[0]
        out = _compute_model_output(model, mechanism_outputs, h3_random, random_r3)
        out_mean = out.mean(axis=-1)[:200]  # subsample
        n = len(out_mean)

        dists = np.abs(out_mean[:, None] - out_mean[None, :])
        eps = np.median(dists) * 0.15
        recurrence = (dists < eps).astype(float)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        ax1.imshow(recurrence, cmap="binary", origin="lower",
                  extent=[0, n / FRAME_RATE, 0, n / FRAME_RATE])
        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel("Time (s)")
        ax1.set_title(f"Recurrence Plot — {model.NAME} (ε={eps:.4f})")

        # Distance matrix
        im = ax2.imshow(dists, cmap="viridis", origin="lower",
                       extent=[0, n / FRAME_RATE, 0, n / FRAME_RATE])
        ax2.set_xlabel("Time (s)")
        ax2.set_ylabel("Time (s)")
        ax2.set_title(f"Distance Matrix — {model.NAME}")
        fig.colorbar(im, ax=ax2, label="L1 Distance", shrink=0.8)

        plt.tight_layout()
        path = _save(fig, "15_recurrence_plot")
        assert path.exists()

    def test_viz_16_information_flow_sankey(
        self, imu_models, mechanism_outputs, zero_mechanism_outputs,
        h3_ones, h3_zeros, random_r3, zero_r3,
    ):
        """Information flow diagram: R³ → Mechanism → H³ → Output."""
        # Compute contribution fractions for each tier
        tiers = {"alpha": imu_models[:3], "beta": imu_models[3:12], "gamma": imu_models[12:]}

        fig, ax = plt.subplots(figsize=(12, 7))

        y_positions = {"alpha": 5, "beta": 3, "gamma": 1}
        bar_height = 0.6

        for tier_name, models in tiers.items():
            y = y_positions[tier_name]
            model = models[0]  # representative

            # Full output
            with torch.no_grad():
                out_full = model.compute(mechanism_outputs, h3_ones, random_r3)
            full_energy = out_full.mean().item()

            # Mechanism only
            with torch.no_grad():
                out_mech = model.compute(mechanism_outputs, h3_ones, zero_r3)
            mech_energy = out_mech.mean().item()

            # R³ only
            with torch.no_grad():
                out_r3 = model.compute(zero_mechanism_outputs, h3_ones, random_r3)
            r3_energy = out_r3.mean().item()

            # H³ suppression
            with torch.no_grad():
                out_h3_off = model.compute(mechanism_outputs, h3_zeros, random_r3)
            h3_suppressed = out_h3_off.mean().item()

            total = mech_energy + r3_energy
            if total > 0:
                mech_frac = mech_energy / total
                r3_frac = r3_energy / total
            else:
                mech_frac = r3_frac = 0.5

            h3_gate = h3_suppressed / max(full_energy, 1e-8)

            color = TIER_COLORS[tier_name]

            # Draw stacked bar
            ax.barh(y, mech_frac, height=bar_height, color="#2196F3", alpha=0.7,
                   label="Mechanism" if tier_name == "alpha" else "")
            ax.barh(y, r3_frac, height=bar_height, left=mech_frac,
                   color="#FF9800", alpha=0.7,
                   label="R³" if tier_name == "alpha" else "")

            # H³ gate indicator
            ax.plot([1.1], [y], marker="o", markersize=15,
                   color=color, markeredgecolor="black")
            ax.text(1.15, y, f"H³ gate\n{h3_gate:.2f}", fontsize=8,
                   va="center", ha="left")

            # Labels
            ax.text(-0.12, y, f"{tier_name.upper()}\n({model.NAME})",
                   fontsize=9, va="center", ha="right", fontweight="bold",
                   color=color)
            ax.text(mech_frac / 2, y, f"{mech_frac:.0%}", fontsize=8,
                   va="center", ha="center", color="white", fontweight="bold")
            ax.text(mech_frac + r3_frac / 2, y, f"{r3_frac:.0%}", fontsize=8,
                   va="center", ha="center", color="white", fontweight="bold")

        ax.set_xlim(-0.2, 1.4)
        ax.set_ylim(-0.5, 6.5)
        ax.set_xlabel("Contribution Fraction")
        ax.set_title("Information Flow — R³ vs Mechanism Contribution by Tier + H³ Gate Effect")
        ax.legend(loc="upper right")
        ax.set_yticks([])
        ax.grid(True, alpha=0.3, axis="x")

        path = _save(fig, "16_information_flow")
        assert path.exists()

    def test_viz_17_memory_consolidation_curve(
        self, imu_models, h3_by_horizon
    ):
        """H³ modulation smoothness at H16 vs H18."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        t_axis = np.arange(SCI_T) / FRAME_RATE

        for h_idx, ax, label in [(16, ax1, "H16 (1s — working memory)"),
                                  (18, ax2, "H18 (2s — consolidation)")]:
            if h_idx not in h3_by_horizon:
                ax.text(0.5, 0.5, f"H{h_idx} not in demand", transform=ax.transAxes,
                       ha="center", va="center")
                continue

            h3_features = h3_by_horizon[h_idx]
            for i, (key, val) in enumerate(sorted(h3_features.items())):
                signal = val[0].numpy()
                ax.plot(t_axis, signal, alpha=0.5, linewidth=0.8,
                       label=f"R³[{key[0]}]" if i < 4 else None)

            std_val = np.mean([v[0].numpy().std() for v in h3_features.values()])
            ax.set_title(f"{label}\nMean σ = {std_val:.4f}")
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("H³ Feature Value")
            ax.set_ylim(-0.05, 1.05)
            if i < 8:
                ax.legend(fontsize=7, loc="upper right")
            ax.grid(True, alpha=0.3)

        fig.suptitle("Memory Consolidation Hierarchy — Shorter Horizons are More Variable",
                    fontsize=12)
        plt.tight_layout()

        path = _save(fig, "17_memory_consolidation_curve")
        assert path.exists()

    def test_viz_18_sigmoid_landscape(self):
        """3D surface of sigmoid(w_m × m + w_r3 × r) for each tier."""
        m_vals = np.linspace(0, 1, 50)
        r_vals = np.linspace(0, 1, 50)
        M, R = np.meshgrid(m_vals, r_vals)

        tier_weights = [
            ("Alpha (0.7m + 0.3r)", 0.7, 0.3),
            ("Beta (0.6m + 0.4r)", 0.6, 0.4),
            ("Gamma (0.5m + 0.5r)", 0.5, 0.5),
        ]

        fig = plt.figure(figsize=(18, 5))

        for i, (title, wm, wr) in enumerate(tier_weights):
            Z = 1 / (1 + np.exp(-(wm * M + wr * R)))

            ax = fig.add_subplot(1, 3, i + 1, projection="3d")
            ax.plot_surface(M, R, Z, cmap="viridis", alpha=0.8,
                          edgecolor="none")
            ax.set_xlabel("Mechanism")
            ax.set_ylabel("R³")
            ax.set_zlabel("σ(z)")
            ax.set_title(title)
            ax.set_zlim(0.4, 0.8)
            ax.view_init(elev=25, azim=135)

        fig.suptitle("Sigmoid Activation Landscape by Tier", fontsize=12)
        plt.tight_layout()

        path = _save(fig, "18_sigmoid_landscape")
        assert path.exists()

    def test_viz_19_saturation_map(
        self, imu_models, mechanism_outputs, h3_random, random_r3
    ):
        """Fraction of saturated outputs per model."""
        names = []
        fractions_low = []
        fractions_high = []
        colors = []

        for model in imu_models:
            out = _compute_model_output(model, mechanism_outputs, h3_random, random_r3)
            total = out.size
            low = (out < 0.05).sum() / total
            high = (out > 0.95).sum() / total

            names.append(model.NAME)
            fractions_low.append(low)
            fractions_high.append(high)
            colors.append(TIER_COLORS[model.TIER])

        fig, ax = plt.subplots(figsize=(14, 5))
        x = np.arange(len(names))
        width = 0.35

        bars_low = ax.bar(x - width / 2, fractions_low, width, label="< 0.05 (low tail)",
                         color="#2196F3", alpha=0.7)
        bars_high = ax.bar(x + width / 2, fractions_high, width, label="> 0.95 (high tail)",
                          color="#FF5722", alpha=0.7)

        # Color x-labels by tier
        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=45, ha="right", fontsize=8)
        for i, label in enumerate(ax.get_xticklabels()):
            label.set_color(colors[i])

        ax.set_ylabel("Fraction of Output Values")
        ax.set_title("Sigmoid Saturation Map — Low and High Tail Fractions")
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3, axis="y")

        # Tier separators
        ax.axvline(2.5, color="black", linewidth=1, linestyle="--", alpha=0.3)
        ax.axvline(11.5, color="black", linewidth=1, linestyle="--", alpha=0.3)

        plt.tight_layout()
        path = _save(fig, "19_saturation_map")
        assert path.exists()

    def test_viz_20_autocorrelation_decay(
        self, imu_models, mechanism_outputs, h3_random, structured_r3
    ):
        """ACF decay curves for all 15 models."""
        fig, ax = plt.subplots(figsize=(12, 6))
        max_lag = 100

        for model in imu_models:
            out = _compute_model_output(model, mechanism_outputs, h3_random, structured_r3)
            out_mean = out.mean(axis=-1)  # (T,)

            x = out_mean - out_mean.mean()
            var = np.var(x)
            if var < 1e-12:
                continue
            acf = np.correlate(x, x, mode="full")
            acf = acf[len(x) - 1:][:max_lag]
            acf = acf / (var * len(x))

            lag_axis = np.arange(max_lag) / FRAME_RATE * 1000  # ms
            color = TIER_COLORS[model.TIER]
            alpha = 0.9 if model.TIER == "alpha" else 0.5
            ax.plot(lag_axis, acf, color=color, alpha=alpha, linewidth=1,
                   label=model.NAME if model.TIER == "alpha" else None)

        ax.axhline(1 / np.e, color="red", linestyle="--", linewidth=0.5,
                  label="1/e threshold")
        ax.axhline(0, color="gray", linewidth=0.5)
        ax.set_xlabel("Lag (ms)")
        ax.set_ylabel("ACF")
        ax.set_title("Temporal Autocorrelation Decay — All 15 IMU Models")
        ax.legend(fontsize=7, loc="upper right", ncol=2)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-0.5, 1.1)

        path = _save(fig, "20_autocorrelation_decay")
        assert path.exists()
