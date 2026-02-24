import { useMemo } from 'react'
import { FUNCTIONS } from '../data/functions'
import { MECHANISMS } from '../data/mechanisms'
import { RELAYS } from '../data/relays'
import { useBeliefData, type BeliefDataResult } from './useBeliefData'
import type { FunctionDef } from '../data/functions'
import type { MechanismDef } from '../data/mechanisms'
import type { RelayDef } from '../data/relays'

export interface FunctionDataResult {
  fn: FunctionDef | undefined
  beliefs: BeliefDataResult
  mechanisms: MechanismDef[]
  relay: RelayDef | undefined
}

export function useFunctionData(functionId: string): FunctionDataResult {
  const fn = useMemo(() => FUNCTIONS.find((f) => f.id === functionId), [functionId])
  const beliefs = useBeliefData(functionId)
  const mechanisms = useMemo(() => MECHANISMS.filter((m) => m.functionId === functionId), [functionId])
  const relay = useMemo(() => RELAYS.find((r) => r.functionId === functionId), [functionId])

  return { fn, beliefs, mechanisms, relay }
}
