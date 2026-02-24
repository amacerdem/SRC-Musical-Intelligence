import { useMemo } from 'react';
import GlassPanel from '../components/layout/GlassPanel';
import SignalTrace from '../components/charts/SignalTrace';
import Waveform from '../components/audio/Waveform';
import { usePipelineStore } from '../stores/pipelineStore';
import { useAudioStore } from '../stores/audioStore';
import { colors, FRAME_RATE } from '../design/tokens';

export default function RewardDetailView() {
  const { rewardData, r3Frames, r3Features } = usePipelineStore();
  const { currentFrame } = useAudioStore();

  const hasData = rewardData !== null && r3Frames > 0;

  const stats = useMemo(() => {
    if (!rewardData) return null;
    const n = rewardData.length;
    let sum = 0, posCount = 0, maxVal = -Infinity, minVal = Infinity;
    let maxIdx = 0, minIdx = 0;
    for (let i = 0; i < n; i++) {
      sum += rewardData[i];
      if (rewardData[i] > 0) posCount++;
      if (rewardData[i] > maxVal) { maxVal = rewardData[i]; maxIdx = i; }
      if (rewardData[i] < minVal) { minVal = rewardData[i]; minIdx = i; }
    }
    const mean = sum / n;
    let varSum = 0;
    for (let i = 0; i < n; i++) varSum += (rewardData[i] - mean) ** 2;
    return {
      mean, std: Math.sqrt(varSum / n), min: minVal, max: maxVal,
      positivePct: (posCount / n) * 100,
      peakTime: maxIdx / FRAME_RATE, troughTime: minIdx / FRAME_RATE, n,
    };
  }, [rewardData]);

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

  if (!hasData) {
    return (
      <div className="flex items-center justify-center h-full">
        <GlassPanel className="p-8" glow="reward">
          <h2 className="text-lg font-semibold mb-2" style={{ color: colors.reward }}>Reward Analyzer</h2>
          <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>No reward data available.</p>
        </GlassPanel>
      </div>
    );
  }

  const curVal = currentFrame < r3Frames ? rewardData![currentFrame] : 0;

  return (
    <div className="flex flex-col gap-3 p-4 h-full overflow-y-auto">
      <GlassPanel small className="p-2">
        <Waveform height={35} />
      </GlassPanel>

      {/* Main reward trace */}
      <GlassPanel className="p-4" glow="reward">
        <div className="flex items-center justify-between mb-2">
          <h2 className="text-sm font-medium" style={{ color: colors.reward }}>Reward Signal</h2>
          <span className="font-data text-lg" style={{ color: curVal > 0 ? colors.c3 : colors.danger }}>
            {curVal > 0 ? '+' : ''}{curVal.toFixed(4)}
          </span>
        </div>
        <SignalTrace
          data={rewardData!}
          nFeatures={1}
          nFrames={r3Frames}
          signals={[{ name: 'reward', color: colors.reward, featureIndex: 0 }]}
          height={140}
          yRange={[-0.3, 0.5]}
        />
      </GlassPanel>

      {/* Energy overlay */}
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

      {/* Stats grid */}
      {stats && (
        <div className="grid grid-cols-4 gap-3">
          {[
            { label: 'Mean', value: `${stats.mean > 0 ? '+' : ''}${stats.mean.toFixed(4)}`, color: stats.mean > 0 ? colors.c3 : colors.danger },
            { label: 'Std', value: stats.std.toFixed(4), color: 'var(--text-primary)' },
            { label: 'Positive', value: `${stats.positivePct.toFixed(1)}%`, color: colors.reward },
            { label: 'Peak', value: `+${stats.max.toFixed(3)} @ ${stats.peakTime.toFixed(1)}s`, color: colors.c3 },
            { label: 'Min', value: `${stats.min.toFixed(3)} @ ${stats.troughTime.toFixed(1)}s`, color: colors.danger },
            { label: 'Range', value: (stats.max - stats.min).toFixed(4), color: 'var(--text-primary)' },
            { label: 'Frames', value: stats.n.toString(), color: 'var(--text-secondary)' },
            { label: 'Duration', value: `${(stats.n / FRAME_RATE).toFixed(1)}s`, color: 'var(--text-secondary)' },
          ].map(({ label, value, color }) => (
            <GlassPanel key={label} small className="p-3">
              <div className="text-xs" style={{ color: 'var(--text-muted)' }}>{label}</div>
              <div className="font-data text-sm mt-0.5" style={{ color }}>{value}</div>
            </GlassPanel>
          ))}
        </div>
      )}

      <GlassPanel small className="p-3">
        <div className="text-xs" style={{ color: 'var(--text-muted)' }}>
          R = salience \u00D7 (1.5\u00D7surprise + 0.8\u00D7resolution + 0.5\u00D7exploration - 0.6\u00D7monotony) \u00D7 fam_mod \u00D7 da_gain
        </div>
      </GlassPanel>
    </div>
  );
}
