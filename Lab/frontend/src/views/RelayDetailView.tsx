import { useEffect, useMemo } from 'react';
import GlassPanel from '../components/layout/GlassPanel';
import SignalTrace from '../components/charts/SignalTrace';
import Waveform from '../components/audio/Waveform';
import { usePipelineStore } from '../stores/pipelineStore';
import { useAudioStore } from '../stores/audioStore';
import { useExperimentData } from '../hooks/useExperimentData';
import { RELAY_INFO, colors } from '../design/tokens';

interface Props {
  relayName: string;
}

export default function RelayDetailView({ relayName }: Props) {
  const { relayCache, r3Frames, currentExperimentId } = usePipelineStore();
  const { currentFrame } = useAudioStore();
  const { loadRelay } = useExperimentData();

  const relayInfo = RELAY_INFO.find(r => r.name === relayName);
  const relayColor = relayInfo?.color || colors.c3;

  // Load relay data if not cached
  useEffect(() => {
    if (relayInfo) loadRelay(relayInfo.name, relayInfo.dim);
  }, [currentExperimentId, relayInfo]);

  const cached = relayCache[relayName];

  if (!cached) {
    return (
      <div className="flex items-center justify-center h-full">
        <GlassPanel className="p-8">
          <h2 className="text-lg font-semibold mb-2" style={{ color: relayColor }}>{relayName}</h2>
          <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>Loading relay data...</p>
        </GlassPanel>
      </div>
    );
  }

  const { data, dim } = cached;

  return (
    <div className="flex flex-col gap-3 p-4 h-full overflow-y-auto">
      <GlassPanel small className="p-2">
        <Waveform height={30} />
      </GlassPanel>

      {/* Header */}
      <div className="flex items-center gap-3 px-1">
        <span className="w-3 h-3 rounded-full" style={{ background: relayColor }} />
        <span className="text-sm font-semibold" style={{ color: relayColor }}>
          {relayName}
        </span>
        <span className="text-xs" style={{ color: 'var(--text-muted)' }}>
          {relayInfo?.unit} \u00B7 {relayInfo?.detail}
        </span>
        <span className="font-data text-xs ml-auto" style={{ color: 'var(--text-muted)' }}>
          {dim}D
        </span>
      </div>

      {/* All dimensions overview */}
      <GlassPanel className="p-3">
        <div className="text-xs mb-2" style={{ color: 'var(--text-muted)' }}>All {dim} dimensions</div>
        <SignalTrace
          data={data}
          nFeatures={dim}
          nFrames={r3Frames}
          signals={Array.from({ length: Math.min(dim, 6) }, (_, i) => ({
            name: `${relayName}[${i}]`,
            color: relayColor,
            featureIndex: i,
          }))}
          height={120}
        />
      </GlassPanel>

      {/* Individual dimension traces */}
      <div className="grid grid-cols-2 gap-3">
        {Array.from({ length: dim }, (_, i) => {
          const dimData = new Float32Array(r3Frames);
          for (let t = 0; t < r3Frames; t++) {
            dimData[t] = data[t * dim + i];
          }
          const curVal = currentFrame < r3Frames ? dimData[currentFrame] : 0;

          return (
            <GlassPanel key={i} small className="p-3">
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs" style={{ color: relayColor }}>
                  [{i}]
                </span>
                <span className="font-data text-xs">{curVal.toFixed(4)}</span>
              </div>
              <SignalTrace
                data={dimData}
                nFeatures={1}
                nFrames={r3Frames}
                signals={[{ name: `dim${i}`, color: relayColor, featureIndex: 0 }]}
                height={40}
              />
            </GlassPanel>
          );
        })}
      </div>
    </div>
  );
}
