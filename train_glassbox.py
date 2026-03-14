#!/usr/bin/env python3
"""Glass-box MI model: cascaded R³ → H³ → Beliefs → 5+5.

Full 4-head architecture mirroring the original pipeline.
Every intermediate layer is learned AND inspectable:

    mel(128,T) → R³Head    → 97D   (spectral features)
    R³(97,T)   → H³Head    → 637D  (multi-scale temporal morphology)
    [R³⊕H³]    → BeliefHead→ 131D  (cognitive beliefs)
    beliefs     → DimHead   → 10D   (5+5 dual-radar dimensions)

Ground truth comes from the full MI pipeline (R³→H³→C³).

Usage:
    python train_glassbox.py              # generate data + train
    python train_glassbox.py --train-only # skip data generation
"""
from __future__ import annotations

import argparse
import importlib
import json
import multiprocessing as mp
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

import numpy as np
import torch
import torch.nn as nn
from torch import Tensor
from torch.utils.data import Dataset, DataLoader

# ── Constants ──────────────────────────────────────────────────────────
SAMPLE_RATE = 44100
HOP_LENGTH = 256
N_MELS = 128
N_FFT = 2048
FRAME_RATE = SAMPLE_RATE / HOP_LENGTH  # 172.27 Hz

PROJECT_ROOT = Path(__file__).resolve().parent
_DEFAULT_AUDIO_DIR = PROJECT_ROOT / "Legacy" / "test-classics" / "segments"
_DEFAULT_DATA_DIR = PROJECT_ROOT / "training_data"
_DEFAULT_MODEL_DIR = PROJECT_ROOT / "trained_models"

# These are set from CLI args in main()
SEGMENTS_DIR = _DEFAULT_AUDIO_DIR
DATA_DIR = _DEFAULT_DATA_DIR
MODEL_DIR = _DEFAULT_MODEL_DIR

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
# beliefs module is now in Musical_Intelligence/brain/beliefs.py


# ======================================================================
# PART 1: Data Generation
# ======================================================================

_DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
_MEL_TRANSFORM = None


def _get_mel_transform():
    global _MEL_TRANSFORM
    if _MEL_TRANSFORM is None:
        import torchaudio
        _MEL_TRANSFORM = torchaudio.transforms.MelSpectrogram(
            sample_rate=SAMPLE_RATE, n_fft=N_FFT,
            hop_length=HOP_LENGTH, n_mels=N_MELS, power=2.0,
        ).to(_DEVICE)
    return _MEL_TRANSFORM


def load_audio(filepath: Path) -> Tuple[Tensor, Tensor, float]:
    """Load audio → (waveform, mel, duration_s) via ffmpeg. Mel on GPU if available."""
    cmd = [
        "ffmpeg", "-i", str(filepath),
        "-f", "f32le", "-acodec", "pcm_f32le",
        "-ar", str(SAMPLE_RATE), "-ac", "1",
        "-v", "quiet", "-",
    ]
    result = subprocess.run(cmd, capture_output=True, timeout=60)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed on {filepath.name}")
    samples = np.frombuffer(result.stdout, dtype=np.float32)
    if len(samples) == 0:
        raise RuntimeError(f"Empty audio: {filepath.name}")
    waveform = torch.from_numpy(samples.copy()).unsqueeze(0)
    duration_s = waveform.shape[-1] / SAMPLE_RATE

    pad_len = N_FFT // 2
    edge_l = waveform[:, :1].expand(-1, pad_len)
    edge_r = waveform[:, -1:].expand(-1, pad_len)
    waveform_padded = torch.cat([edge_l, waveform, edge_r], dim=-1).to(_DEVICE)

    mel_transform = _get_mel_transform()
    mel = mel_transform(waveform_padded)
    pad_frames = pad_len // HOP_LENGTH
    mel = mel[:, :, pad_frames: mel.shape[-1] - pad_frames]
    mel = torch.log1p(mel)
    mel_max = mel.amax(dim=(-2, -1), keepdim=True).clamp(min=1e-8)
    mel = mel / mel_max
    # waveform stays on CPU (only needed for sr), mel on GPU
    return waveform.to(_DEVICE), mel, duration_s


_FUNCTION_IDS = ("f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9")
_ROLE_TO_DEPTH = {"relay": 0, "encoder": 1, "associator": 2, "integrator": 3, "hub": 4}


def collect_mechanisms() -> List[Any]:
    from Musical_Intelligence.contracts.bases.nucleus import _NucleusBase
    instances = []
    for fn in _FUNCTION_IDS:
        mod_path = f"Musical_Intelligence.brain.functions.{fn}.mechanisms"
        try:
            mod = importlib.import_module(mod_path)
            for name in getattr(mod, "__all__", []):
                cls = getattr(mod, name, None)
                if cls and isinstance(cls, type) and issubclass(cls, _NucleusBase):
                    try:
                        instances.append(cls())
                    except Exception:
                        pass
        except Exception:
            pkg_dir = PROJECT_ROOT / "Musical_Intelligence" / "brain" / "functions" / fn / "mechanisms"
            if not pkg_dir.is_dir():
                continue
            for sub in sorted(pkg_dir.iterdir()):
                if not sub.is_dir() or sub.name.startswith(("_", ".")):
                    continue
                try:
                    sub_mod = importlib.import_module(f"{mod_path}.{sub.name}")
                except Exception:
                    continue
                for attr_name in dir(sub_mod):
                    attr = getattr(sub_mod, attr_name, None)
                    if attr and isinstance(attr, type) and issubclass(attr, _NucleusBase) and attr is not _NucleusBase:
                        try:
                            instances.append(attr())
                        except Exception:
                            pass
    return instances


def fix_depths(nuclei):
    for n in nuclei:
        role = getattr(n, "ROLE", "relay")
        min_depth = _ROLE_TO_DEPTH.get(role, 0)
        if n.PROCESSING_DEPTH < min_depth:
            n.PROCESSING_DEPTH = min_depth


def _init_worker(data_dir_str, h3_tuple_order_list):
    """Initialize MI pipeline in each worker process."""
    global _W_NUCLEI, _W_H3_DEMAND, _W_H3_ORDER, _W_N_H3
    global _W_R3, _W_H3, _W_EXEC, _W_BELIEFS, _W_DIM
    global _W_DATA_DIR

    _W_DATA_DIR = Path(data_dir_str)
    _W_H3_ORDER = [tuple(t) for t in h3_tuple_order_list]
    _W_N_H3 = len(_W_H3_ORDER)

    _W_NUCLEI = collect_mechanisms()
    fix_depths(_W_NUCLEI)

    _W_H3_DEMAND = set()
    for m in _W_NUCLEI:
        for spec in m.h3_demand:
            _W_H3_DEMAND.add(spec.as_tuple())

    from Musical_Intelligence.ear.r3 import R3Extractor
    from Musical_Intelligence.ear.h3 import H3Extractor
    from Musical_Intelligence.brain.executor import execute
    from Musical_Intelligence.brain.beliefs import compute_beliefs
    from Musical_Intelligence.brain.dimensions import DimensionInterpreter

    _W_R3 = R3Extractor()
    _W_H3 = H3Extractor()
    _W_EXEC = execute
    _W_BELIEFS = compute_beliefs
    _W_DIM = DimensionInterpreter()


def _process_segment(seg_path_str):
    """Process a single segment in a worker process. Returns (stem, ok)."""
    seg_path = Path(seg_path_str)
    out_file = _W_DATA_DIR / f"{seg_path.stem}.npz"
    if out_file.exists():
        return (seg_path.stem, True)

    try:
        waveform, mel, dur = load_audio(seg_path)
        with torch.no_grad():
            r3_out = _W_R3.extract(mel, audio=waveform, sr=SAMPLE_RATE)
            h3_out = _W_H3.extract(r3_out.features, _W_H3_DEMAND)
            outputs, _, _ = _W_EXEC(_W_NUCLEI, h3_out.features, r3_out.features)

        T = r3_out.features.shape[1]
        r3_np = r3_out.features[0].cpu().numpy()
        mel_np = mel[0].cpu().numpy()

        h3_np = np.zeros((T, _W_N_H3), dtype=np.float32)
        for j, tup in enumerate(_W_H3_ORDER):
            if tup in h3_out.features:
                h3_np[:, j] = h3_out.features[tup][0].cpu().numpy()

        relays = {n.NAME: outputs[n.NAME][0].cpu().numpy()
                  for n in _W_NUCLEI if n.NAME in outputs}
        beliefs = _W_BELIEFS(relays, _W_NUCLEI, normalize=True)

        dim_result = _W_DIM.interpret_numpy(beliefs)
        dims_10 = np.concatenate(
            [dim_result["musical_5d"], dim_result["emotional_5d"]], axis=-1,
        ).astype(np.float32)

        np.savez_compressed(
            out_file,
            mel=mel_np.astype(np.float32),
            r3=r3_np.astype(np.float32),
            h3=h3_np,
            beliefs=beliefs.astype(np.float32),
            dims=dims_10,
        )
        return (seg_path.stem, True)

    except Exception as e:
        return (seg_path.stem, False, str(e))


def generate_training_data(num_workers=1):
    """Run MI pipeline on all segments, save (mel, r3, h3, beliefs, dims) per segment."""
    DATA_DIR.mkdir(exist_ok=True)

    segments = sorted(
        p for ext in ("*.mp3", "*.wav", "*.flac")
        for p in SEGMENTS_DIR.rglob(ext)
        if not p.name.startswith("._")
    )
    print(f"Found {len(segments)} segments", flush=True)

    # Initialize pipeline (main process, for h3 tuple order)
    print("Initializing MI pipeline...", flush=True)
    nuclei = collect_mechanisms()
    fix_depths(nuclei)

    h3_demand: Set[Tuple[int, int, int, int]] = set()
    for m in nuclei:
        for spec in m.h3_demand:
            h3_demand.add(spec.as_tuple())

    h3_tuple_order = sorted(h3_demand)
    n_h3 = len(h3_tuple_order)
    print(f"Ready: {len(nuclei)} mechanisms, {n_h3} H³ demands\n", flush=True)

    with open(DATA_DIR / "h3_tuple_order.json", "w") as f:
        json.dump([list(t) for t in h3_tuple_order], f)

    # Filter out already-completed segments
    todo = []
    manifest = []
    for seg_path in segments:
        out_file = DATA_DIR / f"{seg_path.stem}.npz"
        if out_file.exists():
            manifest.append(seg_path.stem)
        else:
            todo.append(seg_path)

    cached = len(manifest)
    print(f"  {cached} cached, {len(todo)} to process (workers={num_workers})\n", flush=True)

    if not todo:
        print("All segments already cached!", flush=True)
        with open(DATA_DIR / "manifest.json", "w") as f:
            json.dump(manifest, f)
        return manifest

    t0 = time.perf_counter()
    completed = 0
    failed = 0

    if num_workers > 1:
        # Multiprocessing mode
        h3_order_list = [list(t) for t in h3_tuple_order]
        with mp.Pool(
            processes=num_workers,
            initializer=_init_worker,
            initargs=(str(DATA_DIR), h3_order_list),
        ) as pool:
            for i, result in enumerate(pool.imap_unordered(
                _process_segment,
                [str(p) for p in todo],
                chunksize=4,
            )):
                if len(result) == 2:
                    manifest.append(result[0])
                    completed += 1
                else:
                    failed += 1
                    if failed <= 10:
                        print(f"  FAILED: {result[0][:40]} — {result[2]}", flush=True)

                done = i + 1
                if done % 50 == 0 or done == 1:
                    elapsed = time.perf_counter() - t0
                    rate = done / elapsed if elapsed > 0 else 0
                    eta = (len(todo) - done) / rate if rate > 0 else 0
                    print(f"  [{cached+done:4d}/{len(segments)}]  {rate:.1f} seg/s  "
                          f"ETA {eta:.0f}s  OK={cached+completed} FAIL={failed}", flush=True)
    else:
        # Single-process mode (original)
        from Musical_Intelligence.ear.r3 import R3Extractor
        from Musical_Intelligence.ear.h3 import H3Extractor
        from Musical_Intelligence.brain.executor import execute
        from Musical_Intelligence.brain.beliefs import compute_beliefs
        from Musical_Intelligence.brain.dimensions import DimensionInterpreter

        r3_extractor = R3Extractor()
        h3_extractor = H3Extractor()
        dim_interp = DimensionInterpreter()

        for i, seg_path in enumerate(todo):
            try:
                waveform, mel, dur = load_audio(seg_path)
                with torch.no_grad():
                    r3_out = r3_extractor.extract(mel, audio=waveform, sr=SAMPLE_RATE)
                    h3_out = h3_extractor.extract(r3_out.features, h3_demand)
                    outputs, _, _ = execute(nuclei, h3_out.features, r3_out.features)

                T = r3_out.features.shape[1]
                r3_np = r3_out.features[0].cpu().numpy()
                mel_np = mel[0].cpu().numpy()

                h3_np = np.zeros((T, n_h3), dtype=np.float32)
                for j, tup in enumerate(h3_tuple_order):
                    if tup in h3_out.features:
                        h3_np[:, j] = h3_out.features[tup][0].cpu().numpy()

                relays = {n.NAME: outputs[n.NAME][0].cpu().numpy()
                          for n in nuclei if n.NAME in outputs}
                beliefs = compute_beliefs(relays, nuclei, normalize=True)

                dim_result = dim_interp.interpret_numpy(beliefs)
                dims_10 = np.concatenate(
                    [dim_result["musical_5d"], dim_result["emotional_5d"]], axis=-1,
                ).astype(np.float32)

                out_file = DATA_DIR / f"{seg_path.stem}.npz"
                np.savez_compressed(
                    out_file,
                    mel=mel_np.astype(np.float32),
                    r3=r3_np.astype(np.float32),
                    h3=h3_np,
                    beliefs=beliefs.astype(np.float32),
                    dims=dims_10,
                )
                manifest.append(seg_path.stem)
                completed += 1

            except Exception as e:
                failed += 1
                if failed <= 5:
                    print(f"  [{cached+i+1:4d}] FAILED: {seg_path.name[:50]} — {e}", flush=True)

            done = i + 1
            if done % 50 == 0 or done == 1:
                elapsed = time.perf_counter() - t0
                rate = done / elapsed if elapsed > 0 else 0
                eta = (len(todo) - done) / rate if rate > 0 else 0
                print(f"  [{cached+done:4d}/{len(segments)}]  {rate:.1f} seg/s  "
                      f"ETA {eta:.0f}s  OK={cached+completed} FAIL={failed}", flush=True)

    elapsed = time.perf_counter() - t0
    print(f"\nData generation done: {cached+completed}/{len(segments)} in {elapsed:.0f}s "
          f"({elapsed/60:.1f}min), {failed} failed", flush=True)

    with open(DATA_DIR / "manifest.json", "w") as f:
        json.dump(manifest, f)

    return manifest


# ======================================================================
# PART 2: Model Architecture — 4-head glass-box
# ======================================================================

def _load_n_h3() -> int:
    """Load H³ tuple count from saved order file."""
    path = DATA_DIR / "h3_tuple_order.json"
    if path.exists():
        with open(path) as f:
            return len(json.load(f))
    return 637  # fallback default


class R3Head(nn.Module):
    """mel(128,T) → R³(97,T) — replaces 9-group DSP pipeline."""

    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv1d(128, 256, 7, padding=3),
            nn.GELU(),
            nn.BatchNorm1d(256),

            nn.Conv1d(256, 256, 5, padding=4, dilation=2),
            nn.GELU(),
            nn.BatchNorm1d(256),

            nn.Conv1d(256, 192, 5, padding=8, dilation=4),
            nn.GELU(),
            nn.BatchNorm1d(192),

            nn.Conv1d(192, 128, 3, padding=1),
            nn.GELU(),

            nn.Conv1d(128, 97, 1),
            nn.Sigmoid(),
        )

    def forward(self, mel: Tensor) -> Tensor:
        return self.net(mel)


class H3Head(nn.Module):
    """R³(97,T) → H³(N_h3,T) — replaces multi-scale temporal morphology.

    Two-stage architecture:
      1. Dilated Conv: local context (~3s receptive field at 172Hz)
      2. Transformer Encoder: global context (full piece, via self-attention)

    This mirrors H³'s 32 horizons: micro/meso via conv, macro/ultra via attention.
    Positional encoding uses sinusoidal (time-aware, handles variable lengths).
    """

    def __init__(self, n_h3: int = 637, d_model: int = 256,
                 n_heads: int = 8, n_layers: int = 4, max_len: int = 8192):
        super().__init__()

        # Stage 1: Dilated conv for local features (~3s)
        self.local_conv = nn.Sequential(
            nn.Conv1d(97, 256, 7, padding=3),
            nn.GELU(),
            nn.BatchNorm1d(256),

            nn.Conv1d(256, 384, 5, padding=4, dilation=2),
            nn.GELU(),
            nn.BatchNorm1d(384),

            nn.Conv1d(384, 384, 5, padding=8, dilation=4),
            nn.GELU(),
            nn.BatchNorm1d(384),

            nn.Conv1d(384, d_model, 5, padding=16, dilation=8),
            nn.GELU(),
            nn.BatchNorm1d(d_model),
        )

        # Positional encoding (sinusoidal, no learnable limit)
        self.register_buffer("pe", self._sinusoidal_pe(max_len, d_model))

        # Stage 2: Transformer encoder for global context
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=n_heads,
            dim_feedforward=d_model * 4,
            dropout=0.1,
            activation="gelu",
            batch_first=True,
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=n_layers)

        # Projection to H³ output
        self.proj = nn.Sequential(
            nn.Linear(d_model, n_h3),
            nn.Tanh(),  # H³ values in [-1, 1]
        )

    @staticmethod
    def _sinusoidal_pe(max_len: int, d_model: int) -> Tensor:
        pe = torch.zeros(max_len, d_model)
        pos = torch.arange(max_len).unsqueeze(1).float()
        div = torch.exp(torch.arange(0, d_model, 2).float() * (-np.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(pos * div)
        pe[:, 1::2] = torch.cos(pos * div)
        return pe.unsqueeze(0)  # (1, max_len, d_model)

    def forward(self, r3: Tensor) -> Tensor:
        """r3: (B, 97, T) → h3: (B, N_h3, T)"""
        # Local conv: (B, 97, T) → (B, d_model, T)
        x = self.local_conv(r3)

        # Conv1d output → Transformer input: (B, d_model, T) → (B, T, d_model)
        x = x.transpose(1, 2)

        # Add positional encoding
        T = x.shape[1]
        x = x + self.pe[:, :T, :]

        # Global attention
        x = self.transformer(x)  # (B, T, d_model)

        # Project to H³: (B, T, d_model) → (B, T, N_h3) → (B, N_h3, T)
        x = self.proj(x)
        return x.transpose(1, 2)


class BeliefHead(nn.Module):
    """[R³(97)⊕H³(N_h3)](T) → beliefs(131,T) — replaces C³ mechanisms.

    Takes concatenated R³ + H³ as input, mirroring how C³ mechanisms
    read both spectral features and temporal morphology.
    """

    def __init__(self, n_h3: int = 637):
        super().__init__()
        in_ch = 97 + n_h3  # R³ + H³ concatenated
        self.net = nn.Sequential(
            nn.Conv1d(in_ch, 512, 5, padding=2),
            nn.GELU(),
            nn.BatchNorm1d(512),

            nn.Conv1d(512, 384, 5, padding=4, dilation=2),
            nn.GELU(),
            nn.BatchNorm1d(384),

            nn.Conv1d(384, 256, 3, padding=2, dilation=2),
            nn.GELU(),
            nn.BatchNorm1d(256),

            nn.Conv1d(256, 131, 1),
            nn.Sigmoid(),
        )

    def forward(self, r3: Tensor, h3: Tensor) -> Tensor:
        """r3: (B,97,T), h3: (B,N_h3,T) → beliefs: (B,131,T)"""
        x = torch.cat([r3, h3], dim=1)
        return self.net(x)


class DimHead(nn.Module):
    """beliefs(131,T) → dims(10,T) — learned 5+5 dual-radar.

    Small head: captures nonlinear belief→dimension relationships
    that the original weighted-sum formulas may underfit.
    """

    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv1d(131, 64, 3, padding=1),
            nn.GELU(),

            nn.Conv1d(64, 32, 3, padding=1),
            nn.GELU(),

            nn.Conv1d(32, 10, 1),
            nn.Sigmoid(),  # dimensions are in [0, 1]
        )

    def forward(self, beliefs: Tensor) -> Tensor:
        return self.net(beliefs)


class GlassBoxMI(nn.Module):
    """Full 4-head glass-box MI model.

    mel → R³ → H³ → Beliefs → 5+5

    Every intermediate is inspectable with semantic meaning:
    - R³: 97 spectral features (speed, roughness, consonance, ...)
    - H³: 637 temporal morphology features (trends, periodicity, ...)
    - Beliefs: 131 cognitive beliefs (harmonic_stability, mood, ...)
    - 5+5: dual-radar dimensions (speed↔fast, sad↔happy, ...)
    """

    def __init__(self, n_h3: int = 637):
        super().__init__()
        self.r3_head = R3Head()
        self.h3_head = H3Head(n_h3)
        self.belief_head = BeliefHead(n_h3)
        self.dim_head = DimHead()

    def forward(self, mel: Tensor) -> Dict[str, Tensor]:
        r3 = self.r3_head(mel)                  # (B, 97, T)
        h3 = self.h3_head(r3)                   # (B, N_h3, T)
        beliefs = self.belief_head(r3, h3)       # (B, 131, T)
        dims = self.dim_head(beliefs)            # (B, 10, T)
        return {
            "r3": r3,
            "h3": h3,
            "beliefs": beliefs,
            "dims": dims,
            "musical_5d": dims[:, :5],           # (B, 5, T)
            "emotional_5d": dims[:, 5:],         # (B, 5, T)
        }

    @torch.no_grad()
    def predict(self, mel: Tensor) -> Dict[str, Tensor]:
        self.eval()
        return self.forward(mel)


# ======================================================================
# PART 3: Dataset
# ======================================================================

class MIDataset(Dataset):
    """Loads pre-computed (mel, r3, h3, beliefs, dims) chunks."""

    def __init__(self, data_dir: Path, manifest: List[str], chunk_size: int = 512):
        self.data_dir = data_dir
        self.manifest = manifest
        self.chunk_size = chunk_size

        self.chunks: List[Tuple[int, int]] = []
        for fi, name in enumerate(manifest):
            path = data_dir / f"{name}.npz"
            if not path.exists():
                continue
            with np.load(path) as data:
                T = data["r3"].shape[0]
            n_chunks = max(1, T // chunk_size)
            for c in range(n_chunks):
                self.chunks.append((fi, c * chunk_size))

    def __len__(self):
        return len(self.chunks)

    def __getitem__(self, idx):
        fi, start = self.chunks[idx]
        end = start + self.chunk_size
        path = self.data_dir / f"{self.manifest[fi]}.npz"

        with np.load(path) as data:
            mel = data["mel"][:, start:end]          # (128, T)
            r3 = data["r3"][start:end]                # (T, 97)
            h3 = data["h3"][start:end]                # (T, N_h3)
            beliefs = data["beliefs"][start:end]      # (T, 131)
            dims = data["dims"][start:end]            # (T, 10)

        T = mel.shape[1]
        if T < self.chunk_size:
            mel = np.pad(mel, ((0, 0), (0, self.chunk_size - T)))
            r3 = np.pad(r3, ((0, self.chunk_size - T), (0, 0)))
            h3 = np.pad(h3, ((0, self.chunk_size - T), (0, 0)))
            beliefs = np.pad(beliefs, ((0, self.chunk_size - T), (0, 0)))
            dims = np.pad(dims, ((0, self.chunk_size - T), (0, 0)))

        return {
            "mel": torch.from_numpy(mel),               # (128, chunk)
            "r3": torch.from_numpy(r3.T),               # (97, chunk)
            "h3": torch.from_numpy(h3.T),               # (N_h3, chunk)
            "beliefs": torch.from_numpy(beliefs.T),      # (131, chunk)
            "dims": torch.from_numpy(dims.T),            # (10, chunk)
        }


# ======================================================================
# PART 4: Training
# ======================================================================

def train(manifest: List[str], epochs: int = 50, batch_size: int = 16,
          lr: float = 1e-3, chunk_size: int = 512):
    """Train the 4-head glass-box model."""
    MODEL_DIR.mkdir(exist_ok=True)
    n_h3 = _load_n_h3()

    device = (
        torch.device("mps") if torch.backends.mps.is_available()
        else torch.device("cuda") if torch.cuda.is_available()
        else torch.device("cpu")
    )
    print(f"Device: {device}", flush=True)

    np.random.seed(42)
    indices = np.random.permutation(len(manifest))
    split = int(0.9 * len(manifest))
    train_manifest = [manifest[i] for i in indices[:split]]
    val_manifest = [manifest[i] for i in indices[split:]]

    train_ds = MIDataset(DATA_DIR, train_manifest, chunk_size)
    val_ds = MIDataset(DATA_DIR, val_manifest, chunk_size)
    print(f"Train: {len(train_manifest)} seg ({len(train_ds)} chunks), "
          f"Val: {len(val_manifest)} seg ({len(val_ds)} chunks)", flush=True)

    train_dl = DataLoader(train_ds, batch_size=batch_size, shuffle=True,
                          num_workers=0, pin_memory=True)
    val_dl = DataLoader(val_ds, batch_size=batch_size, shuffle=False,
                        num_workers=0, pin_memory=True)

    model = GlassBoxMI(n_h3=n_h3).to(device)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"\nModel: {n_params:,} total parameters", flush=True)
    print(f"  R³Head:     {sum(p.numel() for p in model.r3_head.parameters()):,}", flush=True)
    print(f"  H³Head:     {sum(p.numel() for p in model.h3_head.parameters()):,}", flush=True)
    print(f"  BeliefHead: {sum(p.numel() for p in model.belief_head.parameters()):,}", flush=True)
    print(f"  DimHead:    {sum(p.numel() for p in model.dim_head.parameters()):,}", flush=True)

    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

    # Loss weights — cascaded, so upstream errors compound
    w_r3 = 1.0
    w_h3 = 1.5       # H³ is critical bridge
    w_beliefs = 2.0   # beliefs are the hardest
    w_dims = 1.0      # 5+5 end target

    best_val_loss = float("inf")
    history = []

    print(f"\nTraining {epochs} epochs...\n", flush=True)

    for epoch in range(epochs):
        t0 = time.perf_counter()

        # ── Train ──
        model.train()
        train_losses = {"r3": 0.0, "h3": 0.0, "beliefs": 0.0, "dims": 0.0}
        n_train = 0

        for batch in train_dl:
            mel = batch["mel"].to(device)
            r3_t = batch["r3"].to(device)
            h3_t = batch["h3"].to(device)
            b_t = batch["beliefs"].to(device)
            d_t = batch["dims"].to(device)

            # Forward through cascade
            r3_pred = model.r3_head(mel)
            h3_pred = model.h3_head(r3_pred)
            b_pred = model.belief_head(r3_pred, h3_pred)
            d_pred = model.dim_head(b_pred)

            loss_r3 = nn.functional.mse_loss(r3_pred, r3_t)
            loss_h3 = nn.functional.mse_loss(h3_pred, h3_t)
            loss_b = nn.functional.mse_loss(b_pred, b_t)
            loss_d = nn.functional.mse_loss(d_pred, d_t)

            loss = w_r3 * loss_r3 + w_h3 * loss_h3 + w_beliefs * loss_b + w_dims * loss_d

            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()

            bs = mel.shape[0]
            train_losses["r3"] += loss_r3.item() * bs
            train_losses["h3"] += loss_h3.item() * bs
            train_losses["beliefs"] += loss_b.item() * bs
            train_losses["dims"] += loss_d.item() * bs
            n_train += bs

        scheduler.step()

        # ── Validate ──
        model.eval()
        val_losses = {"r3": 0.0, "h3": 0.0, "beliefs": 0.0, "dims": 0.0}
        n_val = 0

        with torch.no_grad():
            for batch in val_dl:
                mel = batch["mel"].to(device)
                r3_t = batch["r3"].to(device)
                h3_t = batch["h3"].to(device)
                b_t = batch["beliefs"].to(device)
                d_t = batch["dims"].to(device)

                r3_pred = model.r3_head(mel)
                h3_pred = model.h3_head(r3_pred)
                b_pred = model.belief_head(r3_pred, h3_pred)
                d_pred = model.dim_head(b_pred)

                bs = mel.shape[0]
                val_losses["r3"] += nn.functional.mse_loss(r3_pred, r3_t).item() * bs
                val_losses["h3"] += nn.functional.mse_loss(h3_pred, h3_t).item() * bs
                val_losses["beliefs"] += nn.functional.mse_loss(b_pred, b_t).item() * bs
                val_losses["dims"] += nn.functional.mse_loss(d_pred, d_t).item() * bs
                n_val += bs

        # Compute averages
        tr = {k: v / n_train for k, v in train_losses.items()}
        vl = {k: v / n_val for k, v in val_losses.items()}
        val_total = sum(w * vl[k] for w, k in zip([w_r3, w_h3, w_beliefs, w_dims],
                                                    ["r3", "h3", "beliefs", "dims"]))
        elapsed = time.perf_counter() - t0

        history.append({
            "epoch": epoch + 1, "lr": scheduler.get_last_lr()[0],
            **{f"train_{k}": v for k, v in tr.items()},
            **{f"val_{k}": v for k, v in vl.items()},
        })

        improved = ""
        if val_total < best_val_loss:
            best_val_loss = val_total
            torch.save(model.state_dict(), MODEL_DIR / "glassbox_best.pt")
            improved = " ★"

        print(f"E{epoch+1:3d}/{epochs}  "
              f"R³ {tr['r3']:.5f}/{vl['r3']:.5f}  "
              f"H³ {tr['h3']:.5f}/{vl['h3']:.5f}  "
              f"B {tr['beliefs']:.5f}/{vl['beliefs']:.5f}  "
              f"D {tr['dims']:.5f}/{vl['dims']:.5f}  "
              f"{elapsed:.1f}s{improved}", flush=True)

    torch.save(model.state_dict(), MODEL_DIR / "glassbox_final.pt")
    with open(MODEL_DIR / "training_history.json", "w") as f:
        json.dump(history, f, indent=2)

    print(f"\nTraining complete. Best val loss: {best_val_loss:.6f}", flush=True)
    return model


# ======================================================================
# PART 5: Evaluation
# ======================================================================

def evaluate(model: GlassBoxMI, manifest: List[str]):
    """Evaluate trained model vs MI ground truth."""
    device = next(model.parameters()).device
    model.eval()

    from Musical_Intelligence.brain.dimensions.models.musical import MUSICAL_NAMES
    from Musical_Intelligence.brain.dimensions.models.emotional import EMOTIONAL_NAMES

    print("\n" + "=" * 70, flush=True)
    print("EVALUATION: AI predictions vs MI ground truth", flush=True)
    print("=" * 70, flush=True)

    np.random.seed(123)
    eval_indices = np.random.choice(len(manifest), min(10, len(manifest)), replace=False)

    all_corrs = {"r3": [], "h3": [], "beliefs": [], "dims": []}

    for idx in eval_indices:
        name = manifest[idx]
        path = DATA_DIR / f"{name}.npz"
        with np.load(path) as data:
            mel_np = data["mel"]
            r3_gt = data["r3"]
            h3_gt = data["h3"]
            beliefs_gt = data["beliefs"]
            dims_gt = data["dims"]

        mel_t = torch.from_numpy(mel_np).unsqueeze(0).to(device)

        with torch.no_grad():
            result = model.forward(mel_t)
            r3_pred = result["r3"][0].cpu().numpy().T
            h3_pred = result["h3"][0].cpu().numpy().T
            beliefs_pred = result["beliefs"][0].cpu().numpy().T
            dims_pred = result["dims"][0].cpu().numpy().T

        def mean_corr(gt, pred):
            corrs = []
            for d in range(gt.shape[1]):
                if gt[:, d].std() > 0.001 and pred[:, d].std() > 0.001:
                    r = np.corrcoef(gt[:, d], pred[:, d])[0, 1]
                    if not np.isnan(r):
                        corrs.append(r)
            return np.mean(corrs) if corrs else 0.0

        r3_r = mean_corr(r3_gt, r3_pred)
        h3_r = mean_corr(h3_gt, h3_pred)
        b_r = mean_corr(beliefs_gt, beliefs_pred)
        d_r = mean_corr(dims_gt, dims_pred)

        all_corrs["r3"].append(r3_r)
        all_corrs["h3"].append(h3_r)
        all_corrs["beliefs"].append(b_r)
        all_corrs["dims"].append(d_r)

        piece = name.rsplit("__", 1)[0][:35] if "__" in name else name[:35]
        print(f"  {piece:35s}  R³={r3_r:.3f}  H³={h3_r:.3f}  B={b_r:.3f}  5+5={d_r:.3f}",
              flush=True)

    print(f"\n  Mean correlation:", flush=True)
    for k in ("r3", "h3", "beliefs", "dims"):
        print(f"    {k:8s} r = {np.mean(all_corrs[k]):.3f}", flush=True)

    # Per-dimension 5+5 breakdown
    dim_names = list(MUSICAL_NAMES) + list(EMOTIONAL_NAMES)
    print(f"\n  Per-dimension 5+5 (last segment):", flush=True)
    for d, name in enumerate(dim_names):
        gt_col = dims_gt[:, d]
        pred_col = dims_pred[:, d]
        if gt_col.std() > 0.001:
            r = np.corrcoef(gt_col, pred_col)[0, 1]
            print(f"    {name:16s}  r={r:.3f}  "
                  f"GT=[{gt_col.min():.2f},{gt_col.max():.2f}]  "
                  f"AI=[{pred_col.min():.2f},{pred_col.max():.2f}]", flush=True)

    # Speed benchmark
    print("\nSpeed benchmark:", flush=True)
    mel_bench = torch.randn(1, 128, 4000).to(device)
    times = []
    for _ in range(10):
        t0 = time.perf_counter()
        with torch.no_grad():
            _ = model.forward(mel_bench)
        if device.type == "mps":
            torch.mps.synchronize()
        elif device.type == "cuda":
            torch.cuda.synchronize()
        times.append(time.perf_counter() - t0)

    avg_ms = np.mean(times[2:]) * 1000
    print(f"  24s audio → full glass-box in {avg_ms:.1f}ms  "
          f"({24000/avg_ms:.0f}x realtime)", flush=True)
    print(f"  MI pipeline: ~2000ms → Speedup: {2000/avg_ms:.0f}x", flush=True)


# ======================================================================
# Main
# ======================================================================

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train-only", action="store_true")
    parser.add_argument("--audio-dir", type=str, default=None,
                        help="Directory containing audio files (mp3/wav/flac)")
    parser.add_argument("--data-dir", type=str, default=None,
                        help="Directory for training data (npz files)")
    parser.add_argument("--model-dir", type=str, default=None,
                        help="Directory to save trained models")
    parser.add_argument("--workers", type=int, default=1,
                        help="Number of parallel workers for data generation")
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--chunk-size", type=int, default=512)
    args = parser.parse_args()

    # Override global paths if provided
    global SEGMENTS_DIR, DATA_DIR, MODEL_DIR
    if args.audio_dir:
        SEGMENTS_DIR = Path(args.audio_dir)
    if args.data_dir:
        DATA_DIR = Path(args.data_dir)
    if args.model_dir:
        MODEL_DIR = Path(args.model_dir)

    if args.train_only:
        with open(DATA_DIR / "manifest.json") as f:
            manifest = json.load(f)
        print(f"Loaded manifest: {len(manifest)} segments", flush=True)
    else:
        manifest = generate_training_data(num_workers=args.workers)

    model = train(manifest, epochs=args.epochs, batch_size=args.batch_size,
                  lr=args.lr, chunk_size=args.chunk_size)
    evaluate(model, manifest)


if __name__ == "__main__":
    main()
