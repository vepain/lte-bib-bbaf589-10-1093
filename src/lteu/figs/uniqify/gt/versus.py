"""Versus figures for uniqify ground truths."""

from pathlib import Path

import pandas as pd

from lteu.eval.run import files as eval_files
from lteu.figs import items, ops
from lteu.figs.versus import main as vs_main


def get_dataframe(
    x_evals_tsv: Path,
    y_evals_tsv: Path,
    measure: items.MeasureCodes,
) -> pd.DataFrame:
    """Get the dataframe for a versus figure for ground truths."""
    x_df = eval_files.to_dataframe(x_evals_tsv)
    y_df = eval_files.to_dataframe(y_evals_tsv)
    df = ops.merge_versions(x_df, y_df)

    df = ops.remove_samples_with_nan(df)

    df = pd.pivot_table(
        df,
        index=items.Header.SAMPLE_ID,
        columns=items.Header.VERSION,
        values=measure.to_column(),
    )

    return vs_main.add_class_column(df, items.Versions.V1, items.Versions.V2)
