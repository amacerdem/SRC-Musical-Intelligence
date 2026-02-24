import { useEffect } from 'react';
import GlassPanel from '../components/layout/GlassPanel';
import SignalTrace from '../components/charts/SignalTrace';
import Waveform from '../components/audio/Waveform';
import { usePipelineStore } from '../stores/pipelineStore';
import { useAudioStore } from '../stores/audioStore';
import { useNavigationStore } from '../stores/navigationStore';
import { useExperimentData } from '../hooks/useExperimentData';
import { colors, RELAY_INFO } from '../design/tokens';

interface Props {
  initialTab?: string;
}

export default function C3LayerView({ initialTab }: Props) {
  const { r3Frames, rewardData, ramData, relayCache, currentExperimentId } = usePipelineStore();
  const { currentFrame } = useAudioStore();
  const { navigateIn } = useNavigationStore();
  const { loadBeliefs, loadNeuro, loadRelay } = useExperimentData();

  // Load relays on mount
  useEffect(() => {
    for (const r of RELAY_INFO) {
      loadRelay(r.name, r.dim);
    }
    loadBeliefs();
    loadNeuro();
  }, [currentExperimentId]);

  if (!currentExperimentId) {
    return (
      <div className="flex items-center justify-center h-full">
        <GlassPanel className="p-8" glow="c3">
          <h2 className="text-lg font-semibold mb-2" style={{ color: colors.c3 }}>C\u00B3 Cognition</h2>
          <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>Run a pipeline to explore the cognitive brain.</p>
        </GlassPanel>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-3 p-4 h-full overflow-y-auto">
      <GlassPanel small className="p-2">
        <Waveform height={30} />
      </GlassPanel>

      {/* 9 Relay cards — the neural architecture */}
      <div className="grid grid-cols-3 gap-3">
        {RELAY_INFO.map((relay) => {
          const cached = relayCache[relay.name];
          const isLoaded = !!cached;

          // Mean output at cursor
          let meanVal = 0;
          if (cached && currentFrame < r3Frames) {
            for (let d = 0; d < cached.dim; d++) {
              meanVal += cached.data[currentFrame * cached.dim + d];
            }
            meanVal /= cached.dim;
          }

          return (
            <GlassPanel
              key={relay.name}
              small
              className="p-3 cursor-pointer transition-all hover:scale-[1.01]"
              onClick={() => navigateIn({ type: 'relay', name: relay.name })}
              style={{ borderColor: `${relay.color}20` }}
            >
              <div className="flex items-center justify-between mb-1">
                <div className="flex items-center gap-2">
                  <span
                    className="w-2.5 h-2.5 rounded-full"
                    style={{
                      background: relay.color,
                      boxShadow: meanVal > 0.2 ? `0 0 ${meanVal * 12}px ${relay.color}50` : 'none',
                    }}
                  />
                  <span className="text-xs font-semibold" style={{ color: relay.color }}>
                    {relay.name}
                  </span>
                  <span className="text-[10px]" style={{ color: 'var(--text-muted)' }}>
                    {relay.unit}
                  </span>
                </div>
                <span className="font-data text-[10px]" style={{ color: 'var(--text-muted)' }}>
                  {relay.dim}D
                </span>
              </div>

              {/* Mini trace */}
              {isLoaded ? (
                <SignalTrace
                  data={cached.data}
                  nFeatures={cached.dim}
                  nFrames={r3Frames}
                  signals={[{ name: relay.name, color: relay.color, featureIndex: 0 }]}
                  height={40}
                />
              ) : (
                <div className="h-10 flex items-center justify-center text-[10px]" style={{ color: 'var(--text-muted)' }}>
                  Loading...
                </div>
              )}

              <div className="flex items-center justify-between mt-1">
                <span className="text-[10px] truncate" style={{ color: 'var(--text-muted)' }}>
                  {relay.detail}
                </span>
                {isLoaded && (
                  <span className="font-data text-xs" style={{ color: relay.color }}>
                    {meanVal.toFixed(3)}
                  </span>
                )}
              </div>
            </GlassPanel>
          );
        })}
      </div>

      {/* Quick links */}
      <div className="flex gap-3">
        <GlassPanel
          small
          className="flex-1 p-3 cursor-pointer hover:scale-[1.01] transition-all"
          onClick={() => navigateIn({ type: 'beliefs' })}
        >
          <div className="text-xs font-medium mb-1" style={{ color: colors.c3 }}>131 Beliefs</div>
          <div className="text-[10px]" style={{ color: 'var(--text-muted)' }}>
            36 Core (Bayesian PE) + 65 Appraisal + 30 Anticipation
          </div>
        </GlassPanel>

        <GlassPanel
          small
          className="flex-1 p-3 cursor-pointer hover:scale-[1.01] transition-all"
          onClick={() => navigateIn({ type: 'ram' })}
        >
          <div className="text-xs font-medium mb-1" style={{ color: colors.c3 }}>RAM</div>
          <div className="text-[10px]" style={{ color: 'var(--text-muted)' }}>
            26 brain regions \u00B7 STG convergence hub
          </div>
        </GlassPanel>

        <GlassPanel
          small
          className="flex-1 p-3 cursor-pointer hover:scale-[1.01] transition-all"
          onClick={() => navigateIn({ type: 'reward' })}
          style={{ borderColor: `${colors.reward}20` }}
        >
          <div className="text-xs font-medium mb-1" style={{ color: colors.reward }}>Reward</div>
          <div className="font-data text-sm" style={{ color: rewardData && rewardData[currentFrame] > 0 ? colors.c3 : colors.danger }}>
            {rewardData ? (rewardData[currentFrame] > 0 ? '+' : '') + rewardData[currentFrame]?.toFixed(4) : 'N/A'}
          </div>
        </GlassPanel>
      </div>

      <div className="flex items-center gap-4 px-2">
        <span className="font-data text-xs" style={{ color: 'var(--text-muted)' }}>
          9 relays \u00B7 131 beliefs \u00B7 9 functions \u00B7 26 brain regions \u00B7 4 neuro channels
        </span>
      </div>
    </div>
  );
}
