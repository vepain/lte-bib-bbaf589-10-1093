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
    return pd.read_csv(tsv_path, dtype=HEADER_TYPES, sep="\t")
