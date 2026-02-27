"""DGTP Functional Test — v1.0
Tests DGTP 9D: E0-E2, M0-M1, P0-P1, F0-F1.
Domain-General Temporal Processing. Associator depth 2, reads BARM, SNEM.
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
SAMPLE_RATE=44100;HOP_LENGTH=256;N_MELS=128;N_FFT=2048;H3_WARMUP=180
E0=0;E1=1;E2=2;M0=3;M1=4;P0=5;P1=6;F0=7;F1=8
DIM_NAMES=["E0:music_timing","E1:speech_timing","E2:shared_mech",
    "M0:domain_corr","M1:shared_var","P0:music_beat","P1:domain_general",
    "F0:cross_domain","F1:training_transfer"]
OUTPUT_DIM=9
@dataclass
class TestResult:
    name:str;group:str;passed:bool;message:str;values:Dict[str,Any]=field(default_factory=dict)
class DGTPTestRunner:
    def __init__(self):
        self.results:List[TestResult]=[];self.relay_cache:Dict[str,np.ndarray]={};self.pipeline=None
    def _init_pipeline(self):
        print("Initializing MI Pipeline...");self.pipeline=MIPipeline();print()
    def _load_wav(self,name):
        import soundfile as sf
        data,sr=sf.read(str(STIMULI_DIR/f"{name}.wav"),dtype="float32")
        if data.ndim==2:data=data.mean(axis=1)
        w=torch.from_numpy(data).unsqueeze(0)
        if sr!=SAMPLE_RATE:w=torchaudio.transforms.Resample(sr,SAMPLE_RATE)(w)
        p=N_FFT//2;wp=torch.cat([w[:,:1].expand(-1,p),w,w[:,-1:].expand(-1,p)],dim=-1)
        mel=torchaudio.transforms.MelSpectrogram(sample_rate=SAMPLE_RATE,n_fft=N_FFT,hop_length=HOP_LENGTH,n_mels=N_MELS,power=2.0)(wp)
        pf=p//HOP_LENGTH;mel=mel[:,:,pf:mel.shape[-1]-pf];mel=torch.log1p(mel);mel=mel/mel.amax(dim=(-2,-1),keepdim=True).clamp(min=1e-8)
        return w,mel
    def _load_and_run(self,name):
        if name in self.relay_cache:return self.relay_cache[name]
        w,mel=self._load_wav(name)
        with torch.no_grad():
            r3=self.pipeline.r3_extractor.extract(mel,audio=w,sr=SAMPLE_RATE)
            h3=self.pipeline.h3_extractor.extract(r3.features,self.pipeline.h3_demand)
            o,_,_=self.pipeline._execute(self.pipeline.nuclei,h3.features,r3.features)
        relay=o.get("DGTP")
        if relay is None:raise RuntimeError(f"DGTP not found for '{name}'")
        r=relay.squeeze(0).numpy() if isinstance(relay,torch.Tensor) else relay
        if r.ndim==3:r=r[0]
        self.relay_cache[name]=r;return r
    def _mean(self,name,dim,skip_warmup=True):
        r=self._load_and_run(name);s=H3_WARMUP if(skip_warmup and r.shape[0]>H3_WARMUP+50)else 0;return float(r[s:,dim].mean())
    def _test(self,g,n,c,m,**v):self.results.append(TestResult(n,g,c,m,v))
    def test_T1(self):
        G="T1";r=self._load_and_run("g1_01_single")
        self._test(G,"T1_ndim",r.ndim==2,f"ndim={r.ndim}");self._test(G,"T1_dim",r.shape[1]==OUTPUT_DIM,f"D={r.shape[1]}");self._test(G,"T1_frames",r.shape[0]>100,f"T={r.shape[0]}")
    def test_T2(self):
        G="T2"
        for s in ["g1_01_single","g1_05_minor_2nd","g2_01_low","g2_03_high","g3_04_dense","g4_03_arpeggio","g5_01_piano","g5_02_organ"]:
            r=self._load_and_run(s);lo,hi=float(r.min()),float(r.max());self._test(G,f"T2_{s}",lo>=-0.001 and hi<=1.001,f"[{lo:.4f},{hi:.4f}]")
    def test_T3(self):
        G="T3";stims=["g1_01_single","g1_05_minor_2nd","g2_01_low","g2_03_high","g3_04_dense","g4_03_arpeggio","g5_02_organ"]
        means=np.array([[self._mean(s,d) for d in range(OUTPUT_DIM)] for s in stims])
        for d in range(OUTPUT_DIM):
            v=float(means[:,d].std());thresh=0.0003 if d in(E1,P0,P1,F0,F1)else 0.001;self._test(G,f"T3_{DIM_NAMES[d]}",v>thresh,f"std={v:.4f}>{thresh}")
    def test_T4(self):
        G="T4"
        for s in ["g1_01_single","g4_02_melody","g4_03_arpeggio"]:
            e0=self._mean(s,E0);self._test(G,f"T4_E0_{s}",e0>0.0,f"E0({e0:.4f})>0")
            e2=self._mean(s,E2);self._test(G,f"T4_E2_{s}",e2>0.0,f"E2({e2:.4f})>0 (sqrt(E0*E1))")
    def test_T5(self):
        G="T5"
        for s in ["g1_01_single","g1_05_minor_2nd","g3_04_dense","g4_01_sustained","g4_03_arpeggio"]:
            for d,nm in [(P0,"P0"),(P1,"P1")]:v=self._mean(s,d);self._test(G,f"T5_{nm}_{s}",v>0.0,f"{nm}({v:.4f})>0")
    def test_T6(self):
        G="T6";stims=["g1_01_single","g1_03_fifth","g1_05_minor_2nd","g2_01_low","g2_03_high","g3_04_dense","g4_01_sustained","g4_03_arpeggio"]
        e2s=np.array([self._mean(s,E2) for s in stims]);f0s=np.array([self._mean(s,F0) for s in stims])
        r=float(np.corrcoef(e2s,f0s)[0,1]);self._test(G,"T6_F0_E2",abs(r)>0.10,f"|r(F0,E2)|={abs(r):.4f}>0.10 (E2 feeds F0 50%)")
    def test_T7(self):
        G="T7"
        for d in range(OUTPUT_DIM):
            p=self._mean("g5_01_piano",d);o=self._mean("g5_02_organ",d);self._test(G,f"T7_{DIM_NAMES[d]}",p>0.0 and o>0.0,f"p={p:.4f},o={o:.4f}>0")
    def test_T8(self):
        G="T8"
        COUPLED={(0,2),(1,2),(0,3),(1,3),(2,3),(2,4),(2,7),(0,5),(3,5),(4,6),(3,7),(3,8),(4,8),(0,7),(1,7),(4,7),(5,7),(7,8)}
        stims=["g1_01_single","g1_03_fifth","g1_05_minor_2nd","g2_01_low","g2_03_high","g3_04_dense","g4_01_sustained","g4_03_arpeggio","g5_02_organ"]
        means=np.array([[self._mean(s,d) for d in range(OUTPUT_DIM)] for s in stims])
        for i in range(OUTPUT_DIM):
            for j in range(i+1,OUTPUT_DIM):
                if(i,j)in COUPLED:continue
                r=abs(float(np.corrcoef(means[:,i],means[:,j])[0,1]));self._test(G,f"T8_{i}_{j}",r<0.99,f"|r|={r:.3f}<0.99")
    def run_all(self):
        t0=time.time();self._init_pipeline()
        for t in [self.test_T1,self.test_T2,self.test_T3,self.test_T4,self.test_T5,self.test_T6,self.test_T7,self.test_T8]:
            nm=t.__name__;print(f"\n{'='*60}\n  {nm}\n{'='*60}")
            try:t()
            except Exception as ex:self.results.append(TestResult(f"{nm}_exc",nm,False,f"EXCEPTION: {ex}",{}));import traceback;traceback.print_exc()
        self._report(time.time()-t0)
    def _report(self,elapsed):
        passed=sum(1 for r in self.results if r.passed);total=len(self.results);failed=total-passed
        print(f"\n{'='*60}\n  DGTP RESULTS\n{'='*60}\n  Total:{total} Passed:{passed} Failed:{failed} Time:{elapsed:.1f}s\n{'='*60}")
        if failed:
            print("  FAILURES:")
            for r in self.results:
                if not r.passed:print(f"    FAIL {r.name}: {r.message}")
        ts=datetime.now().strftime("%Y%m%d_%H%M%S");out=RESULTS_DIR/f"dgtp_results_{ts}.json"
        with open(out,"w") as f:json.dump({"mechanism":"DGTP","function":"F3","timestamp":ts,"total":total,"passed":passed,"failed":failed,"elapsed_s":round(elapsed,1),"results":[{"name":r.name,"group":r.group,"passed":r.passed,"message":r.message,"values":r.values}for r in self.results]},f,indent=2)
        print(f"  Report: {out}")
if __name__=="__main__":DGTPTestRunner().run_all()
