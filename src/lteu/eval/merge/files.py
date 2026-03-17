"""Merge evaluations files module."""

from enum import StrEnum
from pathlib import Path

import pandas as pd

from lteu.eval.run import files as eval_files


class Header(StrEnum):
    """Header."""

    SAMPLE_ID = eval_files.Header.SAMPLE_ID
    TOOL_CODE = "tool_code"
    UNW_COMPLETENESS = eval_files.Header.UNW_COMPLETENESS
    UNW_HOMOGENEITY = eval_files.Header.UNW_HOMOGENEITY
    W_COMPLETENESS = eval_files.Header.W_COMPLETENESS
    W_HOMOGENEITY = eval_files.Header.W_HOMOGENEITY


HEADER_TYPES = {
    Header.SAMPLE_ID: str,
    Header.TOOL_CODE: str,
    Header.UNW_COMPLETENESS: float,
    Header.UNW_HOMOGENEITY: float,
    Header.W_COMPLETENESS: float,
    Header.W_HOMOGENEITY: float,
}


def to_dataframe(path: Path) -> pd.DataFrame:
    """Convert a file to a pandas DataFrame."""
    return pd.read_csv(path, sep="\t")


def new_dataframe() -> pd.DataFrame:
    """Create an empty DataFrame."""
    return pd.DataFrame(columns=list(HEADER_TYPES.keys()))
