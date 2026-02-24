import { useEffect } from 'react';
import GlassPanel from '../components/layout/GlassPanel';
import SignalTrace from '../components/charts/SignalTrace';
import Waveform from '../components/audio/Waveform';
import { usePipelineStore } from '../stores/pipelineStore';
import { useAudioStore } from '../stores/audioStore';
import { useExperimentData } from '../hooks/useExperimentData';
import { NEURO_CHANNELS, colors } from '../design/tokens';

export default function NeuroDetailView() {
  const { neuroData, r3Frames, currentExperimentId } = usePipelineStore();
  const { currentFrame } = useAudioStore();
  const { loadNeuro } = useExperimentData();

  useEffect(() => {
    loadNeuro();
  }, [currentExperimentId]);

  if (!neuroData) {
    return (
      <div className="flex items-center justify-center h-full">
        <GlassPanel className="p-8">
          <h2 className="text-lg font-semibold mb-2" style={{ color: '#ef4444' }}>Neurochemical State</h2>
          <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>Loading neuro data...</p>
        </GlassPanel>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-3 p-4 h-full overflow-y-auto">
      <GlassPanel small className="p-2">
        <Waveform height={30} />
      </GlassPanel>

      {/* All 4 channels */}
      {NEURO_CHANNELS.map((ch, i) => {
        const curVal = currentFrame < r3Frames ? neuroData[currentFrame * 4 + i] : 0;
        return (
          <GlassPanel key={ch.short} small className="p-3">
            <div className="flex items-center justify-between mb-1">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full" style={{ background: ch.color }} />
                <span className="text-xs font-semibold" style={{ color: ch.color }}>{ch.name}</span>
                <span className="text-[10px]" style={{ color: 'var(--text-muted)' }}>{ch.short}</span>
              </div>
              <span className="font-data text-sm" style={{ color: ch.color }}>{curVal.toFixed(4)}</span>
            </div>
            <SignalTrace
              data={neuroData}
              nFeatures={4}
              nFrames={r3Frames}
              signals={[{ name: ch.short, color: ch.color, featureIndex: i }]}
              height={70}
            />
          </GlassPanel>
        );
      })}

      {/* Info */}
      <GlassPanel small className="p-3">
        <div className="text-xs" style={{ color: 'var(--text-muted)' }}>
          DA: reward, motivation, salience \u00B7
          NE: arousal, attention \u00B7
          OPI: pleasure, analgesia \u00B7
          5HT: mood, tonal stability
        </div>
      </GlassPanel>
    </div>
  );
}
