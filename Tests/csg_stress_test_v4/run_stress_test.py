#!/usr/bin/env python3
"""CSG Mechanism Stress Test v4.0

Comprehensive stress test for the Consonance-Salience Gradient (CSG) mechanism.
Runs ALL audio files through the full MI pipeline and extracts:
- Per-dimension temporal traces (12D: E0-E2, M0-M2, P0-P2, F0-F2)
- H³ demand tuple decomposition (18 tuples × horizon × morph × law)
- Belief decomposition (band/law ablation for all 5 CSG beliefs)
- Boundary artifact analysis (edge frame detection)
- Cross-audio comparative analysis

All data stored as JSON in Tests/csg_stress_test_v4/results/

Usage:
    cd "/Volumes/SRC-9/SRC Musical Intelligence"
    python -m Tests.csg_stress_test_v4.run_stress_test
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
TEST_DIR = Path(__file__).resolve().parent
RESULTS_DIR = TEST_DIR / "results"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Backend imports
sys.path.insert(0, str(PROJECT_ROOT / "Lab"))
from backend.config import AUDIO_CATALOG, MIDI_CATALOG, FRAME_RATE
from backend.pipeline import MIPipeline, ExperimentResult
from backend.belief_decomposition import (
    compute_belief_decomposition,
    _get_mechanism_h3_keys,
    _filter_h3_by_horizon,
    _filter_h3_by_law,
    _filter_h3_by_band,
    _zero_pad_missing,
    HORIZON_BANDS,
    BAND_ORDER,
    LAW_ORDER,
    LAW_NAMES,
)
from backend.beliefs import get_beliefs_registry, build_dim_lookup


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class NumpyEncoder(json.JSONEncoder):
    """JSON encoder that handles numpy types."""
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, (np.float32, np.float64)):
            return float(obj)
        if isinstance(obj, (np.int32, np.int64)):
            return int(obj)
        if isinstance(obj, np.bool_):
            return bool(obj)
        return super().default(obj)


def save_json(data: Any, path: Path, label: str = "") -> None:
    """Save data as JSON with numpy support."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, cls=NumpyEncoder, indent=2, ensure_ascii=False)
    size_kb = path.stat().st_size / 1024
    print(f"  [{label}] Saved: {path.name} ({size_kb:.1f} KB)")


def temporal_stats(trace: np.ndarray) -> Dict[str, Any]:
    """Compute comprehensive temporal statistics for a 1D trace."""
    if len(trace) == 0:
        return {"empty": True}

    # Basic stats
    stats: Dict[str, Any] = {
        "n_frames": len(trace),
        "duration_s": round(len(trace) / FRAME_RATE, 3),
        "mean": round(float(np.mean(trace)), 6),
        "std": round(float(np.std(trace)), 6),
        "min": round(float(np.min(trace)), 6),
        "max": round(float(np.max(trace)), 6),
        "range": round(float(np.ptp(trace)), 6),
        "median": round(float(np.median(trace)), 6),
    }

    # Quartiles
    q25, q75 = np.percentile(trace, [25, 75])
    stats["q25"] = round(float(q25), 6)
    stats["q75"] = round(float(q75), 6)
    stats["iqr"] = round(float(q75 - q25), 6)

    # Temporal dynamics
    if len(trace) > 1:
        velocity = np.diff(trace)
        stats["velocity_mean"] = round(float(np.mean(velocity)), 6)
        stats["velocity_std"] = round(float(np.std(velocity)), 6)
        stats["velocity_max"] = round(float(np.max(np.abs(velocity))), 6)

        # Acceleration
        if len(trace) > 2:
            accel = np.diff(velocity)
            stats["accel_mean"] = round(float(np.mean(accel)), 6)
            stats["accel_std"] = round(float(np.std(accel)), 6)

    # Temporal segments (divide into 10 windows)
    n_windows = min(10, len(trace))
    window_size = len(trace) // n_windows
    if window_size > 0:
        windowed_means = []
        for i in range(n_windows):
            start = i * window_size
            end = start + window_size if i < n_windows - 1 else len(trace)
            windowed_means.append(round(float(np.mean(trace[start:end])), 6))
        stats["temporal_windows"] = windowed_means

    # Edge analysis (first/last 4 frames vs interior)
    edge_frames = min(4, len(trace) // 4)
    if edge_frames > 0 and len(trace) > edge_frames * 4:
        interior = trace[edge_frames:-edge_frames]
        stats["edge_first_4"] = round(float(np.mean(trace[:edge_frames])), 6)
        stats["edge_last_4"] = round(float(np.mean(trace[-edge_frames:])), 6)
        stats["interior_mean"] = round(float(np.mean(interior)), 6)
        stats["edge_deviation_first"] = round(
            float(np.mean(trace[:edge_frames]) - np.mean(interior)), 6
        )
        stats["edge_deviation_last"] = round(
            float(np.mean(trace[-edge_frames:]) - np.mean(interior)), 6
        )

    return stats


def temporal_trace_export(trace: np.ndarray, downsample: int = 1) -> List[float]:
    """Export a temporal trace as list, optionally downsampled."""
    if downsample > 1:
        # Take every nth sample
        return [round(float(v), 6) for v in trace[::downsample]]
    return [round(float(v), 6) for v in trace]


# ---------------------------------------------------------------------------
# CSG-specific constants
# ---------------------------------------------------------------------------

CSG_DIMENSIONS = [
    "E0:salience_activation",
    "E1:sensory_evidence",
    "E2:consonance_valence",
    "M0:salience_response",
    "M1:rt_valence_judgment",
    "M2:aesthetic_appreciation",
    "P0:salience_network",
    "P1:affective_evaluation",
    "P2:sensory_load",
    "F0:valence_pred",
    "F1:processing_pred",
    "F2:aesthetic_pred",
]

CSG_LAYERS = {
    "E": {"name": "Extraction", "scope": "internal", "dims": [0, 1, 2]},
    "M": {"name": "Memory", "scope": "internal", "dims": [3, 4, 5]},
    "P": {"name": "Present", "scope": "hybrid", "dims": [6, 7, 8]},
    "F": {"name": "Forecast", "scope": "external", "dims": [9, 10, 11]},
}

CSG_BELIEFS = [
    "consonance_salience_gradient",
    "salience_network_activation",
    "sensory_load",
    "consonance_valence_mapping",
    "processing_load_pred",
]

# Activation ranges for validation
DIM_RANGES = {
    "E0": (0.0, 1.0),   # sigmoid
    "E1": (0.0, 1.0),   # sigmoid
    "E2": (-1.0, 1.0),  # tanh
    "M0": (0.0, 1.0),   # sigmoid
    "M1": (0.0, 1.0),   # sigmoid
    "M2": (0.0, 1.0),   # sigmoid
    "P0": (0.0, 1.0),   # sigmoid
    "P1": (-1.0, 1.0),  # tanh
    "P2": (0.0, 1.0),   # sigmoid
    "F0": (-1.0, 1.0),  # tanh
    "F1": (0.0, 1.0),   # sigmoid
    "F2": (0.0, 1.0),   # sigmoid
}


# ---------------------------------------------------------------------------
# STAGE 1: Full pipeline extraction
# ---------------------------------------------------------------------------

def stage_1_extraction(
    pipeline: MIPipeline,
    audio_keys: List[str],
) -> Dict[str, ExperimentResult]:
    """Run full pipeline on all audio files, export raw data as JSON."""
    print("\n" + "=" * 72)
    print("STAGE 1: Full Pipeline Extraction")
    print("=" * 72)

    stage_dir = RESULTS_DIR / "stage_1_extraction"
    stage_dir.mkdir(parents=True, exist_ok=True)

    results: Dict[str, ExperimentResult] = {}
    stage_report: Dict[str, Any] = {
        "stage": "1_extraction",
        "timestamp": datetime.now().isoformat(),
        "n_audio": len(audio_keys),
        "audio_keys": audio_keys,
        "results": {},
    }

    for i, key in enumerate(audio_keys):
        print(f"\n  [{i+1}/{len(audio_keys)}] Processing: {key}")
        t0 = time.perf_counter()

        try:
            result = pipeline.run(key, excerpt_s=30.0)
            elapsed = time.perf_counter() - t0
            results[key] = result

            # CSG relay data
            csg_relay = result.relays.get("CSG")
            if csg_relay is None:
                print(f"    WARNING: No CSG relay data for {key}")
                continue

            T, D = csg_relay.shape
            print(f"    OK: {T} frames, {D}D, {result.duration_s:.1f}s, {result.fps:.0f} fps, {elapsed:.1f}s")

            # Per-dimension data export
            audio_data: Dict[str, Any] = {
                "audio_name": key,
                "n_frames": T,
                "duration_s": round(result.duration_s, 3),
                "fps": round(result.fps, 1),
                "elapsed_s": round(elapsed, 2),
                "csg_output_dim": D,
                "dimensions": {},
            }

            for d_idx, d_name in enumerate(CSG_DIMENSIONS):
                if d_idx >= D:
                    break
                trace = csg_relay[:, d_idx]
                audio_data["dimensions"][d_name] = {
                    "index": d_idx,
                    "stats": temporal_stats(trace),
                    "trace": temporal_trace_export(trace),
                }

            # R³ inputs used by CSG
            r3_indices = [0, 1, 4, 9, 10, 12, 17, 21, 22]
            r3_names = [
                "roughness", "sethares_dissonance", "sensory_pleasantness",
                "spectral_centroid", "loudness", "warmth",
                "spectral_autocorrelation", "spectral_flux", "energy_change",
            ]
            audio_data["r3_inputs"] = {}
            for r3_idx, r3_name in zip(r3_indices, r3_names):
                if r3_idx < result.r3.shape[1]:
                    r3_trace = result.r3[:, r3_idx]
                    audio_data["r3_inputs"][r3_name] = {
                        "r3_index": r3_idx,
                        "stats": temporal_stats(r3_trace),
                        "trace": temporal_trace_export(r3_trace),
                    }

            # H³ tuples relevant to CSG
            csg_h3_keys = set()
            for n in pipeline.nuclei:
                if n.NAME == "CSG":
                    for spec in n.h3_demand:
                        csg_h3_keys.add(spec.as_tuple())
                    break

            audio_data["h3_demands"] = {
                "n_tuples": len(csg_h3_keys),
                "tuples": {},
            }
            for t_idx, h3_key in enumerate(sorted(csg_h3_keys)):
                tuple_str = f"({h3_key[0]},{h3_key[1]},{h3_key[2]},{h3_key[3]})"
                # Find this tuple in result.h3_tuples
                if h3_key in result.h3_tuples:
                    h3_idx = result.h3_tuples.index(h3_key)
                    h3_trace = result.h3_data[h3_idx]
                    audio_data["h3_demands"]["tuples"][tuple_str] = {
                        "r3_idx": h3_key[0],
                        "horizon": h3_key[1],
                        "morph": h3_key[2],
                        "law": h3_key[3],
                        "stats": temporal_stats(h3_trace),
                        "trace": temporal_trace_export(h3_trace),
                    }

            # Belief values
            audio_data["beliefs"] = {}
            beliefs_reg = get_beliefs_registry()
            for b in beliefs_reg:
                if b["name"] in CSG_BELIEFS:
                    b_idx = b["index"]
                    if b_idx < result.beliefs.shape[1]:
                        b_trace = result.beliefs[:, b_idx]
                        audio_data["beliefs"][b["name"]] = {
                            "index": b_idx,
                            "type": b["type"],
                            "stats": temporal_stats(b_trace),
                            "trace": temporal_trace_export(b_trace),
                        }

            save_json(audio_data, stage_dir / f"{key.replace('/', '_')}.json", key)

            # Summary for stage report
            stage_report["results"][key] = {
                "n_frames": T,
                "duration_s": round(result.duration_s, 3),
                "fps": round(result.fps, 1),
                "elapsed_s": round(elapsed, 2),
                "dim_stats": {
                    d_name: {
                        "mean": audio_data["dimensions"][d_name]["stats"]["mean"],
                        "std": audio_data["dimensions"][d_name]["stats"]["std"],
                        "range": [
                            audio_data["dimensions"][d_name]["stats"]["min"],
                            audio_data["dimensions"][d_name]["stats"]["max"],
                        ],
                    }
                    for d_name in CSG_DIMENSIONS
                    if d_name in audio_data["dimensions"]
                },
            }

        except Exception as e:
            print(f"    ERROR: {e}")
            stage_report["results"][key] = {"error": str(e)}

    save_json(stage_report, stage_dir / "_stage_1_report.json", "STAGE 1")
    print(f"\n  STAGE 1 COMPLETE: {len(results)}/{len(audio_keys)} audio files processed")
    return results


# ---------------------------------------------------------------------------
# STAGE 2: Per-dimension temporal analysis
# ---------------------------------------------------------------------------

def stage_2_dimension_analysis(
    results: Dict[str, ExperimentResult],
) -> None:
    """Deep temporal analysis per CSG dimension across all audio."""
    print("\n" + "=" * 72)
    print("STAGE 2: Per-Dimension Temporal Analysis")
    print("=" * 72)

    stage_dir = RESULTS_DIR / "stage_2_dimensions"
    stage_dir.mkdir(parents=True, exist_ok=True)

    report: Dict[str, Any] = {
        "stage": "2_dimensions",
        "timestamp": datetime.now().isoformat(),
        "n_dimensions": 12,
        "dimensions": {},
        "validation": {},
    }

    for d_idx, d_name in enumerate(CSG_DIMENSIONS):
        dim_code = d_name.split(":")[0]  # "E0", "M1", etc.
        expected_range = DIM_RANGES[dim_code]
        layer_code = dim_code[0]
        layer_info = CSG_LAYERS[layer_code]

        dim_report: Dict[str, Any] = {
            "index": d_idx,
            "full_name": d_name,
            "code": dim_code,
            "layer": layer_code,
            "layer_name": layer_info["name"],
            "scope": layer_info["scope"],
            "expected_range": list(expected_range),
            "per_audio": {},
            "cross_audio": {},
        }

        all_means = []
        all_stds = []
        all_edge_devs_first = []
        all_edge_devs_last = []
        violations = []

        for audio_key, result in results.items():
            csg = result.relays.get("CSG")
            if csg is None or d_idx >= csg.shape[1]:
                continue

            trace = csg[:, d_idx]
            stats = temporal_stats(trace)
            dim_report["per_audio"][audio_key] = stats

            all_means.append(stats["mean"])
            all_stds.append(stats["std"])

            if "edge_deviation_first" in stats:
                all_edge_devs_first.append(stats["edge_deviation_first"])
            if "edge_deviation_last" in stats:
                all_edge_devs_last.append(stats["edge_deviation_last"])

            # Range validation
            if stats["min"] < expected_range[0] - 0.001:
                violations.append({
                    "audio": audio_key,
                    "type": "below_min",
                    "value": stats["min"],
                    "expected_min": expected_range[0],
                })
            if stats["max"] > expected_range[1] + 0.001:
                violations.append({
                    "audio": audio_key,
                    "type": "above_max",
                    "value": stats["max"],
                    "expected_max": expected_range[1],
                })

            # Dead signal check (std < 0.001)
            if stats["std"] < 0.001:
                violations.append({
                    "audio": audio_key,
                    "type": "dead_signal",
                    "std": stats["std"],
                })

        # Cross-audio aggregation
        if all_means:
            dim_report["cross_audio"] = {
                "mean_of_means": round(float(np.mean(all_means)), 6),
                "std_of_means": round(float(np.std(all_means)), 6),
                "mean_of_stds": round(float(np.mean(all_stds)), 6),
                "range_of_means": [
                    round(float(np.min(all_means)), 6),
                    round(float(np.max(all_means)), 6),
                ],
            }
            if all_edge_devs_first:
                dim_report["cross_audio"]["mean_edge_dev_first"] = round(
                    float(np.mean(all_edge_devs_first)), 6
                )
            if all_edge_devs_last:
                dim_report["cross_audio"]["mean_edge_dev_last"] = round(
                    float(np.mean(all_edge_devs_last)), 6
                )

        dim_report["violations"] = violations
        dim_report["n_violations"] = len(violations)
        report["dimensions"][d_name] = dim_report

        # Validation summary
        status = "PASS" if len(violations) == 0 else "FAIL"
        print(f"  {dim_code:3s} | {d_name.split(':')[1]:25s} | "
              f"mean={np.mean(all_means):+.4f} | std={np.mean(all_stds):.4f} | {status}")
        if violations:
            for v in violations:
                print(f"       VIOLATION: {v['audio']} — {v['type']}: {v.get('value', v.get('std', ''))}")

    # Overall validation
    total_violations = sum(
        d["n_violations"] for d in report["dimensions"].values()
    )
    report["validation"] = {
        "total_violations": total_violations,
        "status": "PASS" if total_violations == 0 else "FAIL",
    }

    save_json(report, stage_dir / "_stage_2_report.json", "STAGE 2")
    print(f"\n  STAGE 2 COMPLETE: {total_violations} violations")


# ---------------------------------------------------------------------------
# STAGE 3: H³ demand tuple decomposition
# ---------------------------------------------------------------------------

def stage_3_h3_decomposition(
    pipeline: MIPipeline,
    results: Dict[str, ExperimentResult],
) -> None:
    """Decompose CSG output by H³ tuples, horizons, morphs, and laws."""
    print("\n" + "=" * 72)
    print("STAGE 3: H³ Demand Tuple Decomposition")
    print("=" * 72)

    import torch

    stage_dir = RESULTS_DIR / "stage_3_h3_decomposition"
    stage_dir.mkdir(parents=True, exist_ok=True)

    # Get CSG mechanism instance
    csg_mechanism = None
    for n in pipeline.nuclei:
        if n.NAME == "CSG":
            csg_mechanism = n
            break

    if csg_mechanism is None:
        print("  ERROR: CSG mechanism not found")
        return

    csg_h3_keys = _get_mechanism_h3_keys(csg_mechanism)
    print(f"  CSG H³ demands: {len(csg_h3_keys)} tuples")

    report: Dict[str, Any] = {
        "stage": "3_h3_decomposition",
        "timestamp": datetime.now().isoformat(),
        "n_tuples": len(csg_h3_keys),
        "tuples_sorted": [list(k) for k in sorted(csg_h3_keys)],
        "per_audio": {},
    }

    for audio_key, result in results.items():
        print(f"\n  [{audio_key}] Decomposing H³ demands...")

        # We need the H³ features dict and R³ tensor
        # Re-run R³ + H³ to get the raw feature dicts (not available in ExperimentResult)
        # Instead, reconstruct from h3_tuples + h3_data
        T = result.n_frames
        h3_features = {}
        for i, key_tuple in enumerate(result.h3_tuples):
            h3_features[key_tuple] = torch.from_numpy(
                result.h3_data[i:i+1]  # (1, T) — batch dim
            )
        r3_tensor = torch.from_numpy(result.r3).unsqueeze(0)  # (1, T, 97)

        # Scope to CSG's demands
        mech_h3 = {k: v for k, v in h3_features.items() if k in csg_h3_keys}

        audio_decomp: Dict[str, Any] = {
            "n_frames": T,
            "duration_s": round(result.duration_s, 3),
        }

        # --- Per-tuple ablation ---
        # For each tuple, run CSG with ONLY that tuple (others zeroed)
        tuple_contributions: Dict[str, Any] = {}
        ref = next(iter(mech_h3.values()))

        for h3_key in sorted(csg_h3_keys):
            single = {h3_key: mech_h3[h3_key]}
            padded = _zero_pad_missing(single, csg_h3_keys, ref)
            with torch.no_grad():
                out = csg_mechanism.compute(padded, r3_tensor)
            out_np = out[0].cpu().numpy()  # (T, 12)

            tuple_str = f"({h3_key[0]},{h3_key[1]},{h3_key[2]},{h3_key[3]})"
            per_dim = {}
            for d_idx, d_name in enumerate(CSG_DIMENSIONS):
                if d_idx < out_np.shape[1]:
                    per_dim[d_name] = temporal_stats(out_np[:, d_idx])
                    per_dim[d_name]["trace"] = temporal_trace_export(out_np[:, d_idx])

            tuple_contributions[tuple_str] = {
                "r3_idx": h3_key[0],
                "horizon": h3_key[1],
                "morph": h3_key[2],
                "law": h3_key[3],
                "dimensions": per_dim,
            }

        audio_decomp["per_tuple"] = tuple_contributions

        # --- Per-horizon ablation ---
        horizons_used = sorted({k[1] for k in csg_h3_keys})
        horizon_contributions: Dict[str, Any] = {}
        for h_idx in horizons_used:
            filtered = _filter_h3_by_horizon(mech_h3, h_idx)
            padded = _zero_pad_missing(filtered, csg_h3_keys, ref)
            with torch.no_grad():
                out = csg_mechanism.compute(padded, r3_tensor)
            out_np = out[0].cpu().numpy()

            per_dim = {}
            for d_idx, d_name in enumerate(CSG_DIMENSIONS):
                if d_idx < out_np.shape[1]:
                    per_dim[d_name] = temporal_stats(out_np[:, d_idx])
                    per_dim[d_name]["trace"] = temporal_trace_export(out_np[:, d_idx])

            horizon_contributions[f"H{h_idx}"] = {
                "horizon_idx": h_idx,
                "n_tuples": len(filtered),
                "dimensions": per_dim,
            }

        audio_decomp["per_horizon"] = horizon_contributions

        # --- Per-band ablation ---
        band_contributions: Dict[str, Any] = {}
        for band_name in BAND_ORDER:
            filtered = _filter_h3_by_band(mech_h3, HORIZON_BANDS[band_name])
            if not filtered:
                continue
            padded = _zero_pad_missing(filtered, csg_h3_keys, ref)
            with torch.no_grad():
                out = csg_mechanism.compute(padded, r3_tensor)
            out_np = out[0].cpu().numpy()

            per_dim = {}
            for d_idx, d_name in enumerate(CSG_DIMENSIONS):
                if d_idx < out_np.shape[1]:
                    per_dim[d_name] = temporal_stats(out_np[:, d_idx])
                    per_dim[d_name]["trace"] = temporal_trace_export(out_np[:, d_idx])

            band_contributions[band_name] = {
                "n_tuples": len(filtered),
                "dimensions": per_dim,
            }

        audio_decomp["per_band"] = band_contributions

        # --- Per-law ablation ---
        law_contributions: Dict[str, Any] = {}
        for law_idx in LAW_ORDER:
            filtered = _filter_h3_by_law(mech_h3, law_idx)
            if not filtered:
                continue
            padded = _zero_pad_missing(filtered, csg_h3_keys, ref)
            with torch.no_grad():
                out = csg_mechanism.compute(padded, r3_tensor)
            out_np = out[0].cpu().numpy()

            per_dim = {}
            for d_idx, d_name in enumerate(CSG_DIMENSIONS):
                if d_idx < out_np.shape[1]:
                    per_dim[d_name] = temporal_stats(out_np[:, d_idx])
                    per_dim[d_name]["trace"] = temporal_trace_export(out_np[:, d_idx])

            law_contributions[f"L{law_idx}_{LAW_NAMES[law_idx]}"] = {
                "law_idx": law_idx,
                "n_tuples": len(filtered),
                "dimensions": per_dim,
            }

        audio_decomp["per_law"] = law_contributions

        # --- Full baseline (all tuples) for reference ---
        with torch.no_grad():
            full_out = csg_mechanism.compute(mech_h3, r3_tensor)
        full_np = full_out[0].cpu().numpy()
        baseline_dims = {}
        for d_idx, d_name in enumerate(CSG_DIMENSIONS):
            if d_idx < full_np.shape[1]:
                baseline_dims[d_name] = temporal_stats(full_np[:, d_idx])
        audio_decomp["full_baseline"] = baseline_dims

        report["per_audio"][audio_key] = {"summary": {
            "n_frames": T,
            "n_horizons": len(horizons_used),
            "horizons_used": horizons_used,
            "n_bands_active": len(band_contributions),
            "n_laws_active": len(law_contributions),
        }}

        save_json(audio_decomp, stage_dir / f"{audio_key.replace('/', '_')}.json", audio_key)

    save_json(report, stage_dir / "_stage_3_report.json", "STAGE 3")
    print(f"\n  STAGE 3 COMPLETE: {len(results)} audio files decomposed")


# ---------------------------------------------------------------------------
# STAGE 4: Boundary artifact & edge analysis
# ---------------------------------------------------------------------------

def stage_4_boundary_analysis(
    results: Dict[str, ExperimentResult],
) -> None:
    """Analyze boundary artifacts in CSG dimensions."""
    print("\n" + "=" * 72)
    print("STAGE 4: Boundary Artifact & Edge Analysis")
    print("=" * 72)

    stage_dir = RESULTS_DIR / "stage_4_boundary"
    stage_dir.mkdir(parents=True, exist_ok=True)

    EDGE_FRAMES = 8  # Analyze first/last 8 frames (~46ms at 172 Hz)
    ARTIFACT_THRESHOLD = 0.05  # Deviation > 5% of interior range is flagged

    report: Dict[str, Any] = {
        "stage": "4_boundary",
        "timestamp": datetime.now().isoformat(),
        "edge_frames_analyzed": EDGE_FRAMES,
        "artifact_threshold": ARTIFACT_THRESHOLD,
        "per_audio": {},
        "summary": {},
    }

    total_artifacts = 0
    total_checks = 0

    for audio_key, result in results.items():
        csg = result.relays.get("CSG")
        if csg is None:
            continue

        T = csg.shape[0]
        if T < EDGE_FRAMES * 4:
            print(f"  [{audio_key}] Too short ({T} frames), skipping")
            continue

        audio_report: Dict[str, Any] = {
            "n_frames": T,
            "dimensions": {},
            "artifacts_found": 0,
        }

        for d_idx, d_name in enumerate(CSG_DIMENSIONS):
            if d_idx >= csg.shape[1]:
                break

            trace = csg[:, d_idx]
            interior = trace[EDGE_FRAMES:-EDGE_FRAMES]
            interior_mean = float(np.mean(interior))
            interior_std = float(np.std(interior))
            interior_range = float(np.ptp(interior))

            first_edge = trace[:EDGE_FRAMES]
            last_edge = trace[-EDGE_FRAMES:]

            first_mean = float(np.mean(first_edge))
            last_mean = float(np.mean(last_edge))

            first_dev = first_mean - interior_mean
            last_dev = last_mean - interior_mean

            # Flag artifact if deviation exceeds threshold relative to interior range
            ref_range = max(interior_range, 0.01)  # Avoid division by zero
            first_artifact = abs(first_dev) / ref_range > ARTIFACT_THRESHOLD
            last_artifact = abs(last_dev) / ref_range > ARTIFACT_THRESHOLD

            dim_report = {
                "interior_mean": round(interior_mean, 6),
                "interior_std": round(interior_std, 6),
                "interior_range": round(interior_range, 6),
                "first_edge": {
                    "mean": round(first_mean, 6),
                    "values": [round(float(v), 6) for v in first_edge],
                    "deviation": round(first_dev, 6),
                    "deviation_pct": round(abs(first_dev) / ref_range * 100, 2),
                    "artifact": first_artifact,
                },
                "last_edge": {
                    "mean": round(last_mean, 6),
                    "values": [round(float(v), 6) for v in last_edge],
                    "deviation": round(last_dev, 6),
                    "deviation_pct": round(abs(last_dev) / ref_range * 100, 2),
                    "artifact": last_artifact,
                },
            }

            if first_artifact or last_artifact:
                audio_report["artifacts_found"] += 1
                total_artifacts += 1

            total_checks += 1
            audio_report["dimensions"][d_name] = dim_report

        # Also check R³ pleasantness edge
        if result.r3.shape[1] > 4:
            pleas_trace = result.r3[:, 4]  # sensory_pleasantness
            interior = pleas_trace[EDGE_FRAMES:-EDGE_FRAMES]
            first_mean = float(np.mean(pleas_trace[:EDGE_FRAMES]))
            last_mean = float(np.mean(pleas_trace[-EDGE_FRAMES:]))
            int_mean = float(np.mean(interior))
            audio_report["r3_pleasantness_edge"] = {
                "interior_mean": round(int_mean, 6),
                "first_edge_mean": round(first_mean, 6),
                "last_edge_mean": round(last_mean, 6),
                "first_deviation": round(first_mean - int_mean, 6),
                "last_deviation": round(last_mean - int_mean, 6),
            }

        report["per_audio"][audio_key] = audio_report

        status = "PASS" if audio_report["artifacts_found"] == 0 else f"FAIL ({audio_report['artifacts_found']} artifacts)"
        print(f"  [{audio_key}] {status}")
        if audio_report["artifacts_found"] > 0:
            for d_name, d_rep in audio_report["dimensions"].items():
                if d_rep["first_edge"]["artifact"]:
                    print(f"     FIRST edge: {d_name} dev={d_rep['first_edge']['deviation_pct']:.1f}%")
                if d_rep["last_edge"]["artifact"]:
                    print(f"     LAST  edge: {d_name} dev={d_rep['last_edge']['deviation_pct']:.1f}%")

    report["summary"] = {
        "total_checks": total_checks,
        "total_artifacts": total_artifacts,
        "artifact_rate": round(total_artifacts / max(total_checks, 1) * 100, 2),
        "status": "PASS" if total_artifacts == 0 else "FAIL",
    }

    save_json(report, stage_dir / "_stage_4_report.json", "STAGE 4")
    print(f"\n  STAGE 4 COMPLETE: {total_artifacts}/{total_checks} artifacts ({report['summary']['artifact_rate']}%)")


# ---------------------------------------------------------------------------
# STAGE 5: Cross-audio comparative analysis + final report
# ---------------------------------------------------------------------------

def stage_5_comparative_report(
    results: Dict[str, ExperimentResult],
) -> None:
    """Cross-audio comparative analysis and final comprehensive report."""
    print("\n" + "=" * 72)
    print("STAGE 5: Cross-Audio Comparative Analysis")
    print("=" * 72)

    stage_dir = RESULTS_DIR / "stage_5_comparative"
    stage_dir.mkdir(parents=True, exist_ok=True)

    # Separate MIDI (controlled stimuli) from real audio
    midi_keys = [k for k in results if k.startswith("midi/")]
    real_keys = [k for k in results if not k.startswith("midi/")]

    report: Dict[str, Any] = {
        "stage": "5_comparative",
        "timestamp": datetime.now().isoformat(),
        "n_midi": len(midi_keys),
        "n_real": len(real_keys),
        "midi_keys": midi_keys,
        "real_keys": real_keys,
    }

    # --- A. MIDI Controlled Tests ---
    print("\n  --- MIDI Controlled Tests ---")
    midi_analysis: Dict[str, Any] = {}

    # Expected behavior checks for MIDI files
    midi_expectations = {
        "midi/csg/01_major_triad": {
            "description": "Consonant chord — low salience expected",
            "E0_salience": "low",      # Consonant → low dissonance salience
            "E2_valence": "positive",   # Consonant → positive valence
            "P1_valence": "positive",   # Pleasant → positive
        },
        "midi/csg/02_m2_dyad": {
            "description": "Minor 2nd — high roughness, high salience",
            "E0_salience": "high",      # Dissonant → high salience
            "E2_valence": "negative",   # Dissonant → negative valence
            "P2_load": "high",          # High processing demand
        },
        "midi/csg/03_cluster": {
            "description": "4-note cluster — maximum dissonance",
            "E0_salience": "highest",   # Maximum dissonance
            "E2_valence": "most_negative",
        },
        "midi/csg/04_V7_I_resolution": {
            "description": "V7→I — tension then release",
            "temporal_pattern": "decrease",  # Salience should decrease
        },
        "midi/csg/05_I_V7_tension": {
            "description": "I→V7 — consonance then tension",
            "temporal_pattern": "increase",  # Salience should increase
        },
        "midi/csg/06_single_note": {
            "description": "Single C4 — baseline, minimal salience",
            "E0_salience": "baseline",
            "E2_valence": "near_zero_positive",
            "temporal_pattern": "flat",
        },
    }

    for midi_key in sorted(midi_keys):
        result = results[midi_key]
        csg = result.relays.get("CSG")
        if csg is None:
            continue

        T = csg.shape[0]
        expectations = midi_expectations.get(midi_key, {})
        desc = expectations.get("description", midi_key)

        analysis: Dict[str, Any] = {
            "description": desc,
            "n_frames": T,
            "checks": [],
        }

        # Dimension means
        dim_means: Dict[str, float] = {}
        for d_idx, d_name in enumerate(CSG_DIMENSIONS):
            if d_idx < csg.shape[1]:
                dim_means[d_name] = float(np.mean(csg[:, d_idx]))
        analysis["dim_means"] = {k: round(v, 4) for k, v in dim_means.items()}

        # Temporal pattern check (first half vs second half)
        half = T // 2
        if half > 0:
            first_half = {d: float(np.mean(csg[:half, i])) for i, d in enumerate(CSG_DIMENSIONS) if i < csg.shape[1]}
            second_half = {d: float(np.mean(csg[half:, i])) for i, d in enumerate(CSG_DIMENSIONS) if i < csg.shape[1]}
            analysis["first_half_means"] = {k: round(v, 4) for k, v in first_half.items()}
            analysis["second_half_means"] = {k: round(v, 4) for k, v in second_half.items()}

            if expectations.get("temporal_pattern") == "decrease":
                # E0 salience should be higher in first half
                e0_diff = first_half.get("E0:salience_activation", 0) - second_half.get("E0:salience_activation", 0)
                check = {"test": "salience_decrease", "e0_diff": round(e0_diff, 4), "pass": e0_diff > 0.02}
                analysis["checks"].append(check)
                status = "PASS" if check["pass"] else "FAIL"
                print(f"  [{midi_key}] {desc}: salience decrease={e0_diff:+.4f} → {status}")

            elif expectations.get("temporal_pattern") == "increase":
                e0_diff = second_half.get("E0:salience_activation", 0) - first_half.get("E0:salience_activation", 0)
                check = {"test": "salience_increase", "e0_diff": round(e0_diff, 4), "pass": e0_diff > 0.02}
                analysis["checks"].append(check)
                status = "PASS" if check["pass"] else "FAIL"
                print(f"  [{midi_key}] {desc}: salience increase={e0_diff:+.4f} → {status}")

            elif expectations.get("temporal_pattern") == "flat":
                e0_std = float(np.std(csg[:, 0]))
                check = {"test": "temporal_flatness", "e0_std": round(e0_std, 4), "pass": e0_std < 0.05}
                analysis["checks"].append(check)
                status = "PASS" if check["pass"] else "FAIL"
                print(f"  [{midi_key}] {desc}: E0 std={e0_std:.4f} → {status}")

        # Valence check
        if expectations.get("E2_valence") == "positive":
            e2_mean = dim_means.get("E2:consonance_valence", 0)
            check = {"test": "valence_positive", "e2_mean": round(e2_mean, 4), "pass": e2_mean > 0.0}
            analysis["checks"].append(check)
            status = "PASS" if check["pass"] else "FAIL"
            print(f"  [{midi_key}] {desc}: E2 valence={e2_mean:+.4f} → {status}")

        elif expectations.get("E2_valence") == "negative":
            e2_mean = dim_means.get("E2:consonance_valence", 0)
            check = {"test": "valence_negative", "e2_mean": round(e2_mean, 4), "pass": e2_mean < 0.0}
            analysis["checks"].append(check)
            status = "PASS" if check["pass"] else "FAIL"
            print(f"  [{midi_key}] {desc}: E2 valence={e2_mean:+.4f} → {status}")

        midi_analysis[midi_key] = analysis

    report["midi_analysis"] = midi_analysis

    # --- B. Real Audio Cross-Comparison ---
    print("\n  --- Real Audio Cross-Comparison ---")
    real_comparison: Dict[str, Any] = {}

    # Collect per-dimension stats across all real audio
    for d_idx, d_name in enumerate(CSG_DIMENSIONS):
        dim_values: Dict[str, Dict[str, float]] = {}
        for rk in real_keys:
            csg = results[rk].relays.get("CSG")
            if csg is None or d_idx >= csg.shape[1]:
                continue
            trace = csg[:, d_idx]
            dim_values[rk] = {
                "mean": round(float(np.mean(trace)), 4),
                "std": round(float(np.std(trace)), 4),
                "min": round(float(np.min(trace)), 4),
                "max": round(float(np.max(trace)), 4),
            }

        if dim_values:
            means = [v["mean"] for v in dim_values.values()]
            real_comparison[d_name] = {
                "per_audio": dim_values,
                "cross_mean": round(float(np.mean(means)), 4),
                "cross_std": round(float(np.std(means)), 4),
                "cross_range": [round(float(np.min(means)), 4), round(float(np.max(means)), 4)],
            }

    report["real_comparison"] = real_comparison

    # --- C. Consonance hierarchy validation ---
    print("\n  --- Consonance Hierarchy Validation ---")
    # Expected: single note > major triad > ... > cluster (for E2:consonance_valence)
    hierarchy_keys = [
        "midi/csg/06_single_note",     # Highest consonance
        "midi/csg/01_major_triad",     # High consonance
        "midi/csg/05_I_V7_tension",    # Mixed (starts consonant)
        "midi/csg/04_V7_I_resolution", # Mixed (starts dissonant)
        "midi/csg/02_m2_dyad",         # Low consonance
        "midi/csg/03_cluster",         # Lowest consonance
    ]

    hierarchy_checks = []
    e2_values = {}
    for hk in hierarchy_keys:
        if hk in results:
            csg = results[hk].relays.get("CSG")
            if csg is not None and csg.shape[1] > 2:
                e2_values[hk] = float(np.mean(csg[:, 2]))

    if len(e2_values) >= 2:
        sorted_by_e2 = sorted(e2_values.items(), key=lambda x: x[1], reverse=True)
        report["consonance_hierarchy"] = {
            "expected_order": hierarchy_keys,
            "actual_order": [k for k, v in sorted_by_e2],
            "values": {k: round(v, 4) for k, v in sorted_by_e2},
        }
        for k, v in sorted_by_e2:
            short = k.split("/")[-1]
            print(f"    E2:consonance_valence | {short:25s} = {v:+.4f}")

    # --- D. Cross-dimension correlation matrix ---
    print("\n  --- Cross-Dimension Correlations (real audio) ---")
    all_dim_traces: Dict[str, List[float]] = {d: [] for d in CSG_DIMENSIONS}
    for rk in real_keys:
        csg = results[rk].relays.get("CSG")
        if csg is None:
            continue
        for d_idx, d_name in enumerate(CSG_DIMENSIONS):
            if d_idx < csg.shape[1]:
                all_dim_traces[d_name].extend(csg[:, d_idx].tolist())

    n_dims = len(CSG_DIMENSIONS)
    corr_matrix = np.zeros((n_dims, n_dims))
    for i, d1 in enumerate(CSG_DIMENSIONS):
        for j, d2 in enumerate(CSG_DIMENSIONS):
            if len(all_dim_traces[d1]) > 0 and len(all_dim_traces[d2]) > 0:
                a1 = np.array(all_dim_traces[d1])
                a2 = np.array(all_dim_traces[d2])
                if len(a1) == len(a2) and np.std(a1) > 1e-8 and np.std(a2) > 1e-8:
                    corr_matrix[i, j] = np.corrcoef(a1, a2)[0, 1]

    report["correlation_matrix"] = {
        "labels": CSG_DIMENSIONS,
        "values": [[round(float(corr_matrix[i, j]), 3) for j in range(n_dims)] for i in range(n_dims)],
    }

    # Print notable correlations
    for i in range(n_dims):
        for j in range(i + 1, n_dims):
            r = corr_matrix[i, j]
            if abs(r) > 0.7:
                print(f"    r={r:+.3f} | {CSG_DIMENSIONS[i].split(':')[0]} × {CSG_DIMENSIONS[j].split(':')[0]}")

    # --- E. Final summary ---
    total_checks = sum(len(a.get("checks", [])) for a in midi_analysis.values())
    passed_checks = sum(
        sum(1 for c in a.get("checks", []) if c.get("pass"))
        for a in midi_analysis.values()
    )

    report["final_summary"] = {
        "total_midi_checks": total_checks,
        "passed_midi_checks": passed_checks,
        "midi_pass_rate": round(passed_checks / max(total_checks, 1) * 100, 1),
        "n_audio_processed": len(results),
        "status": "PASS" if passed_checks == total_checks else "PARTIAL",
    }

    save_json(report, stage_dir / "_stage_5_report.json", "STAGE 5")
    print(f"\n  STAGE 5 COMPLETE: {passed_checks}/{total_checks} MIDI checks passed")


# ---------------------------------------------------------------------------
# FINAL REPORT
# ---------------------------------------------------------------------------

def generate_final_report(all_audio_keys: List[str], t_start: float) -> None:
    """Generate the master summary report."""
    print("\n" + "=" * 72)
    print("FINAL REPORT GENERATION")
    print("=" * 72)

    elapsed = time.perf_counter() - t_start

    # Load all stage reports
    stage_reports = {}
    for stage_num in range(1, 6):
        stage_names = {
            1: "stage_1_extraction",
            2: "stage_2_dimensions",
            3: "stage_3_h3_decomposition",
            4: "stage_4_boundary",
            5: "stage_5_comparative",
        }
        report_path = RESULTS_DIR / stage_names[stage_num] / f"_stage_{stage_num}_report.json"
        if report_path.exists():
            with open(report_path, encoding="utf-8") as f:
                stage_reports[f"stage_{stage_num}"] = json.load(f)

    final = {
        "test_name": "CSG Mechanism Stress Test v4.0",
        "timestamp": datetime.now().isoformat(),
        "total_elapsed_s": round(elapsed, 1),
        "n_audio_files": len(all_audio_keys),
        "audio_files": all_audio_keys,
        "pipeline_version": "v4.0",
        "frame_rate_hz": FRAME_RATE,
        "csg_output_dim": 12,
        "csg_h3_demands": 18,
        "csg_beliefs": CSG_BELIEFS,
        "stages": {},
    }

    # Summarize each stage
    if "stage_1" in stage_reports:
        s1 = stage_reports["stage_1"]
        final["stages"]["1_extraction"] = {
            "status": "COMPLETE",
            "n_processed": len(s1.get("results", {})),
        }

    if "stage_2" in stage_reports:
        s2 = stage_reports["stage_2"]
        val = s2.get("validation", {})
        final["stages"]["2_dimensions"] = {
            "status": val.get("status", "UNKNOWN"),
            "total_violations": val.get("total_violations", -1),
        }

    if "stage_3" in stage_reports:
        final["stages"]["3_h3_decomposition"] = {"status": "COMPLETE"}

    if "stage_4" in stage_reports:
        s4 = stage_reports["stage_4"]
        summary = s4.get("summary", {})
        final["stages"]["4_boundary"] = {
            "status": summary.get("status", "UNKNOWN"),
            "total_artifacts": summary.get("total_artifacts", -1),
            "artifact_rate_pct": summary.get("artifact_rate", -1),
        }

    if "stage_5" in stage_reports:
        s5 = stage_reports["stage_5"]
        fs = s5.get("final_summary", {})
        final["stages"]["5_comparative"] = {
            "status": fs.get("status", "UNKNOWN"),
            "midi_pass_rate_pct": fs.get("midi_pass_rate", -1),
        }

    # Overall status
    stage_statuses = [s.get("status", "UNKNOWN") for s in final["stages"].values()]
    if all(s in ("PASS", "COMPLETE") for s in stage_statuses):
        final["overall_status"] = "ALL PASS"
    elif any(s == "FAIL" for s in stage_statuses):
        final["overall_status"] = "FAIL"
    else:
        final["overall_status"] = "PARTIAL"

    save_json(final, RESULTS_DIR / "FINAL_REPORT.json", "FINAL")

    # Print summary
    print(f"\n  {'=' * 50}")
    print(f"  CSG Stress Test v4.0 — FINAL RESULTS")
    print(f"  {'=' * 50}")
    print(f"  Audio files:    {len(all_audio_keys)}")
    print(f"  Total time:     {elapsed:.1f}s")
    for stage_name, stage_data in final["stages"].items():
        status = stage_data.get("status", "?")
        print(f"  {stage_name:20s} → {status}")
    print(f"  {'=' * 50}")
    print(f"  OVERALL: {final['overall_status']}")
    print(f"  {'=' * 50}")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    t_start = time.perf_counter()

    print("=" * 72)
    print("CSG MECHANISM STRESS TEST v4.0")
    print(f"Started: {datetime.now().isoformat()}")
    print("=" * 72)

    # All audio files (real + MIDI)
    all_audio_keys = sorted(AUDIO_CATALOG.keys()) + sorted(
        k for k in MIDI_CATALOG.keys() if k.startswith("midi/csg/")
    )
    print(f"\nAudio files to process: {len(all_audio_keys)}")
    for k in all_audio_keys:
        print(f"  - {k}")

    # Initialize pipeline
    print("\nInitializing MI Pipeline...")
    pipeline = MIPipeline()

    # Stage 1: Full extraction
    results = stage_1_extraction(pipeline, all_audio_keys)

    # Stage 2: Dimension analysis
    stage_2_dimension_analysis(results)

    # Stage 3: H³ decomposition
    stage_3_h3_decomposition(pipeline, results)

    # Stage 4: Boundary analysis
    stage_4_boundary_analysis(results)

    # Stage 5: Comparative analysis
    stage_5_comparative_report(results)

    # Final report
    generate_final_report(all_audio_keys, t_start)


if __name__ == "__main__":
    main()
