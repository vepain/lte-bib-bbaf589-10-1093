"""Evaluation module."""

import numpy as np
import pandas as pd

from lteu.data.plaseval import bins as pe_bins


def get_unweighted_contingency_table(
    ground_truth: pd.DataFrame,
    predictions: pd.DataFrame,
) -> pd.DataFrame:
    """Obtain the unweighted contingency table.

    Arguments
    ---------
    ground_truth: pd.DataFrame
        The ground truth (plasEval format).
    predictions: pd.DataFrame
        The predictions (plasEval format).
    """
    # Rename columns to differentiate betweens ground truth and prediction set ids
    ground_truth = ground_truth.rename(columns={pe_bins.Header.PLASMID: "K"})
    predictions = predictions.rename(columns={pe_bins.Header.PLASMID: "C"})

    # Merge on contig (outer=union, inner=intersection)
    merge_df = ground_truth[["K", pe_bins.Header.CONTIG]].merge(
        predictions[["C", pe_bins.Header.CONTIG]],
        on=pe_bins.Header.CONTIG,
        how="outer",
        suffixes=("_true", "_pred"),
    )

    # Assign each contig weight 1
    merge_df["weight"] = 1

    # Build unweighted contingency table
    return merge_df.pivot_table(
        index="C",
        columns="K",
        values="weight",
        aggfunc="sum",
    ).fillna(0)


def get_weighted_contingency_table(
    ground_truth: pd.DataFrame,
    predictions: pd.DataFrame,
) -> pd.DataFrame:
    """Obtain the weighted contingency table.

    Arguments
    ---------
    ground_truth: pd.DataFrame
        The ground truth (plasEval format).
    predictions: pd.DataFrame
        The predictions (plasEval format).
    """
    # Rename columns to differentiate betweens ground truth and prediction set ids
    ground_truth = ground_truth.rename(columns={pe_bins.Header.PLASMID: "K"})
    predictions = predictions.rename(columns={pe_bins.Header.PLASMID: "C"})

    # Merge on contig (outer=union, inner=intersection)
    merge_df = ground_truth[["K", pe_bins.Header.CONTIG, pe_bins.Header.CTG_LEN]].merge(
        predictions[["C", pe_bins.Header.CONTIG]],
        on=pe_bins.Header.CONTIG,
        how="outer",
        suffixes=("_true", "_pred"),
    )

    # Build weighted contingency table
    return merge_df.pivot_table(
        index="C",
        columns="K",
        values=pe_bins.Header.CTG_LEN,
        aggfunc="sum",
    ).fillna(0)


def get_prob_matrix(contingency_tab: pd.DataFrame) -> np.ndarray:
    """Obtain the unweighted contingency table.

    Arguments
    ---------
    contingency_tab: pd.DataFrame
    """
    # Convert to probabilities
    contingency_mat = contingency_tab.to_numpy(dtype=float)
    total = contingency_mat.sum()
    return contingency_mat / total


def homogeneity(
    ground_truth: pd.DataFrame,
    predictions: pd.DataFrame,
    weight: bool,  # noqa: FBT001
) -> float:
    """Compute the homogeneity.

    Arguments
    ---------
    ground_truth: pd.DataFrame
        The ground truth (plasEval format).
    predictions: pd.DataFrame
        The predictions (plasEval format).
    weight: bool
        Consider using the contig length as a weight or not.
    """
    if weight:
        contingency_tab = get_weighted_contingency_table(ground_truth, predictions)
    else:
        contingency_tab = get_unweighted_contingency_table(ground_truth, predictions)
    prob_matrix = get_prob_matrix(contingency_tab)

    # Marginal probabilities
    p_k = prob_matrix.sum(axis=0, keepdims=True)  # sum over C (columns)

    # Joint entropy H(C,K)
    mask = prob_matrix > 0
    h_ck = -np.sum(prob_matrix[mask] * np.log2(prob_matrix[mask]))

    # Entropy H(K)
    mask_k = p_k > 0
    h_k = -np.sum(p_k[mask_k] * np.log2(p_k[mask_k]))

    # Conditional entropy H(C|K)
    h_c_given_k = h_ck - h_k

    # Homogeneity
    if h_ck == 0:
        return 0.0
    return 1 - h_c_given_k / h_ck


def completeness(
    ground_truth: pd.DataFrame,
    predictions: pd.DataFrame,
    weight: bool,  # noqa: FBT001
) -> float:
    """Compute the completeness.

    Arguments
    ---------
    ground_truth: pd.DataFrame
        The ground truth (plasEval format).
    predictions: pd.DataFrame
        The predictions (plasEval format).
    weight: bool
        Consider using the contig length as a weight or not.
    """
    if weight:
        contingency_tab = get_weighted_contingency_table(ground_truth, predictions)
    else:
        contingency_tab = get_unweighted_contingency_table(ground_truth, predictions)
    prob_matrix = get_prob_matrix(contingency_tab)

    # Marginal probabilities
    p_c = prob_matrix.sum(axis=1, keepdims=True)  # sum over K (rows)

    # Joint entropy H(K,C)
    mask = prob_matrix > 0
    h_kc = -np.sum(prob_matrix[mask] * np.log2(prob_matrix[mask]))

    # Entropy H(C)
    mask_c = p_c > 0
    h_c = -np.sum(p_c[mask_c] * np.log2(p_c[mask_c]))

    # Conditional entropy H(K|C)
    h_k_given_c = h_kc - h_c

    # Completeness
    if h_kc == 0:
        return 0.0
    return 1 - h_k_given_c / h_kc
