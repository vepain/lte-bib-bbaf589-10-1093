"""Samples applications."""

from pathlib import Path
from typing import Annotated

import typer

from lteu import log
from lteu.data.plaseval import bins as pe_bins

from . import files as smp_files

APP = typer.Typer(name="smp", help="Samples commands.")


class RepeatsInputs:
    """Repeats command inputs."""

    SAMPLES_TSV = typer.Argument(
        help="Path to the samples TSV file.",
    )

    GROUND_TRUTH_DIR = typer.Argument(
        help="Path to the ground truth directory.",
    )

    FILTERED_SAMPLES_TSV = typer.Argument(
        help="Path to the filtered samples TSV file.",
    )


@APP.command("repeats")
def keep_only_gt_bins_with_repeats(
    samples_tsv: Annotated[Path, RepeatsInputs.SAMPLES_TSV],
    gt_dir: Annotated[Path, RepeatsInputs.GROUND_TRUTH_DIR],
    filtered_samples_tsv: Annotated[Path, RepeatsInputs.FILTERED_SAMPLES_TSV],
) -> None:
    """Keep only the samples with repeats in the ground truth bins."""
    log.print_title("Keep only the samples with repeats in the ground truth bins")

    log.print_inputs(
        (
            f"Samples TSV file: {log.fmt_file(samples_tsv)}",
            f"Ground truth directory: {log.fmt_dir(gt_dir)}",
            f"Filtered samples TSV file: {log.fmt_file(filtered_samples_tsv)}",
        ),
    )

    smp_df = smp_files.to_dataframe(samples_tsv)
    filt_df = smp_files.new_dataframe()

    for smp_id in smp_df[smp_files.Header.SAMPLE_ID]:
        gt_file = gt_dir / pe_bins.fname(smp_id)

        gt_df = pe_bins.to_dataframe(gt_file)

        if len(gt_df) > len(gt_df[pe_bins.Header.CONTIG].unique()):
            filt_df.loc[len(filt_df)] = {smp_files.Header.SAMPLE_ID: smp_id}

    filtered_samples_tsv.parent.mkdir(parents=True, exist_ok=True)

    smp_files.to_file(filt_df, filtered_samples_tsv)

    log.print_done(f"Created {log.fmt_file(filtered_samples_tsv)} file")
