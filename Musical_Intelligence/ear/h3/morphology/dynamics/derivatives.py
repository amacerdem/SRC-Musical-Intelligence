"""Dynamics derivative morphs: M8-M13 velocity and acceleration.

All functions are pure (torch only, no project dependencies).
"""
from __future__ import annotations

import torch
from torch import Tensor


def m8_velocity(window: Tensor, weights: Tensor) -> Tensor:
    """M8: Instantaneous velocity (last first-difference).

    Formula: window[:, -1] - window[:, -2]

    Args:
        window: (B, W) R3 values in the time window.
        weights: (W,) Unused (interface consistency).

    Returns:
        (B,) One scalar per batch item.

    Properties:
        - Signed, min window = 2.
        - Returns zeros(B) for win_len < 2.
    """
    B, W = window.shape
    if W < 2:
        return torch.zeros(B, device=window.device, dtype=window.dtype)
    return window[:, -1] - window[:, -2]


def m9_velocity_mean(window: Tensor, weights: Tensor) -> Tensor:
    """M9: Mean velocity (mean of first differences).

    Formula: mean(diff(window, dim=-1), dim=-1)

    Args:
        window: (B, W) R3 values in the time window.
        weights: (W,) Unused (interface consistency).

    Returns:
        (B,) One scalar per batch item.

    Properties:
        - Signed, min window = 2.
        - Returns zeros(B) for win_len < 2.
    """
    B, W = window.shape
    if W < 2:
        return torch.zeros(B, device=window.device, dtype=window.dtype)
    d1 = torch.diff(window, dim=-1)  # (B, W-1)
    return torch.mean(d1, dim=-1)


def m10_velocity_std(window: Tensor, weights: Tensor) -> Tensor:
    """M10: Velocity standard deviation.

    Formula: std(diff(window, dim=-1), dim=-1)

    Args:
        window: (B, W) R3 values in the time window.
        weights: (W,) Unused (interface consistency).

    Returns:
        (B,) One scalar per batch item.

    Properties:
        - Unsigned, min window = 3.
        - Returns zeros(B) for win_len < 3.
    """
    B, W = window.shape
    if W < 3:
        return torch.zeros(B, device=window.device, dtype=window.dtype)
    d1 = torch.diff(window, dim=-1)  # (B, W-1)
    return torch.std(d1, dim=-1)


def m11_acceleration(window: Tensor, weights: Tensor) -> Tensor:
    """M11: Instantaneous acceleration (last second-difference).

    Formula: window[:, -1] - 2*window[:, -2] + window[:, -3]

    Args:
        window: (B, W) R3 values in the time window.
        weights: (W,) Unused (interface consistency).

    Returns:
        (B,) One scalar per batch item.

    Properties:
        - Signed, min window = 3.
        - Returns zeros(B) for win_len < 3.
    """
    B, W = window.shape
    if W < 3:
        return torch.zeros(B, device=window.device, dtype=window.dtype)
    d2 = torch.diff(torch.diff(window, dim=-1), dim=-1)  # (B, W-2)
    return d2[:, -1]


def m12_acceleration_mean(window: Tensor, weights: Tensor) -> Tensor:
    """M12: Mean acceleration (mean of second differences).

    Formula: mean(diff(diff(window, dim=-1), dim=-1), dim=-1)

    Args:
        window: (B, W) R3 values in the time window.
        weights: (W,) Unused (interface consistency).

    Returns:
        (B,) One scalar per batch item.

    Properties:
        - Signed, min window = 3.
        - Returns zeros(B) for win_len < 3.
    """
    B, W = window.shape
    if W < 3:
        return torch.zeros(B, device=window.device, dtype=window.dtype)
    d2 = torch.diff(torch.diff(window, dim=-1), dim=-1)  # (B, W-2)
    return torch.mean(d2, dim=-1)


def m13_acceleration_std(window: Tensor, weights: Tensor) -> Tensor:
    """M13: Acceleration standard deviation.

    Formula: std(diff(diff(window, dim=-1), dim=-1), dim=-1)

    Args:
        window: (B, W) R3 values in the time window.
        weights: (W,) Unused (interface consistency).

    Returns:
        (B,) One scalar per batch item.

    Properties:
        - Unsigned, min window = 4.
        - Returns zeros(B) for win_len < 4.
    """
    B, W = window.shape
    if W < 4:
        return torch.zeros(B, device=window.device, dtype=window.dtype)
    d2 = torch.diff(torch.diff(window, dim=-1), dim=-1)  # (B, W-2)
    return torch.std(d2, dim=-1)
