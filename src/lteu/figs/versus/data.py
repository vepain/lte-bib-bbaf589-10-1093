"""Data operations for versus figures."""

from enum import StrEnum

import pandas as pd


class Versions(StrEnum):
    """Versions."""

    V1 = "v1"
    V2 = "v2"


def merge_versions(
    v1_df: pd.DataFrame,
    v2_df: pd.DataFrame,
    version_col: str,
) -> pd.DataFrame:
    """Merge the TSV files from different versions."""
    v1_df[version_col] = Versions.V1
    v2_df[version_col] = Versions.V2
    return pd.concat([v1_df, v2_df])


class Class(StrEnum):
    """Class values."""

    ABOVE = "Above"
    EQUAL = "Equal"
    BELOW = "Below"


def add_class_column(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    class_col: str,
) -> pd.DataFrame:
    """Add a class column to a dataframe."""

    # class column is either Below, Equal or Above the diagonal
    def _class_value(row: pd.Series) -> str:
        if row[x_col] > row[y_col]:
            return Class.BELOW
        if row[x_col] < row[y_col]:
            return Class.ABOVE
        return Class.EQUAL

    df[class_col] = df.apply(_class_value, axis=1)

    return df
