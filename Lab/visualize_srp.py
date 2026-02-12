"""
S³ Musical Intelligence — SRP Visualization
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Generates a publication-quality multi-panel visualization of the
Striatal Reward Pathway (19D) output synchronized with audio.

Usage:
    python Lab/visualize_srp.py <audio_path> [--json <srp_json>] [--out <output_png>]

If --json is not given, runs the full MI pipeline on the audio first.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyArrowPatch
from scipy.ndimage import gaussian_filter1d

# ─── S³ Brand Palette ────────────────────────────────────────────
BG = "#0a0a0f"
BG_PANEL = "#0d0d14"
GRID_COLOR = "#1a1a2e"
TEXT_COLOR = "#c8c8d4"
ACCENT = "#6366f1"       # Indigo
GOLD = "#f59e0b"
WANTING_RED = "#ef4444"
LIKING_BLUE = "#3b82f6"
PLEASURE_PURPLE = "#a855f7"
CAUDATE_ORANGE = "#f97316"
NACC_GREEN = "#22c55e"
OPIOID_AMBER = "#fbbf24"
TENSION_ROSE = "#f43f5e"
HARMONIC_CORAL = "#fb923c"
DYNAMIC_RED = "#dc2626"
PEAK_SLATE = "#94a3b8"
FORECAST_RED = "#ef4444"
CHILLS_CYAN = "#06b6d4"
RESOLVE_EMERALD = "#10b981"
VTA_GRAY = "#9ca3af"
COUPLING_VIOLET = "#8b5cf6"
PE_TEAL = "#14b8a6"
REACTION_PLUM = "#c084fc"
CLIMAX_GLOW = "#f59e0b"
WAVEFORM_COLOR = "#4338ca"

# ─── Musical Moments per piece ──────────────────────────────────
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

# Default: empty (auto-detected from filename or no annotations)
MOMENTS = []


def detect_moments(audio_path: str | None) -> list:
    """Match audio filename to known moment maps."""
    if not audio_path:
        return []
    name = Path(audio_path).stem.lower()
    for key, moments in MOMENTS_DB.items():
        if key in name:
            return moments
    return []


def load_audio_envelope(audio_path: str, fps: float) -> np.ndarray:
    """Load audio and compute RMS envelope at frame rate."""
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
        # Normalize to [0, 1]
        envelope = envelope / (envelope.max() + 1e-8)
        return envelope
    except Exception as e:
        print(f"  Could not load audio envelope: {e}")
        return None


def run_pipeline(audio_path: str, json_path: str) -> dict:
    """Run MI pipeline and export JSON."""
    import subprocess
    mi_dir = Path(__file__).resolve().parent.parent
    cmd = [
        sys.executable, "-m", "mi", audio_path,
        "--json", json_path,
    ]
    print(f"  Running MI pipeline...")
    result = subprocess.run(cmd, cwd=str(mi_dir), capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError("MI pipeline failed")
    print(result.stdout)
    with open(json_path) as f:
        return json.load(f)


def create_visualization(
    data: dict,
    audio_path: str | None = None,
    output_path: str = "srp_visualization.png",
    smooth_sigma: float = 3.0,
    moments: list | None = None,
):
    """Create the multi-panel SRP visualization."""

    srp = data["SRP"]
    dim_names = srp["dimensions"]
    raw = np.array(srp["values"])
    T = raw.shape[0]
    fps = 172.265625
    time = np.arange(T) / fps
    duration = T / fps

    values = {name: raw[:, i] for i, name in enumerate(dim_names)}

    # Smooth
    sigma = smooth_sigma * fps
    s = {name: gaussian_filter1d(v, sigma) for name, v in values.items()}

    # Detect musical moments
    piece_moments = moments if moments is not None else detect_moments(audio_path)

    # Find climax region from moments (if any)
    climax_region = None
    for start, end, label, _ in piece_moments:
        if "climax" in label.lower():
            climax_region = (start, end)
            break

    # Load audio envelope if available
    envelope = None
    if audio_path and Path(audio_path).exists():
        envelope = load_audio_envelope(audio_path, fps)
        if envelope is not None:
            # Match length
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

    n_panels = 6 if envelope is not None else 5
    height_ratios = [1.2, 2.5, 2, 2.5, 2, 2] if envelope is not None else [2.5, 2, 2.5, 2, 2]

    fig = plt.figure(figsize=(22, 3.2 * n_panels + 2))
    gs = gridspec.GridSpec(
        n_panels, 1,
        height_ratios=height_ratios,
        hspace=0.08,
        left=0.06, right=0.94,
        top=0.94, bottom=0.04,
    )

    axes = [fig.add_subplot(gs[i]) for i in range(n_panels)]

    # ─── Title ───────────────────────────────────────────────────
    title = data.get("audio", {}).get("filename", "")
    if not title:
        title = Path(audio_path).stem if audio_path else "SRP Output"
    # Clean up long filenames
    if len(title) > 80:
        title = title[:77] + "..."

    fig.text(
        0.06, 0.975,
        "S³",
        fontsize=28, fontweight="bold", color=ACCENT,
        va="top", ha="left",
    )
    fig.text(
        0.105, 0.975,
        " Musical Intelligence — Striatal Reward Pathway",
        fontsize=16, fontweight="light", color=TEXT_COLOR,
        va="top", ha="left",
    )
    fig.text(
        0.06, 0.955,
        title,
        fontsize=10, color="#6b7280",
        va="top", ha="left", style="italic",
    )

    # Stats line
    onset_skip = int(2 * fps)
    wanting_peak_idx = np.argmax(s["wanting"][onset_skip:]) + onset_skip
    liking_peak_idx = np.argmax(s["liking"][onset_skip:]) + onset_skip
    lag = time[liking_peak_idx] - time[wanting_peak_idx]

    fig.text(
        0.94, 0.975,
        f"19D × {T} frames  |  {duration:.1f}s  |  {fps:.1f} Hz",
        fontsize=9, color="#6b7280",
        va="top", ha="right",
    )
    lag_color = NACC_GREEN if 2 <= lag <= 30 else WANTING_RED
    fig.text(
        0.94, 0.957,
        f"wanting >> liking lag: {lag:.1f}s",
        fontsize=10, fontweight="bold", color=lag_color,
        va="top", ha="right",
    )

    # ─── Helper: annotate musical moments ────────────────────────
    def add_moments(ax):
        for start, end, label, color in piece_moments:
            if start < duration:
                ax.axvspan(
                    start, min(end, duration),
                    alpha=0.25, color=color, zorder=0,
                )

    def add_climax_highlight(ax):
        if climax_region:
            ax.axvspan(climax_region[0], climax_region[1],
                        alpha=0.08, color=CLIMAX_GLOW, zorder=0)

    def style_axis(ax, ylabel, show_xlabel=False):
        ax.set_facecolor(BG_PANEL)
        ax.set_xlim(0, duration)
        ax.set_ylabel(ylabel, fontsize=10, fontweight="bold", color=ACCENT)
        ax.grid(True, alpha=0.15, color=GRID_COLOR, linewidth=0.5)
        ax.tick_params(axis="both", labelsize=8)
        if not show_xlabel:
            ax.set_xticklabels([])
        else:
            ax.set_xlabel("Time (seconds)", fontsize=10)
        for spine in ax.spines.values():
            spine.set_color(GRID_COLOR)
            spine.set_linewidth(0.5)

    panel_idx = 0

    # ─── Panel 0: Audio Waveform ─────────────────────────────────
    if envelope is not None:
        ax = axes[panel_idx]
        add_moments(ax)
        ax.fill_between(time, 0, envelope, color=WAVEFORM_COLOR, alpha=0.6, linewidth=0)
        ax.plot(time, envelope, color=WAVEFORM_COLOR, linewidth=0.5, alpha=0.8)
        # Moment labels
        for start, end, label, _ in piece_moments:
            mid = (start + min(end, duration)) / 2
            if mid < duration:
                ax.text(
                    mid, 0.92, label,
                    transform=ax.get_xaxis_transform(),
                    ha="center", va="top", fontsize=7.5,
                    color="#94a3b8", fontweight="bold",
                    linespacing=1.1,
                )
        style_axis(ax, "Audio")
        ax.set_ylim(0, 1.05)
        panel_idx += 1

    # ─── Panel: P — Wanting vs Liking (THE STAR) ─────────────────
    ax = axes[panel_idx]
    add_moments(ax)
    add_climax_highlight(ax)

    ax.plot(time, s["wanting"], color=WANTING_RED, linewidth=2.5,
            label=f"wanting  (peak {time[wanting_peak_idx]:.0f}s)", zorder=5)
    ax.plot(time, s["liking"], color=LIKING_BLUE, linewidth=2.5,
            label=f"liking  (peak {time[liking_peak_idx]:.0f}s)", zorder=5)
    ax.plot(time, s["pleasure"], color=PLEASURE_PURPLE, linewidth=2,
            alpha=0.7, label="pleasure", zorder=4)

    # Mark peaks with dots
    ax.scatter([time[wanting_peak_idx]], [s["wanting"][wanting_peak_idx]],
               color=WANTING_RED, s=60, zorder=10, edgecolors="white", linewidths=1.5)
    ax.scatter([time[liking_peak_idx]], [s["liking"][liking_peak_idx]],
               color=LIKING_BLUE, s=60, zorder=10, edgecolors="white", linewidths=1.5)

    # Draw lag arrow
    arrow_y = max(s["wanting"][wanting_peak_idx], s["liking"][liking_peak_idx]) + 0.012
    ax.annotate(
        "", xy=(time[liking_peak_idx], arrow_y),
        xytext=(time[wanting_peak_idx], arrow_y),
        arrowprops=dict(
            arrowstyle="->", color=GOLD,
            lw=2, connectionstyle="arc3,rad=0",
        ),
        zorder=11,
    )
    mid_arrow = (time[wanting_peak_idx] + time[liking_peak_idx]) / 2
    ax.text(mid_arrow, arrow_y + 0.008, f"{lag:.1f}s",
            ha="center", va="bottom", fontsize=9,
            fontweight="bold", color=GOLD, zorder=11)

    # Moment labels on first SRP panel if no waveform
    if envelope is None:
        for start, end, label, _ in piece_moments:
            mid = (start + min(end, duration)) / 2
            if mid < duration:
                ax.text(mid, 0.98, label,
                        transform=ax.get_xaxis_transform(),
                        ha="center", va="top", fontsize=7,
                        color="#6b7280", fontweight="bold")

    style_axis(ax, "P  Psychological")
    leg = ax.legend(loc="upper left", fontsize=8, framealpha=0.3,
                    edgecolor=GRID_COLOR, facecolor=BG_PANEL)
    for text in leg.get_texts():
        text.set_color(TEXT_COLOR)
    panel_idx += 1

    # ─── Panel: N — Neurochemical ────────────────────────────────
    ax = axes[panel_idx]
    add_moments(ax)
    add_climax_highlight(ax)

    ax.plot(time, s["da_caudate"], color=CAUDATE_ORANGE, linewidth=2.2,
            label="da_caudate (anticipatory)")
    ax.plot(time, s["da_nacc"], color=NACC_GREEN, linewidth=2.2,
            label="da_nacc (consummatory)")
    ax.plot(time, s["opioid_proxy"], color=OPIOID_AMBER, linewidth=1.5,
            alpha=0.7, label="opioid_proxy")

    # Mark peaks
    caud_peak = np.argmax(s["da_caudate"][onset_skip:]) + onset_skip
    nacc_peak = np.argmax(s["da_nacc"][onset_skip:]) + onset_skip
    ax.scatter([time[caud_peak]], [s["da_caudate"][caud_peak]],
               color=CAUDATE_ORANGE, s=50, zorder=10, edgecolors="white", linewidths=1)
    ax.scatter([time[nacc_peak]], [s["da_nacc"][nacc_peak]],
               color=NACC_GREEN, s=50, zorder=10, edgecolors="white", linewidths=1)

    style_axis(ax, "N  Neurochemical")
    leg = ax.legend(loc="upper left", fontsize=8, framealpha=0.3,
                    edgecolor=GRID_COLOR, facecolor=BG_PANEL)
    for text in leg.get_texts():
        text.set_color(TEXT_COLOR)
    panel_idx += 1

    # ─── Panel: T+M — Musical Tracking ───────────────────────────
    ax = axes[panel_idx]
    add_moments(ax)
    add_climax_highlight(ax)

    ax.plot(time, s["dynamic_intensity"], color=DYNAMIC_RED, linewidth=2.5,
            label="dynamic_intensity")
    ax.plot(time, s["harmonic_tension"], color=HARMONIC_CORAL, linewidth=2.5,
            label="harmonic_tension")
    ax.plot(time, s["tension"], color=TENSION_ROSE, linewidth=1.8,
            alpha=0.7, label="tension")
    ax.plot(time, s["peak_detection"], color=PEAK_SLATE, linewidth=1.8,
            alpha=0.7, label="peak_detection")
    ax.plot(time, s["reaction"], color=REACTION_PLUM, linewidth=1.5,
            alpha=0.5, label="reaction")

    style_axis(ax, "T+M  Musical")
    leg = ax.legend(loc="upper left", fontsize=8, framealpha=0.3,
                    edgecolor=GRID_COLOR, facecolor=BG_PANEL, ncol=2)
    for text in leg.get_texts():
        text.set_color(TEXT_COLOR)
    panel_idx += 1

    # ─── Panel: F — Forecast ─────────────────────────────────────
    ax = axes[panel_idx]
    add_moments(ax)
    add_climax_highlight(ax)

    ax.plot(time, s["reward_forecast"], color=FORECAST_RED, linewidth=2.2,
            label="reward_forecast")
    ax.plot(time, s["chills_proximity"], color=CHILLS_CYAN, linewidth=2.2,
            label="chills_proximity")
    ax.plot(time, s["resolution_expect"], color=RESOLVE_EMERALD, linewidth=2.2,
            label="resolution_expect")

    style_axis(ax, "F  Forecast")
    leg = ax.legend(loc="upper left", fontsize=8, framealpha=0.3,
                    edgecolor=GRID_COLOR, facecolor=BG_PANEL)
    for text in leg.get_texts():
        text.set_color(TEXT_COLOR)
    panel_idx += 1

    # ─── Panel: C — Circuit ──────────────────────────────────────
    ax = axes[panel_idx]
    add_moments(ax)
    add_climax_highlight(ax)

    ax.plot(time, s["vta_drive"], color=VTA_GRAY, linewidth=2,
            label="vta_drive")
    ax.plot(time, s["stg_nacc_coupling"], color=COUPLING_VIOLET, linewidth=2,
            label="stg_nacc_coupling")
    ax.plot(time, s["prediction_error"], color=PE_TEAL, linewidth=1.5,
            alpha=0.7, label="prediction_error")
    ax.plot(time, s["prediction_match"], color="#64748b", linewidth=1.5,
            alpha=0.5, label="prediction_match")

    style_axis(ax, "C  Circuit", show_xlabel=True)
    leg = ax.legend(loc="upper left", fontsize=8, framealpha=0.3,
                    edgecolor=GRID_COLOR, facecolor=BG_PANEL, ncol=2)
    for text in leg.get_texts():
        text.set_color(TEXT_COLOR)

    # ─── Footer ──────────────────────────────────────────────────
    fig.text(
        0.5, 0.008,
        "S³ — Spectral Sound Space  |  Musical Intelligence  |  "
        "Striatal Reward Pathway (19D)  |  "
        "Salimpoor 2011, Howe 2013, Berridge 2003",
        fontsize=7.5, color="#4b5563",
        ha="center", va="bottom",
    )

    # ─── Save ────────────────────────────────────────────────────
    fig.savefig(
        output_path, dpi=200,
        facecolor=BG, edgecolor="none",
        bbox_inches="tight", pad_inches=0.3,
    )
    plt.close(fig)
    print(f"\n  Saved: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="S³ Musical Intelligence — SRP Visualization"
    )
    parser.add_argument("audio", help="Path to audio file")
    parser.add_argument("--json", default=None, help="Pre-computed SRP JSON")
    parser.add_argument("--out", default=None, help="Output PNG path")
    parser.add_argument("--sigma", type=float, default=3.0,
                        help="Gaussian smooth sigma in seconds (default: 3.0)")
    args = parser.parse_args()

    audio_path = args.audio
    mi_dir = Path(__file__).resolve().parent.parent

    # Resolve audio path relative to MI directory
    if not Path(audio_path).is_absolute():
        audio_path = str(mi_dir / audio_path)

    # JSON path
    if args.json:
        json_path = args.json
        with open(json_path) as f:
            data = json.load(f)
    else:
        json_path = "/tmp/srp_viz_output.json"
        data = run_pipeline(audio_path, json_path)

    # Output path
    if args.out:
        output_path = args.out
    else:
        stem = Path(audio_path).stem
        output_path = str(mi_dir / "Lab" / f"{stem}_srp.png")

    create_visualization(
        data,
        audio_path=audio_path,
        output_path=output_path,
        smooth_sigma=args.sigma,
    )


if __name__ == "__main__":
    main()
