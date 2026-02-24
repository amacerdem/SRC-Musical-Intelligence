import { useMemo } from 'react';
import GlassPanel from '../components/layout/GlassPanel';
import SignalTrace from '../components/charts/SignalTrace';
import Waveform from '../components/audio/Waveform';
import { usePipelineStore } from '../stores/pipelineStore';
import { useAudioStore } from '../stores/audioStore';
import { R3_GROUPS, R3_GROUP_COLORS, colors } from '../design/tokens';

interface Props {
  groupKey?: string;
  groupName?: string;
  featureIndex?: number;
  featureName?: string;
}

export default function FeatureDetailView({ groupKey, groupName, featureIndex, featureName }: Props) {
  const { r3Features, r3Names, r3Frames } = usePipelineStore();
  const { currentFrame } = useAudioStore();

  const hasData = r3Features !== null && r3Frames > 0;

  // Determine which features to show
  const features = useMemo(() => {
    if (featureIndex !== undefined) {
      return [{ index: featureIndex, name: featureName || r3Names[featureIndex] || `f${featureIndex}` }];
    }
    if (groupKey) {
      const group = R3_GROUPS.find(g => g.key === groupKey);
      if (group) {
        const [start, end] = group.range;
        return Array.from({ length: end - start }, (_, i) => ({
          index: start + i,
          name: r3Names[start + i] || `f${start + i}`,
        }));
      }
    }
    return [];
  }, [groupKey, featureIndex, featureName, r3Names]);

  const groupColor = groupKey ? R3_GROUP_COLORS[groupKey] || colors.r3 : colors.r3;

  if (!hasData) {
    return (
      <div className="flex items-center justify-center h-full">
        <GlassPanel className="p-8" glow="r3">
          <h2 className="text-lg font-semibold mb-2" style={{ color: groupColor }}>
            {groupName || featureName || 'Feature Detail'}
          </h2>
          <p className="text-sm" style={{ color: 'var(--text-secondary)' }}>No data available.</p>
        </GlassPanel>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-3 p-4 h-full overflow-y-auto">
      <GlassPanel small className="p-2">
        <Waveform height={30} />
      </GlassPanel>

      {/* Header */}
      <div className="flex items-center gap-3 px-1">
        <span className="w-3 h-3 rounded-full" style={{ background: groupColor }} />
        <span className="text-sm font-semibold" style={{ color: groupColor }}>
          {groupKey ? `Group ${groupKey}: ${groupName}` : featureName}
        </span>
        <span className="font-data text-xs" style={{ color: 'var(--text-muted)' }}>
          {features.length} features
        </span>
      </div>

      {/* Individual feature traces */}
      {features.map((feat) => {
        // Extract single-feature data
        const featureData = new Float32Array(r3Frames);
        for (let t = 0; t < r3Frames; t++) {
          featureData[t] = r3Features![t * 97 + feat.index];
        }
        const curVal = currentFrame < r3Frames ? featureData[currentFrame] : 0;

        return (
          <GlassPanel key={feat.index} small className="p-3">
            <div className="flex items-center justify-between mb-1">
              <span className="text-xs font-medium" style={{ color: groupColor }}>
                [{feat.index}] {feat.name}
              </span>
              <span className="font-data text-sm" style={{ color: groupColor }}>
                {curVal.toFixed(4)}
              </span>
            </div>
            <SignalTrace
              data={featureData}
              nFeatures={1}
              nFrames={r3Frames}
              signals={[{ name: feat.name, color: groupColor, featureIndex: 0 }]}
              height={features.length > 4 ? 60 : 100}
            />
          </GlassPanel>
        );
      })}

      {/* Stats footer */}
      <GlassPanel small className="p-3">
        <div className="text-xs" style={{ color: 'var(--text-muted)' }}>
          {r3Frames} frames \u00B7 Range [0, 1] \u00B7 Frozen boundary \u00B7 Frame rate: 172.27 Hz
        </div>
      </GlassPanel>
    </div>
  );
}
