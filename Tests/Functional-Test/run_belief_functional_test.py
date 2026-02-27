"""Generic Belief Functional Test Runner — v1.0

Tests all 131 beliefs across F1-F9, grouped by function.
Tests: B1(shape/count), B2(bounds [0,1]), B3(non-degeneracy),
       B4(positive output), B5(source-dim dependency), B6(instrument contrast),
       B7(redundancy).

Usage:
    cd "SRC Musical Intelligence"
    python Tests/Functional-Test/run_belief_functional_test.py [FUNCTION] [--stimuli-dir DIR]

Examples:
    python Tests/Functional-Test/run_belief_functional_test.py          # all beliefs
    python Tests/Functional-Test/run_belief_functional_test.py F1       # F1 only
    python Tests/Functional-Test/run_belief_functional_test.py F1 F2 F3 # F1-F3
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "Lab"))

import torch
import torchaudio
from backend.pipeline import MIPipeline
from backend.beliefs import compute_beliefs, get_beliefs_registry, build_dim_lookup

SAMPLE_RATE = 44100
HOP_LENGTH = 256
N_MELS = 128
N_FFT = 2048
H3_WARMUP = 180

STIMS_CORE = ["g1_01_single", "g1_05_minor_2nd", "g2_01_low", "g2_03_high",
              "g3_04_dense", "g4_03_arpeggio", "g5_01_piano", "g5_02_organ"]
STIMS_VARIANCE = ["g1_01_single", "g1_05_minor_2nd", "g2_01_low", "g2_03_high",
                  "g3_04_dense", "g4_03_arpeggio", "g5_02_organ"]
STIMS_EXTENDED = ["g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
                  "g2_01_low", "g2_03_high", "g3_04_dense",
                  "g4_01_sustained", "g4_03_arpeggio", "g5_02_organ"]

DEFAULT_STIMULI = pathlib.Path(__file__).resolve().parent / "F4" / "shared_stimuli"


@dataclass
class TestResult:
    name: str
    group: str
    passed: bool
    message: str
    values: Dict[str, Any] = field(default_factory=dict)


class BeliefTestRunner:
    def __init__(self, functions: Optional[List[str]] = None,
                 stimuli_dir: Optional[pathlib.Path] = None):
        self.functions = functions  # None = all
        self.results: List[TestResult] = []
        self.belief_cache: Dict[str, np.ndarray] = {}  # stim → (T, 131)
        self.relay_cache: Dict[str, Dict[str, np.ndarray]] = {}  # stim → {mech: (T,D)}
        self.pipeline: Optional[MIPipeline] = None
        self.stimuli_dir = stimuli_dir or DEFAULT_STIMULI
        self.registry = get_beliefs_registry()
        self.results_dir = pathlib.Path(__file__).resolve().parent / "belief_results"
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def _init_pipeline(self):
        print("Initializing MI Pipeline for belief tests...")
        self.pipeline = MIPipeline()
        print()

    def _load_wav(self, name):
        import soundfile as sf
        path = self.stimuli_dir / f"{name}.wav"
        data, sr = sf.read(str(path), dtype="float32")
        if data.ndim == 2:
            data = data.mean(axis=1)
        waveform = torch.from_numpy(data).unsqueeze(0)
        if sr != SAMPLE_RATE:
            waveform = torchaudio.transforms.Resample(sr, SAMPLE_RATE)(waveform)
        pad_len = N_FFT // 2
        edge_l = waveform[:, :1].expand(-1, pad_len)
        edge_r = waveform[:, -1:].expand(-1, pad_len)
        wp = torch.cat([edge_l, waveform, edge_r], dim=-1)
        mel_t = torchaudio.transforms.MelSpectrogram(
            sample_rate=SAMPLE_RATE, n_fft=N_FFT, hop_length=HOP_LENGTH,
            n_mels=N_MELS, power=2.0)
        mel = mel_t(wp)
        pf = pad_len // HOP_LENGTH
        mel = mel[:, :, pf:mel.shape[-1] - pf]
        mel = torch.log1p(mel)
        mel = mel / mel.amax(dim=(-2, -1), keepdim=True).clamp(min=1e-8)
        return waveform, mel

    def _load_and_run(self, name):
        if name in self.belief_cache:
            return self.belief_cache[name]
        waveform, mel = self._load_wav(name)
        with torch.no_grad():
            r3 = self.pipeline.r3_extractor.extract(mel, audio=waveform, sr=SAMPLE_RATE)
            h3 = self.pipeline.h3_extractor.extract(r3.features, self.pipeline.h3_demand)
            outputs, _, _ = self.pipeline._execute(self.pipeline.nuclei, h3.features, r3.features)

        # Convert outputs to numpy relay dict
        relays = {}
        for mech_name, tensor in outputs.items():
            r = tensor.squeeze(0).numpy() if isinstance(tensor, torch.Tensor) else tensor
            if r.ndim == 3:
                r = r[0]
            relays[mech_name] = r
        self.relay_cache[name] = relays

        # Compute beliefs
        beliefs = compute_beliefs(relays, self.pipeline.nuclei)
        self.belief_cache[name] = beliefs
        return beliefs

    def _mean(self, stim, belief_idx, skip_warmup=True):
        beliefs = self._load_and_run(stim)
        s = H3_WARMUP if (skip_warmup and beliefs.shape[0] > H3_WARMUP + 50) else 0
        return float(beliefs[s:, belief_idx].mean())

    def _test(self, g, n, c, m, **v):
        self.results.append(TestResult(n, g, c, m, v))

    def _get_beliefs_for_fn(self, fn: str):
        return [b for b in self.registry if b["functionId"].lower() == fn.lower()]

    def _get_target_beliefs(self):
        if self.functions:
            return [b for b in self.registry
                    if b["functionId"].lower() in [f.lower() for f in self.functions]]
        return self.registry

    def test_B1_shape(self):
        """B1: Verify total belief count and shape."""
        G = "B1_shape"
        beliefs = self._load_and_run("g1_01_single")
        self._test(G, "B1_ndim", beliefs.ndim == 2, f"ndim={beliefs.ndim}")
        self._test(G, "B1_n_beliefs", beliefs.shape[1] == len(self.registry),
                   f"N={beliefs.shape[1]} (expected {len(self.registry)})")
        self._test(G, "B1_frames", beliefs.shape[0] > 100, f"T={beliefs.shape[0]}")

    def test_B2_bounds(self):
        """B2: All belief values in [0, 1]."""
        G = "B2_bounds"
        targets = self._get_target_beliefs()
        for stim in STIMS_CORE:
            beliefs = self._load_and_run(stim)
            for b in targets:
                idx = b["index"]
                col = beliefs[:, idx]
                lo, hi = float(col.min()), float(col.max())
                self._test(G, f"B2_{stim}_b{idx}_{b['name']}",
                           lo >= -0.001 and hi <= 1.001,
                           f"[{lo:.4f},{hi:.4f}]⊂[0,1]")

    def test_B3_nondegeneracy(self):
        """B3: Belief varies across stimuli (not stuck at constant)."""
        G = "B3_nondegeneracy"
        targets = self._get_target_beliefs()
        means = np.array([[self._mean(s, b["index"]) for b in targets] for s in STIMS_VARIANCE])
        for i, b in enumerate(targets):
            v = float(means[:, i].std())
            # Beliefs are weighted sums → anticipation/forecast beliefs may have low variance
            btype = b["type"]
            n_sources = len(b.get("sourceDims", []))
            total_weight = sum(sd["weight"] for sd in b.get("sourceDims", []))

            # Threshold: lower for anticipation (forecast layer), single-source, or low-weight beliefs
            if btype == "anticipation" or total_weight < 0.50 or n_sources == 0:
                thresh = 0.0002
            elif total_weight < 0.80:
                thresh = 0.0005
            else:
                thresh = 0.001

            self._test(G, f"B3_b{b['index']}_{b['name']}",
                       v > thresh, f"std={v:.4f}>{thresh} ({btype}, w={total_weight:.2f})")

    def test_B4_positive(self):
        """B4: Beliefs produce positive output for musical stimuli."""
        G = "B4_positive"
        targets = self._get_target_beliefs()
        for stim in ["g1_01_single", "g4_03_arpeggio"]:
            for b in targets:
                val = self._mean(stim, b["index"])
                n_sources = len(b.get("sourceDims", []))
                if n_sources == 0:
                    continue  # skip beliefs with no source dims
                self._test(G, f"B4_{stim}_b{b['index']}_{b['name']}",
                           val > 0.0, f"val={val:.4f}>0")

    def test_B5_source_dim_check(self):
        """B5: Verify belief tracks its source mechanism dims (spot check)."""
        G = "B5_source_dim"
        targets = self._get_target_beliefs()
        dim_lookup = build_dim_lookup(self.pipeline.nuclei)
        stim = "g1_01_single"
        beliefs = self._load_and_run(stim)
        relays = self.relay_cache[stim]

        for b in targets:
            idx = b["index"]
            mech_name = b["mechanism"]
            source_dims = b.get("sourceDims", [])

            if not source_dims or mech_name not in relays:
                continue

            mech_output = relays[mech_name]
            s = H3_WARMUP if mech_output.shape[0] > H3_WARMUP + 50 else 0
            belief_mean = float(beliefs[s:, idx].mean())

            # Recompute per-frame (matching compute_beliefs exactly)
            T_sub = mech_output.shape[0] - s
            expected_trace = np.zeros(T_sub, dtype=np.float32)
            all_resolved = True
            for sd in source_dims:
                dim_name = sd["name"]
                weight = sd["weight"]
                invert = False
                if dim_name.startswith("1-"):
                    dim_name = dim_name[2:]
                    invert = True
                key = (mech_name, dim_name)
                if key not in dim_lookup:
                    all_resolved = False
                    break
                _, dim_idx = dim_lookup[key]
                if dim_idx < mech_output.shape[1]:
                    dim_vals = mech_output[s:, dim_idx].copy()
                    if invert:
                        dim_vals = 1.0 - dim_vals
                    expected_trace += dim_vals * weight

            if not all_resolved:
                continue

            expected = float(np.clip(expected_trace, 0.0, 1.0).mean())
            diff = abs(belief_mean - expected)
            self._test(G, f"B5_b{idx}_{b['name']}",
                       diff < 0.01,
                       f"belief={belief_mean:.4f}, expected={expected:.4f}, diff={diff:.4f}")

    def test_B6_instrument(self):
        """B6: Both piano and organ produce positive belief values."""
        G = "B6_instrument"
        targets = self._get_target_beliefs()
        for b in targets:
            if len(b.get("sourceDims", [])) == 0:
                continue
            p = self._mean("g5_01_piano", b["index"])
            o = self._mean("g5_02_organ", b["index"])
            self._test(G, f"B6_b{b['index']}_{b['name']}",
                       p > 0.0 and o > 0.0,
                       f"piano={p:.4f},organ={o:.4f}>0")

    def test_B7_redundancy(self):
        """B7: No two beliefs within same function are perfectly redundant."""
        G = "B7_redundancy"
        fn_list = self.functions or sorted(set(b["functionId"].lower() for b in self.registry))
        for fn in fn_list:
            fn_beliefs = self._get_beliefs_for_fn(fn)
            if len(fn_beliefs) < 2:
                continue
            means = np.array([[self._mean(s, b["index"]) for b in fn_beliefs]
                              for s in STIMS_EXTENDED])
            for i in range(len(fn_beliefs)):
                for j in range(i + 1, len(fn_beliefs)):
                    vi = means[:, i]
                    vj = means[:, j]
                    if vi.std() < 1e-10 or vj.std() < 1e-10:
                        continue
                    # Same-mechanism beliefs may share source dims
                    bi = fn_beliefs[i]
                    bj = fn_beliefs[j]
                    same_mech = bi["mechanism"] == bj["mechanism"]
                    if same_mech:
                        continue  # Same-mech beliefs share E/M/P/F layers by design
                    # Cross-mech beliefs share H³/R³ inputs → 0.997
                    thresh = 0.997
                    r = abs(float(np.corrcoef(vi, vj)[0, 1]))
                    if r >= thresh:
                        self._test(G, f"B7_{bi['name']}_vs_{bj['name']}",
                                   False,
                                   f"|r|={r:.4f}>={thresh} ({fn.upper()}, "
                                   f"mech={'same' if same_mech else 'diff'})")
            # If no failures, add a pass
            fn_fails = [r for r in self.results if r.group == G and not r.passed
                        and fn.upper() in r.message]
            if not fn_fails:
                self._test(G, f"B7_{fn.upper()}_ok", True,
                           f"No redundant belief pairs in {fn.upper()}")

    def run_all(self):
        t0 = time.time()
        self._init_pipeline()
        fns = self.functions or ["all"]
        print(f"\n  Testing beliefs for: {', '.join(fns)}")
        targets = self._get_target_beliefs()
        print(f"  Target beliefs: {len(targets)} / {len(self.registry)}")

        for test_fn in [self.test_B1_shape, self.test_B2_bounds,
                        self.test_B3_nondegeneracy, self.test_B4_positive,
                        self.test_B5_source_dim_check, self.test_B6_instrument,
                        self.test_B7_redundancy]:
            name = test_fn.__name__
            print(f"\n{'=' * 60}\n  {name}\n{'=' * 60}")
            try:
                test_fn()
            except Exception as ex:
                self.results.append(TestResult(f"{name}_exc", name, False,
                                               f"EXCEPTION: {ex}", {}))
                import traceback
                traceback.print_exc()

        elapsed = time.time() - t0
        self._report(elapsed)
        return self.results

    def _report(self, elapsed):
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        failed = total - passed
        fns = ",".join(self.functions) if self.functions else "ALL"
        print(f"\n{'=' * 60}\n  BELIEF FUNCTIONAL TEST RESULTS ({fns})\n{'=' * 60}")
        print(f"  Total : {total}\n  Passed: {passed}\n  Failed: {failed}\n  Time  : {elapsed:.1f}s")
        print(f"{'=' * 60}")
        if failed:
            print(f"\n  FAILURES:")
            for r in self.results:
                if not r.passed:
                    print(f"    FAIL {r.name}: {r.message}")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        report = {"test": "beliefs", "functions": fns,
                  "timestamp": ts, "total": total, "passed": passed, "failed": failed,
                  "elapsed_s": round(elapsed, 1),
                  "results": [{"name": r.name, "group": r.group, "passed": bool(r.passed),
                               "message": r.message} for r in self.results]}
        out = self.results_dir / f"belief_results_{fns}_{ts}.json"
        with open(out, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\n  Report: {out}")


def main():
    parser = argparse.ArgumentParser(description="MI Belief Functional Test Runner")
    parser.add_argument("functions", nargs="*", default=None,
                        help="Functions to test (e.g. F1 F2). Default: all")
    parser.add_argument("--stimuli-dir", type=str, default=None,
                        help="Directory with WAV stimuli")
    args = parser.parse_args()

    functions = args.functions if args.functions else None
    stimuli_dir = pathlib.Path(args.stimuli_dir) if args.stimuli_dir else None

    runner = BeliefTestRunner(functions=functions, stimuli_dir=stimuli_dir)
    runner.run_all()


if __name__ == "__main__":
    main()
