"""Evaluation files."""

from enum import StrEnum
from pathlib import Path

import pandas as pd


class Header(StrEnum):
    """Evaluation file header."""

    SAMPLE_ID = "sample_id"
    UNW_COMPLETENESS = "unweighted_completeness"
    UNW_HOMOGENEITY = "unweighted_homogeneity"
    W_COMPLETENESS = "weighted_completeness"
    W_HOMOGENEITY = "weighted_homogeneity"


HEADER_TYPES = {
    Header.SAMPLE_ID: str,
    Header.UNW_COMPLETENESS: float,
    Header.UNW_HOMOGENEITY: float,
    Header.W_COMPLETENESS: float,
    Header.W_HOMOGENEITY: float,
}


def to_dataframe(path: Path) -> pd.DataFrame:
    """Convert a file to a pandas DataFrame."""
    return pd.read_csv(path, sep="\t", dtype=HEADER_TYPES)


def new_dataframe() -> pd.DataFrame:
    """Create an empty DataFrame."""
    return pd.DataFrame(columns=list(HEADER_TYPES.keys()))
