"""Tools."""

from enum import StrEnum

import seaborn as sns


class Binning(StrEnum):
    """Binning tools code."""

    HYASP = "hyasp"
    MOB = "mob"
    PLASBIN_FLOW = "pbf"
    GPLAS_TWO = "gplas2"

    def to_label_wrap(self) -> str:
        """Get the corresponding label (wrapped)."""
        return self.to_label()

    def to_label(self) -> str:
        """Get the corresponding label."""
        match self:
            case Binning.HYASP:
                return "HyAsP"
            case Binning.MOB:
                return "MOB-recon"
            case Binning.PLASBIN_FLOW:
                return "PlasBin-flow"
            case Binning.GPLAS_TWO:
                return "gplas2"

    def to_color(self) -> tuple[float, float, float]:
        """Get the corresponding color."""
        palette = sns.color_palette("Set3")
        match self:
            case Binning.HYASP:
                return palette[0]
            case Binning.MOB:
                return palette[1]
            case Binning.PLASBIN_FLOW:
                return palette[2]
            case Binning.GPLAS_TWO:
                return palette[3]
