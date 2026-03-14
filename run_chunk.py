#!/usr/bin/env python3
"""Process a chunk of audio files through MI pipeline."""
import sys
import json
import time
from pathlib import Path

import numpy as np
import torch

chunk_file = sys.argv[1]
data_dir = sys.argv[2] if len(sys.argv) > 2 else "/workspace/training_data"

with open(chunk_file) as f:
    files = [l.strip() for l in f if l.strip()]

print(f"Chunk {chunk_file}: {len(files)} files", flush=True)

sys.path.insert(0, str(Path(__file__).resolve().parent))

from train_glassbox import (collect_mechanisms, fix_depths, load_audio, SAMPLE_RATE)
from Musical_Intelligence.ear.r3 import R3Extractor
from Musical_Intelligence.ear.h3 import H3Extractor
from Musical_Intelligence.brain.executor import execute
from Musical_Intelligence.brain.beliefs import compute_beliefs
from Musical_Intelligence.brain.dimensions import DimensionInterpreter

nuclei = collect_mechanisms()
fix_depths(nuclei)

h3_demand = set()
for m in nuclei:
    for spec in m.h3_demand:
        h3_demand.add(spec.as_tuple())

with open(Path(data_dir) / "h3_tuple_order.json") as f:
    h3_tuple_order = [tuple(t) for t in json.load(f)]
n_h3 = len(h3_tuple_order)

r3x = R3Extractor()
h3x = H3Extractor()
dim_interp = DimensionInterpreter()

print(f"Ready: {len(nuclei)} mechanisms, {n_h3} H³ demands", flush=True)

t0 = time.perf_counter()
ok = fail = 0

for i, fpath in enumerate(files):
    seg_path = Path(fpath)
    out_file = Path(data_dir) / f"{seg_path.stem}.npz"
    if out_file.exists():
        ok += 1
        continue
    try:
        waveform, mel, dur = load_audio(seg_path)
        with torch.no_grad():
            r3_out = r3x.extract(mel, audio=waveform, sr=SAMPLE_RATE)
            h3_out = h3x.extract(r3_out.features, h3_demand)
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
        np.savez_compressed(
            out_file,
            mel=mel_np.astype(np.float32),
            r3=r3_np.astype(np.float32),
            h3=h3_np,
            beliefs=beliefs.astype(np.float32),
            dims=dims_10,
        )
        ok += 1
    except Exception as e:
        fail += 1
        if fail <= 3:
            print(f"  FAIL: {seg_path.name} — {e}", flush=True)
    if (i + 1) % 50 == 0:
        elapsed = time.perf_counter() - t0
        rate = (i + 1) / elapsed
        print(f"  [{i+1}/{len(files)}] {rate:.1f}/s OK={ok} FAIL={fail}", flush=True)

elapsed = time.perf_counter() - t0
print(f"Done: {ok}/{len(files)} in {elapsed:.0f}s, {fail} failed", flush=True)
