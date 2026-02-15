#!/usr/bin/env python3
"""BCH-R-Nucleus — Consonance Hierarchy Visualization.

Professional dark-theme visualization of BCH response to the 6 canonical
consonance intervals: P1 > P5 > P4 > M3 > m6 > TT.

Reads pre-computed WebLab data and interval markers.

Usage:
    python Lab/WebLab/scripts/visualize_bch_consonance.py
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np
from scipy.ndimage import gaussian_filter1d

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.patches as mpatches

# ======================================================================
# Paths
# ======================================================================
_SCRIPT_DIR = Path(__file__).resolve().parent
_WEBLAB_DIR = _SCRIPT_DIR.parent
_EXP_DIR = _WEBLAB_DIR / "experiments" / "BCH-R-Nucleus"
_PROJECT_ROOT = _WEBLAB_DIR.parent.parent

# ======================================================================
# Theme (matching All-α1 style)
# ======================================================================
BG = "#0a0a0f"
BG_PANEL = "#0d0d14"
GRID_COLOR = "#1a1a2e"
TEXT_COLOR = "#c8c8d4"
TEXT_DIM = "#6b7280"
ACCENT = "#6366f1"

# Interval colors — warm→cool gradient following consonance rank
INTERVAL_COLORS = {
    "Unison (P1)":         "#22c55e",  # green (most consonant)
    "Perfect Fifth (P5)":  "#06b6d4",  # cyan
    "Perfect Fourth (P4)": "#3b82f6",  # blue
    "Major Third (M3)":    "#a855f7",  # purple
    "Minor Sixth (m6)":    "#f97316",  # orange
    "Tritone (TT)":        "#ef4444",  # red (most dissonant)
}

# BCH dimension colors
C_NPS = "#ef4444"
C_HARMONICITY = "#3b82f6"
C_HIERARCHY = "#a855f7"
C_FFR = "#f97316"
C_NPS_T = "#fb7185"
C_HARM_INT = "#60a5fa"
C_CONS_SIG = "#22c55e"
C_TEMPLATE = "#06b6d4"
C_NEURAL_P = "#eab308"
C_CONS_PRED = "#f472b6"
C_PITCH_PROP = "#94a3b8"
C_INTERVAL_E = "#c084fc"

# RAM
C_AN = "#ef4444"; C_CN = "#f97316"; C_IC = "#fbbf24"
C_MGB = "#22c55e"; C_A1_HG = "#3b82f6"; C_STG = "#a855f7"

# Neuro
C_DA = "#ef4444"; C_NE = "#3b82f6"; C_OPI = "#22c55e"; C_5HT = "#f59e0b"

# Ψ³
C_VALENCE = "#10b981"; C_AROUSAL = "#ef4444"
C_TENSION = "#a855f7"; C_DOMINANCE = "#60a5fa"

SIGMA_S = 0.3  # light smoothing for synth (cleaner signal)


# ======================================================================
# Load data
# ======================================================================
def load_experiment():
    """Load all WebLab data + interval markers."""
    with open(_EXP_DIR / "meta.json") as f:
        meta = json.load(f)

    with open(_EXP_DIR / "r3.json") as f:
        r3 = np.array(json.load(f))  # (T_lod, 128)

    with open(_EXP_DIR / "nuclei" / "BCH.json") as f:
        bch_data = json.load(f)
    bch_output = np.array(bch_data["output"])  # (T_lod, 12)

    with open(_EXP_DIR / "ram.json") as f:
        ram = np.array(json.load(f))  # (T_lod, 26)

    with open(_EXP_DIR / "neuro.json") as f:
        neuro = np.array(json.load(f))  # (T_lod, 4)

    with open(_EXP_DIR / "psi.json") as f:
        psi = json.load(f)
    psi_affect = np.array(psi["affect"])
    psi_emotion = np.array(psi["emotion"])

    with open(_EXP_DIR / "interval_markers.json") as f:
        markers = json.load(f)

    stride = meta["lod_stride"]
    frame_rate = meta["frame_rate"]
    T_lod = meta["lod_frames"]
    time_axis = np.arange(T_lod) * stride / frame_rate

    return {
        "meta": meta,
        "time": time_axis,
        "r3": r3,
        "bch": bch_output,
        "ram": ram,
        "neuro": neuro,
        "psi_affect": psi_affect,
        "psi_emotion": psi_emotion,
        "markers": markers,
        "T_lod": T_lod,
        "stride": stride,
        "frame_rate": frame_rate,
    }


# ======================================================================
# Helpers
# ======================================================================
def sm(y: np.ndarray, frame_rate: float) -> np.ndarray:
    sigma = SIGMA_S * frame_rate
    # Adjust for LOD stride
    return gaussian_filter1d(y, sigma=max(1, sigma))


# Collector for auto y-limits
_traces: dict[int, list] = {}
_pid = 0


def begin_panel():
    global _pid
    _pid += 1
    _traces[_pid] = []
    return _pid


def add_line(ax, time, vals, color, label, fr, lw=1.8, ls="-", alpha=0.9):
    smoothed = sm(vals, fr / 4)  # reduced sigma for LOD
    ax.plot(time, smoothed, color=color, linewidth=lw, linestyle=ls,
            alpha=alpha, label=label)
    _traces[_pid].append(smoothed)


def auto_ylim(pid, pad=0.15):
    traces = _traces.get(pid, [])
    if not traces:
        return (-0.05, 1.05)
    all_v = np.concatenate(traces)
    lo, hi = float(np.min(all_v)), float(np.max(all_v))
    span = hi - lo
    if span < 0.02:
        mid = (lo + hi) / 2
        lo, hi = mid - 0.05, mid + 0.05
        span = 0.1
    return (lo - span * pad, hi + span * pad)


def style_panel(ax, title, ylim=None):
    ax.set_facecolor(BG_PANEL)
    ax.set_title(title, fontsize=10, fontweight="bold", color=TEXT_COLOR,
                 loc="left", pad=6)
    ax.set_ylabel("Activation", fontsize=8, fontweight="bold", color=ACCENT)
    if ylim:
        ax.set_ylim(ylim)
    ax.grid(True, alpha=0.15, color=GRID_COLOR, linewidth=0.5)
    for sp in ax.spines.values():
        sp.set_color(GRID_COLOR)
        sp.set_linewidth(0.5)
    ax.tick_params(labelsize=7, colors=TEXT_COLOR)


def add_legend(ax, ncol=3, loc="upper right"):
    leg = ax.legend(fontsize=6.5, ncol=ncol, loc=loc, framealpha=0.3,
                    facecolor=BG_PANEL, edgecolor=GRID_COLOR,
                    labelcolor=TEXT_COLOR, handlelength=1.5, columnspacing=1.0)
    leg.get_frame().set_linewidth(0.5)


def add_interval_bands(ax, markers, duration):
    """Add colored background bands for each interval."""
    for m in markers:
        name = m["name"]
        color = INTERVAL_COLORS.get(name, "#6b7280")
        ax.axvspan(m["start_s"], m["end_s"], alpha=0.08, color=color, zorder=0)


def add_interval_labels(ax, markers, y_pos=0.97):
    """Add interval name labels at top of panel."""
    for m in markers:
        name = m["name"]
        color = INTERVAL_COLORS.get(name, "#6b7280")
        mid = (m["start_s"] + m["end_s"]) / 2
        # Short label
        short = name.split("(")[1].rstrip(")") if "(" in name else name
        ax.text(mid, y_pos, short, fontsize=7, color=color, alpha=0.9,
                ha="center", va="top", transform=ax.get_xaxis_transform(),
                fontweight="bold")


# ======================================================================
# Main
# ======================================================================
def main():
    print("Loading experiment data...")
    D = load_experiment()
    time = D["time"]
    bch = D["bch"]
    markers = D["markers"]
    fr = D["frame_rate"] / D["stride"]
    duration = time[-1]

    # Active RAM regions
    ram_active = {}
    ram_labels = ["A1_HG", "STG", "", "", "", "", "", "", "", "", "",
                  "", "", "", "", "", "", "", "MGB", "", "",
                  "IC", "AN", "CN", "", ""]
    for i in range(D["ram"].shape[1]):
        col = D["ram"][:, i]
        if np.abs(col).max() > 1e-4:
            label = ram_labels[i] if i < len(ram_labels) and ram_labels[i] else f"R{i}"
            ram_active[label] = col

    # =====================================================================
    # Setup matplotlib
    # =====================================================================
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica Neue", "Arial", "DejaVu Sans"],
        "font.size": 9,
        "axes.facecolor": BG_PANEL,
        "figure.facecolor": BG,
        "text.color": TEXT_COLOR,
        "axes.labelcolor": TEXT_COLOR,
        "xtick.color": TEXT_COLOR,
        "ytick.color": TEXT_COLOR,
    })

    height_ratios = [1.0, 2.8, 2.8, 2.2, 1.8, 2.2, 1.8]
    fig_h = sum(height_ratios) * 2.6 + 3.5
    fig = plt.figure(figsize=(24, fig_h))
    gs = GridSpec(7, 1, figure=fig, height_ratios=height_ratios, hspace=0.10,
                  top=0.940, bottom=0.035, left=0.055, right=0.975)

    # =====================================================================
    # Header
    # =====================================================================
    fig.text(0.025, 0.977, "S\u00B3", fontsize=32, fontweight="bold",
             color=ACCENT, va="top")
    fig.text(0.065, 0.977,
             "Musical Intelligence — BCH-R-Nucleus  Consonance Hierarchy Test",
             fontsize=18, fontweight="light", color=TEXT_COLOR, va="top")
    fig.text(0.065, 0.960,
             "Synthetic Piano Dyads: P1 → P5 → P4 → M3 → m6 → TT  "
             "(8s each, C4 base)",
             fontsize=11, fontstyle="italic", color=TEXT_DIM, va="top")

    T_total = D["meta"]["total_frames"]
    fig.text(0.975, 0.977,
             f"R³ 128D  |  H³ 16 tuples  |  C³ BCH 12D",
             fontsize=9, color=TEXT_DIM, va="top", ha="right")
    fig.text(0.975, 0.963,
             f"50 channels  |  {T_total} frames → {D['T_lod']} LOD  |  "
             f"Bidelman & Krishnan 2009",
             fontsize=9, color=TEXT_DIM, va="top", ha="right")

    # =====================================================================
    # Panel 0: Waveform + Interval Labels
    # =====================================================================
    ax0 = fig.add_subplot(gs[0])
    ax0.set_facecolor(BG_PANEL)

    # Generate simple envelope from R³ energy group mean
    energy = D["r3"][:, 7:12].mean(axis=1)
    ax0.fill_between(time, -energy, energy, color="#4338ca", alpha=0.6, linewidth=0)
    ax0.plot(time, energy, color="#818cf8", linewidth=0.3, alpha=0.5)
    ax0.plot(time, -energy, color="#818cf8", linewidth=0.3, alpha=0.5)
    emax = np.max(np.abs(energy)) * 1.4
    ax0.set_ylim(-emax, emax)
    ax0.set_xlim(0, duration)
    ax0.set_ylabel("Energy", fontsize=8, fontweight="bold", color=ACCENT)
    ax0.tick_params(labelsize=6, colors=TEXT_COLOR)
    ax0.set_xticklabels([])
    for sp in ax0.spines.values():
        sp.set_color(GRID_COLOR)
        sp.set_linewidth(0.5)

    add_interval_bands(ax0, markers, duration)
    # Labels above waveform
    for m in markers:
        name = m["name"]
        color = INTERVAL_COLORS.get(name, TEXT_DIM)
        mid = (m["start_s"] + m["end_s"]) / 2
        short = name.split("(")[1].rstrip(")") if "(" in name else name
        freq_label = f"{m['freq2']:.0f}Hz"
        ax0.text(mid, emax * 0.85, short, fontsize=9, color=color, ha="center",
                 fontweight="bold", alpha=0.9)
        ax0.text(mid, -emax * 0.85, freq_label, fontsize=6.5, color=color,
                 ha="center", alpha=0.7)

    # =====================================================================
    # Panel 1: BCH E+M Layer (6D)
    # =====================================================================
    ax1 = fig.add_subplot(gs[1])
    pid1 = begin_panel()
    add_line(ax1, time, bch[:, 0], C_NPS, "f01 NPS", fr, lw=2.2)
    add_line(ax1, time, bch[:, 1], C_HARMONICITY, "f02 Harmonicity", fr, lw=2.2)
    add_line(ax1, time, bch[:, 2], C_HIERARCHY, "f03 Hierarchy", fr, lw=2.0)
    add_line(ax1, time, bch[:, 3], C_FFR, "f04 FFR-Behavior", fr, lw=1.8, alpha=0.8)
    add_line(ax1, time, bch[:, 4], C_NPS_T, "nps_t", fr, lw=1.5, ls="--", alpha=0.7)
    add_line(ax1, time, bch[:, 5], C_HARM_INT, "harm_interval", fr, lw=1.5, ls="--", alpha=0.7)
    style_panel(ax1, "BCH E+M Layer — Internal Neural Circuit (6D)", ylim=auto_ylim(pid1))
    add_legend(ax1, ncol=3)
    add_interval_bands(ax1, markers, duration)
    add_interval_labels(ax1, markers)
    ax1.set_xlim(0, duration)
    ax1.set_xticklabels([])

    # =====================================================================
    # Panel 2: BCH P+F Layer (6D)
    # =====================================================================
    ax2 = fig.add_subplot(gs[2])
    pid2 = begin_panel()
    add_line(ax2, time, bch[:, 6], C_CONS_SIG, "consonance_signal", fr, lw=2.5)
    add_line(ax2, time, bch[:, 7], C_TEMPLATE, "template_match", fr, lw=2.2)
    add_line(ax2, time, bch[:, 8], C_NEURAL_P, "neural_pitch", fr, lw=2.0)
    add_line(ax2, time, bch[:, 9], C_CONS_PRED, "consonance_pred", fr, lw=1.6, ls="--", alpha=0.8)
    add_line(ax2, time, bch[:, 10], C_PITCH_PROP, "pitch_propagation", fr, lw=1.6, ls="--", alpha=0.7)
    add_line(ax2, time, bch[:, 11], C_INTERVAL_E, "interval_expect", fr, lw=1.6, ls="--", alpha=0.8)
    style_panel(ax2, "BCH P+F Layer — Cognitive Output (6D)", ylim=auto_ylim(pid2))
    add_legend(ax2, ncol=3)
    add_interval_bands(ax2, markers, duration)
    add_interval_labels(ax2, markers)
    ax2.set_xlim(0, duration)
    ax2.set_xticklabels([])

    # =====================================================================
    # Panel 3: RAM — Brain Regions
    # =====================================================================
    ax3 = fig.add_subplot(gs[3])
    pid3 = begin_panel()
    ram_c = {"AN": C_AN, "CN": C_CN, "IC": C_IC, "MGB": C_MGB,
             "A1_HG": C_A1_HG, "STG": C_STG}
    ram_lw = {"IC": 2.5, "A1_HG": 2.0, "MGB": 2.0}
    for rname in ["AN", "CN", "IC", "MGB", "A1_HG", "STG"]:
        if rname in ram_active:
            add_line(ax3, time, ram_active[rname],
                     ram_c.get(rname, "#94a3b8"), rname, fr,
                     lw=ram_lw.get(rname, 1.8))
    style_panel(ax3, f"Region Activation Map — Ascending Auditory Pathway ({len(ram_active)} / 26)",
                ylim=auto_ylim(pid3))
    add_legend(ax3, ncol=3)
    add_interval_bands(ax3, markers, duration)
    add_interval_labels(ax3, markers)
    ax3.set_xlim(0, duration)
    ax3.set_xticklabels([])

    # =====================================================================
    # Panel 4: Neurochemistry (4D)
    # =====================================================================
    ax4 = fig.add_subplot(gs[4])
    pid4 = begin_panel()
    add_line(ax4, time, D["neuro"][:, 0], C_DA, "DA (Dopamine)", fr, lw=2.2)
    add_line(ax4, time, D["neuro"][:, 1], C_NE, "NE", fr, lw=1.4, ls="--", alpha=0.5)
    add_line(ax4, time, D["neuro"][:, 2], C_OPI, "OPI", fr, lw=1.4, ls="--", alpha=0.5)
    add_line(ax4, time, D["neuro"][:, 3], C_5HT, "5HT (Serotonin)", fr, lw=1.8, alpha=0.8)
    style_panel(ax4, "Neurochemical State (4D)", ylim=auto_ylim(pid4))
    add_legend(ax4, ncol=4)
    add_interval_bands(ax4, markers, duration)
    add_interval_labels(ax4, markers)
    ax4.set_xlim(0, duration)
    ax4.set_xticklabels([])

    # =====================================================================
    # Panel 5: Ψ³ Affect (4D)
    # =====================================================================
    ax5 = fig.add_subplot(gs[5])
    pid5 = begin_panel()
    add_line(ax5, time, D["psi_affect"][:, 0], C_VALENCE, "valence", fr, lw=2.5)
    add_line(ax5, time, D["psi_affect"][:, 1], C_AROUSAL, "arousal", fr, lw=2.0, alpha=0.7)
    add_line(ax5, time, D["psi_affect"][:, 2], C_TENSION, "tension", fr, lw=2.2)
    add_line(ax5, time, D["psi_affect"][:, 3], C_DOMINANCE, "dominance", fr, lw=1.6, alpha=0.6)
    style_panel(ax5, "Ψ³ Affect — Core Emotional Coordinates (4D)", ylim=auto_ylim(pid5))
    add_legend(ax5, ncol=4)
    add_interval_bands(ax5, markers, duration)
    add_interval_labels(ax5, markers)
    ax5.set_xlim(0, duration)
    ax5.set_xticklabels([])

    # =====================================================================
    # Panel 6: Per-interval consonance bar summary
    # =====================================================================
    ax6 = fig.add_subplot(gs[6])
    ax6.set_facecolor(BG_PANEL)

    # Compute mean BCH values per interval (from steady-state, skip first 1s)
    bar_names = []
    cons_means = []
    nps_means = []
    harm_means = []
    hier_means = []
    bar_colors = []
    skip_frames = int(1.0 * fr)  # skip warmup

    for m in markers:
        name = m["name"]
        short = name.split("(")[1].rstrip(")") if "(" in name else name
        bar_names.append(short)
        bar_colors.append(INTERVAL_COLORS.get(name, TEXT_DIM))

        # Find LOD frame range for this interval
        f_start = int(m["start_s"] * fr)
        f_end = int(m["end_s"] * fr)
        f_start = min(f_start + skip_frames, f_end - 1)
        f_end = min(f_end, len(bch))

        seg = bch[f_start:f_end, :]
        if len(seg) > 0:
            cons_means.append(seg[:, 6].mean())
            nps_means.append(seg[:, 0].mean())
            harm_means.append(seg[:, 1].mean())
            hier_means.append(seg[:, 2].mean())
        else:
            cons_means.append(0)
            nps_means.append(0)
            harm_means.append(0)
            hier_means.append(0)

    x = np.arange(len(bar_names))
    w = 0.2
    bars1 = ax6.bar(x - 1.5*w, cons_means, w, color=[c for c in bar_colors],
                     alpha=0.9, label="Consonance Signal")
    bars2 = ax6.bar(x - 0.5*w, nps_means, w, color=[c for c in bar_colors],
                     alpha=0.6, label="NPS", hatch="//")
    bars3 = ax6.bar(x + 0.5*w, harm_means, w, color=[c for c in bar_colors],
                     alpha=0.4, label="Harmonicity", hatch="\\\\")
    bars4 = ax6.bar(x + 1.5*w, hier_means, w, color=[c for c in bar_colors],
                     alpha=0.3, label="Hierarchy", hatch="xx")

    ax6.set_xticks(x)
    ax6.set_xticklabels(bar_names, fontsize=9, fontweight="bold")
    for tick, color in zip(ax6.get_xticklabels(), bar_colors):
        tick.set_color(color)

    ax6.set_title("BCH Response Summary — Mean Activation per Interval (steady-state)",
                  fontsize=10, fontweight="bold", color=TEXT_COLOR, loc="left", pad=6)
    ax6.set_ylabel("Mean", fontsize=8, fontweight="bold", color=ACCENT)
    ax6.grid(True, alpha=0.15, color=GRID_COLOR, linewidth=0.5, axis="y")
    for sp in ax6.spines.values():
        sp.set_color(GRID_COLOR)
        sp.set_linewidth(0.5)
    ax6.tick_params(labelsize=7, colors=TEXT_COLOR)

    # Custom legend
    legend_patches = [
        mpatches.Patch(facecolor=TEXT_COLOR, alpha=0.9, label="Consonance"),
        mpatches.Patch(facecolor=TEXT_COLOR, alpha=0.6, hatch="//", label="NPS"),
        mpatches.Patch(facecolor=TEXT_COLOR, alpha=0.4, hatch="\\\\", label="Harmonicity"),
        mpatches.Patch(facecolor=TEXT_COLOR, alpha=0.3, hatch="xx", label="Hierarchy"),
    ]
    leg = ax6.legend(handles=legend_patches, fontsize=7, ncol=4, loc="upper right",
                     framealpha=0.3, facecolor=BG_PANEL, edgecolor=GRID_COLOR,
                     labelcolor=TEXT_COLOR)
    leg.get_frame().set_linewidth(0.5)

    # Expected ranking annotation
    ax6.text(0.5, -0.18,
             "Expected Hierarchy (Bidelman 2009): P1 > P5 > P4 > M3 > m6 > TT",
             fontsize=8, color=TEXT_DIM, ha="center",
             transform=ax6.transAxes, fontstyle="italic")

    # =====================================================================
    # Save
    # =====================================================================
    fig_path = _EXP_DIR / "BCH-R-Nucleus_consonance_hierarchy.png"
    fig.savefig(str(fig_path), dpi=200, bbox_inches="tight", pad_inches=0.3,
                facecolor=BG, edgecolor="none")
    plt.close(fig)
    print(f"Saved: {fig_path}")

    # Print consonance ranking
    print("\nBCH Consonance Ranking (mean consonance_signal):")
    ranked = sorted(zip(bar_names, cons_means), key=lambda x: -x[1])
    for i, (name, val) in enumerate(ranked):
        expected_rank = ["P1", "P5", "P4", "M3", "m6", "TT"]
        match = "✓" if name == expected_rank[i] else "✗"
        print(f"  {i+1}. {name:>4} = {val:.4f}  {match}")


if __name__ == "__main__":
    main()
