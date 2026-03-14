#!/usr/bin/env python3
"""Run full R³→H³→C³→5+5 pipeline on a single audio file.

Output: frame-by-frame 5+5 dimensions at 100ms (10fps) resolution.
"""
from __future__ import annotations

import importlib
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

import numpy as np
import torch
from torch import Tensor

# ── Constants ──────────────────────────────────────────────────────────
SAMPLE_RATE = 44100
HOP_LENGTH = 256
N_MELS = 128
N_FFT = 2048
FRAME_RATE = SAMPLE_RATE / HOP_LENGTH  # 172.27 Hz
TARGET_FPS = 10  # 100ms windows

PROJECT_ROOT = Path(__file__).resolve().parent

# Ensure project root is on sys.path
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Also add the app backend for beliefs.py
APP_BACKEND = PROJECT_ROOT / "My Musical Mind (Test-01)" / "backend"
if str(APP_BACKEND) not in sys.path:
    sys.path.insert(0, str(APP_BACKEND))


# ── Audio loading ──────────────────────────────────────────────────────

def load_audio(filepath: str | Path, excerpt_s: float | None = None) -> Tuple[Tensor, Tensor, float]:
    """Load audio file → (waveform, mel, duration_s) using ffmpeg."""
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Audio file not found: {filepath}")

    # Decode to raw PCM via ffmpeg
    cmd = [
        "ffmpeg", "-i", str(filepath),
        "-f", "f32le", "-acodec", "pcm_f32le",
        "-ar", str(SAMPLE_RATE), "-ac", "1",
        "-v", "quiet", "-"
    ]
    result = subprocess.run(cmd, capture_output=True, timeout=60)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {result.stderr.decode()}")

    samples = np.frombuffer(result.stdout, dtype=np.float32)
    waveform = torch.from_numpy(samples.copy()).unsqueeze(0)  # (1, N)

    # Truncate if needed
    if excerpt_s is not None:
        max_samples = int(excerpt_s * SAMPLE_RATE)
        if waveform.shape[-1] > max_samples:
            waveform = waveform[:, :max_samples]

    duration_s = waveform.shape[-1] / SAMPLE_RATE

    # Edge-pad to prevent boundary artifacts
    pad_len = N_FFT // 2
    edge_l = waveform[:, :1].expand(-1, pad_len)
    edge_r = waveform[:, -1:].expand(-1, pad_len)
    waveform_padded = torch.cat([edge_l, waveform, edge_r], dim=-1)

    # Mel spectrogram via torchaudio
    import torchaudio
    mel_transform = torchaudio.transforms.MelSpectrogram(
        sample_rate=SAMPLE_RATE,
        n_fft=N_FFT,
        hop_length=HOP_LENGTH,
        n_mels=N_MELS,
        power=2.0,
    )
    mel = mel_transform(waveform_padded)  # (1, 128, T_padded)

    # Trim padding frames
    pad_frames = pad_len // HOP_LENGTH
    mel = mel[:, :, pad_frames: mel.shape[-1] - pad_frames]

    # Log-normalize
    mel = torch.log1p(mel)
    mel_max = mel.amax(dim=(-2, -1), keepdim=True).clamp(min=1e-8)
    mel = mel / mel_max

    return waveform, mel, duration_s


# ── Mechanism collection ──────────────────────────────────────────────

_FUNCTION_IDS = ("f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9")
_ROLE_TO_DEPTH = {"relay": 0, "encoder": 1, "associator": 2, "integrator": 3, "hub": 4}


def collect_mechanisms() -> List[Any]:
    """Auto-discover all mechanism instances from F1-F9."""
    from Musical_Intelligence.contracts.bases.nucleus import _NucleusBase

    instances: List[Any] = []
    for fn in _FUNCTION_IDS:
        mod_path = f"Musical_Intelligence.brain.functions.{fn}.mechanisms"
        try:
            mod = importlib.import_module(mod_path)
            for name in getattr(mod, "__all__", []):
                cls = getattr(mod, name, None)
                if cls is None:
                    continue
                try:
                    if isinstance(cls, type) and issubclass(cls, _NucleusBase):
                        instances.append(cls())
                except Exception:
                    continue
        except Exception:
            pkg_dir = PROJECT_ROOT / "Musical_Intelligence" / "brain" / "functions" / fn / "mechanisms"
            if not pkg_dir.is_dir():
                continue
            for sub in sorted(pkg_dir.iterdir()):
                if not sub.is_dir() or sub.name.startswith(("_", ".")):
                    continue
                sub_mod_path = f"{mod_path}.{sub.name}"
                try:
                    sub_mod = importlib.import_module(sub_mod_path)
                except Exception:
                    continue
                for attr_name in dir(sub_mod):
                    attr = getattr(sub_mod, attr_name, None)
                    if attr is None:
                        continue
                    try:
                        if (isinstance(attr, type)
                                and issubclass(attr, _NucleusBase)
                                and attr is not _NucleusBase
                                and not attr_name.startswith("_")):
                            instances.append(attr())
                    except Exception:
                        continue
    return instances


def fix_depths(nuclei: List[Any]) -> None:
    for n in nuclei:
        role = getattr(n, "ROLE", "relay")
        min_depth = _ROLE_TO_DEPTH.get(role, 0)
        if n.PROCESSING_DEPTH < min_depth:
            n.PROCESSING_DEPTH = min_depth


# ── Resample to target FPS ────────────────────────────────────────────

def resample_to_fps(data: np.ndarray, native_fps: float, target_fps: float) -> np.ndarray:
    """Resample (T, D) array from native_fps to target_fps using averaging."""
    T, D = data.shape
    window = int(round(native_fps / target_fps))
    if window < 1:
        window = 1
    n_out = T // window
    if n_out == 0:
        return data[:1]
    trimmed = data[:n_out * window]
    return trimmed.reshape(n_out, window, D).mean(axis=1)


# ── Main ──────────────────────────────────────────────────────────────

def main():
    audio_path = (
        PROJECT_ROOT / "Legacy" / "test-classics" / "segments"
        / "Ballade no. 2 - Op. 38__seg019.mp3"
    )

    print(f"[1/7] Loading audio: {audio_path.name}")
    t0 = time.perf_counter()
    waveform, mel, duration_s = load_audio(audio_path)
    n_frames = mel.shape[-1]
    print(f"       Duration: {duration_s:.2f}s, {n_frames} frames @ {FRAME_RATE:.1f} Hz")

    print("[2/7] Initializing mechanisms...")
    nuclei = collect_mechanisms()
    fix_depths(nuclei)
    print(f"       {len(nuclei)} mechanisms loaded")

    # Collect H³ demands
    h3_demand: Set[Tuple[int, int, int, int]] = set()
    for m in nuclei:
        for spec in m.h3_demand:
            h3_demand.add(spec.as_tuple())
    print(f"       {len(h3_demand)} H³ demand tuples")

    print("[3/7] R³ extraction...")
    from Musical_Intelligence.ear.r3 import R3Extractor
    r3_extractor = R3Extractor()
    with torch.no_grad():
        r3_output = r3_extractor.extract(mel, audio=waveform, sr=SAMPLE_RATE)
    r3_features = r3_output.features  # (1, T, 97)
    print(f"       R³: {r3_features.shape}")

    print("[4/7] H³ extraction...")
    from Musical_Intelligence.ear.h3 import H3Extractor
    h3_extractor = H3Extractor()
    with torch.no_grad():
        h3_output = h3_extractor.extract(r3_features, h3_demand)
    print(f"       H³: {h3_output.n_tuples} tuples computed")

    print("[5/7] C³ execution...")
    from Musical_Intelligence.brain.executor import execute
    with torch.no_grad():
        outputs, ram, neuro = execute(nuclei, h3_output.features, r3_features)
    print(f"       C³: {len(outputs)} mechanism outputs")

    # Convert to numpy relay dict
    relays: Dict[str, np.ndarray] = {}
    for nucleus in nuclei:
        if nucleus.NAME in outputs:
            relays[nucleus.NAME] = outputs[nucleus.NAME][0].cpu().numpy()

    print("[6/7] Computing 131 beliefs...")
    from beliefs import compute_beliefs, normalize_beliefs
    beliefs_raw = compute_beliefs(relays, nuclei)  # (T, 131)
    beliefs_131 = normalize_beliefs(beliefs_raw)    # variance recovery
    # Count how many beliefs were actually stretched
    n_stretched = sum(
        1 for i in range(131)
        if (beliefs_raw[:, i].max() - beliefs_raw[:, i].min()) >= 0.01
    )
    print(f"       Beliefs: {beliefs_131.shape} ({n_stretched}/131 normalized)")

    print("[7/7] Computing 5+5 dimensions...")
    from Musical_Intelligence.brain.dimensions import DimensionInterpreter
    dim_interp = DimensionInterpreter()
    dim_result = dim_interp.interpret_numpy(beliefs_131)
    musical_5d = dim_result["musical_5d"]   # (T, 5)
    emotional_5d = dim_result["emotional_5d"]  # (T, 5)
    print(f"       Musical 5D: {musical_5d.shape}, Emotional 5D: {emotional_5d.shape}")

    # Resample to 10fps (100ms)
    musical_10fps = resample_to_fps(musical_5d, FRAME_RATE, TARGET_FPS)
    emotional_10fps = resample_to_fps(emotional_5d, FRAME_RATE, TARGET_FPS)

    elapsed = time.perf_counter() - t0
    print(f"\n=== Done in {elapsed:.1f}s ===")
    print(f"Output: {musical_10fps.shape[0]} frames @ {TARGET_FPS}fps (100ms resolution)")

    # Build JSON output
    from Musical_Intelligence.brain.dimensions.models.musical import MUSICAL_NAMES
    from Musical_Intelligence.brain.dimensions.models.emotional import EMOTIONAL_NAMES

    frames = []
    for i in range(musical_10fps.shape[0]):
        t_sec = i / TARGET_FPS
        frame = {
            "time_s": round(t_sec, 2),
            "musical": {MUSICAL_NAMES[j]: round(float(musical_10fps[i, j]), 4) for j in range(5)},
            "emotional": {EMOTIONAL_NAMES[j]: round(float(emotional_10fps[i, j]), 4) for j in range(5)},
        }
        frames.append(frame)

    output = {
        "file": audio_path.name,
        "duration_s": round(duration_s, 2),
        "fps": TARGET_FPS,
        "n_frames": len(frames),
        "pipeline": "R³(97D)→H³→C³(131 beliefs)→5+5 dimensions",
        "radar_1_musical": {"dims": list(MUSICAL_NAMES), "labels": "Slow↔Fast, Quiet↔Loud, Light↔Heavy, Smooth↔Rough, Thin↔Deep"},
        "radar_2_emotional": {"dims": list(EMOTIONAL_NAMES), "labels": "Sad↔Happy, Chill↔Hyped, Soft↔Hard, Surprising↔Predictable, Dreamy↔Focused"},
        "frames": frames,
    }

    out_path = PROJECT_ROOT / "analysis_5d_result.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to: {out_path}")

    # Print summary stats
    print("\n─── Summary Statistics ───")
    for name, data in [("Musical", musical_10fps), ("Emotional", emotional_10fps)]:
        names = MUSICAL_NAMES if name == "Musical" else EMOTIONAL_NAMES
        print(f"\n{name} 5D:")
        for j, dim_name in enumerate(names):
            col = data[:, j]
            print(f"  {dim_name:16s}  mean={col.mean():.3f}  std={col.std():.3f}  "
                  f"min={col.min():.3f}  max={col.max():.3f}")


if __name__ == "__main__":
    main()
