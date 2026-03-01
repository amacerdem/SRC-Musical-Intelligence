/** Shared types for the Neuroacoustic Atlas */

export interface AtlasNode {
  id: string
  type: 'r3-group' | 'h3-scale' | 'function' | 'belief' | 'relay' | 'mechanism'
       | 'dim-psychology' | 'dim-cognition' | 'dim-neuroscience'
  label: string
  color: string
  description?: string
  functionId?: string
  beliefIndex?: number
  beliefIndices?: number[]
  features?: string[]
  dimRange?: [number, number]
}
