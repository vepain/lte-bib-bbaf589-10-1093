"""Evaluation module."""

import pandas as pd


def v_measure(ground_truth: pd.DataFrame, predictions: pd.DataFrame) -> float:
    """Compute the V-measure.

    Arguments
    ---------
    ground_truth: pd.DataFrame
        The ground truth (PlasEval format).
    predictions: pd.DataFrame
        The predictions (PlasEval format).
    """
    raise NotImplementedError


def weighted_v_measure(ground_truth: pd.DataFrame, predictions: pd.DataFrame) -> float:
    """Compute the weighted V-measure.

    Arguments
    ---------
    ground_truth: pd.DataFrame
        The ground truth (PlasEval format).
    predictions: pd.DataFrame
        The predictions (PlasEval format).
    """
    raise NotImplementedError
