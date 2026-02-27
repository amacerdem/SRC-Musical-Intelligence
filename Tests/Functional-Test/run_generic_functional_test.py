"""Generic Functional Test Runner — v1.0

Runs a standard functional test battery for any MI mechanism.
Tests: T1(dimensionality), T2(bounds), T3(non-degeneracy), T4(positive output),
       T5(M/P layer bounded), T6(forecast correlation), T7(instrument contrast),
       T8(redundancy).

Usage:
    cd "SRC Musical Intelligence"
    python Tests/Functional-Test/run_generic_functional_test.py MECHANISM_NAME OUTPUT_DIM [FUNCTION]

Example:
    python Tests/Functional-Test/run_generic_functional_test.py MEAMN 12 F4
"""
from __future__ import annotations

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

SAMPLE_RATE = 44100
HOP_LENGTH = 256
N_MELS = 128
N_FFT = 2048
H3_WARMUP = 180

STIMS_CORE = ["g1_01_single", "g1_05_minor_2nd", "g2_01_low", "g2_03_high",
              "g3_04_dense", "g4_03_arpeggio", "g5_01_piano", "g5_02_organ"]
STIMS_EXTENDED = ["g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
                  "g2_01_low", "g2_03_high", "g3_04_dense",
                  "g4_01_sustained", "g4_03_arpeggio", "g5_02_organ"]
STIMS_VARIANCE = ["g1_01_single", "g1_05_minor_2nd", "g2_01_low", "g2_03_high",
                  "g3_04_dense", "g4_03_arpeggio", "g5_02_organ"]


@dataclass
class TestResult:
    name: str
    group: str
    passed: bool
    message: str
    values: Dict[str, Any] = field(default_factory=dict)


class GenericTestRunner:
    def __init__(self, mech_name: str, output_dim: int, function: str = "F?",
                 stimuli_dir: Optional[pathlib.Path] = None,
                 results_dir: Optional[pathlib.Path] = None,
                 tanh_dims: Optional[Set[int]] = None,
                 low_var_dims: Optional[Set[int]] = None,
                 dead_dims: Optional[Set[int]] = None,
                 coupled: Optional[Set[Tuple[int, int]]] = None):
        self.mech_name = mech_name
        self.output_dim = output_dim
        self.function = function
        self.results: List[TestResult] = []
        self.relay_cache: Dict[str, np.ndarray] = {}
        self.pipeline: MIPipeline = None
        self.tanh_dims = tanh_dims or set()
        self.low_var_dims = low_var_dims or set()
        self.dead_dims = dead_dims or set()
        self.coupled = coupled or set()

        if stimuli_dir:
            self.stimuli_dir = stimuli_dir
        else:
            self.stimuli_dir = pathlib.Path(__file__).resolve().parent / function / mech_name / "stimuli"

        if results_dir:
            self.results_dir = results_dir
        else:
            self.results_dir = pathlib.Path(__file__).resolve().parent / function / mech_name / "results"
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def _init_pipeline(self):
        print(f"Initializing MI Pipeline for {self.mech_name} ({self.output_dim}D)...")
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
        if name in self.relay_cache:
            return self.relay_cache[name]
        waveform, mel = self._load_wav(name)
        with torch.no_grad():
            r3 = self.pipeline.r3_extractor.extract(mel, audio=waveform, sr=SAMPLE_RATE)
            h3 = self.pipeline.h3_extractor.extract(r3.features, self.pipeline.h3_demand)
            outputs, _, _ = self.pipeline._execute(self.pipeline.nuclei, h3.features, r3.features)
        relay = outputs.get(self.mech_name)
        if relay is None:
            raise RuntimeError(f"{self.mech_name} not found in pipeline outputs")
        r = relay.squeeze(0).numpy() if isinstance(relay, torch.Tensor) else relay
        if r.ndim == 3:
            r = r[0]
        self.relay_cache[name] = r
        return r

    def _mean(self, name, dim, skip_warmup=True):
        r = self._load_and_run(name)
        s = H3_WARMUP if (skip_warmup and r.shape[0] > H3_WARMUP + 50) else 0
        return float(r[s:, dim].mean())

    def _test(self, g, n, c, m, **v):
        self.results.append(TestResult(n, g, c, m, v))

    def test_T1_dimensionality(self):
        G = "T1_dimensionality"
        r = self._load_and_run("g1_01_single")
        self._test(G, "T1_ndim", r.ndim == 2, f"ndim={r.ndim}")
        self._test(G, "T1_dim_count", r.shape[1] == self.output_dim, f"D={r.shape[1]}")
        self._test(G, "T1_frames", r.shape[0] > 100, f"T={r.shape[0]}")

    def test_T2_bounds(self):
        G = "T2_bounds"
        for stim in STIMS_CORE:
            r = self._load_and_run(stim)
            for d in range(self.output_dim):
                col = r[:, d]
                lo, hi = float(col.min()), float(col.max())
                if d in self.tanh_dims:
                    self._test(G, f"T2_{stim}_d{d}", lo >= -1.001 and hi <= 1.001,
                               f"d{d}[{lo:.4f},{hi:.4f}]⊂[-1,1]")
                else:
                    self._test(G, f"T2_{stim}_d{d}", lo >= -0.001 and hi <= 1.001,
                               f"d{d}[{lo:.4f},{hi:.4f}]⊂[0,1]")

    def test_T3_nondegeneracy(self):
        G = "T3_nondegeneracy"
        means = np.array([[self._mean(s, d) for d in range(self.output_dim)] for s in STIMS_VARIANCE])
        for d in range(self.output_dim):
            if d in self.dead_dims:
                self._test(G, f"T3_d{d}", True, f"SKIP (dead/reserved dim)")
                continue
            v = float(means[:, d].std())
            thresh = 0.0003 if d in self.low_var_dims else 0.001
            self._test(G, f"T3_d{d}", v > thresh, f"std={v:.4f}>{thresh}")

    def test_T4_positive(self):
        G = "T4_positive"
        for stim in ["g1_01_single", "g4_02_melody", "g4_03_arpeggio"]:
            for d in range(min(3, self.output_dim)):
                val = self._mean(stim, d)
                if d in self.tanh_dims:
                    self._test(G, f"T4_d{d}_{stim}", -1.0 <= val <= 1.0,
                               f"d{d}({val:.4f})∈[-1,1]")
                else:
                    self._test(G, f"T4_d{d}_{stim}", val > 0.0,
                               f"d{d}({val:.4f})>0")

    def test_T5_instrument(self):
        G = "T5_instrument"
        for d in range(self.output_dim):
            if d in self.dead_dims:
                self._test(G, f"T5_d{d}", True, f"SKIP (dead/reserved dim)")
                continue
            p = self._mean("g5_01_piano", d)
            o = self._mean("g5_02_organ", d)
            if d in self.tanh_dims:
                self._test(G, f"T5_d{d}", -1.0 <= p <= 1.0 and -1.0 <= o <= 1.0,
                           f"piano={p:.4f},organ={o:.4f}∈[-1,1]")
            else:
                self._test(G, f"T5_d{d}", p > 0.0 and o > 0.0,
                           f"piano={p:.4f},organ={o:.4f}>0")

    def test_T6_redundancy(self):
        G = "T6_redundancy"
        means = np.array([[self._mean(s, d) for d in range(self.output_dim)] for s in STIMS_EXTENDED])
        n_fail = 0
        for i in range(self.output_dim):
            for j in range(i + 1, self.output_dim):
                if (i, j) in self.coupled or (j, i) in self.coupled:
                    continue
                if i in self.dead_dims or j in self.dead_dims:
                    continue
                vi = means[:, i]
                vj = means[:, j]
                if vi.std() < 1e-10 or vj.std() < 1e-10:
                    continue
                r = abs(float(np.corrcoef(vi, vj)[0, 1]))
                if r >= 0.99:
                    n_fail += 1
                    self._test(G, f"T6_{i}_{j}", False,
                               f"|r(d{i},d{j})|={r:.3f}>=0.99 (COUPLED?)")
        if n_fail == 0:
            self._test(G, "T6_all_unique", True, "No redundant pairs found")

    def run_all(self):
        t0 = time.time()
        self._init_pipeline()
        for t in [self.test_T1_dimensionality, self.test_T2_bounds,
                  self.test_T3_nondegeneracy, self.test_T4_positive,
                  self.test_T5_instrument, self.test_T6_redundancy]:
            name = t.__name__
            print(f"\n{'=' * 60}\n  {name}\n{'=' * 60}")
            try:
                t()
            except Exception as ex:
                self.results.append(TestResult(f"{name}_exc", name, False, f"EXCEPTION: {ex}", {}))
                import traceback; traceback.print_exc()
        elapsed = time.time() - t0
        self._report(elapsed)
        return self.results

    def _report(self, elapsed):
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        failed = total - passed
        print(f"\n{'=' * 60}\n  {self.mech_name} FUNCTIONAL TEST RESULTS\n{'=' * 60}")
        print(f"  Total : {total}\n  Passed: {passed}\n  Failed: {failed}\n  Time  : {elapsed:.1f}s")
        print(f"{'=' * 60}")
        if failed:
            print(f"\n  FAILURES:")
            for r in self.results:
                if not r.passed:
                    print(f"    FAIL {r.name}: {r.message}")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        report = {"mechanism": self.mech_name, "function": self.function,
                  "timestamp": ts, "total": total, "passed": passed, "failed": failed,
                  "elapsed_s": round(elapsed, 1),
                  "results": [{"name": r.name, "group": r.group, "passed": r.passed,
                               "message": r.message, "values": r.values} for r in self.results]}
        out = self.results_dir / f"{self.mech_name.lower()}_results_{ts}.json"
        with open(out, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\n  Report: {out}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generic MI Mechanism Functional Test")
    parser.add_argument("mech_name", help="Mechanism name (e.g. MEAMN)")
    parser.add_argument("output_dim", type=int, help="Output dimensionality")
    parser.add_argument("function", nargs="?", default="F?", help="Function (e.g. F4)")
    parser.add_argument("--stimuli-dir", type=str, default=None, help="Shared stimuli directory")
    parser.add_argument("--tanh-dims", type=str, default=None, help="Comma-separated tanh dim indices")
    parser.add_argument("--low-var-dims", type=str, default=None, help="Comma-separated low-var dim indices (default: last 25%%)")
    parser.add_argument("--dead-dims", type=str, default=None, help="Comma-separated dead/reserved dim indices (skipped in T3/T5/T6)")
    parser.add_argument("--coupled", type=str, default=None, help="Coupled pairs: i-j,k-l (exempt from T6 redundancy)")
    args = parser.parse_args()

    if args.low_var_dims is not None:
        low_var_dims = set(int(x) for x in args.low_var_dims.split(",") if x.strip())
    else:
        forecast_start = int(args.output_dim * 0.75)
        low_var_dims = set(range(forecast_start, args.output_dim))

    tanh_dims = set()
    if args.tanh_dims:
        tanh_dims = set(int(x) for x in args.tanh_dims.split(",") if x.strip())

    dead_dims = set()
    if args.dead_dims:
        dead_dims = set(int(x) for x in args.dead_dims.split(",") if x.strip())

    coupled = set()
    if args.coupled:
        for pair in args.coupled.split(","):
            parts = pair.strip().split("-")
            if len(parts) == 2:
                coupled.add((int(parts[0]), int(parts[1])))

    stimuli_dir = pathlib.Path(args.stimuli_dir) if args.stimuli_dir else None

    runner = GenericTestRunner(
        mech_name=args.mech_name,
        output_dim=args.output_dim,
        function=args.function,
        stimuli_dir=stimuli_dir,
        low_var_dims=low_var_dims,
        tanh_dims=tanh_dims,
        dead_dims=dead_dims,
        coupled=coupled,
    )
    runner.run_all()


if __name__ == "__main__":
    main()
