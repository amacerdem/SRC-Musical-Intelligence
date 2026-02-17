"""StageExecutor -- Executes R3 spectral groups in DAG-ordered stages.

Iterates through the 2-stage dependency DAG and invokes each spectral group's
``compute()`` (Stage 1) or ``compute_with_deps()`` (Stage 2) method in the
correct order.  Groups within the same stage are executed sequentially for now;
the stage structure preserves the option for future CUDA multi-stream
parallelism.

Execution flow::

    Stage 1 (parallel-ready):
        For each group in {A, B, C, D, F, J, K}:
            outputs[group_name] = group.compute(mel)

    Stage 2 (parallel-ready, after Stage 1):
        For each group in {G, H}:
            deps_dict = {dep_name: outputs[dep_name] for dep_name in group.DEPENDENCIES}
            outputs[group_name] = group.compute_with_deps(mel, deps_dict)

See Also:
    Docs/R3/Pipeline/DependencyDAG.md  -- execution semantics
    Docs/R3/R3-SPECTRAL-ARCHITECTURE.md  Section 11
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from .dag import DependencyDAG

if TYPE_CHECKING:
    from torch import Tensor

    from ....contracts.bases.base_spectral_group import BaseSpectralGroup


class StageExecutor:
    """Executes R3 spectral groups according to the 3-stage DAG.

    The executor receives the mel spectrogram and a dict of instantiated
    spectral group objects (keyed by canonical ``GROUP_NAME``), then
    processes them stage by stage, threading dependency outputs from
    earlier stages into later ones.

    This class is stateless; all state lives in the groups themselves.
    """

    def execute(
        self,
        mel: Tensor,
        groups: Dict[str, BaseSpectralGroup],
        dag: DependencyDAG,
        *,
        audio: "Tensor | None" = None,
        sr: int = 44100,
    ) -> Dict[str, Tensor]:
        """Execute all spectral groups in DAG-ordered stages.

        Args:
            mel: ``(B, N_MELS, T)`` log-mel spectrogram tensor.
                ``N_MELS`` = 128, frame rate 172.27 Hz.
            groups: Dict mapping canonical ``GROUP_NAME`` (e.g.
                ``"consonance"``) to the corresponding
                :class:`BaseSpectralGroup` instance.  All 9 groups must
                be present.
            dag: The :class:`DependencyDAG` defining stage membership and
                dependency edges.
            audio: Optional ``(B, N_SAMPLES)`` raw waveform tensor at
                *sr* Hz.  When provided, Stage 1 groups that override
                ``compute_from_audio()`` receive it for higher-fidelity
                feature extraction (e.g. psychoacoustic consonance).
            sr: Sample rate in Hz (default 44100).  Only used when *audio*
                is provided.

        Returns:
            Dict mapping canonical group name to output tensor
            ``(B, T, group_dim)`` for each group.

        Raises:
            KeyError: If a group required by the DAG is missing from
                *groups*.
        """
        outputs: Dict[str, Tensor] = {}

        for stage_num in dag.stages:
            stage_group_names = dag.get_stage(stage_num)

            for group_name in stage_group_names:
                if group_name not in groups:
                    raise KeyError(
                        f"Group {group_name!r} (stage {stage_num}) "
                        f"not found in the provided groups dict. "
                        f"Available: {sorted(groups)}"
                    )

                group = groups[group_name]
                dep_names = dag.get_dependencies(group_name)

                if not dep_names:
                    # Stage 1: try audio path first, fall back to mel
                    result = None
                    if audio is not None:
                        result = group.compute_from_audio(mel, audio, sr)
                    if result is None:
                        result = group.compute(mel)
                    outputs[group_name] = result
                else:
                    # Stage 2-3 group: build deps_dict from prior outputs
                    deps_dict: Dict[str, Tensor] = {}
                    for dep_name in dep_names:
                        if dep_name not in outputs:
                            raise KeyError(
                                f"Dependency {dep_name!r} for group "
                                f"{group_name!r} has not been computed yet. "
                                f"This indicates a DAG ordering error."
                            )
                        deps_dict[dep_name] = outputs[dep_name]

                    outputs[group_name] = group.compute_with_deps(
                        mel, deps_dict
                    )

        return outputs

    # ------------------------------------------------------------------
    # Repr
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return "StageExecutor()"
