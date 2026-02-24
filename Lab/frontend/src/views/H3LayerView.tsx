import { useState, useMemo } from 'react';
import GlassPanel from '../components/layout/GlassPanel';
import HeatmapChart from '../components/charts/HeatmapChart';
import Waveform from '../components/audio/Waveform';
import { usePipelineStore } from '../stores/pipelineStore';
import { colors } from '../design/tokens';

const MORPHS = [
  'value','mean','std','median','max','range','skewness','kurtosis',
  'velocity','velocity_mean','velocity_std','acceleration','acceleration_mean',
  'acceleration_std','periodicity','smoothness','curvature','shape_period',
  'trend','stability','entropy','zero_crossings','peaks','symmetry',
];

const LAWS = ['L0 Memory', 'L1 Prediction', 'L2 Integration'];

const HORIZON_BANDS = [
  { name: 'Micro', range: [0, 8], color: '#60a5fa', detail: '5.8ms-250ms \u00B7 Sensory' },
  { name: 'Meso', range: [8, 16], color: '#a78bfa', detail: '300ms-800ms \u00B7 Beat' },
  { name: 'Macro', range: [16, 24], color: '#f59e0b', detail: '1s-25s \u00B7 Section' },
  { name: 'Ultra', range: [24, 32], color: '#ef4444', detail: '36s-981s \u00B7 Form' },
];

export default function H3LayerView() {
  const { h3Tuples, h3Values, h3NTuples, r3Names, r3Frames } = usePipelineStore();
  const [selectedR3, setSelectedR3] = useState(0);
  const [selectedMorph, setSelectedMorph] = useState(8);
  const [selectedLaw, setSelectedLaw] = useState(0);

  const hasData = h3Tuples !== null && h3NTuples > 0;

  const heatmapData = useMemo(() => {
    if (!hasData || !h3Tuples || !h3Values) return null;
    const nFrames = r3Frames;
    const result = new Float32Array(32 * nFrames);
    for (let i = 0; i < h3NTuples; i++) {
      if (h3Tuples[i * 4] === selectedR3 && h3Tuples[i * 4 + 2] === selectedMorph && h3Tuples[i * 4 + 3] === selectedLaw) {
        const horizon = h3Tuples[i * 4 + 1];
        for (let f = 0; f < nFrames; f++) {
          result[horizon * nFrames + f] = h3Values[i * nFrames + f];
        }
      }
    }
    return result;
  }, [hasData, h3Tuples, h3Values, h3NTuples, r3Frames, selectedR3, selectedMorph, selectedLaw]);

  const horizonLabels = Array.from({ length: 32 }, (_, i) => `H${i}`);

  if (!hasData) {
    return (
      <div className="flex items-center justify-center h-full">
        <GlassPanel className="p-8" glow="h3">
          <h2 className="text-lg font-semibold mb-2" style={{ color: colors.h3 }}>H\u00B3 Temporal</h2>
          <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>Run a pipeline to view temporal morphologies.</p>
        </GlassPanel>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-3 p-4 h-full overflow-y-auto">
      <GlassPanel small className="p-2">
        <Waveform height={30} />
      </GlassPanel>

      {/* Controls */}
      <div className="flex gap-3">
        <GlassPanel small className="p-3 flex-1">
          <label className="text-xs mb-1 block" style={{ color: 'var(--text-muted)' }}>R\u00B3 Feature</label>
          <select
            className="w-full px-2 py-1.5 rounded-lg text-sm font-data"
            style={{ background: 'rgba(255,255,255,0.04)', border: '1px solid rgba(255,255,255,0.08)', color: 'var(--text-primary)' }}
            value={selectedR3}
            onChange={(e) => setSelectedR3(Number(e.target.value))}
          >
            {r3Names.map((name, i) => (
              <option key={i} value={i}>[{i}] {name}</option>
            ))}
          </select>
        </GlassPanel>

        <GlassPanel small className="p-3 flex-1">
          <label className="text-xs mb-1 block" style={{ color: 'var(--text-muted)' }}>Morphology</label>
          <select
            className="w-full px-2 py-1.5 rounded-lg text-sm font-data"
            style={{ background: 'rgba(255,255,255,0.04)', border: '1px solid rgba(255,255,255,0.08)', color: 'var(--text-primary)' }}
            value={selectedMorph}
            onChange={(e) => setSelectedMorph(Number(e.target.value))}
          >
            {MORPHS.map((name, i) => (
              <option key={i} value={i}>M{i} {name}</option>
            ))}
          </select>
        </GlassPanel>

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

      {/* Heatmap */}
      <GlassPanel className="p-3" glow="h3">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium" style={{ color: colors.h3 }}>Horizon \u00D7 Time Heatmap</span>
          <span className="font-data text-xs" style={{ color: 'var(--text-muted)' }}>
            [{selectedR3}] {r3Names[selectedR3]} \u00B7 M{selectedMorph} {MORPHS[selectedMorph]} \u00B7 L{selectedLaw}
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
        <div className="flex gap-3 mt-2">
          {HORIZON_BANDS.map((band) => (
            <span key={band.name} className="flex items-center gap-1.5 text-xs">
              <span className="w-2 h-2 rounded-sm" style={{ background: band.color }} />
              <span style={{ color: 'var(--text-muted)' }}>{band.name} ({band.detail})</span>
            </span>
          ))}
        </div>
      </GlassPanel>

      <div className="flex items-center gap-4 px-2">
        <span className="font-data text-xs" style={{ color: 'var(--text-muted)' }}>
          {h3NTuples} tuples demanded \u00B7 {r3Frames} frames \u00B7 97\u00D732\u00D724\u00D73 = 223,488 theoretical
        </span>
      </div>
    </div>
  );
}
