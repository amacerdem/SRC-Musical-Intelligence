import { useEffect } from 'react'
import { useC3Store } from '../stores/c3Store'

export interface RelayDataResult {
  data: Float32Array | null
  dim: number
  loading: boolean
}

export function useRelayData(relayName: string | null, experimentId?: string): RelayDataResult {
  const { relayCache, relayLoading, loadRelay } = useC3Store()

  useEffect(() => {
    if (relayName && experimentId && !relayCache[relayName]) {
      loadRelay(experimentId, relayName)
    }
  }, [relayName, experimentId, relayCache, loadRelay])

  if (!relayName) return { data: null, dim: 0, loading: false }

  return {
    data: relayCache[relayName]?.data ?? null,
    dim: relayCache[relayName]?.dim ?? 0,
    loading: relayLoading[relayName] ?? false,
  }
}
