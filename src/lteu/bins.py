"""Bins."""

from enum import StrEnum


class Contents(StrEnum):
    """Bin contents."""

    ONLY_PLASMIDS = "only_plasmids"
    WITH_CHROMOSOMES = "with_chromosomes"

    def to_label(self) -> str:
        """Get the corresponding label."""
        match self:
            case Contents.ONLY_PLASMIDS:
                return "Only plasmids"
            case Contents.WITH_CHROMOSOMES:
                return "With chromosomes"
