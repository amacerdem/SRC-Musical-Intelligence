/** Centralized data loading hook for experiment results. */

import { useEffect } from 'react';
import { usePipelineStore } from '../stores/pipelineStore';
import { fetchBinary } from '../api/client';

export function useExperimentData() {
  const {
    currentExperimentId,
    r3Features, r3Frames,
    rewardData, ramData,
    beliefsData, neuroData,
    relayCache,
    setR3Data, setRewardData, setRamData,
    setBeliefsData, setNeuroData, setRelayData,
  } = usePipelineStore();

  // Load core data when experiment changes
  useEffect(() => {
    if (!currentExperimentId) return;

    // Load R3
    if (!r3Features) {
      fetchBinary(`/pipeline/results/${currentExperimentId}/r3`)
        .then(({ data, headers }) => {
          const frames = parseInt(headers.get('X-N-Frames') || '0');
          const names = (headers.get('X-Feature-Names') || '').split(',');
          setR3Data(new Float32Array(data), names, frames);
        })
        .catch(() => {});
    }

    // Load reward
    if (!rewardData) {
      fetchBinary(`/pipeline/results/${currentExperimentId}/c3/reward`)
        .then(({ data }) => setRewardData(new Float32Array(data)))
        .catch(() => {});
    }

    // Load RAM
    if (!ramData) {
      fetchBinary(`/pipeline/results/${currentExperimentId}/c3/ram`)
        .then(({ data }) => setRamData(new Float32Array(data)))
        .catch(() => {});
    }
  }, [currentExperimentId]);

  // Lazy loaders for depth-1+ data
  const loadBeliefs = () => {
    if (beliefsData || !currentExperimentId) return;
    fetchBinary(`/pipeline/results/${currentExperimentId}/c3/beliefs`)
      .then(({ data, headers }) => {
        const nBeliefs = parseInt(headers.get('X-N-Beliefs') || '0');
        const names = (headers.get('X-Belief-Names') || '').split(',');
        setBeliefsData(new Float32Array(data), names, nBeliefs);
      })
      .catch(() => {});
  };

  const loadNeuro = () => {
    if (neuroData || !currentExperimentId) return;
    fetchBinary(`/pipeline/results/${currentExperimentId}/c3/neuro`)
      .then(({ data }) => setNeuroData(new Float32Array(data)))
      .catch(() => {});
  };

  const loadRelay = (name: string, dim: number) => {
    if (relayCache[name] || !currentExperimentId) return;
    fetchBinary(`/pipeline/results/${currentExperimentId}/c3/relays/${name.toLowerCase()}`)
      .then(({ data, headers }) => {
        const d = parseInt(headers.get('X-N-Dims') || String(dim));
        setRelayData(name, new Float32Array(data), d);
      })
      .catch(() => {});
  };

  return {
    hasData: currentExperimentId !== null && r3Features !== null,
    loadBeliefs,
    loadNeuro,
    loadRelay,
  };
}
