import type { AtlasNode } from './types'
import { BELIEFS } from '../../data/beliefs'
import { FUNCTIONS } from '../../data/functions'

interface Props {
  node: AtlasNode | null
  x: number
  y: number
}

export function AtlasTooltip({ node, x, y }: Props) {
  if (!node) return null

  const offsetX = x + 280 > window.innerWidth ? -260 : 16
  const offsetY = y + 200 > window.innerHeight ? -180 : 16

  return (
    <div
      className="fixed z-50 pointer-events-none"
      style={{ left: x + offsetX, top: y + offsetY }}
    >
      <div
        className="glass-3 rounded-xl border border-white/10 p-3 min-w-[220px] max-w-[280px]"
        style={{ boxShadow: `0 0 24px ${node.color}20, 0 8px 32px rgba(0,0,0,0.5)` }}
      >
        {/* Header */}
        <div className="flex items-center gap-2 mb-1.5">
          <div className="w-2.5 h-2.5 rounded-full" style={{ background: node.color }} />
          <span className="text-sm font-semibold text-text-primary">{node.label}</span>
        </div>

        {/* Type badge */}
        <div className="flex items-center gap-1.5 mb-2">
          <span className="glass-badge text-[10px] px-2 py-0.5 rounded-full border"
            style={{
              background: `${node.color}18`,
              color: node.color,
              borderColor: `${node.color}30`,
            }}
          >
            {node.type}
          </span>
          {node.functionId && (
            <span className="text-[10px] text-text-tertiary mono">
              {FUNCTIONS.find(f => f.id === node.functionId)?.name ?? node.functionId}
            </span>
          )}
        </div>

        {/* Description */}
        {node.description && (
          <p className="text-xs text-text-secondary leading-relaxed mb-2">
            {node.description}
          </p>
        )}

        {/* Belief details */}
        {node.type === 'belief' && node.beliefIndex != null && (
          <div className="text-[10px] text-text-tertiary mono space-y-0.5">
            <div>b{node.beliefIndex} &middot; {BELIEFS[node.beliefIndex]?.type ?? '—'}</div>
            <div>{BELIEFS[node.beliefIndex]?.mechanism ?? '—'}</div>
          </div>
        )}

        {/* Dimension belief list */}
        {node.type.startsWith('dim-') && node.beliefIndices && (
          <div className="mt-1 space-y-0.5">
            <div className="text-[10px] text-text-tertiary uppercase tracking-wider">
              Source beliefs ({node.beliefIndices.length})
            </div>
            <div className="flex flex-wrap gap-1 mt-1">
              {node.beliefIndices.map(bi => (
                <span key={bi} className="text-[10px] mono px-1.5 py-0.5 rounded bg-white/5 text-text-secondary">
                  b{bi}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* R³ group features */}
        {node.type === 'r3-group' && node.features && (
          <div className="mt-1 space-y-0.5">
            <div className="text-[10px] text-text-tertiary uppercase tracking-wider">
              {node.features.length} features [{node.dimRange?.[0]}:{node.dimRange?.[1]}]
            </div>
            <div className="text-[10px] mono text-text-secondary leading-relaxed mt-1">
              {node.features.slice(0, 6).join(', ')}
              {node.features.length > 6 && `, +${node.features.length - 6} more`}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
