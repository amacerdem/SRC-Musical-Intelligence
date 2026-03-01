import { R3_GROUPS } from '../../../data/r3'
import type { AtlasNode } from '../types'

interface Props {
  x: number
  y: number
  onHover: (node: AtlasNode | null, e: React.MouseEvent) => void
  selected: string | null
  dimmed: boolean
}

const GROUP_H = 48
const GROUP_W = 140
const GAP = 8

export function R3Layer({ x, y, onHover, selected, dimmed }: Props) {
  const totalH = R3_GROUPS.length * (GROUP_H + GAP) - GAP

  return (
    <g opacity={dimmed ? 0.15 : 1} style={{ transition: 'opacity 0.3s' }}>
      {/* Layer label */}
      <text
        x={x + GROUP_W / 2} y={y - 24}
        textAnchor="middle" fill="rgba(255,255,255,0.4)"
        fontSize={13} fontWeight={600} letterSpacing="0.06em"
      >
        R³ — 97D
      </text>
      <text
        x={x + GROUP_W / 2} y={y - 8}
        textAnchor="middle" fill="rgba(255,255,255,0.2)"
        fontSize={9} letterSpacing="0.04em"
      >
        PERCEPTUAL FRONT-END
      </text>

      {/* Border box */}
      <rect
        x={x - 12} y={y - 12}
        width={GROUP_W + 24} height={totalH + 24}
        rx={14} fill="none"
        stroke="rgba(255,255,255,0.06)" strokeWidth={1}
        strokeDasharray="4 4"
      />

      {R3_GROUPS.map((g, i) => {
        const gy = y + i * (GROUP_H + GAP)
        const isSelected = selected === `r3-${g.id}`
        const nodeData: AtlasNode = {
          id: `r3-${g.id}`,
          type: 'r3-group',
          label: `${g.id} — ${g.name}`,
          color: g.color,
          description: `${g.domain} domain, ${g.dim}D [${g.start}:${g.end}]`,
          features: g.features,
          dimRange: [g.start, g.end],
        }

        return (
          <g
            key={g.id}
            onMouseEnter={e => onHover(nodeData, e)}
            onMouseLeave={() => onHover(null, null!)}
            style={{ cursor: 'pointer' }}
          >
            <rect
              x={x} y={gy}
              width={GROUP_W} height={GROUP_H}
              rx={8}
              fill={isSelected ? `${g.color}25` : `${g.color}10`}
              stroke={isSelected ? g.color : `${g.color}40`}
              strokeWidth={isSelected ? 1.5 : 0.8}
              style={{ transition: 'all 0.2s' }}
            />
            {/* Group letter */}
            <text
              x={x + 12} y={gy + 20}
              fill={g.color} fontSize={14} fontWeight={700}
              fontFamily="var(--font-mono)"
            >
              {g.id}
            </text>
            {/* Group name */}
            <text
              x={x + 32} y={gy + 20}
              fill="rgba(255,255,255,0.75)" fontSize={11} fontWeight={500}
            >
              {g.name}
            </text>
            {/* Dim count */}
            <text
              x={x + GROUP_W - 10} y={gy + 20}
              textAnchor="end"
              fill="rgba(255,255,255,0.3)" fontSize={10}
              fontFamily="var(--font-mono)"
            >
              {g.dim}D
            </text>
            {/* Stage indicator */}
            <text
              x={x + 12} y={gy + 38}
              fill="rgba(255,255,255,0.2)" fontSize={9}
              fontFamily="var(--font-mono)"
            >
              [{g.start}:{g.end}] · {g.domain}
            </text>
          </g>
        )
      })}

      {/* Output port */}
      <circle
        cx={x + GROUP_W + 12} cy={y + totalH / 2}
        r={4} fill="rgba(255,255,255,0.15)" stroke="rgba(255,255,255,0.3)" strokeWidth={0.8}
      />
    </g>
  )
}

export const R3_LAYER_WIDTH = GROUP_W + 24
export const R3_LAYER_HEIGHT = R3_GROUPS.length * (GROUP_H + GAP) - GAP
export const R3_OUT_X = GROUP_W + 12
export const R3_OUT_Y = R3_LAYER_HEIGHT / 2
