"""Evaluation application."""

from pathlib import Path
from typing import Annotated

import typer

from lteu import log
from lteu.data.plaseval import bins as pe_bins
from lteu.samples import files as smp_files

from . import files, main

APP = typer.Typer()


class Inputs:
    """Inputs for run command."""

    PREDICTIONS_DIR = typer.Argument(
        help="Path to the predictions directory.",
    )
    GROUND_TRUTH_DIR = typer.Argument(
        help="Path to the ground truth directory.",
    )

    SAMPLES_TSV = typer.Argument(
        help="Path to the samples TSV file.",
    )

    EVAL_TSV = typer.Argument(
        help="Path to the evaluation TSV file.",
    )


@APP.command("run")
def evaluate(
    preds_dir: Annotated[Path, Inputs.PREDICTIONS_DIR],
    gt_dir: Annotated[Path, Inputs.GROUND_TRUTH_DIR],
    samples_tsv: Annotated[Path, Inputs.SAMPLES_TSV],
    eval_tsv: Annotated[Path, Inputs.EVAL_TSV],
) -> None:
    """Compute the completeness and homogeneity."""
    log.print_title("Compute the completeness and homogeneity")

    log.print_inputs(
        (
            f"Predictions directory: {log.fmt_dir(preds_dir)}",
            f"Ground truth directory: {log.fmt_dir(gt_dir)}",
            f"Samples TSV file: {log.fmt_file(samples_tsv)}",
            f"Evaluation TSV file: {log.fmt_file(eval_tsv)}",
        ),
    )

    smp_df = smp_files.to_dataframe(samples_tsv)
    eval_df = files.new_dataframe()

    nb_no_eval = 0

    for smp_id in smp_df[smp_files.Header.SAMPLE_ID]:
        pred_file = preds_dir / pe_bins.fname(smp_id)
        gt_file = gt_dir / pe_bins.fname(smp_id)

        if not pred_file.exists() or not gt_file.exists():
            nb_no_eval += 1
            # Add a row with Nan for the two columns
            eval_df.loc[len(eval_df)] = {
                files.Header.SAMPLE_ID: smp_id,
                files.Header.UNW_COMPLETENESS: None,
                files.Header.UNW_HOMOGENEITY: None,
                files.Header.W_COMPLETENESS: None,
                files.Header.W_HOMOGENEITY: None,
            }
            continue

        pred_df = pe_bins.to_dataframe(preds_dir / pe_bins.fname(smp_id))
        gt_df = pe_bins.to_dataframe(gt_dir / pe_bins.fname(smp_id))

        unw_completeness = main.completeness(pred_df, gt_df, weight=False)
        unw_homogeneity = main.homogeneity(pred_df, gt_df, weight=False)

        w_completeness = main.completeness(pred_df, gt_df, weight=True)
        w_homogeneity = main.homogeneity(pred_df, gt_df, weight=True)

        eval_df.loc[len(eval_df)] = {
            files.Header.SAMPLE_ID: smp_id,
            files.Header.UNW_COMPLETENESS: unw_completeness,
            files.Header.UNW_HOMOGENEITY: unw_homogeneity,
            files.Header.W_COMPLETENESS: w_completeness,
            files.Header.W_HOMOGENEITY: w_homogeneity,
        }

    if nb_no_eval:
        log.print_warning(f"{nb_no_eval} samples on {len(smp_df)} have no evaluation")

    eval_tsv.parent.mkdir(parents=True, exist_ok=True)
    eval_df.to_csv(eval_tsv, sep="\t", index=False)

    log.print_done(f"Created {log.fmt_file(eval_tsv)} file")
