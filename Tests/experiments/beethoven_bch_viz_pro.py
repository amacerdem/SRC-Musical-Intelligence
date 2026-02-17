#!/usr/bin/env python3
"""Beethoven Pathétique BCH — Professional Dark-Theme Visualization.

Single-image, 7-panel + waveform visualization of ALL 50 time series
produced by BCH (Brainstem Consonance Hierarchy) from Beethoven's
Pathétique Sonata Op.13 I. Grave–Allegro (first 60 seconds).

Style: Matches the All-α1 Comprehensive Analysis format.

Usage:
    python Tests/experiments/beethoven_bch_viz_pro.py
"""
from __future__ import annotations

import os
import sys

_PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import librosa
import numpy as np
import torch
from scipy.ndimage import gaussian_filter1d

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from Musical_Intelligence.ear.r3 import R3Extractor
from Musical_Intelligence.ear.h3 import H3Extractor
from Musical_Intelligence.brain.orchestrator import BrainOrchestrator
from Musical_Intelligence.brain.units.spu.relays.bch import BCH
from Musical_Intelligence.brain.regions import ALL_REGIONS

# ======================================================================
# Theme constants (matching All-α1 style)
# ======================================================================
BG = "#0a0a0f"
BG_PANEL = "#0d0d14"
GRID_COLOR = "#1a1a2e"
TEXT_COLOR = "#c8c8d4"
TEXT_DIM = "#6b7280"
ACCENT = "#6366f1"

# ======================================================================
# Color palettes per panel
# ======================================================================

# Panel 1: BCH E+M Layer (Internal Neural Circuit)
C_NPS = "#ef4444"         # red
C_HARMONICITY = "#3b82f6" # blue
C_HIERARCHY = "#a855f7"   # purple
C_FFR = "#f97316"         # orange
C_NPS_T = "#fb7185"       # rose (dashed)
C_HARM_INT = "#60a5fa"    # light blue (dashed)

# Panel 2: BCH P+F Layer (Cognitive Output)
C_CONS_SIG = "#22c55e"    # green
C_TEMPLATE = "#06b6d4"    # cyan
C_NEURAL_P = "#eab308"    # yellow
C_CONS_PRED = "#f472b6"   # pink (dashed)
C_PITCH_PROP = "#94a3b8"  # slate (dashed)
C_INTERVAL = "#c084fc"    # lavender (dashed)

# Panel 3: RAM (Brain Regions)
C_AN = "#ef4444"
C_CN = "#f97316"
C_IC = "#fbbf24"
C_MGB = "#22c55e"
C_A1_HG = "#3b82f6"
C_STG = "#a855f7"

# Panel 4: Neurochemistry
C_DA = "#ef4444"
C_NE = "#3b82f6"
C_OPI = "#22c55e"
C_5HT = "#f59e0b"

# Panel 5: Ψ³ Affect
C_VALENCE = "#10b981"
C_AROUSAL = "#ef4444"
C_TENSION = "#a855f7"
C_DOMINANCE = "#60a5fa"

# Panel 6: Ψ³ Emotion (7D)
C_JOY = "#fbbf24"
C_SADNESS = "#3b82f6"
C_FEAR = "#ef4444"
C_AWE = "#a855f7"
C_NOSTALGIA = "#f97316"
C_TENDERNESS = "#14b8a6"
C_SERENITY = "#22c55e"

# Panel 7: Ψ³ Extended (Aesthetic + Bodily + Cognitive + Temporal)
C_BEAUTY = "#f59e0b"
C_GROOVE = "#f472b6"
C_FLOW = "#06b6d4"
C_SURPRISE = "#ef4444"
C_CLOSURE = "#22c55e"
C_CHILLS = "#a855f7"
C_MOVEMENT = "#fb7185"
C_BREATH = "#94a3b8"
C_TRELEASE = "#14b8a6"
C_FAMILIAR = "#f97316"
C_ABSORB = "#60a5fa"
C_EXPECT = "#eab308"
C_ATTN = "#c084fc"
C_ANTICIP = "#ef4444"
C_RESOLUT = "#22c55e"
C_BUILDUP = "#f59e0b"
C_RELEASE = "#3b82f6"

# Musical moment highlight colors
GRAVE_COLOR = "#6366f1"     # indigo
ALLEGRO_COLOR = "#f59e0b"   # gold
DISSONANT_COLOR = "#ef4444" # red

# ======================================================================
# Audio & pipeline constants
# ======================================================================
AUDIO_PATH = os.path.join(
    _PROJECT_ROOT,
    "Test-Audio",
    "Beethoven - Pathetique Sonata Op13 I. Grave - Allegro.wav",
)
FIG_DIR = os.path.join(_PROJECT_ROOT, "Tests", "reports")
SR = 44100
HOP = 256
N_MELS = 128
FRAME_RATE = SR / HOP
DURATION_S = 60.0
SIGMA_S = 0.8  # Gaussian smoothing sigma in seconds


# ======================================================================
# Pipeline
# ======================================================================
def run_pipeline(device: torch.device):
    """Run BCH pipeline and return all data."""
    y_full, _ = librosa.load(AUDIO_PATH, sr=SR, mono=True, duration=DURATION_S)

    mel = librosa.feature.melspectrogram(
        y=y_full, sr=SR, n_mels=N_MELS, hop_length=HOP, n_fft=1024,
    )
    mel_db = librosa.power_to_db(mel, ref=np.max)
    mel_norm = (mel_db - mel_db.min()) / (mel_db.max() - mel_db.min() + 1e-8)
    mel_t = torch.tensor(mel_norm, dtype=torch.float32, device=device).unsqueeze(0)

    print("  R³ ...", flush=True)
    r3_out = R3Extractor().extract(mel_t)
    r3 = r3_out.features

    print("  H³ ...", flush=True)
    bch = BCH()
    demand = bch.h3_demand_tuples()
    h3_out = H3Extractor().extract(r3, demand)

    h3_gpu = {k: v.to(device) for k, v in h3_out.features.items()}
    r3_gpu = r3.to(device)

    print("  C³ ...", flush=True)
    brain = BrainOrchestrator(nuclei=[bch])
    brain_out = brain.process(r3_gpu, h3_gpu)
    bch_full = bch.compute(h3_gpu, r3_gpu)

    T = r3.shape[1]

    return {
        "waveform": y_full,
        "T": T,
        "time": np.arange(T) / FRAME_RATE,
        "bch": bch_full[0].cpu().numpy(),
        "ram": brain_out.ram[0].cpu().numpy(),
        "neuro": brain_out.neuro[0].cpu().numpy(),
        "psi_affect": brain_out.psi.affect[0].cpu().numpy(),
        "psi_emotion": brain_out.psi.emotion[0].cpu().numpy(),
        "psi_aesthetic": brain_out.psi.aesthetic[0].cpu().numpy(),
        "psi_bodily": brain_out.psi.bodily[0].cpu().numpy(),
        "psi_cognitive": brain_out.psi.cognitive[0].cpu().numpy(),
        "psi_temporal": brain_out.psi.temporal[0].cpu().numpy(),
    }


# ======================================================================
# Helpers
# ======================================================================
def sm(y: np.ndarray) -> np.ndarray:
    """Gaussian smooth for visual clarity."""
    sigma = SIGMA_S * FRAME_RATE
    return gaussian_filter1d(y, sigma=sigma)


# Collector for auto y-limits
_panel_traces: dict[int, list[np.ndarray]] = {}
_panel_id = 0


def begin_panel():
    """Start collecting traces for auto y-range."""
    global _panel_id
    _panel_id += 1
    _panel_traces[_panel_id] = []
    return _panel_id


def add_line(ax, time, vals, color, label, lw=1.8, ls="-", alpha=0.9):
    """Add a smoothed trace and record for auto-ylim."""
    smoothed = sm(vals)
    ax.plot(time, smoothed, color=color, linewidth=lw, linestyle=ls,
            alpha=alpha, label=label)
    if _panel_id in _panel_traces:
        _panel_traces[_panel_id].append(smoothed)


def auto_ylim(panel_id: int, pad_frac: float = 0.12) -> tuple[float, float]:
    """Compute y-limits from all traces in a panel."""
    traces = _panel_traces.get(panel_id, [])
    if not traces:
        return (-0.05, 1.05)
    all_vals = np.concatenate(traces)
    lo, hi = float(np.min(all_vals)), float(np.max(all_vals))
    span = hi - lo
    if span < 0.01:
        # Very flat — center and expand
        mid = (lo + hi) / 2
        lo, hi = mid - 0.05, mid + 0.05
    pad = span * pad_frac
    return (lo - pad, hi + pad)


def style_panel(ax, title, ylabel="Activation", ylim=None):
    """Apply dark-theme styling to a panel."""
    ax.set_facecolor(BG_PANEL)
    ax.set_title(title, fontsize=10, fontweight="bold", color=TEXT_COLOR,
                 loc="left", pad=6)
    ax.set_ylabel(ylabel, fontsize=8, fontweight="bold", color=ACCENT)
    if ylim is not None:
        ax.set_ylim(ylim)
    ax.grid(True, alpha=0.15, color=GRID_COLOR, linewidth=0.5)
    for spine in ax.spines.values():
        spine.set_color(GRID_COLOR)
        spine.set_linewidth(0.5)
    ax.tick_params(labelsize=7, colors=TEXT_COLOR)
    ax.set_xlim(0, None)


def add_legend(ax, ncol=3, loc="upper right"):
    """Add styled legend."""
    leg = ax.legend(
        fontsize=6.5, ncol=ncol, loc=loc,
        framealpha=0.3, facecolor=BG_PANEL, edgecolor=GRID_COLOR,
        labelcolor=TEXT_COLOR, handlelength=1.5, columnspacing=1.0,
    )
    leg.get_frame().set_linewidth(0.5)


def add_moment(ax, t_start, t_end, color, label=None, alpha=0.08):
    """Add a highlighted musical moment region."""
    ax.axvspan(t_start, t_end, alpha=alpha, color=color, zorder=0)
    if label:
        mid = (t_start + t_end) / 2
        ax.text(mid, 0.97, label, fontsize=6.5, color=color, alpha=0.8,
                ha="center", va="top", transform=ax.get_xaxis_transform(),
                fontweight="bold")


# ======================================================================
# Main visualization
# ======================================================================
def main():
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"Device: {device}")
    print("Running pipeline...")
    D = run_pipeline(device)

    time = D["time"]
    bch = D["bch"]
    T = D["T"]
    duration = time[-1]

    # Active RAM
    active_ram = {}
    ram_colors = {}
    ram_palette = {
        "AN": C_AN, "CN": C_CN, "IC": C_IC,
        "MGB": C_MGB, "A1_HG": C_A1_HG, "STG": C_STG,
    }
    for region in ALL_REGIONS:
        col = D["ram"][:, region.index]
        if np.abs(col).max() > 1e-5:
            active_ram[region.abbreviation] = col
            ram_colors[region.abbreviation] = ram_palette.get(
                region.abbreviation, "#94a3b8"
            )

    # Detect musical moments from consonance
    cons = sm(bch[:, 6])
    grave_end = 10.0

    # Dissonant moment clusters
    dissonant_frames = np.argsort(cons)[:500]
    dissonant_times = dissonant_frames / FRAME_RATE
    dis_clusters = []
    if len(dissonant_times) > 0:
        sorted_t = np.sort(dissonant_times)
        cs, ce = sorted_t[0], sorted_t[0]
        for t in sorted_t[1:]:
            if t - ce < 2.0:
                ce = t
            else:
                if ce - cs > 0.5:
                    dis_clusters.append((cs, ce))
                cs, ce = t, t
        if ce - cs > 0.5:
            dis_clusters.append((cs, ce))

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

    height_ratios = [1.0, 2.8, 2.8, 2.4, 1.8, 2.2, 2.8]
    fig_height = sum(height_ratios) * 2.6 + 3.5
    fig = plt.figure(figsize=(24, fig_height))
    gs = GridSpec(
        7, 1, figure=fig,
        height_ratios=height_ratios,
        hspace=0.10,
        top=0.945, bottom=0.035, left=0.055, right=0.975,
    )

    # =====================================================================
    # Header
    # =====================================================================
    fig.text(
        0.025, 0.977, "S\u00B3",
        fontsize=32, fontweight="bold", color=ACCENT,
        va="top", ha="left",
    )
    fig.text(
        0.065, 0.977,
        "Musical Intelligence — BCH Single-Nucleus Analysis",
        fontsize=18, fontweight="light", color=TEXT_COLOR,
        va="top", ha="left",
    )
    fig.text(
        0.065, 0.960,
        "Beethoven — Pathétique Sonata Op.13 I. Grave–Allegro  (first 60s)",
        fontsize=11, fontstyle="italic", color=TEXT_DIM,
        va="top", ha="left",
    )
    n_active_ram = len(active_ram)
    total_ch = 12 + n_active_ram + 4 + 28
    fig.text(
        0.975, 0.977,
        f"R³ 97D  |  H³ 16 tuples  |  C³ BCH 12D",
        fontsize=9, color=TEXT_DIM, va="top", ha="right",
    )
    fig.text(
        0.975, 0.963,
        f"{total_ch} channels  |  {T} frames @ {FRAME_RATE:.1f} Hz  |  MPS GPU",
        fontsize=9, color=TEXT_DIM, va="top", ha="right",
    )

    def moments(ax):
        add_moment(ax, 0, grave_end, GRAVE_COLOR, alpha=0.06)
        for cs, ce in dis_clusters[:3]:
            add_moment(ax, cs, ce, DISSONANT_COLOR, alpha=0.06)

    # =====================================================================
    # Panel 0: Waveform
    # =====================================================================
    ax0 = fig.add_subplot(gs[0])
    ax0.set_facecolor(BG_PANEL)

    wav = D["waveform"]
    envelope = np.abs(wav)
    from scipy.signal import resample
    env_ds = resample(envelope, T)
    env_smooth = gaussian_filter1d(env_ds, sigma=FRAME_RATE * 0.05)

    ax0.fill_between(time, -env_smooth, env_smooth,
                      color="#4338ca", alpha=0.6, linewidth=0)
    ax0.plot(time, env_smooth, color="#818cf8", linewidth=0.3, alpha=0.5)
    ax0.plot(time, -env_smooth, color="#818cf8", linewidth=0.3, alpha=0.5)
    ax0.set_ylim(-np.max(env_smooth) * 1.3, np.max(env_smooth) * 1.3)
    ax0.set_xlim(0, duration)
    ax0.set_ylabel("Audio", fontsize=8, fontweight="bold", color=ACCENT)
    ax0.tick_params(labelsize=6, colors=TEXT_COLOR)
    ax0.set_xticklabels([])
    for spine in ax0.spines.values():
        spine.set_color(GRID_COLOR)
        spine.set_linewidth(0.5)

    ax0.text(grave_end / 2, np.max(env_smooth) * 1.15, "Grave",
             fontsize=8, color=GRAVE_COLOR, ha="center", fontweight="bold", alpha=0.8)
    ax0.text((grave_end + duration) / 2, np.max(env_smooth) * 1.15,
             "Allegro di molto e con brio",
             fontsize=8, color=ALLEGRO_COLOR, ha="center", fontweight="bold", alpha=0.8)
    ax0.axvline(grave_end, color=GRID_COLOR, linewidth=0.8, linestyle="--", alpha=0.5)
    moments(ax0)

    # =====================================================================
    # Panel 1: BCH E+M Layer (Internal Neural Circuit, 6D)
    # =====================================================================
    ax1 = fig.add_subplot(gs[1])
    pid1 = begin_panel()

    add_line(ax1, time, bch[:, 0], C_NPS, "f01 NPS", lw=2.2)
    add_line(ax1, time, bch[:, 1], C_HARMONICITY, "f02 Harmonicity", lw=2.2)
    add_line(ax1, time, bch[:, 2], C_HIERARCHY, "f03 Hierarchy", lw=2.0)
    add_line(ax1, time, bch[:, 3], C_FFR, "f04 FFR-Behavior", lw=1.8, alpha=0.8)
    add_line(ax1, time, bch[:, 4], C_NPS_T, "nps_t", lw=1.5, ls="--", alpha=0.7)
    add_line(ax1, time, bch[:, 5], C_HARM_INT, "harm_interval", lw=1.5, ls="--", alpha=0.7)

    style_panel(ax1, "BCH E+M Layer — Internal Neural Circuit (6D)",
                ylim=auto_ylim(pid1))
    add_legend(ax1, ncol=3)
    moments(ax1)
    ax1.set_xticklabels([])

    # =====================================================================
    # Panel 2: BCH P+F Layer (Cognitive Output, 6D)
    # =====================================================================
    ax2 = fig.add_subplot(gs[2])
    pid2 = begin_panel()

    add_line(ax2, time, bch[:, 6], C_CONS_SIG, "consonance_signal", lw=2.5)
    add_line(ax2, time, bch[:, 7], C_TEMPLATE, "template_match", lw=2.2)
    add_line(ax2, time, bch[:, 8], C_NEURAL_P, "neural_pitch", lw=2.0)
    add_line(ax2, time, bch[:, 9], C_CONS_PRED, "consonance_pred", lw=1.6, ls="--", alpha=0.8)
    add_line(ax2, time, bch[:, 10], C_PITCH_PROP, "pitch_propagation", lw=1.6, ls="--", alpha=0.7)
    add_line(ax2, time, bch[:, 11], C_INTERVAL, "interval_expect", lw=1.6, ls="--", alpha=0.8)

    style_panel(ax2, "BCH P+F Layer — Cognitive Output (6D, External+Hybrid)",
                ylim=auto_ylim(pid2))
    add_legend(ax2, ncol=3)
    moments(ax2)
    ax2.set_xticklabels([])

    # =====================================================================
    # Panel 3: RAM (6 active regions)
    # =====================================================================
    ax3 = fig.add_subplot(gs[3])
    pid3 = begin_panel()

    ram_order = ["AN", "CN", "IC", "MGB", "A1_HG", "STG"]
    ram_lw = {"AN": 1.8, "CN": 1.8, "IC": 2.5, "MGB": 2.0, "A1_HG": 2.0, "STG": 1.6}
    for rname in ram_order:
        if rname in active_ram:
            add_line(ax3, time, active_ram[rname], ram_colors[rname],
                     rname, lw=ram_lw.get(rname, 1.8))

    style_panel(ax3,
                f"Region Activation Map — Ascending Auditory Pathway ({n_active_ram} / 26)",
                ylim=auto_ylim(pid3))
    add_legend(ax3, ncol=3)
    moments(ax3)
    ax3.set_xticklabels([])

    # =====================================================================
    # Panel 4: Neurochemistry (4D)
    # =====================================================================
    ax4 = fig.add_subplot(gs[4])
    pid4 = begin_panel()

    add_line(ax4, time, D["neuro"][:, 0], C_DA, "DA (Dopamine)", lw=2.2)
    add_line(ax4, time, D["neuro"][:, 1], C_NE, "NE (Norepinephrine)", lw=1.6, ls="--", alpha=0.6)
    add_line(ax4, time, D["neuro"][:, 2], C_OPI, "OPI (Opioid)", lw=1.6, ls="--", alpha=0.6)
    add_line(ax4, time, D["neuro"][:, 3], C_5HT, "5HT (Serotonin)", lw=1.8, alpha=0.8)

    style_panel(ax4, "Neurochemical State (4D)", ylim=auto_ylim(pid4))
    add_legend(ax4, ncol=4)
    moments(ax4)
    ax4.set_xticklabels([])

    # =====================================================================
    # Panel 5: Ψ³ Affect + Emotion (11D)
    # =====================================================================
    ax5 = fig.add_subplot(gs[5])
    pid5 = begin_panel()

    # Affect — solid, thicker
    add_line(ax5, time, D["psi_affect"][:, 0], C_VALENCE, "valence", lw=2.5)
    add_line(ax5, time, D["psi_affect"][:, 1], C_AROUSAL, "arousal", lw=2.0, alpha=0.7)
    add_line(ax5, time, D["psi_affect"][:, 2], C_TENSION, "tension", lw=2.2)
    add_line(ax5, time, D["psi_affect"][:, 3], C_DOMINANCE, "dominance", lw=1.6, alpha=0.6)

    # Emotion — dashed, thinner
    add_line(ax5, time, D["psi_emotion"][:, 0], C_JOY, "joy", lw=1.5, ls="--", alpha=0.8)
    add_line(ax5, time, D["psi_emotion"][:, 1], C_SADNESS, "sadness", lw=1.5, ls="--", alpha=0.8)
    add_line(ax5, time, D["psi_emotion"][:, 2], C_FEAR, "fear", lw=1.4, ls=":", alpha=0.7)
    add_line(ax5, time, D["psi_emotion"][:, 3], C_AWE, "awe", lw=1.4, ls=":", alpha=0.7)
    add_line(ax5, time, D["psi_emotion"][:, 4], C_NOSTALGIA, "nostalgia", lw=1.4, ls=":", alpha=0.7)
    add_line(ax5, time, D["psi_emotion"][:, 5], C_TENDERNESS, "tenderness", lw=1.4, ls=":", alpha=0.7)
    add_line(ax5, time, D["psi_emotion"][:, 6], C_SERENITY, "serenity", lw=1.4, ls=":", alpha=0.7)

    style_panel(ax5, "Ψ³ Affect (4D) + Emotion (7D)", ylim=auto_ylim(pid5))
    add_legend(ax5, ncol=4, loc="upper right")
    moments(ax5)
    ax5.set_xticklabels([])

    # =====================================================================
    # Panel 6: Ψ³ Extended (17D)
    # =====================================================================
    ax6 = fig.add_subplot(gs[6])
    pid6 = begin_panel()

    # Aesthetic — solid
    add_line(ax6, time, D["psi_aesthetic"][:, 0], C_BEAUTY, "beauty", lw=2.0)
    add_line(ax6, time, D["psi_aesthetic"][:, 1], C_GROOVE, "groove", lw=1.6, alpha=0.7)
    add_line(ax6, time, D["psi_aesthetic"][:, 2], C_FLOW, "flow", lw=1.6, alpha=0.7)
    add_line(ax6, time, D["psi_aesthetic"][:, 3], C_SURPRISE, "surprise", lw=1.8)
    add_line(ax6, time, D["psi_aesthetic"][:, 4], C_CLOSURE, "closure", lw=1.8)

    # Bodily — dashed
    add_line(ax6, time, D["psi_bodily"][:, 0], C_CHILLS, "chills", lw=1.5, ls="--", alpha=0.8)
    add_line(ax6, time, D["psi_bodily"][:, 1], C_MOVEMENT, "movement", lw=1.5, ls="--", alpha=0.7)
    add_line(ax6, time, D["psi_bodily"][:, 2], C_BREATH, "breathing", lw=1.3, ls="--", alpha=0.6)
    add_line(ax6, time, D["psi_bodily"][:, 3], C_TRELEASE, "t_release", lw=1.5, ls="--", alpha=0.7)

    # Cognitive — dotted
    add_line(ax6, time, D["psi_cognitive"][:, 0], C_FAMILIAR, "familiarity", lw=1.4, ls=":", alpha=0.7)
    add_line(ax6, time, D["psi_cognitive"][:, 1], C_ABSORB, "absorption", lw=1.4, ls=":", alpha=0.7)
    add_line(ax6, time, D["psi_cognitive"][:, 2], C_EXPECT, "expectation", lw=1.4, ls=":", alpha=0.7)
    add_line(ax6, time, D["psi_cognitive"][:, 3], C_ATTN, "attention", lw=1.4, ls=":", alpha=0.7)

    # Temporal — dash-dot
    add_line(ax6, time, D["psi_temporal"][:, 0], C_ANTICIP, "anticipation", lw=1.5, ls="-.", alpha=0.8)
    add_line(ax6, time, D["psi_temporal"][:, 1], C_RESOLUT, "resolution", lw=1.5, ls="-.", alpha=0.7)
    add_line(ax6, time, D["psi_temporal"][:, 2], C_BUILDUP, "buildup", lw=1.5, ls="-.", alpha=0.7)
    add_line(ax6, time, D["psi_temporal"][:, 3], C_RELEASE, "release", lw=1.5, ls="-.", alpha=0.7)

    style_panel(ax6, "Ψ³ Aesthetic (5D) + Bodily (4D) + Cognitive (4D) + Temporal (4D)",
                ylim=auto_ylim(pid6))
    add_legend(ax6, ncol=6, loc="upper right")
    moments(ax6)
    ax6.set_xlabel("Time (seconds)", fontsize=9, color=TEXT_COLOR)

    # =====================================================================
    # Save
    # =====================================================================
    os.makedirs(FIG_DIR, exist_ok=True)
    fig_path = os.path.join(
        FIG_DIR,
        "Beethoven - Pathetique Sonata Op13 I. Grave - Allegro_bch_full.png",
    )
    fig.savefig(fig_path, dpi=200, bbox_inches="tight", pad_inches=0.3,
                facecolor=BG, edgecolor="none")
    plt.close(fig)
    print(f"\nSaved: {fig_path}")


if __name__ == "__main__":
    main()
