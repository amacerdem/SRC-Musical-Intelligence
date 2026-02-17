#!/usr/bin/env python3
"""Beethoven Pathétique BCH — Full Data Visualization.

Recreates BCH pipeline on MPS and visualizes ALL 50 time series
produced by a single nucleus.

Usage:
    python Tests/experiments/beethoven_bch_visualize.py
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
from torch import Tensor
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from Musical_Intelligence.ear.r3 import R3Extractor
from Musical_Intelligence.ear.h3 import H3Extractor
from Musical_Intelligence.brain.orchestrator import BrainOrchestrator
from Musical_Intelligence.brain.units.spu.relays.bch import BCH
from Musical_Intelligence.brain.regions import ALL_REGIONS

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------
def run_pipeline(device: torch.device):
    """Run full pipeline and return all data tensors."""
    # Audio → mel
    y, sr = librosa.load(AUDIO_PATH, sr=SR, mono=True, duration=DURATION_S)
    mel = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=N_MELS, hop_length=HOP, n_fft=1024)
    mel_db = librosa.power_to_db(mel, ref=np.max)
    mel_norm = (mel_db - mel_db.min()) / (mel_db.max() - mel_db.min() + 1e-8)
    mel_t = torch.tensor(mel_norm, dtype=torch.float32, device=device).unsqueeze(0)

    # R³
    print("  R³ extraction...", flush=True)
    r3_ext = R3Extractor()
    r3_out = r3_ext.extract(mel_t)
    r3 = r3_out.features  # (1, T, 97)

    # BCH demand → H³
    print("  H³ extraction...", flush=True)
    bch = BCH()
    demand = bch.h3_demand_tuples()
    h3_ext = H3Extractor()
    h3_out = h3_ext.extract(r3, demand)

    h3_gpu = {k: v.to(device) for k, v in h3_out.features.items()}
    r3_gpu = r3.to(device)

    # Brain forward
    print("  Brain forward...", flush=True)
    brain = BrainOrchestrator(nuclei=[bch])
    brain_out = brain.process(r3_gpu, h3_gpu)

    # BCH full 12D (including internal E/M layers)
    bch_full = bch.compute(h3_gpu, r3_gpu)  # (1, T, 12)

    T = r3.shape[1]
    time_axis = np.arange(T) / FRAME_RATE

    return {
        "time": time_axis,
        "T": T,
        "bch_full": bch_full[0].cpu().numpy(),     # (T, 12)
        "brain_tensor": brain_out.tensor[0].cpu().numpy(),  # (T, 6)
        "ram": brain_out.ram[0].cpu().numpy(),      # (T, 26)
        "neuro": brain_out.neuro[0].cpu().numpy(),  # (T, 4)
        "psi_affect": brain_out.psi.affect[0].cpu().numpy(),
        "psi_emotion": brain_out.psi.emotion[0].cpu().numpy(),
        "psi_aesthetic": brain_out.psi.aesthetic[0].cpu().numpy(),
        "psi_bodily": brain_out.psi.bodily[0].cpu().numpy(),
        "psi_cognitive": brain_out.psi.cognitive[0].cpu().numpy(),
        "psi_temporal": brain_out.psi.temporal[0].cpu().numpy(),
    }


# ---------------------------------------------------------------------------
# Smoothing helper
# ---------------------------------------------------------------------------
def smooth(y: np.ndarray, window: int = 51) -> np.ndarray:
    """Simple moving average for visual clarity."""
    if len(y) < window:
        return y
    kernel = np.ones(window) / window
    return np.convolve(y, kernel, mode="same")


# ---------------------------------------------------------------------------
# Color palettes
# ---------------------------------------------------------------------------
PAL_E = ["#E63946", "#F4A261", "#2A9D8F", "#264653"]
PAL_M = ["#457B9D", "#1D3557"]
PAL_P = ["#E76F51", "#F4A261", "#2A9D8F"]
PAL_F = ["#6A0572", "#AB83A1", "#D4A5A5"]
PAL_RAM = ["#264653", "#2A9D8F", "#E9C46A", "#F4A261", "#E76F51", "#E63946"]
PAL_NEURO = ["#E63946", "#457B9D", "#2A9D8F", "#F4A261"]
PAL_AFFECT = ["#2ECC71", "#E74C3C", "#9B59B6", "#3498DB"]
PAL_EMOTION = ["#F1C40F", "#3498DB", "#E74C3C", "#9B59B6", "#E67E22", "#1ABC9C", "#2ECC71"]
PAL_AESTHETIC = ["#E91E63", "#FF9800", "#00BCD4", "#FF5722", "#4CAF50"]
PAL_BODILY = ["#9C27B0", "#FF5722", "#607D8B", "#4CAF50"]
PAL_COGNITIVE = ["#795548", "#FF9800", "#3F51B5", "#009688"]
PAL_TEMPORAL = ["#F44336", "#4CAF50", "#FF9800", "#2196F3"]

SW = 85  # smoothing window


def plot_panel(ax, time, data_dict, palette, title, ylabel="value"):
    """Plot multiple traces on one axis."""
    for i, (name, vals) in enumerate(data_dict.items()):
        color = palette[i % len(palette)]
        ax.plot(time, smooth(vals, SW), color=color, linewidth=0.8, label=name, alpha=0.9)
    ax.set_ylabel(ylabel, fontsize=7)
    ax.set_title(title, fontsize=9, fontweight="bold", loc="left")
    ax.legend(fontsize=5.5, ncol=min(len(data_dict), 4), loc="upper right",
              framealpha=0.7, handlelength=1.2)
    ax.set_xlim(time[0], time[-1])
    ax.tick_params(labelsize=6)
    ax.grid(True, alpha=0.2)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"Device: {device}")
    print("Running pipeline...")
    D = run_pipeline(device)

    time = D["time"]
    bch = D["bch_full"]

    # Active RAM regions
    active_ram = {}
    for region in ALL_REGIONS:
        col = D["ram"][:, region.index]
        if np.abs(col).max() > 1e-5:
            active_ram[region.abbreviation] = col

    # =====================================================================
    # Figure: 10-panel visualization
    # =====================================================================
    fig = plt.figure(figsize=(18, 28))
    gs = GridSpec(10, 1, figure=fig, hspace=0.42)

    # --- 1. BCH E-layer (4D) ---
    ax1 = fig.add_subplot(gs[0])
    plot_panel(ax1, time, {
        "f01 NPS": bch[:, 0],
        "f02 Harmonicity": bch[:, 1],
        "f03 Hierarchy": bch[:, 2],
        "f04 FFR-Behavior": bch[:, 3],
    }, PAL_E, "BCH E-Layer (Extraction, 4D) — Internal")

    # --- 2. BCH M-layer (2D) ---
    ax2 = fig.add_subplot(gs[1])
    plot_panel(ax2, time, {
        "nps_t": bch[:, 4],
        "harm_interval": bch[:, 5],
    }, PAL_M, "BCH M-Layer (Mechanism, 2D) — Internal")

    # --- 3. BCH P-layer (3D) ---
    ax3 = fig.add_subplot(gs[2])
    plot_panel(ax3, time, {
        "consonance_signal": bch[:, 6],
        "template_match": bch[:, 7],
        "neural_pitch": bch[:, 8],
    }, PAL_P, "BCH P-Layer (Cognitive, 3D) — External")

    # --- 4. BCH F-layer (3D) ---
    ax4 = fig.add_subplot(gs[3])
    plot_panel(ax4, time, {
        "consonance_pred": bch[:, 9],
        "pitch_propagation": bch[:, 10],
        "interval_expect": bch[:, 11],
    }, PAL_F, "BCH F-Layer (Forecast, 3D) — Hybrid")

    # --- 5. RAM Active Regions (6 channels) ---
    ax5 = fig.add_subplot(gs[4])
    plot_panel(ax5, time, active_ram, PAL_RAM,
               f"Region Activation Map ({len(active_ram)} active / 26)")

    # --- 6. Neurochemistry (4D) ---
    ax6 = fig.add_subplot(gs[5])
    plot_panel(ax6, time, {
        "DA (Dopamine)": D["neuro"][:, 0],
        "NE (Norepinephrine)": D["neuro"][:, 1],
        "OPI (Opioid)": D["neuro"][:, 2],
        "5HT (Serotonin)": D["neuro"][:, 3],
    }, PAL_NEURO, "Neurochemical State (4D)")

    # --- 7. Ψ³ Affect (4D) ---
    ax7 = fig.add_subplot(gs[6])
    plot_panel(ax7, time, {
        "valence": D["psi_affect"][:, 0],
        "arousal": D["psi_affect"][:, 1],
        "tension": D["psi_affect"][:, 2],
        "dominance": D["psi_affect"][:, 3],
    }, PAL_AFFECT, "Ψ³ Affect (4D)")

    # --- 8. Ψ³ Emotion (7D) ---
    ax8 = fig.add_subplot(gs[7])
    plot_panel(ax8, time, {
        "joy": D["psi_emotion"][:, 0],
        "sadness": D["psi_emotion"][:, 1],
        "fear": D["psi_emotion"][:, 2],
        "awe": D["psi_emotion"][:, 3],
        "nostalgia": D["psi_emotion"][:, 4],
        "tenderness": D["psi_emotion"][:, 5],
        "serenity": D["psi_emotion"][:, 6],
    }, PAL_EMOTION, "Ψ³ Emotion (7D)")

    # --- 9. Ψ³ Aesthetic (5D) ---
    ax9 = fig.add_subplot(gs[8])
    plot_panel(ax9, time, {
        "beauty": D["psi_aesthetic"][:, 0],
        "groove": D["psi_aesthetic"][:, 1],
        "flow": D["psi_aesthetic"][:, 2],
        "surprise": D["psi_aesthetic"][:, 3],
        "closure": D["psi_aesthetic"][:, 4],
    }, PAL_AESTHETIC, "Ψ³ Aesthetic (5D)")

    # --- 10. Ψ³ Bodily + Cognitive + Temporal (12D) ---
    ax10 = fig.add_subplot(gs[9])
    combined = {}
    for i, name in enumerate(["chills", "movement", "breath", "release"]):
        combined[f"B:{name}"] = D["psi_bodily"][:, i]
    for i, name in enumerate(["familiar", "absorb", "expect", "attn"]):
        combined[f"C:{name}"] = D["psi_cognitive"][:, i]
    for i, name in enumerate(["anticip", "resolut", "buildup", "release"]):
        combined[f"T:{name}"] = D["psi_temporal"][:, i]
    all_pal = PAL_BODILY + PAL_COGNITIVE + PAL_TEMPORAL
    plot_panel(ax10, time, combined, all_pal,
               "Ψ³ Bodily(4D) + Cognitive(4D) + Temporal(4D)")
    ax10.set_xlabel("Time (seconds)", fontsize=8)

    # --- Suptitle ---
    total_channels = 12 + len(active_ram) + 4 + 28
    fig.suptitle(
        f"Beethoven — Pathétique Sonata Op.13 I. Grave–Allegro  |  "
        f"BCH Single Nucleus  |  {total_channels} Time Series  |  "
        f"{D['T']} frames @ {FRAME_RATE:.1f} Hz  |  MPS GPU",
        fontsize=12, fontweight="bold", y=0.995,
    )

    # Save
    os.makedirs(FIG_DIR, exist_ok=True)
    fig_path = os.path.join(FIG_DIR, "beethoven_bch_all_50_channels.png")
    fig.savefig(fig_path, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"\nSaved: {fig_path}")

    # =====================================================================
    # Figure 2: Heatmap overview — all 50 channels stacked
    # =====================================================================
    print("Generating heatmap...")

    # Build the full (50, T) matrix with labels
    channels = []
    labels = []

    # BCH 12D
    bch_names = [
        "E: f01_nps", "E: f02_harmonicity", "E: f03_hierarchy", "E: f04_ffr_behavior",
        "M: nps_t", "M: harm_interval",
        "P: consonance_signal", "P: template_match", "P: neural_pitch",
        "F: consonance_pred", "F: pitch_propagation", "F: interval_expect",
    ]
    for i, name in enumerate(bch_names):
        channels.append(smooth(bch[:, i], SW))
        labels.append(name)

    # RAM active
    for rname, vals in active_ram.items():
        channels.append(smooth(vals, SW))
        labels.append(f"RAM: {rname}")

    # Neuro
    for i, name in enumerate(["Neuro: DA", "Neuro: NE", "Neuro: OPI", "Neuro: 5HT"]):
        channels.append(smooth(D["neuro"][:, i], SW))
        labels.append(name)

    # Ψ³
    psi_groups = [
        ("Affect", D["psi_affect"], ["valence", "arousal", "tension", "dominance"]),
        ("Emotion", D["psi_emotion"],
         ["joy", "sadness", "fear", "awe", "nostalgia", "tenderness", "serenity"]),
        ("Aesthetic", D["psi_aesthetic"], ["beauty", "groove", "flow", "surprise", "closure"]),
        ("Bodily", D["psi_bodily"], ["chills", "movement", "breath", "release"]),
        ("Cognitive", D["psi_cognitive"], ["familiar", "absorb", "expect", "attn"]),
        ("Temporal", D["psi_temporal"], ["anticip", "resolut", "buildup", "release"]),
    ]
    for group_name, arr, names in psi_groups:
        for i, name in enumerate(names):
            channels.append(smooth(arr[:, i], SW))
            labels.append(f"Ψ³ {group_name}: {name}")

    matrix = np.stack(channels)  # (N_channels, T)
    N_ch = len(channels)

    # Downsample time for heatmap readability
    step = max(1, D["T"] // 600)
    matrix_ds = matrix[:, ::step]
    time_ds = time[::step]

    fig2, ax = plt.subplots(figsize=(18, 14))
    im = ax.imshow(
        matrix_ds, aspect="auto", cmap="magma", interpolation="bilinear",
        extent=[time_ds[0], time_ds[-1], N_ch - 0.5, -0.5],
        vmin=0, vmax=1,
    )
    ax.set_yticks(range(N_ch))
    ax.set_yticklabels(labels, fontsize=5.5)
    ax.set_xlabel("Time (seconds)", fontsize=9)
    ax.set_title(
        f"BCH Full Output Heatmap — {N_ch} Channels × {D['T']} Frames  |  "
        f"Beethoven Pathétique Op.13  |  MPS GPU",
        fontsize=11, fontweight="bold",
    )

    # Group separators
    separators = [4, 6, 9, 12, 12 + len(active_ram),
                  12 + len(active_ram) + 4]
    psi_offset = 12 + len(active_ram) + 4
    psi_sizes = [4, 7, 5, 4, 4, 4]
    for ps in psi_sizes[:-1]:
        psi_offset += ps
        separators.append(psi_offset)

    for sep in separators:
        ax.axhline(sep - 0.5, color="white", linewidth=0.8, alpha=0.7)

    cb = fig2.colorbar(im, ax=ax, shrink=0.6, pad=0.01)
    cb.set_label("Activation", fontsize=8)
    cb.ax.tick_params(labelsize=6)

    fig2_path = os.path.join(FIG_DIR, "beethoven_bch_heatmap_50ch.png")
    fig2.savefig(fig2_path, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig2)
    print(f"Saved: {fig2_path}")

    print(f"\nTotal unique time series: {N_ch}")
    print("Done!")


if __name__ == "__main__":
    main()
