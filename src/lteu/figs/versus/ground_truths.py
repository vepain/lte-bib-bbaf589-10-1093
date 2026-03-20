"""Versus figures for uniqify ground truths."""

from enum import StrEnum
from pathlib import Path

import pandas as pd

from lteu.eval import measures
from lteu.eval.run import files as eval_files
from lteu.figs import data as figs_data
from lteu.figs.versus import data as vs_data


class Columns(StrEnum):
    """Columns."""

    SAMPLE_ID = eval_files.Header.SAMPLE_ID
    CLASS = "Class"
    VERSION = "version"
    UNW_COMPLETENESS = eval_files.Header.UNW_COMPLETENESS
    UNW_HOMOGENEITY = eval_files.Header.UNW_HOMOGENEITY
    W_COMPLETENESS = eval_files.Header.W_COMPLETENESS
    W_HOMOGENEITY = eval_files.Header.W_HOMOGENEITY


def get_dataframe(
    x_evals_tsv: Path,
    y_evals_tsv: Path,
    measure: measures.Items,
) -> pd.DataFrame:
    """Get the dataframe for a versus figure for ground truths."""
    x_df = eval_files.to_dataframe(x_evals_tsv)
    y_df = eval_files.to_dataframe(y_evals_tsv)
    df = vs_data.merge_versions(x_df, y_df, Columns.VERSION)

    df = figs_data.remove_samples_with_nan(df, Columns.SAMPLE_ID)

    df = pd.pivot_table(
        df,
        index=Columns.SAMPLE_ID,
        columns=Columns.VERSION,
        values=eval_files.Header.from_measure(measure),
    )

    return vs_data.add_class_column(
        df,
        vs_data.Versions.V1,
        vs_data.Versions.V2,
        Columns.CLASS,
    )
