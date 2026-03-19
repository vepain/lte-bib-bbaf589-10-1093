"""Commons for distribution figures."""

from enum import StrEnum

import pandas as pd

from lteu.eval import measures


class Contents(StrEnum):
    """Contents."""

    ONLY_PLASMIDS = "only_plasmids"
    WITH_CHROMOSOMES = "with_chromosomes"

    def to_label(self) -> str:
        """Get the corresponding label."""
        match self:
            case Contents.ONLY_PLASMIDS:
                return "Only plasmids"
            case Contents.WITH_CHROMOSOMES:
                return "With chromosomes"


def replace_measures_cols_to_class_mode_val_cols(
    df: pd.DataFrame,
    unchanged_cols: list[str],
    measure_class_col: str,
    measure_mode_col: str,
    measure_val_col: str,
) -> pd.DataFrame:
    """Replace the measures columns by class, mode and value columns."""
    df = df.melt(
        id_vars=unchanged_cols,
        value_vars=list(measures.Items),
        var_name="tmp_var",
        value_name=measure_val_col,
    )

    def replace_measure_col_to_class_and_mode_cols(
        df: pd.DataFrame,
        measure_col: str,
        measure_class_col: str,
        measure_mode_col: str,
    ) -> pd.DataFrame:
        """Replace the measure column to measure class and mode columns."""
        df[measure_class_col] = df[measure_col].apply(
            measures.Items.to_class,
        )
        df[measure_mode_col] = df[measure_col].apply(
            measures.Items.to_mode,
        )
        return df.drop(columns=[measure_col])

    # Create two columns according to the value in tmp_var column
    return replace_measure_col_to_class_and_mode_cols(
        df,
        "tmp_var",
        measure_class_col,
        measure_mode_col,
    )
