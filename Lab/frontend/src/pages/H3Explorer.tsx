import { useState, useMemo } from 'react';
import GlassPanel from '../components/layout/GlassPanel';
import HeatmapChart from '../components/charts/HeatmapChart';
import SignalTrace from '../components/charts/SignalTrace';
import Waveform from '../components/audio/Waveform';
import { usePipelineStore } from '../stores/pipelineStore';
import { useAudioStore } from '../stores/audioStore';
import { colors, FRAME_RATE } from '../design/tokens';

const MORPHS = [
  'value','mean','std','median','max','range','skewness','kurtosis',
  'velocity','velocity_mean','velocity_std','acceleration','acceleration_mean',
  'acceleration_std','periodicity','smoothness','curvature','shape_period',
  'trend','stability','entropy','zero_crossings','peaks','symmetry',
];

const LAWS = ['L0 Memory', 'L1 Prediction', 'L2 Integration'];

const HORIZON_BANDS = [
  { name: 'Micro', range: [0, 8], color: '#60a5fa' },
  { name: 'Meso', range: [8, 16], color: '#a78bfa' },
  { name: 'Macro', range: [16, 24], color: '#f59e0b' },
  { name: 'Ultra', range: [24, 32], color: '#ef4444' },
];

export default function H3Explorer() {
  const { h3Tuples, h3Values, h3NTuples, r3Names, r3Frames } = usePipelineStore();
  const [selectedR3, setSelectedR3] = useState(0);
  const [selectedMorph, setSelectedMorph] = useState(8); // velocity
  const [selectedLaw, setSelectedLaw] = useState(0);    // L0

  const hasData = h3Tuples !== null && h3NTuples > 0;

  // Build horizon × time heatmap for selected r3/morph/law
  const heatmapData = useMemo(() => {
    if (!hasData || !h3Tuples || !h3Values) return null;

    const nFrames = r3Frames;
    const nHorizons = 32;
    const result = new Float32Array(nHorizons * nFrames);

    for (let i = 0; i < h3NTuples; i++) {
      const r3Idx = h3Tuples[i * 4];
      const horizon = h3Tuples[i * 4 + 1];
      const morph = h3Tuples[i * 4 + 2];
      const law = h3Tuples[i * 4 + 3];

      if (r3Idx === selectedR3 && morph === selectedMorph && law === selectedLaw) {
        // Copy this tuple's values into the heatmap row
        for (let f = 0; f < nFrames; f++) {
          result[horizon * nFrames + f] = h3Values[i * nFrames + f];
        }
      }
    }
    return result;
  }, [hasData, h3Tuples, h3Values, h3NTuples, r3Frames, selectedR3, selectedMorph, selectedLaw]);

  // Available tuples for current selection
  const availableTuples = useMemo(() => {
    if (!h3Tuples) return [];
    const tuples: { r3: number; h: number; m: number; l: number; index: number }[] = [];
    for (let i = 0; i < h3NTuples; i++) {
      tuples.push({
        r3: h3Tuples[i * 4],
        h: h3Tuples[i * 4 + 1],
        m: h3Tuples[i * 4 + 2],
        l: h3Tuples[i * 4 + 3],
        index: i,
      });
    }
    return tuples;
  }, [h3Tuples, h3NTuples]);

  const horizonLabels = Array.from({ length: 32 }, (_, i) => `H${i}`);

  if (!hasData) {
    return (
      <div className="flex flex-col gap-4 p-4 h-full">
        <GlassPanel className="p-6 flex-1 flex items-center justify-center" glow="h3">
          <div className="text-center">
            <h2 className="text-lg font-semibold mb-2" style={{ color: colors.h3 }}>H³ Explorer</h2>
            <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
              Run a pipeline first to visualize H³ morphologies.
            </p>
            <p className="text-xs mt-2" style={{ color: 'var(--text-muted)' }}>
              32 horizons · 24 morphs · 3 laws
            </p>
          </div>
        </GlassPanel>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-3 p-4 h-full overflow-y-auto">
      {/* Audio timeline */}
      <GlassPanel small className="p-3">
        <Waveform height={30} />
      </GlassPanel>

      {/* Controls */}
      <div className="flex gap-3">
        {/* R³ feature selector */}
        <GlassPanel small className="p-3 flex-1">
          <label className="text-xs mb-1 block" style={{ color: 'var(--text-muted)' }}>R³ Feature</label>
          <select
            className="w-full px-2 py-1.5 rounded-lg text-sm font-data"
            style={{
              background: 'rgba(255,255,255,0.04)',
              border: '1px solid rgba(255,255,255,0.08)',
              color: 'var(--text-primary)',
            }}
            value={selectedR3}
            onChange={(e) => setSelectedR3(Number(e.target.value))}
          >
            {r3Names.map((name, i) => (
              <option key={i} value={i}>[{i}] {name}</option>
            ))}
          </select>
        </GlassPanel>

        {/* Morph selector */}
        <GlassPanel small className="p-3 flex-1">
          <label className="text-xs mb-1 block" style={{ color: 'var(--text-muted)' }}>Morphology</label>
          <select
            className="w-full px-2 py-1.5 rounded-lg text-sm font-data"
            style={{
              background: 'rgba(255,255,255,0.04)',
              border: '1px solid rgba(255,255,255,0.08)',
              color: 'var(--text-primary)',
            }}
            value={selectedMorph}
            onChange={(e) => setSelectedMorph(Number(e.target.value))}
          >
            {MORPHS.map((name, i) => (
              <option key={i} value={i}>M{i} {name}</option>
            ))}
          </select>
        </GlassPanel>

        {/* Law selector */}
        <GlassPanel small className="p-3">
          <label className="text-xs mb-1 block" style={{ color: 'var(--text-muted)' }}>Law</label>
          <div className="flex gap-1.5">
            {LAWS.map((name, i) => (
              <button
                key={i}
                onClick={() => setSelectedLaw(i)}
                className="px-3 py-1.5 rounded-lg text-xs font-data transition-colors"
                style={{
                  background: selectedLaw === i ? `${colors.h3}20` : 'rgba(255,255,255,0.03)',
                  color: selectedLaw === i ? colors.h3 : 'var(--text-muted)',
                  border: `1px solid ${selectedLaw === i ? colors.h3 + '30' : 'rgba(255,255,255,0.06)'}`,
                }}
              >
                L{i}
              </button>
            ))}
          </div>
        </GlassPanel>
      </div>

      {/* Horizon × Time heatmap */}
      <GlassPanel className="p-3" glow="h3">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium" style={{ color: colors.h3 }}>
            Horizon × Time Heatmap
          </span>
          <span className="font-data text-xs" style={{ color: 'var(--text-muted)' }}>
            [{selectedR3}] {r3Names[selectedR3]} · M{selectedMorph} {MORPHS[selectedMorph]} · L{selectedLaw}
          </span>
        </div>
        <HeatmapChart
          data={heatmapData}
          nRows={32}
          nCols={r3Frames}
          height={280}
          rowLabels={horizonLabels}
          colormap="viridis"
        />
        {/* Band labels */}
        <div className="flex gap-3 mt-2">
          {HORIZON_BANDS.map((band) => (
            <span key={band.name} className="flex items-center gap-1.5 text-xs">
              <span className="w-2 h-2 rounded-sm" style={{ background: band.color }} />
              <span style={{ color: 'var(--text-muted)' }}>{band.name} (H{band.range[0]}-H{band.range[1] - 1})</span>
            </span>
          ))}
        </div>
      </GlassPanel>

      {/* Stats */}
      <div className="flex items-center gap-4 px-2">
        <span className="font-data text-xs" style={{ color: 'var(--text-muted)' }}>
          {h3NTuples} tuples demanded · {r3Frames} frames
        </span>
        <span className="font-data text-xs" style={{ color: 'var(--text-muted)' }}>
          {availableTuples.filter(t => t.r3 === selectedR3).length} tuples for [{selectedR3}]
        </span>
      </div>
    </div>
  );
}
