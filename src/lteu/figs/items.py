"""Figure items."""

from enum import StrEnum
from typing import Literal

import seaborn as sns

from lteu import tools
from lteu.eval.merge import files as merge_files
from lteu.eval.run import files as eval_files


class Header(StrEnum):
    """Base Header."""

    SAMPLE_ID = eval_files.Header.SAMPLE_ID
    VERSION = "version"
    TOOL_CODE = merge_files.Header.TOOL_CODE
    UNW_COMPLETENESS = eval_files.Header.UNW_COMPLETENESS
    UNW_HOMOGENEITY = eval_files.Header.UNW_HOMOGENEITY
    W_COMPLETENESS = eval_files.Header.W_COMPLETENESS
    W_HOMOGENEITY = eval_files.Header.W_HOMOGENEITY


class Versions(StrEnum):
    """Versions."""

    V1 = "v1"
    V2 = "v2"


class Contents(StrEnum):
    """Contents."""

    ONLY_PLASMIDS = "only_plasmids"
    WITH_CHROMOSOMES = "with_chromosomes"

    def to_label(self) -> str:
        """Get the corresponding label."""
        match self:
            case Contents.ONLY_PLASMIDS:
                return "Only plasmids"
            case Contents.WITH_CHROMOSOMES:
                return "With chromosomes"


class MeasureCodes(StrEnum):
    """Measure codes base class."""

    UNW_COMPLETENESS = "unw_comp"
    UNW_HOMOGENEITY = "unw_hom"
    W_COMPLETENESS = "w_comp"
    W_HOMOGENEITY = "w_hom"

    def to_column(self) -> str:
        """Get the corresponding column."""
        match self:
            case MeasureCodes.UNW_COMPLETENESS:
                return eval_files.Header.UNW_COMPLETENESS
            case MeasureCodes.UNW_HOMOGENEITY:
                return eval_files.Header.UNW_HOMOGENEITY
            case MeasureCodes.W_COMPLETENESS:
                return eval_files.Header.W_COMPLETENESS
            case MeasureCodes.W_HOMOGENEITY:
                return eval_files.Header.W_HOMOGENEITY

    def to_label(self, mode: Literal["single", "plural"] = "single") -> str:
        """Get the corresponding label."""
        match self:
            case MeasureCodes.UNW_COMPLETENESS:
                return (
                    "Unweighted completeness"
                    if mode == "single"
                    else "Unweighted completenesses"
                )
            case MeasureCodes.UNW_HOMOGENEITY:
                return (
                    "Unweighted homogeneity"
                    if mode == "single"
                    else "Unweighted homogeneities"
                )
            case MeasureCodes.W_COMPLETENESS:
                return (
                    "Weighted completeness"
                    if mode == "single"
                    else "Weighted completenesses"
                )
            case MeasureCodes.W_HOMOGENEITY:
                return (
                    "Weighted homogeneity"
                    if mode == "single"
                    else "Weighted homogeneities"
                )


def tools_color_palette(
    tools: list[tools.Binning],
) -> list[tuple[float, float, float]]:
    """Get the corresponding color palette."""
    return [tool.to_color() for tool in tools]


def columns_color_palette(columns: list[str]) -> list[tuple[float, float, float]]:
    """Get the corresponding color palette."""
    return tools_color_palette([tools.Binning(tool_code) for tool_code in columns])


# REVIEW (refactor) Useless?
class Presence(StrEnum):
    """Presence."""

    YES = "Yes"
    NO = "No"

    def to_color(self) -> tuple[float, float, float]:
        """Get the corresponding color."""
        palette = sns.color_palette("Set3")
        match self:
            case Presence.YES:
                return palette[4]
            case Presence.NO:
                return palette[3]

    @classmethod
    def column_name(cls) -> str:
        """Get the corresponding column name."""
        return "Evaluation?"
