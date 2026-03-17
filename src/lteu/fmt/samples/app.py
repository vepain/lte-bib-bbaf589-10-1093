"""Formatting module."""

# Due to typer

from pathlib import Path
from typing import Annotated

import pandas as pd
import typer

from lteu import log
from lteu.data.origin import gt as origin_gt
from lteu.samples import files as smp_files

APP = typer.Typer()


class SamplesInputs:
    """Inputs for samples command."""

    XLSX_PATH = typer.Argument(
        help="Path to the predictions.xlsx file.",
    )

    TSV_OUTPUT = typer.Argument(
        help="Path to the output TSV file.",
    )


@APP.command("samples")
def extract_samples_with_complete_hybrid_assembly(
    xlsx_path: Annotated[Path, SamplesInputs.XLSX_PATH],
    tsv_output: Annotated[Path, SamplesInputs.TSV_OUTPUT],
) -> None:
    """Extract samples with complete hybrid assemblies."""
    log.print_title("Extract samples with complete hybrid assemblies")

    log.print_inputs(
        (
            f"Predictions XLSX file: {log.fmt_file(xlsx_path)}",
            f"Output TSV file: {log.fmt_file(tsv_output)}",
        ),
    )

    tsv_output.parent.mkdir(parents=True, exist_ok=True)

    gt_df = origin_gt.to_dataframe(xlsx_path)
    gt_df = gt_df[gt_df[origin_gt.Header.HAS_COMPLETE_HYBRID_ASM]]

    final_smps = pd.DataFrame(
        gt_df[origin_gt.Header.SAMPLE_ID].unique(),
        columns=list(smp_files.HEADER_TYPES.keys()),
    )

    log.print_info(f"{final_smps.size} samples with complete hybrid assemblies")

    smp_files.to_file(final_smps, tsv_output)

    log.print_done(f"Created {log.fmt_file(tsv_output)} file")
