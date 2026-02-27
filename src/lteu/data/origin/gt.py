"""Original ground truth Excel sheet."""

from enum import StrEnum

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
