import { useAudioStore } from '../../stores/audioStore';
import { usePipelineStore } from '../../stores/pipelineStore';
import { useNavigationStore } from '../../stores/navigationStore';
import Breadcrumb from './Breadcrumb';
import { colors } from '../../design/tokens';

interface Props {
  onRunPipeline: () => void;
}

export default function TopBar({ onRunPipeline }: Props) {
  const { currentFile, isPlaying } = useAudioStore();
  const { currentExperimentId, rewardData, r3Frames } = usePipelineStore();
  const { currentDepth, navigateOut } = useNavigationStore();

  const rewardMean = rewardData
    ? rewardData.reduce((a, b) => a + b, 0) / rewardData.length
    : null;

  return (
    <header
      className="flex items-center justify-between px-4 py-2"
      style={{
        background: 'rgba(255,255,255,0.02)',
        borderBottom: '1px solid rgba(255,255,255,0.04)',
      }}
    >
      <div className="flex items-center gap-3">
        {currentDepth > 0 && (
          <button
            onClick={navigateOut}
            className="w-7 h-7 rounded-lg flex items-center justify-center text-xs transition-colors hover:bg-white/5"
            style={{ color: 'var(--text-secondary)', border: '1px solid rgba(255,255,255,0.06)' }}
          >
            ←
          </button>
        )}
        <Breadcrumb />
      </div>

      <div className="flex items-center gap-4">
        {currentExperimentId && rewardMean !== null && (
          <div className="flex items-center gap-3">
            <span className="font-data text-xs" style={{ color: colors.reward }}>
              R={rewardMean > 0 ? '+' : ''}{rewardMean.toFixed(3)}
            </span>
            <span className="font-data text-xs" style={{ color: 'var(--text-muted)' }}>
              {r3Frames}f
            </span>
          </div>
        )}

        {currentFile && (
          <span
            className="w-2 h-2 rounded-full"
            style={{ background: isPlaying ? '#10b981' : 'var(--text-muted)' }}
          />
        )}

        <button
          onClick={onRunPipeline}
          className="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors"
          style={{
            background: `${colors.c3}15`,
            color: colors.c3,
            border: `1px solid ${colors.c3}25`,
          }}
        >
          Run Pipeline
        </button>
      </div>
    </header>
  );
}
