"""Samples files."""

from enum import StrEnum
from pathlib import Path

import pandas as pd


class Header(StrEnum):
    """Samples TSV header."""

    SAMPLE_ID = "Sample ID"


HEADER_TYPES = {
    Header.SAMPLE_ID: str,
}


def to_dataframe(tsv_path: Path) -> pd.DataFrame:
    """Load the samples TSV file."""
    return pd.read_csv(tsv_path, sep="\t")


def new_dataframe() -> pd.DataFrame:
    """Create a new dataframe."""
    return pd.DataFrame(columns=list(HEADER_TYPES.keys()))


def to_file(df: pd.DataFrame, tsv_path: Path) -> None:
    """Save the samples TSV file."""
    df.to_csv(tsv_path, sep="\t", index=False)
