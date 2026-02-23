/* ── Load and parse the MI analysis JSON ─────────────────────────── */

import { useState, useEffect } from "react";

export interface AnalysisData {
  meta: {
    version: string;
    piece: string;
    duration_s: number;
    frames: number;
    fps: number;
    trace_points: number;
  };
  r3_groups: {
    time_s: number[];
    A_consonance: number[];
    B_energy: number[];
    C_timbre: number[];
    D_change: number[];
    F_pitch: number[];
    G_rhythm: number[];
    H_harmony: number[];
    J_ext_timbre: number[];
    K_modulation: number[];
  };
  beliefs: {
    time_s: number[];
    consonance: number[];
    tempo: number[];
    salience: number[];
    familiarity: number[];
    reward: number[];
  };
  prediction_errors: {
    consonance: number[];
    tempo: number[];
    salience: number[];
    familiarity: number[];
  };
  precision: {
    consonance: number[];
    tempo: number[];
    salience: number[];
    familiarity: number[];
  };
  ram: {
    regions: string[];
    traces: Record<string, number[]>;
  };
  relays: {
    bch_consonance_signal: number[];
    hmce_a1_encoding: number[];
    snem_entrainment: number[];
    mmp_familiarity: number[];
    daed_wanting: number[];
    daed_liking: number[];
    mpg_onset: number[];
  };
  summary: {
    beliefs: Record<string, { mean: number; std: number; min: number; max: number }>;
    reward: { mean: number; std: number; min: number; max: number; pct_positive: number };
    r3_group_means: Record<string, number>;
  };
}

export function useAnalysisData() {
  const [data, setData] = useState<AnalysisData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/data/shifting-rooms-analysis.json")
      .then((r) => r.json())
      .then((d) => { setData(d); setLoading(false); })
      .catch((e) => { console.error("Failed to load analysis:", e); setLoading(false); });
  }, []);

  return { data, loading };
}
