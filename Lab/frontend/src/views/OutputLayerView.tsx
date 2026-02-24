import { useMemo } from 'react';
import GlassPanel from '../components/layout/GlassPanel';
import SignalTrace from '../components/charts/SignalTrace';
import HeatmapChart from '../components/charts/HeatmapChart';
import Waveform from '../components/audio/Waveform';
import { usePipelineStore } from '../stores/pipelineStore';
import { useAudioStore } from '../stores/audioStore';
import { useNavigationStore } from '../stores/navigationStore';
import { colors, RAM_REGIONS, FRAME_RATE } from '../design/tokens';

export default function OutputLayerView() {
  const { rewardData, ramData, r3Frames, r3Features } = usePipelineStore();
  const { currentFrame } = useAudioStore();
  const { navigateIn } = useNavigationStore();

  const hasReward = rewardData !== null && r3Frames > 0;

  // Reward stats
  const rewardStats = useMemo(() => {
    if (!rewardData) return null;
    const n = rewardData.length;
    let sum = 0, posCount = 0;
    for (let i = 0; i < n; i++) {
      sum += rewardData[i];
      if (rewardData[i] > 0) posCount++;
    }
    return { mean: sum / n, positivePct: (posCount / n) * 100, n };
  }, [rewardData]);

  // Energy signal
  const energySignal = useMemo(() => {
    if (!r3Features || r3Frames === 0) return null;
    const energy = new Float32Array(r3Frames);
    for (let t = 0; t < r3Frames; t++) {
      let sum = 0;
      for (let f = 7; f < 12; f++) sum += r3Features[t * 97 + f];
      energy[t] = sum / 5;
    }
    return energy;
  }, [r3Features, r3Frames]);

  if (!hasReward) {
    return (
      <div className="flex items-center justify-center h-full">
        <GlassPanel className="p-8" glow="reward">
          <h2 className="text-lg font-semibold mb-2" style={{ color: colors.reward }}>Output Layer</h2>
          <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>Run a pipeline to view outputs.</p>
        </GlassPanel>
      </div>
    );
  }

  const curReward = currentFrame < r3Frames ? rewardData![currentFrame] : 0;

  return (
    <div className="flex flex-col gap-3 p-4 h-full overflow-y-auto">
      <GlassPanel small className="p-2">
        <Waveform height={30} />
      </GlassPanel>

      {/* Reward card — clickable */}
      <GlassPanel
        className="p-4 cursor-pointer hover:scale-[1.005] transition-all"
        glow="reward"
        onClick={() => navigateIn({ type: 'reward' })}
      >
        <div className="flex items-center justify-between mb-2">
          <h2 className="text-sm font-medium" style={{ color: colors.reward }}>Reward Signal</h2>
          <span className="font-data text-lg" style={{ color: curReward > 0 ? colors.c3 : colors.danger }}>
            {curReward > 0 ? '+' : ''}{curReward.toFixed(4)}
          </span>
        </div>
        <SignalTrace
          data={rewardData!}
          nFeatures={1}
          nFrames={r3Frames}
          signals={[{ name: 'reward', color: colors.reward, featureIndex: 0 }]}
          height={100}
          yRange={[-0.3, 0.5]}
        />
        {rewardStats && (
          <div className="flex gap-4 mt-2">
            <span className="font-data text-xs" style={{ color: rewardStats.mean > 0 ? colors.c3 : colors.danger }}>
              mean={rewardStats.mean > 0 ? '+' : ''}{rewardStats.mean.toFixed(4)}
            </span>
            <span className="font-data text-xs" style={{ color: colors.reward }}>
              {rewardStats.positivePct.toFixed(1)}% positive
            </span>
          </div>
        )}
      </GlassPanel>

      {/* Secondary outputs */}
      <div className="grid grid-cols-2 gap-3">
        {/* Neuro */}
        <GlassPanel
          small
          className="p-3 cursor-pointer hover:scale-[1.01] transition-all"
          onClick={() => navigateIn({ type: 'neuro' })}
        >
          <div className="text-xs font-medium mb-1" style={{ color: '#ef4444' }}>Neurochemical State</div>
          <div className="text-[10px] mb-2" style={{ color: 'var(--text-muted)' }}>
            DA \u00B7 NE \u00B7 OPI \u00B7 5HT \u2014 4D
          </div>
          <div className="text-[10px] text-right" style={{ color: 'var(--text-muted)' }}>Click to explore \u203A</div>
        </GlassPanel>

        {/* RAM */}
        <GlassPanel
          small
          className="p-3 cursor-pointer hover:scale-[1.01] transition-all"
          onClick={() => navigateIn({ type: 'ram' })}
        >
          <div className="text-xs font-medium mb-1" style={{ color: colors.c3 }}>Region Activation Map</div>
          <div className="text-[10px] mb-2" style={{ color: 'var(--text-muted)' }}>
            26 regions \u00B7 12 cortical + 9 subcortical + 5 brainstem
          </div>
          <div className="text-[10px] text-right" style={{ color: 'var(--text-muted)' }}>Click to explore \u203A</div>
        </GlassPanel>
      </div>

      {/* Energy correlate */}
      {energySignal && (
        <GlassPanel small className="p-3">
          <div className="text-xs mb-1" style={{ color: 'var(--text-muted)' }}>
            Energy (R\u00B3 Group B mean) \u2014 salience correlate
          </div>
          <SignalTrace
            data={energySignal}
            nFeatures={1}
            nFrames={r3Frames}
            signals={[{ name: 'energy', color: colors.r3, featureIndex: 0 }]}
            height={50}
          />
        </GlassPanel>
      )}

      {/* Formula */}
      <GlassPanel small className="p-3">
        <div className="text-xs" style={{ color: 'var(--text-muted)' }}>
          R = salience \u00D7 (1.5\u00D7surprise + 0.8\u00D7resolution + 0.5\u00D7exploration - 0.6\u00D7monotony) \u00D7 fam_mod \u00D7 da_gain
        </div>
      </GlassPanel>
    </div>
  );
}
