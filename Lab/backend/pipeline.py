"""MI Pipeline wrapper — initializes R³/H³/C³ and runs end-to-end analysis.

Singleton ``MIPipeline`` is created at app startup (lifespan) and reused
for all pipeline runs.  The heavy init (~5-10s) happens once; subsequent
runs only load audio + forward-pass.

Usage::

    pipeline = MIPipeline()
    result = pipeline.run("bach", excerpt_s=30.0)
"""
from __future__ import annotations

import importlib
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

import numpy as np
import torch
from torch import Tensor

from .config import (
    AUDIO_CATALOG,
    AUDIO_DIR,
    FRAME_RATE,
    HOP_LENGTH,
    MIDI_CATALOG,
    N_FFT,
    N_MELS,
    PROJECT_ROOT,
    SAMPLE_RATE,
)

# Ensure project root is on sys.path so MI package is importable
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------

@dataclass
class ExperimentResult:
    audio_name: str
    duration_s: float
    n_frames: int
    fps: float
    r3: np.ndarray                             # (T, 97)
    h3_tuples: List[Tuple[int, int, int, int]] # demand keys
    h3_data: np.ndarray                        # (N_tuples, T)
    beliefs: np.ndarray                        # (T, 131) — full C³ external tensor
    relays: Dict[str, np.ndarray] = field(default_factory=dict)  # name → (T, D)
    ram: np.ndarray = field(default_factory=lambda: np.empty(0))  # (T, 26)
    neuro: np.ndarray = field(default_factory=lambda: np.empty(0))  # (T, 4)
    reward: np.ndarray = field(default_factory=lambda: np.empty(0))  # (T,)
    psi: Dict[str, np.ndarray] = field(default_factory=dict)     # domain → (T, D)
    dim_6d: np.ndarray = field(default_factory=lambda: np.empty(0))   # (T, 6)
    dim_12d: np.ndarray = field(default_factory=lambda: np.empty(0))  # (T, 12)
    dim_24d: np.ndarray = field(default_factory=lambda: np.empty(0))  # (T, 24)
    belief_decomposition: Dict[str, Dict[str, np.ndarray]] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Mechanism collection (from Tests/conftest.py pattern)
# ---------------------------------------------------------------------------

_FUNCTION_IDS = ("f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9")


def _collect_mechanism_instances() -> List[Any]:
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
            # Fallback: scan subpackages
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


# ---------------------------------------------------------------------------
# Audio loading (self-contained, avoids broken preprocessing.py import)
# ---------------------------------------------------------------------------

def _load_audio(
    name: str,
    excerpt_s: float | None = 30.0,
) -> Tuple[Tensor, Tensor, float]:
    """Load audio file → (waveform, mel, duration_s).

    Uses the same logic as Tests/benchmark_real_audio/helpers.py.
    """
    import soundfile as sf
    import torchaudio

    if name in AUDIO_CATALOG:
        filepath = AUDIO_DIR / AUDIO_CATALOG[name]
    elif name in MIDI_CATALOG:
        filepath = MIDI_CATALOG[name]["path"]
    else:
        raise FileNotFoundError(f"Unknown audio: {name}")

    if not filepath.exists():
        raise FileNotFoundError(f"Audio file not found: {filepath}")

    # Load audio
    try:
        data, sr = sf.read(str(filepath), dtype="float32")
        if data.ndim == 2:
            data = data.mean(axis=1)
        waveform = torch.from_numpy(data).unsqueeze(0)  # (1, N)
    except Exception:
        waveform, sr = torchaudio.load(str(filepath))
        if waveform.shape[0] > 1:
            waveform = waveform.mean(dim=0, keepdim=True)

    # Resample if needed
    if sr != SAMPLE_RATE:
        resampler = torchaudio.transforms.Resample(sr, SAMPLE_RATE)
        waveform = resampler(waveform)

    # Truncate
    if excerpt_s is not None:
        max_samples = int(excerpt_s * SAMPLE_RATE)
        if waveform.shape[-1] > max_samples:
            waveform = waveform[:, :max_samples]

    duration_s = waveform.shape[-1] / SAMPLE_RATE

    # Pad waveform edges to prevent mel spectrogram boundary artifacts.
    # torchaudio's MelSpectrogram uses center=True (reflection padding of
    # N_FFT//2 samples).  For audio that starts/ends abruptly, the reflected
    # content differs from the real signal, causing ~4-frame edge artifacts
    # that propagate through R³→H³→C³.  We replicate the first/last sample
    # by N_FFT//2 so the STFT boundary frames see real audio content.
    pad_len = N_FFT // 2
    edge_pad = waveform[:, :1].expand(-1, pad_len)   # first sample repeated
    edge_pad_r = waveform[:, -1:].expand(-1, pad_len) # last sample repeated
    waveform_padded = torch.cat([edge_pad, waveform, edge_pad_r], dim=-1)

    # Mel spectrogram
    mel_transform = torchaudio.transforms.MelSpectrogram(
        sample_rate=SAMPLE_RATE,
        n_fft=N_FFT,
        hop_length=HOP_LENGTH,
        n_mels=N_MELS,
        power=2.0,
    )
    mel = mel_transform(waveform_padded)  # (1, 128, T_padded)

    # Trim the padding frames: pad_len samples → pad_len // HOP_LENGTH frames
    pad_frames = pad_len // HOP_LENGTH
    mel = mel[:, :, pad_frames: mel.shape[-1] - pad_frames]

    mel = torch.log1p(mel)
    mel_max = mel.amax(dim=(-2, -1), keepdim=True).clamp(min=1e-8)
    mel = mel / mel_max

    return waveform, mel, duration_s


# ---------------------------------------------------------------------------
# Depth fix — many mechanisms default to depth 0 regardless of role
# ---------------------------------------------------------------------------

_ROLE_TO_DEPTH = {
    "relay": 0,
    "encoder": 1,
    "associator": 2,
    "integrator": 3,
    "hub": 4,
}


def _fix_processing_depths(nuclei: List[Any]) -> None:
    """Ensure PROCESSING_DEPTH matches the mechanism's role.

    The base classes ``Encoder``, ``Associator`` etc. don't always override
    ``PROCESSING_DEPTH`` from the default 0, causing execution-order bugs.
    This sets the minimum depth for each role (mechanisms that already have
    a higher depth are left unchanged).
    """
    for n in nuclei:
        role = getattr(n, "ROLE", "relay")
        min_depth = _ROLE_TO_DEPTH.get(role, 0)
        if n.PROCESSING_DEPTH < min_depth:
            n.PROCESSING_DEPTH = min_depth


# ---------------------------------------------------------------------------
# Pipeline singleton
# ---------------------------------------------------------------------------

def _select_device() -> torch.device:
    """Pick the best available torch device: MPS (Apple Silicon) > CUDA > CPU."""
    if torch.backends.mps.is_available():
        return torch.device("mps")
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


class MIPipeline:
    """Wraps the full R³→H³→C³ pipeline for the Lab backend."""

    def __init__(self, device: torch.device | str | None = None) -> None:
        print("[MI-Pipeline] Initializing...")
        t0 = time.perf_counter()

        self.device = torch.device(device) if device else _select_device()
        print(f"[MI-Pipeline] Device: {self.device}")

        from Musical_Intelligence.ear.r3 import R3Extractor
        from Musical_Intelligence.ear.h3 import H3Extractor
        from Musical_Intelligence.brain.orchestrator import BrainOrchestrator
        from Musical_Intelligence.brain.executor import execute as _execute
        from Musical_Intelligence.brain.psi_interpreter import PsiInterpreter

        self.r3_extractor = R3Extractor()
        self.h3_extractor = H3Extractor()
        self.nuclei = _collect_mechanism_instances()
        self.psi_interpreter = PsiInterpreter()
        self._execute = _execute

        # Fix depth assignments: many Encoder/Associator mechanisms default
        # to depth 0 (base class default) but need correct role-based depth
        # for the executor to order them properly.
        _fix_processing_depths(self.nuclei)

        # H³ demand set
        self.h3_demand: Set[Tuple[int, int, int, int]] = set()
        for m in self.nuclei:
            for spec in m.h3_demand:
                self.h3_demand.add(spec.as_tuple())

        elapsed = time.perf_counter() - t0
        print(
            f"[MI-Pipeline] Ready — {len(self.nuclei)} mechanisms, "
            f"{len(self.h3_demand)} H³ demands ({elapsed:.1f}s)"
        )

    def run(
        self,
        audio_name: str,
        excerpt_s: float = 30.0,
        *,
        status_callback=None,
    ) -> ExperimentResult:
        """Run full pipeline on audio.

        Args:
            audio_name: Key from AUDIO_CATALOG.
            excerpt_s: Max duration in seconds.
            status_callback: Optional callable(phase, progress) for updates.

        Returns:
            ExperimentResult with all analysis tensors as numpy arrays.
        """
        t0 = time.perf_counter()

        # Phase 1: Load audio
        if status_callback:
            status_callback("loading", 0.0)
        waveform, mel, duration_s = _load_audio(audio_name, excerpt_s)
        n_frames = mel.shape[-1]

        # Move tensors to device (mel computed on CPU for torchaudio compat)
        mel = mel.to(self.device)
        waveform = waveform.to(self.device)

        # Phase 2: R³ extraction
        if status_callback:
            status_callback("r3", 0.1)
        with torch.no_grad():
            r3_output = self.r3_extractor.extract(
                mel, audio=waveform, sr=SAMPLE_RATE,
            )
        r3_features = r3_output.features  # (1, T, 97)

        # Phase 3: H³ extraction
        if status_callback:
            status_callback("h3", 0.3)
        with torch.no_grad():
            h3_output = self.h3_extractor.extract(r3_features, self.h3_demand)

        # Phase 4: C³ brain execution
        if status_callback:
            status_callback("c3", 0.5)
        with torch.no_grad():
            outputs, ram, neuro = self._execute(
                self.nuclei, h3_output.features, r3_features,
            )

        # Phase 5: Assemble tensor and Ψ³
        if status_callback:
            status_callback("psi", 0.8)

        tensor = self._assemble_tensor(outputs)
        psi = self.psi_interpreter.interpret(tensor, ram, neuro)

        # Phase 6: Build reward signal
        reward = tensor.mean(dim=-1) if tensor.shape[-1] > 0 else torch.zeros(1, n_frames)

        elapsed = time.perf_counter() - t0
        fps = n_frames / elapsed if elapsed > 0 else 0.0

        if status_callback:
            status_callback("done", 1.0)

        # Convert to numpy
        relays: Dict[str, np.ndarray] = {}
        for nucleus in self.nuclei:
            if nucleus.NAME in outputs:
                relays[nucleus.NAME] = outputs[nucleus.NAME][0].cpu().numpy()

        # H³ as ordered arrays
        h3_tuples = sorted(h3_output.features.keys())
        h3_data = np.stack(
            [h3_output.features[k][0].cpu().numpy() for k in h3_tuples],
            axis=0,
        ) if h3_tuples else np.empty((0, n_frames), dtype=np.float32)

        # Phase 7: Compute 131 belief traces from mechanism outputs
        if status_callback:
            status_callback("beliefs", 0.9)
        from .beliefs import compute_beliefs
        beliefs_131 = compute_beliefs(relays, self.nuclei)  # (T, 131)

        # Phase 8: Belief horizon decomposition (band/law ablation)
        from .belief_decomposition import compute_belief_decomposition
        belief_decomp = compute_belief_decomposition(
            self.nuclei, h3_output.features, r3_features,
        )

        # Phase 9: Independent 3-tier dimensions (6D + 12D + 24D)
        from Musical_Intelligence.brain.dimensions import DimensionInterpreter
        dim_interp = DimensionInterpreter()
        dim_result = dim_interp.interpret_numpy(beliefs_131)

        # Ψ³ domains
        psi_dict = {
            "affect": psi.affect[0].cpu().numpy(),
            "emotion": psi.emotion[0].cpu().numpy(),
            "aesthetic": psi.aesthetic[0].cpu().numpy(),
            "bodily": psi.bodily[0].cpu().numpy(),
            "cognitive": psi.cognitive[0].cpu().numpy(),
            "temporal": psi.temporal[0].cpu().numpy(),
        }

        return ExperimentResult(
            audio_name=audio_name,
            duration_s=duration_s,
            n_frames=n_frames,
            fps=fps,
            r3=r3_features[0].cpu().numpy(),          # (T, 97)
            h3_tuples=h3_tuples,
            h3_data=h3_data,                           # (N, T)
            beliefs=beliefs_131,                        # (T, 131)
            relays=relays,
            ram=ram[0].cpu().numpy(),                   # (T, 26)
            neuro=neuro[0].cpu().numpy(),               # (T, 4)
            reward=reward[0].cpu().numpy(),             # (T,)
            psi=psi_dict,
            dim_6d=dim_result["dim_6d"],                # (T, 6)
            dim_12d=dim_result["dim_12d"],              # (T, 12)
            dim_24d=dim_result["dim_24d"],              # (T, 24)
            belief_decomposition=belief_decomp,
        )

    def _assemble_tensor(self, outputs: Dict[str, Tensor]) -> Tensor:
        """Replicate BrainOrchestrator._assemble_tensor: external + hybrid dims."""
        parts: List[Tensor] = []
        sorted_nuclei = sorted(
            self.nuclei,
            key=lambda n: (n.PROCESSING_DEPTH, n.NAME),
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
        """Get indices of hybrid + external scoped dimensions from LAYERS."""
        dims: List[int] = []
        for layer in nucleus.LAYERS:
            if layer.scope in ("hybrid", "external"):
                dims.extend(range(layer.start, layer.end))
        return dims
