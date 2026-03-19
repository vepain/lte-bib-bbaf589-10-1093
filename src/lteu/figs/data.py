"""Common figures data."""

from enum import StrEnum
from typing import Literal, assert_never

import pandas as pd
import typer

from lteu.eval.run import files as eval_files


class AppInputs:
    """Operations applications inputs."""

    REMOVE_SAMPLES = typer.Option(
        "--remove-samples",
        "-r",
        help="Mode to remove samples from the dataset",
    )


class RmSamplesModes(StrEnum):
    """Modes for removing samples."""

    FAILS = "fails"
    NOTHING = "nothing"


def remove_samples_with_nan(df: pd.DataFrame, sample_id_col: str) -> pd.DataFrame:
    """Remove rows where samples has a NaN anywhere."""
    df_nan = df[df.isna().any(axis=1)]
    smp_ids = df_nan[sample_id_col].tolist()
    return df[~df[sample_id_col].isin(smp_ids)]


def do_remove_samples_strategy(
    df: pd.DataFrame,
    mode: RmSamplesModes,
    sample_id_col: str,
) -> pd.DataFrame:
    """Do the remove samples strategy."""
    match mode:
        case RmSamplesModes.FAILS:
            return remove_samples_with_nan(df, sample_id_col)
        case RmSamplesModes.NOTHING:
            return df[~df.isna().any(axis=1)]
        case _:
            assert_never(mode)


class MeasureCodes(StrEnum):
    """Measure codes base class."""

    UNW_COMPLETENESS = "unw_comp"
    UNW_HOMOGENEITY = "unw_hom"
    W_COMPLETENESS = "w_comp"
    W_HOMOGENEITY = "w_hom"

    def to_column(self) -> str:
        """Get the corresponding column."""
        match self:
            case MeasureCodes.UNW_COMPLETENESS:
                return eval_files.Header.UNW_COMPLETENESS
            case MeasureCodes.UNW_HOMOGENEITY:
                return eval_files.Header.UNW_HOMOGENEITY
            case MeasureCodes.W_COMPLETENESS:
                return eval_files.Header.W_COMPLETENESS
            case MeasureCodes.W_HOMOGENEITY:
                return eval_files.Header.W_HOMOGENEITY

    def to_label(self, mode: Literal["single", "plural"] = "single") -> str:
        """Get the corresponding label."""
        match self:
            case MeasureCodes.UNW_COMPLETENESS:
                return (
                    "Unweighted completeness"
                    if mode == "single"
                    else "Unweighted completenesses"
                )
            case MeasureCodes.UNW_HOMOGENEITY:
                return (
                    "Unweighted homogeneity"
                    if mode == "single"
                    else "Unweighted homogeneities"
                )
            case MeasureCodes.W_COMPLETENESS:
                return (
                    "Weighted completeness"
                    if mode == "single"
                    else "Weighted completenesses"
                )
            case MeasureCodes.W_HOMOGENEITY:
                return (
                    "Weighted homogeneity"
                    if mode == "single"
                    else "Weighted homogeneities"
                )
