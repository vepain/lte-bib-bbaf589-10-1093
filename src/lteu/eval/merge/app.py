"""Merge evaluations application."""

from pathlib import Path
from typing import Annotated

import pandas as pd
import typer

from lteu import log
from lteu.data import tools

from . import files

APP = typer.Typer()


class Inputs:
    """Arguments and options for merging evaluations."""

    EVAL_TSV = typer.Option(
        "--eval-tsv",
        "-i",
        help="Path to the evaluation TSV file.",
    )

    TOOL_CODE = typer.Option(
        "--tool-code",
        "-t",
        help="Tool code.",
    )

    MERGE_TSV = typer.Argument(
        help="Path to the merge TSV file.",
    )


@APP.command("merge")
def merge_evaluations(
    eval_tsv_files: Annotated[list[Path], Inputs.EVAL_TSV],
    tool_codes: Annotated[list[tools.Binning], Inputs.TOOL_CODE],
    merge_tsv: Annotated[Path, Inputs.MERGE_TSV],
) -> None:
    """Merge evaluations of completeness and homogeneity."""
    log.print_title("Merge evaluations of completeness and homogeneity")

    log.print_inputs(
        (
            (
                "Evaluation TSV files with codes:\n"
                "* "
                + "\n* ".join(
                    [f"{log.fmt_file(eval_tsv)}" for eval_tsv in eval_tsv_files],
                )
            ),
            (
                "Tool codes:\n"
                "* " + "\n* ".join([f"{tool_code}" for tool_code in tool_codes])
            ),
            f"Merge TSV file: {log.fmt_file(merge_tsv)}",
        ),
    )

    if len(eval_tsv_files) != len(tool_codes):
        log.print_error(
            "The number of evaluation TSV files and tool codes must be the same",
        )
        raise typer.Exit(1)

    merge_df = files.new_dataframe()
    for eval_tsv, tool_code in zip(eval_tsv_files, tool_codes, strict=True):
        eval_df = files.to_dataframe(eval_tsv)
        eval_df[files.Header.TOOL_CODE] = tool_code
        merge_df = pd.concat([merge_df, eval_df], ignore_index=True)

    merge_df.to_csv(merge_tsv, sep="\t", index=False)

    log.print_done(f"Created {log.fmt_file(merge_tsv)} file")
