#!/usr/bin/env python3
"""C³ Kernel Beta Test — 3-Piece Analysis with Visualization Export.

Runs the full Audio → R³ → H³ → C³ Kernel (with BCH) pipeline on three
contrasting pieces, exports all raw data as JSON, and generates a
self-contained HTML visualization dashboard.

Output: Lab/WebLab/experiments/Beta-Test/
  - data.json:  all frame-level traces + statistics
  - meta.json:  pipeline metadata
  - index.html: interactive Plotly.js dashboard
"""
from __future__ import annotations

import json
import os
import sys
import time

_PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import librosa
import numpy as np
import torch

from Musical_Intelligence.ear.r3 import R3Extractor
from Musical_Intelligence.ear.h3 import H3Extractor
from Musical_Intelligence.brain.kernel.scheduler import C3Kernel

# ── Config ────────────────────────────────────────────────────────────
SR = 44100
HOP = 256
N_MELS = 128
DURATION = 30

PIECES = {
    "Swan Lake": os.path.join(
        _PROJECT_ROOT, "Test-Audio",
        "Swan Lake Suite, Op. 20a_ I. Scene _Swan Theme_. Moderato"
        " - Pyotr Ilyich Tchaikovsky.wav",
    ),
    "Bach Cello": os.path.join(
        _PROJECT_ROOT, "Test-Audio",
        "Cello Suite No. 1 in G Major, BWV 1007 I. Prélude.wav",
    ),
    "Beethoven Pathétique": os.path.join(
        _PROJECT_ROOT, "Test-Audio",
        "Beethoven - Pathetique Sonata Op13 I. Grave - Allegro.wav",
    ),
}

OUT_DIR = os.path.join(
    _PROJECT_ROOT, "Lab", "WebLab", "experiments", "Beta-Test"
)


def run_pipeline(name: str, path: str) -> dict:
    """Run full pipeline, return all raw traces."""
    print(f"\n  [{name}] Loading...")
    t0 = time.time()
    waveform, sr = librosa.load(path, sr=SR, duration=DURATION, mono=True)
    waveform_t = torch.from_numpy(waveform).unsqueeze(0).float()

    mel_np = librosa.feature.melspectrogram(
        y=waveform, sr=sr, n_mels=N_MELS, hop_length=HOP
    )
    mel_db = librosa.power_to_db(mel_np, ref=np.max)
    mel_norm = (mel_db - mel_db.min()) / (mel_db.max() - mel_db.min() + 1e-8)
    mel_t = torch.from_numpy(mel_norm).unsqueeze(0).float()
    T = mel_t.shape[2]

    print(f"  [{name}] R³ extraction...")
    t1 = time.time()
    r3_ext = R3Extractor()
    r3_out = r3_ext.extract(mel_t, audio=waveform_t, sr=SR)
    r3_tensor = r3_out.features
    feature_map = r3_out.feature_map
    r3_time = time.time() - t1

    print(f"  [{name}] H³ extraction...")
    t2 = time.time()
    kernel_tmp = C3Kernel(feature_map)
    demand = kernel_tmp.h3_demands()
    h3_ext = H3Extractor()
    h3_out = h3_ext.extract(r3_tensor, demand)
    h3_dict = h3_out.features
    h3_time = time.time() - t2

    print(f"  [{name}] C³ Kernel ({T} frames)...")
    t3 = time.time()
    kernel = C3Kernel(feature_map)

    traces = {
        "perceived_consonance": [],
        "tempo_state": [],
        "reward_valence": [],
        "pe_consonance": [],
        "pe_tempo": [],
        "precision_obs_cons": [],
        "precision_obs_tempo": [],
        "precision_pred_cons": [],
        "precision_pred_tempo": [],
    }

    for t in range(T):
        r3_frame = r3_tensor[:, t:t+1, :]
        h3_frame = {}
        for key, val in h3_dict.items():
            if val.shape[1] > t:
                h3_frame[key] = val[:, t:t+1]

        out = kernel.tick(r3_frame, h3_frame)

        traces["perceived_consonance"].append(
            out.beliefs["perceived_consonance"].mean().item())
        traces["tempo_state"].append(
            out.beliefs["tempo_state"].mean().item())
        traces["reward_valence"].append(
            out.beliefs["reward_valence"].mean().item())
        traces["pe_consonance"].append(
            out.pe["perceived_consonance"].mean().item())
        traces["pe_tempo"].append(
            out.pe["tempo_state"].mean().item())
        traces["precision_obs_cons"].append(
            out.precision_obs["perceived_consonance"].mean().item())
        traces["precision_obs_tempo"].append(
            out.precision_obs["tempo_state"].mean().item())
        traces["precision_pred_cons"].append(
            out.precision_pred["perceived_consonance"].item()
            if out.precision_pred["perceived_consonance"].numel() == 1
            else out.precision_pred["perceived_consonance"].mean().item())
        traces["precision_pred_tempo"].append(
            out.precision_pred["tempo_state"].item()
            if out.precision_pred["tempo_state"].numel() == 1
            else out.precision_pred["tempo_state"].mean().item())

    c3_time = time.time() - t3
    total_time = time.time() - t0
    print(f"  [{name}] Done: {c3_time:.1f}s C³, {total_time:.1f}s total")

    return {
        "name": name,
        "T": T,
        "sr": SR,
        "hop": HOP,
        "duration": DURATION,
        "traces": traces,
        "timing": {
            "r3": round(r3_time, 2),
            "h3": round(h3_time, 2),
            "c3": round(c3_time, 2),
            "total": round(total_time, 2),
        },
        "h3_tuples": len(h3_dict),
    }


def compute_stats(result: dict) -> dict:
    """Compute statistics from raw traces."""
    tr = result["traces"]
    T = result["T"]
    frame_rate = SR / HOP
    window_frames = int(5 * frame_rate)

    stats = {"name": result["name"], "T": T, "duration": T / frame_rate}

    for key in ["perceived_consonance", "tempo_state", "reward_valence",
                "pe_consonance", "pe_tempo"]:
        arr = np.array(tr[key])
        stats[key] = {
            "mean": round(float(arr.mean()), 6),
            "std": round(float(arr.std()), 6),
            "min": round(float(arr.min()), 6),
            "max": round(float(arr.max()), 6),
            "range": round(float(arr.max() - arr.min()), 6),
        }

    # Window-by-window
    n_windows = T // window_frames
    windows = []
    for w in range(n_windows):
        s = w * window_frames
        e = (w + 1) * window_frames
        t_s = s / frame_rate
        t_e = e / frame_rate
        windows.append({
            "label": f"{t_s:.0f}-{t_e:.0f}s",
            "cons": round(float(np.array(tr["perceived_consonance"][s:e]).mean()), 6),
            "tempo": round(float(np.array(tr["tempo_state"][s:e]).mean()), 6),
            "reward": round(float(np.array(tr["reward_valence"][s:e]).mean()), 6),
            "pe_cons": round(float(np.abs(np.array(tr["pe_consonance"][s:e])).mean()), 6),
            "pe_tempo": round(float(np.abs(np.array(tr["pe_tempo"][s:e])).mean()), 6),
        })
    stats["windows"] = windows

    # Adaptation
    first = np.array(tr["pe_consonance"][:window_frames])
    last = np.array(tr["pe_consonance"][-window_frames:])
    first_t = np.array(tr["pe_tempo"][:window_frames])
    last_t = np.array(tr["pe_tempo"][-window_frames:])
    rew_first = np.array(tr["reward_valence"][:window_frames])
    rew_last = np.array(tr["reward_valence"][-window_frames:])

    f5 = float(np.abs(first).mean())
    l5 = float(np.abs(last).mean())
    stats["adaptation"] = {
        "pe_cons_first5s": round(f5, 6),
        "pe_cons_last5s": round(l5, 6),
        "pe_cons_reduction_pct": round((f5 - l5) / (f5 + 1e-8) * 100, 2),
        "pe_tempo_first5s": round(float(np.abs(first_t).mean()), 6),
        "pe_tempo_last5s": round(float(np.abs(last_t).mean()), 6),
        "reward_first5s": round(float(rew_first.mean()), 6),
        "reward_last5s": round(float(rew_last.mean()), 6),
    }

    return stats


def downsample(arr, factor=4):
    """Downsample array for HTML embedding."""
    a = np.array(arr)
    n = len(a) // factor * factor
    return a[:n].reshape(-1, factor).mean(axis=1).tolist()


def generate_html(results: list, all_stats: list) -> str:
    """Generate self-contained HTML dashboard."""
    frame_rate = SR / HOP

    # Prepare downsampled data for charts
    ds_factor = 4
    chart_data = {}
    for r in results:
        name = r["name"]
        T = r["T"]
        time_axis = downsample(
            (np.arange(T) / frame_rate).tolist(), ds_factor
        )
        chart_data[name] = {
            "time": [round(t, 3) for t in time_axis],
            "consonance": [round(v, 5) for v in downsample(r["traces"]["perceived_consonance"], ds_factor)],
            "tempo": [round(v, 5) for v in downsample(r["traces"]["tempo_state"], ds_factor)],
            "reward": [round(v, 5) for v in downsample(r["traces"]["reward_valence"], ds_factor)],
            "pe_cons": [round(v, 5) for v in downsample(r["traces"]["pe_consonance"], ds_factor)],
            "pe_tempo": [round(v, 5) for v in downsample(r["traces"]["pe_tempo"], ds_factor)],
            "pi_obs_cons": [round(v, 5) for v in downsample(r["traces"]["precision_obs_cons"], ds_factor)],
            "pi_obs_tempo": [round(v, 5) for v in downsample(r["traces"]["precision_obs_tempo"], ds_factor)],
            "pi_pred_cons": [round(v, 5) for v in downsample(r["traces"]["precision_pred_cons"], ds_factor)],
            "pi_pred_tempo": [round(v, 5) for v in downsample(r["traces"]["precision_pred_tempo"], ds_factor)],
        }

    data_json = json.dumps(chart_data)
    stats_json = json.dumps(all_stats)

    # Color palette
    colors = {
        "Swan Lake": "#4ECDC4",
        "Bach Cello": "#FF6B6B",
        "Beethoven Pathétique": "#FFE66D",
    }
    colors_json = json.dumps(colors)

    # Diagnostic checks
    checks = []
    for s in all_stats:
        pe_decr = s["adaptation"]["pe_cons_first5s"] > s["adaptation"]["pe_cons_last5s"]
        checks.append({"label": f"PE decreases over time ({s['name']})", "pass": pe_decr})

    ranges = [s["perceived_consonance"]["range"] for s in all_stats]
    spread = max(ranges) / (min(ranges) + 1e-8)
    checks.append({"label": f"Consonance range spread > 1.2x ({spread:.2f}x)", "pass": spread > 1.2})

    pe_stds = [s["pe_consonance"]["std"] for s in all_stats]
    pe_spread = max(pe_stds) / (min(pe_stds) + 1e-8)
    checks.append({"label": f"PE_cons std spread > 1.2x ({pe_spread:.2f}x)", "pass": pe_spread > 1.2})

    rew_means = [s["reward_valence"]["mean"] for s in all_stats]
    rew_spread = max(rew_means) - min(rew_means)
    checks.append({"label": f"Reward mean spread > 0.01 ({rew_spread:.4f})", "pass": rew_spread > 0.01})

    tempo_ranges = [s["tempo_state"]["range"] for s in all_stats]
    tempo_spread = max(tempo_ranges) / (min(tempo_ranges) + 1e-8)
    checks.append({"label": f"Tempo range spread > 1.2x ({tempo_spread:.2f}x)", "pass": tempo_spread > 1.2})

    checks_json = json.dumps(checks)
    passed = sum(1 for c in checks if c["pass"])
    total = len(checks)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>C³ Kernel Beta Test — 3-Piece Comparative Analysis</title>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<style>
  :root {{
    --bg: #0a0a0f;
    --surface: #12121a;
    --surface2: #1a1a26;
    --border: #2a2a3a;
    --text: #e0e0e8;
    --text-dim: #8888a0;
    --accent: #6c5ce7;
    --pass: #00b894;
    --fail: #e17055;
    --swan: #4ECDC4;
    --bach: #FF6B6B;
    --beethoven: #FFE66D;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    background: var(--bg);
    color: var(--text);
    font-family: 'SF Mono', 'Fira Code', 'JetBrains Mono', monospace;
    line-height: 1.6;
    min-height: 100vh;
  }}
  .container {{ max-width: 1600px; margin: 0 auto; padding: 24px; }}

  /* Header */
  .header {{
    text-align: center;
    padding: 48px 0 32px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 32px;
  }}
  .header h1 {{
    font-size: 28px;
    font-weight: 300;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: var(--text);
    margin-bottom: 8px;
  }}
  .header h1 span {{ color: var(--accent); font-weight: 600; }}
  .header .subtitle {{
    font-size: 13px;
    color: var(--text-dim);
    letter-spacing: 2px;
  }}
  .header .score {{
    margin-top: 20px;
    font-size: 48px;
    font-weight: 200;
    color: var(--pass);
  }}
  .header .score-label {{
    font-size: 12px;
    color: var(--text-dim);
    letter-spacing: 3px;
    text-transform: uppercase;
  }}

  /* Piece legend */
  .legend {{
    display: flex;
    justify-content: center;
    gap: 32px;
    margin: 24px 0;
  }}
  .legend-item {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
  }}
  .legend-dot {{
    width: 12px;
    height: 12px;
    border-radius: 50%;
  }}

  /* Section */
  .section {{
    margin-bottom: 40px;
  }}
  .section-title {{
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
  }}

  /* Chart grid */
  .chart-row {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 16px;
  }}
  .chart-row.full {{ grid-template-columns: 1fr; }}
  .chart-row.triple {{ grid-template-columns: 1fr 1fr 1fr; }}
  .chart-box {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
    min-height: 340px;
  }}
  .chart-box .plotly-graph-div {{ width: 100% !important; }}

  /* Stats table */
  .stats-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 24px;
  }}
  .stat-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 20px;
  }}
  .stat-card .piece-name {{
    font-size: 12px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text-dim);
    margin-bottom: 12px;
  }}
  .stat-card .metrics {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px 16px;
  }}
  .stat-card .metric {{
    display: flex;
    justify-content: space-between;
    font-size: 12px;
  }}
  .stat-card .metric .label {{ color: var(--text-dim); }}
  .stat-card .metric .value {{ font-weight: 600; }}

  /* Checks */
  .checks {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
    gap: 8px;
  }}
  .check {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    font-size: 12px;
  }}
  .check-badge {{
    padding: 2px 8px;
    border-radius: 4px;
    font-weight: 700;
    font-size: 10px;
    letter-spacing: 1px;
  }}
  .check-badge.pass {{ background: var(--pass); color: #000; }}
  .check-badge.fail {{ background: var(--fail); color: #fff; }}

  /* Heatmap table */
  .heatmap-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
  }}
  .heatmap-table th, .heatmap-table td {{
    padding: 8px 12px;
    text-align: center;
    border: 1px solid var(--border);
  }}
  .heatmap-table th {{
    background: var(--surface2);
    color: var(--text-dim);
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    font-size: 10px;
  }}
  .heatmap-table td {{ background: var(--surface); }}

  /* Timing bar */
  .timing-row {{
    display: flex;
    gap: 24px;
    justify-content: center;
    margin: 16px 0;
    flex-wrap: wrap;
  }}
  .timing-item {{
    font-size: 12px;
    color: var(--text-dim);
  }}
  .timing-item span {{ color: var(--text); font-weight: 600; }}

  /* Footer */
  .footer {{
    text-align: center;
    padding: 32px 0;
    margin-top: 40px;
    border-top: 1px solid var(--border);
    font-size: 11px;
    color: var(--text-dim);
    letter-spacing: 1px;
  }}

  /* Plotly overrides */
  .js-plotly-plot .plotly .modebar {{ top: 4px !important; right: 4px !important; }}
</style>
</head>
<body>
<div class="container">

  <!-- Header -->
  <div class="header">
    <h1><span>C³</span> Kernel Beta Test</h1>
    <div class="subtitle">3-Piece Comparative Analysis &mdash; BCH Injection v1.0 &mdash; 30s Excerpts</div>
    <div class="score">{passed}/{total}</div>
    <div class="score-label">Diagnostic Checks Passed</div>
  </div>

  <!-- Legend -->
  <div class="legend">
    <div class="legend-item"><div class="legend-dot" style="background:var(--swan)"></div> Swan Lake — Tchaikovsky</div>
    <div class="legend-item"><div class="legend-dot" style="background:var(--bach)"></div> Cello Suite No.1 — Bach</div>
    <div class="legend-item"><div class="legend-dot" style="background:var(--beethoven)"></div> Path&eacute;tique Sonata — Beethoven</div>
  </div>

  <!-- Section 1: Belief Time Series -->
  <div class="section">
    <div class="section-title">1 &mdash; Belief Dynamics</div>
    <div class="chart-row">
      <div class="chart-box" id="chart-consonance"></div>
      <div class="chart-box" id="chart-tempo"></div>
    </div>
    <div class="chart-row full">
      <div class="chart-box" id="chart-reward"></div>
    </div>
  </div>

  <!-- Section 2: Prediction Error -->
  <div class="section">
    <div class="section-title">2 &mdash; Prediction Error</div>
    <div class="chart-row">
      <div class="chart-box" id="chart-pe-cons"></div>
      <div class="chart-box" id="chart-pe-tempo"></div>
    </div>
  </div>

  <!-- Section 3: Precision -->
  <div class="section">
    <div class="section-title">3 &mdash; Precision (Observation &amp; Prediction)</div>
    <div class="chart-row">
      <div class="chart-box" id="chart-pi-obs"></div>
      <div class="chart-box" id="chart-pi-pred"></div>
    </div>
  </div>

  <!-- Section 4: Radar Profiles -->
  <div class="section">
    <div class="section-title">4 &mdash; Piece Profiles (Radar)</div>
    <div class="chart-row full">
      <div class="chart-box" id="chart-radar" style="min-height:480px"></div>
    </div>
  </div>

  <!-- Section 5: Adaptation -->
  <div class="section">
    <div class="section-title">5 &mdash; Temporal Adaptation (First 5s vs Last 5s)</div>
    <div class="chart-row">
      <div class="chart-box" id="chart-adapt-pe"></div>
      <div class="chart-box" id="chart-adapt-reward"></div>
    </div>
  </div>

  <!-- Section 6: Window Heatmap -->
  <div class="section">
    <div class="section-title">6 &mdash; Window-by-Window (5s)</div>
    <div class="chart-row full">
      <div class="chart-box" id="chart-heatmap-cons" style="min-height:260px"></div>
    </div>
    <div class="chart-row">
      <div class="chart-box" id="chart-heatmap-tempo" style="min-height:260px"></div>
      <div class="chart-box" id="chart-heatmap-reward" style="min-height:260px"></div>
    </div>
  </div>

  <!-- Section 7: Statistics -->
  <div class="section">
    <div class="section-title">7 &mdash; Statistics</div>
    <div class="stats-grid" id="stats-cards"></div>
  </div>

  <!-- Section 8: Diagnostics -->
  <div class="section">
    <div class="section-title">8 &mdash; Diagnostic Checks</div>
    <div class="checks" id="checks-container"></div>
  </div>

  <!-- Footer -->
  <div class="footer">
    Musical Intelligence &mdash; C&sup3; Kernel v1.0 + BCH Injection &mdash; Generated {time.strftime('%Y-%m-%d %H:%M')}
  </div>

</div>

<script>
const DATA = {data_json};
const STATS = {stats_json};
const COLORS = {colors_json};
const CHECKS = {checks_json};
const PIECE_NAMES = Object.keys(DATA);

const PLOTLY_LAYOUT = {{
  paper_bgcolor: 'rgba(0,0,0,0)',
  plot_bgcolor: 'rgba(18,18,26,1)',
  font: {{ family: 'SF Mono, Fira Code, monospace', size: 11, color: '#8888a0' }},
  margin: {{ l: 50, r: 20, t: 36, b: 40 }},
  xaxis: {{
    gridcolor: '#2a2a3a', zerolinecolor: '#2a2a3a',
    title: {{ text: 'Time (s)', font: {{ size: 10 }} }}
  }},
  yaxis: {{ gridcolor: '#2a2a3a', zerolinecolor: '#2a2a3a' }},
  legend: {{ x: 0.01, y: 0.99, bgcolor: 'rgba(0,0,0,0)', font: {{ size: 10 }} }},
  hoverlabel: {{ font: {{ family: 'SF Mono, monospace', size: 11 }} }},
}};

const PLOTLY_CONFIG = {{
  displayModeBar: true,
  modeBarButtonsToRemove: ['select2d','lasso2d','autoScale2d'],
  toImageButtonOptions: {{ format: 'svg', width: 1920, height: 600 }},
  responsive: true,
}};

function makeTraces(field, yTitle) {{
  return PIECE_NAMES.map(name => ({{
    x: DATA[name].time,
    y: DATA[name][field],
    name: name,
    type: 'scatter',
    mode: 'lines',
    line: {{ color: COLORS[name], width: 1.5 }},
    hovertemplate: '%{{y:.4f}}<extra>' + name + '</extra>',
  }}));
}}

function plotTimeSeries(divId, field, title, yTitle) {{
  const traces = makeTraces(field, yTitle);
  const layout = {{
    ...PLOTLY_LAYOUT,
    title: {{ text: title, font: {{ size: 13, color: '#e0e0e8' }}, x: 0.02 }},
    yaxis: {{ ...PLOTLY_LAYOUT.yaxis, title: {{ text: yTitle, font: {{ size: 10 }} }} }},
    xaxis: {{ ...PLOTLY_LAYOUT.xaxis }},
  }};
  Plotly.newPlot(divId, traces, layout, PLOTLY_CONFIG);
}}

// 1. Beliefs
plotTimeSeries('chart-consonance', 'consonance', 'Perceived Consonance', 'Value');
plotTimeSeries('chart-tempo', 'tempo', 'Tempo State', 'Value');
plotTimeSeries('chart-reward', 'reward', 'Reward Valence', 'Value');

// 2. PE
plotTimeSeries('chart-pe-cons', 'pe_cons', 'PE Consonance', 'Error');
plotTimeSeries('chart-pe-tempo', 'pe_tempo', 'PE Tempo', 'Error');

// 3. Precision
plotTimeSeries('chart-pi-obs', 'pi_obs_cons', 'Precision Obs (Consonance)', 'Precision');
plotTimeSeries('chart-pi-pred', 'pi_pred_cons', 'Precision Pred (Consonance)', 'Precision');

// 4. Radar
(function() {{
  const categories = ['Cons Range', 'Cons Std', 'Tempo Range', 'Reward Range', 'PE Cons Std', 'PE Adapt %'];
  // Normalize each metric to [0, 1] across pieces
  const rawVals = STATS.map(s => [
    s.perceived_consonance.range,
    s.perceived_consonance.std,
    s.tempo_state.range,
    s.reward_valence.range,
    s.pe_consonance.std,
    Math.max(0, s.adaptation.pe_cons_reduction_pct) / 100,
  ]);
  // Find max per category
  const maxes = categories.map((_, i) => Math.max(...rawVals.map(v => v[i])) || 1);
  const traces = STATS.map((s, si) => ({{
    type: 'scatterpolar',
    r: rawVals[si].map((v, i) => v / maxes[i]),
    theta: categories,
    fill: 'toself',
    fillcolor: COLORS[s.name] + '20',
    line: {{ color: COLORS[s.name], width: 2 }},
    name: s.name,
    hovertemplate: '%{{theta}}: %{{r:.3f}}<extra>' + s.name + '</extra>',
  }}));
  Plotly.newPlot('chart-radar', traces, {{
    ...PLOTLY_LAYOUT,
    margin: {{ l: 60, r: 60, t: 40, b: 40 }},
    polar: {{
      bgcolor: 'rgba(18,18,26,1)',
      radialaxis: {{ gridcolor: '#2a2a3a', linecolor: '#2a2a3a', tickfont: {{ size: 9 }}, range: [0, 1.1] }},
      angularaxis: {{ gridcolor: '#2a2a3a', linecolor: '#2a2a3a', tickfont: {{ size: 10, color: '#e0e0e8' }} }},
    }},
    title: {{ text: 'Piece Profiles (Normalized)', font: {{ size: 13, color: '#e0e0e8' }}, x: 0.5 }},
  }}, PLOTLY_CONFIG);
}})();

// 5. Adaptation bars
(function() {{
  const groups = ['|PE cons|', '|PE tempo|'];
  const traces = [];
  STATS.forEach((s, i) => {{
    traces.push({{
      x: ['First 5s', 'Last 5s', 'First 5s', 'Last 5s'],
      y: [s.adaptation.pe_cons_first5s, s.adaptation.pe_cons_last5s,
          s.adaptation.pe_tempo_first5s, s.adaptation.pe_tempo_last5s],
      name: s.name,
      type: 'bar',
      marker: {{ color: COLORS[s.name], opacity: 0.85 }},
      hovertemplate: '%{{y:.4f}}<extra>' + s.name + '</extra>',
    }});
  }});
  Plotly.newPlot('chart-adapt-pe', traces, {{
    ...PLOTLY_LAYOUT,
    barmode: 'group',
    title: {{ text: 'PE Adaptation', font: {{ size: 13, color: '#e0e0e8' }}, x: 0.02 }},
    yaxis: {{ ...PLOTLY_LAYOUT.yaxis, title: {{ text: '|PE|', font: {{ size: 10 }} }} }},
    xaxis: {{ ...PLOTLY_LAYOUT.xaxis, title: {{ text: '' }} }},
  }}, PLOTLY_CONFIG);

  // Reward drift
  const rewTraces = STATS.map(s => ({{
    x: ['First 5s', 'Last 5s'],
    y: [s.adaptation.reward_first5s, s.adaptation.reward_last5s],
    name: s.name,
    type: 'bar',
    marker: {{ color: COLORS[s.name], opacity: 0.85 }},
  }}));
  Plotly.newPlot('chart-adapt-reward', rewTraces, {{
    ...PLOTLY_LAYOUT,
    barmode: 'group',
    title: {{ text: 'Reward Drift', font: {{ size: 13, color: '#e0e0e8' }}, x: 0.02 }},
    yaxis: {{ ...PLOTLY_LAYOUT.yaxis, title: {{ text: 'Reward', font: {{ size: 10 }} }} }},
    xaxis: {{ ...PLOTLY_LAYOUT.xaxis, title: {{ text: '' }} }},
  }}, PLOTLY_CONFIG);
}})();

// 6. Heatmaps
function plotHeatmap(divId, field, title) {{
  const windows = STATS[0].windows.map(w => w.label);
  const z = STATS.map(s => s.windows.map(w => w[field]));
  const names = STATS.map(s => s.name);
  Plotly.newPlot(divId, [{{
    z: z,
    x: windows,
    y: names,
    type: 'heatmap',
    colorscale: [
      [0, '#0a0a2e'],
      [0.25, '#1a1a6c'],
      [0.5, '#6c5ce7'],
      [0.75, '#a29bfe'],
      [1, '#dfe6e9'],
    ],
    hovertemplate: '%{{y}}<br>%{{x}}<br>%{{z:.4f}}<extra></extra>',
    showscale: true,
    colorbar: {{ tickfont: {{ size: 10, color: '#8888a0' }}, len: 0.8 }},
  }}], {{
    ...PLOTLY_LAYOUT,
    margin: {{ l: 150, r: 20, t: 36, b: 40 }},
    title: {{ text: title, font: {{ size: 13, color: '#e0e0e8' }}, x: 0.02 }},
    yaxis: {{ ...PLOTLY_LAYOUT.yaxis, title: '' }},
    xaxis: {{ ...PLOTLY_LAYOUT.xaxis, title: {{ text: 'Window', font: {{ size: 10 }} }} }},
  }}, PLOTLY_CONFIG);
}}
plotHeatmap('chart-heatmap-cons', 'cons', 'Consonance by Window');
plotHeatmap('chart-heatmap-tempo', 'tempo', 'Tempo by Window');
plotHeatmap('chart-heatmap-reward', 'reward', 'Reward by Window');

// 7. Stats cards
(function() {{
  const container = document.getElementById('stats-cards');
  STATS.forEach(s => {{
    const color = COLORS[s.name];
    const card = document.createElement('div');
    card.className = 'stat-card';
    card.style.borderTopColor = color;
    card.style.borderTopWidth = '3px';
    const metrics = [
      ['Consonance mean', s.perceived_consonance.mean.toFixed(4)],
      ['Consonance range', s.perceived_consonance.range.toFixed(4)],
      ['Tempo mean', s.tempo_state.mean.toFixed(4)],
      ['Tempo range', s.tempo_state.range.toFixed(4)],
      ['Reward mean', s.reward_valence.mean.toFixed(4)],
      ['Reward range', s.reward_valence.range.toFixed(4)],
      ['PE cons std', s.pe_consonance.std.toFixed(4)],
      ['PE tempo std', s.pe_tempo.std.toFixed(4)],
      ['PE adapt %', s.adaptation.pe_cons_reduction_pct.toFixed(1) + '%'],
      ['Reward drift', (s.adaptation.reward_last5s - s.adaptation.reward_first5s).toFixed(4)],
    ];
    card.innerHTML = '<div class="piece-name" style="color:' + color + '">' + s.name + '</div>'
      + '<div class="metrics">' + metrics.map(m =>
        '<div class="metric"><span class="label">' + m[0] + '</span><span class="value">' + m[1] + '</span></div>'
      ).join('') + '</div>';
    container.appendChild(card);
  }});
}})();

// 8. Diagnostic checks
(function() {{
  const container = document.getElementById('checks-container');
  CHECKS.forEach(c => {{
    const div = document.createElement('div');
    div.className = 'check';
    const cls = c.pass ? 'pass' : 'fail';
    const label = c.pass ? 'PASS' : 'FAIL';
    div.innerHTML = '<span class="check-badge ' + cls + '">' + label + '</span>' + c.label;
    container.appendChild(div);
  }});
}})();

</script>
</body>
</html>"""
    return html


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)

    print("=" * 60)
    print("  C³ Kernel Beta Test — 3-Piece Visualization Export")
    print("=" * 60)

    results = []
    for name, path in PIECES.items():
        if not os.path.exists(path):
            print(f"  SKIP: {name} — file not found")
            continue
        results.append(run_pipeline(name, path))

    if not results:
        print("No audio files found!")
        return

    # Compute statistics
    all_stats = [compute_stats(r) for r in results]

    # Save data.json (traces downsampled for size)
    frame_rate = SR / HOP
    ds = 4
    export_data = {}
    for r in results:
        T = r["T"]
        export_data[r["name"]] = {
            "time": downsample((np.arange(T) / frame_rate).tolist(), ds),
            "traces": {k: downsample(v, ds) for k, v in r["traces"].items()},
            "timing": r["timing"],
            "h3_tuples": r["h3_tuples"],
        }

    data_path = os.path.join(OUT_DIR, "data.json")
    with open(data_path, "w") as f:
        json.dump(export_data, f, indent=2)
    print(f"\n  Saved: {data_path} ({os.path.getsize(data_path) / 1024:.0f} KB)")

    # Save meta.json
    meta = {
        "test": "C3 Kernel Beta Test",
        "version": "1.0",
        "bch_injection": True,
        "sr": SR,
        "hop": HOP,
        "duration": DURATION,
        "pieces": [r["name"] for r in results],
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    meta_path = os.path.join(OUT_DIR, "meta.json")
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)
    print(f"  Saved: {meta_path}")

    # Save stats.json
    stats_path = os.path.join(OUT_DIR, "stats.json")
    with open(stats_path, "w") as f:
        json.dump(all_stats, f, indent=2)
    print(f"  Saved: {stats_path}")

    # Generate HTML
    html = generate_html(results, all_stats)
    html_path = os.path.join(OUT_DIR, "index.html")
    with open(html_path, "w") as f:
        f.write(html)
    print(f"  Saved: {html_path} ({os.path.getsize(html_path) / 1024:.0f} KB)")

    print(f"\n  Open in browser: file://{html_path}")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
