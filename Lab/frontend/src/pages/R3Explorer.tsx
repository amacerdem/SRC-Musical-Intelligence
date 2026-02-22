import { useState, useMemo } from 'react';
import GlassPanel from '../components/layout/GlassPanel';
import Waveform from '../components/audio/Waveform';
import Spectrogram from '../components/audio/Spectrogram';
import SignalTrace from '../components/charts/SignalTrace';
import { usePipelineStore } from '../stores/pipelineStore';
import { useAudioStore } from '../stores/audioStore';
import { R3_GROUPS, R3_GROUP_COLORS, FRAME_RATE, colors } from '../design/tokens';

export default function R3Explorer() {
  const { r3Features, r3Names, r3Frames } = usePipelineStore();
  const { currentTime, currentFrame } = useAudioStore();
  const [expandedGroup, setExpandedGroup] = useState<string | null>(null);
  const [selectedFeatures, setSelectedFeatures] = useState<Set<number>>(new Set());

  const hasData = r3Features !== null && r3Frames > 0;

  // Build signals for each group
  const groupSignals = useMemo(() => {
    if (!hasData) return {};
    const result: Record<string, { name: string; color: string; featureIndex: number }[]> = {};
    for (const group of R3_GROUPS) {
      const [start, end] = group.range;
      const baseColor = R3_GROUP_COLORS[group.key];
      result[group.key] = [];
      for (let i = start; i < end; i++) {
        result[group.key].push({
          name: r3Names[i] || `f${i}`,
          color: baseColor,
          featureIndex: i,
        });
      }
    }
    return result;
  }, [hasData, r3Names]);

  // Current values at cursor
  const cursorValues = useMemo(() => {
    if (!r3Features || currentFrame >= r3Frames) return null;
    const values: number[] = [];
    for (let i = 0; i < 97; i++) {
      values.push(r3Features[currentFrame * 97 + i]);
    }
    return values;
  }, [r3Features, currentFrame, r3Frames]);

  if (!hasData) {
    return (
      <div className="flex flex-col gap-4 p-4 h-full">
        <GlassPanel className="p-6 flex-1 flex items-center justify-center" glow="r3">
          <div className="text-center">
            <h2 className="text-lg font-semibold mb-2" style={{ color: colors.r3 }}>R³ Explorer</h2>
            <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>
              Run a pipeline first to visualize R³ features.
            </p>
            <p className="text-xs mt-2" style={{ color: 'var(--text-muted)' }}>
              97 features · 9 groups · [0, 1] normalized
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
        <Waveform height={40} />
        <div className="mt-1">
          <Spectrogram height={60} />
        </div>
      </GlassPanel>

      {/* R³ Group traces */}
      {R3_GROUPS.map((group) => {
        const signals = groupSignals[group.key] || [];
        const isExpanded = expandedGroup === group.key;
        const [start, end] = group.range;

        return (
          <GlassPanel
            key={group.key}
            small
            className="p-3"
            style={{ borderColor: isExpanded ? R3_GROUP_COLORS[group.key] + '30' : undefined }}
          >
            {/* Group header */}
            <div
              className="flex items-center justify-between cursor-pointer mb-2"
              onClick={() => setExpandedGroup(isExpanded ? null : group.key)}
            >
              <div className="flex items-center gap-2">
                <span
                  className="w-2.5 h-2.5 rounded-sm"
                  style={{ background: R3_GROUP_COLORS[group.key] }}
                />
                <span className="text-sm font-medium">{group.key}</span>
                <span className="text-xs" style={{ color: 'var(--text-muted)' }}>
                  {group.name} · {end - start}D [{start}:{end}]
                </span>
              </div>

              {/* Cursor values */}
              {cursorValues && (
                <div className="flex gap-1.5">
                  {signals.slice(0, isExpanded ? signals.length : 4).map((s) => (
                    <span key={s.featureIndex} className="font-data text-xs" style={{ color: 'var(--text-muted)' }}>
                      {cursorValues[s.featureIndex]?.toFixed(3)}
                    </span>
                  ))}
                  {!isExpanded && signals.length > 4 && (
                    <span className="text-xs" style={{ color: 'var(--text-muted)' }}>+{signals.length - 4}</span>
                  )}
                </div>
              )}
            </div>

            {/* Compact trace (all features overlaid) */}
            <SignalTrace
              data={r3Features}
              nFeatures={97}
              nFrames={r3Frames}
              signals={signals}
              height={isExpanded ? 0 : 50}
            />

            {/* Expanded: individual traces per feature */}
            {isExpanded && (
              <div className="flex flex-col gap-2 mt-2">
                {signals.map((signal) => (
                  <div key={signal.featureIndex}>
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs" style={{ color: R3_GROUP_COLORS[group.key] }}>
                        [{signal.featureIndex}] {signal.name}
                      </span>
                      {cursorValues && (
                        <span className="font-data text-xs" style={{ color: 'var(--text-primary)' }}>
                          {cursorValues[signal.featureIndex]?.toFixed(4)}
                        </span>
                      )}
                    </div>
                    <SignalTrace
                      data={r3Features}
                      nFeatures={97}
                      nFrames={r3Frames}
                      signals={[signal]}
                      height={40}
                    />
                  </div>
                ))}
              </div>
            )}
          </GlassPanel>
        );
      })}

      {/* Stats footer */}
      <div className="flex items-center gap-4 px-2 py-1">
        <span className="font-data text-xs" style={{ color: 'var(--text-muted)' }}>
          {r3Frames} frames · {(r3Frames / FRAME_RATE).toFixed(1)}s · 97D
        </span>
      </div>
    </div>
  );
}
