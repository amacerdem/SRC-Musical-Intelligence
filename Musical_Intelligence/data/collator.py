"""Collator -- Batch collation for variable-length MI training samples.

Handles padding/truncation of temporal sequences to uniform length
within a batch, producing padded tensors with an attention mask.

Usage::

    from torch.utils.data import DataLoader

    dataset = MIDataset(data_dir="path/to/data", segment_frames=2048)
    collator = MICollator(pad_value=0.0)
    loader = DataLoader(dataset, batch_size=4, collate_fn=collator)
"""
from __future__ import annotations

from typing import Dict, List

import torch
from torch import Tensor


class MICollator:
    """Collates variable-length MI training samples into padded batches.

    Pads all temporal sequences to the maximum length in the batch.
    Produces an ``attention_mask`` tensor indicating valid frames.

    Attributes:
        pad_value: Value used for padding (default 0.0).
    """

    def __init__(self, pad_value: float = 0.0) -> None:
        self._pad_value = pad_value

    def __call__(self, samples: List[Dict[str, Tensor]]) -> Dict[str, Tensor]:
        """Collate a list of samples into a batched dict.

        Parameters
        ----------
        samples : list of dict
            Each dict has keys: ``mel``, ``r3``, ``h3_dense``, ``c3``.
            Each value has shape ``(T_i, dim)`` where ``T_i`` may vary.

        Returns
        -------
        dict
            Batched dict with keys: ``mel``, ``r3``, ``h3_dense``, ``c3``,
            ``attention_mask``. Each tensor has shape ``(B, T_max, dim)``
            except ``attention_mask`` which is ``(B, T_max)`` bool.
        """
        keys = ["mel", "r3", "h3_dense", "c3"]
        batch_size = len(samples)

        # Find max temporal length
        max_t = max(s[keys[0]].shape[0] for s in samples)

        result: Dict[str, Tensor] = {}
        mask = torch.zeros(batch_size, max_t, dtype=torch.bool)

        for key in keys:
            dim = samples[0][key].shape[-1]
            padded = torch.full(
                (batch_size, max_t, dim),
                self._pad_value,
                dtype=samples[0][key].dtype,
            )

            for i, sample in enumerate(samples):
                t = sample[key].shape[0]
                padded[i, :t] = sample[key]
                if key == keys[0]:  # Only set mask once
                    mask[i, :t] = True

            result[key] = padded

        result["attention_mask"] = mask
        return result
