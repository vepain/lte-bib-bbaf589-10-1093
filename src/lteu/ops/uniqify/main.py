"""Operations module."""

import pandas as pd

from lteu.data.plaseval import bins as pe_bins


def unify_repeats(
    ground_truth: pd.DataFrame,
    predictions: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, int]:
    """Unify the repeats in the perfect matching case.

    When one predicted bin equals one ground truth bin,
    their contigs are renamed such that they do not appear in other bins.

    Arguments
    ---------
    ground_truth: pd.DataFrame
        The ground truth (plasEval format).
    predictions: pd.DataFrame
        The predictions (plasEval format).

    Returns
    -------
    ground_truth: pd.DataFrame
        The new ground truth (plasEval format).
    predictions: pd.DataFrame
        The new predictions (plasEval format).
    nb_matchs: int
        The number of perfect matches.
    """
    pred_bin_names: set[str] = set(predictions[pe_bins.Header.PLASMID].unique())
    gt_bin_names: set[str] = set(ground_truth[pe_bins.Header.PLASMID].unique())

    nb_matchs = 0

    pred_bin_names_iter = iter(pred_bin_names)
    pred_bin_id = next(pred_bin_names_iter, None)

    while pred_bin_id is not None and gt_bin_names:
        pred_ctgs = set(
            predictions[predictions[pe_bins.Header.PLASMID] == pred_bin_id][
                pe_bins.Header.CONTIG
            ],
        )

        found_match = False

        gt_bin_names_iter = iter(gt_bin_names)
        gt_bin_id = next(gt_bin_names_iter)

        while not found_match and gt_bin_id is not None:
            gt_ctgs = set(
                ground_truth[ground_truth[pe_bins.Header.PLASMID] == gt_bin_id][
                    pe_bins.Header.CONTIG
                ],
            )
            if pred_ctgs == gt_ctgs:
                found_match = True

                # Rename contigs of predicted bin
                predictions.loc[
                    predictions[pe_bins.Header.PLASMID] == pred_bin_id,
                    pe_bins.Header.CONTIG,
                ] += f"_{nb_matchs}"

                # Rename contigs of ground truth bin
                ground_truth.loc[
                    ground_truth[pe_bins.Header.PLASMID] == gt_bin_id,
                    pe_bins.Header.CONTIG,
                ] += f"_{nb_matchs}"

                gt_bin_names.remove(gt_bin_id)

                nb_matchs += 1
            else:
                gt_bin_id = next(gt_bin_names_iter, None)

        pred_bin_id = next(pred_bin_names_iter, None)

    return ground_truth, predictions, nb_matchs
