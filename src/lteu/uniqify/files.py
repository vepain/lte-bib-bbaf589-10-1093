"""Uniqify operation files."""

from enum import StrEnum
from pathlib import Path

import pandas as pd


class Header(StrEnum):
    """Header names."""

    SAMPLE_ID = "sample_id"
    NB_MATCHES = "nb_matches"


HEADER_TYPES = {
    Header.SAMPLE_ID: str,
    Header.NB_MATCHES: int,
}


def new_dataframe() -> pd.DataFrame:
    """Create a new dataframe."""
    return pd.DataFrame(columns=list(HEADER_TYPES.keys()))


def to_dataframe(path: Path) -> pd.DataFrame:
    """Convert a file to a pandas DataFrame."""
    return pd.read_csv(path, sep="\t", dtype=HEADER_TYPES)  # ty:ignore[invalid-argument-type]


def fname() -> str:
    """Generate a filename from a sample ID."""
    return "nb_matches.tsv"


def to_file(df: pd.DataFrame, path: Path) -> None:
    """Save a pandas DataFrame to a file."""
    df.to_csv(path, sep="\t", index=False)
