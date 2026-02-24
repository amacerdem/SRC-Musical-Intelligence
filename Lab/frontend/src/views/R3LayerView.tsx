import { useMemo } from 'react';
import GlassPanel from '../components/layout/GlassPanel';
import SignalTrace from '../components/charts/SignalTrace';
import Waveform from '../components/audio/Waveform';
import { usePipelineStore } from '../stores/pipelineStore';
import { useAudioStore } from '../stores/audioStore';
import { useNavigationStore } from '../stores/navigationStore';
import { R3_GROUPS, R3_GROUP_COLORS, colors } from '../design/tokens';

export default function R3LayerView() {
  const { r3Features, r3Names, r3Frames } = usePipelineStore();
  const { currentFrame } = useAudioStore();
  const { navigateIn } = useNavigationStore();

  const hasData = r3Features !== null && r3Frames > 0;

  // Group mean energies at cursor
  const cursorValues = useMemo(() => {
    if (!r3Features || currentFrame >= r3Frames) return null;
    const result: Record<string, number> = {};
    for (const g of R3_GROUPS) {
      const [start, end] = g.range;
      let sum = 0;
      for (let i = start; i < end; i++) sum += r3Features[currentFrame * 97 + i];
      result[g.key] = sum / (end - start);
    }
    return result;
  }, [r3Features, currentFrame, r3Frames]);

  if (!hasData) {
    return (
      <div className="flex items-center justify-center h-full">
        <GlassPanel className="p-8" glow="r3">
          <h2 className="text-lg font-semibold mb-2" style={{ color: colors.r3 }}>R\u00B3 Perception</h2>
          <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>Run a pipeline to view spectral features.</p>
        </GlassPanel>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-3 p-4 h-full overflow-y-auto">
      {/* Compact waveform */}
      <GlassPanel small className="p-2">
        <Waveform height={30} />
      </GlassPanel>

      {/* Group cards — 3 per row */}
      <div className="grid grid-cols-3 gap-3">
        {R3_GROUPS.map((group) => {
          const [start, end] = group.range;
          const dim = end - start;
          const groupColor = R3_GROUP_COLORS[group.key];
          const energy = cursorValues?.[group.key] ?? 0;

          // Build group signal data (extract slice from r3Features)
          const groupData = new Float32Array(r3Frames * dim);
          for (let t = 0; t < r3Frames; t++) {
            for (let f = 0; f < dim; f++) {
              groupData[t * dim + f] = r3Features![t * 97 + start + f];
            }
          }

          // Use first feature as representative
          const signals = [{ name: r3Names[start] || `f${start}`, color: groupColor, featureIndex: 0 }];

          return (
            <GlassPanel
              key={group.key}
              small
              className="p-3 cursor-pointer transition-all hover:scale-[1.01]"
              onClick={() => navigateIn({ type: 'r3group', key: group.key, name: group.name })}
              style={{
                borderColor: `${groupColor}25`,
                ['--pulse-color' as any]: `${groupColor}30`,
              }}
            >
              <div className="flex items-center justify-between mb-1">
                <div className="flex items-center gap-2">
                  <span
                    className="w-3 h-3 rounded-full"
                    style={{
                      background: groupColor,
                      boxShadow: energy > 0.2 ? `0 0 ${energy * 15}px ${groupColor}60` : 'none',
                    }}
                  />
                  <span className="text-xs font-semibold" style={{ color: groupColor }}>
                    {group.key} {group.name}
                  </span>
                </div>
                <span className="font-data text-[10px]" style={{ color: 'var(--text-muted)' }}>
                  {dim}D [{start}:{end}]
                </span>
              </div>

              {/* Mini trace */}
              <SignalTrace
                data={groupData}
                nFeatures={dim}
                nFrames={r3Frames}
                signals={signals}
                height={45}
              />

              {/* Current value */}
              <div className="flex items-center justify-between mt-1">
                <span className="text-[10px]" style={{ color: 'var(--text-muted)' }}>
                  {group.detail}
                </span>
                <span className="font-data text-xs" style={{ color: groupColor }}>
                  {energy.toFixed(3)}
                </span>
              </div>

              {/* Click hint */}
              <div className="text-[10px] mt-1 text-right" style={{ color: 'var(--text-muted)' }}>
                Click to explore \u203A
              </div>
            </GlassPanel>
          );
        })}
      </div>

      {/* Footer stats */}
      <div className="flex items-center gap-4 px-2 py-1">
        <span className="font-data text-xs" style={{ color: 'var(--text-muted)' }}>
          97 features \u00B7 9 groups \u00B7 {r3Frames} frames \u00B7 Frozen boundary
        </span>
      </div>
    </div>
  );
}
