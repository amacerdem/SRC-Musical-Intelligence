"""Reusable assertion helpers for micro-belief tests.

All helpers operate on ``(B, T)`` belief tensors (typically ``B=1``).
They trim the first *warmup* frames to avoid H³ edge effects.
"""
from __future__ import annotations

from torch import Tensor

WARMUP_FRAMES = 50


def _trim(t: Tensor) -> Tensor:
    """Remove warmup frames from the time dimension."""
    if t.shape[-1] > WARMUP_FRAMES * 2:
        return t[:, WARMUP_FRAMES:]
    return t


# ── Ordering ─────────────────────────────────────────────────────────

def assert_greater(
    result_a: Tensor,
    result_b: Tensor,
    label_a: str,
    label_b: str,
    margin: float = 0.0,
) -> None:
    """Assert mean(a) > mean(b) + margin (after warmup trim)."""
    ma = _trim(result_a).mean().item()
    mb = _trim(result_b).mean().item()
    assert ma > mb + margin, (
        f"{label_a} ({ma:.4f}) should be > {label_b} ({mb:.4f}) "
        f"by at least {margin}"
    )


def assert_ordering(
    results: dict[str, Tensor],
    order: list[str],
    belief_name: str,
) -> None:
    """Assert that mean values follow the given ordering (descending).

    ``order`` is a list of keys into *results*, from highest to lowest.
    """
    means = {k: _trim(results[k]).mean().item() for k in order}
    for i in range(len(order) - 1):
        hi, lo = order[i], order[i + 1]
        assert means[hi] > means[lo], (
            f"[{belief_name}] {hi} ({means[hi]:.4f}) should be > "
            f"{lo} ({means[lo]:.4f})"
        )


# ── Temporal trends ──────────────────────────────────────────────────

def assert_rising(
    result: Tensor,
    label: str,
    n_segments: int = 4,
    tolerance: float = 0.05,
) -> None:
    """Assert the signal generally rises over time (segment means increase)."""
    trimmed = _trim(result)
    T = trimmed.shape[-1]
    seg = T // n_segments
    means = [
        trimmed[0, i * seg : (i + 1) * seg].mean().item()
        for i in range(n_segments)
    ]
    for i in range(1, n_segments):
        assert means[i] >= means[i - 1] - tolerance, (
            f"[{label}] segment {i} ({means[i]:.4f}) should be >= "
            f"segment {i - 1} ({means[i - 1]:.4f}) - {tolerance}"
        )


def assert_falling(
    result: Tensor,
    label: str,
    n_segments: int = 4,
    tolerance: float = 0.05,
) -> None:
    """Assert the signal generally falls over time."""
    trimmed = _trim(result)
    T = trimmed.shape[-1]
    seg = T // n_segments
    means = [
        trimmed[0, i * seg : (i + 1) * seg].mean().item()
        for i in range(n_segments)
    ]
    for i in range(1, n_segments):
        assert means[i] <= means[i - 1] + tolerance, (
            f"[{label}] segment {i} ({means[i]:.4f}) should be <= "
            f"segment {i - 1} ({means[i - 1]:.4f}) + {tolerance}"
        )


def assert_halves(
    result: Tensor,
    label: str,
    direction: str = "rising",
) -> None:
    """Assert second half mean > first half mean (or vice versa)."""
    trimmed = _trim(result)
    T = trimmed.shape[-1]
    first = trimmed[0, : T // 2].mean().item()
    second = trimmed[0, T // 2 :].mean().item()
    if direction == "rising":
        assert second > first, (
            f"[{label}] second half ({second:.4f}) should be > "
            f"first half ({first:.4f})"
        )
    else:
        assert first > second, (
            f"[{label}] first half ({first:.4f}) should be > "
            f"second half ({second:.4f})"
        )


# ── Stability ────────────────────────────────────────────────────────

def assert_stable(
    result: Tensor,
    label: str,
    max_std: float = 0.15,
) -> None:
    """Assert belief value has low variance (stable response)."""
    std = _trim(result)[0].std().item()
    assert std < max_std, (
        f"[{label}] std ({std:.4f}) should be < {max_std}"
    )


# ── Range ────────────────────────────────────────────────────────────

def assert_in_range(
    result: Tensor,
    label: str,
    low: float = 0.0,
    high: float = 1.0,
    margin: float = 0.05,
) -> None:
    """Assert all values fall within [low - margin, high + margin]."""
    trimmed = _trim(result)
    mn = trimmed.min().item()
    mx = trimmed.max().item()
    assert mn >= low - margin, (
        f"[{label}] min ({mn:.4f}) below {low - margin}"
    )
    assert mx <= high + margin, (
        f"[{label}] max ({mx:.4f}) above {high + margin}"
    )
