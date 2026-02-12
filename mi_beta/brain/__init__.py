"""MI-Beta BRAIN -- Multi-model cognitive architecture.

This package implements the brain layer of the MI pipeline:

    Ear (Cochlea -> R3 -> H3)
        |
        v
    Brain (regions, neurochemicals, units, mechanisms, pathways)
        |
        v
    Language (L3 semantic interpretation)

Subpackages:
    regions/         -- Anatomical brain region definitions (MNI152)
    neurochemicals/  -- Neurochemical system definitions and state management
    units/           -- Cognitive units (ARU, SPU, STU, IMU, ...)
    mechanisms/      -- Shared mechanism implementations
    pathways/        -- Cross-unit pathway declarations

The BrainOrchestrator lives in mi_beta.pipeline.brain_runner to keep
the brain package focused on definitions.  Re-exported here for
convenience via lazy import to avoid circular dependencies:

    from mi_beta.brain import BrainOrchestrator
"""


def __getattr__(name: str):
    if name == "BrainOrchestrator":
        from mi_beta.pipeline.brain_runner import BrainOrchestrator
        return BrainOrchestrator
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__: list[str] = [
    "BrainOrchestrator",
]
