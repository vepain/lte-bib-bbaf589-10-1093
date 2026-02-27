"""Evaluation module."""

import pandas as pd


def homogeneity(
    ground_truth: pd.DataFrame,
    predictions: pd.DataFrame,
    weight: bool,  # noqa: FBT001
) -> float:
    """Compute the homogeneity.

    Arguments
    ---------
    ground_truth: pd.DataFrame
        The ground truth (PlasEval format).
    predictions: pd.DataFrame
        The predictions (PlasEval format).
    weight: bool
        Consider using the contig length as a weight or not.
    """
    raise NotImplementedError


def completeness(
    ground_truth: pd.DataFrame,
    predictions: pd.DataFrame,
    weight: bool,  # noqa: FBT001
) -> float:
    """Compute the completeness.

    Arguments
    ---------
    ground_truth: pd.DataFrame
        The ground truth (PlasEval format).
    predictions: pd.DataFrame
        The predictions (PlasEval format).
    weight: bool
        Consider using the contig length as a weight or not.
    """
    raise NotImplementedError
