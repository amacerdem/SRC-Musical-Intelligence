"""Citation -- Single empirical finding with effect size.

A Citation is NOT a bibliography entry -- it is a specific CLAIM from a specific
study, used to ground cognitive model dimensions and mechanisms in empirical
evidence.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Citation:
    """A single empirical finding supporting a model dimension or mechanism.

    Attributes:
        author:      First author last name (e.g. ``"Salimpoor"``).
        year:        Publication year.
        finding:     One-line summary of the relevant finding.
        effect_size: Reported effect size (e.g. ``"r=0.84"``, ``"d=0.67"``).
                     Empty string if not applicable.
    """

    author: str
    year: int
    finding: str
    effect_size: str = ""

    # ------------------------------------------------------------------
    # Computed properties
    # ------------------------------------------------------------------

    @property
    def short_ref(self) -> str:
        """Short-form reference: ``"Author YEAR"``."""
        return f"{self.author} {self.year}"
