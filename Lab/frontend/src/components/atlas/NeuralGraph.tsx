/**
 * NeuralGraph — organic neural-network visualization of the entire MI system.
 *
 * Renders R³→H³→C³→Dimensions as interconnected neurons with
 * animated flow edges, breathing halos, and pulsing nodes.
 */
import { useMemo } from 'react'
import { R3_GROUPS } from '../../data/r3'
import { FUNCTIONS } from '../../data/functions'
import { BELIEFS } from '../../data/beliefs'
import { RELAYS } from '../../data/relays'
import { ALL_DIMS, LAYER_COLORS, NEURO_DOMAINS } from '../../data/dimensions'
import type { AtlasNode } from './types'

// ═══════════════════════════════════════════════════════════════
// Types
// ═══════════════════════════════════════════════════════════════

interface GraphNode {
  id: string
  x: number
  y: number
  r: number
  color: string
  opacity: number
  pulseDelay: number
  tooltip: AtlasNode
}

interface GraphEdge {
  id: string
  x1: number; y1: number
  x2: number; y2: number
  color: string
  width: number
  opacity: number
  animated: boolean
  /** Source belief index — for highlight matching */
  beliefIdx?: number
  /** Target dimension key — for highlight matching */
  dimKey?: string
}

interface Props {
  onHover: (node: AtlasNode | null, e: React.MouseEvent) => void
  onClick: (nodeId: string | null) => void
  selected: string | null
  highlightBeliefs?: Set<number>
  visibleLayers: { r3: boolean; h3: boolean; c3: boolean; dims: boolean }
}

// ═══════════════════════════════════════════════════════════════
// Layout Constants
// ═══════════════════════════════════════════════════════════════

export const CANVAS_W = 2100
export const CANVAS_H = 1100

const TYPE_COLORS = { core: '#34d399', appraisal: '#60a5fa', anticipation: '#fbbf24' }

/** Function cluster center positions — organic, not grid-aligned */
const FN_POS: Record<string, { x: number; y: number }> = {
  f1: { x: 660, y: 170 }, f2: { x: 920, y: 145 }, f3: { x: 1180, y: 175 },
  f4: { x: 640, y: 470 }, f5: { x: 900, y: 450 }, f6: { x: 1160, y: 480 },
  f7: { x: 670, y: 770 }, f8: { x: 930, y: 790 }, f9: { x: 1180, y: 760 },
}

// ═══════════════════════════════════════════════════════════════
// Layout Computation
// ═══════════════════════════════════════════════════════════════

function layoutR3(): GraphNode[] {
  return R3_GROUPS.map((g, i) => ({
    id: `r3-${g.id}`,
    x: 100,
    y: 80 + i * 112,
    r: 12 + g.dim * 0.7,
    color: g.color,
    opacity: 0.8,
    pulseDelay: i * 0.4,
    tooltip: {
      id: `r3-${g.id}`, type: 'r3-group', label: `${g.id} — ${g.name}`,
      color: g.color,
      description: `${g.domain} domain · ${g.dim}D [${g.start}:${g.end}]`,
      features: g.features, dimRange: [g.start, g.end],
    },
  }))
}

function layoutH3(): GraphNode[] {
  const scales = ['Micro', 'Meso', 'Macro', 'Ultra']
  const colors = ['#a78bfa', '#818cf8', '#6366f1', '#4f46e5']
  return scales.map((s, i) => ({
    id: `h3-${s.toLowerCase()}`,
    x: 320,
    y: 200 + i * 200,
    r: 20,
    color: colors[i],
    opacity: 0.75,
    pulseDelay: i * 0.6 + 1,
    tooltip: {
      id: `h3-${s.toLowerCase()}`, type: 'h3-scale', label: `${s} Scale`,
      color: colors[i],
      description: `Horizons H${i * 8}–H${i * 8 + 7} · 8 horizons × 24 morphs × 3 laws`,
    },
  }))
}

function layoutC3(): { fnNodes: GraphNode[]; beliefNodes: GraphNode[]; relayNodes: GraphNode[] } {
  const fnNodes: GraphNode[] = []
  const beliefNodes: GraphNode[] = []
  const relayNodes: GraphNode[] = []

  const beliefsByFn = new Map<string, typeof BELIEFS>()
  for (const f of FUNCTIONS) beliefsByFn.set(f.id, [])
  for (const b of BELIEFS) beliefsByFn.get(b.functionId)?.push(b)

  for (const fn of FUNCTIONS) {
    const pos = FN_POS[fn.id]
    if (!pos) continue

    // Function center node
    fnNodes.push({
      id: `fn-${fn.id}`,
      x: pos.x, y: pos.y,
      r: 28,
      color: fn.color,
      opacity: 0.9,
      pulseDelay: fn.index * 0.3 + 2,
      tooltip: {
        id: `fn-${fn.id}`, type: 'function',
        label: `F${fn.index} — ${fn.name}`, color: fn.color,
        description: fn.description, functionId: fn.id,
      },
    })

    // Relay node (if exists)
    const relay = RELAYS.find(r => r.functionId === fn.id)
    if (relay) {
      relayNodes.push({
        id: `relay-${relay.name}`,
        x: pos.x, y: pos.y - 38,
        r: 7,
        color: fn.color,
        opacity: 0.7,
        pulseDelay: fn.index * 0.3 + 2.5,
        tooltip: {
          id: `relay-${relay.name}`, type: 'relay',
          label: relay.name, color: fn.color,
          description: `${relay.fullName} · ${relay.outputDim}D`,
          functionId: fn.id,
        },
      })
    }

    // Belief nodes arranged in circle
    const beliefs = beliefsByFn.get(fn.id) ?? []
    const radius = 58 + beliefs.length * 1.2
    beliefs.forEach((b, i) => {
      const angle = (2 * Math.PI * i) / beliefs.length - Math.PI / 2
      beliefNodes.push({
        id: `b-${b.index}`,
        x: pos.x + radius * Math.cos(angle),
        y: pos.y + radius * Math.sin(angle),
        r: b.type === 'core' ? 5 : 4,
        color: TYPE_COLORS[b.type],
        opacity: 0.7,
        pulseDelay: b.index * 0.08,
        tooltip: {
          id: `b-${b.index}`, type: 'belief',
          label: b.name.replace(/_/g, ' '), color: TYPE_COLORS[b.type],
          description: `${b.type} belief · F${fn.index} ${fn.name}`,
          functionId: fn.id, beliefIndex: b.index,
        },
      })
    })
  }

  return { fnNodes, beliefNodes, relayNodes }
}

function layoutDims(): GraphNode[] {
  const nodes: GraphNode[] = []
  const baseX = 1600

  // Psychology — 2 rows × 3
  ALL_DIMS.filter(d => d.layer === 'psychology').forEach((d, i) => {
    nodes.push({
      id: `dim-psychology-${d.index}`,
      x: baseX + (i % 3) * 56,
      y: 140 + Math.floor(i / 3) * 56,
      r: 16,
      color: LAYER_COLORS.psychology,
      opacity: 0.85,
      pulseDelay: i * 0.3 + 5,
      tooltip: {
        id: `dim-psychology-${d.index}`, type: 'dim-psychology',
        label: d.name, color: LAYER_COLORS.psychology,
        description: d.description, beliefIndices: d.beliefIndices,
      },
    })
  })

  // Cognition — 3 rows × 4
  ALL_DIMS.filter(d => d.layer === 'cognition').forEach((d, i) => {
    nodes.push({
      id: `dim-cognition-${d.index}`,
      x: baseX - 14 + (i % 4) * 50,
      y: 340 + Math.floor(i / 4) * 50,
      r: 13,
      color: LAYER_COLORS.cognition,
      opacity: 0.8,
      pulseDelay: i * 0.2 + 6,
      tooltip: {
        id: `dim-cognition-${d.index}`, type: 'dim-cognition',
        label: d.name, color: LAYER_COLORS.cognition,
        description: d.description, beliefIndices: d.beliefIndices,
      },
    })
  })

  // Neuroscience — 6 domains × 4 params
  NEURO_DOMAINS.forEach((domain, di) => {
    domain.indices.forEach((idx, pi) => {
      const d = ALL_DIMS.find(dd => dd.layer === 'neuroscience' && dd.index === idx)!
      nodes.push({
        id: `dim-neuroscience-${d.index}`,
        x: baseX - 10 + pi * 50,
        y: 600 + di * 60,
        r: 11,
        color: LAYER_COLORS.neuroscience,
        opacity: 0.75,
        pulseDelay: (di * 4 + pi) * 0.15 + 7,
        tooltip: {
          id: `dim-neuroscience-${d.index}`, type: 'dim-neuroscience',
          label: d.name, color: LAYER_COLORS.neuroscience,
          description: `${domain.name} · ${d.description}`,
          beliefIndices: d.beliefIndices,
        },
      })
    })
  })

  return nodes
}

/** Compute edges between beliefs and dimensions */
function computeBeliefDimEdges(
  beliefNodes: GraphNode[], dimNodes: GraphNode[],
): GraphEdge[] {
  const bMap = new Map(beliefNodes.map(n => [parseInt(n.id.split('-')[1]), n]))
  const dMap = new Map(dimNodes.map(n => [n.id, n]))
  const edges: GraphEdge[] = []

  for (const dim of ALL_DIMS) {
    const dNode = dMap.get(`dim-${dim.layer}-${dim.index}`)
    if (!dNode) continue
    for (const bi of dim.beliefIndices) {
      const bNode = bMap.get(bi)
      if (!bNode) continue
      edges.push({
        id: `bd-${bi}-${dim.layer}-${dim.index}`,
        x1: bNode.x, y1: bNode.y, x2: dNode.x, y2: dNode.y,
        color: dNode.color, width: 0.6, opacity: 0.04,
        animated: false, beliefIdx: bi, dimKey: `dim-${dim.layer}-${dim.index}`,
      })
    }
  }
  return edges
}

/** Bezier curve between two points with horizontal bias */
function edgePath(x1: number, y1: number, x2: number, y2: number): string {
  const dx = Math.abs(x2 - x1) * 0.4
  return `M${x1},${y1} C${x1 + dx},${y1} ${x2 - dx},${y2} ${x2},${y2}`
}

// ═══════════════════════════════════════════════════════════════
// Component
// ═══════════════════════════════════════════════════════════════

export function NeuralGraph({ onHover, onClick, selected, highlightBeliefs, visibleLayers }: Props) {
  const r3Nodes = useMemo(() => layoutR3(), [])
  const h3Nodes = useMemo(() => layoutH3(), [])
  const { fnNodes, beliefNodes, relayNodes } = useMemo(() => layoutC3(), [])
  const dimNodes = useMemo(() => layoutDims(), [])

  // Belief → Dimension edges
  const bdEdges = useMemo(
    () => computeBeliefDimEdges(beliefNodes, dimNodes),
    [beliefNodes, dimNodes],
  )

  // All nodes in a map for fast lookup
  const nodeMap = useMemo(() => {
    const m = new Map<string, GraphNode>()
    for (const n of [...r3Nodes, ...h3Nodes, ...fnNodes, ...beliefNodes, ...relayNodes, ...dimNodes])
      m.set(n.id, n)
    return m
  }, [r3Nodes, h3Nodes, fnNodes, beliefNodes, relayNodes, dimNodes])

  // Determine which edges to highlight
  const activeEdges = useMemo(() => {
    if (!selected) return new Set<string>()
    const set = new Set<string>()
    for (const e of bdEdges) {
      if (selected === `b-${e.beliefIdx}` || selected === e.dimKey) {
        set.add(e.id)
      }
    }
    return set
  }, [selected, bdEdges])

  function renderNode(n: GraphNode, visible: boolean) {
    if (!visible) return null
    const isSelected = selected === n.id
    const isHighlighted = n.tooltip.beliefIndex != null && highlightBeliefs?.has(n.tooltip.beliefIndex)
    const dim = highlightBeliefs && !isHighlighted && n.tooltip.type === 'belief'

    return (
      <g
        key={n.id}
        style={{ cursor: 'pointer' }}
        onMouseEnter={e => onHover(n.tooltip, e)}
        onMouseLeave={() => onHover(null, null!)}
        onClick={e => { e.stopPropagation(); onClick(n.id) }}
      >
        {/* Halo / glow */}
        <circle
          cx={n.x} cy={n.y} r={n.r * 2.5}
          fill={n.color} opacity={isSelected ? 0.15 : isHighlighted ? 0.1 : 0}
          style={{ transition: 'opacity 0.3s' }}
        />
        {/* Node body */}
        <circle
          cx={n.x} cy={n.y}
          r={isSelected ? n.r + 2 : isHighlighted ? n.r + 1 : n.r}
          fill={dim ? `${n.color}30` : n.color}
          opacity={dim ? 0.3 : n.opacity}
          stroke={isSelected ? 'white' : 'transparent'}
          strokeWidth={isSelected ? 1.5 : 0}
          style={{
            animation: `atlas-pulse ${2.5 + (n.pulseDelay % 2)}s ease-in-out infinite`,
            animationDelay: `${n.pulseDelay}s`,
            transition: 'r 0.2s, opacity 0.2s',
          }}
        />
      </g>
    )
  }

  return (
    <g>
      {/* ── Background: Central brain glow ── */}
      <circle cx={900} cy={480} r={85} fill="#6366f1" opacity={0.04}
        style={{ animation: 'atlas-halo 5s ease-in-out infinite' }} />
      <circle cx={900} cy={480} r={350} fill="url(#brain-radial)" opacity={0.06}
        style={{ animation: 'atlas-halo 7s ease-in-out infinite', animationDelay: '1s' }} />

      <defs>
        <radialGradient id="brain-radial">
          <stop offset="0%" stopColor="#818cf8" stopOpacity="1" />
          <stop offset="100%" stopColor="#818cf8" stopOpacity="0" />
        </radialGradient>
      </defs>

      {/* ── Layer flow edges (thick, animated) ── */}
      {visibleLayers.r3 && visibleLayers.h3 && (
        <path
          d={edgePath(140, 530, 300, 500)}
          fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth={3}
          strokeDasharray="5 18"
          style={{ animation: 'atlas-flow 3s linear infinite' }}
        />
      )}
      {visibleLayers.h3 && visibleLayers.c3 && (
        <path
          d={edgePath(340, 500, 540, 460)}
          fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth={3}
          strokeDasharray="5 18"
          style={{ animation: 'atlas-flow 3s linear infinite', animationDelay: '0.5s' }}
        />
      )}
      {visibleLayers.c3 && visibleLayers.dims && (
        <path
          d={edgePath(1330, 480, 1560, 500)}
          fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth={3}
          strokeDasharray="5 18"
          style={{ animation: 'atlas-flow 3s linear infinite', animationDelay: '1s' }}
        />
      )}

      {/* ── R³ → H³ individual edges ── */}
      {visibleLayers.r3 && visibleLayers.h3 && r3Nodes.map(rn =>
        h3Nodes.map(hn => (
          <path
            key={`${rn.id}-${hn.id}`}
            d={edgePath(rn.x + rn.r, rn.y, hn.x - hn.r, hn.y)}
            fill="none" stroke={rn.color} strokeWidth={0.4} opacity={0.06}
            strokeDasharray="2 10"
            style={{ animation: 'atlas-flow 4s linear infinite', animationDelay: `${rn.tooltip.pulseDelay || 0}s` }}
          />
        ))
      )}

      {/* ── H³ → Function edges ── */}
      {visibleLayers.h3 && visibleLayers.c3 && h3Nodes.map(hn =>
        fnNodes.map(fn => (
          <path
            key={`${hn.id}-${fn.id}`}
            d={edgePath(hn.x + hn.r, hn.y, fn.x - fn.r - 60, fn.y)}
            fill="none" stroke={fn.color} strokeWidth={0.3} opacity={0.05}
            strokeDasharray="2 14"
            style={{ animation: 'atlas-flow 5s linear infinite' }}
          />
        ))
      )}

      {/* ── Belief → Dimension edges ── */}
      {visibleLayers.c3 && visibleLayers.dims && bdEdges.map(e => {
        const active = activeEdges.has(e.id)
        return (
          <path
            key={e.id}
            d={edgePath(e.x1, e.y1, e.x2, e.y2)}
            fill="none"
            stroke={e.color}
            strokeWidth={active ? 1.2 : e.width}
            opacity={active ? 0.35 : e.opacity}
            strokeDasharray={active ? '3 8' : undefined}
            style={active ? { animation: 'atlas-flow 2s linear infinite' } : { transition: 'opacity 0.3s' }}
          />
        )
      })}

      {/* ── Function auras (breathing halos) ── */}
      {visibleLayers.c3 && fnNodes.map(fn => (
        <circle
          key={`aura-${fn.id}`}
          cx={fn.x} cy={fn.y} r={85}
          fill={fn.color} opacity={0.03}
          style={{
            animation: 'atlas-halo 4s ease-in-out infinite',
            animationDelay: `${fn.pulseDelay * 0.5}s`,
          }}
        />
      ))}

      {/* ── Function labels ── */}
      {visibleLayers.c3 && fnNodes.map(fn => {
        const f = FUNCTIONS.find(f => f.id === fn.tooltip.functionId)
        return (
          <text
            key={`label-${fn.id}`}
            x={fn.x} y={fn.y + 4}
            textAnchor="middle" fill="white" fontSize={11} fontWeight={700}
            fontFamily="var(--font-mono)" opacity={0.85}
            style={{ pointerEvents: 'none' }}
          >
            F{f?.index}
          </text>
        )
      })}

      {/* ── Dimension tier labels ── */}
      {visibleLayers.dims && (
        <>
          <text x={1630} y={110} textAnchor="middle" fill={LAYER_COLORS.psychology}
            fontSize={10} fontWeight={600} opacity={0.6} letterSpacing="0.05em">
            PSYCHOLOGY · 6D
          </text>
          <text x={1630} y={310} textAnchor="middle" fill={LAYER_COLORS.cognition}
            fontSize={10} fontWeight={600} opacity={0.6} letterSpacing="0.05em">
            COGNITION · 12D
          </text>
          <text x={1630} y={575} textAnchor="middle" fill={LAYER_COLORS.neuroscience}
            fontSize={10} fontWeight={600} opacity={0.6} letterSpacing="0.05em">
            NEUROSCIENCE · 24D
          </text>
        </>
      )}

      {/* ── Dimension domain labels ── */}
      {visibleLayers.dims && NEURO_DOMAINS.map((domain, di) => (
        <text
          key={domain.key}
          x={1560} y={618 + di * 60}
          fill="rgba(255,255,255,0.15)" fontSize={7}
          fontFamily="var(--font-mono)" textAnchor="end"
        >
          {domain.name}
        </text>
      ))}

      {/* ── R³ layer label ── */}
      {visibleLayers.r3 && (
        <>
          <text x={100} y={50} textAnchor="middle" fill="rgba(255,255,255,0.35)"
            fontSize={12} fontWeight={600} letterSpacing="0.06em">R³ · 97D</text>
          <text x={100} y={65} textAnchor="middle" fill="rgba(255,255,255,0.15)"
            fontSize={8}>PERCEPTUAL</text>
        </>
      )}

      {/* ── H³ layer label ── */}
      {visibleLayers.h3 && (
        <>
          <text x={320} y={165} textAnchor="middle" fill="rgba(255,255,255,0.35)"
            fontSize={12} fontWeight={600} letterSpacing="0.06em">H³</text>
          <text x={320} y={180} textAnchor="middle" fill="rgba(255,255,255,0.15)"
            fontSize={8}>TEMPORAL</text>
        </>
      )}

      {/* ── Render all nodes ── */}
      {r3Nodes.map(n => renderNode(n, visibleLayers.r3))}
      {h3Nodes.map(n => renderNode(n, visibleLayers.h3))}
      {beliefNodes.map(n => renderNode(n, visibleLayers.c3))}
      {relayNodes.map(n => renderNode(n, visibleLayers.c3))}
      {fnNodes.map(n => renderNode(n, visibleLayers.c3))}
      {dimNodes.map(n => renderNode(n, visibleLayers.dims))}

      {/* ── Dimension name labels (small) ── */}
      {visibleLayers.dims && dimNodes.map(n => (
        <text
          key={`dl-${n.id}`}
          x={n.x} y={n.y + n.r + 12}
          textAnchor="middle" fill="rgba(255,255,255,0.35)"
          fontSize={7} fontWeight={500}
          style={{ pointerEvents: 'none' }}
        >
          {n.tooltip.label}
        </text>
      ))}
    </g>
  )
}
