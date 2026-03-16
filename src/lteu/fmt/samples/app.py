"""Formatting module."""

# Due to typer

from pathlib import Path
from typing import Annotated

import pandas as pd
import typer

from lteu import log
from lteu.data import samples as smp_data
from lteu.data.origin import gt as origin_gt

APP = typer.Typer(name="smp", help="Samples formatting.")


class CompleteHybridAsm:
    """Complete hybrid assembly args and opts."""

    class Args:
        """Complete hybrid assembly args."""

        XLSX_PATH = typer.Argument(
            help="Path to the predictions.xlsx file.",
        )

        TSV_OUTPUT = typer.Argument(
            help="Path to the output TSV file.",
        )


@APP.command("complete-hybrid-asm")
def extract_complete_assembly(
    xlsx_path: Annotated[Path, CompleteHybridAsm.Args.XLSX_PATH],
    tsv_output: Annotated[Path, CompleteHybridAsm.Args.TSV_OUTPUT],
) -> None:
    """Extract complete hybrid assemblies."""
    log.print_title("Extract complete hybrid assemblies")

    tsv_output.parent.mkdir(parents=True, exist_ok=True)

    gt_df = origin_gt.to_dataframe(xlsx_path)
    gt_df = gt_df[gt_df[origin_gt.Header.HAS_COMPLETE_HYBRID_ASM]]

    final_smps = pd.Series(
        gt_df[origin_gt.Header.SAMPLE_ID].unique(),
        name=smp_data.Header.SAMPLE_ID,
    )

    log.print_info(f"{final_smps.size} samples with complete hybrid assemblies")

    final_smps.to_csv(
        tsv_output,
        sep="\t",
        index=False,
    )

    log.print_done(f"Created {log.fmt_file(tsv_output)} file")
