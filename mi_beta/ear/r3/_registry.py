"""R3 feature registry: manages spectral group registration and index assignment."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from ...contracts.base_spectral_group import BaseSpectralGroup


@dataclass(frozen=True)
class R3GroupInfo:
    name: str                  # "consonance"
    dim: int                   # 7
    start: int                 # 0
    end: int                   # 7
    feature_names: Tuple[str, ...]


@dataclass(frozen=True)
class R3FeatureMap:
    total_dim: int             # 49
    groups: Tuple[R3GroupInfo, ...]


class R3FeatureRegistry:
    """Collects spectral groups and assigns contiguous INDEX_RANGEs."""

    def __init__(self) -> None:
        self._groups: List[BaseSpectralGroup] = []
        self._frozen = False

    def register(self, group: BaseSpectralGroup) -> None:
        if self._frozen:
            raise RuntimeError("Registry is frozen; cannot register new groups")
        self._groups.append(group)

    def freeze(self) -> R3FeatureMap:
        """Assign contiguous INDEX_RANGEs to each group and return feature map."""
        self._frozen = True
        offset = 0
        infos = []
        for group in self._groups:
            start = offset
            end = offset + group.OUTPUT_DIM
            group.INDEX_RANGE = (start, end)
            infos.append(R3GroupInfo(
                name=group.GROUP_NAME,
                dim=group.OUTPUT_DIM,
                start=start,
                end=end,
                feature_names=tuple(group.feature_names),
            ))
            offset = end

        return R3FeatureMap(
            total_dim=offset,
            groups=tuple(infos),
        )

    @property
    def groups(self) -> List[BaseSpectralGroup]:
        return list(self._groups)
