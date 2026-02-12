"""
S³ Musical Intelligence — All-α1 Comprehensive Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Runs the complete MI pipeline and generates:
  1. Comprehensive JSON with all 26D Brain + 104D L³ outputs
  2. Publication-quality multi-panel visualization organized by ARU-α model

ARU-α1 Models (unified in MusicalBrain 26D):
  α.1 SRP — Striatal Reward Pathway   → Reward (9D)   [Salimpoor 2011]
  α.2 AAC — Autonomic-Affective Coupling → Autonomic (5D)  [de Fleurian 2021]
  α.3 VMM — Valence-Mode Mapping       → Affect (6D)   [Fritz 2009]
  + Shared State (4D) + Integration (2D)

Usage:
    python Lab/analyze_all_alpha1.py <audio_path> [--out <output_dir>] [--sigma <seconds>]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import torch

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.ndimage import gaussian_filter1d


# ─── S³ Brand Palette ────────────────────────────────────────────
BG = "#0a0a0f"
BG_PANEL = "#0d0d14"
GRID_COLOR = "#1a1a2e"
TEXT_COLOR = "#c8c8d4"
ACCENT = "#6366f1"
GOLD = "#f59e0b"

# α.1 SRP Colors
WANTING_RED = "#ef4444"
LIKING_BLUE = "#3b82f6"
PLEASURE_PURPLE = "#a855f7"
CAUDATE_ORANGE = "#f97316"
NACC_GREEN = "#22c55e"
OPIOID_AMBER = "#fbbf24"
TENSION_ROSE = "#f43f5e"
FORECAST_CYAN = "#06b6d4"
PMATCH_SLATE = "#94a3b8"

# α.2 AAC Colors
SCR_YELLOW = "#eab308"
HR_ROSE = "#fb7185"
RESPR_TEAL = "#14b8a6"
CHILLS_CYAN = "#06b6d4"
ANS_VIOLET = "#8b5cf6"

# α.3 VMM Colors
VALENCE_EMERALD = "#10b981"
MODE_AMBER = "#f59e0b"
CONS_VAL_BLUE = "#60a5fa"
HAPPY_LIME = "#84cc16"
SAD_INDIGO = "#818cf8"
CERTAINTY_GRAY = "#9ca3af"

# Shared / Integration
AROUSAL_RED = "#dc2626"
PE_TEAL = "#14b8a6"
HARMONIC_CORAL = "#fb923c"
MOMENTUM_PURPLE = "#c084fc"
BEAUTY_GOLD = "#f59e0b"
ARC_PINK = "#f472b6"

WAVEFORM_COLOR = "#4338ca"
CLIMAX_GLOW = "#f59e0b"


# ─── Musical Moments ─────────────────────────────────────────────
MOMENTS_DB = {
    "swan lake": [
        (0, 5, "Intro", "#334155"),
        (5, 30, "Opening\nTremolo", "#1e293b"),
        (30, 60, "Swan Theme\n(Oboe)", "#1e3a5f"),
        (60, 95, "Development", "#1e293b"),
        (95, 130, "Buildup", "#2d1b0e"),
        (130, 160, "Climax", "#3b1306"),
        (160, 183, "Resolution", "#1a1a2e"),
    ],
    "duel of the fates": [
        (0, 8, "Choir\nIntro", "#334155"),
        (8, 25, "Strings\nEntry", "#1e293b"),
        (25, 55, "Main Theme", "#1e3a5f"),
        (55, 75, "First\nBattle", "#2d1b0e"),
        (75, 95, "Bridge", "#1e293b"),
        (95, 130, "Second\nWave", "#2d1b0e"),
        (130, 155, "Climax", "#3b1306"),
        (155, 178, "Coda", "#1a1a2e"),
    ],
    "herald of the change": [
        (0, 15, "Intro\n(Strings)", "#334155"),
        (15, 45, "First Theme\n(Horns)", "#1e293b"),
        (45, 75, "Build &\nLayer", "#1e3a5f"),
        (75, 120, "Rising\nTension", "#2d1b0e"),
        (120, 180, "Expansion", "#1e293b"),
        (180, 240, "Climax\nPlateau", "#3b1306"),
        (240, 275, "Resolution", "#1a1a2e"),
        (275, 310, "Coda", "#334155"),
    ],
    "pathetique": [
        (0, 30, "Grave\n(Intro)", "#334155"),
        (30, 75, "Allegro\nExposition A", "#1e293b"),
        (75, 130, "Exposition B\n(2nd Theme)", "#1e3a5f"),
        (130, 170, "Exposition\nClosing", "#2d1b0e"),
        (170, 260, "Development", "#1e293b"),
        (260, 340, "Recapitulation", "#1e3a5f"),
        (340, 420, "Recap\nContinued", "#2d1b0e"),
        (420, 460, "Climax", "#3b1306"),
        (460, 498, "Coda", "#1a1a2e"),
    ],
    "cello suite": [
        (0, 15, "Opening\nArpeggio", "#334155"),
        (15, 35, "First\nPhrase", "#1e293b"),
        (35, 55, "Rising\nSequence", "#1e3a5f"),
        (55, 75, "Pedal\nPoint", "#2d1b0e"),
        (75, 100, "Development", "#1e293b"),
        (100, 120, "Climax", "#3b1306"),
        (120, 140, "Descent", "#1a1a2e"),
        (140, 160, "Coda", "#334155"),
    ],
}


def detect_moments(audio_path: str | None) -> list:
    if not audio_path:
        return []
    name = Path(audio_path).stem.lower()
    for key, moments in MOMENTS_DB.items():
        if key in name:
            return moments
    return []


def load_audio_envelope(audio_path: str, fps: float) -> np.ndarray | None:
    try:
        import soundfile as sf
        wav, sr = sf.read(audio_path, dtype="float32")
        if wav.ndim > 1:
            wav = wav.mean(axis=1)
        hop = int(sr / fps)
        n_frames = len(wav) // hop
        envelope = np.zeros(n_frames)
        for i in range(n_frames):
            start = i * hop
            end = min(start + hop, len(wav))
            envelope[i] = np.sqrt(np.mean(wav[start:end] ** 2))
        envelope = envelope / (envelope.max() + 1e-8)
        return envelope
    except Exception as e:
        print(f"  Could not load audio envelope: {e}")
        return None


# ═══════════════════════════════════════════════════════════════════
# JSON EXPORT
# ═══════════════════════════════════════════════════════════════════

def export_comprehensive_json(output, audio_path: str, json_path: str, config) -> dict:
    """Export full analysis results to JSON."""
    brain = output.brain
    tensor = brain.tensor.detach().cpu().squeeze(0)  # (T, 26)
    T, D = tensor.shape

    data = {
        "meta": {
            "model": "MusicalBrain v2.1",
            "version": "2.1.0",
            "audio": Path(audio_path).name,
            "audio_path": str(audio_path),
            "duration_s": round(T / config.frame_rate, 2),
            "frames": T,
            "frame_rate": config.frame_rate,
            "brain_dim": D,
            "aru_alpha_models": {
                "alpha_1_srp": {
                    "name": "Striatal Reward Pathway",
                    "pathway": "reward",
                    "dims": 9,
                    "range": [4, 13],
                    "citations": ["Salimpoor 2011", "Berridge 2003", "Blood & Zatorre 2001"],
                },
                "alpha_2_aac": {
                    "name": "Autonomic-Affective Coupling",
                    "pathway": "autonomic",
                    "dims": 5,
                    "range": [19, 24],
                    "citations": ["de Fleurian & Pearce 2021", "Fancourt 2020", "Peng 2022"],
                },
                "alpha_3_vmm": {
                    "name": "Valence-Mode Mapping",
                    "pathway": "affect",
                    "dims": 6,
                    "range": [13, 19],
                    "citations": ["Fritz 2009", "Koelsch 2006", "Mitterschiffthaler 2007"],
                },
            },
        },
        "brain": {
            "dimensions": list(brain.dimension_names),
            "pathways": {
                name: {
                    "range": list(rng),
                    "dimensions": list(brain.dimension_names[rng[0]:rng[1]]),
                }
                for name, rng in brain.pathway_ranges.items()
            },
            "shape": [T, D],
            "values": tensor.tolist(),
        },
        "statistics": {},
    }

    # Per-dimension statistics
    for i, dim_name in enumerate(brain.dimension_names):
        vals = tensor[:, i].numpy()
        data["statistics"][dim_name] = {
            "mean": round(float(vals.mean()), 6),
            "std": round(float(vals.std()), 6),
            "min": round(float(vals.min()), 6),
            "max": round(float(vals.max()), 6),
            "median": round(float(np.median(vals)), 6),
            "q25": round(float(np.percentile(vals, 25)), 6),
            "q75": round(float(np.percentile(vals, 75)), 6),
        }

    # Key musical events
    fps = config.frame_rate
    onset_skip = int(2 * fps)
    time = np.arange(T) / fps

    vals_np = tensor.numpy()
    dim_idx = {name: i for i, name in enumerate(brain.dimension_names)}

    wanting = vals_np[:, dim_idx["wanting"]]
    liking = vals_np[:, dim_idx["liking"]]
    pleasure = vals_np[:, dim_idx["pleasure"]]
    da_caudate = vals_np[:, dim_idx["da_caudate"]]
    da_nacc = vals_np[:, dim_idx["da_nacc"]]
    chills = vals_np[:, dim_idx["chills_intensity"]]

    wanting_peak_idx = np.argmax(wanting[onset_skip:]) + onset_skip
    pleasure_peak_idx = np.argmax(pleasure[onset_skip:]) + onset_skip
    chills_peak_idx = np.argmax(chills[onset_skip:]) + onset_skip

    # Salimpoor W→L lag: search for liking peak within ±30s of wanting peak
    # (not global argmax — liking is often flat for tonal music)
    salimpoor_window = int(30 * fps)
    l_search_start = max(onset_skip, wanting_peak_idx - salimpoor_window)
    l_search_end = min(T, wanting_peak_idx + salimpoor_window)
    liking_peak_idx = l_search_start + np.argmax(liking[l_search_start:l_search_end])

    data["events"] = {
        "wanting_peak_s": round(time[wanting_peak_idx], 2),
        "liking_peak_s": round(time[liking_peak_idx], 2),
        "pleasure_peak_s": round(time[pleasure_peak_idx], 2),
        "chills_peak_s": round(time[chills_peak_idx], 2),
        "wanting_liking_lag_s": round(time[liking_peak_idx] - time[wanting_peak_idx], 2),
        "da_caudate_at_t0": round(float(da_caudate[0]), 6),
        "da_nacc_range": [round(float(da_nacc.min()), 4), round(float(da_nacc.max()), 4)],
        "pleasure_range": [round(float(pleasure.min()), 4), round(float(pleasure.max()), 4)],
        "salimpoor_criterion": bool(2.0 <= (time[liking_peak_idx] - time[wanting_peak_idx]) <= 30.0),
    }

    # L³ Semantics
    if output.semantics is not None:
        sem = output.semantics
        sem_tensor = sem.tensor.detach().cpu().squeeze(0)  # (T, 104)
        data["semantics"] = {
            "model": sem.model_name,
            "total_dim": sem.total_dim,
            "shape": list(sem_tensor.shape),
            "groups": {},
        }
        for group_name, group in sem.groups.items():
            gt = group.tensor.detach().cpu().squeeze(0).numpy()
            data["semantics"]["groups"][group_name] = {
                "dimensions": list(group.dimension_names),
                "dim": group.tensor.shape[-1],
                "statistics": {
                    dim_name: {
                        "mean": round(float(gt[:, j].mean()), 6),
                        "std": round(float(gt[:, j].std()), 6),
                        "min": round(float(gt[:, j].min()), 6),
                        "max": round(float(gt[:, j].max()), 6),
                    }
                    for j, dim_name in enumerate(group.dimension_names)
                },
            }

    # Write JSON
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"  JSON saved: {json_path}")
    print(f"    Brain: {D}D × {T} frames ({T/fps:.1f}s)")
    if output.semantics:
        print(f"    L³: {sem.total_dim}D ({len(sem.groups)} groups)")

    return data


# ═══════════════════════════════════════════════════════════════════
# VISUALIZATION
# ═══════════════════════════════════════════════════════════════════

def create_visualization(
    data: dict,
    audio_path: str | None = None,
    output_path: str = "all_alpha1.png",
    smooth_sigma: float = 3.0,
):
    """Create comprehensive multi-panel visualization for all α1 models."""

    brain = data["brain"]
    dim_names = brain["dimensions"]
    raw = np.array(brain["values"])
    T, D = raw.shape
    fps = data["meta"]["frame_rate"]
    time = np.arange(T) / fps
    duration = T / fps

    values = {name: raw[:, i] for i, name in enumerate(dim_names)}

    # Smooth
    sigma = smooth_sigma * fps
    s = {name: gaussian_filter1d(v, sigma) for name, v in values.items()}

    # Moments
    piece_moments = detect_moments(audio_path)
    climax_region = None
    for start, end, label, _ in piece_moments:
        if "climax" in label.lower():
            climax_region = (start, end)
            break

    # Audio envelope
    envelope = None
    if audio_path and Path(audio_path).exists():
        envelope = load_audio_envelope(audio_path, fps)
        if envelope is not None:
            if len(envelope) > T:
                envelope = envelope[:T]
            elif len(envelope) < T:
                envelope = np.pad(envelope, (0, T - len(envelope)))
            envelope = gaussian_filter1d(envelope, sigma * 0.3)

    # ─── Figure Setup ────────────────────────────────────────────
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

    n_panels = 7
    height_ratios = [1.0, 2.8, 2.0, 2.2, 2.4, 1.8, 1.8]

    fig = plt.figure(figsize=(24, 3.2 * n_panels + 3))
    gs = gridspec.GridSpec(
        n_panels, 1,
        height_ratios=height_ratios,
        hspace=0.08,
        left=0.06, right=0.94,
        top=0.94, bottom=0.04,
    )
    axes = [fig.add_subplot(gs[i]) for i in range(n_panels)]

    # ─── Title ───────────────────────────────────────────────────
    audio_name = data["meta"]["audio"]
    if len(audio_name) > 80:
        audio_name = audio_name[:77] + "..."

    fig.text(0.06, 0.978, "S³",
             fontsize=32, fontweight="bold", color=ACCENT, va="top")
    fig.text(0.105, 0.978,
             " Musical Intelligence — All-α1 Comprehensive Analysis",
             fontsize=18, fontweight="light", color=TEXT_COLOR, va="top")
    fig.text(0.06, 0.958, audio_name,
             fontsize=11, color="#6b7280", va="top", style="italic")

    # Stats line
    events = data.get("events", {})
    w_peak = events.get("wanting_peak_s", 0)
    l_peak = events.get("liking_peak_s", 0)
    lag = events.get("wanting_liking_lag_s", 0)
    salimpoor = events.get("salimpoor_criterion", False)

    fig.text(0.94, 0.978,
             f"26D × {T} frames  |  {duration:.1f}s  |  {fps:.1f} Hz  |  L³ 104D",
             fontsize=9, color="#6b7280", va="top", ha="right")

    lag_color = NACC_GREEN if salimpoor else WANTING_RED
    fig.text(0.94, 0.960,
             f"W→L lag: {lag:.1f}s  |  Salimpoor: {'PASS' if salimpoor else 'FAIL'}",
             fontsize=11, fontweight="bold", color=lag_color, va="top", ha="right")

    # ─── Helpers ─────────────────────────────────────────────────
    def add_moments(ax):
        for start, end, label, color in piece_moments:
            if start < duration:
                ax.axvspan(start, min(end, duration),
                           alpha=0.25, color=color, zorder=0)

    def add_climax(ax):
        if climax_region:
            ax.axvspan(climax_region[0], climax_region[1],
                       alpha=0.08, color=CLIMAX_GLOW, zorder=0)

    def style_axis(ax, ylabel, show_xlabel=False, ylim=None):
        ax.set_facecolor(BG_PANEL)
        ax.set_xlim(0, duration)
        ax.set_ylabel(ylabel, fontsize=10, fontweight="bold", color=ACCENT)
        ax.grid(True, alpha=0.15, color=GRID_COLOR, linewidth=0.5)
        ax.tick_params(axis="both", labelsize=8)
        if ylim:
            ax.set_ylim(*ylim)
        if not show_xlabel:
            ax.set_xticklabels([])
        else:
            ax.set_xlabel("Time (seconds)", fontsize=10)
        for spine in ax.spines.values():
            spine.set_color(GRID_COLOR)
            spine.set_linewidth(0.5)

    def add_legend(ax, **kwargs):
        kw = dict(loc="upper left", fontsize=7.5, framealpha=0.3,
                  edgecolor=GRID_COLOR, facecolor=BG_PANEL)
        kw.update(kwargs)
        leg = ax.legend(**kw)
        for text in leg.get_texts():
            text.set_color(TEXT_COLOR)

    onset_skip = int(2 * fps)

    # ═════════════════════════════════════════════════════════════
    # PANEL 0: Audio Waveform
    # ═════════════════════════════════════════════════════════════
    ax = axes[0]
    add_moments(ax)
    if envelope is not None:
        ax.fill_between(time, 0, envelope, color=WAVEFORM_COLOR, alpha=0.6, linewidth=0)
        ax.plot(time, envelope, color=WAVEFORM_COLOR, linewidth=0.5, alpha=0.8)
    for start, end, label, _ in piece_moments:
        mid = (start + min(end, duration)) / 2
        if mid < duration:
            ax.text(mid, 0.92, label, transform=ax.get_xaxis_transform(),
                    ha="center", va="top", fontsize=7.5, color="#94a3b8",
                    fontweight="bold", linespacing=1.1)
    style_axis(ax, "Audio")
    ax.set_ylim(0, 1.05)

    # ═════════════════════════════════════════════════════════════
    # PANEL 1: α.1 SRP — Reward Pathway (THE STAR)
    # ═════════════════════════════════════════════════════════════
    ax = axes[1]
    add_moments(ax)
    add_climax(ax)

    # Peak finding: use RAW data for accuracy (smoothing distorts sharp peaks)
    raw_wanting = raw[:, dim_names.index("wanting")]
    raw_liking = raw[:, dim_names.index("liking")]

    wanting_peak_idx = np.argmax(raw_wanting[onset_skip:]) + onset_skip

    # Salimpoor: search for liking peak within ±30s of wanting peak
    salimpoor_window = int(30 * fps)
    l_start = max(onset_skip, wanting_peak_idx - salimpoor_window)
    l_end = min(T, wanting_peak_idx + salimpoor_window)
    liking_peak_idx = l_start + np.argmax(raw_liking[l_start:l_end])

    wl_lag = time[liking_peak_idx] - time[wanting_peak_idx]

    # Main signals
    ax.plot(time, s["wanting"], color=WANTING_RED, linewidth=2.5,
            label="wanting (%.0fs)" % time[wanting_peak_idx], zorder=5)
    ax.plot(time, s["liking"], color=LIKING_BLUE, linewidth=2.5,
            label="liking (%.0fs)" % time[liking_peak_idx], zorder=5)
    ax.plot(time, s["pleasure"], color=PLEASURE_PURPLE, linewidth=2.2,
            alpha=0.8, label="pleasure", zorder=4)

    # Underlying DA signals (thinner, dashed)
    ax.plot(time, s["da_caudate"], color=CAUDATE_ORANGE, linewidth=1.5,
            linestyle="--", alpha=0.7, label="da_caudate")
    ax.plot(time, s["da_nacc"], color=NACC_GREEN, linewidth=1.5,
            linestyle="--", alpha=0.7, label="da_nacc")
    ax.plot(time, s["opioid_proxy"], color=OPIOID_AMBER, linewidth=1.2,
            linestyle=":", alpha=0.5, label="opioid")

    # Peak markers (at raw peak positions, y from smoothed curves)
    ax.scatter([time[wanting_peak_idx]], [s["wanting"][wanting_peak_idx]],
               color=WANTING_RED, s=70, zorder=10, edgecolors="white", linewidths=1.5)
    ax.scatter([time[liking_peak_idx]], [s["liking"][liking_peak_idx]],
               color=LIKING_BLUE, s=70, zorder=10, edgecolors="white", linewidths=1.5)

    # Lag arrow
    arrow_y = max(s["wanting"][wanting_peak_idx], s["liking"][liking_peak_idx]) + 0.015
    ax.annotate("", xy=(time[liking_peak_idx], arrow_y),
                xytext=(time[wanting_peak_idx], arrow_y),
                arrowprops=dict(arrowstyle="->", color=GOLD, lw=2))
    mid_arrow = (time[wanting_peak_idx] + time[liking_peak_idx]) / 2
    ax.text(mid_arrow, arrow_y + 0.008, "%.1fs" % wl_lag,
            ha="center", va="bottom", fontsize=10, fontweight="bold", color=GOLD, zorder=11)

    style_axis(ax, "α.1 SRP  Reward", ylim=(-0.05, 1.05))
    add_legend(ax, ncol=3)

    # ═════════════════════════════════════════════════════════════
    # PANEL 2: α.1 SRP — Reward Detail
    # ═════════════════════════════════════════════════════════════
    ax = axes[2]
    add_moments(ax)
    add_climax(ax)

    ax.plot(time, s["tension"], color=TENSION_ROSE, linewidth=2.2, label="tension")
    ax.plot(time, s["reward_forecast"], color=FORECAST_CYAN, linewidth=2.2,
            label="reward_forecast")
    ax.plot(time, s["prediction_match"], color=PMATCH_SLATE, linewidth=1.8,
            alpha=0.7, label="prediction_match")

    style_axis(ax, "α.1 SRP  Detail", ylim=(-1.1, 1.1))
    add_legend(ax)

    # ═════════════════════════════════════════════════════════════
    # PANEL 3: α.2 AAC — Autonomic Pathway
    # ═════════════════════════════════════════════════════════════
    ax = axes[3]
    add_moments(ax)
    add_climax(ax)

    ax.plot(time, s["scr"], color=SCR_YELLOW, linewidth=2.2, label="SCR (skin conductance)")
    ax.plot(time, 1.0 - s["hr"], color=HR_ROSE, linewidth=2.2, label="1−HR (vagal withdrawal)")
    ax.plot(time, s["respr"], color=RESPR_TEAL, linewidth=2.0, label="RespR")
    ax.plot(time, s["chills_intensity"], color=CHILLS_CYAN, linewidth=2.5,
            alpha=0.9, label="chills_intensity")
    ax.plot(time, s["ans_composite"], color=ANS_VIOLET, linewidth=1.5,
            linestyle="--", alpha=0.7, label="ANS composite")

    # Mark chills peak
    chills_peak_idx = np.argmax(s["chills_intensity"][onset_skip:]) + onset_skip
    ax.scatter([time[chills_peak_idx]], [s["chills_intensity"][chills_peak_idx]],
               color=CHILLS_CYAN, s=60, zorder=10, edgecolors="white", linewidths=1.5)
    ax.text(time[chills_peak_idx], s["chills_intensity"][chills_peak_idx] + 0.015,
            "%.0fs" % time[chills_peak_idx],
            ha="center", fontsize=8, fontweight="bold", color=CHILLS_CYAN)

    style_axis(ax, "α.2 AAC  Autonomic", ylim=(-0.05, 1.05))
    add_legend(ax, ncol=3)

    # ═════════════════════════════════════════════════════════════
    # PANEL 4: α.3 VMM — Affect Pathway
    # ═════════════════════════════════════════════════════════════
    ax = axes[4]
    add_moments(ax)
    add_climax(ax)

    ax.plot(time, s["f03_valence"], color=VALENCE_EMERALD, linewidth=2.5,
            label="valence (bipolar)")
    ax.axhline(0, color="#4b5563", linewidth=0.5, linestyle="--", alpha=0.3)

    ax.plot(time, s["mode_signal"], color=MODE_AMBER, linewidth=2.0,
            label="mode_signal (major/minor)")
    ax.plot(time, s["consonance_valence"], color=CONS_VAL_BLUE, linewidth=2.0,
            label="consonance_valence")
    ax.plot(time, s["happy_pathway"], color=HAPPY_LIME, linewidth=1.8,
            alpha=0.7, label="happy_pathway")
    ax.plot(time, s["sad_pathway"], color=SAD_INDIGO, linewidth=1.8,
            alpha=0.7, label="sad_pathway")
    ax.plot(time, s["emotion_certainty"], color=CERTAINTY_GRAY, linewidth=1.2,
            linestyle=":", alpha=0.6, label="certainty")

    style_axis(ax, "α.3 VMM  Affect", ylim=(-0.3, 1.05))
    add_legend(ax, ncol=3)

    # ═════════════════════════════════════════════════════════════
    # PANEL 5: Shared State
    # ═════════════════════════════════════════════════════════════
    ax = axes[5]
    add_moments(ax)
    add_climax(ax)

    ax.plot(time, s["arousal"], color=AROUSAL_RED, linewidth=2.5, label="arousal")
    ax.plot(time, s["prediction_error"], color=PE_TEAL, linewidth=2.0,
            label="prediction_error")
    ax.plot(time, s["harmonic_context"], color=HARMONIC_CORAL, linewidth=2.0,
            label="harmonic_context")
    ax.plot(time, s["emotional_momentum"], color=MOMENTUM_PURPLE, linewidth=2.0,
            label="emotional_momentum")
    ax.axhline(0, color="#4b5563", linewidth=0.5, linestyle="--", alpha=0.3)

    style_axis(ax, "Shared State", ylim=(-1.05, 1.05))
    add_legend(ax, ncol=2)

    # ═════════════════════════════════════════════════════════════
    # PANEL 6: Integration
    # ═════════════════════════════════════════════════════════════
    ax = axes[6]
    add_moments(ax)
    add_climax(ax)

    ax.plot(time, s["beauty"], color=BEAUTY_GOLD, linewidth=2.5, label="beauty")
    ax.plot(time, s["emotional_arc"], color=ARC_PINK, linewidth=2.5, label="emotional_arc")

    # Mark beauty peak
    beauty_peak_idx = np.argmax(s["beauty"][onset_skip:]) + onset_skip
    ax.scatter([time[beauty_peak_idx]], [s["beauty"][beauty_peak_idx]],
               color=BEAUTY_GOLD, s=60, zorder=10, edgecolors="white", linewidths=1.5)
    ax.text(time[beauty_peak_idx], s["beauty"][beauty_peak_idx] + 0.01,
            "%.0fs" % time[beauty_peak_idx],
            ha="center", fontsize=8, fontweight="bold", color=BEAUTY_GOLD)

    style_axis(ax, "Integration", show_xlabel=True, ylim=(-0.05, 1.05))
    add_legend(ax)

    # ─── Footer ──────────────────────────────────────────────────
    fig.text(
        0.5, 0.008,
        "S³ — Spectral Sound Space  |  Musical Intelligence  |  "
        "MusicalBrain v2.1 (26D)  |  All-α1: SRP + AAC + VMM  |  "
        "Salimpoor 2011, de Fleurian 2021, Fritz 2009",
        fontsize=8, color="#4b5563", ha="center", va="bottom",
    )

    # ─── Save ────────────────────────────────────────────────────
    fig.savefig(output_path, dpi=200,
                facecolor=BG, edgecolor="none",
                bbox_inches="tight", pad_inches=0.3)
    plt.close(fig)
    print(f"  PNG saved: {output_path}")
    return output_path


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="S³ Musical Intelligence — All-α1 Comprehensive Analysis"
    )
    parser.add_argument("audio", help="Path to audio file")
    parser.add_argument("--out", default=None, help="Output directory")
    parser.add_argument("--sigma", type=float, default=1.0,
                        help="Gaussian smooth sigma in seconds (default: 1.0)")
    args = parser.parse_args()

    mi_dir = Path(__file__).resolve().parent.parent
    audio_path = args.audio
    if not Path(audio_path).is_absolute():
        audio_path = str(mi_dir / audio_path)

    if not Path(audio_path).exists():
        print(f"Error: {audio_path} not found", file=sys.stderr)
        sys.exit(1)

    # Output directory
    if args.out:
        out_dir = Path(args.out)
    else:
        out_dir = mi_dir / "Lab" / "Experiments" / "Aru_Models" / "All-α1"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Stem for filenames
    stem = Path(audio_path).stem
    # Clean long stems
    if len(stem) > 60:
        stem = stem[:57] + "..."

    print(f"\n{'━' * 60}")
    print(f"  S³ Musical Intelligence — All-α1 Analysis")
    print(f"  Audio: {Path(audio_path).name}")
    print(f"{'━' * 60}\n")

    # ─── Run MI Pipeline ─────────────────────────────────────────
    # Ensure mi package is importable
    if str(mi_dir) not in sys.path:
        sys.path.insert(0, str(mi_dir))
    from mi.core.config import MI_CONFIG
    from mi.pipeline import MIPipeline
    from mi.io.audio import load_audio

    config = MI_CONFIG
    pipeline = MIPipeline(config)

    print(f"  Loading audio...")
    waveform = load_audio(Path(audio_path), config)
    samples = waveform.shape[-1]
    print(f"    Samples: {samples:,} ({samples/config.sample_rate:.1f}s)")

    print(f"  Processing pipeline...")
    output = pipeline.process(waveform, return_semantics=True)

    brain = output.brain
    B, T, D = brain.tensor.shape
    print(f"    Brain: {D}D × {T} frames ({T/config.frame_rate:.1f}s)")
    if output.semantics:
        print(f"    L³: {output.semantics.total_dim}D ({len(output.semantics.groups)} groups)")

    # ─── Export JSON ─────────────────────────────────────────────
    json_path = str(out_dir / f"{stem}_all_alpha1.json")
    print(f"\n  Exporting JSON...")
    data = export_comprehensive_json(output, audio_path, json_path, config)

    # ─── Print Summary ───────────────────────────────────────────
    events = data["events"]
    stats = data["statistics"]

    print(f"\n  ┌─ Key Results ──────────────────────────────────────")
    print(f"  │ Wanting peak:   {events['wanting_peak_s']:.1f}s")
    print(f"  │ Liking peak:    {events['liking_peak_s']:.1f}s")
    print(f"  │ W→L lag:        {events['wanting_liking_lag_s']:.1f}s  "
          f"({'PASS' if events['salimpoor_criterion'] else 'FAIL'} Salimpoor)")
    print(f"  │ Pleasure peak:  {events['pleasure_peak_s']:.1f}s  "
          f"[{events['pleasure_range'][0]:.3f}, {events['pleasure_range'][1]:.3f}]")
    print(f"  │ Chills peak:    {events['chills_peak_s']:.1f}s")
    print(f"  │ da_caudate(t=0): {events['da_caudate_at_t0']:.6f}")
    print(f"  │ da_nacc range:  [{events['da_nacc_range'][0]:.3f}, {events['da_nacc_range'][1]:.3f}]")
    print(f"  └──────────────────────────────────────────────────")

    print(f"\n  ┌─ Per-Dimension Statistics ─────────────────────────")
    for name in brain.dimension_names:
        st = stats[name]
        print(f"  │ {name:25s}  μ={st['mean']:+.3f}  σ={st['std']:.3f}  "
              f"[{st['min']:+.3f}, {st['max']:+.3f}]")
    print(f"  └──────────────────────────────────────────────────")

    # ─── Visualization ───────────────────────────────────────────
    png_path = str(out_dir / f"{stem}_all_alpha1.png")
    print(f"\n  Generating visualization...")
    create_visualization(
        data, audio_path=audio_path,
        output_path=png_path, smooth_sigma=args.sigma,
    )

    print(f"\n{'━' * 60}")
    print(f"  Analysis complete!")
    print(f"  JSON: {json_path}")
    print(f"  PNG:  {png_path}")
    print(f"{'━' * 60}\n")


if __name__ == "__main__":
    main()
