import { useNavigationStore } from '../../stores/navigationStore';
import { usePipelineStore } from '../../stores/pipelineStore';
import { useAudioStore } from '../../stores/audioStore';
import { colors, R3_GROUPS, R3_GROUP_COLORS, RELAY_INFO, RAM_REGIONS, NEURO_CHANNELS } from '../../design/tokens';

interface NavItem {
  label: string;
  sublabel?: string;
  color: string;
  onClick: () => void;
  active?: boolean;
  dim?: string;
}

export default function ContextSidebar() {
  const { depthPath, navigateIn, currentDepth } = useNavigationStore();
  const { r3Features, r3Frames, rewardData, currentExperimentId } = usePipelineStore();
  const { currentFrame } = useAudioStore();
  const current = depthPath[depthPath.length - 1];
  const hasData = r3Features !== null;

  let items: NavItem[] = [];

  if (currentDepth === 0) {
    // Root: show layer clusters
    items = [
      {
        label: 'R\u00B3 Perception',
        sublabel: '97D \u00B7 9 groups',
        color: colors.r3,
        onClick: () => navigateIn({ type: 'r3' }),
        dim: '97D',
      },
      {
        label: 'H\u00B3 Temporal',
        sublabel: '32 horizons',
        color: colors.h3,
        onClick: () => navigateIn({ type: 'h3' }),
        dim: '131 tuples',
      },
      {
        label: 'C\u00B3 Cognition',
        sublabel: '9 relays \u00B7 131 beliefs',
        color: colors.c3,
        onClick: () => navigateIn({ type: 'c3' }),
        dim: '131',
      },
      {
        label: 'Output',
        sublabel: 'Reward \u00B7 Neuro \u00B7 RAM',
        color: colors.reward,
        onClick: () => navigateIn({ type: 'output' }),
      },
    ];
  } else if (current.type === 'r3') {
    // R3: show 9 groups
    items = R3_GROUPS.map((g) => {
      let energy = 0;
      if (hasData && currentFrame < r3Frames) {
        const [start, end] = g.range;
        for (let i = start; i < end; i++) {
          energy += r3Features![currentFrame * 97 + i];
        }
        energy /= (end - start);
      }
      return {
        label: `${g.key} ${g.name}`,
        sublabel: g.detail,
        color: R3_GROUP_COLORS[g.key],
        dim: `${g.range[1] - g.range[0]}D`,
        onClick: () => navigateIn({ type: 'r3group', key: g.key, name: g.name }),
      };
    });
  } else if (current.type === 'c3') {
    // C3: show relays + beliefs + RAM + neuro
    items = [
      ...RELAY_INFO.map((r) => ({
        label: r.name,
        sublabel: `${r.unit} \u00B7 ${r.detail}`,
        color: r.color,
        dim: `${r.dim}D`,
        onClick: () => navigateIn({ type: 'relay', name: r.name }),
      })),
      {
        label: 'Beliefs',
        sublabel: '36 Core + 65 Appraisal + 30 Anticipation',
        color: colors.c3,
        dim: '131',
        onClick: () => navigateIn({ type: 'beliefs' }),
      },
      {
        label: 'RAM',
        sublabel: '26 brain regions',
        color: colors.c3,
        dim: '26D',
        onClick: () => navigateIn({ type: 'ram' }),
      },
    ];
  } else if (current.type === 'output') {
    items = [
      {
        label: 'Reward',
        sublabel: rewardData ? `mean ${(rewardData.reduce((a, b) => a + b, 0) / rewardData.length).toFixed(3)}` : 'Not loaded',
        color: colors.reward,
        onClick: () => navigateIn({ type: 'reward' }),
      },
      {
        label: 'Neuro',
        sublabel: 'DA \u00B7 NE \u00B7 OPI \u00B7 5HT',
        color: '#ef4444',
        dim: '4D',
        onClick: () => navigateIn({ type: 'neuro' }),
      },
      {
        label: 'RAM',
        sublabel: '26 brain regions',
        color: colors.c3,
        dim: '26D',
        onClick: () => navigateIn({ type: 'ram' }),
      },
    ];
  }

  return (
    <aside
      className="flex flex-col gap-0.5 p-2 overflow-y-auto"
      style={{
        width: 200,
        minHeight: '100%',
        background: 'rgba(255,255,255,0.02)',
        borderRight: '1px solid rgba(255,255,255,0.04)',
      }}
    >
      {/* Logo */}
      <div className="px-3 py-3 mb-1">
        <h1
          className="text-base font-semibold tracking-tight cursor-pointer"
          style={{ color: 'var(--text-primary)' }}
          onClick={() => useNavigationStore.getState().navigateToRoot()}
        >
          MI-Lab
        </h1>
        <p className="text-xs mt-0.5" style={{ color: 'var(--text-muted)' }}>
          Neural Depth Navigator
        </p>
      </div>

      {/* Navigation items */}
      <nav className="flex flex-col gap-0.5">
        {items.map((item) => (
          <button
            key={item.label}
            onClick={item.onClick}
            className="flex flex-col gap-0.5 px-3 py-2 rounded-xl text-left transition-all duration-150 hover:bg-white/5 group"
            style={{
              background: item.active ? 'rgba(255,255,255,0.06)' : 'transparent',
            }}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span
                  className="w-1.5 h-1.5 rounded-full"
                  style={{ background: item.color }}
                />
                <span className="text-xs font-medium" style={{ color: item.color }}>
                  {item.label}
                </span>
              </div>
              {item.dim && (
                <span className="font-data text-[10px]" style={{ color: 'var(--text-muted)' }}>
                  {item.dim}
                </span>
              )}
            </div>
            {item.sublabel && (
              <span
                className="text-[10px] pl-3.5 truncate opacity-0 group-hover:opacity-100 transition-opacity"
                style={{ color: 'var(--text-muted)' }}
              >
                {item.sublabel}
              </span>
            )}
          </button>
        ))}
      </nav>

      {/* Bottom */}
      <div className="mt-auto px-3 py-3">
        {currentExperimentId && (
          <div className="text-[10px] font-data truncate mb-1" style={{ color: 'var(--text-muted)' }}>
            {currentExperimentId}
          </div>
        )}
        <div className="text-[10px] font-data" style={{ color: 'var(--text-muted)' }}>
          v0.2.0 \u00B7 Kernel v4.0
        </div>
      </div>
    </aside>
  );
}
