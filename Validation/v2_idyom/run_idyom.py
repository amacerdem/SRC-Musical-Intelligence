"""Run IDyOM on melodic corpora → information content per note."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

import numpy as np


def run_idyom_on_melodies(
    melodies: List[Dict],
    order: int = 5,
) -> List[Dict]:
    """Run IDyOMpy on a list of melodies.

    Computes information content (IC) and entropy per note using
    a variable-order Markov model (IDyOMpy).

    Args:
        melodies: List of melody dicts with 'pitches' and 'durations'.
        order: Maximum model order for IDyOM.

    Returns:
        List of dicts with 'ic' (per-note IC), 'entropy', 'melody_name'.
    """
    try:
        from idyompy import IDyOM
        return _run_with_idyompy(melodies, order)
    except ImportError:
        print("[V2] IDyOMpy not installed, using simplified n-gram model")
        return _run_simplified_model(melodies, order)


def _run_with_idyompy(melodies: List[Dict], order: int) -> List[Dict]:
    """Run using the idyompy package."""
    from idyompy import IDyOM

    # Train IDyOM on the full corpus
    all_pitches = [m["pitches"].tolist() for m in melodies]
    model = IDyOM(order=order)
    model.train(all_pitches)

    results = []
    for melody in melodies:
        pitches = melody["pitches"].tolist()
        ic_values = []
        entropy_values = []

        for i in range(1, len(pitches)):
            context = pitches[max(0, i - order):i]
            distribution = model.predict(context)

            if distribution is not None:
                actual = pitches[i]
                prob = distribution.get(actual, 1e-10)
                ic = -np.log2(max(prob, 1e-10))
                entropy = -sum(p * np.log2(max(p, 1e-10))
                               for p in distribution.values() if p > 0)
            else:
                ic = 4.0  # default high IC
                entropy = 4.0

            ic_values.append(ic)
            entropy_values.append(entropy)

        results.append({
            "ic": np.array(ic_values),
            "entropy": np.array(entropy_values),
            "melody_name": melody["name"],
        })

    return results


def _run_simplified_model(melodies: List[Dict], order: int) -> List[Dict]:
    """Simplified n-gram model as fallback when IDyOMpy is unavailable.

    Uses a simple conditional probability model:
    P(note_t | note_{t-1}, ..., note_{t-n})
    IC = -log2(P)
    """
    from collections import Counter, defaultdict

    # Build n-gram counts from all melodies
    ngram_counts: Dict[int, Dict] = {}
    for n in range(1, order + 1):
        ngram_counts[n] = defaultdict(Counter)

    for melody in melodies:
        pitches = melody["pitches"].tolist()
        for n in range(1, min(order + 1, len(pitches))):
            for i in range(n, len(pitches)):
                context = tuple(pitches[i - n:i])
                target = pitches[i]
                ngram_counts[n][context][target] += 1

    # Compute IC per note using backoff
    results = []
    for melody in melodies:
        pitches = melody["pitches"].tolist()
        ic_values = []
        entropy_values = []

        for i in range(1, len(pitches)):
            ic = 4.0  # default
            entropy = 4.0
            actual = pitches[i]

            # Try longest matching context first (backoff)
            for n in range(min(order, i), 0, -1):
                context = tuple(pitches[i - n:i])
                if context in ngram_counts[n]:
                    counts = ngram_counts[n][context]
                    total = sum(counts.values())
                    prob = counts.get(actual, 0) / total
                    if prob > 0:
                        ic = -np.log2(prob)
                        entropy = -sum(
                            (c / total) * np.log2(c / total)
                            for c in counts.values() if c > 0
                        )
                        break

            ic_values.append(ic)
            entropy_values.append(entropy)

        results.append({
            "ic": np.array(ic_values),
            "entropy": np.array(entropy_values),
            "melody_name": melody["name"],
        })

    return results
