#!/usr/bin/env python3
"""Run the MI pipeline on an audio file and export WebLab experiment data.

Usage:
    python scripts/run_pipeline.py <audio.wav> --slug <name> [--output <dir>]

Example:
    python scripts/run_pipeline.py ~/Music/swan_lake.wav --slug swan-lake
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import torch

# Ensure project root is on path
_SCRIPT_DIR = Path(__file__).resolve().parent
_WEBLAB_DIR = _SCRIPT_DIR.parent
_PROJECT_ROOT = _WEBLAB_DIR.parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))


def _to_list(t: torch.Tensor) -> list:
    """Convert tensor to nested Python list, rounding to 4 decimals."""
    return np.round(t.detach().cpu().numpy(), 4).tolist()


def run_pipeline(audio_path: str, slug: str, output_dir: Path) -> None:
    exp_dir = output_dir / slug
    exp_dir.mkdir(parents=True, exist_ok=True)
    (exp_dir / "nuclei").mkdir(exist_ok=True)

    print(f"[WebLab] Processing: {audio_path}")
    print(f"[WebLab] Output:     {exp_dir}")

    # ── 1. Load audio ─────────────────────────────────────────
    import torchaudio

    t0 = time.time()
    waveform, sr = torchaudio.load(audio_path)
    if sr != 44100:
        waveform = torchaudio.functional.resample(waveform, sr, 44100)
        sr = 44100
    # Mono
    if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0, keepdim=True)
    duration_s = waveform.shape[-1] / sr
    print(f"  Audio loaded: {duration_s:.1f}s @ {sr}Hz ({time.time()-t0:.1f}s)")

    # Copy audio file
    shutil.copy2(audio_path, exp_dir / "audio.wav")

    # ── 2. Cochlea (mel spectrogram) ──────────────────────────
    t0 = time.time()
    mel_transform = torchaudio.transforms.MelSpectrogram(
        sample_rate=sr, n_fft=2048, hop_length=256, n_mels=128
    )
    mel = mel_transform(waveform)  # (1, 128, T)
    mel = torch.log1p(mel)
    # Normalize to [0, 1]
    mel_min = mel.min()
    mel_range = mel.max() - mel_min
    if mel_range > 0:
        mel = (mel - mel_min) / mel_range
    mel = mel.unsqueeze(0)  # (1, 1, 128, T) → need (B, 128, T) for R3
    mel = mel.squeeze(0)    # (1, 128, T)
    T = mel.shape[-1]
    FRAME_RATE = sr / 256
    print(f"  Mel spectrogram: T={T}, frame_rate={FRAME_RATE:.2f}Hz ({time.time()-t0:.1f}s)")

    # ── 3. R³ extraction ──────────────────────────────────────
    t0 = time.time()
    from Musical_Intelligence.ear.r3 import R3Extractor
    r3_ext = R3Extractor()
    r3_out = r3_ext.extract(mel)
    r3_tensor = r3_out.features  # (1, T, 128)
    print(f"  R³ extracted: {r3_tensor.shape} ({time.time()-t0:.1f}s)")

    # ── 4. Nuclei setup ───────────────────────────────────────
    from Musical_Intelligence.brain.units.spu.relays.bch import BCH
    nuclei = [BCH()]

    # ── 5. H³ extraction ──────────────────────────────────────
    t0 = time.time()
    all_demands = set()
    for n in nuclei:
        for spec in n.h3_demand:
            all_demands.add(spec.as_tuple())

    from Musical_Intelligence.ear.h3 import H3Extractor
    h3_ext = H3Extractor()
    h3_out = h3_ext.extract(r3_tensor, all_demands)
    h3_features = h3_out.features
    print(f"  H³ extracted: {len(h3_features)} tuples ({time.time()-t0:.1f}s)")

    # ── 6. Brain processing ───────────────────────────────────
    t0 = time.time()
    from Musical_Intelligence.brain.orchestrator import BrainOrchestrator
    from Musical_Intelligence.brain.psi_interpreter import PsiInterpreter

    psi = PsiInterpreter()
    orch = BrainOrchestrator(nuclei=nuclei, psi_interpreter=psi)
    brain_out = orch.process(
        r3_features=r3_tensor[:, :, :49],  # Brain sees first 49D
        h3_features=h3_features,
    )
    print(f"  Brain output: tensor={brain_out.tensor.shape}, ram={brain_out.ram.shape}, "
          f"neuro={brain_out.neuro.shape} ({time.time()-t0:.1f}s)")

    # ── 7. Downsample + export ────────────────────────────────
    MAX_LOD_FRAMES = 2000
    stride = max(1, T // MAX_LOD_FRAMES)
    lod_frames = len(range(0, T, stride))

    print(f"  Downsampling: stride={stride}, lod_frames={lod_frames}")

    # R³ (T_lod, 128)
    r3_lod = r3_tensor[0, ::stride, :].detach()
    _write_json(exp_dir / "r3.json", _to_list(r3_lod))

    # RAM (T_lod, 26)
    ram_lod = brain_out.ram[0, ::stride, :].detach()
    _write_json(exp_dir / "ram.json", _to_list(ram_lod))

    # Neuro (T_lod, 4)
    neuro_lod = brain_out.neuro[0, ::stride, :].detach()
    _write_json(exp_dir / "neuro.json", _to_list(neuro_lod))

    # Psi (6 domains)
    psi_export = {
        "affect": _to_list(brain_out.psi.affect[0, ::stride, :]),
        "emotion": _to_list(brain_out.psi.emotion[0, ::stride, :]),
        "aesthetic": _to_list(brain_out.psi.aesthetic[0, ::stride, :]),
        "bodily": _to_list(brain_out.psi.bodily[0, ::stride, :]),
        "cognitive": _to_list(brain_out.psi.cognitive[0, ::stride, :]),
        "temporal": _to_list(brain_out.psi.temporal[0, ::stride, :]),
    }
    _write_json(exp_dir / "psi.json", psi_export)

    # H³ sparse features
    h3_export: dict[str, list] = {}
    for key, tensor in h3_features.items():
        str_key = f"{key[0]}_{key[1]}_{key[2]}_{key[3]}"
        h3_export[str_key] = _to_list(tensor[0, ::stride])
    _write_json(exp_dir / "h3.json", h3_export)

    # Per-nucleus data
    # We need to extract outputs from the orchestrator run
    # Re-run executor to get per-nucleus outputs
    from Musical_Intelligence.brain.executor import execute
    outputs, _, _ = execute(
        nuclei=nuclei,
        h3_features=h3_features,
        r3_features=r3_tensor[:, :, :49],
    )

    for n in nuclei:
        nuc_output = outputs[n.NAME]  # (1, T, dim)
        nuc_lod = nuc_output[0, ::stride, :].detach()

        nuc_data: dict[str, Any] = {
            "name": n.NAME,
            "full_name": n.FULL_NAME,
            "unit": n.UNIT,
            "role": n.ROLE,
            "depth": n.PROCESSING_DEPTH,
            "output_dim": n.OUTPUT_DIM,
            "output": _to_list(nuc_lod),
            "dimension_names": list(n.dimension_names),
            "layers": [
                {
                    "code": layer.code,
                    "name": layer.name,
                    "start": layer.start,
                    "end": layer.end,
                    "scope": layer.scope,
                    "dim_names": list(layer.dim_names),
                }
                for layer in n.LAYERS
            ],
            "region_links": [
                {
                    "dim_name": rl.dim_name,
                    "region": rl.region,
                    "weight": rl.weight,
                    "citation": rl.citation,
                }
                for rl in n.region_links
            ],
            "neuro_links": [
                {
                    "dim_name": nl.dim_name,
                    "channel": nl.channel,
                    "channel_name": nl.channel_name,
                    "effect": nl.effect,
                    "weight": nl.weight,
                    "citation": nl.citation,
                }
                for nl in n.neuro_links
            ],
            "h3_demands": [
                {
                    "r3_idx": d.r3_idx,
                    "r3_name": d.r3_name,
                    "horizon": d.horizon,
                    "horizon_label": d.horizon_label,
                    "morph": d.morph,
                    "morph_name": d.morph_name,
                    "law": d.law,
                    "law_name": d.law_name,
                    "purpose": d.purpose,
                    "citation": d.citation,
                }
                for d in n.h3_demand
            ],
            "metadata": {
                "evidence_tier": n.metadata.evidence_tier,
                "confidence_range": list(n.metadata.confidence_range),
                "version": n.metadata.version,
                "paper_count": n.metadata.effective_paper_count,
                "citations": [
                    {
                        "author": c.author,
                        "year": c.year,
                        "finding": c.finding,
                        "effect_size": c.effect_size,
                    }
                    for c in n.metadata.citations
                ],
                "falsification_criteria": list(n.metadata.falsification_criteria),
            },
        }
        _write_json(exp_dir / "nuclei" / f"{n.NAME}.json", nuc_data)

    # Experiment metadata
    meta: dict[str, Any] = {
        "slug": slug,
        "title": Path(audio_path).stem.replace("_", " ").title(),
        "duration_s": round(duration_s, 3),
        "total_frames": T,
        "lod_frames": lod_frames,
        "lod_stride": stride,
        "frame_rate": round(FRAME_RATE, 6),
        "nuclei": [n.NAME for n in nuclei],
        "r3_dim": 128,
        "created_at": datetime.now().isoformat(),
    }
    _write_json(exp_dir / "meta.json", meta)

    print(f"\n[WebLab] Experiment '{slug}' exported to {exp_dir}")
    print(f"  Files: meta.json, audio.wav, r3.json, ram.json, neuro.json, psi.json, h3.json")
    print(f"  Nuclei: {', '.join(n.NAME for n in nuclei)}")


def _write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, separators=(",", ":")))


def main():
    parser = argparse.ArgumentParser(description="Run MI pipeline → WebLab experiment")
    parser.add_argument("audio", help="Path to audio WAV file")
    parser.add_argument("--slug", required=True, help="Experiment slug (directory name)")
    parser.add_argument("--output", default=str(_WEBLAB_DIR / "experiments"),
                        help="Output directory (default: Lab/WebLab/experiments)")
    args = parser.parse_args()
    run_pipeline(args.audio, args.slug, Path(args.output))


if __name__ == "__main__":
    main()
