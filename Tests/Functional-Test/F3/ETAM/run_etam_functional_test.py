"""ETAM Functional Test — v1.0
Tests ETAM 11D: E0-E3, M0-M1, P0-P1, F0-F2.
Entrainment, Tempo and Attention Modulation. Encoder depth 1, cross-reads HMCE.
"""
from __future__ import annotations
import json, pathlib, sys, time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "Lab"))
import torch, torchaudio
from backend.pipeline import MIPipeline

STIMULI_DIR = pathlib.Path(__file__).resolve().parent / "stimuli"
RESULTS_DIR = pathlib.Path(__file__).resolve().parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)
SAMPLE_RATE = 44100; HOP_LENGTH = 256; N_MELS = 128; N_FFT = 2048; H3_WARMUP = 180

E0=0;E1=1;E2=2;E3=3;M0=4;M1=5;P0=6;P1=7;F0=8;F1=9;F2=10
DIM_NAMES = ["E0:early_window","E1:middle_window","E2:late_window","E3:instrument_asymm",
    "M0:attention_gain","M1:entrainment_idx","P0:envelope_tracking","P1:stream_separation",
    "F0:tracking_pred","F1:attention_sustain","F2:segregation_pred"]
OUTPUT_DIM = 11

@dataclass
class TestResult:
    name: str; group: str; passed: bool; message: str; values: Dict[str,Any] = field(default_factory=dict)

class ETAMTestRunner:
    def __init__(self):
        self.results: List[TestResult] = []; self.relay_cache: Dict[str,np.ndarray] = {}; self.pipeline = None
    def _init_pipeline(self):
        print("Initializing MI Pipeline..."); self.pipeline = MIPipeline(); print()
    def _load_wav(self, name):
        import soundfile as sf
        data, sr = sf.read(str(STIMULI_DIR/f"{name}.wav"), dtype="float32")
        if data.ndim == 2: data = data.mean(axis=1)
        waveform = torch.from_numpy(data).unsqueeze(0)
        if sr != SAMPLE_RATE: waveform = torchaudio.transforms.Resample(sr, SAMPLE_RATE)(waveform)
        pad = N_FFT//2
        wp = torch.cat([waveform[:,:1].expand(-1,pad), waveform, waveform[:,-1:].expand(-1,pad)], dim=-1)
        mel = torchaudio.transforms.MelSpectrogram(sample_rate=SAMPLE_RATE, n_fft=N_FFT, hop_length=HOP_LENGTH, n_mels=N_MELS, power=2.0)(wp)
        pf = pad//HOP_LENGTH; mel = mel[:,:,pf:mel.shape[-1]-pf]
        mel = torch.log1p(mel); mel = mel/mel.amax(dim=(-2,-1),keepdim=True).clamp(min=1e-8)
        return waveform, mel
    def _load_and_run(self, name):
        if name in self.relay_cache: return self.relay_cache[name]
        waveform, mel = self._load_wav(name)
        with torch.no_grad():
            r3 = self.pipeline.r3_extractor.extract(mel, audio=waveform, sr=SAMPLE_RATE)
            h3 = self.pipeline.h3_extractor.extract(r3.features, self.pipeline.h3_demand)
            outputs, _, _ = self.pipeline._execute(self.pipeline.nuclei, h3.features, r3.features)
        relay = outputs.get("ETAM")
        if relay is None: raise RuntimeError(f"ETAM not found for '{name}'")
        r = relay.squeeze(0).numpy() if isinstance(relay, torch.Tensor) else relay
        if r.ndim == 3: r = r[0]
        self.relay_cache[name] = r; return r
    def _mean(self, name, dim, skip_warmup=True):
        r = self._load_and_run(name); s = H3_WARMUP if (skip_warmup and r.shape[0]>H3_WARMUP+50) else 0
        return float(r[s:,dim].mean())
    def _test(self, g, n, c, m, **v): self.results.append(TestResult(n, g, c, m, v))

    def test_T1_dimensionality(self):
        G="T1"; r=self._load_and_run("g1_01_single")
        self._test(G,"T1_ndim",r.ndim==2,f"ndim={r.ndim}")
        self._test(G,"T1_dim",r.shape[1]==OUTPUT_DIM,f"D={r.shape[1]}")
        self._test(G,"T1_frames",r.shape[0]>100,f"T={r.shape[0]}")
    def test_T2_bounds(self):
        G="T2"
        for s in ["g1_01_single","g1_05_minor_2nd","g2_01_low","g2_03_high","g3_04_dense","g4_03_arpeggio","g5_01_piano","g5_02_organ"]:
            r=self._load_and_run(s); lo,hi=float(r.min()),float(r.max())
            self._test(G,f"T2_{s}",lo>=-0.001 and hi<=1.001,f"[{lo:.4f},{hi:.4f}]⊂[0,1]")
    def test_T3_nondegeneracy(self):
        G="T3"
        stims=["g1_01_single","g1_05_minor_2nd","g2_01_low","g2_03_high","g3_04_dense","g4_03_arpeggio","g5_02_organ"]
        means=np.array([[self._mean(s,d) for d in range(OUTPUT_DIM)] for s in stims])
        for d in range(OUTPUT_DIM):
            v=float(means[:,d].std()); thresh=0.0003 if d in (F0,F1,F2) else 0.001
            self._test(G,f"T3_{DIM_NAMES[d]}",v>thresh,f"std={v:.4f}>{thresh}")
    def test_T4_windows(self):
        G="T4"
        for s in ["g1_01_single","g4_02_melody","g4_03_arpeggio"]:
            for d,nm in [(E0,"E0"),(E1,"E1"),(E2,"E2"),(E3,"E3")]:
                v=self._mean(s,d); self._test(G,f"T4_{nm}_{s}",v>0.0,f"{nm}({v:.4f})>0")
    def test_T5_m_layer(self):
        G="T5"
        stims=["g1_01_single","g1_05_minor_2nd","g3_04_dense","g4_01_sustained","g4_03_arpeggio"]
        for s in stims:
            m0=self._mean(s,M0); m1=self._mean(s,M1)
            self._test(G,f"T5_M0_bounded_{s}",0.0<=m0<=1.0,f"M0({m0:.4f})")
            self._test(G,f"T5_M1_bounded_{s}",0.0<=m1<=1.0,f"M1({m1:.4f})")
    def test_T6_p_layer(self):
        G="T6"
        for s in ["g1_01_single","g1_05_minor_2nd","g3_04_dense","g4_01_sustained","g4_03_arpeggio"]:
            for d,nm in [(P0,"P0"),(P1,"P1")]:
                v=self._mean(s,d); self._test(G,f"T6_{nm}_{s}",v>0.0,f"{nm}({v:.4f})>0")
    def test_T7_forecast(self):
        G="T7"
        stims=["g1_01_single","g1_03_fifth","g1_05_minor_2nd","g2_01_low","g2_03_high","g3_04_dense","g4_01_sustained","g4_03_arpeggio"]
        e0s=np.array([self._mean(s,E0) for s in stims]); f0s=np.array([self._mean(s,F0) for s in stims])
        r=float(np.corrcoef(e0s,f0s)[0,1])
        self._test(G,"T7_F0_E0_corr",abs(r)>0.10,f"|r(F0,E0)|={abs(r):.4f}>0.10 (E0 feeds F0 at 50%)")
    def test_T8_instrument(self):
        G="T8"
        for d in range(OUTPUT_DIM):
            p=self._mean("g5_01_piano",d); o=self._mean("g5_02_organ",d)
            self._test(G,f"T8_{DIM_NAMES[d]}",p>0.0 and o>0.0,f"piano={p:.4f},organ={o:.4f}>0")
    def test_T9_redundancy(self):
        G="T9"
        COUPLED={
            (0,4),(1,4),(2,4),(0,6),(2,7),(3,7),(3,10),(2,10),
            (4,6),(4,9),(5,8),(0,8),(0,9),(1,6),(1,9),
            (6,8),(6,9),(7,10),
        }
        stims=["g1_01_single","g1_03_fifth","g1_05_minor_2nd","g2_01_low","g2_03_high","g3_04_dense","g4_01_sustained","g4_03_arpeggio","g5_02_organ"]
        means=np.array([[self._mean(s,d) for d in range(OUTPUT_DIM)] for s in stims])
        for i in range(OUTPUT_DIM):
            for j in range(i+1,OUTPUT_DIM):
                if (i,j) in COUPLED: continue
                r=abs(float(np.corrcoef(means[:,i],means[:,j])[0,1]))
                self._test(G,f"T9_{i}_{j}",r<0.99,f"|r({DIM_NAMES[i]},{DIM_NAMES[j]})|={r:.3f}<0.99")
    def run_all(self):
        t0=time.time(); self._init_pipeline()
        for t in [self.test_T1_dimensionality,self.test_T2_bounds,self.test_T3_nondegeneracy,
                  self.test_T4_windows,self.test_T5_m_layer,self.test_T6_p_layer,
                  self.test_T7_forecast,self.test_T8_instrument,self.test_T9_redundancy]:
            nm=t.__name__; print(f"\n{'='*60}\n  {nm}\n{'='*60}")
            try: t()
            except Exception as ex: self.results.append(TestResult(f"{nm}_exc",nm,False,f"EXCEPTION: {ex}",{})); import traceback; traceback.print_exc()
        self._report(time.time()-t0)
    def _report(self, elapsed):
        passed=sum(1 for r in self.results if r.passed); total=len(self.results); failed=total-passed
        print(f"\n{'='*60}\n  ETAM FUNCTIONAL TEST RESULTS\n{'='*60}")
        print(f"  Total : {total}\n  Passed: {passed}\n  Failed: {failed}\n  Time  : {elapsed:.1f}s\n{'='*60}")
        if failed:
            print(f"\n  FAILURES:")
            for r in self.results:
                if not r.passed: print(f"    FAIL {r.name}: {r.message}")
        ts=datetime.now().strftime("%Y%m%d_%H%M%S")
        out=RESULTS_DIR/f"etam_results_{ts}.json"
        with open(out,"w") as f: json.dump({"mechanism":"ETAM","function":"F3","timestamp":ts,"total":total,"passed":passed,"failed":failed,"elapsed_s":round(elapsed,1),"results":[{"name":r.name,"group":r.group,"passed":r.passed,"message":r.message,"values":r.values} for r in self.results]},f,indent=2)
        print(f"\n  Report: {out}")

if __name__=="__main__": ETAMTestRunner().run_all()
