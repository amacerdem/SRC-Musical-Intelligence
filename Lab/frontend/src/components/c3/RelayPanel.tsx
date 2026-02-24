import type { RelayDef } from '../../data/relays'
import { GlassChip } from '../glass/GlassChip'

interface RelayPanelProps {
  relay: RelayDef
  color?: string
}

const LAYER_COLORS: Record<string, string> = {
  E: '#f97316',
  M: '#8b5cf6',
  P: '#3b82f6',
  F: '#22c55e',
  'N+C': '#ec4899',
  'T+M': '#f59e0b',
}

const VIS_LABELS: Record<string, string> = {
  internal: 'int',
  hybrid: 'hyb',
  external: 'ext',
}

export function RelayPanel({ relay, color }: RelayPanelProps) {
  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center gap-3">
        <span className="mono text-lg font-semibold" style={{ color }}>{relay.name}</span>
        <span className="text-sm text-text-secondary">{relay.fullName}</span>
        <GlassChip label={`${relay.outputDim}D`} color={color} size="md" />
        <GlassChip label={relay.unit} />
      </div>

      {/* Dimension table */}
      <div className="glass-card overflow-hidden">
        <table className="w-full text-xs">
          <thead>
            <tr className="border-b border-border-subtle">
              <th className="text-left px-4 py-2 text-text-tertiary font-medium w-8">#</th>
              <th className="text-left px-4 py-2 text-text-tertiary font-medium">Layer</th>
              <th className="text-left px-4 py-2 text-text-tertiary font-medium">Dimension Name</th>
              <th className="text-left px-4 py-2 text-text-tertiary font-medium">Visibility</th>
              <th className="text-right px-4 py-2 text-text-tertiary font-medium w-20">Trace</th>
            </tr>
          </thead>
          <tbody>
            {relay.dims.map((dim, i) => (
              <tr key={i} className="border-b border-border-subtle/50 hover:bg-white/2">
                <td className="px-4 py-1.5 mono text-text-tertiary">{i}</td>
                <td className="px-4 py-1.5">
                  <span
                    className="inline-block w-5 text-center mono font-semibold text-[10px] rounded"
                    style={{
                      color: LAYER_COLORS[dim.layer] ?? '#888',
                      backgroundColor: `${LAYER_COLORS[dim.layer] ?? '#888'}15`,
                    }}
                  >
                    {dim.layer}
                  </span>
                </td>
                <td className="px-4 py-1.5 mono text-text-primary">{dim.name}</td>
                <td className="px-4 py-1.5">
                  <span className={`text-[10px] ${
                    dim.visibility === 'hybrid' ? 'text-blue-400' :
                    dim.visibility === 'external' ? 'text-green-400' :
                    'text-text-tertiary'
                  }`}>
                    {VIS_LABELS[dim.visibility]}
                  </span>
                </td>
                <td className="px-4 py-1.5 text-right">
                  <span className="text-text-tertiary italic text-[10px]">no data</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Layer summary bar */}
      <div className="flex h-4 rounded-md overflow-hidden bg-white/3">
        {(() => {
          const layers: Record<string, number> = {}
          for (const d of relay.dims) {
            layers[d.layer] = (layers[d.layer] ?? 0) + 1
          }
          return Object.entries(layers).map(([layer, count]) => (
            <div
              key={layer}
              className="flex items-center justify-center text-[9px] font-semibold mono text-white/80"
              style={{
                width: `${(count / relay.outputDim) * 100}%`,
                backgroundColor: LAYER_COLORS[layer] ?? '#666',
                opacity: 0.6,
              }}
              title={`${layer} [${count}D]`}
            >
              {layer}[{count}]
            </div>
          ))
        })()}
      </div>
    </div>
  )
}
