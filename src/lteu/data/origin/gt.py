"""Original ground truth Excel sheet."""

from enum import StrEnum
from pathlib import Path

import pandas as pd

SHEET_NAME = "Ground-truth"


class Header(StrEnum):
    """Ground truth headers."""

    SAMPLE_ID = "Sample ID"
    SR_CTG_ID = "SR contig ID"
    TAXON = "Taxon"
    GT_CLASS = "Ground-truth class"
    HYBRID_CTG_ID = "Hybrid contig ID"
    HAS_COMPLETE_HYBRID_ASM = "Has complete hybrid assembly?"
    SR_CTG_HAS_ARGS = "SR contig has ARGs"
    SR_CTG_LEN = "SR contig length"


HEADER_TYPES = {
    Header.SAMPLE_ID: str,
    Header.SR_CTG_ID: str,
    Header.TAXON: str,
    Header.GT_CLASS: str,
    Header.HYBRID_CTG_ID: str,
    Header.HAS_COMPLETE_HYBRID_ASM: bool,
    Header.SR_CTG_HAS_ARGS: bool,
    Header.SR_CTG_LEN: int,
}


def to_dataframe(xlsx_path: Path) -> pd.DataFrame:
    """Load the ground truth Excel sheet."""
    return pd.read_excel(xlsx_path, sheet_name=SHEET_NAME, dtype=HEADER_TYPES)
