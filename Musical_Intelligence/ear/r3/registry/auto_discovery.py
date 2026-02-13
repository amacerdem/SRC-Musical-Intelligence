"""Auto-discovery of R3 spectral groups from the groups/ directory.

Scans ``ear/r3/groups/`` subdirectories (``a_consonance`` through
``k_modulation``), imports the ``group`` module from each, and collects
``BaseSpectralGroup`` subclass instances sorted by ``GROUP_NAME``.

The discovery algorithm:

    1. Resolve the ``groups/`` directory relative to this file's location.
    2. Iterate over subdirectories whose names match the ``{letter}_{name}``
       pattern (a_consonance, b_energy, ..., k_modulation).
    3. For each subdirectory, attempt ``importlib.import_module`` of its
       ``group`` module.
    4. Inspect all attributes of the imported module; for each class that
       is a proper subclass of ``BaseSpectralGroup`` (not the base itself),
       instantiate it.
    5. Sort collected instances by ``GROUP_NAME`` alphabetically.
    6. Return the list.  If the groups directory has no implementations
       yet, return an empty list (graceful fallback).
"""
from __future__ import annotations

import importlib
import inspect
import logging
import pathlib
from typing import List

from ....contracts.bases.base_spectral_group import BaseSpectralGroup

logger = logging.getLogger(__name__)

# The 11 expected subdirectory names in alphabetical/index order.
_GROUP_SUBDIRS = (
    "a_consonance",
    "b_energy",
    "c_timbre",
    "d_change",
    "e_interactions",
    "f_pitch_chroma",
    "g_rhythm_groove",
    "h_harmony",
    "i_information",
    "j_timbre_extended",
    "k_modulation",
)

# Relative package path from registry/ to groups/
# registry is at: Musical_Intelligence.ear.r3.registry
# groups  is at: Musical_Intelligence.ear.r3.groups
_GROUPS_PACKAGE = "..groups"


def auto_discover_groups() -> List[BaseSpectralGroup]:
    """Scan ``ear/r3/groups/`` and return instances of all discovered groups.

    For each of the 11 expected subdirectories (``a_consonance`` through
    ``k_modulation``), imports the ``group`` module, finds all
    ``BaseSpectralGroup`` subclasses, and instantiates them.

    Returns:
        List of ``BaseSpectralGroup`` instances sorted by ``GROUP_NAME``
        alphabetically.  Returns an empty list if no group implementations
        exist yet (graceful fallback).
    """
    instances: List[BaseSpectralGroup] = []

    # Resolve the groups/ directory on the filesystem to check existence
    groups_dir = pathlib.Path(__file__).resolve().parent.parent / "groups"
    if not groups_dir.is_dir():
        logger.debug(
            "Groups directory not found at %s; returning empty list.",
            groups_dir,
        )
        return []

    for subdir_name in _GROUP_SUBDIRS:
        subdir_path = groups_dir / subdir_name
        if not subdir_path.is_dir():
            logger.debug("Skipping missing group subdirectory: %s", subdir_name)
            continue

        # Build the fully-qualified module path relative to this package.
        # From registry/, ..groups.{subdir_name}.group resolves to
        # Musical_Intelligence.ear.r3.groups.{subdir_name}.group
        module_path = f"{_GROUPS_PACKAGE}.{subdir_name}.group"

        try:
            mod = importlib.import_module(module_path, package=__package__)
        except ImportError as exc:
            logger.debug(
                "Could not import group module %s: %s",
                module_path,
                exc,
            )
            continue
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "Unexpected error importing group module %s: %s",
                module_path,
                exc,
            )
            continue

        # Inspect all module attributes for BaseSpectralGroup subclasses
        for attr_name in dir(mod):
            attr = getattr(mod, attr_name, None)
            if attr is None:
                continue
            if not isinstance(attr, type):
                continue
            if not issubclass(attr, BaseSpectralGroup):
                continue
            if attr is BaseSpectralGroup:
                continue
            # Skip abstract classes
            if inspect.isabstract(attr):
                continue

            try:
                instance = attr()
                instances.append(instance)
                logger.debug(
                    "Discovered group: %s from %s.%s",
                    instance.GROUP_NAME,
                    module_path,
                    attr_name,
                )
            except Exception as exc:  # noqa: BLE001
                logger.warning(
                    "Failed to instantiate %s.%s: %s",
                    module_path,
                    attr_name,
                    exc,
                )

    # Sort by GROUP_NAME alphabetically (which also matches A-K index order)
    instances.sort(key=lambda g: g.GROUP_NAME)
    return instances
