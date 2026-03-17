"""Operation application."""

from pathlib import Path
from typing import Annotated

import typer

from lteu import log
from lteu.data.plaseval import bins as pe_bins
from lteu.samples import files as smp_files

from . import files, main

APP = typer.Typer(name="uniqify", help="Uniqify commands.")


class ToolInputs:
    """Inputs for tool command."""

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


@APP.command("tool")
def distinguish_repeats(
    preds_dir: Annotated[Path, ToolInputs.PREDICTIONS_DIR],
    gt_dir: Annotated[Path, ToolInputs.GROUND_TRUTH_DIR],
    samples_tsv: Annotated[Path, ToolInputs.SAMPLES_TSV],
    output_dir: Annotated[Path, ToolInputs.OUTPUT_DIR],
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

    smp_df = smp_files.to_dataframe(samples_tsv)

    out_preds_dir = output_dir / "binning"
    out_gt_dir = output_dir / "ground_truths"

    out_preds_dir.mkdir(parents=True, exist_ok=True)
    out_gt_dir.mkdir(parents=True, exist_ok=True)

    nb_matches_df = files.new_dataframe()

    nb_no_eval = 0

    for smp_id in smp_df[smp_files.Header.SAMPLE_ID]:
        pred_file = preds_dir / pe_bins.fname(smp_id)
        gt_file = gt_dir / pe_bins.fname(smp_id)

        if not pred_file.exists() or not gt_file.exists():
            nb_no_eval += 1
            nb_matches_df.loc[len(nb_matches_df)] = {
                files.Header.SAMPLE_ID: smp_id,
                files.Header.NB_MATCHES: None,
            }
            continue

        pred_df = pe_bins.to_dataframe(pred_file)
        gt_df = pe_bins.to_dataframe(gt_file)

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


class GTInputs:
    """Inputs for gt command."""

    GROUND_TRUTH_DIR = typer.Argument(
        help="Path to the ground truth directory.",
    )

    SAMPLES_TSV = typer.Argument(
        help="Path to the samples TSV file.",
    )

    NEW_GT_DIR = typer.Argument(
        help="Path to the new ground truths directory.",
    )


@APP.command("gt")
def distinguish_repeats_in_ground_truth(
    gt_dir: Annotated[Path, GTInputs.GROUND_TRUTH_DIR],
    samples_tsv: Annotated[Path, GTInputs.SAMPLES_TSV],
    new_gt_dir: Annotated[Path, GTInputs.NEW_GT_DIR],
) -> None:
    """Distinguish the repeats in the ground truth bins for a list of samples."""
    log.print_title(
        "Distinguish the repeats in the ground truth bins for a list of samples",
    )

    log.print_inputs(
        (
            f"Ground truth directory: {log.fmt_dir(gt_dir)}",
            f"Samples TSV file: {log.fmt_file(samples_tsv)}",
            f"New ground truth directory: {log.fmt_dir(new_gt_dir)}",
        ),
    )

    smp_df = smp_files.to_dataframe(samples_tsv)

    new_gt_dir.mkdir(parents=True, exist_ok=True)

    for smp_id in smp_df[smp_files.Header.SAMPLE_ID]:
        gt_df = pe_bins.to_dataframe(gt_dir / pe_bins.fname(smp_id))

        new_gt_df = main.uniqify_ground_truth(gt_df)

        pe_bins.to_file(new_gt_df, new_gt_dir / pe_bins.fname(smp_id))

    log.print_done(f"Created {log.fmt_dir(new_gt_dir)} directory")
