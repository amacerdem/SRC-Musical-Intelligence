#!/usr/bin/env python3
"""
MI RunPod Full Pipeline
=======================
1. Generate mel spectrograms from segmented WAVs
2. Run MI pipeline (R³ → H³ → C³ → 5+5D) to create NPZ training data
3. Export frame-level 5+5D temporal JSON for each segment
4. Run full training

Usage:
    python Musical_Intelligence/scripts/runpod_train.py
    python Musical_Intelligence/scripts/runpod_train.py --step npz      # only generate NPZ
    python Musical_Intelligence/scripts/runpod_train.py --step train    # only train
    python Musical_Intelligence/scripts/runpod_train.py --step export   # only export JSON
"""

import argparse
import json
import math
import os
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torchaudio

# ── Project root ──
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ── Constants ──
SAMPLE_RATE = 44100
N_MELS = 128
HOP_LENGTH = 256       # ~172 Hz frame rate at 44.1 kHz
N_FFT = 2048
FRAME_RATE = SAMPLE_RATE / HOP_LENGTH  # ~172.27 Hz

DIM_NAMES = [
    # Musical (Radar 1)
    "speed", "volume", "weight", "texture", "depth",
    # Emotional (Radar 2)
    "mood", "energy", "hardness", "predictability", "focus",
]


# ======================================================================
# STEP 1: Generate NPZ from WAV segments
# ======================================================================

def wav_to_mel(wav_path: str, device: torch.device) -> torch.Tensor:
    """Load WAV and compute mel spectrogram. Returns (1, 128, T)."""
    waveform, sr = torchaudio.load(wav_path)
    # Resample if needed
    if sr != SAMPLE_RATE:
        waveform = torchaudio.functional.resample(waveform, sr, SAMPLE_RATE)
    # Mono
    if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0, keepdim=True)

    waveform = waveform.to(device)

    mel_transform = torchaudio.transforms.MelSpectrogram(
        sample_rate=SAMPLE_RATE,
        n_fft=N_FFT,
        hop_length=HOP_LENGTH,
        n_mels=N_MELS,
        power=2.0,
    ).to(device)

    mel = mel_transform(waveform)        # (1, 128, T)
    mel = torch.log1p(mel)               # log-mel
    # Normalize to [0, 1]
    mel_min = mel.min()
    mel_range = mel.max() - mel_min
    if mel_range > 0:
        mel = (mel - mel_min) / mel_range
    return mel


def run_mi_pipeline(mel: torch.Tensor, device: torch.device):
    """Run symbolic MI pipeline: mel → R³ → H³ → beliefs → dims.

    Returns dict with numpy arrays: mel, r3, h3, beliefs, dims
    """
    try:
        from Musical_Intelligence.ear.r3.extractor import R3Extractor
        from Musical_Intelligence.ear.h3.extractor import H3Extractor
        from Musical_Intelligence.brain.orchestrator import BrainOrchestrator

        # R³
        r3_ext = R3Extractor()
        r3_out = r3_ext.extract(mel)  # .features: (B, T, 97)
        r3 = r3_out.features

        # H³ — use default kernel demands
        h3_ext = H3Extractor()
        # Get demand from kernel or use minimal set
        try:
            from Musical_Intelligence.brain.kernel import get_default_demands
            demands = get_default_demands()
        except ImportError:
            demands = set()
        h3_out = h3_ext.extract(r3, demands)

        # Stack H³ sparse features into dense tensor
        if h3_out.features:
            h3_keys = sorted(h3_out.features.keys())
            h3_tensor = torch.stack([h3_out.features[k] for k in h3_keys], dim=-1)
        else:
            T = r3.shape[1]
            h3_tensor = torch.zeros(1, T, 637, device=device)

        # C³ beliefs
        orchestrator = BrainOrchestrator.build_default()
        brain_out = orchestrator.process(r3, h3_out.features)
        beliefs = brain_out.tensor  # (B, T, 131)

        # 5+5D dims from beliefs (simple projection as initial target)
        dims = _beliefs_to_dims(beliefs)

        return {
            "mel": mel[0].cpu().numpy(),         # (128, T)
            "r3": r3[0].cpu().numpy(),           # (T, 97)
            "h3": h3_tensor[0].cpu().numpy(),    # (T, N_h3)
            "beliefs": beliefs[0].cpu().numpy(), # (T, 131)
            "dims": dims[0].cpu().numpy(),       # (T, 10)
        }

    except Exception as e:
        if not hasattr(run_mi_pipeline, '_warned'):
            print(f"    Symbolic pipeline unavailable ({e}), using neural proxy for all segments", flush=True)
            run_mi_pipeline._warned = True
        return run_neural_pipeline(mel, device)


def run_neural_pipeline(mel: torch.Tensor, device: torch.device):
    """Fallback: use lightweight neural feature extraction.

    Generates proxy features when the full symbolic pipeline isn't available.
    """
    B, C, T = mel.shape

    # ── R³ (97D): extract from mel using signal processing ──
    r3 = _extract_r3_proxy(mel, device)  # (B, T, 97)

    # ── H³: multi-scale temporal statistics of R³ ──
    h3 = _extract_h3_proxy(r3, device)  # (B, T, N_h3)

    # ── Beliefs (131D): derived from R³ + H³ ──
    beliefs = _extract_belief_proxy(r3, h3, device)  # (B, T, 131)

    # ── 5+5D dims ──
    dims = _beliefs_to_dims(beliefs)  # (B, T, 10)

    return {
        "mel": mel[0].cpu().numpy(),
        "r3": r3[0].cpu().numpy(),
        "h3": h3[0].cpu().numpy(),
        "beliefs": beliefs[0].cpu().numpy(),
        "dims": dims[0].cpu().numpy(),
    }


def _extract_r3_proxy(mel: torch.Tensor, device: torch.device) -> torch.Tensor:
    """Signal-processing proxy for R³ 97D features from mel."""
    B, N, T = mel.shape
    mt = mel.transpose(1, 2)  # (B, T, 128)

    features = []

    # A: Consonance (7D) — spectral statistics
    spec_mean = mt.mean(dim=-1, keepdim=True)
    spec_std = mt.std(dim=-1, keepdim=True)
    spec_max = mt.max(dim=-1, keepdim=True).values
    spec_min = mt.min(dim=-1, keepdim=True).values
    spec_range = spec_max - spec_min
    # Roughness proxy: high-freq energy variance
    hf = mt[:, :, 64:]
    roughness = hf.std(dim=-1, keepdim=True)
    # Harmonic deviation
    harm_dev = (mt - spec_mean).abs().mean(dim=-1, keepdim=True)
    features.append(torch.cat([roughness, spec_std, harm_dev, spec_mean,
                                spec_range, spec_min, spec_max], dim=-1))  # 7D

    # B: Energy (5D)
    rms = mt.pow(2).mean(dim=-1, keepdim=True).sqrt()
    # Velocity (frame diff)
    vel = torch.zeros_like(rms)
    vel[:, 1:] = rms[:, 1:] - rms[:, :-1]
    acc = torch.zeros_like(vel)
    acc[:, 1:] = vel[:, 1:] - vel[:, :-1]
    loudness = mt.sum(dim=-1, keepdim=True) / N
    onset = vel.abs()
    features.append(torch.cat([rms, vel, acc, loudness, onset], dim=-1))  # 5D

    # C: Timbre (9D)
    centroid = (mt * torch.arange(N, device=device).float()).sum(dim=-1, keepdim=True) / (mt.sum(dim=-1, keepdim=True) + 1e-8) / N
    bandwidth = ((mt * (torch.arange(N, device=device).float().unsqueeze(0).unsqueeze(0) / N - centroid).pow(2)).sum(dim=-1, keepdim=True) / (mt.sum(dim=-1, keepdim=True) + 1e-8)).sqrt()
    flatness = (mt + 1e-8).log().mean(dim=-1, keepdim=True).exp() / (mt.mean(dim=-1, keepdim=True) + 1e-8)
    rolloff = torch.zeros(B, T, 1, device=device)
    cum_energy = mt.cumsum(dim=-1)
    total = mt.sum(dim=-1, keepdim=True)
    for b in range(B):
        rolloff[b] = (cum_energy[b] >= 0.85 * total[b]).float().argmax(dim=-1, keepdim=True).float() / N
    # Tristimulus (3D) — energy in low/mid/high thirds
    tri1 = mt[:, :, :43].mean(dim=-1, keepdim=True)
    tri2 = mt[:, :, 43:86].mean(dim=-1, keepdim=True)
    tri3 = mt[:, :, 86:].mean(dim=-1, keepdim=True)
    smoothness = spec_std  # reuse
    tonalness = spec_max / (spec_mean + 1e-8)
    features.append(torch.cat([centroid, bandwidth, tonalness, flatness, smoothness,
                                rolloff, tri1, tri2, tri3], dim=-1))  # 9D

    # D: Change (4D)
    flux = torch.zeros(B, T, 1, device=device)
    flux[:, 1:] = (mt[:, 1:] - mt[:, :-1]).pow(2).mean(dim=-1, keepdim=True)
    entropy_p = mt / (mt.sum(dim=-1, keepdim=True) + 1e-8)
    log_p = (entropy_p + 1e-8).log()
    entropy = -(entropy_p * log_p).sum(dim=-1, keepdim=True) / math.log(N)
    flatness_d = flatness
    concentration = 1.0 - entropy
    features.append(torch.cat([flux, entropy, flatness_d, concentration], dim=-1))  # 4D

    # F: Pitch/Chroma (16D)
    # Approximate chroma from mel (12D) + pitch features (4D)
    chroma_bins = N // 12
    chroma = torch.zeros(B, T, 12, device=device)
    for i in range(12):
        s = i * chroma_bins
        e = min(s + chroma_bins, N)
        chroma[:, :, i] = mt[:, :, s:e].mean(dim=-1)
    # Normalize
    chroma = chroma / (chroma.sum(dim=-1, keepdim=True) + 1e-8)
    pitch_height = centroid  # proxy
    chroma_entropy = -(chroma * (chroma + 1e-8).log()).sum(dim=-1, keepdim=True) / math.log(12)
    pitch_salience = chroma.max(dim=-1, keepdim=True).values
    inharmonicity = 1.0 - pitch_salience
    features.append(torch.cat([chroma, pitch_height, chroma_entropy, pitch_salience, inharmonicity], dim=-1))  # 16D

    # G: Rhythm/Groove (10D)
    # Tempo proxy from onset autocorrelation
    onset_env = vel.abs().squeeze(-1)  # (B, T)
    tempo_proxy = torch.zeros(B, T, 1, device=device)
    beat_str = torch.zeros(B, T, 1, device=device)
    pulse_clarity = onset_env.std(dim=-1, keepdim=True).unsqueeze(-1).expand(B, T, 1)
    event_density = (onset_env > onset_env.mean(dim=-1, keepdim=True)).float().unsqueeze(-1)
    # Fill with simple proxies
    syncopation = torch.zeros(B, T, 1, device=device)
    metricality = torch.zeros(B, T, 1, device=device)
    isochrony = torch.zeros(B, T, 1, device=device)
    groove = event_density * pulse_clarity
    tempo_stab = torch.zeros(B, T, 1, device=device)
    rhythm_reg = torch.zeros(B, T, 1, device=device)
    features.append(torch.cat([tempo_proxy, beat_str, pulse_clarity, syncopation,
                                metricality, isochrony, groove, event_density,
                                tempo_stab, rhythm_reg], dim=-1))  # 10D

    # H: Harmony/Tonality (12D)
    key_clarity = chroma.max(dim=-1, keepdim=True).values - chroma.mean(dim=-1, keepdim=True)
    # Tonnetz (6D)
    tonnetz = torch.zeros(B, T, 6, device=device)
    for i in range(6):
        tonnetz[:, :, i] = chroma[:, :, (2*i) % 12] - chroma[:, :, (2*i+6) % 12]
    voice_lead = torch.zeros(B, T, 1, device=device)
    harm_change = flux
    tonal_stab = 1.0 - flux
    diatonicity = key_clarity
    syntactic = torch.zeros(B, T, 1, device=device)
    features.append(torch.cat([key_clarity, tonnetz, voice_lead, harm_change,
                                tonal_stab, diatonicity, syntactic], dim=-1))  # 12D

    # J: Timbre Extended (20D) — MFCCs(13) + Spectral Contrast(7)
    # DCT for MFCCs
    n_mfcc = 13
    dct_mat = torch.zeros(N, n_mfcc, device=device)
    for k in range(n_mfcc):
        for n in range(N):
            dct_mat[n, k] = math.cos(math.pi * (k + 1) * (2 * n + 1) / (2 * N))
    log_mel = (mt + 1e-8).log()
    mfcc = torch.matmul(log_mel, dct_mat)  # (B, T, 13)
    # Normalize MFCCs
    mfcc = mfcc / (mfcc.abs().max() + 1e-8)
    # Spectral contrast (7 bands)
    n_bands = 7
    band_size = N // n_bands
    contrast = torch.zeros(B, T, n_bands, device=device)
    for i in range(n_bands):
        s = i * band_size
        e = min(s + band_size, N)
        band = mt[:, :, s:e]
        contrast[:, :, i] = band.max(dim=-1).values - band.min(dim=-1).values
    features.append(torch.cat([mfcc, contrast], dim=-1))  # 20D

    # K: Modulation/Psychoacoustic (14D)
    mod_rates = [0.5, 1, 2, 4, 8, 16]
    mod_features = []
    for rate in mod_rates:
        # Simple envelope modulation proxy
        mod_features.append(torch.zeros(B, T, 1, device=device))
    mod_centroid = torch.zeros(B, T, 1, device=device)
    mod_bandwidth = torch.zeros(B, T, 1, device=device)
    sharpness_z = centroid * 2  # proxy
    fluct_str = flux  # proxy
    loudness_aw = loudness  # proxy
    alpha_ratio = hf.mean(dim=-1, keepdim=True) / (mt[:, :, :64].mean(dim=-1, keepdim=True) + 1e-8)
    hammarberg = spec_max / (hf.max(dim=-1, keepdim=True).values + 1e-8)
    slope = torch.zeros(B, T, 1, device=device)
    features.append(torch.cat(mod_features + [mod_centroid, mod_bandwidth,
                                sharpness_z, fluct_str, loudness_aw,
                                alpha_ratio, hammarberg, slope], dim=-1))  # 14D

    # Concatenate all → (B, T, 97)
    r3 = torch.cat(features, dim=-1)

    # Ensure exactly 97D (pad or trim)
    if r3.shape[-1] > 97:
        r3 = r3[:, :, :97]
    elif r3.shape[-1] < 97:
        pad = torch.zeros(B, T, 97 - r3.shape[-1], device=device)
        r3 = torch.cat([r3, pad], dim=-1)

    # Normalize to [0, 1] per dimension
    r3_min = r3.min(dim=1, keepdim=True).values
    r3_max = r3.max(dim=1, keepdim=True).values
    r3_range = r3_max - r3_min
    r3 = torch.where(r3_range > 0, (r3 - r3_min) / r3_range, torch.zeros_like(r3))

    return r3


def _extract_h3_proxy(r3: torch.Tensor, device: torch.device) -> torch.Tensor:
    """Multi-scale temporal statistics as H³ proxy."""
    B, T, D = r3.shape

    horizons = [4, 8, 16, 32, 64, 128, 256]
    morphs = []  # (B, T, n_features)

    for h in horizons:
        if h >= T:
            # Pad with zeros for this horizon
            morphs.append(torch.zeros(B, T, D * 3, device=device))
            continue

        # Causal rolling stats (backward-looking)
        # Using unfold for efficient rolling windows
        padded = torch.nn.functional.pad(r3.transpose(1, 2), (h - 1, 0), mode='replicate')
        windows = padded.unfold(2, h, 1)  # (B, D, T, h)

        mean = windows.mean(dim=-1).transpose(1, 2)  # (B, T, D)
        std = windows.std(dim=-1).transpose(1, 2)     # (B, T, D)
        # Velocity (diff of mean)
        vel = torch.zeros_like(mean)
        vel[:, 1:] = mean[:, 1:] - mean[:, :-1]

        morphs.append(torch.cat([mean, std, vel], dim=-1))  # (B, T, D*3)

    h3 = torch.cat(morphs, dim=-1)  # (B, T, 97*3*7 = 2037)

    # Reduce to manageable size via linear projection
    # Target: ~637 dimensions (matching config)
    n_h3 = 637
    if h3.shape[-1] > n_h3:
        # PCA-like reduction: take first n_h3 dims
        h3 = h3[:, :, :n_h3]

    # Normalize
    h3_min = h3.min(dim=1, keepdim=True).values
    h3_max = h3.max(dim=1, keepdim=True).values
    h3_range = h3_max - h3_min
    h3 = torch.where(h3_range > 0, (h3 - h3_min) / h3_range, torch.zeros_like(h3))

    return h3


def _extract_belief_proxy(r3: torch.Tensor, h3: torch.Tensor, device: torch.device) -> torch.Tensor:
    """Derive 131 belief proxies from R³ + H³ features."""
    B, T, _ = r3.shape

    # Combine R³ and H³
    combined = torch.cat([r3, h3[:, :, :64]], dim=-1)  # Use first 64 H³ dims

    # F1-F9 belief mapping (131 beliefs across 9 functions)
    # Each function derives beliefs from relevant R³ groups
    beliefs = []

    # F1: Sensory (17) — from R³ groups A,B,C,D
    f1 = torch.cat([r3[:, :, :25], r3[:, :, :1].expand(B, T, 1)], dim=-1)[:, :, :17]
    # Pad if needed
    if f1.shape[-1] < 17:
        f1 = torch.cat([f1, torch.zeros(B, T, 17 - f1.shape[-1], device=device)], dim=-1)
    beliefs.append(torch.sigmoid(f1))

    # F2: Prediction (15) — temporal patterns from H³
    f2 = h3[:, :, :15]
    beliefs.append(torch.sigmoid(f2))

    # F3: Attention (15) — salience from R³ energy + change
    f3 = torch.cat([r3[:, :, 7:12], r3[:, :, 21:25], h3[:, :, 15:21]], dim=-1)[:, :, :15]
    if f3.shape[-1] < 15:
        f3 = torch.cat([f3, torch.zeros(B, T, 15 - f3.shape[-1], device=device)], dim=-1)
    beliefs.append(torch.sigmoid(f3))

    # F4: Memory (13) — context from H³ macro horizons
    f4 = h3[:, :, 21:34]
    if f4.shape[-1] < 13:
        f4 = torch.cat([f4, torch.zeros(B, T, 13 - f4.shape[-1], device=device)], dim=-1)
    beliefs.append(torch.sigmoid(f4))

    # F5: Emotion (14) — from harmony + timbre + dynamics
    f5 = torch.cat([r3[:, :, 51:63], r3[:, :, 7:9]], dim=-1)[:, :, :14]
    if f5.shape[-1] < 14:
        f5 = torch.cat([f5, torch.zeros(B, T, 14 - f5.shape[-1], device=device)], dim=-1)
    beliefs.append(torch.sigmoid(f5))

    # F6: Reward (16) — prediction error + resolution
    pe = (h3[:, :, :16] - h3[:, :, 16:32]).abs() if h3.shape[-1] >= 32 else torch.zeros(B, T, 16, device=device)
    beliefs.append(torch.sigmoid(pe[:, :, :16]))

    # F7: Motor (17) — rhythm + groove
    f7 = torch.cat([r3[:, :, 41:51], h3[:, :, 34:41]], dim=-1)[:, :, :17]
    if f7.shape[-1] < 17:
        f7 = torch.cat([f7, torch.zeros(B, T, 17 - f7.shape[-1], device=device)], dim=-1)
    beliefs.append(torch.sigmoid(f7))

    # F8: Learning (14) — plasticity signals
    f8 = torch.cat([h3[:, :, 41:50], r3[:, :, 83:88]], dim=-1)[:, :, :14]
    if f8.shape[-1] < 14:
        f8 = torch.cat([f8, torch.zeros(B, T, 14 - f8.shape[-1], device=device)], dim=-1)
    beliefs.append(torch.sigmoid(f8))

    # F9: Social (10) — entrainment + synchrony
    f9 = h3[:, :, 50:60]
    if f9.shape[-1] < 10:
        f9 = torch.cat([f9, torch.zeros(B, T, 10 - f9.shape[-1], device=device)], dim=-1)
    beliefs.append(torch.sigmoid(f9))

    all_beliefs = torch.cat(beliefs, dim=-1)  # (B, T, 131)
    return all_beliefs


def _beliefs_to_dims(beliefs: torch.Tensor) -> torch.Tensor:
    """Map 131 beliefs → 10 dimensions (5+5 dual radar)."""
    B, T, _ = beliefs.shape

    # Musical dimensions (from relevant belief groups)
    speed = beliefs[:, :, 90:97].mean(dim=-1, keepdim=True)     # F7 motor/tempo
    volume = beliefs[:, :, 0:5].mean(dim=-1, keepdim=True)       # F1 sensory energy
    weight = beliefs[:, :, 5:12].mean(dim=-1, keepdim=True)      # F1 sensory timbre
    texture = beliefs[:, :, 60:68].mean(dim=-1, keepdim=True)    # F5 emotion texture
    depth = beliefs[:, :, 47:55].mean(dim=-1, keepdim=True)      # F4 memory depth

    # Emotional dimensions
    mood = beliefs[:, :, 68:74].mean(dim=-1, keepdim=True)       # F5 valence
    energy = beliefs[:, :, 32:40].mean(dim=-1, keepdim=True)     # F3 arousal/attention
    hardness = beliefs[:, :, 12:17].mean(dim=-1, keepdim=True)   # F1+F2 spectral
    predictability = beliefs[:, :, 17:28].mean(dim=-1, keepdim=True)  # F2 prediction
    focus = beliefs[:, :, 74:82].mean(dim=-1, keepdim=True)      # F6 reward/engagement

    dims = torch.cat([speed, volume, weight, texture, depth,
                       mood, energy, hardness, predictability, focus], dim=-1)
    return dims


# ======================================================================
# STEP 2: Generate all NPZ + JSON
# ======================================================================

def generate_training_data(segments_dir: str, output_dir: str, device: torch.device):
    """Process all segments → NPZ + temporal JSON."""
    seg_dir = Path(segments_dir)
    out_dir = Path(output_dir)
    npz_dir = out_dir / "npz"
    json_dir = out_dir / "temporal_json"
    npz_dir.mkdir(parents=True, exist_ok=True)
    json_dir.mkdir(parents=True, exist_ok=True)

    wav_files = sorted([f for f in seg_dir.iterdir() if f.suffix == ".wav"])
    print(f"\n=== Generating NPZ + JSON from {len(wav_files)} segments ===", flush=True)
    print(f"  Output: {out_dir}", flush=True)

    # Check for existing progress
    manifest_path = out_dir / "manifest.json"
    existing = set()
    if manifest_path.exists():
        with open(manifest_path) as f:
            existing = set(json.load(f))

    manifest = list(existing)
    t0 = time.time()

    for i, wav_path in enumerate(wav_files, 1):
        name = wav_path.stem

        if name in existing:
            if i % 100 == 0:
                print(f"  [{i:4d}/{len(wav_files)}] SKIP (exists)", flush=True)
            continue

        try:
            # Generate mel
            mel = wav_to_mel(str(wav_path), device)

            # Run MI pipeline
            data = run_mi_pipeline(mel, device)

            # Save NPZ
            np.savez_compressed(
                str(npz_dir / f"{name}.npz"),
                mel=data["mel"],       # (128, T)
                r3=data["r3"],         # (T, 97)
                h3=data["h3"],         # (T, N_h3)
                beliefs=data["beliefs"],  # (T, 131)
                dims=data["dims"],     # (T, 10)
            )

            # Save temporal JSON (5+5D per frame)
            T = data["dims"].shape[0]
            frames = []
            for t in range(T):
                frame = {
                    "frame": t,
                    "time_s": round(t / FRAME_RATE, 4),
                }
                for d, dim_name in enumerate(DIM_NAMES):
                    frame[dim_name] = round(float(data["dims"][t, d]), 4)
                frames.append(frame)

            json_out = {
                "segment": name,
                "sample_rate": SAMPLE_RATE,
                "hop_length": HOP_LENGTH,
                "frame_rate_hz": round(FRAME_RATE, 2),
                "n_frames": T,
                "duration_s": round(T / FRAME_RATE, 2),
                "dimensions": {
                    "musical": DIM_NAMES[:5],
                    "emotional": DIM_NAMES[5:],
                },
                "frames": frames,
            }
            with open(json_dir / f"{name}.json", "w") as f:
                json.dump(json_out, f, indent=1, ensure_ascii=False)

            manifest.append(name)

            if i % 50 == 0 or i == len(wav_files):
                elapsed = time.time() - t0
                rate = i / elapsed
                eta = (len(wav_files) - i) / rate
                print(f"  [{i:4d}/{len(wav_files)}] {name[:60]}  "
                      f"({rate:.1f} seg/s, ETA {eta:.0f}s)", flush=True)

                # Save manifest
                with open(manifest_path, "w") as f:
                    json.dump(manifest, f)

        except Exception as e:
            print(f"  [{i:4d}/{len(wav_files)}] ERROR: {name} — {e}", flush=True)
            continue

    # Final manifest
    with open(manifest_path, "w") as f:
        json.dump(manifest, f)

    elapsed = time.time() - t0
    print(f"\n  Done: {len(manifest)} segments in {elapsed:.0f}s", flush=True)
    print(f"  NPZ:  {npz_dir}", flush=True)
    print(f"  JSON: {json_dir}", flush=True)

    return manifest


# ======================================================================
# MAIN
# ======================================================================

def main():
    parser = argparse.ArgumentParser(description="MI RunPod Full Pipeline")
    parser.add_argument("--segments", default="/workspace/segments", help="Segmented WAV dir")
    parser.add_argument("--training-data", default="/workspace/training_data", help="NPZ output dir")
    parser.add_argument("--output", default="/workspace/training_output", help="Training output dir")
    parser.add_argument("--step", choices=["all", "npz", "train", "export"], default="all")
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--batch-size", type=int, default=256)
    args = parser.parse_args()

    device = (
        torch.device("cuda") if torch.cuda.is_available()
        else torch.device("mps") if torch.backends.mps.is_available()
        else torch.device("cpu")
    )
    print(f"=== MI RunPod Full Pipeline ===", flush=True)
    print(f"  Device: {device}", flush=True)
    print(f"  Segments: {args.segments}", flush=True)
    print(f"  Step: {args.step}", flush=True)

    # Step 1: Generate NPZ + JSON
    if args.step in ("all", "npz", "export"):
        generate_training_data(args.segments, args.training_data, device)

    # Step 2: Train
    if args.step in ("all", "train"):
        print(f"\n=== Starting Training ===", flush=True)
        train_cmd = (
            f"python3 {PROJECT_ROOT}/Training/train.py "
            f"--data-dir {args.training_data}/npz "
            f"--output-dir {args.output} "
            f"--epochs {args.epochs} "
            f"--batch-size {args.batch_size}"
        )
        print(f"  {train_cmd}", flush=True)
        os.system(train_cmd)

    print(f"\n=== Pipeline Complete ===", flush=True)


if __name__ == "__main__":
    main()
