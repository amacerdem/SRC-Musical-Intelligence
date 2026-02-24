import { useMemo } from 'react';
import GlassPanel from '../components/layout/GlassPanel';
import HeatmapChart from '../components/charts/HeatmapChart';
import Waveform from '../components/audio/Waveform';
import { usePipelineStore } from '../stores/pipelineStore';
import { useAudioStore } from '../stores/audioStore';
import { colors, RAM_REGIONS } from '../design/tokens';

export default function RamDetailView() {
  const { ramData, r3Frames } = usePipelineStore();
  const { currentFrame } = useAudioStore();

  const nRegions = 26;

  const curValues = useMemo(() => {
    if (!ramData || currentFrame >= r3Frames) return null;
    const vals: number[] = [];
    for (let r = 0; r < nRegions; r++) {
      vals.push(ramData[currentFrame * nRegions + r]);
    }
    return vals;
  }, [ramData, currentFrame, r3Frames]);

  if (!ramData) {
    return (
      <div className="flex items-center justify-center h-full">
        <GlassPanel className="p-8" glow="c3">
          <h2 className="text-lg font-semibold mb-2" style={{ color: colors.c3 }}>Region Activation Map</h2>
          <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>No RAM data available.</p>
        </GlassPanel>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-3 p-4 h-full overflow-y-auto">
      <GlassPanel small className="p-2">
        <Waveform height={30} />
      </GlassPanel>

      {/* Heatmap */}
      <GlassPanel className="p-3" glow="c3">
        <div className="text-sm font-medium mb-2" style={{ color: colors.c3 }}>
          Region Activation Map \u2014 26 Regions \u00D7 Time
        </div>
        <HeatmapChart
          data={ramData}
          nRows={nRegions}
          nCols={r3Frames}
          height={350}
          rowLabels={RAM_REGIONS}
          colormap="magma"
          valueRange={[0, 1]}
        />
      </GlassPanel>

      {/* Current values */}
      {curValues && (
        <GlassPanel small className="p-3">
          <div className="text-xs mb-2" style={{ color: 'var(--text-muted)' }}>Activation at Frame {currentFrame}</div>
          <div className="grid grid-cols-4 gap-x-4 gap-y-1">
            {RAM_REGIONS.map((region, i) => (
              <div key={region} className="flex items-center justify-between">
                <span className="text-xs" style={{ color: 'var(--text-secondary)' }}>{region}</span>
                <div className="flex items-center gap-1.5">
                  <div className="w-12 h-1.5 rounded-full overflow-hidden" style={{ background: 'rgba(255,255,255,0.06)' }}>
                    <div
                      className="h-full rounded-full"
                      style={{ width: `${(curValues[i] || 0) * 100}%`, background: colors.c3 }}
                    />
                  </div>
                  <span className="font-data text-xs w-10 text-right">{(curValues[i] || 0).toFixed(3)}</span>
                </div>
              </div>
            ))}
          </div>
        </GlassPanel>
      )}

      {/* Region groups */}
      <div className="flex gap-3">
        {[
          { label: 'Cortical', count: 12, color: colors.c3 },
          { label: 'Subcortical', count: 9, color: colors.reward },
          { label: 'Brainstem', count: 5, color: colors.danger },
        ].map(g => (
          <GlassPanel key={g.label} small className="flex-1 p-3">
            <div className="text-xs" style={{ color: g.color }}>{g.label}</div>
            <div className="font-data text-sm" style={{ color: 'var(--text-primary)' }}>{g.count} regions</div>
          </GlassPanel>
        ))}
      </div>
    </div>
  );
}
