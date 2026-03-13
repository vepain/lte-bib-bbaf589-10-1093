"""PlasEval plasmid bins files."""

from enum import StrEnum
from pathlib import Path

import pandas as pd


class Header(StrEnum):
    """Plasmid bins header."""

    PLASMID = "plasmid"
    CONTIG = "contig"
    CTG_LEN = "contig_len"


HEADER_TYPES = {
    Header.PLASMID: str,
    Header.CONTIG: str,
    Header.CTG_LEN: int,
}


def to_dataframe(tsv_path: Path) -> pd.DataFrame:
    """Load the plasmid bins TSV file."""
    return pd.read_csv(tsv_path, dtype=HEADER_TYPES, sep="\t")


def fname(sample_id: str) -> str:
    """Generate a filename from a sample ID."""
    return f"{sample_id}.tsv"


def to_file(df: pd.DataFrame, tsv_path: Path) -> None:
    """Save the plasmid bins TSV file."""
    df.to_csv(tsv_path, sep="\t", index=False)
