"""Operation application."""

from pathlib import Path
from typing import Annotated

import typer

from lteu import log
from lteu.data import samples as smp
from lteu.data.plaseval import bins as pe_bins

from . import files, main

APP = typer.Typer(help="Uniqify commands.")


class Args:
    """Arguments."""

    PREDICTIONS_DIR = typer.Argument(
        help="Path to the predictions directory.",
    )
    GROUND_TRUTH_DIR = typer.Argument(
        help="Path to the ground truth directory.",
    )

    SAMPLES_TSV = typer.Argument(
        help="Path to the samples TSV file.",
    )

    OUTPUT_DIR = typer.Argument(
        help=(
            "Path to the output directory."
            " Parent of the new predictions and ground truth directories."
        ),
    )


@APP.command("uniqify")
def distinguish_repeats(
    preds_dir: Annotated[Path, Args.PREDICTIONS_DIR],
    gt_dir: Annotated[Path, Args.GROUND_TRUTH_DIR],
    samples_tsv: Annotated[Path, Args.SAMPLES_TSV],
    output_dir: Annotated[Path, Args.OUTPUT_DIR],
) -> None:
    """Distinguish the repeats in the bins for a list of samples."""
    log.print_title("Distinguish the repeats in the bins for a list of samples")

    log.print_inputs(
        (
            f"Predictions directory: {log.fmt_dir(preds_dir)}",
            f"Ground truth directory: {log.fmt_dir(gt_dir)}",
            f"Samples TSV file: {log.fmt_file(samples_tsv)}",
            f"Output directory: {log.fmt_dir(output_dir)}",
        ),
    )

    smp_df = smp.to_dataframe(samples_tsv)

    out_preds_dir = output_dir / "predictions"
    out_gt_dir = output_dir / "ground_truths"

    out_preds_dir.mkdir(parents=True, exist_ok=True)
    out_gt_dir.mkdir(parents=True, exist_ok=True)

    nb_matches_df = files.new_dataframe()

    nb_no_eval = 0

    for smp_id in smp_df[smp.Header.SAMPLE_ID]:
        pred_file = preds_dir / pe_bins.fname(smp_id)
        gt_file = gt_dir / pe_bins.fname(smp_id)

        if not pred_file.exists() or not gt_file.exists():
            nb_no_eval += 1
            nb_matches_df.loc[len(nb_matches_df)] = {
                files.Header.SAMPLE_ID: smp_id,
                files.Header.NB_MATCHES: None,
            }
            continue

        pred_df = pe_bins.to_dataframe(preds_dir / pe_bins.fname(smp_id))
        gt_df = pe_bins.to_dataframe(gt_dir / pe_bins.fname(smp_id))

        gt_df, pred_df, nb_match = main.unify_repeats(gt_df, pred_df)

        nb_matches_df.loc[len(nb_matches_df)] = {
            files.Header.SAMPLE_ID: smp_id,
            files.Header.NB_MATCHES: nb_match,
        }

        pe_bins.to_file(pred_df, out_preds_dir / pe_bins.fname(smp_id))
        pe_bins.to_file(gt_df, out_gt_dir / pe_bins.fname(smp_id))

    if nb_no_eval:
        log.print_warning(f"{nb_no_eval} samples on {len(smp_df)} have no evaluation")

    files.to_file(nb_matches_df, output_dir / files.fname())
    log.print_done(f"Created {log.fmt_file(output_dir / files.fname())} file")

    log.print_done(f"Created {log.fmt_dir(out_preds_dir)} directory")
    log.print_done(f"Created {log.fmt_dir(out_gt_dir)} directory")
