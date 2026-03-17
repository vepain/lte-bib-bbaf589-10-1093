"""Original predictions results."""

from enum import StrEnum
from pathlib import Path

import pandas as pd

from lteu import tools

SHEET_NAME = "Plasmid Reconstruction"


class Header(StrEnum):
    """Plasmid reconstruction headers."""

    SAMPLE_ID = "Sample ID"
    SR_CTG_ID = "SR contig ID"
    HYASP = "HyAsP"
    MOB = "MOB-suite"
    PLASBIN_FLOW = "PlasBin-Flow"
    GPLAS_TWO = "gplas2"


def binning_tool_to_header(binning_tool: tools.Binning) -> Header:
    """Convert binning tool to header."""
    match binning_tool:
        case tools.Binning.HYASP:
            return Header.HYASP
        case tools.Binning.MOB:
            return Header.MOB
        case tools.Binning.PLASBIN_FLOW:
            return Header.PLASBIN_FLOW
        case tools.Binning.GPLAS_TWO:
            return Header.GPLAS_TWO


HEADER_TYPES = {
    Header.SAMPLE_ID: str,
    Header.SR_CTG_ID: str,
    Header.HYASP: str,
    Header.MOB: str,
    Header.PLASBIN_FLOW: str,
    Header.GPLAS_TWO: str,
}


def to_dataframe(xlsx_path: Path) -> pd.DataFrame:
    """Load the plasmid reconstruction Excel sheet."""
    return pd.read_excel(xlsx_path, sheet_name=SHEET_NAME)
