import type { FunctionDef } from '../../data/functions'
import { GlassBadge } from '../glass/GlassBadge'
import { GlassChip } from '../glass/GlassChip'

interface FunctionHeaderProps {
  fn: FunctionDef
  mechanismCount: number
}

export function FunctionHeader({ fn, mechanismCount }: FunctionHeaderProps) {
  const { beliefCounts: bc } = fn

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-3">
        <span
          className="w-3 h-3 rounded-full shrink-0"
          style={{ backgroundColor: fn.color }}
        />
        <h1
          className="text-2xl font-semibold tracking-tight"
          style={{ color: fn.color }}
        >
          F{fn.index} {fn.name}
        </h1>
        <GlassChip label={fn.unit} color={fn.color} size="md" />
      </div>

      <p className="text-sm text-text-secondary max-w-2xl">{fn.description}</p>

      <div className="flex items-center gap-2 flex-wrap">
        <GlassBadge type="core" count={bc.core} />
        <GlassBadge type="appraisal" count={bc.appraisal} />
        <GlassBadge type="anticipation" count={bc.anticipation} />
        <span className="mx-1 text-border-default">|</span>
        <GlassChip label={`${mechanismCount} mechanisms`} />
        {fn.relay && <GlassChip label={fn.relay} color={fn.color} />}
        <GlassChip label={`depth ${fn.depthRange[0]}\u2013${fn.depthRange[1]}`} />
      </div>
    </div>
  )
}
