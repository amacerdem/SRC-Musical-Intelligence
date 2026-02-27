import { useEffect, useMemo } from 'react'
import { useC3Store } from '../stores/c3Store'
import type { LayerMeta } from '../stores/c3Store'

export interface DimensionTrace {
  index: number
  name: string
  layerCode: string
  scope: string
  data: number[]
}

export interface LayerGroup {
  code: string
  name: string
  scope: string
  traces: DimensionTrace[]
}

/**
 * Fetches mechanism relay data + metadata, splits into per-dimension traces
 * grouped by layer (E/M/P/F).
 */
export function useRelayDimensions(
  mechanismName: string,
  experimentId: string | null,
  autoLoad: boolean,
): { layers: LayerGroup[] | null; loading: boolean } {
  const relayCache = useC3Store((s) => s.relayCache)
  const relayLoading = useC3Store((s) => s.relayLoading)
  const mechanismMeta = useC3Store((s) => s.mechanismMeta)
  const mechanismMetaLoading = useC3Store((s) => s.mechanismMetaLoading)
  const loadRelay = useC3Store((s) => s.loadRelay)
  const loadMechanismMeta = useC3Store((s) => s.loadMechanismMeta)

  // Trigger loads when autoLoad is true
  useEffect(() => {
    if (!autoLoad || !experimentId) return
    loadMechanismMeta()
    loadRelay(experimentId, mechanismName)
  }, [autoLoad, experimentId, mechanismName, loadMechanismMeta, loadRelay])

  const loading = !!(relayLoading[mechanismName] || mechanismMetaLoading)

  const layers = useMemo(() => {
    const relay = relayCache[mechanismName]
    const meta = mechanismMeta?.[mechanismName]
    if (!relay || !meta) return null

    const { data, dim } = relay
    const nFrames = data.length / dim

    return meta.layers.map((layer: LayerMeta): LayerGroup => {
      const traces: DimensionTrace[] = []
      for (let d = layer.start; d < layer.end; d++) {
        const dimName = meta.dimensions[d] ?? `D${d}`
        const trace: number[] = new Array(nFrames)
        for (let t = 0; t < nFrames; t++) {
          trace[t] = data[t * dim + d]
        }
        traces.push({
          index: d,
          name: dimName,
          layerCode: layer.code,
          scope: layer.scope,
          data: trace,
        })
      }
      return {
        code: layer.code,
        name: layer.name,
        scope: layer.scope,
        traces,
      }
    })
  }, [relayCache, mechanismMeta, mechanismName])

  return { layers, loading }
}
