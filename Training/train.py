#!/usr/bin/env python3
"""Glass-box MI Training — Per-dimension tracking & deep observability.

Architecture:  mel(128,T) → R³(97) → H³(637) → Beliefs(131) → Dims(10)

Every head, every group, every individual dimension is tracked per epoch.
Outputs:
  - logs/epoch_NNN.json       per-epoch full metrics
  - logs/summary.csv          one-line-per-epoch for quick plotting
  - logs/per_dim/              per-dimension CSVs
  - checkpoints/best.pt       best model (val loss)
  - checkpoints/final.pt      final model
  - checkpoints/epoch_NNN.pt  periodic snapshots

Usage:
    python Training/train.py --data-dir /workspace/training_data --epochs 50
    python Training/train.py --data-dir /workspace/training_data --epochs 50 --batch-size 2048
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import torch
import torch.nn as nn
from torch import Tensor
from torch.utils.data import Dataset, DataLoader

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ======================================================================
# SEMANTIC NAMES — every dimension is named & grouped
# ======================================================================

R3_GROUPS = {
    "A_consonance": (0, 7),
    "B_energy": (7, 12),
    "C_timbre": (12, 21),
    "D_change": (21, 25),
    "F_pitch_chroma": (25, 41),
    "G_rhythm_groove": (41, 51),
    "H_harmony_tonality": (51, 63),
    "J_timbre_ext": (63, 83),
    "K_modulation_psycho": (83, 97),
}

R3_NAMES = [
    "roughness", "sethares_dissonance", "helmholtz_kang", "stumpf_fusion",
    "sensory_pleasantness", "inharmonicity", "harmonic_deviation",
    "amplitude", "velocity_A", "acceleration_A", "loudness", "onset_strength",
    "warmth", "sharpness", "tonalness", "clarity", "spectral_smoothness",
    "spectral_autocorrelation", "tristimulus1", "tristimulus2", "tristimulus3",
    "spectral_flux", "distribution_entropy", "distribution_flatness", "distribution_concentration",
    "chroma_C", "chroma_Db", "chroma_D", "chroma_Eb", "chroma_E", "chroma_F",
    "chroma_Gb", "chroma_G", "chroma_Ab", "chroma_A", "chroma_Bb", "chroma_B",
    "pitch_height", "pitch_class_entropy", "pitch_salience", "inharmonicity_index",
    "tempo_estimate", "beat_strength", "pulse_clarity", "syncopation_index",
    "metricality_index", "isochrony_nPVI", "groove_index", "event_density",
    "tempo_stability", "rhythmic_regularity",
    "key_clarity", "tonnetz_fifth_x", "tonnetz_fifth_y", "tonnetz_minor_x",
    "tonnetz_minor_y", "tonnetz_major_x", "tonnetz_major_y", "voice_leading_distance",
    "harmonic_change", "tonal_stability", "diatonicity", "syntactic_irregularity",
    "mfcc_1", "mfcc_2", "mfcc_3", "mfcc_4", "mfcc_5", "mfcc_6", "mfcc_7",
    "mfcc_8", "mfcc_9", "mfcc_10", "mfcc_11", "mfcc_12", "mfcc_13",
    "spectral_contrast_1", "spectral_contrast_2", "spectral_contrast_3",
    "spectral_contrast_4", "spectral_contrast_5", "spectral_contrast_6", "spectral_contrast_7",
    "modulation_0_5Hz", "modulation_1Hz", "modulation_2Hz", "modulation_4Hz",
    "modulation_8Hz", "modulation_16Hz", "modulation_centroid", "modulation_bandwidth",
    "sharpness_zwicker", "fluctuation_strength", "loudness_a_weighted",
    "alpha_ratio", "hammarberg_index", "spectral_slope_0_500",
]

BELIEF_NAMES = [
    "salience_network", "phrase_boundary_pred", "contour_state",
    "consonance_forecast", "consonance_signal", "template_match", "hierarchy",
    "pitch_continuation", "pitch_prominence_sig", "octave_equivalence_index",
    "chroma_identity_signal", "aesthetic_integration", "reward_response_pred",
    "spectral_temporal_interaction", "recognition_pred", "melody_retrieval",
    "detection_function", "abstract_future_500ms", "hierarchy_gradient",
    "midlevel_future_200ms", "sensory_match", "high_level_lead",
    "arousal_change_1_3s", "arousal_response", "defense_cascade",
    "information_content", "valence_response", "valence_shift_2_5s",
    "alpha_beta_error", "gamma_power", "sequence_completion_2s", "gamma_match",
    "affective_evaluation", "processing_pred", "salience_network_f3",
    "sensory_load", "inharmonic_capture", "attention_shift_pred",
    "spectral_encoding", "precision_weighting", "n1p2_engagement",
    "aesthetic_judgment", "beat_locked_activity", "beat_onset_pred",
    "ssep_enhancement", "meter_position_pred", "selective_gain",
    "melodic_identification", "preservation_index", "scaffold_fc",
    "memory_state", "emotional_color", "f01_retrieval", "nostalgia_link",
    "memory_state_f4", "self_ref_fc", "mem_vividness_fc",
    "storage_state", "segmentation_state", "binding_state",
    "ans_response", "chills_intensity", "driving_signal", "emotional_arousal",
    "emotion_certainty", "happy_pathway", "mode_detection_state",
    "perceived_happy", "perceived_sad", "sad_pathway",
    "nostalgia_intens", "vividness_pred", "mpfc_activation", "wellbeing_enhance",
    "caudate_activation", "nacc_activation", "dissociation_index", "temporal_phase",
    "wanting_index", "chills_proximity", "harmonic_tension", "liking",
    "peak_detection", "pleasure", "prediction_error", "prediction_match",
    "resolution_expect", "reward_forecast", "tension", "wanting",
    "coupling_strength", "beat_gamma", "groove_index_f7", "groove_prediction",
    "meter_integration", "motor_preparation", "velocity_optimization",
    "next_beat_pred_T", "period_entrainment", "period_lock_strength",
    "variability_reduction", "context_depth", "long_context", "medium_context",
    "phrase_boundary_pred_f7", "short_context", "structure_pred",
    "detection_accuracy", "multisensory_integration", "statistical_model",
    "plasticity_magnitude", "trained_timbre_response", "between_reduction",
    "transfer_limit", "expertise_enhancement", "developmental_trajectory",
    "pitch_mmn", "rhythm_mmn", "timbre_mmn",
    "compartmentalization", "within_connectivity",
    "flow_sustain_pred", "entrainment_quality", "group_flow_state",
    "social_bonding_index", "social_prediction_error", "synchrony_reward",
    "catchiness_pred", "neural_synchrony", "visual_modulation", "social_coordination",
]

BELIEF_FUNCTIONS = {
    "F1_sensory":    (0, 17),
    "F2_prediction": (17, 32),
    "F3_attention":  (32, 47),
    "F4_memory":     (47, 60),
    "F5_emotion":    (60, 74),
    "F6_reward":     (74, 90),
    "F7_motor":      (90, 107),
    "F8_learning":   (107, 121),
    "F9_social":     (121, 131),
}

DIM_NAMES = [
    # Musical (Radar 1)
    "speed", "volume", "weight", "texture", "depth",
    # Emotional (Radar 2)
    "mood", "energy", "hardness", "predictability", "focus",
]

assert len(R3_NAMES) == 97
assert len(BELIEF_NAMES) == 131
assert len(DIM_NAMES) == 10


# ======================================================================
# MODEL ARCHITECTURE (same as train_glassbox.py)
# ======================================================================

class R3Head(nn.Module):
    """mel(128,T) → R³(97,T) — spectral feature extraction."""
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv1d(128, 256, 5, padding=2), nn.GELU(), nn.BatchNorm1d(256),
            nn.Conv1d(256, 256, 5, padding=4, dilation=2), nn.GELU(), nn.BatchNorm1d(256),
            nn.Conv1d(256, 128, 3, padding=2, dilation=2), nn.GELU(), nn.BatchNorm1d(128),
            nn.Conv1d(128, 97, 1),
        )

    def forward(self, mel: Tensor) -> Tensor:
        return self.net(mel)


class H3Head(nn.Module):
    """R³(97,T) → H³(N_h3,T) — multi-scale temporal morphology."""
    def __init__(self, n_h3: int = 637, d_model: int = 256, n_heads: int = 4,
                 n_layers: int = 2, max_len: int = 8192):
        super().__init__()
        self.local_conv = nn.Sequential(
            nn.Conv1d(97, d_model, 7, padding=3), nn.GELU(), nn.BatchNorm1d(d_model),
        )
        self.register_buffer("pe", self._sinusoidal_pe(max_len, d_model))
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model, nhead=n_heads, dim_feedforward=d_model * 4,
            dropout=0.1, activation="gelu", batch_first=True,
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=n_layers)
        self.proj = nn.Sequential(nn.Linear(d_model, n_h3), nn.Tanh())

    @staticmethod
    def _sinusoidal_pe(max_len: int, d_model: int) -> Tensor:
        pe = torch.zeros(max_len, d_model)
        pos = torch.arange(max_len).unsqueeze(1).float()
        div = torch.exp(torch.arange(0, d_model, 2).float() * (-np.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(pos * div)
        pe[:, 1::2] = torch.cos(pos * div)
        return pe.unsqueeze(0)

    def forward(self, r3: Tensor) -> Tensor:
        x = self.local_conv(r3)
        x = x.transpose(1, 2)
        T = x.shape[1]
        x = x + self.pe[:, :T, :]
        x = self.transformer(x)
        x = self.proj(x)
        return x.transpose(1, 2)


class BeliefHead(nn.Module):
    """[R³(97)⊕H³(N_h3)](T) → beliefs(131,T)."""
    def __init__(self, n_h3: int = 637):
        super().__init__()
        in_ch = 97 + n_h3
        self.net = nn.Sequential(
            nn.Conv1d(in_ch, 512, 5, padding=2), nn.GELU(), nn.BatchNorm1d(512),
            nn.Conv1d(512, 384, 5, padding=4, dilation=2), nn.GELU(), nn.BatchNorm1d(384),
            nn.Conv1d(384, 256, 3, padding=2, dilation=2), nn.GELU(), nn.BatchNorm1d(256),
            nn.Conv1d(256, 131, 1), nn.Sigmoid(),
        )

    def forward(self, r3: Tensor, h3: Tensor) -> Tensor:
        return self.net(torch.cat([r3, h3], dim=1))


class DimHead(nn.Module):
    """beliefs(131,T) → dims(10,T) — 5+5 dual-radar."""
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv1d(131, 64, 3, padding=1), nn.GELU(),
            nn.Conv1d(64, 32, 3, padding=1), nn.GELU(),
            nn.Conv1d(32, 10, 1), nn.Sigmoid(),
        )

    def forward(self, beliefs: Tensor) -> Tensor:
        return self.net(beliefs)


class GlassBoxMI(nn.Module):
    """Full 4-head: mel → R³ → H³ → Beliefs → 5+5."""
    def __init__(self, n_h3: int = 637):
        super().__init__()
        self.r3_head = R3Head()
        self.h3_head = H3Head(n_h3)
        self.belief_head = BeliefHead(n_h3)
        self.dim_head = DimHead()

    def forward(self, mel: Tensor) -> Dict[str, Tensor]:
        r3 = self.r3_head(mel)
        h3 = self.h3_head(r3)
        beliefs = self.belief_head(r3, h3)
        dims = self.dim_head(beliefs)
        return {"r3": r3, "h3": h3, "beliefs": beliefs, "dims": dims}


# ======================================================================
# DATASET — preload into RAM
# ======================================================================

class MIDataset(Dataset):
    """Preloads segment-level numpy arrays, chunks on-the-fly in __getitem__."""

    def __init__(self, data_dir: Path, manifest: List[str], chunk_size: int = 512):
        self.chunk_size = chunk_size
        # Store segment-level arrays (not per-chunk — saves RAM)
        self.segments: List[Dict[str, np.ndarray]] = []
        self.chunks: List[Tuple[int, int]] = []  # (seg_idx, start_frame)

        print(f"  Preloading {len(manifest)} segments into RAM...", flush=True)
        skipped = 0
        for i, name in enumerate(manifest):
            path = data_dir / f"{name}.npz"
            if not path.exists():
                skipped += 1
                continue
            with np.load(path) as data:
                seg = {
                    "mel": data["mel"].astype(np.float32),       # (128, T)
                    "r3": data["r3"].astype(np.float32),         # (T, 97)
                    "h3": data["h3"].astype(np.float32),         # (T, N_h3)
                    "beliefs": data["beliefs"].astype(np.float32),  # (T, 131)
                    "dims": data["dims"].astype(np.float32),     # (T, 10)
                }
            T = seg["mel"].shape[1]
            seg_idx = len(self.segments)
            self.segments.append(seg)
            n_chunks = max(1, T // chunk_size)
            for c in range(n_chunks):
                self.chunks.append((seg_idx, c * chunk_size))
            if (i + 1) % 500 == 0:
                print(f"    {i+1}/{len(manifest)} loaded ({len(self.chunks)} chunks)", flush=True)
        print(f"  Done: {len(self.chunks)} chunks from {len(self.segments)} segments "
              f"(skipped {skipped})", flush=True)

    def __len__(self):
        return len(self.chunks)

    def __getitem__(self, idx):
        seg_idx, start = self.chunks[idx]
        seg = self.segments[seg_idx]
        end = start + self.chunk_size

        mel = seg["mel"][:, start:end]
        r3 = seg["r3"][start:end]
        h3 = seg["h3"][start:end]
        beliefs = seg["beliefs"][start:end]
        dims = seg["dims"][start:end]

        Tc = mel.shape[1]
        if Tc < self.chunk_size:
            mel = np.pad(mel, ((0, 0), (0, self.chunk_size - Tc)))
            r3 = np.pad(r3, ((0, self.chunk_size - Tc), (0, 0)))
            h3 = np.pad(h3, ((0, self.chunk_size - Tc), (0, 0)))
            beliefs = np.pad(beliefs, ((0, self.chunk_size - Tc), (0, 0)))
            dims = np.pad(dims, ((0, self.chunk_size - Tc), (0, 0)))

        return {
            "mel": torch.from_numpy(mel),
            "r3": torch.from_numpy(r3.T.copy()),
            "h3": torch.from_numpy(h3.T.copy()),
            "beliefs": torch.from_numpy(beliefs.T.copy()),
            "dims": torch.from_numpy(dims.T.copy()),
        }


# ======================================================================
# PER-DIMENSION METRICS
# ======================================================================

def per_dim_mse(pred: Tensor, target: Tensor) -> Tensor:
    """MSE per output dimension. pred/target: (B, D, T) → returns (D,)."""
    return ((pred - target) ** 2).mean(dim=(0, 2))


def per_dim_mae(pred: Tensor, target: Tensor) -> Tensor:
    """MAE per output dimension. (B, D, T) → (D,)."""
    return (pred - target).abs().mean(dim=(0, 2))


def per_dim_corr(pred: Tensor, target: Tensor) -> Tensor:
    """Pearson correlation per dimension. (B, D, T) → (D,).
    Flatten B×T, compute per D."""
    D = pred.shape[1]
    # (B, D, T) → (D, B*T)
    p = pred.transpose(0, 1).reshape(D, -1)
    t = target.transpose(0, 1).reshape(D, -1)
    p_mean = p.mean(dim=1, keepdim=True)
    t_mean = t.mean(dim=1, keepdim=True)
    p_c = p - p_mean
    t_c = t - t_mean
    num = (p_c * t_c).sum(dim=1)
    den = (p_c.norm(dim=1) * t_c.norm(dim=1)).clamp(min=1e-8)
    return num / den


class MetricsAccumulator:
    """Accumulates per-dimension metrics across batches."""

    def __init__(self):
        self.reset()

    def reset(self):
        self._mse_sum: Dict[str, Tensor] = {}
        self._mae_sum: Dict[str, Tensor] = {}
        self._pred_all: Dict[str, List[Tensor]] = {}
        self._tgt_all: Dict[str, List[Tensor]] = {}
        self._n = 0

    def update(self, head: str, pred: Tensor, target: Tensor, bs: int):
        mse = per_dim_mse(pred, target) * bs
        mae = per_dim_mae(pred, target) * bs
        if head not in self._mse_sum:
            self._mse_sum[head] = torch.zeros_like(mse)
            self._mae_sum[head] = torch.zeros_like(mae)
            self._pred_all[head] = []
            self._tgt_all[head] = []
        self._mse_sum[head] += mse
        self._mae_sum[head] += mae
        # Store subset for correlation (every 10th batch to save memory)
        if self._n % 10 == 0:
            self._pred_all[head].append(pred.detach())
            self._tgt_all[head].append(target.detach())
        self._n += 1

    def compute(self, n_samples: int) -> Dict:
        result = {}
        for head in self._mse_sum:
            mse = (self._mse_sum[head] / n_samples).cpu().numpy()
            mae = (self._mae_sum[head] / n_samples).cpu().numpy()
            # Compute correlation from stored samples
            if self._pred_all[head]:
                p = torch.cat(self._pred_all[head], dim=0)
                t = torch.cat(self._tgt_all[head], dim=0)
                corr = per_dim_corr(p, t).cpu().numpy()
            else:
                corr = np.zeros_like(mse)
            result[head] = {
                "mse": mse.tolist(),
                "mae": mae.tolist(),
                "corr": corr.tolist(),
                "mse_mean": float(mse.mean()),
                "mae_mean": float(mae.mean()),
                "corr_mean": float(corr.mean()),
            }
        return result


# ======================================================================
# GROUPED METRICS
# ======================================================================

def compute_group_metrics(per_dim: Dict, head: str, groups: Dict[str, Tuple[int, int]]) -> Dict:
    """Aggregate per-dim metrics into named groups."""
    mse = per_dim[head]["mse"]
    mae = per_dim[head]["mae"]
    corr = per_dim[head]["corr"]
    result = {}
    for name, (start, end) in groups.items():
        result[name] = {
            "mse": float(np.mean(mse[start:end])),
            "mae": float(np.mean(mae[start:end])),
            "corr": float(np.mean(corr[start:end])),
            "n_dims": end - start,
        }
    return result


# ======================================================================
# TRAINING LOOP
# ======================================================================

def train(args):
    out_dir = Path(args.output_dir)
    log_dir = out_dir / "logs"
    ckpt_dir = out_dir / "checkpoints"
    perdim_dir = log_dir / "per_dim"
    for d in [log_dir, ckpt_dir, perdim_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # Device
    device = (
        torch.device("cuda") if torch.cuda.is_available()
        else torch.device("mps") if torch.backends.mps.is_available()
        else torch.device("cpu")
    )
    print(f"Device: {device}", flush=True)

    # Load manifest
    data_dir = Path(args.data_dir)
    with open(data_dir / "manifest.json") as f:
        manifest = json.load(f)
    print(f"Manifest: {len(manifest)} segments", flush=True)

    # Split 90/10
    n_val = max(1, len(manifest) // 10)
    rng = np.random.RandomState(42)
    idx = rng.permutation(len(manifest))
    val_names = [manifest[i] for i in idx[:n_val]]
    train_names = [manifest[i] for i in idx[n_val:]]

    # Datasets
    print("\n[Train set]", flush=True)
    train_ds = MIDataset(data_dir, train_names, chunk_size=args.chunk_size)
    print("[Val set]", flush=True)
    val_ds = MIDataset(data_dir, val_names, chunk_size=args.chunk_size)
    print(f"\nTrain: {len(train_names)} seg ({len(train_ds)} chunks)", flush=True)
    print(f"Val:   {len(val_names)} seg ({len(val_ds)} chunks)", flush=True)

    # Detect N_h3 from first sample
    n_h3 = train_ds.tensors[0][2].shape[0]
    print(f"H³ dim: {n_h3}", flush=True)

    # DataLoader
    train_dl = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True,
                          num_workers=0, pin_memory=True)
    val_dl = DataLoader(val_ds, batch_size=args.batch_size, shuffle=False,
                        num_workers=0, pin_memory=True)

    # Model
    model = GlassBoxMI(n_h3=n_h3).to(device)
    total_params = sum(p.numel() for p in model.parameters())
    print(f"\nModel: {total_params:,} params", flush=True)
    print(f"  R³Head:     {sum(p.numel() for p in model.r3_head.parameters()):,}", flush=True)
    print(f"  H³Head:     {sum(p.numel() for p in model.h3_head.parameters()):,}", flush=True)
    print(f"  BeliefHead: {sum(p.numel() for p in model.belief_head.parameters()):,}", flush=True)
    print(f"  DimHead:    {sum(p.numel() for p in model.dim_head.parameters()):,}", flush=True)

    # Optimizer
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)

    # Loss weights
    W = {"r3": 1.0, "h3": 1.5, "beliefs": 2.0, "dims": 1.0}

    # CSV headers for per-dim tracking
    _init_per_dim_csvs(perdim_dir)

    # Summary CSV
    summary_path = log_dir / "summary.csv"
    with open(summary_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "epoch", "lr", "elapsed_s",
            "train_r3", "train_h3", "train_beliefs", "train_dims", "train_total",
            "val_r3", "val_h3", "val_beliefs", "val_dims", "val_total",
            "val_r3_corr", "val_h3_corr", "val_beliefs_corr", "val_dims_corr",
            # R³ groups
            *[f"val_r3_{g}_mse" for g in R3_GROUPS],
            *[f"val_r3_{g}_corr" for g in R3_GROUPS],
            # Belief functions
            *[f"val_b_{g}_mse" for g in BELIEF_FUNCTIONS],
            *[f"val_b_{g}_corr" for g in BELIEF_FUNCTIONS],
            # 10 dimensions individually
            *[f"val_dim_{n}_mse" for n in DIM_NAMES],
            *[f"val_dim_{n}_corr" for n in DIM_NAMES],
            "improved",
        ])

    best_val_loss = float("inf")
    print(f"\nTraining {args.epochs} epochs, batch_size={args.batch_size}\n", flush=True)
    print(f"{'Ep':>4} {'R³':>10} {'H³':>10} {'Belief':>10} {'Dims':>10} "
          f"{'Total':>10} {'vR³':>10} {'vH³':>10} {'vBel':>10} {'vDim':>10} "
          f"{'vTot':>10} {'Time':>6}", flush=True)
    print("-" * 120, flush=True)

    for epoch in range(args.epochs):
        t0 = time.perf_counter()

        # ── TRAIN ──
        model.train()
        train_loss = {k: 0.0 for k in W}
        n_train = 0

        for batch in train_dl:
            mel = batch["mel"].to(device)
            targets = {k: batch[k].to(device) for k in ["r3", "h3", "beliefs", "dims"]}

            r3_pred = model.r3_head(mel)
            h3_pred = model.h3_head(r3_pred)
            b_pred = model.belief_head(r3_pred, h3_pred)
            d_pred = model.dim_head(b_pred)
            preds = {"r3": r3_pred, "h3": h3_pred, "beliefs": b_pred, "dims": d_pred}

            losses = {k: nn.functional.mse_loss(preds[k], targets[k]) for k in W}
            loss = sum(W[k] * losses[k] for k in W)

            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()

            bs = mel.shape[0]
            for k in W:
                train_loss[k] += losses[k].item() * bs
            n_train += bs

        scheduler.step()

        # ── VALIDATE with per-dim metrics ──
        model.eval()
        val_loss = {k: 0.0 for k in W}
        n_val = 0
        metrics = MetricsAccumulator()

        with torch.no_grad():
            for batch in val_dl:
                mel = batch["mel"].to(device)
                targets = {k: batch[k].to(device) for k in ["r3", "h3", "beliefs", "dims"]}

                r3_pred = model.r3_head(mel)
                h3_pred = model.h3_head(r3_pred)
                b_pred = model.belief_head(r3_pred, h3_pred)
                d_pred = model.dim_head(b_pred)
                preds = {"r3": r3_pred, "h3": h3_pred, "beliefs": b_pred, "dims": d_pred}

                bs = mel.shape[0]
                for k in W:
                    val_loss[k] += nn.functional.mse_loss(preds[k], targets[k]).item() * bs
                n_val += bs

                for k in W:
                    metrics.update(k, preds[k], targets[k], bs)

        # Averages
        tr = {k: v / n_train for k, v in train_loss.items()}
        vl = {k: v / n_val for k, v in val_loss.items()}
        tr_total = sum(W[k] * tr[k] for k in W)
        vl_total = sum(W[k] * vl[k] for k in W)
        elapsed = time.perf_counter() - t0

        # Per-dim metrics
        pdm = metrics.compute(n_val)

        # Group metrics
        r3_groups = compute_group_metrics(pdm, "r3", R3_GROUPS)
        belief_funcs = compute_group_metrics(pdm, "beliefs", BELIEF_FUNCTIONS)

        # Best model
        improved = vl_total < best_val_loss
        if improved:
            best_val_loss = vl_total
            torch.save(model.state_dict(), ckpt_dir / "best.pt")

        # Periodic checkpoint
        if (epoch + 1) % 10 == 0 or epoch == 0:
            torch.save(model.state_dict(), ckpt_dir / f"epoch_{epoch+1:03d}.pt")

        # ── LOGGING ──

        # Console
        star = " *" if improved else ""
        print(f"{epoch+1:4d} "
              f"{tr['r3']:.6f} {tr['h3']:.6f} {tr['beliefs']:.6f} {tr['dims']:.6f} "
              f"{tr_total:.6f} "
              f"{vl['r3']:.6f} {vl['h3']:.6f} {vl['beliefs']:.6f} {vl['dims']:.6f} "
              f"{vl_total:.6f} {elapsed:5.1f}s{star}", flush=True)

        # Per-dim console (every 5 epochs)
        if (epoch + 1) % 5 == 0:
            print(f"\n  --- Epoch {epoch+1} Per-Dimension Detail ---", flush=True)

            # R³ groups
            print(f"  R³ Groups:", flush=True)
            for gname, gm in r3_groups.items():
                print(f"    {gname:25s}  MSE={gm['mse']:.6f}  r={gm['corr']:+.4f}", flush=True)

            # Belief functions
            print(f"  Belief Functions:", flush=True)
            for fname, fm in belief_funcs.items():
                print(f"    {fname:25s}  MSE={fm['mse']:.6f}  r={fm['corr']:+.4f}", flush=True)

            # 10 dims individually
            print(f"  Dimensions (5+5):", flush=True)
            dim_mse = pdm["dims"]["mse"]
            dim_corr = pdm["dims"]["corr"]
            print(f"    {'Musical:':<12}", end="", flush=True)
            for i in range(5):
                print(f"  {DIM_NAMES[i]:>14s}={dim_mse[i]:.5f} r={dim_corr[i]:+.3f}", end="", flush=True)
            print(flush=True)
            print(f"    {'Emotional:':<12}", end="", flush=True)
            for i in range(5, 10):
                print(f"  {DIM_NAMES[i]:>14s}={dim_mse[i]:.5f} r={dim_corr[i]:+.3f}", end="", flush=True)
            print(f"\n", flush=True)

            # Top 5 worst beliefs
            b_mse = np.array(pdm["beliefs"]["mse"])
            worst = np.argsort(b_mse)[-5:][::-1]
            print(f"  Top-5 hardest beliefs:", flush=True)
            for idx in worst:
                print(f"    b{idx:3d} {BELIEF_NAMES[idx]:30s}  MSE={b_mse[idx]:.6f}  r={pdm['beliefs']['corr'][idx]:+.4f}", flush=True)
            print(flush=True)

        # Full epoch JSON
        epoch_data = {
            "epoch": epoch + 1,
            "lr": scheduler.get_last_lr()[0],
            "elapsed_s": elapsed,
            "train": tr,
            "train_total": tr_total,
            "val": vl,
            "val_total": vl_total,
            "improved": improved,
            "per_dim": pdm,
            "r3_groups": r3_groups,
            "belief_functions": belief_funcs,
        }
        with open(log_dir / f"epoch_{epoch+1:03d}.json", "w") as f:
            json.dump(epoch_data, f, indent=2)

        # Summary CSV row
        lr = scheduler.get_last_lr()[0]
        with open(summary_path, "a", newline="") as f:
            w = csv.writer(f)
            w.writerow([
                epoch + 1, f"{lr:.8f}", f"{elapsed:.1f}",
                f"{tr['r3']:.6f}", f"{tr['h3']:.6f}", f"{tr['beliefs']:.6f}", f"{tr['dims']:.6f}", f"{tr_total:.6f}",
                f"{vl['r3']:.6f}", f"{vl['h3']:.6f}", f"{vl['beliefs']:.6f}", f"{vl['dims']:.6f}", f"{vl_total:.6f}",
                f"{pdm['r3']['corr_mean']:.4f}", f"{pdm['h3']['corr_mean']:.4f}",
                f"{pdm['beliefs']['corr_mean']:.4f}", f"{pdm['dims']['corr_mean']:.4f}",
                *[f"{r3_groups[g]['mse']:.6f}" for g in R3_GROUPS],
                *[f"{r3_groups[g]['corr']:.4f}" for g in R3_GROUPS],
                *[f"{belief_funcs[g]['mse']:.6f}" for g in BELIEF_FUNCTIONS],
                *[f"{belief_funcs[g]['corr']:.4f}" for g in BELIEF_FUNCTIONS],
                *[f"{pdm['dims']['mse'][i]:.6f}" for i in range(10)],
                *[f"{pdm['dims']['corr'][i]:.4f}" for i in range(10)],
                "1" if improved else "0",
            ])

        # Per-dim CSVs (append row per epoch)
        _append_per_dim_csvs(perdim_dir, epoch + 1, pdm)

    # Final save
    torch.save(model.state_dict(), ckpt_dir / "final.pt")
    print(f"\nTraining complete. Best val loss: {best_val_loss:.6f}", flush=True)
    print(f"Outputs: {out_dir}", flush=True)


def _init_per_dim_csvs(perdim_dir: Path):
    """Create CSV files for per-dimension tracking."""
    # R³: 97 dimensions
    with open(perdim_dir / "r3.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["epoch", *[f"{n}_mse" for n in R3_NAMES], *[f"{n}_corr" for n in R3_NAMES]])

    # Beliefs: 131 dimensions
    with open(perdim_dir / "beliefs.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["epoch", *[f"{n}_mse" for n in BELIEF_NAMES], *[f"{n}_corr" for n in BELIEF_NAMES]])

    # Dims: 10 dimensions
    with open(perdim_dir / "dims.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["epoch", *[f"{n}_mse" for n in DIM_NAMES], *[f"{n}_corr" for n in DIM_NAMES]])


def _append_per_dim_csvs(perdim_dir: Path, epoch: int, pdm: Dict):
    """Append one row per epoch to each per-dim CSV."""
    for fname, key, names in [
        ("r3.csv", "r3", R3_NAMES),
        ("beliefs.csv", "beliefs", BELIEF_NAMES),
        ("dims.csv", "dims", DIM_NAMES),
    ]:
        with open(perdim_dir / fname, "a", newline="") as f:
            w = csv.writer(f)
            mse = pdm[key]["mse"]
            corr = pdm[key]["corr"]
            w.writerow([epoch, *[f"{v:.6f}" for v in mse], *[f"{v:.4f}" for v in corr]])


# ======================================================================
# MAIN
# ======================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Glass-box MI Training")
    parser.add_argument("--data-dir", type=str, required=True, help="Directory with NPZ + manifest.json")
    parser.add_argument("--output-dir", type=str, default=str(PROJECT_ROOT / "Training" / "runs" / "default"),
                        help="Output dir for logs/checkpoints")
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--batch-size", type=int, default=256)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--chunk-size", type=int, default=512)
    args = parser.parse_args()
    train(args)
