"""Experiment initialization."""

from pathlib import Path
from typing import Annotated

import requests
import typer

from lteu import bins, log, tools
from lteu.exp import files as exp_files
from lteu.fmt.plaseval import app as fmt_pe_app
from lteu.fmt.samples import app as fmt_smp_app

APP = typer.Typer()


class Inputs:
    """Inputs for init command."""

    DATA_DIR = typer.Argument(
        help="Path to the data directory.",
    )


@APP.command()
def init(data_dir: Annotated[Path, Inputs.DATA_DIR]) -> None:
    """Initialize the experiments."""
    log.print_title("Initialize the experiments")
    log.print_inputs((f"Data directory: {log.fmt_dir(data_dir)}",))
    log.print_empty_line()

    original_fs = exp_files.Original(data_dir)
    samples_fs = exp_files.Samples(data_dir)
    ground_truths_fs = exp_files.GroundTruths(data_dir)
    binning_fs = exp_files.Binning(data_dir)

    data_dir.mkdir(parents=True, exist_ok=True)
    log.print_done(f"Created {log.fmt_dir(data_dir)} directory")

    predictions_xlsx_url = "https://github.com/broadinstitute/plasmid-detection-benchmark/raw/refs/heads/main/data/predictions.xlsx"

    # Download the URL content to the predictions.xlsx file
    original_fs.predictions_xlsx().parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(predictions_xlsx_url, stream=True, timeout=30)

    if not response.ok:
        log.print_error(f"Failed to download {predictions_xlsx_url}")
        raise typer.Exit(1)

    with original_fs.predictions_xlsx().open(mode="wb") as file:
        for chunk in response.iter_content(chunk_size=10 * 1024):
            file.write(chunk)

    log.print_done(f"Created {log.fmt_file(original_fs.predictions_xlsx())} file")

    log.print_empty_line()
    log.print_title("Format the samples to the PlasEval format")
    log.print_empty_line()

    fmt_smp_app.extract_samples_with_complete_hybrid_assembly(
        xlsx_path=original_fs.predictions_xlsx(),
        tsv_output=samples_fs.complete_hybrid_asm_tsv(),
    )

    log.print_empty_line()
    log.print_title("Format the ground truth to the PlasEval format")
    log.print_empty_line()

    for content in bins.Contents:
        fmt_pe_app.gt_to_plaseval(
            xlsx_path=original_fs.predictions_xlsx(),
            output_dir=ground_truths_fs.content_dir(content),
            with_chromosomes=(content == bins.Contents.WITH_CHROMOSOMES),
        )

    log.print_empty_line()
    log.print_title("Format the tools bins to the PlasEval format")
    log.print_empty_line()

    for tool in tools.Binning:
        for content in bins.Contents:
            fmt_pe_app.bins_to_plaseval(
                xlsx_path=original_fs.predictions_xlsx(),
                tool=tool,
                output_dir=binning_fs.tool_dir(content, tool),
                with_chromosomes=(content == bins.Contents.WITH_CHROMOSOMES),
            )

    log.print_empty_line()
    log.print_done("Experiments initialized")
