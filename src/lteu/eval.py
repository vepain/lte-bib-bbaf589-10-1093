"""Evaluation module."""

import numpy as np
import pandas as pd


def get_unweighted_contingency_table(
    ground_truth: pd.DataFrame,
    predictions: pd.DataFrame,
):
    """Obtain the unweighted contingency table.

    Arguments
    ---------
    ground_truth: pd.DataFrame
        The ground truth (PlasEval format).
    predictions: pd.DataFrame
        The predictions (PlasEval format).
    """
    # Rename columns to differentiate betweens ground truth and prediction set ids
    ground_truth = ground_truth.rename(columns={"plasmid": "K"})
    predictions = predictions.rename(columns={"plasmid": "C"})

    # Merge on contig (contigs unique to only one set of bins will be removed in this step)
    merge_df = ground_truth[["K", "contig"]].merge(
        predictions[["C", "contig"]],
        on="contig",
        how="outer",
    )

    # Assign each contig weight 1
    merge_df["weight"] = 1

    # Build unweighted contingency table
    contingency_tab = merge_df.pivot_table(
        index="C",
        columns="K",
        values="weight",
        aggfunc="sum",
    ).fillna(0)
    print(contingency_tab)
    return contingency_tab


def get_weighted_contingency_table(
    ground_truth: pd.DataFrame,
    predictions: pd.DataFrame,
):
    """Obtain the weighted contingency table.

    Arguments
    ---------
    ground_truth: pd.DataFrame
        The ground truth (PlasEval format).
    predictions: pd.DataFrame
        The predictions (PlasEval format).
    """
    # Rename columns to differentiate betweens ground truth and prediction set ids
    ground_truth = ground_truth.rename(columns={"plasmid": "K"})
    predictions = predictions.rename(columns={"plasmid": "C"})

    # Merge on contig (contigs unique to only one set of bins will be removed in this step)
    merge_df = ground_truth[["K", "contig", "contig_len"]].merge(
        predictions[["C", "contig"]],
        on="contig",
        how="outer",
    )

    # Build weighted contingency table
    contingency_tab = merge_df.pivot_table(
        index="C",
        columns="K",
        values="contig_len",
        aggfunc="sum",
    ).fillna(0)
    print(contingency_tab)
    return contingency_tab


def get_prob_matrix(contingency_tab):
    """Obtain the unweighted contingency table.

    Arguments
    ---------
    contingency_tab: pd.DataFrame
    """
    # Convert to probabilities
    contingency_mat = contingency_tab.to_numpy(dtype=float)
    total = contingency_mat.sum()
    P = contingency_mat / total
    return P


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
    if weight:
        print("Here")
        contingency_tab = get_weighted_contingency_table(ground_truth, predictions)
    else:
        print("No, no, here")
        contingency_tab = get_unweighted_contingency_table(ground_truth, predictions)
    P = get_prob_matrix(contingency_tab)

    # Marginal probabilities
    P_C = P.sum(axis=1, keepdims=True)  # sum over K (rows)
    P_K = P.sum(axis=0, keepdims=True)  # sum over C (columns)

    # Joint entropy H(C,K)
    mask = P > 0
    H_CK = -np.sum(P[mask] * np.log2(P[mask]))

    # Entropy H(K)
    maskK = P_K > 0
    H_K = -np.sum(P_K[maskK] * np.log2(P_K[maskK]))

    # Conditional entropy H(C|K)
    H_C_given_K = H_CK - H_K

    # Homogeneity
    if H_CK == 0:
        return 0.0
    return 1 - H_C_given_K / H_CK


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
    if weight:
        contingency_tab = get_weighted_contingency_table(ground_truth, predictions)
    else:
        contingency_tab = get_unweighted_contingency_table(ground_truth, predictions)
    P = get_prob_matrix(contingency_tab)

    # Marginal probabilities
    P_K = P.sum(axis=0, keepdims=True)  # sum over C (columns)
    P_C = P.sum(axis=1, keepdims=True)  # sum over K (rows)

    # Joint entropy H(K,C)
    mask = P > 0
    H_KC = -np.sum(P[mask] * np.log2(P[mask]))

    # Entropy H(C)
    maskC = P_C > 0
    H_C = -np.sum(P_C[maskC] * np.log2(P_C[maskC]))

    # Conditional entropy H(K|C)
    H_K_given_C = H_KC - H_C

    # Completeness
    if H_KC == 0:
        return 0.0
    return 1 - H_K_given_C / H_KC
