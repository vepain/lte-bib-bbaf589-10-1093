"""Common figures data."""

from enum import StrEnum
from typing import assert_never

import pandas as pd
import typer


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
