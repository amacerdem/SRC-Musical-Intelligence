import type { AtlasNode } from '../types'

interface Props {
  x: number
  y: number
  onHover: (node: AtlasNode | null, e: React.MouseEvent) => void
  selected: string | null
  dimmed: boolean
}

const SCALES = [
  { key: 'micro', label: 'Micro', range: 'H0–H7', color: '#a78bfa' },
  { key: 'meso', label: 'Meso', range: 'H8–H15', color: '#818cf8' },
  { key: 'macro', label: 'Macro', range: 'H16–H23', color: '#6366f1' },
  { key: 'ultra', label: 'Ultra', range: 'H24–H31', color: '#4f46e5' },
]

const SCALE_W = 120
const SCALE_H = 44
const GAP = 10

export function H3Layer({ x, y, onHover, selected, dimmed }: Props) {
  const totalH = SCALES.length * (SCALE_H + GAP) - GAP + 80

  return (
    <g opacity={dimmed ? 0.15 : 1} style={{ transition: 'opacity 0.3s' }}>
      {/* Layer label */}
      <text
        x={x + SCALE_W / 2} y={y - 24}
        textAnchor="middle" fill="rgba(255,255,255,0.4)"
        fontSize={13} fontWeight={600} letterSpacing="0.06em"
      >
        H³
      </text>
      <text
        x={x + SCALE_W / 2} y={y - 8}
        textAnchor="middle" fill="rgba(255,255,255,0.2)"
        fontSize={9} letterSpacing="0.04em"
      >
        TEMPORAL MORPHOLOGY
      </text>

      {/* Border box */}
      <rect
        x={x - 12} y={y - 12}
        width={SCALE_W + 24} height={totalH + 24}
        rx={14} fill="none"
        stroke="rgba(255,255,255,0.06)" strokeWidth={1}
        strokeDasharray="4 4"
      />

      {SCALES.map((s, i) => {
        const sy = y + i * (SCALE_H + GAP)
        const isSelected = selected === `h3-${s.key}`
        const nodeData: AtlasNode = {
          id: `h3-${s.key}`,
          type: 'h3-scale',
          label: `${s.label} Scale`,
          color: s.color,
          description: `Horizons ${s.range} — 8 horizons × 24 morphs × 3 laws = 576 tuples per R³ dim`,
        }

        return (
          <g
            key={s.key}
            onMouseEnter={e => onHover(nodeData, e)}
            onMouseLeave={() => onHover(null, null!)}
            style={{ cursor: 'pointer' }}
          >
            <rect
              x={x} y={sy}
              width={SCALE_W} height={SCALE_H}
              rx={8}
              fill={isSelected ? `${s.color}25` : `${s.color}08`}
              stroke={isSelected ? s.color : `${s.color}30`}
              strokeWidth={isSelected ? 1.5 : 0.8}
              style={{ transition: 'all 0.2s' }}
            />
            <text
              x={x + 12} y={sy + 18}
              fill={s.color} fontSize={12} fontWeight={600}
            >
              {s.label}
            </text>
            <text
              x={x + 12} y={sy + 34}
              fill="rgba(255,255,255,0.25)" fontSize={9}
              fontFamily="var(--font-mono)"
            >
              {s.range}
            </text>
          </g>
        )
      })}

      {/* Summary stats */}
      <text
        x={x + SCALE_W / 2} y={y + SCALES.length * (SCALE_H + GAP) + 12}
        textAnchor="middle" fill="rgba(255,255,255,0.2)"
        fontSize={9} fontFamily="var(--font-mono)"
      >
        32 × 24 × 3
      </text>
      <text
        x={x + SCALE_W / 2} y={y + SCALES.length * (SCALE_H + GAP) + 26}
        textAnchor="middle" fill="rgba(255,255,255,0.15)"
        fontSize={9} fontFamily="var(--font-mono)"
      >
        ~8,600 active
      </text>

      {/* Input port */}
      <circle
        cx={x - 12} cy={y + (SCALES.length * (SCALE_H + GAP) - GAP) / 2}
        r={4} fill="rgba(255,255,255,0.15)" stroke="rgba(255,255,255,0.3)" strokeWidth={0.8}
      />
      {/* Output port */}
      <circle
        cx={x + SCALE_W + 12} cy={y + (SCALES.length * (SCALE_H + GAP) - GAP) / 2}
        r={4} fill="rgba(255,255,255,0.15)" stroke="rgba(255,255,255,0.3)" strokeWidth={0.8}
      />
    </g>
  )
}

export const H3_LAYER_WIDTH = SCALE_W + 24
export const H3_LAYER_HEIGHT = SCALES.length * (SCALE_H + GAP) - GAP + 80
