import { useNavigationStore, type DepthSegment } from '../../stores/navigationStore';
import { colors } from '../../design/tokens';

function segmentLabel(seg: DepthSegment): { text: string; color: string } {
  switch (seg.type) {
    case 'root': return { text: 'Neural Overview', color: 'var(--text-primary)' };
    case 'r3': return { text: 'R\u00B3 Perception', color: colors.r3 };
    case 'h3': return { text: 'H\u00B3 Temporal', color: colors.h3 };
    case 'c3': return { text: 'C\u00B3 Cognition', color: colors.c3 };
    case 'output': return { text: 'Output', color: colors.reward };
    case 'r3group': return { text: `Group ${seg.key}`, color: colors.r3 };
    case 'h3horizon': return { text: seg.band, color: colors.h3 };
    case 'relay': return { text: seg.name, color: colors.c3 };
    case 'beliefs': return { text: 'Beliefs', color: colors.c3 };
    case 'ram': return { text: 'RAM', color: colors.c3 };
    case 'reward': return { text: 'Reward', color: colors.reward };
    case 'neuro': return { text: 'Neuro', color: colors.danger || '#ef4444' };
    case 'feature': return { text: seg.name, color: colors.r3 };
    default: return { text: '?', color: 'var(--text-muted)' };
  }
}

export default function Breadcrumb() {
  const { depthPath, navigateOut, navigateToRoot } = useNavigationStore();

  if (depthPath.length <= 1) return null;

  return (
    <div className="flex items-center gap-1">
      {depthPath.map((seg, i) => {
        const { text, color } = segmentLabel(seg);
        const isLast = i === depthPath.length - 1;
        const isClickable = !isLast;

        return (
          <span key={i} className="flex items-center gap-1">
            {i > 0 && (
              <span className="text-xs mx-0.5" style={{ color: 'var(--text-muted)' }}>/</span>
            )}
            <button
              onClick={() => {
                if (i === 0) navigateToRoot();
                else if (isClickable) {
                  // Navigate back to this depth
                  const stepsBack = depthPath.length - 1 - i;
                  for (let s = 0; s < stepsBack; s++) navigateOut();
                }
              }}
              className={`text-xs transition-colors ${isClickable ? 'hover:underline cursor-pointer' : 'cursor-default'}`}
              style={{
                color: isLast ? color : 'var(--text-muted)',
                fontWeight: isLast ? 600 : 400,
              }}
            >
              {text}
            </button>
          </span>
        );
      })}
    </div>
  );
}
