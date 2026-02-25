import { type H3TupleMeta, LAW_COLORS } from '../../data/h3Demands'
import { SignalTrace } from '../charts/SignalTrace'
import { Loader2 } from 'lucide-react'

interface H3TupleRowProps {
  meta: H3TupleMeta
  data: Float32Array | null
  color?: string
  cursorFrame?: number
  totalFrames?: number
}

export function H3TupleRow({ meta, data, color, cursorFrame, totalFrames }: H3TupleRowProps) {
  const lawColor = LAW_COLORS[meta.lawName] ?? '#60a5fa'

  return (
    <div className="rounded-lg bg-white/[0.02] border border-white/5 px-3 py-2">
      {/* Header */}
      <div className="flex items-center gap-2 mb-1">
        <span
          className="w-2 h-2 rounded-full shrink-0"
          style={{ backgroundColor: lawColor }}
          title={`L${meta.law} ${meta.lawName}`}
        />
        <span className="mono text-[10px] text-text-tertiary">
          ({meta.r3Idx}, H{meta.horizon}, M{meta.morph}, L{meta.law})
        </span>
        <span className="text-xs text-text-secondary truncate flex-1">
          {meta.r3Name} · {meta.morphName} · {meta.horizonLabel} · {meta.lawName}
        </span>
        {meta.weight != null && (
          <span className="mono text-[10px] px-1.5 py-0.5 rounded bg-white/5 text-text-tertiary shrink-0">
            w={meta.weight}
          </span>
        )}
      </div>

      {/* Purpose */}
      <div className="text-[10px] text-text-tertiary mb-1.5 ml-4">{meta.purpose}</div>

      {/* Trace */}
      {data ? (
        <SignalTrace
          data={data}
          nChannels={1}
          colors={[color ?? lawColor]}
          height={70}
          cursorFrame={cursorFrame}
          totalFrames={totalFrames}
        />
      ) : (
        <div className="h-[70px] flex items-center justify-center text-text-tertiary">
          <Loader2 size={12} className="animate-spin mr-1.5" />
          <span className="text-[10px]">loading H3 data...</span>
        </div>
      )}
    </div>
  )
}
