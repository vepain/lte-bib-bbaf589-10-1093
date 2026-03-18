"""Common operations."""

from enum import StrEnum
from pathlib import Path
from typing import Literal, assert_never

import pandas as pd
import typer

from lteu import tools
from lteu.eval.merge import files as merge_files

from . import items


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


def get_tools_evals(
    v1_merge_tool_evals_tsv: Path,
    v2_merge_tool_evals_tsv: Path,
    methods: list[tools.Binning],
    remove_samples: RmSamplesModes,
    purpose: Literal["figures", "stats"],
) -> pd.DataFrame:
    """Read the TSV file and filter it."""
    v1_df = merge_files.to_dataframe(v1_merge_tool_evals_tsv)
    v2_df = merge_files.to_dataframe(v2_merge_tool_evals_tsv)
    df = merge_versions(v1_df, v2_df)
    df = _keep_only_methods(df, methods)

    match remove_samples:
        case RmSamplesModes.FAILS:
            df = remove_samples_with_nan(df)
        case RmSamplesModes.NOTHING:
            pass
        case _:
            assert_never(remove_samples)

    match purpose:
        case "stats":
            set_method_order(df, methods)
        case "figures":
            pass  # XXX Can't configurate Categorical columns for seaborn
            # seaborn violin plots have weird shapes otherwise...
        case _:
            assert_never(purpose)

    return df


def merge_versions(
    v1_df: pd.DataFrame,
    v2_df: pd.DataFrame,
) -> pd.DataFrame:
    """Merge the TSV files from different versions."""
    v1_df[items.Header.VERSION] = items.Versions.V1
    v2_df[items.Header.VERSION] = items.Versions.V2
    return pd.concat([v1_df, v2_df])


def _keep_only_methods(
    df: pd.DataFrame,
    methods: list[tools.Binning],
) -> pd.DataFrame:
    """Keep only the specified methods."""
    return df[df[merge_files.Header.TOOL_CODE].isin(set(methods))]


def remove_samples_with_nan(df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows where samples has a NaN anywhere."""
    df_nan = df[df.isna().any(axis=1)]
    smp_ids = df_nan[merge_files.Header.SAMPLE_ID].tolist()
    return df[~df[merge_files.Header.SAMPLE_ID].isin(smp_ids)]


def _order_methods(df: pd.DataFrame, methods: list[tools.Binning]) -> pd.DataFrame:
    """Order the methods."""
    return df.sort_values(
        by=[merge_files.Header.TOOL_CODE],
        key=lambda x: [methods.index(m) for m in x],
    )


def set_method_order(df: pd.DataFrame, methods: list[tools.Binning]) -> None:
    """Set method order rule according to the user custom order."""
    df[merge_files.Header.TOOL_CODE] = pd.Categorical(
        df[merge_files.Header.TOOL_CODE],
        categories=methods,
        ordered=True,
    )


def add_column_eval_exists(df: pd.DataFrame) -> None:
    """Add a column indicating if the binning results exist."""
    df[items.Presence.column_name()] = (
        df.isna()
        .any(axis=1)
        .map(
            lambda x: items.Presence.NO if x else items.Presence.YES,
        )
    )
