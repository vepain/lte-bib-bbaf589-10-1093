"""Measures module."""

from __future__ import annotations

from enum import StrEnum
from typing import Literal


class Items(StrEnum):
    """Measures."""

    UNW_COMPLETENESS = "unweighted_completeness"
    UNW_HOMOGENEITY = "unweighted_homogeneity"
    W_COMPLETENESS = "weighted_completeness"
    W_HOMOGENEITY = "weighted_homogeneity"

    def to_class(self) -> Class:
        """Get measure class."""
        match self:
            case Items.UNW_COMPLETENESS | Items.W_COMPLETENESS:
                return Class.COMPLETENESS
            case Items.UNW_HOMOGENEITY | Items.W_HOMOGENEITY:
                return Class.HOMOGENEITY

    def to_mode(self) -> Mode:
        """Get measure mode."""
        match self:
            case Items.UNW_COMPLETENESS | Items.UNW_HOMOGENEITY:
                return Mode.UNWEIGHTED
            case Items.W_COMPLETENESS | Items.W_HOMOGENEITY:
                return Mode.WEIGHTED

    def to_label(self, mode: Literal["single", "plural"] = "single") -> str:
        """Get the corresponding label."""
        match self:
            case Items.UNW_COMPLETENESS:
                return (
                    "Unweighted completeness"
                    if mode == "single"
                    else "Unweighted completenesses"
                )
            case Items.UNW_HOMOGENEITY:
                return (
                    "Unweighted homogeneity"
                    if mode == "single"
                    else "Unweighted homogeneities"
                )
            case Items.W_COMPLETENESS:
                return (
                    "Weighted completeness"
                    if mode == "single"
                    else "Weighted completenesses"
                )
            case Items.W_HOMOGENEITY:
                return (
                    "Weighted homogeneity"
                    if mode == "single"
                    else "Weighted homogeneities"
                )


class Class(StrEnum):
    """Measure class."""

    COMPLETENESS = "Completeness"
    HOMOGENEITY = "Homogeneity"


class Mode(StrEnum):
    """Measure modes."""

    UNWEIGHTED = "Unweighted"
    WEIGHTED = "Weighted"


class Codes(StrEnum):
    """Measure codes base class."""

    UNW_COMPLETENESS = "unw_comp"
    UNW_HOMOGENEITY = "unw_hom"
    W_COMPLETENESS = "w_comp"
    W_HOMOGENEITY = "w_hom"

    def to_measure(self) -> Items:
        """Get the corresponding measure."""
        match self:
            case Codes.UNW_COMPLETENESS:
                return Items.UNW_COMPLETENESS
            case Codes.UNW_HOMOGENEITY:
                return Items.UNW_HOMOGENEITY
            case Codes.W_COMPLETENESS:
                return Items.W_COMPLETENESS
            case Codes.W_HOMOGENEITY:
                return Items.W_HOMOGENEITY
