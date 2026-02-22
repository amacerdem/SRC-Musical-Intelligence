"""Pipeline execution service — runs R³ → H³ → C³ and stores results."""

import json
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

import h5py
import numpy as np
import torch

from config import EXPERIMENTS_DIR, SAMPLE_RATE, HOP_LENGTH, FRAME_RATE
from services.audio_service import load_audio

# Global state for tracking running pipelines
_pipeline_status: dict[str, dict] = {}


def get_status(experiment_id: str) -> dict | None:
    return _pipeline_status.get(experiment_id)


def run_pipeline(
    audio_filename: str,
    excerpt_start: Optional[float] = None,
    excerpt_duration: Optional[float] = None,
) -> str:
    """Run the full MI pipeline on an audio file. Returns experiment_id."""
    experiment_id = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:6]
    _pipeline_status[experiment_id] = {
        "status": "running",
        "phase": "loading",
        "progress": 0.0,
        "fps": 0.0,
    }

    try:
        # ── Load audio ──
        _pipeline_status[experiment_id]["phase"] = "audio"
        samples, sr = load_audio(audio_filename)

        # Excerpt
        if excerpt_start is not None:
            start_sample = int(excerpt_start * sr)
            samples = samples[start_sample:]
        if excerpt_duration is not None:
            end_sample = int(excerpt_duration * sr)
            samples = samples[:end_sample]

        duration = len(samples) / sr
        n_frames = int(len(samples) / HOP_LENGTH)

        # ── Mel spectrogram ──
        _pipeline_status[experiment_id]["phase"] = "mel"
        _pipeline_status[experiment_id]["progress"] = 0.05
        waveform = torch.from_numpy(samples).unsqueeze(0)  # (1, N)

        import torchaudio
        mel_transform = torchaudio.transforms.MelSpectrogram(
            sample_rate=SAMPLE_RATE, n_fft=2048, hop_length=HOP_LENGTH, n_mels=128,
        )
        mel = mel_transform(waveform)  # (1, 128, T)
        mel_log = torch.log1p(mel)
        actual_frames = mel_log.shape[2]

        # ── R³ ──
        _pipeline_status[experiment_id]["phase"] = "r3"
        _pipeline_status[experiment_id]["progress"] = 0.10
        t0 = time.time()

        from Musical_Intelligence.ear.r3.extractor import R3Extractor
        r3_extractor = R3Extractor()
        r3_output = r3_extractor(mel_log)  # R3Output
        r3_features = r3_output.features  # (1, T, 97)
        r3_names = list(r3_output.feature_names)

        r3_time = time.time() - t0
        _pipeline_status[experiment_id]["progress"] = 0.30

        # ── H³ ──
        _pipeline_status[experiment_id]["phase"] = "h3"
        t0 = time.time()

        from Musical_Intelligence.ear.h3.extractor import H3Extractor
        # Collect H³ demand from C³ kernel
        from Musical_Intelligence.brain.kernel.scheduler import C3Scheduler
        scheduler = C3Scheduler()
        h3_demand = scheduler.h3_demand()

        h3_extractor = H3Extractor()
        h3_output = h3_extractor(r3_features, demand=h3_demand)

        h3_time = time.time() - t0
        _pipeline_status[experiment_id]["progress"] = 0.60

        # ── C³ ──
        _pipeline_status[experiment_id]["phase"] = "c3"
        t0 = time.time()

        c3_output = scheduler.run(
            r3=r3_features,
            h3=h3_output.features,
        )

        c3_time = time.time() - t0
        total_time = r3_time + h3_time + c3_time
        fps = actual_frames / total_time if total_time > 0 else 0

        _pipeline_status[experiment_id]["progress"] = 0.90
        _pipeline_status[experiment_id]["fps"] = round(fps, 1)

        # ── Save to HDF5 ──
        _pipeline_status[experiment_id]["phase"] = "saving"
        h5_path = EXPERIMENTS_DIR / f"{experiment_id}.h5"

        with h5py.File(h5_path, "w") as f:
            # Meta
            meta = f.create_group("meta")
            meta.attrs["audio_name"] = audio_filename
            meta.attrs["timestamp"] = datetime.now().isoformat()
            meta.attrs["duration_sec"] = duration
            meta.attrs["n_frames"] = actual_frames
            meta.attrs["fps"] = fps
            meta.attrs["kernel_version"] = "v4.0"

            # Audio
            audio_g = f.create_group("audio")
            audio_g.create_dataset("waveform", data=samples.astype(np.float32))
            audio_g.create_dataset("mel", data=mel_log.squeeze(0).numpy().astype(np.float32))
            audio_g.attrs["sr"] = SAMPLE_RATE

            # R³
            r3_g = f.create_group("r3")
            r3_np = r3_features.squeeze(0).detach().numpy()  # (T, 97)
            r3_g.create_dataset("features", data=r3_np.astype(np.float32))
            r3_g.create_dataset("feature_names", data=r3_names)

            # H³
            h3_g = f.create_group("h3")
            h3_dict = h3_output.features
            tuples_list = list(h3_dict.keys())
            if tuples_list:
                tuples_arr = np.array(tuples_list, dtype=np.int32)  # (N, 4)
                values_list = [h3_dict[k].squeeze(0).detach().numpy() for k in tuples_list]
                values_arr = np.stack(values_list, axis=0).astype(np.float32)  # (N, T)
                h3_g.create_dataset("tuples", data=tuples_arr)
                h3_g.create_dataset("values", data=values_arr)

            # C³
            c3_g = f.create_group("c3")
            # Beliefs
            if hasattr(c3_output, 'beliefs'):
                beliefs_g = c3_g.create_group("beliefs")
                beliefs = c3_output.beliefs  # dict or tensor
                if isinstance(beliefs, dict):
                    names = list(beliefs.keys())
                    beliefs_g.create_dataset("names", data=names)
                    obs = np.stack([beliefs[n].get("observed", torch.zeros(actual_frames)).detach().numpy()
                                    for n in names], axis=1)  # (T, N)
                    beliefs_g.create_dataset("observed", data=obs.astype(np.float32))

            # Relays
            if hasattr(c3_output, 'relays'):
                relays_g = c3_g.create_group("relays")
                for rname, rdata in c3_output.relays.items():
                    relay_np = rdata.squeeze(0).detach().numpy() if isinstance(rdata, torch.Tensor) else rdata
                    relays_g.create_dataset(rname.lower(), data=relay_np.astype(np.float32))

            # RAM
            if hasattr(c3_output, 'ram') and c3_output.ram is not None:
                ram_np = c3_output.ram.squeeze(0).detach().numpy()
                c3_g.create_dataset("ram", data=ram_np.astype(np.float32))

            # Neuro
            if hasattr(c3_output, 'neuro') and c3_output.neuro is not None:
                neuro_np = c3_output.neuro.squeeze(0).detach().numpy()
                c3_g.create_dataset("neuro", data=neuro_np.astype(np.float32))

            # Reward
            if hasattr(c3_output, 'reward') and c3_output.reward is not None:
                reward_np = c3_output.reward.squeeze(0).detach().numpy()
                c3_g.create_dataset("reward", data=reward_np.astype(np.float32))

            # Salience
            if hasattr(c3_output, 'salience') and c3_output.salience is not None:
                sal_g = f.create_group("salience")
                sal_np = c3_output.salience.squeeze(0).detach().numpy()
                if sal_np.ndim == 1:
                    sal_g.create_dataset("total", data=sal_np.astype(np.float32))
                else:
                    sal_g.create_dataset("total", data=sal_np.astype(np.float32))

        # Save metadata JSON
        reward_data = c3_output.reward.squeeze(0).detach().numpy() if hasattr(c3_output, 'reward') and c3_output.reward is not None else np.zeros(1)
        meta_json = {
            "experiment_id": experiment_id,
            "audio_name": audio_filename,
            "timestamp": datetime.now().isoformat(),
            "duration": round(duration, 2),
            "n_frames": actual_frames,
            "fps": round(fps, 1),
            "kernel_version": "v4.0",
            "reward_mean": round(float(reward_data.mean()), 6),
            "reward_positive_pct": round(float((reward_data > 0).mean() * 100), 1),
            "r3_time": round(r3_time, 3),
            "h3_time": round(h3_time, 3),
            "c3_time": round(c3_time, 3),
        }
        (EXPERIMENTS_DIR / f"{experiment_id}.json").write_text(
            json.dumps(meta_json, indent=2)
        )

        _pipeline_status[experiment_id] = {
            "status": "complete",
            "phase": "done",
            "progress": 1.0,
            "fps": round(fps, 1),
        }
        return experiment_id

    except Exception as e:
        _pipeline_status[experiment_id] = {
            "status": "error",
            "phase": "error",
            "progress": 0.0,
            "fps": 0.0,
            "error": str(e),
        }
        raise
