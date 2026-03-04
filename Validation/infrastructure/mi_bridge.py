"""MI Pipeline Bridge — wraps the full R³→H³→C³ pipeline for validation use.

Provides a clean interface for all validation modules to run MI analysis,
extract specific output layers, and simulate pharmacological modifications.

Designed as a session-scoped singleton (expensive init ~5-10s, reuse across tests).
"""
from __future__ import annotations

import importlib
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np
import torch
from torch import Tensor

from Validation.config.paths import MI_ROOT, PROJECT_ROOT, TEST_AUDIO
from Validation.config.constants import (
    DA, NE, OPI, _5HT, FRAME_RATE, HOP_LENGTH, N_FFT, N_MELS, SAMPLE_RATE,
    NEURO_BASELINE,
)

# Ensure MI package is importable
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ── Result container ──

@dataclass
class ValidationResult:
    """Result from a single MI pipeline run for validation purposes."""
    audio_path: str
    duration_s: float
    n_frames: int
    fps: float
    r3: np.ndarray                              # (T, 97)
    h3_tuples: List[Tuple[int, int, int, int]]  # demand keys
    h3_data: np.ndarray                         # (N_tuples, T)
    beliefs: np.ndarray                         # (T, 131)
    relays: Dict[str, np.ndarray] = field(default_factory=dict)
    ram: np.ndarray = field(default_factory=lambda: np.empty(0))       # (T, 26)
    neuro: np.ndarray = field(default_factory=lambda: np.empty(0))     # (T, 4)
    reward: np.ndarray = field(default_factory=lambda: np.empty(0))    # (T,)
    psi: Dict[str, np.ndarray] = field(default_factory=dict)
    dim_6d: np.ndarray = field(default_factory=lambda: np.empty(0))    # (T, 6)
    dim_12d: np.ndarray = field(default_factory=lambda: np.empty(0))   # (T, 12)
    dim_24d: np.ndarray = field(default_factory=lambda: np.empty(0))   # (T, 24)
    neuro_gains: Optional[Dict[str, float]] = None  # if pharmacologically modified


# ── Audio loading (standalone, no catalog dependency) ──

def load_audio(
    path: str | Path,
    excerpt_s: float | None = 30.0,
    device: torch.device | None = None,
) -> Tuple[Tensor, Tensor, float]:
    """Load audio file → (waveform, mel, duration_s).

    Args:
        path: Path to audio file (wav, mp3, flac, etc.)
        excerpt_s: Max duration in seconds (None = full length).
        device: Torch device for output tensors.

    Returns:
        Tuple of (waveform (1,N), mel (1,128,T), duration_s).
    """
    import soundfile as sf
    import torchaudio

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Audio file not found: {path}")

    # Load
    try:
        data, sr = sf.read(str(path), dtype="float32")
        if data.ndim == 2:
            data = data.mean(axis=1)
        waveform = torch.from_numpy(data).unsqueeze(0)
    except Exception:
        waveform, sr = torchaudio.load(str(path))
        if waveform.shape[0] > 1:
            waveform = waveform.mean(dim=0, keepdim=True)

    # Resample
    if sr != SAMPLE_RATE:
        resampler = torchaudio.transforms.Resample(sr, SAMPLE_RATE)
        waveform = resampler(waveform)

    # Truncate
    if excerpt_s is not None:
        max_samples = int(excerpt_s * SAMPLE_RATE)
        if waveform.shape[-1] > max_samples:
            waveform = waveform[:, :max_samples]

    duration_s = waveform.shape[-1] / SAMPLE_RATE

    # Edge padding to prevent mel boundary artifacts
    pad_len = N_FFT // 2
    edge_pad_l = waveform[:, :1].expand(-1, pad_len)
    edge_pad_r = waveform[:, -1:].expand(-1, pad_len)
    waveform_padded = torch.cat([edge_pad_l, waveform, edge_pad_r], dim=-1)

    # Mel spectrogram
    mel_transform = torchaudio.transforms.MelSpectrogram(
        sample_rate=SAMPLE_RATE,
        n_fft=N_FFT,
        hop_length=HOP_LENGTH,
        n_mels=N_MELS,
        power=2.0,
    )
    mel = mel_transform(waveform_padded)

    # Trim padding frames
    pad_frames = pad_len // HOP_LENGTH
    mel = mel[:, :, pad_frames: mel.shape[-1] - pad_frames]

    # Normalize
    mel = torch.log1p(mel)
    mel_max = mel.amax(dim=(-2, -1), keepdim=True).clamp(min=1e-8)
    mel = mel / mel_max

    if device is not None:
        waveform = waveform.to(device)
        mel = mel.to(device)

    return waveform, mel, duration_s


# ── Role → depth mapping ──

_ROLE_TO_DEPTH = {
    "relay": 0, "encoder": 1, "associator": 2, "integrator": 3, "hub": 4,
}

_FUNCTION_IDS = ("f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9")


def _collect_mechanisms() -> List[Any]:
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
            pkg_dir = MI_ROOT / "brain" / "functions" / fn / "mechanisms"
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


def _fix_depths(nuclei: List[Any]) -> None:
    """Ensure PROCESSING_DEPTH matches mechanism role."""
    for n in nuclei:
        role = getattr(n, "ROLE", "relay")
        min_depth = _ROLE_TO_DEPTH.get(role, 0)
        if n.PROCESSING_DEPTH < min_depth:
            n.PROCESSING_DEPTH = min_depth


# ── Main Bridge class ──

class MIBridge:
    """Wraps the full MI pipeline for validation use.

    Usage:
        bridge = MIBridge()
        result = bridge.run("/path/to/audio.wav")
        result = bridge.run_with_modified_neuro("/path/to/audio.wav", da_gain=1.5)
    """

    def __init__(self, device: str | torch.device | None = None) -> None:
        print("[MIBridge] Initializing...")
        t0 = time.perf_counter()

        if device is None:
            if torch.backends.mps.is_available():
                self.device = torch.device("mps")
            elif torch.cuda.is_available():
                self.device = torch.device("cuda")
            else:
                self.device = torch.device("cpu")
        else:
            self.device = torch.device(device)

        from Musical_Intelligence.ear.r3 import R3Extractor
        from Musical_Intelligence.ear.h3 import H3Extractor
        from Musical_Intelligence.brain.executor import execute as _execute
        from Musical_Intelligence.brain.psi_interpreter import PsiInterpreter

        self.r3_extractor = R3Extractor()
        self.h3_extractor = H3Extractor()
        self.nuclei = _collect_mechanisms()
        self.psi_interpreter = PsiInterpreter()
        self._execute = _execute

        _fix_depths(self.nuclei)

        # Build H³ demand set
        self.h3_demand: Set[Tuple[int, int, int, int]] = set()
        for m in self.nuclei:
            for spec in m.h3_demand:
                self.h3_demand.add(spec.as_tuple())

        elapsed = time.perf_counter() - t0
        print(
            f"[MIBridge] Ready — {len(self.nuclei)} mechanisms, "
            f"{len(self.h3_demand)} H³ demands ({elapsed:.1f}s)"
        )

    def run(
        self,
        audio_path: str | Path,
        excerpt_s: float = 30.0,
    ) -> ValidationResult:
        """Run the full MI pipeline on an audio file.

        Args:
            audio_path: Path to audio file.
            excerpt_s: Max duration in seconds.

        Returns:
            ValidationResult with all output tensors as numpy arrays.
        """
        return self._run_pipeline(audio_path, excerpt_s)

    def run_with_modified_neuro(
        self,
        audio_path: str | Path,
        excerpt_s: float = 30.0,
        *,
        da_gain: float = 1.0,
        ne_gain: float = 1.0,
        opi_gain: float = 1.0,
        sht_gain: float = 1.0,
    ) -> ValidationResult:
        """Run MI with pharmacological neurochemical modification.

        Scales the neurochemical accumulation by the specified gains.
        da_gain=1.5 simulates enhanced DA (e.g. levodopa).
        opi_gain=0.1 simulates opioid antagonism (e.g. naltrexone).

        Args:
            audio_path: Path to audio file.
            excerpt_s: Max duration in seconds.
            da_gain: Multiplier for DA channel accumulation.
            ne_gain: Multiplier for NE channel accumulation.
            opi_gain: Multiplier for OPI channel accumulation.
            sht_gain: Multiplier for 5HT channel accumulation.

        Returns:
            ValidationResult with modified neurochemistry.
        """
        gains = {"DA": da_gain, "NE": ne_gain, "OPI": opi_gain, "5HT": sht_gain}
        return self._run_pipeline(audio_path, excerpt_s, neuro_gains=gains)

    def extract_beliefs(
        self,
        audio_path: str | Path,
        excerpt_s: float = 30.0,
    ) -> np.ndarray:
        """Extract (T, 131) belief time series."""
        result = self.run(audio_path, excerpt_s)
        return result.beliefs

    def extract_ram(
        self,
        audio_path: str | Path,
        excerpt_s: float = 30.0,
    ) -> np.ndarray:
        """Extract (T, 26) region activation map."""
        result = self.run(audio_path, excerpt_s)
        return result.ram

    def extract_neuro(
        self,
        audio_path: str | Path,
        excerpt_s: float = 30.0,
    ) -> np.ndarray:
        """Extract (T, 4) neurochemical state."""
        result = self.run(audio_path, excerpt_s)
        return result.neuro

    def extract_r3(
        self,
        audio_path: str | Path,
        excerpt_s: float = 30.0,
    ) -> np.ndarray:
        """Extract (T, 97) R³ features."""
        result = self.run(audio_path, excerpt_s)
        return result.r3

    def extract_psi(
        self,
        audio_path: str | Path,
        excerpt_s: float = 30.0,
    ) -> Dict[str, np.ndarray]:
        """Extract Ψ³ domain tensors."""
        result = self.run(audio_path, excerpt_s)
        return result.psi

    # ── Internal pipeline ──

    def _run_pipeline(
        self,
        audio_path: str | Path,
        excerpt_s: float,
        neuro_gains: Optional[Dict[str, float]] = None,
    ) -> ValidationResult:
        """Core pipeline execution with optional neurochemical modification."""
        t0 = time.perf_counter()

        # Load audio
        waveform, mel, duration_s = load_audio(audio_path, excerpt_s, self.device)
        n_frames = mel.shape[-1]

        # R³ extraction
        with torch.no_grad():
            r3_output = self.r3_extractor.extract(mel, audio=waveform, sr=SAMPLE_RATE)
        r3_features = r3_output.features  # (1, T, 97)

        # H³ extraction
        with torch.no_grad():
            h3_output = self.h3_extractor.extract(r3_features, self.h3_demand)

        # C³ brain execution
        with torch.no_grad():
            outputs, ram, neuro = self._execute(
                self.nuclei, h3_output.features, r3_features,
            )

        # Apply neurochemical gains if specified (pharmacological simulation)
        # Uses ADDITIVE shift model: drug effect = (gain - 1.0) × baseline
        #   Levodopa (DA gain=1.5): shift = +0.25 → DA increases
        #   Risperidone (DA gain=0.3): shift = -0.35 → DA decreases
        #   Naltrexone (OPI gain=0.1): shift = -0.45 → OPI decreases
        if neuro_gains is not None:
            channel_map = {"DA": DA, "NE": NE, "OPI": OPI, "5HT": _5HT}
            for ch_name, ch_idx in channel_map.items():
                gain = neuro_gains.get(ch_name, 1.0)
                if gain != 1.0:
                    shift = (gain - 1.0) * NEURO_BASELINE
                    neuro[:, :, ch_idx] = neuro[:, :, ch_idx] + shift
            neuro.clamp_(0.0, 1.0)

        # Assemble belief tensor
        tensor = self._assemble_tensor(outputs)
        psi = self.psi_interpreter.interpret(tensor, ram, neuro)

        # Reward signal with neurochemical modulation (REWARD-FORMULA.md v3.0):
        # Base reward from belief dynamics
        reward = tensor.mean(dim=-1) if tensor.shape[-1] > 0 else torch.zeros(1, n_frames)

        # DA modulates reward seeking/anticipation (Ferreri 2019, Salimpoor 2011)
        # OPI modulates hedonic pleasure/liking (Mallik 2017, Berridge 2007)
        da_state = neuro[:, :, DA]    # (B, T)
        opi_state = neuro[:, :, OPI]  # (B, T)
        da_mod = 1.0 + 0.5 * (da_state - NEURO_BASELINE)    # centered: 1.0 at baseline
        opi_mod = 1.0 + 0.6 * (opi_state - NEURO_BASELINE)  # centered: 1.0 at baseline
        reward = reward * da_mod * opi_mod

        elapsed = time.perf_counter() - t0
        fps = n_frames / elapsed if elapsed > 0 else 0.0

        # Convert to numpy
        relays: Dict[str, np.ndarray] = {}
        for nucleus in self.nuclei:
            if nucleus.NAME in outputs:
                relays[nucleus.NAME] = outputs[nucleus.NAME][0].cpu().numpy()

        h3_tuples = sorted(h3_output.features.keys())
        h3_data = np.stack(
            [h3_output.features[k][0].cpu().numpy() for k in h3_tuples],
            axis=0,
        ) if h3_tuples else np.empty((0, n_frames), dtype=np.float32)

        # Compute 131 belief traces
        from Lab.backend.beliefs import compute_beliefs
        beliefs_131 = compute_beliefs(relays, self.nuclei)

        # 3-tier dimensions
        from Musical_Intelligence.brain.dimensions import DimensionInterpreter
        dim_interp = DimensionInterpreter()
        dim_result = dim_interp.interpret_numpy(beliefs_131)

        psi_dict = {
            "affect": psi.affect[0].cpu().numpy(),
            "emotion": psi.emotion[0].cpu().numpy(),
            "aesthetic": psi.aesthetic[0].cpu().numpy(),
            "bodily": psi.bodily[0].cpu().numpy(),
            "cognitive": psi.cognitive[0].cpu().numpy(),
            "temporal": psi.temporal[0].cpu().numpy(),
        }

        return ValidationResult(
            audio_path=str(audio_path),
            duration_s=duration_s,
            n_frames=n_frames,
            fps=fps,
            r3=r3_features[0].cpu().numpy(),
            h3_tuples=h3_tuples,
            h3_data=h3_data,
            beliefs=beliefs_131,
            relays=relays,
            ram=ram[0].cpu().numpy(),
            neuro=neuro[0].cpu().numpy(),
            reward=reward[0].cpu().numpy(),
            psi=psi_dict,
            dim_6d=dim_result["dim_6d"],
            dim_12d=dim_result["dim_12d"],
            dim_24d=dim_result["dim_24d"],
            neuro_gains=neuro_gains,
        )

    def _assemble_tensor(self, outputs: Dict[str, Tensor]) -> Tensor:
        """Replicate MIPipeline._assemble_tensor: external + hybrid dims."""
        parts: List[Tensor] = []
        sorted_nuclei = sorted(
            self.nuclei, key=lambda n: (n.PROCESSING_DEPTH, n.NAME),
        )
        for nucleus in sorted_nuclei:
            if nucleus.NAME not in outputs:
                continue
            full_output = outputs[nucleus.NAME]
            exp_dims = self._get_exportable_dims(nucleus)
            if exp_dims:
                idx = torch.tensor(exp_dims, dtype=torch.long, device=full_output.device)
                parts.append(full_output.index_select(-1, idx))

        if not parts:
            B, T = next(iter(outputs.values())).shape[:2]
            return torch.zeros(B, T, 0, device=next(iter(outputs.values())).device)

        return torch.cat(parts, dim=-1)

    @staticmethod
    def _get_exportable_dims(nucleus) -> List[int]:
        """Get indices of hybrid + external scoped dimensions."""
        dims: List[int] = []
        for layer in nucleus.LAYERS:
            if layer.scope in ("hybrid", "external"):
                dims.extend(range(layer.start, layer.end))
        return dims
